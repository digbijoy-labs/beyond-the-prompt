"""
Cryptographic Escrow Gate & Anti-Tampering Verification (Chapter 19)
Implements HMAC-SHA256 signature binding, temporal expiry, and dual-key authorization.
"""

from __future__ import annotations

import hmac
import time
from dataclasses import dataclass


class SecurityError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class TamperingDetectedError(Exception):
    pass


@dataclass
class EscrowToken:
    id: str
    hash: str
    sig: str
    expires_at: float


@dataclass
class ApprovalDecision:
    action_id: str
    payload_hash: str
    user: str
    decision: str
    expires_at: float


class EscrowGate:
    """
    Cryptographic authorization gateway enforcing dual-key HMAC token binding
    and runtime payload anti-tampering verification before high-blast actions.
    """

    def __init__(self, secret: str, approvers: set[str]):
        self.secret = secret.encode()
        self.approvers = approvers
        self.registry: dict[str, EscrowToken] = {}

    def register(self, aid: str, h: str, ttl: float = 300) -> str:
        msg = f"{aid}:{h}".encode()
        sig = hmac.new(self.secret, msg, "sha256").hexdigest()
        tok = EscrowToken(aid, h, sig, time.time() + ttl)
        self.registry[aid] = tok
        return sig

    def authorize(self, aid: str, h: str, app: ApprovalDecision) -> bool:
        tok, now = self.registry.pop(aid, None), time.time()
        if not tok or now > tok.expires_at or now > app.expires_at:
            raise SecurityError("Token or approval expired")
        msg = f"{tok.id}:{tok.hash}".encode()
        exp = hmac.new(self.secret, msg, "sha256").hexdigest()
        if not hmac.compare_digest(tok.sig, exp):
            raise SecurityError("HMAC verification failed")
        if app.decision != "APPROVED" or app.user not in self.approvers:
            raise UnauthorizedError("Approver unauthorized")
        if app.action_id != tok.id or app.payload_hash != tok.hash:
            raise SecurityError("Approval unbound to action")
        if not hmac.compare_digest(tok.hash, h):
            raise TamperingDetectedError("Payload tampered")
        return True
