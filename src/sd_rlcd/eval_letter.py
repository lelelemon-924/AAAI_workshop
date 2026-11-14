"""Letter-logit content readout evaluator (optional `[train]` extras).

Usage:
  pip install -e ".[train]"
  python -m sd_rlcd.eval_letter --data data/pilot_rm/test.jsonl --model Qwen/Qwen2.5-0.5B-Instruct --limit 48
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .metrics import PredRow, summarize
from .schema import BenchItem
from .templates import content_noul_text


def _load_items(path: Path, limit: int | None) -> list[BenchItem]:
    items: list[BenchItem] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            items.append(BenchItem.model_validate_json(line))
            if limit is not None and len(items) >= limit:
                break
    return items


def score_letter_readout(model_name: str, items: list[BenchItem], device: str = "cpu") -> list[PredRow]:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    model.eval()

    # Prefer single-token yes/no if available; else A/B.
    yes_id = tok.encode(" yes", add_special_tokens=False)[-1]
    no_id = tok.encode(" no", add_special_tokens=False)[-1]

    rows: list[PredRow] = []
    for it in items:
        prompt = content_noul_text(it) + "\nAnswer:"
        enc = tok(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            logits = model(**enc).logits[0, -1]
        pair = torch.stack([logits[yes_id], logits[no_id]])
        probs = torch.softmax(pair, dim=0)
        p_yes = float(probs[0].item())
        rows.append(
            PredRow(
                pair_id=it.pair_id,
                style_id=it.style_id,
                y_content=it.content_label,
                p_content=p_yes,
            )
        )
    return rows


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True)
    p.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    p.add_argument("--device", default="cpu")
    p.add_argument("--limit", type=int, default=48)
    p.add_argument("--out", default="outputs/letter_readout.json")
    args = p.parse_args(argv)

    items = _load_items(Path(args.data), args.limit)
    rows = score_letter_readout(args.model, items, device=args.device)
    summary = summarize(rows)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
