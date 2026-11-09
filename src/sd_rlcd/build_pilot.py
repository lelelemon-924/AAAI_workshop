from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

from .schema import STYLE_LEVELS, BenchItem, StyleId

STYLES: list[StyleId] = ["concise", "detailed", "markdown"]
SEED = 20261109


def _pair_hash(prompt: str) -> str:
    return hashlib.sha1(prompt.encode("utf-8")).hexdigest()[:8]


def assign_split(prompt: str, train: float = 0.7, cal: float = 0.1) -> str:
    """Deterministic split from prompt hash."""
    h = int(hashlib.sha1(f"{SEED}:{prompt}".encode()).hexdigest()[:8], 16)
    u = (h % 10_000) / 10_000.0
    if u < train:
        return "train"
    if u < train + cal:
        return "cal"
    return "test"


def synthetic_pilot(n_prompts: int = 60) -> list[BenchItem]:
    """Offline pilot grid so metrics/CI work without HuggingFace."""
    rng = random.Random(SEED)
    domains = ["chat", "code", "math", "safety-refuse", "safety-response"]
    items: list[BenchItem] = []
    for i in range(n_prompts):
        domain = domains[i % len(domains)]
        prompt = f"[synthetic-{domain}] Explain concept #{i}: why does method X work?"
        pair_id = f"synth-{_pair_hash(prompt)}"
        split = assign_split(prompt)
        chosen_base = f"Method X works because of property P{i}."
        rejected_base = f"Method X works because of unrelated property Q{i}."
        styled = {
            "concise": lambda t: t,
            "detailed": lambda t: t + " " + "Additionally, context elaborates the same claim without new facts. " * 2,
            "markdown": lambda t: f"## Answer\n\n- **Claim:** {t}\n- **Note:** formatted only.",
        }
        for style in STYLES:
            for label, base in ((1, chosen_base), (0, rejected_base)):
                response = styled[style](base)
                # tiny noise so strings differ across prompts
                response = response + (f" [{rng.randint(0, 999)}]" if style == "concise" else "")
                items.append(
                    BenchItem(
                        id=f"{pair_id}-{'chosen' if label else 'rejected'}-{style}",
                        source="synthetic",
                        split=split,  # type: ignore[arg-type]
                        domain=domain,
                        prompt=prompt,
                        response=response,
                        content_label=label,
                        style_id=style,
                        style_level=dict(STYLE_LEVELS[style]),
                        pair_id=pair_id,
                        meta={"synthetic_index": i},
                    )
                )
    return items


def from_rmbench_row(row: dict, index: int) -> list[BenchItem]:
    prompt = row["prompt"]
    domain = row.get("domain", "unknown")
    pair_id = f"rmbench-{_pair_hash(prompt)}"
    split = assign_split(prompt)
    items: list[BenchItem] = []
    for style_idx, style in enumerate(STYLES):
        for label, key in ((1, "chosen"), (0, "rejected")):
            response = row[key][style_idx]
            items.append(
                BenchItem(
                    id=f"{pair_id}-{key}-{style}",
                    source="rmbench",
                    split=split,  # type: ignore[arg-type]
                    domain=domain,
                    prompt=prompt,
                    response=response,
                    content_label=label,
                    style_id=style,
                    style_level=dict(STYLE_LEVELS[style]),
                    pair_id=pair_id,
                    meta={"rmbench_index": index},
                )
            )
    return items


def try_load_rmbench(max_prompts: int = 300) -> list[BenchItem] | None:
    try:
        from datasets import load_dataset  # type: ignore
    except ImportError:
        return None
    try:
        ds = load_dataset("THU-KEG/RM-Bench", split="train")
    except Exception:
        return None

    # Stratify by domain so pilot is not chat-only (HF order is domain-sorted).
    by_domain: dict[str, list[tuple[int, dict]]] = {}
    for i, row in enumerate(ds):
        row_d = dict(row)
        by_domain.setdefault(str(row_d.get("domain", "unknown")), []).append((i, row_d))

    rng = random.Random(SEED)
    domains = sorted(by_domain)
    per = max(1, max_prompts // max(len(domains), 1))
    picked: list[tuple[int, dict]] = []
    picked_ids: set[int] = set()
    for d in domains:
        pool = by_domain[d][:]
        rng.shuffle(pool)
        for idx_row in pool[:per]:
            if len(picked) >= max_prompts:
                break
            picked.append(idx_row)
            picked_ids.add(idx_row[0])
    if len(picked) < max_prompts:
        leftover = [x for d in domains for x in by_domain[d] if x[0] not in picked_ids]
        rng.shuffle(leftover)
        for idx_row in leftover[: max_prompts - len(picked)]:
            picked.append(idx_row)

    items: list[BenchItem] = []
    for i, row in picked:
        items.extend(from_rmbench_row(row, i))
    return items


def write_jsonl(items: list[BenchItem], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(item.model_dump_json() + "\n")


def build_pilot(out_dir: Path, max_prompts: int = 300, force_synthetic: bool = False) -> dict:
    if force_synthetic:
        items = synthetic_pilot(n_prompts=min(60, max_prompts))
        source = "synthetic"
    else:
        items = try_load_rmbench(max_prompts=max_prompts)
        if items is None:
            items = synthetic_pilot(n_prompts=min(60, max_prompts))
            source = "synthetic_fallback"
        else:
            source = "rmbench"

    out_dir = Path(out_dir)
    write_jsonl(items, out_dir / "all.jsonl")
    for split in ("train", "cal", "test"):
        subset = [x for x in items if x.split == split]
        write_jsonl(subset, out_dir / f"{split}.jsonl")

    summary = {
        "source": source,
        "n_items": len(items),
        "n_pairs": len({x.pair_id for x in items}),
        "splits": {s: sum(1 for x in items if x.split == s) for s in ("train", "cal", "test")},
        "domains": sorted({x.domain for x in items}),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
