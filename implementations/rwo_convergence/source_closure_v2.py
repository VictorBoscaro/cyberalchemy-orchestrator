"""Deterministic source-closure v2 derivation for RWO-CVG-002.

This module is intentionally source-only.  It reads regular files through the
existing race-aware lock primitives, parses Python syntax, and computes hashes.
It never resolves or executes a product tool, child process, runner, or network
operation.
"""

from __future__ import annotations

import ast
import hashlib
import stat
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any

from .canonical import TreeMember, tree_digest
from .lock import LockError, normalize_relative_path, stable_read


CLOSURE_SCHEMA = "rwo.runner-source-closure/v2"
DELTA_SCHEMA = "rwo.runner-source-snapshot-delta/v1"
GROUP_ORDER = (
    "AX-PYTHON",
    "AX-RUST",
    "AX-CROSS-LANGUAGE",
    "AX-GO",
    "AX-SHARED-DISPATCH",
)
FORBIDDEN_COMPARATOR_MODULES = {
    "asyncio.subprocess",
    "importlib",
    "multiprocessing",
    "subprocess",
}
FORBIDDEN_LOCAL_COMPARATOR_MODULES = {
    "cli",
    "descriptors",
    "integration",
    "process",
    "publisher",
    "runners",
    "supervisor",
}
FORBIDDEN_DYNAMIC_CALLS = {"__import__", "compile", "eval", "exec"}
FORBIDDEN_OS_CALLS = {
    "execl",
    "execle",
    "execlp",
    "execlpe",
    "execv",
    "execve",
    "execvp",
    "execvpe",
    "popen",
    "posix_spawn",
    "posix_spawnp",
    "spawnl",
    "spawnle",
    "spawnlp",
    "spawnlpe",
    "spawnv",
    "spawnve",
    "spawnvp",
    "spawnvpe",
    "system",
}


class SourceClosureError(RuntimeError):
    """The candidate cannot satisfy the closed source contract."""


def _sort_paths(values: Sequence[str] | set[str]) -> list[str]:
    return sorted(values, key=lambda value: value.encode("utf-8"))


def _path(value: Any, *, label: str) -> str:
    if not isinstance(value, str):
        raise SourceClosureError(f"{label} must be a string")
    try:
        return normalize_relative_path(value)
    except LockError as exc:
        raise SourceClosureError(f"{label}: {exc}") from exc


def _mapping(value: Any, *, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise SourceClosureError(f"{label} must be an object")
    return value


def _string_list(value: Any, *, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise SourceClosureError(f"{label} must be a string array")
    paths = [_path(item, label=f"{label} member") for item in value]
    if len(paths) != len(set(paths)):
        raise SourceClosureError(f"{label} contains duplicate members")
    return paths


def _group(design: Mapping[str, Any], group_id: str) -> Mapping[str, Any]:
    groups = design.get("groups")
    if not isinstance(groups, list):
        raise SourceClosureError("successor design has no groups")
    matches = [
        item
        for item in groups
        if isinstance(item, Mapping) and item.get("group_id") == group_id
    ]
    if len(matches) != 1:
        raise SourceClosureError(f"successor design must contain one {group_id} group")
    return matches[0]


def _profile_runner(profile: Mapping[str, Any], runner_id: str) -> Mapping[str, Any]:
    runners = profile.get("runners")
    if not isinstance(runners, list):
        raise SourceClosureError("runner profile has no runners")
    matches = [
        item
        for item in runners
        if isinstance(item, Mapping) and item.get("runner_id") == runner_id
    ]
    if len(matches) != 1:
        raise SourceClosureError(f"runner profile must contain one {runner_id}")
    return matches[0]


def _prior_group(prior: Mapping[str, Any], axis_id: str) -> Mapping[str, Any]:
    groups = prior.get("runner_groups")
    if not isinstance(groups, list):
        raise SourceClosureError("prior closure has no runner_groups")
    matches = [
        item
        for item in groups
        if isinstance(item, Mapping) and item.get("axis_id") == axis_id
    ]
    if len(matches) != 1:
        raise SourceClosureError(f"prior closure must contain one {axis_id} group")
    return matches[0]


def _walk_regular_files(root: Path, relative_root: str) -> list[str]:
    relative_root = _path(relative_root, label="source root")
    target = root.joinpath(*PurePosixPath(relative_root).parts)
    try:
        info = target.lstat()
    except FileNotFoundError as exc:
        raise SourceClosureError(f"source root does not exist: {relative_root}") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise SourceClosureError(f"source root is not a real directory: {relative_root}")
    paths: list[str] = []
    for candidate in target.rglob("*"):
        relative = candidate.relative_to(root).as_posix()
        info = candidate.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise SourceClosureError(f"symbolic link in source root: {relative}")
        if stat.S_ISREG(info.st_mode):
            paths.append(_path(relative, label="expanded source member"))
        elif not stat.S_ISDIR(info.st_mode):
            raise SourceClosureError(f"special file in source root: {relative}")
    return _sort_paths(paths)


def _all_snapshot_members(root: Path) -> list[str]:
    members: list[str] = []
    for candidate in root.rglob("*"):
        relative = candidate.relative_to(root).as_posix()
        info = candidate.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise SourceClosureError(f"symbolic link in accepted snapshot: {relative}")
        if stat.S_ISREG(info.st_mode):
            members.append(_path(relative, label="accepted snapshot member"))
        elif not stat.S_ISDIR(info.st_mode):
            raise SourceClosureError(f"special file in accepted snapshot: {relative}")
    return _sort_paths(members)


def _member(root: Path, path: str) -> dict[str, Any]:
    try:
        data, info = stable_read(root, path)
    except LockError as exc:
        raise SourceClosureError(str(exc)) from exc
    return {
        "path": path,
        "type": "file",
        "mode": f"{stat.S_IMODE(info.st_mode):04o}",
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def _tree(rows: Sequence[Mapping[str, Any]]) -> str:
    return tree_digest(
        TreeMember(row["path"], row["size_bytes"], row["sha256"])
        for row in rows
    )


def _local_import_target(package: str, level: int, module: str | None) -> str | None:
    parts = package.split(".")
    if level:
        if level > len(parts):
            raise SourceClosureError("comparator relative import escapes its package")
        prefix = parts[: len(parts) - level + 1]
    else:
        prefix = []
    suffix = module.split(".") if module else []
    target = ".".join(prefix + suffix)
    local_prefix = "implementations.rwo_convergence"
    if target == local_prefix or target.startswith(local_prefix + "."):
        return target
    return None


def _module_path(module: str) -> str:
    return module.replace(".", "/") + ".py"


def _attribute_name(node: ast.AST) -> str | None:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return ".".join(reversed(parts))
    return None


def _audit_python_module(data: bytes, path: str) -> tuple[set[str], list[str]]:
    try:
        tree = ast.parse(data.decode("utf-8", "strict"), filename=path)
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise SourceClosureError(f"cannot parse comparator closure member {path}: {exc}") from exc
    package = path.removesuffix(".py").replace("/", ".").rsplit(".", 1)[0]
    local: set[str] = set()
    findings: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if any(
                    alias.name == forbidden or alias.name.startswith(forbidden + ".")
                    for forbidden in FORBIDDEN_COMPARATOR_MODULES
                ):
                    raise SourceClosureError(
                        f"forbidden comparator capability import {alias.name!r} in {path}"
                    )
                target = _local_import_target(package, 0, alias.name)
                if target:
                    local.add(target)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if any(
                module == forbidden or module.startswith(forbidden + ".")
                for forbidden in FORBIDDEN_COMPARATOR_MODULES
            ):
                raise SourceClosureError(
                    f"forbidden comparator capability import {module!r} in {path}"
                )
            target = _local_import_target(package, node.level, node.module)
            if target:
                local.add(target)
        elif isinstance(node, ast.Call):
            called = _attribute_name(node.func)
            if called in FORBIDDEN_DYNAMIC_CALLS:
                raise SourceClosureError(f"forbidden dynamic call {called!r} in {path}")
            if called and called.startswith("os.") and called.split(".")[-1] in FORBIDDEN_OS_CALLS:
                raise SourceClosureError(f"forbidden process call {called!r} in {path}")
    for target in sorted(local):
        leaf = target.rsplit(".", 1)[-1]
        if leaf in FORBIDDEN_LOCAL_COMPARATOR_MODULES:
            raise SourceClosureError(
                f"forbidden runner-launcher dependency {target!r} in {path}"
            )
        findings.append(target)
    return local, findings


def comparator_source_closure(
    repository_root: Path | str,
    entry: str = "implementations/rwo_convergence/comparator.py",
) -> tuple[list[str], dict[str, Any]]:
    """Return the transitive local-import closure and a no-launch audit."""

    root = Path(repository_root).resolve(strict=True)
    entry = _path(entry, label="comparator entry")
    pending = [entry.removesuffix(".py").replace("/", ".")]
    seen_modules: set[str] = set()
    edges: list[dict[str, str]] = []
    while pending:
        module = pending.pop()
        if module in seen_modules:
            continue
        seen_modules.add(module)
        path = _module_path(module)
        try:
            data, _ = stable_read(root, path)
        except LockError as exc:
            raise SourceClosureError(str(exc)) from exc
        local, _ = _audit_python_module(data, path)
        for target in sorted(local):
            edges.append({"from": path, "to": _module_path(target)})
            if target not in seen_modules:
                pending.append(target)
    members = _sort_paths({_module_path(module) for module in seen_modules})
    return members, {
        "entry": entry,
        "transitive_local_imports": sorted(
            edges, key=lambda row: (row["from"].encode(), row["to"].encode())
        ),
        "forbidden_capabilities": [
            "dynamic import",
            "process execution",
            "runner-launcher import",
            "subprocess import",
        ],
        "verdict": "source-audit-pass",
        "execution_attempted": False,
    }


def _resolved_groups(
    root: Path,
    successor_design: Mapping[str, Any],
    current_profile: Mapping[str, Any],
    prior_closure: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, set[str]]]:
    if successor_design.get("schema_version") != "rwo.runner-source-closure-design/v2":
        raise SourceClosureError("unsupported successor source-closure design")
    if current_profile.get("schema_version") != "rwo.runner-profile/v1":
        raise SourceClosureError("unsupported current runner profile")
    if prior_closure.get("schema_version") != "rwo.runner-source-closure/v1":
        raise SourceClosureError("unsupported prior source closure")

    path_groups: dict[str, set[str]] = defaultdict(set)
    output: list[dict[str, Any]] = []

    python_design = _group(successor_design, "AX-PYTHON")
    python_members = _string_list(python_design.get("members"), label="AX-PYTHON members")
    if python_design.get("member_count") != 26 or len(python_members) != 26:
        raise SourceClosureError("AX-PYTHON must contain the exact 26-member union")
    profile_python = _profile_runner(current_profile, "RUN-PYTHON-REFERENCE")
    profile_python_members = set(
        _string_list(profile_python.get("source_members"), label="Python profile members")
    )
    if not profile_python_members.issubset(set(python_members)):
        raise SourceClosureError("AX-PYTHON design does not contain the current profile")
    output.append(
        {
            "group_id": "AX-PYTHON",
            "member_count": len(python_members),
            "members": _sort_paths(python_members),
            "rationale": "exact 26-member successor union",
        }
    )
    for path in python_members:
        path_groups[path].add("AX-PYTHON")

    rust_design = _group(successor_design, "AX-RUST")
    expected_expansion = [
        "implementations/rwo-rust/Cargo.toml",
        "implementations/rwo-rust/Cargo.lock",
        "implementations/rwo-rust/src/**",
    ]
    if rust_design.get("expansion") != expected_expansion:
        raise SourceClosureError("AX-RUST expansion contract changed")
    rust_members = expected_expansion[:2] + _walk_regular_files(
        root, "implementations/rwo-rust/src"
    )
    rust_members = _sort_paths(set(rust_members))
    output.append(
        {
            "group_id": "AX-RUST",
            "member_count": len(rust_members),
            "members": rust_members,
            "rationale": "Cargo manifests plus recursive exact src member expansion",
        }
    )
    for path in rust_members:
        path_groups[path].add("AX-RUST")

    comparator_design = _group(successor_design, "AX-CROSS-LANGUAGE")
    required = comparator_design.get("required_members")
    if required != ["implementations/rwo_convergence/comparator.py"]:
        raise SourceClosureError("AX-CROSS-LANGUAGE comparator entry changed")
    comparator_members, comparator_audit = comparator_source_closure(root, required[0])
    output.append(
        {
            "group_id": "AX-CROSS-LANGUAGE",
            "member_count": len(comparator_members),
            "members": comparator_members,
            "rationale": "transitive local-import closure of the pure comparator",
            "comparator_capability_audit": comparator_audit,
        }
    )
    for path in comparator_members:
        path_groups[path].add("AX-CROSS-LANGUAGE")

    go_design = _group(successor_design, "AX-GO")
    go_base = "implementations/rwo-sidecar-go"
    go_members = {
        f"{go_base}/go.mod",
        f"{go_base}/go.sum",
    }
    for path in _walk_regular_files(root, go_base):
        relative = PurePosixPath(path).relative_to(go_base)
        if path.endswith(".go") or (relative.parts and relative.parts[0] == "testdata"):
            go_members.add(path)
    required_main = f"{go_base}/cmd/rwo-local-runtime/main.go"
    if required_main not in go_members:
        raise SourceClosureError("AX-GO is missing cmd/rwo-local-runtime/main.go")
    go_members_ordered = _sort_paths(go_members)
    output.append(
        {
            "group_id": "AX-GO",
            "member_count": len(go_members_ordered),
            "members": go_members_ordered,
            "rationale": "go.mod/go.sum, every current .go file, and recursive testdata members",
            "child_executable_disposition": {
                "status": "excluded-runtime-input",
                "reason": "ChildKernelConfig executable paths require a separate exact accepted executable binding; U01 binds source only.",
            },
        }
    )
    for path in go_members_ordered:
        path_groups[path].add("AX-GO")

    shared_design = _group(successor_design, "AX-SHARED-DISPATCH")
    if shared_design.get("member_source") != "the exact 26-member current profile list":
        raise SourceClosureError("AX-SHARED-DISPATCH member source changed")
    profile_shared = _profile_runner(current_profile, "RUN-SHARED-DISPATCH-CHILD-LOCAL")
    shared_members = _string_list(
        profile_shared.get("source_members"), label="shared-dispatch profile members"
    )
    if len(shared_members) != 26:
        raise SourceClosureError("AX-SHARED-DISPATCH profile must contain exactly 26 members")
    old_shared = _prior_group(prior_closure, "AX-SHARED-DISPATCH")
    old_members = set(
        _string_list(old_shared.get("required_source_members"), label="prior shared members")
    )
    omissions = _sort_paths(set(shared_members) - old_members)
    if len(omissions) != 14 or not old_members.issubset(set(shared_members)):
        raise SourceClosureError(
            "AX-SHARED-DISPATCH must retain the exact fourteen older-design omission negatives"
        )
    output.append(
        {
            "group_id": "AX-SHARED-DISPATCH",
            "member_count": len(shared_members),
            "members": _sort_paths(shared_members),
            "rationale": "exact current profile source list",
            "omission_witnesses": [
                {"path": path, "status": "required-and-present"} for path in omissions
            ],
        }
    )
    for path in shared_members:
        path_groups[path].add("AX-SHARED-DISPATCH")

    if [group["group_id"] for group in output] != list(GROUP_ORDER):
        raise SourceClosureError("source groups are not in canonical order")
    return output, path_groups


def _validate_accepted_binding(
    rows: Sequence[Mapping[str, Any]], binding: Mapping[str, Any]
) -> dict[str, Any]:
    required = {"lock_sha256", "tree_sha256", "member_count", "snapshot_locator"}
    if set(binding) != required:
        raise SourceClosureError("accepted snapshot binding fields are not closed")
    if binding.get("member_count") != len(rows):
        raise SourceClosureError("accepted snapshot member count mismatch")
    observed_tree = _tree(rows)
    if binding.get("tree_sha256") != observed_tree:
        raise SourceClosureError("accepted snapshot tree digest mismatch")
    for key in ("lock_sha256", "tree_sha256"):
        value = binding.get(key)
        if (
            not isinstance(value, str)
            or len(value) != 64
            or any(char not in "0123456789abcdef" for char in value)
        ):
            raise SourceClosureError(f"accepted snapshot {key} is invalid")
    locator = binding.get("snapshot_locator")
    if not isinstance(locator, str) or not locator or locator.startswith("/"):
        raise SourceClosureError("accepted snapshot locator must be stable and non-absolute")
    return dict(binding)


def build_source_closure_v2(
    repository_root: Path | str,
    accepted_snapshot_root: Path | str,
    *,
    successor_design: Mapping[str, Any],
    current_profile: Mapping[str, Any],
    prior_closure: Mapping[str, Any],
    accepted_binding: Mapping[str, Any],
    source_bindings: Sequence[Mapping[str, Any]],
    closure_id: str = "RWO-CVG-002-source-closure-candidate",
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build an exact candidate closure and a non-authoritative snapshot delta."""

    root = Path(repository_root).resolve(strict=True)
    snapshot = Path(accepted_snapshot_root).resolve(strict=True)
    if not root.is_dir() or not snapshot.is_dir():
        raise SourceClosureError("repository and accepted snapshot roots must be directories")
    accepted_paths = _all_snapshot_members(snapshot)
    accepted_rows = [_member(snapshot, path) for path in accepted_paths]
    normalized_binding = _validate_accepted_binding(accepted_rows, accepted_binding)
    groups, path_groups = _resolved_groups(root, successor_design, current_profile, prior_closure)

    candidate_paths = set(path_groups)
    for path in accepted_paths:
        target = root.joinpath(*PurePosixPath(path).parts)
        try:
            info = target.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise SourceClosureError(f"accepted source path is no longer a regular file: {path}")
        candidate_paths.add(path)

    candidate_rows: list[dict[str, Any]] = []
    for path in _sort_paths(candidate_paths):
        row = _member(root, path)
        groups_for_path = _sort_paths(path_groups.get(path, set()))
        rationale = list(groups_for_path)
        if path in accepted_paths:
            rationale.append("preserved-accepted-snapshot")
        row["groups"] = groups_for_path
        row["rationale"] = rationale
        candidate_rows.append(row)

    accepted_by_path = {row["path"]: row for row in accepted_rows}
    candidate_by_path = {row["path"]: row for row in candidate_rows}
    additions = [candidate_by_path[path] for path in _sort_paths(set(candidate_by_path) - set(accepted_by_path))]
    removals = [accepted_by_path[path] for path in _sort_paths(set(accepted_by_path) - set(candidate_by_path))]
    changes: list[dict[str, Any]] = []
    unchanged = 0
    for path in _sort_paths(set(accepted_by_path) & set(candidate_by_path)):
        before = accepted_by_path[path]
        after = candidate_by_path[path]
        if any(before[key] != after[key] for key in ("mode", "size_bytes", "sha256")):
            changes.append({"path": path, "before": before, "after": after})
        else:
            unchanged += 1

    normalized_sources: list[dict[str, Any]] = []
    for index, raw in enumerate(source_bindings):
        binding = _mapping(raw, label=f"source binding {index}")
        required = {"role", "path", "sha256", "size_bytes"}
        if set(binding) != required:
            raise SourceClosureError(f"source binding {index} fields are not closed")
        path = _path(binding.get("path"), label=f"source binding {index} path")
        data, _ = stable_read(root, path)
        if binding.get("size_bytes") != len(data) or binding.get("sha256") != hashlib.sha256(data).hexdigest():
            raise SourceClosureError(f"source binding drift: {path}")
        if not isinstance(binding.get("role"), str) or not binding["role"]:
            raise SourceClosureError(f"source binding {index} role is invalid")
        normalized_sources.append(dict(binding))
    normalized_sources.sort(key=lambda row: (row["role"].encode(), row["path"].encode()))

    candidate_tree = _tree(candidate_rows)
    closure = {
        "schema_version": CLOSURE_SCHEMA,
        "closure_id": closure_id,
        "posture": "candidate-valid-acceptance-required",
        "source_bindings": normalized_sources,
        "accepted_snapshot_binding": normalized_binding,
        "groups": groups,
        "preserved_accepted_member_count": sum(
            1 for row in candidate_rows if "preserved-accepted-snapshot" in row["rationale"]
        ),
        "member_count": len(candidate_rows),
        "members": candidate_rows,
        "tree_sha256": candidate_tree,
        "global_rules": {
            "execution_root": "byte-exact-read-only-task-snapshot",
            "network": "forbidden",
            "shell_commands": "forbidden",
            "product_runner_execution": "forbidden-in-u01",
            "unlisted_children": "terminal-block",
            "ambient_path_or_cache": "forbidden",
            "member_order": "utf8-bytewise-path",
        },
        "validation_posture": {
            "source_reads_only": True,
            "product_runner_executed": False,
            "toolchain_executed": False,
            "acceptance_required": True,
        },
        "authority_effect": "none",
    }
    delta = {
        "schema_version": DELTA_SCHEMA,
        "delta_id": f"{closure_id}-against-accepted",
        "accepted_snapshot_binding": normalized_binding,
        "candidate_binding": {
            "closure_id": closure_id,
            "member_count": len(candidate_rows),
            "tree_sha256": candidate_tree,
        },
        "added_count": len(additions),
        "added": additions,
        "removed_count": len(removals),
        "removed": removals,
        "changed_count": len(changes),
        "changed": changes,
        "unchanged_count": unchanged,
        "acceptance_effect": "none",
        "authority_effect": "none",
    }
    return closure, delta


def verify_source_closure_v2(
    repository_root: Path | str, closure: Mapping[str, Any]
) -> None:
    """Rehash every candidate member and fail on deletion, mutation, or reordering."""

    root = Path(repository_root).resolve(strict=True)
    if closure.get("schema_version") != CLOSURE_SCHEMA:
        raise SourceClosureError("unsupported closure schema")
    if closure.get("authority_effect") != "none":
        raise SourceClosureError("source closure cannot carry authority")
    members = closure.get("members")
    if not isinstance(members, list) or closure.get("member_count") != len(members):
        raise SourceClosureError("source closure member count mismatch")
    paths = [row.get("path") for row in members if isinstance(row, Mapping)]
    if len(paths) != len(members) or paths != _sort_paths(paths) or len(paths) != len(set(paths)):
        raise SourceClosureError("source closure paths are not unique and canonically ordered")
    observed: list[dict[str, Any]] = []
    for raw in members:
        path = _path(raw.get("path"), label="closure member path")
        row = _member(root, path)
        for key in ("type", "mode", "size_bytes", "sha256"):
            if raw.get(key) != row[key]:
                raise SourceClosureError(f"source closure drift for {path}: {key}")
        observed.append(row)
    if _tree(observed) != closure.get("tree_sha256"):
        raise SourceClosureError("source closure tree digest mismatch")
    member_set = set(paths)
    groups = closure.get("groups")
    if not isinstance(groups, list) or [group.get("group_id") for group in groups] != list(GROUP_ORDER):
        raise SourceClosureError("source closure groups are incomplete or unordered")
    for group in groups:
        group_members = group.get("members")
        if (
            not isinstance(group_members, list)
            or group.get("member_count") != len(group_members)
            or group_members != _sort_paths(group_members)
            or not set(group_members).issubset(member_set)
        ):
            raise SourceClosureError(f"invalid group inventory: {group.get('group_id')}")
