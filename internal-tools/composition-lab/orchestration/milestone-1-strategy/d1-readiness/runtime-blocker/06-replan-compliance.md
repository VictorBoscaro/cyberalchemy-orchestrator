---
artifact_kind: runtime-blocker-replan-compliance
status: ready-for-strategy-replan
date: 2026-08-13
scope: connectionless staged research under the current legacy-managed runtime
---

# Replan compliance: smallest valid connectionless sequence

## Verdict

The current runtime can execute only connectionless, turn-zero seats with empty input manifests.
That makes the following alternatives materially different:

1. **Several independent `n=1` research dispatches:** valid. Each dispatch can inspect its own
   frozen corpus, writes only its own `findings.md`, is approved and closed independently, and has
   no downstream claim.
2. **One dispatch containing several explorers and no connections:** structurally compilable but
   not a valid replacement for D1a. With total `n >= 2`, the research capability requires both
   `research.md` and `findings.md`; parallel explorers have neither a governed collector nor a
   consumer of the other returns. Concurrent shared-file writes would introduce races and still
   would not prove collection or synthesis.
3. **A later connectionless synthesis dispatch:** valid only if its complete effective upstream
   content is frozen into the exact confirmed `initial_prompt`. Merely naming repository paths and
   asking the writer to read them is the weaker staged-repository handoff diagnosed in 02/05 and,
   when treated as a required upstream input, triggers the lifecycle requirement for a governed
   non-empty manifest compiler extension that does not exist.
4. **Approval:** `final_approver: parent` is the only executable choice for these one-seat
   dispatches. The schema does not admit a human identity as `final_approver`; the human confirms
   each opening sheet. A dedicated agent approver inside the same connectionless dispatch would
   launch at turn zero without governed access to the result it must approve and can race it.

Therefore the smallest sequence that preserves D1a's four distinct proof regimes, a synthesis,
and an independent coverage check is **six successful one-seat research dispatches**:

```text
E1 configuration --\
E2 enacted traces --+--> S1 synthesis --> A1 coverage/provenance audit
E3 normative status-+
E4 controls --------/
```

The arrows are parent-enforced stage boundaries between closed dispatches, not ledger
`connections`, runtime handoffs, or evidence that a consumer read a repository file. S1 receives
the exact bytes of E1-E4 inside its confirmed prompt. A1 receives the exact S1 bytes, its source
manifest, and, if needed for a claimed check, the exact E1-E4 bytes inside its confirmed prompt.
All six opening records omit `connections` entirely.

If A1 returns a correction, the smallest valid correction is a **seventh, new S2 writer
dispatch**, followed by a new audit dispatch. It is not a `feedback` loop and must not be reported
as one. The current D1a `max_loops: 2` has no force across these dispatches; a two-correction policy
must be kept explicitly in the orchestration plan and each round separately confirmed, opened,
and closed.

This replan does not preserve the original D1a runtime claim. It supports only: each producer
dispatch completed and froze a result; a later prompt contained specified bytes from those
results; and the downstream agent was launched with that prompt digest. It does not establish an
intradispatch data edge, runtime-observed producer output, or causal consumption.

## Preconditions common to every dispatch

Before shaping each dispatch, the lifecycle must possess:

- the objective and boundaries;
- an unmodified strategy route receipt resolving `research` to ledger type `research`, capability
  ref `research`, authority `legacy-managed`, and tool profile `host/inherited@1`;
- a complete, local `research-initial-definitions.md` in that dispatch's unique working folder;
- an entry-prepared exact opening JSON and its entry-owned non-mutating validation receipt;
- an unused `YYYY-MM-DD-<slug>` dispatch ID and an agent name present in
  `telemetry/agents/agent-pool.yaml`.

The existing D1a `route-receipt.json`, opening record, validation receipt, and confirmation cannot
be reused: the objective, groups, prompts, outputs, approver, working folders, and topology all
change. Each new dispatch needs its own current route receipt and validation. `parent_dispatch_id`
must be absent unless a real registered meta-dispatch planned these records; the mere fact that the
parent orchestrates a series does not authorize that field.

The user's requirement that other agents help decide every substantive dispatch is satisfied only
if the current planning/replan dispatch supplies the frozen stage design, and later agents prepare
material upstream-dependent prompts. Reading it literally as “every helper invocation must first
have another helper invocation” has no finite base case. It cannot create an unregistered helper:
`research` owns no bounded helper exemption. Any additional governed planning dispatch would need
its own route, confirmation, opening, binding, verification, and close.

## Exact initial-definition and output layout

No working folder is shared. This avoids `findings.md` collisions and makes every research output
contract locally complete.

| Dispatch | Required initial definitions | Required output |
|---|---|---|
| E1 | `internal-tools/composition-lab/research/milestone-1/01-repository-inventory/stages/01-configuration/research-initial-definitions.md` | same folder, `findings.md` |
| E2 | `.../stages/02-enacted-traces/research-initial-definitions.md` | same folder, `findings.md` |
| E3 | `.../stages/03-normative-status/research-initial-definitions.md` | same folder, `findings.md` |
| E4 | `.../stages/04-controls/research-initial-definitions.md` | same folder, `findings.md` |
| S1 | `.../stages/05-raw-synthesis/research-initial-definitions.md` | same folder, `findings.md` |
| A1 | `.../stages/06-coverage-audit/research-initial-definitions.md` | same folder, `findings.md` |

Here `...` expands to
`internal-tools/composition-lab/research/milestone-1/01-repository-inventory`.

Each initial-definitions document must contain, in the research capability's informational
categories, the local business context, purpose, refinable question, confirmed constraints,
current evidence baseline, and known gaps. E1-E4 inherit the common boundaries from the existing
repository-inventory definitions but narrow the question and corpus segment to their one proof
regime. S1 must additionally state that E1-E4 are frozen evidence inputs, identify their producer
dispatch IDs, paths, SHA-256 digests, byte sizes, close status, and the reduced claim. A1 must do
the same for S1 and define the exact audit checks. These documents supply context; they do not
substitute for putting required upstream bytes into the confirmed prompt.

For `n=1`, `findings.md` is the only capability-required research output. There is no
`research.md`. The four extractor findings remain the preserved raw returns; S1 cites them by
dispatch ID, path, and digest and synthesizes them in its own `findings.md`. This is compliant with
the output rule and is more honest than manufacturing a nominal `research.md` in a one-seat
dispatch.

## Six exact opening-record shapes

Every opening is a separate strict schema `0.6.3` record with exactly these common choices:

```json
{
  "schema_version": "0.6.3",
  "dispatch_type": "research",
  "max_loops": 1,
  "final_approver": "parent",
  "invoked_by": "victorboscaro@outlook.com",
  "groups": [
    {
      "group_id": "<one unique group id>",
      "n": 1,
      "agents": [
        {
          "role": "<explorer|writer|auditor>",
          "model": "<confirmed concrete model>",
          "token_budget": "<confirmed positive integer>",
          "agent_name": "<pool name>",
          "initial_prompt": "<complete frozen briefing>"
        }
      ]
    }
  ]
}
```

`token_budget` is an integer in the real JSON. The record also contains its unique
`dispatch_id`, non-empty `goal`, 2-4 sentence `context`, and exact `working_folder`. It omits
`connections`, `meta`, `parent_dispatch_id`, `output_mode`, `code_contract`, timestamps, and all
unknown keys. In particular, do not carry the old `anti_bias_mode` field into these records unless
the current entry skill emits and validates it under a newer authoritative schema.

The stage-specific values are:

| ID | group / role / agent | budget | goal and prompt effect |
|---|---|---:|---|
| `2026-08-13-lens-inventory-configuration` | `configuration`; explorer; Liskov | 6,500 | Extract only occurrence identity and literal dispatch/configuration fields from the frozen D1 corpus segment; write its own `findings.md`; no classification or effect claim. |
| `2026-08-13-lens-inventory-enacted-traces` | `enacted_traces`; explorer; Nonaka | 6,500 | Extract only preserved enacted traces from the two frozen Robot-Talks samples; write its own `findings.md`; do not infer execution or effect. |
| `2026-08-13-lens-inventory-normative-status` | `normative_status`; explorer; Lamport | 6,500 | Extract only normative/provenance clauses and statuses from the frozen skill/probe/review segment; write its own `findings.md`; separate prescription from instance. |
| `2026-08-13-lens-inventory-controls` | `controls`; explorer; Peirce | 6,500 | Run the eight preregistered control searches on frozen occurrence identities; write its own `findings.md`; use witness/not-observed without classifying composition. |
| `2026-08-13-lens-inventory-raw-synthesis` | `raw_synthesis`; writer; Knuth | 10,500 | Consume the verbatim E1-E4 bytes embedded in the prompt; apply the ownership/merge rule; emit the deduplicated raw inventory in `findings.md`, preserve conflict, and make no lens/composition/effect classification. |
| `2026-08-13-lens-inventory-coverage-audit` | `coverage_audit`; auditor; Hamming | 5,000 | Consume the embedded frozen S1 bundle (and embedded raw bytes required by each audit check); emit a findings verdict matrix/PASS-or-bounded-corrections with exact evidence; perform no synthesis correction. |

Before S1 is entry-prepared, all E1-E4 close rows must exist and their `findings.md` bytes must be
frozen. Its `initial_prompt` must contain, for each source, a delimiter, producer dispatch ID,
repo-relative path, SHA-256, byte size, and the complete bytes. Before A1 is entry-prepared, S1
must likewise be closed and frozen. The human confirms these exact long prompts; replacing even one
embedded byte is a material change requiring a new validation and confirmation.

If prompt size exceeds the effective host context or any complete content cannot be embedded, this
route fails closed. Falling back to path-only reading would require the governed repository-source
manifest compiler extension identified in diagnostics 02 and 05.

## Confirmation, compile, open, launch, verify, and close per stage

For each of E1-E4, then S1, then A1, perform the complete lifecycle independently:

1. **Confirm:** show the human the exact opening JSON, sole agent and complete prompt, model,
   token budget, filesystem effect (`findings.md` only), and exact working folder. Obtain explicit
   confirmation for that record. A batch confirmation cannot cover S1 or A1 before their embedded
   upstream bytes exist.
2. **Compile:** use the frozen opening JSON, current `research` capability ref, authority
   `legacy-managed`, and `.codex/workflow-inputs/<dispatch-id>`. Use only the generated
   `launch-plan.json`; do not edit the empty manifest or binding envelope.
3. **Open once:** call `dispatch_workflow open` with a unique nonce, host, session name, and origin
   ref. Require `status=launch-authorized`, one session ID, the ledger append receipt, and ACI
   opening receipt. Do not call the appender separately and do not save bridge stdout in the
   working folder.
4. **Launch:** invoke exactly the sole generated `spawn_arguments`. The first line must be the
   generated `ACI-WORKFLOW-BINDING-V1:` envelope, and the hook must authorize the same parent.
5. **Verify:** join the seat; inspect the actual `findings.md`, checks, effective model/tool surface,
   and terminal binding. Parent approval is a lifecycle act and cannot be skipped under the user's
   “orchestrate only” constraint. If that constraint forbids even artifact/receipt verification,
   no compliant dispatch can close.
6. **Close once:** only after acceptance, call `dispatch_workflow close` and require
   `status=closed` plus YAML/orchestration receipts. Never hand-edit the ledger.

For a successful first-pass stage, the exact close-record shape is:

```json
{
  "close_of": "<that dispatch_id>",
  "exit_reason": "resolved",
  "agents_spawned": {
    "total": 1,
    "tree": {"<explorer|writer|auditor>": 1, "helpers": 0},
    "loops_used": 0
  },
  "invoked_by": "victorboscaro@outlook.com"
}
```

`feedback_prompts` is absent because there is no feedback edge. A retry/re-run must be reflected in
the actual counts and `loops_used`; do not copy the nominal close. Use `error`, `user_abort`, or
another closed-vocabulary reason when that is what happened. Every dispatch produces exactly two
ledger appends through open/close: one opening row and one close row.

## Approver boundary

The human is mandatory at the Principle-2 opening confirmation gate but is not a legal persisted
`final_approver` value. `parent` is legal and minimal. It does not authorize the parent to perform
the explorer, writer, or auditor work; it does require the parent to verify the actual artifact,
binding terminality, and the selected capability's acceptance contract before closing.

Using a dedicated approver is possible only after a valid way exists to give it the artifact it
approves. Under the current runtime that means a separate connectionless audit/approval dispatch
with the relevant bytes embedded in its exact prompt, whose own `final_approver` is still `parent`.
Putting an approver beside a producer in one no-connections dispatch is not independent downstream
approval.

## Final decision

Adopt the six-dispatch staged program if the milestone accepts the reduced evidence claim and the
cost of six confirmations, openings, output checks, and closes. Reject the single multi-explorer
connectionless dispatch. Do not reuse or flatten the existing D1a record. If exact files cannot be
embedded in the confirmed S1/A1 prompts, stop: the next valid route is the governed repository
manifest extension, not an informal path handoff.

The missing `runtime-blocker/04-*.md` is itself a repository fact: this assessment read the existing
01, 02, 03, and 05 diagnostics and did not infer a nonexistent fourth report.
