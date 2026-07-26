---
name: "pdf"
description: "Read, create, inspect, render, and verify PDF files where visual layout matters."
---

# PDF Skill

## Workflow

1. Prefer visual review: render PDF pages to PNGs and inspect them.
2. Use a reliable PDF generator. For this task, local HTML/CSS printed by installed Chrome is the required reproducible generator because it matches the reference PDF's producer.
3. Use PyMuPDF for text extraction, metadata, font inspection, and rendering; do not rely on text extraction alone for layout fidelity.
4. After each meaningful update, re-render pages and verify alignment, spacing, and legibility.

## Temp and output conventions

- Use `tmp/pdfs/work-context-system-view/` for intermediate rendered files.
- Write the requested final artifact and its reproducible source under
  `plans/governed-agent-work-infrastructure/essays/work-context-system-view/pdf-version/`.
- Keep filenames stable and descriptive.

## Quality expectations

- Maintain polished visual design: consistent typography, spacing, margins, and section hierarchy.
- Avoid clipped text, overlapping elements, broken tables, black squares, unreadable glyphs, accidental blank pages, and stranded headings.
- Tables and code or diagram blocks must remain sharp, aligned, and legible.
- Use ASCII hyphens in generated presentation text. Do not alter literal source text merely to satisfy this presentation preference.
- References must remain human-readable; never leave tool tokens or placeholders.

## Final checks

- Do not deliver until the latest rendered-page inspection shows zero visual or formatting defects.
- Confirm page size, page count, fonts, section transitions, first and last pages, and representative table/code pages.
- Reopen the final PDF and compare its extracted text with the source body, explicitly accounting for PDF extraction order, Markdown link labels, and visual list markers.
- Keep the reproducible HTML/CSS or generator source beside the PDF.
