"""
Adaptive Cognitive Router (Chapter 2 Reference Blueprint)
Dynamically assigns model inference tiers based on budget, complexity,
and latency profiles under modern inference scaling laws.
"""

from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class ModelTier(str, Enum):
    FRONTIER_REASONING = "frontier_reasoning"  # Claude Mythos, GPT-6 Astra, DeepSeek-R1
    FAST_ORCHESTRATOR = "fast_orchestrator"    # Claude 5.1 Fable, Gemini 3.8 Flash, Qwen 3.8 Max
    SPECIALIZED_SLM = "specialized_slm"        # Mistral Large 3, GLM-5.3, CodeGLM


class TaskProfile(BaseModel):
    task_id: str
    complexity_score: float = Field(..., ge=0.0, le=1.0, description="0.0 simple to 1.0 hyper-complex")
    requires_formal_proof: bool = False
    context_tokens: int = Field(default=2048, ge=0)
    latency_budget_sec: float = Field(default=10.0, gt=0.0)


class RoutingDecision(BaseModel):
    tier: ModelTier
    recommended_model: str
    rationale: str
    test_time_compute_budget: int  # Additional reasoning tokens allotted


class AdaptiveCognitiveRouter:
    """
    Budget-aware inference engine routing tasks to optimal compute substrates.
    Prevents deploying high-cost frontier reasoning models for deterministic tasks.
    """

    def route(self, profile: TaskProfile) -> RoutingDecision:
        if profile.requires_formal_proof or profile.complexity_score > 0.8:
            return RoutingDecision(
                tier=ModelTier.FRONTIER_REASONING,
                recommended_model="anthropic/claude-5-mythos",
                rationale="Formal proof or high cognitive complexity mandates test-time reasoning tree search",
                test_time_compute_budget=4096,
            )

        if profile.context_tokens > 64000 or profile.complexity_score > 0.4:
            return RoutingDecision(
                tier=ModelTier.FAST_ORCHESTRATOR,
                recommended_model="google/gemini-3.8-flash",
                rationale="High token throughput and long-context working memory with sub-second latency",
                test_time_compute_budget=512,
            )

        return RoutingDecision(
            tier=ModelTier.SPECIALIZED_SLM,
            recommended_model="deepseek/deepseek-v4-pro",
            rationale="Low-complexity task optimized for fast local or edge inference efficiency",
            test_time_compute_budget=0,
        )
