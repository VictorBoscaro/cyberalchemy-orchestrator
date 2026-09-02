"""Mandatory Claude/Codex Agent-tool lifecycle adapter for the local bridge."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Sequence

from .canonical import canonical_digest, canonical_text
from .dispatch_types import (
    live_dispatch_type_values,
    load_dispatch_type_registry,
    resolve_dispatch_capability,
)
from .errors import GateBlockedError, ValidationError
from .agent_roles import load_accepted_role_registry, load_host_role_routing
from .local_pilot import preflight_local_pilot
from .orchestration_bridge import (
    LEDGER,
    LocalOrchestrationLoggingBridge,
)

POLICY = Path(
    "docs/features/agent-provenance-telemetry/integration/stage-f/"
    "host-hook-policy.json"
)
POLICY_FIELDS = {
    "schema",
    "enabled",
    "hosts",
    "principal_id",
    "authorization_evidence_ref",
    "authorization_evidence_digest",
    "database",
    "ledger",
    "compatibility_dispatch_type",
    "default_token_budget",
    "capability_ttl_seconds",
}
AGENT_TOOL_NAMES = {"Agent", "spawn_agent", "followup_task"}
WORKFLOW_BINDING_MARKER = "ACI-WORKFLOW-BINDING-V1:"
WORKFLOW_ENVELOPE_FIELDS = {
    "schema",
    "dispatch_id",
    "group_id",
    "seat_index",
    "turn_ordinal",
    "attempt_id",
    "prompt_template_path",
    "prompt_template_digest",
    "workflow_manifest_path",
    "workflow_manifest_digest",
}
RUNNING_STATUSES = {"running", "pending", "in_progress"}
def _strict_object(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise GateBlockedError(f"{label} shape is invalid")
    return value


def _safe_part(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", value).strip("-")[:64] or "agent"


def _find_string(value: Any, key: str) -> str | None:
    if isinstance(value, dict):
        candidate = value.get(key)
        if isinstance(candidate, str) and candidate:
            return candidate
        for nested in value.values():
            found = _find_string(nested, key)
            if found:
                return found
    elif isinstance(value, list):
        for nested in value:
            found = _find_string(nested, key)
            if found:
                return found
    elif isinstance(value, str):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return None
        return _find_string(decoded, key)
    return None


class HostDispatchHook:
    """Turn host lifecycle events into exact bridge open/close operations."""

    def __init__(
        self,
        *,
        root: Path,
        host: str,
        now=None,
    ) -> None:
        self.root = Path(root).resolve()
        self.host = host
        self.now = now or (lambda: datetime.now(timezone.utc))
        self.policy = self._load_policy()
        self.agent_role_registry = load_accepted_role_registry(self.root)
        self.agent_role_routing = load_host_role_routing(self.root, self.agent_role_registry)
        database = (self.root / self.policy["database"]).resolve()
        ledger = (self.root / self.policy["ledger"]).resolve()
        if ledger != (self.root / LEDGER).resolve():
            raise GateBlockedError("host hook policy must select the exact dispatch ledger")
        try:
            database.relative_to(self.root)
            ledger.relative_to(self.root)
        except ValueError as exc:
            raise GateBlockedError("host hook policy path escapes repository") from exc
        self.database = database
        self.ledger = ledger
        self.state_root = database.parent / "orchestration-hooks" / host

    def _load_policy(self) -> dict[str, Any]:
        try:
            policy = json.loads((self.root / POLICY).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise GateBlockedError("mandatory host-hook policy is unavailable") from exc
        _strict_object(policy, POLICY_FIELDS, "host-hook policy")
        digest = policy["authorization_evidence_digest"]
        if (
            policy["schema"] != "aci-host-dispatch-hook-policy/v1"
            or policy["enabled"] is not True
            or not isinstance(policy["hosts"], list)
            or self.host not in policy["hosts"]
            or not isinstance(policy["principal_id"], str)
            or not policy["principal_id"]
            or not isinstance(policy["authorization_evidence_ref"], str)
            or not policy["authorization_evidence_ref"]
            or not isinstance(digest, str)
            or not re.fullmatch(r"sha256:[0-9a-f]{64}", digest)
            or policy["compatibility_dispatch_type"]
            not in live_dispatch_type_values(self.root)
            or not isinstance(policy["default_token_budget"], int)
            or policy["default_token_budget"] <= 0
            or not isinstance(policy["capability_ttl_seconds"], int)
            or not 1 <= policy["capability_ttl_seconds"] <= 600
        ):
            raise GateBlockedError("mandatory host-hook policy is invalid")
        return policy

    def _state_path(self, event: dict[str, Any]) -> Path:
        session_id = self._required_text(event, "session_id")
        tool_use_id = self._required_text(event, "tool_use_id")
        session = canonical_digest({"session_id": session_id})[7:23]
        tool = canonical_digest({"tool_use_id": tool_use_id})[7:31]
        return self.state_root / session / f"{tool}.json"

    @staticmethod
    def _required_text(event: dict[str, Any], field: str) -> str:
        value = event.get(field)
        if not isinstance(value, str) or not value:
            raise GateBlockedError(f"host hook input requires {field}")
        return value

    @staticmethod
    def _read_state(path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise GateBlockedError("host dispatch state is malformed") from exc
        if not isinstance(state, dict):
            raise GateBlockedError("host dispatch state is malformed")
        return state

    @staticmethod
    def _write_state(path: Path, state: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(
            f".{path.name}.{os.getpid()}.{os.urandom(4).hex()}.tmp"
        )
        try:
            with temporary.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(canonical_text(state))
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            if temporary.exists():
                temporary.unlink()

    def _runtime_bridge(self):
        runtime, receipt = preflight_local_pilot(
            repo_root=self.root,
            database_path=self.database,
            ledger_path=self.ledger,
            host="127.0.0.1",
            opted_in=True,
            now=self.now,
        )
        return runtime, LocalOrchestrationLoggingBridge(
            runtime=runtime,
            project_dir=self.root,
            prepared_receipt={"preflight": receipt},
        )

    def _authority(
        self,
        runtime,
        *,
        operation: str,
        record: dict[str, Any],
        session_name: str | None = None,
        origin_ref: str | None = None,
        session_id: str | None = None,
        nonce: str,
    ):
        context: dict[str, Any] = {
            "operation": operation,
            "dispatch_id": record[
                "dispatch_id" if operation == "open" else "close_of"
            ],
            "record_digest": canonical_digest(record),
            "authorization_evidence_ref": self.policy[
                "authorization_evidence_ref"
            ],
            "authorization_evidence_digest": self.policy[
                "authorization_evidence_digest"
            ],
            "nonce": nonce,
        }
        action = f"orchestration.bridge.{operation}"
        phase = "bootstrap" if operation == "open" else "finalize"
        if operation == "open":
            context.update(
                {"session_name": session_name, "origin_ref": origin_ref}
            )
        else:
            context["session_id"] = session_id
        expires_at = (
            self.now()
            + timedelta(seconds=self.policy["capability_ttl_seconds"])
        ).isoformat()
        issued = runtime.issue_capability(
            principal_id=self.policy["principal_id"],
            action=action,
            phase=phase,
            context=context,
            expires_at=expires_at,
        )
        return runtime.capabilities.resolve(
            issued["token"], action=action, phase=phase
        )

    def open_parent_dispatch(
        self,
        *,
        record: dict[str, Any],
        session_name: str,
        origin_ref: str,
        nonce: str,
    ) -> dict[str, Any]:
        """Open one confirmed parent through the same fail-closed bridge as hooks."""
        runtime, bridge = self._runtime_bridge()
        authority = self._authority(
            runtime,
            operation="open",
            record=record,
            session_name=session_name,
            origin_ref=origin_ref,
            nonce=nonce,
        )
        return bridge.open_dispatch(
            authority=authority,
            record=record,
            session_name=session_name,
            origin_ref=origin_ref,
        )

    def close_parent_dispatch(
        self,
        *,
        record: dict[str, Any],
        session_id: str,
        nonce: str,
    ) -> dict[str, Any]:
        """Close one parent after every bound seat has reached a terminal state."""
        runtime, bridge = self._runtime_bridge()
        authority = self._authority(
            runtime,
            operation="close",
            record=record,
            session_id=session_id,
            nonce=nonce,
        )
        return bridge.close_dispatch(
            authority=authority,
            record=record,
            session_id=session_id,
        )

    @staticmethod
    def _prompt(tool_input: dict[str, Any]) -> str:
        for field in ("message", "prompt"):
            value = tool_input.get(field)
            if isinstance(value, str) and value.strip():
                return value.strip()
        raise GateBlockedError("Agent tool input requires message or prompt")

    @staticmethod
    def _workflow_envelope(
        tool_input: dict[str, Any],
    ) -> tuple[dict[str, Any], str] | None:
        raw = next(
            (
                tool_input[field]
                for field in ("message", "prompt")
                if isinstance(tool_input.get(field), str)
            ),
            None,
        )
        if raw is None or not raw.startswith(WORKFLOW_BINDING_MARKER):
            return None
        first, separator, prompt_body = raw.partition("\n")
        if not separator or not prompt_body:
            raise GateBlockedError(
                "workflow binding marker requires a prompt body"
            )
        encoded = first[len(WORKFLOW_BINDING_MARKER) :]
        try:
            padding = "=" * (-len(encoded) % 4)
            decoded = base64.urlsafe_b64decode(encoded + padding)
            envelope = json.loads(decoded.decode("utf-8"))
        except Exception as exc:
            raise GateBlockedError("workflow binding envelope is malformed") from exc
        _strict_object(envelope, WORKFLOW_ENVELOPE_FIELDS, "workflow binding")
        if envelope["schema"] != "aci-host-workflow-binding/v1":
            raise GateBlockedError("workflow binding schema is unsupported")
        return envelope, prompt_body

    def _role(self, text: str) -> str:
        lowered = text.lower()
        for route in self.agent_role_routing["routes"]:
            if any(word in lowered for word in route["keywords"]):
                return route["role"]
        return self.agent_role_routing["fallback_role"]

    def _opening_record(
        self, event: dict[str, Any]
    ) -> tuple[dict[str, Any], str, str, str]:
        tool_input = event.get("tool_input")
        if not isinstance(tool_input, dict):
            raise GateBlockedError("Agent tool input must be an object")
        prompt = self._prompt(tool_input)
        session_id = self._required_text(event, "session_id")
        tool_use_id = self._required_text(event, "tool_use_id")
        identity = canonical_digest(
            {
                "host": self.host,
                "session_id": session_id,
                "tool_use_id": tool_use_id,
            }
        )[7:23]
        dispatch_id = (
            f"{self.now().date().isoformat()}-auto-{self.host}-agent-{identity}"
        )
        label = next(
            (
                tool_input[field].strip()
                for field in ("task_name", "description", "name")
                if isinstance(tool_input.get(field), str)
                and tool_input[field].strip()
            ),
            f"{self.host} agent {identity}",
        )
        model = tool_input.get("model") or event.get("model") or f"{self.host}-default"
        if not isinstance(model, str):
            model = f"{self.host}-default"
        role = self._role(f"{label}\n{prompt}")
        agent_name = _safe_part(label)
        registry = load_dispatch_type_registry(self.root)
        compatibility_type = self.policy["compatibility_dispatch_type"]
        compatibility_entry = next(
            (
                entry
                for entry in registry["types"]
                if entry["ledger_value"] == compatibility_type
            ),
            None,
        )
        if compatibility_entry is None or not compatibility_entry.get("capability_ref"):
            raise GateBlockedError("compatibility dispatch type is not canonically routable")
        capability_route = resolve_dispatch_capability(
            self.root,
            capability_ref=compatibility_entry["capability_ref"],
            authority_mode="legacy-managed",
        )
        record = {
            "dispatch_id": dispatch_id,
            "schema_version": registry["ledger_schema_version"],
            "agent_role_registry_ref": registry["agent_role_registry_ref"],
            "dispatch_type": compatibility_type,
            "capability_route": capability_route,
            "goal": f"Automatically supervise host agent call: {label[:240]}",
            "context": (
                f"Mandatory {self.host} host hook captured this Agent tool call "
                "before launch. The review/inline dispatch type is a compatibility "
                "envelope for an arbitrary host-returned subagent; the concrete "
                f"task role is recorded as {role}. Launch is denied unless YAML "
                "and ACI opening receipts both succeed."
            ),
            "max_loops": 1,
            "final_approver": "parent",
            "anti_bias_mode": "disabled",
            "output_mode": "inline",
            "invoked_by": self.policy["principal_id"],
            "groups": [
                {
                    "group_id": f"{self.host}-agent",
                    "n": 1,
                    "agents": [
                        {
                            "agent_name": agent_name,
                            "role": role,
                            "model": model,
                            "token_budget": self.policy["default_token_budget"],
                            "initial_prompt": prompt,
                        }
                    ],
                }
            ],
            "connections": [],
        }
        return record, role, session_id, tool_use_id

    def pre_tool_use(self, event: dict[str, Any]) -> dict[str, Any]:
        if event.get("tool_name") not in AGENT_TOOL_NAMES:
            raise GateBlockedError("mandatory hook accepts only the Agent tool")
        tool_input = event.get("tool_input")
        if not isinstance(tool_input, dict):
            raise GateBlockedError("Agent tool input must be an object")
        workflow = self._workflow_envelope(tool_input)
        if workflow is not None:
            envelope, prompt_body = workflow
            state_path = self._state_path(event)
            input_digest = canonical_digest(tool_input)
            existing = self._read_state(state_path)
            if existing:
                if (
                    existing.get("host") != self.host
                    or existing.get("tool_input_digest") != input_digest
                    or existing.get("binding_id") is None
                    or existing.get("status") not in {"opened", "closed"}
                ):
                    raise GateBlockedError(
                        "bound host Agent retry differs from recorded launch"
                    )
                if existing["status"] == "closed":
                    raise GateBlockedError("bound host Agent tool id is already closed")
                return existing
            tool_name = event["tool_name"]
            turn_ordinal = envelope["turn_ordinal"]
            if (
                tool_name == "followup_task"
                and (
                    not isinstance(turn_ordinal, int)
                    or turn_ordinal <= 0
                )
            ):
                raise GateBlockedError("followup_task requires turn_ordinal > 0")
            if tool_name != "followup_task" and turn_ordinal != 0:
                raise GateBlockedError("spawn launch requires turn_ordinal 0")
            runtime, _bridge = self._runtime_bridge()
            receipt = runtime.bind_host_workflow_turn(
                host=self.host,
                host_session_id=self._required_text(event, "session_id"),
                tool_use_id=self._required_text(event, "tool_use_id"),
                tool_input=tool_input,
                dispatch_id=envelope["dispatch_id"],
                group_id=envelope["group_id"],
                seat_index=envelope["seat_index"],
                turn_ordinal=turn_ordinal,
                attempt_id=envelope["attempt_id"],
                prompt_body=prompt_body,
                prompt_template_path=envelope["prompt_template_path"],
                prompt_template_digest=envelope["prompt_template_digest"],
                workflow_manifest_path=envelope["workflow_manifest_path"],
                workflow_manifest_digest=envelope["workflow_manifest_digest"],
                actor_ref=self.policy["principal_id"],
            )
            if receipt.get("status") != "launch-authorized":
                raise GateBlockedError(
                    "runtime did not authorize bound host Agent launch"
                )
            state = {
                "schema": "aci-host-workflow-state/v1",
                "host": self.host,
                "host_session_id": self._required_text(event, "session_id"),
                "tool_use_id": self._required_text(event, "tool_use_id"),
                "tool_input_digest": input_digest,
                "dispatch_id": receipt["dispatch_id"],
                "session_id": receipt["session_id"],
                "binding_id": receipt["binding_id"],
                "group_id": receipt["group_id"],
                "seat_index": receipt["seat_index"],
                "turn_ordinal": receipt["turn_ordinal"],
                "attempt_id": receipt["attempt_id"],
                "role": "bound-seat",
                "agent_type": tool_input.get("subagent_type"),
                "agent_id": (
                    tool_input.get("target")
                    if tool_name == "followup_task"
                    else None
                ),
                "status": "opened",
                "bound_event_id": receipt["bound_event_id"],
                "workflow_manifest_artifact_id": receipt[
                    "workflow_manifest_artifact_id"
                ],
            }
            self._write_state(state_path, state)
            return state
        if event["tool_name"] == "followup_task":
            raise GateBlockedError(
                "followup_task requires a governed workflow binding envelope"
            )
        record, role, host_session_id, tool_use_id = self._opening_record(event)
        state_path = self._state_path(event)
        input_digest = canonical_digest(event["tool_input"])
        existing = self._read_state(state_path)
        if existing:
            if (
                existing.get("host") != self.host
                or existing.get("tool_input_digest") != input_digest
                or existing.get("dispatch_id") != record["dispatch_id"]
                or existing.get("status") not in {"preparing", "opened", "closed"}
            ):
                raise GateBlockedError("host Agent retry differs from recorded launch")
            if existing["status"] == "closed":
                raise GateBlockedError("host Agent tool id is already closed")
            if existing["status"] == "opened":
                return existing
            state = existing
        else:
            state = {
                "schema": "aci-host-dispatch-state/v1",
                "host": self.host,
                "host_session_id": host_session_id,
                "tool_use_id": tool_use_id,
                "tool_input_digest": input_digest,
                "dispatch_id": record["dispatch_id"],
                "session_id": None,
                "role": role,
                "agent_type": event["tool_input"].get("subagent_type"),
                "agent_id": None,
                "status": "preparing",
                "record": record,
            }
            self._write_state(state_path, state)
        runtime, bridge = self._runtime_bridge()
        session_name = f"{self.host}-mandatory-agent-hook"
        origin_ref = f"{self.host}:session:{host_session_id}"
        authority = self._authority(
            runtime,
            operation="open",
            record=record,
            session_name=session_name,
            origin_ref=origin_ref,
            nonce=f"{self.host}:{tool_use_id}:open",
        )
        opened = bridge.open_dispatch(
            authority=authority,
            record=record,
            session_name=session_name,
            origin_ref=origin_ref,
        )
        if opened.get("status") != "launch-authorized":
            raise GateBlockedError("bridge did not authorize Agent launch")
        state = {
            **state,
            "session_id": opened["session_id"],
            "status": "opened",
            "opened_event_id": opened["orchestration_receipt"][
                "orchestration_dispatch"
            ]["event_id"],
            "opened_offset": opened["orchestration_receipt"]["first_offset"],
        }
        self._write_state(state_path, state)
        return state

    def _close_state(
        self,
        path: Path,
        state: dict[str, Any],
        *,
        exit_reason: str,
    ) -> dict[str, Any]:
        if state.get("status") == "closed":
            return state
        binding_id = state.get("binding_id")
        if isinstance(binding_id, str) and binding_id:
            terminal_state = {
                "resolved": "resolved",
                "error": "error",
                "user_abort": "cancelled",
            }[exit_reason]
            runtime, _bridge = self._runtime_bridge()
            terminal = runtime.complete_host_workflow_turn(
                binding_id=binding_id,
                state=terminal_state,
                agent_id=state.get("agent_id"),
                actor_ref=self.policy["principal_id"],
            )
            state = {
                **state,
                "status": "closed",
                "exit_reason": exit_reason,
                "binding_state": terminal["state"],
                "terminal_event_id": terminal["terminal_event_id"],
            }
            self._write_state(path, state)
            return state
        record = {
            "close_of": state["dispatch_id"],
            "schema_version": state["record"]["schema_version"],
            "agent_role_registry_ref": state["record"]["agent_role_registry_ref"],
            "exit_reason": exit_reason,
            "capability_route_digest": state["record"]["capability_route"][
                "route_digest"
            ],
            "agents_spawned": {
                "total": 1,
                "tree": {state["role"]: 1, "helpers": 0},
                "loops_used": 1,
            },
            "feedback_prompts": [],
            "invoked_by": self.policy["principal_id"],
        }
        runtime, bridge = self._runtime_bridge()
        authority = self._authority(
            runtime,
            operation="close",
            record=record,
            session_id=state["session_id"],
            nonce=f"{self.host}:{state['tool_use_id']}:close:{exit_reason}",
        )
        closed = bridge.close_dispatch(
            authority=authority,
            record=record,
            session_id=state["session_id"],
        )
        state = {
            **state,
            "status": "closed",
            "exit_reason": exit_reason,
            "closed_event_id": closed["orchestration_receipt"][
                "orchestration_dispatch"
            ]["event_id"],
            "closed_offset": closed["orchestration_receipt"]["first_offset"],
        }
        self._write_state(path, state)
        return state

    def post_tool_use(self, event: dict[str, Any]) -> dict[str, Any]:
        path = self._state_path(event)
        state = self._read_state(path)
        if not state:
            raise GateBlockedError("Agent completed without a bridge opening state")
        if canonical_digest(event.get("tool_input")) != state.get(
            "tool_input_digest"
        ):
            raise GateBlockedError("completed Agent input differs from opening state")
        if state.get("status") == "closed":
            return state
        response = event.get("tool_response")
        agent_id = _find_string(response, "agent_id")
        status = _find_string(response, "status")
        if agent_id:
            state = {**state, "agent_id": agent_id}
            self._write_state(path, state)
        if status and status.lower() in RUNNING_STATUSES:
            if not agent_id:
                raise GateBlockedError("running Agent response has no agent_id")
            return state
        return self._close_state(path, state, exit_reason="resolved")

    def post_tool_failure(self, event: dict[str, Any]) -> dict[str, Any]:
        path = self._state_path(event)
        state = self._read_state(path)
        if not state:
            raise GateBlockedError("failed Agent call has no bridge opening state")
        if canonical_digest(event.get("tool_input")) != state.get(
            "tool_input_digest"
        ):
            raise GateBlockedError("failed Agent input differs from opening state")
        return self._close_state(path, state, exit_reason="error")

    def _open_states(self, host_session_id: str) -> list[tuple[Path, dict[str, Any]]]:
        if not self.state_root.exists():
            return []
        states: list[tuple[Path, dict[str, Any]]] = []
        for path in self.state_root.glob("*/*.json"):
            state = self._read_state(path)
            if (
                state
                and state.get("host_session_id") == host_session_id
                and state.get("status") == "opened"
            ):
                states.append((path, state))
        return states

    def subagent_stop(self, event: dict[str, Any]) -> dict[str, Any]:
        host_session_id = self._required_text(event, "session_id")
        agent_id = self._required_text(event, "agent_id")
        candidates = [
            (path, state)
            for path, state in self._open_states(host_session_id)
            if state.get("agent_id") == agent_id
        ]
        if not candidates:
            agent_type = event.get("agent_type")
            unclaimed = [
                (path, state)
                for path, state in self._open_states(host_session_id)
                if state.get("agent_id") is None
                and (
                    state.get("agent_type") == agent_type
                    or state.get("agent_type") is None
                )
            ]
            if len(unclaimed) == 1:
                path, state = unclaimed[0]
                state = {**state, "agent_id": agent_id}
                self._write_state(path, state)
                candidates = [(path, state)]
        if len(candidates) != 1:
            raise GateBlockedError(
                "SubagentStop cannot resolve exactly one bridge opening"
            )
        return self._close_state(*candidates[0], exit_reason="resolved")

    def session_end(self, event: dict[str, Any]) -> list[dict[str, Any]]:
        host_session_id = self._required_text(event, "session_id")
        return [
            self._close_state(path, state, exit_reason="user_abort")
            for path, state in self._open_states(host_session_id)
        ]

    def handle(self, event: dict[str, Any]) -> Any:
        tool_name = event.get("tool_name")
        if isinstance(tool_name, str) and tool_name != "Agent":
            canonical_tool_name = next(
                (
                    candidate
                    for candidate in ("spawn_agent", "followup_task")
                    if tool_name.endswith(candidate)
                ),
                tool_name,
            )
            event = {
                **event,
                "tool_name": canonical_tool_name,
            }
        event_name = event.get("hook_event_name")
        if event_name == "PreToolUse":
            return self.pre_tool_use(event)
        if event_name == "PostToolUse":
            return self.post_tool_use(event)
        if event_name == "PostToolUseFailure":
            return self.post_tool_failure(event)
        if event_name == "SubagentStop":
            return self.subagent_stop(event)
        if event_name == "SessionEnd":
            return self.session_end(event)
        if event_name == "Stop":
            return self.session_end(event)
        raise GateBlockedError(f"unsupported mandatory hook event: {event_name}")


def _deny(host: str, reason: str) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Mandatory {host} orchestration bridge blocked Agent launch: {reason}"
            ),
        }
    }


def _stop_block(host: str, reason: str) -> dict[str, Any]:
    if host == "claude":
        return {
            "decision": "block",
            "reason": f"Mandatory bridge close failed; retry closure: {reason}",
        }
    return {
        "continue": False,
        "stopReason": f"Mandatory bridge close failed; retry closure: {reason}",
        "systemMessage": f"Mandatory bridge close failed: {reason}",
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="host-dispatch-hook")
    result.add_argument("--host", choices=("claude", "codex"), required=True)
    return result


def run(
    argv: Sequence[str] | None = None,
    *,
    stdin: str | None = None,
) -> tuple[int, dict[str, Any] | None]:
    args = parser().parse_args(argv)
    raw = sys.stdin.read() if stdin is None else stdin
    try:
        event = json.loads(raw)
        if not isinstance(event, dict):
            raise ValidationError("hook input must be one JSON object")
        cwd = event.get("cwd")
        if not isinstance(cwd, str) or not cwd:
            raise GateBlockedError("hook input requires cwd")
        root_text = os.environ.get("ACI_HOST_HOOK_PROJECT_ROOT")
        if root_text:
            root = Path(root_text)
        else:
            root = Path(cwd)
            while root != root.parent and not (root / ".git").exists():
                root = root.parent
        hook = HostDispatchHook(root=root, host=args.host)
        result = hook.handle(event)
        return 0, None if result is not None else None
    except Exception as exc:
        event_name = None
        try:
            decoded = json.loads(raw)
            event_name = decoded.get("hook_event_name")
        except Exception:
            pass
        if event_name == "PreToolUse":
            return 0, _deny(args.host, str(exc))
        if event_name in {"SubagentStop", "Stop"}:
            return 0, _stop_block(args.host, str(exc))
        return 0, {
            "systemMessage": (
                f"Mandatory {args.host} orchestration bridge lifecycle error: {exc}"
            )
        }


def main() -> None:
    code, output = run()
    if output is not None:
        print(json.dumps(output, ensure_ascii=False, separators=(",", ":")))
    raise SystemExit(code)


if __name__ == "__main__":
    main()
