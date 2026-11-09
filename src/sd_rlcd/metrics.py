from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import numpy as np


@dataclass
class PredRow:
    pair_id: str
    style_id: str
    y_content: int
    p_content: float
    p_style: float | None = None


def accuracy(rows: list[PredRow], threshold: float = 0.5) -> float:
    if not rows:
        return float("nan")
    correct = sum(int((r.p_content >= threshold) == bool(r.y_content)) for r in rows)
    return correct / len(rows)


def brier(rows: list[PredRow]) -> float:
    if not rows:
        return float("nan")
    return float(np.mean([(r.p_content - r.y_content) ** 2 for r in rows]))


def ece(rows: list[PredRow], n_bins: int = 15) -> float:
    if not rows:
        return float("nan")
    ps = np.array([r.p_content for r in rows], dtype=float)
    ys = np.array([r.y_content for r in rows], dtype=float)
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    total = 0.0
    for i in range(n_bins):
        lo, hi = bins[i], bins[i + 1]
        mask = (ps >= lo) & (ps < hi if i < n_bins - 1 else ps <= hi)
        if not np.any(mask):
            continue
        conf = float(ps[mask].mean())
        acc = float(ys[mask].mean())
        total += (mask.sum() / len(ps)) * abs(acc - conf)
    return float(total)


def style_conditional_ece(rows: list[PredRow], n_bins: int = 15) -> dict[str, float]:
    by_style: dict[str, list[PredRow]] = defaultdict(list)
    for r in rows:
        by_style[r.style_id].append(r)
    return {s: ece(rs, n_bins=n_bins) for s, rs in sorted(by_style.items())}


def hard_accuracy(rows: list[PredRow]) -> float:
    """Fraction of pair_ids where p(chosen,concise) > p(rejected,markdown).

    Expects both cells present; skips incomplete pairs.
    """
    by_pair: dict[str, dict[tuple[int, str], float]] = defaultdict(dict)
    for r in rows:
        by_pair[r.pair_id][(r.y_content, r.style_id)] = r.p_content

    wins = 0
    total = 0
    for cells in by_pair.values():
        a = cells.get((1, "concise"))
        b = cells.get((0, "markdown"))
        if a is None or b is None:
            continue
        total += 1
        wins += int(a > b)
    return wins / total if total else float("nan")


def style_flip_rate(rows: list[PredRow], threshold: float = 0.5) -> float:
    """How often content decision flips across styles for the same (pair, content)."""
    by_key: dict[tuple[str, int], list[int]] = defaultdict(list)
    for r in rows:
        by_key[(r.pair_id, r.y_content)].append(int(r.p_content >= threshold))
    flips = 0
    total = 0
    for preds in by_key.values():
        if len(preds) < 2:
            continue
        total += 1
        flips += int(len(set(preds)) > 1)
    return flips / total if total else float("nan")


def confidence_inflation(rows: list[PredRow]) -> float:
    """E[p|wrong,markdown] - E[p|wrong,concise]."""
    md = [r.p_content for r in rows if r.y_content == 0 and r.style_id == "markdown"]
    cn = [r.p_content for r in rows if r.y_content == 0 and r.style_id == "concise"]
    if not md or not cn:
        return float("nan")
    return float(np.mean(md) - np.mean(cn))


def coverage_at_error(rows: list[PredRow], max_error: float = 0.05) -> float:
    """Highest coverage with empirical error <= max_error when accepting top-p by confidence."""
    if not rows:
        return float("nan")
    order = sorted(rows, key=lambda r: r.p_content, reverse=True)
    best = 0.0
    correct = 0
    for k, r in enumerate(order, start=1):
        correct += int(r.y_content == 1)
        err_rate = 1.0 - (correct / k)
        if err_rate <= max_error:
            best = k / len(rows)
    return best


def summarize(rows: list[PredRow]) -> dict[str, float | dict[str, float]]:
    return {
        "n": len(rows),
        "accuracy": accuracy(rows),
        "brier": brier(rows),
        "ece": ece(rows),
        "ece_by_style": style_conditional_ece(rows),
        "hard_accuracy": hard_accuracy(rows),
        "style_flip_rate": style_flip_rate(rows),
        "confidence_inflation": confidence_inflation(rows),
        "coverage_at_5pct_error": coverage_at_error(rows, 0.05),
        "coverage_at_10pct_error": coverage_at_error(rows, 0.10),
    }
