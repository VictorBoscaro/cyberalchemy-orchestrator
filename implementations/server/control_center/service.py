"""Presentation-neutral Phase 1 read models for the Control Center."""

from __future__ import annotations

import hashlib
import base64
import json
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .local_store import LocalControlCenterStore
from .path_engine import find_paths, normalize_edges
from .sources import DispatchSource, SkillGraphSource, SourceSnapshot, pending_items
from .evidence import (
    EvidenceProvider,
    UnavailableEvidenceProvider,
    normalize_evidence,
)

SCHEMA_VERSION = "1"
OWNER = "@VictorBoscaro"
TOPOLOGY_MODELS = {"skill-relations", "dispatch-lineage", "intra-dispatch"}
MODEL_EDGE_KINDS = {
    "skill-relations": {"explicit_path", "named_reference"},
    "dispatch-lineage": {"parent_dispatch_id"},
    "intra-dispatch": {"sequential", "zig-zag", "feedback"},
}
_CURSOR_DOMAIN = b"skill-control-center-catalog-cursor-v1\0"


def _canonical_text(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold().strip()
    return " ".join(text.split())


def _snapshot_id(*parts: str) -> str:
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()
    return f"control-center:{digest[:16]}"


def _cursor_encode(payload: dict[str, Any]) -> str:
    body = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    wrapper = {
        "payload": payload,
        "signature": hashlib.sha256(_CURSOR_DOMAIN + body).hexdigest(),
    }
    encoded = json.dumps(
        wrapper, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return base64.urlsafe_b64encode(encoded).decode("ascii").rstrip("=")


def _cursor_decode(value: str) -> dict[str, Any] | None:
    try:
        padded = value + "=" * (-len(value) % 4)
        wrapper = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
        payload = wrapper["payload"]
        body = json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        expected = hashlib.sha256(_CURSOR_DOMAIN + body).hexdigest()
        if wrapper.get("signature") != expected or not isinstance(payload, dict):
            return None
        return payload
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None


def _parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


class ControlCenterService:
    """Composes frozen skill evidence and live read-only dispatch ledgers."""

    def __init__(
        self,
        *,
        repo_root: Path,
        repos: Iterable[Path],
        store: LocalControlCenterStore | None = None,
        evidence_provider: EvidenceProvider | None = None,
    ) -> None:
        self.repo_root = repo_root
        self.repos = list(repos)
        self.store = store or LocalControlCenterStore()
        self.evidence_provider = evidence_provider or UnavailableEvidenceProvider()
        self.skills = SkillGraphSource(
            repo_root / "experiments" / "skill-relationship-graph" / "graph.json",
            skills_dir=repo_root / ".agents" / "skills",
        )
        self.dispatches = DispatchSource(self.repos)

    def _envelope(
        self,
        request: dict[str, Any],
        *,
        snapshot_id: str | None,
        source_facts: list[dict[str, Any]],
        data: dict[str, Any] | None,
        result_state: str = "complete",
        completeness: str = "complete",
        warnings: list[dict[str, Any] | str] | None = None,
        error_scope: str | None = None,
    ) -> dict[str, Any]:
        return {
            "request_id": str(request.get("request_id") or ""),
            "schema_version": SCHEMA_VERSION,
            "scope_id": str(request.get("scope_id") or ""),
            "snapshot_id": snapshot_id,
            "result_state": result_state,
            "error_scope": error_scope,
            "completeness": completeness,
            "source_facts": source_facts,
            "warnings": warnings or [],
            "data": data,
        }

    def _invalid(
        self,
        request: dict[str, Any],
        *,
        query: str,
        fields: list[str],
        snapshot: SourceSnapshot | None = None,
    ) -> dict[str, Any]:
        return self._envelope(
            request,
            snapshot_id=snapshot.snapshot_id if snapshot else None,
            source_facts=snapshot.source_facts if snapshot else [],
            data={
                "query_state": "invalid-request",
                "query": query,
                "field_errors": sorted(set(fields)),
            },
        )

    def invalid_request(
        self, request: dict[str, Any], *, query: str, fields: list[str]
    ) -> dict[str, Any]:
        """Public parse-boundary adapter for the six HTTP routes."""
        return self._invalid(request, query=query, fields=fields)

    def _common_errors(self, request: dict[str, Any]) -> list[str]:
        errors = [
            key
            for key in ("scope_id", "request_id", "schema_version")
            if not isinstance(request.get(key), str) or not request[key].strip()
        ]
        if request.get("schema_version") not in {None, SCHEMA_VERSION}:
            errors.append("schema_version")
        return errors

    def attention(self, request: dict[str, Any]) -> dict[str, Any]:
        dispatch_snapshot = self.dispatches.read()
        common = self._common_errors(request)
        start = _parse_utc(request.get("window_start_utc"))
        end = _parse_utc(request.get("window_end_utc"))
        limit = request.get("limit", 50)
        if not start:
            common.append("window_start_utc")
        if not end or (start and end <= start):
            common.append("window_end_utc")
        if not isinstance(limit, int) or not 1 <= limit <= 200:
            common.append("limit")
        if common:
            return self._invalid(
                request, query="GetAttentionQueue", fields=common, snapshot=dispatch_snapshot
            )

        items: list[dict[str, Any]] = []
        allowed_kinds = set(request.get("kinds") or [])
        allowed_severity = set(request.get("severity") or [])
        allowed_objects = set(request.get("object_kind") or [])

        def add(item: dict[str, Any]) -> None:
            if allowed_kinds and item["kind"] not in allowed_kinds:
                return
            if allowed_severity and item["severity"] not in allowed_severity:
                return
            if allowed_objects and item["object_kind"] not in allowed_objects:
                return
            occurred = _parse_utc(item.get("occurred_or_detected_at_utc"))
            if occurred and not (start <= occurred < end):
                return
            items.append(item)

        for pending in pending_items(self.repos):
            file_name = pending.get("_file") or "(unknown)"
            add(
                {
                    "object_id": f"{pending.get('_repo')}:{file_name}",
                    "object_kind": "dispatch",
                    "kind": "pending-approval",
                    "severity": "warning",
                    "reason": "Dispatch sheet is pending operator confirmation.",
                    "state": "pending",
                    "scope_id": request["scope_id"],
                    "evidence_ids": [str(pending.get("_path") or file_name)],
                    "safe_next_action": "open-detail",
                    "occurred_or_detected_at_utc": None,
                    "owner": OWNER,
                }
            )
        for row in dispatch_snapshot.nodes:
            if row.get("_state") != "open":
                continue
            add(
                {
                    "object_id": row["_stable_id"],
                    "object_kind": "dispatch",
                    "kind": "blocker",
                    "severity": "info",
                    "reason": "Dispatch has no joined close row.",
                    "state": "open",
                    "scope_id": request["scope_id"],
                    "evidence_ids": [f"{row['_stable_id']}:open"],
                    "safe_next_action": "open-detail",
                    "occurred_or_detected_at_utc": row.get("created"),
                    "owner": OWNER,
                }
            )
        for fact in dispatch_snapshot.source_facts:
            if fact.get("ingestion_state") == "accepted" and not fact.get("warnings"):
                continue
            add(
                {
                    "object_id": fact["source_id"],
                    "object_kind": "source",
                    "kind": "degraded-source",
                    "severity": "warning",
                    "reason": "Source is incomplete or has parser warnings.",
                    "state": fact.get("ingestion_state"),
                    "scope_id": request["scope_id"],
                    "evidence_ids": [fact["source_id"]],
                    "safe_next_action": "open-detail",
                    "occurred_or_detected_at_utc": None,
                    "owner": OWNER,
                }
            )
        severity_rank = {"critical": 0, "warning": 1, "info": 2}
        items.sort(
            key=lambda row: (
                severity_rank[row["severity"]],
                1 if row["occurred_or_detected_at_utc"] is None else 0,
                "" if row["occurred_or_detected_at_utc"] is None else _reverse_time(row["occurred_or_detected_at_utc"]),
                row["object_kind"],
                row["object_id"],
            )
        )
        return self._envelope(
            request,
            snapshot_id=dispatch_snapshot.snapshot_id,
            source_facts=dispatch_snapshot.source_facts,
            result_state="partial" if dispatch_snapshot.completeness == "partial" else "complete",
            completeness=dispatch_snapshot.completeness,
            data={
                "query_state": "success",
                "items": items[:limit],
                "empty_reason": "no-actionable-item" if not items else None,
                "next_cursor": None,
            },
        )

    def _evidence_summary(self, object_kind: str, object_id: str) -> dict[str, Any]:
        try:
            value = self.evidence_provider.summary(object_kind, object_id)
        except Exception:
            value = None
        normalized = normalize_evidence(value)
        return {
            key: normalized[key]
            for key in (
                "evidence_classes",
                "completeness",
                "freshness",
                "logical_invocation_count",
                "exhaustive",
            )
        }

    def _evidence_answer(
        self,
        object_kind: str,
        object_id: str,
        request: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            value = self.evidence_provider.answer(
                object_kind,
                object_id,
                str(request.get("claim_id") or "times-used"),
                request.get("window_start_utc"),
                request.get("window_end_utc"),
            )
        except Exception:
            value = None
        result = normalize_evidence(value)
        result.setdefault(
            "normalized_window",
            {
                "start_utc": request.get("window_start_utc"),
                "end_utc": request.get("window_end_utc"),
                "basis": "UTC",
            },
        )
        result["query_state"] = "success"
        result["owner"] = OWNER
        return result

    def catalog(self, request: dict[str, Any]) -> dict[str, Any]:
        skill_snapshot = self.skills.read()
        dispatch_snapshot = self.dispatches.read()
        common = self._common_errors(request)
        kinds = set(request.get("object_kinds") or [])
        limit = request.get("limit", 50)
        if not kinds or not kinds <= {"skill", "dispatch"}:
            common.append("object_kinds")
        if not isinstance(limit, int) or not 1 <= limit <= 200:
            common.append("limit")
        if common:
            return self._invalid(request, query="SearchCatalog", fields=common)

        needle = _canonical_text(request.get("query", ""))
        filters = request.get("filters") or {}
        normalized_input = {
            "query": needle,
            "object_kinds": sorted(kinds),
            "filters": filters,
        }
        filter_digest = hashlib.sha256(
            json.dumps(
                normalized_input,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        snapshot_id = _snapshot_id(skill_snapshot.snapshot_id, dispatch_snapshot.snapshot_id)
        cursor_payload = None
        if request.get("cursor"):
            cursor_payload = _cursor_decode(str(request["cursor"]))
            query_state = None
            if cursor_payload is None or cursor_payload.get("filter_digest") != filter_digest:
                query_state = "invalid-cursor"
            elif cursor_payload.get("snapshot_id") != snapshot_id:
                query_state = "stale-snapshot"
            elif not isinstance(cursor_payload.get("last_sort_tuple"), list):
                query_state = "invalid-cursor"
            if query_state:
                return self._envelope(
                    request,
                    snapshot_id=snapshot_id,
                    source_facts=[
                        *skill_snapshot.source_facts,
                        *dispatch_snapshot.source_facts,
                    ],
                    data={
                        "query_state": query_state,
                        "matches": [],
                        "active_filters": normalized_input,
                        "no_match": False,
                        "next_cursor": None,
                    },
                )
        matches: list[dict[str, Any]] = []
        if "skill" in kinds:
            for node in skill_snapshot.nodes:
                haystacks = {"label": node["id"], "description": node.get("description", "")}
                matched_fields = [
                    field for field, value in haystacks.items() if needle in _canonical_text(value)
                ]
                if needle and not matched_fields:
                    continue
                matches.append(
                    {
                        "object_id": node["id"],
                        "object_kind": "skill",
                        "display_label": node["id"],
                        "description": node.get("description"),
                        "path": node.get("path"),
                        "status": "available",
                        "matched_fields": matched_fields or ["label"],
                        "evidence_summary": self._evidence_summary("skill", node["id"]),
                        "has_attention": False,
                        "owner": OWNER,
                    }
                )
        if "dispatch" in kinds:
            for row in dispatch_snapshot.nodes:
                label = str(row.get("goal") or row.get("dispatch_id") or "")
                haystacks = {"label": label, "id": row.get("dispatch_id", "")}
                matched_fields = [
                    field for field, value in haystacks.items() if needle in _canonical_text(value)
                ]
                if needle and not matched_fields:
                    continue
                matches.append(
                    {
                        "object_id": row["_stable_id"],
                        "object_kind": "dispatch",
                        "display_label": label,
                        "status": row.get("_state"),
                        "matched_fields": matched_fields or ["label"],
                        "evidence_summary": self._evidence_summary(
                            "dispatch", row["_stable_id"]
                        ),
                        "has_attention": row.get("_state") == "open",
                        "owner": OWNER,
                    }
                )
        if filters.get("status"):
            matches = [m for m in matches if m["status"] in set(filters["status"])]
        if filters.get("freshness"):
            matches = [
                m
                for m in matches
                if m["evidence_summary"]["freshness"] in set(filters["freshness"])
            ]
        if filters.get("evidence_class"):
            matches = [
                m
                for m in matches
                if set(m["evidence_summary"]["evidence_classes"])
                & set(filters["evidence_class"])
            ]
        if filters.get("has_attention") is not None:
            matches = [
                m for m in matches if m["has_attention"] is bool(filters["has_attention"])
            ]
        def sort_key(row: dict[str, Any]) -> tuple[str, str, str]:
            return (
                _canonical_text(row["display_label"]),
                row["object_kind"],
                row["object_id"],
            )
        matches.sort(key=sort_key)
        if cursor_payload is not None:
            last = tuple(str(value) for value in cursor_payload["last_sort_tuple"])
            matches = [row for row in matches if sort_key(row) > last]
        page = matches[:limit]
        next_cursor = None
        if len(matches) > limit and page:
            next_cursor = _cursor_encode(
                {
                    "snapshot_id": snapshot_id,
                    "filter_digest": filter_digest,
                    "last_sort_tuple": list(sort_key(page[-1])),
                }
            )
        selected_snapshots = []
        if "skill" in kinds:
            selected_snapshots.append(skill_snapshot)
        if "dispatch" in kinds:
            selected_snapshots.append(dispatch_snapshot)
        completeness = (
            "unavailable"
            if selected_snapshots
            and all(snapshot.completeness == "unavailable" for snapshot in selected_snapshots)
            else "partial"
            if any(snapshot.completeness != "complete" for snapshot in selected_snapshots)
            else "complete"
        )
        if completeness == "unavailable":
            return self._envelope(
                request,
                snapshot_id=snapshot_id,
                source_facts=[
                    fact
                    for snapshot in selected_snapshots
                    for fact in snapshot.source_facts
                ],
                data=None,
                result_state="unavailable",
                completeness="unavailable",
            )
        exhaustive_absence = completeness == "complete" and not page
        return self._envelope(
            request,
            snapshot_id=snapshot_id,
            source_facts=[
                fact
                for snapshot in selected_snapshots
                for fact in snapshot.source_facts
            ],
            result_state=completeness,
            completeness=completeness,
            data={
                "query_state": "no-match" if exhaustive_absence else "success",
                "matches": page,
                "active_filters": normalized_input,
                "no_match": exhaustive_absence,
                "next_cursor": next_cursor,
            },
        )

    def object_detail(
        self, object_kind: str, object_id: str, request: dict[str, Any]
    ) -> dict[str, Any]:
        common = self._common_errors(request)
        if object_kind not in {"skill", "dispatch"}:
            common.append("object_kind")
        if not object_id:
            common.append("object_id")
        start_value = request.get("window_start_utc")
        end_value = request.get("window_end_utc")
        if bool(start_value) != bool(end_value):
            common.extend(["window_start_utc", "window_end_utc"])
        elif start_value and end_value:
            start = _parse_utc(start_value)
            end = _parse_utc(end_value)
            if not start:
                common.append("window_start_utc")
            if not end or (start and end <= start):
                common.append("window_end_utc")
        if common:
            return self._invalid(request, query="GetObjectDetail", fields=common)

        snapshot = self.skills.read() if object_kind == "skill" else self.dispatches.read()
        if object_kind == "skill":
            row = next((n for n in snapshot.nodes if n["id"] == object_id), None)
            identity = (
                {
                    "object_id": row["id"],
                    "object_kind": "skill",
                    "display_label": row["id"],
                    "description": row.get("description"),
                    "path": row.get("path"),
                    "owner": OWNER,
                }
                if row
                else None
            )
            relations = ["skill-relations"]
        else:
            row = next((n for n in snapshot.nodes if n["_stable_id"] == object_id), None)
            identity = (
                {
                    "object_id": row["_stable_id"],
                    "object_kind": "dispatch",
                    "display_label": row.get("goal") or row.get("dispatch_id"),
                    "dispatch_id": row.get("dispatch_id"),
                    "repo": row.get("_repo"),
                    "status": row.get("_state"),
                    "dispatch_type": row.get("dispatch_type"),
                    "parent_dispatch_id": row.get("parent_dispatch_id"),
                    "owner": OWNER,
                }
                if row
                else None
            )
            relations = ["dispatch-lineage", "intra-dispatch"]
        partial = snapshot.completeness == "partial"
        if not identity and partial:
            return self._envelope(
                request,
                snapshot_id=snapshot.snapshot_id,
                source_facts=snapshot.source_facts,
                data=None,
                result_state="partial",
                completeness="partial",
            )
        state = "partial" if partial else "complete"
        return self._envelope(
            request,
            snapshot_id=snapshot.snapshot_id,
            source_facts=snapshot.source_facts,
            result_state=state,
            completeness=snapshot.completeness,
            data={
                "query_state": "found" if identity else "not-found",
                "identity": identity,
                "source_revision": snapshot.snapshot_id,
                "relations_available": relations if identity else [],
                "evidence": (
                    self._evidence_answer(object_kind, object_id, request)
                    if identity and start_value and end_value
                    else None
                ),
                "safe_actions": (
                    ["open-detail", "open-topology", "edit-local-preference", "edit-draft"]
                    if identity
                    else []
                ),
                "authority_route": "unavailable",
            },
        )

    def _topology_snapshot(
        self, model: str, dispatch_id: str | None = None
    ) -> tuple[SourceSnapshot, list[dict[str, Any]], list[dict[str, Any]]]:
        if model == "skill-relations":
            source = self.skills.read()
            nodes = [
                {
                    "id": row["id"],
                    "display_label": row["id"],
                    "object_kind": "skill",
                    "path": row.get("path"),
                    "owner": OWNER,
                }
                for row in source.nodes
            ]
            edges = []
            for edge in source.edges:
                evidence_values = edge.get("evidence") or ["unknown-evidence"]
                for evidence_id in evidence_values:
                    edges.append(
                        {
                            "source_id": edge["source"],
                            "target_id": edge["target"],
                            "edge_kind": edge["relation"],
                            "label": (
                                "mention"
                                if edge["relation"] == "named_reference"
                                else "explicit path reference"
                            ),
                            "strength": (
                                "weak"
                                if edge["relation"] == "named_reference"
                                else "strong"
                            ),
                            "evidence_id": evidence_id,
                            "evidence_class": "declared",
                            "provenance": source.snapshot_id,
                            "snapshot_id": source.snapshot_id,
                        }
                    )
            return source, nodes, normalize_edges(edges)
        source = self.dispatches.read()
        if model == "dispatch-lineage":
            nodes = [
                {
                    "id": row["_stable_id"],
                    "display_label": row.get("goal") or row.get("dispatch_id"),
                    "object_kind": "dispatch",
                    "status": row.get("_state"),
                    "owner": OWNER,
                }
                for row in source.nodes
            ]
            edges = [
                {
                    "source_id": edge["source"],
                    "target_id": edge["target"],
                    "edge_kind": "parent_dispatch_id",
                    "evidence_id": edge["evidence"][0],
                    "evidence_class": "declared",
                    "provenance": source.snapshot_id,
                    "snapshot_id": source.snapshot_id,
                    "resolved": edge.get("resolved", False),
                }
                for edge in source.edges
            ]
            return source, nodes, normalize_edges(edges)

        selected = next(
            (
                row
                for row in source.nodes
                if row["_stable_id"] == dispatch_id or row.get("dispatch_id") == dispatch_id
            ),
            None,
        )
        groups = selected.get("groups") if isinstance(selected, dict) else []
        connections = selected.get("connections") if isinstance(selected, dict) else []
        identity_prefix = selected["_stable_id"] if selected else str(dispatch_id or "missing")
        nodes = [
            {
                "id": f"{identity_prefix}:{group['group_id']}",
                "group_id": str(group["group_id"]),
                "display_label": str(group["group_id"]),
                "object_kind": "dispatch-group",
                "role": group.get("role"),
                "owner": OWNER,
            }
            for group in (groups or [])
            if isinstance(group, dict) and group.get("group_id")
        ]
        edges = [
            {
                "source_id": f"{identity_prefix}:{edge['from']}",
                "target_id": f"{identity_prefix}:{edge['to']}",
                "edge_kind": str(edge["type"]),
                "evidence_id": f"{selected['_stable_id']}:connection:{index}",
                "evidence_class": "declared",
                "provenance": source.snapshot_id,
                "snapshot_id": source.snapshot_id,
            }
            for index, edge in enumerate(connections or [])
            if isinstance(edge, dict)
            and edge.get("from")
            and edge.get("to")
            and edge.get("type")
        ] if selected else []
        scoped = SourceSnapshot(
            snapshot_id=f"{source.snapshot_id}:{dispatch_id or 'missing'}",
            nodes=[],
            edges=[],
            source_facts=source.source_facts,
            completeness=source.completeness,
        )
        return scoped, nodes, normalize_edges(edges)

    def topology(self, model: str, request: dict[str, Any]) -> dict[str, Any]:
        common = self._common_errors(request)
        if model not in TOPOLOGY_MODELS:
            return self._envelope(
                request,
                snapshot_id=None,
                source_facts=[],
                data={
                    "model": model,
                    "query_state": "unsupported-model",
                    "focus_id": request.get("focus_id"),
                    "nodes": [],
                    "edges": [],
                    "semantic_rows": [],
                    "truncated": False,
                    "more_available": False,
                },
            )
        focus_id = request.get("focus_id")
        direction = request.get("direction", "both")
        depth = request.get("depth", 1)
        node_limit = request.get("node_limit", 200)
        edge_kinds = set(request.get("edge_kinds") or [])
        dispatch_id = request.get("dispatch_id")
        if not isinstance(focus_id, str) or not focus_id:
            common.append("focus_id")
        if direction not in {"outbound", "inbound", "both"}:
            common.append("direction")
        if not isinstance(depth, int) or not 0 <= depth <= 10:
            common.append("depth")
        if not isinstance(node_limit, int) or not 1 <= node_limit <= 1000:
            common.append("node_limit")
        if not edge_kinds or not edge_kinds <= MODEL_EDGE_KINDS[model]:
            common.append("edge_kinds")
        if model == "intra-dispatch" and not dispatch_id:
            common.append("dispatch_id")
        if model != "intra-dispatch" and dispatch_id:
            common.append("dispatch_id")
        snapshot, all_nodes, all_edges = self._topology_snapshot(model, dispatch_id)
        if common:
            return self._invalid(
                request, query="GetTopology", fields=common, snapshot=snapshot
            )
        focus_identity = focus_id
        if model == "intra-dispatch":
            focus_identity = next(
                (
                    row["id"]
                    for row in all_nodes
                    if row.get("group_id") == focus_id or row["id"] == focus_id
                ),
                focus_id,
            )
        node_ids = {row["id"] for row in all_nodes}
        if focus_identity not in node_ids:
            if snapshot.completeness != "complete":
                return self._envelope(
                    request,
                    snapshot_id=snapshot.snapshot_id,
                    source_facts=snapshot.source_facts,
                    data=None,
                    result_state=snapshot.completeness,
                    completeness=snapshot.completeness,
                )
            data = {
                "model": model,
                "query_state": "invalid-endpoint",
                "focus_id": focus_id,
                "nodes": [],
                "edges": [],
                "semantic_rows": [],
                "truncated": False,
                "more_available": False,
            }
            return self._envelope(
                request,
                snapshot_id=snapshot.snapshot_id,
                source_facts=snapshot.source_facts,
                data=data,
            )
        selected_edges = [e for e in all_edges if e["edge_kind"] in edge_kinds]
        visible = {focus_identity}
        frontier = {focus_identity}
        for _ in range(depth):
            next_frontier: set[str] = set()
            for edge in selected_edges:
                if direction in {"outbound", "both"} and edge["source_id"] in frontier:
                    next_frontier.add(edge["target_id"])
                if direction in {"inbound", "both"} and edge["target_id"] in frontier:
                    next_frontier.add(edge["source_id"])
            next_frontier -= visible
            visible |= next_frontier
            frontier = next_frontier
        ordered_visible = [focus_identity, *sorted(visible - {focus_identity})]
        truncated = len(ordered_visible) > node_limit
        selected_ids = set(ordered_visible[:node_limit])
        nodes = sorted(
            (row for row in all_nodes if row["id"] in selected_ids), key=lambda row: row["id"]
        )
        edges = [
            edge
            for edge in selected_edges
            if edge["source_id"] in selected_ids and edge["target_id"] in selected_ids
        ]
        semantic_rows = [
            {
                "row_kind": "node",
                "identity": node["id"],
                "display_label": node["display_label"],
            }
            for node in nodes
        ] + [
            {
                "row_kind": "edge",
                "identity": [
                    edge["source_id"],
                    edge["edge_kind"],
                    edge["evidence_id"],
                    edge["target_id"],
                ],
                "source_id": edge["source_id"],
                "edge_kind": edge["edge_kind"],
                "target_id": edge["target_id"],
            }
            for edge in edges
        ]
        if snapshot.completeness == "partial":
            truncated = True
        return self._envelope(
            request,
            snapshot_id=snapshot.snapshot_id,
            source_facts=snapshot.source_facts,
            result_state="partial" if snapshot.completeness == "partial" else "complete",
            completeness=snapshot.completeness,
            data={
                "model": model,
                "query_state": "truncated" if truncated else "success",
                "focus_id": focus_id,
                "nodes": nodes,
                "edges": edges,
                "semantic_rows": semantic_rows,
                "truncated": truncated,
                "more_available": None if snapshot.completeness != "complete" else truncated,
            },
        )

    def path_query(self, request: dict[str, Any]) -> dict[str, Any]:
        common = self._common_errors(request)
        model = request.get("model")
        if model not in TOPOLOGY_MODELS:
            return self._envelope(
                request,
                snapshot_id=None,
                source_facts=[],
                data={
                    "query_state": "unsupported-model",
                    "paths": [],
                    "applied_limits": {},
                    "returned_depth": None,
                    "more_paths_exist": False,
                },
            )
        source_id = request.get("source_id")
        target_id = request.get("target_id")
        direction = request.get("direction")
        edge_kinds = set(request.get("allowed_edge_kinds") or [])
        max_depth = request.get("max_depth")
        max_paths = request.get("max_paths")
        dispatch_id = request.get("dispatch_id")
        if not isinstance(source_id, str) or not source_id:
            common.append("source_id")
        if not isinstance(target_id, str) or not target_id:
            common.append("target_id")
        if direction not in {"outbound", "inbound", "undirected-view"}:
            common.append("direction")
        if not edge_kinds or not edge_kinds <= MODEL_EDGE_KINDS[model]:
            common.append("allowed_edge_kinds")
        if not isinstance(max_depth, int) or not 0 <= max_depth <= 10:
            common.append("max_depth")
        if not isinstance(max_paths, int) or not 1 <= max_paths <= 100:
            common.append("max_paths")
        if model == "intra-dispatch" and not dispatch_id:
            common.append("dispatch_id")
        if model != "intra-dispatch" and dispatch_id:
            common.append("dispatch_id")
        snapshot, nodes, edges = self._topology_snapshot(model, dispatch_id)
        if common:
            return self._invalid(
                request, query="FindPath", fields=common, snapshot=snapshot
            )
        traversal_source = source_id
        traversal_target = target_id
        if model == "intra-dispatch":
            by_group = {
                row.get("group_id"): row["id"]
                for row in nodes
                if row.get("group_id")
            }
            traversal_source = by_group.get(source_id, source_id)
            traversal_target = by_group.get(target_id, target_id)
        if snapshot.completeness != "complete":
            node_ids = {row["id"] for row in nodes}
            if traversal_source not in node_ids or traversal_target not in node_ids:
                return self._envelope(
                    request,
                    snapshot_id=snapshot.snapshot_id,
                    source_facts=snapshot.source_facts,
                    data=None,
                    result_state=snapshot.completeness,
                    completeness=snapshot.completeness,
                )
        result = find_paths(
            nodes=(row["id"] for row in nodes),
            edges=edges,
            source_id=traversal_source,
            target_id=traversal_target,
            direction=direction,
            allowed_edge_kinds=edge_kinds,
            max_depth=max_depth,
            max_paths=max_paths,
        )
        result["applied_limits"] = {"max_depth": max_depth, "max_paths": max_paths}
        if snapshot.completeness == "partial" and result["query_state"] == "no-path":
            result["query_state"] = "truncated"
            result["more_paths_exist"] = None
        return self._envelope(
            request,
            snapshot_id=snapshot.snapshot_id,
            source_facts=snapshot.source_facts,
            data=result,
            result_state="partial" if snapshot.completeness == "partial" else "complete",
            completeness=snapshot.completeness,
        )

    def _unknown_usage_payload(self, request: dict[str, Any]) -> dict[str, Any]:
        return self._evidence_answer("skill", "", request)

    def evidence(
        self, object_kind: str, object_id: str, request: dict[str, Any]
    ) -> dict[str, Any]:
        common = self._common_errors(request)
        start = _parse_utc(request.get("window_start_utc"))
        end = _parse_utc(request.get("window_end_utc"))
        if object_kind not in {"skill", "dispatch"}:
            common.append("object_kind")
        if not object_id:
            common.append("object_id")
        if not request.get("claim_id"):
            common.append("claim_id")
        if not start:
            common.append("window_start_utc")
        if not end or (start and end <= start):
            common.append("window_end_utc")
        if common:
            return self._invalid(request, query="GetUsageEvidence", fields=common)
        snapshot = self.skills.read() if object_kind == "skill" else self.dispatches.read()
        exists = (
            any(row["id"] == object_id for row in snapshot.nodes)
            if object_kind == "skill"
            else any(row["_stable_id"] == object_id for row in snapshot.nodes)
        )
        if not exists and snapshot.completeness == "complete":
            data = {"query_state": "not-found"}
        elif not exists:
            return self._envelope(
                request,
                snapshot_id=snapshot.snapshot_id,
                source_facts=snapshot.source_facts,
                data=None,
                result_state=snapshot.completeness,
                completeness=snapshot.completeness,
            )
        else:
            data = self._evidence_answer(object_kind, object_id, request)
            source_facts = [*snapshot.source_facts, *data["source_facts"]]
            if data["completeness"] != "unavailable":
                return self._envelope(
                    request,
                    snapshot_id=snapshot.snapshot_id,
                    source_facts=source_facts,
                    data=data,
                    result_state=data["completeness"],
                    completeness=data["completeness"],
                )
            return self._envelope(
                request,
                snapshot_id=snapshot.snapshot_id,
                source_facts=source_facts,
                data=None,
                result_state="unavailable",
                completeness="unavailable",
                warnings=[
                    "Usage is unknown; no accepted invocation telemetry source is configured."
                ],
            )
        return self._envelope(
            request,
            snapshot_id=snapshot.snapshot_id,
            source_facts=snapshot.source_facts,
            data=data,
            completeness=snapshot.completeness,
        )


def _reverse_time(value: str) -> str:
    """Lexically reverse an ISO timestamp for ascending tuple sort."""
    return "".join(chr(0x10FFFF - ord(char)) for char in value)
