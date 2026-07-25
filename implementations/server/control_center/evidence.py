"""Safe usage-evidence seam for Phase 1.

The production default is deliberately unavailable. Deterministic fixture
providers are opt-in test adapters and cannot become runtime evidence by merely
placing a fixture on disk.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Protocol


class EvidenceProvider(Protocol):
    def answer(
        self,
        object_kind: str,
        object_id: str,
        claim_id: str,
        start_utc: str | None,
        end_utc: str | None,
    ) -> dict[str, Any]: ...

    def summary(self, object_kind: str, object_id: str) -> dict[str, Any]: ...


def unavailable_evidence() -> dict[str, Any]:
    return {
        "evidence_classes": ["unknown-or-unavailable"],
        "completeness": "unavailable",
        "freshness": "unknown",
        "logical_invocation_count": None,
        "attempt_count": None,
        "retry_count": None,
        "redelivery_count": None,
        "conflict_count": None,
        "diagnostic_completeness": "unavailable",
        "attempt_outcomes": None,
        "logical_invocation_outcome": "unknown",
        "outcome_rule_id": None,
        "outcome_rule_version": None,
        "accepted_sources": None,
        "expected_sources": None,
        "configuration_revision": None,
        "updated_at_utc": None,
        "exhaustive": False,
        "source_facts": [
            {
                "source_id": "sigil-invocations",
                "ingestion_state": "unavailable",
                "coverage": "unavailable",
                "freshness": "unknown",
                "safe_reason": "No accepted invocation telemetry source is configured.",
            }
        ],
    }


def normalize_evidence(value: dict[str, Any] | None) -> dict[str, Any]:
    """Fail closed when a provider violates the Phase 1 evidence algebra."""
    if not isinstance(value, dict):
        return unavailable_evidence()
    result = {**unavailable_evidence(), **deepcopy(value)}
    classes = result.get("evidence_classes")
    completeness = result.get("completeness")
    count = result.get("logical_invocation_count")
    if classes == ["unknown-or-unavailable"] or completeness == "unavailable":
        return unavailable_evidence()
    if (
        not isinstance(classes, list)
        or not classes
        or "unknown-or-unavailable" in classes
        or completeness not in {"complete", "partial"}
        or not isinstance(count, int)
        or count < 0
    ):
        return unavailable_evidence()
    if count == 0 and not (
        completeness == "complete"
        and "observed" in classes
        and result.get("complete_window_coverage") is True
    ):
        return unavailable_evidence()
    if completeness == "partial":
        result["exhaustive"] = False
    result["diagnostic_completeness"] = result.get(
        "diagnostic_completeness", completeness
    )
    return result


class UnavailableEvidenceProvider:
    def answer(
        self,
        object_kind: str,
        object_id: str,
        claim_id: str,
        start_utc: str | None,
        end_utc: str | None,
    ) -> dict[str, Any]:
        del object_kind, object_id, claim_id, start_utc, end_utc
        return unavailable_evidence()

    def summary(self, object_kind: str, object_id: str) -> dict[str, Any]:
        del object_kind, object_id
        return unavailable_evidence()


class FixtureEvidenceProvider:
    """Explicit test adapter over `FX-EVIDENCE-MIXED-v1`.

    Callers must bind every object to a named case. Unbound objects stay
    unavailable; fixture rows are never inferred as real observations.
    """

    def __init__(
        self,
        fixture_path: Path,
        case_by_object_id: dict[str, str],
    ) -> None:
        raw = json.loads(fixture_path.read_text(encoding="utf-8"))
        if raw.get("fixture_id") != "FX-EVIDENCE-MIXED-v1":
            raise ValueError("unexpected evidence fixture")
        self._cases = {case["case_id"]: case for case in raw.get("cases", [])}
        self._bindings = dict(case_by_object_id)

    def _case(self, object_kind: str, object_id: str) -> dict[str, Any]:
        case_id = self._bindings.get(f"{object_kind}:{object_id}")
        result = normalize_evidence(self._cases.get(str(case_id)))
        if result["completeness"] != "unavailable":
            result.update(
                source_facts=[
                    {
                        "source_id": "fixture-evidence-mixed",
                        "ingestion_state": "accepted",
                        "coverage": result["completeness"],
                        "freshness": result["freshness"],
                        "fixture_case_id": case_id,
                    }
                ],
                accepted_sources=["fixture-evidence-mixed"],
                expected_sources=["fixture-evidence-mixed"],
                configuration_revision="FX-EVIDENCE-MIXED-v1",
                diagnostic_completeness=result["completeness"],
            )
        return result

    def answer(
        self,
        object_kind: str,
        object_id: str,
        claim_id: str,
        start_utc: str | None,
        end_utc: str | None,
    ) -> dict[str, Any]:
        result = self._case(object_kind, object_id)
        result.update(
            normalized_window={
                "start_utc": start_utc,
                "end_utc": end_utc,
                "basis": "UTC",
            },
            claim_id=claim_id,
        )
        return result

    def summary(self, object_kind: str, object_id: str) -> dict[str, Any]:
        result = self._case(object_kind, object_id)
        summary = {
            key: result[key]
            for key in (
                "evidence_classes",
                "completeness",
                "freshness",
                "logical_invocation_count",
                "exhaustive",
            )
        }
        if "complete_window_coverage" in result:
            summary["complete_window_coverage"] = result[
                "complete_window_coverage"
            ]
        return summary
