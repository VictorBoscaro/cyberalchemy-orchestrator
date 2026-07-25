"""Deterministic bounded traversal for one isolated topology projection."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable


def edge_identity(edge: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(edge["source_id"]),
        str(edge["edge_kind"]),
        str(edge["evidence_id"]),
        str(edge["target_id"]),
    )


def normalize_edges(edges: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate exact edge identities while retaining parallel evidence edges."""
    by_identity: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for edge in edges:
        by_identity.setdefault(edge_identity(edge), dict(edge))
    return [by_identity[key] for key in sorted(by_identity)]


def find_paths(
    *,
    nodes: Iterable[str],
    edges: Iterable[dict[str, Any]],
    source_id: str,
    target_id: str,
    direction: str,
    allowed_edge_kinds: set[str],
    max_depth: int,
    max_paths: int,
    exploration_limit: int = 20_000,
) -> dict[str, Any]:
    """Enumerate simple paths breadth-first in deterministic path order."""
    node_set = set(nodes)
    if source_id not in node_set or target_id not in node_set:
        return {
            "query_state": "invalid-endpoint",
            "paths": [],
            "returned_depth": None,
            "more_paths_exist": False,
        }

    selected = [
        edge for edge in normalize_edges(edges) if edge["edge_kind"] in allowed_edge_kinds
    ]
    adjacency: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for edge in selected:
        source = str(edge["source_id"])
        target = str(edge["target_id"])
        if direction in {"outbound", "undirected-view"}:
            adjacency[source].append((target, edge))
        if direction in {"inbound", "undirected-view"}:
            adjacency[target].append((source, edge))
    for values in adjacency.values():
        values.sort(key=lambda item: (item[0], edge_identity(item[1])))

    candidates: list[dict[str, Any]] = []
    frontier: list[tuple[list[str], list[dict[str, Any]]]] = [([source_id], [])]
    explored = 0
    safety_truncated = False
    for _depth in range(max_depth + 1):
        next_frontier: list[tuple[list[str], list[dict[str, Any]]]] = []
        for traversed_nodes, traversed_edges in frontier:
            explored += 1
            if explored > exploration_limit:
                safety_truncated = True
                break
            current = traversed_nodes[-1]
            if current == target_id:
                candidates.append(
                    {
                        "node_ids": list(traversed_nodes),
                        "edges": [dict(edge) for edge in traversed_edges],
                        "edge_count": len(traversed_edges),
                    }
                )
                if len(candidates) > max_paths:
                    break
                continue
            if len(traversed_edges) >= max_depth:
                continue
            for next_node, edge in adjacency.get(current, []):
                if next_node in traversed_nodes:
                    continue
                next_frontier.append(
                    ([*traversed_nodes, next_node], [*traversed_edges, edge])
                )
        if safety_truncated or len(candidates) > max_paths:
            break
        next_frontier.sort(
            key=lambda item: tuple(edge_identity(edge) for edge in item[1])
        )
        frontier = next_frontier
    more = len(candidates) > max_paths or safety_truncated
    returned = candidates[:max_paths]
    return {
        "query_state": "truncated" if more else "success" if returned else "no-path",
        "paths": returned,
        "returned_depth": max((p["edge_count"] for p in returned), default=None),
        "more_paths_exist": None if safety_truncated else more,
        "explored_candidates": explored,
        "exploration_limit": exploration_limit,
    }
