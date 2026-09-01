---
title: ACI Execution Policy D0
status: design-draft
updatedAt: 2026-09-01
owner: agents-communication-infra
scope: runtime execution policy contracts
---

# TECH-POLICY-D0 — closed execution-policy contracts and layering

## Decision result

This design closes only the technical shape and sequencing of `ResourceBudget`, `SandboxPolicy`
and `ExecutionAuthorityFence`. It does not select product limits or grants, authorize `OPEN`, move a
Run to `ready`, claim an effect, start a provider, or satisfy target-host cutover evidence.

The current implementation accepts these three controls only as dictionaries in the bounded reveal
delivery proof. That proves transport and digest inclusion, not closed validation or enforcement.
The test values `{"max_tokens":1000}`, `{"network":"denied"}` and
`{"mode":"runtime-managed"}` are therefore compatibility placeholders, not instances of the
contracts below.

Sources:

- [Domain value objects](../../../../specs/domain.md#resourcebudget) define the present field-level
  intent.
- [StartAgentAttempt](../../../../specs/operations.md#startagentattempt) assigns budget and sandbox
  values to confirmed policy and assigns the fence to the cutover verifier.
- [SandboxLauncher](../../../../specs/interfaces.md#internal-sandboxlauncher) keeps target-host
  enforcement and negative escape evidence as a real-provider admission gate.
- [PRODUCT-PASS](DECISION-GATE.md#hard-blocker--product-pass) remains the authority gate for exact
  product-owned values and a new CONF v2.

## Contract-wide rules

All three documents use these rules:

1. The JSON shape is recursively closed. Unknown, missing, duplicate or misspelled fields reject.
2. JSON booleans are not integers. Numeric strings, floats, negative numbers, `null`, infinity and
   implicit coercion reject.
3. There are no defaults. Absence never means unlimited, inherited, host default or allow.
4. Canonical bytes use `aci-cjson-1`; content digests are lowercase
   `sha256:<64-lowercase-hex>` over those exact bytes.
5. A `VersionedReference` is exactly `{name, version, digest}`. It is accepted only after the
   referenced bytes are loaded and reproduce `digest` under the reference owner's contract.
6. The complete policy values are included in `AgentInvocationPlan` canonical bytes. Their equality
   is therefore part of `plan_digest`; the same values are copied without reinterpretation into the
   sealed `AgentExecutionRequest` and its digest.
7. Provider-native translations are observations/materialization metadata. They never replace or
   weaken the canonical controls.
8. Failure to parse, resolve, enforce or prove any required control rejects before effect release.

These rules require a later amendment to the feature specs and runtime. This document does not make
that amendment by itself.

## Closed schema — `aci.resource-budget@1`

The document has exactly these fields, in semantic form:

| Field | Type | Rule |
|---|---|---|
| `schema` | string | Exact `aci.resource-budget@1`. |
| `max_wall_time_ms` | integer | Finite, `>= 0`; `0` denies execution time. |
| `max_input_tokens` | integer | Finite, `>= 0`; unknown provider accounting never becomes zero usage. |
| `max_output_tokens` | integer | Finite, `>= 0`. |
| `max_tool_calls` | integer | Finite, `>= 0`; must be `0` when the confirmed tool profile is `tool.none`. |
| `max_payload_bytes` | integer | Finite, `>= 0`; applies to accepted provider/result payload bytes under the referenced policy. |
| `max_artifact_bytes` | integer | Finite, `>= 0`; applies to artifacts attributable to the Attempt under the referenced policy. |
| `budget_policy_ref` | `VersionedReference` | Exact enforcement and accounting semantics. |

`resource_budget_digest = sha256(aci-cjson-1(resource_budget))`. The digest may be stored as artifact
metadata or in an enclosing contract; it is not inserted into this document and therefore creates no
digest cycle.

### Dispatch budgets are not Attempt budgets

The confirmed dispatch fields `max_attempts_per_turn`, `max_total_turns` and
`wall_clock_seconds` govern scheduling of the complete Run. `ResourceBudget` governs one physical
Attempt. No implementation may divide, copy or reinterpret the dispatch limits into an Attempt
budget implicitly.

- `run_deadline = confirmed_at + wall_clock_seconds` is a deterministic Run-level ceiling.
- Each Attempt receives a product-confirmed `ResourceBudget` and a frozen `deadline` no later than
  `run_deadline`.
- `max_wall_time_ms` and `deadline` both apply; reaching either stops or denies further physical
  execution according to `budget_policy_ref`.
- Retries consume the dispatch attempt ceilings and receive their own explicitly authorized Attempt
  budget. Retry does not reset the Run deadline or aggregate policy accounting.
- Provider counters remain observations. Missing counters do not create unused budget and cannot
  authorize another effect.

The exact per-role/per-operation budget values are product authority and must be present in CONF v2
or in a digest-bound policy table whose complete bytes are part of that authority.

## Closed schema — `aci.sandbox-policy@1`

The top-level document has exactly:

| Field | Type | Rule |
|---|---|---|
| `schema` | string | Exact `aci.sandbox-policy@1`. |
| `policy_ref` | `VersionedReference` | Exact launcher/enforcement semantics. |
| `filesystem_scope` | object | Exact grammar below. |
| `network_scope` | object | Exact grammar below. |
| `process_scope` | object | Exact grammar below. |
| `credential_refs` | list of `VersionedReference` | Ordered, duplicate-free opaque grants; secrets are forbidden. |

`sandbox_policy_digest = sha256(aci-cjson-1(sandbox_policy))`. As with the budget, the digest belongs
to metadata or the enclosing authority, not inside the hashed document.

The v1 scope grammars are deliberately narrow:

```json
{
  "filesystem_scope": {
    "default": "deny",
    "read_roots": [],
    "write_roots": [],
    "link_policy": "deny"
  },
  "network_scope": {
    "default": "deny",
    "allowed_endpoints": []
  },
  "process_scope": {
    "default": "deny",
    "allowed_executables": [],
    "max_child_processes": 0
  }
}
```

- `default` is always the literal `deny` in v1; an allow-by-default policy needs a new schema and a
  product decision.
- Roots are canonical repository-relative paths with `/`, no empty component, `.`, `..`, drive,
  UNC path, wildcard or link traversal. Empty lists grant nothing.
- Endpoint and executable entries require separate closed, digest-pinned definitions before they
  may become non-empty. D0 does not invent those definitions.
- A launcher must validate its host capabilities against the complete policy before process
  creation. Unsupported enforcement rejects; it never silently narrows or widens the policy.

### Fake deny-all lane

The only package admitted before product grants and target-host evidence is a synthetic oracle
fixture for a test-only fake lane. Its policy-reference targets are themselves closed documents.

`aci.budget-policy@1` has exactly `schema`, `scope`, `exhaustion_action` and
`unknown_usage_action`. The synthetic referenced bytes and digest are:

```text
{"exhaustion_action":"deny-new-work","schema":"aci.budget-policy@1","scope":"attempt","unknown_usage_action":"deny-new-work"}
sha256:08f3494d9e869053ee097e854840ade80afcda65cce75ef774038be5c6c242d2
```

`aci.sandbox-enforcement-policy@1` has exactly `schema`, `enforcement_mode` and
`unsupported_control_action`. Its synthetic referenced bytes and digest are:

```text
{"enforcement_mode":"deny-all","schema":"aci.sandbox-enforcement-policy@1","unsupported_control_action":"deny"}
sha256:88f400d1661b69ac6536b548216bb7f5a370042050df2ea7bae49e03952725ea
```

The fully valid, all-zero synthetic `ResourceBudget` has these exact canonical bytes and digest:

```text
{"budget_policy_ref":{"digest":"sha256:08f3494d9e869053ee097e854840ade80afcda65cce75ef774038be5c6c242d2","name":"aci.budget-policy.fake-deny-all","version":"1"},"max_artifact_bytes":0,"max_input_tokens":0,"max_output_tokens":0,"max_payload_bytes":0,"max_tool_calls":0,"max_wall_time_ms":0,"schema":"aci.resource-budget@1"}
sha256:e6e3a27b6fecf0ca8667ca722bb1e74a39e4d1f685da172f75a8077a67ba3836
```

All zero ceilings are valid and deny physical execution or resource consumption. They are not
missing values and are not suitable values for a useful product run.

The fully valid synthetic deny-all `SandboxPolicy` has these exact canonical bytes and digest:

```text
{"credential_refs":[],"filesystem_scope":{"default":"deny","link_policy":"deny","read_roots":[],"write_roots":[]},"network_scope":{"allowed_endpoints":[],"default":"deny"},"policy_ref":{"digest":"sha256:88f400d1661b69ac6536b548216bb7f5a370042050df2ea7bae49e03952725ea","name":"aci.sandbox-policy.fake-deny-all","version":"1"},"process_scope":{"allowed_executables":[],"default":"deny","max_child_processes":0},"schema":"aci.sandbox-policy@1"}
sha256:d865e9f97c6b73afc4748e5bd6d58095e471450d72cd45c3fb4a55a8185e3b1a
```

For oracle tests only, the two values may be collected in
`aci.execution-policy-oracle-fixture@1`. Its exact canonical bytes and content digest are:

```text
{"resource_budget":{"budget_policy_ref":{"digest":"sha256:08f3494d9e869053ee097e854840ade80afcda65cce75ef774038be5c6c242d2","name":"aci.budget-policy.fake-deny-all","version":"1"},"max_artifact_bytes":0,"max_input_tokens":0,"max_output_tokens":0,"max_payload_bytes":0,"max_tool_calls":0,"max_wall_time_ms":0,"schema":"aci.resource-budget@1"},"resource_budget_digest":"sha256:e6e3a27b6fecf0ca8667ca722bb1e74a39e4d1f685da172f75a8077a67ba3836","sandbox_policy":{"credential_refs":[],"filesystem_scope":{"default":"deny","link_policy":"deny","read_roots":[],"write_roots":[]},"network_scope":{"allowed_endpoints":[],"default":"deny"},"policy_ref":{"digest":"sha256:88f400d1661b69ac6536b548216bb7f5a370042050df2ea7bae49e03952725ea","name":"aci.sandbox-policy.fake-deny-all","version":"1"},"process_scope":{"allowed_executables":[],"default":"deny","max_child_processes":0},"schema":"aci.sandbox-policy@1"},"sandbox_policy_digest":"sha256:d865e9f97c6b73afc4748e5bd6d58095e471450d72cd45c3fb4a55a8185e3b1a","schema":"aci.execution-policy-oracle-fixture@1"}
sha256:9abfb7e61f995a90e8a08a72dfa96dda2df956f63e4e4360e78eca22493641f6
```

This combined document is an **oracle fixture**, never executable authority. Production parsers,
confirmation, plan/request acceptance and effect workers must reject it wherever a product-confirmed
policy package or execution authority is required. The fake lane may prove parsing,
canonicalization, synthetic lineage and denial only. It authorizes no subprocess, provider,
filesystem, network or credential effect.

## Closed schema — `aci.execution-authority-fence@1`

The fence document has exactly:

| Field | Type | Rule |
|---|---|---|
| `schema` | string | Exact `aci.execution-authority-fence@1`. |
| `dispatch_id` | string | Exact confirmed runtime dispatch. |
| `run_id` | string | Exact confirmed Run. |
| `authority_mode` | string | Exact `runtime-managed`. |
| `cutover_epoch` | integer | Positive, current monotonic epoch for the target host. |
| `legacy_watcher_disabled_evidence_ref` | `ArtifactId` | Finalized, independently readable target-host evidence. |
| `fence_digest` | digest | Digest of the preimage defined below. |

The digest preimage is the same object with schema
`aci.execution-authority-fence-preimage@1` and without `fence_digest`.

`fence_digest = sha256(aci-cjson-1(fence_preimage))`.

Acceptance and use require all of the following:

1. `dispatch_id`, `run_id` and `authority_mode` equal frozen runtime authority.
2. `cutover_epoch` equals the current accepted host cutover head both at effect claim and immediately
   before physical start.
3. The evidence artifact exists, its bytes reproduce stored metadata, and it binds the same host,
   epoch, watcher-disable state, writer inventory and configuration digests.
4. Verified audit opening, current Run/Group prerequisite heads and sandbox validation pass
   independently. The fence substitutes for none of them.
5. Epoch drift, revoked/missing evidence, unreadable bytes or an unsupported launcher fails closed and
   creates no process.

`cutover_epoch` and watcher-disable evidence are not product-entered fields. They are operational
facts produced only by the cutover verifier after the required target-host evidence exists. A fake
test may use a separately named harness fence but must never report it as an executable production
fence or transition a real Run through it.

### Structurally valid harness fence

Oracle tests use the distinct schema `aci.execution-authority-fence-harness@1`. It has the same
field names and types as the production fence, but its preimage schema is
`aci.execution-authority-fence-harness-preimage@1`. The exact synthetic preimage bytes and digest
are:

```text
{"authority_mode":"runtime-managed","cutover_epoch":1,"dispatch_id":"dispatch_policy_oracle_fixture","legacy_watcher_disabled_evidence_ref":"art_policy_harness_watcher_disabled_fixture","run_id":"run_policy_oracle_fixture","schema":"aci.execution-authority-fence-harness-preimage@1"}
sha256:124d06fa0b4c2e55eef48bc5b0c33ce19880d15ce82e0d3af9518a80536de70f
```

The exact harness fence bytes are:

```text
{"authority_mode":"runtime-managed","cutover_epoch":1,"dispatch_id":"dispatch_policy_oracle_fixture","fence_digest":"sha256:124d06fa0b4c2e55eef48bc5b0c33ce19880d15ce82e0d3af9518a80536de70f","legacy_watcher_disabled_evidence_ref":"art_policy_harness_watcher_disabled_fixture","run_id":"run_policy_oracle_fixture","schema":"aci.execution-authority-fence-harness@1"}
```

Their full-document content digest is
`sha256:4672e47ccc7fb906a14c0cd57de0bbd74271cfb7697d3a539dc97251bb864ba4`;
the embedded `fence_digest` continues to identify the preimage, not the complete fence document.
The harness parser may accept this document for pure oracle tests. The production fence parser
accepts only `aci.execution-authority-fence@1` and therefore must reject the harness literal before
resolving its synthetic evidence reference. No harness document may satisfy cutover, opening,
plan/request acceptance or an effect claim.

## Authority split

| Decision/value | Owner | D0 disposition |
|---|---|---|
| Six numerical Attempt ceilings | Product | Required before CONF v2; no defaults. |
| Per-role/per-operation budget assignment | Product | Required before CONF v2. |
| Filesystem/network/process grants | Product | Empty deny-all is test-only; non-empty values require explicit choice. |
| Credential grants | Product | Empty by default in the fake proposal; any grant requires explicit choice and opaque ref. |
| Tool profile | Product plus capability resolution | `tool.none` mechanically implies `max_tool_calls=0`; any other profile requires reconfirmation. |
| Closed schemas, canonicalization and validation errors | Runtime contract | TECH-POLICY-D0 follow-up work. |
| Policy reference bytes and digests | Runtime contract plus selected product values | Derived only after exact content exists. |
| Run deadline derivation | Runtime contract | `confirmed_at + wall_clock_seconds`; no Attempt-budget inference. |
| Cutover epoch and watcher-disable evidence | Cutover verifier/operator evidence | Cannot be supplied by product preference or local fixture. |
| Fence digest and currentness check | Runtime contract | Derived/checked after complete operational evidence exists. |

## Implementation layering

The layer boundary is decision-first: a later layer starts when its next unit would add less evidence
to the current question than beginning the next distinct question.

| Layer | Decision question | Minimum working unit | Operator-visible outcome | Main risk reduced | Promotion |
|---|---|---|---|---|---|
| L0 — contract oracle | After this layer, we know whether the three policy documents can be parsed, canonicalized and rejected without defaults or ambiguity. | Pure schemas/validators, golden bytes/digests and mutation vectors; zero DB/service/effect. | Exact valid/invalid package report. | Placeholder dictionaries and implicit grants. | Promote only after independent review and complete negative-vector coverage. |
| L1 — synthetic-authority lineage | After this layer, we know whether the exact oracle bytes and references retain one non-executable integrity lineage through local artifact persistence and reopen. | Persist only the synthetic reference targets, policy documents, combined oracle and harness fence through an isolated test seam; no runtime aggregate, plan or request. | Reopen reproduces every fixture byte/digest and one synthetic-lineage receipt. | Fixture drift being mistaken for product or execution authority. | Promote only after replay/conflict/failpoint/reopen proof and explicit production-parser rejection. |
| L2 — fake deny-all | After this layer, we know whether the effect boundary rejects every external action under the fake deny-all package. | Test-only fake worker/launcher denial with zero process/network/filesystem/credential action. | Durable denial/receipt evidence without provider start. | A fixture accidentally becoming executable authority. | Promote only for fake continuation work; never promote real-provider claims. |
| L3 — target-host enforcement | After this layer, we know whether one admitted host can enforce selected policy and a current fence before a real provider starts. | Separate cutover/launcher/provider-admission units with actual epoch and watcher-disable artifact. | One bounded host launch or exact fail-closed denial. | Sandbox escape, dual authority and stale-fence execution. | Requires PRODUCT-PASS, TASK-020 evidence, host negatives and explicit later readiness. |

### Smallest implementation/test increments

1. `POLICY-000` — pure contract/oracle only: three strict decoders, canonical encoders, qualified
   digests, one golden deny-all package and mutations for every field/type/boundary. No migration.
2. `POLICY-001` — synthetic-authority lineage only: persist exact oracle/reference/harness fixture
   bytes and a clearly named non-executable lineage receipt through an isolated test seam; prove
   failpoints, replay, conflict and reopen. Create no `ConfirmedDispatch`, Run, Group, Attempt,
   `AgentInvocationPlan`, `AgentExecutionRequest`, event or effect.
3. `POLICY-002` — fake denial only: a test-only launcher port proves zero external actions for the
   deny-all package. It does not fabricate cutover evidence or a current production fence.
4. `POLICY-003` — operational evidence and real enforcement: separate exact work packs for cutover
   epoch/evidence, sandbox launcher, and provider admission. These may split further if their write
   scopes or evidence owners differ.

Each increment requires its own descriptor, readiness receipt, traceability, focused tests and
independent review before code entry. No migration number or concrete write scope is allocated by
this design. Real `AgentInvocationPlan`/`AgentExecutionRequest` binding is not part of POLICY-001 or
any synthetic lane. It remains behind PRODUCT-PASS, complete CONF v2 bytes, explicit user
confirmation and a later separately readied work unit.

## Negative-vector allocation by layer

### L0 / POLICY-000 — pure contract oracle

Independently test:

- every required field missing, extra and wrong-typed in all five policy/reference schemas and both
  production/harness fence schemas;
- boolean, numeric string, float, negative and implementation-overflow representations for every
  integer;
- zero in every ResourceBudget ceiling is accepted as an explicit denial, while omission rejects;
- one-byte drift in each exact fixture and reference target changes the expected digest;
- mismatched, unreadable and wrong-schema versioned-reference targets;
- `tool.none` with nonzero `max_tool_calls`;
- duplicate credential refs and secret bytes embedded instead of opaque refs;
- allow-by-default, path traversal, drive/UNC/wildcard/link escape, and endpoint/executable entries
  without a closed definition;
- fence and fence-preimage digest-domain substitution; and
- the harness fence is valid under its harness parser and rejected by the production parser solely
  from its schema literal, before evidence resolution.

### L1 / POLICY-001 — synthetic-authority lineage

Independently test:

- reference target body/digest drift, swapped budget/sandbox targets and missing artifact bytes;
- resource/sandbox body drift against the digests stored in the combined oracle;
- combined-oracle member removal, addition, reorder-equivalent canonicalization and digest drift;
- harness preimage/fence/content-digest domain confusion;
- same synthetic key plus identical bytes returns the first lineage receipt, while same key or
  identity with changed bytes conflicts;
- every persistence failpoint followed by reopen yields the complete synthetic unit or none; and
- zero runtime authority rows, plans, requests, events and effects after success and every failure.

### L2 / POLICY-002 — fake deny-all behavior

Independently test:

- every attempted filesystem read/write, network connection, child process, credential resolution,
  tool call and positive wall/token/payload/artifact consumption is denied;
- adding a non-empty grant or positive budget prevents admission to the exact fake deny-all lane;
- retry and reopen reproduce the same denial receipt without performing the denied action;
- no fake result creates a provider identity, target-host fence, verified opening or Run transition;
  and
- attempts to submit the combined oracle or harness fence to production confirmation, plan/request
  acceptance or an effect boundary reject before mutation.

### L3 / POLICY-003 — target-host enforcement

Independently test:

- production fence dispatch/run/mode/epoch/evidence/digest drift;
- stale epoch races between effect claim and immediate pre-start validation;
- missing, corrupt, revoked, cross-host or wrong-epoch watcher-disable evidence;
- filesystem/network/process escape and credential leakage against each selected grant;
- provider-native translation that exceeds, drops or renames a canonical budget ceiling; and
- process creation remains zero whenever opening, prerequisite heads, budget, sandbox or fence fails.

## Non-regression guardrails

- CONF-001 still ends at `opening_pending` with one unclaimed audit-opening intent and zero external
  action.
- HEADS/BUS remain component evidence; no new service/API path makes positive execution reachable.
- Policy absence or ambiguity denies; it never inherits host defaults.
- Opening verification, prerequisite-head CAS, sandbox enforcement and the authority fence remain
  independent conjunctive gates.
- Runtime replay invokes no provider, launcher, appender or policy resolver with external effects.
- CONF v1 remains an immutable component fixture. Exact policy additions require a new dispatch
  identity, CONF v2 bytes and explicit user confirmation.
- No fake-adapter result is promoted as real-provider or target-host enforcement evidence.

## Product decisions still open

Before CONF v2, product must select:

1. all six finite `ResourceBudget` values for each applicable role/operation or one explicitly shared
   package;
2. any non-empty filesystem, network or process grants;
3. any credential grant by opaque versioned reference;
4. whether the confirmed tool profile remains `tool.none`; and
5. the exact policy documents presented for confirmation after their references and digests exist.

The exact deny-all documents and their combined oracle are synthetic test fixtures, not consent,
not a product package and never executable authority.

## Recommended next layer

Start `POLICY-000` only after a separately authored descriptor/readiness receipt names the exact
spec, fixture, pure-module and test scope. The most important deferred scope is any real launcher or
provider execution: it remains blocked by product grants, audit opening, cutover epoch/evidence,
TASK-020 and target-host sandbox negatives.
