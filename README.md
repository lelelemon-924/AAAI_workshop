# SD-RLCD: Style-Decoupled Reinforcement Learning for Calibrated Decisions

Fast-track research package for an AAAI-27 workshop short paper (due **2026-11-20 AoE**), expandable to ACL ARR 2027-01.

**One-liner:** Calibration ≠ style-robustness. Split content correctness and style match into two typed, calibrated decision heads.

## Status

| Milestone | Target | Status |
|---|---|---|
| Style-CalibBench protocol | 2026-11-10 | Done (spec) |
| AAAI short outline | 2026-11-10 | Done |
| Scaffold + metrics | 2026-11-10 | Done |
| Pilot bench (RM-Bench subset) | 2026-11-12 | TODO |
| Dual-head baseline runs | 2026-11-16 | TODO |
| AAAI short draft | 2026-11-18 | TODO |
| Submit RobustAI / SC4AI | 2026-11-20 | TODO |

## Quick start

```bash
cd /Users/zhaoyuesen/Desktop/jev
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m sd_rlcd.cli build-pilot --out data/pilot
python -m sd_rlcd.cli eval-dummy --data data/pilot
```

## Docs

- [Style-CalibBench protocol](docs/STYLE_CALIBBENCH_PROTOCOL.md)
- [AAAI-27 short outline](docs/AAAI_SHORT_OUTLINE.md)
- [Nov 20 reverse timeline](docs/TIMELINE_NOV20.md)
- [AAAI-27 short paper shell](paper/sd_rlcd.tex)

## Target venues (priority)

1. AAAI-27 **RobustAI** workshop (primary)
2. AAAI-27 **SC4AI’27** (backup / parallel short)
3. Expand → ARR 2027-01 → ACL 2027
