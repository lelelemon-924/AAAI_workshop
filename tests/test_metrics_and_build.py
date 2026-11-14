from pathlib import Path

from sd_rlcd.build_pilot import build_pilot, synthetic_pilot
from sd_rlcd.metrics import PredRow, hard_accuracy, summarize
from sd_rlcd.templates import to_decision_request


def test_synthetic_grid_complete():
    items = synthetic_pilot(n_prompts=10)
    assert len(items) == 10 * 6
    pairs = {i.pair_id for i in items}
    for pid in pairs:
        cells = [x for x in items if x.pair_id == pid]
        assert len(cells) == 6


def test_build_pilot_writes(tmp_path: Path):
    summary = build_pilot(tmp_path, max_prompts=20, force_synthetic=True)
    assert (tmp_path / "all.jsonl").exists()
    assert summary["n_pairs"] == 20
    assert summary["source"] == "synthetic"


def test_hard_accuracy_and_dummy_bias():
    rows = [
        PredRow("p1", "concise", 1, 0.60),
        PredRow("p1", "markdown", 0, 0.80),  # style beats content
        PredRow("p1", "concise", 0, 0.40),
        PredRow("p2", "concise", 1, 0.90),
        PredRow("p2", "markdown", 0, 0.20),
        PredRow("p2", "concise", 0, 0.10),
    ]
    assert hard_accuracy(rows) == 0.5
    s = summarize(rows)
    assert s["confidence_inflation"] > 0


def test_decision_request_shape():
    item = synthetic_pilot(1)[0]
    req = to_decision_request(item)
    assert req.questions[0].type == "noul"
    assert req.questions[1].type == "score"
