# Agent Dispatch Protocol — Design Notebook

> Status: working notes; not a ratified discovery, SPEC, recipe, or runtime contract.
>
> Started: 2026-07-25

## Purpose

Capture the evolving decisions for compiling a reusable protocol for each skill into a concrete,
deterministically executable multi-agent dispatch.

The intended chain is:

```text
Skill revision
  -> active Skill Execution Profile
  -> invocation parameters
  -> compiled DispatchSpec
  -> deterministic scheduler + agent adapters + bus
  -> execution journal, receipts, and projections
```

This notebook may later be promoted into the pipeline-visible discovery under
[`agents-communication-infra`](../../features/agents-communication-infra/discovery/agents-communication-protocols/README.md).
Until that promotion, every decision below is provisional.

## Ownership boundary

This design belongs primarily to
[`agents-communication-infra`](../../features/agents-communication-infra/README.md), because that
feature owns the protocol that turns a confirmed dispatch into controlled execution, communication,
state transitions, and official results.

[`agent-provenance-telemetry`](../../features/agent-provenance-telemetry/README.md) is an
observational seam. It records or projects session/dispatch lineage, logical seats, activations,
messages, receipts, source observations, and tags. It must not decide the topology, anti-bias
policy, convergence rule, or next executable transition.

```text
Skill protocol and dispatch topology     agents-communication-infra
Execution and bus semantics              agents-communication-infra
Observed lineage, receipts, and tags     agent-provenance-telemetry
Human topology visualization             derived projection / control center
```

## Working model

### Reusable profile versus concrete dispatch

A `SkillExecutionProfile` is immutable and bound to the transitive digest of one skill revision.
It defines required work, allowed modules, invariants, parameter schemas, gates, and output
contracts. It does not select every concrete seat.

An invocation supplies or infers parameter values inside the profile's declared bounds. A compiler
expands the profile and parameters into a closed `DispatchSpec`. The dispatch contains no unresolved
structural choice when execution begins.

Changing a value inside the parameter schema creates a new `DispatchSpec`, not a new profile
revision. Adding a new semantic option, changing a bound, changing an invariant, or changing the
skill's transitive digest requires a new profile revision and confirmation.

### Three independent dimensions

Do not encode all multi-agent behavior in a single `anti_bias` flag or in agent count.

1. `coverage_policy` determines how the subject is divided into lenses, domains, sections, sources,
   or responsibilities.
2. `bias_control_policy` determines where and how bias is challenged.
3. `interaction_policy` determines when positions are sealed, revealed, discussed, revised, and
   aggregated.

They may be composed, but none implies the others.

## Provisional decision: anti-bias is not universally pairwise

The current workflow rule that every group with `n >= 2` must be pairwise tensioned is too strong
for a general skill protocol. It makes ordinary coverage fan-out difficult, treats useful
non-orthogonal lenses as invalid, and grows a pairwise proof obligation as the group grows.

The protocol should require an explicit bias-control policy, but should not require full pairwise
tension for every multi-seat group.

### Candidate policy vocabulary

```yaml
bias_control:
  mode: none | intra_agent | coverage_diversity | paired_tension | full_pairwise_tension
  evidence_policy: declared | source_manifest | sealed_judgment | adversarial_review
```

- `none`: allowed only when the profile explicitly permits no anti-bias control for that group.
- `intra_agent`: each agent must inspect contrasting sources, methods, hypotheses, or counterexamples.
- `coverage_diversity`: agents use different declared lenses or domains; they need not take opposing
  positions.
- `paired_tension`: each lens or work cell has two deliberately tensioned agents.
- `full_pairwise_tension`: every pair has a predicted disagreement or bias-cancellation relation.
  Reserve this for small groups whose purpose is adversarial judgment.

`intra_agent` improves source or reasoning diversity but is not evidence of independent judgment.
The runtime and UI must not present it as equivalent to independent agents.

`coverage_diversity` permits overlap. Exact duplicate work is also permissible when declared as a
replication policy, but must not be mistaken for broader coverage.

### Suggested defaults by group purpose

| Group purpose | Default bias control | Notes |
|---|---|---|
| Exploratory domain/lens coverage | `coverage_diversity` | Different lenses may overlap and need not conflict |
| Broad search by one agent | `intra_agent` | Require contrasting source classes or hypotheses |
| High-risk research lens | `paired_tension` | Two agents challenge one lens before cross-lens synthesis |
| Independent artifact review | `coverage_diversity` plus sealed first judgments | Attack lenses remain separate before reveal |
| Adversarial adjudication | `full_pairwise_tension` | Prefer small bounded groups |
| Deterministic implementation partition | `none` or `coverage_diversity` | Bias control may occur in a later review stage |

### Scalable research shapes

Small coverage-oriented run:

```text
Lens A: one explorer with intra-agent source diversity
Lens B: one explorer with intra-agent source diversity
Lens C: one explorer with intra-agent source diversity
  -> synthesis
  -> independent review
```

Larger tension-oriented run:

```text
Lens A: explorer A1 <-> challenger A2
Lens B: explorer B1 <-> challenger B2
Lens C: explorer C1 <-> challenger C2
  -> cross-lens synthesis
  -> fresh independent review
```

The larger shape applies tension locally inside each lens. It avoids requiring all six agents to be
pairwise orthogonal or adversarial.

## Topology parameters under discussion

### Group cardinality

The profile may expose bounded seat counts per logical group:

```yaml
groups:
  explorers:
    replicas: {default: 3, min: 1, max: 8}
    coverage_policy: lens_partition
    bias_control_modes:
      allowed: [intra_agent, coverage_diversity, paired_tension]
      default: coverage_diversity
```

Increasing cardinality does not automatically require a new profile revision. Compilation must
still resolve each seat's work descriptor, lens, source policy, and output contract. Repeated work
requires an explicit `replication_policy`.

### Review stacks

A protocol may expose a bounded, repeatable `review_stack`. Each layer creates fresh reviewers
unless the profile explicitly selects persistent identity.

```yaml
review_stack:
  min_layers: 1
  max_layers: 4
  default_layers: 2
  layer_template:
    reviewers: {default: 3, min: 1, max: 5}
    activation_identity: fresh_per_layer
    first_judgment: sealed
```

A layer, deliberation round, rework round, and technical retry are distinct counters.

### Producer-reviewer cells

A producer may have a local reviewer before its contribution reaches group synthesis:

```text
producer draft
  -> sealed local review
  -> producer/reviewer deliberation
  -> revised contribution + unresolved residue
  -> group synthesis
```

Fresh global reviewers should inspect the synthesis. Local reviewers must not silently become the
final independent review group.

### Deliberation and rework

`robot-talks` and `zig-zag` should share a lower-level `DeliberationRound` primitive without
becoming the same semantic operation:

- Robot-talks is an intra-group investigation/deliberation recipe.
- Zig-zag is bounded alternation or rework between groups, stages, or roles.
- `DeliberationRound` owns sealed initial positions, authorized reveal, exchange, revised
  positions, dissent preservation, and convergence evaluation.

Candidate shape:

```yaml
deliberation:
  initial_positions: sealed
  reveal: after_barrier
  exchange: authorized_all_to_all
  revision_rounds: 1

rework:
  mode: producer_reviewer
  max_rounds: 3
  stop_when: no_blocking_dissent
```

`robot_talks: true` and `zig_zag: true` are too coarse as final protocol fields.

## Convergence and progression

"Consensus" must compile to a typed predicate. Candidate predicates include:

- `unanimous_accept`;
- `no_blocking_dissent`;
- `no_dissent_at_or_above(severity)`;
- `all_obligations_satisfied`;
- `adjudicator_accepts_with_residue`.

Every review layer needs separate rules for:

```yaml
layer:
  rework_when: blocking_dissent_exists
  advance_when: no_blocking_dissent

pipeline:
  terminate_when: required_layers_passed
  early_stop:
    enabled: true
    minimum_layers: 2
```

Reaching a loop ceiling never implies approval. Residual dissent remains an immutable part of the
execution evidence.

## Parameter versus protocol revision

| Change | New DispatchSpec | New profile revision |
|---|---:|---:|
| Seat count within declared bounds | yes | no |
| Bias-control mode already allowed for the group | yes | no |
| Review-layer count within declared bounds | yes | no |
| Loop ceiling within declared bounds | yes | no |
| Stop predicate selected from the allowed vocabulary | yes | no |
| Enable an optional declared producer-reviewer cell | yes | no |
| Introduce a new bias-control or interaction mode | — | yes |
| Change the meaning of consensus or approval | — | yes |
| Remove mandatory sealed judgment or role separation | — | yes |
| Change the skill or a semantic transitive dependency | — | yes |

## Open design questions

1. Should `none` be a real bias-control mode or should absence always be expressed by a later
   mandatory review stage?
2. Which group purposes require independent model/provider diversity in addition to prompt/source
   diversity?
3. Should `paired_tension` pair seats statically in the profile or let the compiler create cells
   from declared lenses?
4. Which convergence predicates can the kernel evaluate mechanically, and which require an
   adjudicator contribution?
5. When early stopping is enabled, which review layers remain mandatory regardless of prior
   agreement?
6. Should the existing workflow-level universal P5 rule be replaced, scoped only to explicitly
   adversarial groups, or retained as a strict preset?

## Provisional decision log

| ID | Decision | Status |
|---|---|---|
| ADP-001 | Persist one active immutable execution profile per transitive skill revision. | provisional |
| ADP-002 | Compile invocation parameters into a closed, immutable `DispatchSpec`. | provisional |
| ADP-003 | Separate coverage, bias control, and interaction policies. | provisional |
| ADP-004 | Do not require full pairwise tension for every group with `n >= 2`. | provisional |
| ADP-005 | Support intra-agent, coverage-diverse, paired-tension, and full-pairwise anti-bias modes. | provisional |
| ADP-006 | Treat provenance telemetry as an observational projection, not execution authority. | provisional |
| ADP-007 | Share a lower-level deliberation primitive while keeping robot-talks and zig-zag semantically distinct. | provisional |
| ADP-008 | Evaluate Light, Medium, and Hard as possible reusable execution variants without assuming their final representation. | under discussion |
| ADP-009 | Require one standardized machine-readable projection while keeping its exact format undecided. | under discussion |

## Initial experiment context

- [`skill-protocol-compilation initial definitions`](../../features/agents-communication-infra/experiments/skill-protocol-compilation/experiment-initial-definitions.md)
  records the product meaning, confirmed constraints, evidence baseline, and known gaps. No schema,
  compiler, registry, fixture, or experiment result exists yet.
