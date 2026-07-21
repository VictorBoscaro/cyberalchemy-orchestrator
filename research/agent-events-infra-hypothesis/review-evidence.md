---
title: "Review — evidence / ground-truth fidelity: KT reuse discussion for the agent-events infra hypothesis"
node_type: review
is_session: false
layer: architecture, domain
nature: evaluative
status: exploratory
last_updated: 2026-07-20
tags: [review, evidence, knowledge-taxonomy, ground-truth, orchestration]
---

# Review — EVIDENCE / ground-truth fidelity

> Independent check of `research/agent-events-infra-hypothesis/research.md`,
> `research/agent-events-infra-hypothesis/findings.md`, and
> `vault/hypothesis/orchestration-infra.md` against (a) a real clone of
> `cyberAlchemyAI/knowledge-taxonomy` at
> `C:\Users\victo\AppData\Local\Temp\knowledge-taxonomy-clone` and (b) the
> orchestrator's own code (`implementations/server/ledger.py`,
> `.claude/skills/register-dispatch/SKILL.md`,
> `vault/constitution/engine-constitution.md`). Method: read the cited files
> directly, and independently searched for the cited claims. No coordination
> with any other reviewer.

## Prioritized findings

### 1. [HIGH] "The ledger has already earned append-only / one-writer" — contradicted by the orchestrator's own constitution

**Claim.** `vault/hypothesis/orchestration-infra.md` states the thesis must
avoid "breaking the two things the repo has earned: the append-only ledger
([[engine-constitution]] EG-1/EG-6) and the one-shot agent model" (Opening
section), and repeats EG-1 as settled fact three more times: "the one-writer
spine (EG-1)" (Central thesis), "EG-1 (one writer)… constrain the bus to a
projection" (Connections table). `research/agent-events-infra-hypothesis/research.md`
independently asserts "the EG-1 one-writer spine exists to stop exactly this"
(Round 1, orchestrator freeze position, item 2). `findings.md` repeats it as
"keeping the ledger the authoritative permanent tier (CONST-ENG EG-1
one-writer, EG-6 never-re-validated)" with no caveat.

**Check against.** `vault/constitution/engine-constitution.md:115-133` (EG-1
itself).

**Verdict: REFUTED (overclaim).** EG-1's own text says the opposite of
"earned":
> "**veracity:** medium — the reader/appender split is real and old,
> **but** the 2026-07-18 enum-drift (two close rows that bypassed the
> validated appender — see [[ledger-enum-drift-finding]]) is a live
> counterexample: **the invariant is aspired, not yet enforced
> end-to-end**."
> "**Validation:** deterministic… **Blocked** until the drift is traced."

So EG-1 is a `candidate` rule, `veracity: medium`, with a known, currently
unresolved counterexample (two 2026-07-18 close rows that bypassed the
appender), and its promotion to deterministic validation is explicitly
blocked. This is also the exact gap the user's own memory
(`ledger-enum-drift-finding`) flags as something to investigate "before
Phase 2." None of the three artifacts surface this. They cite EG-1 as an
already-secured invariant to build the bus-as-projection design on top of —
which is precisely backwards: the projection design's own collapse-test
("Projection collapses to duplication… EG-1's one-writer spine is broken")
implicitly assumes EG-1 is currently intact, when the constitution says it
is currently *not* fully enforced.

**Fix.** In `orchestration-infra.md`, downgrade "earned" to "asserted,
`veracity: medium`, with a known live counterexample (2026-07-18 enum
drift) that must be resolved — or explicitly accounted for — before the bus
can safely assume EG-1 holds." Add a dependency note: this thesis inherits
EG-1's open blocker; it should not be scheduled to build before
`ledger-enum-drift-finding` is closed, or it should state why the drift
doesn't threaten the projection design. `research.md`/`findings.md` should
soften "EG-1 one-writer spine exists to stop exactly this" to name the
open drift.

---

### 2. [HIGH] `corpus_hash_at_emit` as "machine-checkable witness" / "the load-bearing gift" — the only observed values are all null, and its semantics are nowhere documented in KT

**Claim.** `research.md` (Round 2, infra holder): "**`corpus_hash_at_emit`
is the machine-checkable witness for 'freeze before the channel'**." Carried
into `findings.md`: "and **`corpus_hash_at_emit`** — a machine-checkable
witness for *freeze-before-the-channel*." Carried into
`orchestration-infra.md` (Central thesis): "the load-bearing gift —
**`corpus_hash_at_emit`**, a machine-checkable witness of *what an agent saw
when it emitted*, i.e. the enforcement handle for freeze," and again in the
worked example ("provably formed *before* it saw peers").

**Check against.**
`internal_tools/vault_telemetry/events/subagent-strategy.jsonl` (the actual
file, 3 lines total — the entire real log in the clone).

**Verdict: REFUTED / unverifiable as stated.** The field is present but
**null in both `dispatched` rows** (the only rows that carry it):
```
{"event_name":"subagent-strategy.dispatched", ..., "corpus_hash_at_emit":null, ...}
{"event_name":"subagent-strategy.dispatched", ..., "corpus_hash_at_emit":null, ...}
```
That is a 100% null rate in the only ground-truth sample available. No `.md`
file anywhere in the clone documents what `corpus_hash_at_emit` is supposed
to contain or how it is computed (`grep -rn "corpus_hash_at_emit"
--include=*.md` returns zero hits). So the claim that this field is
currently a working, "machine-checkable" witness of pre-channel state is not
supported by the evidence — the field exists in the schema/format but is
unpopulated in every observed instance, and its intended semantics are
inferred purely from its name, not confirmed by any KT doc. This is worth
distinguishing from "KT has a lifecycle log with this field name" (true) vs.
"this field is a validated freeze-witness mechanism" (asserted well beyond
what a 3-line, all-null sample can support).

**Fix.** Reframe in all three documents: `corpus_hash_at_emit` is a
**field name that exists in the format** (aspirational or unused in
practice, based on the sample) — a candidate slot to borrow, not
demonstrated precedent. Drop "machine-checkable witness" / "load-bearing
gift" language, or hedge it explicitly ("KT defines the field; whether it is
ever populated, and what it hashes, is unconfirmed from the clone").

---

### 3. [MEDIUM] `spec_hash` as "idempotency/dedup key" — asserted as fact, but undocumented in KT

**Claim.** `research.md`: "`spec_hash` = message idempotency/dedup key."
`findings.md`: "`spec_hash` (idempotency/dedup key)." Both stated flatly, no
hedge.

**Check against.** Same JSONL file; `grep -rn "spec_hash" --include=*.md`
across the whole clone returns zero hits, and `internal_tools/` contains no
code that computes or consumes `spec_hash`.

**Verdict: UNVERIFIABLE as stated (overclaim of certainty).** The field
exists and its value looks like a hash, and it is plausible from context
(one dispatched/closed pair shares the same `spec_hash`) that it functions
as a content key — but nothing in the clone documents it as a "dedup key,"
and no dedup behavior is observably enforced anywhere in the repo. This is
a reasonable *inference*, not an established fact, and open question 2 in
`findings.md` ("Does `spec_hash` idempotency collide with register-dispatch's
dedup-on-`dispatch_id`?") already implicitly treats it as confirmed
idempotent — which the "Reuse candidates" table states as settled ("gives")
rather than "inferred."

**Fix.** Mark `spec_hash`'s role as inferred-from-usage-pattern, not
KT-documented, in the reuse table.

---

### 4. [MEDIUM] "`dispatch_id:layer_id:agent_id` compound addressing already exists" in KT — no such compound string is anywhere in the clone

**Claim.** `research.md` (§4): "Per-agent frontmatter carries `agent_id`,
`layer_id`, `dispatch_id`, `role`, `model`, `decision`, `dissent[]`,
`closure_mark` — i.e. **`dispatch_id:layer_id:agent_id` compound addressing
already exists**, dispatch-scoped." Repeated in Round 2 ("IDs — KT agents
already carry `dispatch_id:layer_id:agent_id` (dispatch-scoped, not
global) — confirms mint-per-dispatch"), and carried into
`orchestration-infra.md`: "the same shape KT independently chose
(`dispatch_id:layer_id:agent_id`)."

**Check against.** `discoveries/domain-hierarchy-standards/agents/06-writer-1.md`
frontmatter (confirmed: separate keys `agent_id: writer-1`, `layer_id: L3`,
`dispatch_id: domain-hierarchy-standards-2026-06-08` — three **independent**
fields, never concatenated). A repo-wide search for the literal patterns
`dispatch_id:layer_id` / `layer_id:agent_id` returns **zero hits** anywhere
in the clone.

**Verdict: PARTIALLY REFUTED (overclaim).** The three fields do exist and
are dispatch-scoped, so an agent *can be addressed* by their combination —
but KT never constructs or writes a `dispatch_id:layer_id:agent_id`
compound string; it is three separate frontmatter keys. Saying KT
"independently chose" this "shape" overstates a post-hoc synthesis (three
fields the reviewer combined) as an existing, chosen ID format. This
weakens (not kills) the "convergent evidence" argument the hypothesis
leans on for its own `dispatch_id:group_id:role#index` minting scheme.

**Fix.** Rephrase to: "KT addresses agents via three separate, always-present
fields (`dispatch_id`, `layer_id`, `agent_id`) that are jointly sufficient to
address an agent uniquely within a dispatch — not a literal compound key KT
itself constructs." Do not claim KT "chose the same shape."

---

### 5. [LOW] `ledger.py` citation range is imprecise

**Claim.** Both `findings.md` ("single integration point
`signature()` ([ledger.py:796-807]...)") and `orchestration-infra.md`
("**`signature()`** ([ledger.py:796-807](../../implementations/server/ledger.py#L796-L807))
is a disk fingerprint (mtime_ns + size)...") cite `ledger.py:796-807`.

**Check against.** `implementations/server/ledger.py`: `def signature(...)`
starts at line **790**; the docstring runs 791-795; the function body the
citation actually needs (`parts: list[tuple] = []` through the final
`parts.append(...)`) is lines 796-807, but the closing `return
tuple(parts)` is line **808**, outside the cited range.

**Verdict: VERIFIED, description accurate — citation range slightly off.**
The prose description ("disk fingerprint (mtime_ns + size) that drives SSE
change-detection") is correct. But the line range omits both the `def`
signature (790) and the `return` statement (808), i.e. it cites the loop
body only, not the whole function a reader would need to see cited code
execute.

**Fix.** Cite `ledger.py:790-808` (the full function) instead of `796-807`.

---

### 6. [LOW / informational] Dispatch/agent-model section (§4, research.md) draws from a *different* dispatch than the one otherwise cited, with no inline citation

**Claim.** `research.md` §4 asserts `mode: zig-zag`, `executors: emulated`,
and `exit_reason` including `dissent_irreconcilable` as part of "the"
dispatch/agent model, without naming a source file (unlike §1–§3, which cite
`schema/v2.2.md`, `docs/system-tagging-engine.md`, `decisions/09`, etc.
inline).

**Check against.** These exact tokens (`mode: zig-zag`, `executors:
emulated`, `exit_reason: [success, dissent_irreconcilable,
reviewer_rejected_twice, max_loops_reached]`) all live in
`experiments/E11-domainspec-adoption-pilot/validation/dispatch.yaml`
— a *different* dispatch from the `domain-hierarchy-standards` one used
elsewhere in the trail (whose `dispatch.yaml` shows `mode: task-fan-out` /
`single`, not `zig-zag`).

**Verdict: VERIFIED, but under-cited.** The claims are true — they exist
verbatim in the clone — but the section reads as if describing one uniform
"dispatch model" without flagging that the enum values were pooled across
at least two different dispatch instances in different subfolders. Not
wrong, but the missing per-file citations (present everywhere else in the
same document) make it harder to audit and slightly overstate uniformity.

**Fix.** Add the source path
(`experiments/E11-domainspec-adoption-pilot/validation/dispatch.yaml`) next
to the `mode`/`executors`/`exit_reason` claims, same as the rest of the
section.

---

## Claims verified accurate (spot-checked, no issue found)

- `domain` is a required, open string with no enum/ids/versioning —
  `schema/v2.2.md:194` ("`domain` — open string") and the frontmatter block
  (`domain: <string>  # required`). Confirmed.
- 5 of 6 facets are closed controlled vocabularies (`nature`, `normativity`,
  `temporality`, `source_confidence`, `content_certainty`) —
  `decisions/09-facet-value-enumeration.md` gives the exact enumerations and
  the IRR-invention story cited. Confirmed, including the "documentation
  failure, not an ontology one" framing (decision-09's own conclusion).
- "Tagging is system-generated, never hand-assigned" —
  `README.md:64` (§3, verbatim) and `docs/system-tagging-engine.md` (status:
  draft, rule-layer table, output contract, `decision ∈ {accepted, proposed,
  withheld, unresolved}`). Confirmed, including "spec, not shipped software"
  (no engine code found in `internal_tools/`, only the JSONL log).
- The two JSONL logs and their claimed fields —
  `internal_tools/vault_telemetry/events/subagent-strategy.jsonl` (dispatch
  lifecycle: `event_name`, `spec_hash`, `mode`, `dispatch_kind`,
  `dispatch_id`, `parent_dispatch_id`, and on `.closed`:
  `exit_reason`/`passes_total`/`convergence_passes`/`final_validator_verdict`
  /`residual_dissents`) and `docs/signals/pipeline-signals.jsonl`
  (`id`/`timestamp`/`session`/`feature`/`type`/`severity`/`category`/`data`,
  including `decision`/`proposal` sub-shapes with `alternatives`/`rationale`/
  `confidence`). Confirmed field-for-field against the actual file contents
  (module the two overclaims at #2/#3 above about what the fields *mean*).
- Domain-hierarchy verdict `closed-negative` —
  `discoveries/domain-hierarchy-standards/LEDGER.md`,
  `agents/06-writer-1.md` (`closure_mark: closed-negative`), and
  `research/findings.md` (`closure_mark: closed-negative`, "~70%
  cross-domain bridges," MSC/ACM-CCS/PhilPapers/PhySH named per-field
  standards, method/framework-as-primary-axis recommendation). Confirmed in
  detail, including the "~70%" figure being explicitly flagged in KT's own
  residue ledger as "a 6-sample estimate, not measured corpus-wide" — a
  caveat the infra artifacts correctly do not overstate.
- Residue is two-kind η^sch ⊥ η^ins with an M6 refutation —
  `meta/framework-connection.md` and `meta/four-repos-residue-unification.md`
  ("M6 refutation, proven in Lean with a four-object counterexample and no
  `sorry`... schema discipline does not force instance discipline"; the
  four-object table lines up η^sch vs η^ins for KT specifically). Confirmed,
  including the careful `[proved]` vs `[position]` vs `[open]` labeling that
  the infra artifacts correctly preserve (not overclaimed as more than
  KT itself claims).
- C7 / declared-scope-with-named-residue, decisions 01/06, H1-H5 —
  `decisions/11-stopping-criterion-c7.md`. Confirmed exactly (v2.1 positivist
  scope, 5 humanities failure modes H1-H5, decision-01 subjective-content,
  decision-06 humanistic-scope-boundary, `persistence_lemma` from the sister
  repo's reflection tower).
- "KT has no bus" — repo-wide `grep -rn "bus\b"` across `.md/.jsonl/.py/.js
  /.ts/.cjs` returns **zero** hits anywhere in the clone. Confirmed.
- Orchestrator side: `register-dispatch/SKILL.md` — `connections` are
  `{from, to, type, loop_cap?}` scheduling edges between `group_id`s (no
  message-passing semantics anywhere in the skill); `agent_name` is
  literally documented as "String from the agent pool, or `null`"
  (nullable, confirmed; non-unique is a reasonable inference — no
  uniqueness constraint exists in the schema table); `feedback_prompts` is
  documented as a close-row JSON column, "each `feedback`-edge ask, recorded
  **verbatim**" (confirmed exact wording match); `dispatch_id` format is
  `YYYY-MM-DD-<slug>` (confirmed, SKILL.md line 49). All accurate.
- `expires` (created + 60d) as "the only time-retention vocabulary in the
  repo" — confirmed: `.claude/skills/close-session/SKILL.md:70`
  (`expires: {created + 60 days}`) is the only `expires`-bearing frontmatter
  spec found repo-wide outside the hypothesis document itself.

## Overall verdict

**ACCURATE-WITH-CORRECTIONS.**

The bulk of the KT-facing claims (schema shape, closed/open facets, the
tagging-engine stance, the domain-hierarchy verdict, the two JSONL log
shapes, the residue calculus, C7, and "KT has no bus") check out precisely
against the clone, often down to exact line/wording matches — this is a
carefully-sourced document by KT-research standards. The failure mode is not
sloppy reading of KT; it is **treating two undocumented/unpopulated KT
field names (`corpus_hash_at_emit`, `spec_hash`) as if their intended
semantics were established fact**, and — the more consequential one —
**treating the orchestrator's own EG-1 (one-writer ledger) as an "earned,"
settled invariant when the orchestrator's own constitution explicitly marks
it `veracity: medium`, blocked, with a live unresolved counterexample**
that the user's own memory already flagged as a pre-Phase-2 gate. That last
point (#1) is the one fix that should happen before this thesis is treated
as buildable, since the entire "bus is a projection, not a second store"
argument leans on EG-1 holding.
