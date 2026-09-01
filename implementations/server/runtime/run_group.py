"""Pure Run/Group reducers and the fail-closed opening execution fence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .errors import (
    InvalidGroupTransition,
    InvalidRunTransition,
    RunGroupFenceClosed,
    RunGroupGuardError,
)


RUN_STATES = (
    "confirmed",
    "opening_pending",
    "ready",
    "running",
    "execution_terminal",
    "close_pending",
    "reconciliation_required",
    "closed",
)
RUN_EVENTS = (
    "run.created",
    "audit_opening.requested",
    "audit_opening.verified",
    "audit_opening.reconciliation_required",
    "reconciliation.retry_requested",
    "run.started",
    "run.execution_terminal_elected",
    "audit_close.requested",
    "audit_close.verified",
    "audit_close.reconciliation_required",
)
GROUP_STATES = (
    "pending",
    "collecting",
    "revealing",
    "deliberating",
    "voting",
    "committing",
    "cancelling",
    "completed",
    "cancelled",
    "failed",
)
GROUP_EVENTS = (
    "group.started",
    "position.accepted",
    "collection.closed",
    "reveal.published",
    "critique.accepted",
    "round.closed",
    "vote.accepted",
    "verdict.computed",
    "group.committed",
    "cancellation.requested",
    "group.cancelled",
    "group.failed",
)

TERMINAL_CAUSE_EXIT_REASONS = {
    "committed_result": "resolved",
    "committed_irreconcilable_dissent": "dissent_irreconcilable",
    "protocol_ceiling": "loop_ceiling_reached",
    "human_cancellation": "user_abort",
    "technical_prevention": "error",
}


@dataclass(frozen=True)
class RunProjection:
    state: str
    opening_verified: bool = False
    opening_verification_event_id: str | None = None
    reconciliation_target: str | None = None
    terminal_cause: str | None = None
    exit_reason: str | None = None


@dataclass(frozen=True)
class GroupProjection:
    state: str
    decision: str | None = None
    dissent_refs: tuple[str, ...] = ()


def _closed_guards(
    guards: Mapping[str, Any], expected: Mapping[str, Any], event_type: str
) -> None:
    if set(guards) != set(expected) or any(
        guards[name] != value for name, value in expected.items()
    ):
        raise RunGroupGuardError(f"guard mismatch for {event_type}")


def _nonempty_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise RunGroupGuardError(f"{label} must be a non-empty string")
    return value


def reduce_run(
    current: RunProjection | None,
    event_type: str,
    guards: Mapping[str, Any],
) -> RunProjection:
    """Reduce exactly one listed RunLifecycle transition."""

    state = current.state if current is not None else None
    if state is None and event_type == "run.created":
        _closed_guards(
            guards,
            {
                "execution_authority_mode": "runtime-managed",
                "frozen_digest_unique": True,
            },
            event_type,
        )
        return RunProjection("confirmed")
    if current is None:
        raise InvalidRunTransition(f"run transition is not admitted: {state!r} + {event_type!r}")
    if state not in RUN_STATES:
        raise InvalidRunTransition(f"unknown run state: {state!r}")

    if state == "confirmed" and event_type == "audit_opening.requested":
        _closed_guards(guards, {"opening_intent_committed": True}, event_type)
        return RunProjection("opening_pending")
    if state == "opening_pending" and event_type == "audit_opening.verified":
        if set(guards) != {"exact_canonical_row", "evidence_event_id"} or guards.get(
            "exact_canonical_row"
        ) is not True:
            raise RunGroupGuardError(f"guard mismatch for {event_type}")
        evidence = _nonempty_text(guards["evidence_event_id"], "evidence_event_id")
        return RunProjection("ready", True, evidence)
    if state == "opening_pending" and event_type == "audit_opening.reconciliation_required":
        _closed_guards(guards, {"same_identity_divergent": True}, event_type)
        return RunProjection("reconciliation_required", reconciliation_target="opening")
    if state == "reconciliation_required" and event_type == "reconciliation.retry_requested":
        target = current.reconciliation_target
        _closed_guards(
            guards,
            {"target": target, "authorized_repair_disposition": True},
            event_type,
        )
        if target == "opening":
            return RunProjection("opening_pending")
        if target == "close":
            return RunProjection(
                "close_pending",
                current.opening_verified,
                current.opening_verification_event_id,
                terminal_cause=current.terminal_cause,
                exit_reason=current.exit_reason,
            )
        raise RunGroupGuardError("reconciliation target is not closed")
    if state == "ready" and event_type == "run.started":
        _closed_guards(guards, {"opening_remains_verified": True}, event_type)
        if not current.opening_verified or current.opening_verification_event_id is None:
            raise RunGroupFenceClosed("run start lacks verified opening evidence")
        return RunProjection(
            "running", True, current.opening_verification_event_id
        )
    if state == "running" and event_type == "run.execution_terminal_elected":
        if set(guards) != {"terminal_cause", "exit_reason"}:
            raise RunGroupGuardError(f"guard mismatch for {event_type}")
        cause = guards["terminal_cause"]
        expected_reason = TERMINAL_CAUSE_EXIT_REASONS.get(cause)
        if expected_reason is None or guards["exit_reason"] != expected_reason:
            raise RunGroupGuardError("terminal cause does not match the closed exit mapping")
        return RunProjection(
            "execution_terminal",
            current.opening_verified,
            current.opening_verification_event_id,
            terminal_cause=cause,
            exit_reason=expected_reason,
        )
    if state == "execution_terminal" and event_type == "audit_close.requested":
        _closed_guards(guards, {"close_derived_from_winner": True}, event_type)
        return RunProjection(
            "close_pending",
            current.opening_verified,
            current.opening_verification_event_id,
            terminal_cause=current.terminal_cause,
            exit_reason=current.exit_reason,
        )
    if state == "close_pending" and event_type == "audit_close.verified":
        _closed_guards(guards, {"exact_canonical_row": True}, event_type)
        return RunProjection(
            "closed",
            current.opening_verified,
            current.opening_verification_event_id,
            terminal_cause=current.terminal_cause,
            exit_reason=current.exit_reason,
        )
    if state == "close_pending" and event_type == "audit_close.reconciliation_required":
        _closed_guards(guards, {"same_identity_divergent": True}, event_type)
        return RunProjection(
            "reconciliation_required",
            current.opening_verified,
            current.opening_verification_event_id,
            "close",
            current.terminal_cause,
            current.exit_reason,
        )
    raise InvalidRunTransition(f"run transition is not admitted: {state!r} + {event_type!r}")


def run_execution_eligible(current: RunProjection) -> bool:
    """Return the deterministic opening fence decision without releasing anything."""

    return (
        current.state in {"ready", "running", "execution_terminal", "close_pending", "closed"}
        and current.opening_verified
        and current.opening_verification_event_id is not None
    )


def require_run_execution_eligible(current: RunProjection) -> None:
    if not run_execution_eligible(current):
        raise RunGroupFenceClosed(f"run execution fence is closed in {current.state}")


def fixed_two_seat_decision(votes: tuple[str, ...]) -> str:
    """Apply the fixed two-seat rule without fabricating a verdict for no quorum."""

    if len(votes) < 2 or any(not isinstance(vote, str) or not vote for vote in votes):
        return "no_quorum"
    if len(votes) != 2:
        raise RunGroupGuardError("fixed-two-seat-proof@1 requires exactly two seats")
    return "consensus" if votes[0] == votes[1] else "dissent"


def reduce_group(
    current: GroupProjection,
    event_type: str,
    guards: Mapping[str, Any],
) -> GroupProjection:
    """Reduce exactly one listed GroupLifecycle transition."""

    state = current.state
    if state not in GROUP_STATES:
        raise InvalidGroupTransition(f"unknown group state: {state!r}")
    if state == "pending" and event_type == "group.started":
        _closed_guards(guards, {"dependencies_delivered": True, "spec_valid": True}, event_type)
        return GroupProjection("collecting")
    if state == "collecting" and event_type == "position.accepted":
        _closed_guards(
            guards,
            {"parent_receipt_verified": True, "logical_key_unused": True},
            event_type,
        )
        return current
    if state == "collecting" and event_type == "collection.closed":
        _closed_guards(
            guards,
            {"eligible_set_frozen": True, "quorum_or_deadline_policy": True},
            event_type,
        )
        return GroupProjection("revealing")
    if state == "revealing" and event_type == "reveal.published":
        if set(guards) != {"exact_manifest", "deliberation_enabled"} or guards.get(
            "exact_manifest"
        ) is not True or not isinstance(guards.get("deliberation_enabled"), bool):
            raise RunGroupGuardError(f"guard mismatch for {event_type}")
        return GroupProjection(
            "deliberating" if guards["deliberation_enabled"] else "voting"
        )
    if state == "deliberating" and event_type == "critique.accepted":
        _closed_guards(guards, {"reply_visible": True, "round_schema_valid": True}, event_type)
        return current
    if state == "deliberating" and event_type == "round.closed":
        _closed_guards(guards, {"criterion_recorded": True}, event_type)
        return GroupProjection("voting")
    if state == "voting" and event_type == "vote.accepted":
        _closed_guards(guards, {"logical_vote_unused": True, "schema_valid": True}, event_type)
        return current
    if state == "voting" and event_type == "verdict.computed":
        if set(guards) != {"decision", "quorum"} or guards.get("quorum") is not True:
            raise RunGroupGuardError(f"guard mismatch for {event_type}")
        decision = guards["decision"]
        if decision not in {"consensus", "dissent"}:
            raise RunGroupGuardError("no_quorum cannot produce verdict.computed")
        return GroupProjection("committing", decision)
    if state == "committing" and event_type == "group.committed":
        if set(guards) != {"typed_result", "persisted_verdict", "dissent_refs"}:
            raise RunGroupGuardError(f"guard mismatch for {event_type}")
        if guards["typed_result"] is not True or guards["persisted_verdict"] is not True:
            raise RunGroupGuardError(f"guard mismatch for {event_type}")
        refs = guards["dissent_refs"]
        if not isinstance(refs, tuple) or any(not isinstance(ref, str) or not ref for ref in refs):
            raise RunGroupGuardError("dissent_refs must be an immutable ID tuple")
        if current.decision == "dissent" and not refs:
            raise RunGroupGuardError("committed dissent must preserve dissent references")
        return GroupProjection("completed", current.decision, refs)
    if state not in {"completed", "cancelled", "failed"} and event_type == "cancellation.requested":
        _closed_guards(guards, {"authorized": True}, event_type)
        return GroupProjection("cancelling", current.decision, current.dissent_refs)
    if state == "cancelling" and event_type == "group.cancelled":
        _closed_guards(guards, {"attempts_terminal_or_deadline": True}, event_type)
        return GroupProjection("cancelled", current.decision, current.dissent_refs)
    if state not in {"completed", "cancelled", "failed", "cancelling"} and event_type == "group.failed":
        _closed_guards(guards, {"declared_retries_exhausted": True}, event_type)
        return GroupProjection("failed", current.decision, current.dissent_refs)
    raise InvalidGroupTransition(
        f"group transition is not admitted: {state!r} + {event_type!r}"
    )
