"""Phase 1 — the reader.

Serves, live, the pending sheets (pre-confirm) and the dispatch history read from
the append-only ledgers of several repos.

This server is **read-only**. The "Fire" button is Phase 2: it writes a confirm,
and whoever runs the chain (check-tension → register-dispatch → agents) is still
Claude in the session. Nothing here writes to the ledger.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from . import config as config_module
from . import ledger

CFG = config_module.load()
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

# Cap on the "everything that's open" list. 200 fits a scrollable screen; beyond
# that what the human needs isn't a longer list, it's a filter.
OPEN_ALL_CAP = 200

app = FastAPI(title="Dispatch control plane — reader", version="0.1.0")


def today_utc() -> str:
    """Today's day in UTC — the SAME reference frame as `ledger.iso_date`.

    If we used local time here and UTC there, the UI's "today" wouldn't match the
    rows' `_day` bucket for a few hours every day. A single reference frame.
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _sort_key(row: dict[str, Any]) -> str:
    """Sorts by recency, tolerating absence: `created`, else the day, else nothing."""
    created = row.get("created")
    if isinstance(created, str):
        return created
    return row.get("_day") or ""


def snapshot() -> dict:
    repos = CFG.resolved_repos()
    return {
        "repos": [ledger.read_repo(r, CFG.limit, CFG.prompt_limit) for r in repos],
        "config": {
            "limit": CFG.limit,
            "poll_seconds": CFG.poll_seconds,
            "repo_count": len(repos),
        },
    }


@app.get("/api/snapshot")
async def api_snapshot() -> dict:
    return snapshot()


@app.get("/api/dispatch/{repo_name}/{dispatch_id}")
async def api_dispatch(repo_name: str, dispatch_id: str) -> dict:
    for repo in CFG.resolved_repos():
        if repo.name == repo_name:
            # The parse is ALWAYS lenient and never raises `LedgerError` — the old
            # `except LedgerError` here was dead code. An unreadable ledger becomes
            # `.error` (OSError caught in the parse), and `find_dispatch` only looks
            # at `ledger_exists`, so without this check a read error would disguise
            # itself as a 404 "dispatch not found". Surface it as a 500.
            data = ledger.load_repo_rows(repo, copy=False)
            if data.error:
                raise HTTPException(status_code=500, detail=data.error)
            found = ledger.find_dispatch(repo, dispatch_id)
            if found is None:
                raise HTTPException(status_code=404, detail="dispatch not found")
            return found
    raise HTTPException(status_code=404, detail="repo not found")


@app.get("/api/overview")
async def api_overview() -> dict:
    """Top panel: aggregates of ALL repos + what needs human attention.

    Distinct from `/api/snapshot`, which serves each repo's recent window. Here
    nothing is truncated by `limit` — the counts are over the entire ledger.
    """
    today = today_utc()
    repos = CFG.resolved_repos()

    summaries: list[dict[str, Any]] = []
    pending_all: list[dict[str, Any]] = []
    open_all: list[dict[str, Any]] = []
    open_today: list[dict[str, Any]] = []

    totals_by_type: dict[str, int] = {}
    totals = {"total": 0, "open": 0, "closed": 0, "pending": 0}
    today_totals = {"created": 0, "closed": 0}

    for repo in repos:
        # Read the pending sheets ONCE per repo and reuse: `summarize_repo` only
        # needs the count and the attention list needs the entries. Before there
        # were two `read_pending` per repo per request (a disk glob each).
        pending = ledger.read_pending(repo)
        summary = ledger.summarize_repo(repo, today=today, pending=pending)
        summaries.append(summary)

        totals["total"] += summary["total"]
        totals["open"] += summary["open"]
        totals["closed"] += summary["closed"]
        totals["pending"] += summary["pending_count"]
        today_totals["created"] += summary["today"]["created"]
        today_totals["closed"] += summary["today"]["closed"]
        for kind, count in summary["by_type"].items():
            totals_by_type[kind] = totals_by_type.get(kind, 0) + count

        # `_repo` marks the origin: the attention lists mix repos, and without the
        # label the client can't link back to the drill-down.
        for entry in pending:
            entry["_repo"] = repo.name
            pending_all.append(entry)

        for row in ledger.load_repo_rows(repo, copy=False).rows:
            if row.get("_state") != "open":
                continue
            item = ledger.slim(row)
            item["_repo"] = repo.name
            open_all.append(item)
            if item["_day"] == today:
                open_today.append(item)

    open_all.sort(key=_sort_key, reverse=True)
    open_today.sort(key=_sort_key, reverse=True)

    attention: dict[str, Any] = {
        "pending": pending_all,
        "open_today": open_today,
        "open_all": open_all[:OPEN_ALL_CAP],
    }
    # The flag lives on the `attention` container, not the list: JSON doesn't let
    # you annotate an array. `_open_all_total` is the real number, so the UI can say
    # "200 of N".
    if len(open_all) > OPEN_ALL_CAP:
        attention["_capped"] = True
        attention["_open_all_total"] = len(open_all)

    return {
        "repos": summaries,
        "totals": {
            "repos": len(repos),
            **totals,
            "by_type": dict(sorted(totals_by_type.items())),
            "today": today_totals,
        },
        "today": today,
        "attention": attention,
        "config": {
            "limit": CFG.limit,
            "poll_seconds": CFG.poll_seconds,
            "repo_count": len(repos),
        },
    }


@app.get("/api/repo/{repo_name}")
async def api_repo(
    repo_name: str,
    state: str | None = Query(None, pattern="^(open|closed|all)$"),
    type: str | None = Query(None),
) -> dict:
    """Drill-down of a repo: the COMPLETE history at listing weight.

    DELIBERATE ASYMMETRY: `state` and `type` filter ONLY `dispatches`. The `summary`
    and the `series` always describe the entire repo, unfiltered. If the chart
    shrank along with the list, the user would lose the reference exactly when
    comparing a slice against the whole — and the axis would rescale on every click.
    The chart is the backdrop; the list is the slice.
    """
    repo = next((r for r in CFG.resolved_repos() if r.name == repo_name), None)
    if repo is None:
        raise HTTPException(status_code=404, detail="repo not found")

    data = ledger.load_repo_rows(repo, copy=False)
    today = today_utc()
    pending = ledger.read_pending(repo)  # one read, reused by summary and by the response

    # Normalize to the default: this way the handler is also callable directly from
    # inside the process (tests), where the defaults would arrive as `Query` objects
    # instead of strings and would filter the whole list out.
    state = state if isinstance(state, str) else "all"
    kind = type if isinstance(type, str) and type else None

    rows = [ledger.slim(row) for row in reversed(data.rows)]  # newest first
    if state != "all":
        rows = [r for r in rows if r["_state"] == state]
    if kind:
        rows = [r for r in rows if (r.get("dispatch_type") or ledger.NO_TYPE) == kind]

    return {
        "name": repo.name,
        "path": str(repo),
        "ledger_exists": data.ledger_exists,
        "error": data.error,
        "warnings": list(data.warnings),
        "summary": ledger.summarize_repo(repo, today=today, pending=pending),
        "series": ledger.daily_series(data.rows),
        "pending": pending,
        "dispatches": rows,
    }


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.get("/api/stream")
async def api_stream() -> StreamingResponse:
    """SSE. Emits the entire snapshot whenever the disk changes.

    Diffing isn't worth it here: the payload is small (bounded by `limit`) and the
    entire snapshot is trivially correct — a client that connects mid-stream
    arrives with the right state already.
    """

    async def gen():
        last = ledger.signature(CFG.resolved_repos())
        yield _sse("snapshot", snapshot())
        while True:
            await asyncio.sleep(CFG.poll_seconds)
            current = ledger.signature(CFG.resolved_repos())
            if current != last:
                last = current
                yield _sse("snapshot", snapshot())
            else:
                yield ": keepalive\n\n"

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def main() -> None:
    import uvicorn

    repos = CFG.resolved_repos()
    print(f"observing {len(repos)} repos:")
    for repo in repos:
        print(f"  - {repo}")
    print(f"\n  http://{CFG.host}:{CFG.port}\n")
    uvicorn.run(app, host=CFG.host, port=CFG.port, log_level="warning")


if __name__ == "__main__":
    main()
