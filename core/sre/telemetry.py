"""
Agentic SRE: Telemetry, Observability & Cost Accounting (Chapter 23)
Tracks OpenTelemetry spans, token consumption rates, and unit economics.
"""

from __future__ import annotations

import time
from pydantic import BaseModel, Field


class StepSpan(BaseModel):
    span_id: str
    stage: str
    tokens_in: int
    tokens_out: int
    duration_ms: float
    cost_usd: float


class AgentTelemetry:
    """
    Evidence Plane collector tracking execution latency and token economics.
    """

    COST_PER_1K_IN = 0.003
    COST_PER_1K_OUT = 0.015

    def __init__(self):
        self.spans: list[StepSpan] = []

    def record_step(self, span_id: str, stage: str, tokens_in: int, tokens_out: int, duration_ms: float) -> StepSpan:
        cost = (tokens_in / 1000.0 * self.COST_PER_1K_IN) + (tokens_out / 1000.0 * self.COST_PER_1K_OUT)
        span = StepSpan(
            span_id=span_id,
            stage=stage,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            duration_ms=duration_ms,
            cost_usd=round(cost, 6),
        )
        self.spans.append(span)
        return span

    def total_cost(self) -> float:
        return sum(s.cost_usd for s in self.spans)
