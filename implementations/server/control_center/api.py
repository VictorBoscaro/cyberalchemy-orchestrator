"""The closed six-route Phase 1 Control Center read inventory."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse

from .service import ControlCenterService


def _common(
    scope_id: str | None, request_id: str | None, schema_version: str | None
) -> dict[str, Any]:
    return {
        "scope_id": scope_id,
        "request_id": request_id,
        "schema_version": schema_version,
    }


def _http_result(body: dict[str, Any]) -> JSONResponse:
    """Map typed query outcomes to the normative transport status."""
    data = body.get("data") or {}
    query_state = data.get("query_state")
    if query_state in {"invalid-cursor", "stale-snapshot"}:
        status = 409
    elif query_state == "invalid-request":
        status = 422
    elif body.get("result_state") == "error" and body.get("error_scope") in {
        "transport",
        "protocol",
    }:
        status = 500
    else:
        status = 200
    return JSONResponse(status_code=status, content=body)


def _parse_int(value: str | None, default: int) -> tuple[int | str, bool]:
    if value is None:
        return default, False
    try:
        return int(value), False
    except ValueError:
        return value, True


def _parse_bool(value: str | None) -> tuple[bool | str | None, bool]:
    if value is None:
        return None, False
    normalized = value.casefold()
    if normalized in {"true", "1"}:
        return True, False
    if normalized in {"false", "0"}:
        return False, False
    return value, True


def _parse_failure(
    service: ControlCenterService,
    request: dict[str, Any],
    *,
    query: str,
    fields: list[str],
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=service.invalid_request(request, query=query, fields=fields),
    )


def create_router(provider: Callable[[], ControlCenterService]) -> APIRouter:
    router = APIRouter(prefix="/v1/control-center", tags=["skill-control-center"])

    @router.get("/attention")
    def attention(
        scope_id: str | None = None,
        request_id: str | None = None,
        schema_version: str | None = None,
        window_start_utc: str | None = None,
        window_end_utc: str | None = None,
        kinds: list[str] | None = Query(None),
        severity: list[str] | None = Query(None),
        object_kind: list[str] | None = Query(None),
        limit: str | None = None,
    ) -> dict[str, Any]:
        parsed_limit, failed = _parse_int(limit, 50)
        service = provider()
        query_request = {
            **_common(scope_id, request_id, schema_version),
            "window_start_utc": window_start_utc,
            "window_end_utc": window_end_utc,
            "kinds": kinds,
            "severity": severity,
            "object_kind": object_kind,
            "limit": parsed_limit,
        }
        if failed:
            return _parse_failure(
                service, query_request, query="GetAttentionQueue", fields=["limit"]
            )
        return _http_result(service.attention(query_request))

    @router.get("/catalog")
    def catalog(
        scope_id: str | None = None,
        request_id: str | None = None,
        schema_version: str | None = None,
        query: str = "",
        object_kinds: list[str] | None = Query(None),
        status: list[str] | None = Query(None),
        evidence_class: list[str] | None = Query(None),
        freshness: list[str] | None = Query(None),
        has_attention: str | None = None,
        limit: str | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        parsed_limit, limit_failed = _parse_int(limit, 50)
        parsed_attention, attention_failed = _parse_bool(has_attention)
        service = provider()
        query_request = {
            **_common(scope_id, request_id, schema_version),
            "query": query,
            "object_kinds": object_kinds,
            "filters": {
                "status": status or [],
                "evidence_class": evidence_class or [],
                "freshness": freshness or [],
                "has_attention": parsed_attention,
            },
            "limit": parsed_limit,
            "cursor": cursor,
        }
        failed_fields = [
            field
            for field, failed in (
                ("limit", limit_failed),
                ("has_attention", attention_failed),
            )
            if failed
        ]
        if failed_fields:
            return _parse_failure(
                service, query_request, query="SearchCatalog", fields=failed_fields
            )
        return _http_result(service.catalog(query_request))

    @router.get("/objects/{object_kind}/{object_id}")
    def object_detail(
        object_kind: str,
        object_id: str,
        scope_id: str | None = None,
        request_id: str | None = None,
        schema_version: str | None = None,
        window_start_utc: str | None = None,
        window_end_utc: str | None = None,
    ) -> dict[str, Any]:
        return _http_result(provider().object_detail(
            object_kind,
            object_id,
            {
                **_common(scope_id, request_id, schema_version),
                "window_start_utc": window_start_utc,
                "window_end_utc": window_end_utc,
            },
        ))

    @router.get("/topology/{model}")
    def topology(
        model: str,
        focus_id: str | None = None,
        dispatch_id: str | None = None,
        direction: str = "both",
        depth: str | None = None,
        edge_kinds: list[str] | None = Query(None),
        node_limit: str | None = None,
        scope_id: str | None = None,
        request_id: str | None = None,
        schema_version: str | None = None,
    ) -> dict[str, Any]:
        parsed_depth, depth_failed = _parse_int(depth, 1)
        parsed_limit, limit_failed = _parse_int(node_limit, 200)
        service = provider()
        query_request = {
            **_common(scope_id, request_id, schema_version),
            "focus_id": focus_id,
            "dispatch_id": dispatch_id,
            "direction": direction,
            "depth": parsed_depth,
            "edge_kinds": edge_kinds,
            "node_limit": parsed_limit,
        }
        failed_fields = [
            field
            for field, failed in (
                ("depth", depth_failed),
                ("node_limit", limit_failed),
            )
            if failed
        ]
        if failed_fields:
            return _parse_failure(
                service, query_request, query="GetTopology", fields=failed_fields
            )
        return _http_result(service.topology(model, query_request))

    @router.post("/path-query")
    async def path_query(request: Request) -> dict[str, Any]:
        service = provider()
        try:
            payload = await request.json()
        except (ValueError, UnicodeDecodeError):
            return _parse_failure(
                service, {}, query="FindPath", fields=["request_body"]
            )
        if not isinstance(payload, dict):
            return _parse_failure(
                service, {}, query="FindPath", fields=["request_body"]
            )
        return _http_result(service.path_query(payload))

    @router.get("/evidence/{object_kind}/{object_id}")
    def evidence(
        object_kind: str,
        object_id: str,
        scope_id: str | None = None,
        request_id: str | None = None,
        schema_version: str | None = None,
        claim_id: str | None = None,
        window_start_utc: str | None = None,
        window_end_utc: str | None = None,
    ) -> dict[str, Any]:
        return _http_result(provider().evidence(
            object_kind,
            object_id,
            {
                **_common(scope_id, request_id, schema_version),
                "claim_id": claim_id,
                "window_start_utc": window_start_utc,
                "window_end_utc": window_end_utc,
            },
        ))

    return router
