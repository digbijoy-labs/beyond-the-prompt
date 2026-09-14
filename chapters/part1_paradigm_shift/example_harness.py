"""
Part 1 Demonstration: Deterministic Execution Harness & Oscillation Arrest
"""

import asyncio
from core.runtime.harness import DeterministicHarness, Stage


async def main():
    print("=== Beyond the Prompt: Part 1 Harness Demonstration ===")
    harness = DeterministicHarness()

    # Register deterministic tool
    def query_database(sql: str) -> dict:
        return {"status": "SUCCESS", "rows": [{"id": 1, "balance": 450000.00}]}

    harness.register_tool("query_database", query_database)

    # 1. Successful Tool Invocation
    print("\n[1] Executing valid database query step:")
    call_1 = {
        "tool_name": "query_database",
        "parameters": {"sql": "SELECT id, balance FROM accounts WHERE id = 1;"},
        "timeout": 2.0,
    }
    obs1 = await harness.execute_step(call_1)
    print(f"Outcome: success={obs1.success}, output={obs1.output}")

    # 2. Schema Coercion Failure Prevention
    print("\n[2] Executing malformed schema call:")
    call_2 = {
        "tool_name": "query_database",
        "parameters": "INVALID_NOT_A_DICT",
    }
    obs2 = await harness.execute_step(call_2)
    print(f"Outcome: success={obs2.success}, error={obs2.error}")

    # 3. Oscillation Loop Arrest
    print("\n[3] Triggering repetitive identical calls to demonstrate oscillation damping:")
    for i in range(3):
        res = await harness.execute_step(call_1)
        print(f"Iteration {i+1}: success={res.success}, error={res.error}")

    print("\n=== Demonstration Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
