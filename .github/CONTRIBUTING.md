# Contributing to Beyond the Prompt Companion Code

We welcome contributions, benchmark extensions, and verified errata submissions!

## Development Guidelines
1. **The Half-Page Signal-to-Noise Rule**: Reference implementations must focus strictly on architectural contracts, state machines, and protocols. Avoid unnecessary scaffolding.
2. **Type Safety & Pydantic v2**: All models must use modern Pydantic v2 schemas and Python 3.12+ type annotations.
3. **Deterministic Governance**: Implementations interacting with untrusted model outputs must include schema coercion, timeouts, and oscillation checks.

## Submitting Pull Requests
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/kernel-enhancement`).
3. Ensure all tests pass (`pytest -v tests/`).
4. Commit your changes with clear messages.
5. Open a Pull Request referencing any relevant book chapters or errata items.
