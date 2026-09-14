"""
Grounded Reflexion Loop & Verifiable Self-Correction (Chapter 11)
Validates execution outputs against deterministic assertions and feeds diagnostic traces back.
"""

from __future__ import annotations

from typing import Any, Callable
from pydantic import BaseModel


class VerificationResult(BaseModel):
    passed: bool
    diagnostic: str = ""


class GroundedReflexionLoop:
    """
    Evaluator-Optimizer runtime that drives iterative candidate repair
    until assertions pass or the retry budget is exhausted.
    """

    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts

    def run(
        self,
        generator: Callable[[str], str],
        verifier: Callable[[str], VerificationResult],
        initial_prompt: str,
    ) -> tuple[str, bool]:
        current_prompt = initial_prompt
        last_output = ""

        for attempt in range(1, self.max_attempts + 1):
            last_output = generator(current_prompt)
            result = verifier(last_output)
            if result.passed:
                return last_output, True

            # Synthesize diagnostic feedback for next turn
            current_prompt = (
                f"{initial_prompt}\n\n"
                f"[ATTEMPT {attempt} FAILED VERIFICATION]\n"
                f"Previous Candidate: {last_output}\n"
                f"Diagnostic Error: {result.diagnostic}\n"
                "Fix the precise invariant violation above."
            )

        return last_output, False
