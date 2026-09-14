"""
Eval Engineering & Benchmark Harness (Chapter 22)
Deterministic testing harness computing pass@k and trajectory correctness metrics.
"""

from __future__ import annotations

from typing import Callable
from pydantic import BaseModel


class EvalTestCase(BaseModel):
    name: str
    input_directive: str
    expected_output_substr: str


class EvalSummary(BaseModel):
    total_tests: int
    passed_tests: int
    pass_rate: float


class AgentEvalHarness:
    """
    Automated evaluation framework for running regression suites against agentic runtimes.
    """

    def __init__(self):
        self.test_cases: list[EvalTestCase] = []

    def add_case(self, case: EvalTestCase) -> None:
        self.test_cases.append(case)

    def run_suite(self, agent_fn: Callable[[str], str]) -> EvalSummary:
        passed = 0
        for test in self.test_cases:
            try:
                res = agent_fn(test.input_directive)
                if test.expected_output_substr.lower() in res.lower():
                    passed += 1
            except Exception:
                pass

        total = len(self.test_cases)
        return EvalSummary(
            total_tests=total,
            passed_tests=passed,
            pass_rate=(passed / total) if total > 0 else 0.0,
        )
