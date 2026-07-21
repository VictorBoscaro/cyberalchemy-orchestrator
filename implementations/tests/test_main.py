"""Endpoint-layer tests (FastAPI) — the coverage hole from FIX 7.

`test_ledger.py` never imports `main`, so /api/overview, /api/repo, the
deliberate filter ASYMMETRY (state/type filter only the list, never the summary
nor the series), the OPEN_ALL_CAP, and the overview totals went untested. Mutation
testing left 9 survivors in exactly those regions.

This file runs in-process with FastAPI's TestClient and uses ASYMMETRIC fixtures
(open != closed, > 40 rows) on purpose: a symmetric 4-row fixture would let the
swapped-counter and cut-at-40 mutants survive.

    python tests/test_main.py      (from implementations/)
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

from server import config as config_module  # noqa: E402
from server import ledger  # noqa: E402
from server import main as main_module  # noqa: E402

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name} {detail}")
        FAILURES.append(name)


# --------------------------------------------------------------------------
# Ledger synthesis (same shape the appender writes)
# --------------------------------------------------------------------------

_GROUP = [
    {
        "group_id": "g",
        "agents": [
            {"role": "explorer", "model": "m", "token_budget": 10, "initial_prompt": "p"}
        ],
    }
]
_SPAWNED = {"total": 1, "tree": {"explorer": 1}, "loops_used": 1}


def _dispatch(did: str, dtype: str, created: str) -> str:
    return (
        f"  - dispatch_id: {json.dumps(did)}\n"
        f'    schema_version: "0.6.0"\n'
        f"    created: {json.dumps(created)}\n"
        f"    dispatch_type: {json.dumps(dtype)}\n"
        f"    goal: {json.dumps('goal of ' + did)}\n"
        f"    groups: {json.dumps(_GROUP)}\n"
    )


def _close(did: str, closed: str) -> str:
    return (
        f"  - close_of: {json.dumps(did)}\n"
        f"    closed: {json.dumps(closed)}\n"
        f'    exit_reason: "resolved"\n'
        f"    agents_spawned: {json.dumps(_SPAWNED)}\n"
    )


def _ledger(rows: list[str]) -> str:
    return "dispatches:\n" + "".join(rows)


def _day(i: int) -> str:
    # Spread across June/2026 — always in the past (today is later), deterministic.
    return f"2026-06-{(i % 27) + 1:02d}"


def _write_repo(root: Path, name: str, text: str) -> None:
    path = root / name / ledger.LEDGER_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _client(root: Path) -> TestClient:
    """Points the module's CFG at a temporary scan root and returns the client.

    Each scenario builds a NEW `Config`, so the (TTL) cache of `resolved_repos`
    starts empty — no contamination between scenarios.
    """
    cfg = config_module.Config(scan_roots=[root])
    main_module.CFG = cfg
    ledger.clear_cache()
    return TestClient(main_module.app)


# --------------------------------------------------------------------------
# Asymmetric fixtures
# --------------------------------------------------------------------------

def _asym_repo() -> str:
    """60 rows, 45 open / 15 closed — asymmetric and > 40."""
    rows: list[str] = []
    # 30 open research
    for i in range(30):
        rows.append(_dispatch(f"2026-06-01-research-open-{i:02d}", "research", f"{_day(i)}T10:00:00.000Z"))
    # 10 open review
    for i in range(10):
        rows.append(_dispatch(f"2026-06-02-review-open-{i:02d}", "review", f"{_day(i)}T11:00:00.000Z"))
    # 5 open code (RESERVED)
    for i in range(5):
        rows.append(_dispatch(f"2026-06-03-code-open-{i:02d}", "code", f"{_day(i)}T12:00:00.000Z"))
    # 15 closed research (dispatch + close)
    for i in range(15):
        did = f"2026-06-04-research-closed-{i:02d}"
        rows.append(_dispatch(did, "research", f"{_day(i)}T13:00:00.000Z"))
        rows.append(_close(did, f"{_day(i)}T14:00:00.000Z"))
    return _ledger(rows)


def _open_rows(prefix: str, n: int) -> str:
    return _ledger(
        [_dispatch(f"{prefix}-{i:04d}", "research", f"{_day(i)}T09:00:00.000Z") for i in range(n)]
    )


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------

def test_repo_filter_asymmetry(root: Path) -> None:
    print("\n/api/repo — state/type asymmetry (filters the list, NEVER summary/series)")
    _write_repo(root, "alpha", _asym_repo())
    client = _client(root)

    full = client.get("/api/repo/alpha").json()
    check("full list has the 60 rows", len(full["dispatches"]) == 60, f"({len(full['dispatches'])})")
    check("summary counts the whole repo", full["summary"]["total"] == 60, f"({full['summary']['total']})")
    check("asymmetric summary: 45 open", full["summary"]["open"] == 45, f"({full['summary']['open']})")
    check("asymmetric summary: 15 closed", full["summary"]["closed"] == 15, f"({full['summary']['closed']})")

    open_only = client.get("/api/repo/alpha", params={"state": "open"}).json()
    closed_only = client.get("/api/repo/alpha", params={"state": "closed"}).json()
    review_only = client.get("/api/repo/alpha", params={"type": "review"}).json()

    # The LIST shrinks...
    check("state=open shrinks the list to 45", len(open_only["dispatches"]) == 45, f"({len(open_only['dispatches'])})")
    check("state=closed shrinks the list to 15", len(closed_only["dispatches"]) == 15, f"({len(closed_only['dispatches'])})")
    check("type=review shrinks the list to 10", len(review_only["dispatches"]) == 10, f"({len(review_only['dispatches'])})")

    # ...but summary and series are IDENTICAL to the unfiltered one (the asymmetry).
    for label, resp in (("state=open", open_only), ("state=closed", closed_only), ("type=review", review_only)):
        check(f"{label}: summary identical to full", resp["summary"] == full["summary"])
        check(f"{label}: series identical to full", resp["series"] == full["series"])

    # Belt and suspenders: byte-for-byte.
    check(
        "summary/series byte-identical under filter",
        json.dumps(open_only["summary"], sort_keys=True) == json.dumps(full["summary"], sort_keys=True)
        and json.dumps(open_only["series"], sort_keys=True) == json.dumps(full["series"], sort_keys=True),
    )


def test_repo_errors(root: Path) -> None:
    print("\n/api/repo — 404 unknown repo, 422 invalid state")
    _write_repo(root, "alpha", _asym_repo())
    client = _client(root)
    check("404 on a nonexistent repo", client.get("/api/repo/does-not-exist").status_code == 404)
    check("422 on a state outside the enum", client.get("/api/repo/alpha", params={"state": "bogus"}).status_code == 422)
    check("state=all is accepted", client.get("/api/repo/alpha", params={"state": "all"}).status_code == 200)


def test_dispatch_endpoint(root: Path) -> None:
    print("\n/api/dispatch — 404s and retrieval of one row")
    _write_repo(root, "alpha", _asym_repo())
    client = _client(root)
    check("404 on a nonexistent repo", client.get("/api/dispatch/does-not-exist/x").status_code == 404)
    check("404 on a nonexistent dispatch", client.get("/api/dispatch/alpha/does-not-exist").status_code == 404)
    ok = client.get("/api/dispatch/alpha/2026-06-01-research-open-00")
    check("finds the dispatch", ok.status_code == 200 and ok.json()["dispatch_id"] == "2026-06-01-research-open-00")


def test_overview_totals(root: Path) -> None:
    print("\n/api/overview — totals = per-repo sum (no double count), open_all matches")
    _write_repo(root, "alpha", _asym_repo())  # 60 total, 45 open
    # repo beta: 20 open + 10 closed = 30 total, 20 open
    beta_rows: list[str] = []
    for i in range(20):
        beta_rows.append(_dispatch(f"2026-06-05-beta-open-{i:02d}", "experiment", f"{_day(i)}T08:00:00.000Z"))
    for i in range(10):
        did = f"2026-06-06-beta-closed-{i:02d}"
        beta_rows.append(_dispatch(did, "research", f"{_day(i)}T08:00:00.000Z"))
        beta_rows.append(_close(did, f"{_day(i)}T09:00:00.000Z"))
    _write_repo(root, "beta", _ledger(beta_rows))
    client = _client(root)

    ov = client.get("/api/overview").json()
    summaries = ov["repos"]
    totals = ov["totals"]

    sum_total = sum(s["total"] for s in summaries)
    sum_open = sum(s["open"] for s in summaries)
    sum_closed = sum(s["closed"] for s in summaries)
    check("totals.total == sum of summaries (90)", totals["total"] == sum_total == 90, f"({totals['total']} vs {sum_total})")
    check("totals.open == sum of summaries (65)", totals["open"] == sum_open == 65, f"({totals['open']} vs {sum_open})")
    check("totals.closed == sum of summaries (25)", totals["closed"] == sum_closed == 25, f"({totals['closed']} vs {sum_closed})")
    check("totals.repos == 2", totals["repos"] == 2, f"({totals['repos']})")

    # by_type summed with no double count: we check the sum.
    bt = totals["by_type"]
    sum_bt: dict[str, int] = {}
    for s in summaries:
        for k, v in s["by_type"].items():
            sum_bt[k] = sum_bt.get(k, 0) + v
    check("overview by_type == sum of per-repo by_type", bt == sum_bt, f"({bt} vs {sum_bt})")

    # 65 open < CAP(200): open_all is NOT capped and matches the open total.
    check("len(attention.open_all) == open total (65)", len(ov["attention"]["open_all"]) == 65, f"({len(ov['attention']['open_all'])})")
    check("not capped below the ceiling", "_capped" not in ov["attention"])


def test_open_all_cap(root: Path) -> None:
    print("\n/api/overview — OPEN_ALL_CAP and _open_all_total")
    cap = main_module.OPEN_ALL_CAP
    total_open = cap + 95  # 295 with CAP=200
    _write_repo(root, "flood", _open_rows("2026-06-07-flood", total_open))
    client = _client(root)

    ov = client.get("/api/overview").json()
    att = ov["attention"]
    check(f"open_all capped at OPEN_ALL_CAP ({cap})", len(att["open_all"]) == cap, f"({len(att['open_all'])})")
    check("_capped present when it overflows", att.get("_capped") is True)
    check("_open_all_total is the real number", att.get("_open_all_total") == total_open, f"({att.get('_open_all_total')})")
    check("totals.open reflects the real total", ov["totals"]["open"] == total_open, f"({ov['totals']['open']})")


def test_snapshot_shape(root: Path) -> None:
    print("\n/api/snapshot — shape intact (nine UIs depend on it)")
    _write_repo(root, "alpha", _asym_repo())
    client = _client(root)
    snap = client.get("/api/snapshot").json()
    check("has repos and config", "repos" in snap and "config" in snap)
    repo = next(r for r in snap["repos"] if r["name"] == "alpha")
    for key in ("name", "path", "ledger_exists", "total_dispatches", "open_dispatches", "warnings", "error", "pending", "dispatches"):
        check(f"snapshot.repo has `{key}`", key in repo)
    check("total_dispatches == 60", repo["total_dispatches"] == 60, f"({repo['total_dispatches']})")
    check("dispatches limited to config.limit (40)", len(repo["dispatches"]) == 40, f"({len(repo['dispatches'])})")


# --------------------------------------------------------------------------
# Mutant verification: I confirm the tests above KILL each mutant. Where I can,
# I mutate the real production code (OPEN_ALL_CAP) and check via the LIVE
# endpoint; where the mutation would live inline in the handler, I fabricate the
# mutant output and show that the test's predicate REJECTS it.
# --------------------------------------------------------------------------

def _asymmetry_holds(full: dict, filtered: dict) -> bool:
    return (
        full["summary"] == filtered["summary"]
        and full["series"] == filtered["series"]
        and len(full["dispatches"]) != len(filtered["dispatches"])
    )


def _cap_holds(overview: dict, cap: int) -> bool:
    att = overview["attention"]
    total = att.get("_open_all_total", len(att["open_all"]))
    if len(att["open_all"]) > cap:
        return False
    if total > cap and att.get("_capped") is not True:
        return False
    return True


def _totals_consistent(overview: dict) -> bool:
    s = overview["repos"]
    t = overview["totals"]
    return (
        t["total"] == sum(x["total"] for x in s)
        and t["open"] == sum(x["open"] for x in s)
        and t["closed"] == sum(x["closed"] for x in s)
    )


def test_mutants(root: Path) -> list[str]:
    print("\nmutant verification (does the test really kill each one?)")
    killed: list[str] = []

    _write_repo(root, "alpha", _asym_repo())
    client = _client(root)
    full = client.get("/api/repo/alpha").json()
    open_only = client.get("/api/repo/alpha", params={"state": "open"}).json()

    # Sanity: on correct code the predicates pass.
    check("baseline: asymmetry holds", _asymmetry_holds(full, open_only))

    # M1 "state filter is a no-op": filtered list == full. The predicate requires
    # different lengths -> rejects -> killed.
    mutant_noop = dict(open_only, dispatches=full["dispatches"])
    m1 = not _asymmetry_holds(full, mutant_noop)
    check("M1 (state filter no-op) is killed", m1)
    if m1:
        killed.append("state-filter-no-op")

    # M2 "state filter also shrinks the summary": the filtered summary becomes
    # that of a slice. I fabricate a different summary; the predicate rejects -> killed.
    shrunk_summary = dict(full["summary"], total=45, open=45, closed=0)
    mutant_shrink = dict(open_only, summary=shrunk_summary)
    m2 = not _asymmetry_holds(full, mutant_shrink)
    check("M2 (state filter shrinks summary) is killed", m2)
    if m2:
        killed.append("state-filter-shrinks-summary")

    # M3 "OPEN_ALL_CAP ignored": REAL module mutation. I raise the CAP and confirm
    # the live output now violates the test's _cap_holds predicate.
    _write_repo(root, "flood", _open_rows("2026-06-07-flood", main_module.OPEN_ALL_CAP + 95))
    client2 = _client(root)
    real_cap = main_module.OPEN_ALL_CAP
    try:
        main_module.OPEN_ALL_CAP = 10 ** 9  # mutant: cap effectively off
        ov_mut = client2.get("/api/overview").json()
    finally:
        main_module.OPEN_ALL_CAP = real_cap
    ov_real = client2.get("/api/overview").json()
    m3 = _cap_holds(ov_real, real_cap) and not _cap_holds(ov_mut, real_cap)
    check("M3 (OPEN_ALL_CAP ignored) is killed", m3, f"(mut len={len(ov_mut['attention']['open_all'])})")
    if m3:
        killed.append("open-all-cap-ignored")

    # M4 "totals double-count": I fabricate an overview with one repo's total
    # doubled; the consistency predicate rejects -> killed.
    good = ov_real
    doubled = json.loads(json.dumps(good))
    doubled["totals"]["total"] += doubled["repos"][0]["total"]  # counted one repo 2x
    m4 = _totals_consistent(good) and not _totals_consistent(doubled)
    check("M4 (totals double-count) is killed", m4)
    if m4:
        killed.append("totals-double-count")

    print(f"        -> mutants killed: {', '.join(killed)}")
    return killed


def main() -> int:
    with tempfile.TemporaryDirectory() as t1:
        test_repo_filter_asymmetry(Path(t1))
    with tempfile.TemporaryDirectory() as t2:
        test_repo_errors(Path(t2))
    with tempfile.TemporaryDirectory() as t3:
        test_dispatch_endpoint(Path(t3))
    with tempfile.TemporaryDirectory() as t4:
        test_overview_totals(Path(t4))
    with tempfile.TemporaryDirectory() as t5:
        test_open_all_cap(Path(t5))
    with tempfile.TemporaryDirectory() as t6:
        test_snapshot_shape(Path(t6))
    with tempfile.TemporaryDirectory() as t7:
        test_mutants(Path(t7))

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S): {', '.join(FAILURES)}")
        return 1
    print("all main tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
