"""
Flow Engineering & Deterministic Statechart DAG (Chapter 9)
Replaces brittle prompt loops with explicit statechart execution graphs
and monotonic step bounding to prevent infinite recovery cycles.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable
from pydantic import BaseModel


class StatechartNode(BaseModel):
    name: str
    is_terminal: bool = False


class StatechartDAG:
    """
    Directed cyclic/acyclic statechart engine with explicit transition guards
    and monotonic step bounding to prevent infinite recovery cycles.
    """

    def __init__(self, initial_state: str, max_steps: int = 25):
        self.current_state = initial_state
        self.max_steps = max_steps
        self.step_count = 0
        self.transitions: dict[str, dict[str, Callable[[dict], bool]]] = {}
        self.nodes: dict[str, StatechartNode] = {}

    def add_state(self, name: str, is_terminal: bool = False) -> None:
        self.nodes[name] = StatechartNode(name=name, is_terminal=is_terminal)
        if name not in self.transitions:
            self.transitions[name] = {}

    def add_transition(self, src: str, dst: str, guard: Callable[[dict], bool]) -> None:
        self.transitions[src][dst] = guard

    def step(self, context: dict) -> str:
        if self.nodes.get(self.current_state, StatechartNode(name=self.current_state)).is_terminal:
            return self.current_state

        self.step_count += 1
        if self.step_count >= self.max_steps:
            for name, node in self.nodes.items():
                if node.is_terminal:
                    self.current_state = name
                    return self.current_state
            self.current_state = "TERMINAL"
            return self.current_state

        available = self.transitions.get(self.current_state, {})
        for next_state, guard_fn in available.items():
            if guard_fn(context):
                self.current_state = next_state
                return self.current_state

        raise RuntimeError(f"State transition deadlock at state '{self.current_state}'")


# ---------------------------------------------------------------------------
# Chapter 9 Reference Implementation Kernel: StateChartEngine
# ---------------------------------------------------------------------------

class InvalidStateError(Exception):
    pass


@dataclass
class MachineState:
    current: str
    step_count: int
    context: dict[str, Any]


class StateChartEngine:
    """
    Guarded statechart execution engine enforcing monotonic step increments
    and global step ceilings to prevent unbounded recovery cycles.
    """

    def __init__(
        self,
        states: set[str],
        transitions: dict[str, dict[str, Any]],
        initial: str,
        max_steps: int = 25,
    ):
        self.states = states
        self.transitions = transitions
        self.initial = initial
        self.max_steps = max_steps

    def step(self, state: MachineState) -> MachineState:
        if state.current not in self.states:
            raise InvalidStateError(f"Unknown: {state.current}")
        state.step_count += 1
        if state.step_count >= self.max_steps:
            state.current = "TERMINAL"
            return state
        edges = self.transitions.get(state.current, {})
        for tgt, guard in edges.items():
            if guard(state.context):
                state.current = tgt
                return state
        return state
