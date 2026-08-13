# Review — runtime type expansion dispatch

**Verdict: BLOCK**

The dispatch is structurally valid, but it cannot yet achieve its stated objective or execute under
its own governed-lifecycle contract. The blocking defects are architectural rather than cosmetic:
`other` is scoped only to `orchestrate`, while the objective requires a safe generic route for any
installed capability lacking a specialized type; and the dispatch's own code work cannot be
launched because every valid `code` opening has connected topology, which the current compiler
rejects before producing a launch plan.

## Coverage

| lens | attacks performed | result |
|---|---|---|
| Fidelity / governance | Compared the objective, exact intended behavior, non-goals, capability mappings, lifecycle claims, review ordering, and historical `others` contract. | Two CRITICAL and three MAJOR findings survived. |
| Mechanics / correctness | Re-ran the dispatch-spec validator; inspected registry, resolver, appender, compiler, blocked session, implementation route, integrity manifest, dirty worktree, and directly affected tests. | Structural validation passed; the execution route does not. |
| Abuse / gaming | Attempted unknown-capability fallback, malformed-code degradation, type/capability mismatch, live-but-non-routable opening, review self-verification, and schema-version ambiguity. | The stated anti-fallback boundary is sound, but the proposed route either remains incomplete or would need a new capability-binding contract to avoid bypass. |

Deterministic evidence:

- `python .agents/skills/dispatch-spec/scripts/validate-dispatch.py internal-tools/need-driven-system-writing/runtime-type-expansion-dispatch.json` → `VALIDATION=pass`.
- `python -m unittest implementations.tests.runtime.test_dispatch_workflow -v` → 6/6 passing.
- Current resolution: `domainspec-implement → code`; `orchestrate`, `decision-gate`,
  `system-view`, `close-session`, and `task-session` each fail with “has no routable dispatch type.”
- The worktree already contains user-owned modifications to the stage-E source manifest and
  `implementations/server/runtime/local_pilot.py`, both integrity-adjacent to the proposed changes.

## Findings

### RTE-01 — `other` does not cover the class of missing-type failures — CRITICAL

**Quoted evidence:** the objective says the runtime should represent “general governed work,” and
the operator's raw request says “pra que a gente nunca deixe de rodar um dispatch por nao ter
tipo.” The exact behavior narrows that to: “A new governed dispatch whose selected installed
capability is orchestrate resolves to the singular canonical ledger dispatch type other.”

Mapping only `orchestrate → other` does not satisfy the broader objective. The blocked implementation
route selects `decision-gate`, `system-view`, `task-session`, `close-session`, and qualified variants
of those capabilities. None would resolve after the proposed change. `code` is already live and
routable through `domainspec-implement`; preserving it is necessary but is not a type expansion.

**Required repair:** redesign `other` as a classification for a *known, installed, explicitly
selected capability that lacks a specialized type*, not as an alias for `orchestrate` and not as an
unknown-capability catch-all. Specialized mappings must win first. The fallback must:

1. resolve only an exact installed capability identity and installed capability path;
2. retain that actual capability identity in the route/binding evidence while emitting ledger type
   `other`;
3. enforce an explicit authority mode and tool profile rather than inherit them by implication;
4. reject missing, malformed, qualified-but-unregistered, or unavailable capabilities;
5. keep `code` pinned to `domainspec-implement`, with no degradation to `other` on any failed code
   precondition.

The dispatch must also repair the parent implementation route's qualified pseudo-capability refs:
either normalize them to exact installed capability IDs with step-local modes, or register them as
real capability identities. A slash suffix must not become proof of installation.

Tests must demonstrate at least one installed unmapped capability resolving to `other`, several
installed unmapped capabilities resolving independently, a nonexistent capability failing closed,
a qualified pseudo-capability failing closed, an explicitly mapped capability retaining its
specialized type, and malformed `code` never degrading to `other`.

### RTE-02 — The dispatch cannot bootstrap its own governed code work — CRITICAL

**Quoted evidence:** the execution contract says: “Root performs orchestration only; every
analysis, mutation, test judgment, review, repair, and report is owned by a downstream seat” and
“Every governed seat prompt begins with ACI-WORKFLOW-BINDING-V1.” Step `s02` delegates mutation to
`domainspec-implement`; step `s03` explicitly refuses connected-topology implementation.

The lifecycle requires an entry-prepared concrete opening and compiled binding before launch. The
appender requires every `code` opening to contain the canonical sequential code topology. The
compiler rejects every non-empty `connections` array. Therefore no compliant code seat can compile
to a bound launch plan, including the seats intended to implement this dispatch. The high-level
dispatch-spec document is not itself a concrete lifecycle opening record and does not supply the
required route receipts or bindings.

**Required repair:** do not execute this dispatch until a governed bootstrap path exists. That path
must be one of:

- a separately authorized runtime-managed/native code launch that preserves the same code contract,
  exact write scope, binding, receipts, and independent verification; or
- a prior governed compiler capability that can materialize the canonical sequential code topology.

Do not route code mutation through `other`, remove the code topology, synthesize binding envelopes
by hand, or treat the high-level dispatch-spec validation receipt as launch authorization. After the
bootstrap exists, replace each executable phase with an entry-prepared concrete opening, immutable
route receipt, successful compile receipt, and lifecycle open/close receipts.

### RTE-03 — The proposed generic route has no durable capability binding — MAJOR

**Quoted evidence:** boundary `other-is-routing-not-authority` says: “Singular other supplies a
canonical type for the installed orchestrate capability only; capability, authority, tool,
appender, binding, and input gates still decide whether execution is permitted.”

The opening-row schema records `dispatch_type` but not the selected capability or route receipt.
Compilation receives `capability_ref` only as a CLI argument, while `open` validates only the row's
type and LIVE status. This is adequate for a one-to-one specialized type, but it is insufficient for
a generic type shared by multiple capabilities: the durable opening would not establish which
capability contract authorized the work.

**Required repair:** add a canonical, digest-bound capability-route reference to the opening and
open authorization path, or introduce an equivalent immutable route receipt that `compile`, `open`,
the host binding, and close evidence all verify. Tests must prove that swapping the capability after
confirmation, compiling one capability and opening another, or presenting a LIVE `other` row
without its verified route is rejected before authorization.

### RTE-04 — The review graph is not a valid independent review — MAJOR

**Quoted evidence:** step `s05` produces three attacker handles; step `s06` assigns only
`review_writer` and requires that “Unsupported findings are removed, not softened.”

The review contract requires independent skeptic verification and explicit coverage/zero-findings
ownership. A writer cannot silently serve as the missing verifier, and the current graph assigns no
coverage auditor. Step `s08` further combines test implementation, three attackers, and the writer
inside one validation step without the required attack → synthesis ↔ verification topology.

**Required repair:** add at least one independent `skeptic` verifier downstream of the writer and a
coverage-auditor seat or explicit parent coverage assignment. Preserve three one-lens attackers,
ensure no attacker verifies its own finding, assign Coverage authorship and the zero-findings flag,
and use the canonical review topology. Keep the review writer's only artifact `review.md`; do not
persist attacker transcripts or refuted findings.

### RTE-05 — The final report is written after the “final” review — MAJOR

**Quoted evidence:** `s05`–`s08` perform review and possible rereview; only afterward does `s09`
“Author the concise user-facing result.” The terminal condition nevertheless claims “independent
review returns PASS” before “the final report is authored.”

This contradicts the user's requirement to review the work after everything is finished. The final
report can introduce unsupported claims after the reviewed corpus is frozen.

**Required repair:** author the report before the terminal review, include it in the exact frozen
review corpus, and permit report repairs only through its original owner followed by deterministic
revalidation and rereview. Terminal PASS must apply to the final hashes of production code, tests,
skill-status report, test report, and user report.

### RTE-06 — Integrity-manifest ownership is missing and already overlaps user work — MAJOR

**Quoted evidence:** `runtime_type_implementer` owns the registry, resolver, appender, and minimal
capability metadata; `compiler_preflight_implementer` owns `dispatch_workflow.py`; the worktree rule
says every implementer “refuses overlap outside assigned ownership.”

The stage-E source manifest pins the registry, resolver, compiler, appender, and runtime test hashes;
`local_pilot.py` pins the manifest hash. The dispatch neither assigns those integrity artifacts nor
tests their regeneration. Both the source manifest and `local_pilot.py` are already modified in the
current worktree, so adding them casually would overwrite or absorb user-owned work.

**Required repair:** add an explicit final integrity owner and validation step after all production
and test changes. Before mutation, snapshot and compare the existing dirty diffs. If the required
manifest/pin update overlaps semantically with those user changes, block for coordination; otherwise
apply a minimal merge that preserves them and record exact before/after hashes. Include the manifest
integrity suite in the affected regression set. Do not broaden any implementation owner's scope
implicitly.

### RTE-07 — Changing `others` to `other` needs an explicit schema migration decision — MAJOR

**Quoted evidence:** the intended behavior says: “The historical plural value others remains
readable as historical ledger data but is not emitted or accepted for a new opening.” Gate `g04`
requires the same compatibility split.

The dispatch never states whether `ledger_schema_version` changes. Reusing `0.6.3` would make rows
with the same declared schema version obey different dispatch-type enums based only on when they
were appended. Grandfathered structural reading preserves bytes, but it does not remove the schema
ambiguity.

**Required repair:** make the compatibility policy explicit and default to a schema-version bump for
new singular `other` openings. Preserve old plural rows byte-for-byte under their old version; reject
plural for new rows; test mixed-version ledger reading, new opening validation, close of a historical
plural dispatch, UI/ledger aggregation, and bridge/runtime resolution. If the owner deliberately
chooses another in-place enum amendment, record that decision and its known audit cost rather than
letting the implementation infer it.

## Exact route repair order

1. Resolve the bootstrap authority in `RTE-02`; without it, no mutation seat may launch.
2. Redesign generic capability resolution and durable binding per `RTE-01` and `RTE-03`.
3. Decide and encode the singular/plural migration boundary per `RTE-07`.
4. Add the integrity owner and dirty-overlap preflight per `RTE-06`.
5. Replace the review and terminal-report order per `RTE-04` and `RTE-05`.
6. Re-run the dispatch-spec validator, compile/open negative and positive fixtures, all directly
   affected runtime/ledger/UI-integrity suites, and the repaired independent review.

The current dispatch must not be registered or launched. `BLOCK` may be lifted only after the two
CRITICAL findings are repaired and the amended route receives a fresh independent review.

## Repair verification — 2026-08-13

**Verdict: BLOCK**

The repaired document passes deterministic dispatch-spec validation and materially repairs five of
the seven original findings. It still cannot execute from its current initial state, and its final
review/repair graph does not yet preserve the promised canonical topology and final-hash ordering.

Validation rerun:

- `python .agents/skills/dispatch-spec/scripts/validate-dispatch.py internal-tools/need-driven-system-writing/runtime-type-expansion-dispatch.json` → `VALIDATION=pass`.

### Original finding disposition

| finding | disposition | evidence |
|---|---|---|
| `RTE-01` generic coverage | **PASS at contract level** | The objective now covers “every exact installed capability”; specialized mappings win; exact installed unmapped capabilities resolve to `other`; missing, malformed, unavailable, and qualified pseudo-capabilities fail closed. The parent-route migration explicitly replaces suffix identities with exact installed IDs plus local modes. |
| `RTE-02` governed bootstrap | **BLOCK** | A direct compiler exception is declared, but pre-generic steps still select unroutable capabilities and the direct seat remains represented as a seat of this dispatch. |
| `RTE-03` durable capability binding | **PASS at contract level** | The route now requires identity, path, digest, authority, and tool profile in an immutable binding verified by append, compile, open, host binding, and close, with explicit swap/missing-binding tests. |
| `RTE-04` independent review | **AMEND required** | Independent attacker, skeptic, coverage, and approver roles now exist, but the repaired route does not materialize the canonical cross-group topology, and rereview collapses all roles into one validation step. |
| `RTE-05` final report ordering | **PASS** | `s09` authors the report before `s10`/`s11`; the final hash corpus explicitly includes the report. |
| `RTE-06` integrity ownership | **PASS for dirty-work protection; AMEND for repair ordering** | Baseline and integrity owners now preserve dirty hunks and block on overlap, but the repair step runs integrity in parallel with production/test/report repairs and has overlapping test ownership. |
| `RTE-07` singular/plural migration | **PASS at contract level** | The route now requires a schema-version bump, singular new rows, plural historical bytes, API alias normalization, mixed-version read/close/aggregation tests, and no silent rewrite. |

### RV-01 — The repaired route still cannot reach its own bootstrap — CRITICAL

**Quoted evidence:** `s00-baseline` selects `capability_ref: "orchestrate"`; the direct exception's
scope says: “One direct subagent seat may edit only implementations/server/runtime/dispatch_workflow.py
and its new focused bootstrap tests”; `s03-build-governed-openings` selects
`capability_ref: "subagents-dispatch-lifecycle"`; generic capability resolution is not implemented
until `s05-runtime-binding`.

In the current runtime, both `orchestrate` and `subagents-dispatch-lifecycle` have no routable type.
The one-seat exception applies only to `s01`, so the route fails at `s00` before that exception and
again at `s03` before `other` exists. This reproduces the missing-type failure the route is intended
to remove.

There is also a governance contradiction. The dispatch includes `s01` as one of its steps, while
`bootstrap_authority.truthfulness` says the seat is “explicitly unbound.” A seat does not cease to
be under this dispatch merely because the artifact labels it an exception. The repository binding
rule requires a seat prompt under a governed dispatch to begin with the binding marker; broad user
authorization to use subagents does not itself create a runtime-managed binding authority or amend
that rule.

**Required repair:** supply an actually executable bootstrap route before `s00`. The repaired route
must not depend on a capability whose type it has not yet installed. Either:

1. use an already available, explicit runtime-managed/native bootstrap authority whose governing
   contract authorizes both the baseline and the minimum compiler/type-binding repair with exact
   scopes and receipts; or
2. obtain and encode a repository-governed bootstrap mechanism outside this dispatch, then begin
   this dispatch only after `other` and sequential compilation are already installed and reviewed.

Do not solve the cycle by relabeling an in-dispatch seat “unbound,” mapping code to `other`, or
letting root perform baseline/opening authoring. After repair, demonstrate from the unmodified
current registry that every pre-`s05` seat can be launched under its declared authority.

### RV-02 — Review topology remains descriptive rather than executable — MAJOR

**Quoted evidence:** `s11-review-convergence` places `review_writer`, `review_skeptic`,
`coverage_auditor`, and `final_approver` in one `dialectic` step and says the writer and skeptic
“exchange at most three times”; `s13-rereview` places all attackers, writer, skeptic, auditor, and
approver in one `validation` step and merely says the “same ... topology runs.”

The repair adds the missing roles, but it does not specify the canonical attacker → writer ↔ skeptic
connections or the auditor's downstream placement as executable groups/handoffs. `s13` is weaker:
it combines attack, synthesis, verification, coverage, and approval in one step without explicit
independence-preserving connections. `s03` promises concrete openings only for “mutation phases,”
so it does not clearly own materialization of review openings.

**Required repair:** require the opening builder to produce concrete governed openings for every
post-bootstrap seat, including review. Materialize separate attacker, writer, skeptic, coverage,
and dedicated-approver groups with the review skill's canonical connections and loop caps. The
rereview must instantiate the same graph, not reference it narratively from a combined step. Require
the approver to receive the complete final hash bundle and do no other work.

### RV-03 — Repair ownership and final integrity ordering are not disjoint — MAJOR

**Quoted evidence:** `bootstrap_compiler_implementer` owns `dispatch_workflow.py and focused
bootstrap compiler tests`; `test_implementer` owns “directly affected test files”; `s12-owner-repair`
runs `runtime_binding_implementer`, `parent_route_migrator`, `test_implementer`, `integrity_owner`,
and `user_report_writer` with `parallel: true` and `join_policy: all`.

The test scopes overlap unless the later test owner explicitly excludes bootstrap-owned tests or
ownership is transferred after bootstrap. More importantly, integrity cannot run in parallel with
production, test, route, and report repairs: it may hash and pin files before sibling owners finish,
so `repaired-final-hash-manifest` is not guaranteed to describe the corpus rereviewed by `s13`.

**Required repair:** make ownership disjoint by naming the bootstrap test paths and excluding them
from later mutation, or explicitly transfer ownership at a recorded handoff. Split repair into:

1. owner-bounded production/route/report repairs;
2. deterministic test update and full test run after those repairs;
3. integrity regeneration after all changed bytes are final;
4. one frozen final hash manifest;
5. full rereview over exactly that manifest.

No integrity owner may run in parallel with a producer of an artifact it hashes.

### Terminal condition

The conceptual generic-type, durable-binding, migration, dirty-work, and report-order repairs are
accepted as a substantially improved plan. Execution remains blocked until `RV-01` is resolved and
the review/repair graph is amended per `RV-02` and `RV-03`, followed by another deterministic
validation and independent re-review.

## Final repair verification — 2026-08-13

**Reviewed dispatch SHA-256:**
`AABAD2F5F07D56348373E715612BD4CC2866785D7C8E4DCD9CDE6D089C5E005A`

**Verdict: BLOCK**

Deterministic validation passes:

- `python .agents/skills/dispatch-spec/scripts/validate-dispatch.py internal-tools/need-driven-system-writing/runtime-type-expansion-dispatch.json` → `VALIDATION=pass`.

### Repair status

| obligation | result | evidence |
|---|---|---|
| `RV-01`: honest executable Stage A | **PASS** | `stage_a_bootstrap_contract.relationship_to_stage_b` now makes Stage A an external prerequisite, explicitly “not a step, seat, child dispatch, or governed execution” of Stage B. It has a frozen contract, disjoint direct-agent roles, exact production/test/integrity ownership, no ACI claim, deterministic tests, independent review, repair order, final hashes, and a blocking terminal receipt. Stage B remains `awaiting-external-bootstrap` until that prerequisite exists. |
| `RV-02`: actual review graph | **PASS** | Both Stage-A and Stage-B graphs explicitly encode independent full-corpus attackers → writer ↔ skeptic (zig-zag/feedback, cap 3) → coverage auditor → dedicated final approver. The repair graph repeats attack, synthesis, skepticism, coverage, and approval rather than collapsing roles into one step. |
| `RV-03`: disjoint ownership and integrity order | **PASS except final report regression** | Stage-A tests have two exclusive named paths; Stage B declares them read-only. Stage-B repair is sequential: original owner repair → Stage-B-only tests → integrity after all producers join → frozen manifest → full reattack/review. Integrity never runs in parallel with an artifact producer. The report exception is recorded below. |
| Generic `other`, strict `code`, durable binding, migration, abuse failures | **PASS at route-contract level** | All previously accepted specialized-first, exact-installed-only, identity/path/digest/authority/tool binding, no code fallback, schema bump, historical plural compatibility, route-swap rejection, connected-input, and dirty-hunk preservation obligations remain present. |
| No success before governed fixture proof | **PASS** | `b02` requires actual governed compile, open, bound-seat execution, downstream input consumption, and close receipts for both `other` and `code`; `g08` refuses terminal PASS until Stage B compiled, opened, ran, closed, passed tests/integrity, and received final-hash approval. |

### FV-01 — Stage-B entry proof is not independently owned and does not separate capability authorities — CRITICAL

**Quoted evidence:** `stage_b_entry_gate.required_preflight` requires: “Generate the Stage-B
concrete opening ... Independently review the opening and route receipt ... compile to a non-empty
generated launch plan.” The only opening role is `b_opening_builder`, whose purpose is to “Generate
and independently freeze the Stage-B opening and route receipt.” Gate `g02-stage-b-preflight` is also
owned by `b_opening_builder`. No independent opening-review role or opening-review receipt exists.

The opening contract is also singular and authority-ambiguous. `b01` selects
`subagents-dispatch-lifecycle`, while later seats select `domainspec-implement`, `review`, and
`orchestrate`. A concrete legacy opening resolves one capability/type route for all of its seats;
per-step `capability_ref` fields in this high-level document are not preserved by that opening's
agent schema. Consequently, one generic `other` opening would authorize later code mutation without
the `code` contract, while one `code` opening could not truthfully authorize the non-code lifecycle,
review, and reporting roles. `b02` itself writes a test file, so this is an actual authority boundary,
not merely a label mismatch.

**Required repair:** make Stage B a governed parent plus separately generated concrete child
openings, one for each effective capability/type boundary. At minimum:

1. assign a distinct read-only opening reviewer who did not generate the parent or child openings;
2. persist an opening-review receipt over exact opening and route hashes before compilation/open;
3. use strict `code` openings with full `code_contract` for every test, route, integrity, or repair
   mutation;
4. use specialized `review` openings for attack/synthesis/verification/coverage/approval;
5. use `other` only for an exact installed unmapped capability and never as the authority envelope
   for a `domainspec-implement` mutation;
6. bind parent/child inputs and receipts through the installed connected-input contract;
7. require each child to compile, open, execute, and close under its own resolved route before its
   output becomes an input to the next step.

The Stage-B entry gate must verify the complete parent/child launch set, not one ambiguous singular
opening, and the independent reviewer—not the builder—must own the preflight verdict.

### FV-02 — The final report again falls outside final hashes and review — MAJOR

**Quoted evidence:** `b04` freezes `stage-b-final-hash-manifest`; `b05`–`b07` review and approve it;
only then does `b14-final-report` “Write the final user report only after Stage-B review PASS.” Its
output is not followed by integrity, attack, skeptic verification, coverage, or approval.

This regresses accepted finding `RTE-05`. Restricting the report to approved receipts reduces risk
but does not verify that it actually represents those receipts accurately. It is a substantive
artifact written by a distinct agent after the reviewed corpus is frozen.

**Required repair:** write the user report before the terminal integrity/hash freeze, include it in
the complete review corpus, and route any verified report defect to `b_report_writer`, followed by
tests as applicable, final integrity, and full rereview. The final approver's receipt must name the
report hash. Root may relay that approved report afterward without authoring a new substantive
summary.

### Final condition

The dispatch is now materially coherent and the previous bootstrap, review-topology, ownership,
migration, binding, and fixture-proof defects are repaired at the contract level. It remains blocked
only on the Stage-B parent/child capability separation with independent opening review (`FV-01`) and
putting the final report inside the terminal hash/review boundary (`FV-02`). Revalidate and re-review
the exact amended hash before any Stage-B registration or launch.

## Terminal repair verification — 2026-08-13

**Reviewed dispatch SHA-256:**
`2D9C9C3B3ACD66D0A0C11DF69F2BC9265B45A3384BB7C317D7F76F78CB342051`

**Verdict: PASS**

Deterministic validation:

- `python .agents/skills/dispatch-spec/scripts/validate-dispatch.py internal-tools/need-driven-system-writing/runtime-type-expansion-dispatch.json` → `VALIDATION=pass`.

### FV-01 verification — PASS

The final contract no longer uses one mixed-authority opening:

- `stage_b_parent_child_contract.parent_authority` limits the parent to non-mutating dependency
  release, receipt joining, terminal success computation, and close.
- Separate parent and child opening authors own disjoint paths.
- `b_opening_reviewer` is read-only, authored no opening, repairs nothing, owns the exact opening
  review receipt, and controls `g02-stage-b-preflight`.
- The entry gate requires opening-review PASS before compilation or open.
- Every parent/child opening is appender-validated and compiled to a non-empty plan under its own
  resolved route.
- `other` is confined to an exact installed non-code capability; all mutation/test/route/integrity
  and repair work uses strict `code` children with complete `code_contract` and readiness; all review
  functions use specialized `review` children.
- Each child has its own immutable route, independently reviewed opening hash, compile/open/binding/
  execution/close receipts, and digest-bound dependency inputs. Parent and siblings cannot lend
  authority.

The opening-authoring and opening-review phases are explicitly preflight work completed before the
governed Stage-B parent begins; the execution proof after that boundary is governed. The contract
does not claim that preflight authoring itself is a bound Stage-B child.

### FV-02 verification — PASS

The report is now inside the terminal evidence boundary:

- `b03a-user-report` writes it before integrity and terminal review.
- `b04-integrity` freezes its hash with all other target bytes.
- attackers, skeptic, coverage auditor, and final approver consume the complete manifest including
  the report.
- `b07` cannot PASS without naming the exact report hash.
- a verified report defect returns only to `b_report_writer`, followed sequentially by tests,
  integrity regeneration, complete reattack, skepticism, coverage, and reapproval.
- after PASS, root may relay only the approved report verbatim; no substantive target mutation is
  permitted.

### Regression check — PASS

The final hash preserves all previously accepted contracts:

- Stage A remains an external, explicitly direct and non-ACI prerequisite with exact ownership,
  deterministic tests, integrity ordering, independent review, final hashes, and honest receipts.
- specialized mappings win; generic `other` applies only to exact installed unmapped capabilities
  and preserves identity/path/digest/authority/tool binding.
- `code` remains specialized and readiness-gated; malformed or failed code cannot fall back.
- the singular schema migration preserves historical plural rows without rewriting them.
- dirty user hunks remain protected by baseline comparison and block-on-overlap behavior.
- review and rereview encode attackers → writer ↔ skeptic → coverage → dedicated approver.
- repair → tests → integrity → frozen manifest → full rereview is sequential and ownership remains
  disjoint.
- `g08-terminal-pass` forbids success until the governed parent and every separately authorized
  `other`, `code`, `review`, and report child has compiled, opened, executed, consumed governed
  inputs, closed, joined, passed tests/integrity, and received complete final-hash approval.

This PASS approves the dispatch contract at the reviewed hash. It is not evidence that Stage A or
Stage B has executed; their receipts and gates remain mandatory.
