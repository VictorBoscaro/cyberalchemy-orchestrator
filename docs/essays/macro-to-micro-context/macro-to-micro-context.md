---
tags: [agents, context, objectives, work-lineage, hierarchy]
node_type: essay
status: draft
version: 0.1.0
last_updated: 2026-07-25
authority: proposal-only
---

# Linking the Macro to the Micro

I want to link the macro to the micro.

If we can do that well, we already have something valuable.

Every task exists inside a broader context. A task can be part of a sprint. The sprint can be part
of a feature. The feature can be part of a project. The project can be part of an application. The
application can serve an objective of a company.

```text
company objective
→ application
→ project
→ feature
→ sprint
→ task
→ attempt
→ file change
```

The work happens at the bottom. Its reason exists above it.

This is close to the idea I take from Clausewitz. A military operation only makes sense in relation
to the political objective it serves. A local victory can be useless, or even harmful, when it is
disconnected from the larger objective.

The same thing happens in software and agent work.

An agent can complete a task correctly. The code can pass its tests. The task can still be the
wrong task. It can support the wrong feature, preserve an assumption that has already changed, or
optimize something that no longer matters to the project.

The problem is not only execution quality. It is the loss of context between levels.

## A task belongs to more than one context

The chain above is useful, but it is not one fixed hierarchy.

A task can be part of a sprint, implement a spec, change a feature, answer a discovery, consume a
research result, and be authorized by a user decision.

```text
Task-T
├── part-of Sprint-S
├── implements Spec-V3
├── changes Feature-F
├── answers Discovery-D
├── uses Research-R
└── authorized-by Decision-A
```

These connections mean different things. They should not be reduced to one `parent_id`.

They also should not be derived only from folders. A file has one physical path. The work it
represents can participate in several contexts at the same time.

I may want to see the repository by feature. Later I may want to see it by Plan, by sprint, by type
of work, or by unresolved objective. Those are different views over the same objects.

The main object is not the folder. The main object is the thing being worked on and its connections
to the rest of the system.

## Going up and going down

From any micro task, I should be able to move upward:

```text
Why does this task exist?
Which sprint does it belong to?
Which feature does it change?
Which project objective does that feature serve?
Which user decision authorized the work?
```

From any macro objective, I should be able to move downward:

```text
Which projects serve this objective?
Which features are active?
Which tasks are being executed?
Which ones are blocked?
Which code and artifacts changed?
What evidence says the objective is being advanced?
```

This gives us two different checks.

The upward path checks purpose and authority. The downward path checks realization.

If a task has no upward path, it may be orphan work.

If an objective has no downward path, it may be only a statement with nothing implementing it.

## User decisions are part of this context

Approvals and rejections need to be saved.

If the user approves a Dispatch, that decision should be linked to the Dispatch. If the user
approves a Discovery, Plan, Research program, or another object, the decision should be linked to
that object.

A rejection is also information. It explains why some work did not happen. It may expose a boundary
that should apply to later proposals.

The decision should not disappear inside the chat.

The user may also authorize a larger workflow:

> Continue this research, review, and implementation workflow without asking me before every task.

That approval is different from approving one Dispatch. It sits at a higher level.

The later Dispatches should connect to it:

```text
User decision
→ authorized workflow
→ generated Dispatch
→ Agent Attempt
→ effect
```

The broad approval is not unlimited. It applies to the objective, scope, kinds of work, limits, and
conditions that the user approved. If the workflow moves outside those boundaries, the connection
breaks and the system needs another decision.

This is another reason to preserve the macro-to-micro path. The system needs to know not only that
an approval exists, but whether the current micro action is still inside it.

## The representation will change

The first representation will not remain correct forever.

A feature can move to another project. A sprint can be reorganized. A discovery can show that the
original objective was wrong. A task can end up changing more than expected. A user can revoke an
approval or replace it with another decision.

The system cannot preserve context by freezing it.

It has to preserve context by recording how it changes.

```text
Feature-F was part of Project-A
Feature-F is now part of Project-B
Decision-D1 authorized the original route
Decision-D2 replaced that route
Task-T was created under D1
Task-U was created under D2
```

The old representation remains part of the history. The current representation can still be
derived.

This is probably where hooks become useful. A hook can detect that code changed, that a task lost
its Spec link, that a feature moved without its research, or that a Dispatch no longer fits the
decision that was supposed to authorize it.

The hook is not the context. It is one mechanism for maintaining the context.

## What the infrastructure needs to preserve

At the smallest level, the system needs:

- things with stable identities;
- typed connections between those things;
- the context in which a connection was accepted;
- the person, agent, or mechanism responsible;
- the history of changes to those connections;
- the decisions that permit, reject, or change work;
- a way to detect when the represented context no longer matches what is happening.

This does not require us to know every type of object in advance.

We can create something before we know whether it is Research, Discovery, a Plan, or another kind
of artifact. We can give it an identity, preserve its origin, attach candidate classifications,
and refine them later.

The same applies to the hierarchy. We do not need one universal structure. We need relations that
say what kind of connection exists and what that connection is allowed to mean.

## Why this may be enough for the first system

If we can preserve the path between macro objectives and micro work, many other things become
possible.

We can organize the same project by feature, Plan, sprint, agent, artifact type, or objective.

We can detect work that no longer serves a live objective.

We can show which user decision authorized an effect.

We can see specs without implementations and implementations that drifted from their specs.

We can create hooks that react to changes in context.

We can ask whether two rules about hierarchy, authority, or workflow contradict each other.

We can give an agent only the part of the broader context it needs without losing the path back to
the whole.

Kernels, a kernel of kernels, SMT solvers, and Lean may become useful later. They would help define
and check which properties must survive when contexts, rules, and representations are combined.

But they are not the starting point.

The starting point is simpler:

> Every piece of work should remain connected to the larger context that gives it purpose.

The first challenge is representing that connection.

The second is keeping it faithful while the work changes.

## Open questions

- Which levels of context are useful in practice, and which are only temporary views?
- Can one object belong to several projects, features, or Plans without creating ambiguous
  authority?
- Which relations should be direct facts, and which can be derived?
- What makes an upward path sufficient to justify a task?
- What evidence shows that micro work actually advanced the macro objective?
- When does a change invalidate an earlier approval?
- How much context should a leaf agent receive, and how much should remain available only through
  lineage?
- How do we measure whether maintaining this structure saves more effort than it creates?
