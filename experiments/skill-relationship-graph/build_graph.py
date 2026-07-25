#!/usr/bin/env python3
"""Build a deterministic static relationship graph from repository skills."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


FRONTMATTER_NAME = re.compile(r"(?m)^name:\s*[\"']?([^\"'\r\n]+?)[\"']?\s*$")
FRONTMATTER_DESCRIPTION = re.compile(
    r"(?m)^description:\s*[\"']?(.+?)[\"']?\s*$"
)
PATH_REFERENCE = re.compile(
    r"(?:\.{1,2}/|\.claude/skills/|\.agents/skills/)"
    r"(?P<name>[a-z0-9][a-z0-9-]*)/SKILL\.md"
)
INLINE_CODE = re.compile(r"`([a-z0-9][a-z0-9-]*)`")


def parse_skill(path: Path) -> tuple[str | None, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_NAME.search(text)
    return (match.group(1).strip() if match else None), text


def parse_description(text: str) -> str:
    match = FRONTMATTER_DESCRIPTION.search(text)
    return match.group(1).strip().strip("\"'") if match else ""


def discover_skills(skills_dir: Path) -> tuple[dict[str, Path], list[str]]:
    skills: dict[str, Path] = {}
    errors: list[str] = []
    for path in sorted(skills_dir.glob("*/SKILL.md")):
        name, _ = parse_skill(path)
        if not name:
            errors.append(f"missing frontmatter name: {path}")
        elif name in skills:
            errors.append(f"duplicate skill name {name}: {skills[name]} and {path}")
        else:
            skills[name] = path
    return skills, errors


def extract_edges(
    skills: dict[str, Path], repo: Path
) -> tuple[list[dict], list[dict]]:
    evidence: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    unresolved: list[dict] = []
    known = set(skills)

    for source, path in sorted(skills.items()):
        _, text = parse_skill(path)
        body = text.split("---", 2)[-1]
        relative_path = path.relative_to(repo).as_posix()

        for line_number, line in enumerate(body.splitlines(), 1):
            for match in PATH_REFERENCE.finditer(line):
                target = match.group("name")
                if target == source:
                    continue
                if target in known:
                    evidence[(source, target, "explicit_path")].add(
                        f"{relative_path}:{line_number}"
                    )
                else:
                    unresolved.append(
                        {
                            "source": source,
                            "target": target,
                            "evidence": f"{relative_path}:{line_number}",
                        }
                    )

            for target in INLINE_CODE.findall(line):
                if target in known and target != source:
                    evidence[(source, target, "named_reference")].add(
                        f"{relative_path}:{line_number}"
                    )

    edges = [
        {
            "source": source,
            "target": target,
            "relation": relation,
            "evidence": sorted(refs),
        }
        for (source, target, relation), refs in sorted(evidence.items())
    ]
    return edges, sorted(unresolved, key=lambda row: tuple(row.values()))


def project(edges: list[dict], relations: set[str]) -> set[tuple[str, str]]:
    return {
        (edge["source"], edge["target"])
        for edge in edges
        if edge["relation"] in relations
    }


def classify(names: set[str], pairs: set[tuple[str, str]]) -> tuple[dict, dict]:
    incoming = {name: 0 for name in names}
    outgoing = {name: 0 for name in names}
    for source, target in pairs:
        outgoing[source] += 1
        incoming[target] += 1

    categories = {"source": [], "sink": [], "isolated": [], "connected": []}
    for name in sorted(names):
        if incoming[name] == 0 and outgoing[name] == 0:
            categories["isolated"].append(name)
        elif incoming[name] == 0:
            categories["source"].append(name)
        elif outgoing[name] == 0:
            categories["sink"].append(name)
        else:
            categories["connected"].append(name)

    degrees = {
        name: {"in": incoming[name], "out": outgoing[name]}
        for name in sorted(names)
    }
    return categories, degrees


def render_experiment(data: dict) -> str:
    inclusive = data["views"]["inclusive"]
    strong = data["views"]["strong"]
    relation_counts: dict[str, int] = defaultdict(int)
    for edge in data["edges"]:
        relation_counts[edge["relation"]] += 1
    return "\n".join(
        [
            "# Skill relationship graph — probe",
            "",
            "## Input",
            "",
            f"- Skill root: `{data['skills_root']}`",
            f"- Files discovered: {data['metrics']['skill_files_discovered']}",
            f"- Files parsed: {data['metrics']['skills_parsed']}",
            "",
            "## Raw result",
            "",
            f"- Distinct inclusive pairs: {inclusive['edge_count']}",
            f"- Distinct strong pairs: {strong['edge_count']}",
            f"- `explicit_path` evidence rows: {relation_counts['explicit_path']}",
            f"- `named_reference` evidence rows: {relation_counts['named_reference']}",
            f"- Unresolved explicit paths: {data['metrics']['unresolved_explicit_paths']}",
            f"- Parse errors: {len(data['parse_errors'])}",
            "",
            "The complete raw result and line-level evidence are in `graph.json`.",
            "",
        ]
    )


def render_findings(data: dict) -> str:
    inclusive = data["views"]["inclusive"]
    strong = data["views"]["strong"]
    categories = inclusive["categories"]
    lines = [
        "# Skill relationship graph — result",
        "",
        "This is a static declaration graph, not runtime invocation proof.",
        "",
        "## Verdict",
        "",
        f"**{data['verdict']}** — {data['verdict_reason']}",
        "",
        "## Summary",
        "",
        f"- Skills parsed: {data['metrics']['skills_parsed']} / "
        f"{data['metrics']['skill_files_discovered']}",
        f"- Inclusive edges: {inclusive['edge_count']}",
        f"- Strong (`SKILL.md` path) edges: {strong['edge_count']}",
        f"- Unresolved explicit paths: {data['metrics']['unresolved_explicit_paths']}",
        "",
        "## Strong view",
        "",
        f"- Sources: {len(strong['categories']['source'])}",
        f"- Sinks: {len(strong['categories']['sink'])}",
        f"- Isolated: {len(strong['categories']['isolated'])}",
        f"- Connected: {len(strong['categories']['connected'])}",
        "- Non-isolated skills: "
        + ", ".join(
            f"`{name}`"
            for name in sorted(
                set(data["views"]["strong"]["degrees"])
                - set(strong["categories"]["isolated"])
            )
        ),
        "",
        "## Inclusive structural classes",
        "",
    ]
    for category in ("source", "sink", "isolated", "connected"):
        values = categories[category]
        lines.append(f"### {category} ({len(values)})")
        lines.append("")
        lines.append(", ".join(f"`{value}`" for value in values) if values else "_none_")
        lines.append("")

    ranked = sorted(
        inclusive["degrees"].items(),
        key=lambda item: (-(item[1]["in"] + item[1]["out"]), item[0]),
    )[:15]
    lines.extend(
        [
            "## Highest-degree skills",
            "",
            "| skill | in | out | total |",
            "|---|---:|---:|---:|",
        ]
    )
    for name, degree in ranked:
        lines.append(
            f"| `{name}` | {degree['in']} | {degree['out']} | "
            f"{degree['in'] + degree['out']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "- `explicit_path` is strong evidence of a declared dependency or routing relation.",
            "- `named_reference` is weaker: it proves a textual mention, not a call.",
            "- A `source`, `sink`, or `isolated` label is structural, not a quality verdict.",
            "- Runtime truth should later add edges from hooks, scripts, dispatches, and telemetry.",
            "",
            "Machine-readable outputs: `graph.json` and `graph.dot`.",
            "",
        ]
    )
    return "\n".join(lines)


def render_dot(names: set[str], pairs: set[tuple[str, str]], categories: dict) -> str:
    colors = {
        "source": "#d97706",
        "sink": "#2563eb",
        "isolated": "#6b7280",
        "connected": "#059669",
    }
    category_by_name = {
        name: category for category, values in categories.items() for name in values
    }
    lines = [
        "digraph skills {",
        '  graph [rankdir="LR"];',
        '  node [shape="box", style="rounded,filled", fontname="Arial", fontcolor="white"];',
    ]
    for name in sorted(names):
        lines.append(
            f'  "{name}" [fillcolor="{colors[category_by_name[name]]}"];'
        )
    for source, target in sorted(pairs):
        lines.append(f'  "{source}" -> "{target}";')
    lines.append("}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("../.."))
    parser.add_argument("--skills-dir", default=".claude/skills")
    parser.add_argument("--out-dir", type=Path, default=Path("."))
    args = parser.parse_args()

    repo = args.repo.resolve()
    skills_dir = (repo / args.skills_dir).resolve()
    out_dir = args.out_dir.resolve()
    skills, parse_errors = discover_skills(skills_dir)
    edges, unresolved = extract_edges(skills, repo)

    inclusive_pairs = project(edges, {"explicit_path", "named_reference"})
    strong_pairs = project(edges, {"explicit_path"})
    inclusive_categories, inclusive_degrees = classify(set(skills), inclusive_pairs)
    strong_categories, strong_degrees = classify(set(skills), strong_pairs)

    discovered_count = len(list(skills_dir.glob("*/SKILL.md")))
    parse_ratio = len(skills) / discovered_count if discovered_count else 0
    nonempty_categories = sum(bool(values) for values in inclusive_categories.values())
    if parse_ratio < 0.95 or unresolved:
        verdict = "INVALID"
        verdict_reason = "the pre-registered parse or resolution validity gate failed."
    elif inclusive_pairs and nonempty_categories >= 2:
        verdict = "SURVIVED"
        verdict_reason = "the graph is non-empty and exposes multiple structural classes."
    else:
        verdict = "FALSIFIED"
        verdict_reason = "the textual graph is empty or structurally non-discriminating."

    data = {
        "schema_version": "skill-relationship-graph.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": repo.as_posix(),
        "skills_root": skills_dir.relative_to(repo).as_posix(),
        "criterion": "criterion.md",
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "metrics": {
            "skill_files_discovered": discovered_count,
            "skills_parsed": len(skills),
            "parse_ratio": parse_ratio,
            "unresolved_explicit_paths": len(unresolved),
        },
        "nodes": [
            {
                "id": name,
                "path": path.relative_to(repo).as_posix(),
                "description": parse_description(parse_skill(path)[1]),
            }
            for name, path in sorted(skills.items())
        ],
        "edges": edges,
        "unresolved_explicit_paths": unresolved,
        "parse_errors": parse_errors,
        "views": {
            "inclusive": {
                "relations": ["explicit_path", "named_reference"],
                "edge_count": len(inclusive_pairs),
                "categories": inclusive_categories,
                "degrees": inclusive_degrees,
            },
            "strong": {
                "relations": ["explicit_path"],
                "edge_count": len(strong_pairs),
                "categories": strong_categories,
                "degrees": strong_degrees,
            },
        },
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "graph.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out_dir / "graph-data.js").write_text(
        "window.SKILL_GRAPH = "
        + json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
        + ";\n",
        encoding="utf-8",
    )
    (out_dir / "graph.dot").write_text(
        render_dot(set(skills), inclusive_pairs, inclusive_categories), encoding="utf-8"
    )
    (out_dir / "experiment.md").write_text(render_experiment(data), encoding="utf-8")
    (out_dir / "findings.md").write_text(render_findings(data), encoding="utf-8")
    print(
        json.dumps(
            {
                "verdict": verdict,
                "skills": len(skills),
                "inclusive_edges": len(inclusive_pairs),
                "strong_edges": len(strong_pairs),
                "categories": {
                    key: len(value) for key, value in inclusive_categories.items()
                },
                "unresolved": len(unresolved),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
