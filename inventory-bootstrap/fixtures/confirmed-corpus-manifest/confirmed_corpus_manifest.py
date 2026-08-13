#!/usr/bin/env python3
"""Materialize and verify the D1 ConfirmedCorpusManifest without mutating sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence

SCHEMA_VERSION = "confirmed-corpus-manifest@1"
PROJECTION_SCHEMA_VERSION = "d1-lens-use-corpus-manifest@1"
SEMANTIC_AUTHORITY = Path(
    "internal-tools/composition-lab/orchestration/milestone-1-strategy/"
    "d1-readiness/runtime-blocker/inventory-bootstrap/04-execution-sheet.md"
)
EXTERNAL_ROW_SOURCE = Path(
    "internal-tools/composition-lab/orchestration/milestone-1-strategy/"
    "d1-readiness/record/d1-dispatch-sheet.md"
)
EXPECTED_SEMANTIC_AUTHORITY_HASH = (
    "2be8ed0276ea55d830907aad0f423db8b4b44f181134092aa44071163c6d4f07"
)
EXPECTED_SEMANTIC_AUTHORITY_SIZE = 26176
EXPECTED_EXTERNAL_HASH = (
    "51e442ee7ccdc15122ee607d2fd3ac2ba8eae9d116ab8db695672d29bae2151e"
)
EXPECTED_EXTERNAL_SIZE = 13063
EXPECTED_REVISION = "6f9d7d860a3e3dd3c6e702fbb1117a3741b22930"

TABLE_ROW = re.compile(
    r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*(entire-file)\s*\|\s*`([0-9a-f]{64})`\s*\|$"
)
EXTERNAL_ROW = re.compile(r"^([0-9a-f]{64})  (.+)$")
CONTROL_LINE = re.compile(r"`(C[1-8])`\s*([^;]+?)(?:;|\.)")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class ManifestError(ValueError):
    """A closed-surface contract or equivalence failure."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _identity(root: Path, relative: Path, revision: str) -> dict[str, Any]:
    path = root / relative
    if not path.is_file():
        raise ManifestError(f"BLOCK/source-missing:{relative.as_posix()}")
    return {
        "path": relative.as_posix(),
        "sha256": _sha256(path),
        "size": path.stat().st_size,
        "revision": revision,
    }


def _assert_identity(
    identity: dict[str, Any], expected_hash: str, expected_size: int
) -> None:
    if identity["sha256"] != expected_hash or identity["size"] != expected_size:
        raise ManifestError("BLOCK/FREEZE_AUTHORITY_DIVERGENCE")


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ManifestError(f"BLOCK/non-utf8-source:{path.as_posix()}") from error


def parse_frozen_table(text: str) -> list[dict[str, Any]]:
    section = _section(text, "## Proposed frozen corpus manifest", "## Exact write set and ownership")
    rows: list[dict[str, Any]] = []
    for line in section.splitlines():
        match = TABLE_ROW.match(line)
        if match:
            ordinal, path, selector, sha256 = match.groups()
            rows.append(
                {
                    "ordinal": int(ordinal),
                    "path": path,
                    "selector": selector,
                    "sha256": sha256,
                }
            )
    if len(rows) != 22 or [row["ordinal"] for row in rows] != list(range(1, 23)):
        raise ManifestError("BLOCK/corpus-cardinality-or-order")
    if any(row["selector"] != "entire-file" for row in rows):
        raise ManifestError("BLOCK/selector-divergence")
    return rows


def parse_external_rows(text: str) -> list[dict[str, str]]:
    rows = [
        {"path": match.group(2), "sha256": match.group(1)}
        for line in text.splitlines()
        if (match := EXTERNAL_ROW.match(line))
    ]
    if len(rows) != 22:
        raise ManifestError("BLOCK/external-corpus-cardinality")
    return rows


def parse_controls(text: str) -> list[dict[str, str]]:
    section = _section(text, "## Proposed frozen corpus manifest", "## Exact write set and ownership")
    controls: list[dict[str, str]] = []
    for match in CONTROL_LINE.finditer(section.replace("\n", " ")):
        control_id, description = match.groups()
        controls.append({"id": control_id, "description": " ".join(description.split())})
    if [control["id"] for control in controls] != [f"C{i}" for i in range(1, 9)]:
        raise ManifestError("BLOCK/control-cardinality-or-order")
    return controls


def _section(text: str, start_heading: str, end_heading: str) -> str:
    start = text.find(start_heading)
    end = text.find(end_heading, start + len(start_heading))
    if start < 0 or end < 0:
        raise ManifestError("BLOCK/frozen-section-missing")
    return text[start:end]


def repository_revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    revision = result.stdout.strip().lower()
    if not HEX40.fullmatch(revision):
        raise ManifestError("BLOCK/invalid-repository-revision")
    return revision


def normalize_manifest_path(root: Path, value: str) -> str:
    candidate = Path(value)
    resolved = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    try:
        return resolved.relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise ManifestError("BLOCK/manifest-path-outside-repository") from error


def materialize(root: Path, manifest_path: str, revision: str | None = None) -> dict[str, Any]:
    revision = revision or repository_revision(root)
    if revision != EXPECTED_REVISION:
        raise ManifestError("BLOCK/repository-revision-drift")

    authority = _identity(root, SEMANTIC_AUTHORITY, revision)
    external = _identity(root, EXTERNAL_ROW_SOURCE, revision)
    _assert_identity(authority, EXPECTED_SEMANTIC_AUTHORITY_HASH, EXPECTED_SEMANTIC_AUTHORITY_SIZE)
    _assert_identity(external, EXPECTED_EXTERNAL_HASH, EXPECTED_EXTERNAL_SIZE)

    authority_text = _read_text(root / SEMANTIC_AUTHORITY)
    table_rows = parse_frozen_table(authority_text)
    external_rows = parse_external_rows(_read_text(root / EXTERNAL_ROW_SOURCE))
    if [
        {"path": row["path"], "sha256": row["sha256"]} for row in table_rows
    ] != external_rows:
        raise ManifestError("BLOCK/FREEZE_AUTHORITY_DIVERGENCE")

    sources: list[dict[str, Any]] = []
    for expected in table_rows:
        actual = _identity(root, Path(expected["path"]), revision)
        if actual["sha256"] != expected["sha256"]:
            raise ManifestError(f"BLOCK/source-drift:{expected['path']}")
        sources.append({"ordinal": expected["ordinal"], "selector": expected["selector"], **actual})

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "confirmed_manifest_path": normalize_manifest_path(root, manifest_path),
        "repository_revision": revision,
        "semantic_authority": authority,
        "external_row_source": external,
        "sources": sources,
        "controls": parse_controls(authority_text),
    }
    validate_shape(manifest)
    return manifest


def validate_shape(manifest: Any) -> None:
    top_keys = {
        "schema_version",
        "confirmed_manifest_path",
        "repository_revision",
        "semantic_authority",
        "external_row_source",
        "sources",
        "controls",
    }
    if not isinstance(manifest, dict) or set(manifest) != top_keys:
        raise ManifestError("BLOCK/manifest-shape")
    if manifest["schema_version"] != SCHEMA_VERSION:
        raise ManifestError("BLOCK/manifest-schema-version")
    if not isinstance(manifest["confirmed_manifest_path"], str) or not manifest["confirmed_manifest_path"]:
        raise ManifestError("BLOCK/manifest-path")
    if not HEX40.fullmatch(manifest.get("repository_revision", "")):
        raise ManifestError("BLOCK/manifest-revision")

    identity_keys = {"path", "sha256", "size", "revision"}
    for name in ("semantic_authority", "external_row_source"):
        value = manifest[name]
        if not isinstance(value, dict) or set(value) != identity_keys:
            raise ManifestError(f"BLOCK/{name}-shape")
        if not HEX64.fullmatch(value.get("sha256", "")) or not isinstance(value.get("size"), int):
            raise ManifestError(f"BLOCK/{name}-identity")
        if value.get("revision") != manifest["repository_revision"]:
            raise ManifestError(f"BLOCK/{name}-revision")

    sources = manifest["sources"]
    if not isinstance(sources, list) or len(sources) != 22:
        raise ManifestError("BLOCK/manifest-source-cardinality")
    source_keys = {"ordinal", "path", "selector", "sha256", "size", "revision"}
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict) or set(source) != source_keys:
            raise ManifestError("BLOCK/manifest-source-shape")
        if source["ordinal"] != index or source["selector"] != "entire-file":
            raise ManifestError("BLOCK/manifest-source-order-or-selector")
        if not HEX64.fullmatch(source.get("sha256", "")) or not isinstance(source.get("size"), int):
            raise ManifestError("BLOCK/manifest-source-identity")
        if source.get("revision") != manifest["repository_revision"]:
            raise ManifestError("BLOCK/manifest-source-revision")

    controls = manifest["controls"]
    if not isinstance(controls, list) or len(controls) != 8:
        raise ManifestError("BLOCK/manifest-control-cardinality")
    if [control.get("id") for control in controls if isinstance(control, dict)] != [f"C{i}" for i in range(1, 9)]:
        raise ManifestError("BLOCK/manifest-control-order")
    if any(set(control) != {"id", "description"} or not control["description"] for control in controls):
        raise ManifestError("BLOCK/manifest-control-shape")


def verify(manifest: dict[str, Any], root: Path, manifest_path: Path) -> None:
    validate_shape(manifest)
    actual_path = normalize_manifest_path(root, str(manifest_path))
    if actual_path != manifest["confirmed_manifest_path"]:
        raise ManifestError("BLOCK/CONFIRMED_MANIFEST_PATH_DIVERGENCE")
    expected = materialize(root, manifest["confirmed_manifest_path"])
    if manifest != expected:
        raise ManifestError("BLOCK/CONFIRMED_CORPUS_MANIFEST_DIVERGENCE")


def load_and_verify_manifest(path: Path, root: Path) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
        manifest = json.loads(raw.decode("utf-8"))
    except UnicodeDecodeError as error:
        raise ManifestError("BLOCK/non-utf8-manifest") from error
    if raw != canonical_json(manifest).encode("utf-8"):
        raise ManifestError("BLOCK/NON_CANONICAL_MANIFEST_SERIALIZATION")
    verify(manifest, root, path)
    return manifest


def project_inventory_manifest(
    manifest: dict[str, Any], manifest_path: Path, root: Path
) -> dict[str, Any]:
    verify(manifest, root, manifest_path)
    manifest_bytes = canonical_json(manifest).encode("utf-8")
    return {
        "schema_version": PROJECTION_SCHEMA_VERSION,
        "source_manifest": {
            "path": manifest["confirmed_manifest_path"],
            "sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "size": len(manifest_bytes),
            "revision": manifest["repository_revision"],
        },
        "repository_revision": manifest["repository_revision"],
        "sources": copy_json(manifest["sources"]),
        "controls": copy_json(manifest["controls"]),
        "denominator": {"source_count": 22, "control_count": 8, "cell_count": 176},
    }


def copy_json(value: Any) -> Any:
    """Copy JSON-compatible data without sharing mutable manifest objects."""
    return json.loads(json.dumps(value))


def validate_projection_shape(projection: Any) -> None:
    keys = {
        "schema_version",
        "source_manifest",
        "repository_revision",
        "sources",
        "controls",
        "denominator",
    }
    if not isinstance(projection, dict) or set(projection) != keys:
        raise ManifestError("BLOCK/inventory-projection-shape")
    if projection.get("schema_version") != PROJECTION_SCHEMA_VERSION:
        raise ManifestError("BLOCK/inventory-projection-schema-version")
    source_manifest = projection.get("source_manifest")
    if not isinstance(source_manifest, dict) or set(source_manifest) != {
        "path", "sha256", "size", "revision"
    }:
        raise ManifestError("BLOCK/inventory-projection-source-manifest")
    denominator = projection.get("denominator")
    if denominator != {"source_count": 22, "control_count": 8, "cell_count": 176}:
        raise ManifestError("BLOCK/inventory-projection-denominator")
    if not isinstance(projection.get("sources"), list) or len(projection["sources"]) != 22:
        raise ManifestError("BLOCK/inventory-projection-sources")
    if not isinstance(projection.get("controls"), list) or len(projection["controls"]) != 8:
        raise ManifestError("BLOCK/inventory-projection-controls")


def verify_inventory_projection(
    manifest: dict[str, Any], manifest_path: Path, projection: Any, root: Path
) -> None:
    validate_projection_shape(projection)
    expected = project_inventory_manifest(manifest, manifest_path, root)
    if projection != expected:
        raise ManifestError("BLOCK/INVENTORY_PROJECTION_DIVERGENCE")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)
    materialize_parser = subparsers.add_parser("materialize")
    materialize_parser.add_argument("--manifest-path", required=True)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("manifest", type=Path)
    project_parser = subparsers.add_parser("project-inventory")
    project_parser.add_argument("manifest", type=Path)
    verify_projection_parser = subparsers.add_parser("verify-inventory-projection")
    verify_projection_parser.add_argument("manifest", type=Path)
    verify_projection_parser.add_argument("projection", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "materialize":
            sys.stdout.write(canonical_json(materialize(args.repo_root.resolve(), args.manifest_path)))
        elif args.command == "verify":
            manifest = load_and_verify_manifest(args.manifest.resolve(), args.repo_root.resolve())
            sys.stdout.write("CONFIRMED_CORPUS_MANIFEST_VERIFIED\n")
        elif args.command == "project-inventory":
            manifest_path = args.manifest.resolve()
            manifest = load_and_verify_manifest(manifest_path, args.repo_root.resolve())
            projection = project_inventory_manifest(manifest, manifest_path, args.repo_root.resolve())
            sys.stdout.write(canonical_json(projection))
        else:
            manifest_path = args.manifest.resolve()
            manifest = load_and_verify_manifest(manifest_path, args.repo_root.resolve())
            with args.projection.open("r", encoding="utf-8") as stream:
                projection = json.load(stream)
            verify_inventory_projection(manifest, manifest_path, projection, args.repo_root.resolve())
            sys.stdout.write("INVENTORY_PROJECTION_VERIFIED\n")
    except (ManifestError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        sys.stderr.write(f"{error}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
