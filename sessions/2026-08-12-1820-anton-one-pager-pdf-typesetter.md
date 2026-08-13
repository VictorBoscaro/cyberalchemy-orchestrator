---
tags: [pdf-typesetting, markdown-rendering, reportlab, professional-introduction, internal-tooling]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-12T18:20:24-03:00
updated_at: 2026-08-12T18:20:24-03:00
expires: 2026-10-11
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 3
importance_rationale: "A small reusable document capability, useful and now parameterized, but off the repository's main governance spine."
---

# Anton one-pager and the document PDF typesetter

## Summary

The session began by rewriting Anton's raw skills-and-limitations text as a one-pager in the same
form as the owner's own introduction PDF, which was located in the repository rather than
described from memory. Anton's limitations were kept but folded into the prose as calibration
rather than listed as apologies, his DevOps claim was rendered with its own caveat, and the
closing section named the agent-building gap as a stated direction instead of inflating it.
The owner then asked for a reusable tool so Anton could convert his own documents, with as much
of the layout as possible exposed as mechanical parameters. The hand-written script was
generalized into a Markdown-to-PDF renderer whose entire design lives in a JSON theme: page,
palette, font roles with fallbacks, every type role, the label band, ornaments, corner marks, and
footer, all overridable from the command line without touching code. Parity was verified rather
than assumed: rendering Anton's Markdown through the tool produces text extraction identical to
the hand-written script, and the Victor pair differs only by a clause that already differed
between its own `.md` and `.py`. The owner rejected the first placement and name, so the tool
moved under `internal-tools/` and was renamed `document-pdf-typesetter`, since the previous name
described the output format instead of the capability. The duplicated PDF under `output/pdf/` was
removed so a single location holds the artifact, and the hand-written script moved into the
tool's `examples/` with its output path corrected. Contact and location fields were left empty by
decision rather than filled with invented values.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [victor_boscaro_introduction.py](tools/pdf/victor_boscaro_introduction.py) | `derives-from` | The default theme's page geometry, palette, type scale, band, ornaments, and footer were extracted parameter by parameter from this hand-written script. |

## Open questions

- Whether the owner's `.md` or `.py` carries the authoritative wording of the Victor one-pager;
  they disagree on one clause ("Use data to separate causes…" versus "Separate causes…"), and
  nothing in the session establishes which was intended.
- Whether `internal-tools` should be renamed `internal_tools`; the owner wrote the underscore
  form twice, while the existing sibling tool established the hyphen form.

## Next steps

1. Resolve the Victor clause divergence and render that one-pager through the typesetter, so a
   single Markdown source feeds the PDF.
2. Copy `internal-tools/document-pdf-typesetter/` into Anton's `.claude/skills/` on his machine
   and confirm the font fallback path on Linux, where Palatino and Constantia are absent.

## Recommendation

Retire the second hand-written script by making the Victor `.md` the single source, as parity is
already demonstrated for the Anton document and the only obstacle is deciding one clause. Two
writers for the same page is what produced the divergence recorded above; collapsing them costs
one editorial decision and removes the class of defect rather than this instance of it.

## Files touched

- internal-tools/document-pdf-typesetter/typeset.py
- internal-tools/document-pdf-typesetter/themes/quiet-paper.json
- internal-tools/document-pdf-typesetter/SKILL.md
- internal-tools/document-pdf-typesetter/README.md
- internal-tools/document-pdf-typesetter/examples/anton-introduction.md
- internal-tools/document-pdf-typesetter/examples/anton_introduction_handwritten.py
- internal-tools/document-pdf-typesetter/out/anton/anton-introduction.pdf
- internal-tools/document-pdf-typesetter/out/anton/anton-introduction.md
- internal-tools/document-pdf-typesetter/out/anton/anton-introduction.png
- output/pdf/anton-introduction-one-pager/ (removed as a duplicate)
- tmp/pdfs/anton-introduction/page-1.png
- tmp/pdfs/one-pager-tool/
