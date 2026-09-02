"""Operational adapter for routed legacy dispatches and bound host seats."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Sequence

from .canonical import canonical_text, digest_bytes
from .dispatch_types import (
    load_dispatch_type_registry,
    live_dispatch_type_values,
    resolve_dispatch_capability,
)
from .errors import GateBlockedError, ValidationError


BINDING_MARKER = "ACI-WORKFLOW-BINDING-V1:"
MANIFEST_SCHEMA = "aci-workflow-input-manifest/v1"
ENVELOPE_SCHEMA = "aci-host-workflow-binding/v1"
LAUNCH_PLAN_SCHEMA = "aci-bound-launch-plan/v1"
APPENDER = Path(".claude/skills/register-dispatch/append-dispatch.cjs")
ROOT_V080_APPENDER = Path(
    "implementation/domainspec/internal_tools/subagents-dispatch-hooks/"
    "skills/register-dispatch/append-dispatch.cjs"
)
ROOT_LEDGER = Path("telemetry/agents/subagents-dispatch.yaml")
CHILD_RECORD_AUTHORITY = "child-ledger-v063"
ROOT_V080_RECORD_AUTHORITY = "domainspec-root-v080"
RECORD_AUTHORITIES = (CHILD_RECORD_AUTHORITY, ROOT_V080_RECORD_AUTHORITY)


def _json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"{label} is unavailable or malformed") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must contain one JSON object")
    return value


def _write_canonical(path: Path, value: dict[str, Any]) -> str:
    body = canonical_text(value).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    return digest_bytes(body)


def _relative_output(repo_root: Path, output_dir: Path) -> Path:
    root = Path(repo_root).resolve()
    target = Path(output_dir)
    if not target.is_absolute():
        target = root / target
    target = target.resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValidationError("workflow output directory must stay inside the repository") from exc
    return target


def _run_appender_validation(
    *,
    validator_root: Path,
    appender: Path,
    arguments: list[str],
    label: str,
) -> None:
    """Run a non-mutating registrar validation command and preserve its failure."""
    if not appender.is_file():
        raise GateBlockedError(f"{label} registrar is unavailable")
    environment = dict(os.environ)
    environment["CLAUDE_PROJECT_DIR"] = str(validator_root)
    try:
        result = subprocess.run(
            ["node", str(appender), *arguments],
            cwd=validator_root,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise GateBlockedError(f"{label} registrar could not run") from exc
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValidationError(f"{label} dispatch opening record is invalid: {detail}")


def _validate_child_opening_record(root: Path, record: dict[str, Any]) -> None:
    """Validate the child-owned legacy record without appending to its ledger."""
    appender = root / APPENDER
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".json", delete=False
        ) as handle:
            handle.write(canonical_text(record))
            temporary = Path(handle.name)
        _run_appender_validation(
            validator_root=root,
            appender=appender,
            arguments=[str(temporary), "--validate-only"],
            label="child-ledger-v063",
        )
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _repo_relative_file(root: Path, relative: object, label: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValidationError(f"{label} must be a non-empty repository-relative file")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValidationError(f"{label} escapes the governance root") from exc
    if not candidate.is_file():
        raise ValidationError(f"{label} is unavailable")
    return candidate


def _parse_root_ledger(path: Path) -> tuple[dict[str, dict[str, Any]], set[str]]:
    """Parse the appender's JSON-scalar YAML dialect without accepting freeform YAML."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise GateBlockedError("root v0.8 dispatch ledger is unavailable") from exc
    dispatches: dict[str, dict[str, Any]] = {}
    closes: set[str] = set()
    current: dict[str, Any] | None = None
    saw_root = False
    line_pattern = re.compile(r"^(  - |    )([A-Za-z_][A-Za-z0-9_]*): (.*)$")
    for line_number, line in enumerate(lines, start=1):
        if not line or line.startswith("#"):
            continue
        if line == "dispatches:":
            if saw_root:
                raise ValidationError("root v0.8 dispatch ledger repeats dispatches")
            saw_root = True
            continue
        match = line_pattern.fullmatch(line)
        if match is None or not saw_root:
            raise ValidationError(
                f"root v0.8 dispatch ledger has an unsupported line at {line_number}"
            )
        try:
            value = json.loads(match.group(3))
        except json.JSONDecodeError as exc:
            raise ValidationError(
                f"root v0.8 dispatch ledger has invalid JSON at {line_number}"
            ) from exc
        prefix, key = match.group(1), match.group(2)
        if prefix == "  - ":
            if key == "dispatch_id":
                if not isinstance(value, str) or value in dispatches:
                    raise ValidationError("root v0.8 dispatch ledger has duplicate dispatch identity")
                current = {key: value}
                dispatches[value] = current
            elif key == "close_of":
                if not isinstance(value, str) or value in closes:
                    raise ValidationError("root v0.8 dispatch ledger has duplicate close identity")
                closes.add(value)
                current = {key: value}
            else:
                raise ValidationError("root v0.8 dispatch ledger row has no dispatch identity")
        elif current is None or key in current:
            raise ValidationError(
                f"root v0.8 dispatch ledger has an invalid continuation at {line_number}"
            )
        else:
            current[key] = value
    if not saw_root:
        raise ValidationError("root v0.8 dispatch ledger is missing dispatches")
    return dispatches, closes


def _validate_root_v080_opening_record(
    governance_root: Path, record: dict[str, Any]
) -> None:
    """Verify an already-registered root v0.8 dispatch without touching either ledger."""
    if record.get("schema_version") != "0.8.0":
        raise ValidationError("domainspec-root-v080 requires schema_version 0.8.0")
    binding = record.get("evidence_binding")
    if not isinstance(binding, dict):
        raise ValidationError("domainspec-root-v080 requires evidence_binding")
    sheet = _repo_relative_file(
        governance_root, binding.get("sheet_path"), "root v0.8 evidence sheet"
    )
    expected_digest = binding.get("sheet_sha256")
    actual_digest = hashlib.sha256(sheet.read_bytes()).hexdigest()
    if not isinstance(expected_digest, str) or actual_digest != expected_digest:
        raise ValidationError("root v0.8 evidence sheet digest does not match")
    sheet_value = _json_object(sheet, "root v0.8 evidence sheet")
    expected_sheet = {key: value for key, value in record.items() if key != "evidence_binding"}
    if sheet_value != expected_sheet:
        raise ValidationError(
            "root v0.8 evidence sheet must equal the registered record without evidence_binding"
        )
    _run_appender_validation(
        validator_root=governance_root,
        appender=governance_root / ROOT_V080_APPENDER,
        arguments=["--validate-sheet", str(sheet)],
        label="root-v0.8",
    )
    dispatches, closes = _parse_root_ledger(governance_root / ROOT_LEDGER)
    dispatch_id = record.get("dispatch_id")
    if not isinstance(dispatch_id, str) or not dispatch_id:
        raise ValidationError("dispatch_id is required")
    ledger_row = dispatches.get(dispatch_id)
    if ledger_row is None:
        raise ValidationError("root v0.8 dispatch is not registered")
    if dispatch_id in closes:
        raise GateBlockedError("root v0.8 dispatch is closed and cannot compile bound seats")
    expected_row = {key: value for key, value in record.items() if key != "project_dir"}
    observed_row = dict(ledger_row)
    observed_row.pop("created", None)
    if "invoked_by" not in expected_row:
        observed_row.pop("invoked_by", None)
    if observed_row != expected_row:
        raise ValidationError("root v0.8 registered row differs from the submitted record")


def validate_opening_record(
    repo_root: Path,
    record: dict[str, Any],
    *,
    record_authority: str = CHILD_RECORD_AUTHORITY,
    governance_root: Path | None = None,
) -> None:
    """Validate the selected record authority before generating any bound seat bytes."""
    root = Path(repo_root).resolve()
    if record_authority == CHILD_RECORD_AUTHORITY:
        registry = load_dispatch_type_registry(root)
        if record.get("schema_version") != registry["ledger_schema_version"]:
            raise ValidationError("dispatch row schema_version differs from the registry")
        _validate_child_opening_record(root, record)
        return
    if record_authority == ROOT_V080_RECORD_AUTHORITY:
        if governance_root is None:
            raise GateBlockedError(
                "domainspec-root-v080 requires an explicit governance root"
            )
        _validate_root_v080_opening_record(Path(governance_root).resolve(), record)
        return
    raise ValidationError(f"unknown record authority {record_authority!r}")


def _sequential_handoffs(
    *,
    root: Path,
    target_dir: Path,
    record: dict[str, Any],
    capability_ref: str,
    route_digest: str,
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    """Validate declared topology and materialize immutable producer outputs by target."""
    groups = record["groups"]
    group_index = {group["group_id"]: index for index, group in enumerate(groups)}
    connections = record.get("connections", [])
    if not isinstance(connections, list):
        raise ValidationError("connections must be an ordered array")
    handoffs: list[dict[str, Any]] = []
    slots_by_target: dict[str, list[dict[str, Any]]] = {
        group_id: [] for group_id in group_index
    }
    seen_pairs: set[tuple[str, str]] = set()
    for connection in connections:
        if not isinstance(connection, dict):
            raise ValidationError("each connection must be an object")
        if set(connection) != {"from", "to", "type"}:
            raise ValidationError("only closed sequential connection records are executable")
        source_group = connection.get("from")
        target_group = connection.get("to")
        if (
            not isinstance(source_group, str)
            or not isinstance(target_group, str)
            or source_group not in group_index
            or target_group not in group_index
        ):
            raise ValidationError("connection endpoints must name declared groups")
        if connection.get("type") != "sequential":
            raise GateBlockedError("only sequential connection semantics are executable")
        if group_index[source_group] >= group_index[target_group]:
            raise GateBlockedError(
                "sequential connections must follow canonical declared group order"
            )
        pair = (source_group, target_group)
        if pair in seen_pairs:
            raise ValidationError("duplicate sequential connection")
        seen_pairs.add(pair)

        receipt_path = target_dir / (
            f"handoff-{group_index[source_group]}-{group_index[target_group]}.json"
        )
        if not receipt_path.is_file():
            raise GateBlockedError("required sequential handoff receipt is unavailable")
        receipt = _json_object(receipt_path, "sequential handoff receipt")
        if set(receipt) != {
            "schema",
            "dispatch_id",
            "capability_ref",
            "route_digest",
            "connection",
            "sources",
        }:
            raise ValidationError("sequential handoff receipt shape is invalid")
        if (
            receipt["schema"] != "aci-workflow-sequential-handoff/v1"
            or receipt["dispatch_id"] != record["dispatch_id"]
            or receipt["capability_ref"] != capability_ref
            or receipt["route_digest"] != route_digest
            or receipt["connection"] != connection
        ):
            raise ValidationError("sequential handoff identity or capability route differs")
        raw_sources = receipt["sources"]
        producer_agents = groups[group_index[source_group]]["agents"]
        if not isinstance(raw_sources, list) or len(raw_sources) != len(producer_agents):
            raise ValidationError("sequential handoff must cover every producer seat exactly once")
        normalized_sources: list[dict[str, Any]] = []
        schema_ref: str | None = None
        total_bytes = 0
        for expected_seat, source in enumerate(raw_sources):
            if (
                not isinstance(source, dict)
                or set(source) != {"seat_index", "producer_output_receipt"}
                or source.get("seat_index") != expected_seat
            ):
                raise ValidationError("sequential handoff producer seats are not canonical")
            output = source.get("producer_output_receipt")
            output_fields = {
                "schema",
                "dispatch_id",
                "producer_binding_id",
                "producer_agent_id",
                "artifact_id",
                "path",
                "data_schema_ref",
                "sha256",
                "size_bytes",
                "route_digest",
                "receipt_digest",
            }
            if not isinstance(output, dict) or set(output) != output_fields:
                raise ValidationError("producer-output receipt shape is invalid")
            body_without_digest = dict(output)
            receipt_digest = body_without_digest.pop("receipt_digest")
            calculated_receipt_digest = digest_bytes(
                canonical_text(body_without_digest).encode("utf-8")
            )
            if (
                output["schema"] != "aci-host-workflow-producer-output/v1"
                or output["dispatch_id"] != record["dispatch_id"]
                or output["route_digest"] != route_digest
                or not isinstance(output["data_schema_ref"], str)
                or not output["data_schema_ref"]
                or not isinstance(output["size_bytes"], int)
                or isinstance(output["size_bytes"], bool)
                or output["size_bytes"] < 0
                or calculated_receipt_digest != receipt_digest
            ):
                raise ValidationError("producer-output receipt is invalid")
            relative = output["path"]
            if (
                not isinstance(relative, str)
                or not relative
                or Path(relative).is_absolute()
                or "\\" in relative
                or ".." in Path(relative).parts
            ):
                raise ValidationError("producer-output path is invalid")
            output_path = (root / relative).resolve()
            try:
                output_path.relative_to(root)
                cursor = root / relative
                while cursor != root:
                    if cursor.is_symlink():
                        raise ValidationError("producer-output symlinks are forbidden")
                    cursor = cursor.parent
                body = output_path.read_bytes()
            except (OSError, ValueError) as exc:
                raise ValidationError("producer-output bytes are unavailable") from exc
            actual_digest = digest_bytes(body)
            if (
                output["sha256"] != actual_digest
                or output["size_bytes"] != len(body)
                or output["artifact_id"]
                != "art_" + actual_digest.removeprefix("sha256:")[:32]
            ):
                raise ValidationError("producer-output bytes differ from immutable receipt")
            if schema_ref is None:
                schema_ref = output["data_schema_ref"]
            elif schema_ref != output["data_schema_ref"]:
                raise ValidationError("sequential producer outputs use different schemas")
            total_bytes += len(body)
            normalized_sources.append(
                {"source_kind": "binding-output", "producer_output_receipt": output}
            )
        if schema_ref is None:
            raise IntegrityError("sequential handoff has no producer schema")
        slots_by_target[target_group].append(
            {
                "name": f"sequential:{source_group}:{target_group}",
                "data_schema_ref": schema_ref,
                "cardinality": {"min": len(normalized_sources), "max": len(normalized_sources)},
                "max_bytes": total_bytes,
                "purpose": f"Exact ordered outputs from {source_group}.",
                "sources": normalized_sources,
            }
        )
        handoffs.append(receipt)
    return handoffs, slots_by_target


def compile_bound_launch_plan(
    *,
    repo_root: Path,
    record: dict[str, Any],
    capability_ref: str,
    output_dir: Path,
    authority_mode: str = "legacy-managed",
    record_authority: str = CHILD_RECORD_AUTHORITY,
    governance_root: Path | None = None,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    validate_opening_record(
        root,
        record,
        record_authority=record_authority,
        governance_root=governance_root,
    )
    route = resolve_dispatch_capability(
        root,
        capability_ref=capability_ref,
        authority_mode=authority_mode,
    )
    if record.get("dispatch_type") != route["ledger_dispatch_type"]:
        raise ValidationError("dispatch row type differs from the resolved capability")
    dispatch_id = record.get("dispatch_id")
    groups = record.get("groups")
    if not isinstance(dispatch_id, str) or not dispatch_id:
        raise ValidationError("dispatch_id is required")
    if not isinstance(groups, list) or not groups:
        raise ValidationError("groups must be a non-empty array")
    target_dir = _relative_output(root, output_dir)
    launches: list[dict[str, Any]] = []
    seen_groups: set[str] = set()
    for group in groups:
        if not isinstance(group, dict):
            raise ValidationError("each group must be an object")
        group_id = group.get("group_id")
        agents = group.get("agents")
        if (
            not isinstance(group_id, str)
            or not group_id
            or group_id in seen_groups
            or not isinstance(agents, list)
            or not agents
        ):
            raise ValidationError("each group requires a unique id and non-empty agents")
        seen_groups.add(group_id)
    handoffs, slots_by_target = _sequential_handoffs(
        root=root,
        target_dir=target_dir,
        record=record,
        capability_ref=capability_ref,
        route_digest=route["route_digest"],
    )
    for group in groups:
        group_id = group.get("group_id")
        agents = group.get("agents")
        for seat_index, agent in enumerate(agents):
            if not isinstance(agent, dict):
                raise ValidationError("each agent must be an object")
            prompt = agent.get("initial_prompt")
            if not isinstance(prompt, str) or not prompt.strip():
                raise ValidationError("each agent requires a non-empty initial_prompt")
            attempt_id = f"attempt-{group_id}-{seat_index}-0"
            manifest = {
                "schema": MANIFEST_SCHEMA,
                "dispatch_id": dispatch_id,
                "route_digest": route["route_digest"],
                "target": {
                    "group_id": group_id,
                    "seat_index": seat_index,
                    "turn_ordinal": 0,
                    "attempt_id": attempt_id,
                },
                "slots": slots_by_target[group_id],
            }
            manifest_path = target_dir / f"{group_id}-{seat_index}-turn-0.json"
            manifest_digest = _write_canonical(manifest_path, manifest)
            manifest_relative = manifest_path.relative_to(root).as_posix()
            envelope = {
                "schema": ENVELOPE_SCHEMA,
                "dispatch_id": dispatch_id,
                "group_id": group_id,
                "seat_index": seat_index,
                "turn_ordinal": 0,
                "attempt_id": attempt_id,
                "prompt_template_path": None,
                "prompt_template_digest": digest_bytes(prompt.encode("utf-8")),
                "workflow_manifest_path": manifest_relative,
                "workflow_manifest_digest": manifest_digest,
            }
            encoded = base64.urlsafe_b64encode(
                canonical_text(envelope).encode("utf-8")
            ).decode("ascii").rstrip("=")
            task_name = f"{group_id}_{seat_index}"
            launches.append(
                {
                    "group_id": group_id,
                    "seat_index": seat_index,
                    "attempt_id": attempt_id,
                    "requested_model": agent.get("model"),
                    "tool_profile_ref": route["tool_profile_ref"],
                    "spawn_arguments": {
                        "task_name": task_name,
                        "message": f"{BINDING_MARKER}{encoded}\n{prompt}",
                    },
                    "workflow_manifest_path": manifest_relative,
                    "workflow_manifest_digest": manifest_digest,
                }
            )
    plan = {
        "schema": LAUNCH_PLAN_SCHEMA,
        "dispatch_id": dispatch_id,
        "execution_authority_mode": authority_mode,
        "record_authority": record_authority,
        "route": route,
        "handoffs": handoffs,
        "launches": launches,
    }
    plan_path = target_dir / "launch-plan.json"
    plan_digest = _write_canonical(plan_path, plan)
    return {
        **plan,
        "launch_plan_path": plan_path.relative_to(root).as_posix(),
        "launch_plan_digest": plan_digest,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="dispatch-workflow")
    result.add_argument("--project-dir", type=Path, default=Path.cwd())
    commands = result.add_subparsers(dest="command", required=True)
    resolve = commands.add_parser("resolve")
    resolve.add_argument("--capability-ref", required=True)
    resolve.add_argument("--authority-mode", default="legacy-managed")
    compile_command = commands.add_parser("compile")
    compile_command.add_argument("--record", type=Path, required=True)
    compile_command.add_argument("--capability-ref", required=True)
    compile_command.add_argument("--output-dir", type=Path, required=True)
    compile_command.add_argument("--authority-mode", default="legacy-managed")
    compile_command.add_argument(
        "--record-authority",
        choices=RECORD_AUTHORITIES,
        default=CHILD_RECORD_AUTHORITY,
    )
    compile_command.add_argument("--governance-root", type=Path)
    opening = commands.add_parser("open")
    opening.add_argument("--record", type=Path, required=True)
    opening.add_argument("--host", choices=("codex", "claude"), required=True)
    opening.add_argument("--session-name", required=True)
    opening.add_argument("--origin-ref", required=True)
    opening.add_argument("--nonce", required=True)
    closing = commands.add_parser("close")
    closing.add_argument("--record", type=Path, required=True)
    closing.add_argument("--host", choices=("codex", "claude"), required=True)
    closing.add_argument("--session-id", required=True)
    closing.add_argument("--nonce", required=True)
    return result


def run(argv: Sequence[str] | None = None) -> dict[str, Any]:
    args = parser().parse_args(argv)
    root = args.project_dir.resolve()
    if args.command == "resolve":
        return resolve_dispatch_capability(
            root,
            capability_ref=args.capability_ref,
            authority_mode=args.authority_mode,
        )
    if args.command == "compile":
        return compile_bound_launch_plan(
            repo_root=root,
            record=_json_object(args.record, "dispatch opening record"),
            capability_ref=args.capability_ref,
            output_dir=args.output_dir,
            authority_mode=args.authority_mode,
            record_authority=args.record_authority,
            governance_root=args.governance_root,
        )
    record = _json_object(args.record, "dispatch lifecycle record")
    from .host_dispatch_hook import HostDispatchHook

    hook = HostDispatchHook(root=root, host=args.host)
    if args.command == "open":
        validate_opening_record(root, record)
        if record.get("dispatch_type") not in live_dispatch_type_values(root):
            raise GateBlockedError("dispatch opening type is not LIVE")
        return hook.open_parent_dispatch(
            record=record,
            session_name=args.session_name,
            origin_ref=args.origin_ref,
            nonce=args.nonce,
        )
    return hook.close_parent_dispatch(
        record=record,
        session_id=args.session_id,
        nonce=args.nonce,
    )


def main() -> None:
    print(json.dumps(run(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
