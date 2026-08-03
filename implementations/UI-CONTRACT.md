# UI Contract — Phase 1 (reader)

All variants consume the same API and follow the same `data-testid`s, so
that a single Playwright test runs against all ten. **Only the aesthetics vary.**

## Where the file lives

`implementations/static/ui/<slug>/index.html` — **a single self-contained file**.
Inline CSS and JS. **Zero external dependencies** (no CDN, no remote font, no
build): the page has to open offline. Use only system fonts
(`ui-monospace`, `Georgia`, `system-ui`, etc.).

## API

| Endpoint | What it returns |
|---|---|
| `GET /api/snapshot` | The entire state, recent window per repo (see shape below). |
| `GET /api/stream` | SSE. Emits `event: snapshot` with the same payload whenever the disk changes. Connect with `EventSource` and re-render. |
| `GET /api/dispatch/{repo_name}/{dispatch_id}` | A single dispatch without truncating the prompts (for a detail panel). 404 if the repo/id doesn't exist; 500 if the ledger exists but couldn't be read. |
| `GET /api/overview` | Top panel: aggregates for ALL repos + what needs human attention (see shape below). Nothing is truncated by `limit`. |
| `GET /api/repo/{repo_name}` | Drill-down of a repo: the FULL history at listing weight (`slim` rows), plus `summary` and `series`. Optional filters `?state=open\|closed\|all` and `?type=<dispatch_type>` (see the ASYMMETRY below). 404 if the repo doesn't exist; 422 if `state` is outside the enum. |

**The `_` prefix convention (scoped to row-shaped objects):** in an object that
shares the namespace of a ledger row (a dispatch, a sheet), every field
with a `_` prefix is computed by the reader and the rest come literally from the ledger — the
`_` exists so that a computed field never shadows a real ledger key (e.g.,
`status` in pre-v0.5.2 rows). The rule does NOT apply to container/aggregate objects that
aren't rows (`summary`, `series`, `totals`, `attention`): they have no
ledger namespace to protect, and so they return keys without a prefix on purpose (`total`,
`open`, `by_type`, ...).

### DAY reference — UTC

`today`, each dispatch's `_day`, and the buckets of `series["days"]` are **UTC
calendar days**, not the browser's timezone. This is deliberate: the server and all
clients need to agree on which chart bar a row falls into. If a client
used the LOCAL day, the same row would jump buckets depending on who's looking, and the UI's "today"
would diverge from the rows' `_day` by a few hours every day. Derive the day from the
`_day`/`today` field the API already gives you — **do not** recompute it from `created` with
`new Date()` in the local timezone.

### Shape of `/api/snapshot`

```jsonc
{
  "repos": [
    {
      "name": "domainspec-lean-formalization",
      "path": "C:\\Users\\victo\\...",
      "ledger_exists": true,
      "total_dispatches": 334,      // total in the ledger
      "open_dispatches": 23,        // no close row
      "warnings": ["line 13: ..."], // old rows unreadable (non-fatal)
      "error": null,                // fatal read failure
      "pending": [ /* pre-confirm sheets — see below */ ],
      "dispatches": [ /* the N most recent, newest first */ ]
    }
  ],
  "config": { "limit": 40, "poll_seconds": 1.0, "repo_count": 11 }
}
```

### A dispatch

The current writer emits schema `0.6.2`. The reader remains deliberately
compatible with historical `0.6.0` and `0.6.1` rows and does not rewrite ledger data.

```jsonc
{
  "dispatch_id": "2026-06-12-residue-precedent-sweep",
  "schema_version": "0.6.2",
  "created": "2026-06-12T18:00:00.000Z",
  "invoked_by": "victorboscaro@gmail.com",
  "dispatch_type": "review",          // research|code|review|plan|suggestion|experiment
  "goal": "…",
  "context": "…",
  "max_loops": 1,
  "final_approver": "parent",
  "anti_bias_mode": "enabled",       // enabled|disabled; required since 0.6.2
  "anti_bias_global": "novelty optimism vs precedent skepticism",
  "working_folder": "research/…/",
  "output_mode": "persisted",         // review only: inline|persisted
  "groups": [
    {
      "group_id": "explorers",
      "n": 2,
      "anti_bias": "source corpus (formal literature vs practice blogs)",
      "robot_talks": false,            // optional
      "layers": 1,                     // optional
      "agents": [
        {
          "agent_name": "Abramsky, Samson",   // can be null
          "role": "explorer",                 // explorer|synthesizer|skeptic|writer|auditor|planner|coder
          "model": "claude-sonnet-5",
          "token_budget": 800,
          "angle": "takes the side of the formal literature",
          "initial_prompt": "…",
          "_prompt_truncated": true           // present only if truncated
        }
      ]
    }
  ],
  "connections": [
    { "from": "explorers", "to": "synthesizer", "type": "sequential" },
    { "from": "skeptic", "to": "synthesizer", "type": "feedback", "loop_cap": 2 }
  ],

  // computed by the reader:
  "_state": "open",        // "open" | "closed"
  "_live": true,           // dispatch_type is LIVE (research/code/review/experiment)
  "_legacy": false,        // pre-v0.5.2 row, no `groups`
  "_agent_count": 3,
  "_orphan_close": true,   // present only on a close row without a dispatch row
  "_close": {              // null while open
    "close_of": "…",
    "closed": "2026-06-12T19:00:00.000Z",
    "exit_reason": "resolved",  // resolved|loop_ceiling_reached|dissent_irreconcilable|user_abort|error
    "agents_spawned": { "total": 3, "tree": {"explorer": 2}, "loops_used": 1 },
    "feedback_prompts": ["…"]
  }
}
```

### A pending sheet

```jsonc
{
  "_file": "2026-07-19-example.json",
  "_path": "C:\\…\\telemetry\\agents\\pending\\2026-07-19-example.json",
  "_mtime": 1752900000.0,
  "_error": null,
  "_agent_count": 4,
  "_live": true,
  "sheet": { /* same shape as the dispatch, WITHOUT the `_` fields or `_close` */ }
}
```

> `_mtime` is `null` (instead of an epoch float) when `_error` is set — the
> sheet disappeared or became unreadable between the scan and the read.

### Shape of `/api/overview`

Aggregates for ALL repos + the human attention queues. Nothing truncated by `limit`.

```jsonc
{
  "repos": [ /* one `summary` object per repo — see shape below */ ],
  "totals": {
    "repos": 11,
    "total": 703, "open": 43, "closed": 660, "pending": 1,
    "by_type": { "research": 500, "review": 140, "(no type)": 55 },  // summed per repo
    "today": { "created": 3, "closed": 1 }                            // UTC day
  },
  "today": "2026-07-20",           // TODAY's day in UTC
  "attention": {
    "pending": [ /* pending sheet + "_repo": "<name>" */ ],
    "open_today": [ /* `slim` dispatch + "_repo", open and with _day == today */ ],
    "open_all":  [ /* `slim` dispatch + "_repo", all open; MAX. 200 */ ],
    "_capped": true,               // present ONLY when open_all exceeded 200
    "_open_all_total": 253         // present ONLY when capped — the real total
  },
  "config": { "limit": 40, "poll_seconds": 1.0, "repo_count": 11 }
}
```

Each object in `repos` (and the `summary` from `/api/repo`) — a repo's aggregate:

```jsonc
{
  "name": "domainspec-core", "path": "C:\\…", "ledger_exists": true, "error": null,
  "warning_count": 0,             // how many old rows produced a warning
  "total": 181,                   // all joined rows (not the `limit` window)
  "open": 5, "closed": 176,
  "legacy": 12,                   // pre-v0.5.2 rows (no `groups`)
  "by_type": { "research": 150, "review": 20, "(no type)": 11 },
  "live": 170,                    // dispatch_type LIVE (research/code/review/experiment)
  "reserved": 4,                  // non-LIVE and non-legacy type
  "pending_count": 0,
  "today": { "created": 0, "closed": 0 },
  "open_now": 5,                  // == open (own name; may diverge in Phase 2)
  "first_day": "2026-01-01", "last_day": "2026-07-19",  // UTC days
  "last_created": "2026-07-19T20:00:00.000Z"            // most recent raw ISO
}
```

> **Not a partition:** `total == live + reserved + legacy` is **not** guaranteed. A
> research row whose `groups` failed lenient parsing ends up without `groups` and counts in
> `live` AND in `legacy` at the same time. Don't render the three as slices of a whole.

### Shape of `/api/repo/{repo_name}`

```jsonc
{
  "name": "domainspec-core", "path": "C:\\…", "ledger_exists": true, "error": null,
  "warnings": [ "line 13: …" ],
  "summary": { /* same shape as the `repos` object above — ALWAYS the entire repo */ },
  "series": { /* daily histogram — see below */ },
  "pending": [ /* this repo's pending sheets */ ],
  "dispatches": [ /* `slim` rows, newest first; THIS list is filtered */ ]
}
```

**Deliberate ASYMMETRY:** `?state=` and `?type=` filter **only** `dispatches`. The
`summary` and `series` always describe the entire repo — the chart is the stable
backdrop, the list is the cut. If the series shrank along with it, the axis would change
scale on every click.

The `dispatches` list is **`slim`** (counts instead of prompts, and a trimmed-down
`_close`): it's lossy for the old keys of legacy rows. For the entire row (all
fields, uncut prompts), request `GET /api/dispatch/{repo}/{dispatch_id}`.

A `slim` row:

```jsonc
{
  "dispatch_id": "…", "created": "…Z", "_day": "2026-06-12",  // _day is UTC
  "dispatch_type": "research", "goal": "… (cut to ~240 chars)",
  "invoked_by": "…", "working_folder": "…", "max_loops": 1,
  "final_approver": "parent", "anti_bias_mode": "enabled", "anti_bias_global": "…",
  "_state": "open", "_live": true, "_legacy": false, "_agent_count": 3,
  "_close": { "closed": "…Z", "exit_reason": "resolved" },  // null while open
  "_goal_truncated": true,        // only if the goal was cut
  "_orphan_close": true,          // only on an orphan close row
  "_group_count": 2, "_robot_talks": false,
  "_roles": { "explorer": 2, "writer": 1 },
  "_connection_types": [ "feedback", "sequential" ]
}
```

The `series` histogram (from `daily_series`):

```jsonc
{
  "days": [ "2026-06-01", "2026-06-02", … ],  // contiguous, UTC; upper edge = today
  "types": [ "research", "review" ],          // sorted
  "series": { "research": [1,0,2,…], "review": [0,1,0,…] },  // aligned to `days`
  "totals": { "research": 42, "review": 8 },  // only what's PLOTTED
  "max_day": 5,                               // the tallest stacked column
  "undated": 3,                               // rows without a readable day
  "out_of_range": 1,                          // rows dated outside the window…
  "truncated_span": false                     // …(cap of 1000 days, future, or days=N)
}
```

> Invariant: `sum(totals) + out_of_range + undated == total rows`. A date in the
> distant future (century typo) does not anchor the axis — it becomes `out_of_range`.

## What the screen needs to communicate

In order of importance — the UI exists for the **human gate**:

1. **Pending sheets first, with strong emphasis.** This is the proposal
   awaiting confirmation: the most important object on the screen. If there are zero,
   say so explicitly instead of leaving it empty.
2. **"Dispatch" button on each pending sheet — `disabled`**, with the label
   making clear it's Phase 2 (e.g., title "confirmar dispara na Fase 2").
   It marks the gate's place; it doesn't work yet.
3. **Open vs closed.** A dispatch with no close row is alive. When closing,
   show the `exit_reason` (`resolved` is good; `error` and
   `dissent_irreconcilable` deserve an alert color).
4. **Anti-bias mode, groups and agents**: show `anti_bias_mode` explicitly. When
   enabled, show each agent's **`angle`** against the group's **`anti_bias`**;
   when disabled, do not report missing tension fields as an error.
5. **`connections` as typed edges**: `sequential`, `zig-zag`, `feedback`
   need to be visually distinct; show `loop_cap` when present.
6. **LIVE vs RESERVED.** `research`, `code`, `review`, and `experiment` are LIVE.
   `plan` and `suggestion` are reserved — mark them visibly.
7. **Legacy rows** (`_legacy: true`, no `groups`) and **`_orphan_close`** must
   appear as what they are, not disappear.
8. **Warnings and errors per repo** accessible (can be collapsed).
9. **Live connection indicator** (SSE connected / down).
10. Filter or grouping by repo — there are 11 repos and ~700 dispatches.

## Required `data-testid`s

The Playwright test is the same for all ten. Without these attributes, the variant fails.

| testid | Where |
|---|---|
| `app` | Root element, after the first render. |
| `live-indicator` | SSE state. Must contain the text `connected` when connected. |
| `pending-list` | Container for pending sheets (exists even with zero). |
| `pending-card` | One per pending sheet. |
| `dispatch-button` | One per pending sheet, `disabled`. |
| `dispatch-list` | Container for the history. |
| `dispatch-card` | One per rendered dispatch. |
| `repo-section` | One per repo shown (or per repo group). |
| `total-count` | Element whose text contains the total dispatch count. |

In addition, every `dispatch-card` must carry
`data-dispatch-id="<dispatch_id>"` and `data-state="open|closed"`.

## Rules

- Portuguese in labels.
- Has to handle `null`/missing in almost everything: old rows don't have `groups`,
  `agent_name` can be `null`, `connections` may not exist.
- ~700 dispatches total — don't freeze the page; the API already limits to 40 per repo.
- No writing: it's a reader.
