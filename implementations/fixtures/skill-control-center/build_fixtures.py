"""Build the deterministic Phase 1 Control Center fixture corpus."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from implementations.server.control_center.fixtures import fixture_digest

OUTPUT = Path(__file__).resolve().parent
GENERATED_AT = "2026-07-25T00:00:00Z"
SCHEMA = "1"


def base(fixture_id: str, source_revision: str) -> dict[str, Any]:
    return {
        "fixture_id": fixture_id,
        "schema_version": SCHEMA,
        "source_revision": source_revision,
        "generated_at_utc": GENERATED_AT,
    }


def state_case(state_id: str, *, producer: str, representation: str) -> dict[str, Any]:
    case = {
        "case_id": f"state-{state_id}",
        "state_id": state_id,
        "test_id": f"cc-state-{state_id}",
        "producer": producer,
        "required_representation": representation,
    }
    case["sha256"] = fixture_digest(case)
    return case


def write(name: str, fixture: dict[str, Any]) -> dict[str, Any]:
    fixture["sha256"] = fixture_digest(fixture)
    path = OUTPUT / name
    path.write_text(
        json.dumps(fixture, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    entry = {
        "fixture_id": fixture["fixture_id"],
        "schema_version": fixture["schema_version"],
        "path": name,
        "sha256": fixture["sha256"],
    }
    entry["cases"] = [
        {"case_id": case["case_id"], "sha256": case["sha256"]}
        for case in fixture.get("state_cases", [])
    ]
    return entry


def skill_fixture() -> dict[str, Any]:
    source_path = REPO_ROOT / "experiments" / "skill-relationship-graph" / "graph.json"
    source = json.loads(source_path.read_text(encoding="utf-8-sig"))
    fixture = base("FX-SKILL-TOPOLOGY-v1", source["schema_version"])
    fixture.update(
        nodes=source["nodes"],
        edges=source["edges"],
        expected_counts={
            "nodes": 72,
            "edges": 261,
            "explicit_path": 7,
            "named_reference": 254,
        },
        owner="@VictorBoscaro",
        state_cases=[
            state_case(
                "focal-lineage",
                producer="explicit-topology-success",
                representation="model/focus and graph/table identity parity",
            ),
            state_case(
                "invalid-endpoint",
                producer="complete-identity-coverage",
                representation="named endpoint/model and unchanged query",
            ),
            state_case(
                "truncated",
                producer="bounded-truncation",
                representation="limits, returned evidence IDs and more-paths state",
            ),
        ],
    )
    return fixture


def dispatch_fixture() -> dict[str, Any]:
    fixture = base("FX-DISPATCH-CATALOG-v1", "synthetic-phase1-v1")
    rows: list[dict[str, Any]] = []
    states = ("open", "closed", "pending")
    for index in range(700):
        dispatch_id = f"fixture-dispatch-{index:03d}"
        row: dict[str, Any] = {
            "object_id": f"fixture:{dispatch_id}",
            "dispatch_id": dispatch_id,
            "object_kind": "dispatch",
            "display_label": f"Fixture dispatch {index:03d}",
            "status": states[index % len(states)],
            "dispatch_type": ("research", "review", "experiment")[index % 3],
            "created": f"2026-07-{(index % 24) + 1:02d}T{index % 24:02d}:00:00Z",
            "owner": "@VictorBoscaro",
            "groups": [],
            "connections": [],
        }
        if index == 1:
            row["parent_dispatch_id"] = "fixture-dispatch-000"
        if index == 2:
            row["parent_dispatch_id"] = "missing-parent"
            row["case_ids"] = ["unresolved-parent"]
        if index == 3:
            row["legacy"] = True
            row["dispatch_type"] = None
            row["case_ids"] = ["legacy-row"]
        if index == 4:
            row["orphan_close"] = True
            row["case_ids"] = ["orphan-close"]
        if index == 5:
            row["groups"] = [
                {"group_id": "probe", "role": "investigate"},
                {"group_id": "synthesize", "role": "synthesize"},
            ]
            row["connections"] = [
                {"from": "probe", "to": "synthesize", "type": "sequential"}
            ]
            row["case_ids"] = ["intra-dispatch-topology"]
        rows.append(row)
    fixture.update(
        rows=rows,
        required_cases={
            "root_child_chain": ["fixture-dispatch-000", "fixture-dispatch-001"],
            "unresolved_parent": "fixture-dispatch-002",
            "legacy_row": "fixture-dispatch-003",
            "orphan_close": "fixture-dispatch-004",
            "intra_dispatch_topology": "fixture-dispatch-005",
            "states": ["pending", "open", "closed"],
        },
        expected_count=700,
        state_cases=[
            state_case(
                "loading",
                producer="pending-read-request",
                representation="busy status with stable scope, identity and focus",
            ),
            state_case(
                "empty",
                producer="complete-empty-result",
                representation="scope-specific empty copy distinct from unavailable",
            ),
            state_case(
                "no-match",
                producer="complete-search-no-match",
                representation="active query, filters, scope and reversible reset",
            ),
        ],
    )
    return fixture


def evidence_fixture() -> dict[str, Any]:
    fixture = base("FX-EVIDENCE-MIXED-v1", "synthetic-evidence-v1")
    fixture["cases"] = [
        {
            "case_id": "complete-positive-fresh",
            "evidence_classes": ["observed"],
            "completeness": "complete",
            "freshness": "fresh",
            "logical_invocation_count": 3,
            "attempt_count": 4,
            "retry_count": 1,
            "redelivery_count": 1,
            "conflict_count": 0,
            "exhaustive": True,
        },
        {
            "case_id": "complete-zero-stale",
            "evidence_classes": ["observed"],
            "completeness": "complete",
            "freshness": "stale",
            "logical_invocation_count": 0,
            "attempt_count": 0,
            "retry_count": 0,
            "complete_window_coverage": True,
            "exhaustive": True,
        },
        {
            "case_id": "partial-lower-bound",
            "evidence_classes": ["observed"],
            "completeness": "partial",
            "freshness": "unknown",
            "logical_invocation_count": 2,
            "attempt_count": 2,
            "retry_count": 0,
            "exhaustive": False,
        },
        {
            "case_id": "unavailable-not-zero",
            "evidence_classes": ["unknown-or-unavailable"],
            "completeness": "unavailable",
            "freshness": "unknown",
            "logical_invocation_count": None,
            "attempt_count": None,
            "retry_count": None,
            "redelivery_count": None,
            "conflict_count": None,
            "exhaustive": False,
        },
        {
            "case_id": "dedupe-retry-conflict",
            "evidence_classes": ["observed", "declared"],
            "completeness": "complete",
            "freshness": "fresh",
            "deliveries": [
                {"producer": "fixture", "event_id": "e1", "attempt_id": "a1"},
                {"producer": "fixture", "event_id": "e1", "attempt_id": "a1"},
                {"producer": "fixture", "event_id": "e2", "attempt_id": "a2"},
            ],
            "logical_invocation_count": 1,
            "attempt_count": 2,
            "retry_count": 1,
            "redelivery_count": 1,
            "conflict_count": 1,
            "exhaustive": True,
        },
    ]
    fixture["state_cases"] = [
        state_case(
            "observed",
            producer="observed-evidence-answer",
            representation="counts, window, proof, coverage, freshness and source",
        ),
        state_case(
            "stale",
            producer="stale-degraded-source",
            representation="source, SLA, origin, last ingest and impact",
        ),
        state_case(
            "partial",
            producer="partial-result-failed-partition",
            representation="lower bound, retained facts and failed source",
        ),
    ]
    return fixture


def draft_fixture() -> dict[str, Any]:
    fixture = base("FX-DRAFT-v1", "phase1-local-operations-v1")
    fixture.update(
        owner="@VictorBoscaro",
        target={
            "target_kind": "skill",
            "target_id": "research",
            "base_revision_or_hash": "sha256:fixture-base",
        },
        proposed_patch=[
            {"op": "replace", "path": "/metadata/label", "value": "Research"}
        ],
        effective_values={
            "metadata.label": {"value": "Research", "origin": "proposal"}
        },
        validation_previews={
            "valid": {"authoritative": False, "findings": []},
            "invalid": {
                "authoritative": False,
                "findings": [{"code": "fixture-invalid-value"}],
            },
        },
        operation_codes={
            "preference": [
                "saved-local",
                "invalid-local-scope",
                "local-conflict",
                "invalid-local-preference",
                "forbidden-local-target",
                "save-failed",
                "protocol-error",
            ],
            "draft": [
                "draft-saved",
                "invalid-draft",
                "forbidden-draft-state",
                "draft-conflict",
                "invalid-draft-schema",
                "invalid-draft-patch",
                "unsupported-target-kind",
                "draft-state-ineligible",
                "save-failed",
                "protocol-error",
            ],
            "validation": [
                "validation-valid",
                "validation-invalid",
                "draft-not-found",
                "draft-conflict",
                "validation-ineligible",
                "validation-unavailable",
                "validation-error",
                "invalid-validator",
                "forbidden-validation-effect",
                "validation-save-failed",
                "protocol-error",
            ],
        },
        lifecycle_states=[
            "clean",
            "draft-dirty",
            "draft-saved",
            "validating",
            "valid",
            "invalid",
            "save-failed",
        ],
        authority_route="unavailable",
        authoritative_effects=[],
        state_cases=[
            state_case(
                "draft-dirty",
                producer="local-edit",
                representation="unsaved marker, target, base and diff",
            ),
            state_case(
                "draft-saved",
                producer="draft-saved",
                representation="local revision, diff and validate action",
            ),
            state_case(
                "validating",
                producer="validation-started",
                representation="attempt status, protected edit and live announcement",
            ),
            state_case(
                "valid",
                producer="validation-valid",
                representation="valid non-authoritative preview and validator version",
            ),
            state_case(
                "invalid",
                producer="validation-invalid",
                representation="field-linked findings and non-authoritative label",
            ),
            state_case(
                "save-failed",
                producer="retryable-persistence-error",
                representation="retained input, unchanged revision and retry focus",
            ),
            state_case(
                "local-conflict",
                producer="local-cas-mismatch",
                representation="stored/caller revisions and refresh/review action",
            ),
        ],
    )
    return fixture


def interface_fixture() -> dict[str, Any]:
    fixture = base("FX-INTERFACE-BOUNDARY-v1", "phase1-interface-v1")
    fixture["cases"] = [
        {
            "case_id": "complete-binding",
            "host_id": "implementations-fastapi-loopback",
            "auth_contract_id": "local-loopback-process-boundary-v1",
            "route_owner_id": "@VictorBoscaro",
            "interface_state": "available",
            "published_route_count": 6,
        },
        {
            "case_id": "missing-host",
            "host_id": None,
            "auth_contract_id": "local-loopback-process-boundary-v1",
            "route_owner_id": "@VictorBoscaro",
            "interface_state": "unavailable",
            "published_route_count": 0,
            "safe_recovery": "Bind host_id at the composition root.",
        },
        {
            "case_id": "missing-auth-contract",
            "host_id": "implementations-fastapi-loopback",
            "auth_contract_id": None,
            "route_owner_id": "@VictorBoscaro",
            "interface_state": "unavailable",
            "published_route_count": 0,
            "safe_recovery": "Bind auth_contract_id at the composition root.",
        },
        {
            "case_id": "missing-route-owner",
            "host_id": "implementations-fastapi-loopback",
            "auth_contract_id": "local-loopback-process-boundary-v1",
            "route_owner_id": None,
            "interface_state": "unavailable",
            "published_route_count": 0,
            "safe_recovery": "Bind route_owner_id at the composition root.",
        },
    ]
    fixture["state_cases"] = [
        state_case(
            "read-api-unavailable",
            producer="missing-if-i5-binding",
            representation="no published call, missing binding and safe recovery",
        )
    ]
    return fixture


def main() -> None:
    entries = [
        write("skill-topology.json", skill_fixture()),
        write("dispatch-catalog.json", dispatch_fixture()),
        write("evidence-mixed.json", evidence_fixture()),
        write("draft.json", draft_fixture()),
        write("interface-boundary.json", interface_fixture()),
    ]
    manifest = {
        "schema_version": "1",
        "generated_at_utc": GENERATED_AT,
        "fixtures": entries,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
