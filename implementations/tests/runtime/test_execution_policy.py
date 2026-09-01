from __future__ import annotations

import ast
import copy
import inspect
import json
import os
import socket
import sqlite3
import subprocess
import time
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

from implementations.server.runtime.canonical import canonical_bytes, digest_bytes
from implementations.server.runtime import execution_policy as execution_policy_module
from implementations.server.runtime.execution_policy import (
    INT64_MAX,
    ExecutionPolicyContractError,
    ParsedExecutionPolicyOracleFixtureForTest,
    ParsedHarnessAuthorityFenceForTest,
    ParsedProductionAuthorityFence,
    parse_execution_authority_fence,
    parse_execution_authority_fence_harness_for_test,
    parse_execution_policy_oracle_fixture_for_test,
    parse_production_policy_document,
    parse_resource_budget,
    parse_sandbox_policy,
    versioned_reference_key,
)


FIXTURE_PATH = Path(__file__).with_name("execution_policy_oracle_v1.json")

# Independent test authority copied literally from reviewed TECH-POLICY-D0.  Neither
# bytes nor digests are derived from the checked-in fixture being tested.
AUTHORITY_VECTORS = {
    "budget_policy": (
        b'{"exhaustion_action":"deny-new-work","schema":"aci.budget-policy@1",'
        b'"scope":"attempt","unknown_usage_action":"deny-new-work"}',
        "sha256:08f3494d9e869053ee097e854840ade80afcda65cce75ef774038be5c6c242d2",
    ),
    "sandbox_enforcement_policy": (
        b'{"enforcement_mode":"deny-all","schema":"aci.sandbox-enforcement-policy@1",'
        b'"unsupported_control_action":"deny"}',
        "sha256:88f400d1661b69ac6536b548216bb7f5a370042050df2ea7bae49e03952725ea",
    ),
    "resource_budget": (
        b'{"budget_policy_ref":{"digest":"sha256:08f3494d9e869053ee097e854840ade80'
        b'afcda65cce75ef774038be5c6c242d2","name":"aci.budget-policy.fake-deny-all",'
        b'"version":"1"},"max_artifact_bytes":0,"max_input_tokens":0,'
        b'"max_output_tokens":0,"max_payload_bytes":0,"max_tool_calls":0,'
        b'"max_wall_time_ms":0,"schema":"aci.resource-budget@1"}',
        "sha256:e6e3a27b6fecf0ca8667ca722bb1e74a39e4d1f685da172f75a8077a67ba3836",
    ),
    "sandbox_policy": (
        b'{"credential_refs":[],"filesystem_scope":{"default":"deny","link_policy":"deny",'
        b'"read_roots":[],"write_roots":[]},"network_scope":{"allowed_endpoints":[],'
        b'"default":"deny"},"policy_ref":{"digest":"sha256:88f400d1661b69ac6536b548216bb7f5'
        b'a370042050df2ea7bae49e03952725ea","name":"aci.sandbox-policy.fake-deny-all",'
        b'"version":"1"},"process_scope":{"allowed_executables":[],"default":"deny",'
        b'"max_child_processes":0},"schema":"aci.sandbox-policy@1"}',
        "sha256:d865e9f97c6b73afc4748e5bd6d58095e471450d72cd45c3fb4a55a8185e3b1a",
    ),
    "combined_oracle": (
        b'{"resource_budget":{"budget_policy_ref":{"digest":"sha256:08f3494d9e869053ee097e854840ade80'
        b'afcda65cce75ef774038be5c6c242d2","name":"aci.budget-policy.fake-deny-all",'
        b'"version":"1"},"max_artifact_bytes":0,"max_input_tokens":0,'
        b'"max_output_tokens":0,"max_payload_bytes":0,"max_tool_calls":0,'
        b'"max_wall_time_ms":0,"schema":"aci.resource-budget@1"},'
        b'"resource_budget_digest":"sha256:e6e3a27b6fecf0ca8667ca722bb1e74a39e4d1f685da172f75a8077a67ba3836",'
        b'"sandbox_policy":{"credential_refs":[],"filesystem_scope":{"default":"deny",'
        b'"link_policy":"deny","read_roots":[],"write_roots":[]},"network_scope":{'
        b'"allowed_endpoints":[],"default":"deny"},"policy_ref":{"digest":"sha256:'
        b'88f400d1661b69ac6536b548216bb7f5a370042050df2ea7bae49e03952725ea",'
        b'"name":"aci.sandbox-policy.fake-deny-all","version":"1"},"process_scope":{'
        b'"allowed_executables":[],"default":"deny","max_child_processes":0},'
        b'"schema":"aci.sandbox-policy@1"},"sandbox_policy_digest":"sha256:'
        b'd865e9f97c6b73afc4748e5bd6d58095e471450d72cd45c3fb4a55a8185e3b1a",'
        b'"schema":"aci.execution-policy-oracle-fixture@1"}',
        "sha256:9abfb7e61f995a90e8a08a72dfa96dda2df956f63e4e4360e78eca22493641f6",
    ),
    "harness_fence_preimage": (
        b'{"authority_mode":"runtime-managed","cutover_epoch":1,'
        b'"dispatch_id":"dispatch_policy_oracle_fixture",'
        b'"legacy_watcher_disabled_evidence_ref":'
        b'"art_policy_harness_watcher_disabled_fixture",'
        b'"run_id":"run_policy_oracle_fixture",'
        b'"schema":"aci.execution-authority-fence-harness-preimage@1"}',
        "sha256:124d06fa0b4c2e55eef48bc5b0c33ce19880d15ce82e0d3af9518a80536de70f",
    ),
    "harness_fence_document": (
        b'{"authority_mode":"runtime-managed","cutover_epoch":1,'
        b'"dispatch_id":"dispatch_policy_oracle_fixture",'
        b'"fence_digest":"sha256:124d06fa0b4c2e55eef48bc5b0c33ce19880d15ce82e0d3af9518a80536de70f",'
        b'"legacy_watcher_disabled_evidence_ref":'
        b'"art_policy_harness_watcher_disabled_fixture",'
        b'"run_id":"run_policy_oracle_fixture",'
        b'"schema":"aci.execution-authority-fence-harness@1"}',
        "sha256:4672e47ccc7fb906a14c0cd57de0bbd74271cfb7697d3a539dc97251bb864ba4",
    ),
}


def raw_json(value) -> bytes:
    """Emit syntactically valid JSON without applying aci-cjson-1 first."""

    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def nested_member(value, path):
    current = value
    for component in path:
        current = current[component]
    return current


def json_with_duplicate(value, object_path, duplicate_field, path=()) -> bytes:
    """Serialize one otherwise-canonical document with one duplicate member."""

    if isinstance(value, dict):
        members = []
        for key in sorted(value):
            rendered = (
                json.dumps(key, ensure_ascii=False).encode("utf-8")
                + b":"
                + json_with_duplicate(
                    value[key], object_path, duplicate_field, path + (key,)
                )
            )
            members.append(rendered)
            if path == object_path and key == duplicate_field:
                members.append(rendered)
        return b"{" + b",".join(members) + b"}"
    if isinstance(value, list):
        return b"[" + b",".join(
            json_with_duplicate(item, object_path, duplicate_field, path + (index,))
            for index, item in enumerate(value)
        ) + b"]"
    return raw_json(value)


class ExecutionPolicyOracleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        transport = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.transport = transport
        cls.fixture_vectors = {
            item["name"]: (item["canonical_json"].encode("utf-8"), item["digest"])
            for item in transport["vectors"]
        }
        cls.vectors = AUTHORITY_VECTORS

    def setUp(self) -> None:
        self.budget_target = self.vectors["budget_policy"][0]
        self.sandbox_target = self.vectors["sandbox_enforcement_policy"][0]
        self.budget_bytes = self.vectors["resource_budget"][0]
        self.sandbox_bytes = self.vectors["sandbox_policy"][0]
        self.oracle_bytes = self.vectors["combined_oracle"][0]
        self.harness_bytes = self.vectors["harness_fence_document"][0]
        self.budget = json.loads(self.budget_bytes)
        self.sandbox = json.loads(self.sandbox_bytes)
        self.harness = json.loads(self.harness_bytes)

    def assert_rejected(self, callable_, *args, **kwargs) -> None:
        with self.assertRaises(ExecutionPolicyContractError):
            callable_(*args, **kwargs)

    def parse_budget(self, value=None, target=None, tool_profile="tool.none"):
        raw = self.budget_bytes if value is None else canonical_bytes(value)
        return parse_resource_budget(
            raw,
            self.budget_target if target is None else target,
            tool_profile,
        )

    def parse_sandbox(self, value=None, target=None, credentials=None):
        raw = self.sandbox_bytes if value is None else canonical_bytes(value)
        return parse_sandbox_policy(
            raw,
            self.sandbox_target if target is None else target,
            {} if credentials is None else credentials,
        )

    def test_fixture_is_closed_non_executable_seven_vector_transport(self) -> None:
        self.assertEqual(
            set(self.transport), {"schema", "authority", "vectors"}
        )
        self.assertEqual(self.transport["schema"], "aci.execution-policy-oracle-vectors@1")
        self.assertEqual(self.transport["authority"], "test-only-non-executable")
        self.assertEqual(len(self.vectors), 7)
        self.assertEqual(self.fixture_vectors, AUTHORITY_VECTORS)
        self.assertEqual(
            set(self.vectors),
            {
                "budget_policy",
                "sandbox_enforcement_policy",
                "resource_budget",
                "sandbox_policy",
                "combined_oracle",
                "harness_fence_preimage",
                "harness_fence_document",
            },
        )

    def test_all_seven_literal_bytes_and_qualified_digests(self) -> None:
        for name, (raw, expected) in self.vectors.items():
            with self.subTest(name=name):
                self.assertEqual(canonical_bytes(json.loads(raw)), raw)
                self.assertEqual(digest_bytes(raw), expected)
                drift = raw[:-1] + (b" " if raw[-1:] != b" " else b"\t")
                self.assertNotEqual(digest_bytes(drift), expected)

    def test_all_five_document_parsers_require_exact_raw_canonical_bytes(self) -> None:
        production_fence = canonical_bytes(self._production_fence())
        cases = (
            (
                "resource-budget",
                self.budget_bytes,
                lambda raw: parse_resource_budget(raw, self.budget_target, "tool.none"),
            ),
            (
                "sandbox-policy",
                self.sandbox_bytes,
                lambda raw: parse_sandbox_policy(raw, self.sandbox_target, {}),
            ),
            (
                "production-fence",
                production_fence,
                parse_execution_authority_fence,
            ),
            (
                "harness-fence",
                self.harness_bytes,
                parse_execution_authority_fence_harness_for_test,
            ),
            (
                "combined-oracle",
                self.oracle_bytes,
                lambda raw: parse_execution_policy_oracle_fixture_for_test(
                    raw,
                    self.budget_bytes,
                    self.sandbox_bytes,
                    self.budget_target,
                    self.sandbox_target,
                    {},
                    "tool.none",
                ),
            ),
        )
        for label, raw, parser in cases:
            decoded = json.loads(raw)
            reversed_top = raw_json(dict(reversed(list(decoded.items()))))
            escaped = raw.replace(b"runtime-managed", b"\\u0072untime-managed", 1)
            if escaped == raw:
                escaped = raw.replace(b"aci", b"\\u0061ci", 1)
            for fault, candidate in (
                ("leading-whitespace", b" " + raw),
                ("trailing-whitespace", raw + b"\n"),
                ("key-order", reversed_top),
                ("escape-spelling", escaped),
            ):
                with self.subTest(document=label, fault=fault):
                    self.assertNotEqual(candidate, raw)
                    self.assert_rejected(parser, candidate)
        for label, raw, parser, marker in (
            ("resource-budget", self.budget_bytes, cases[0][2], b'"max_wall_time_ms":0'),
            ("sandbox-policy", self.sandbox_bytes, cases[1][2], b'"max_child_processes":0'),
            ("combined-oracle", self.oracle_bytes, cases[4][2], b'"max_wall_time_ms":0'),
        ):
            with self.subTest(document=label, fault="negative-zero"):
                self.assert_rejected(parser, raw.replace(marker, marker[:-1] + b"-0", 1))

    def test_decoder_limits_are_typed_contract_rejections(self) -> None:
        oversized_integer = self.budget_bytes.replace(
            b'"max_wall_time_ms":0',
            b'"max_wall_time_ms":' + b"9" * 5000,
        )
        deeply_nested = b'{"x":' + b"[" * 2000 + b"0" + b"]" * 2000 + b"}"
        malformed = self.budget_bytes[:-1]
        invalid_utf8 = b'{"schema":"aci.resource-budget@1","x":"\xff"}'
        for fault, raw in (
            ("integer-conversion-limit", oversized_integer),
            ("decoder-recursion-limit", deeply_nested),
            ("malformed-json", malformed),
            ("invalid-utf8", invalid_utf8),
        ):
            with self.subTest(fault=fault):
                try:
                    parse_resource_budget(raw, self.budget_target, "tool.none")
                except ExecutionPolicyContractError:
                    pass
                except (ValueError, RecursionError, OverflowError) as exc:
                    self.fail(f"raw decoder exception leaked: {type(exc).__name__}")
                else:
                    self.fail("bounded decoder fault unexpectedly accepted")

    def test_valid_budget_reproduces_golden_and_explicit_zero(self) -> None:
        parsed = self.parse_budget()
        self.assertEqual(parsed.canonical_bytes, self.budget_bytes)
        self.assertEqual(parsed.content_digest, self.vectors["resource_budget"][1])
        for name in (
            "max_wall_time_ms",
            "max_input_tokens",
            "max_output_tokens",
            "max_tool_calls",
            "max_payload_bytes",
            "max_artifact_bytes",
        ):
            self.assertEqual(parsed.value[name], 0)

    def test_budget_is_recursively_closed_and_duplicate_safe(self) -> None:
        for mutation in ("missing", "extra", "ref_missing", "ref_extra"):
            value = copy.deepcopy(self.budget)
            if mutation == "missing":
                del value["max_wall_time_ms"]
            elif mutation == "extra":
                value["wall_clock_seconds"] = 1
            elif mutation == "ref_missing":
                del value["budget_policy_ref"]["version"]
            else:
                value["budget_policy_ref"]["secret"] = "forbidden"
            with self.subTest(mutation=mutation):
                self.assert_rejected(
                    parse_resource_budget,
                    canonical_bytes(value),
                    self.budget_target,
                    "tool.none",
                )
        duplicate = self.budget_bytes[:-1] + b',"schema":"aci.resource-budget@1"}'
        self.assert_rejected(
            parse_resource_budget, duplicate, self.budget_target, "tool.none"
        )

    def test_every_budget_integer_rejects_wrong_primitives_and_range(self) -> None:
        names = (
            "max_wall_time_ms",
            "max_input_tokens",
            "max_output_tokens",
            "max_tool_calls",
            "max_payload_bytes",
            "max_artifact_bytes",
        )
        invalid = (True, "0", 0.0, -1, INT64_MAX + 1, None)
        for name in names:
            for candidate in invalid:
                value = copy.deepcopy(self.budget)
                value[name] = candidate
                with self.subTest(name=name, candidate=candidate):
                    self.assert_rejected(
                        parse_resource_budget,
                        raw_json(value),
                        self.budget_target,
                        "tool.other" if name == "max_tool_calls" else "tool.none",
                    )

    def test_every_integer_leaf_rejects_every_invalid_json_numeric_representation(self) -> None:
        zero_domain_tokens = (
            b"true",
            b'"0"',
            b"0.0",
            b"-1",
            b"9223372036854775808",
            b"18446744073709551616",
            b"null",
            b"NaN",
            b"Infinity",
            b"-Infinity",
            b"-0",
            b"1e0",
            b"00",
            b"+0",
        )
        budget_fields = (
            "max_wall_time_ms",
            "max_input_tokens",
            "max_output_tokens",
            "max_tool_calls",
            "max_payload_bytes",
            "max_artifact_bytes",
        )
        for field in budget_fields:
            marker = f'"{field}":0'.encode("ascii")
            for token in zero_domain_tokens:
                raw = self.budget_bytes.replace(marker, marker[:-1] + token, 1)
                with self.subTest(document="budget", field=field, token=token):
                    self.assert_rejected(
                        parse_resource_budget,
                        raw,
                        self.budget_target,
                        "tool.other" if field == "max_tool_calls" else "tool.none",
                    )

        child_marker = b'"max_child_processes":0'
        for token in zero_domain_tokens:
            raw = self.sandbox_bytes.replace(
                child_marker, child_marker[:-1] + token, 1
            )
            with self.subTest(document="sandbox", field="max_child_processes", token=token):
                self.assert_rejected(
                    parse_sandbox_policy, raw, self.sandbox_target, {}
                )

        positive_domain_tokens = (
            b"true",
            b'"1"',
            b"1.0",
            b"0",
            b"-1",
            b"9223372036854775808",
            b"18446744073709551616",
            b"null",
            b"NaN",
            b"Infinity",
            b"-Infinity",
            b"-0",
            b"1e0",
            b"01",
            b"+1",
        )
        fence_cases = (
            ("production", canonical_bytes(self._production_fence()), parse_execution_authority_fence),
            ("harness", self.harness_bytes, parse_execution_authority_fence_harness_for_test),
        )
        marker = b'"cutover_epoch":1'
        for domain, base, parser in fence_cases:
            for token in positive_domain_tokens:
                raw = base.replace(marker, marker[:-1] + token, 1)
                with self.subTest(document=domain, field="cutover_epoch", token=token):
                    self.assert_rejected(parser, raw)

    def test_budget_integer_upper_bound_accepts_without_coercion(self) -> None:
        value = copy.deepcopy(self.budget)
        for name in (
            "max_wall_time_ms",
            "max_input_tokens",
            "max_output_tokens",
            "max_payload_bytes",
            "max_artifact_bytes",
        ):
            value[name] = INT64_MAX
        value["max_tool_calls"] = INT64_MAX
        parsed = self.parse_budget(value, tool_profile="tool.other")
        self.assertEqual(parsed.value["max_wall_time_ms"], INT64_MAX)
        raw_nan = self.budget_bytes.replace(b'"max_wall_time_ms":0', b'"max_wall_time_ms":NaN')
        self.assert_rejected(
            parse_resource_budget, raw_nan, self.budget_target, "tool.none"
        )

    def test_tool_none_is_an_explicit_mechanical_ceiling(self) -> None:
        value = copy.deepcopy(self.budget)
        value["max_tool_calls"] = 1
        self.assert_rejected(
            parse_resource_budget,
            canonical_bytes(value),
            self.budget_target,
            "tool.none",
        )
        self.parse_budget(value, tool_profile="tool.other")
        self.assert_rejected(
            parse_resource_budget, self.budget_bytes, self.budget_target, ""
        )

    def test_budget_target_bytes_digest_schema_and_canonical_form_are_exact(self) -> None:
        self.parse_budget()
        self.assert_rejected(
            parse_resource_budget,
            self.budget_bytes,
            self.budget_target + b" ",
            "tool.none",
        )
        wrong = json.loads(self.budget_target)
        wrong["schema"] = "aci.sandbox-enforcement-policy@1"
        wrong_raw = canonical_bytes(wrong)
        ref = copy.deepcopy(self.budget)
        ref["budget_policy_ref"]["digest"] = digest_bytes(wrong_raw)
        self.assert_rejected(
            parse_resource_budget, canonical_bytes(ref), wrong_raw, "tool.none"
        )
        noncanonical = b'{"schema":"aci.budget-policy@1","scope":"attempt","exhaustion_action":"deny-new-work","unknown_usage_action":"deny-new-work"}'
        value = copy.deepcopy(self.budget)
        value["budget_policy_ref"]["digest"] = digest_bytes(noncanonical)
        self.assert_rejected(
            parse_resource_budget, canonical_bytes(value), noncanonical, "tool.none"
        )

    def test_budget_reference_and_owner_target_complete_field_matrix(self) -> None:
        for field in ("name", "version", "digest"):
            missing = copy.deepcopy(self.budget)
            del missing["budget_policy_ref"][field]
            self.assert_rejected(
                parse_resource_budget,
                canonical_bytes(missing),
                self.budget_target,
                "tool.none",
            )
            wrong = copy.deepcopy(self.budget)
            wrong["budget_policy_ref"][field] = None
            self.assert_rejected(
                parse_resource_budget,
                canonical_bytes(wrong),
                self.budget_target,
                "tool.none",
            )
        target = json.loads(self.budget_target)
        for field in target:
            missing_target = dict(target)
            del missing_target[field]
            raw = canonical_bytes(missing_target)
            budget = copy.deepcopy(self.budget)
            budget["budget_policy_ref"]["digest"] = digest_bytes(raw)
            self.assert_rejected(
                parse_resource_budget, canonical_bytes(budget), raw, "tool.none"
            )
            wrong_target = dict(target)
            wrong_target[field] = None
            raw = canonical_bytes(wrong_target)
            budget = copy.deepcopy(self.budget)
            budget["budget_policy_ref"]["digest"] = digest_bytes(raw)
            self.assert_rejected(
                parse_resource_budget, canonical_bytes(budget), raw, "tool.none"
            )
        duplicate_target = self.budget_target[:-1] + b',"scope":"attempt"}'
        budget = copy.deepcopy(self.budget)
        budget["budget_policy_ref"]["digest"] = digest_bytes(duplicate_target)
        self.assert_rejected(
            parse_resource_budget,
            canonical_bytes(budget),
            duplicate_target,
            "tool.none",
        )

    def test_valid_sandbox_reproduces_golden_default_deny(self) -> None:
        parsed = self.parse_sandbox()
        self.assertEqual(parsed.canonical_bytes, self.sandbox_bytes)
        self.assertEqual(parsed.content_digest, self.vectors["sandbox_policy"][1])
        self.assertEqual(parsed.value["filesystem_scope"]["link_policy"], "deny")

    def test_sandbox_is_recursively_closed_and_duplicate_safe(self) -> None:
        mutations = []
        top = copy.deepcopy(self.sandbox)
        del top["credential_refs"]
        mutations.append(top)
        top_extra = copy.deepcopy(self.sandbox)
        top_extra["secrets"] = []
        mutations.append(top_extra)
        for scope_name in ("filesystem_scope", "network_scope", "process_scope"):
            missing = copy.deepcopy(self.sandbox)
            del missing[scope_name][next(iter(missing[scope_name]))]
            mutations.append(missing)
            extra = copy.deepcopy(self.sandbox)
            extra[scope_name]["grant"] = "allow"
            mutations.append(extra)
        for value in mutations:
            self.assert_rejected(
                parse_sandbox_policy, canonical_bytes(value), self.sandbox_target, {}
            )
        duplicate = self.sandbox_bytes[:-1] + b',"schema":"aci.sandbox-policy@1"}'
        self.assert_rejected(parse_sandbox_policy, duplicate, self.sandbox_target, {})

    def test_sandbox_complete_recursive_missing_and_wrong_type_matrix(self) -> None:
        for field in self.sandbox:
            missing = copy.deepcopy(self.sandbox)
            del missing[field]
            self.assert_rejected(
                parse_sandbox_policy, canonical_bytes(missing), self.sandbox_target, {}
            )
            wrong = copy.deepcopy(self.sandbox)
            wrong[field] = None
            self.assert_rejected(
                parse_sandbox_policy, canonical_bytes(wrong), self.sandbox_target, {}
            )
        for scope_name in ("filesystem_scope", "network_scope", "process_scope"):
            for field in self.sandbox[scope_name]:
                missing = copy.deepcopy(self.sandbox)
                del missing[scope_name][field]
                self.assert_rejected(
                    parse_sandbox_policy,
                    canonical_bytes(missing),
                    self.sandbox_target,
                    {},
                )
                wrong = copy.deepcopy(self.sandbox)
                wrong[scope_name][field] = None
                self.assert_rejected(
                    parse_sandbox_policy,
                    canonical_bytes(wrong),
                    self.sandbox_target,
                    {},
                )
        nested_duplicate = self.sandbox_bytes.replace(
            b'"filesystem_scope":{"default":"deny"',
            b'"filesystem_scope":{"default":"deny","default":"deny"',
        )
        self.assert_rejected(
            parse_sandbox_policy, nested_duplicate, self.sandbox_target, {}
        )

    def test_sandbox_default_and_link_policy_must_deny(self) -> None:
        for path in (
            ("filesystem_scope", "default"),
            ("filesystem_scope", "link_policy"),
            ("network_scope", "default"),
            ("process_scope", "default"),
        ):
            value = copy.deepcopy(self.sandbox)
            value[path[0]][path[1]] = "allow"
            with self.subTest(path=path):
                self.assert_rejected(
                    parse_sandbox_policy, canonical_bytes(value), self.sandbox_target, {}
                )

    def test_sandbox_lexical_roots_accept_only_canonical_relative_slash_paths(self) -> None:
        value = copy.deepcopy(self.sandbox)
        value["filesystem_scope"]["read_roots"] = ["docs", "src/module"]
        value["filesystem_scope"]["write_roots"] = ["out/result.json"]
        self.parse_sandbox(value)
        invalid = ("", "/abs", "a//b", ".", "a/./b", "..", "a/../b", "C:/x", "\\\\host\\x", "a\\b", "*.py", "a?[x]")
        for root in invalid:
            candidate = copy.deepcopy(self.sandbox)
            candidate["filesystem_scope"]["read_roots"] = [root]
            with self.subTest(root=root):
                self.assert_rejected(
                    parse_sandbox_policy,
                    canonical_bytes(candidate),
                    self.sandbox_target,
                    {},
                )

    def test_sandbox_endpoint_and_executable_definitions_remain_closed_empty(self) -> None:
        for scope, field, item in (
            ("network_scope", "allowed_endpoints", "https://example.invalid"),
            ("process_scope", "allowed_executables", "python"),
        ):
            value = copy.deepcopy(self.sandbox)
            value[scope][field] = [item]
            self.assert_rejected(
                parse_sandbox_policy, canonical_bytes(value), self.sandbox_target, {}
            )

    def test_max_child_processes_has_exact_unsigned_int64_interval(self) -> None:
        for candidate in (0, INT64_MAX):
            value = copy.deepcopy(self.sandbox)
            value["process_scope"]["max_child_processes"] = candidate
            self.parse_sandbox(value)
        for candidate in (True, "0", 0.0, -1, INT64_MAX + 1, None):
            value = copy.deepcopy(self.sandbox)
            value["process_scope"]["max_child_processes"] = candidate
            self.assert_rejected(
                parse_sandbox_policy, raw_json(value), self.sandbox_target, {}
            )

    def test_nonempty_opaque_credential_reference_uses_exact_owner_bytes_only(self) -> None:
        opaque = b"owner-defined opaque credential target bytes"
        reference = {
            "name": "credential.example",
            "version": "7",
            "digest": digest_bytes(opaque),
        }
        value = copy.deepcopy(self.sandbox)
        value["credential_refs"] = [reference]
        key = versioned_reference_key(reference)
        parsed = self.parse_sandbox(value, credentials={key: opaque})
        self.assertEqual(tuple(parsed.value["credential_refs"]), (reference,))
        self.assert_rejected(
            parse_sandbox_policy, canonical_bytes(value), self.sandbox_target, {}
        )
        self.assert_rejected(
            parse_sandbox_policy,
            canonical_bytes(value),
            self.sandbox_target,
            {key: opaque + b"!"},
        )
        self.assert_rejected(
            parse_sandbox_policy,
            canonical_bytes(value),
            self.sandbox_target,
            {key: opaque, "extra": b"x"},
        )

    def test_duplicate_credential_refs_and_embedded_secret_fields_reject(self) -> None:
        opaque = b"opaque"
        reference = {"name": "cred", "version": "1", "digest": digest_bytes(opaque)}
        key = versioned_reference_key(reference)
        value = copy.deepcopy(self.sandbox)
        value["credential_refs"] = [reference, copy.deepcopy(reference)]
        self.assert_rejected(
            parse_sandbox_policy,
            canonical_bytes(value),
            self.sandbox_target,
            {key: opaque},
        )
        secret = copy.deepcopy(self.sandbox)
        secret["credential_refs"] = [{**reference, "secret": "bytes"}]
        self.assert_rejected(
            parse_sandbox_policy,
            canonical_bytes(secret),
            self.sandbox_target,
            {key: opaque},
        )

    def test_sandbox_enforcement_target_digest_schema_and_shape_are_exact(self) -> None:
        self.parse_sandbox()
        self.assert_rejected(
            parse_sandbox_policy, self.sandbox_bytes, self.sandbox_target + b" ", {}
        )
        wrong = json.loads(self.sandbox_target)
        wrong["schema"] = "aci.budget-policy@1"
        wrong_raw = canonical_bytes(wrong)
        value = copy.deepcopy(self.sandbox)
        value["policy_ref"]["digest"] = digest_bytes(wrong_raw)
        self.assert_rejected(
            parse_sandbox_policy, canonical_bytes(value), wrong_raw, {}
        )

    def test_sandbox_reference_and_owner_target_complete_field_matrix(self) -> None:
        for field in ("name", "version", "digest"):
            missing = copy.deepcopy(self.sandbox)
            del missing["policy_ref"][field]
            self.assert_rejected(
                parse_sandbox_policy, canonical_bytes(missing), self.sandbox_target, {}
            )
            wrong = copy.deepcopy(self.sandbox)
            wrong["policy_ref"][field] = None
            self.assert_rejected(
                parse_sandbox_policy, canonical_bytes(wrong), self.sandbox_target, {}
            )
        target = json.loads(self.sandbox_target)
        for field in target:
            missing_target = dict(target)
            del missing_target[field]
            raw = canonical_bytes(missing_target)
            sandbox = copy.deepcopy(self.sandbox)
            sandbox["policy_ref"]["digest"] = digest_bytes(raw)
            self.assert_rejected(
                parse_sandbox_policy, canonical_bytes(sandbox), raw, {}
            )
            wrong_target = dict(target)
            wrong_target[field] = None
            raw = canonical_bytes(wrong_target)
            sandbox = copy.deepcopy(self.sandbox)
            sandbox["policy_ref"]["digest"] = digest_bytes(raw)
            self.assert_rejected(
                parse_sandbox_policy, canonical_bytes(sandbox), raw, {}
            )

    def test_t_pol0_1_complete_recursive_document_fault_matrix(self) -> None:
        opaque = b"owner-contract-target"
        credential_ref = {
            "name": "credential.owner.example",
            "version": "1",
            "digest": digest_bytes(opaque),
        }
        sandbox_with_credential = copy.deepcopy(self.sandbox)
        sandbox_with_credential["credential_refs"] = [credential_ref]
        credential_map = {versioned_reference_key(credential_ref): opaque}

        documents = (
            (
                "resource-budget",
                self.budget,
                ((), ("budget_policy_ref",)),
                lambda raw: parse_resource_budget(raw, self.budget_target, "tool.none"),
            ),
            (
                "sandbox-policy",
                sandbox_with_credential,
                (
                    (),
                    ("policy_ref",),
                    ("filesystem_scope",),
                    ("network_scope",),
                    ("process_scope",),
                    ("credential_refs", 0),
                ),
                lambda raw: parse_sandbox_policy(
                    raw, self.sandbox_target, credential_map
                ),
            ),
            (
                "production-fence",
                self._production_fence(),
                ((),),
                parse_execution_authority_fence,
            ),
            (
                "harness-fence",
                self.harness,
                ((),),
                parse_execution_authority_fence_harness_for_test,
            ),
            (
                "combined-oracle",
                json.loads(self.oracle_bytes),
                (
                    (),
                    ("resource_budget",),
                    ("resource_budget", "budget_policy_ref"),
                    ("sandbox_policy",),
                    ("sandbox_policy", "policy_ref"),
                    ("sandbox_policy", "filesystem_scope"),
                    ("sandbox_policy", "network_scope"),
                    ("sandbox_policy", "process_scope"),
                ),
                lambda raw: parse_execution_policy_oracle_fixture_for_test(
                    raw,
                    self.budget_bytes,
                    self.sandbox_bytes,
                    self.budget_target,
                    self.sandbox_target,
                    {},
                    "tool.none",
                ),
            ),
        )
        for document, base, object_paths, parser in documents:
            for object_path in object_paths:
                original_object = nested_member(base, object_path)
                self.assertIsInstance(original_object, dict)
                extra = copy.deepcopy(base)
                nested_member(extra, object_path)["unexpected_field"] = None
                with self.subTest(document=document, path=object_path, fault="extra"):
                    self.assert_rejected(parser, canonical_bytes(extra))
                for field in tuple(original_object):
                    missing = copy.deepcopy(base)
                    del nested_member(missing, object_path)[field]
                    misspelled = copy.deepcopy(base)
                    target = nested_member(misspelled, object_path)
                    target[field + "_misspelled"] = target.pop(field)
                    wrong = copy.deepcopy(base)
                    nested_member(wrong, object_path)[field] = None
                    duplicate = json_with_duplicate(base, object_path, field)
                    for fault, raw in (
                        ("missing", canonical_bytes(missing)),
                        ("misspelled", canonical_bytes(misspelled)),
                        ("wrong-primitive", canonical_bytes(wrong)),
                        ("duplicate", duplicate),
                    ):
                        with self.subTest(
                            document=document,
                            path=object_path,
                            field=field,
                            fault=fault,
                        ):
                            self.assert_rejected(parser, raw)

    def test_t_pol0_1_complete_reference_owner_target_fault_matrix(self) -> None:
        targets = (
            (
                "budget-owner-target",
                json.loads(self.budget_target),
                lambda raw: self._budget_with_target(raw),
            ),
            (
                "sandbox-owner-target",
                json.loads(self.sandbox_target),
                lambda raw: self._sandbox_with_target(raw),
            ),
        )
        for label, base, parser in targets:
            extra = dict(base)
            extra["unexpected_field"] = None
            self.assert_rejected(parser, canonical_bytes(extra))
            for field in base:
                missing = dict(base)
                del missing[field]
                misspelled = dict(base)
                misspelled[field + "_misspelled"] = misspelled.pop(field)
                wrong = dict(base)
                wrong[field] = None
                duplicate = json_with_duplicate(base, (), field)
                for fault, raw in (
                    ("missing", canonical_bytes(missing)),
                    ("misspelled", canonical_bytes(misspelled)),
                    ("wrong-primitive", canonical_bytes(wrong)),
                    ("duplicate", duplicate),
                ):
                    with self.subTest(target=label, field=field, fault=fault):
                        self.assert_rejected(parser, raw)

    def _budget_with_target(self, target: bytes):
        budget = copy.deepcopy(self.budget)
        budget["budget_policy_ref"]["digest"] = digest_bytes(target)
        return parse_resource_budget(canonical_bytes(budget), target, "tool.none")

    def _sandbox_with_target(self, target: bytes):
        sandbox = copy.deepcopy(self.sandbox)
        sandbox["policy_ref"]["digest"] = digest_bytes(target)
        return parse_sandbox_policy(canonical_bytes(sandbox), target, {})

    def _production_fence(self, epoch=1):
        preimage = {
            "schema": "aci.execution-authority-fence-preimage@1",
            "dispatch_id": "dispatch_test",
            "run_id": "run_test",
            "authority_mode": "runtime-managed",
            "cutover_epoch": epoch,
            "legacy_watcher_disabled_evidence_ref": "art_test",
        }
        value = dict(preimage)
        value["schema"] = "aci.execution-authority-fence@1"
        value["fence_digest"] = digest_bytes(canonical_bytes(preimage))
        return value

    def test_harness_fence_reproduces_disjoint_preimage_and_document_goldens(self) -> None:
        parsed = parse_execution_authority_fence_harness_for_test(self.harness_bytes)
        self.assertIs(type(parsed), ParsedHarnessAuthorityFenceForTest)
        self.assertNotIsInstance(parsed, ParsedProductionAuthorityFence)
        with self.assertRaises(TypeError):
            parsed.value["run_id"] = "mutated"
        with self.assertRaises(TypeError):
            parsed.preimage["run_id"] = "mutated"
        self.assertEqual(parsed.preimage_bytes, self.vectors["harness_fence_preimage"][0])
        self.assertEqual(parsed.preimage_digest, self.vectors["harness_fence_preimage"][1])
        self.assertEqual(parsed.canonical_bytes, self.harness_bytes)
        self.assertEqual(parsed.content_digest, self.vectors["harness_fence_document"][1])

    def test_production_fence_has_distinct_schema_preimage_and_structural_result(self) -> None:
        value = self._production_fence()
        parsed = parse_execution_authority_fence(canonical_bytes(value))
        self.assertIs(type(parsed), ParsedProductionAuthorityFence)
        self.assertNotIsInstance(parsed, ParsedHarnessAuthorityFenceForTest)
        with self.assertRaises(TypeError):
            parsed.value["run_id"] = "mutated"
        with self.assertRaises(TypeError):
            parsed.preimage["run_id"] = "mutated"
        self.assertEqual(parsed.preimage["schema"], "aci.execution-authority-fence-preimage@1")
        self.assertEqual(parsed.preimage_digest, value["fence_digest"])

    def test_production_and_harness_schema_domains_cannot_substitute(self) -> None:
        self.assert_rejected(parse_execution_authority_fence, self.harness_bytes)
        production = canonical_bytes(self._production_fence())
        self.assert_rejected(
            parse_execution_authority_fence_harness_for_test, production
        )
        value = copy.deepcopy(self.harness)
        production_preimage = dict(value)
        del production_preimage["fence_digest"]
        production_preimage["schema"] = "aci.execution-authority-fence-preimage@1"
        value["fence_digest"] = digest_bytes(canonical_bytes(production_preimage))
        self.assert_rejected(
            parse_execution_authority_fence_harness_for_test, canonical_bytes(value)
        )

    def test_fence_is_closed_duplicate_safe_and_digest_bound(self) -> None:
        value = self._production_fence()
        for mutation in ("missing", "extra", "digest"):
            candidate = copy.deepcopy(value)
            if mutation == "missing":
                del candidate["run_id"]
            elif mutation == "extra":
                candidate["host"] = "invented"
            else:
                candidate["run_id"] = "drift"
            self.assert_rejected(
                parse_execution_authority_fence, canonical_bytes(candidate)
            )
        raw = canonical_bytes(value)
        duplicate = raw[:-1] + b',"run_id":"run_test"}'
        self.assert_rejected(parse_execution_authority_fence, duplicate)

    def test_both_fence_domains_complete_missing_and_wrong_type_matrix(self) -> None:
        cases = (
            (self._production_fence(), parse_execution_authority_fence),
            (self.harness, parse_execution_authority_fence_harness_for_test),
        )
        for base, parser in cases:
            for field in base:
                missing = copy.deepcopy(base)
                del missing[field]
                with self.subTest(parser=parser.__name__, field=field, fault="missing"):
                    self.assert_rejected(parser, canonical_bytes(missing))
                wrong = copy.deepcopy(base)
                wrong[field] = None
                with self.subTest(parser=parser.__name__, field=field, fault="wrong"):
                    self.assert_rejected(parser, canonical_bytes(wrong))

    def test_fence_epoch_exact_positive_int64_range_for_both_domains(self) -> None:
        for epoch in (1, INT64_MAX):
            parse_execution_authority_fence(canonical_bytes(self._production_fence(epoch)))
            harness = copy.deepcopy(self.harness)
            harness["cutover_epoch"] = epoch
            preimage = dict(harness)
            del preimage["fence_digest"]
            preimage["schema"] = "aci.execution-authority-fence-harness-preimage@1"
            harness["fence_digest"] = digest_bytes(canonical_bytes(preimage))
            parse_execution_authority_fence_harness_for_test(canonical_bytes(harness))
        for epoch in (0, -1, INT64_MAX + 1, True, "1", 1.0, None):
            value = self._production_fence(1)
            value["cutover_epoch"] = epoch
            self.assert_rejected(parse_execution_authority_fence, raw_json(value))

    def test_valid_combined_oracle_reproduces_golden_member_lineage(self) -> None:
        parsed = parse_execution_policy_oracle_fixture_for_test(
            self.oracle_bytes,
            self.budget_bytes,
            self.sandbox_bytes,
            self.budget_target,
            self.sandbox_target,
            {},
            "tool.none",
        )
        self.assertIs(type(parsed), ParsedExecutionPolicyOracleFixtureForTest)
        self.assertNotIsInstance(parsed, ParsedProductionAuthorityFence)
        self.assertNotIsInstance(parsed, ParsedHarnessAuthorityFenceForTest)
        with self.assertRaises(TypeError):
            parsed.value["schema"] = "mutated"
        with self.assertRaises(TypeError):
            parsed.value["resource_budget"]["max_wall_time_ms"] = 1
        self.assertEqual(parsed.canonical_bytes, self.oracle_bytes)
        self.assertEqual(parsed.content_digest, self.vectors["combined_oracle"][1])

    def test_combined_oracle_is_closed_and_exactly_member_bound(self) -> None:
        oracle = json.loads(self.oracle_bytes)
        for mutation in ("missing", "extra", "member", "member_digest"):
            value = copy.deepcopy(oracle)
            if mutation == "missing":
                del value["resource_budget_digest"]
            elif mutation == "extra":
                value["authority"] = True
            elif mutation == "member":
                value["resource_budget"]["max_wall_time_ms"] = 1
            else:
                value["sandbox_policy_digest"] = self.vectors["resource_budget"][1]
            self.assert_rejected(
                parse_execution_policy_oracle_fixture_for_test,
                canonical_bytes(value),
                self.budget_bytes,
                self.sandbox_bytes,
                self.budget_target,
                self.sandbox_target,
                {},
                "tool.none",
            )

    def test_combined_oracle_complete_missing_wrong_type_and_duplicate_matrix(self) -> None:
        oracle = json.loads(self.oracle_bytes)
        for field in oracle:
            missing = copy.deepcopy(oracle)
            del missing[field]
            self.assert_rejected(
                parse_execution_policy_oracle_fixture_for_test,
                canonical_bytes(missing),
                self.budget_bytes,
                self.sandbox_bytes,
                self.budget_target,
                self.sandbox_target,
                {},
                "tool.none",
            )
            wrong = copy.deepcopy(oracle)
            wrong[field] = None
            self.assert_rejected(
                parse_execution_policy_oracle_fixture_for_test,
                canonical_bytes(wrong),
                self.budget_bytes,
                self.sandbox_bytes,
                self.budget_target,
                self.sandbox_target,
                {},
                "tool.none",
            )
        duplicate = self.oracle_bytes.replace(
            b'"resource_budget":{', b'"resource_budget":{"schema":"duplicate",'
        )
        self.assert_rejected(
            parse_execution_policy_oracle_fixture_for_test,
            duplicate,
            self.budget_bytes,
            self.sandbox_bytes,
            self.budget_target,
            self.sandbox_target,
            {},
            "tool.none",
        )

    def test_oracle_and_harness_are_rejected_by_production_policy_firewall(self) -> None:
        self.assert_rejected(parse_production_policy_document, self.oracle_bytes)
        self.assert_rejected(parse_production_policy_document, self.harness_bytes)
        parsed = parse_production_policy_document(
            self.budget_bytes,
            budget_policy_target_bytes=self.budget_target,
            confirmed_tool_profile="tool.none",
        )
        self.assertEqual(parsed.content_digest, self.vectors["resource_budget"][1])

    def test_parsers_expose_no_dispatch_budget_or_scheduler_inference_surface(self) -> None:
        parameters = set(inspect.signature(parse_resource_budget).parameters)
        self.assertEqual(
            parameters,
            {"raw", "budget_policy_target_bytes", "confirmed_tool_profile"},
        )
        forbidden = {
            "max_attempts_per_turn",
            "max_total_turns",
            "wall_clock_seconds",
            "deadline",
            "usage",
            "scheduler",
        }
        self.assertTrue(parameters.isdisjoint(forbidden))

    def test_pure_oracle_has_zero_external_effects(self) -> None:
        def fail(*_args, **_kwargs):
            raise AssertionError("external effect boundary was called")

        source = inspect.getsource(execution_policy_module)
        tree = ast.parse(source)
        imported_roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
        self.assertLessEqual(
            imported_roots,
            {
                "__future__",
                "re",
                "dataclasses",
                "types",
                "typing",
                "canonical",
                "errors",
            },
        )
        called_names = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name):
                called_names.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                called_names.add(node.func.attr)
        forbidden_effect_calls = {
            "connect",
            "execute",
            "commit",
            "persist",
            "finalize",
            "journal",
            "audit",
            "open",
            "read_bytes",
            "write_bytes",
            "now",
            "utcnow",
            "time",
            "monotonic",
            "getenv",
            "putenv",
            "socket",
            "create_connection",
            "urlopen",
            "get_password",
            "resolve_credential",
            "start_provider",
            "invoke_tool",
            "launch",
            "Popen",
            "run",
        }
        self.assertTrue(called_names.isdisjoint(forbidden_effect_calls))

        patches = (
            patch("builtins.open", side_effect=fail),
            patch.object(Path, "open", side_effect=fail),
            patch.object(Path, "read_bytes", side_effect=fail),
            patch.object(Path, "write_bytes", side_effect=fail),
            patch.object(sqlite3, "connect", side_effect=fail),
            patch.object(time, "time", side_effect=fail),
            patch.object(time, "monotonic", side_effect=fail),
            patch("os.getenv", side_effect=fail),
            patch.object(os, "putenv", side_effect=fail),
            patch.object(subprocess, "Popen", side_effect=fail),
            patch.object(subprocess, "run", side_effect=fail),
            patch.object(socket, "socket", side_effect=fail),
            patch.object(socket, "create_connection", side_effect=fail),
            patch.object(urllib.request, "urlopen", side_effect=fail),
        )
        for active in patches:
            active.start()
        try:
            self.parse_budget()
            self.parse_sandbox()
            parse_execution_authority_fence(
                canonical_bytes(self._production_fence())
            )
            parse_execution_authority_fence_harness_for_test(self.harness_bytes)
            parse_execution_policy_oracle_fixture_for_test(
                self.oracle_bytes,
                self.budget_bytes,
                self.sandbox_bytes,
                self.budget_target,
                self.sandbox_target,
                {},
                "tool.none",
            )
        finally:
            for active in reversed(patches):
                active.stop()


if __name__ == "__main__":
    unittest.main()
