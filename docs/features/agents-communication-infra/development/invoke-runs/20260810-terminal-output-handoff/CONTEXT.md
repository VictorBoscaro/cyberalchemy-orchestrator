# Context — bounded terminal-output handoff

## Objective

Make a downstream seat launchable from an upstream seat's exact terminal response without asking an agent to copy that response into a repository file. The host runtime owns capture, persistence, attribution, materialization, and delivery.

## Accepted decisions

- D1: persist the exact host-observed terminal response as a content-addressed artifact; only that artifact may satisfy `binding-output`.
- D2: ratify the current Python + SQLite runtime as the implementation baseline.
- The existing connected-topology compiler fence remains until the downstream materializer is proven.

## Obligations

1. Bind bytes to the exact parent dispatch, producer group, seat, turn, and terminal state.
2. Persist bytes and SHA-256 before exposing an artifact receipt.
3. Materialize downstream input only from an accepted artifact receipt and a pre-confirmed slot mapping.
4. Never launch a dynamic consumer with `slots: []`.
5. Make commit, publication, delivery, and retry restart-safe and deduplicated.
6. Reject arbitrary paths, cross-dispatch producers, digest drift, and terminal turns without an artifact.
7. Preserve the bounded Stage F claim; this is not provider-complete effective-input evidence or a general workflow-graph solution.
8. L0/L1 covers exactly one completed producer and one required consumer slot; fan-in and non-success completion policies are L2.

## Evidence boundary

The closed scope and exact source digests are recorded in `design-selection/design-scope-manifest.json`. The local inventory was valid but empty, so no inventory entry was selected.
