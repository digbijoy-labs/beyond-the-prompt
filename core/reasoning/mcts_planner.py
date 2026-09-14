"""
Test-Time Compute (TTC) Engine & MCTS Candidate Search (Chapter 10)
Explores candidate action trees scored by Process Reward Models (PRMs).
"""

from __future__ import annotations

import math
from typing import Callable
from pydantic import BaseModel, Field


class PlanNode(BaseModel):
    action: str
    visits: int = 0
    total_score: float = 0.0
    children: list[PlanNode] = Field(default_factory=list)

    @property
    def uct_score(self) -> float:
        if self.visits == 0:
            return float("inf")
        # Exploration-exploitation trade-off
        return (self.total_score / self.visits) + 1.414 * math.sqrt(math.log(self.visits + 1) / self.visits)


class MCTSPlanner:
    """
    Budget-aware rollout planner performing tree-search over reasoning candidates.
    """

    def __init__(self, reward_model: Callable[[str], float]):
        self.reward_model = reward_model

    def search(self, initial_state: str, candidate_actions: list[str], rollouts: int = 10) -> str:
        root = PlanNode(action=initial_state)
        root.children = [PlanNode(action=act) for act in candidate_actions]

        for _ in range(rollouts):
            # Selection
            best_child = max(root.children, key=lambda n: n.uct_score)
            # Rollout & PRM evaluation
            reward = self.reward_model(best_child.action)
            # Backpropagation
            best_child.visits += 1
            best_child.total_score += reward
            root.visits += 1

        # Pick highest average reward candidate
        best_overall = max(root.children, key=lambda n: (n.total_score / max(1, n.visits)))
        return best_overall.action
