import asyncio
import pytest
from core.runtime.harness import DeterministicHarness, Stage


@pytest.mark.asyncio
async def test_harness_successful_execution():
    harness = DeterministicHarness()

    def sample_tool(query: str) -> str:
        return f"result_for_{query}"

    harness.register_tool("sample_tool", sample_tool)

    payload = {
        "tool_name": "sample_tool",
        "parameters": {"query": "vector_db"},
        "timeout": 2.0,
    }

    obs = await harness.execute_step(payload)
    assert obs.success is True
    assert obs.output == "result_for_vector_db"
    assert harness.state == Stage.OBSERVE


@pytest.mark.asyncio
async def test_harness_unregistered_tool():
    harness = DeterministicHarness()
    payload = {
        "tool_name": "non_existent",
        "parameters": {},
        "timeout": 1.0,
    }
    obs = await harness.execute_step(payload)
    assert obs.success is False
    assert "Unregistered tool" in obs.error
    assert harness.state == Stage.RECOVER


@pytest.mark.asyncio
async def test_harness_oscillation_detection():
    harness = DeterministicHarness()
    harness.register_tool("echo", lambda x: x)
    payload = {"tool_name": "echo", "parameters": {"x": 1}}

    # First execution succeeds
    obs1 = await harness.execute_step(payload)
    assert obs1.success is True

    # Second execution succeeds
    obs2 = await harness.execute_step(payload)
    assert obs2.success is True

    # Third identical execution triggers oscillation detection
    obs3 = await harness.execute_step(payload)
    assert obs3.success is False
    assert "Oscillation loop detected" in obs3.error


@pytest.mark.asyncio
async def test_harness_timeout_bounding():
    harness = DeterministicHarness()

    async def slow_tool():
        await asyncio.sleep(0.5)
        return "done"

    harness.register_tool("slow_tool", slow_tool)
    payload = {
        "tool_name": "slow_tool",
        "parameters": {},
        "timeout": 0.1,
    }
    obs = await harness.execute_step(payload)
    assert obs.success is False
    assert "timed out" in obs.error
