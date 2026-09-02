from __future__ import annotations

import copy
import json
import tempfile
import threading
import unittest
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from implementations.server.runtime.canonical import canonical_bytes, canonical_digest, digest_bytes
from implementations.server.runtime.confirmation import (
    build_confirmation_batch,
    derive_id,
    require_authority_document,
    require_derived_document,
    require_effect_ceiling,
)
from implementations.server.runtime.errors import (
    ConfirmedAuthorityConflict,
    ConfirmationObservationConflict,
    IdempotencyConflict,
    RuntimeContractError,
)
from implementations.server.runtime.service import RuntimeService, RuntimeSettings


REPO = Path(__file__).resolve().parents[3]
FIXTURE = (
    REPO
    / "docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v2"
)
FIXED_NOW = datetime(2026, 8, 31, 20, 6, tzinfo=timezone.utc)

AUTHORITY_TABLES = (
    "confirmation_observations",
    "confirmed_dispatches",
    "runs",
    "confirmed_turn_graphs",
    "continuation_input_mappings",
    "events",
    "aggregate_heads",
    "effect_intents",
    "command_receipts",
    "artifacts",
)
EMPTY_AUTHORITY_COUNTS = {table: 0 for table in AUTHORITY_TABLES} | {"artifacts": 1}
ACCEPTED_AUTHORITY_COUNTS = {
    "confirmation_observations": 1,
    "confirmed_dispatches": 1,
    "runs": 1,
    "confirmed_turn_graphs": 1,
    "continuation_input_mappings": 2,
    "events": 2,
    "aggregate_heads": 1,
    "effect_intents": 1,
    "command_receipts": 1,
    "artifacts": 10,
}


def _pointer_parent(document, pointer: str):
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]
    parent = document
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    return parent, parts[-1]


def _remove(document, pointer: str):
    parent, key = _pointer_parent(document, pointer)
    return parent.pop(int(key)) if isinstance(parent, list) else parent.pop(key)


def _add(document, pointer: str, value):
    parent, key = _pointer_parent(document, pointer)
    if isinstance(parent, list):
        parent.append(value) if key == "-" else parent.insert(int(key), value)
    else:
        parent[key] = value


def apply_patch(document, operations):
    result = copy.deepcopy(document)
    for operation in operations:
        op = operation["op"]
        if op == "remove":
            _remove(result, operation["path"])
        elif op == "replace":
            parent, key = _pointer_parent(result, operation["path"])
            if isinstance(parent, list):
                parent[int(key)] = copy.deepcopy(operation["value"])
            else:
                parent[key] = copy.deepcopy(operation["value"])
        elif op == "add":
            _add(result, operation["path"], copy.deepcopy(operation["value"]))
        elif op in {"copy", "move"}:
            value = _remove(result, operation["from"]) if op == "move" else copy.deepcopy(
                _value_at(result, operation["from"])
            )
            _add(result, operation["path"], value)
        else:
            raise AssertionError(f"unsupported fixture patch: {op}")
    return result


def _value_at(document, pointer: str):
    value = document
    for part in pointer.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


class RuntimeConfirmationTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.documents = {
            path.name: path.read_bytes()
            for path in FIXTURE.iterdir()
            if path.suffix == ".json"
        }
        self.values = {
            name: json.loads(body) for name, body in self.documents.items()
        }
        negative = self.values["negative-vectors.json"]
        self.document_cases = {
            case["case_id"]: case for case in negative["document_cases"]
        }
        self.scenario_cases = {
            case["case_id"]: case for case in negative["scenario_cases"]
        }
        trusted = self.values["trusted-issuer-context.json"]
        self.issuer_ref = trusted["admitted_issuer_ref"]
        self.host_context = trusted["authenticated_host_context"]
        self.database_path = self.root / "runtime.sqlite3"
        self.service = self._service(self.database_path)
        self.preview_id = self._seed_preview(self.service)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _service(self, database_path: Path) -> RuntimeService:
        service = RuntimeService(
            RuntimeSettings(
                database_path,
                REPO,
                self.root / "ledger.yaml",
                confirmation_issuer_ref=self.issuer_ref,
                confirmation_host_context=self.host_context,
            ),
            now=lambda: FIXED_NOW,
        )
        service.open()
        return service

    def _seed_preview(
        self,
        service: RuntimeService,
        *,
        finalization_receipt_ref: str | None = None,
        **metadata,
    ) -> str:
        body = self.documents["capability-resolution.json"]
        artifact_metadata = {
            "media_type": "application/json",
            "schema_ref": "aci.capability-resolution@1",
            "classification": "runtime-internal",
        }
        artifact_metadata.update(metadata)
        prepared = service.artifacts.prepare(
            body,
            **artifact_metadata,
        )
        if finalization_receipt_ref is not None:
            prepared = replace(
                prepared,
                finalization_receipt_ref=finalization_receipt_ref,
            )
        service.artifacts.commit(prepared)
        return prepared.artifact_id

    def _kwargs(self, overrides: dict[str, bytes] | None = None) -> dict:
        values = dict(self.documents)
        values.update(overrides or {})
        return {
            "pending_sheet_bytes": values["pending-sheet.json"],
            "capability_resolution_bytes": values["capability-resolution.json"],
            "capability_resolution_artifact_id": self.preview_id,
            "trusted_issuer_context_bytes": values["trusted-issuer-context.json"],
            "confirmation_observation_bytes": values["confirmation-observation.json"],
            "identity_derivation_bytes": values["identity-derivation.json"],
            "payload_schema_bundle_bytes": values["confirmation-payload-schemas.json"],
            "command_bytes": values["confirmation-command.json"],
        }

    def _pure_batch(self, overrides: dict[str, bytes] | None = None):
        return build_confirmation_batch(repo_root=REPO, **self._kwargs(overrides))

    def _patched_bytes(self, case_id: str) -> tuple[str, bytes]:
        case = self.document_cases[case_id]
        document = case["document"]
        value = apply_patch(self.values[document], case["patch"])
        return document, canonical_bytes(value)

    def _assert_code(self, case_id: str, action) -> None:
        with self.assertRaises(RuntimeContractError, msg=case_id) as caught:
            action()
        self.assertEqual(caught.exception.code, self.document_cases[case_id]["error"], case_id)

    def _command_variant(self, *, key: str, command_id: str) -> bytes:
        command = copy.deepcopy(self.values["confirmation-command.json"])
        command["idempotency_key"] = key
        command["command_id"] = command_id
        return canonical_bytes(command)

    def _divergent_overrides(self, *, observation_id: str) -> dict[str, bytes]:
        observation = copy.deepcopy(self.values["confirmation-observation.json"])
        observation["observed_at"] = "2026-08-31T20:06:01.000Z"
        observation["observation_id"] = observation_id
        return self._observation_overrides(observation)

    def _observation_overrides(self, observation: dict) -> dict[str, bytes]:
        trusted = copy.deepcopy(self.values["trusted-issuer-context.json"])
        trusted["observed_confirmation"].update(
            {
                name: observation[name]
                for name in (
                    "action",
                    "dispatch_id",
                    "dispatch_revision",
                    "observed_at",
                    "presented_dispatch_spec_digest",
                    "presented_pending_sheet_digest",
                )
            }
        )
        observation_bytes = canonical_bytes(observation)
        observation_digest = digest_bytes(observation_bytes)
        authority = copy.deepcopy(self.values["confirmed-authority.json"])
        authority["confirmation_observation_digest"] = observation_digest
        authority_digest = canonical_digest(authority)
        command = copy.deepcopy(self.values["confirmation-command.json"])
        command["command_id"] = "cmd_fixture_confirmation_divergent"
        command["idempotency_key"] = "fixture-confirm-divergent"
        command["causation_id"] = observation["observation_id"]
        command["authority_context"]["confirmation_observation_digest"] = observation_digest
        command["semantic_intent"]["confirmation_observation_digest"] = observation_digest
        command["semantic_intent"]["confirmed_authority_digest"] = authority_digest
        return {
            "trusted-issuer-context.json": canonical_bytes(trusted),
            "confirmation-observation.json": observation_bytes,
            "confirmation-command.json": canonical_bytes(command),
        }

    def _counts(self, service: RuntimeService, tables: tuple[str, ...]) -> dict[str, int]:
        with service.database.connect() as conn:
            return {
                table: int(conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0])
                for table in tables
            }

    def _assert_complete_unit(self, service: RuntimeService, receipt: dict) -> None:
        """Compare the complete durable AUTH1 unit, including after reopen."""

        expected = self.values["expected-acceptance.json"]
        expected_receipt = self.values["confirmation-receipt.json"]
        self.assertEqual(receipt, expected_receipt)
        batch = self._pure_batch()
        with service.database.connect() as conn:
            self.assertEqual(
                {
                    table: int(conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0])
                    for table in (
                        "confirmation_observations",
                        "confirmed_dispatches",
                        "runs",
                        "confirmed_turn_graphs",
                        "continuation_input_mappings",
                        "events",
                        "aggregate_heads",
                        "effect_intents",
                        "command_receipts",
                        "artifacts",
                    )
                },
                {
                    "confirmation_observations": 1,
                    "confirmed_dispatches": 1,
                    "runs": 1,
                    "confirmed_turn_graphs": 1,
                    "continuation_input_mappings": 2,
                    "events": 2,
                    "aggregate_heads": 1,
                    "effect_intents": 1,
                    "command_receipts": 1,
                    "artifacts": 10,
                },
            )

            for (_, schema_ref, body), artifact_id in zip(
                batch.artifact_documents, expected_receipt["artifact_ids"]
            ):
                row = conn.execute(
                    "SELECT * FROM artifacts WHERE artifact_id=?", (artifact_id,)
                ).fetchone()
                self.assertIsNotNone(row, artifact_id)
                self.assertEqual(bytes(row["body"]), body, artifact_id)
                self.assertEqual(row["content_hash"], digest_bytes(body), artifact_id)
                self.assertEqual(row["schema_ref"], schema_ref, artifact_id)
                self.assertEqual(row["classification"], "runtime-internal", artifact_id)

            observation = dict(conn.execute("SELECT * FROM confirmation_observations").fetchone())
            for name, value in expected["confirmation_observation_record"].items():
                if name == "issuer_ref":
                    self.assertEqual(json.loads(observation["issuer_ref_json"]), value)
                else:
                    column = {
                        "artifact_id": "observation_artifact_id",
                        "digest": "observation_digest",
                    }.get(name, name)
                    self.assertEqual(observation[column], value, name)

            dispatch = dict(conn.execute("SELECT * FROM confirmed_dispatches").fetchone())
            for name, value in expected["confirmed_dispatch"].items():
                self.assertEqual(dispatch[name], value, name)

            run = dict(conn.execute("SELECT * FROM runs").fetchone())
            for name, value in expected["run"].items():
                self.assertEqual(run[name], value, name)

            graph = dict(conn.execute("SELECT * FROM confirmed_turn_graphs").fetchone())
            expected_graph = expected["turn_graph"]
            for name in (
                "graph_id",
                "dispatch_id",
                "run_id",
                "dispatch_spec_digest",
                "graph_digest",
                "continuation_id",
                "node_count",
                "edge_count",
                "mapping_count",
            ):
                self.assertEqual(graph[name], expected_graph[name], name)
            self.assertEqual(
                [entry["source_message_id"] for entry in json.loads(graph["source_messages_json"])],
                expected_graph["source_message_ids"],
            )

            mappings = [
                dict(row)
                for row in conn.execute(
                    "SELECT * FROM continuation_input_mappings ORDER BY slot_ordinal"
                )
            ]
            self.assertEqual(len(mappings), 2)
            for actual, expected_mapping in zip(
                mappings, self.values["continuation-mappings.json"]["mappings"]
            ):
                actual["visibility_policy_ref"] = json.loads(
                    actual.pop("visibility_policy_ref_json")
                )
                self.assertEqual(actual, expected_mapping)
            self.assertEqual(
                [mapping["mapping_id"] for mapping in mappings],
                expected_graph["mapping_ids"],
            )

            command_receipt = dict(conn.execute("SELECT * FROM command_receipts").fetchone())
            self.assertEqual(json.loads(command_receipt["result_receipt_json"]), receipt)
            event_rows = conn.execute("SELECT * FROM events ORDER BY journal_offset").fetchall()
            for row, expected_event in zip(event_rows, expected["events"]):
                authority = json.loads(row["authority_context_json"])
                actual_envelope = {
                    "actor_principal_id": authority["human_principal_id"],
                    "aggregate_id": row["aggregate_id"],
                    "aggregate_type": row["aggregate_type"],
                    "aggregate_version": row["aggregate_version"],
                    "causation_id": row["causation_id"],
                    "command_id": row["command_id"],
                    "correlation_id": row["correlation_id"],
                    "dispatch_id": row["correlation_id"],
                    "event_count": row["event_count"],
                    "event_id": row["event_id"],
                    "event_ordinal": row["event_ordinal"],
                    "event_type": row["event_type"],
                    "idempotency_key": command_receipt["idempotency_key"],
                    "journal_offset": row["journal_offset"],
                    "payload_hash": row["payload_hash"],
                    "payload_ref": row["payload_ref"],
                    "recorded_at": row["recorded_at"],
                    "run_id": row["aggregate_id"],
                    "schema_digest": row["schema_digest"],
                    "schema_ref": row["schema_ref"],
                }
                self.assertEqual(actual_envelope, expected_event["envelope"])

            head = dict(conn.execute("SELECT * FROM aggregate_heads").fetchone())
            self.assertEqual(head["aggregate_id"], receipt["head"]["aggregate_id"])
            self.assertEqual(head["current_version"], receipt["head"]["version"])
            self.assertEqual(head["state_hash"], receipt["head"]["state_hash"])
            self.assertEqual(
                dict(conn.execute("SELECT * FROM effect_intents").fetchone()),
                expected["effect_intent"],
            )

    def _execute_document_vectors(self) -> set[str]:
        batch = self._pure_batch()
        pure_batch_cases = {
            "trusted_issuer_forgery",
            "issuer_evidence_ref_drift",
            "issuer_evidence_digest_drift",
            "channel_principal_forgery",
            "channel_forgery",
            "action_drift",
            "observed_at_drift",
            "dispatch_mismatch",
            "dispatch_revision_mismatch",
            "presented_pending_sheet_digest_drift",
            "dispatch_spec_digest_drift",
            "observation_schema_missing",
            "observation_schema_wrong",
            "pending_sheet_digest_drift",
            "capability_resolution_drift",
            "identity_derivation_contract_drift",
            "payload_schema_bundle_drift",
            "graph_node_drift",
            "graph_edge_drift",
            "loop_ceiling_drift",
            "graph_node_add",
            "graph_node_remove",
            "graph_node_reorder",
            "graph_edge_remove",
            "graph_edge_reorder",
        }
        authority_cases = {
            "schema_versions_missing",
            "schema_versions_extra",
            "schema_versions_drift",
        }
        derived_cases = {
            "derived_identity_injection": (batch.graph, {"graph_id"}),
            "continuation_id_injection": (
                batch.graph,
                {"continuation_bindings.0.continuation_id"},
            ),
            "source_message_id_injection": (
                batch.graph,
                {"source_messages.0.source_message_id"},
            ),
            "mapping_id_injection": (batch.mapping_set, {"mappings.0.mapping_id"}),
            "event_id_injection": (
                self.values["expected-acceptance.json"],
                {"events.0.envelope.event_id"},
            ),
            "run_id_injection": (
                self.values["expected-acceptance.json"],
                {"run.run_id"},
            ),
            "effect_id_injection": (
                self.values["expected-acceptance.json"],
                {"effect_intent.effect_id"},
            ),
            "receipt_id_injection": (
                self.values["confirmation-receipt.json"],
                {"receipt_id"},
            ),
        }
        mapping_cases = {
            "mapping_cardinality_drift",
            "mapping_order_drift",
            "mapping_selector_drift",
            "mapping_binding_digest_drift",
            "mapping_target_selector_drift",
            "mapping_reverse_binding",
            "mapping_duplicate",
            "mapping_add",
            "mapping_slot_name_drift",
            "mapping_slot_ordinal_drift",
        }
        executor_ids = (
            pure_batch_cases
            | authority_cases
            | set(derived_cases)
            | mapping_cases
            | {"legacy_authority_mode", "authority_digest_conflict"}
        )
        self.assertEqual(executor_ids, set(self.document_cases))
        executed: set[str] = set()
        default_postcondition = self.values["negative-vectors.json"][
            "default_document_postcondition"
        ]

        for case_id, case in self.document_cases.items():
            with self.subTest(vector=case_id):
                required = {"case_id", "classification", "document", "error", "patch"}
                allowed = required | {"postcondition"}
                self.assertEqual(set(case) - allowed, set())
                self.assertEqual(required - set(case), set())
                self.assertEqual(case["case_id"], case_id)
                self.assertEqual(
                    case["classification"],
                    "conf_001_runtime"
                    if case_id == "authority_digest_conflict"
                    else "contract_oracle",
                )
                document, body = self._patched_bytes(case_id)
                self.assertEqual(document, case["document"])
                before = self._counts(self.service, AUTHORITY_TABLES)
                conflict_service = None

                try:
                    if case_id == "legacy_authority_mode":
                        self.service.confirm_runtime_dispatch(
                            **self._kwargs({document: body})
                        )
                    elif case_id in pure_batch_cases:
                        self._pure_batch({document: body})
                    elif case_id in authority_cases:
                        require_authority_document(json.loads(body), batch.authority)
                    elif case_id in derived_cases:
                        expected, identity_fields = derived_cases[case_id]
                        require_derived_document(
                            json.loads(body),
                            expected,
                            identity_fields=identity_fields,
                        )
                    elif case_id in mapping_cases:
                        require_derived_document(json.loads(body), batch.mapping_set)
                    else:
                        patched_authority = json.loads(body)
                        oracle_delta = {
                            key
                            for key in batch.authority
                            if batch.authority[key] != patched_authority[key]
                        }
                        self.assertEqual(
                            oracle_delta, {"confirmation_observation_digest"}
                        )
                        runtime_overrides = self._divergent_overrides(
                            observation_id="obs_fixture_vector_authority_conflict"
                        )
                        runtime_authority = self._pure_batch(runtime_overrides).authority
                        runtime_delta = {
                            key
                            for key in batch.authority
                            if batch.authority[key] != runtime_authority[key]
                        }
                        self.assertEqual(runtime_delta, oracle_delta)
                        self.assertNotEqual(
                            canonical_digest(patched_authority),
                            canonical_digest(batch.authority),
                        )
                        self.assertNotEqual(
                            canonical_digest(runtime_authority),
                            canonical_digest(batch.authority),
                        )
                        conflict_root = self.root / "vector-authority-conflict"
                        conflict_root.mkdir()
                        conflict_service = self._service(
                            conflict_root / "runtime.sqlite3"
                        )
                        self._seed_preview(conflict_service)
                        conflict_service.confirm_runtime_dispatch(**self._kwargs())
                        conflict_service.confirm_runtime_dispatch(
                            **self._kwargs(runtime_overrides)
                        )
                except RuntimeContractError as exc:
                    observed_error = exc.code
                else:
                    observed_error = "none"

                self.assertEqual(observed_error, case["error"])
                postcondition = case.get("postcondition", default_postcondition)
                tokens = set(postcondition.split("; "))
                self.assertTrue(tokens)
                if "all_confirmation_table_counts_zero" in tokens:
                    self.assertEqual(
                        self._counts(self.service, AUTHORITY_TABLES),
                        EMPTY_AUTHORITY_COUNTS,
                    )
                if "legacy_path_unchanged" in tokens:
                    self.assertEqual(
                        self._counts(self.service, AUTHORITY_TABLES), before
                    )
                if "original_acceptance_only" in tokens:
                    self.assertIsNotNone(conflict_service)
                    self.assertEqual(
                        self._counts(conflict_service, AUTHORITY_TABLES),
                        ACCEPTED_AUTHORITY_COUNTS,
                    )
                if "zero_new_rows_events_effects" in tokens:
                    target = conflict_service or self.service
                    expected = (
                        ACCEPTED_AUTHORITY_COUNTS
                        if conflict_service is not None
                        else before
                    )
                    self.assertEqual(self._counts(target, AUTHORITY_TABLES), expected)
                supported = {
                    "all_confirmation_table_counts_zero",
                    "legacy_path_unchanged",
                    "original_acceptance_only",
                    "zero_new_rows_events_effects",
                }
                self.assertEqual(tokens - supported, set())
                executed.add(case_id)
        return executed

    def _execute_scenario_vectors(self) -> set[str]:
        executed: set[str] = set()
        for case_id, case in self.scenario_cases.items():
            with self.subTest(vector=case_id):
                self.assertEqual(
                    set(case),
                    {
                        "action",
                        "case_id",
                        "classification",
                        "error",
                        "postcondition",
                        "setup",
                    },
                )
                self.assertEqual(case["case_id"], case_id)
                self.assertEqual(case["classification"], "conf_001_runtime")
                action = case["action"]
                operation = action["operation"]
                action_shapes = {
                    "register_same_observation": {"document", "operation"},
                    "register_observation": {"document", "operation", "patch"},
                    "retry_same_command": {"failpoint", "operation"},
                    "race_two_equal_authorities": {
                        "barrier",
                        "idempotency_keys",
                        "operation",
                    },
                    "race_two_divergent_authorities": {
                        "barrier",
                        "idempotency_keys",
                        "operation",
                    },
                    "observe_boundary_spies": {"operation"},
                }
                expected_action_shape = action_shapes.get(operation)
                if operation == "confirm":
                    expected_action_shape = (
                        {"idempotency_key", "operation"}
                        if "idempotency_key" in action
                        else {"document", "operation", "patch"}
                    )
                self.assertEqual(set(action), expected_action_shape)
                setup_shapes = {
                    "register_same_observation": {"accepted_observation"},
                    "register_observation": {"accepted_observation"},
                    "confirm": {"accepted_command"},
                    "retry_same_command": {"command"},
                    "race_two_equal_authorities": {"command", "dispatch_id"},
                    "race_two_divergent_authorities": {
                        "command",
                        "dispatch_id",
                    },
                    "observe_boundary_spies": {"accepted_receipt"},
                }
                self.assertEqual(set(case["setup"]), setup_shapes[operation])
                root = self.root / f"scenario-{case_id}"
                root.mkdir()
                service = self._service(root / "runtime.sqlite3")
                self._seed_preview(service)
                first = None
                results: list[dict] = []
                errors: list[Exception] = []
                process_run = None
                process_popen = None
                accepted = None

                try:
                    if operation == "register_same_observation":
                        self.assertEqual(
                            case["setup"]["accepted_observation"],
                            action["document"],
                        )
                        first = service.confirm_runtime_dispatch(**self._kwargs())
                        accepted = self._counts(service, AUTHORITY_TABLES)
                        replay_command = self._command_variant(
                            key="vector-observation-replay",
                            command_id="cmd_vector_observation_replay",
                        )
                        results.append(
                            service.confirm_runtime_dispatch(
                                **self._kwargs(
                                    {
                                        action["document"]: self.documents[action["document"]],
                                        "confirmation-command.json": replay_command,
                                    }
                                )
                            )
                        )
                        self.assertEqual(
                            self._counts(service, AUTHORITY_TABLES), accepted
                        )
                    elif operation == "register_observation":
                        self.assertEqual(
                            case["setup"]["accepted_observation"],
                            action["document"],
                        )
                        first = service.confirm_runtime_dispatch(**self._kwargs())
                        accepted = self._counts(service, AUTHORITY_TABLES)
                        observation = apply_patch(
                            self.values[action["document"]], action["patch"]
                        )
                        service.confirm_runtime_dispatch(
                            **self._kwargs(self._observation_overrides(observation))
                        )
                    elif operation == "confirm":
                        self.assertEqual(
                            case["setup"]["accepted_command"],
                            "confirmation-command.json",
                        )
                        first = service.confirm_runtime_dispatch(**self._kwargs())
                        accepted = self._counts(service, AUTHORITY_TABLES)
                        if "idempotency_key" in action:
                            command_bytes = self._command_variant(
                                key=action["idempotency_key"],
                                command_id="cmd_vector_identity_replay",
                            )
                        else:
                            self.assertEqual(
                                action["document"], "confirmation-command.json"
                            )
                            command_bytes = canonical_bytes(
                                apply_patch(
                                    self.values[action["document"]], action["patch"]
                                )
                            )
                        results.append(
                            service.confirm_runtime_dispatch(
                                **self._kwargs(
                                    {"confirmation-command.json": command_bytes}
                                )
                            )
                        )
                    elif operation == "retry_same_command":
                        self.assertEqual(
                            case["setup"]["command"], "confirmation-command.json"
                        )

                        def after_commit(name: str) -> None:
                            if name == action["failpoint"]:
                                raise RuntimeError(name)

                        with self.assertRaisesRegex(
                            RuntimeError, action["failpoint"]
                        ):
                            service.confirm_runtime_dispatch(
                                **self._kwargs(), failpoint=after_commit
                            )
                        first = self.values["confirmation-receipt.json"]
                        accepted = self._counts(service, AUTHORITY_TABLES)
                        results.append(
                            service.confirm_runtime_dispatch(**self._kwargs())
                        )
                    elif operation in {
                        "race_two_equal_authorities",
                        "race_two_divergent_authorities",
                    }:
                        self.assertEqual(
                            action["barrier"],
                            "inside_begin_immediate_before_identity_guard",
                        )
                        keys = action["idempotency_keys"]
                        self.assertEqual(len(keys), 2)
                        second_service = self._service(root / "runtime.sqlite3")
                        barrier = threading.Barrier(2)

                        def run(target_service, kwargs):
                            try:
                                barrier.wait()
                                results.append(
                                    target_service.confirm_runtime_dispatch(**kwargs)
                                )
                            except Exception as exc:
                                errors.append(exc)

                        left = self._kwargs(
                            {
                                "confirmation-command.json": self._command_variant(
                                    key=keys[0], command_id="cmd_vector_race_left"
                                )
                            }
                        )
                        right_overrides = (
                            self._divergent_overrides(
                                observation_id="obs_vector_race_divergent"
                            )
                            if operation == "race_two_divergent_authorities"
                            else {
                                "confirmation-command.json": self._command_variant(
                                    key=keys[1], command_id="cmd_vector_race_right"
                                )
                            }
                        )
                        threads = (
                            threading.Thread(target=run, args=(service, left)),
                            threading.Thread(
                                target=run,
                                args=(second_service, self._kwargs(right_overrides)),
                            ),
                        )
                        for thread in threads:
                            thread.start()
                        for thread in threads:
                            thread.join()
                        if operation == "race_two_divergent_authorities":
                            if len(errors) != 1 or not isinstance(
                                errors[0], ConfirmedAuthorityConflict
                            ):
                                raise AssertionError(errors)
                        elif errors:
                            raise AssertionError(errors)
                    elif operation == "observe_boundary_spies":
                        self.assertEqual(
                            case["setup"]["accepted_receipt"],
                            "confirmation-receipt.json",
                        )
                        with patch("subprocess.run") as process_run, patch(
                            "subprocess.Popen"
                        ) as process_popen:
                            first = service.confirm_runtime_dispatch(**self._kwargs())
                        accepted = self._counts(service, AUTHORITY_TABLES)
                        require_effect_ceiling(
                            [
                                self._pure_batch().effect_intent,
                                self._pure_batch().effect_intent,
                            ],
                            self._pure_batch().effect_intent,
                        )
                    else:
                        raise AssertionError(f"unmapped scenario operation: {operation}")
                except RuntimeContractError as exc:
                    errors.append(exc)

                observed_error = "none"
                if operation == "race_two_divergent_authorities":
                    observed_error = "one_confirmed_authority_conflict"
                elif errors:
                    self.assertEqual(len(errors), 1)
                    observed_error = errors[0].code.lower()
                self.assertEqual(observed_error, case["error"])
                self.assertEqual(
                    self._counts(service, AUTHORITY_TABLES),
                    ACCEPTED_AUTHORITY_COUNTS,
                )
                if accepted is not None:
                    self.assertEqual(
                        self._counts(service, AUTHORITY_TABLES), accepted
                    )

                tokens = set(case["postcondition"].split("; "))
                if tokens & {
                    "byte_identical_first_observation",
                    "byte_identical_first_receipt",
                }:
                    self.assertEqual(results, [first])
                if "both_results_byte_identical_first_receipt" in tokens:
                    self.assertEqual(len(results), 2)
                    self.assertEqual(results[0], results[1])
                if tokens & {
                    "one_observation_only",
                    "original_observation_only",
                    "original_acceptance_only",
                    "one_acceptance_unit",
                    "one_conflict",
                    "zero_partial_state",
                    "zero_new_rows_events_effects",
                }:
                    self.assertEqual(
                        self._counts(service, AUTHORITY_TABLES),
                        ACCEPTED_AUTHORITY_COUNTS,
                    )
                if "one_pending_audit_opening_intent_only" in tokens:
                    with service.database.connect() as conn:
                        effect = dict(
                            conn.execute("SELECT * FROM effect_intents").fetchone()
                        )
                    self.assertEqual(
                        effect,
                        self.values["expected-acceptance.json"]["effect_intent"],
                    )
                if "zero_external_calls_attempts_continuations" in tokens:
                    process_run.assert_not_called()
                    process_popen.assert_not_called()
                    self.assertEqual(
                        self._counts(
                            service,
                            ("agent_attempts", "sandbox_launch_effects"),
                        ),
                        {"agent_attempts": 0, "sandbox_launch_effects": 0},
                    )
                supported = {
                    "byte_identical_first_observation",
                    "byte_identical_first_receipt",
                    "both_results_byte_identical_first_receipt",
                    "one_observation_only",
                    "original_observation_only",
                    "original_acceptance_only",
                    "one_acceptance_unit",
                    "one_conflict",
                    "zero_partial_state",
                    "zero_new_rows_events_effects",
                    "one_pending_audit_opening_intent_only",
                    "zero_external_calls_attempts_continuations",
                }
                self.assertEqual(tokens - supported, set())
                executed.add(case_id)
        return executed

    def test_auth1_golden_runtime_unit_and_legacy_rejection(self) -> None:
        receipt = self.service.confirm_runtime_dispatch(**self._kwargs())
        self._assert_complete_unit(self.service, receipt)

        legacy_root = self.root / "legacy"
        legacy_root.mkdir()
        legacy = self._service(legacy_root / "runtime.sqlite3")
        self._seed_preview(legacy)
        document, body = self._patched_bytes("legacy_authority_mode")
        self.assertEqual(document, "pending-sheet.json")
        with self.assertRaises(RuntimeContractError) as caught:
            legacy.confirm_runtime_dispatch(**self._kwargs({document: body}))
        self.assertEqual(caught.exception.code, "legacy_authority_mode")
        self.assertEqual(
            self._counts(legacy, ("confirmed_dispatches", "runs", "events", "effect_intents")),
            {"confirmed_dispatches": 0, "runs": 0, "events": 0, "effect_intents": 0},
        )

    def test_auth2_canonical_package_authority_and_identities(self) -> None:
        manifest = self.values["manifest.json"]
        self.assertEqual(canonical_bytes(manifest), self.documents["manifest.json"])
        for name, expected_digest in manifest["documents"].items():
            body = self.documents[name]
            self.assertEqual(canonical_bytes(json.loads(body)), body, name)
            self.assertEqual(digest_bytes(body), expected_digest, name)
        batch = self._pure_batch()
        expected_documents = {
            "dispatch-spec.json": batch.dispatch_spec,
            "confirmed-turn-graph.json": batch.graph,
            "continuation-mappings.json": batch.mapping_set,
            "confirmed-authority.json": batch.authority,
            "run-created-payload.json": batch.run_created_payload,
            "audit-opening-requested-payload.json": batch.audit_opening_requested_payload,
            "audit-opening-effect.json": batch.effect_payload,
        }
        for name, actual in expected_documents.items():
            self.assertEqual(actual, self.values[name], name)
        ids = manifest["expected_ids"]
        self.assertEqual(batch.run_record["run_id"], ids["run_id"])
        self.assertEqual(batch.graph_record["graph_id"], ids["graph_id"])
        self.assertEqual(batch.graph_record["continuation_id"], ids["continuation_id"])
        self.assertEqual([row["mapping_id"] for row in batch.mapping_records], ids["mapping_ids"])
        self.assertEqual(batch.effect_intent["effect_id"], ids["opening_effect_id"])
        self.assertEqual(batch.receipt_id, ids["receipt_id"])
        self.assertEqual(
            [message["source_message_id"] for message in batch.graph["source_messages"]],
            ids["source_message_ids"],
        )
        legacy_body = self.service.artifacts.get_authorized(
            self.preview_id,
            principal_id="runtime-confirmation",
            action="artifact.read",
            authorizer=lambda _principal, _action, classification: (
                classification == "runtime-internal"
            ),
        )
        self.assertEqual(legacy_body, self.documents["capability-resolution.json"])
        self.assertEqual(
            self.preview_id,
            "art_" + digest_bytes(legacy_body).removeprefix("sha256:")[:32],
        )
        referenced_body, reference = self.service.artifacts.get_authorized_with_reference(
            self.preview_id,
            principal_id="runtime-confirmation",
            action="artifact.read",
            authorizer=lambda _principal, _action, classification: (
                classification == "runtime-internal"
            ),
        )
        self.assertEqual(referenced_body, legacy_body)
        self.assertEqual(reference["artifact_id"], self.preview_id)
        self.assertEqual(reference["schema_ref"], "aci.capability-resolution@1")
        self.assertTrue(str(reference["finalization_receipt_ref"]).startswith("afr_"))

    def test_auth3_trusted_observation_boundary_and_identity(self) -> None:
        case_ids = (
            "trusted_issuer_forgery",
            "issuer_evidence_ref_drift",
            "issuer_evidence_digest_drift",
            "channel_principal_forgery",
            "channel_forgery",
            "action_drift",
            "observed_at_drift",
            "dispatch_mismatch",
            "dispatch_revision_mismatch",
            "presented_pending_sheet_digest_drift",
            "dispatch_spec_digest_drift",
            "observation_schema_missing",
            "observation_schema_wrong",
        )
        for case_id in case_ids:
            with self.subTest(case_id=case_id):
                document, body = self._patched_bytes(case_id)
                self._assert_code(
                    case_id,
                    lambda document=document, body=body: self._pure_batch({document: body}),
                )

        first = self.service.confirm_runtime_dispatch(**self._kwargs())
        replay = self.service.confirm_runtime_dispatch(
            **self._kwargs(
                {
                    "confirmation-command.json": self._command_variant(
                        key="fixture-confirm-observation-replay",
                        command_id="cmd_fixture_observation_replay",
                    )
                }
            )
        )
        self.assertEqual(replay, first)
        with self.assertRaises(ConfirmationObservationConflict):
            self.service.confirm_runtime_dispatch(
                **self._kwargs(self._divergent_overrides(observation_id="obs_fixture_chat_001"))
            )

    def test_auth4_digest_domains_and_closed_schema_lineage(self) -> None:
        for case_id in (
            "pending_sheet_digest_drift",
            "capability_resolution_drift",
            "identity_derivation_contract_drift",
            "payload_schema_bundle_drift",
        ):
            with self.subTest(case_id=case_id):
                document, body = self._patched_bytes(case_id)
                self._assert_code(
                    case_id,
                    lambda document=document, body=body: self._pure_batch({document: body}),
                )
        batch = self._pure_batch()
        digests = {
            digest_bytes(self.documents["pending-sheet.json"]),
            canonical_digest(batch.dispatch_spec),
            canonical_digest(batch.authority),
        }
        self.assertEqual(len(digests), 3)
        for case_id in (
            "schema_versions_missing",
            "schema_versions_extra",
            "schema_versions_drift",
        ):
            with self.subTest(case_id=case_id):
                _, body = self._patched_bytes(case_id)
                actual = json.loads(body)
                self._assert_code(
                    case_id,
                    lambda actual=actual: require_authority_document(actual, batch.authority),
                )

        preview_metadata_cases = {
            "schema-ref": {"schema_ref": "aci.capability-resolution@999"},
            "media-type": {"media_type": "application/octet-stream"},
            "classification": {"classification": "public"},
            "redaction-policy": {"redaction_policy_ref": "aci.redaction.mask@1"},
            "retention-policy": {"retention_policy_ref": "aci.retention.forever@1"},
            "tombstone-policy": {"tombstone_policy_ref": "aci.tombstone.delete@1"},
            "authorization-policy": {
                "authorization_policy_ref": "aci.artifact.public-reader@1"
            },
            "policy-bundle-digest": {"policy_bundle_digest": "sha256:" + "f" * 64},
            "finalization-receipt": {"finalization_receipt_ref": "invalid"},
        }
        for case_id, metadata in preview_metadata_cases.items():
            with self.subTest(case_id=case_id):
                root = self.root / f"preview-{case_id}"
                root.mkdir()
                service = self._service(root / "runtime.sqlite3")
                preview_id = self._seed_preview(service, **metadata)
                kwargs = self._kwargs()
                kwargs["capability_resolution_artifact_id"] = preview_id
                with self.assertRaises(RuntimeContractError):
                    service.confirm_runtime_dispatch(**kwargs)
                self.assertEqual(
                    self._counts(service, AUTHORITY_TABLES),
                    EMPTY_AUTHORITY_COUNTS,
                )

    def test_auth5_bounded_projection_mapping_and_derived_identity_rejection(self) -> None:
        batch = self._pure_batch()
        pending_cases = (
            "graph_node_drift",
            "graph_edge_drift",
            "loop_ceiling_drift",
            "graph_node_add",
            "graph_node_remove",
            "graph_node_reorder",
            "graph_edge_remove",
            "graph_edge_reorder",
        )
        for case_id in pending_cases:
            with self.subTest(case_id=case_id):
                document, body = self._patched_bytes(case_id)
                self._assert_code(
                    case_id,
                    lambda document=document, body=body: self._pure_batch({document: body}),
                )

        derived_cases = {
            "derived_identity_injection": (batch.graph, {"graph_id"}),
            "continuation_id_injection": (
                batch.graph,
                {"continuation_bindings.0.continuation_id"},
            ),
            "source_message_id_injection": (
                batch.graph,
                {"source_messages.0.source_message_id"},
            ),
            "mapping_id_injection": (batch.mapping_set, {"mappings.0.mapping_id"}),
            "event_id_injection": (
                self.values["expected-acceptance.json"],
                {"events.0.envelope.event_id"},
            ),
            "run_id_injection": (
                self.values["expected-acceptance.json"],
                {"run.run_id"},
            ),
            "effect_id_injection": (
                self.values["expected-acceptance.json"],
                {"effect_intent.effect_id"},
            ),
            "receipt_id_injection": (
                self.values["confirmation-receipt.json"],
                {"receipt_id"},
            ),
        }
        for case_id, (expected, identity_fields) in derived_cases.items():
            with self.subTest(case_id=case_id):
                _, body = self._patched_bytes(case_id)
                actual = json.loads(body)
                self._assert_code(
                    case_id,
                    lambda actual=actual, expected=expected, identity_fields=identity_fields: (
                        require_derived_document(
                            actual,
                            expected,
                            identity_fields=identity_fields,
                        )
                    ),
                )

        mapping_cases = (
            "mapping_cardinality_drift",
            "mapping_order_drift",
            "mapping_selector_drift",
            "mapping_binding_digest_drift",
            "mapping_target_selector_drift",
            "mapping_reverse_binding",
            "mapping_duplicate",
            "mapping_add",
            "mapping_slot_name_drift",
            "mapping_slot_ordinal_drift",
        )
        for case_id in mapping_cases:
            with self.subTest(case_id=case_id):
                _, body = self._patched_bytes(case_id)
                actual = json.loads(body)
                self._assert_code(
                    case_id,
                    lambda actual=actual: require_derived_document(actual, batch.mapping_set),
                )

    def test_auth6_key_identity_replay_conflict_and_concurrency(self) -> None:
        first = self.service.confirm_runtime_dispatch(**self._kwargs())
        self.assertEqual(self.service.confirm_runtime_dispatch(**self._kwargs()), first)
        drift = copy.deepcopy(self.values["confirmation-command.json"])
        drift["semantic_intent"]["dispatch_revision"] = "r2"
        with self.assertRaises(IdempotencyConflict):
            self.service.confirm_runtime_dispatch(
                **self._kwargs({"confirmation-command.json": canonical_bytes(drift)})
            )
        malformed_prerequisite = copy.deepcopy(
            self.values["confirmation-command.json"]
        )
        malformed_prerequisite["prerequisites"] = [
            {"aggregate_id": "foreign", "expected_version": 999}
        ]
        with self.assertRaises(RuntimeContractError) as malformed:
            self.service.confirm_runtime_dispatch(
                **self._kwargs(
                    {
                        "confirmation-command.json": canonical_bytes(
                            malformed_prerequisite
                        )
                    }
                )
            )
        self.assertEqual(malformed.exception.code, "confirmation_projection_mismatch")
        divergent_prerequisite = copy.deepcopy(
            self.values["confirmation-command.json"]
        )
        divergent_prerequisite["prerequisites"] = [
            {
                "aggregate_id": "foreign",
                "expected_version": 999,
                "state_hash": "sha256:" + "0" * 64,
            }
        ]
        with self.assertRaises(IdempotencyConflict):
            self.service.confirm_runtime_dispatch(
                **self._kwargs(
                    {
                        "confirmation-command.json": canonical_bytes(
                            divergent_prerequisite
                        )
                    }
                )
            )
        self.assertEqual(
            self._counts(
                self.service,
                ("confirmed_dispatches", "runs", "effect_intents", "command_receipts"),
            ),
            {
                "confirmed_dispatches": 1,
                "runs": 1,
                "effect_intents": 1,
                "command_receipts": 1,
            },
        )
        identity_replay = self.service.confirm_runtime_dispatch(
            **self._kwargs(
                {
                    "confirmation-command.json": self._command_variant(
                        key="fixture-confirm-002", command_id="cmd_fixture_confirmation_002"
                    )
                }
            )
        )
        self.assertEqual(identity_replay, first)
        with self.assertRaises(ConfirmedAuthorityConflict):
            self.service.confirm_runtime_dispatch(
                **self._kwargs(self._divergent_overrides(observation_id="obs_fixture_chat_002"))
            )

        for divergent in (False, True):
            with self.subTest(divergent=divergent):
                race_root = self.root / ("race-divergent" if divergent else "race-equal")
                race_root.mkdir()
                database = race_root / "runtime.sqlite3"
                first_service = self._service(database)
                self._seed_preview(first_service)
                second_service = self._service(database)
                barrier = threading.Barrier(2)
                results: list[dict] = []
                errors: list[Exception] = []

                def run(service, kwargs):
                    try:
                        barrier.wait()
                        results.append(service.confirm_runtime_dispatch(**kwargs))
                    except Exception as exc:  # evidence collection for the race
                        errors.append(exc)

                left = self._kwargs(
                    {
                        "confirmation-command.json": self._command_variant(
                            key="race-a", command_id="cmd_race_a"
                        )
                    }
                )
                right_overrides = (
                    self._divergent_overrides(observation_id="obs_race_divergent")
                    if divergent
                    else {
                        "confirmation-command.json": self._command_variant(
                            key="race-b", command_id="cmd_race_b"
                        )
                    }
                )
                right = self._kwargs(right_overrides)
                threads = [
                    threading.Thread(target=run, args=(first_service, left)),
                    threading.Thread(target=run, args=(second_service, right)),
                ]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
                if divergent:
                    self.assertEqual(len(results), 1)
                    self.assertEqual(len(errors), 1)
                    self.assertIsInstance(errors[0], ConfirmedAuthorityConflict)
                else:
                    self.assertEqual(errors, [])
                    self.assertEqual(len(results), 2)
                    self.assertEqual(results[0], results[1])
                self.assertEqual(
                    self._counts(first_service, ("confirmed_dispatches", "runs", "effect_intents")),
                    {"confirmed_dispatches": 1, "runs": 1, "effect_intents": 1},
                )

    def test_auth7_all_failpoints_lost_response_reopen_and_migration(self) -> None:
        failpoints = self.values["negative-vectors.json"]["failpoints"]
        self.assertEqual(len(failpoints), 21)
        owned_tables = (
            "confirmation_observations",
            "confirmed_dispatches",
            "runs",
            "confirmed_turn_graphs",
            "continuation_input_mappings",
            "events",
            "aggregate_heads",
            "effect_intents",
            "command_receipts",
        )
        for index, point in enumerate(failpoints):
            with self.subTest(point=point):
                root = self.root / f"fail-{index}"
                root.mkdir()
                service = self._service(root / "runtime.sqlite3")
                self._seed_preview(service)

                def failpoint(name: str, target=point) -> None:
                    if name == target:
                        raise RuntimeError(target)

                with self.assertRaisesRegex(RuntimeError, point):
                    service.confirm_runtime_dispatch(
                        **self._kwargs(), failpoint=failpoint
                    )
                reopened = self._service(root / "runtime.sqlite3")
                self.assertEqual(
                    self._counts(reopened, owned_tables),
                    {table: 0 for table in owned_tables},
                )
                self.assertEqual(self._counts(reopened, ("artifacts",)), {"artifacts": 1})

        lost_root = self.root / "lost"
        lost_root.mkdir()
        lost = self._service(lost_root / "runtime.sqlite3")
        self._seed_preview(lost)

        def after_commit(name: str) -> None:
            if name == "confirmation.after_commit":
                raise RuntimeError(name)

        with self.assertRaisesRegex(RuntimeError, "after_commit"):
            lost.confirm_runtime_dispatch(**self._kwargs(), failpoint=after_commit)
        reopened = self._service(lost_root / "runtime.sqlite3")
        self.assertEqual(reopened.database.migrate(), [])
        recovered = reopened.confirm_runtime_dispatch(**self._kwargs())
        self.assertEqual(recovered, self.values["confirmation-receipt.json"])
        with reopened.database.connect() as conn:
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 16)
            migration = dict(
                conn.execute(
                    "SELECT name,checksum FROM schema_migrations WHERE version=15"
                ).fetchone()
            )
            self.assertEqual(migration["name"], "015_runtime_attempt_result_bus.sql")
            self.assertEqual(
                migration["checksum"],
                digest_bytes(
                    (
                        REPO
                        / "implementations/server/runtime/migrations/"
                        "015_runtime_attempt_result_bus.sql"
                    ).read_bytes()
                ),
            )
            self.assertEqual(conn.execute("PRAGMA quick_check").fetchone()[0], "ok")
        self._assert_complete_unit(reopened, recovered)

    def test_auth8_effect_ceiling_and_zero_external_actions(self) -> None:
        executed = self._execute_document_vectors() | self._execute_scenario_vectors()
        all_cases = set(self.document_cases) | set(self.scenario_cases)
        self.assertEqual(executed, all_cases)
        self.assertEqual(len(executed), 56)
        with patch("subprocess.run") as process_run, patch("subprocess.Popen") as process_popen:
            receipt = self.service.confirm_runtime_dispatch(**self._kwargs())
        process_run.assert_not_called()
        process_popen.assert_not_called()
        self.assertEqual(receipt, self.values["confirmation-receipt.json"])
        with self.service.database.connect() as conn:
            effect = dict(conn.execute("SELECT * FROM effect_intents").fetchone())
            attempts = conn.execute("SELECT count(*) FROM agent_attempts").fetchone()[0]
            launch_effects = conn.execute("SELECT count(*) FROM sandbox_launch_effects").fetchone()[0]
        self.assertEqual(effect, self.values["expected-acceptance.json"]["effect_intent"])
        self.assertEqual(attempts, 0)
        self.assertEqual(launch_effects, 0)
        with self.assertRaises(RuntimeContractError) as caught:
            require_effect_ceiling(
                [self._pure_batch().effect_intent, self._pure_batch().effect_intent],
                self._pure_batch().effect_intent,
            )
        self.assertEqual(caught.exception.code, "forbidden_effect_boundary")


if __name__ == "__main__":
    unittest.main()
