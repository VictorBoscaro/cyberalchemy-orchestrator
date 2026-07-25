"""Host PostToolUse adapter for dispatch input-ingestion lineage."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from .canonical import canonical_digest, canonical_text
from .errors import GateBlockedError, ValidationError
from .host_dispatch_hook import HostDispatchHook, _find_string

EXACT_FILE_TOOLS = {"Read", "read_file", "view_image"}
SEARCH_TOOLS = {"Glob", "Grep", "search_files", "rg"}
WEB_TOOLS = {"WebFetch", "WebSearch", "web.run"}
MCP_TOOLS = {"read_mcp_resource"}
SHELL_TOOLS = {"Bash", "shell_command", "exec"}
SUPPORTED_TOOLS = (
    EXACT_FILE_TOOLS | SEARCH_TOOLS | WEB_TOOLS | MCP_TOOLS | SHELL_TOOLS
)


class HostIngestionHook:
    """Attribute observable host inputs to exactly one open wrapped dispatch."""

    def __init__(self, *, root: Path, host: str, now=None) -> None:
        self.dispatch_hook = HostDispatchHook(root=root, host=host, now=now)
        self.root = self.dispatch_hook.root
        self.host = host
        self.now = now or (lambda: datetime.now(timezone.utc))

    @staticmethod
    def _required_text(event: dict[str, Any], field: str) -> str:
        value = event.get(field)
        if not isinstance(value, str) or not value:
            raise GateBlockedError(f"ingestion hook input requires {field}")
        return value

    def _dispatch_state(self, event: dict[str, Any]) -> dict[str, Any] | None:
        host_session_id = self._required_text(event, "session_id")
        states = self.dispatch_hook._open_states(host_session_id)
        if not states:
            return None
        agent_id = event.get("agent_id") or _find_string(
            event.get("tool_response"), "agent_id"
        )
        if isinstance(agent_id, str) and agent_id:
            exact = [state for _, state in states if state.get("agent_id") == agent_id]
            if len(exact) == 1:
                return exact[0]
        if len(states) == 1:
            return states[0][1]
        raise GateBlockedError(
            "input ingestion cannot resolve exactly one open dispatch"
        )

    @staticmethod
    def _path_from_input(tool_input: dict[str, Any]) -> str | None:
        for key in ("file_path", "path", "filename"):
            value = tool_input.get(key)
            if isinstance(value, str) and value:
                return value
        return None

    def _classify(
        self, event: dict[str, Any]
    ) -> tuple[dict[str, Any], bytes | None]:
        tool_name = self._required_text(event, "tool_name")
        if tool_name not in SUPPORTED_TOOLS:
            raise GateBlockedError(f"unsupported ingestion tool: {tool_name}")
        tool_input = event.get("tool_input")
        if not isinstance(tool_input, dict):
            raise GateBlockedError("ingestion tool input must be an object")
        common = {
            "agent_id": (
                event.get("agent_id")
                if isinstance(event.get("agent_id"), str)
                else None
            ),
            "tool_name": tool_name,
            "purpose": "Input observed by the mandatory host lineage hook.",
            "observed_at": self.now().isoformat(),
        }
        if tool_name in EXACT_FILE_TOOLS:
            raw_path = self._path_from_input(tool_input)
            if not raw_path:
                raise GateBlockedError("file ingestion tool has no path")
            path = Path(raw_path)
            if not path.is_absolute():
                cwd = Path(self._required_text(event, "cwd"))
                path = cwd / path
            path = path.resolve()
            try:
                relative = path.relative_to(self.root).as_posix()
            except ValueError as exc:
                raise GateBlockedError(
                    "file ingestion outside repository is not authorized"
                ) from exc
            if not path.is_file():
                raise GateBlockedError("file ingestion target is not a regular file")
            body = path.read_bytes()
            return (
                {
                    **common,
                    "source_kind": "repository_file",
                    "locator": relative,
                    "repo_relative_path": relative,
                    "media_type": (
                        mimetypes.guess_type(path.name)[0]
                        or "application/octet-stream"
                    ),
                    "coverage": "exact",
                },
                body,
            )
        if tool_name in SEARCH_TOOLS:
            return (
                {
                    **common,
                    "source_kind": "repository_search",
                    "locator": "search:" + canonical_digest(tool_input),
                    "repo_relative_path": None,
                    "media_type": None,
                    "coverage": "metadata_only",
                    "purpose": (
                        "Repository search observed; result paths are not claimed as "
                        "individually ingested until an exact read occurs."
                    ),
                },
                None,
            )
        if tool_name in WEB_TOOLS:
            locator = next(
                (
                    tool_input[key]
                    for key in ("url", "query", "q")
                    if isinstance(tool_input.get(key), str)
                    and tool_input[key]
                ),
                "web:" + canonical_digest(tool_input),
            )
            return (
                {
                    **common,
                    "source_kind": "external_url",
                    "locator": locator,
                    "repo_relative_path": None,
                    "media_type": None,
                    "coverage": "metadata_only",
                    "purpose": (
                        "External acquisition locator observed; response bytes remain "
                        "host-managed unless explicitly captured as an artifact."
                    ),
                },
                None,
            )
        if tool_name in MCP_TOOLS:
            locator = next(
                (
                    tool_input[key]
                    for key in ("uri", "ref_id")
                    if isinstance(tool_input.get(key), str)
                    and tool_input[key]
                ),
                "mcp:" + canonical_digest(tool_input),
            )
            return (
                {
                    **common,
                    "source_kind": "mcp_resource",
                    "locator": locator,
                    "repo_relative_path": None,
                    "media_type": None,
                    "coverage": "metadata_only",
                },
                None,
            )
        return (
            {
                **common,
                "source_kind": "shell_opaque",
                "locator": "shell:" + canonical_digest(tool_input),
                "repo_relative_path": None,
                "media_type": None,
                "coverage": "opaque",
                "purpose": (
                    "Shell execution may access files internally; exact file lineage "
                    "is unavailable unless the files are read through an instrumented tool."
                ),
            },
            None,
        )

    def post_tool_use(self, event: dict[str, Any]) -> dict[str, Any] | None:
        state = self._dispatch_state(event)
        if state is None:
            return None
        classified, content = self._classify(event)
        intent = {
            "agent_id": classified["agent_id"] or state.get("agent_id"),
            "tool_use_id": self._required_text(event, "tool_use_id"),
            "tool_name": classified["tool_name"],
            "source_kind": classified["source_kind"],
            "locator": classified["locator"],
            "repo_relative_path": classified["repo_relative_path"],
            "media_type": classified["media_type"],
            "coverage": classified["coverage"],
            "purpose": classified["purpose"],
            "observed_at": classified["observed_at"],
        }
        runtime, _ = self.dispatch_hook._runtime_bridge()
        issued = runtime.issue_capability(
            principal_id=self.dispatch_hook.policy["principal_id"],
            action="ingestion.record",
            phase="observe",
            context={
                "session_id": state["session_id"],
                "dispatch_id": state["dispatch_id"],
                "host": self.host,
                "tool_use_id": intent["tool_use_id"],
                "intent_digest": canonical_digest(intent),
            },
            expires_at=None,
        )
        return runtime.record_dispatch_ingestion(
            token=issued["token"], intent=intent, content=content
        )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="host-ingestion-hook")
    result.add_argument("--host", choices=("claude", "codex"), required=True)
    return result


def run(
    argv: Sequence[str] | None = None, *, stdin: str | None = None
) -> tuple[int, dict[str, Any] | None]:
    args = parser().parse_args(argv)
    raw = sys.stdin.read() if stdin is None else stdin
    try:
        event = json.loads(raw)
        if not isinstance(event, dict):
            raise ValidationError("hook input must be one JSON object")
        if event.get("hook_event_name") != "PostToolUse":
            raise GateBlockedError("ingestion hook accepts only PostToolUse")
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
        result = HostIngestionHook(root=root, host=args.host).post_tool_use(event)
        return 0, None if result is not None else None
    except Exception as exc:
        return 0, {
            "systemMessage": (
                f"Mandatory {args.host} input-lineage recording failed: {exc}"
            )
        }


def main() -> None:
    code, output = run()
    if output is not None:
        print(json.dumps(output, ensure_ascii=False, separators=(",", ":")))
    raise SystemExit(code)


if __name__ == "__main__":
    main()
