"""Prospective local bridge from sanctioned YAML dispatches to ACI receipts."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

from .canonical import canonical_digest, digest_bytes
from .capabilities import CapabilityContext
from .errors import GateBlockedError, ValidationError
from .local_pilot import preflight_local_pilot
from .service import RuntimeService

LIVE_DISPATCH_TYPES = {"research", "review", "experiment"}
APPENDER = Path(".claude/skills/register-dispatch/append-dispatch.cjs")
LEDGER = Path("telemetry/agents/subagents-dispatch.yaml")
POLICY_REF = "policy:local-orchestration-logging-bridge@1"
POLICY_DIGEST = canonical_digest(
    {
        "policy_ref": POLICY_REF,
        "authority_mode": "legacy-managed",
        "launch_requires": [
            "validated-yaml-opening",
            "current-session-link",
            "aci-orchestration-open-receipt",
        ],
    }
)


@dataclass(frozen=True)
class AppenderReceipt:
    operation: str
    dispatch_id: str
    stdout: str
    ledger_before_digest: str | None
    ledger_after_digest: str
    changed: bool


class LocalOrchestrationLoggingBridge:
    """Compose the legacy appender with ACI without changing either authority."""

    def __init__(
        self,
        *,
        runtime: RuntimeService,
        project_dir: Path,
        appender_path: Path | None = None,
        node_executable: str = "node",
        prepared_receipt: dict[str, Any] | None = None,
        failpoint: Callable[[str], None] | None = None,
    ) -> None:
        self.runtime = runtime
        self.project_dir = Path(project_dir).resolve()
        self.ledger_path = (self.project_dir / LEDGER).resolve()
        self.appender_path = (
            Path(appender_path).resolve()
            if appender_path
            else (self.project_dir / APPENDER).resolve()
        )
        self.node_executable = node_executable
        self.failpoint = failpoint or (lambda _: None)
        if self.runtime.settings.ledger_path.resolve() != self.ledger_path:
            raise GateBlockedError(
                "bridge project ledger must equal the configured runtime ledger"
            )
        if not self.appender_path.is_file():
            raise GateBlockedError("validated dispatch appender is unavailable")
        self._prepared_receipt = prepared_receipt

    def prepare(self) -> dict[str, Any]:
        if self._prepared_receipt is not None:
            return self._prepared_receipt
        opened = self.runtime.open()
        profiles = self.runtime.register_profiles()
        self._prepared_receipt = {"runtime": opened, "profiles": profiles}
        return self._prepared_receipt

    @staticmethod
    def _authority_values(
        authority: CapabilityContext,
        *,
        operation: str,
        record: dict[str, Any],
        session_name: str | None = None,
        origin_ref: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, str]:
        identity_field = "dispatch_id" if operation == "open" else "close_of"
        dispatch_id = record.get(identity_field)
        expected_action = f"orchestration.bridge.{operation}"
        expected_phase = "bootstrap" if operation == "open" else "finalize"
        required = {
            "operation",
            "dispatch_id",
            "record_digest",
            "authorization_evidence_ref",
            "authorization_evidence_digest",
            "nonce",
        }
        if operation == "open":
            required |= {"session_name", "origin_ref"}
        else:
            required.add("session_id")
        context = authority.context
        if (
            authority.action != expected_action
            or authority.phase != expected_phase
            or authority.expires_at is None
            or set(context) != required
            or context.get("operation") != operation
            or context.get("dispatch_id") != dispatch_id
            or context.get("record_digest") != canonical_digest(record)
            or not isinstance(context.get("nonce"), str)
            or not context["nonce"]
            or (
                operation == "open"
                and (
                    context.get("session_name") != session_name
                    or context.get("origin_ref") != origin_ref
                )
            )
            or (operation == "close" and context.get("session_id") != session_id)
        ):
            raise GateBlockedError("bridge capability scope is incomplete or mismatched")
        evidence_ref = context["authorization_evidence_ref"]
        evidence_digest = context["authorization_evidence_digest"]
        if not isinstance(evidence_ref, str) or not isinstance(evidence_digest, str):
            raise GateBlockedError("bridge capability evidence is malformed")
        return {
            "actor_ref": authority.principal_id,
            "authorization_evidence_ref": evidence_ref,
            "authorization_evidence_digest": evidence_digest,
        }

    def _append(self, record: dict[str, Any]) -> AppenderReceipt:
        if not isinstance(record, dict):
            raise ValidationError("dispatch appender record must be an object")
        is_close = "close_of" in record
        identity_field = "close_of" if is_close else "dispatch_id"
        dispatch_id = record.get(identity_field)
        if not isinstance(dispatch_id, str) or not dispatch_id:
            raise ValidationError(f"{identity_field} is required")
        if not is_close and record.get("dispatch_type") not in LIVE_DISPATCH_TYPES:
            raise GateBlockedError(
                "local bridge permits only live research, review, or experiment dispatches"
            )
        submitted = dict(record)
        submitted["project_dir"] = str(self.project_dir)
        before = self.ledger_path.read_bytes() if self.ledger_path.exists() else None
        temporary: Path | None = None
        completed: subprocess.CompletedProcess[str] | None = None
        try:
            descriptor = tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                suffix=".json",
                prefix=".orchestration-dispatch-",
                delete=False,
            )
            temporary = Path(descriptor.name)
            with descriptor:
                json.dump(
                    submitted,
                    descriptor,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                descriptor.write("\n")
            environment = {
                key: os.environ[key]
                for key in (
                    "PATH",
                    "PATHEXT",
                    "SystemRoot",
                    "WINDIR",
                    "COMSPEC",
                    "TEMP",
                    "TMP",
                    "USERPROFILE",
                )
                if key in os.environ
            }
            environment["CLAUDE_PROJECT_DIR"] = str(self.project_dir)
            try:
                completed = subprocess.run(
                    [
                        self.node_executable,
                        str(self.appender_path),
                        str(temporary),
                    ],
                    cwd=self.project_dir,
                    env=environment,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    capture_output=True,
                    check=False,
                    timeout=15,
                )
            except subprocess.TimeoutExpired as exc:
                raise GateBlockedError("validated dispatch appender timed out") from exc
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout).strip()
                raise GateBlockedError(
                    f"validated dispatch appender rejected the record: {detail}"
                )
        finally:
            if temporary and temporary.exists():
                temporary.unlink()
        after = self.ledger_path.read_bytes()
        snapshot = (
            self.runtime.legacy.resolve_close(self.ledger_path, dispatch_id)
            if is_close
            else self.runtime.legacy.resolve(self.ledger_path, dispatch_id)
        )
        expected = {
            key: value for key, value in submitted.items() if key != "project_dir"
        }
        for key, value in expected.items():
            if snapshot.row.get(key) != value:
                raise GateBlockedError(
                    f"existing YAML {snapshot.row_kind} differs at field {key}"
                )
        permitted_extra = {"created", "closed", "invoked_by"}
        extras = set(snapshot.row) - set(expected)
        if not extras.issubset(permitted_extra):
            raise GateBlockedError(
                "validated YAML row contains unexpected fields: "
                + ",".join(sorted(extras - permitted_extra))
            )
        assert completed is not None
        return AppenderReceipt(
            operation="close" if is_close else "open",
            dispatch_id=dispatch_id,
            stdout=completed.stdout.strip(),
            ledger_before_digest=digest_bytes(before) if before is not None else None,
            ledger_after_digest=digest_bytes(after),
            changed=before != after,
        )

    def open_dispatch(
        self,
        *,
        authority: CapabilityContext,
        record: dict[str, Any],
        session_name: str,
        origin_ref: str,
    ) -> dict[str, Any]:
        common = self._authority_values(
            authority,
            operation="open",
            record=record,
            session_name=session_name,
            origin_ref=origin_ref,
        )
        result = self._open_dispatch_authorized(
            record=record,
            session_name=session_name,
            origin_ref=origin_ref,
            **common,
        )
        self.runtime.capabilities.consume(authority.capability_id)
        return result

    def _open_dispatch_authorized(
        self,
        *,
        record: dict[str, Any],
        session_name: str,
        origin_ref: str,
        actor_ref: str,
        authorization_evidence_ref: str,
        authorization_evidence_digest: str,
    ) -> dict[str, Any]:
        """Return a launch receipt; callers must not launch before this succeeds."""
        self.prepare()
        origin_digest = canonical_digest({"origin_ref": origin_ref})
        session = self.runtime.ensure_session(
            origin_digest=origin_digest,
            name=session_name,
            actor_ref=actor_ref,
            actor_authentication_ref=authorization_evidence_ref,
            actor_authentication_digest=authorization_evidence_digest,
            idempotency_key="bridge-session",
        )
        dispatch_id = record.get("dispatch_id")
        if not isinstance(dispatch_id, str) or not dispatch_id:
            raise ValidationError("dispatch_id is required")
        appended = self._append(record)
        self.failpoint("after_yaml_open")
        session_id = session["session"]["session_id"]
        link = self.runtime.link_session_dispatch(
            session_id=session_id,
            dispatch_id=dispatch_id,
            actor_ref=actor_ref,
            authorization_policy_ref=POLICY_REF,
            authorization_policy_digest=POLICY_DIGEST,
            authorization_evidence_ref=authorization_evidence_ref,
            authorization_evidence_digest=authorization_evidence_digest,
            idempotency_key=f"bridge-link:{dispatch_id}",
        )
        self.failpoint("after_session_link")
        accepted = self.runtime.record_orchestration_dispatch_opened(
            session_id=session_id,
            dispatch_id=dispatch_id,
            actor_ref=actor_ref,
            authorization_evidence_ref=authorization_evidence_ref,
            authorization_evidence_digest=authorization_evidence_digest,
            idempotency_key=f"bridge-open:{dispatch_id}",
        )
        self.failpoint("after_open_accept")
        return {
            "status": "launch-authorized",
            "dispatch_id": dispatch_id,
            "session_id": session_id,
            "yaml": appended.__dict__,
            "session_receipt": session,
            "link_receipt": link,
            "orchestration_receipt": accepted,
        }

    def close_dispatch(
        self,
        *,
        authority: CapabilityContext,
        record: dict[str, Any],
        session_id: str,
    ) -> dict[str, Any]:
        common = self._authority_values(
            authority,
            operation="close",
            record=record,
            session_id=session_id,
        )
        result = self._close_dispatch_authorized(
            record=record,
            session_id=session_id,
            **common,
        )
        self.runtime.capabilities.consume(authority.capability_id)
        return result

    def _close_dispatch_authorized(
        self,
        *,
        record: dict[str, Any],
        session_id: str,
        actor_ref: str,
        authorization_evidence_ref: str,
        authorization_evidence_digest: str,
    ) -> dict[str, Any]:
        self.prepare()
        dispatch_id = record.get("close_of")
        if not isinstance(dispatch_id, str) or not dispatch_id:
            raise ValidationError("close_of is required")
        preflight = self.runtime.require_orchestration_dispatch_can_close(
            session_id=session_id,
            dispatch_id=dispatch_id,
            actor_ref=actor_ref,
            authorization_evidence_ref=authorization_evidence_ref,
            authorization_evidence_digest=authorization_evidence_digest,
        )
        appended = self._append(record)
        self.failpoint("after_yaml_close")
        accepted = self.runtime.record_orchestration_dispatch_closed(
            session_id=session_id,
            dispatch_id=dispatch_id,
            actor_ref=actor_ref,
            authorization_evidence_ref=authorization_evidence_ref,
            authorization_evidence_digest=authorization_evidence_digest,
            idempotency_key=f"bridge-close:{dispatch_id}",
        )
        self.failpoint("after_close_accept")
        return {
            "status": "closed",
            "dispatch_id": dispatch_id,
            "session_id": session_id,
            "preflight": preflight,
            "yaml": appended.__dict__,
            "orchestration_receipt": accepted,
        }


def _record(path: Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValidationError("record JSON must contain one object")
    return value


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="orchestration-bridge")
    result.add_argument("--project-dir", type=Path, required=True)
    result.add_argument("--database", type=Path, required=True)
    result.add_argument("--ledger", type=Path, required=True)
    commands = result.add_subparsers(dest="command", required=True)
    opening = commands.add_parser("open")
    opening.add_argument("--record", type=Path, required=True)
    opening.add_argument("--session-name", required=True)
    opening.add_argument("--origin-ref", required=True)
    closing = commands.add_parser("close")
    closing.add_argument("--record", type=Path, required=True)
    closing.add_argument("--session-id", required=True)
    return result


def run(argv: Sequence[str] | None = None) -> dict[str, Any]:
    args = parser().parse_args(argv)
    project_dir = args.project_dir.resolve()
    ledger = args.ledger.resolve()
    expected = (project_dir / LEDGER).resolve()
    if ledger != expected:
        raise GateBlockedError("bridge requires the project's exact dispatch ledger")
    runtime, preflight = preflight_local_pilot(
        repo_root=project_dir,
        database_path=args.database.resolve(),
        ledger_path=ledger,
        host="127.0.0.1",
        opted_in=os.environ.get("ACI_LOCAL_PILOT_ENABLED") == "1",
    )
    bridge = LocalOrchestrationLoggingBridge(
        runtime=runtime,
        project_dir=project_dir,
        prepared_receipt={"preflight": preflight},
    )
    token = os.environ.pop("ACI_ORCHESTRATION_BRIDGE_TOKEN", "")
    if not token:
        raise GateBlockedError("ACI_ORCHESTRATION_BRIDGE_TOKEN is required")
    record = _record(args.record)
    action = f"orchestration.bridge.{args.command}"
    phase = "bootstrap" if args.command == "open" else "finalize"
    authority = runtime.capabilities.resolve(token, action=action, phase=phase)
    if args.command == "open":
        return bridge.open_dispatch(
            authority=authority,
            record=record,
            session_name=args.session_name,
            origin_ref=args.origin_ref,
        )
    return bridge.close_dispatch(
        authority=authority,
        record=record,
        session_id=args.session_id,
    )


def main() -> None:
    print(json.dumps(run(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
