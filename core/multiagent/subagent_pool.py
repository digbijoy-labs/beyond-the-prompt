"""
Subagents and Context Isolation: Blast-Radius Bounding (Chapter 18)
Manages ephemeral child worker lifecycles to protect parent context windows.
"""

from __future__ import annotations

import uuid
from typing import Any, Callable
from pydantic import BaseModel


class SubagentResult(BaseModel):
    worker_id: str
    status: str
    output: Any


class SubagentPool:
    """
    Spawns ephemeral, single-task subagents with sandboxed scopes.
    """

    def __init__(self, max_concurrency: int = 5):
        self.max_concurrency = max_concurrency
        self.active_workers: dict[str, str] = {}

    def dispatch_ephemeral(self, task_name: str, worker_fn: Callable[..., Any], **kwargs) -> SubagentResult:
        if len(self.active_workers) >= self.max_concurrency:
            raise RuntimeError(f"Subagent pool concurrency ceiling ({self.max_concurrency}) reached")

        worker_id = f"worker-{task_name}-{str(uuid.uuid4())[:8]}"
        self.active_workers[worker_id] = task_name
        try:
            res = worker_fn(**kwargs)
            return SubagentResult(worker_id=worker_id, status="SUCCESS", output=res)
        finally:
            self.active_workers.pop(worker_id, None)
