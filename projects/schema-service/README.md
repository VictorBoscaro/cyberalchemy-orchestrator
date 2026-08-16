# Schema Service

Status: bootstrap.

This README describes the intended boundary of Schema Service; it does not claim that the service
is implemented. The project will provide the minimum shared machinery needed to define, identify,
resolve, and validate schemas without knowing the semantics of folders, artifacts, code, or any
other governed subject.

## Why it matters

Different domains need a common way to operationalize schemas. Without one, each domain may invent
its own identifiers, definition format, resolution rules, validation behavior, and update mechanics.
This service is intended to supply that shared substrate while leaving domain rules to specialized
services.

A new governed subject does not require a new schema definition. It is represented by an instance
manifest that references a reusable schema. Whether a subject must be governed is decided by its
domain; this service does not automatically enroll every file or directory. A new schema is
justified only by evidence that existing contracts cannot represent or validate a materially
different kind of subject.

## Operational model

```text
instance manifest -> SchemaId -> immutable schema definition -> validator -> result
```

A schema revision is immutable. Evolution publishes a new revision rather than changing what an
existing identifier means. Reconciling an instance manifest after its subject changes is a separate
candidate capability, not part of schema-definition evolution.

## Candidate instance metadata

```yaml
schema: artifact/example@0
```

The resolvable schema reference is the only cross-domain field currently supported by the operating
model. `id` and `objective` are hypotheses for shared instance metadata; they must earn admission
through conformance cases showing that they cannot be derived or owned by a domain. Open `tags` are
an optional discovery surface and must not silently control behavior.

A condensed summary should initially be a derived projection of the governed subject and its
objective. Persisting or refreshing it becomes a service responsibility only when a concrete
consumer or freshness failure demonstrates that derivation on demand is insufficient.

## Boundary

The service will own schema definitions and their metaschema, `SchemaId`, registry and resolution,
validation, and publication of new immutable revisions. It does not define what makes a folder,
document, research result, or code unit valid.

These responsibilities may later become internal services or modules. They remain conceptual
boundaries during bootstrap and must not become subdirectories until implementation evidence shows
that separate ownership, lifecycle, or interfaces are necessary.
