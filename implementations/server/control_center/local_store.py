"""In-process Phase 1 local preference and proposal ports."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from threading import RLock
from typing import Any


def _result(code: str, **values: Any) -> dict[str, Any]:
    retryable = {
        "local-conflict",
        "save-failed",
        "draft-conflict",
        "validation-unavailable",
        "validation-error",
        "validation-save-failed",
    }
    return {
        "code": code,
        "authoritative_effects": [],
        "retry_class": "retryable" if code in retryable else "terminal",
        **values,
    }


class LocalControlCenterStore:
    """CAS-backed local state with no authoritative dependencies."""

    preference_kinds = {"filter", "layout", "pin", "comparison-set", "saved-view"}
    target_kinds = {"skill", "dispatch", "runtime", "source"}

    def __init__(self) -> None:
        self._preferences: dict[tuple[str, str], dict[str, Any]] = {}
        self._preference_revisions: dict[tuple[str, str], int] = {}
        self._drafts: dict[str, dict[str, Any]] = {}
        self._lock = RLock()

    def load_preferences(self, scope_id: str, schema_version: str) -> dict[str, Any]:
        with self._lock:
            values = {
                kind: deepcopy(row["value"])
                for (scope, kind), row in self._preferences.items()
                if scope == scope_id and row["schema_version"] == schema_version
            }
            revision = self._preference_revisions.get((scope_id, schema_version), 0)
        return {
            "scope_id": scope_id,
            "revision": revision,
            "schema_version": schema_version,
            "values": values,
        }

    def save_preference(self, input_: dict[str, Any], current_scope_id: str) -> dict[str, Any]:
        required = {
            "user_scope_id",
            "expected_revision",
            "preference_kind",
            "value",
            "schema_version",
        }
        if input_.get("user_scope_id") != current_scope_id:
            return _result("invalid-local-scope", input_retained=False)
        if not required.issubset(input_):
            return _result("invalid-local-preference", input_retained=False)
        key = (current_scope_id, input_["preference_kind"])
        scope_revision_key = (current_scope_id, input_["schema_version"])
        with self._lock:
            revision = self._preference_revisions.get(scope_revision_key, 0)
            if input_["expected_revision"] != revision:
                return _result(
                    "local-conflict",
                    input_retained=True,
                    retained_input=deepcopy(input_),
                    current_revision=revision,
                )
            if (
                input_.get("preference_kind") not in self.preference_kinds
                or input_.get("schema_version") != "1"
            ):
                return _result("invalid-local-preference", input_retained=False)
            value = input_.get("value")
            if isinstance(value, dict) and value.get("target_store") not in {
                None,
                "local",
                "browser-local",
            }:
                return _result("forbidden-local-target", input_retained=False)
            next_revision = revision + 1
            self._preferences[key] = {
                "revision": next_revision,
                "value": deepcopy(input_["value"]),
                "schema_version": input_["schema_version"],
            }
            self._preference_revisions[scope_revision_key] = next_revision
        return _result(
            "saved-local",
            input_retained=False,
            revision=next_revision,
            value=deepcopy(input_["value"]),
        )

    def get_proposal(self, proposal_id: str) -> dict[str, Any] | None:
        with self._lock:
            value = self._drafts.get(proposal_id)
            return deepcopy(value) if value else None

    def list_proposals(self, scope_id: str) -> list[dict[str, Any]]:
        del scope_id  # Storage is process-local in Phase 1; no authority identity is implied.
        with self._lock:
            return [
                {
                    key: deepcopy(value[key])
                    for key in (
                        "proposal_id",
                        "target_kind",
                        "target_id",
                        "draft_revision",
                        "lifecycle_state",
                        "updated_at_utc",
                    )
                }
                for value in sorted(
                    self._drafts.values(), key=lambda row: row["proposal_id"]
                )
            ]

    def save_proposal(self, input_: dict[str, Any]) -> dict[str, Any]:
        required = {
            "proposal_id",
            "expected_draft_revision",
            "target_kind",
            "target_id",
            "base_revision_or_hash",
            "proposed_patch",
            "effective_values",
            "schema_version",
        }
        if not required.issubset(input_) or not input_.get("target_id") or not input_.get(
            "base_revision_or_hash"
        ):
            return _result("invalid-draft", input_retained=False)
        if not isinstance(input_["proposed_patch"], list) or not input_["proposed_patch"]:
            return _result("invalid-draft", input_retained=False)
        if not all(
            isinstance(value, dict) and value.get("origin")
            for value in input_["effective_values"].values()
        ):
            return _result("invalid-draft", input_retained=False)
        if input_.get("lifecycle_state") in {
            "approved",
            "applying",
            "accepted",
            "conflict",
            "indeterminate-reconciling",
            "failed",
        }:
            return _result("forbidden-draft-state", input_retained=False)
        with self._lock:
            current = self._drafts.get(input_["proposal_id"])
            revision = current["draft_revision"] if current else 0
            if input_["expected_draft_revision"] != revision:
                return _result(
                    "draft-conflict",
                    input_retained=True,
                    retained_input=deepcopy(input_),
                    current_revision=revision,
                )
            if input_["schema_version"] != "1":
                return _result("invalid-draft-schema", input_retained=False)
            if not all(
                isinstance(op, dict)
                and op.get("op") in {"add", "remove", "replace", "test"}
                and isinstance(op.get("path"), str)
                for op in input_["proposed_patch"]
            ):
                return _result("invalid-draft-patch", input_retained=False)
            if input_["target_kind"] not in self.target_kinds:
                return _result("unsupported-target-kind", input_retained=False)
            if current and current["lifecycle_state"] == "validating":
                return _result("draft-state-ineligible", input_retained=False)
            next_revision = revision + 1
            stored = deepcopy(input_)
            stored.pop("expected_draft_revision", None)
            stored.update(
                draft_revision=next_revision,
                lifecycle_state="draft-saved",
                validation_preview=None,
                updated_at_utc=datetime.now(timezone.utc).isoformat(),
                authoritative=False,
            )
            self._drafts[input_["proposal_id"]] = stored
        return _result(
            "draft-saved",
            input_retained=False,
            draft_revision=next_revision,
            proposal=deepcopy(stored),
        )

    def validate_proposal(self, input_: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            proposal = self._drafts.get(str(input_.get("proposal_id", "")))
            if proposal is None:
                return _result("draft-not-found", input_retained=False)
            if input_.get("draft_revision") != proposal["draft_revision"]:
                return _result(
                    "draft-conflict",
                    input_retained=True,
                    retained_input=deepcopy(input_),
                    current_revision=proposal["draft_revision"],
                )
            if proposal["lifecycle_state"] != "draft-saved":
                return _result("validation-ineligible", input_retained=False)
            if not input_.get("validator_id") or not input_.get("validator_version"):
                return _result("invalid-validator", input_retained=False)
            if set(input_.get("requested_effects") or []) & {
                "approve",
                "apply",
                "retry",
                "reconcile",
            }:
                return _result("forbidden-validation-effect", input_retained=False)
            if (
                input_["validator_id"] != "phase1-preview"
                or input_["validator_version"] != "1"
            ):
                return _result("validation-unavailable", input_retained=True, retained_input=deepcopy(input_))
            findings = []
            for operation in proposal["proposed_patch"]:
                if operation["path"].startswith(("/apply", "/retry", "/reconcile", "/receipt")):
                    findings.append(
                        {
                            "code": "forbidden-authoritative-path",
                            "path": operation["path"],
                            "message": "Phase 1 proposals cannot target authoritative routes.",
                        }
                    )
            code = "validation-invalid" if findings else "validation-valid"
            proposal["lifecycle_state"] = "invalid" if findings else "valid"
            proposal["validation_preview"] = {
                "authoritative": False,
                "validator_id": input_["validator_id"],
                "validator_version": input_["validator_version"],
                "draft_revision": proposal["draft_revision"],
                "findings": findings,
            }
            proposal["updated_at_utc"] = datetime.now(timezone.utc).isoformat()
            preview = deepcopy(proposal["validation_preview"])
        return _result(code, input_retained=False, preview=preview)
