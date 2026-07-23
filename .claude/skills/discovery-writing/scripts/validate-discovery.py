#!/usr/bin/env python3
"""Validate deterministic discovery structure; semantic review remains reviewer-owned."""

from __future__ import annotations

import re
from datetime import datetime
from hashlib import sha256
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
ALLOWED_NATURE = {"explanatory", "reference", "technical"}
ALLOWED_STATUS = {"draft", "exploratory", "active", "consolidated", "evergreen"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ORDERED_HEADINGS = [
    "Objective",
    "1. Business Context",
    "2. Core Concepts",
    "Open Questions",
    "Decisions Baked In",
    "Connections",
    "Flow Diagram",
    "Appendix — Changelog",
]
LOCATION_TOKEN = re.compile(
    r"(?:"
    r"(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.[A-Za-z0-9]+:\d+"
    r"|[A-Z][A-Za-z0-9_]*\.[a-zA-Z_][A-Za-z0-9_]*"
    r"|(?:\[[^\]]+\]\([^)]+\)|(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+)"
    r"\s+§\s*[A-Za-z0-9][A-Za-z0-9.-]*"
    r")"
)


def main() -> int:
    parser = ArgumentParser(
        description=(
            "Validate deterministic discovery structure, exact provenance footer, "
            "local links, and trailing whitespace. Semantic linkage remains reviewer-owned."
        )
    )
    parser.add_argument("discovery", nargs="?")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run in-memory regression checks and exit.",
    )
    parser.add_argument(
        "--provenance-mode",
        choices=("dispatch", "basis", "none"),
    )
    parser.add_argument(
        "--expected-source",
        help="Exact dispatch findings path=sha256:<64-hex> binding.",
    )
    parser.add_argument("--dispatch-id")
    parser.add_argument(
        "--source-basis",
        action="append",
        default=[],
        help="Exact path=sha256:<64-hex> binding; repeat once per basis source.",
    )
    parser.add_argument(
        "--research-source",
        action="append",
        default=[],
        help="Exact path=sha256:<64-hex> binding linked before Connections; repeat as needed.",
    )
    args = parser.parse_args()

    if args.self_test:
        return run_self_tests()
    if not args.discovery:
        parser.error("discovery is required unless --self-test is used")
    if not args.provenance_mode:
        parser.error("--provenance-mode is required unless --self-test is used")
    validate_cli_contract(parser, args)
    path = Path(args.discovery).resolve()
    expected_binding = (
        parse_binding(parser, "--expected-source", args.expected_source)
        if args.expected_source
        else None
    )
    source_bindings = [
        parse_binding(parser, "--source-basis", item) for item in args.source_basis
    ]
    research_bindings = [
        parse_binding(parser, "--research-source", item)
        for item in args.research_source
    ]
    expected_source = expected_binding[0] if expected_binding else None
    source_basis = [item[0] for item in source_bindings]
    research_sources = [item[0] for item in research_bindings]

    required_bindings = [
        item
        for item in (expected_binding, *source_bindings, *research_bindings)
        if item is not None
    ]
    if not path.is_file():
        parser.error(f"discovery not found: {path}")
    for source, expected_hash in required_bindings:
        if not source.is_file():
            parser.error(f"source not found: {source}")
        source_bytes = source.read_bytes()
        actual_hash = sha256(source_bytes).hexdigest()
        if not hash_matches(expected_hash, source_bytes):
            parser.error(
                f"source hash mismatch: {source} "
                f"(expected {expected_hash}, got {actual_hash})"
            )

    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    outside_text, fences_balanced = text_outside_fences(lines)

    if not fences_balanced:
        errors.append("code fence or HTML comment is unclosed")
    validate_trailing_whitespace(lines, errors)
    validate_repo_path(path, errors)

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

    validate_heading_order(outside_text, errors)
    validate_objective(outside_text, errors)
    validate_business_context(outside_text, errors)
    validate_core_concepts(outside_text, errors)
    validate_open_questions(outside_text, errors)
    validate_decision_table(outside_text, errors)
    validate_connections_table(outside_text, errors)
    validate_flow(text, outside_text, errors)
    validate_changelog(outside_text, errors)
    validate_links(path, outside_text, errors)
    validate_research_links(path, outside_text, research_sources, errors)
    validate_source_footer(
        path,
        lines,
        args.provenance_mode,
        expected_source,
        args.dispatch_id,
        source_basis,
        errors,
    )

    if errors:
        for error in errors:
            print(f"[discovery] {path}: {error}")
        print(f"discovery validation: FAIL ({len(errors)} issue(s))")
        return 1

    heading_count = len(re.findall(r"(?m)^##\s+.+?\s*$", outside_text))
    print(
        "discovery validation: PASS "
        f"(frontmatter={len(keys)} keys, headings={heading_count}, "
        f"provenance={args.provenance_mode}; semantic review still required)"
    )
    return 0


def validate_cli_contract(parser: ArgumentParser, args: object) -> None:
    mode = args.provenance_mode
    has_dispatch_pair = bool(args.expected_source) and bool(args.dispatch_id)
    has_partial_dispatch = bool(args.expected_source) != bool(args.dispatch_id)

    if has_partial_dispatch:
        parser.error("--expected-source and --dispatch-id must be supplied together")
    if len(args.source_basis) != len(set(args.source_basis)):
        parser.error("--source-basis paths must not be duplicated")
    if len(args.research_source) != len(set(args.research_source)):
        parser.error("--research-source paths must not be duplicated")
    if mode == "dispatch":
        if not has_dispatch_pair:
            parser.error(
                "dispatch mode requires --expected-source and --dispatch-id"
            )
        if args.source_basis:
            parser.error("dispatch mode forbids --source-basis")
    elif mode == "basis":
        if has_dispatch_pair:
            parser.error("basis mode forbids --expected-source and --dispatch-id")
        if not args.source_basis:
            parser.error("basis mode requires at least one --source-basis")
    elif has_dispatch_pair or args.source_basis:
        parser.error(
            "none mode forbids --expected-source, --dispatch-id, and --source-basis"
        )


def parse_binding(
    parser: ArgumentParser,
    option: str,
    raw: str,
) -> tuple[Path, str]:
    path_text, separator, digest = raw.rpartition("=")
    if not digest.startswith("sha256:"):
        parser.error(f"{option} must use exact path=sha256:<64-hex> syntax")
    digest_value = digest.removeprefix("sha256:").lower()
    if (
        not separator
        or not path_text
        or re.fullmatch(r"[0-9a-f]{64}", digest_value) is None
    ):
        parser.error(f"{option} must use exact path=sha256:<64-hex> syntax")
    return Path(path_text).resolve(), digest_value


def hash_matches(expected_hash: str, data: bytes) -> bool:
    return sha256(data).hexdigest() == expected_hash


def text_outside_fences(lines: list[str]) -> tuple[str, bool]:
    outside: list[str] = []
    fence_char: str | None = None
    fence_length = 0
    in_comment = False
    for line in lines:
        if fence_char is not None:
            closing = re.match(
                rf"^ {{0,3}}{re.escape(fence_char)}{{{fence_length},}}\s*$",
                line,
            )
            if closing:
                fence_char = None
                fence_length = 0
            outside.append("")
            continue
        masked, in_comment = mask_html_comments(line, in_comment)
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", masked)
        if opening:
            fence_char = opening.group(1)[0]
            fence_length = len(opening.group(1))
            outside.append("")
        else:
            outside.append(masked)
    return "\n".join(outside), fence_char is None and not in_comment


def mask_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    visible: list[str] = []
    cursor = 0
    while cursor < len(line):
        if in_comment:
            close = line.find("-->", cursor)
            if close < 0:
                return "".join(visible), True
            in_comment = False
            cursor = close + 3
            continue
        opening = line.find("<!--", cursor)
        if opening < 0:
            visible.append(line[cursor:])
            break
        visible.append(line[cursor:opening])
        in_comment = True
        cursor = opening + 4
    return "".join(visible), in_comment


def validate_trailing_whitespace(lines: list[str], errors: list[str]) -> None:
    bad = [
        str(index)
        for index, line in enumerate(lines, 1)
        if re.search(r"[ \t]+$", line)
    ]
    if bad:
        errors.append(
            "trailing whitespace at line(s): " + ", ".join(bad)
        )


def validate_repo_path(path: Path, errors: list[str]) -> None:
    repo_root = find_repo_root(path)
    if repo_root is None:
        errors.append("target is not inside a Git repository")
        return
    relative = path.relative_to(repo_root).as_posix()
    allowed_path = (
        re.fullmatch(r"docs/features/[^/]+/discovery/[^/]+\.md", relative)
        or re.fullmatch(r"vault/discovery/[^/]+-definitions/[^/]+\.md", relative)
    )
    if allowed_path is None:
        errors.append(
            f"target path is outside the two allowed discovery shapes: {relative}"
        )


def find_repo_root(path: Path) -> Path | None:
    return next(
        (parent for parent in (path.parent, *path.parents) if (parent / ".git").exists()),
        None,
    )


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
    if not valid_date(scalar(frontmatter, "last_updated")):
        errors.append("last_updated must be a real calendar date in YYYY-MM-DD")


def valid_date(value: str) -> bool:
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is None:
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def h2_section(text: str, heading: str) -> str | None:
    match = re.search(
        rf"(?ims)^##\s+{re.escape(heading)}\s*$.*?(?=^##\s+|\Z)",
        text,
    )
    return match.group(0) if match else None


def raw_h2_section(raw_text: str, outside_text: str, heading: str) -> str | None:
    raw_lines = raw_text.splitlines()
    outside_lines = outside_text.splitlines()
    start = next(
        (
            index
            for index, line in enumerate(outside_lines)
            if re.fullmatch(rf"##\s+{re.escape(heading)}\s*", line)
        ),
        None,
    )
    if start is None:
        return None
    end = next(
        (
            index
            for index, line in enumerate(outside_lines[start + 1:], start + 1)
            if re.match(r"^##\s+", line)
        ),
        len(raw_lines),
    )
    return "\n".join(raw_lines[start:end])


def validate_heading_order(text: str, errors: list[str]) -> None:
    headings = [
        match.group(1).strip()
        for match in re.finditer(r"(?m)^##\s+(.+?)\s*$", text)
    ]
    if headings and headings[0] != "Objective":
        errors.append("Objective must be the first H2 heading")
    if headings and headings[-1] != "Appendix — Changelog":
        errors.append("Appendix — Changelog must be the final H2 heading")
    cursor = -1
    for required in ORDERED_HEADINGS:
        occurrences = [
            index for index, heading in enumerate(headings) if heading == required
        ]
        if not occurrences:
            errors.append(f"required exact H2 heading is missing: {required}")
            continue
        if len(occurrences) > 1:
            errors.append(f"required H2 heading is duplicated: {required}")
        found = next((index for index in occurrences if index > cursor), None)
        if found is None:
            errors.append(f"required H2 heading is misplaced: {required}")
        else:
            cursor = found


def prose_sentence_count(prose: str) -> int:
    prose = re.sub(r"\s+", " ", prose).strip()
    if not prose:
        return 0
    return len(
        [
            item
            for item in re.split(r"(?<=[.!?])\s+", prose)
            if item.strip()
        ]
    )


def validate_objective(text: str, errors: list[str]) -> None:
    objective = h2_section(text, "Objective")
    if objective is None:
        return
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

    body = re.sub(r"(?m)^##\s+Objective\s*$", "", objective, count=1)
    body = body.split("**Status:**", 1)[0]
    body = re.sub(r"(?m)^\s*<!--.*?-->\s*$", "", body)
    count = prose_sentence_count(body)
    if count == 0:
        errors.append("Objective must contain non-empty prose before the Status block")
    elif count > 3:
        errors.append(f"Objective must contain at most 3 sentences; found {count}")


def subsection_content(
    block: str,
    start_pattern: str,
    end_pattern: str | None,
) -> str | None:
    end = rf"(?=^{end_pattern}|\Z)" if end_pattern else r"(?=\Z)"
    match = re.search(
        rf"(?ims)^{start_pattern}\s*(?:—\s*)?(.*?){end}",
        block,
    )
    return match.group(1).strip() if match else None


def validate_business_context(text: str, errors: list[str]) -> None:
    business = h2_section(text, "1. Business Context")
    if business is None:
        return
    why_marker = r"\*\*Why now\*\*"
    broken_marker = r"\*\*What's broken \(as of \d{4}-\d{2}-\d{2}\)\*\*"
    stays_marker = r"\*\*What stays the same\*\*"
    why = subsection_content(business, why_marker, broken_marker)
    broken = subsection_content(business, broken_marker, stays_marker)
    stays = subsection_content(business, stays_marker, None)

    if why is None:
        errors.append("Business Context requires exact subsection **Why now**")
    elif not re.search(r"\w", why):
        errors.append("Why now must be non-empty")
    if broken is None:
        errors.append(
            "Business Context requires dated subsection "
            "**What's broken (as of YYYY-MM-DD)**"
        )
    elif not re.search(r"\w", broken):
        errors.append("What's broken must be non-empty")
    else:
        entries = broken_entries(broken)
        for index, entry in enumerate(entries, 1):
            if LOCATION_TOKEN.search(entry) is None:
                errors.append(
                    f"What's broken entry {index} lacks a strict location "
                    "(file:line, Class.method, or doc §section)"
                )
    date_match = re.search(
        r"\*\*What's broken \(as of (\d{4}-\d{2}-\d{2})\)\*\*",
        business,
    )
    if date_match is not None and not valid_date(date_match.group(1)):
        errors.append("What's broken snapshot must use a real calendar date")
    if stays is None:
        errors.append("Business Context requires exact subsection **What stays the same**")
    elif not re.search(r"[A-Za-z0-9]", stays):
        errors.append("What stays the same must be non-empty")


def broken_entries(block: str) -> list[str]:
    bullets = [
        match.group(0).strip()
        for match in re.finditer(
            r"(?ms)^\s*(?:[-*+]|\d+\.)\s+.*?"
            r"(?=^\s*(?:[-*+]|\d+\.)\s+|^\s*\|.*\|\s*$|\Z)",
            block,
        )
    ]
    table_entries: list[str] = []
    table_group: list[str] = []
    for line in (*block.splitlines(), ""):
        if re.match(r"^\s*\|.*\|\s*$", line):
            table_group.append(line.strip())
            continue
        if table_group:
            non_separator = [
                item
                for item in table_group
                if not all(
                    re.fullmatch(r":?-{3,}:?", cell.strip())
                    for cell in item.strip("|").split("|")
                )
            ]
            table_entries.extend(non_separator[1:])
            table_group = []
    entries = bullets + table_entries
    return entries if entries else [block.strip()]


def validate_core_concepts(text: str, errors: list[str]) -> None:
    core = h2_section(text, "2. Core Concepts")
    if core is None:
        return
    headings = re.findall(r"(?m)^###\s+(.+?)\s*$", core)
    if not headings:
        errors.append("Core Concepts requires at least one PascalCase H3 heading")
        return
    invalid = [
        heading
        for heading in headings
        if re.fullmatch(r"[A-Z][A-Za-z0-9]*", heading) is None
    ]
    if invalid:
        errors.append(
            "Core Concepts H3 headings must be bare PascalCase names; invalid: "
            + ", ".join(invalid)
        )


def validate_open_questions(text: str, errors: list[str]) -> None:
    block = h2_section(text, "Open Questions")
    if block is None:
        return
    id_matches = list(
        re.finditer(
            r"(?m)^(?:#{3,6}\s+|\d+\.\s+|[-*]\s+)?(OQ-[A-Za-z0-9]+)\b",
            block,
        )
    )
    oq_ids = [match.group(1) for match in id_matches]
    no_questions = re.fullmatch(
        r"(?is)##\s+Open Questions\s*\n+\s*No open questions\.\s*",
        block,
    )
    if not oq_ids and no_questions is None:
        errors.append(
            "Open Questions must contain OQ identifiers or exactly 'No open questions.'"
        )
    if len(oq_ids) != len(set(oq_ids)):
        errors.append("Open Questions identifiers must be unique")
    for index, match in enumerate(id_matches):
        end = id_matches[index + 1].start() if index + 1 < len(id_matches) else len(block)
        entry = block[match.start():end]
        for marker in ("**Question:**", "**Recommendation:**"):
            if marker not in entry:
                errors.append(f"{match.group(1)} is missing {marker}")
        if re.search(r"(?i)settle(?:ment)? (?:in|stage)", entry) is None:
            errors.append(f"{match.group(1)} is missing a settlement stage")


def table_rows(block: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in block.splitlines():
        if not re.match(r"^\s*\|.*\|\s*$", line):
            continue
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def has_table_header(block: str, expected: tuple[str, ...]) -> bool:
    expected_lower = tuple(item.lower() for item in expected)
    return any(
        tuple(cell.lower() for cell in row) == expected_lower
        for row in table_rows(block)
    )


def table_data_rows(block: str, expected_header: tuple[str, ...]) -> list[list[str]]:
    expected_lower = tuple(item.lower() for item in expected_header)
    lines = block.splitlines()
    for index, line in enumerate(lines):
        if not re.match(r"^\s*\|.*\|\s*$", line):
            continue
        row = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if tuple(cell.lower() for cell in row) != expected_lower:
            continue
        result: list[list[str]] = []
        for candidate_line in lines[index + 1:]:
            if not re.match(r"^\s*\|.*\|\s*$", candidate_line):
                break
            candidate = [
                cell.strip()
                for cell in candidate_line.strip().strip("|").split("|")
            ]
            if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in candidate):
                result.append(candidate)
        return result
    return []


def validate_decision_table(text: str, errors: list[str]) -> None:
    block = h2_section(text, "Decisions Baked In")
    header = ("ID", "Decision", "Where")
    if block is not None and not has_table_header(block, header):
        errors.append(
            "Decisions Baked In requires exact table header | ID | Decision | Where |"
        )
        return
    if block is None:
        return
    rows = table_data_rows(block, header)
    no_decisions = [["—", "No decisions ratified.", "—"]]
    if rows == no_decisions:
        return
    if not rows:
        errors.append(
            "Decisions Baked In requires a decision row or exact "
            "| — | No decisions ratified. | — | row"
        )
        return
    for row in rows:
        if len(row) != 3 or re.fullmatch(r"[A-Z]+D-\d+", row[0]) is None:
            errors.append(f"invalid decision row: {' | '.join(row)}")
        elif not row[1] or re.search(r"§\s*\d", row[2]) is None:
            errors.append(
                f"decision {row[0]} requires non-empty text and a Where §section"
            )


def validate_connections_table(text: str, errors: list[str]) -> None:
    block = h2_section(text, "Connections")
    if block is not None and not has_table_header(
        block, ("Document", "Type", "Description")
    ):
        errors.append(
            "Connections requires exact table header "
            "| Document | Type | Description |"
        )


def validate_flow(raw_text: str, outside_text: str, errors: list[str]) -> None:
    block = h2_section(outside_text, "Flow Diagram")
    if block is None:
        return
    raw_block = raw_h2_section(raw_text, outside_text, "Flow Diagram")
    mermaid_bodies = extract_mermaid_bodies(raw_block or "")
    if len(mermaid_bodies) != 1:
        errors.append(
            "Flow Diagram must contain exactly one Mermaid fence before the changelog"
        )
    elif not any(
        line.strip() and not line.lstrip().startswith("%%")
        for line in mermaid_bodies[0].splitlines()
    ):
        errors.append(
            "Flow Diagram Mermaid fence requires at least one non-comment statement"
        )
    body = re.sub(r"(?m)^##\s+Flow Diagram\s*$", "", block, count=1).strip()
    if not re.search(r"[A-Za-z0-9]", body):
        errors.append("Flow Diagram requires a non-empty explanatory paragraph")
        return
    count = prose_sentence_count(body)
    if count > 4:
        errors.append(
            f"Flow Diagram explanatory paragraph must be at most 4 sentences; found {count}"
        )


def extract_mermaid_bodies(block: str) -> list[str]:
    bodies: list[str] = []
    lines = block.splitlines()
    index = 0
    while index < len(lines):
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})mermaid\s*$", lines[index])
        if opening is None:
            index += 1
            continue
        marker = opening.group(1)[0]
        length = len(opening.group(1))
        body: list[str] = []
        index += 1
        while index < len(lines):
            if re.match(
                rf"^ {{0,3}}{re.escape(marker)}{{{length},}}\s*$",
                lines[index],
            ):
                bodies.append("\n".join(body))
                break
            body.append(lines[index])
            index += 1
        index += 1
    return bodies


def validate_changelog(text: str, errors: list[str]) -> None:
    block = h2_section(text, "Appendix — Changelog")
    if block is None:
        return
    body = re.sub(
        r"(?m)^##\s+Appendix — Changelog\s*$",
        "",
        block,
        count=1,
    )
    footer_at = re.search(r"(?m)^\*\*Source (?:dispatch|basis):\*\*", body)
    if footer_at:
        body = body[: footer_at.start()]
    header = ("Version", "Date", "Changes")
    if not has_table_header(body, header):
        errors.append(
            "Appendix — Changelog requires exact table header "
            "| Version | Date | Changes |"
        )
        return
    rows = table_data_rows(body, header)
    if not rows:
        errors.append("Appendix — Changelog requires at least one data row")
        return
    for row in rows:
        if (
            len(row) != 3
            or re.fullmatch(r"v?\d+\.\d+\.\d+", row[0]) is None
            or not valid_date(row[1])
            or not re.search(r"\w", row[2])
        ):
            errors.append(
                "each changelog row requires semver, real YYYY-MM-DD date, "
                f"and non-empty change text: {' | '.join(row)}"
            )


def local_link_targets(path: Path, text: str) -> list[Path]:
    targets: list[Path] = []
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = target.split("#", 1)[0]
        if not target or re.match(r"^(?:https?|mailto):", target):
            continue
        targets.append((path.parent / target).resolve())
    return targets


def validate_links(path: Path, text: str, errors: list[str]) -> None:
    repo_root = find_repo_root(path)
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).split("#", 1)[0]
        if not target or re.match(r"^(?:https?|mailto):", target):
            continue
        if Path(target).is_absolute():
            line = text[: match.start()].count("\n") + 1
            errors.append(f"local link must be relative at line {line}: {target}")
            continue
        resolved = (path.parent / target).resolve()
        if repo_root is not None:
            try:
                resolved.relative_to(repo_root)
            except ValueError:
                line = text[: match.start()].count("\n") + 1
                errors.append(
                    f"local link escapes repository at line {line}: {target}"
                )
                continue
        if not resolved.exists():
            line = text[: match.start()].count("\n") + 1
            errors.append(f"broken local link at line {line}: {target}")


def validate_research_links(
    path: Path,
    text: str,
    research_sources: list[Path],
    errors: list[str],
) -> None:
    if not research_sources:
        return
    owner_area = text.split("## Connections", 1)[0]
    linked = set(local_link_targets(path, owner_area))
    for research_source in research_sources:
        if research_source not in linked:
            errors.append(
                "research source is not linked in a substantive provenance-owner "
                f"location before Connections: {research_source}"
            )


def validate_source_footer(
    path: Path,
    lines: list[str],
    mode: str,
    expected_source: Path | None,
    dispatch_id: str | None,
    source_basis: list[Path],
    errors: list[str],
) -> None:
    outside_text, _ = text_outside_fences(lines)
    outside_lines = outside_text.splitlines()
    nonempty = [(index, line) for index, line in enumerate(outside_lines) if line.strip()]
    footer_lines = [
        (index, line)
        for index, line in nonempty
        if re.match(r"(?i)^\*\*Source (?:dispatch|basis):\*\*", line.strip())
    ]
    last_line = nonempty[-1][1].strip() if nonempty else ""

    expected_footer_kind = None if mode == "none" else mode
    if expected_footer_kind is None:
        if footer_lines:
            errors.append("none mode forbids Source dispatch and Source basis footers")
        return
    if len(footer_lines) != 1:
        errors.append(
            f"{mode} mode requires exactly one Source {mode} footer outside code fences"
        )
        return
    footer_index, footer = footer_lines[0]
    if footer_index != nonempty[-1][0]:
        errors.append(f"Source {mode} footer must be the final non-empty line")
        return
    if footer.strip() != last_line:
        errors.append(f"Source {mode} footer must be terminal")

    if mode == "dispatch":
        match = re.fullmatch(
            r"\*\*Source dispatch:\*\* `([^`]+)` — \[([^\]]+)\]\(([^)]+)\)",
            footer.strip(),
        )
        if match is None:
            errors.append(
                "Source dispatch footer must exactly match "
                "**Source dispatch:** `<id>` — [findings](<relative-path>)"
            )
            return
        if match.group(1) != dispatch_id:
            errors.append("Source dispatch footer lacks the expected dispatch id")
        target = match.group(3).split("#", 1)[0]
        if not relative_link_within_repo(path, target):
            errors.append(
                "Source dispatch footer link must be relative and resolve within the repository"
            )
            return
        resolved = (path.parent / target).resolve()
        if resolved != expected_source:
            errors.append(
                "Source dispatch footer does not link the exact expected findings path"
            )
        return

    match = re.fullmatch(r"\*\*Source basis:\*\* (.+)", footer.strip())
    if match is None:
        errors.append(
            "Source basis footer must exactly start with **Source basis:**"
        )
        return
    parts = [part.strip() for part in match.group(1).split(";")]
    if any(
        re.fullmatch(r"\[[^\]]+\]\([^)]+\)", part) is None
        for part in parts
    ):
        errors.append(
            "Source basis footer must contain only semicolon-separated Markdown links"
        )
        return
    for part in parts:
        target_match = re.fullmatch(r"\[[^\]]+\]\(([^)]+)\)", part)
        assert target_match is not None
        if not relative_link_within_repo(path, target_match.group(1).split("#", 1)[0]):
            errors.append(
                "Source basis footer links must be relative and resolve within the repository"
            )
            return
    resolved = local_link_targets(path, "\n".join(parts))
    if len(resolved) != len(set(resolved)):
        errors.append("Source basis footer contains duplicate paths")
    if set(resolved) != set(source_basis) or len(resolved) != len(source_basis):
        errors.append(
            "Source basis footer must link every and only the supplied --source-basis paths"
        )


def relative_link_within_repo(path: Path, target: str) -> bool:
    if not target or Path(target).is_absolute():
        return False
    repo_root = find_repo_root(path)
    if repo_root is None:
        return False
    try:
        (path.parent / target).resolve().relative_to(repo_root)
    except ValueError:
        return False
    return True


def run_self_tests() -> int:
    failures: list[str] = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            failures.append(name)

    outside, balanced = text_outside_fences(
        ["~~~mermaid", "## spoof", "~~~~", "## Objective"]
    )
    check("tilde fence matching", balanced and "## spoof" not in outside)
    _, balanced = text_outside_fences(["````", "~~~", "```"])
    check("fence type and length mismatch rejection", not balanced)
    hidden, balanced = text_outside_fences(
        ["<!--", "**Source dispatch:** `spoof` — [x](x.md)", "-->", "visible"]
    )
    check(
        "HTML comment masking",
        balanced and "Source dispatch" not in hidden and "visible" in hidden,
    )
    _, balanced = text_outside_fences(["<!-- unclosed"])
    check("unclosed HTML comment rejection", not balanced)
    check("nature exact contract", "procedural" not in ALLOWED_NATURE)
    check("real calendar dates", valid_date("2026-07-23") and not valid_date("2026-02-30"))
    test_parser = ArgumentParser(add_help=False)
    _, parsed_digest = parse_binding(
        test_parser,
        "--source-basis",
        "source.md=sha256:" + ("a" * 64),
    )
    check("path-hash binding syntax", parsed_digest == "a" * 64)
    check(
        "source hash recomputation",
        hash_matches(sha256(b"source").hexdigest(), b"source")
        and not hash_matches("0" * 64, b"source"),
    )
    check(
        "strict locations",
        LOCATION_TOKEN.search("src/a.py:12") is not None
        and LOCATION_TOKEN.search("ClassName.method") is not None
        and LOCATION_TOKEN.search("design.md §2.1") is not None
        and LOCATION_TOKEN.search("src/a.py") is None,
    )
    entries = broken_entries(
        "- Broken at src/a.py:12.\n- Missing strict location.\n"
    )
    check(
        "per-broken-entry location",
        len(entries) == 2
        and LOCATION_TOKEN.search(entries[0]) is not None
        and LOCATION_TOKEN.search(entries[1]) is None,
    )

    errors: list[str] = []
    validate_heading_order(
        "## Preface\nx\n## Objective\nx\n## Appendix — Changelog\nx",
        errors,
    )
    check("Objective first H2", any("first H2" in item for item in errors))
    errors = []
    validate_heading_order(
        "## Objective\nx\n## Appendix — Changelog\nx\n## Extra\nx",
        errors,
    )
    check("no H2 after ending", any("final H2" in item for item in errors))

    errors = []
    validate_open_questions(
        "## Open Questions\nOQ-X1\n**Question:** Q?\n"
        "**Recommendation:** R.\nSettlement stage: SPEC.\n"
        "OQ-X2\n**Question:** Q?\n## Decisions Baked In\n",
        errors,
    )
    check(
        "per-OQ fields",
        any("OQ-X2 is missing **Recommendation:**" in item for item in errors)
        and any("OQ-X2 is missing a settlement stage" in item for item in errors),
    )

    errors = []
    validate_decision_table(
        "## Decisions Baked In\n| ID | Decision | Where |\n"
        "| --- | --- | --- |\n| — | No decisions ratified. | — |\n",
        errors,
    )
    check("exact no-decisions row", not errors)
    errors = []
    validate_decision_table(
        "## Decisions Baked In\n| ID | Decision | Where |\n"
        "| --- | --- | --- |\n",
        errors,
    )
    check("decision row required", bool(errors))

    one_flow = (
        "## Flow Diagram\n~~~mermaid\nflowchart TD\nA-->B\n~~~\n"
        "This paragraph explains the flow.\n## Appendix — Changelog\n"
    )
    outside, _ = text_outside_fences(one_flow.splitlines())
    errors = []
    validate_flow(one_flow, outside, errors)
    check("exactly one Mermaid fence", not errors)
    two_flows = one_flow.replace(
        "This paragraph",
        "```mermaid\nflowchart TD\nB-->C\n```\nThis paragraph",
    )
    outside, _ = text_outside_fences(two_flows.splitlines())
    errors = []
    validate_flow(two_flows, outside, errors)
    check("duplicate Mermaid rejection", any("exactly one" in item for item in errors))
    empty_flow = (
        "## Flow Diagram\n```mermaid\n%% only a comment\n```\n"
        "This paragraph explains the flow.\n## Appendix — Changelog\n"
    )
    outside, _ = text_outside_fences(empty_flow.splitlines())
    errors = []
    validate_flow(empty_flow, outside, errors)
    check(
        "empty Mermaid rejection",
        any("non-comment statement" in item for item in errors),
    )

    errors = []
    validate_changelog(
        "## Appendix — Changelog\n| Version | Date | Changes |\n"
        "| --- | --- | --- |\n| 1.2.3 | 2026-02-30 | Changed. |\n",
        errors,
    )
    check("changelog date validation", bool(errors))
    errors = []
    validate_changelog(
        "## Appendix — Changelog\n| Version | Date | Changes |\n"
        "| --- | --- | --- |\n| 1.2.3 | 2026-07-23 | Changed. |\n",
        errors,
    )
    check("changelog valid row", not errors)

    errors = []
    objective = (
        "## Objective\nOne. Two. Three. Four.\n\n"
        "**Status:** v1\n**Owner:** @owner\n"
    )
    validate_objective(objective, errors)
    check("Objective sentence ceiling", any("at most 3" in item for item in errors))

    repo_root = find_repo_root(Path(__file__).resolve())
    if repo_root is not None:
        discovery = repo_root / "docs/features/x/discovery/y.md"
        check(
            "relative provenance containment",
            relative_link_within_repo(discovery, "../../../source.md")
            and not relative_link_within_repo(discovery, "../../../../../../outside.md"),
        )
        errors = []
        validate_source_footer(
            discovery,
            [
                "```text",
                "**Source dispatch:** `spoof` — [findings](../../../source.md)",
                "```",
                "ordinary terminal text",
            ],
            "none",
            None,
            None,
            [],
            errors,
        )
        check("fenced footer spoof ignored", not errors)
        errors = []
        validate_source_footer(
            discovery,
            [
                "<!--",
                "**Source dispatch:** `spoof` — [findings](../../../source.md)",
                "-->",
                "ordinary terminal text",
            ],
            "none",
            None,
            None,
            [],
            errors,
        )
        check("HTML-comment footer spoof ignored", not errors)

    if failures:
        for failure in failures:
            print(f"[self-test] FAIL: {failure}")
        print(f"validator self-test: FAIL ({len(failures)} issue(s))")
        return 1
    print("validator self-test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
