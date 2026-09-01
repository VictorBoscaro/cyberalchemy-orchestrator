"""Pure projection and lifecycle policy for the bounded continuation consumer."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Mapping

from .errors import (
    ContinuationAuthorityError,
    ContinuationMixedSourceState,
    InvalidContinuationTransition,
)


CONTINUATION_STATES = (
    "suspended",
    "resume_requested",
    "resuming",
    "resume_unknown",
    "reconstruction_eligible",
    "resumed",
    "cancel_requested",
    "cancelled",
    "expired",
)

CONTINUATION_EVENTS = (
    "continuation.suspended",
    "continuation.resume_requested",
    "continuation.resuming",
    "continuation.resumed",
    "continuation.resume_unknown",
    "continuation.provider_lost",
    "continuation.reconstruction_requested",
    "continuation.cancel_requested",
    "continuation.cancelled",
    "continuation.expired",
)

_TRANSITIONS = {
    (None, "continuation.suspended"): "suspended",
    ("suspended", "continuation.resume_requested"): "resume_requested",
    ("resume_requested", "continuation.resuming"): "resuming",
    ("resuming", "continuation.resumed"): "resumed",
    ("resuming", "continuation.resume_unknown"): "resume_unknown",
    ("resume_unknown", "continuation.resumed"): "resumed",
    ("suspended", "continuation.provider_lost"): "reconstruction_eligible",
    ("resuming", "continuation.provider_lost"): "reconstruction_eligible",
    ("resume_unknown", "continuation.provider_lost"): "reconstruction_eligible",
    (
        "reconstruction_eligible",
        "continuation.reconstruction_requested",
    ): "resume_requested",
    ("suspended", "continuation.cancel_requested"): "cancel_requested",
    ("resume_requested", "continuation.cancel_requested"): "cancel_requested",
    ("resuming", "continuation.cancel_requested"): "cancel_requested",
    ("resume_unknown", "continuation.cancel_requested"): "cancel_requested",
    (
        "reconstruction_eligible",
        "continuation.cancel_requested",
    ): "cancel_requested",
    ("cancel_requested", "continuation.cancelled"): "cancelled",
    ("suspended", "continuation.expired"): "expired",
    ("resume_requested", "continuation.expired"): "expired",
    ("reconstruction_eligible", "continuation.expired"): "expired",
}


def reduce_continuation(state: str | None, event_type: str) -> str:
    """Apply only a transition named by AgentContinuationLifecycle."""

    try:
        return _TRANSITIONS[(state, event_type)]
    except KeyError as exc:
        raise InvalidContinuationTransition(
            f"continuation transition is not admitted: {state!r} + {event_type!r}"
        ) from exc


def derive_deadline_utc(confirmed_at: str, wall_clock_seconds: int) -> str:
    """Derive the frozen UTC deadline from confirmation authority only."""

    if not isinstance(confirmed_at, str) or not confirmed_at:
        raise ContinuationAuthorityError("confirmed_at must be a UTC timestamp")
    if isinstance(wall_clock_seconds, bool) or not isinstance(wall_clock_seconds, int):
        raise ContinuationAuthorityError("wall_clock_seconds must be an integer")
    if wall_clock_seconds < 0:
        raise ContinuationAuthorityError("wall_clock_seconds cannot be negative")
    normalized = confirmed_at[:-1] + "+00:00" if confirmed_at.endswith("Z") else confirmed_at
    try:
        value = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ContinuationAuthorityError("confirmed_at is not an ISO timestamp") from exc
    if value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise ContinuationAuthorityError("confirmed_at must carry the UTC timezone")
    try:
        deadline = value.astimezone(timezone.utc) + timedelta(seconds=wall_clock_seconds)
    except (OverflowError, ValueError) as exc:
        raise ContinuationAuthorityError("confirmed deadline overflows UTC") from exc
    return deadline.isoformat()


def require_exact_zero_official_facts(
    facts: Iterable[Mapping[str, Any]], expected_source_message_ids: tuple[str, str]
) -> tuple[str, str]:
    """Admit only the pre-CONT-002 state where neither mapped output is official."""

    rows = tuple(facts)
    if len(expected_source_message_ids) != 2 or len(set(expected_source_message_ids)) != 2:
        raise ContinuationAuthorityError("confirmed source-message identities are not exact")
    if rows:
        raise ContinuationMixedSourceState(
            "official continuation inputs require CONT-002 resolution"
        )
    return expected_source_message_ids


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContinuationAuthorityError(f"{label} must be a non-empty string")
    return value


def _require_digest(value: Any, label: str) -> str:
    value = _require_text(value, label)
    if not value.startswith("sha256:") or len(value) != 71:
        raise ContinuationAuthorityError(f"{label} must be a sha256 digest")
    try:
        int(value[7:], 16)
    except ValueError as exc:
        raise ContinuationAuthorityError(f"{label} must be a sha256 digest") from exc
    return value


def _require_policy_ref(value: Any) -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != {"digest", "name", "version"}:
        raise ContinuationAuthorityError("resume policy reference is invalid")
    return {
        "digest": _require_digest(value["digest"], "resume_policy_ref.digest"),
        "name": _require_text(value["name"], "resume_policy_ref.name"),
        "version": _require_text(value["version"], "resume_policy_ref.version"),
    }


@dataclass(frozen=True)
class SuspensionProjection:
    confirmed_authority_digest: str
    dispatch_id: str
    continuation_id: str
    source_attempt_id: str
    source_turn_ordinal: int
    target_turn_ordinal: int
    seat_id: str
    agent_instance_id: str
    ordered_mappings: tuple[dict[str, Any], dict[str, Any]]
    context_snapshot_artifact_id: str
    context_snapshot_content_hash: str
    provider_continuation_ref_digest: str | None
    resume_policy_ref: dict[str, str]
    deadline_utc: str

    @property
    def ordered_mapping_ids(self) -> tuple[str, str]:
        return tuple(mapping["mapping_id"] for mapping in self.ordered_mappings)  # type: ignore[return-value]

    def semantic_intent(self) -> dict[str, Any]:
        return {
            "agent_instance_id": self.agent_instance_id,
            "confirmed_authority_digest": self.confirmed_authority_digest,
            "context_snapshot_artifact_id": self.context_snapshot_artifact_id,
            "context_snapshot_content_hash": self.context_snapshot_content_hash,
            "continuation_id": self.continuation_id,
            "deadline_utc": self.deadline_utc,
            "dispatch_id": self.dispatch_id,
            "ordered_awaited_mapping_ids": list(self.ordered_mapping_ids),
            "ordered_input_mapping_ids": list(self.ordered_mapping_ids),
            "provider_continuation_ref_digest": self.provider_continuation_ref_digest,
            "resume_policy_ref": self.resume_policy_ref,
            "seat_id": self.seat_id,
            "source_attempt_id": self.source_attempt_id,
            "source_turn_ordinal": self.source_turn_ordinal,
        }

    def event_payload(self) -> dict[str, Any]:
        return {
            **self.semantic_intent(),
            "schema": "aci.continuation-suspended@1",
            "state": "suspended",
            "target_turn_ordinal": self.target_turn_ordinal,
            "version": 1,
        }

    def next_state(self) -> dict[str, Any]:
        return {
            "continuation_id": self.continuation_id,
            "deadline_utc": self.deadline_utc,
            "dispatch_id": self.dispatch_id,
            "state": reduce_continuation(None, "continuation.suspended"),
        }


def project_suspension(
    *,
    confirmed_authority_digest: Any,
    dispatch_id: Any,
    continuation_id: Any,
    source_attempt_id: Any,
    source_turn_ordinal: Any,
    target_turn_ordinal: Any,
    seat_id: Any,
    agent_instance_id: Any,
    mappings: Iterable[Mapping[str, Any]],
    context_snapshot_artifact_id: Any,
    context_snapshot_content_hash: Any,
    provider_continuation_ref_digest: Any,
    resume_policy_ref: Any,
    confirmed_at: Any,
    wall_clock_seconds: Any,
) -> SuspensionProjection:
    """Build the closed suspension projection from already-read authority."""

    dispatch_id = _require_text(dispatch_id, "dispatch_id")
    continuation_id = _require_text(continuation_id, "continuation_id")
    source_attempt_id = _require_text(source_attempt_id, "source_attempt_id")
    seat_id = _require_text(seat_id, "seat_id")
    agent_instance_id = _require_text(agent_instance_id, "agent_instance_id")
    if isinstance(source_turn_ordinal, bool) or not isinstance(source_turn_ordinal, int):
        raise ContinuationAuthorityError("source_turn_ordinal must be an integer")
    if target_turn_ordinal != source_turn_ordinal + 1:
        raise ContinuationAuthorityError("target turn is not the next bounded turn")

    ordered = tuple(dict(mapping) for mapping in mappings)
    if len(ordered) != 2:
        raise ContinuationAuthorityError("exactly two continuation mappings are required")
    for ordinal, mapping in enumerate(ordered):
        if mapping.get("slot_ordinal") != ordinal:
            raise ContinuationAuthorityError("continuation mapping order differs")
        if mapping.get("dispatch_id") != dispatch_id:
            raise ContinuationAuthorityError("continuation mapping dispatch differs")
        if mapping.get("continuation_id") != continuation_id:
            raise ContinuationAuthorityError("continuation mapping identity differs")
        if mapping.get("target_seat_id") != seat_id:
            raise ContinuationAuthorityError("continuation mapping target seat differs")
        if mapping.get("target_turn_ordinal") != target_turn_ordinal:
            raise ContinuationAuthorityError("continuation mapping target turn differs")
        _require_text(mapping.get("mapping_id"), "mapping_id")
        _require_digest(mapping.get("confirmed_binding_digest"), "confirmed_binding_digest")
    mapping_ids = tuple(mapping["mapping_id"] for mapping in ordered)
    if len(set(mapping_ids)) != 2:
        raise ContinuationAuthorityError("continuation mapping identities differ")

    provider_digest = None
    if provider_continuation_ref_digest is not None:
        provider_digest = _require_digest(
            provider_continuation_ref_digest,
            "provider_continuation_ref_digest",
        )
    return SuspensionProjection(
        confirmed_authority_digest=_require_digest(
            confirmed_authority_digest, "confirmed_authority_digest"
        ),
        dispatch_id=dispatch_id,
        continuation_id=continuation_id,
        source_attempt_id=source_attempt_id,
        source_turn_ordinal=source_turn_ordinal,
        target_turn_ordinal=target_turn_ordinal,
        seat_id=seat_id,
        agent_instance_id=agent_instance_id,
        ordered_mappings=(ordered[0], ordered[1]),
        context_snapshot_artifact_id=_require_text(
            context_snapshot_artifact_id, "context_snapshot_artifact_id"
        ),
        context_snapshot_content_hash=_require_digest(
            context_snapshot_content_hash, "context_snapshot_content_hash"
        ),
        provider_continuation_ref_digest=provider_digest,
        resume_policy_ref=_require_policy_ref(resume_policy_ref),
        deadline_utc=derive_deadline_utc(confirmed_at, wall_clock_seconds),
    )


def restore_suspension(
    *,
    confirmed_authority_digest: Any,
    dispatch_id: Any,
    continuation_id: Any,
    source_attempt_id: Any,
    source_turn_ordinal: Any,
    target_turn_ordinal: Any,
    seat_id: Any,
    agent_instance_id: Any,
    mappings: Iterable[Mapping[str, Any]],
    context_snapshot_artifact_id: Any,
    context_snapshot_content_hash: Any,
    provider_continuation_ref_digest: Any,
    resume_policy_ref: Any,
    deadline_utc: Any,
) -> SuspensionProjection:
    """Rebuild a command projection from the accepted continuation bytes."""

    deadline = _require_text(deadline_utc, "deadline_utc")
    if derive_deadline_utc(deadline, 0) != deadline:
        raise ContinuationAuthorityError("persisted continuation deadline is not canonical UTC")
    projection = project_suspension(
        confirmed_authority_digest=confirmed_authority_digest,
        dispatch_id=dispatch_id,
        continuation_id=continuation_id,
        source_attempt_id=source_attempt_id,
        source_turn_ordinal=source_turn_ordinal,
        target_turn_ordinal=target_turn_ordinal,
        seat_id=seat_id,
        agent_instance_id=agent_instance_id,
        mappings=mappings,
        context_snapshot_artifact_id=context_snapshot_artifact_id,
        context_snapshot_content_hash=context_snapshot_content_hash,
        provider_continuation_ref_digest=provider_continuation_ref_digest,
        resume_policy_ref=resume_policy_ref,
        confirmed_at=deadline,
        wall_clock_seconds=0,
    )
    return projection
