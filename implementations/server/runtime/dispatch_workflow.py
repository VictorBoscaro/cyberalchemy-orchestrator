"""Operational adapter for routed legacy dispatches and bound host seats."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Sequence

from .canonical import canonical_text, digest_bytes, parse_strict_json
from .dispatch_types import (
    load_dispatch_type_registry,
    live_dispatch_type_values,
    resolve_dispatch_capability,
)
from .errors import GateBlockedError, ValidationError
from .host_dispatch_hook import HostDispatchHook


BINDING_MARKER = "ACI-WORKFLOW-BINDING-V1:"
MANIFEST_SCHEMA = "aci-workflow-input-manifest/v1"
ENVELOPE_SCHEMA = "aci-host-workflow-binding/v1"
LAUNCH_PLAN_SCHEMA = "aci-bound-launch-plan/v1"
APPENDER = Path(".claude/skills/register-dispatch/append-dispatch.cjs")
HANDOFF_SCHEMA = "aci-workflow-sequential-handoff/v1"
PRODUCER_OUTPUT_SCHEMA = "aci-host-workflow-producer-output/v1"
_GROUP_ID = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?$")


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


def _repository_file(repo_root: Path, relative: str) -> tuple[bytes, str]:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValidationError("sequential handoff source path must be repository-relative")
    root = Path(repo_root).resolve()
    unresolved = root / relative
    resolved = unresolved.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValidationError("sequential handoff source escapes the repository") from exc
    cursor = unresolved
    while cursor != root:
        if cursor.is_symlink():
            raise ValidationError("sequential handoff source symlinks are forbidden")
        cursor = cursor.parent
    if not resolved.is_file():
        raise ValidationError("sequential handoff source is missing")
    body = resolved.read_bytes()
    return body, resolved.relative_to(root).as_posix()


def _handoff_receipt(
    *,
    repo_root: Path,
    target_dir: Path,
    dispatch_id: str,
    route: dict[str, Any],
    connection: dict[str, Any],
    from_index: int,
    to_index: int,
    upstream_seat_count: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt_path = target_dir / f"handoff-{from_index}-{to_index}.json"
    try:
        raw = receipt_path.read_bytes()
        receipt = parse_strict_json(raw)
    except (OSError, ValidationError) as exc:
        raise GateBlockedError(
            "workflow compiler does not materialize connection handoffs when "
            f"the sequential receipt for {connection['from']} -> "
            f"{connection['to']} is unavailable or malformed"
        ) from exc
    expected_fields = {
        "schema",
        "dispatch_id",
        "capability_ref",
        "route_digest",
        "connection",
        "sources",
    }
    if not isinstance(receipt, dict) or set(receipt) != expected_fields:
        raise ValidationError("sequential handoff receipt shape is invalid")
    if (
        receipt["schema"] != HANDOFF_SCHEMA
        or receipt["dispatch_id"] != dispatch_id
        or receipt["capability_ref"] != route["capability_ref"]
        or receipt["route_digest"] != route["route_digest"]
        or receipt["connection"] != connection
    ):
        raise ValidationError("sequential handoff identity or capability route differs")
    sources = receipt["sources"]
    if not isinstance(sources, list) or len(sources) != upstream_seat_count:
        raise ValidationError("sequential handoff must contain one source per upstream seat")
    manifested_sources: list[dict[str, Any]] = []
    data_schema_ref: str | None = None
    total_bytes = 0
    for expected_seat, source in enumerate(sources):
        fields = {"seat_index", "producer_output_receipt"}
        if not isinstance(source, dict) or set(source) != fields:
            raise ValidationError("sequential handoff source shape is invalid")
        if source["seat_index"] != expected_seat:
            raise ValidationError("sequential handoff sources must follow upstream seat order")
        output = source["producer_output_receipt"]
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
        if (
            output["schema"] != PRODUCER_OUTPUT_SCHEMA
            or output["dispatch_id"] != dispatch_id
            or output["route_digest"] != route["route_digest"]
            or any(
                not isinstance(output[field], str) or not output[field]
                for field in (
                    "producer_binding_id",
                    "producer_agent_id",
                    "artifact_id",
                    "path",
                    "data_schema_ref",
                    "sha256",
                    "receipt_digest",
                )
            )
            or isinstance(output["size_bytes"], bool)
            or not isinstance(output["size_bytes"], int)
            or output["size_bytes"] < 0
        ):
            raise ValidationError("producer-output receipt identity is invalid")
        receipt_body = dict(output)
        claimed_receipt_digest = receipt_body.pop("receipt_digest")
        if digest_bytes(canonical_text(receipt_body).encode("utf-8")) != claimed_receipt_digest:
            raise ValidationError("producer-output receipt digest is invalid")
        body, normalized_path = _repository_file(repo_root, output["path"])
        actual_digest = digest_bytes(body)
        if normalized_path != output["path"]:
            raise ValidationError("producer-output receipt path is not canonical")
        if output["sha256"] != actual_digest or output["size_bytes"] != len(body):
            raise ValidationError("producer-output bytes differ from immutable receipt")
        if data_schema_ref is None:
            data_schema_ref = output["data_schema_ref"]
        elif output["data_schema_ref"] != data_schema_ref:
            raise ValidationError("one sequential handoff cannot mix data schemas")
        total_bytes += len(body)
        manifested_sources.append(
            {
                "source_kind": "binding-output",
                "producer_output_receipt": output,
            }
        )
    slot = {
        "name": f"sequential-{connection['from']}",
        "data_schema_ref": data_schema_ref,
        "cardinality": {"min": upstream_seat_count, "max": upstream_seat_count},
        "max_bytes": total_bytes,
        "purpose": f"Consume the exact terminal output of group {connection['from']}.",
        "sources": manifested_sources,
    }
    receipt_ref = {
        "from": connection["from"],
        "to": connection["to"],
        "path": receipt_path.relative_to(Path(repo_root).resolve()).as_posix(),
        "digest": digest_bytes(raw),
        "route_digest": route["route_digest"],
    }
    return slot, receipt_ref


def validate_opening_record(repo_root: Path, record: dict[str, Any]) -> None:
    """Run the canonical appender's complete opening validation without appending."""
    root = Path(repo_root).resolve()
    appender = root / APPENDER
    if not appender.is_file():
        raise GateBlockedError("validated dispatch appender is unavailable")
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".json", delete=False
        ) as handle:
            handle.write(canonical_text(record))
            temporary = Path(handle.name)
        environment = dict(os.environ)
        environment["CLAUDE_PROJECT_DIR"] = str(root)
        result = subprocess.run(
            ["node", str(appender), str(temporary), "--validate-only"],
            cwd=root,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise GateBlockedError("validated dispatch appender could not run") from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValidationError(f"dispatch opening record is invalid: {detail}")


def compile_bound_launch_plan(
    *,
    repo_root: Path,
    record: dict[str, Any],
    capability_ref: str,
    output_dir: Path,
    authority_mode: str = "legacy-managed",
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    validate_opening_record(root, record)
    route = resolve_dispatch_capability(
        root,
        capability_ref=capability_ref,
        authority_mode=authority_mode,
    )
    if record.get("capability_route") != route:
        raise ValidationError("dispatch row capability route differs from resolved route")
    registry = load_dispatch_type_registry(root)
    if record.get("schema_version") != registry["ledger_schema_version"]:
        raise ValidationError("dispatch row schema_version differs from the registry")
    if record.get("dispatch_type") != route["ledger_dispatch_type"]:
        raise ValidationError("dispatch row type differs from the resolved capability")
    dispatch_id = record.get("dispatch_id")
    groups = record.get("groups")
    if not isinstance(dispatch_id, str) or not dispatch_id:
        raise ValidationError("dispatch_id is required")
    if not isinstance(groups, list) or not groups:
        raise ValidationError("groups must be a non-empty array")
    connections = record.get("connections", [])
    if not isinstance(connections, list):
        raise ValidationError("connections must be an array")
    target_dir = _relative_output(root, output_dir)
    prepared_groups: list[tuple[str, list[dict[str, Any]]]] = []
    seen_groups: set[str] = set()
    for group in groups:
        if not isinstance(group, dict):
            raise ValidationError("each group must be an object")
        group_id = group.get("group_id")
        agents = group.get("agents")
        if (
            not isinstance(group_id, str)
            or not group_id
            or not _GROUP_ID.fullmatch(group_id)
            or group_id in seen_groups
            or not isinstance(agents, list)
            or not agents
        ):
            raise ValidationError("each group requires a unique id and non-empty agents")
        seen_groups.add(group_id)
        prepared_agents: list[dict[str, Any]] = []
        for seat_index, agent in enumerate(agents):
            if not isinstance(agent, dict):
                raise ValidationError("each agent must be an object")
            prompt = agent.get("initial_prompt")
            if not isinstance(prompt, str) or not prompt.strip():
                raise ValidationError("each agent requires a non-empty initial_prompt")
            prepared_agents.append(agent)
        prepared_groups.append((group_id, prepared_agents))

    group_indexes = {
        group_id: index for index, (group_id, _) in enumerate(prepared_groups)
    }
    incoming_slots: dict[str, list[tuple[int, dict[str, Any]]]] = {
        group_id: [] for group_id, _ in prepared_groups
    }
    handoff_refs: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str]] = set()
    prepared_connections: list[tuple[int, int, dict[str, Any]]] = []
    for connection in connections:
        if not isinstance(connection, dict):
            raise ValidationError("each connection must be an object")
        connection_type = connection.get("type")
        if connection_type != "sequential":
            raise GateBlockedError(
                f"unsupported workflow connection semantics: {connection_type!r}"
            )
        if set(connection) != {"from", "to", "type"}:
            raise ValidationError(
                "sequential connections contain exactly from, to, and type"
            )
        source_group = connection.get("from")
        target_group = connection.get("to")
        if source_group not in group_indexes or target_group not in group_indexes:
            raise ValidationError("sequential connection references an unknown group")
        edge = (source_group, target_group)
        if edge in seen_edges:
            raise ValidationError("duplicate sequential connections are forbidden")
        seen_edges.add(edge)
        from_index = group_indexes[source_group]
        to_index = group_indexes[target_group]
        if from_index >= to_index:
            raise GateBlockedError(
                "sequential connections must follow canonical declared group order"
            )
        prepared_connections.append((from_index, to_index, connection))
    for from_index, to_index, connection in sorted(prepared_connections):
        source_group = connection["from"]
        target_group = connection["to"]
        slot, receipt_ref = _handoff_receipt(
            repo_root=root,
            target_dir=target_dir,
            dispatch_id=dispatch_id,
            route=route,
            connection=connection,
            from_index=from_index,
            to_index=to_index,
            upstream_seat_count=len(prepared_groups[from_index][1]),
        )
        incoming_slots[target_group].append((from_index, slot))
        handoff_refs.append(receipt_ref)

    launches: list[dict[str, Any]] = []
    for group_id, agents in prepared_groups:
        slots = [
            slot
            for _, slot in sorted(incoming_slots[group_id], key=lambda item: item[0])
        ]
        for seat_index, agent in enumerate(agents):
            prompt = agent["initial_prompt"]
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
                "slots": slots,
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
        "route": route,
        "handoffs": handoff_refs,
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
        )
    record = _json_object(args.record, "dispatch lifecycle record")
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
