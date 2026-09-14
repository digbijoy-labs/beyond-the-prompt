"""
Compound AI Systems & Autonomous Software Engineering Flywheels (Chapter 24)
DSPy-style prompt compilation, continuous reflection, and trajectory optimization.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class TrajectoryExample(BaseModel):
    task: str
    successful_reasoning: str
    score: float


class CompoundFlywheel:
    """
    Self-improving runtime synthesizer curating top-scoring traces into dynamic few-shot exemplars.
    """

    def __init__(self, exemplar_capacity: int = 5):
        self.exemplar_capacity = exemplar_capacity
        self.exemplars: list[TrajectoryExample] = []

    def submit_trace(self, example: TrajectoryExample) -> None:
        self.exemplars.append(example)
        # Keep highest-scoring trajectories
        self.exemplars.sort(key=lambda x: x.score, reverse=True)
        self.exemplars = self.exemplars[:self.exemplar_capacity]

    def render_few_shot_block(self) -> str:
        if not self.exemplars:
            return ""
        blocks = ["<curated_exemplars>"]
        for idx, ex in enumerate(self.exemplars, 1):
            blocks.append(f"Example {idx}:")
            blocks.append(f"Task: {ex.task}")
            blocks.append(f"Optimal Trajectory: {ex.successful_reasoning}\n")
        blocks.append("</curated_exemplars>")
        return "\n".join(blocks)
