"""
Comprehensive Verification of Architectural Reference Kernels from Beyond the Prompt.
Covers Chapter 9 (Statechart Monotonic Ceilings), Chapter 19 (EscrowGate), and Chapter 23 (EconomicGovernor).
"""

import hashlib
import time
import pytest

from core.hitl.escrow_gate import (
    EscrowGate,
    ApprovalDecision,
    SecurityError,
    UnauthorizedError,
    TamperingDetectedError,
)
from core.flow.statechart import (
    StateChartEngine,
    MachineState,
    InvalidStateError,
    StatechartDAG,
)
from core.sre.telemetry import (
    EconomicGovernor,
    ModelRates,
    BudgetExceededError,
)


def test_escrow_gate_full_lifecycle():
    secret = "production-secret-signing-key-2026"
    gate = EscrowGate(secret=secret, approvers={"alice_sre", "bob_lead"})

    params = {"action": "scale_cluster", "nodes": 10}
    raw = str(sorted(params.items())).encode()
    p_hash = hashlib.sha256(raw).hexdigest()
    act_id = "act_101"

    # 1. Register token
    sig = gate.register(act_id, p_hash, ttl=60.0)
    assert act_id in gate.registry
    assert gate.registry[act_id].sig == sig

    # 2. Authorize with valid approval
    decision = ApprovalDecision(
        action_id=act_id,
        payload_hash=p_hash,
        user="alice_sre",
        decision="APPROVED",
        expires_at=time.time() + 60.0,
    )
    assert gate.authorize(act_id, p_hash, decision) is True
    assert act_id not in gate.registry

    # 3. Tampered payload fails
    gate.register(act_id, p_hash, ttl=60.0)
    with pytest.raises(TamperingDetectedError, match="Payload tampered"):
        gate.authorize(act_id, "tampered_hash_value", decision)

    # 4. Unauthorized approver fails
    gate.register(act_id, p_hash, ttl=60.0)
    unauth_decision = ApprovalDecision(
        action_id=act_id,
        payload_hash=p_hash,
        user="mallory_intruder",
        decision="APPROVED",
        expires_at=time.time() + 60.0,
    )
    with pytest.raises(UnauthorizedError, match="Approver unauthorized"):
        gate.authorize(act_id, p_hash, unauth_decision)

    # 5. Expired token fails
    gate.register(act_id, p_hash, ttl=-10.0)
    with pytest.raises(SecurityError, match="Token or approval expired"):
        gate.authorize(act_id, p_hash, decision)


def test_statechart_engine_monotonic_step_ceiling():
    transitions = {
        "INGEST": {"VALIDATE": lambda ctx: ctx.get("valid", True)},
        "VALIDATE": {"RETRY": lambda ctx: ctx.get("retry", True)},
        "RETRY": {"VALIDATE": lambda ctx: True},  # Cycle!
    }
    engine = StateChartEngine(
        states={"INGEST", "VALIDATE", "RETRY", "TERMINAL"},
        transitions=transitions,
        initial="INGEST",
        max_steps=6,
    )

    state = MachineState(current="INGEST", step_count=0, context={"valid": True, "retry": True})

    # Step through cycling states
    while state.current != "TERMINAL":
        state = engine.step(state)

    # Assert harness terminated at monotonic ceiling
    assert state.step_count == 6
    assert state.current == "TERMINAL"


def test_statechart_dag_step_bounding():
    dag = StatechartDAG(initial_state="START", max_steps=5)
    dag.add_state("START")
    dag.add_state("LOOP_A")
    dag.add_state("LOOP_B")
    dag.add_state("DONE", is_terminal=True)

    dag.add_transition("START", "LOOP_A", lambda ctx: True)
    dag.add_transition("LOOP_A", "LOOP_B", lambda ctx: True)
    dag.add_transition("LOOP_B", "LOOP_A", lambda ctx: True)  # Infinite cycle

    while dag.current_state != "DONE" and dag.current_state != "TERMINAL":
        dag.step({})

    assert dag.step_count == 5
    assert dag.current_state in ("DONE", "TERMINAL")


def test_economic_governor_cost_tracking_and_cprt():
    rates = {
        "gpt-4o": ModelRates(in_price=5.0, out_price=15.0),
        "slm": ModelRates(in_price=0.5, out_price=1.5),
    }
    gov = EconomicGovernor(rates=rates, budget=1.0)

    # Step 1: 10,000 input tokens, 2,000 output tokens on gpt-4o
    # (10k * 5.0 + 2k * 15.0) / 1e6 = (50,000 + 30,000) / 1e6 = 0.080 USD
    c1 = gov.record_step("gpt-4o", 10_000, 2_000)
    assert round(c1, 4) == 0.0800

    # Task 1 completes
    gov.record_completion("task_1", ok=True)
    assert len(gov.completions) == 1
    assert round(gov.completions[0]["cost"], 4) == 0.0800

    # Step 2: 20,000 input tokens, 5,000 output tokens on slm
    # (20k * 0.5 + 5k * 1.5) / 1e6 = (10,000 + 7,500) / 1e6 = 0.0175 USD
    c2 = gov.record_step("slm", 20_000, 5_000)
    assert round(c2, 4) == 0.0175

    # Task 2 completes (failed task)
    gov.record_completion("task_2", ok=False)
    assert len(gov.completions) == 2
    assert round(gov.completions[1]["cost"], 4) == 0.0175

    # Summary report
    rep = gov.compute_summary_report()
    assert round(rep["spend"], 4) == 0.0975
    assert rep["ok"] == 1
    assert round(rep["cprt"], 4) == 0.0975

    # Test budget circuit breaker
    with pytest.raises(BudgetExceededError):
        gov.record_step("gpt-4o", 200_000, 50_000)
