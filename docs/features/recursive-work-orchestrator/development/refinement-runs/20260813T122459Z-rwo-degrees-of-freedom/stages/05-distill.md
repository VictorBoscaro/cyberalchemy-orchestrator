# Stage 05 — Distill

- Capability: `distill`
- Mode: `standard`
- Role path: three true read-only subagents
- Verdict: `pass with repaired unit`

## Selected smallest coherent unit

The **Authority Transition Slice (ATS)** is the smallest coherent research unit:

```text
authenticated initiator
+ pre-state and grant ancestry
+ requested operation, resource, and phase
+ policy/version and derivation rule
+ effective principal, tool, or adapter
+ topology, context, budget, time, retry, and depth bounds
+ enforcement points actually traversed
-> accepted or denied post-state and external effects
+ authorization, enforcement, denial/revocation, and effect receipts
```

An ATS studies one protected operation where authority is exercised, derived, transferred,
attenuated, issued, revoked, or used to change state or cause an effect. Pre/post authority may be
equal when an existing grant is exercised. A static
protected-action envelope is retained as the human-readable projection of one or more ATS records;
it is not the primary evidence unit.

## Why this is the optimization point

- A matrix row is too small: it misses token transfer, confused deputies, retries, fan-out,
  policy changes, and data promoted into control.
- One actor or subsystem is the wrong boundary: amplification crosses children, tools, adapters,
  context, and phases.
- A general IAM model is too large: the V1 decision needs conservation and delegation properties,
  not federation, account lifecycle, or a general policy language.
- ATS is large enough to carry causality and small enough to compare a closed set of freedoms.

## Closed transition classes

1. read, list, search, export, disclose, write, execute, publish, or cause a local/external effect;
2. semantically derive, delegate, attenuate, or transfer authority or scope;
3. issue, consume, revoke, renew, or expire the credential/token representing a grant;
4. create or mutate topology, including child work and dynamic graph artifacts;
5. mutate policy, tool profile, adapter registration, budget, or other authority-shaping config;
6. materialize, redact, declassify, or interpret context, secrets, credentials, tokens, privileged
   instructions, model/provider egress, or data that might become policy or executable control.

Each class is tested through five paths: direct; via child/seat; via tool/adapter/subprocess; via
retry, resume, fan-out, fan-in, or a separate run; and through concurrent/interleaved execution.

## Required properties

- **No amplification:** for qualitative dimensions, derived action/resource/phase/audience sets are
  subsets of their parent grant; expiry cannot extend; delegation, issuance, policy mutation, and
  scheduler-equivalent bits cannot appear without an exact authority-root decision receipt.
- **Conservation:** per quantitative dimension,
  `spent + reserved_live + reclaimable <= root_ceiling`; remaining depth decreases, deadlines do
  not extend, and concurrent allocation is accounted atomically. Incomparable or unknown bounds
  fail closed.
- **No implicit inheritance:** parentage, lineage, composition, output, context, or a tool call never
  transfers authority by itself.
- **No nominal escape:** leaf, skill, tool, adapter, or subprocess behavior is judged by its effect,
  not its label. Scheduler-equivalent means creating, authorizing, scheduling, or delegating
  executable work, or issuing grants outside the frozen root plan. Launcher, subprocess, tool, and
  adapter boundaries must mediate those effects.
- **Evidence specificity:** issuance, authorization, enforcement, delivery, effect, denial, and
  revocation receipts are different evidence types.
- **Trace composition:** multi-step and concurrent attacks emit an ordered or partially ordered ATS
  trace; invariants are checked after every transition and over the complete trace.

## Utility witnesses

The recomposed envelope must support:

1. parallel research with synthesis and review;
2. local code mutation in a confined workspace plus bounded tests and independent review;
3. proposal/draft production with a human gate and no simulated apply;
4. bounded diagnose–repair loops with exhaustion;
5. an external effect only when its adapter enforces the exact approved envelope and reconciles the
   actual effect; otherwise the workflow ends at draft.

## Attack suite

At minimum: self-issued capability; bearer lending; tool/subprocess laundering; nested scheduler
disguised as a leaf; circular authority reference; credential/context smuggling; aggregate fan-out
or retry amplification; topology artifact promoted to executable control; two-step policy/tool
escalation; collusive grants; retry/effect duplication; and receipt theater.

## Recomposition proof

ATS records group into five user-facing Freedom Slices:

- topology and delegation;
- execution resources: model, tools, context, filesystem, network, subprocess, secrets;
- external effects and adapters;
- quotas and continuity: budget, depth, time, retries, persistence, resume;
- authority administration: approve, issue, delegate, revoke, policy and break-glass.

Their projections recompose the actor × action × resource × phase matrix. Coverage requires every
seed freedom to map to at least one ATS, every matrix decision to trace back to ATS evidence, five
utility witnesses to remain possible, and the attack suite to fail closed or expose a named gap.

## Deferred complexity

Multi-tenant IAM, identity lifecycle, SSO/federation, general RBAC/ABAC language, token cryptography,
credential-broker design, admin UI, per-object user rules, implementation/optimization of transitive delegation,
runtime implementation, and guarantees for unbounded/dynamic distributed computation remain out.
The research must still define and test semantic attenuation across multi-hop delegation.

Transition classes are behavioral types; Freedom Slices are resource/presentation groupings. Each
ATS has exactly one primary transition class and one primary Freedom Slice, with optional secondary
tags recorded by the coverage ledger.

## Role reconciliation

- Modeler proposal: use a Freedom Slice containing full protected action envelopes — **revised**;
  retained as the projection/catalog layer.
- Skeptic objection: static envelopes miss transition and composition attacks — **accepted**; ATS
  becomes the primary unit and conservation becomes mandatory.
- Utility audit: universal read-only is safe but not a general orchestration V1 — **accepted**;
  confined local mutation and conditional adapter-mediated effects are required witnesses.
