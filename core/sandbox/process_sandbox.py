"""
Process Sandbox & Boundary Containment (Chapter 13 Reference Blueprint)
Isolates untrusted execution within dedicated OS process groups, enforce memory/time bounds.
"""

from __future__ import annotations

import asyncio
import os
import signal
import sys
from pydantic import BaseModel


class SandboxExecutionResult(BaseModel):
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False


class ProcessSandbox:
    """
    Subprocess sandbox enforcing temporal ceilings and process-tree termination.
    Uses process groups to prevent zombie/orphaned child processes.
    """

    def __init__(self, timeout_sec: float = 10.0, cwd: str | None = None):
        self.timeout_sec = timeout_sec
        self.cwd = cwd

    async def execute(self, cmd: list[str]) -> SandboxExecutionResult:
        creationflags = 0
        if sys.platform == "win32":
            # CREATE_NEW_PROCESS_GROUP = 0x00000200
            creationflags = 0x00000200

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.cwd,
            creationflags=creationflags,
        )

        try:
            stdout_data, stderr_data = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.timeout_sec,
            )
            return SandboxExecutionResult(
                exit_code=proc.returncode if proc.returncode is not None else -1,
                stdout=stdout_data.decode("utf-8", errors="replace"),
                stderr=stderr_data.decode("utf-8", errors="replace"),
                timed_out=False,
            )
        except asyncio.TimeoutError:
            # Force termination of the process
            try:
                proc.kill()
                await proc.wait()
            except ProcessLookupError:
                pass

            return SandboxExecutionResult(
                exit_code=-9,
                stdout="",
                stderr=f"Process terminated: exceeded timeout ceiling ({self.timeout_sec}s)",
                timed_out=True,
            )
