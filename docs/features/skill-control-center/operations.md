# Operations: Skill & Dispatch Control Center

Phase 1 operations mutate only user-local preferences or non-authoritative proposal state. None
calls a configuration writer, requests approval, applies, retries, reconciles, emits an accepted
receipt, or changes an authoritative revision. This boundary derives from the
[Phase 1 decision](../../decisions/skill-control-center-phase-1-scope.md#decision).

## SaveLocalPreference

**Type:** Operation (local mutation)  
**Actor:** Current operator  
**Triggers:** Commit of a filter, layout, pin, comparison set or saved-view preference

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `user_scope_id` | string | yes | Browser/user-local namespace; never an authority identity |
| `expected_revision` | non-negative integer | yes | Last local revision read; use `0` only when the preference key is absent |
| `preference_kind` | enum | yes | `filter`, `layout`, `pin`, `comparison-set`, `saved-view` |
| `value` | JSON value | yes | Value allowed by the versioned preference schema |
| `schema_version` | string | yes | Preference schema identifier |

### Rules

| ID | Rule | Formal | Authority |
|---|---|---|---|
| SLP-R1 | Writes stay inside the current local namespace. | `target_scope = current_user_scope` | [Scope decision](../../decisions/skill-control-center-phase-1-scope.md#decision) |
| SLP-R2 | The caller must use the current revision. | `expected_revision = stored_revision` | [Discovery authority table](discovery/control-center.md#7-configuration-authority-and-receipt-boundary) |
| SLP-R3 | The kind and value must satisfy the named schema. | `validate(schema_version, preference_kind, value)=true` | [Discovery authority table](discovery/control-center.md#7-configuration-authority-and-receipt-boundary) |
| SLP-R4 | The operation cannot address authoritative stores. | `target_store ∩ authoritative_stores = ∅` | [Phase 1 guardrails](BACKLOG.md#phase-1-guardrails) |

### Calculations

| ID | Calculation | Formula | Authority |
|---|---|---|---|
| SLP-C1 | Next local preference revision | `result_revision = expected_revision + 1` | [AD-005](architecture.md#ad-005) |

### State Transition

The following matrix is total for every recognized result code. `retryable` means the exact retained
input may be attempted again after the named safe action; `terminal` ends this attempt.

**Normative first-match precedence:** evaluate `SLP-R1`, `SLP-R2`, `SLP-R3`, then `SLP-R4`.
Return the first failing rule's code. Only when all four pass may persistence run; persistence
failure precedes success. `protocol-error` is a consumer-side guard for an undeclared producer
code and never competes with producer input failures.

| From | Condition | `result.code` | To | Retry class | Input retained | Stored revision effect | Safe next action |
|---|---|---|---|---|---|---|---|
| `absent` | SLP-R1..4 pass and `expected_revision=0` | `saved-local` | `saved-local` | terminal | no | atomic create at `1` | Continue |
| `saved-local` | SLP-R1..4 pass and CAS matches | `saved-local` | `saved-local` | terminal | no | atomic replace at `expected+1` | Continue |
| any | SLP-R1 fails | `invalid-local-scope` | unchanged | terminal | no | unchanged | Restore current scope |
| any | SLP-R2 fails | `local-conflict` | unchanged | retryable | yes | unchanged | Refresh revision, review retained value |
| any | SLP-R3 fails | `invalid-local-preference` | unchanged | terminal | no | unchanged | Correct kind/value/schema |
| any | SLP-R4 fails | `forbidden-local-target` | unchanged | terminal | no | unchanged | Use local target only |
| any | Atomic persistence fails before commit | `save-failed` | unchanged | retryable | yes | unchanged; no partial write | Retry exact retained input |
| any | Store/consumer receives an undeclared code | `protocol-error` | unchanged | terminal | no | unchanged | Stop and report contract mismatch |

All rows have `authoritative_effects=∅`. The closed code set is exactly
`{saved-local, invalid-local-scope, local-conflict, invalid-local-preference,
forbidden-local-target, save-failed, protocol-error}`.

### Postconditions

| Postcondition | Authority |
|---|---|
| Success atomically writes the complete value once and returns `saved-local`, the stored value and the SLP-C1 revision. | [AD-005](architecture.md#ad-005) |
| No Dispatch, skill source, telemetry source or authoritative configuration revision changes. | [Phase 1 decision](../../decisions/skill-control-center-phase-1-scope.md#decision) |

### Error States

Every non-success condition maps one-to-one to the State Transition matrix. Closed-code and
retention authority: [AD-006](architecture.md#ad-006), [AD-007](architecture.md#ad-007).

## SaveChangeProposal

**Type:** Operation (local draft mutation)  
**Actor:** Draft owner  
**Triggers:** Explicit save of a new or edited proposal

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `proposal_id` | string | yes | Stable local proposal identity |
| `expected_draft_revision` | non-negative integer | yes | Use `0` only when `proposal_id` is absent; otherwise the last stored revision read |
| `target_kind` | string | yes | Stable target kind displayed to the operator |
| `target_id` | string | yes | Stable target identity |
| `base_revision_or_hash` | string | yes | Disclosed authoritative base witness; not modified |
| `proposed_patch` | JSON Patch-like array | yes | Explicit proposed changes |
| `effective_values` | object | yes | Preview values with an origin per value |
| `schema_version` | string | yes | Draft schema identifier |

### Rules

| ID | Rule | Formal | Authority |
|---|---|---|---|
| SCP-R1 | Target, base and diff are explicit. | `target_id != "" && base != "" && len(patch)>0` | [ChangeProposal](discovery/control-center.md#changeproposal) |
| SCP-R2 | Every effective value has an origin. | `∀v ∈ effective_values: origin(v) != null` | [SCD-09](discovery/control-center.md#7-configuration-authority-and-receipt-boundary) |
| SCP-R3 | Save is local and non-authoritative. | `authoritative_effects = ∅` | [Scope decision](../../decisions/skill-control-center-phase-1-scope.md#decision) |
| SCP-R4 | Deferred lifecycle tokens cannot be stored as Phase 1 outcomes. | `state ∉ {approved, applying, accepted, conflict, indeterminate-reconciling, failed}` | [Phase 1 guardrails](BACKLOG.md#phase-1-guardrails) |
| SCP-R5 | Draft create/update uses compare-and-swap semantics. | `(absent(proposal) && expected=0) || (!absent(proposal) && expected=stored_revision)` | [AD-005](architecture.md#ad-005) |
| SCP-R6 | Schema, patch and target kind are recognized. | `known(schema_version) && well_formed(patch) && supported(target_kind)` | [AD-007](architecture.md#ad-007) |

### Calculations

| ID | Calculation | Formula | Authority |
|---|---|---|---|
| SCP-C1 | Next local draft revision | `result_draft_revision = expected_draft_revision + 1` | [AD-005](architecture.md#ad-005) |

### State Transition

**Normative first-match precedence:** evaluate missing required content/origins (`SCP-R1/R2`),
forbidden lifecycle (`SCP-R4`), CAS (`SCP-R5`), unknown schema, malformed patch, unsupported target
kind (`SCP-R6` subchecks in that order), then source-state eligibility. Only when every gate passes
may persistence run; persistence failure precedes success. `protocol-error` is consumer-side only
and never competes with producer failures. `SCP-R3` is a non-fallible boundary invariant:
the operation has no authoritative dependency or write capability, and every matrix row enforces
`authoritative_effects=∅`.

| From | Condition | `result.code` | To | Retry class | Input retained | Stored revision effect | Safe next action |
|---|---|---|---|---|---|---|---|
| `clean` with absent proposal | SCP-R1..6 pass and `expected=0` | `draft-saved` | `draft-saved` | terminal | no | atomic create at `1` | Inspect or validate |
| `draft-dirty`, `draft-saved`, `valid`, `invalid`, `save-failed` | SCP-R1..6 pass and CAS matches | `draft-saved` | `draft-saved` | terminal | no | atomic replace at `expected+1` | Inspect or validate |
| any allowed source | SCP-R1 or SCP-R2 fails | `invalid-draft` | unchanged | terminal | no | unchanged | Correct required content/origins |
| any allowed source | SCP-R4 fails | `forbidden-draft-state` | unchanged | terminal | no | unchanged | Return to Phase 1 lifecycle |
| any allowed source | SCP-R5 fails | `draft-conflict` | unchanged | retryable | yes | unchanged | Refresh base/revision and review retained input |
| any allowed source | unknown schema | `invalid-draft-schema` | unchanged | terminal | no | unchanged | Use supported schema |
| any allowed source | malformed patch | `invalid-draft-patch` | unchanged | terminal | no | unchanged | Correct patch |
| any allowed source | unsupported target kind | `unsupported-target-kind` | unchanged | terminal | no | unchanged | Choose supported target |
| `validating` or any undeclared source | save requested | `draft-state-ineligible` | unchanged | terminal | no | unchanged | Wait or return to editable state |
| any allowed source | Atomic persistence fails before commit | `save-failed` | `save-failed` | retryable | yes | unchanged; no partial write | Retry exact retained input |
| any | Store/consumer receives an undeclared code | `protocol-error` | unchanged | terminal | no | unchanged | Stop and report contract mismatch |

All rows have `authoritative_effects=∅`. The closed code set is exactly
`{draft-saved, invalid-draft, forbidden-draft-state, draft-conflict, invalid-draft-schema,
invalid-draft-patch, unsupported-target-kind, draft-state-ineligible, save-failed,
protocol-error}`.

### Postconditions

| Postcondition | Authority |
|---|---|
| Success atomically writes the complete saved [ChangeProposal](discovery/control-center.md#changeproposal) once and returns the SCP-C1 revision. | [AD-005](architecture.md#ad-005) |
| The original base witness and explicit diff remain inspectable. | [ChangeProposal](discovery/control-center.md#changeproposal) |
| No capability, approval, idempotency key, authoritative event or receipt is created. | [Phase 1 decision](../../decisions/skill-control-center-phase-1-scope.md#decision) |

### Error States

Every non-success condition maps one-to-one to the State Transition matrix. Closed-code and
retention authority: [AD-006](architecture.md#ad-006), [AD-007](architecture.md#ad-007).

## ValidateChangeProposal

**Type:** Operation (local validation mutation)  
**Actor:** Draft owner  
**Triggers:** Explicit validation of one saved proposal revision

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `proposal_id` | string | yes | Saved proposal identity |
| `draft_revision` | non-negative integer | yes | Exact saved revision to validate |
| `validator_id` | string | yes | Named preview validator |
| `validator_version` | string | yes | Exact rule-set version |

### Rules

| ID | Rule | Formal | Authority |
|---|---|---|---|
| VCP-R1 | Validation targets the exact current saved revision. | `draft_revision = stored_revision && state=draft-saved` | [Draft boundary](SPEC.md#safe-preparation) |
| VCP-R2 | Validator identity and version are disclosed. | `validator_id != "" && validator_version != ""` | [SCD-09](discovery/control-center.md#7-configuration-authority-and-receipt-boundary) |
| VCP-R3 | Result is always non-authoritative. | `result.authoritative=false` | [SCC-R-011](SPEC.md#formal-rules-and-invariants) |
| VCP-R4 | Validation cannot call deferred routes. | `calls ∩ {approve, apply, retry, reconcile}=∅` | [Phase 1 guardrails](BACKLOG.md#phase-1-guardrails) |

### Calculations

None. The validator evaluates a versioned rule set and returns findings; it derives no independent
numeric domain value.

### State Transition

**Normative first-match precedence:** evaluate proposal absence (`draft-not-found`), revision
mismatch (`draft-conflict`), source-state eligibility (`validation-ineligible`), validator
identity/version (`invalid-validator`), then forbidden validator effects
(`forbidden-validation-effect`). After these request/authority-safety gates pass, emit
`validation-started` and enter `validating`; only then check validator availability, execute the
validator and attempt preview persistence. `validation-unavailable`, `validation-error`, and
`validation-save-failed` precede success. Only an atomic preview commit may select
`validation-valid` or `validation-invalid`. `protocol-error` is consumer-side only and never
competes with producer failures.

Transient boundary (not a `result.code` and therefore not a member of the closed result-code set):

| From | Event | To | Guard | Effect |
|---|---|---|---|---|
| `draft-saved` | `validation-started` | `validating` | Absence, revision, state, validator identity and forbidden-effect gates all pass | Bind proposal/revision/validator attempt; then evaluate availability and execution |

| From | Condition | `result.code` | To | Retry class | Input retained | Stored draft revision effect | Safe next action |
|---|---|---|---|---|---|---|---|
| any | Proposal absent | `draft-not-found` | unchanged | terminal | no | unchanged | Return to catalog/draft list |
| any | Revision differs | `draft-conflict` | unchanged | retryable | yes | unchanged | Refresh and validate retained request |
| any except `draft-saved` | State is ineligible | `validation-ineligible` | unchanged | terminal | no | unchanged | Save proposal first |
| any | VCP-R2 fails | `invalid-validator` | unchanged | terminal | no | unchanged | Select a known validator/version |
| any | VCP-R3 or VCP-R4 would fail | `forbidden-validation-effect` | unchanged | terminal | no | unchanged | Stop; use preview-only validator |
| `draft-saved -> validating` | Validator unavailable | `validation-unavailable` | `draft-saved` | retryable | yes | unchanged | Retry same validation |
| `draft-saved -> validating` | Validator execution error | `validation-error` | `draft-saved` | retryable | yes | unchanged | Retry after diagnostic |
| `draft-saved -> validating` | Atomic preview persistence fails before commit | `validation-save-failed` | `draft-saved` | retryable | yes | unchanged; no partial write | Retry exact validation request |
| `draft-saved -> validating` | Findings empty and preview commit succeeds | `validation-valid` | `valid` | terminal | no | unchanged | Review preview |
| `draft-saved -> validating` | Findings non-empty and preview commit succeeds | `validation-invalid` | `invalid` | terminal | no | unchanged | Edit proposal |
| any | Store/consumer receives an undeclared code | `protocol-error` | unchanged | terminal | no | unchanged | Stop and report contract mismatch |

All rows have `authoritative_effects=∅`. The closed code set is exactly
`{validation-valid, validation-invalid, draft-not-found, draft-conflict,
validation-ineligible, validation-unavailable, validation-error, invalid-validator,
forbidden-validation-effect, validation-save-failed, protocol-error}`.

### Postconditions

| Postcondition | Authority |
|---|---|
| Result atomically stores a complete preview bound to proposal ID, unchanged draft revision, validator identity/version and all findings. | [SCD-09](discovery/control-center.md#7-configuration-authority-and-receipt-boundary) |
| `valid` means only that the proposal passed the preview rule set. | [Phase 1 assumptions](../../decisions/skill-control-center-phase-1-scope.md#assumptions) |
| No authoritative revision, capability, approval or receipt changes. | [Phase 1 decision](../../decisions/skill-control-center-phase-1-scope.md#decision) |

### Error States

Every non-success condition maps one-to-one to the State Transition matrix. Closed-code and
retention authority: [AD-006](architecture.md#ad-006), [AD-007](architecture.md#ad-007).

## Operation Invariants

| ID | Invariant | Formal | Authority |
|---|---|---|---|
| OP-I1 | Phase 1 operations affect local stores only. | `∀op: write_set(op) ⊆ {local_preferences, local_drafts, local_validation_results}` | [Phase 1 decision](../../decisions/skill-control-center-phase-1-scope.md#decision) |
| OP-I2 | No operation can return `applied` or an accepted receipt. | `∀op: outcome(op) ∉ {applied, accepted-receipt}` | [Phase 1 guardrails](BACKLOG.md#phase-1-guardrails) |
| OP-I3 | A validation result cannot grant authority. | `validation.authoritative=false && validation.capability_grant=null` | [SCC-R-011](SPEC.md#formal-rules-and-invariants) |
| OP-I4 | Every retryable error retains recoverable local input. | `retryable(error) => input_retained=true && authoritative_effects=∅` | [AD-006](architecture.md#ad-006) |
