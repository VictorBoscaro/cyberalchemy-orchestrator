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
