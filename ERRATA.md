# Errata & Architecture Updates: Beyond the Prompt

This document tracks verified technical errata, clarifications, and dependency updates for ***Beyond the Prompt: The Architecture of Autonomous Systems*** (Jay Thorne / Digbijoy Labs).

---

## Submitting Corrections

If you discover a typographical error, architectural discrepancy, or broken API contract, please open an Issue using the **Errata Submission** template on GitHub.

| Chapter | Section / Page | Reported Discrepancy | Corrected Blueprint / Architecture | Status |
| :--- | :--- | :--- | :--- | :--- |
| *Initial Release* | Front Matter | First edition release baseline | All reference blueprints verified on Python 3.12+ and Pydantic v2.8 | Verified |

---

## Protocol Baseline

- **Model Context Protocol (MCP)**: Grounded against MCP revision `2026-07-28` specification.
- **OpenTelemetry GenAI**: Aligned with OpenTelemetry Semantic Conventions v1.28.0+.
- **Type Coercion & Schema Validation**: Aligned with Pydantic v2.8+.
