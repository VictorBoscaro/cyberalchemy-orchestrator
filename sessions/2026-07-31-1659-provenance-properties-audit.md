---
tags: [provenance, artifact-lineage, dispatch-ledger, frontmatter-conventions, ingestion-telemetry]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-07-31T16:59:04-03:00
updated_at: 2026-07-31T16:59:04-03:00
expires: 2026-09-29
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "Audited three owner-named properties against the real repository and found two absent and one partial, then routed the corrective work to a new feature package and separated it from BL-3."
---

# Provenance properties audit and artifact-lineage routing

## Summary

The session began as an orientation request about what this repository is for and became an
evidence audit of three properties the owner proposed. The owner corrected the framing: the
target is a machine that performs work — any work — which needs both tools that do the work and
a substrate that records decisions, connects a task to the larger context it serves, and knows
dependencies; "perfect task, wrong work" is one symptom of the missing substrate, not the scope.
Three read-only subagents audited the properties. Detached execution from a payload is absent —
nothing consumes the `.confirmed` marker beyond a UI flag, every launch still requires the parent
session's `Agent` call, and typed `connections` are stored but never scheduled. Source-consumption
logging is partial — 414 `dispatch_ingestions` rows running by default, but none attributed to a
registered dispatch, roughly 38% coverage of wrapped launches, zero `external_url` rows, and hook
failures swallowed at exit 0. Provenance queries are absent — no ledger row carries a plan, task,
or artifact link, the appender rejects unknown keys, and `plan_id` is null in all three plans.
Three contradictions surfaced along the way, recorded as edges below. The owner then reframed the
fix away from assigning `plan_id` toward nearest-neighbor lineage declared in frontmatter —
`derived_from` as one genealogical parent, `evidence` as many non-transitive supports — which
makes the file path the identity and removes the need for an admission gate; that convention was
found already present but unpromoted in six files, one of them pinning the parent version. The
work was routed to a new feature package rather than a Plan, and separated explicitly from
BACKLOG.md's BL-3, which addresses epistemic nodes and is blocked on OQ-3; drafted dispatch
prompts were rejected by the owner and no document was authored.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [plans/governed-agent-work-infrastructure/PLAN.md](../plans/governed-agent-work-infrastructure/PLAN.md) | `is-part-of` | The audit measured this root Plan's own stated cross-cutting gap — the absent provenance spine and the four disjoint id-spaces — against the working repository. |
| [BACKLOG.md](../BACKLOG.md) | `validates` | Produced counts supporting BL-3's premise that the id-spaces are disjoint: no ledger row carries a plan, task, or artifact link, and `plan_id` is null in all three plans. |
| [README.md](../README.md) | `contradicts` | README states the ACI local pilot is opt-in and off by default, while `implementations/server/runtime/host_dispatch_hook.py` passes `opted_in=True` as a hardcoded argument, so the ingestion hooks run regardless of the environment flag. |
| [docs/discovery/README.md](../docs/discovery/README.md) | `contradicts` | This index declares its discoveries are authored via `.claude/skills/discovery-writing/SKILL.md`, but that skill states only two target paths are accepted and `docs/discovery/` is not among them. |

## Open questions

- How the lineage edge exists for source files, which carry no YAML frontmatter. The owner named
  code deriving from a spec as a primary case. Whether any convention already exists in source
  files was **not checked this session** — the frontmatter survey covered `*.md` only.
- Whether renames and moves should be absorbed by accepting edge breakage and detecting it, or by
  tracking the rename. A recommendation was offered and not decided.
- Whether the ledger row joins the same path namespace through a `serves:` field, given that a
  schema bump to 0.6.2 was previously attempted and abandoned. The reason for that abandonment was
  not read this session.
- Whether the existing discovery validator already owns edge validation. Fixtures for it exist in
  this repository; its implementation was not located here.
- Whether `AGENTS.md` should be re-attested into the Stage-E manifest or reverted to its committed
  form. Until one is chosen, the mandatory hook denies every `Agent` launch.

## Next steps

1. Clear the Stage-E `AGENTS.md` digest mismatch — no delegated work can run before it.
2. Redraft the writer and reviewer prompts for the artifact-lineage scoping README; the drafts
   produced this session were rejected by the owner and the specific defect was not stated.
3. Correct the README claim that the ACI local pilot is off by default.

## Recommendation

The keystone is the open question about source files. The owner named code deriving from a spec as
a primary use case, and the survey that grounds this convention covered Markdown only — 105 of 234
files under `docs/` carry frontmatter, and no equivalent check was run against source. If source
files turn out to have no place to carry the edge, the convention covers documents alone, which is
materially narrower than what was asked for, and that narrowing should be known before the scoping
README is written rather than discovered inside it. Attack it by checking whether any source file
in this repository already declares an upstream artifact, before assuming a mechanism must be
invented.

## Files touched

- sessions/2026-07-31-1659-provenance-properties-audit.md
