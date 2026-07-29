---
tags: [pdf-publication, build-pipeline, byte-economy, render-reproducibility, baseline-freeze, red-team-review]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-07-29T10:10:26-03:00
updated_at: 2026-07-29T10:10:26-03:00
expires: 2026-09-27
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "Establishes that the shipped short-version PDFs are unversioned and unreproducible, and that a 52-56% lossless size reduction is available, but gates both behind an undecided baseline."
---

# Short-version PDF pipeline review

## Summary

The owner asked to make the PDFs under the short-version page far more efficient while keeping them
exactly the same, with better code to extend and change them. Direct measurement found that 67.9% of
the 514,178-byte base PDF is page content streams stored with no compression filter at all, and a red
team traced the cause to the stamper's pypdf write pass, which decompresses through `merge_page()`
and never re-applies Flate; the available saving is 287,838 bytes on the base and 232,241 on the
revision, lossless by construction. A four-lens review dispatch (byte economy, fidelity, mechanics,
operability) with a confrontation round, two verifiers and a coverage auditor produced 37 verified
change requests across six artifacts, every one verdict FIX. Verification overturned two attacker
positions that the attackers themselves had defended: the encoding defect is already realized in all
five shipped HTML files rather than latent, and roughly half of each hand-forked style block is
unreferenced rather than fully used. The consensus critical finding that in-place stamping corrupts
the PDF did not reproduce on pypdf 6.14.2 and was downgraded. A live conflict over whether the base
PDF preserves the ff ligature was settled by measurement as extractor-dependent, which bars
extracted-text equality as an acceptance gate for any future fidelity check. The operability lens
established the ordering that governs everything else: the stamper, the mark, the variants and both
revision files are untracked, so no reduction is currently revertable and committing the baseline
must precede the byte fix. The owner froze the baseline as the current rendered appearance, but which
PDF that names was left undecided and blocks seven findings plus the fate of the build script, the
four render folders and the three variants. Nothing was optimized: this session produced change
requests, not fixes. The coverage audit corrected the review's own overclaim of complete lens
coverage and named three empty target-lens cells.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [work-context-system-view essay](../plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md) | `is-part-of` | The reviewed PDF pipeline exists to publish this essay; the corpus is its short-version print edition. |
| [Short work-context essay review and revision](2026-07-29-0311-work-context-short-review-revision.md) | `contradicts` | That session's `review/review.md` claims it inspected the frozen page renders of the revision artifact, but the review file predates that artifact by eleven minutes and the only renders on disk predate both. |

## Open questions

- Which PDF is the frozen baseline: `work-context-system-view-short-polished-diagrams.pdf`
  (Palatino/Constantia) or `...-revision.pdf` (Georgia/Arial), or both for different purposes? The
  corpus never states it. `variants/INDEX.md:9` was argued to settle it and does not — it is a link
  label. The three variants carry the old title and text matching neither file.
- Whether the appearance should stay on proprietary Windows-bundled faces behind a hard-failing font
  precondition, or be re-frozen on metric-compatible OFL faces (Gelasio, Liberation Sans), which
  preserves advance widths and pagination but changes glyph outlines.
- Whether the three uncovered target-lens cells matter: `cyberalchemy-mark.svg` was never attacked
  from operability, and the `variants/` group never from byte economy or mechanics.

## Next steps

1. Hash-freeze the five PDFs and their HTML, then commit the untracked corpus with a `.gitattributes`
   binary rule. Until this lands, the byte fix rewrites a file git cannot restore.
2. Decide the baseline question above; seven change requests are gated on it.
3. Apply the content-stream compression fix in `stamp-cyberalchemy.py`, verified by decoded-stream
   byte-equality rather than rasterization, including the `/Pattern` and `/Form` streams.
4. Write the render command down as a committed script; it currently exists only as prose in three
   `rationale.txt` files that disagree with each other.
5. Retract the false extracted-text equality claims in `variants/INDEX.md` and each `rationale.txt`.

## Recommendation

Do step 1 before anything else and treat it as the whole point of the session's ordering argument.
The 56% saving is real and measured, but it is an unrevertable edit to an unversioned file, and the
cost of waiting is one commit. The structural answer to the "code to extend" half of the request is
one `build.py` in `short-version/` with variant deltas rather than hardening the existing PowerShell
script — that script writes one of five shipped documents and the other four already bypass it, each
carrying its own independent style block. Hardening it is a worthwhile stopgap and should not be
mistaken for the fix.

## Files touched

- plans/governed-agent-work-infrastructure/essays/work-context-system-view/pdf-version/short-version/review/pdf-pipeline-optimization/review.md
- .codex/workflow-inputs/2026-07-29-short-version-pdf-pipeline-review/attacker-positions.md
- telemetry/agents/subagents-dispatch.yaml
- sessions/2026-07-29-1010-short-version-pdf-pipeline-review.md
