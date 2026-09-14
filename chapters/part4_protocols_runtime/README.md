# Part IV: Protocols, Runtime Execution & ACIs

Chapters 13 through 16 cover the physical execution boundary: Model Context Protocol (MCP), process sandboxing, and durable event sourcing.

- **Chapter 13**: Secure Execution Sandboxes: Containing Untrusted Code (`core/sandbox/process_sandbox.py`)
- **Chapter 14**: The Model Context Protocol (MCP): Open Protocol for Agent Tools (`core/protocols/mcp_server.py`)
- **Chapter 15**: Agent-Computer Interfaces (ACI): Shell Sandboxes and Workspaces (`core/aci/workspace_controller.py`)
- **Chapter 16**: Durable Agent Execution: State Persistence and Replay (`core/durable/temporal_state.py`)

## Running Demonstrations

```bash
python -m chapters.part4_protocols_runtime.example_mcp_client
```
