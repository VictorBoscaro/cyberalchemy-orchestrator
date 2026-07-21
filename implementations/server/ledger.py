"""Reader for the append-only ledger of subagent dispatches.

Mirrors the line forms written by `register-dispatch/append-dispatch.cjs`:
every non-comment line is `dispatches:`, a row start `  - key: <json>`, or a
continuation `    key: <json>`. Every value is JSON.

TWO PRINCIPLES this module follows:

1. **Structural only.** Rows written under pre-v0.5.2 schemas are historical
   artifacts and are never re-validated semantically — they carry old keys
   (`status`, top-level `agents`, `corpus`, ...) and keep passing.

2. **Lenient by default — unlike the appender.** The appender is strict because
   it *protects* the file: it refuses to write into a corrupted ledger. The
   reader has the opposite job — show what's there. Real ledgers contain old
   prettified rows (multi-line JSON, trailing commas) that the appender would
   reject; losing a repo's entire history over one such row would be worse than
   displaying it. In lenient mode an unreadable row becomes a warning and is
   skipped; the rest of the ledger is served.

This module NEVER writes. The ledger is append-only and belongs to the appender.

CONVENTION (scoped to objects with ROW SHAPE): in an object that shares a ledger
row's namespace, every field computed by this reader carries a `_` prefix. This
isn't cosmetic — the `status` key really exists on pre-v0.5.2 rows, so a computed
field named `status` would overwrite the historical data; the `_` guarantees a
computed field never collides with a key from the ledger's own namespace. The rule
does NOT apply to container/aggregate objects that are not rows and have no such
namespace to protect (`summarize_repo` returns `total`, `open`, `by_type`, ...
without a prefix on purpose — there's no ledger key to shadow there).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# Like the appender (append-dispatch.cjs:315), but with the value optional: old
# prettified rows open the value on the next line (`    agents:`).
ROW_RE = re.compile(r"^(  - |    )([A-Za-z_][A-Za-z0-9_]*):(?: (.*))?$")

LEDGER_RELPATH = Path("telemetry") / "agents" / "subagents-dispatch.yaml"
PENDING_RELPATH = Path("telemetry") / "agents" / "pending"

# Only these three are dispatchable under v0.6.0; the rest are reserved names.
LIVE_TYPES = {"research", "review", "experiment"}

# Bucket for dispatches without a `dispatch_type` (pre-v0.5.2 rows lack the field).
# An explicit label rather than `None` because the key becomes a chart column and a
# legend in the UI — and `null` as a series name is worse than a word.
NO_TYPE = "(no type)"

# A day span larger than this almost certainly comes from a corrupted date (a
# row with `1970-01-01` would generate ~20k buckets). See `daily_series`.
MAX_SPAN_DAYS = 1000

_MISSING = object()

_ISO_DAY_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")


class LedgerError(Exception):
    """The ledger is structurally corrupted (only raised in strict mode)."""


@dataclass
class ParseResult:
    rows: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _loads(text: str) -> tuple[Any, str | None]:
    """JSON, tolerating a trailing comma (legal in YAML flow, illegal in JSON)."""
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        cleaned = re.sub(r",(\s*[\]}])", r"\1", text)
        if cleaned != text:
            try:
                return json.loads(cleaned), "trailing comma tolerated"
            except json.JSONDecodeError:
                pass
        return _MISSING, str(exc)


def parse_ledger(text: str, *, lenient: bool = True) -> ParseResult:
    """Converts the ledger text into raw rows, in file order.

    In strict mode it raises `LedgerError` at the first problem (the appender's
    semantics). In lenient mode it accumulates warnings and carries on.
    """
    result = ParseResult()
    current: dict[str, Any] | None = None
    lines = text.split("\n")
    i = 0

    def problem(lineno: int, why: str) -> None:
        if not lenient:
            raise LedgerError(f"line {lineno}: {why}")
        result.warnings.append(f"line {lineno}: {why}")

    while i < len(lines):
        lineno = i + 1
        line = lines[i].rstrip("\r")  # tolerates CRLF conversion
        i += 1

        if line == "" or line.startswith("#") or line == "dispatches:":
            continue

        match = ROW_RE.match(line)
        if not match:
            problem(lineno, "unrecognized line form")
            continue

        indent, key, inline = match.groups()

        # Possibly multi-line value: accumulate until it becomes valid JSON or
        # until the next row line.
        buffer = inline if inline is not None else ""
        value, err = (_MISSING, "empty value")
        if buffer.strip():
            value, err = _loads(buffer)
        while value is _MISSING and i < len(lines):
            nxt = lines[i].rstrip("\r")
            if ROW_RE.match(nxt):
                break  # another key started — the value never closed
            buffer += "\n" + nxt
            i += 1
            if buffer.strip():
                value, err = _loads(buffer)

        if value is _MISSING:
            problem(lineno, f'value of "{key}" is not valid JSON ({err})')
            continue
        if err:
            result.warnings.append(f'line {lineno}: "{key}" — {err}')

        if indent == "  - ":
            if key not in ("dispatch_id", "close_of"):
                problem(lineno, f'row must start with dispatch_id or close_of, got "{key}"')
                current = None
                continue
            current = {key: value}
            result.rows.append(current)
        else:
            if current is None:
                problem(lineno, "continuation before any row")
                continue
            current[key] = value

    return result


def join_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Match each dispatch row with its close row (the two-append discipline).

    Returns oldest first. A dispatch without a close row is open; an orphan close
    row (dispatch never registered) is a break of the upstream discipline and is
    exposed as such rather than silenced.
    """
    dispatches: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    closes: dict[str, dict[str, Any]] = {}

    for row in rows:
        if "dispatch_id" in row:
            did = row["dispatch_id"]
            # An id is contractually a non-empty string (append-dispatch.cjs:145).
            # A row whose `dispatch_id` parsed to a JSON list/object is not
            # hashable and, used as a dict key, would raise TypeError — bringing
            # down the ENTIRE parse of the repo (join_rows runs before the cache)
            # and 500ing every endpoint. Skipping the row honors Principle 1 (an
            # unreadable row becomes a warning and is skipped; the rest is served).
            if not isinstance(did, str):
                continue
            if did not in dispatches:
                order.append(did)
            dispatches[did] = row
        elif "close_of" in row:
            close_of = row["close_of"]
            if not isinstance(close_of, str):
                continue
            closes[close_of] = row

    joined: list[dict[str, Any]] = []
    for did in order:
        row = dict(dispatches[did])
        close = closes.get(did)
        row["_close"] = close
        row["_state"] = "closed" if close else "open"
        # Pre-v0.5.2 rows lack `groups`; we mark rather than try to adapt.
        row["_legacy"] = "groups" not in row
        row["_live"] = row.get("dispatch_type") in LIVE_TYPES
        row["_agent_count"] = count_agents(row)
        joined.append(row)

    for close_of, close in closes.items():
        if close_of not in dispatches:
            joined.append(
                {
                    "dispatch_id": close_of,
                    "goal": "(orphan close row — the dispatch row was never written)",
                    "_orphan_close": True,
                    "_close": close,
                    "_state": "closed",
                    "_legacy": True,
                    "_live": False,
                    "_agent_count": 0,
                }
            )

    return joined


def count_agents(row: dict[str, Any]) -> int:
    groups = row.get("groups")
    if not isinstance(groups, list):
        return 0
    return sum(
        len(g["agents"])
        for g in groups
        if isinstance(g, dict) and isinstance(g.get("agents"), list)
    )


# ---------------------------------------------------------------------------
# Parse cache
# ---------------------------------------------------------------------------


@dataclass
class RepoRows:
    """A repo's ledger already parsed and joined, plus the read context."""

    rows: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ledger_exists: bool = False
    error: str | None = None


# ledger path -> (fingerprint, RepoRows). Process memo, no expiry: the key IS
# already the content (mtime_ns + size), so hitting a stale entry is impossible.
# The memory ceiling is the number of observed repos. The key ASSUMES every write
# changes the file size — true for the append-only appender, which always appends a
# row. An out-of-band edit that preserved the exact size could serve stale until
# the next append.
_CACHE: dict[str, tuple[tuple[int, int] | None, RepoRows]] = {}

# Counter of real parses. Exists so the test can prove the cache hit — without it
# "didn't reparse" would only be observable by time, which is a fragile metric.
_parse_count = 0


def clear_cache() -> None:
    """Empties the memo. Only tests need it: in production the fingerprint suffices."""
    global _parse_count
    _CACHE.clear()
    _parse_count = 0


def parse_count() -> int:
    """How many real parses have happened since the last `clear_cache`."""
    return _parse_count


def _fingerprint(path: Path) -> tuple[int, int] | None:
    """The SAME fingerprint `signature` uses — mtime_ns + size, or None."""
    try:
        stat = path.stat()
    except OSError:
        return None
    return (stat.st_mtime_ns, stat.st_size)


def load_repo_rows(repo: Path, *, copy: bool = True) -> RepoRows:
    """A repo's joined rows, reparsing only when the file changed.

    A full parse of the largest real ledger (~1.5 MB) costs hundreds of ms, and
    `/api/stream` hits the disk every second while the new aggregations need the
    ENTIRE ledger (truncating by `limit` is no longer an escape). Without a memo,
    the per-request cost would grow with history — which is append-only and only
    grows.

    `copy=True` returns the TOP-level dicts copied, so the receiver can annotate
    fields (`_repo`, ...) without contaminating the cache. The copy is shallow on
    purpose: the nested values (`groups`, `connections`) weigh almost everything,
    and no function in this module edits them in-place — `truncate_prompts` and
    `slim` rebuild what they touch. A deep copy here would cost more than the parse
    the cache saves.

    The REAL guarantee of `copy=False`: the VALUES (top-level and nested dicts) are
    shared with the cache — safe thanks to the copy-on-write discipline of every
    writer in this module, which rebuilds what it touches rather than mutating —
    but the list CONTAINER is private per caller (a shallow `list(rows)` copy).
    Without it, a `data.rows.reverse()`/`.sort()` in any caller would permanently
    corrupt the chronological order the cache serves to `read_repo`,
    `first_day`/`last_day` and `daily_series`. The list copy is O(n) of pointers,
    cheap next to the parse — it closes the container-mutation hole without touching
    the ~1.5 MB of nested values.
    """
    global _parse_count

    ledger_path = repo / LEDGER_RELPATH
    key = str(ledger_path)
    fingerprint = _fingerprint(ledger_path)

    cached = _CACHE.get(key)
    if cached is not None and cached[0] == fingerprint:
        data = cached[1]
    else:
        data = _read_repo_rows(ledger_path)
        _parse_count += 1
        _CACHE[key] = (fingerprint, data)

    if not copy:
        # Values shared, list container private per caller.
        return RepoRows(
            rows=list(data.rows),
            warnings=data.warnings,
            ledger_exists=data.ledger_exists,
            error=data.error,
        )
    return RepoRows(
        rows=[dict(row) for row in data.rows],
        warnings=list(data.warnings),
        ledger_exists=data.ledger_exists,
        error=data.error,
    )


def _read_repo_rows(ledger_path: Path) -> RepoRows:
    """Raw read of a ledger. A missing ledger is not an error — it's a new repo."""
    if not ledger_path.is_file():
        return RepoRows(ledger_exists=False)
    try:
        text = ledger_path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return RepoRows(ledger_exists=True, error=str(exc))
    parsed = parse_ledger(text)
    return RepoRows(
        rows=join_rows(parsed.rows),
        warnings=parsed.warnings,
        ledger_exists=True,
    )


def truncate_prompts(row: dict[str, Any], limit: int) -> dict[str, Any]:
    """Shrinks the `initial_prompt`s for the listing. The detail view serves the full text."""
    groups = row.get("groups")
    if not isinstance(groups, list):
        return row

    trimmed_groups = []
    truncated_any = False
    for group in groups:
        if not isinstance(group, dict):
            trimmed_groups.append(group)
            continue
        group = dict(group)
        agents = []
        for agent in group.get("agents", []) or []:
            if isinstance(agent, dict) and isinstance(agent.get("initial_prompt"), str):
                agent = dict(agent)
                prompt = agent["initial_prompt"]
                if len(prompt) > limit:
                    agent["initial_prompt"] = prompt[:limit] + "…"
                    agent["_prompt_truncated"] = True
                    truncated_any = True
            agents.append(agent)
        group["agents"] = agents
        trimmed_groups.append(group)

    row = dict(row)
    row["groups"] = trimmed_groups
    row["_prompts_truncated"] = truncated_any
    return row


def read_pending(repo: Path) -> list[dict[str, Any]]:
    """Reads the pre-confirm sheets from `telemetry/agents/pending/*.json`.

    This is the NEW control-plane artifact: the sheet the human reviews before
    confirming. It's not part of the ledger and is the only editable surface.
    """
    pending_dir = repo / PENDING_RELPATH
    if not pending_dir.is_dir():
        return []

    sheets: list[dict[str, Any]] = []
    for path in sorted(pending_dir.glob("*.json")):
        entry: dict[str, Any] = {
            "_file": path.name,
            "_path": str(path),
            "_mtime": None,
            "_error": None,
        }
        try:
            # `stat` INSIDE the guard, alongside the read: the pending dir is the
            # only editable surface, so a sheet can be deleted/renamed between the
            # `glob` above and the `stat` here. Outside the guard that OSError would
            # bubble up as a 500 in /api/snapshot, /api/overview AND /api/repo, and
            # would even kill the SSE generator — taking down every connected UI. A
            # sheet that vanishes mid-scan degrades to an entry with `_error`.
            entry["_mtime"] = path.stat().st_mtime
            sheet = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            entry["_error"] = f"unreadable sheet: {exc}"
            entry["sheet"] = None
        else:
            entry["sheet"] = sheet
            if isinstance(sheet, dict):
                entry["_agent_count"] = count_agents(sheet)
                entry["_live"] = sheet.get("dispatch_type") in LIVE_TYPES
        sheets.append(entry)
    return sheets


def read_repo(repo: Path, limit: int, prompt_limit: int) -> dict[str, Any]:
    """A repo's state: pending sheets + the `limit` most recent dispatches.

    Goes through the parse cache, but the SHAPE of the return is untouched: ten UI
    variants and the tests already consume exactly these keys.
    """
    data = load_repo_rows(repo)
    result: dict[str, Any] = {
        "name": repo.name,
        "path": str(repo),
        "ledger_exists": data.ledger_exists,
        "pending": read_pending(repo),
        "dispatches": [],
        "total_dispatches": 0,
        "open_dispatches": 0,
        "warnings": [],
        "error": data.error,
    }

    if not data.ledger_exists or data.error:
        return result

    joined = data.rows
    result["warnings"] = data.warnings
    result["total_dispatches"] = len(joined)
    result["open_dispatches"] = sum(1 for d in joined if d["_state"] == "open")

    # Most recent first; the ledger is chronological by append.
    result["dispatches"] = [
        truncate_prompts(d, prompt_limit) for d in reversed(joined)
    ][:limit]
    return result


def find_dispatch(repo: Path, dispatch_id: str) -> dict[str, Any] | None:
    """One dispatch, truncating nothing — for the detail view."""
    data = load_repo_rows(repo)
    if not data.ledger_exists:
        return None
    for row in data.rows:
        if row.get("dispatch_id") == dispatch_id:
            return row
    return None


# ---------------------------------------------------------------------------
# Aggregations
# ---------------------------------------------------------------------------


def _iso_day(value: Any) -> str | None:
    """`YYYY-MM-DD` from the start of an ISO-8601 string, if any."""
    if not isinstance(value, str):
        return None
    match = _ISO_DAY_RE.match(value.strip())
    if not match:
        return None
    year, month, day = (int(g) for g in match.groups())
    try:
        date(year, month, day)
    except ValueError:
        return None  # 2026-13-45 matches the regex but isn't a day
    return match.group(0)


def iso_date(row: dict[str, Any]) -> str | None:
    """A dispatch's `YYYY-MM-DD` day, with a fallback via the `dispatch_id`.

    The day is derived from the UTC of `created` (which ends in `Z`), NOT the
    user's timezone. It's a choice, and it's that choice for a reason: the
    `dispatch_id` — the only source of a day that legacy rows have — is already
    written with a date prefix, and server and client must agree on which chart
    column a dispatch falls in. Converting to the browser's local time would make
    the same row jump buckets depending on who's looking. In practice the drift is
    at most one day, and only for dispatches near the UTC rollover.

    Precedence: `created` → `_close.closed` → `dispatch_id` prefix → None. The
    `_close.closed` comes BEFORE the id prefix because it's STAMPED by the appender
    (append-dispatch.cjs:351) — it's authoritative, whereas the id's `YYYY-MM-DD`
    prefix is just an unenforced convention (the appender doesn't validate the id
    format). An orphan close row with a malformed id still has the exact closing
    timestamp in `_close.closed`; without this precedence it would be left dateless
    with the data in hand. The id prefix comes last — it's what recovers the day
    for pre-v0.5.2 rows that have neither `created` nor `_close`.
    """
    day = _iso_day(row.get("created"))
    if day:
        return day
    close = row.get("_close")
    if isinstance(close, dict):
        day = _iso_day(close.get("closed"))
        if day:
            return day
    return _iso_day(row.get("dispatch_id"))


def _type_of(row: dict[str, Any]) -> str:
    """`dispatch_type`, or the explicit bucket when absent/non-string."""
    value = row.get("dispatch_type")
    return value if isinstance(value, str) and value else NO_TYPE


def summarize_repo(
    repo: Path, *, today: str, pending: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    """Aggregates over a repo's ENTIRE ledger (not over the `limit` window).

    Counts are always over all joined rows: a panel that said "181 dispatches" but
    counted only the 40 served would be a silent lie.

    `pending` is optional only for PERFORMANCE: here only `len(pending)` is used,
    for `pending_count`, but `/api/overview` already reads the pending sheets per
    repo for the attention list. Passing them avoids a second `read_pending` (a
    disk glob) per repo per request. Absent, it reads on its own.
    """
    data = load_repo_rows(repo, copy=False)
    rows = data.rows
    if pending is None:
        pending = read_pending(repo)

    by_type: dict[str, int] = {}
    open_count = closed_count = legacy_count = live_count = 0
    created_today = closed_today = 0
    days: list[str] = []
    created_stamps: list[str] = []

    for row in rows:
        by_type[_type_of(row)] = by_type.get(_type_of(row), 0) + 1
        if row.get("_state") == "open":
            open_count += 1
        else:
            closed_count += 1
        if row.get("_legacy"):
            legacy_count += 1
        if row.get("_live"):
            live_count += 1

        day = iso_date(row)
        if day:
            days.append(day)
            if day == today:
                created_today += 1

        close = row.get("_close")
        if isinstance(close, dict) and _iso_day(close.get("closed")) == today:
            closed_today += 1

        created = row.get("created")
        if isinstance(created, str):
            created_stamps.append(created)

    return {
        "name": repo.name,
        "path": str(repo),
        "ledger_exists": data.ledger_exists,
        "error": data.error,
        "warning_count": len(data.warnings),
        "total": len(rows),
        "open": open_count,
        "closed": closed_count,
        "legacy": legacy_count,
        "by_type": dict(sorted(by_type.items())),
        "live": live_count,
        # RESERVED = a type not dispatchable under v0.6.0. Legacy rows stay out of
        # both sides: they predate the distinction existing.
        # CAVEAT (not a partition): `total == live + reserved + legacy` is NOT
        # guaranteed. A research row whose `groups` failed the lenient parse ends up
        # WITHOUT `groups` → `_legacy=True` AND `_live=True` at once, counted in both
        # counts. The UI must NOT render live/reserved/legacy as a closed partition
        # of `total`. (Pinned in test_legacy_live_double_count.)
        "reserved": sum(1 for r in rows if not r.get("_live") and not r.get("_legacy")),
        "pending_count": len(pending),
        "today": {"created": created_today, "closed": closed_today},
        # Same number as `open`, under its own name: the UI's "running" surface is
        # conceptually a different thing and may diverge in Phase 2.
        "open_now": open_count,
        "first_day": min(days) if days else None,
        "last_day": max(days) if days else None,
        "last_created": max(created_stamps) if created_stamps else None,
    }


def _group_stats(row: dict[str, Any]) -> dict[str, Any]:
    """Flattens `groups`/`connections` into counts — enough for the listing."""
    roles: dict[str, int] = {}
    group_count = 0
    robot_talks = False

    groups = row.get("groups")
    if isinstance(groups, list):
        for group in groups:
            if not isinstance(group, dict):
                continue
            group_count += 1
            if group.get("robot_talks"):
                robot_talks = True
            for agent in group.get("agents") or []:
                if not isinstance(agent, dict):
                    continue
                role = agent.get("role")
                if isinstance(role, str) and role:
                    roles[role] = roles.get(role, 0) + 1

    conn_types: set[str] = set()
    connections = row.get("connections")
    if isinstance(connections, list):
        for conn in connections:
            if isinstance(conn, dict) and isinstance(conn.get("type"), str):
                conn_types.add(conn["type"])

    return {
        "_group_count": group_count,
        "_robot_talks": robot_talks,
        "_roles": dict(sorted(roles.items())),
        "_connection_types": sorted(conn_types),
    }


def slim(row: dict[str, Any], *, goal_limit: int = 240) -> dict[str, Any]:
    """The dispatch at listing weight: header + counts, zero prompt.

    The new listings walk the entire ledger (~700 rows), and it's `initial_prompt`
    that carries almost every byte. `truncate_prompts` shrinks the prompts but
    still sends the `groups` tree; here it disappears entirely and becomes a count.
    Whoever wants the text requests `/api/dispatch/{repo}/{id}`.
    """
    goal = row.get("goal")
    truncated = False
    if isinstance(goal, str) and len(goal) > goal_limit:
        goal = goal[:goal_limit] + "…"
        truncated = True

    close = row.get("_close")
    slim_close = None
    if isinstance(close, dict):
        # Only what the listing shows. `agents_spawned` and `feedback_prompts`
        # are left for the detail view — `feedback_prompts` is long text.
        slim_close = {
            "closed": close.get("closed"),
            "exit_reason": close.get("exit_reason"),
        }

    out: dict[str, Any] = {
        "dispatch_id": row.get("dispatch_id"),
        "created": row.get("created"),
        "_day": iso_date(row),
        "dispatch_type": row.get("dispatch_type"),
        "goal": goal,
        "invoked_by": row.get("invoked_by"),
        "working_folder": row.get("working_folder"),
        "max_loops": row.get("max_loops"),
        "final_approver": row.get("final_approver"),
        "anti_bias_global": row.get("anti_bias_global"),
        "_state": row.get("_state"),
        "_live": row.get("_live"),
        "_legacy": row.get("_legacy"),
        "_agent_count": row.get("_agent_count"),
        "_close": slim_close,
    }
    if truncated:
        out["_goal_truncated"] = True
    if row.get("_orphan_close"):
        out["_orphan_close"] = True
    out.update(_group_stats(row))
    return out


def daily_series(
    rows: list[dict[str, Any]], *, days: int | None = None
) -> dict[str, Any]:
    """Daily histogram stacked by `dispatch_type`.

    The days are CONTIGUOUS from the first to the last observed, with zeros in the
    empty ones. Skipping the days without a dispatch would shrink the axis and make
    an irregular cadence look regular — the chart would lie about exactly what it
    exists to show.
    """
    counts: dict[str, dict[str, int]] = {}
    totals: dict[str, int] = {}
    undated = 0

    for row in rows:
        day = iso_date(row)
        if not day:
            undated += 1
            continue
        counts.setdefault(day, {})
        kind = _type_of(row)
        counts[day][kind] = counts[day].get(kind, 0) + 1

    if not counts:
        return {
            "days": [],
            "types": [],
            "series": {},
            "totals": {},
            "max_day": 0,
            "undated": undated,
            "out_of_range": 0,
            "truncated_span": False,
        }

    first = date.fromisoformat(min(counts))
    last = date.fromisoformat(max(counts))

    # Clamp the UPPER edge of the window to TODAY (UTC). The remote past is already
    # capped by MAX_SPAN_DAYS below, but the future wasn't: a single century typo (a
    # row dated 2126) would become the `last` anchor and push every real row out of
    # range — the chart would go empty over ONE row. Dates beyond today are
    # out_of_range, not an anchor. (Clock skew within the span is harmless — the
    # point is the far-future outlier that redefines the axis.)
    today = datetime.now(timezone.utc).date()
    if last > today:
        last = today
    if first > last:
        first = last
    span = (last - first).days + 1

    # A single corrupted date (1970) would stretch the axis to tens of thousands of
    # buckets and crash the client. We prefer the most RECENT days: the remote past
    # of a live ledger is what matters least.
    truncated_span = span > MAX_SPAN_DAYS
    if truncated_span:
        span = MAX_SPAN_DAYS
        first = last - timedelta(days=span - 1)

    day_list = [(first + timedelta(days=i)).isoformat() for i in range(span)]
    if days is not None and days > 0 and days < len(day_list):
        day_list = day_list[-days:]

    window = set(day_list)
    out_of_range = sum(
        total
        for day, kinds in counts.items()
        if day not in window
        for total in [sum(kinds.values())]
    )

    kinds_present = sorted(
        {kind for day, kinds in counts.items() if day in window for kind in kinds}
    )
    series = {
        kind: [counts.get(day, {}).get(kind, 0) for day in day_list]
        for kind in kinds_present
    }
    for kind in kinds_present:
        totals[kind] = sum(series[kind])

    max_day = max(
        (sum(counts.get(day, {}).values()) for day in day_list), default=0
    )

    return {
        "days": day_list,
        "types": kinds_present,
        "series": series,
        "totals": totals,
        "max_day": max_day,
        "undated": undated,
        # Dated rows that fell outside the window (by span cap or by `days`).
        # `totals` counts only what's plotted, so this number is what would be
        # missing to reconcile with `summarize_repo.total`.
        "out_of_range": out_of_range,
        "truncated_span": truncated_span,
    }


def signature(repos: list[Path]) -> tuple:
    """Cheap fingerprint of the on-disk state, to detect change without reparsing.

    Covers the ledger and each pending sheet (mtime + size). An append changes the
    size; a sheet edit changes the mtime.
    """
    parts: list[tuple] = []
    for repo in repos:
        paths = [repo / LEDGER_RELPATH]
        pending_dir = repo / PENDING_RELPATH
        if pending_dir.is_dir():
            paths.extend(sorted(pending_dir.glob("*.json")))
        for path in paths:
            try:
                stat = path.stat()
                parts.append((str(path), stat.st_mtime_ns, stat.st_size))
            except OSError:
                parts.append((str(path), None, None))
    return tuple(parts)
