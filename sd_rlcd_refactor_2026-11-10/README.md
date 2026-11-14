# AAAI-27 Workshop Paper

Manuscript sources for the AAAI-27 workshop submission.

**Current manuscript title**

*Calibration Is Not Style Robustness: A Decision-Native Audit of Style-Conditional Reliability*

## Repository contents

- `paper/sd_rlcd.tex` — main LaTeX source.
- `paper/sd_rlcd.bib` — bibliography (retained from the existing repository).
- `paper/sd_rlcd.pdf` — compiled manuscript; regenerate after changing the source.
- `paper/aaai2027.sty` / `paper/aaai2027.bst` — AAAI-27 style files.
- `paper/figures/` — figures. Check and regenerate these against the current manuscript; the refactored TeX intentionally does not include the previous figures because their visual contents were not available for verification.
- `NEXT_EXPERIMENTS.md` — prioritized validation and experiment plan.
- `REFACTOR_NOTES.md` — scope, interpretation, and validation caveats.

## Build

From `paper/`, run:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error sd_rlcd.tex
```

The manuscript uses the AAAI-27 author kit. Confirm that the exact official style files are present before compiling or submitting.

## Important scientific-status note

The current two-stage description freezes the shared trunk and content head during Stage B. Therefore, Stage B cannot change the content probabilities. A matched Stage-A-only control is required before attributing any content-side improvement to the style-head objective.

The single concise-correct versus markdown-incorrect comparison is called **Extreme-Corner Accuracy (ECA)** in the manuscript. It must not be confused with the standard RM-Bench Hard metric.

The reported numeric values must be regenerated from experiment logs before submission. See `NEXT_EXPERIMENTS.md`.
