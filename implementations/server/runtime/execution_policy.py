"""Pure POLICY-000 execution-policy contract oracle.

This module validates bytes already supplied by its caller.  It owns no storage,
resolver, clock, environment, launcher, provider, or other effectful dependency.
The harness and combined-oracle entry points are deliberately separate from the
production document entry point.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from .canonical import canonical_bytes, digest_bytes, parse_strict_json
from .errors import ValidationError


INT64_MAX = 2**63 - 1
_DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")
_WILDCARDS = frozenset("*?[]")


class ExecutionPolicyContractError(ValidationError):
    """Typed rejection for the non-authoritative POLICY-000 boundary."""


@dataclass(frozen=True)
class ParsedPolicyDocument:
    """A complete validated value plus its canonical identity."""

    value: Mapping[str, Any]
    canonical_bytes: bytes
    content_digest: str


@dataclass(frozen=True)
class ParsedProductionAuthorityFence(ParsedPolicyDocument):
    """A production-domain structure; it is not verified cutover authority."""

    preimage: Mapping[str, Any]
    preimage_bytes: bytes
    preimage_digest: str


@dataclass(frozen=True)
class ParsedHarnessAuthorityFenceForTest(ParsedPolicyDocument):
    """A test-only fence value that cannot inhabit the production result type."""

    preimage: Mapping[str, Any]
    preimage_bytes: bytes
    preimage_digest: str


@dataclass(frozen=True)
class ParsedExecutionPolicyOracleFixtureForTest(ParsedPolicyDocument):
    """A test-only combined oracle value, never executable policy authority."""


def _reject(message: str) -> None:
    raise ExecutionPolicyContractError(message)


def _decode_object(raw: bytes, label: str) -> dict[str, Any]:
    if not isinstance(raw, bytes):
        _reject(f"{label} must be supplied as exact bytes")
    try:
        value = parse_strict_json(raw)
    except ValidationError as exc:
        raise ExecutionPolicyContractError(f"invalid {label}: {exc}") from exc
    except (ValueError, RecursionError, OverflowError) as exc:
        raise ExecutionPolicyContractError(
            f"invalid {label}: bounded JSON decoding failed"
        ) from exc
    if not isinstance(value, dict):
        _reject(f"{label} must be a JSON object")
    try:
        expected = canonical_bytes(value)
    except (ValidationError, ValueError, RecursionError, OverflowError) as exc:
        raise ExecutionPolicyContractError(
            f"invalid {label}: canonical projection failed"
        ) from exc
    if raw != expected:
        _reject(f"{label} bytes must be exact canonical aci-cjson-1")
    return value


def _closed(value: Mapping[str, Any], fields: set[str], label: str) -> None:
    actual = set(value)
    missing = fields - actual
    extra = actual - fields
    if missing or extra:
        _reject(
            f"{label} fields are not closed; missing={sorted(missing)!r}, "
            f"extra={sorted(extra)!r}"
        )


def _literal(value: Any, expected: str, label: str) -> None:
    if not isinstance(value, str) or value != expected:
        _reject(f"{label} must equal {expected!r}")


def _nonempty_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value:
        _reject(f"{label} must be a non-empty string")


def _digest(value: Any, label: str) -> None:
    if not isinstance(value, str) or _DIGEST_RE.fullmatch(value) is None:
        _reject(f"{label} must be a qualified lowercase SHA-256 digest")


def _int64(value: Any, minimum: int, label: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        _reject(f"{label} must be an integer")
    if value < minimum or value > INT64_MAX:
        _reject(f"{label} is outside {minimum}..{INT64_MAX}")


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(member) for key, member in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(member) for member in value)
    return value


def _parsed(value: dict[str, Any]) -> ParsedPolicyDocument:
    body = canonical_bytes(value)
    return ParsedPolicyDocument(
        value=_freeze(value),
        canonical_bytes=body,
        content_digest=digest_bytes(body),
    )


def _versioned_reference(value: Any, label: str) -> dict[str, str]:
    if not isinstance(value, dict):
        _reject(f"{label} must be an object")
    _closed(value, {"name", "version", "digest"}, label)
    _nonempty_string(value["name"], f"{label}.name")
    _nonempty_string(value["version"], f"{label}.version")
    _digest(value["digest"], f"{label}.digest")
    return value


def versioned_reference_key(reference: Mapping[str, Any]) -> str:
    """Return the exact map key used for opaque credential target bytes."""

    value = _versioned_reference(reference, "versioned reference")
    return canonical_bytes(value).decode("utf-8")


def _verify_target_digest(reference: Mapping[str, Any], raw: bytes, label: str) -> None:
    if not isinstance(raw, bytes):
        _reject(f"{label} target must be supplied as exact bytes")
    if digest_bytes(raw) != reference["digest"]:
        _reject(f"{label} target digest does not match its reference")


def _parse_budget_policy_target(raw: bytes, reference: Mapping[str, Any]) -> None:
    _verify_target_digest(reference, raw, "budget policy")
    value = _decode_object(raw, "budget-policy target")
    _closed(
        value,
        {"schema", "scope", "exhaustion_action", "unknown_usage_action"},
        "budget-policy target",
    )
    _literal(value["schema"], "aci.budget-policy@1", "budget-policy target.schema")
    _literal(value["scope"], "attempt", "budget-policy target.scope")
    _literal(
        value["exhaustion_action"],
        "deny-new-work",
        "budget-policy target.exhaustion_action",
    )
    _literal(
        value["unknown_usage_action"],
        "deny-new-work",
        "budget-policy target.unknown_usage_action",
    )
    if canonical_bytes(value) != raw:
        _reject("budget-policy target bytes are not canonical aci-cjson-1")


def _parse_sandbox_enforcement_target(raw: bytes, reference: Mapping[str, Any]) -> None:
    _verify_target_digest(reference, raw, "sandbox enforcement policy")
    value = _decode_object(raw, "sandbox-enforcement target")
    _closed(
        value,
        {"schema", "enforcement_mode", "unsupported_control_action"},
        "sandbox-enforcement target",
    )
    _literal(
        value["schema"],
        "aci.sandbox-enforcement-policy@1",
        "sandbox-enforcement target.schema",
    )
    _literal(value["enforcement_mode"], "deny-all", "sandbox-enforcement target.enforcement_mode")
    _literal(
        value["unsupported_control_action"],
        "deny",
        "sandbox-enforcement target.unsupported_control_action",
    )
    if canonical_bytes(value) != raw:
        _reject("sandbox-enforcement target bytes are not canonical aci-cjson-1")


def parse_resource_budget(
    raw: bytes,
    budget_policy_target_bytes: bytes,
    confirmed_tool_profile: str,
) -> ParsedPolicyDocument:
    """Validate one closed Attempt budget and its caller-supplied policy target."""

    value = _decode_object(raw, "resource budget")
    fields = {
        "schema",
        "max_wall_time_ms",
        "max_input_tokens",
        "max_output_tokens",
        "max_tool_calls",
        "max_payload_bytes",
        "max_artifact_bytes",
        "budget_policy_ref",
    }
    _closed(value, fields, "resource budget")
    _literal(value["schema"], "aci.resource-budget@1", "resource budget.schema")
    for name in fields - {"schema", "budget_policy_ref"}:
        _int64(value[name], 0, f"resource budget.{name}")
    _nonempty_string(confirmed_tool_profile, "confirmed tool profile")
    if confirmed_tool_profile == "tool.none" and value["max_tool_calls"] != 0:
        _reject("tool.none requires max_tool_calls=0")
    reference = _versioned_reference(value["budget_policy_ref"], "resource budget.budget_policy_ref")
    _parse_budget_policy_target(budget_policy_target_bytes, reference)
    return _parsed(value)


def _root(root: Any, label: str) -> None:
    if not isinstance(root, str) or not root:
        _reject(f"{label} must be a non-empty canonical relative path")
    if root.startswith(("/", "\\")) or "\\" in root or ":" in root:
        _reject(f"{label} must be repository-relative and use '/' separators")
    if any(character in root for character in _WILDCARDS):
        _reject(f"{label} may not contain wildcard syntax")
    components = root.split("/")
    if any(component in {"", ".", ".."} for component in components):
        _reject(f"{label} contains an empty, dot, or dot-dot component")


def _string_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        _reject(f"{label} must be a list")
    return value


def parse_sandbox_policy(
    raw: bytes,
    sandbox_enforcement_target_bytes: bytes,
    credential_target_bytes: Mapping[str, bytes],
) -> ParsedPolicyDocument:
    """Validate one closed default-deny sandbox policy without inspecting a host."""

    value = _decode_object(raw, "sandbox policy")
    _closed(
        value,
        {
            "schema",
            "policy_ref",
            "filesystem_scope",
            "network_scope",
            "process_scope",
            "credential_refs",
        },
        "sandbox policy",
    )
    _literal(value["schema"], "aci.sandbox-policy@1", "sandbox policy.schema")
    policy_ref = _versioned_reference(value["policy_ref"], "sandbox policy.policy_ref")
    _parse_sandbox_enforcement_target(sandbox_enforcement_target_bytes, policy_ref)

    filesystem = value["filesystem_scope"]
    if not isinstance(filesystem, dict):
        _reject("sandbox policy.filesystem_scope must be an object")
    _closed(filesystem, {"default", "read_roots", "write_roots", "link_policy"}, "filesystem scope")
    _literal(filesystem["default"], "deny", "filesystem scope.default")
    _literal(filesystem["link_policy"], "deny", "filesystem scope.link_policy")
    for list_name in ("read_roots", "write_roots"):
        roots = _string_list(filesystem[list_name], f"filesystem scope.{list_name}")
        for index, root in enumerate(roots):
            _root(root, f"filesystem scope.{list_name}[{index}]")

    network = value["network_scope"]
    if not isinstance(network, dict):
        _reject("sandbox policy.network_scope must be an object")
    _closed(network, {"default", "allowed_endpoints"}, "network scope")
    _literal(network["default"], "deny", "network scope.default")
    endpoints = _string_list(network["allowed_endpoints"], "network scope.allowed_endpoints")
    if endpoints:
        _reject("non-empty endpoint grants have no closed L0 definition")

    process = value["process_scope"]
    if not isinstance(process, dict):
        _reject("sandbox policy.process_scope must be an object")
    _closed(process, {"default", "allowed_executables", "max_child_processes"}, "process scope")
    _literal(process["default"], "deny", "process scope.default")
    executables = _string_list(process["allowed_executables"], "process scope.allowed_executables")
    if executables:
        _reject("non-empty executable grants have no closed L0 definition")
    _int64(process["max_child_processes"], 0, "process scope.max_child_processes")

    if not isinstance(credential_target_bytes, Mapping):
        _reject("credential target bytes must be an exact reference-keyed map")
    refs = _string_list(value["credential_refs"], "sandbox policy.credential_refs")
    keys: list[str] = []
    parsed_refs: list[dict[str, str]] = []
    for index, item in enumerate(refs):
        reference = _versioned_reference(item, f"sandbox policy.credential_refs[{index}]")
        key = versioned_reference_key(reference)
        if key in keys:
            _reject("sandbox policy.credential_refs contains a duplicate reference")
        keys.append(key)
        parsed_refs.append(reference)
    if set(credential_target_bytes) != set(keys):
        _reject("credential target-byte map must contain exactly every credential reference")
    for key, reference in zip(keys, parsed_refs):
        _verify_target_digest(reference, credential_target_bytes[key], "credential")
    return _parsed(value)


def _parse_fence(
    raw: bytes, harness: bool
) -> ParsedProductionAuthorityFence | ParsedHarnessAuthorityFenceForTest:
    label = "harness fence" if harness else "production fence"
    value = _decode_object(raw, label)
    schema = (
        "aci.execution-authority-fence-harness@1"
        if harness
        else "aci.execution-authority-fence@1"
    )
    preimage_schema = (
        "aci.execution-authority-fence-harness-preimage@1"
        if harness
        else "aci.execution-authority-fence-preimage@1"
    )
    fields = {
        "schema",
        "dispatch_id",
        "run_id",
        "authority_mode",
        "cutover_epoch",
        "legacy_watcher_disabled_evidence_ref",
        "fence_digest",
    }
    _closed(value, fields, label)
    # Schema is checked before any other field.  The pure parser has no evidence resolver.
    _literal(value["schema"], schema, f"{label}.schema")
    _nonempty_string(value["dispatch_id"], f"{label}.dispatch_id")
    _nonempty_string(value["run_id"], f"{label}.run_id")
    _literal(value["authority_mode"], "runtime-managed", f"{label}.authority_mode")
    _int64(value["cutover_epoch"], 1, f"{label}.cutover_epoch")
    _nonempty_string(
        value["legacy_watcher_disabled_evidence_ref"],
        f"{label}.legacy_watcher_disabled_evidence_ref",
    )
    _digest(value["fence_digest"], f"{label}.fence_digest")
    preimage = {key: member for key, member in value.items() if key != "fence_digest"}
    preimage["schema"] = preimage_schema
    preimage_body = canonical_bytes(preimage)
    preimage_digest = digest_bytes(preimage_body)
    if preimage_digest != value["fence_digest"]:
        _reject(f"{label}.fence_digest does not identify its exact preimage")
    body = canonical_bytes(value)
    result_type = (
        ParsedHarnessAuthorityFenceForTest
        if harness
        else ParsedProductionAuthorityFence
    )
    return result_type(
        value=_freeze(value),
        canonical_bytes=body,
        content_digest=digest_bytes(body),
        preimage=_freeze(preimage),
        preimage_bytes=preimage_body,
        preimage_digest=preimage_digest,
    )


def parse_execution_authority_fence(raw: bytes) -> ParsedProductionAuthorityFence:
    """Parse a production fence structurally; never resolve or assert host evidence."""

    result = _parse_fence(raw, harness=False)
    if not isinstance(result, ParsedProductionAuthorityFence):  # defensive type firewall
        _reject("production fence parser crossed its authority domain")
    return result


def parse_execution_authority_fence_harness_for_test(
    raw: bytes,
) -> ParsedHarnessAuthorityFenceForTest:
    """Parse the disjoint test-harness fence domain."""

    result = _parse_fence(raw, harness=True)
    if not isinstance(result, ParsedHarnessAuthorityFenceForTest):
        _reject("harness fence parser crossed its test-only domain")
    return result


def parse_execution_policy_oracle_fixture_for_test(
    raw: bytes,
    resource_budget_bytes: bytes,
    sandbox_policy_bytes: bytes,
    budget_policy_target_bytes: bytes,
    sandbox_enforcement_target_bytes: bytes,
    credential_target_bytes: Mapping[str, bytes],
    confirmed_tool_profile: str,
) -> ParsedExecutionPolicyOracleFixtureForTest:
    """Validate the non-executable combined oracle and exact member lineage."""

    value = _decode_object(raw, "execution-policy oracle fixture")
    _closed(
        value,
        {
            "schema",
            "resource_budget",
            "resource_budget_digest",
            "sandbox_policy",
            "sandbox_policy_digest",
        },
        "execution-policy oracle fixture",
    )
    _literal(
        value["schema"],
        "aci.execution-policy-oracle-fixture@1",
        "execution-policy oracle fixture.schema",
    )
    _digest(value["resource_budget_digest"], "execution-policy oracle resource_budget_digest")
    _digest(value["sandbox_policy_digest"], "execution-policy oracle sandbox_policy_digest")
    budget = parse_resource_budget(
        resource_budget_bytes, budget_policy_target_bytes, confirmed_tool_profile
    )
    sandbox = parse_sandbox_policy(
        sandbox_policy_bytes,
        sandbox_enforcement_target_bytes,
        credential_target_bytes,
    )
    if canonical_bytes(value["resource_budget"]) != budget.canonical_bytes:
        _reject("oracle resource_budget does not equal the supplied exact member")
    if canonical_bytes(value["sandbox_policy"]) != sandbox.canonical_bytes:
        _reject("oracle sandbox_policy does not equal the supplied exact member")
    if value["resource_budget_digest"] != budget.content_digest:
        _reject("oracle resource_budget_digest does not identify the supplied member")
    if value["sandbox_policy_digest"] != sandbox.content_digest:
        _reject("oracle sandbox_policy_digest does not identify the supplied member")
    body = canonical_bytes(value)
    return ParsedExecutionPolicyOracleFixtureForTest(
        value=_freeze(value),
        canonical_bytes=body,
        content_digest=digest_bytes(body),
    )


def parse_production_policy_document(
    raw: bytes,
    *,
    budget_policy_target_bytes: bytes | None = None,
    confirmed_tool_profile: str | None = None,
    sandbox_enforcement_target_bytes: bytes | None = None,
    credential_target_bytes: Mapping[str, bytes] | None = None,
) -> ParsedPolicyDocument:
    """Production-shaped policy firewall; test-only schemas always reject."""

    value = _decode_object(raw, "production policy document")
    schema = value.get("schema")
    if schema == "aci.resource-budget@1":
        if budget_policy_target_bytes is None or confirmed_tool_profile is None:
            _reject("resource-budget reference bytes and tool profile are required")
        return parse_resource_budget(raw, budget_policy_target_bytes, confirmed_tool_profile)
    if schema == "aci.sandbox-policy@1":
        if sandbox_enforcement_target_bytes is None or credential_target_bytes is None:
            _reject("sandbox reference target bytes are required")
        return parse_sandbox_policy(
            raw, sandbox_enforcement_target_bytes, credential_target_bytes
        )
    _reject("schema is not an executable production policy document")
