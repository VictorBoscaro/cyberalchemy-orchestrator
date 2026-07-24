"""Intent-only HTTP surface; production composition keeps its serve gate closed."""

from __future__ import annotations

import base64
import binascii
from collections.abc import Callable
from typing import Annotated, Any

from fastapi import APIRouter, Header, HTTPException, Query, Response

from .errors import AuthorizationError, RuntimeContractError, ValidationError
from .provenance import ProvenanceService
from .service import RuntimeService


def _bearer(value: str) -> str:
    if not value.startswith("Bearer ") or not value[7:]:
        raise AuthorizationError("Bearer capability required")
    return value[7:]


def _require_authority_evidence(
    context: dict[str, Any], *, references: tuple[str, ...], digests: tuple[str, ...]
) -> None:
    for field in references:
        value = context.get(field)
        if not isinstance(value, str) or not value:
            raise AuthorizationError(f"{field} is required")
    for field in digests:
        value = context.get(field)
        if not (
            isinstance(value, str)
            and value.startswith("sha256:")
            and len(value) == 71
            and all(character in "0123456789abcdef" for character in value[7:])
        ):
            raise AuthorizationError(f"{field} must be a qualified sha256 digest")


def create_router(
    service_provider: Callable[[], RuntimeService],
    *,
    enabled: Callable[[], bool],
) -> APIRouter:
    router = APIRouter(prefix="/api/runtime", tags=["runtime"])

    def service() -> RuntimeService:
        if not enabled():
            raise HTTPException(
                503,
                detail={
                    "code": "LOCAL_PILOT_SERVE_BLOCKED",
                    "message": "a separate serve-enablement receipt is required",
                },
            )
        return service_provider()

    def call(fn):
        try:
            return fn()
        except RuntimeContractError as exc:
            status = {
                "AUTHORIZATION_DENIED": 403,
                "NOT_FOUND": 404,
                "VALIDATION_ERROR": 400,
                "READ_INTEGRITY_FAILURE": 400,
            }.get(exc.code, 409)
            raise HTTPException(
                status, detail={"code": exc.code, "message": str(exc)}
            ) from exc

    @router.get("/session")
    def session(
        authorization: Annotated[str, Header(alias="Authorization")],
    ) -> dict[str, Any]:
        runtime = service()

        def execute():
            context = runtime.capabilities.resolve(
                _bearer(authorization), action="session.read", phase="observe"
            )
            return runtime.get_session(context.context["session_id"])

        return call(execute)

    @router.post("/dispatch-links")
    def dispatch_link(
        intent: dict[str, Any],
        authorization: Annotated[str, Header(alias="Authorization")],
    ) -> dict[str, Any]:
        runtime = service()

        def execute():
            if set(intent) - {"dispatch_id", "idempotency_key"}:
                raise ValidationError("dispatch-link body contains non-intent fields")
            context = runtime.capabilities.resolve(
                _bearer(authorization), action="dispatch.link", phase="bootstrap"
            )
            _require_authority_evidence(
                context.context,
                references=(
                    "authorization_policy_ref",
                    "authorization_evidence_ref",
                ),
                digests=(
                    "authorization_policy_digest",
                    "authorization_evidence_digest",
                ),
            )
            return runtime.link_session_dispatch(
                session_id=context.context["session_id"],
                dispatch_id=intent["dispatch_id"],
                idempotency_key=intent.get("idempotency_key", "link"),
                actor_ref=context.principal_id,
                authorization_policy_ref=context.context[
                    "authorization_policy_ref"
                ],
                authorization_policy_digest=context.context[
                    "authorization_policy_digest"
                ],
                authorization_evidence_ref=context.context[
                    "authorization_evidence_ref"
                ],
                authorization_evidence_digest=context.context[
                    "authorization_evidence_digest"
                ],
            )

        return call(execute)

    @router.post("/bus/publications")
    def publish(
        intent: dict[str, Any],
        authorization: Annotated[str, Header(alias="Authorization")],
    ) -> dict[str, Any]:
        runtime = service()
        return call(lambda: runtime.publish(_bearer(authorization), intent))

    @router.post("/bus/publications/verify")
    def verify(
        intent: dict[str, Any],
        authorization: Annotated[str, Header(alias="Authorization")],
    ) -> dict[str, Any]:
        runtime = service()

        def execute():
            if set(intent) != {"publication_receipt"}:
                raise ValidationError("verify body must contain only publication_receipt")
            return runtime.verify_publication(
                _bearer(authorization), intent["publication_receipt"]
            )

        return call(execute)

    @router.post("/scouts")
    def start_scout(
        intent: dict[str, Any],
        authorization: Annotated[str, Header(alias="Authorization")],
        idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    ) -> dict[str, Any]:
        runtime = service()
        expected = {
            "session_id",
            "dispatch_id",
            "objective_ref",
            "shape",
            "source_mode",
            "seat_id",
            "attempt_id",
            "operation_id",
        }
        if set(intent) != expected:
            return call(
                lambda: (_ for _ in ()).throw(
                    ValidationError("Scout start intent field set is invalid")
                )
            )
        return call(
            lambda: runtime.start_reference_scout(
                token=_bearer(authorization),
                idempotency_key=idempotency_key,
                **intent,
            )
        )

    @router.post("/scouts/{scout_run_id}/commit")
    def commit_scout(
        scout_run_id: str,
        intent: dict[str, Any],
        authorization: Annotated[str, Header(alias="Authorization")],
        idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    ) -> dict[str, Any]:
        if intent:
            return call(
                lambda: (_ for _ in ()).throw(
                    ValidationError("Scout commit body must be empty")
                )
            )
        return call(
            lambda: service().commit_reference_scout(
                token=_bearer(authorization),
                scout_run_id=scout_run_id,
                idempotency_key=idempotency_key,
            )
        )

    @router.post("/scouts/{scout_run_id}/deliver")
    def deliver_scout(
        scout_run_id: str,
        intent: dict[str, Any],
        authorization: Annotated[str, Header(alias="Authorization")],
        idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    ) -> dict[str, Any]:
        if intent:
            return call(
                lambda: (_ for _ in ()).throw(
                    ValidationError("Scout delivery body must be empty")
                )
            )
        return call(
            lambda: service().deliver_reference_scout(
                token=_bearer(authorization),
                scout_run_id=scout_run_id,
                idempotency_key=idempotency_key,
            )
        )

    @router.post("/scouts/{scout_run_id}/terminate")
    def terminate_scout(
        scout_run_id: str,
        intent: dict[str, Any],
        authorization: Annotated[str, Header(alias="Authorization")],
        idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    ) -> dict[str, Any]:
        if set(intent) != {"outcome", "reason"}:
            return call(
                lambda: (_ for _ in ()).throw(
                    ValidationError("Scout termination body is invalid")
                )
            )
        return call(
            lambda: service().terminate_reference_scout(
                token=_bearer(authorization),
                scout_run_id=scout_run_id,
                outcome=intent["outcome"],
                reason=intent["reason"],
                idempotency_key=idempotency_key,
            )
        )

    @router.get("/scouts/{scout_run_id}")
    def get_scout(
        scout_run_id: str,
        authorization: Annotated[str, Header(alias="Authorization")],
    ) -> dict[str, Any]:
        runtime = service()

        def execute():
            context = runtime.capabilities.resolve(
                _bearer(authorization), action="scout.read", phase="observe"
            )
            if context.context.get("scout_run_id") != scout_run_id:
                raise AuthorizationError("Scout read scope mismatch")
            return runtime.get_reference_scout(scout_run_id)

        return call(execute)

    @router.post("/dispatches/{dispatch_id}/ingestions")
    def record_ingestion(
        dispatch_id: str,
        request: dict[str, Any],
        authorization: Annotated[str, Header(alias="Authorization")],
    ) -> dict[str, Any]:
        runtime = service()

        def execute():
            if set(request) != {"intent", "content_base64"}:
                raise ValidationError("ingestion request field set is invalid")
            intent = request["intent"]
            if not isinstance(intent, dict):
                raise ValidationError("ingestion intent must be an object")
            context = runtime.capabilities.resolve(
                _bearer(authorization), action="ingestion.record", phase="observe"
            )
            if context.context.get("dispatch_id") != dispatch_id:
                raise AuthorizationError("ingestion dispatch path scope mismatch")
            encoded = request["content_base64"]
            if encoded is None:
                content = None
            elif isinstance(encoded, str):
                try:
                    content = base64.b64decode(encoded, validate=True)
                except (ValueError, binascii.Error) as exc:
                    raise ValidationError("ingestion content is not valid base64") from exc
            else:
                raise ValidationError("ingestion content_base64 is invalid")
            return runtime.record_dispatch_ingestion(
                token=_bearer(authorization), intent=intent, content=content
            )

        return call(execute)

    @router.get("/dispatches/{dispatch_id}/lineage")
    def dispatch_lineage(
        dispatch_id: str,
        authorization: Annotated[str, Header(alias="Authorization")],
    ) -> dict[str, Any]:
        runtime = service()

        def execute():
            context = runtime.capabilities.resolve(
                _bearer(authorization), action="dispatch.read", phase="observe"
            )
            if context.context.get("dispatch_id") != dispatch_id:
                raise AuthorizationError("dispatch read scope mismatch")
            return runtime.get_dispatch_operational_lineage(dispatch_id)

        return call(execute)

    @router.get("/events")
    def events(
        authorization: Annotated[str, Header(alias="Authorization")],
        after: int = Query(0, ge=0),
        through: int | None = Query(None, ge=0),
    ) -> dict[str, Any]:
        runtime = service()

        def execute():
            runtime.capabilities.resolve(
                _bearer(authorization), action="events.read", phase="observe"
            )
            return runtime.journal.read_complete_groups(after=after, through=through)

        return call(execute)

    @router.get("/artifacts/{artifact_id}")
    def artifact(
        artifact_id: str,
        authorization: Annotated[str, Header(alias="Authorization")],
    ):
        from fastapi.responses import Response

        runtime = service()

        def execute():
            context = runtime.capabilities.resolve(
                _bearer(authorization), action="artifact.read", phase="collect"
            )
            body = runtime.artifacts.get_authorized(
                artifact_id,
                principal_id=context.principal_id,
                action="artifact.read",
                authorizer=lambda principal, action, classification: (
                    principal == context.principal_id
                    and action == "artifact.read"
                    and classification
                    in {"runtime-internal", "sensitive-output", "public"}
                ),
            )
            return Response(body, media_type="application/octet-stream")

        return call(execute)

    @router.get("/projections/{name}/{key}")
    def projection(
        name: str,
        key: str,
        authorization: Annotated[str, Header(alias="Authorization")],
    ) -> dict[str, Any]:
        runtime = service()

        def execute():
            runtime.capabilities.resolve(
                _bearer(authorization), action="projection.read", phase="observe"
            )
            return runtime.projections.get(name, key)

        return call(execute)

    return router


def create_provenance_router(
    service_provider: Callable[[], RuntimeService],
    *,
    enabled: Callable[[], bool],
) -> APIRouter:
    """Frozen intent-only APT surface; production composition keeps it gated."""
    router = APIRouter(prefix="/api/provenance", tags=["provenance"])

    def services() -> tuple[RuntimeService, ProvenanceService]:
        if not enabled():
            raise HTTPException(
                503,
                detail={
                    "code": "LOCAL_PILOT_SERVE_BLOCKED",
                    "message": "a separate serve-enablement receipt is required",
                },
            )
        runtime = service_provider()
        return runtime, ProvenanceService(runtime)

    def call(fn):
        try:
            return fn()
        except RuntimeContractError as exc:
            status = {
                "AUTHORIZATION_DENIED": 403,
                "NOT_FOUND": 404,
                "VALIDATION_ERROR": 400,
                "READ_INTEGRITY_FAILURE": 400,
                "PROJECTION_LAG": 503,
            }.get(exc.code, 409)
            raise HTTPException(
                status, detail={"code": exc.code, "message": str(exc)}
            ) from exc

    @router.post("/sessions/ensure")
    def ensure_session(
        intent: dict[str, Any],
        authorization: Annotated[str, Header(alias="Authorization")],
        idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    ) -> dict[str, Any]:
        runtime, _ = services()

        def execute():
            if set(intent) != {"name"}:
                raise ValidationError("ensure-session intent field set is invalid")
            context = runtime.capabilities.resolve(
                _bearer(authorization), action="session.ensure", phase="bootstrap"
            )
            origin_digest = context.context.get("origin_digest")
            if (
                not isinstance(origin_digest, str)
            ):
                raise AuthorizationError("host-derived session origin is required")
            _require_authority_evidence(
                context.context,
                references=("actor_authentication_ref",),
                digests=("actor_authentication_digest",),
            )
            return runtime.ensure_session(
                origin_digest=origin_digest,
                name=intent["name"],
                idempotency_key=idempotency_key,
                actor_ref=context.principal_id,
                actor_authentication_ref=context.context["actor_authentication_ref"],
                actor_authentication_digest=context.context[
                    "actor_authentication_digest"
                ],
            )

        return call(execute)

    @router.post("/sessions/{session_id}/dispatches")
    def link_dispatch(
        session_id: str,
        intent: dict[str, Any],
        authorization: Annotated[str, Header(alias="Authorization")],
        idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    ) -> dict[str, Any]:
        runtime, _ = services()

        def execute():
            if set(intent) != {"dispatch_id"}:
                raise ValidationError("dispatch-link intent field set is invalid")
            context = runtime.capabilities.resolve(
                _bearer(authorization), action="dispatch.link", phase="bootstrap"
            )
            if context.context.get("session_id") != session_id:
                raise AuthorizationError("session link scope mismatch")
            _require_authority_evidence(
                context.context,
                references=(
                    "authorization_policy_ref",
                    "authorization_evidence_ref",
                ),
                digests=(
                    "authorization_policy_digest",
                    "authorization_evidence_digest",
                ),
            )
            return runtime.link_session_dispatch(
                session_id=session_id,
                dispatch_id=intent["dispatch_id"],
                idempotency_key=idempotency_key,
                actor_ref=context.principal_id,
                authorization_policy_ref=context.context[
                    "authorization_policy_ref"
                ],
                authorization_policy_digest=context.context[
                    "authorization_policy_digest"
                ],
                authorization_evidence_ref=context.context[
                    "authorization_evidence_ref"
                ],
                authorization_evidence_digest=context.context[
                    "authorization_evidence_digest"
                ],
            )

        return call(execute)

    @router.post("/sessions/start-new")
    def start_new_session(
        intent: dict[str, Any],
        authorization: Annotated[str, Header(alias="Authorization")],
        idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    ) -> dict[str, Any]:
        runtime, _ = services()
        if set(intent) != {"name", "expected_current_session_id"}:
            return call(
                lambda: (_ for _ in ()).throw(
                    ValidationError("start-new intent field set is invalid")
                )
            )
        return call(
            lambda: runtime.start_new_session(
                token=_bearer(authorization),
                name=intent["name"],
                expected_current_session_id=intent["expected_current_session_id"],
                idempotency_key=idempotency_key,
            )
        )

    @router.post("/dispatches/{repo_id}/{dispatch_id}/research")
    def append_research(
        repo_id: str,
        dispatch_id: str,
        intent: dict[str, Any],
        response: Response,
        authorization: Annotated[str, Header(alias="Authorization")],
        idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    ) -> dict[str, Any]:
        runtime, provenance = services()

        def execute():
            if repo_id != runtime.settings.repo_id:
                raise ValidationError("repository is outside this runtime")
            receipt = provenance.append_research_submission(
                token=_bearer(authorization),
                dispatch_id=dispatch_id,
                idempotency_key=idempotency_key,
                intent=intent,
            )
            if receipt.get("projection_status") == "pending":
                response.status_code = 202
            return receipt

        return call(execute)

    @router.get("/sessions/{session_id}")
    def get_session(
        session_id: str,
        authorization: Annotated[str, Header(alias="Authorization")],
    ) -> dict[str, Any]:
        runtime, _ = services()

        def execute():
            context = runtime.capabilities.resolve(
                _bearer(authorization), action="session.read", phase="observe"
            )
            if context.context.get("session_id") != session_id:
                raise AuthorizationError("session read scope mismatch")
            return runtime.projections.get_apt_session(session_id)

        return call(execute)

    @router.get("/dispatches/{repo_id}/{dispatch_id}")
    def get_dispatch(
        repo_id: str,
        dispatch_id: str,
        authorization: Annotated[str, Header(alias="Authorization")],
    ) -> dict[str, Any]:
        runtime, provenance = services()

        def execute():
            if repo_id != runtime.settings.repo_id:
                raise ValidationError("repository is outside this runtime")
            return provenance.get_dispatch(
                token=_bearer(authorization), dispatch_id=dispatch_id
            )

        return call(execute)

    @router.get("/research/{capture_id}")
    def get_research(
        capture_id: str,
        authorization: Annotated[str, Header(alias="Authorization")],
    ) -> dict[str, Any]:
        _, provenance = services()
        return call(
            lambda: provenance.get_research(
                token=_bearer(authorization), capture_id=capture_id
            )
        )

    @router.get("/research/{capture_id}/answer")
    def get_answer(
        capture_id: str,
        authorization: Annotated[str, Header(alias="Authorization")],
    ) -> dict[str, str]:
        _, provenance = services()
        return call(
            lambda: {
                "final_answer": provenance.get_answer(
                    token=_bearer(authorization), capture_id=capture_id
                )
            }
        )

    return router


def create_health_router(
    service_provider: Callable[[], RuntimeService],
    *,
    enabled: Callable[[], bool],
) -> APIRouter:
    router = APIRouter(tags=["runtime-health"])

    @router.get("/api/health")
    def health() -> dict[str, Any]:
        if not enabled():
            raise HTTPException(
                503,
                detail={
                    "code": "LOCAL_PILOT_SERVE_BLOCKED",
                    "message": "a separate serve-enablement receipt is required",
                },
            )
        try:
            return service_provider().health()
        except RuntimeContractError as exc:
            raise HTTPException(
                503, detail={"code": exc.code, "message": str(exc)}
            ) from exc

    return router
