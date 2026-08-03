from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OUTPUT = REPO / "implementations" / "as-built" / "source-manifest-current.json"

ROOTS = (
    REPO / "implementations",
    REPO / ".codex" / "hooks.json",
    REPO / ".claude" / "settings.json",
    REPO / ".claude" / "hooks",
    REPO / "telemetry" / "agents" / "subagents-dispatch.yaml",
    REPO / "docs" / "decisions",
    REPO / "docs" / "features" / "agents-communication-infra",
    REPO / "docs" / "features" / "agent-provenance-telemetry",
    REPO / "docs" / "features" / "skill-control-center",
    REPO / "plans" / "governed-agent-work-infrastructure" / "PLAN.md",
    REPO / "plans" / "governed-agent-work-infrastructure" / "workstreams",
)

EXCLUDED_PARTS = {
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "screenshots",
    "as-built",
}
EXCLUDED_SUFFIXES = {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".sqlite3", ".log"}


def candidates(root: Path):
    if root.is_file():
        yield root
        return
    if not root.exists():
        return
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = set(path.relative_to(REPO).parts)
        if relative_parts & EXCLUDED_PARTS:
            continue
        if path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        yield path


files: dict[str, str] = {}
for root in ROOTS:
    for path in candidates(root):
        relative = path.relative_to(REPO).as_posix()
        files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()

payload = {
    "schema": "cyberalchemy.as-built-source-manifest/v2",
    "snapshot_commit": "63777abd838995c8512bcea806546c3f2ab6add6",
    "scope_note": "Current code-first AS-BUILT corpus after observed mid-investigation source drift; the original frozen manifest remains source-manifest.json. Generated outputs, screenshots, caches, logs and databases are excluded.",
    "files": dict(sorted(files.items())),
}
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
