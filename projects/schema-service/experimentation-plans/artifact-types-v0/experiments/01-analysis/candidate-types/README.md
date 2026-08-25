# Candidate types

These files are experiment-local inputs. Their location provides custody and discoverability only;
it does not publish them or make them valid normative schemas.

## Reference form

A later fixture that opts into experimental resolution must use this shape:

```yaml
experimental_schema_ref:
  experiment_ref: exp-schema-analysis-001
  candidate_revision_id: candidate:exp-schema-analysis-001:schema:analysis-observed-phenomenon@0
  definition_digest: sha256:37c87ec5f3a225eb1c93f666b7124f4b240628f04b6d88deb183fcdb8090bbd4
```

It must not put that value in `schema`. That field remains reserved for a revision-exact schema
published by an authorized registry operation.

## Resolution contract

An experimental resolver must receive all three reference values plus the declared candidate root
from [`experiment-manifest.yaml`](../experiment-manifest.yaml). It then:

1. verifies that the manifest and catalog carry the same `experiment_ref`;
2. requires manifest mode `experimental_only` and catalog state `active`;
3. locates the exact `candidate_revision_id` only in this catalog;
4. verifies the referenced file digest before reading its definition;
5. resolves candidate dependencies only inside this same experiment and published dependencies
   through a separately authorized normative resolver;
6. marks every derived report with the experimental reference and validator identity.

Missing scope, ambiguous identity, digest mismatch, terminal lifecycle state or unavailable base
must fail closed. There is no lookup by proposed type label, directory scan, "latest" revision or
fallback from experimental to normative mode.

A normative-only resolver must reject `experimental_schema_ref` without consulting this directory.

## Identity and lifecycle

- `candidate_type_id` identifies the experiment-local candidate distinction.
- `candidate_revision_id` identifies one immutable candidate definition revision.
- `proposed_type_id` is a publication proposal and is not resolvable.
- A future published `SchemaId` would be a fourth, authorized identity linked through a promotion
  record; it cannot replace any of the identifiers above retroactively.

Only `active` candidates may serve new runs. `superseded`, `abandoned` and `promoted` candidates are
retained for exact replay and provenance. A changed definition receives a new
`candidate_revision_id` and digest; it is never edited in place after use by a frozen run.

## Promotion boundary

This package cannot promote a candidate. A later authorized publication must collision-check the
proposed type, publish an immutable normative revision and preserve a mapping containing at least:

```text
experiment_ref
candidate_type_id
candidate_revision_id
definition_digest
publishing_authority_ref
published_schema_id
```

Promotion does not change prior fixture references, reports or manifest revisions.
