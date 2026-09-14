"""
Deterministic Execution Harness (Chapter 1 Reference Blueprint)
Enforces the 5-Plane Boundary: isolates tool executions, guards against
oscillation loops, and trips circuit breakers on repeated failures.
"""

from __future__ import annotations

import asyncio
import hashlib
import inspect
from enum import Enum
from typing import Any, Callable
from pydantic import BaseModel, Field


class Stage(str, Enum):
    INTERPRET = "interpret"
    PLAN = "plan"
    ACT = "act"
    OBSERVE = "observe"
    VERIFY = "verify"
    RECOVER = "recover"
    LEARN = "learn"


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Oscillation damping and failure-trip circuit breaker."""

    def __init__(self, failure_threshold: int = 3, recovery_time: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def can_execute(self) -> bool:
        return self.state != CircuitState.OPEN

    def record_success(self) -> None:
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self) -> None:
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN


class ToolCallPayload(BaseModel):
    tool_name: str = Field(..., description="Name of the registered tool to invoke")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Validated parameter payload")
    timeout: float = Field(default=5.0, ge=0.1, le=300.0, description="Execution timeout bound in seconds")


class ExecutionObservation(BaseModel):
    success: bool
    output: Any = None
    error: str | None = None
    stage_transition: Stage | None = None


class DeterministicHarness:
    """
    Deterministic AI Harness operating at the Control/Execution Plane boundary.
    Interprets raw probabilistic model tool requests, validates schemas,
    bounds execution, and detects loop oscillations.
    """

    def __init__(self, tool_registry: dict[str, Callable] | None = None):
        self.tool_registry: dict[str, Callable] = tool_registry or {}
        self.circuit_breaker = CircuitBreaker()
        self.action_history: list[str] = []
        self.state: Stage = Stage.INTERPRET

    def register_tool(self, name: str, fn: Callable) -> None:
        self.tool_registry[name] = fn

    async def execute_step(self, raw_call: dict[str, Any]) -> ExecutionObservation:
        # 1. Circuit breaker gate
        if not self.circuit_breaker.can_execute():
            self.state = Stage.RECOVER
            return ExecutionObservation(
                success=False,
                error="Circuit breaker OPEN: downstream systems protected",
                stage_transition=self.state,
            )

        # 2. Schema Coercion
        try:
            validated = ToolCallPayload.model_validate(raw_call)
        except Exception as exc:
            self.circuit_breaker.record_failure()
            self.state = Stage.RECOVER
            return ExecutionObservation(
                success=False,
                error=f"Schema validation error: {exc}",
                stage_transition=self.state,
            )

        # 3. Oscillation Damping (Cryptographic Hash Sliding Window)
        action_hash = hashlib.sha256(validated.model_dump_json().encode()).hexdigest()
        if self.action_history[-3:].count(action_hash) >= 2:
            self.circuit_breaker.record_failure()
            self.state = Stage.RECOVER
            return ExecutionObservation(
                success=False,
                error=f"Oscillation loop detected for action hash {action_hash[:8]}",
                stage_transition=self.state,
            )

        self.action_history.append(action_hash)

        # 4. Tool Resolution
        tool_fn = self.tool_registry.get(validated.tool_name)
        if not tool_fn:
            self.circuit_breaker.record_failure()
            self.state = Stage.RECOVER
            return ExecutionObservation(
                success=False,
                error=f"Unregistered tool: '{validated.tool_name}'",
                stage_transition=self.state,
            )

        # 5. Bounded Execution
        self.state = Stage.ACT
        try:
            if inspect.iscoroutinefunction(tool_fn):
                coro = tool_fn(**validated.parameters)
            else:
                coro = asyncio.to_thread(tool_fn, **validated.parameters)

            res = await asyncio.wait_for(coro, timeout=validated.timeout)
            self.circuit_breaker.record_success()
            self.state = Stage.OBSERVE
            return ExecutionObservation(
                success=True,
                output=res,
                stage_transition=self.state,
            )
        except asyncio.TimeoutError:
            self.circuit_breaker.record_failure()
            self.state = Stage.RECOVER
            return ExecutionObservation(
                success=False,
                error=f"Execution timed out after {validated.timeout}s",
                stage_transition=self.state,
            )
        except Exception as exc:
            self.circuit_breaker.record_failure()
            self.state = Stage.RECOVER
            return ExecutionObservation(
                success=False,
                error=f"Execution exception: {str(exc)}",
                stage_transition=self.state,
            )
