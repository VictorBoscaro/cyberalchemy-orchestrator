"""Pure retry-treatment classification outside the RWO semantic kernel.

The classifier chooses a closed treatment from already-known delivery facts. It
does not wait, back off, write a queue, or make another delivery attempt.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RetryDecision:
    treatment: str
    reason: str | None = None
    preserve_identity_and_payload: bool = False
    semantic_disposition: str | None = None
    next_policy_routes: tuple[str, ...] = ()


def classify_retry(
    *,
    kernel_outcome: str | None = None,
    adapter_outcome: str | None = None,
    submission_state: str | None = None,
    command_validity: str | None = None,
    attempt_budget: str | None = None,
    budget_open: bool | None = None,
    frozen_policy: str | None = None,
    lease_state: str | None = None,
    policy_allows: bool = False,
    adapter_capabilities: Iterable[str] = (),
) -> RetryDecision:
    """Classify one retry situation without changing semantic command identity."""

    capabilities = frozenset(adapter_capabilities)
    if attempt_budget == "exhausted":
        return RetryDecision(
            "DeadLetter" if frozen_policy == "dead-letter" else "Escalate",
            reason="ATTEMPT_BUDGET_EXHAUSTED",
        )
    if lease_state == "ownership-lost":
        return RetryDecision(
            "ReconcileThenDecide" if "owner-recovery" in capabilities else "Escalate",
            reason="OWNERSHIP_LOST",
        )
    if kernel_outcome in {"Rejected", "DivergentDuplicate"}:
        return RetryDecision("DoNotRetry", reason=kernel_outcome)
    if kernel_outcome == "Duplicate":
        return RetryDecision(
            "DoNotRetry", semantic_disposition="acknowledge-convergence"
        )
    if adapter_outcome == "terminal-rejection" or command_validity == "invalid":
        return RetryDecision(
            "DoNotRetry",
            reason="TERMINAL_REJECTION_OR_INVALID_COMMAND",
            next_policy_routes=("DeadLetter", "Escalate"),
        )
    if submission_state == "unknown":
        if {"status-query", "journal-lookup"} & capabilities:
            return RetryDecision("ReconcileThenDecide", reason="DELIVERY_UNKNOWN")
        if (
            "end-to-end-idempotency-key" in capabilities
            and policy_allows
            and budget_open is True
        ):
            return RetryDecision(
                "RetrySame", preserve_identity_and_payload=True
            )
        return RetryDecision("Escalate", reason="AMBIGUOUS_DELIVERY")
    if submission_state == "definitely-not-submitted" and budget_open is True:
        if adapter_outcome == "rate-limited" and "policy-backoff" not in capabilities:
            return RetryDecision("Escalate", reason="BACKOFF_CAPABILITY_REQUIRED")
        return RetryDecision("RetrySame", preserve_identity_and_payload=True)
    return RetryDecision("DoNotRetry", reason="INSUFFICIENT_RETRY_EVIDENCE")
