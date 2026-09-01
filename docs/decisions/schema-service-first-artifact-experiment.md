---
status: accepted
date: 2026-08-25
scope: schema-service-first-artifact-experiment
---

# Schema Service First Artifact Experiment

## Decision

Start the Schema Service artifact-model experiments with the `skill` family rather than the
previously planned `analysis` family.

This decision changes the experiment order; it does not yet approve a complete skill schema,
criterion, fixture set, resolver, registry, or runtime. The first subsequent design task is to
determine what the skill schema should express and to bound the smallest useful skill experiment.

The existing `analysis` package remains evidence and deferred experimental material. It is not
rejected or promoted.

## Options considered

1. Keep `analysis` first to isolate identity, revision, content change, and reclassification in a
   comparatively simple document family.
2. Start with `skill`, using an operational artifact family to expose definition, representation,
   installation, invocation, receipt, and lifecycle boundaries.

## Rationale

The `analysis` experiment depends on subtype distinctions that are not yet demonstrated by a
corpus and may test an uncertain epistemic taxonomy more than the Schema Service kernel. A skill
has stronger repository-local operational precedents and can make the kernel's distinctions
concrete while the schema is designed from witnessed roles.

Starting with `skill` does not justify modeling the entire compound graph at once. Scope, fixtures,
criterion, identities, and the exact set of required roles remain subject to explicit design and
review.

## Source of decision

The repository owner explicitly selected `skill` as the first family on 2026-08-25, after comparing
it with the existing `analysis`-first rationale.

## Remaining blockers and deferred decisions

- Decide the smallest skill lifecycle slice that can test the kernel without implying a universal
  runtime.
- Design the candidate skill schema, including its objective, identities, properties, relations,
  and acquisition modes.
- Reorder and repair the governing experimentation plan before any criterion, fixture, or run is
  created.
- Preserve the still-applicable review findings about per-candidate lifecycle and revision
  immutability; reassess base resolution and successor gates under the new order.

## Next step

Define the semantic subject of the skill schema and distinguish it from source package, release,
installation, tool invocation, and receipt before selecting fields.
