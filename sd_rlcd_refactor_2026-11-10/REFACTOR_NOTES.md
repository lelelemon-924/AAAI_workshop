# SD-RLCD manuscript refactor package

Prepared from the publicly readable `main`-branch README, `paper/sd_rlcd.tex`, and `paper/sd_rlcd.bib` on 2026-11-10.

## What this refactor changes

1. Reframes Style-CalibBench as a decision-native evaluation protocol adapted from RM-Bench, not a wholly new dataset.
2. Renames the single concise-correct vs. markdown-wrong comparison to **Extreme-Corner Accuracy (ECA)**.
3. Explicitly distinguishes ECA from standard RM-Bench Hard Accuracy.
4. Rewrites the method section to state the mathematical consequence of Stage-B freezing:
   - `theta_B = theta_A`
   - `phi_c,B = phi_c,A`
   - `p_c^B(x,r) = p_c^A(x,r)` (up to deterministic inference/numerical details)
5. Removes the unsupported claim that the frozen Stage-B style objective causes the content-side gain or that the frozen model is necessarily a Pareto knee.
6. Preserves the point estimates already present in the public manuscript, but changes the interpretation to descriptive rather than causal.
7. Adds explicit submission-blocking validation items: Stage-A-only control, official RM-Bench metrics, prompt-clustered confidence intervals, selective-risk protocol, style-label documentation, semantic-preservation audit, domain counts, and licensing review.

## Important status

This is a **conservative manuscript refactor**, not a verified camera-ready paper. The public README lists manuscript files and figures; the experiment code, run logs, split manifest, and raw outputs were not available for inspection in this pass. Therefore, the reported numerical values have been transcribed from the current manuscript and have not been independently reproduced.

Do not submit until:
- every number is regenerated from logged runs;
- the Stage-A-only control is added;
- the ECA/standard RM-Bench metric distinction is reflected in all tables and figures;
- figure PDFs are checked and updated (the refactored TeX omits the old figures because their visual content could not be inspected here);
- the revised source compiles with the exact AAAI-27 author kit.

## Recommended method redesign (not claimed as implemented)

If the paper is to remain a methods paper, the current frozen auxiliary-head design is insufficient to support a claim that style training improves content robustness. A more defensible candidate is:

\[
L_{\mathrm{pair}} =
\mathbb{E}\left[
\max\{0, m - (z_c(x,r^+_{s^+}) - z_c(x,r^-_{s^-}))\}
\right]
\]

\[
L_{\mathrm{inv}} =
\mathbb{E}\left[
(p_c(x,r_{y,s})-p_c(x,r_{y,s'}))^2
\right]
\]

\[
\min_{\theta,\phi_c}\quad
L_{\mathrm{pair}}+\alpha L_{\mathrm{inv}}
\quad\text{s.t.}\quad
L_c \leq L_c^{\mathrm{base}}+\epsilon .
\]

A primal-dual implementation can optimize

\[
\min_{\theta,\phi_c}\max_{\lambda\geq 0}
L_{\mathrm{pair}}+\alpha L_{\mathrm{inv}}
+\lambda(L_c-L_c^{\mathrm{base}}-\epsilon).
\]

This lets the counterfactual robustness objective update the content pathway while penalizing violations of a content-loss budget. It is only a proposal: the paper must not describe it as implemented or report results for it until code and experiments exist. The calibration split must not be reused to tune against the final test set.

## Files

- `paper/sd_rlcd.tex`: replacement manuscript source.
- `NEXT_EXPERIMENTS.md`: prioritized experiment plan.
- `UPLOAD_TO_GITHUB.md`: local commands to apply, compile, commit, and push.
