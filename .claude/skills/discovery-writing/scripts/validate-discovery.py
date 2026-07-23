#!/usr/bin/env python3
"""Validate one discovery against the authoring contract."""

from __future__ import annotations

import re
from argparse import ArgumentParser
from pathlib import Path


REQUIRED_FRONTMATTER = {
    "tags",
    "node_type",
    "is_session",
    "layer",
    "nature",
    "status",
    "veracity",
    "conviction",
    "version",
    "last_updated",
}
ALLOWED_LAYER = {"ontology", "architecture", "domain", "application", "external"}
ALLOWED_NATURE = {"explanatory", "procedural", "reference", "technical"}
ALLOWED_STATUS = {"draft", "exploratory", "active", "consolidated", "evergreen"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ORDERED_HEADINGS = [
    "objective",
    "1. business context",
    "2. core concepts",
    "open questions",
    "decisions baked in",
    "connections",
    "flow diagram",
    "appendix — changelog",
]


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("discovery")
    parser.add_argument("--expected-source")
    parser.add_argument("--dispatch-id")
    parser.add_argument("--research-source")
    args = parser.parse_args()

    path = Path(args.discovery).resolve()
    if bool(args.expected_source) != bool(args.dispatch_id):
        parser.error("--expected-source and --dispatch-id must be supplied together")
    expected_source = (
        Path(args.expected_source).resolve() if args.expected_source else None
    )
    research_source = (
        Path(args.research_source).resolve() if args.research_source else None
    )
    if not path.is_file():
        parser.error(f"discovery not found: {path}")
    if expected_source is not None and not expected_source.is_file():
        parser.error(f"expected source not found: {expected_source}")
    if research_source is not None and not research_source.is_file():
        parser.error(f"research source not found: {research_source}")

    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    repo_root = next(
        (parent for parent in (path.parent, *path.parents) if (parent / ".git").exists()),
        None,
    )
    if repo_root is None:
        errors.append("target is not inside a Git repository")
    else:
        relative = path.relative_to(repo_root).as_posix()
        allowed_path = (
            re.fullmatch(r"docs/features/[^/]+/discovery/[^/]+\.md", relative)
            or re.fullmatch(r"vault/discovery/[^/]+-definitions/[^/]+\.md", relative)
        )
        if allowed_path is None:
            errors.append(
                f"target path is outside the two allowed discovery shapes: {relative}"
            )

    frontmatter = read_frontmatter(lines, errors)
    key_list = re.findall(
        r"(?m)^([A-Za-z_][A-Za-z0-9_-]*):",
        frontmatter,
    )
    keys = set(key_list)
    for key in sorted({item for item in key_list if key_list.count(item) > 1}):
        errors.append(f"duplicate top-level frontmatter key: {key}")
    for key in sorted(REQUIRED_FRONTMATTER - keys):
        errors.append(f"required frontmatter key is missing: {key}")

    if scalar(frontmatter, "node_type") != "discovery":
        errors.append("node_type must be discovery")
    if scalar(frontmatter, "is_session") != "false":
        errors.append("is_session must be false")
    validate_values(frontmatter, errors)

    headings = [
        (match.group(1).strip().lower(), text[: match.start()].count("\n") + 1)
        for match in re.finditer(r"(?m)^##\s+(.+?)\s*$", text)
    ]
    cursor = -1
    for required in ORDERED_HEADINGS:
        found = next(
            (
                (index, line)
                for index, (heading, line) in enumerate(headings)
                if heading == required and index > cursor
            ),
            None,
        )
        if found is None:
            errors.append(
                f"required H2 heading is missing or misplaced: {required}"
            )
        else:
            cursor = found[0]

    objective = section(text, "Objective", r"1\. Business Context")
    if objective is None:
        errors.append("Objective block is missing")
    else:
        for marker in ("**Status:**", "**Owner:**"):
            if marker not in objective:
                errors.append(f"Objective block is missing {marker}")
        owner = re.search(r"(?m)^\*\*Owner:\*\*\s*(\S+)\s*$", objective)
        if owner is None:
            errors.append("Owner must appear alone on its bold-label line")
        elif re.fullmatch(
            r"@[A-Za-z0-9][A-Za-z0-9._-]*",
            owner.group(1),
        ) is None:
            errors.append(
                "Owner must be one exact @handle using letters, numbers, dot, underscore, or hyphen"
            )

    open_questions = section(text, "Open Questions", "Decisions Baked In")
    if open_questions is None:
        errors.append("Open Questions block is missing")
    else:
        oq_ids = set(re.findall(r"\bOQ-[A-Za-z0-9]+", open_questions))
        no_questions = re.fullmatch(
            r"(?is)##\s+Open Questions\s*\n+\s*No open questions\.\s*",
            open_questions,
        )
        if not oq_ids and no_questions is None:
            errors.append(
                "Open Questions must contain OQ identifiers or exactly 'No open questions.'"
            )
        if oq_ids:
            for marker in ("**Question:**", "**Recommendation:**"):
                if marker not in open_questions:
                    errors.append(f"Open Questions section is missing {marker}")
            if re.search(r"(?i)settle(?:ment)? (?:in|stage)", open_questions) is None:
                errors.append("Open Questions section is missing a settlement stage")

    flow = section(text, "Flow Diagram", "Appendix — Changelog")
    if flow is None or "```mermaid" not in flow:
        errors.append("Flow Diagram must contain a Mermaid fence before the changelog")
    if text.count("```") % 2:
        errors.append("code fences are unbalanced")

    validate_links(path, text, errors)
    validate_source_footer(
        path,
        text,
        expected_source,
        args.dispatch_id,
        research_source,
        errors,
    )

    if errors:
        for error in errors:
            print(f"[discovery] {path}: {error}")
        print(f"discovery validation: FAIL ({len(errors)} issue(s))")
        return 1

    print(
        "discovery validation: PASS "
        f"(frontmatter={len(keys)} keys, headings={len(headings)})"
    )
    return 0


def read_frontmatter(lines: list[str], errors: list[str]) -> str:
    if len(lines) < 3 or lines[0].strip() != "---":
        errors.append("frontmatter must start on line 1")
        return ""
    try:
        end = next(
            index
            for index, line in enumerate(lines[1:], 1)
            if line.strip() == "---"
        )
    except StopIteration:
        errors.append("frontmatter closing delimiter is missing")
        return ""
    return "\n".join(lines[1:end])


def scalar(frontmatter: str, name: str) -> str:
    match = re.search(
        rf"(?m)^{re.escape(name)}:\s*(.*?)\s*$",
        frontmatter,
    )
    return match.group(1).strip() if match else ""


def list_values(frontmatter: str, name: str) -> set[str]:
    raw = scalar(frontmatter, name)
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    return {item.strip() for item in raw.split(",") if item.strip()}


def validate_values(frontmatter: str, errors: list[str]) -> None:
    for name, allowed in (
        ("layer", ALLOWED_LAYER),
        ("nature", ALLOWED_NATURE),
    ):
        actual = list_values(frontmatter, name)
        if not actual or not actual <= allowed:
            errors.append(
                f"{name} must contain only {sorted(allowed)}; got {sorted(actual)}"
            )
    if scalar(frontmatter, "status") not in ALLOWED_STATUS:
        errors.append(f"status must be one of {sorted(ALLOWED_STATUS)}")
    for name in ("veracity", "conviction"):
        if scalar(frontmatter, name) not in ALLOWED_CONFIDENCE:
            errors.append(f"{name} must be one of {sorted(ALLOWED_CONFIDENCE)}")
    if re.fullmatch(r"\d+\.\d+\.\d+", scalar(frontmatter, "version")) is None:
        errors.append("version must use semantic numeric form X.Y.Z")
    if re.fullmatch(
        r"\d{4}-\d{2}-\d{2}",
        scalar(frontmatter, "last_updated"),
    ) is None:
        errors.append("last_updated must use YYYY-MM-DD")


def section(text: str, start: str, end: str) -> str | None:
    match = re.search(
        rf"(?ims)^##\s+{re.escape(start)}\s*$.*?(?=^##\s+{end}\s*$)",
        text,
    )
    return match.group(0) if match else None


def validate_links(path: Path, text: str, errors: list[str]) -> None:
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).split("#", 1)[0]
        if not target or re.match(r"^(?:https?|mailto):", target):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            line = text[: match.start()].count("\n") + 1
            errors.append(f"broken local link at line {line}: {target}")


def validate_source_footer(
    path: Path,
    text: str,
    expected_source: Path | None,
    dispatch_id: str | None,
    research_source: Path | None,
    errors: list[str],
) -> None:
    footer_match = re.search(
        r"(?is)\*\*source dispatch(?::)?\*\*:?.*\Z",
        text.strip(),
    )
    if expected_source is None:
        if footer_match is not None:
            errors.append(
                "Source dispatch footer exists but no expected dispatch was supplied"
            )
        validate_research_link(path, text, research_source, errors)
        return
    if footer_match is None:
        errors.append("final Source dispatch footer is missing")
        return
    footer = footer_match.group(0)
    footer_id = re.search(
        r"(?is)^\*\*source dispatch(?::)?\*\*:?\s*`([^`]+)`",
        footer,
    )
    if footer_id is None or footer_id.group(1) != dispatch_id:
        errors.append("Source dispatch footer lacks the expected dispatch id")
    footer_targets = []
    for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", footer):
        target = link.split("#", 1)[0]
        if target and not re.match(r"^(?:https?|mailto):", target):
            footer_targets.append((path.parent / target).resolve())
    if expected_source not in footer_targets:
        errors.append(
            "Source dispatch footer does not link the exact expected findings path"
        )
    validate_research_link(path, text, research_source, errors)


def validate_research_link(
    path: Path,
    text: str,
    research_source: Path | None,
    errors: list[str],
) -> None:
    if research_source is None:
        return
    linked = {
        (path.parent / target.split("#", 1)[0]).resolve()
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        if target and not re.match(r"^(?:https?|mailto):", target)
    }
    if research_source not in linked:
        errors.append(
            "document does not link the exact explicitly resolved research source"
        )


if __name__ == "__main__":
    raise SystemExit(main())
