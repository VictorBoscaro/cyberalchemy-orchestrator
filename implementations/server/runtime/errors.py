"""Closed runtime error vocabulary used at trusted boundaries."""


class RuntimeContractError(Exception):
    code = "RUNTIME_CONTRACT_ERROR"


class ValidationError(RuntimeContractError):
    code = "VALIDATION_ERROR"


class AuthorizationError(RuntimeContractError):
    code = "AUTHORIZATION_DENIED"


class ConflictError(RuntimeContractError):
    code = "CONFLICT"


class IdempotencyConflict(ConflictError):
    code = "IDEMPOTENCY_CONFLICT"


class VersionConflict(ConflictError):
    code = "VERSION_CONFLICT"


class IntegrityError(RuntimeContractError):
    code = "READ_INTEGRITY_FAILURE"


class NotFoundError(RuntimeContractError):
    code = "NOT_FOUND"


class GateBlockedError(RuntimeContractError):
    code = "LOCAL_PILOT_SERVE_BLOCKED"


class ConfirmationContractError(ValidationError):
    """Fail-closed error whose code is part of confirmation authority v1."""


class LegacyAuthorityMode(ConfirmationContractError):
    code = "legacy_authority_mode"


class PendingSheetDigestMismatch(ConfirmationContractError):
    code = "pending_sheet_digest_mismatch"


class DispatchSpecDigestMismatch(ConfirmationContractError):
    code = "dispatch_spec_digest_mismatch"


class UntrustedConfirmationIssuer(ConfirmationContractError):
    code = "untrusted_confirmation_issuer"


class UntrustedConfirmationObservation(ConfirmationContractError):
    code = "untrusted_confirmation_observation"


class ConfirmationObservationScopeMismatch(ConfirmationContractError):
    code = "confirmation_observation_scope_mismatch"


class ConfirmationObservationConflict(ConflictError):
    code = "confirmation_observation_conflict"


class InvalidBoundedGraph(ConfirmationContractError):
    code = "invalid_bounded_graph"


class ConfirmationProjectionMismatch(ConfirmationContractError):
    code = "confirmation_projection_mismatch"


class DerivedIdentityMismatch(ConfirmationContractError):
    code = "derived_identity_mismatch"


class IdentityDerivationMismatch(ConfirmationContractError):
    code = "identity_derivation_mismatch"


class ConfirmationPayloadSchemaMismatch(ConfirmationContractError):
    code = "confirmation_payload_schema_mismatch"


class ConfirmationSchemaVersionsMismatch(ConfirmationContractError):
    code = "confirmation_schema_versions_mismatch"


class ConfirmedAuthorityConflict(ConflictError):
    code = "confirmed_authority_conflict"


class ForbiddenEffectBoundary(ConfirmationContractError):
    code = "forbidden_effect_boundary"


class ContinuationContractError(ValidationError):
    """Fail-closed error for the bounded continuation consumer contract."""


class ContinuationAuthorityError(ContinuationContractError):
    code = "continuation_authority_invalid"


class ContinuationPrerequisiteError(ContinuationContractError):
    code = "continuation_prerequisite_invalid"


class ContinuationMixedSourceState(ContinuationContractError):
    code = "continuation_mixed_source_state"


class InvalidContinuationTransition(ContinuationContractError):
    code = "invalid_continuation_transition"


class RunGroupContractError(ValidationError):
    """Fail-closed error for the pure Run/Group component contract."""


class InvalidRunTransition(RunGroupContractError):
    code = "invalid_run_transition"


class InvalidGroupTransition(RunGroupContractError):
    code = "invalid_group_transition"


class RunGroupGuardError(RunGroupContractError):
    code = "run_group_guard_invalid"


class RunGroupFenceClosed(RunGroupContractError):
    code = "run_group_fence_closed"


class RunGroupHeadConflict(VersionConflict):
    code = "run_group_head_conflict"
