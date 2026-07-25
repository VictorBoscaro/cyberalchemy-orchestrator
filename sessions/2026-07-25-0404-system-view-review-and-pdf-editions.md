---
tags: [agents, architecture, anti-bias, research, documentation]
node_type: audit
is_session: true
layer: [architecture, domain]
nature: explanatory
status: active
created: 2026-07-25
timestamp: 2026-07-25T04:04:59-03:00
expires: 2026-09-23
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "Hardened an operational review artifact while producing durable, reproducible visual editions of a core architecture view; the Lean posture remains explicitly unsettled."
---

# System View Review and PDF Editions

## Summary

The session first reconstructed the prior system-view introduction work and confirmed that its
opening had been rewritten for outside-reader clarity and inspectable grounding. It then evaluated
an adversarial review prompt and found it intellectually strong but too broad, partly
solution-anchored, and mixed between document review and research-program design. The user directed
that Lean is likely necessary but should remain an explicit, falsifiable bet rather than a
decision. A controlled writer and independent reviewers hardened the prompt through bounded
obligations, universal citation rules, a grounding gate, typed synthesis categories, and a
pre-registered Lean experiment condition. The requested reviewer zig-zag was unavailable because
the runtime cannot bind downstream manifests, so the user accepted independent reviews instead.
The session also produced five visual editions of the system view from identical text and added a
reproducible generator. An initial source-selection mistake was corrected and the erroneous
generated outputs were sent to the Recycle Bin. The review prompt remains in a temporary
research-oriented location pending a repository-wide convention for operational prompts.

## Open questions

- What repository-wide canonical home should own operational prompts such as the adversarial
  system-view review prompt?
- What governed mechanism should support standing or delegated dispatch confirmation without
  weakening the current concrete-proposal gate?

## Next steps

- Re-run `tools/build_system_view_pdf_versions.py` whenever the source system view changes.
- Move the adversarial review prompt only after its canonical artifact class and home are decided.

## Recommendation

Because the repository currently has no canonical prompt directory, prioritize the
operational-prompt ownership question and then relocate the review prompt once under the decided
artifact class.

## Files touched

- research/agent-language-mathematical-formalization/adversarial-review-prompt.md
- docs/architecture/pdf-versions/01-editorial.pdf
- docs/architecture/pdf-versions/02-swiss.pdf
- docs/architecture/pdf-versions/03-blueprint.pdf
- docs/architecture/pdf-versions/04-academic.pdf
- docs/architecture/pdf-versions/05-studio.pdf
- tools/build_system_view_pdf_versions.py
- telemetry/agents/subagents-dispatch.yaml
- sessions/2026-07-25-0404-system-view-review-and-pdf-editions.md

## User direction preserved

- Treat Lean as a likely requirement but keep it as a falsifiable bet until evidence earns a
  stronger status.
- Keep every PDF edition textually identical and vary only layout, presentation, and non-textual
  figures.
- Minimize repeated dispatch-confirmation interruptions, while acknowledging that the current
  repository policy still requires concrete confirmation for real dispatches.
