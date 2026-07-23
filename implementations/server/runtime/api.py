"""Intent-only HTTP surface; production composition keeps its serve gate closed."""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any

from fastapi import APIRouter, Header, HTTPException, Query

from .errors import AuthorizationError, RuntimeContractError, ValidationError
from .provenance import ProvenanceService
from .service import RuntimeService


def _bearer(value: str) -> str:
    if not value.startswith("Bearer ") or not value[7:]:
        raise AuthorizationError("Bearer capability required")
    return value[7:]


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
            return runtime.link_session_dispatch(
                session_id=context.context["session_id"],
                dispatch_id=intent["dispatch_id"],
                idempotency_key=intent.get("idempotency_key", "link"),
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
            if not isinstance(origin_digest, str):
                raise AuthorizationError("host-derived session origin is required")
            return runtime.ensure_session(
                origin_digest=origin_digest,
                name=intent["name"],
                idempotency_key=idempotency_key,
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
            return runtime.link_session_dispatch(
                session_id=session_id,
                dispatch_id=intent["dispatch_id"],
                idempotency_key=idempotency_key,
            )

        return call(execute)

    @router.post("/dispatches/{repo_id}/{dispatch_id}/research")
    def append_research(
        repo_id: str,
        dispatch_id: str,
        intent: dict[str, Any],
        authorization: Annotated[str, Header(alias="Authorization")],
        idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    ) -> dict[str, Any]:
        runtime, provenance = services()

        def execute():
            if repo_id != runtime.settings.repo_id:
                raise ValidationError("repository is outside this runtime")
            return provenance.append_research_submission(
                token=_bearer(authorization),
                dispatch_id=dispatch_id,
                idempotency_key=idempotency_key,
                intent=intent,
            )

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
            return runtime.get_session(session_id)

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
