# Observation Probe lenses

These files define candidate, versioned lenses for `ObservationProbeTool` / **Sonda** runs.
A lens declares how a target may be observed and the shape and limits of its observations. It does
not transform the target, promote observations to facts or authorize writes to the target.

The first executable shadow lens is
[`agent-pool-scientist-tags@1`](agent-pool-scientist-tags@1.json). It observes the pinned agent-pool
snapshot without changing `agent-pool.yaml`.

Knowledge Taxonomy facets remain a separate future lens family. They classify information records;
they are not expertise tags and must not be merged into agent profile tags.
