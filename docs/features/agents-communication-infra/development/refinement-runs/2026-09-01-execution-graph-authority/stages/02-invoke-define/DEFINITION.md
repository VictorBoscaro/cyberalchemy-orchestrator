# ExecutionGraph v2 definition

## Need

The user should be able to state an intent such as “review what was done” without authoring a
technical dispatch. The agent must compile a complete proposal, show it at the requested depth and
obtain authority to execute exactly that proposal—no more and no less.

## Defined thing

`ExecutionGraph v2` is one closed, immutable, canonical JSON document that carries all
pre-execution authority for a dispatch. It is both:

- the runtime input contract after confirmation; and
- the source from which topology, basic and full confirmation views are computed.

It is not a run record, confirmation observation, receipt bundle or mutable execution state.

## Actors and ownership

| Actor | Owns | Does not own |
|---|---|---|
| User | intent, choice of presentation depth, explicit confirmation/rejection | Manual entry of provider, sandbox, prompt or graph fields |
| Compiler agent | complete graph proposal and explanation of assumptions | Authority to execute before confirmation |
| Capability resolver | exact available provider/model/tool identities used in the proposal | Silent substitution after confirmation |
| Trusted confirmation adapter | principal/channel/time evidence bound to graph revision/digest | Editing graph content |
| Runtime | validation, acceptance, derived IDs, attempts, receipts and results | Inventing missing executable values |

## Required semantic components

1. **Identity and intent:** graph ID/revision, user request, compiled objective and provenance.
2. **Topology:** ordered nodes, typed edges, dependencies, joins and allowed communication flow.
3. **Per-node work:** stable node/seat identity, role/name, exact task instructions, input/context
   selection, expected output and validation.
4. **Effective execution grant:** exact provider/model/profile, tools and capability restrictions.
5. **Resource and safety policy:** attempts, tokens/time, filesystem, network, commands, external
   effects and escalation rules.
6. **Lifecycle:** entry conditions, completion/stop conditions, failure behavior and aggregation.
7. **Canonicalization:** schema version, closed decoding, ordering rules, canonical bytes and digest.
8. **Presentation contract:** deterministic topology/basic/full projections with disclosure rules;
   every view names the same graph revision and full digest.

## Invariants

- There is exactly one pre-execution authority document per graph revision.
- No executable default may be added after confirmation.
- Resolved effective capabilities, not merely requirements, are confirmed.
- A reference that affects execution is immutable and digest-pinned; otherwise its bytes are
  embedded.
- Any mutation of an authority-bearing value changes canonical bytes/digest and requires a new
  confirmation observation.
- Presentation depth changes disclosure only; it never changes authority.
- Confirmation observation and runtime-derived state cite the graph digest and remain outside the
  graph document.
- Secrets are never embedded; the graph authorizes a secret handle/policy, and runtime resolves it
  without making the secret value part of the confirmed artifact.

## Candidate boundary decision

Keep the “one canonical JSON” decision, but state it precisely as **one complete pre-execution
authority document**, not “one JSON containing every fact in the dispatch lifecycle.” That
narrowing is required for the decision to be coherent: facts that do not exist until confirmation
or execution cannot truthfully be fields of the proposed graph.

## Success tests

1. Given one graph, topology/basic/full renders produce the same revision and digest.
2. Removing or mutating a prompt, context input, model, policy, budget, edge or stop rule is either
   invalid or yields a different digest.
3. A runtime can execute without selecting an unconfirmed executable default.
4. Principal/time/receipt/attempt/result fields are rejected as graph fields.
5. A review → correct → verify fixture can be confirmed and deterministically expanded into
   runtime-owned IDs without changing its logical authority.

## Current status

This is a refinement definition, not an accepted feature specification and not implementation
evidence.
