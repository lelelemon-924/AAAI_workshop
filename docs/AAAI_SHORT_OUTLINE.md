# AAAI-27 Workshop Short Paper Outline (≤4 pages + refs)

**Working title:**  
*Calibration Is Not Style-Robustness: Style-Decoupled RLCD for Typed Decisions*

**Primary target:** Multi-Objective and Multi-Task Optimization for Robust AI (RobustAI)  
**Backup:** SC4AI’27 / Trust4RSI-Agent  
**Deadline:** 2026-11-20 AoE · Non-archival preferred

---

## Contribution bullets (paste into abstract/intro)

1. **Problem.** We show that Jev-style typed decision models and letter-logit readouts can be *calibrated on average* yet still assign systematically higher confidence to stylistically decorated *incorrect* answers—so calibration alone does not imply style-robust automation.
2. **Benchmark.** We introduce **Style-CalibBench**, which crosses content correctness with controlled style (concise / detailed / markdown, plus Flattery factors) and exposes decision-native Noul/Score questions plus Hard cross-style probes.
3. **Method.** We propose **SD-RLCD**: train separate content and style heads with strictly proper scoring rules, and use only the content probability for selective accept/defer.
4. **Evidence.** On Style-CalibBench, SD-RLCD improves Hard accuracy and reduces style-conditional ECE / style-flip relative to single-head RLCD and scalar reward models, without sacrificing overall content AUROC.

---

## Abstract (draft ~150 words)

Reward models used in RLHF are known to prefer length, markdown, and other stylistic cues over substance. System One decision models trained for calibrated typed outputs (RLCD / Jev-style readouts) promise probabilities that software can trust, but it is unclear whether those probabilities remain meaningful under style variation. We construct Style-CalibBench by crossing correct/incorrect content with controlled styles from RM-Bench-style grids, and evaluate models through typed Noul/Score questions. We find that single-head calibrated decision models still exhibit confidence inflation on decorated wrong answers and fail Hard cross-style comparisons. We propose Style-Decoupled RLCD (SD-RLCD), which optimizes separate content and style distributions with proper scoring rules and gates deployment decisions on content confidence alone. Experiments on small open models show improved Hard accuracy and lower style-entanglement while preserving selective-prediction gains of calibration-aware training. Our results argue that automation-facing alignment should treat style as a second objective, not a side effect of preference optimization.

---

## Section plan (page budget)

### §1 Introduction (0.6–0.7p)
- Hook: automation needs *probabilities*, not preferred prose (Jev / RLCD framing).
- Gap: RM style bias literature vs RLCD literature do not meet.
- Teaser Figure 1: reliability curves split by style; Hard pair cartoon.
- Contributions list (4 bullets above).

### §2 Background (0.4p)
- RLHF / RM style bias (RM-Bench, Flattery).
- RLCD / typed decisions / proper scoring (TypeSafe; OpenJev-RLCD).
- One sentence: we do **not** claim to reverse-engineer proprietary Jev.

### §3 Style-CalibBench (0.8p)
- Construction from RM-Bench 3×2 grid; optional Flattery axes.
- Typed questions; Hard probe definition.
- Metrics: Acc, Hard Acc, ECE, style-conditional ECE, style-flip, coverage@err.
- Table 1: dataset stats by domain/style.

### §4 SD-RLCD (0.6p)
- Dual typed heads; Stage A/B proper scores; inference policy.
- Eq: Brier on \(u_c\), ordinal proper score / CE on \(u_s\).
- Contrast with scalar RM and single-head RLCD.

### §5 Experiments (1.0–1.2p)
- Setup: model sizes, LoRA, baselines (`rm_scalar`, `letter_readout`, `letter_sft`, `rlcd_single`, `sd_rlcd`).
- **Table 2:** main metrics.
- **Figure 2:** reliability diagrams by style.
- **Figure 3:** selective coverage curves.
- Ablation: shared trunk vs stop-grad; style head on/off at inference.
- Optional: one qualitative failure case (markdown wrong beats concise right).

### §6 Related work (0.3p, or fold into §2 if tight)
- Calibrated RL, RM debiasing (CHARM, SteerRM, Patterning), LLM-as-judge calibration.

### §7 Limitations & conclusion (0.3p)
- Small models; synthetic style transforms; no proprietary Jev API guarantee.
- Takeaway: *calibrated ≠ style-robust*; decouple for automation.

### References (unlimited) · Ethics / AI-use (2–4 sentences)

---

## Figures / tables to produce (priority order)

1. **Fig 1** — Conceptual: content×style grid + Hard arrow.  
2. **Tab 1** — Bench stats.  
3. **Tab 2** — Main results.  
4. **Fig 2** — Style-conditional reliability.  
5. **Fig 3** — Selective prediction.  

---

## Claims we will NOT make (avoid reviewer traps)

- “We open-sourced Jev / rediscovered TypeSafe RLCD.”
- “SD-RLCD beats GPT-class judges everywhere.”
- “Style head improves factual accuracy by itself” (only claim *robustness / selective* gains).

---

## Writing checklist before submit

- [ ] Anonymous PDF, AAAI format
- [ ] 4 pages main (RobustAI short) or check venue page limit
- [ ] Reproducibility: seed, model ID, data hash in appendix/footnote
- [ ] Disclose LLM assistance for rewriting / writing
- [ ] Dual-submit RobustAI + SC4AI only if both allow (prefer one archival conflict-free; both non-archival OK)
