# Retrospective dispatch backfill staging

Status: **COMPLETE STAGING / NOT YET AUTHORIZED TO APPEND**

This directory is staging only. The appender is used only with `--validate-only`; neither repository ledger is modified.

## Audited scope

- 49 missing logical dispatches were audited: 14 for `cyberalchemy-orchestrator` and 35 for `domainspec-lean-formalization`.
- The Cyberalchemy set contains 11 direct executions and 3 formally opened attempts closed with `error`.
- The Lean set contains 35 direct executions.
- Expected complete backfill: 49 opening records plus 49 close records.
- Currently staged: 49 opening records plus 49 close records: 14 pairs under `cyber/` and 35 pairs under `lean/`.
- `source-rollout-map.json` records the 323 direct seats and their source rollout/hash evidence.

## What is staged

The following formal attempts are recoverable from their preserved `opening.json` and `close.json` evidence and are staged as canonical schema `0.6.3` records:

- `2026-08-10-craft-root-ledger-review`
- `2026-08-10-dispatch-defects-backlog-review`
- `2026-08-10-review-next-path-reconciliation`

For these records, the staged opening and close JSON files are byte-for-byte copies of their preserved workflow `opening.json` and `close.json` sources. This includes the original `context`, `anti_bias_mode: "disabled"`, declared token budgets, close counts, and `feedback_prompts`. Retrospective explanations are confined to this manifest; no rollout is attributed to these formal attempts.

### Contract drift

The installed `register-dispatch/SKILL.md` omits `anti_bias_mode` from its documented top-level field table, while the installed `append-dispatch.cjs` requires `anti_bias_mode` and accepts only `enabled | disabled`. The staging follows the executable validator because it is the enforcing implementation. The Cyberalchemy registry remains the sole source for ledger schema version `0.6.3` and live dispatch-type values; the executable supplies the field-level validation that the registry does not enumerate.

### External Lean append blocker

The target repository `C:\Users\victo\domainspec-lean-formalization` does not contain `implementations/contracts/dispatch-type-registry.v1.json`. Consequently, the Lean staging records were schema-validated through the Cyberalchemy registry and appender, but they must **not** be appended to the Lean ledger until the canonical registry has been distributed there through the governed infrastructure path and the records pass that target-local validator. This is an external deployment/governance blocker, not evidence that the staged Lean JSON is invalid under the present Cyberalchemy schema.

## Compatibility treatment for the 46 direct executions

The direct rollouts prove task names, parent/child paths, timestamps, working directories, effective models, agent nicknames, launch order, completion/failure state, and in many cases durable artifacts. They do **not** expose the full briefing required by `groups[].agents[].initial_prompt`:

- the parent rollout stores `spawn_agent.arguments.message` as a Fernet-like `gAAAAA...` ciphertext;
- the child rollout stores only the plaintext `Message Type: NEW_TASK` envelope header and an `encrypted_content` payload;
- no plaintext projection was found in repository telemetry, workflow inputs, `state_5.sqlite`, or `logs_2.sqlite`;
- research `dispatch.yaml` files sometimes contain short task descriptions, but those are not evidence that the text equals the full briefing actually delivered.

The current `register-dispatch` contract defines `initial_prompt` as the full briefing the agent received. The original plaintext is unrecoverable, so the 46 direct openings deliberately do **not** claim prompt fidelity. Under explicit staging authorization, each seat instead carries an unmistakable retrospective compatibility marker with its observed `agent_path`, source-rollout path, rollout SHA-256, and encrypted-payload SHA-256. This is a known semantic divergence from the ordinary `initial_prompt` contract and requires explicit human acceptance before append.

Every direct seat uses numeric token budget `4000`, and every direct opening context states that this is a **compatibility envelope value, not observed execution budget**. Every direct opening also declares `anti_bias_mode: "disabled"` as a retrospective compatibility value; it was not observed in the direct runtime. Direct openings use `agent_name: null` because rollout nicknames are not exact canonical pool names. Their `final_approver` is therefore `parent`. Agent roles are compatibility classifications inferred from observed task names, not values preserved in rollout `agent_role` metadata (which was generally null). Sequential connections encode observed launch order only and do not claim governed dependencies or ACI bindings.

### Cyberalchemy direct compatibility records (11)

- `2026-08-09-permguard-pep-integration-review`
- `2026-08-10-core-update-precedent-triad`
- `2026-08-10-yoneda-selmer-crossrepo-scout`
- `2026-08-10-superinterviewer-authority-foundation`
- `2026-08-10-superinterviewer-bootstrap-program`
- `2026-08-10-superinterviewer-repository-routing`
- `2026-08-10-superinterviewer-foundation-v01`
- `2026-08-11-minimal-knowledge-kernel-direct-review`
- `2026-08-11-entre-sistemas-v02-production`
- `2026-08-11-entre-sistemas-v02-review`
- `2026-08-11-predictive-epistemic-grammar-research`

### Lean direct compatibility records (35)

- `2026-08-09-category-theory-craft-proofs-v3-review-repair`
- `2026-08-09-permguard-proof-carrying-boundaries`
- `2026-08-09-task-relative-property-role-reversal`
- `2026-08-09-multi-repository-commit-sweep`
- `2026-08-10-yoneda-selmer-framing`
- `2026-08-10-yoneda-selmer-review-r1`
- `2026-08-10-yoneda-selmer-review-r2`
- `2026-08-10-analogy-lineage-fit-audit`
- `2026-08-10-ownership-comparator-map`
- `2026-08-10-yoneda-selmer-precedent-triad`
- `2026-08-10-fundamental-ideas-repo-map`
- `2026-08-10-minimalism-composition-initial-wave`
- `2026-08-10-minimalism-composition-research`
- `2026-08-10-minimalism-composition-review`
- `2026-08-10-minimalism-composition-spec-v1`
- `2026-08-11-minimalism-composition-spec-v2`
- `2026-08-11-minimalism-composition-spec-v3`
- `2026-08-11-minimalism-layered-assessment`
- `2026-08-10-analogy-relevance-scout`
- `2026-08-10-analogy-architecture-witness`
- `2026-08-10-coextension-architecture-witness`
- `2026-08-11-object-partial-functor-initial-definitions`
- `2026-08-11-constraint-generativity-resistance`
- `2026-08-11-generativity-profile-admissibility`
- `2026-08-11-epistemic-test-design`
- `2026-08-11-formal-stress-review`
- `2026-08-11-observed-revision-build`
- `2026-08-11-observed-revision-review`
- `2026-08-11-prefunctor-composition-failure`
- `2026-08-11-coextendability-chain-failure`
- `2026-08-11-finite-local-global-gap`
- `2026-08-11-knowledge-loop-underdetermination`
- `2026-08-11-final-lean-hygiene`
- `2026-08-11-final-post-fix-claim-review`
- `2026-08-11-reflection-tower-reconciliation`

## Exclusions confirmed by the audit

- two draft-only envelopes: `2026-08-10-terminal-output-spec-review` and `2026-08-10-assess-work-progress-skill-review`;
- orphaned formal intent `2026-08-11-review-minimal-knowledge-kernel`, superseded by the direct fallback `2026-08-11-minimal-knowledge-kernel-direct-review`;
- semantic duplicate `2026-08-11-partial-functor-disclosure-gate`, already represented in the Lean ledger as `2026-08-11-partialfunctorextension-disclosure-gate`;
- Robot-Talks sessions and bounded helpers, including PDF reference helpers and the present ledger/UI auditors.

## Validation gate

The staged corpus currently passes deterministic checks for:

- 49 unique opening IDs and 49 exactly paired close IDs;
- repository split of 14 Cyberalchemy and 35 Lean pairs;
- 323 direct seats and 323 matching source-rollout SHA-256 values;
- UTF-8 and JSON parsing;
- canonical schema-shape constraints, review output contracts, research working folders, group/connection references, and close totals;
- absence of all 49 IDs from both current ledgers.

All 98 opening/close records pass independently through the Cyberalchemy appender's non-mutating `--validate-only` mode (`98/98`, zero failures). This loads the Cyberalchemy registry for schema version and type authority but returns before reading or writing a ledger.

Before any append, require all of the following:

1. explicit human acceptance of the exact 49-ID set;
2. explicit human acceptance of `4000` as a compatibility envelope value, not an observed execution budget, for direct records;
3. explicit acceptance that the retrospective markers are evidence references rather than the original full prompts;
4. explicit acceptance that direct `anti_bias_mode: "disabled"` is a compatibility value, not an observed runtime declaration;
5. 49 opening and 49 close JSON files with unique IDs across both staging subdirectories;
6. UTF-8 and JSON parsing checks;
7. canonical schema validation against `ledger_schema_version: 0.6.3`;
8. semantic duplicate check against both current ledgers;
9. governed distribution of the canonical dispatch-type registry to the Lean target, followed by target-local validation of all 35 Lean pairs;
10. append only through each target repository's canonical appender, after the gate.
