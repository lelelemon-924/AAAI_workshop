from __future__ import annotations

import argparse
import json
from pathlib import Path

from .build_pilot import build_pilot
from .metrics import PredRow, summarize
from .schema import BenchItem
from .templates import to_decision_request


def _load_jsonl(path: Path) -> list[BenchItem]:
    items: list[BenchItem] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(BenchItem.model_validate_json(line))
    return items


def cmd_build_pilot(args: argparse.Namespace) -> None:
    summary = build_pilot(
        Path(args.out),
        max_prompts=args.max_prompts,
        force_synthetic=args.synthetic,
    )
    print(json.dumps(summary, indent=2))


def cmd_export_requests(args: argparse.Namespace) -> None:
    items = _load_jsonl(Path(args.data))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for item in items:
            req = to_decision_request(item, style_target=args.style_target)
            f.write(req.model_dump_json() + "\n")
    print(f"wrote {len(items)} requests -> {out}")


def _style_biased_dummy(p_base: float, style_id: str, y: int) -> float:
    """Toy model: inflated confidence for markdown, especially on wrong answers."""
    boost = {"concise": -0.05, "detailed": 0.02, "markdown": 0.12}[style_id]
    p = p_base + boost + (0.08 if (y == 0 and style_id == "markdown") else 0.0)
    return float(min(0.99, max(0.01, p)))


def cmd_eval_dummy(args: argparse.Namespace) -> None:
    data = Path(args.data)
    path = data / "test.jsonl" if data.is_dir() else data
    items = _load_jsonl(path)
    rows = [
        PredRow(
            pair_id=it.pair_id,
            style_id=it.style_id,
            y_content=it.content_label,
            p_content=_style_biased_dummy(0.55 if it.content_label else 0.45, it.style_id, it.content_label),
            p_style=None,
        )
        for it in items
    ]
    summary = summarize(rows)
    print(json.dumps(summary, indent=2))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="sd-rlcd")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build-pilot", help="Build Style-CalibBench pilot JSONL")
    p_build.add_argument("--out", default="data/pilot")
    p_build.add_argument("--max-prompts", type=int, default=300)
    p_build.add_argument("--synthetic", action="store_true", help="Force synthetic grid")
    p_build.set_defaults(func=cmd_build_pilot)

    p_exp = sub.add_parser("export-requests", help="Export Jev-style decision requests")
    p_exp.add_argument("--data", required=True, help="JSONL of BenchItem")
    p_exp.add_argument("--out", default="data/pilot/requests.jsonl")
    p_exp.add_argument("--style-target", default="markdown")
    p_exp.set_defaults(func=cmd_export_requests)

    p_eval = sub.add_parser("eval-dummy", help="Run metrics on a style-biased dummy scorer")
    p_eval.add_argument("--data", default="data/pilot")
    p_eval.set_defaults(func=cmd_eval_dummy)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
