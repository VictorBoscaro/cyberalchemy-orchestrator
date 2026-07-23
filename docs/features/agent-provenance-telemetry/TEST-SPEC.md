---
tags: [agent-provenance-telemetry, spec, test]
node_type: spec
is_session: false
layer: application
nature: procedural, technical
status: planned
version: 0.1.0
last_updated: 2026-07-23
feature: agent-provenance-telemetry
testSpecGate: pending
executionStatus: not-run
---

# Test Spec: Agent Provenance Telemetry

This planned test contract preserves the stable anchors for all 26 contracts in
[rules.md](specs/rules.md), all 53 reciprocal Operation clause IDs and the remaining approved
DomainSpec aspects. It defines fixture inputs, expected/negative/property/replay/fault obligations
but does not claim executable test code, execution, passing evidence or review approval.

## Gate Status

| Field | Value |
|---|---|
| Specification status | `planned` |
| Review gate | `pending` |
| Executable tests | not claimed |
| Test execution | `not-run` |
| Passing evidence | none |
| Reserved coverage | 26 rule contracts, 53 Operation clauses, 6 Events, 3 Workflows, 3 Queries, 3 Mappings, Interfaces, state/replay/persistence, observability and 12 stories |

## Test Matrix

| ID | Planned test obligation | Validates | Status |
|---|---|---|---|
| [APT-TEST-R1](#apt-r1--single-join-authority) | Reserve single-edge authority coverage. | [APT-R1](specs/rules.md#apt-r1--single-join-authority) | planned |
| [APT-TEST-R2](#apt-r2--idempotent-append) | Reserve idempotency/append-before-ack coverage. | [APT-R2](specs/rules.md#apt-r2--idempotent-append) | planned |
| [APT-TEST-R3](#apt-r3--artifact-only-raw-return) | Reserve capture status/cardinality coverage. | [APT-R3](specs/rules.md#apt-r3--artifact-only-raw-return) | planned |
| [APT-TEST-R4](#apt-r4--extraction-provenance) | Reserve byte-exact extraction coverage. | [APT-R4](specs/rules.md#apt-r4--extraction-provenance) | planned |
| [APT-TEST-R5](#apt-r5--capture-supersession) | Reserve capture-CAS coverage. | [APT-R5](specs/rules.md#apt-r5--capture-supersession) | planned |
| [APT-TEST-R6](#apt-r6--replay-determinism) | Reserve deterministic as-of replay coverage. | [APT-R6](specs/rules.md#apt-r6--replay-determinism) | planned |
| [APT-TEST-R7](#apt-r7--protocol-profile-binding) | Reserve exact-profile binding coverage. | [APT-R7](specs/rules.md#apt-r7--protocol-profile-binding) | planned |
| [APT-TEST-R8](#apt-r8--telemetry-non-authority) | Reserve telemetry non-authority coverage. | [APT-R8](specs/rules.md#apt-r8--telemetry-non-authority) | planned |
| [APT-TEST-C01](#session-context-binding) | Reserve context-binding coverage. | [APT-C01](specs/rules.md#session-context-binding) | planned |
| [APT-TEST-C02](#rollover-authorization) | Reserve rollover-authorization coverage. | [APT-C02](specs/rules.md#rollover-authorization) | planned |
| [APT-TEST-C03](#link-session-dispatch-authorization) | Reserve link-authorization coverage. | [APT-C03](specs/rules.md#link-session-dispatch-authorization) | planned |
| [APT-TEST-C04](#dispatch-snapshot-identity) | Reserve dispatch-snapshot coverage. | [APT-C04](specs/rules.md#dispatch-snapshot-identity) | planned |
| [APT-TEST-C05](#capture-digest) | Reserve closed capture-digest coverage. | [APT-C05](specs/rules.md#capture-digest) | planned |
| [APT-TEST-C06](#research-synthesis-pins) | Reserve synthesis-pin coverage. | [APT-C06](specs/rules.md#research-synthesis-pins) | planned |
| [APT-TEST-C07](#raw-selector-validity) | Reserve raw-selector coverage. | [APT-C07](specs/rules.md#raw-selector-validity) | planned |
| [APT-TEST-C08](#evidence-reference-validity) | Reserve evidence-reference coverage. | [APT-C08](specs/rules.md#evidence-reference-validity) | planned |
| [APT-TEST-C09](#question-derivation-validity) | Reserve question-derivation coverage. | [APT-C09](specs/rules.md#question-derivation-validity) | planned |
| [APT-TEST-C10](#research-fact-appended-closed-union) | Reserve fact-union coverage. | [APT-C10](specs/rules.md#research-fact-appended-closed-union) | planned |
| [APT-TEST-C11](#research-fact-locality) | Reserve fact-locality coverage. | [APT-C11](specs/rules.md#research-fact-locality) | planned |
| [APT-TEST-C12](#research-fact-typing) | Reserve fact-typing coverage. | [APT-C12](specs/rules.md#research-fact-typing) | planned |
| [APT-TEST-C13](#reference-check-typing) | Reserve reference-check coverage. | [APT-C13](specs/rules.md#reference-check-typing) | planned |
| [APT-TEST-C14](#formalization-locality) | Reserve formalization coverage. | [APT-C14](specs/rules.md#formalization-locality) | planned |
| [APT-TEST-C15](#fact-append-identity) | Reserve global fact-ID coverage. | [APT-C15](specs/rules.md#fact-append-identity) | planned |
| [APT-TEST-C16](#disposition-and-assessment-chains) | Reserve aggregate-chain coverage. | [APT-C16](specs/rules.md#disposition-and-assessment-chains) | planned |
| [APT-TEST-C17](#probe-lineage-append) | Reserve probe partition/receipt coverage. | [APT-C17](specs/rules.md#probe-lineage-append) | planned |
| [APT-TEST-C18](#relational-collection-canonicalization) | Reserve collection-canonicalization coverage. | [APT-C18](specs/rules.md#relational-collection-canonicalization) | planned |

## Reserved Coverage Anchors

Every section below preserves its original stable anchor. Exact shared fixtures, case shapes,
runner partitions and expected results are defined in the matrices following these anchors.

<a id="apt-r1--single-join-authority"></a>

### APT-TEST-R1 — Single Join Authority

**Validates:** [APT-R1](specs/rules.md#apt-r1--single-join-authority).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="apt-r2--idempotent-append"></a>

### APT-TEST-R2 — Idempotent Append

**Validates:** [APT-R2](specs/rules.md#apt-r2--idempotent-append).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="apt-r3--artifact-only-raw-return"></a>

### APT-TEST-R3 — Artifact-Only Raw Return

**Validates:** [APT-R3](specs/rules.md#apt-r3--artifact-only-raw-return).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="apt-r4--extraction-provenance"></a>

### APT-TEST-R4 — Extraction Provenance

**Validates:** [APT-R4](specs/rules.md#apt-r4--extraction-provenance).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="apt-r5--capture-supersession"></a>

### APT-TEST-R5 — Capture Supersession

**Validates:** [APT-R5](specs/rules.md#apt-r5--capture-supersession).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="apt-r6--replay-determinism"></a>

### APT-TEST-R6 — Replay Determinism

**Validates:** [APT-R6](specs/rules.md#apt-r6--replay-determinism).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="apt-r7--protocol-profile-binding"></a>

### APT-TEST-R7 — Protocol Profile Binding

**Validates:** [APT-R7](specs/rules.md#apt-r7--protocol-profile-binding).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="apt-r8--telemetry-non-authority"></a>

### APT-TEST-R8 — Telemetry Non-Authority

**Validates:** [APT-R8](specs/rules.md#apt-r8--telemetry-non-authority).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="session-context-binding"></a>

### APT-TEST-C01 — Session Context Binding

**Validates:** [APT-C01](specs/rules.md#session-context-binding).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="rollover-authorization"></a>

### APT-TEST-C02 — Rollover Authorization

**Validates:** [APT-C02](specs/rules.md#rollover-authorization).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="link-session-dispatch-authorization"></a>

### APT-TEST-C03 — Link Session Dispatch Authorization

**Validates:** [APT-C03](specs/rules.md#link-session-dispatch-authorization).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="dispatch-snapshot-identity"></a>

### APT-TEST-C04 — Dispatch Snapshot Identity

**Validates:** [APT-C04](specs/rules.md#dispatch-snapshot-identity).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="capture-digest"></a>

### APT-TEST-C05 — Capture Digest

**Validates:** [APT-C05](specs/rules.md#capture-digest).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="research-synthesis-pins"></a>

### APT-TEST-C06 — Research Synthesis Pins

**Validates:** [APT-C06](specs/rules.md#research-synthesis-pins).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="raw-selector-validity"></a>

### APT-TEST-C07 — Raw Selector Validity

**Validates:** [APT-C07](specs/rules.md#raw-selector-validity).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="evidence-reference-validity"></a>

### APT-TEST-C08 — Evidence Reference Validity

**Validates:** [APT-C08](specs/rules.md#evidence-reference-validity).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="question-derivation-validity"></a>

### APT-TEST-C09 — Question Derivation Validity

**Validates:** [APT-C09](specs/rules.md#question-derivation-validity).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="research-fact-appended-closed-union"></a>

### APT-TEST-C10 — Research Fact Appended Closed Union

**Validates:** [APT-C10](specs/rules.md#research-fact-appended-closed-union).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="research-fact-locality"></a>

### APT-TEST-C11 — Research Fact Locality

**Validates:** [APT-C11](specs/rules.md#research-fact-locality).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="research-fact-typing"></a>

### APT-TEST-C12 — Research Fact Typing

**Validates:** [APT-C12](specs/rules.md#research-fact-typing).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="reference-check-typing"></a>

### APT-TEST-C13 — Reference Check Typing

**Validates:** [APT-C13](specs/rules.md#reference-check-typing).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="formalization-locality"></a>

### APT-TEST-C14 — Formalization Locality

**Validates:** [APT-C14](specs/rules.md#formalization-locality).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="fact-append-identity"></a>

### APT-TEST-C15 — Fact Append Identity

**Validates:** [APT-C15](specs/rules.md#fact-append-identity).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="disposition-and-assessment-chains"></a>

### APT-TEST-C16 — Disposition and Assessment Chains

**Validates:** [APT-C16](specs/rules.md#disposition-and-assessment-chains).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="probe-lineage-append"></a>

### APT-TEST-C17 — Probe Lineage Append

**Validates:** [APT-C17](specs/rules.md#probe-lineage-append).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

<a id="relational-collection-canonicalization"></a>

### APT-TEST-C18 — Relational Collection Canonicalization

**Validates:** [APT-C18](specs/rules.md#relational-collection-canonicalization).  
**Status:** planned/not-run; exact cases use the shared fixtures and Contract Case Matrix below.

## Suite Partition

| Level | Type | Boundary | Execution claim |
|---|---|---|---|
| L1 | unit/schema/property | Closed domain values, canonical preimages, reducers and mappings | planned/not-run |
| L2 | contract | ProvenanceAppendPort, ProvenanceQueryPort and owner-evidence shapes/errors | planned/not-run |
| L3 | integration | APT application binder → local ACICommandAdapter → fake/conformance ACI boundary | planned/not-run |
| L4 | replay/fault/race | Atomic groups, journal-prefix reader, checkpoints, crash failpoints and concurrent CAS/semantic keys | planned/not-run |
| L5 | security/observability | Redaction, prohibited content, bounded labels, non-authority and retention configuration | planned/not-run |

No L-level is an implementation directory or a report of execution. A future runner manifest must
bind every test ID below to exactly one executable case or parameterized case family without
renumbering these IDs.

## Fixture Corpus

| Fixture | Setup and owned inputs | Required variants |
|---|---|---|
| `FX-INVOCATION` | TrustedInvocationContext with owner-bound principal, origin tuple, correlation and authentication evidence | valid; missing auth; wrong principal; unknown field |
| `FX-SESSION` | Empty/current origin binding, stable ensure key, owner-issued Session/event IDs/times and authorization evidence | new; semantic reuse; exact retry; changed digest; stale predecessor; authorized rollover |
| `FX-DISPATCH` | Same Dispatch represented by closed DispatchAuthoritySnapshotRef variants | `aci_managed` with all authority fields including accepted offset; `legacy_ledger` with ledger-row identity/digest and optional non-authoritative row index; mixed/omitted/tampered |
| `FX-ARTIFACT` | Already-finalized textual UTF-8 artifact plus exact digest/media/charset/classification/policy evidence | valid; unfinalized; wrong digest/media/charset; raw bytes forbidden |
| `FX-CAPTURE` | Current Session/link/snapshot and complete `apt.research-capture@1` slot vector | captured; partial with/without selected evidence; missing; correction; ordered synthesis; every invalid status permutation |
| `FX-FACTS` | One current non-missing capture and all eight Entity payload variants plus disposition/assessment variants | valid selector-bearing seven Entities; non-extraction ReferenceCheck; locality/type/head/actor/digest mutations |
| `FX-PROBE` | Committed bundle/recommendation, exact profile receipts, delivery/use heads and unordered item collections | zero-new; mixed; all-new; duplicate key; missing dependency; exact/divergent global fact collision |
| `FX-JOURNAL` | ACI groups with positive offsets, receipt range/count/order/digest, schemas and aggregate versions | single event; rollover pair; probe batch; incomplete/overlap/fork/gap/tamper |
| `FX-CHECKPOINT` | Artifact-backed decoded state with exact prefix/group/recipe/spec/reducer/profile bindings | eligible historical; future; inside group; corrupt; incompatible; canonical-null checkpoint |
| `FX-QUERY` | Authorized QueryIntent, requested offset, pinned manifests/snapshots and canonical prefix | SessionRecord; DispatchScopeProjection; ResearchRecord; boundary before/inside/after group |
| `FX-TELEMETRY` | Closed logs/spans/metrics and exporter failure injector | every append branch; pre/post-boundary replay rejection; pre-source rejection; prohibited content; cardinality overflow |

Every mutation fixture records before/after journal event count, receipt set, semantic-key set,
aggregate heads and result mapping. Every read fixture records external-call/write/publication
counts and exact `requested_o/effective_as_of`.

## Contract Case Matrix: 8 Rules and 18 Clauses

The original 26 anchors above identify these parameterized case families.

| Stable anchor | Level/type | Setup and input | Expected positive / negative / property obligation |
|---|---|---|---|
| `apt-r1--single-join-authority` | L3 integration/property | `FX-SESSION + FX-DISPATCH`; permutations of ensure/link order and reverse reads | One authoritative Session→Dispatch edge; conflicting or inferred reverse link appends nothing |
| `apt-r2--idempotent-append` | L3/L4 contract/fault | Every submitted Operation, crash before/after commit, same/different digest | Same identity/digest returns byte-stable receipt and no new event; changed digest conflicts; post-commit lost response converges |
| `apt-r3--artifact-only-raw-return` | L1/L3 schema/security | Full `FX-CAPTURE` status Cartesian matrix | Only exact captured/partial/missing slot combinations pass; no raw body crosses event/result/telemetry |
| `apt-r4--extraction-provenance` | L1 property | Seven extraction-bearing Entity variants over UTF-8 boundary generator | Exact non-empty byte slice/digests/actor/method pass; boundary, digest or attribution mutations fail |
| `apt-r5--capture-supersession` | L3/L4 race | Two corrections against the same current capture head | One CAS winner; stale/fork/self/cross-chain/cycle loser appends nothing |
| `apt-r6--replay-determinism` | L1/L4 property/replay | Same verified prefix from empty state and eligible checkpoints | Equal canonical values/hashes; future/incomplete/forked/tampered input fails without effects |
| `apt-r7--protocol-profile-binding` | L2/L3 contract | Probe, atomic-group and semantic-registry profile IDs/versions/digests/receipts | Exact registered bindings pass; every missing/cross/mismatched field blocks mutation |
| `apt-r8--telemetry-non-authority` | L3/L5 security/fault | Telemetry/exporter failures and delivery-only probe evidence | No signal changes control/result; delivery does not imply access/support; no telemetry value authorizes replay/write |
| `session-context-binding` | L1/L3 state/integration | Empty/current origin tuple with new keys/names | First ensure binds once; current binding reuses immutable Session/name; wrong-origin ensure key conflicts |
| `rollover-authorization` | L2/L3 contract | Valid and tampered single-use rollover authorization | Exact action/origin/predecessor/principal/nonce/expiry gives one atomic pair; any mismatch gives none |
| `link-session-dispatch-authorization` | L2/L3 contract | Current/stale Session plus action-specific authorization | Exact current/authorized link passes; stale, absent, replayed or wrong-action evidence fails |
| `dispatch-snapshot-identity` | L1/L2 schema | Both `FX-DISPATCH` variants and mixed-field mutations | Equality/hash use all variant authority fields; accepted offset only for ACI; row index never authority |
| `capture-digest` | L1 property | Change each capture preimage slot independently and permute only canonical sets | Every semantic slot/order mutation changes digest; object-key order does not; omission differs from canonical null |
| `research-synthesis-pins` | L1/L3 property | Ordered same-Dispatch current pins plus duplicate/cross/stale/self variants | Exact unique ordered pins pass and order changes digest; invalid member rejects whole capture |
| `raw-selector-validity` | L1 property | UTF-8 strings including multibyte boundaries and half-open ranges | Valid byte boundaries reproduce selected digest; empty, split-codepoint and out-of-range selectors fail |
| `evidence-reference-validity` | L2 contract | Each closed failure/evidence discriminator with owner version/digest | Exact selected owner ref passes; dangling, mixed, stale or selector-as-evidence fails |
| `question-derivation-validity` | L1 contract | Same-capture question and pinned Dispatch-scope derivation refs | Typed exact source/version/pointer passes; text similarity, cross-capture and stale/wrong snapshot fail |
| `research-fact-appended-closed-union` | L1 schema | All ten payload families plus cross-family slot injection | Exactly one of eight Entity/disposition/assessment passes; mixed/unknown slots fail |
| `research-fact-locality` | L1/L3 property | Cross-product of capture-local targets/refs | Same-current-capture edges pass; cross/missing/stale/missing-capture fact fails |
| `research-fact-typing` | L1 schema/property | Variant cardinality and enum boundary generator | Every required/forbidden/conditional field enforced; duplicate relational members rejected |
| `reference-check-typing` | L1 schema | Check kinds/results, optional relation/evidence and checker subject keys | Claim-support requires relation; others forbid it; independent checker/method chains coexist |
| `formalization-locality` | L1 schema | Candidate with claim, notation, legend, reading, logic family, assumptions and scope | Exact same-capture claim and complete interpretation pass; missing/cross target or conflated governance/proof refs fail |
| `fact-append-identity` | L3/L4 race/property | Same global fact ID across direct/probe paths | Exact digest/subject/predecessor returns existing event; any mismatch conflicts atomically |
| `disposition-and-assessment-chains` | L3/L4 race | Canonical TargetRef chain keys and concurrent expected head/version | Correct actor/type/ID/CAS advances once; stale/wrong actor/type/ID fails without artifact read |
| `probe-lineage-append` | L3/L4 integration/fault | Zero/mixed/all-new `FX-PROBE`, crash/race and permutation cases | Total partition/mapping; receipt only nonempty new set; conflict rejects new portion; exact retry stable |
| `relational-collection-canonicalization` | L1 property | Set/list permutation and duplicate generator | Declared sets canonicalize permutation-equally, duplicates fail; semantic ordered lists preserve order |

## Operation Clause Matrix: 6 Operations / 53 Reciprocal IDs

Each row is a planned parameterized test. The fixture named in the row supplies valid baseline data;
the stated mutation is the negative input. Calculation-only `APT-OP-*-C*` formula rows are exercised
by the referenced clause/property cases and are not assigned unregistered reciprocal IDs.
Each reciprocal clause ID is defined by its owning [Operation](specs/operations.md).

| Stable ID / anchor | Level/type | Fixture/input | Expected assertion |
|---|---|---|---|
| <a id="apt-op-ens-1"></a>`APT-OP-ENS-1` | L3 idempotency | `FX-SESSION`; retry then changed digest | Same receipt/no delta; changed digest conflict |
| <a id="apt-op-ens-2"></a>`APT-OP-ENS-2` | L1 property | Origin tuple permutations | Context key equals canonical tuple digest and is not caller-selectable |
| <a id="apt-op-ens-3"></a>`APT-OP-ENS-3` | L3 semantic reuse | Same ensure key/origin, new command | Existing Session, no event/receipt claim |
| <a id="apt-op-ens-4"></a>`APT-OP-ENS-4` | L2 authority | Caller attempts Session ID/time/evidence | Owner values retained; caller authority fields rejected |
| <a id="apt-op-ens-5"></a>`APT-OP-ENS-5` | L3 state | Current origin with new key/name | Current immutable Session/name reused; no rename/event |
| <a id="apt-op-ens-6"></a>`APT-OP-ENS-6` | L3 negative | Ensure key bound to another origin | Conflict and zero journal delta |
| <a id="apt-op-rol-1"></a>`APT-OP-ROL-1` | L3 CAS | Current versus stale predecessor | Only exact current binding proceeds |
| <a id="apt-op-rol-2"></a>`APT-OP-ROL-2` | L1 schema | Successor owner IDs/origin | New IDs/key, same exact origin |
| <a id="apt-op-rol-3"></a>`APT-OP-ROL-3` | L2 authorization | Mutate actor/auth/origin between two events | Exact equality required; replay makes no policy call |
| <a id="apt-op-rol-4"></a>`APT-OP-ROL-4` | L4 atomicity | Failpoint between pair members | Both visible at group boundary or neither |
| <a id="apt-op-rol-5"></a>`APT-OP-ROL-5` | L4 idempotency | Lost response then retry/digest mutation | Stable pair receipt or idempotency conflict |
| <a id="apt-op-link-1"></a>`APT-OP-LINK-1` | L3 state | Current, historical and unbound Session | Only exact current origin binding links |
| <a id="apt-op-link-2"></a>`APT-OP-LINK-2` | L1 schema | Both snapshot variants | Input Dispatch equals variant authority identity |
| <a id="apt-op-link-3"></a>`APT-OP-LINK-3` | L3 property | Empty/same/contradictory link plus retry | Empty accepts, same exact reuses, contradiction rejects |
| <a id="apt-op-link-4"></a>`APT-OP-LINK-4` | L3 non-authority | Instrument Dispatch writer | Zero Dispatch writes; APT event only |
| <a id="apt-op-link-5"></a>`APT-OP-LINK-5` | L2 authorization | Action/policy/evidence mutation | Exact pinned authorization required; replay makes no policy call |
| <a id="apt-op-cap-1"></a>`APT-OP-CAP-1` | L1 schema | Add/remove each capture slot | Exact v1 slots present; nonapplicable is canonical null |
| <a id="apt-op-cap-2"></a>`APT-OP-CAP-2` | L1 table-driven | Full status matrix | Only exact captured/partial/missing combinations pass |
| <a id="apt-op-cap-3"></a>`APT-OP-CAP-3` | L2 artifact | Finalization/media/charset/digest mutations | Only finalized textual UTF-8 exact evidence passes |
| <a id="apt-op-cap-4"></a>`APT-OP-CAP-4` | L1 schema | Snapshot Dispatch mismatch | Both variants enforce exact Dispatch identity |
| <a id="apt-op-cap-5"></a>`APT-OP-CAP-5` | L3/L4 CAS | Initial/correction/fork/cycle cases | Initial iff no head; correction exact-current only |
| <a id="apt-op-cap-6"></a>`APT-OP-CAP-6` | L1 property | Synthesis pin order/member mutations | Unique ordered preexisting current same-Dispatch exact pins only |
| <a id="apt-op-cap-7"></a>`APT-OP-CAP-7` | L3 idempotency | Capture identity/digest variants | Sole `capture_operation_id`; exact retry stable; changed digest conflicts |
| <a id="apt-op-cap-8"></a>`APT-OP-CAP-8` | L3 authority | Missing/stale Session/link | New capture requires current binding and exact link |
| <a id="apt-op-fact-1"></a>`APT-OP-FACT-1` | L1/L3 identity | FactEnvelope field/head mutations | Five fields exact; member identity distinct from command |
| <a id="apt-op-fact-2"></a>`APT-OP-FACT-2` | L1 locality | Cross-capture edge generator | All fact/reference/selector edges stay in current non-missing capture |
| <a id="apt-op-fact-3"></a>`APT-OP-FACT-3` | L1 property | UTF-8 selector/digest/actor/method mutations | Exact nonempty bytes and all provenance evidence required |
| <a id="apt-op-fact-4"></a>`APT-OP-FACT-4` | L1 schema | Relation/check/formalization cardinalities | Closed variant constraints and duplicate rejection |
| <a id="apt-op-fact-5"></a>`APT-OP-FACT-5` | L1 property | Target/policy/actor/method key mutations | Aggregate type/ID equal canonical chain mapping |
| <a id="apt-op-fact-6"></a>`APT-OP-FACT-6` | L4 CAS race | Two aggregate writers | One exact head/version winner; loser no delta |
| <a id="apt-op-fact-7"></a>`APT-OP-FACT-7` | L3 idempotency | Retry/changed payload digest | Stable retry or conflict |
| <a id="apt-op-fact-8"></a>`APT-OP-FACT-8` | L1 schema | Cross-family FactEnvelope/CAS fields | Entity xor disposition xor assessment enforced |
| <a id="apt-op-fact-9"></a>`APT-OP-FACT-9` | L2 authority/property | Caller IDs/times; canonical key order | Owner fields retained; ACI accepted digest authoritative |
| <a id="apt-op-fact-10"></a>`APT-OP-FACT-10` | L2 auth | Payload/ingestion actor mismatch | Disposition/assessment actor equality required |
| <a id="apt-op-fact-11"></a>`APT-OP-FACT-11` | L4 semantic race | Same fact ID direct/direct and direct/probe | Transactional reread exact→existing; divergent→conflict |
| <a id="apt-op-fact-12"></a>`APT-OP-FACT-12` | L2 attribution | Replace extractor with ingestion actor | Allowed only with proof that principal performed registered extraction |
| <a id="apt-op-probe-1"></a>`APT-OP-PROBE-1` | L2 evidence | Bundle identity/digest/ref mutations | Exact committed recommendation acceptance required |
| <a id="apt-op-probe-2"></a>`APT-OP-PROBE-2` | L2 profile | ID/version/digest/receipt mutation | Registry, binding and bundle profile equal exactly |
| <a id="apt-op-probe-3"></a>`APT-OP-PROBE-3` | L2 semantics | Host observation only | Proves worker evidence only, never research access/support |
| <a id="apt-op-probe-4"></a>`APT-OP-PROBE-4` | L3 CAS | Recommendation composite/head mutations | Stable derived key and exact current predecessor |
| <a id="apt-op-probe-5"></a>`APT-OP-PROBE-5` | L3 integration | Proven use through batch | Same fact validator/registry; outer command ID on event |
| <a id="apt-op-probe-6"></a>`APT-OP-PROBE-6` | L3 idempotency | Submitted retry versus unseen zero-new | Receipt only for submitted command; zero-new no claim |
| <a id="apt-op-probe-7"></a>`APT-OP-PROBE-7` | L1/L2 evidence | 0..N use items with missing evidence | Every use requires current capture and byte-exact evidence |
| <a id="apt-op-probe-8"></a>`APT-OP-PROBE-8` | L2 semantics | Delivery with zero proven uses | Delivery-only and no access/consulted/support |
| <a id="apt-op-probe-9"></a>`APT-OP-PROBE-9` | L1 property | All unique item permutations | Same canonical order/digest; duplicate key rejects |
| <a id="apt-op-probe-10"></a>`APT-OP-PROBE-10` | L4 atomicity | Mixed group failpoints | All new members or none; existing never receipt member |
| <a id="apt-op-probe-11"></a>`APT-OP-PROBE-11` | L3 dependency | Use with prior/same-group/missing delivery | Only prior or canonically preceding delivery passes |
| <a id="apt-op-probe-12"></a>`APT-OP-PROBE-12` | L1/L3 negative | Duplicate key/virtual sequence/fork | Reject whole group against pre-command heads |
| <a id="apt-op-probe-13"></a>`APT-OP-PROBE-13` | L4 race | Concurrent same fact ID | Exact loser existing; divergent loser group conflict |
| <a id="apt-op-probe-14"></a>`APT-OP-PROBE-14` | L2 attribution | Delivery/event/use actor mutations | Ingestion equality plus independently valid extraction attribution |
| <a id="apt-op-probe-15"></a>`APT-OP-PROBE-15` | L3 table-driven | Zero/mixed/all-new/conflict | Exact total partition and result union |
| <a id="apt-op-probe-16"></a>`APT-OP-PROBE-16` | L4 transaction | Commit failpoint at key/head/event/mapping/receipt | New members and applicable records all-or-none |
| <a id="apt-op-probe-17"></a>`APT-OP-PROBE-17` | L4 transaction/race | Delivery exact/divergent collision | Exact accepted ref or whole-group semantic conflict |

## Cross-Aspect Test Matrix

| Stable ID / anchor | Level/type | Setup/input | Expected / validates |
|---|---|---|---|
| <a id="apt-state-01"></a>`APT-STATE-01` | L4 replay | `FX-JOURNAL` complete/incomplete atomic groups | Apply complete group once at last offset; incomplete member has zero projection effect ([atomic groups](specs/states.md#atomic-group-invariants)) |
| <a id="apt-state-02"></a>`APT-STATE-02` | L1 state/property | Session ensure/rollover/link transitions | Exact transition/rejection tables and invariants hold ([Session Context Binding](specs/states.md#session-context-binding)) |
| <a id="apt-state-03"></a>`APT-STATE-03` | L1/L4 state/race | Capture initial/correction/synthesis | Currentness transition and stale rejection hold ([Research Capture Currentness](specs/states.md#research-capture-currentness)) |
| <a id="apt-state-04"></a>`APT-STATE-04` | L1 state | Disposition/assessment streams | Canonical head/version reduction and per-target projections agree ([Disposition Read Projections](specs/states.md#disposition-read-projections)) |
| <a id="apt-state-05"></a>`APT-STATE-05` | L4 semantic registry | Global fact collisions | Exact result partition and receipt-only-new invariants ([semantic profile](specs/states.md#transactional-semantic-uniqueness-and-result-mapping-profile)) |
| <a id="apt-state-06"></a>`APT-STATE-06` | L4 replay/property | Random verified group sequences | Empty/checkpoint folds agree and reducer has zero effects ([test derivation](specs/states.md#test-derivation-contract)) |
| <a id="apt-evt-01"></a>`APT-EVT-01` | L1 schema | SessionStarted payload/envelope mutations | Exact closed payload, owner fields and single-event atomicity ([SessionStarted](specs/events.md#sessionstarted)) |
| <a id="apt-evt-02"></a>`APT-EVT-02` | L1/L4 schema | SessionContextRebound alone/pair | Only verified ordered rollover group is visible ([SessionContextRebound](specs/events.md#sessioncontextrebound)) |
| <a id="apt-evt-03"></a>`APT-EVT-03` | L1 schema | SessionDispatchLinked variant snapshot | Link payload exact; no Dispatch mutation fields ([SessionDispatchLinked](specs/events.md#sessiondispatchlinked)) |
| <a id="apt-evt-04"></a>`APT-EVT-04` | L1 security/schema | ResearchCaptureAppended status/body mutations | Closed capture only; raw bytes absent ([ResearchCaptureAppended](specs/events.md#researchcaptureappended)) |
| <a id="apt-evt-05"></a>`APT-EVT-05` | L1 schema/property | Ten ResearchFactAppended variants | Exclusive union, global Entity identity and aggregate CAS fields ([ResearchFactAppended](specs/events.md#researchfactappended)) |
| <a id="apt-evt-06"></a>`APT-EVT-06` | L1/L4 schema | Delivery/use batch payloads | Exact partition/group/privacy semantics ([ReferenceProbeLineageAppended](specs/events.md#referenceprobelineageappended)) |
| <a id="apt-wf-01"></a>`APT-WF-01` | L3 workflow | Ensure, explicit rollover, optional link branch matrix | Per-step atomic boundaries; no compensation/automatic rollover ([StartOrReuseSession](specs/workflows.md#startorreusesession)) |
| <a id="apt-wf-02"></a>`APT-WF-02` | L3 workflow | Capture status × fact-family × item-failure matrix | Capture persists independently; only seven Entity variants read raw bytes; aggregate branch does not ([CaptureAndEnrichResearch](specs/workflows.md#captureandenrichresearch)) |
| <a id="apt-wf-03"></a>`APT-WF-03` | L3/L4 workflow | Probe zero/mixed/all-new and failures | One mutation Operation, exact reconciliation and no saga/compensation ([IngestReferenceProbeLineage](specs/workflows.md#ingestreferenceprobelineage)) |
| <a id="apt-query-01"></a>`APT-QUERY-01` | L1/L4 query/property | SessionRecord manifest at boundary generator | Exact binder manifest, current Session/dispatch/research formulas and stable hash ([SessionRecord](specs/queries.md#sessionrecord)) |
| <a id="apt-query-02"></a>`APT-QUERY-02` | L1/L4 query/property | Both Dispatch snapshot variants and historical offsets | Exact snapshot/hash, dedupe/count formulas, no current external leak ([DispatchScopeProjection](specs/queries.md#dispatchscopeprojection)) |
| <a id="apt-query-03"></a>`APT-QUERY-03` | L1/L4 query/property | Research capture/fact/check/review histories | Exact manifest, precedence, supersession, counts and hash ([ResearchRecord](specs/queries.md#researchrecord)) |
| <a id="apt-map-01"></a>`APT-MAP-01` | L1 mapping/property | All six bound commands and owner fields | Lossless exact payload/envelope mapping; no receipt/group recursion ([APTFactToACIEvent](specs/mappings.md#aptfacttoacievent)) |
| <a id="apt-map-02"></a>`APT-MAP-02` | L1 mapping/property | Probe item permutations/partitions | Stable delivery/use mapping, canonical order and total result mapping ([ProbeBundleToReferenceLineage](specs/mappings.md#probebundletoreferencelineage)) |
| <a id="apt-map-03"></a>`APT-MAP-03` | L1 mapping/property | Verified prefix/manifests for all three queries | Every output field derives losslessly; forbidden/raw fields absent ([ProvenanceFactsToReadModels](specs/mappings.md#provenancefactstoreadmodels)) |
| <a id="apt-iface-01"></a>`APT-IFACE-01` | L2 contract | Every closed caller intent with unknown/owner fields | Exact allowlists/default nulls; unknown/forged owner fields reject ([caller shapes](specs/interfaces.md#caller-intent-shapes)) |
| <a id="apt-iface-02"></a>`APT-IFACE-02` | L2 contract | Six append methods and all result branches | Method-specific input/output, auth/evidence and processing order ([ProvenanceAppendPort](specs/interfaces.md#provenanceappendport)) |
| <a id="apt-iface-03"></a>`APT-IFACE-03` | L2 contract | Single/atomic adapter requests and unknown response | No generic append/store/transaction handle; exact ACI result verification ([ACICommandAdapter](specs/interfaces.md#acicommandadapter)) |
| <a id="apt-iface-04"></a>`APT-IFACE-04` | L2 contract | Every boundary/operation error code | Closed code, safe detail and derived retryability; APPEND_FAILED only same-command ([InterfaceError](specs/interfaces.md#interfaceerror)) |
| <a id="apt-iface-05"></a>`APT-IFACE-05` | L2 contract | Three query intents/results/errors | Exact requested/effective/source manifests; closed authorization/integrity errors ([ProvenanceQueryPort](specs/interfaces.md#provenancequeryport)) |
| <a id="apt-iface-06"></a>`APT-IFACE-06` | L2 static architecture | Dependency/import graph plus write-call scan for domain and application modules | Domain imports no owner/evidence ports; neither domain nor application writes the ACI journal, artifact backend or Dispatch ledger directly; all accepted writes cross the declared adapter/owner boundary ([Boundary Principles](specs/interfaces.md#boundary-principles), [Authority Boundary](specs/persistence-and-replay.md#authority-boundary)) |
| <a id="apt-pr-01"></a>`APT-PR-01` | L3 architecture contract | Instrument all APT storage/bus calls | ACI journal sole authority; zero APT authoritative store/bus ([Authority Boundary](specs/persistence-and-replay.md#authority-boundary)) |
| <a id="apt-pr-02"></a>`APT-PR-02` | L4 fault | Failpoint before every atomic member/commit/response | No partial receipt/event/head/key/mapping; post-commit retry stable ([Atomic Commands](specs/persistence-and-replay.md#atomic-commands-results-and-receipts)) |
| <a id="apt-pr-03"></a>`APT-PR-03` | L4 race | Same command, fact ID, capture/fact/aggregate heads | Idempotency, semantic registry and CAS choose one exact outcome ([Crash/Race](specs/persistence-and-replay.md#crash-race-and-recovery-invariants)) |
| <a id="apt-pr-04"></a>`APT-PR-04` | L4 replay | Empty/eligible/future/inside/corrupt checkpoints | Eligible iff complete verified boundary ≤ effective as-of; parity/no future leak ([Checkpoints](specs/persistence-and-replay.md#checkpoint-contract)) |
| <a id="apt-pr-05"></a>`APT-PR-05` | L4 replay | Pre/post-boundary and invalid prefix cases | Input binding authorized; pure reducer zero I/O/effects; incomplete returns READ_INTEGRITY_FAILURE ([Replay](specs/persistence-and-replay.md#replay-algorithm)) |
| <a id="apt-pr-06"></a>`APT-PR-06` | L3 security | Captured/partial/missing artifacts and transient selector reads | Artifact-only persistence; no raw research body in authoritative/derived surfaces ([Artifact-Only](specs/persistence-and-replay.md#artifact-only-persistence)) |
| <a id="apt-pr-07"></a>`APT-PR-07` | L3 migration contract | Unknown/out-of-order/divergent versions/checksums | Writes/replay blocked; external maintenance rebuild only; no event reinterpretation ([Migration](specs/persistence-and-replay.md#migration-contract)) |
| <a id="apt-pr-08"></a>`APT-PR-08` | L4 projection | Delete/stale/corrupt projection | Query rejects/falls back pure replay; never rebuilds; accepted state unchanged ([Projection Persistence](specs/persistence-and-replay.md#projection-persistence)) |
| <a id="apt-pr-09"></a>`APT-PR-09` | L4 migration/replay | Supported historical event corpus through either its retained version reader or a reviewed deterministic upcast; replay from empty and every eligible pre/post-migration checkpoint | Each registered and supported compatibility path, whichever the implementation declares, produces the same verified events, reducer state, manifests and hashes at every complete boundary as empty replay; compare retained-reader and upcast results only when both paths are declared; no event is rewritten and checkpoint/replay parity holds ([Migration Contract](specs/persistence-and-replay.md#migration-contract), [Checkpoint Contract](specs/persistence-and-replay.md#checkpoint-contract)) |
| <a id="apt-pr-10"></a>`APT-PR-10` | L3/L4 negative integration/replay | Finalized artifact exists, but its capture append is rejected, crashes before commit or remains outside a complete verified atomic group; then attempt fact append, synthesis and replay | The artifact is orphan/uncommitted evidence only: no accepted capture, fact or synthesized event is created or projected; no head, semantic key, mapping or receipt advances ([Artifact-Only Persistence](specs/persistence-and-replay.md#artifact-only-persistence), [Atomic Commands](specs/persistence-and-replay.md#atomic-commands-results-and-receipts)) |
| <a id="apt-obs-01"></a>`APT-OBS-01` | L5 schema | Every required log schema and null matrix | Closed slots/enums/correlation; normalized capture command identity ([Structured Logs](specs/observability.md#structured-log-schemas)) |
| <a id="apt-obs-02"></a>`APT-OBS-02` | L5 schema | Every span result enum/workflow span | Finite result enums; source nullable before selection; trace continuity not replay continuity ([Trace Contract](specs/observability.md#trace-contract)) |
| <a id="apt-obs-03"></a>`APT-OBS-03` | L5 metrics | Every metric and forbidden label injection | Exact bounded dimensions; accepted event only newly accepted; split verified lags ([Metric Schemas](specs/observability.md#metric-schemas)) |
| <a id="apt-obs-04"></a>`APT-OBS-04` | L5 security/property | Raw bodies/selectors/text/locators/credentials/exceptions across signals | Prohibited content retained zero times; only bounded violation reason ([Classification](specs/observability.md#data-classification-and-redaction)) |
| <a id="apt-obs-05"></a>`APT-OBS-05` | L5 fault | Logger/tracer/exporter/alert failure injection | No result/control-flow/retry/rebuild effect ([Non-Authority](specs/observability.md#non-authority-contract)) |
| <a id="apt-obs-06"></a>`APT-OBS-06` | L5 schema | `apt.event.group.accepted@1`, retry/existing branches and offset zero | Positive group offsets/count arithmetic; counter delta only accepted-new; zero genesis only ([Structured Log Schemas](specs/observability.md#structured-log-schemas)) |
| <a id="apt-obs-07"></a>`APT-OBS-07` | L5 schema | Replay pre/post boundary/source selection | No invented effective/source/lag; duration only selected source; rejection still counted ([Metric Schemas](specs/observability.md#metric-schemas)) |
| <a id="apt-obs-08"></a>`APT-OBS-08` | L5 policy | Retention/classification policy refs and expiry | Finite policy required for readiness; telemetry expiry changes no authority ([Retention](specs/observability.md#retention-and-access)) |
| <a id="apt-obs-09"></a>`APT-OBS-09` | L5 static/fault/non-authority | Exercise every dashboard query and runbook diagnostic with instrumented command, retry, rebuild and authority-write ports | Views remain read-only: zero command submission, retry initiation, projection rebuild, journal/artifact/Dispatch write or authority decision, including missing/stale telemetry branches ([Dashboard and Runbook Views](specs/observability.md#dashboard-and-runbook-views), [Non-Authority Contract](specs/observability.md#non-authority-contract)) |

## Story-to-Test Coverage

| Story | Primary test IDs | Acceptance coverage |
|---|---|---|
| [US-1](STORIES.md#us-1-ensure-one-coarse-session-for-a-host-context) | [APT-TEST-R2](#apt-r2--idempotent-append), [APT-TEST-C01](#session-context-binding), [APT-OP-ENS-1](#apt-op-ens-1), [APT-OP-ENS-2](#apt-op-ens-2), [APT-OP-ENS-3](#apt-op-ens-3), [APT-OP-ENS-4](#apt-op-ens-4), [APT-OP-ENS-5](#apt-op-ens-5), [APT-OP-ENS-6](#apt-op-ens-6) | New/reuse/conflict/owner binding |
| [US-2](STORIES.md#us-2-roll-over-a-session-only-with-explicit-authorization) | [APT-TEST-C02](#rollover-authorization), [APT-OP-ROL-1](#apt-op-rol-1), [APT-OP-ROL-2](#apt-op-rol-2), [APT-OP-ROL-3](#apt-op-rol-3), [APT-OP-ROL-4](#apt-op-rol-4), [APT-OP-ROL-5](#apt-op-rol-5), [APT-WF-01](#apt-wf-01) | Authorization, atomic pair, retry |
| [US-3](STORIES.md#us-3-link-the-current-session-to-an-authoritative-dispatch) | [APT-TEST-R1](#apt-r1--single-join-authority), [APT-TEST-C03](#link-session-dispatch-authorization), [APT-TEST-C04](#dispatch-snapshot-identity), [APT-OP-LINK-1](#apt-op-link-1), [APT-OP-LINK-2](#apt-op-link-2), [APT-OP-LINK-3](#apt-op-link-3), [APT-OP-LINK-4](#apt-op-link-4), [APT-OP-LINK-5](#apt-op-link-5) | Current link, both snapshot variants, no reverse authority |
| [US-4](STORIES.md#us-4-read-dispatch-scope-without-changing-dispatch-authority) | [APT-QUERY-02](#apt-query-02), [APT-MAP-03](#apt-map-03), [APT-IFACE-06](#apt-iface-06), [APT-PR-08](#apt-pr-08) | Pinned projection, historical unlinked, no Dispatch write |
| [US-5](STORIES.md#us-5-capture-an-exact-producer-outcome) | [APT-TEST-R3](#apt-r3--artifact-only-raw-return), [APT-TEST-C05](#capture-digest), [APT-TEST-C08](#evidence-reference-validity), [APT-OP-CAP-1](#apt-op-cap-1), [APT-OP-CAP-2](#apt-op-cap-2), [APT-OP-CAP-3](#apt-op-cap-3), [APT-OP-CAP-4](#apt-op-cap-4), [APT-PR-10](#apt-pr-10) | Exact status/evidence/artifact/digest and orphan rejection |
| [US-6](STORIES.md#us-6-correct-or-synthesize-captures-by-forward-append) | [APT-TEST-R5](#apt-r5--capture-supersession), [APT-TEST-C06](#research-synthesis-pins), [APT-TEST-C18](#relational-collection-canonicalization), [APT-OP-CAP-5](#apt-op-cap-5), [APT-OP-CAP-6](#apt-op-cap-6), [APT-OP-CAP-7](#apt-op-cap-7), [APT-OP-CAP-8](#apt-op-cap-8), [APT-PR-10](#apt-pr-10) | Correction CAS, ordered synthesis and no synthesis from orphan evidence |
| [US-7](STORIES.md#us-7-enrich-a-capture-with-attributed-questions-answers-problems-and-claims) | [APT-TEST-R4](#apt-r4--extraction-provenance), [APT-TEST-C07](#raw-selector-validity), [APT-TEST-C09](#question-derivation-validity), [APT-TEST-C10](#research-fact-appended-closed-union), [APT-TEST-C11](#research-fact-locality), [APT-TEST-C12](#research-fact-typing), [APT-TEST-C15](#fact-append-identity), [APT-OP-FACT-1](#apt-op-fact-1), [APT-OP-FACT-2](#apt-op-fact-2), [APT-OP-FACT-3](#apt-op-fact-3), [APT-OP-FACT-4](#apt-op-fact-4), [APT-OP-FACT-7](#apt-op-fact-7), [APT-OP-FACT-8](#apt-op-fact-8), [APT-OP-FACT-9](#apt-op-fact-9), [APT-OP-FACT-10](#apt-op-fact-10), [APT-OP-FACT-11](#apt-op-fact-11), [APT-OP-FACT-12](#apt-op-fact-12) | Extraction, locality, union, typing, identity |
| [US-8](STORIES.md#us-8-record-reference-use-claim-relation-and-independent-checks) | [APT-TEST-C08](#evidence-reference-validity), [APT-TEST-C11](#research-fact-locality), [APT-TEST-C13](#reference-check-typing), [APT-TEST-C15](#fact-append-identity), [APT-EVT-05](#apt-evt-05) | Use/relation/check semantics and evidence |
| [US-9](STORIES.md#us-9-preserve-candidate-formalization-and-append-only-review-chains) | [APT-TEST-C12](#research-fact-typing), [APT-TEST-C14](#formalization-locality), [APT-TEST-C16](#disposition-and-assessment-chains), [APT-OP-FACT-5](#apt-op-fact-5), [APT-OP-FACT-6](#apt-op-fact-6), [APT-OP-FACT-10](#apt-op-fact-10) | Candidate completeness and aggregate CAS |
| [US-10](STORIES.md#us-10-ingest-an-idempotent-mixed-probe-lineage-result) | [APT-TEST-R2](#apt-r2--idempotent-append), [APT-TEST-R7](#apt-r7--protocol-profile-binding), [APT-TEST-C15](#fact-append-identity), [APT-TEST-C17](#probe-lineage-append), [APT-TEST-C18](#relational-collection-canonicalization), [APT-OP-PROBE-1](#apt-op-probe-1), [APT-OP-PROBE-2](#apt-op-probe-2), [APT-OP-PROBE-3](#apt-op-probe-3), [APT-OP-PROBE-4](#apt-op-probe-4), [APT-OP-PROBE-5](#apt-op-probe-5), [APT-OP-PROBE-6](#apt-op-probe-6), [APT-OP-PROBE-7](#apt-op-probe-7), [APT-OP-PROBE-8](#apt-op-probe-8), [APT-OP-PROBE-9](#apt-op-probe-9), [APT-OP-PROBE-10](#apt-op-probe-10), [APT-OP-PROBE-11](#apt-op-probe-11), [APT-OP-PROBE-12](#apt-op-probe-12), [APT-OP-PROBE-13](#apt-op-probe-13), [APT-OP-PROBE-14](#apt-op-probe-14), [APT-OP-PROBE-15](#apt-op-probe-15), [APT-OP-PROBE-16](#apt-op-probe-16), [APT-OP-PROBE-17](#apt-op-probe-17) | Profiles, partition, receipt, idempotency, delivery-only |
| [US-11](STORIES.md#us-11-rebuild-session-dispatch-and-research-records-at-an-explicit-offset) | [APT-TEST-R6](#apt-r6--replay-determinism), [APT-QUERY-01](#apt-query-01), [APT-QUERY-02](#apt-query-02), [APT-QUERY-03](#apt-query-03), [APT-PR-04](#apt-pr-04), [APT-PR-05](#apt-pr-05), [APT-PR-08](#apt-pr-08), [APT-PR-09](#apt-pr-09) | As-of, manifests/formulas, migration/checkpoint parity and integrity |
| [US-12](STORIES.md#us-12-diagnose-safely-without-making-telemetry-authoritative) | [APT-TEST-R8](#apt-r8--telemetry-non-authority), [APT-OBS-01](#apt-obs-01), [APT-OBS-02](#apt-obs-02), [APT-OBS-03](#apt-obs-03), [APT-OBS-04](#apt-obs-04), [APT-OBS-05](#apt-obs-05), [APT-OBS-06](#apt-obs-06), [APT-OBS-07](#apt-obs-07), [APT-OBS-08](#apt-obs-08), [APT-OBS-09](#apt-obs-09) | Privacy, cardinality, read-only non-authority and retention |

## Source Coverage and Zero-Orphan Gate

| Source | Required | Covered by | Planned count |
|---|---:|---|---:|
| Rules | 8/8 | APT-TEST-R1..R8 | 8 |
| Rule clauses | 18/18 | APT-TEST-C01..C18 | 18 |
| Operations | 6/6 | 53 reciprocal APT-OP IDs plus shared error/crash cases | 53 |
| State/reducer areas | all registered state sections | APT-STATE-01..06 | 6 |
| Events | 6/6 | APT-EVT-01..06 | 6 |
| Workflows | 3/3 | APT-WF-01..03 | 3 |
| Queries | 3/3 | APT-QUERY-01..03 | 3 |
| Registered Mappings | 3/3 | APT-MAP-01..03 | 3 |
| Interfaces/shapes/errors | append/query/adapter/intents/errors/static dependencies | APT-IFACE-01..06 | 6 |
| Persistence/replay | authority, atomicity, crash/race, checkpoints, replay, artifact, migration compatibility, projection and orphan rejection | APT-PR-01..10 | 10 |
| Observability | logs, spans, metrics, privacy, non-authority, group, replay null matrix, retention and read-only diagnostic views | APT-OBS-01..09 | 9 |
| Stories | 12/12 | Story-to-Test Coverage | 12 |

Gate checks required before review:

```text
all inbound TEST-SPEC.md#anchors resolve
all Test Matrix IDs resolve to exactly one stable anchor
all stable test anchors appear in a matrix/detail row
rules = 8/8
clauses = 18/18
operations = 6/6 and reciprocal_operation_ids = 53/53
events = 6/6
workflows = 3/3
queries = 3/3
mappings = 3/3
interfaces = 6 planned cases
persistence_and_replay = 10 planned cases
observability = 9 planned cases
stories = 12/12
executionStatus = not-run
passing_evidence = none
```

## Known Gaps

- Exact executable file paths, runner commands, seeds, generated-case counts, timeout budgets and
  evidence receipt locations remain deferred to implementation readiness.
- Profile conformance fixtures require the exact ACI-registered profile digests/receipts; until
  available, affected cases remain planned and blocked rather than skipped or simulated as passing.
- No implementation path, executable test, test command, execution receipt or passing verdict
  exists yet.

## Out of Scope

- UI rendering/interaction tests; this increment specifies domain/application/read contracts only.
- Deployment, multi-host durability and production SLO tests.
- Historical backfill, bibliographic equivalence, promoted global assertions or ontology acceptance.
- Testing ACI internals beyond the exact profile/command/artifact/read boundaries consumed by APT.

## Connections

| Document | Type | Description |
|---|---|---|
| [rules.md](specs/rules.md) | `verifies-planned` | Source of the 26 reserved coverage obligations. |
| [operations.md](specs/operations.md) | `verifies-planned` | Supplies six Operations, 53 reciprocal clauses and crash/race obligations. |
| [states.md](specs/states.md) | `verifies-planned` | Supplies reducer transitions, atomic-group and semantic-registry invariants. |
| [events.md](specs/events.md) | `verifies-planned` | Supplies six closed Event payload contracts. |
| [workflows.md](specs/workflows.md) | `verifies-planned` | Supplies three orchestration contracts and step boundaries. |
| [queries.md](specs/queries.md) | `verifies-planned` | Supplies three deterministic query manifests/formulas/hashes. |
| [mappings.md](specs/mappings.md) | `verifies-planned` | Supplies three registered lossless mappings. |
| [interfaces.md](specs/interfaces.md) | `verifies-planned` | Supplies closed intents, ports, outcomes and errors. |
| [persistence-and-replay.md](specs/persistence-and-replay.md) | `verifies-planned` | Supplies authority, crash/race/checkpoint/replay/migration obligations. |
| [observability.md](specs/observability.md) | `verifies-planned` | Supplies signal schemas, privacy, cardinality, retention and non-authority. |
| [STORIES.md](STORIES.md) | `accepts-planned` | Supplies 12 L0 journeys and acceptance criteria. |
