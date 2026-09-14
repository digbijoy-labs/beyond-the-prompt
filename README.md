# Beyond the Prompt: The Architecture of Autonomous Systems

[![CI Verification](https://github.com/digbijoylabs/beyond-the-prompt/actions/workflows/ci.yml/badge.svg)](https://github.com/digbijoylabs/beyond-the-prompt/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Protocol: MCP 2026-07-28](https://img.shields.io/badge/protocol-MCP_2026--07--28-orange.svg)](https://modelcontextprotocol.io)

> **Official Companion Repository & Reference Architectural Kernels**  
> Companion code, state machine blueprints, and verified execution harnesses for the book:  
> ***Beyond the Prompt: The Architecture of Autonomous Systems: Context Engineering, Graph Engineering, Loop Design, and Production AI Harnesses***  
> by **Jay Thorne** | Published by **Digbijoy Labs Publications** (2026).

---

## 🏛 The 5-Plane Cognitive Runtime Architecture

In enterprise production environments, large language models (LLMs) cannot govern their own execution. A model is an untrusted, probabilistic central processing unit operating inside a hardened, deterministic runtime system governed by an engineered **AI Harness**.

```
+-------------------------------------------------------------------------+
|                           5-PLANE COGNITIVE MATRIX                      |
+-------------------------------------------------------------------------+
|  1. INTELLIGENCE PLANE | Frontier Reasoning (Claude Mythos, GPT-6, R1)  |
|                        | Fast Orchestrators & Sovereign SLMs (GLM, Qwen)|
+-------------------------------------------------------------------------+
|  2. CONTEXT PLANE      | Prefix KV-Cache Compaction Cascades            |
|                        | Virtual Memory Paging & GraphRAG Substrates     |
+-------------------------------------------------------------------------+
|  3. EXECUTION PLANE    | Model Context Protocol (MCP) Servers           |
|                        | OS MicroVM Sandboxes & Process Group Isolation  |
+-------------------------------------------------------------------------+
|  4. CONTROL PLANE      | 7-Stage State Graph & Guarded Statecharts       |
|                        | Oscillation Damping & Hardware Circuit Breakers |
+-------------------------------------------------------------------------+
|  5. EVIDENCE PLANE     | OpenTelemetry GenAI Semantic Spans & Telemetry  |
|                        | Cryptographic Audit Journals & Unit Economics   |
+-------------------------------------------------------------------------+
```

---

## 📂 Repository Layout

The repository mirrors the six major architectural parts of the book:

```
beyond-the-prompt/
├── core/                                # Verified production runtime kernels
│   ├── runtime/harness.py               # Deterministic Execution Harness (Ch 1)
│   ├── intelligence/cognitive_router.py # Budget-Aware Inference Engine (Ch 2)
│   ├── gateway/model_gateway.py         # Multi-Provider Failover Gateway (Ch 3)
│   ├── tools/tool_registry.py           # Grammar-Constrained Tool Coercion (Ch 4)
│   ├── context/prefix_compiler.py       # Static KV Prefix Cache Governor (Ch 5)
│   ├── context/compaction_cascade.py    # Recursive Context Compaction (Ch 6)
│   ├── graph/graph_rag_engine.py        # Knowledge Graph & Multi-Hop Traversal (Ch 7)
│   ├── memory/hybrid_memory_substrate.py# Tiered Working/Episodic/Fact Memory (Ch 8)
│   ├── flow/statechart.py               # Guarded Statechart DAG Engine (Ch 9)
│   ├── reasoning/mcts_planner.py        # Test-Time Compute (TTC) Rollout Search (Ch 10)
│   ├── loop/self_correction.py          # Grounded Evaluator-Optimizer Reflexion (Ch 11)
│   ├── governance/loop_governor.py      # Oscillation Damping & Cycle Arrest (Ch 12)
│   ├── sandbox/process_sandbox.py       # OS Process Group Sandbox (Ch 13)
│   ├── protocols/mcp_server.py          # Model Context Protocol (MCP) Host (Ch 14)
│   ├── aci/workspace_controller.py      # Safe Agent-Computer Interface (Ch 15)
│   ├── durable/temporal_state.py        # Event-Sourced Journal State Store (Ch 16)
│   ├── protocols/a2a_messaging.py       # Agent-to-Agent (A2A) Message Envelope (Ch 17)
│   ├── multiagent/subagent_pool.py      # Ephemeral Subagent Worker Isolation (Ch 18)
│   ├── hitl/authorization_gate.py       # Two-Phase Policy Decision Point (Ch 19)
│   ├── spec/executable_spec.py          # Spec-Driven Executable Prompt Engine (Ch 20)
│   ├── security/zero_trust_guard.py     # Prompt Injection & Canary Filter (Ch 21)
│   ├── evals/eval_runner.py             # Deterministic Trajectory Benchmarks (Ch 22)
│   ├── sre/telemetry.py                 # OpenTelemetry GenAI Cost/Latency Tracker (Ch 23)
│   └── compound/flywheel.py             # DSPy-style Exemplar Flywheel (Ch 24)
├── chapters/                            # Runnable chapter demonstrations & guides
│   ├── part1_paradigm_shift/            # Chapters 1–4 Walkthroughs
│   ├── part2_context_graph/             # Chapters 5–8 Walkthroughs
│   ├── part3_flow_loops/                # Chapters 9–12 Walkthroughs
│   ├── part4_protocols_runtime/         # Chapters 13–16 Walkthroughs
│   ├── part5_multi_agent_swarms/        # Chapters 17–20 Walkthroughs
│   └── part6_eval_security/             # Chapters 21–24 Walkthroughs
├── tests/                               # Comprehensive automated test suite
├── ERRATA.md                            # Living errata & architecture changelog
└── pyproject.toml                       # Python 3.12+ project configuration
```

---

## 🚀 Quickstart

### 1. Prerequisites
- Python 3.12 or higher
- Git

### 2. Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/digbijoylabs/beyond-the-prompt.git
cd beyond-the-prompt
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the Test Suite
Verify that all architectural kernels and invariants pass verification:

```bash
pytest -v tests/
```

### 4. Run Chapter Demonstrations
Execute any chapter reference blueprint directly:

```bash
# Part 1: Deterministic Execution Harness
python -m chapters.part1_paradigm_shift.example_harness

# Part 2: Context Compaction & GraphRAG
python -m chapters.part2_context_graph.example_graphrag

# Part 4: Model Context Protocol (MCP) Server
python -m chapters.part4_protocols_runtime.example_mcp_client
```

---

## ⚡ The 7-Stage State Graph Reference Pattern

Rather than naive linear prompt chains, *Beyond the Prompt* formalizes autonomous task execution as a 7-stage directed state graph:

$$\text{Interpret} \longrightarrow \text{Plan} \longrightarrow \text{Act} \longrightarrow \text{Observe} \longrightarrow \text{Verify} \longrightarrow \text{Recover} \longrightarrow \text{Learn}$$

Every stage is validated by strict schema coercion, hardware-timed timeouts, and cryptographic cycle detectors.

---

## 📖 Book Information & Citation

If you use these architectural kernels or citation references in your research, production systems, or publications, please cite:

```bibtex
@book{thorne2026beyondtheprompt,
  author    = {Jay Thorne},
  title     = {Beyond the Prompt: The Architecture of Autonomous Systems},
  subtitle  = {Context Engineering, Graph Engineering, Loop Design, and Production AI Harnesses},
  publisher = {Digbijoy Labs Publications},
  year      = {2026},
  isbn      = {Pending / Release Edition},
  url       = {https://github.com/digbijoylabs/beyond-the-prompt}
}
```

---

## 🤝 Community & Contributions

- **Discussions & Issues**: Report errata, ask architectural questions, or submit PRs via [GitHub Issues](https://github.com/digbijoylabs/beyond-the-prompt/issues).
- **Errata Tracking**: Review verified updates in [ERRATA.md](ERRATA.md).
- **Code of Conduct**: This repository enforces the [Contributor Covenant](.github/CODE_OF_CONDUCT.md).

---

## 📄 License

This companion codebase is open-sourced under the [MIT License](LICENSE).
