from __future__ import annotations

import unittest

from server.control_center.path_engine import find_paths


def edge(source: str, target: str, evidence: str) -> dict:
    return {
        "source_id": source,
        "target_id": target,
        "edge_kind": "declared",
        "evidence_id": evidence,
    }


class DeterministicPathEngineTest(unittest.TestCase):
    def test_shortest_then_lexical_parallel_edges_and_cycles(self):
        edges = [
            edge("a", "b", "z"),
            edge("a", "b", "a"),
            edge("b", "a", "cycle"),
            edge("b", "c", "bc"),
            edge("a", "c", "direct"),
        ]
        result = find_paths(
            nodes={"a", "b", "c"},
            edges=edges,
            source_id="a",
            target_id="c",
            direction="outbound",
            allowed_edge_kinds={"declared"},
            max_depth=3,
            max_paths=10,
        )
        self.assertEqual(result["query_state"], "success")
        self.assertEqual([path["edge_count"] for path in result["paths"]], [1, 2, 2])
        self.assertEqual(
            [path["edges"][0]["evidence_id"] for path in result["paths"][1:]],
            ["a", "z"],
        )
        self.assertTrue(
            all(len(path["node_ids"]) == len(set(path["node_ids"])) for path in result["paths"])
        )

    def test_limit_reports_truncated_and_zero_depth_identity(self):
        limited = find_paths(
            nodes={"a", "b", "c"},
            edges=[edge("a", "b", "1"), edge("b", "c", "2"), edge("a", "c", "3")],
            source_id="a",
            target_id="c",
            direction="outbound",
            allowed_edge_kinds={"declared"},
            max_depth=2,
            max_paths=1,
        )
        self.assertEqual(limited["query_state"], "truncated")
        self.assertTrue(limited["more_paths_exist"])
        identity = find_paths(
            nodes={"a"},
            edges=[],
            source_id="a",
            target_id="a",
            direction="outbound",
            allowed_edge_kinds={"declared"},
            max_depth=0,
            max_paths=1,
        )
        self.assertEqual(identity["query_state"], "success")
        self.assertEqual(identity["paths"][0]["edge_count"], 0)


if __name__ == "__main__":
    unittest.main()
