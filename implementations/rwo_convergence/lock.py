"""Race-aware selector expansion and source locking."""

from __future__ import annotations

import fnmatch
import hashlib
import os
import stat
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any

from .canonical import CanonicalizationError, TreeMember, tree_digest

LOCK_SCHEMA = "rwo.convergence-lock/v1"
FORBIDDEN_PARTS = {"__pycache__", "target"}
FORBIDDEN_COPY_SEGMENTS = {"staging", "rollback-baseline"}


class LockError(RuntimeError):
    """A selector or source member could not be locked safely."""


def normalize_relative_path(raw: str) -> str:
    if not isinstance(raw, str) or not raw:
        raise LockError("path must be a non-empty string")
    if "\\" in raw or "\0" in raw:
        raise LockError(f"unsafe path spelling: {raw!r}")
    path = PurePosixPath(raw)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise LockError(f"path must be normalized and repository-relative: {raw!r}")
    normalized = path.as_posix()
    if normalized != raw:
        raise LockError(f"path is not normalized: {raw!r}")
    return normalized


def _forbidden(path: str) -> bool:
    parts = PurePosixPath(path).parts
    if any(part in FORBIDDEN_PARTS for part in parts):
        return True
    for index, part in enumerate(parts):
        if part in FORBIDDEN_COPY_SEGMENTS and "projects" in parts[index + 1 :]:
            return True
    return False


def _check_component_chain(root: Path, relative: str) -> None:
    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError as exc:
            raise LockError(f"source member does not exist: {relative}") from exc
        if stat.S_ISLNK(info.st_mode):
            raise LockError(f"symbolic links are forbidden: {relative}")


def stable_read(root: Path | str, relative: str) -> tuple[bytes, os.stat_result]:
    """Read a regular member while detecting path swaps and in-place writes."""

    root_path = Path(root).resolve(strict=True)
    relative = normalize_relative_path(relative)
    if _forbidden(relative):
        raise LockError(f"hard-excluded source member: {relative}")
    _check_component_chain(root_path, relative)
    target = root_path.joinpath(*PurePosixPath(relative).parts)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(target, flags)
    except OSError as exc:
        raise LockError(f"cannot open source member safely: {relative}: {exc}") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise LockError(f"source member is not a regular file: {relative}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity = lambda item: (item.st_dev, item.st_ino, item.st_size, item.st_mtime_ns, item.st_ctime_ns)
    if identity(before) != identity(after):
        raise LockError(f"source changed while being read: {relative}")
    final = target.lstat()
    if identity(before) != identity(final) or stat.S_ISLNK(final.st_mode):
        raise LockError(f"source path changed while being read: {relative}")
    data = b"".join(chunks)
    if len(data) != before.st_size:
        raise LockError(f"short read: {relative}")
    return data, before


def _expand_one(root: Path, pattern: str) -> list[str]:
    pattern = normalize_relative_path(pattern)
    if _forbidden(pattern):
        raise LockError(f"hard-excluded selector: {pattern}")
    has_magic = any(char in pattern for char in "*?[")
    if has_magic:
        matches = []
        for candidate in root.glob(pattern):
            relative = candidate.relative_to(root).as_posix()
            if candidate.is_file() and not candidate.is_symlink() and not _forbidden(relative):
                matches.append(relative)
        if not matches:
            raise LockError(f"selector matched no regular files: {pattern}")
        return sorted(set(matches), key=lambda value: value.encode("utf-8"))
    target = root.joinpath(*PurePosixPath(pattern).parts)
    _check_component_chain(root, pattern)
    if target.is_file():
        return [pattern]
    if not target.is_dir():
        raise LockError(f"selector is neither a regular file nor directory: {pattern}")
    matches = []
    for candidate in target.rglob("*"):
        relative = candidate.relative_to(root).as_posix()
        if candidate.is_symlink():
            raise LockError(f"symbolic link below selected directory: {relative}")
        if candidate.is_file() and not _forbidden(relative):
            matches.append(relative)
        elif candidate.exists() and not candidate.is_dir() and not candidate.is_file():
            raise LockError(f"special member below selected directory: {relative}")
    if not matches:
        raise LockError(f"selected directory has no regular files: {pattern}")
    return sorted(matches, key=lambda value: value.encode("utf-8"))


def scope_selectors(scope_manifest: Mapping[str, Any]) -> list[dict[str, str]]:
    """Return the exact 45 named source selectors from the design scope."""

    selected: dict[str, dict[str, str]] = {}
    sources = scope_manifest.get("source_contracts")
    footprint = scope_manifest.get("target_footprint")
    if not isinstance(sources, list) or not isinstance(footprint, Mapping):
        raise LockError("invalid design scope manifest")
    rows = list(sources) + list(footprint.get("inclusions", []))
    for raw in rows:
        if not isinstance(raw, Mapping):
            raise LockError("scope selector must be an object")
        selector = raw.get("selector")
        path = raw.get("path")
        digest = raw.get("digest")
        if not all(isinstance(item, str) and item for item in (selector, path, digest)):
            raise LockError("scope selector is incomplete")
        normalize_relative_path(path)
        row = {"selector_id": selector, "path": path, "expected_sha256": digest}
        if selector in selected and selected[selector] != row:
            raise LockError(f"conflicting scope selector: {selector}")
        selected[selector] = row
    result = sorted(selected.values(), key=lambda row: row["selector_id"].encode("ascii"))
    if len(result) != 45:
        raise LockError(f"expected exactly 45 scope selectors, found {len(result)}")
    return result


def runner_dependency_patterns(source_closure: Mapping[str, Any]) -> list[dict[str, str]]:
    """Extract closed runner dependencies without treating them as new scope selectors."""

    groups = source_closure.get("runner_groups")
    if not isinstance(groups, list):
        raise LockError("runner source closure has no runner_groups")
    result: list[dict[str, str]] = []
    for group in groups:
        if not isinstance(group, Mapping) or not isinstance(group.get("axis_id"), str):
            raise LockError("invalid runner group")
        axis = group["axis_id"]
        values: list[str] = []
        for field in ("required_source_members", "required_source_roots"):
            raw = group.get(field, [])
            if not isinstance(raw, list) or any(not isinstance(item, str) for item in raw):
                raise LockError(f"{axis}.{field} must be a string array")
            values.extend(raw)
        for index, path in enumerate(values):
            result.append({"dependency_id": f"{axis}:{index:02d}", "path": normalize_relative_path(path)})
    return result


def build_lock(
    repository_root: Path | str,
    selectors: Sequence[Mapping[str, str]],
    *,
    dependency_patterns: Sequence[Mapping[str, str]] = (),
    lock_id: str = "RWO-CVG-001-lock",
) -> dict[str, Any]:
    root = Path(repository_root).resolve(strict=True)
    if not root.is_dir():
        raise LockError("repository root must be a directory")
    member_sources: dict[str, set[str]] = defaultdict(set)
    normalized_selectors: list[dict[str, str]] = []
    for raw in selectors:
        selector_id = raw.get("selector_id")
        path = raw.get("path")
        expected = raw.get("expected_sha256")
        if not isinstance(selector_id, str) or not selector_id.isascii() or not selector_id:
            raise LockError("selector_id must be non-empty ASCII")
        if not isinstance(path, str) or not isinstance(expected, str):
            raise LockError(f"selector {selector_id} is incomplete")
        members = _expand_one(root, path)
        if len(members) != 1 or members[0] != path:
            raise LockError(f"primary scope selector must resolve to its exact file: {selector_id}")
        data, _ = stable_read(root, path)
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            raise LockError(f"source digest mismatch for {selector_id}: expected {expected}, got {actual}")
        member_sources[path].add(f"scope:{selector_id}")
        normalized_selectors.append({"selector_id": selector_id, "path": path, "expected_sha256": expected})
    if len({row["selector_id"] for row in normalized_selectors}) != len(normalized_selectors):
        raise LockError("duplicate primary selector ID")

    normalized_dependencies: list[dict[str, str]] = []
    for raw in dependency_patterns:
        dependency_id = raw.get("dependency_id")
        pattern = raw.get("path")
        if not isinstance(dependency_id, str) or not dependency_id.isascii() or not isinstance(pattern, str):
            raise LockError("invalid runner dependency")
        matches = _expand_one(root, pattern)
        normalized_dependencies.append({"dependency_id": dependency_id, "path": pattern})
        for path in matches:
            member_sources[path].add(f"dependency:{dependency_id}")

    casefolded: dict[str, str] = {}
    members: list[dict[str, Any]] = []
    tree_members: list[TreeMember] = []
    for path in sorted(member_sources, key=lambda value: value.encode("utf-8")):
        folded = path.casefold()
        if folded in casefolded and casefolded[folded] != path:
            raise LockError(f"case-fold collision: {casefolded[folded]!r} and {path!r}")
        casefolded[folded] = path
        data, info = stable_read(root, path)
        digest = hashlib.sha256(data).hexdigest()
        row = {
            "path": path,
            "type": "file",
            "mode": f"{stat.S_IMODE(info.st_mode):04o}",
            "size_bytes": len(data),
            "sha256": digest,
            "sources": sorted(member_sources[path]),
        }
        members.append(row)
        tree_members.append(TreeMember(path, len(data), digest))
    return {
        "schema_version": LOCK_SCHEMA,
        "lock_id": lock_id,
        "catalog_bindings": [
            dict(row)
            for row in sorted(normalized_selectors, key=lambda item: item["selector_id"].encode("ascii"))
            if row["selector_id"] in {
                "design.axis-claim-catalog",
                "design.expectation-bindings",
                "design.runner-source-closure",
                "design.canonicalization",
            }
        ],
        "selector_count": len(normalized_selectors),
        "selectors": sorted(normalized_selectors, key=lambda row: row["selector_id"].encode("ascii")),
        "runner_dependencies": sorted(normalized_dependencies, key=lambda row: row["dependency_id"].encode("ascii")),
        "member_count": len(members),
        "members": members,
        "tree_sha256": tree_digest(tree_members),
        "execution_posture": {
            "source": "byte-exact-read-only-snapshot",
            "network": "forbidden",
            "shell": "forbidden",
            "unlisted_children": "forbidden",
        },
        "authority_effect": "none",
    }


def verify_lock(repository_root: Path | str, lock: Mapping[str, Any]) -> None:
    if lock.get("schema_version") != LOCK_SCHEMA or lock.get("authority_effect") != "none":
        raise LockError("invalid lock envelope")
    members = lock.get("members")
    catalog_bindings = lock.get("catalog_bindings")
    if not isinstance(catalog_bindings, list):
        raise LockError("lock has no catalog bindings")
    if lock.get("selector_count") == 45 and len(catalog_bindings) != 4:
        raise LockError("live lock must bind exactly four design catalogs")
    if not isinstance(members, list) or lock.get("member_count") != len(members):
        raise LockError("lock member count mismatch")
    observed: list[TreeMember] = []
    seen: set[str] = set()
    for raw in members:
        if not isinstance(raw, Mapping):
            raise LockError("lock member must be an object")
        path = raw.get("path")
        if not isinstance(path, str) or path in seen:
            raise LockError("invalid or duplicate lock member path")
        seen.add(path)
        data, info = stable_read(repository_root, path)
        digest = hashlib.sha256(data).hexdigest()
        if raw.get("type") != "file" or raw.get("size_bytes") != len(data) or raw.get("sha256") != digest:
            raise LockError(f"locked source drift: {path}")
        if raw.get("mode") != f"{stat.S_IMODE(info.st_mode):04o}":
            raise LockError(f"locked source mode drift: {path}")
        observed.append(TreeMember(path, len(data), digest))
    if tree_digest(observed) != lock.get("tree_sha256"):
        raise LockError("locked tree digest mismatch")
