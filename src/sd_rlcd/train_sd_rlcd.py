"""SD-RLCD training stub.

Workshop path (implement by 11-14):
1. Load BenchItem JSONL (train/cal).
2. Tokenize content Noul as letter options A/B (yes/no).
3. Stage A: minimize Brier/log on content softmax over {A,B}.
4. Stage B: minimize CE/Brier on style Score tokens {1..5}.
5. Save LoRA; evaluate with metrics.summarize.

This module intentionally has no heavy imports so `pip install -e .` stays light.
Install extras: `pip install -e ".[train]"`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SDRLCDConfig:
    model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"
    lora_r: int = 16
    lr: float = 2e-5
    max_len: int = 1024
    stage_a_epochs: int = 2
    stage_b_epochs: int = 1
    seed: int = 20261109


def proper_brier(prob_correct: float, y: int) -> float:
    """Scalar Brier for binary content head; training loop should use vector form."""
    return (prob_correct - y) ** 2


def planned_stages(cfg: SDRLCDConfig) -> list[str]:
    return [
        f"load:{cfg.model_name}",
        "stageA:content_proper_score",
        "stageB:style_proper_score",
        "eval:hard_acc+ece_by_style",
    ]
