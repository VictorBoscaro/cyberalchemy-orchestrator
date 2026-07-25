---
tags: [agents, architecture, invariants, modularity, mathematics]
node_type: candidate-invariant-set
is_session: false
status: proposed
version: 0.2.0
last_updated: 2026-07-24
parent_plan: plans/agent-language-research-program/PLAN.md
authority: research-input-only
---

# Candidate System Invariants

These are candidates for the finite global law set owned by the agent language and its
infrastructure. They are not ratified requirements. One released kernel version should expose an
explicit, countable set of system invariants; changing that set is a versioned kernel change.

Systems created by users on top of the kernel may define and evolve additional invariants without
changing the kernel invariant count. Research should try to remove, split, derive, or falsify the
candidate kernel invariants before ratifying the first set.

## What “invariant” means here

For a system state \(s\), an invariant is a predicate \(P(s)\) preserved by every valid transition
\(t\):

\[
P(s) \land valid(t, s) \Rightarrow P(t(s)).
\]

For modular composition, preservation matters as much as truth in isolated modules. If \(A\) and
\(B\) are valid modules, their composition must preserve the kernel laws:

\[
K(A) \land K(B) \land compatible(A,B) \Rightarrow K(A \otimes B).
\]

This does not mean every value stays unchanged. Identities, classifications, relationships, and
state may evolve; the laws governing how they evolve remain preserved.

## Two invariant levels

Let \(I_K(v)\) be the kernel invariant set for system version \(v\), and let \(I_U(c)\) be the
additional invariant set selected by one user configuration \(c\):

\[
I_{effective}(v,c) = I_K(v) \cup I_U(c).
\]

For a fixed kernel version, \(|I_K(v)|\) is fixed and inspectable. The user may easily change
\(|I_U(c)|\) by adding, disabling, scoping, composing, or retiring user-level invariants.

A user invariant may constrain the permitted state space further, but it cannot make a state valid
when a kernel invariant rejects it:

\[
Valid(s,v,c) \Rightarrow
\bigwedge_{i \in I_K(v)} i(s)
\land
\bigwedge_{j \in I_U(c)} j(s).
\]

This requires a governed invariant mechanism with at least identity, version, scope, applicability,
evaluation semantics, dependencies, enforcement or advisory mode, violation behavior, provenance,
and lifecycle. Those fields are a research target, not a settled schema.

## Candidate minimal kernel

### K1 — Explicit, non-self-created authority

Every consequential command, effect, visibility grant, promotion, or mutation executes under an
identifiable authority. Content cannot assert its own authority, and automation cannot acquire more
authority than was delegated to its definition or run.

This permits manual, scheduled, conditional, and event-originated work without making the trigger
itself an authorization.

### K2 — Durable causality and provenance

Every accepted fact or effect is traceable to its cause, responsible actor or mechanism, effective
configuration, and evidence. Acceptance is recorded before acknowledgement; correction adds a new
fact or explicit supersession rather than silently rewriting accepted history.

### K3 — Progressive definition with honest partiality

A governable thing needs only a stable identity, provenance, and the minimum properties required
for its current operation. It need not declare every class, category, role, or future use at
creation time.

Unknown, absent, unavailable, redacted, empty, false, and zero remain distinguishable. Later
classification enriches knowledge; it does not pretend that the classification was always known.

### K4 — Resolved contracts at effect boundaries

Partial definition is allowed while describing or exploring. Before a consequential effect, the
system resolves and records the effective contract needed for that effect: applicable definitions,
parameters, defaults, policies, capabilities, versions, and their origins. Missing required
semantics fail closed or escalate; they are not guessed invisibly.

### K5 — One owner for each authoritative fact; derived views stay derived

Each kind of authoritative fact has one declared owner and validated write boundary. Indexes,
dashboards, telemetry, recommendations, summaries, and other projections may be rebuilt and may
lag, but cannot silently become execution or truth authority.

### K6 — Replayable, idempotent, and honestly observable transitions

Accepted history determines reconstructible state without re-running external effects. Identical
retries do not create duplicate logical results; conflicting retries remain conflicts. Partial,
late, failed, unknown, and dissenting outcomes remain visible rather than being normalized into
success.

### K7 — Governed extensions and user invariants preserve the kernel

New event types, actions, agent constructs, categories, relationships, schedules, tools, and
modules may add local semantics and user-configured invariants without changing the meaning of
already accepted kernel facts. Every extension must map its effects, authority, provenance, and
observability into the common boundaries. A user invariant may strengthen or specialize valid
behavior within its scope; weakening a kernel invariant requires an explicit versioned kernel
change.

## Deliberately not global invariants yet

The following may become policies, profiles, local contracts, or derived consequences rather than
kernel invariants:

- Interviewer is a mode, capability, skill, or agent type.
- Scout is one particular ontological kind.
- Every task always uses exactly two agents.
- Every object is fully typed at creation.
- Every operation is event-triggered.
- Every artifact lives in Git.
- Every decision requires a human.
- Every workflow uses the same review topology.
- Every user system has the same number of user-defined invariants.

Keeping these outside the kernel preserves freedom to discover better classifications and
compositions.

## Minimality tests

For each candidate invariant, research should ask:

1. **Necessity:** what concrete system failure becomes possible if it is removed?
2. **Independence:** is it derivable from the remaining invariants?
3. **Locality:** can a module enforce it locally, or does it couple unrelated modules globally?
4. **Compositionality:** if two valid modules compose, what proves the invariant survives?
5. **Extensibility:** does it constrain safety and meaning, or merely freeze today's taxonomy?
6. **Observability:** what evidence demonstrates that the invariant held for one execution?

The target is not the smallest count at any cost. It is the smallest independent set of global laws
whose preservation lets modules vary safely.
