"""APT application slice over the ACI-owned journal, artifacts and projections."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import replace
from typing import Any

from .canonical import canonical_bytes, canonical_digest, canonical_text, parse_strict_json
from .errors import (
    AuthorizationError,
    ConflictError,
    IdempotencyConflict,
    NotFoundError,
    ValidationError,
)
from .service import RuntimeService

APT_POLICY_BUNDLE_DIGEST = (
    "sha256:6345bde1c44f9832ce6a4c8e07f5f9484ac265ff4c96276d4dfa47c590149299"
)


def _digest_object(data: bytes | str) -> dict[str, str]:
    value = (
        hashlib.sha256(data).hexdigest()
        if isinstance(data, bytes)
        else data.removeprefix("sha256:")
    )
    return {"algorithm": "sha256", "value": value}


def _nonempty(value: Any, name: str, *, maximum: int = 65536) -> str:
    if not isinstance(value, str) or not value or len(value.encode("utf-8")) > maximum:
        raise ValidationError(f"{name} must be bounded non-empty UTF-8 text")
    return value


class ProvenanceService:
    def __init__(self, runtime: RuntimeService) -> None:
        self.runtime = runtime

    def _validate_bound_batch(
        self,
        conn,
        *,
        capture_payload: dict[str, Any],
        fact_payloads: list[dict[str, Any]],
        artifact_id: str,
        artifact_hash: str,
        artifact_body: bytes,
    ) -> None:
        """Revalidate the closed composite at the authoritative write boundary."""
        capture = capture_payload["research_capture"]
        if set(capture_payload) != {
            "research_capture",
            "session_dispatch_link_id",
            "actor_ref",
        }:
            raise ValidationError("capture batch envelope is open")
        if set(capture) != {
            "schema_ref",
            "research_capture_id",
            "expected_contribution_id",
            "capture_operation_id",
            "dispatch_id",
            "dispatch_snapshot_ref",
            "origin_refs",
            "producer_ref",
            "capture_status",
            "raw_return",
            "partial_reason",
            "failure_reason",
            "failure_evidence_ref",
            "supersedes_capture_id",
            "synthesizes",
            "captured_at",
            "capture_digest",
        } or capture["schema_ref"] != "apt.research-capture@1":
            raise ValidationError("capture batch entity is open or wrong-schema")
        if canonical_digest(
            {key: value for key, value in capture.items() if key != "capture_digest"}
        ) != self.runtime._content_digest_string(capture["capture_digest"]):
            raise ValidationError("capture batch digest mismatch")
        link = conn.execute(
            "SELECT * FROM dispatch_links WHERE dispatch_id=?",
            (capture["dispatch_id"],),
        ).fetchone()
        raw = capture["raw_return"]
        if (
            not link
            or capture_payload["session_dispatch_link_id"]
            != self.runtime._stable_id(
                "lnk_",
                [link["session_id"], capture["dispatch_id"], link["row_digest"]],
            )
            or self.runtime._content_digest_string(
                capture["dispatch_snapshot_ref"]["row_digest"]
            )
            != link["row_digest"]
            or raw["artifact_id"] != artifact_id
            or self.runtime._content_digest_string(raw["content_digest"])
            != artifact_hash
            or capture["capture_status"] != "captured"
            or any(
                capture[name] is not None
                for name in (
                    "partial_reason",
                    "failure_reason",
                    "failure_evidence_ref",
                )
            )
        ):
            raise ConflictError("capture batch authority/evidence mismatch")
        known_subjects: dict[str, str] = {}
        known_claim_statements: dict[str, str] = {}
        entity_fields = {
            "research_question": {
                "research_question_id", "research_capture_id", "fact",
                "question_text", "derives_from", "extraction",
            },
            "research_answer": {
                "research_answer_id", "research_capture_id", "fact",
                "question_ids", "extraction",
            },
            "reference_use": {
                "reference_use_id", "research_capture_id", "fact", "reference_id",
                "reference_kind", "locator_observed", "source_observation_id",
                "probe_recommendation_ref", "use_kind", "anchor_quality", "extraction",
            },
            "research_problem": {
                "problem_id", "research_capture_id", "fact", "kind", "statement",
                "blocks", "evidence_refs", "extraction",
            },
            "research_claim": {
                "research_claim_id", "research_capture_id", "fact", "statement",
                "answer_ids", "extraction",
            },
            "formalization_candidate": {
                "formalization_id", "research_capture_id", "fact",
                "research_claim_id", "notation", "latex", "legend", "reading",
                "logic_family", "assumptions", "scope", "extraction",
            },
        }
        for wrapped in fact_payloads:
            if set(wrapped) != {
                "payload_variant",
                "payload",
                "actor_ref",
                "event_occurred_at",
            }:
                raise ValidationError("fact batch envelope is open")
            kind, entity = wrapped["payload_variant"], wrapped["payload"]
            if kind not in entity_fields or set(entity) != entity_fields[kind]:
                raise ValidationError("fact batch entity is open or wrong-variant")
            fact = entity["fact"]
            if set(fact) != {
                "fact_id", "subject_id", "operation_id", "occurred_at",
                "supersedes_fact_id",
            } or set(entity["extraction"]) != {
                "mode", "actor_ref", "method_ref", "extracted_at",
                "source_capture_id", "source_capture_digest", "selector",
            }:
                raise ValidationError("fact/extraction batch shape is open")
            if (
                entity["research_capture_id"] != capture["research_capture_id"]
                or fact["subject_id"] in known_subjects
                or entity["extraction"]["source_capture_id"]
                != capture["research_capture_id"]
                or self.runtime._content_digest_string(
                    entity["extraction"]["source_capture_digest"]
                )
                != self.runtime._content_digest_string(capture["capture_digest"])
                or fact["occurred_at"] != wrapped["event_occurred_at"]
            ):
                raise ValidationError("fact batch capture/subject binding mismatch")
            selector = entity["extraction"]["selector"]
            start, end = selector["start_inclusive"], selector["end_exclusive"]
            if (
                selector.get("schema_ref") != "apt.raw-selector@1"
                or selector.get("unit") != "utf8-byte"
                or not isinstance(start, int)
                or not isinstance(end, int)
                or not (0 <= start < end <= len(artifact_body))
                or self.runtime._content_digest_string(
                    selector["selected_text_digest"]
                )
                != "sha256:" + hashlib.sha256(artifact_body[start:end]).hexdigest()
            ):
                raise ValidationError("fact batch selector mismatch")
            selected = parse_strict_json(artifact_body[start:end])
            expected_type = {
                "research_question": "question",
                "research_answer": "answer",
                "reference_use": "reference",
                "research_problem": "problem",
                "research_claim": "claim",
                "formalization_candidate": "formalization",
            }.get(kind)
            if selected.get("type") != expected_type:
                raise ValidationError("fact selector semantic type mismatch")
            frame_matches = {
                "research_question": lambda: selected
                == {
                    "mode": "declared",
                    "type": "question",
                    "question_text": entity["question_text"],
                },
                "research_answer": lambda: (
                    set(selected) == {"mode", "type", "final_answer"}
                    and selected["mode"] == "declared"
                    and isinstance(selected["final_answer"], str)
                    and bool(selected["final_answer"])
                ),
                "reference_use": lambda: selected
                == {
                    "mode": "declared",
                    "type": "reference",
                    "reference_kind": entity["reference_kind"],
                    "locator_observed": entity["locator_observed"],
                    "use_kind": entity["use_kind"],
                },
                "research_problem": lambda: selected
                == {
                    "mode": "declared",
                    "type": "problem",
                    "kind": entity["kind"],
                    "statement": entity["statement"],
                },
                "research_claim": lambda: (
                    selected.get("mode") == "inferred"
                    and selected.get("type") == "claim"
                    and selected.get("statement") == entity["statement"]
                    and set(selected) == {"mode", "type", "statement", "derivation"}
                ),
                "formalization_candidate": lambda: (
                    selected.get("mode") == "declared"
                    and selected.get("type") == "formalization"
                    and all(
                        selected.get(name) == entity[name]
                        for name in (
                            "notation", "latex", "legend", "reading",
                            "logic_family", "assumptions", "scope",
                        )
                    )
                    and selected.get("claim")
                    == known_claim_statements.get(entity["research_claim_id"])
                    and set(selected)
                    == {
                        "mode", "type", "claim", "notation", "latex", "legend",
                        "reading", "logic_family", "assumptions", "scope",
                    }
                ),
            }[kind]()
            if not frame_matches:
                raise ValidationError("selected frame and semantic fact diverge")
            dependencies: list[tuple[str, str]] = []
            if kind == "research_answer":
                dependencies.extend((value, "research_question") for value in entity["question_ids"])
            elif kind == "research_claim":
                dependencies.extend((value, "research_answer") for value in entity["answer_ids"])
            elif kind == "formalization_candidate":
                dependencies.append((entity["research_claim_id"], "research_claim"))
            for subject_id, expected_kind in dependencies:
                if known_subjects.get(subject_id) != expected_kind:
                    raise ConflictError("fact batch edge is dangling or wrong-kind")
            known_subjects[fact["subject_id"]] = kind
            if kind == "research_claim":
                known_claim_statements[fact["subject_id"]] = entity["statement"]

    @staticmethod
    def _bound_envelope(records: list[dict[str, Any]]) -> tuple[bytes, list[dict[str, Any]]]:
        body = bytearray(b"APT-RESEARCH-SUBMISSION/1\n")
        selectors: list[dict[str, Any]] = []
        for record in records:
            encoded = canonical_bytes(record)
            body.extend(str(len(encoded)).encode("ascii"))
            body.extend(b"\n")
            start = len(body)
            body.extend(encoded)
            end = len(body)
            body.extend(b"\n")
            selectors.append(
                {
                    "schema_ref": "apt.raw-selector@1",
                    "unit": "utf8-byte",
                    "start_inclusive": start,
                    "end_exclusive": end,
                    "selected_text_digest": _digest_object(encoded),
                }
            )
        return bytes(body), selectors

    def append_research_submission(
        self,
        *,
        token: str,
        dispatch_id: str,
        idempotency_key: str,
        intent: dict[str, Any],
        _retry_after_race: bool = True,
    ) -> dict[str, Any]:
        expected = {
            "session_id",
            "expected_contribution_id",
            "question",
            "final_answer",
            "references",
            "problems",
            "formalizations",
        }
        if set(intent) != expected or not idempotency_key:
            raise ValidationError("research submission intent field set is invalid")
        context = self.runtime.capabilities.resolve(
            token, action="apt.append", phase="capture"
        )
        if (
            context.context.get("session_id") != intent["session_id"]
            or context.context.get("dispatch_id") != dispatch_id
        ):
            raise AuthorizationError("research capability scope mismatch")
        question = _nonempty(intent["question"], "question", maximum=32768)
        answer = _nonempty(intent["final_answer"], "final_answer", maximum=1048576)
        contribution = _nonempty(
            intent["expected_contribution_id"], "expected_contribution_id", maximum=256
        )
        for name, limit in (("references", 128), ("problems", 128), ("formalizations", 64)):
            if not isinstance(intent[name], list) or len(intent[name]) > limit:
                raise ValidationError(f"{name} must be a bounded list")
        link = self.runtime.apt_dispatch_link(dispatch_id, intent["session_id"])
        if not link:
            raise ConflictError("accepted session-to-dispatch link is required")
        dispatch_snapshot = self.runtime.legacy.resolve(
            self.runtime.settings.ledger_path, dispatch_id
        )
        if dispatch_snapshot.row_digest != link["row_digest"]:
            raise ConflictError("linked dispatch snapshot no longer matches")

        normalized_refs = []
        for ref in intent["references"]:
            if not isinstance(ref, dict) or set(ref) != {
                "reference_kind",
                "locator_observed",
                "use_kind",
            }:
                raise ValidationError("reference intent field set is invalid")
            if ref["reference_kind"] not in {
                "file",
                "url",
                "paper",
                "commit",
                "dataset",
                "command-output",
            } or ref["use_kind"] not in {"mentioned", "cited", "claimed_consulted"}:
                raise ValidationError("reference enum is invalid")
            normalized_refs.append(
                {
                    **ref,
                    "locator_observed": _nonempty(
                        ref["locator_observed"], "locator_observed", maximum=8192
                    ),
                }
            )
        normalized_problems = []
        for problem in intent["problems"]:
            if not isinstance(problem, dict) or set(problem) != {"kind", "statement"}:
                raise ValidationError("problem intent field set is invalid")
            if problem["kind"] not in {
                "gap",
                "contradiction",
                "blocker",
                "uncertainty",
                "failed_check",
            }:
                raise ValidationError("problem kind is invalid")
            normalized_problems.append(
                {
                    "kind": problem["kind"],
                    "statement": _nonempty(
                        problem["statement"], "problem statement", maximum=32768
                    ),
                }
            )
        normalized_forms = []
        for form in intent["formalizations"]:
            fields = {
                "claim",
                "notation",
                "latex",
                "legend",
                "reading",
                "logic_family",
                "assumptions",
                "scope",
            }
            if not isinstance(form, dict) or set(form) != fields:
                raise ValidationError("formalization intent field set is invalid")
            if (
                not isinstance(form["legend"], dict)
                or not form["legend"]
                or len(form["legend"]) > 128
            ):
                raise ValidationError("formalization legend must be non-empty")
            legend: dict[str, str] = {}
            for key, value in form["legend"].items():
                legend[_nonempty(key, "legend key", maximum=256)] = _nonempty(
                    value, "legend value", maximum=4096
                )
            if (
                not isinstance(form["assumptions"], list)
                or len(form["assumptions"]) > 128
            ):
                raise ValidationError("formalization assumptions must be a list")
            assumptions = [
                _nonempty(value, "assumption", maximum=8192)
                for value in form["assumptions"]
            ]
            normalized_forms.append(
                {
                    **form,
                    "claim": _nonempty(form["claim"], "claim", maximum=32768),
                    "notation": _nonempty(form["notation"], "notation", maximum=32768),
                    "latex": (
                        _nonempty(form["latex"], "latex", maximum=32768)
                        if form["latex"] is not None
                        else None
                    ),
                    "legend": legend,
                    "reading": _nonempty(form["reading"], "reading", maximum=32768),
                    "logic_family": _nonempty(
                        form["logic_family"], "logic_family", maximum=256
                    ),
                    "scope": _nonempty(form["scope"], "scope", maximum=8192),
                    "assumptions": assumptions,
                }
            )

        bound_intent = {
            "session_id": intent["session_id"],
            "dispatch_id": dispatch_id,
            "expected_contribution_id": contribution,
            "question": question,
            "final_answer": answer,
            "references": normalized_refs,
            "problems": normalized_problems,
            "formalizations": normalized_forms,
        }
        submission_digest = canonical_digest(bound_intent)
        aggregate_id = self.runtime._stable_id(
            "apt.research:", [dispatch_id, contribution]
        )
        prior = self.runtime.apt_command_result(aggregate_id, idempotency_key)
        if prior:
            result = prior
            if result.get("submission_digest") != submission_digest:
                raise IdempotencyConflict(
                    "research idempotency key reused with different submission"
                )
            try:
                state = self.runtime.projections.catch_up_apt(self.runtime.journal)
                result["projection_status"] = (
                    "current"
                    if state["current"]
                    and int(state["apt_source_through_offset"])
                    >= int(result["last_offset"])
                    else "pending"
                )
            except Exception:
                result["projection_status"] = "pending"
            return result

        records: list[dict[str, Any]] = [
            {"mode": "declared", "type": "question", "question_text": question},
            {"mode": "declared", "type": "answer", "final_answer": answer},
        ]
        records.extend(
            {"mode": "declared", "type": "reference", **ref}
            for ref in normalized_refs
        )
        records.extend(
            {"mode": "declared", "type": "problem", **problem}
            for problem in normalized_problems
        )
        for form in normalized_forms:
            records.append(
                {
                    "mode": "inferred",
                    "type": "claim",
                    "statement": form["claim"],
                    "derivation": "formalization-declared-claim",
                }
            )
            records.append({"mode": "declared", "type": "formalization", **form})
        artifact_body, selectors = self._bound_envelope(records)
        prepared = self.runtime.artifacts.prepare(
            artifact_body,
            media_type=(
                "application/vnd.cyberalchemy.apt-research-submission;"
                "version=1;charset=utf-8"
            ),
            schema_ref="apt.research-submission-envelope@1",
            classification="sensitive-output",
            redaction_policy_ref="aci.redaction.none@1",
            retention_policy_ref="apt.retention.local-sensitive-output@1",
            tombstone_policy_ref="apt.tombstone.preserve-identity-and-audit@1",
            authorization_policy_ref="apt.authorization.provenance-artifact-read@1",
            policy_bundle_digest=APT_POLICY_BUNDLE_DIGEST,
        )
        # The receipt identity is content/policy stable; this keeps the capture
        # payload deterministic under concurrent exact calls.
        prepared = replace(
            prepared,
            finalization_receipt_ref=(
                "afr_" + prepared.content_hash.removeprefix("sha256:")[:32]
            ),
        )
        content_digest = _digest_object(artifact_body)
        raw_ref = {
            "artifact_id": prepared.artifact_id,
            "content_digest": content_digest,
            "media_type": prepared.media_type,
            "charset": "utf-8",
            "classification": "sensitive-output",
            "redaction_policy_ref": prepared.redaction_policy_ref,
            "retention_policy_ref": prepared.retention_policy_ref,
            "tombstone_policy_ref": prepared.tombstone_policy_ref,
            "finalization_receipt_ref": prepared.finalization_receipt_ref,
        }
        capture_id = self.runtime._stable_id("cap_", submission_digest)
        existing_capture_projection = self.runtime.apt_capture_projection_payload(
            capture_id
        )
        captured_at = (
            existing_capture_projection["captured_at"]
            if existing_capture_projection
            else link["linked_at"]
        )
        snapshot = {
            "kind": "legacy_ledger",
            "ledger_row_identity": {
                "dispatch_id": dispatch_id,
                "row_kind": dispatch_snapshot.row_kind,
                "appender_identity": dispatch_snapshot.appender_identity,
                "contract_version": dispatch_snapshot.contract_version,
            },
            "row_digest": _digest_object(link["row_digest"]),
        }
        capture = {
            "schema_ref": "apt.research-capture@1",
            "research_capture_id": capture_id,
            "expected_contribution_id": contribution,
            "capture_operation_id": self.runtime._stable_id(
                "op_", [submission_digest, "capture"]
            ),
            "dispatch_id": dispatch_id,
            "dispatch_snapshot_ref": snapshot,
            "origin_refs": [],
            "producer_ref": {
                "kind": "host_actor",
                "host_actor_id": context.principal_id,
                "activation_id": context.context.get("activation_id")
                or self.runtime._stable_id(
                    "act_",
                    [context.principal_id, intent["session_id"], dispatch_id],
                ),
            },
            "capture_status": "captured",
            "raw_return": raw_ref,
            "partial_reason": None,
            "failure_reason": None,
            "failure_evidence_ref": None,
            "supersedes_capture_id": None,
            "synthesizes": [],
            "captured_at": captured_at,
            "capture_digest": None,
        }
        capture["capture_digest"] = _digest_object(
            canonical_digest({k: v for k, v in capture.items() if k != "capture_digest"})
        )
        link_id = self.runtime._stable_id(
            "lnk_", [link["session_id"], dispatch_id, link["row_digest"]]
        )
        capture_payload = {
            "research_capture": capture,
            "session_dispatch_link_id": link_id,
            "actor_ref": context.principal_id,
        }

        question_id = self.runtime._stable_id("q_", [capture_id, "question"])
        answer_id = self.runtime._stable_id("ans_", [capture_id, "answer"])
        facts: list[tuple[str, dict[str, Any]]] = []

        def extraction(selector_index: int, mode: str) -> dict[str, Any]:
            return {
                "mode": mode,
                "actor_ref": context.principal_id,
                "method_ref": "apt.bound-submission@1",
                "extracted_at": captured_at,
                "source_capture_id": capture_id,
                "source_capture_digest": capture["capture_digest"],
                "selector": selectors[selector_index],
            }

        def envelope(subject_id: str, index: int) -> dict[str, Any]:
            return {
                "fact_id": self.runtime._stable_id(
                    "fact_", [capture_id, subject_id, index]
                ),
                "subject_id": subject_id,
                "operation_id": self.runtime._stable_id(
                    "op_", [submission_digest, subject_id]
                ),
                "occurred_at": captured_at,
                "supersedes_fact_id": None,
            }

        facts.append(
            (
                "research_question",
                {
                    "research_question_id": question_id,
                    "research_capture_id": capture_id,
                    "fact": envelope(question_id, 0),
                    "question_text": question,
                    "derives_from": [],
                    "extraction": extraction(0, "declared"),
                },
            )
        )
        facts.append(
            (
                "research_answer",
                {
                    "research_answer_id": answer_id,
                    "research_capture_id": capture_id,
                    "fact": envelope(answer_id, 1),
                    "question_ids": [question_id],
                    "extraction": extraction(1, "declared"),
                },
            )
        )
        selector_index = 2
        for index, ref in enumerate(normalized_refs):
            subject = self.runtime._stable_id(
                "ref_", [capture_id, ref["reference_kind"], ref["locator_observed"]]
            )
            facts.append(
                (
                    "reference_use",
                    {
                        "reference_use_id": subject,
                        "research_capture_id": capture_id,
                        "fact": envelope(subject, selector_index),
                        "reference_id": self.runtime._stable_id(
                            "source_", [ref["reference_kind"], ref["locator_observed"]]
                        ),
                        **ref,
                        "source_observation_id": None,
                        "probe_recommendation_ref": None,
                        "anchor_quality": "locator",
                        "extraction": extraction(selector_index, "declared"),
                    },
                )
            )
            selector_index += 1
        for problem in normalized_problems:
            subject = self.runtime._stable_id(
                "problem_", [capture_id, problem["kind"], problem["statement"]]
            )
            facts.append(
                (
                    "research_problem",
                    {
                        "problem_id": subject,
                        "research_capture_id": capture_id,
                        "fact": envelope(subject, selector_index),
                        **problem,
                        "blocks": [],
                        "evidence_refs": [],
                        "extraction": extraction(selector_index, "declared"),
                    },
                )
            )
            selector_index += 1
        for form in normalized_forms:
            claim_id = self.runtime._stable_id("claim_", [capture_id, form["claim"]])
            facts.append(
                (
                    "research_claim",
                    {
                        "research_claim_id": claim_id,
                        "research_capture_id": capture_id,
                        "fact": envelope(claim_id, selector_index),
                        "statement": form["claim"],
                        "answer_ids": [answer_id],
                        "extraction": extraction(selector_index, "inferred"),
                    },
                )
            )
            selector_index += 1
            formalization_id = self.runtime._stable_id(
                "form_", [capture_id, claim_id, form["notation"]]
            )
            facts.append(
                (
                    "formalization_candidate",
                    {
                        "formalization_id": formalization_id,
                        "research_capture_id": capture_id,
                        "fact": envelope(formalization_id, selector_index),
                        "research_claim_id": claim_id,
                        "notation": form["notation"],
                        "latex": form["latex"],
                        "legend": form["legend"],
                        "reading": form["reading"],
                        "logic_family": form["logic_family"],
                        "assumptions": form["assumptions"],
                        "scope": form["scope"],
                        "extraction": extraction(selector_index, "declared"),
                    },
                )
            )
            selector_index += 1

        items = [
            {
                "item_key": "capture:" + capture_id,
                "kind": "capture",
                "payload": capture_payload,
                "semantic_digest": canonical_digest(capture),
            }
        ]
        items.extend(
            {
                "item_key": "fact:" + entity["fact"]["fact_id"],
                "kind": kind,
                "payload": {
                    "payload_variant": kind,
                    "payload": entity,
                    "actor_ref": context.principal_id,
                    "event_occurred_at": captured_at,
                },
                "semantic_digest": canonical_digest(entity),
            }
            for kind, entity in facts
        )
        fact_envelopes = [
            item["payload"]["payload"]["fact"]
            for item in items
            if item["kind"] != "capture"
        ]
        capture_existing, existing_facts = self.runtime.apt_semantic_partition(
            capture_id,
            self.runtime._content_digest_string(capture["capture_digest"]),
            fact_envelopes,
        )
        for item in items:
            if item["kind"] == "capture":
                existing = capture_existing
                exact = (
                    existing
                    and existing["capture_digest"]
                    == self.runtime._content_digest_string(capture["capture_digest"])
                )
                accepted = existing["accepted_event_id"] if existing else None
            else:
                fact = item["payload"]["payload"]["fact"]
                existing = existing_facts.get(fact["fact_id"])
                exact = (
                    existing
                    and existing["canonical_payload_digest"]
                    == item["semantic_digest"]
                    and existing["subject_id"] == fact["subject_id"]
                    and existing["supersedes_fact_id"] == fact["supersedes_fact_id"]
                )
                accepted = existing["accepted_event_id"] if existing else None
            if existing and not exact:
                raise ConflictError(f"semantic conflict for {item['item_key']}")
            item["status"] = "existing_exact" if existing else "submitted_new"
            item["accepted_event_id"] = accepted
        new_items = [item for item in items if item["status"] == "submitted_new"]
        if not new_items:
            result = {
                "status": "existing_exact",
                "submitted": False,
                "submission_digest": submission_digest,
                "research_capture_id": capture_id,
                "semantic_results": [
                    {
                        "item_key": item["item_key"],
                        "status": item["status"],
                        "accepted_event_id": item["accepted_event_id"],
                    }
                    for item in items
                ],
            }
            try:
                state = self.runtime.projections.catch_up_apt(self.runtime.journal)
                result["projection_status"] = (
                    "current" if state["current"] else "pending"
                )
            except Exception:
                result["projection_status"] = "pending"
            return result

        event_types = {
            "capture": "apt.research_capture_appended",
            **{kind: "apt.research_fact_appended" for kind, _ in facts},
        }
        events = [
            self.runtime._event(event_types[item["kind"]], item["payload"])
            for item in new_items
        ]
        head = self.runtime.journal.head(aggregate_id)
        command = self.runtime._command(
            command_name="apt.append-bound-research-submission@1",
            scope_key=aggregate_id,
            idempotency_key=idempotency_key,
            aggregate_type="apt.research",
            aggregate_id=aggregate_id,
            expected_version=head["current_version"],
            authority={
                "capability_id": context.capability_id,
                "principal_id": context.principal_id,
                "action": "apt.append",
            },
            intent={"submission_digest": submission_digest},
        )

        def result_builder(committed, base):
            iterator = iter(committed)
            results = []
            for item in items:
                if item["status"] == "submitted_new":
                    accepted_event_id = next(iterator).event_id
                    status = "accepted_new"
                else:
                    accepted_event_id = item["accepted_event_id"]
                    status = "existing_exact"
                results.append(
                    {
                        "item_key": item["item_key"],
                        "status": status,
                        "accepted_event_id": accepted_event_id,
                    }
                )
            return {
                **base,
                "submission_digest": submission_digest,
                "research_capture_id": capture_id,
                "semantic_results": results,
                "projection_status": "pending",
            }

        def mutate(conn, committed, result):
            self._validate_bound_batch(
                conn,
                capture_payload=capture_payload,
                fact_payloads=[item["payload"] for item in items if item["kind"] != "capture"],
                artifact_id=prepared.artifact_id,
                artifact_hash=prepared.content_hash,
                artifact_body=artifact_body,
            )
            committed_iter = iter(committed)
            result_by_key = {row["item_key"]: row for row in result["semantic_results"]}
            for item in items:
                if item["status"] == "submitted_new":
                    record = next(committed_iter)
                    accepted_event_id = record.event_id
                    if item["kind"] == "capture":
                        conn.execute(
                            """
                            INSERT INTO apt_capture_keys(
                              research_capture_id,dispatch_id,expected_contribution_id,
                              capture_operation_id,supersedes_capture_id,capture_digest,
                              accepted_event_id,is_current
                            ) VALUES(?,?,?,?,?,?,?,1)
                            """,
                            (
                                capture_id,
                                dispatch_id,
                                contribution,
                                capture["capture_operation_id"],
                                None,
                                self.runtime._content_digest_string(
                                    capture["capture_digest"]
                                ),
                                accepted_event_id,
                            ),
                        )
                    else:
                        entity = item["payload"]["payload"]
                        fact = entity["fact"]
                        conn.execute(
                            """
                            INSERT INTO apt_semantic_facts(
                              fact_id,research_capture_id,subject_id,fact_kind,
                              supersedes_fact_id,canonical_payload_digest,
                              accepted_event_id,is_current
                            ) VALUES(?,?,?,?,?,?,?,1)
                            """,
                            (
                                fact["fact_id"],
                                capture_id,
                                fact["subject_id"],
                                item["kind"],
                                fact["supersedes_fact_id"],
                                item["semantic_digest"],
                                accepted_event_id,
                            ),
                        )
                else:
                    accepted_event_id = item["accepted_event_id"]
                mapped = result_by_key[item["item_key"]]
                conn.execute(
                    """
                    INSERT INTO apt_semantic_request_results(
                      request_key,item_key,request_digest,result_status,result_json,
                      accepted_event_id
                    ) VALUES(?,?,?,?,?,?)
                    """,
                    (
                        f"{aggregate_id}:{idempotency_key}",
                        item["item_key"],
                        submission_digest,
                        mapped["status"],
                        canonical_text(mapped),
                        accepted_event_id,
                    ),
                )
        try:
            receipt = self.runtime.journal.accept(
                command,
                events,
                next_state={"submission_digest": submission_digest},
                additional_artifacts=(prepared,) if capture_existing is None else (),
                result_builder=result_builder,
                mutate=mutate,
            )
        except IdempotencyConflict:
            if not _retry_after_race:
                raise
            # A concurrent exact request may have committed after our initial
            # receipt lookup but before journal acceptance. Re-enter once so
            # the authoritative receipt check decides exact retry vs conflict.
            return self.append_research_submission(
                token=token,
                dispatch_id=dispatch_id,
                idempotency_key=idempotency_key,
                intent=intent,
                _retry_after_race=False,
            )
        except sqlite3.IntegrityError as exc:
            raise ConflictError("research semantic currentness conflict") from exc
        except ConflictError:
            if not _retry_after_race:
                raise
            return self.append_research_submission(
                token=token,
                dispatch_id=dispatch_id,
                idempotency_key=idempotency_key,
                intent=intent,
                _retry_after_race=False,
            )
        result = dict(receipt)
        try:
            state = self.runtime.projections.catch_up_apt(self.runtime.journal)
            result["projection_status"] = (
                "current"
                if state["current"]
                and int(state["apt_source_through_offset"])
                >= int(result["last_offset"])
                else "pending"
            )
        except Exception:
            # Projection is outside the authoritative append transaction. A
            # projector failure must not erase or rewrite the durable receipt.
            result["projection_status"] = "pending"
        return result

    def get_research(self, *, token: str, capture_id: str) -> dict[str, Any]:
        context = self.runtime.capabilities.resolve(
            token, action="projection.read", phase="observe"
        )
        result = self.runtime.projections.get_apt_research(capture_id)
        capture = result["capture"]
        link = self.runtime.apt_dispatch_link(capture["dispatch_id"])
        if (
            not link
            or context.context.get("session_id") != link["session_id"]
            or context.context.get("dispatch_id") != capture["dispatch_id"]
        ):
            raise AuthorizationError("research projection scope mismatch")
        return result

    def get_dispatch(self, *, token: str, dispatch_id: str) -> dict[str, Any]:
        context = self.runtime.capabilities.resolve(
            token, action="projection.read", phase="observe"
        )
        link = self.runtime.apt_dispatch_link(dispatch_id)
        if (
            not link
            or context.context.get("session_id") != link["session_id"]
            or context.context.get("dispatch_id") != dispatch_id
        ):
            raise AuthorizationError("dispatch projection scope mismatch")
        return self.runtime.projections.get_apt_dispatch(dispatch_id)

    def get_answer(self, *, token: str, capture_id: str) -> str:
        context = self.runtime.capabilities.resolve(
            token, action="artifact.read", phase="collect"
        )
        # Protected reads are projection-bound too: a lagging projector must
        # return PROJECTION_LAG rather than disclose from a newer authority row.
        self.runtime.projections.get_apt_research(capture_id)
        capture, answer = self.runtime.apt_answer_binding(capture_id)
        if not capture or not answer:
            raise NotFoundError("research answer not found")
        if (
            context.context.get("session_id") != capture["session_id"]
            or context.context.get("dispatch_id") != capture["dispatch_id"]
            or context.context.get("research_capture_id") != capture_id
        ):
            raise AuthorizationError("answer artifact scope mismatch")
        body = self.runtime.artifacts.get_authorized(
            answer["artifact_id"],
            principal_id=context.principal_id,
            action="artifact.read",
            authorizer=lambda principal, action, classification: (
                principal == context.principal_id
                and action == "artifact.read"
                and classification == "sensitive-output"
            ),
        )
        selector = json.loads(answer["selector_json"])
        selected = body[
            selector["start_inclusive"] : selector["end_exclusive"]
        ]
        if _digest_object(selected) != selector["selected_text_digest"]:
            raise ConflictError("answer selector digest mismatch")
        record = parse_strict_json(selected)
        if set(record) != {"mode", "type", "final_answer"} or record != {
            "mode": "declared",
            "type": "answer",
            "final_answer": record["final_answer"],
        }:
            raise ConflictError("answer frame semantic mismatch")
        return record["final_answer"]
