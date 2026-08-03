"""Read-only source adapters for the Control Center."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .. import ledger


@dataclass(frozen=True)
class SourceSnapshot:
    snapshot_id: str
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]
    source_facts: list[dict[str, Any]]
    completeness: str = "complete"


class SkillGraphSource:
    """Loads the frozen extraction witness and verifies its stated invariants."""

    def __init__(self, graph_path: Path, *, skills_dir: Path | None = None):
        self.graph_path = graph_path
        self.skills_dir = skills_dir

    def read(self) -> SourceSnapshot:
        raw = self.graph_path.read_bytes()
        data = json.loads(raw.decode("utf-8-sig"))
        nodes = list(data.get("nodes") or [])
        edges = list(data.get("edges") or [])
        if len(nodes) != 72 or len(edges) != 261:
            raise ValueError("skill graph fixture violates the frozen 72/261 contract")
        explicit = sum(edge.get("relation") == "explicit_path" for edge in edges)
        named = sum(edge.get("relation") == "named_reference" for edge in edges)
        if (explicit, named) != (7, 254):
            raise ValueError("skill graph relation counts violate the frozen contract")
        fixture_digest = hashlib.sha256(raw).hexdigest()
        warnings: list[str] = []
        completeness = "complete"
        if self.skills_dir is not None:
            module_path = self.graph_path.with_name("build_graph.py")
            spec = importlib.util.spec_from_file_location(
                "_control_center_skill_graph_builder", module_path
            )
            if spec is None or spec.loader is None:
                raise RuntimeError("skill graph builder cannot be loaded")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            repo_root = self.graph_path.parents[2]
            skills, errors = module.discover_skills(self.skills_dir)
            live_edges, unresolved = module.extract_edges(skills, repo_root)
            nodes = []
            for name, path in sorted(skills.items()):
                _, text = module.parse_skill(path)
                nodes.append(
                    {
                        "id": name,
                        "path": path.relative_to(repo_root).as_posix(),
                        "description": module.parse_description(text),
                    }
                )
            edges = live_edges
            warnings = [*errors, *[f"unresolved explicit path: {row}" for row in unresolved]]
            if warnings:
                completeness = "partial"
        normalized = json.dumps(
            {"nodes": nodes, "edges": edges},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        digest = hashlib.sha256(normalized).hexdigest()
        return SourceSnapshot(
            snapshot_id=f"skill-graph:{digest[:16]}",
            nodes=sorted(nodes, key=lambda row: row["id"]),
            edges=sorted(
                edges,
                key=lambda row: (
                    row["source"],
                    row["relation"],
                    "|".join(row.get("evidence") or []),
                    row["target"],
                ),
            ),
            source_facts=[
                {
                    "source_id": "skill-relationship-graph",
                    "revision": digest,
                    "fixture_revision": fixture_digest,
                    "ingestion_state": "accepted",
                    "coverage": completeness,
                    "path": str(self.graph_path),
                    "warnings": warnings,
                }
            ],
            completeness=completeness,
        )


class DispatchSource:
    """Normalizes existing ledger rows without inventing parentage."""

    def __init__(self, repos: Iterable[Path]):
        self.repos = list(repos)

    def read(self) -> SourceSnapshot:
        nodes: list[dict[str, Any]] = []
        edges: list[dict[str, Any]] = []
        facts: list[dict[str, Any]] = []
        incomplete = False
        signatures: list[str] = []
        for repo in self.repos:
            parsed = ledger.load_repo_rows(repo, copy=False)
            signatures.append(f"{repo}:{ledger.signature([repo])}")
            if parsed.error:
                incomplete = True
                facts.append(
                    {
                        "source_id": f"dispatch-ledger:{repo.name}",
                        "ingestion_state": "failed",
                        "safe_error": parsed.error,
                    }
                )
                continue
            facts.append(
                {
                    "source_id": f"dispatch-ledger:{repo.name}",
                    "revision": signatures[-1],
                    "ingestion_state": "accepted",
                    "coverage": "complete",
                    "warnings": list(parsed.warnings),
                }
            )
            by_id: dict[str, dict[str, Any]] = {}
            for row in parsed.rows:
                dispatch_id = row.get("dispatch_id")
                if not isinstance(dispatch_id, str):
                    continue
                item = dict(row)
                item["_repo"] = repo.name
                item["_stable_id"] = f"{repo.name}:{dispatch_id}"
                by_id[dispatch_id] = item
                nodes.append(item)
            for dispatch_id, row in by_id.items():
                parent_id = row.get("parent_dispatch_id")
                if not isinstance(parent_id, str) or not parent_id:
                    continue
                edges.append(
                    {
                        "source": f"{repo.name}:{parent_id}",
                        "target": f"{repo.name}:{dispatch_id}",
                        "relation": "parent_dispatch_id",
                        "evidence": [f"{repo.name}:{dispatch_id}:parent_dispatch_id"],
                        "resolved": parent_id in by_id,
                    }
                )
        digest = hashlib.sha256("\n".join(signatures).encode()).hexdigest()
        return SourceSnapshot(
            snapshot_id=f"dispatch-ledgers:{digest[:16]}",
            nodes=sorted(nodes, key=lambda row: row["_stable_id"]),
            edges=sorted(edges, key=lambda row: (row["source"], row["target"])),
            source_facts=facts,
            completeness="partial" if incomplete else "complete",
        )


def pending_items(repos: Iterable[Path]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for repo in repos:
        for item in ledger.read_pending(repo):
            result.append({**item, "_repo": repo.name})
    return result
