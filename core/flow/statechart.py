"""
Flow Engineering & Deterministic Statechart DAG (Chapter 9)
Replaces brittle prompt loops with explicit statechart execution graphs.
"""

from __future__ import annotations

from typing import Callable
from pydantic import BaseModel


class StatechartNode(BaseModel):
    name: str
    is_terminal: bool = False


class StatechartDAG:
    """
    Directed cyclic/acyclic statechart engine with explicit transition guards.
    """

    def __init__(self, initial_state: str):
        self.current_state = initial_state
        self.transitions: dict[str, dict[str, Callable[[dict], bool]]] = {}
        self.nodes: dict[str, StatechartNode] = {}

    def add_state(self, name: str, is_terminal: bool = False) -> None:
        self.nodes[name] = StatechartNode(name=name, is_terminal=is_terminal)
        if name not in self.transitions:
            self.transitions[name] = {}

    def add_transition(self, src: str, dst: str, guard: Callable[[dict], bool]) -> None:
        self.transitions[src][dst] = guard

    def step(self, context: dict) -> str:
        if self.nodes[self.current_state].is_terminal:
            return self.current_state

        available = self.transitions.get(self.current_state, {})
        for next_state, guard_fn in available.items():
            if guard_fn(context):
                self.current_state = next_state
                return self.current_state

        raise RuntimeError(f"State transition deadlock at state '{self.current_state}'")
