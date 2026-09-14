"""
Zero-Trust Agent Security & Prompt Injection Defense (Chapter 21)
Detects indirect prompt injection, canary token exfiltration, and privilege escalation.
"""

from __future__ import annotations

import secrets
import re
from pydantic import BaseModel


class SecurityAssessment(BaseModel):
    is_safe: bool
    risk_score: float  # 0.0 to 1.0
    flagged_patterns: list[str] = []


class ZeroTrustGuard:
    """
    Perimeter inspection layer sanitizing untrusted inputs and tool observations.
    """

    SUSPICIOUS_PATTERNS = [
        r"ignore (all )?previous instructions",
        r"system prompt override",
        r"<script>",
        r"BEGIN PRIVATE KEY",
        r"reveal your secret token",
    ]

    def __init__(self):
        self.canary_token = f"CANARY_{secrets.token_hex(8)}"

    def inspect_text(self, text: str) -> SecurityAssessment:
        flags = []
        for pattern in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                flags.append(pattern)

        if self.canary_token in text:
            flags.append("CANARY_TOKEN_LEAK")

        is_safe = len(flags) == 0
        score = 1.0 if not is_safe else 0.0
        return SecurityAssessment(is_safe=is_safe, risk_score=score, flagged_patterns=flags)
