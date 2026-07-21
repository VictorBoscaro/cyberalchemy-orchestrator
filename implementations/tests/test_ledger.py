"""Tests for the ledger reader.

Runs against synthetic fixtures (deterministic) and, if they exist, against the
machine's real ledgers (smoke test — never fails on content, only on a crash).

    python -m implementations.tests.test_ledger      (from the repo root)
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from server import config as config_module  # noqa: E402
from server import ledger  # noqa: E402

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name} {detail}")
        FAILURES.append(name)


LEDGER_OK = """# header comment
# second comment line
dispatches:
  - dispatch_id: "2026-06-12-alpha"
    schema_version: "0.6.0"
    created: "2026-06-12T18:00:00.000Z"
    dispatch_type: "research"
    goal: "objective alpha"
    context: "alpha context"
    max_loops: 1
    final_approver: "parent"
    working_folder: "research/alpha/"
    groups: [{"group_id":"explorers","n":2,"anti_bias":"axis","agents":[{"role":"explorer","model":"m","token_budget":800,"initial_prompt":"AAAAAAAAAA","angle":"a"},{"role":"explorer","model":"m","token_budget":800,"initial_prompt":"B","angle":"b"}]}]
    connections: [{"from":"explorers","to":"explorers","type":"feedback","loop_cap":2}]
  - dispatch_id: "2026-06-13-beta"
    schema_version: "0.6.1"
    dispatch_type: "review"
    goal: "objective beta"
    output_mode: "inline"
    groups: [{"group_id":"g","agents":[{"role":"planner","model":"m","token_budget":10,"initial_prompt":"p"},{"role":"coder","model":"m","token_budget":10,"initial_prompt":"p"}]}]
  - close_of: "2026-06-12-alpha"
    closed: "2026-06-12T19:00:00.000Z"
    exit_reason: "resolved"
    agents_spawned: {"total":2,"tree":{"explorer":2},"loops_used":1}
"""

LEGACY = """dispatches:
  - dispatch_id: "2026-01-01-old"
    status: "done"
    agents: [{"name":"x"}]
    corpus: "some"
"""

ORPHAN = """dispatches:
  - close_of: "2026-05-05-ghost"
    exit_reason: "error"
    agents_spawned: {"total":0,"tree":{},"loops_used":0}
"""


def test_parse_and_join() -> None:
    print("\nparse + join (schema v0.6.0 and v0.6.1)")
    parsed = ledger.parse_ledger(LEDGER_OK)
    check("3 raw rows", len(parsed.rows) == 3, f"(got {len(parsed.rows)})")
    check("clean ledger raises no warning", parsed.warnings == [], f"({parsed.warnings})")

    joined = ledger.join_rows(parsed.rows)
    check("2 dispatches after the join", len(joined) == 2, f"(got {len(joined)})")

    alpha = next(d for d in joined if d["dispatch_id"] == "2026-06-12-alpha")
    beta = next(d for d in joined if d["dispatch_id"] == "2026-06-13-beta")

    check("alpha closed by the close row", alpha["_state"] == "closed")
    check("alpha carries the exit_reason", alpha["_close"]["exit_reason"] == "resolved")
    check("beta stays open", beta["_state"] == "open")
    check("beta has no close", beta["_close"] is None)
    check("groups comes as a parsed list", isinstance(alpha["groups"], list))
    check("connections with a typed edge", alpha["connections"][0]["type"] == "feedback")
    check("loop_cap preserved", alpha["connections"][0]["loop_cap"] == 2)
    check("agent count", alpha["_agent_count"] == 2)
    check("research is LIVE", alpha["_live"] is True)
    check("v0.6.0 is not legacy", alpha["_legacy"] is False)
    check("v0.6.1 is not legacy", beta["_legacy"] is False)
    check("v0.6.1 output_mode is preserved", beta["output_mode"] == "inline")
    check(
        "v0.6.1 planner/coder roles are preserved",
        [a["role"] for a in beta["groups"][0]["agents"]] == ["planner", "coder"],
    )


def test_truncation() -> None:
    print("\ninitial_prompt truncation")
    joined = ledger.join_rows(ledger.parse_ledger(LEDGER_OK).rows)
    alpha = next(d for d in joined if d["dispatch_id"] == "2026-06-12-alpha")

    trimmed = ledger.truncate_prompts(alpha, 5)
    prompt = trimmed["groups"][0]["agents"][0]["initial_prompt"]
    check("long prompt truncated", prompt == "AAAAA…", f"(got {prompt!r})")
    check("truncation flag on the agent", trimmed["groups"][0]["agents"][0]["_prompt_truncated"] is True)
    check("truncation flag on the row", trimmed["_prompts_truncated"] is True)
    check("short prompt intact", trimmed["groups"][0]["agents"][1]["initial_prompt"] == "B")
    check("original not mutated", alpha["groups"][0]["agents"][0]["initial_prompt"] == "AAAAAAAAAA")


def test_legacy_and_orphan() -> None:
    print("\ngrandfathering + orphan close")
    legacy = ledger.join_rows(ledger.parse_ledger(LEGACY).rows)
    check("pre-v0.5.2 row is read", len(legacy) == 1)
    check("marked as legacy", legacy[0]["_legacy"] is True)
    # Regression: `status` is a REAL key on pre-v0.5.2 rows. A computed field with
    # that name would wipe the historical data — hence the `_` prefix.
    check("historical `status` key preserved", legacy[0]["status"] == "done")
    check("computed state does not collide", legacy[0]["_state"] == "open")
    check("count_agents tolerates missing groups", legacy[0]["_agent_count"] == 0)

    orphan = ledger.join_rows(ledger.parse_ledger(ORPHAN).rows)
    check("orphan close is exposed", len(orphan) == 1 and orphan[0]["_orphan_close"] is True)


def test_prettified_legacy() -> None:
    """Real shape found in the domainspec ledger: multi-line JSON + trailing comma."""
    print("\nprettified old rows (real domainspec data)")
    text = (
        "dispatches:\n"
        '  - dispatch_id: "2026-06-12-prettified"\n'
        '    corpus: "internal_tools/x"\n'
        '    status: "dispatched"\n'
        "    anti_bias:\n"
        "      {\n"
        '        "axis": "critical lens",\n'
        '        "pairs":\n'
        "          [\n"
        '            "a ⟂ b",\n'
        '            "b ⟂ c",\n'
        "          ],\n"
        "      }\n"
        "    max_loops: 1\n"
    )
    parsed = ledger.parse_ledger(text)
    check("the row survives", len(parsed.rows) == 1, f"(got {len(parsed.rows)})")
    row = parsed.rows[0]
    check("multi-line value reassembled", isinstance(row.get("anti_bias"), dict))
    check("trailing comma tolerated", row["anti_bias"]["pairs"] == ["a ⟂ b", "b ⟂ c"])
    check("key after the block is read", row.get("max_loops") == 1)
    check("tolerance is warned", any("comma" in w for w in parsed.warnings))


def test_lenient_vs_strict() -> None:
    print("\nlenient skips the bad row; strict raises")
    broken = (
        "dispatches:\n"
        '  - dispatch_id: "good-1"\n'
        '    goal: "survives"\n'
        "  this is not a row\n"
        '  - dispatch_id: "good-2"\n'
        '    goal: "also survives"\n'
    )
    parsed = ledger.parse_ledger(broken)
    check("good rows preserved around the junk", len(parsed.rows) == 2, f"(got {len(parsed.rows)})")
    check("the problem becomes a warning", len(parsed.warnings) == 1, f"({parsed.warnings})")

    try:
        ledger.parse_ledger(broken, lenient=False)
        check("strict mode raises", False, "(did not raise)")
    except ledger.LedgerError:
        check("strict mode raises", True)


def test_corruption() -> None:
    print("\nstructural corruption (strict mode)")
    cases = {
        "invalid line shape": "dispatches:\n  this is not a row\n",
        "invalid JSON": 'dispatches:\n  - dispatch_id: {not json\n',
        "row starting wrong": 'dispatches:\n  - goal: "x"\n',
        "continuation without row": 'dispatches:\n    goal: "x"\n',
    }
    for name, text in cases.items():
        try:
            ledger.parse_ledger(text, lenient=False)
            check(name, False, "(did not raise LedgerError)")
        except ledger.LedgerError:
            check(name, True)


def test_iso_date() -> None:
    print("\niso_date (UTC day, with fallback on the dispatch_id)")
    check(
        "good created wins",
        ledger.iso_date({"created": "2026-06-12T18:00:00.000Z", "dispatch_id": "2020-01-01-x"})
        == "2026-06-12",
    )
    check(
        "no created falls back to the id prefix",
        ledger.iso_date({"dispatch_id": "2026-07-10-ui11-metatype-review"}) == "2026-07-10",
    )
    check(
        "malformed created falls back to the id",
        ledger.iso_date({"created": "yesterday", "dispatch_id": "2026-07-10-x"}) == "2026-07-10",
    )
    check(
        "created with an impossible month falls back to the id",
        ledger.iso_date({"created": "2026-13-45T00:00:00Z", "dispatch_id": "2026-07-10-x"})
        == "2026-07-10",
    )
    check("junk on both sides becomes None", ledger.iso_date({"created": None, "dispatch_id": "no-date"}) is None)
    check("empty row becomes None", ledger.iso_date({}) is None)


def test_join_non_hashable_id() -> None:
    print("\njoin_rows tolerates a non-hashable id (FIX 2: does not raise TypeError)")
    # A `dispatch_id`/`close_of` that parsed to a JSON list is not hashable;
    # used as a dict key it would raise TypeError and take down the ENTIRE repo
    # parse (500 on every endpoint). The reader is lenient: skips the row and moves on.
    rows = [
        {"dispatch_id": ["2026-06-01", "x"], "goal": "id became a list"},
        {"dispatch_id": "2026-06-02-good", "goal": "survives"},
        {"close_of": ["list"], "exit_reason": "resolved"},
    ]
    try:
        joined = ledger.join_rows(rows)
    except TypeError as exc:
        check("join_rows does not raise on a non-hashable id", False, f"({exc})")
        return
    check("join_rows does not raise on a non-hashable id", True)
    check("the list-id row is skipped", len(joined) == 1, f"(got {len(joined)})")
    check("the good row survives around it", joined[0]["dispatch_id"] == "2026-06-02-good")


def test_iso_date_close_precedence() -> None:
    print("\niso_date: _close.closed before the id prefix (FIX 3: stamped > convention)")
    # Orphan close row, id with no date prefix, but `_close.closed` stamped: the
    # exact close day was at hand and previously went unread.
    orphan = {"dispatch_id": "id-no-date", "_close": {"closed": "2026-07-15T09:00:00.000Z"}}
    check("orphan close resolves by the close day", ledger.iso_date(orphan) == "2026-07-15", f"({ledger.iso_date(orphan)})")
    check(
        "created still beats the close",
        ledger.iso_date({"created": "2026-01-02T00:00:00Z", "_close": {"closed": "2026-07-15T00:00:00Z"}}) == "2026-01-02",
    )
    check(
        "unreadable close falls back to the id prefix",
        ledger.iso_date({"dispatch_id": "2026-03-03-x", "_close": {"closed": "yesterday"}}) == "2026-03-03",
    )
    check("nothing date-like stays None", ledger.iso_date({"dispatch_id": "no-date", "_close": {"closed": "yesterday"}}) is None)


def _row(did: str, kind: str | None = "research", **extra) -> dict:
    row = {"dispatch_id": did, "dispatch_type": kind, "_state": "open", "_legacy": False}
    row.update(extra)
    return row


def test_daily_series() -> None:
    print("\ndaily_series (contiguous days, gaps zero-filled)")
    rows = [
        _row("2026-06-01-a", "research"),
        _row("2026-06-01-b", "review"),
        _row("2026-06-04-c", "research"),
    ]
    series = ledger.daily_series(rows)
    check(
        "contiguous axis from first to last",
        series["days"] == ["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04"],
        f"({series['days']})",
    )
    check("types present and sorted", series["types"] == ["research", "review"])
    check("gap becomes zero", series["series"]["research"] == [1, 0, 0, 1], f"({series['series']['research']})")
    check("short series filled", series["series"]["review"] == [1, 0, 0, 0])
    check("totals by type", series["totals"] == {"research": 2, "review": 1})
    check("max_day is the tallest column", series["max_day"] == 2, f"({series['max_day']})")
    check("nothing undated", series["undated"] == 0)
    check("span not truncated", series["truncated_span"] is False)

    single = ledger.daily_series([_row("2026-06-01-a", "research")])
    check("a single day yields one bucket", single["days"] == ["2026-06-01"])
    check("a single day, max_day=1", single["max_day"] == 1)

    empty = ledger.daily_series([_row("no-date", "research"), _row("other", None)])
    check("zero dated rows: empty axis", empty["days"] == [])
    check("zero dated rows: empty series", empty["series"] == {} and empty["totals"] == {})
    check("undated are reported", empty["undated"] == 2, f"({empty['undated']})")
    check("max_day zero", empty["max_day"] == 0)

    no_type = ledger.daily_series([_row("2026-06-01-a", None)])
    check("missing type becomes its own bucket", no_type["types"] == [ledger.NO_TYPE], f"({no_type['types']})")

    # A 1970 date would stretch the axis to ~20k buckets.
    wild = ledger.daily_series([_row("1970-01-01-a"), _row("2026-06-01-b")])
    check("pathological span is capped", wild["truncated_span"] is True)
    check("axis capped at MAX_SPAN_DAYS", len(wild["days"]) == ledger.MAX_SPAN_DAYS, f"({len(wild['days'])})")
    check("the out-of-window row is reported", wild["out_of_range"] == 1, f"({wild['out_of_range']})")

    windowed = ledger.daily_series(rows, days=2)
    check("days=N cuts to the last N", windowed["days"] == ["2026-06-03", "2026-06-04"], f"({windowed['days']})")
    check("days=N reports what fell outside", windowed["out_of_range"] == 2, f"({windowed['out_of_range']})")


def test_daily_series_future_clamp() -> None:
    print("\ndaily_series clamps the future edge to today (FIX 4: a 2126 typo does not zero the chart)")
    rows = [
        _row("2026-06-01-a", "research"),
        _row("2026-06-02-b", "research"),
        _row("2126-06-01-typo", "research"),  # century typo: must not anchor the axis
    ]
    series = ledger.daily_series(rows)
    check("the real rows stay plotted", series["totals"].get("research", 0) == 2, f"({series['totals']})")
    check("the 2126 row is out_of_range, not an anchor", series["out_of_range"] == 1, f"({series['out_of_range']})")
    check("the axis did not blow up to thousands of buckets", len(series["days"]) <= ledger.MAX_SPAN_DAYS, f"({len(series['days'])})")
    # The accounting invariant must stay exact.
    plotted = sum(sum(s) for s in series["series"].values())
    check(
        "plotted + out_of_range + undated == len(rows)",
        plotted + series["out_of_range"] + series["undated"] == len(rows),
        f"({plotted}+{series['out_of_range']}+{series['undated']} vs {len(rows)})",
    )


def test_slim() -> None:
    print("\nslim (listing weight, no prompt at all)")
    joined = ledger.join_rows(ledger.parse_ledger(LEDGER_OK).rows)
    alpha = next(d for d in joined if d["dispatch_id"] == "2026-06-12-alpha")

    s = ledger.slim(alpha, goal_limit=8)
    blob = json.dumps(s, ensure_ascii=False)
    check("initial_prompt appears nowhere", "initial_prompt" not in blob)
    check("groups does not appear", "groups" not in s)
    check("goal truncated", s["goal"] == "objectiv…", f"({s['goal']!r})")
    check("goal-truncated flag", s["_goal_truncated"] is True)
    check("_day computed", s["_day"] == "2026-06-12")
    check("group count", s["_group_count"] == 1)
    check("roles counted", s["_roles"] == {"explorer": 2}, f"({s['_roles']})")
    check("distinct, sorted connection types", s["_connection_types"] == ["feedback"])
    check("missing robot_talks becomes False", s["_robot_talks"] is False)
    check("_close slimmed to just closed/exit_reason", set(s["_close"]) == {"closed", "exit_reason"}, f"({s['_close']})")
    check("agents_spawned does not leak", "agents_spawned" not in blob)
    check("original not mutated", "initial_prompt" in json.dumps(alpha["groups"]))

    beta = next(d for d in joined if d["dispatch_id"] == "2026-06-13-beta")
    sb = ledger.slim(beta)
    check("short goal gets no flag", "_goal_truncated" not in sb)
    check("open one has _close None", sb["_close"] is None)

    legacy = ledger.join_rows(ledger.parse_ledger(LEGACY).rows)[0]
    sl = ledger.slim(legacy)
    check("legacy without groups survives slim", sl["_group_count"] == 0 and sl["_roles"] == {})
    check("legacy without dispatch_type becomes None in the raw field", sl["dispatch_type"] is None)


def _write_ledger(root: Path, text: str) -> None:
    path = root / ledger.LEDGER_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_summarize_repo(tmp_root: Path) -> None:
    print("\nsummarize_repo (aggregate over the whole ledger)")
    repo = tmp_root / "repo-summary"
    _write_ledger(repo, LEDGER_OK + LEGACY.split("dispatches:\n", 1)[1] + ORPHAN.split("dispatches:\n", 1)[1])
    ledger.clear_cache()

    s = ledger.summarize_repo(repo, today="2026-06-12")
    check("total includes the orphan close", s["total"] == 4, f"({s['total']})")
    check("open", s["open"] == 2, f"({s['open']})")
    check("closed (alpha + orphan)", s["closed"] == 2, f"({s['closed']})")
    check("legacy counts the old one + the orphan", s["legacy"] == 2, f"({s['legacy']})")
    check(
        "by_type with a bucket for the missing type",
        s["by_type"] == {"research": 1, "review": 1, ledger.NO_TYPE: 2},
        f"({s['by_type']})",
    )
    check("live = research + review", s["live"] == 2, f"({s['live']})")
    check("reserved excludes legacy", s["reserved"] == 0, f"({s['reserved']})")
    check("today: 1 created", s["today"]["created"] == 1, f"({s['today']})")
    check("today: 1 closed", s["today"]["closed"] == 1, f"({s['today']})")
    check("open_now mirrors open", s["open_now"] == s["open"])
    check("first day", s["first_day"] == "2026-01-01", f"({s['first_day']})")
    check("last day", s["last_day"] == "2026-06-13", f"({s['last_day']})")
    check("last_created is the most recent raw ISO", s["last_created"] == "2026-06-12T18:00:00.000Z")
    check("no error", s["error"] is None and s["ledger_exists"] is True)

    missing = ledger.summarize_repo(tmp_root / "repo-nonexistent", today="2026-06-12")
    check("repo with no ledger does not explode", missing["total"] == 0 and missing["ledger_exists"] is False)


def test_legacy_live_double_count(tmp_root: Path) -> None:
    print("\nrow that is both _legacy and _live (FIX 8b: pin the non-partition)")
    # A research row (LIVE) whose `groups` fails the lenient parse ends up WITHOUT
    # `groups` → `_legacy=True` AND `_live=True`, counted in both sums. We pin that
    # `total == live + reserved + legacy` does NOT hold, so the frontend agent
    # does not render the three as a closed partition.
    text = (
        "dispatches:\n"
        '  - dispatch_id: "2026-06-20-broken-groups"\n'
        '    schema_version: "0.6.0"\n'
        '    dispatch_type: "research"\n'
        '    goal: "objective"\n'
        "    groups: @@@not-json\n"
    )
    joined = ledger.join_rows(ledger.parse_ledger(text).rows)
    check("the row survives the unreadable groups", len(joined) == 1, f"(got {len(joined)})")
    row = joined[0]
    check("no groups becomes _legacy", row["_legacy"] is True)
    check("research stays _live", row["_live"] is True)

    repo = tmp_root / "repo-double"
    _write_ledger(repo, text)
    ledger.clear_cache()
    s = ledger.summarize_repo(repo, today="2026-06-20")
    check("counted in legacy", s["legacy"] == 1, f"({s['legacy']})")
    check("counted in live", s["live"] == 1, f"({s['live']})")
    check("reserved excludes it (it is live)", s["reserved"] == 0, f"({s['reserved']})")
    check(
        "live+reserved+legacy does NOT partition total (double count pinned)",
        s["live"] + s["reserved"] + s["legacy"] == 2 and s["total"] == 1,
        f"(l+r+leg={s['live'] + s['reserved'] + s['legacy']}, total={s['total']})",
    )


def test_parse_cache(tmp_root: Path) -> None:
    print("\nparse cache (fingerprint mtime_ns + size)")
    repo = tmp_root / "repo-cache"
    _write_ledger(repo, LEDGER_OK)
    ledger.clear_cache()

    first = ledger.load_repo_rows(repo)
    check("first read parses", ledger.parse_count() == 1, f"({ledger.parse_count()})")
    check("rows came through", len(first.rows) == 2)

    ledger.load_repo_rows(repo)
    ledger.load_repo_rows(repo)
    check("untouched file does not reparse", ledger.parse_count() == 1, f"({ledger.parse_count()})")

    # read_repo and find_dispatch also go through the cache.
    ledger.read_repo(repo, 40, 280)
    ledger.find_dispatch(repo, "2026-06-12-alpha")
    check("read_repo/find_dispatch reuse", ledger.parse_count() == 1, f"({ledger.parse_count()})")

    # The cache must not be contaminated by whoever received the rows.
    first.rows[0]["_pollution"] = True
    check("caller mutation does not enter the cache", "_pollution" not in ledger.load_repo_rows(repo).rows[0])

    # Content change (size + mtime) invalidates.
    _write_ledger(repo, LEDGER_OK + '  - dispatch_id: "2026-06-14-gamma"\n    goal: "new"\n')
    again = ledger.load_repo_rows(repo)
    check("append invalidates the cache", ledger.parse_count() == 2, f"({ledger.parse_count()})")
    check("the new row appears", len(again.rows) == 3, f"({len(again.rows)})")

    # Only the mtime, same size: the fingerprint carries both.
    path = repo / ledger.LEDGER_RELPATH
    stat = path.stat()
    os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 10_000_000_000))
    ledger.load_repo_rows(repo)
    check("new mtime with same size invalidates", ledger.parse_count() == 3, f"({ledger.parse_count()})")

    ledger.clear_cache()
    check("clear_cache zeroes the counter", ledger.parse_count() == 0)


def test_real_repos() -> None:
    print("\nsmoke against the real ledgers")
    cfg = config_module.load()
    repos = cfg.resolved_repos()
    check("auto-discovery found repos", len(repos) > 0, f"(got {len(repos)})")

    start = time.time()
    total = 0
    for repo in repos:
        try:
            data = ledger.read_repo(repo, cfg.limit, cfg.prompt_limit)
        except Exception as exc:  # noqa: BLE001 — smoke test: any crash is a failure
            check(f"{repo.name} reads without crashing", False, f"({type(exc).__name__}: {exc})")
            continue
        total += data["total_dispatches"]
        status = data["error"] or "ok"
        print(
            f"        {repo.name:<32} total={data['total_dispatches']:<5}"
            f" open={data['open_dispatches']:<4} pending={len(data['pending']):<3}"
            f" warnings={len(data['warnings']):<3} {status}"
        )
        check(f"{repo.name} has no fatal error", data["error"] is None, f"({data['error']})")
        # A ledger with old rows should still deliver history: warnings are
        # acceptable, zeroing out the repo is not.
        if data["ledger_exists"]:
            check(
                f"{repo.name} delivers dispatches",
                data["total_dispatches"] > 0,
                f"(0 dispatches, warnings={len(data['warnings'])})",
            )

    elapsed = time.time() - start
    print(f"        -> {total} dispatches in {elapsed:.2f}s")
    check("parse of all repos < 5s", elapsed < 5.0, f"({elapsed:.2f}s)")


def main() -> int:
    test_parse_and_join()
    test_truncation()
    test_legacy_and_orphan()
    test_prettified_legacy()
    test_lenient_vs_strict()
    test_corruption()
    test_join_non_hashable_id()
    test_iso_date()
    test_iso_date_close_precedence()
    test_daily_series()
    test_daily_series_future_clamp()
    test_slim()
    with tempfile.TemporaryDirectory() as tmp:
        test_summarize_repo(Path(tmp))
        test_legacy_live_double_count(Path(tmp))
        test_parse_cache(Path(tmp))
    ledger.clear_cache()
    test_real_repos()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S): {', '.join(FAILURES)}")
        return 1
    print("all tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
