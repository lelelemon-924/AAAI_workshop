# Reverse Timeline → 2026-11-20 AoE

Today assumed: **2026-11-09**. Buffer: submit by **11-19 20:00 CST**.

## Critical path

```
Protocol ✓ → Pilot data → Dummy metrics CI → Baselines → SD-RLCD → Tables/Figs → Draft → Polish → Submit
```

| Date | Owner focus | Exit criteria |
|---|---|---|
| **11-09 (today)** | Spec + scaffold + outline | Repo builds; `eval-dummy` green |
| **11-10** | Download RM-Bench; implement builder | `data/pilot` JSONL ≥ 300 prompts × 6 |
| **11-11** | Metrics + letter-readout eval path | Table stub on frozen LM (even 0.5B) |
| **11-12** | `rm_scalar` + `letter_sft` content-only | Hard Acc numbers exist |
| **11-13** | Single-head RLCD (Brier) | Selective curve v0 |
| **11-14–15** | SD-RLCD dual head | Main Table 2 complete |
| **11-16** | Ablations + figures | Fig 1–3 PNGs frozen |
| **11-17** | Paper draft v1 (all sections) | 4-page PDF compiles |
| **11-18** | Internal review / cut fluff | Claims match tables |
| **11-19** | Submit RobustAI; optional SC4AI | Confirmation emails saved |
| **11-20** | Hard deadline AoE | — |

## Parallel tracks (if bandwidth)

- **Track B:** Flattery length/sycophancy subset (nice-to-have for §3).
- **Track C:** ARR long-paper skeleton (intro+related) — do **after** workshop PDF exists.
- **Track D:** Jev API probe only if key available; otherwise footnote “closed API”.

## Decision locks (do not reopen after date)

| Decision | Lock by | Default |
|---|---|---|
| Base model | 11-11 | Qwen2.5-1.5B-Instruct |
| Primary workshop | 11-12 | RobustAI |
| Page format | 11-12 | AAAI short 4p |
| Whether to dual-submit SC4AI | 11-18 | Yes only if PDF already done |

## Risk → mitigation

| Risk | Mitigation |
|---|---|
| GPU / training slow | Fall back to SFT dual-head CE; still claim decoupling via heads |
| RM-Bench download blocked | Ship synthetic mini-grid (50 prompts) + state limitation |
| Hard Acc noisy | Bootstrap CIs; report prompt-level majority |
| Scope creep (vision, agents) | Explicitly out of workshop scope |

## Daily standup questions

1. Did Hard Acc / ECE numbers move today?
2. Is the paper claim still supported by the latest table?
3. What can be cut without killing the story?
