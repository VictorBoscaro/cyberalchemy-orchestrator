# TASK-POLICY-000 - pure execution-policy contract oracle

## Status

- **State:** `READY_FOR_CODE_ENTRY`
- **SWU:** `SWU-ACI-EXECUTION-POLICY-ORACLE-000`
- **Reason:** the reviewed technical design and the complete normative DomainSpec L0 contract are
  independently reviewed and digest-pinned. This readiness authorizes only the three bounded
  implementation paths below; implementation has not started.

## Decision question

After this L0 unit, we know whether `ResourceBudget`, `SandboxPolicy` and the production/harness
`ExecutionAuthorityFence` domains can be decoded, canonically encoded, digested and rejected without
defaults or ambiguity.

## Frozen planning authority

- [TECH-POLICY-D0](../../development/invoke-runs/20260831-resumable-feedback/plan/TECH-POLICY-D0.md)
  at `sha256:522a8cac79335e6190fb4799cbea95c0f58621f4f9ea5f72add2437690b8130e`.
- [Independent TECH-D0 review](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/TECH-D0-REVIEW.md)
  at `sha256:43ba27747ccaa54d6a4cc49ed3102ea582423f19f1ad6a69f5de7d6e5f291179`,
  verdict `PASS` only for authoring this bounded work pack.
- [Domain model](../../specs/domain.md) at
  `sha256:986bb2db5e602ad81df576e04f84d49643c31769098c278ae936ada55eb2714d`.
- [Feature SPEC](../../specs/SPEC.md) at
  `sha256:37337699cf8313e13ed162ce495fdbeaa6aed8bd16fbc4f7c4aede59613bfd30`.
- [L0 TEST-SPEC](../../specs/TEST-SPEC.md) at
  `sha256:6bb27f65fe11c02c0b9f6ade6ad11b14b046a1c689b248e68c3902dcabdeeb51`.
- [Rules](../../specs/rules.md) at
  `sha256:8c0010dfe88026060127f80a4ee08ea10051f95bd288b9244d6f596e65c75047`.
- [Interfaces](../../specs/interfaces.md) at
  `sha256:c257dd59a1a895c8007d4fa4f041bab038086bb3d439bd9e5c3d0977d84f8cde`.
- [Architecture](../../specs/architecture.md) at
  `sha256:3ac37b4f1d85b28d0d6d48daa37fa82dc90d009d93c9e5f165c82b7a3363a510`.
- [Glossary](../../specs/glossary.md) at
  `sha256:9bfb5f4d27da40489209dfe273a48164f88ba195b110a20017db4eb9965d5816`.
- [Integrated DomainSpec review](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-000-DOMAINSPEC-REVIEW.md)
  at `sha256:71a4ac667b4aa55fc5487d36f8dddaa603899feebefb80c9c7dff356a931896c`,
  verdict `PASS` for this exact seven-document normative package.

## Bounded deliverable

One implementation task may add only:

- `implementations/server/runtime/execution_policy.py` - pure strict decoder, canonical encoder,
  qualified-digest and oracle validation logic;
- `implementations/tests/runtime/execution_policy_oracle_v1.json` - the seven exact synthetic
  bytes/digest vectors frozen by TECH-POLICY-D0, clearly marked non-executable;
- `implementations/tests/runtime/test_execution_policy.py` - the complete L0 positive and mutation
  corpus.

The implementation may reuse `runtime/canonical.py` and `runtime/errors.py` read-only. It must not
add persistence, migrations, aggregates, plans, requests, events, effects, service/API paths,
provider/launcher calls or executable authority.

## L0 proof obligations

- Reproduce all seven TECH-POLICY-D0 digests exactly.
- Reject missing, unknown, duplicate and wrong-typed fields recursively.
- Enforce exact signed-64 ranges: every `ResourceBudget` ceiling and `max_child_processes` accepts
  only `0..9223372036854775807`, while production and harness `cutover_epoch` accept only
  `1..9223372036854775807`; reject booleans, numeric strings, floats, negatives, overflow and
  coercion, while preserving explicit zero ceilings.
- Require an exact caller-supplied target-byte map keyed to every reference. Validate the known
  budget/enforcement target schemas and digests; verify every non-empty credential reference under
  its reference-owner contract with zero I/O and without inventing a universal credential schema.
- Enforce only the closed lexical sandbox grammar in L0: canonical relative `/` roots,
  `link_policy=deny`, and rejection of empty components, `.`, `..`, drives, UNC and wildcards.
  Physical symlink, junction/reparse-point and resolved-containment enforcement remains exclusively
  POLICY-003/L3 and outside this task.
- Validate `tool.none` compatibility, duplicate credential rejection and default-deny scopes.
- Reject every one-byte golden drift and every fence/preimage digest-domain substitution.
- Accept the harness fence only through the harness decoder and reject it through the production
  decoder before evidence resolution.
- Prove the combined oracle and all harness values authorize zero external action.

## Exact code-entry condition

The condition is satisfied only while every authority pin above still matches, the descriptor pins
this TASK digest and the fresh code-readiness receipt returns `PASS` for exactly the three bounded
write paths. Any digest or scope drift closes the gate before implementation.
