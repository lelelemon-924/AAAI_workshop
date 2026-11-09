from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

StyleId = Literal["concise", "detailed", "markdown"]
Split = Literal["train", "cal", "test"]


STYLE_LEVELS: dict[StyleId, dict[StyleId, int]] = {
    "concise": {"concise": 5, "detailed": 2, "markdown": 1},
    "detailed": {"concise": 2, "detailed": 5, "markdown": 3},
    "markdown": {"concise": 1, "detailed": 3, "markdown": 5},
}


class BenchItem(BaseModel):
    id: str
    source: str
    split: Split
    domain: str
    prompt: str
    response: str
    content_label: int = Field(ge=0, le=1)
    style_id: StyleId
    style_level: dict[str, int]
    pair_id: str
    meta: dict[str, Any] = Field(default_factory=dict)


class TypedQuestion(BaseModel):
    id: str
    type: Literal["noul", "choice", "score"]
    text: str
    options: list[str] | None = None
    levels: list[int] | None = None


class DecisionRequest(BaseModel):
    state: dict[str, str]
    questions: list[TypedQuestion]
