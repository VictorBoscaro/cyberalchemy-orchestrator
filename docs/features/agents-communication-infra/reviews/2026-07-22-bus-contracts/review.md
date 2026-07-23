# Review — Bus Contracts Discovery

## Coverage

| attacker | lens | findings raised | zero-findings defence |
|---|---|---:|---|
| Dijkstra, Edsger W. | fidelity / governance | 7 | n/a |
| Hoare, C. A. R. | mechanics / correctness | 11 | n/a |
| Parnas, David | ownership / reference integrity | 10 | n/a |
| Liskov, Barbara | operability / abuse | 9 | n/a |

- Collapse note: `robot_talks=false`; the four attacks remained independent, so no
  post-discussion convergence could erase their initial positions.
- Lens coverage: the complete target was attacked from all four declared lenses.
- Verification: Lamport applied literal refutation; Brooks applied adversarial survivability. Both
  reread the complete target and checked all 37 raised candidates. Correlated candidates were
  deduplicated. M6, P3 and P8 were refuted by both; M11 was refuted by one verifier and therefore
  dropped. The severity of the blockers finding was demoted to MINOR under claim ≤ proof.

## `docs/features/agents-communication-infra/discovery/bus-contracts/README.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---:|---|---|---|---|
| 1 | `bus-contracts/README.md` | “`#### Knowledge/context bus`” and “`propose context -> persist proposal -> adjudicate -> promote/reject`”, despite “não devem ampliar o primeiro contrato” | MAJOR | Remove the knowledge procedure, operation and probe; retain only an explicit extension seam for a future discovery. |
| 2 | `bus-contracts/README.md` | The document separately declares “`#### Work/output bus`” and “`#### Review bus`” and leaves their relation open in question 12. | MAJOR | Define one Work Bus with distinct `submit_work` and `submit_review` contracts/capabilities. |
| 3 | `bus-contracts/README.md` | “`#### Control bus`” owns assignment/cancel/reopen and is also exposed as `request_control_action(...)`. | MAJOR | Model control as the canonical command/control plane, not an agent-authored bus. |
| 4 | `bus-contracts/README.md` | “Skills [...] não podem substituir [...] a autoridade da SPEC”, but the example mixes SPEC and skills under `authority_refs`. | MAJOR | Separate normative references from review-lens skill references and state precedence. |
| 5 | `bus-contracts/README.md` | `WorkSubmission` is persisted “após aceitação”, while the receipt proves only that a candidate “foi persistida”; question 14 still asks which messages use official verification. | MAJOR | Specify candidate, receipt verification and official acceptance states, actors and release gate. |
| 6 | `bus-contracts/README.md` | `PublicationReceipt` is assigned to “journal/projeção canônica” and later listed among artifacts subject to retention. | MAJOR | Keep canonical receipt bytes/identity as durable journal evidence; artifact copies are derived only. |
| 7 | `bus-contracts/README.md` | “O `dispatch_kind` [...] permanece imutável” with `research \| implementation`, while review is called only a phase/role. | MAJOR | Rename the concept to `work_kind` and distinguish it explicitly from governed `dispatch_type`. |
| 8 | `bus-contracts/README.md` | Consumers derive from `GroupSpec`, workflow/recipe, roles, dependencies, phase, connections and ACL, while `ReviewProfile` is also said to select consumers without a routing schema. | MAJOR | Compile one immutable `RoutingPlan`; route rework by `subject_kind + remediation_scope` to a responsible work item/role. |
| 9 | `bus-contracts/README.md` | H1 says the agent supplies only semantic content but requires an already-finalized `report_ref`, with no creation/finalization operation. | MAJOR | Let `submit_work` accept inline content or an authorized file and let the runtime finalize/inject the artifact reference. |
| 10 | `bus-contracts/README.md` | Implementation submission contains only `summary` and `blockers`; automatic capture is qualified by “quando a superfície permitir”. | MAJOR | Require an observed change set, a validated declared fallback, or explicit no-change evidence. |
| 11 | `bus-contracts/README.md` | Files and diffs are captured, but reliable attribution in an already-modified worktree remains an open question. | MAJOR | Finalize an immutable `ChangeSetArtifact` from an assignment baseline, with path ownership and overlap/concurrency detection. |
| 12 | `bus-contracts/README.md` | `blockers` occurs in work payloads while blocking is also a control action and ordinary agent text cannot change official state. | MINOR | Keep blocker details out of completed work submission state; use a typed control command and optionally reference it. |
| 13 | `bus-contracts/README.md` | The orchestrator may reopen work, but multiple valid outputs versus retry remains an open question. | MAJOR | Define logical submission identity, generation, active-assignment lease/CAS, `supersedes` and late-result handling. |
| 14 | `bus-contracts/README.md` | Operational outputs follow retention/tombstone while handoffs and later work consume bodies by reference. | MAJOR | Pin artifacts while reachable from active or retained authoritative records; define deterministic tombstone behavior. |
| 15 | `bus-contracts/README.md` | Handoff dedupe uses only “source aggregate + connection”. | MAJOR | Include source commit/result digest and connection version in the logical delivery key. |
| 16 | `bus-contracts/README.md` | `EffectiveInputArtifact` is both a pre-invocation composition and “tudo que o agente pôde observar como input”. | MAJOR | Restrict it to the initial invocation snapshot and introduce a mediated execution-observation manifest/log. |
| 17 | `bus-contracts/README.md` | Artifact acceptance requires finalization but does not require producer assignment, classification ACL or authorized reuse. | MAJOR | Validate provenance, producer attempt/assignment, access capability, classification and reuse policy for every reference. |
| 18 | `bus-contracts/README.md` | The wrong-channel principle forbids work→review/knowledge/control, but the probe tests only knowledge and control. | MAJOR | Test the full role × capability × schema matrix, especially worker→`submit_review` and reviewer→`submit_work`. |

**Verdict:** FIX

## Refuted findings

- Stale-review protection was not absent: exact submission/version binding and invalidation by new
  hash are already stated. Generation/CAS details remain covered by change request 13.
- The text did not prove concurrent ownership of artifact metadata between journal and artifact
  service; that stronger claim was dropped.
- `kernel/materializer` did not by itself prove two competing authors of the same handoff fact; that
  claim was dropped.
- The document already requires distinct capabilities for different authority/effect classes, so
  the broader claim that critique and review necessarily share one contract was dropped.

## Change requests

1. MAJOR — Reduce the active scope to one Work Bus; defer knowledge and keep only its extension seam.
2. MAJOR — Treat review as an operation of the Work Bus and control as command plane, not additional buses.
3. MAJOR — Separate normative references from skill-based review lenses.
4. MAJOR — Specify candidate persistence, receipt verification, official acceptance and release semantics.
5. MAJOR — Make canonical receipt ownership and retention unambiguous.
6. MAJOR — Rename `dispatch_kind` to avoid collision with governed `dispatch_type`.
7. MAJOR — Compile one routing authority and define deterministic remediation routing.
8. MAJOR — Make artifact creation a mediated consequence of `submit_work`, not a manual agent prerequisite.
9. MAJOR — Require immutable, attributable implementation evidence and safe worktree baselines.
10. MAJOR — Define generation, retry, replacement, rework and late-result semantics.
11. MAJOR — Pin referenced artifacts and strengthen handoff delivery identity.
12. MAJOR — Separate initial input snapshot from observations acquired during execution.
13. MAJOR — Bind every artifact reference to provenance, assignment and ACL.
14. MAJOR — Expand negative capability probes to a complete producer/operation/schema matrix.
15. MINOR — Move state-changing blocker semantics to a typed control command.

## Dispatch closure

- `exit_reason`: `resolved`
- `agents_spawned`: 6 (`explorer`: 4, `skeptic`: 2, helpers: 0); loops used: 1
