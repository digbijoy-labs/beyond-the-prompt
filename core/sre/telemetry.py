"""
Agentic SRE: Telemetry, Observability & Cost Accounting (Chapter 23)
Tracks OpenTelemetry spans, token consumption rates, and unit economics.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any
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


# ---------------------------------------------------------------------------
# Chapter 23 Reference Implementation Kernel: EconomicGovernor
# ---------------------------------------------------------------------------

class BudgetExceededError(Exception):
    pass


@dataclass
class ModelRates:
    in_price: float
    out_price: float


@dataclass
class TelemetrySpan:
    model: str
    cost: float


class EconomicGovernor:
    """
    Financial governor tracking per-turn token expenditures, enforcing hard
    dollar budgets, and computing Cost-Per-Resolved-Task (CPRT) unit economics.
    """

    def __init__(self, rates: dict[str, ModelRates], budget: float):
        self.rates = rates
        self.budget = budget
        self.spans: list[TelemetrySpan] = []
        self.completions: list[dict[str, Any]] = []
        self._last_offset: float = 0.0

    def record_step(self, m: str, tin: int, tout: int) -> float:
        r = self.rates[m]
        cost = (tin * r.in_price + tout * r.out_price) / 1e6
        if sum(s.cost for s in self.spans) + cost > self.budget:
            raise BudgetExceededError("Budget breached")
        self.spans.append(TelemetrySpan(model=m, cost=cost))
        return cost

    def record_completion(self, tid: str, ok: bool) -> None:
        curr = sum(s.cost for s in self.spans)
        self.completions.append({
            "id": tid, "ok": ok, "cost": curr - self._last_offset
        })
        self._last_offset = curr

    def compute_summary_report(self) -> dict[str, float]:
        tot = sum(c["cost"] for c in self.completions)
        res = sum(1 for c in self.completions if c["ok"])
        cprt = tot / max(1, res)
        return {"spend": tot, "ok": res, "cprt": cprt}
