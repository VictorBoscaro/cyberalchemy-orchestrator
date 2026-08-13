---
name: document-pdf-typesetter
description: Turn a Markdown document into a typeset one-page PDF using the one-pager-pdf renderer, choosing the theme parameters (page, palette, fonts, type scale, label band, footer) that fit the document instead of editing layout code. Use when asked to make a PDF, a one-pager, an introduction sheet, a profile, or a printable version of a Markdown file.
---

# Document PDF typesetter

Render a Markdown document as a single typeset page. The renderer at
`typeset.py` owns the drawing; a JSON theme owns every design decision. Your job is
to shape the Markdown into the supported structure and to choose theme parameters — never to
fork the Python for a one-off look.

## Tool

```
python typeset.py --input DOC.md --output DOC.pdf [options]
```

| Option | Effect |
| --- | --- |
| `-i, --input` | Markdown source |
| `-o, --output` | destination PDF (parent directories are created) |
| `-t, --theme` | theme JSON; default `themes/quiet-paper.json` |
| `--set path=<json>` | override any theme value, repeatable (e.g. `--set type.body.size=10.5`) |
| `--band-section NAME` | render that section's bullet list as the column band, repeatable |
| `--footer-left`, `--footer-right` | footer text shortcuts |
| `--preview OUT.png` | also write a PNG of page 1 (needs PyMuPDF) |
| `--preview-dpi` | preview resolution, default 110 |
| `--max-pages N` | exit non-zero when the render exceeds N pages |
| `--emit-theme` | print the resolved theme (defaults plus overrides) and exit |

Values passed to `--set` are parsed as JSON, so quote strings: `--set palette.accent='"#1f5f4a"'`.
Requires `reportlab`; `pymupdf` only for previews.

## Supported Markdown

```markdown
# Title

**Subtitle line / second phrase**

## Section heading

A paragraph. Inline **bold**, *italic*, and `code` are supported.

- **Label:** cell text
- **Label:** cell text
```

- The first `# ` line is the title.
- A paragraph that is entirely bold, before any section, is the subtitle.
- `## ` starts a section; paragraphs under it become body text.
- A bullet list becomes the four-across label band by default. Set
  `sections.default_list_style` to `bullets` for ordinary bullets, or override one section with
  `--band-section "What I do"`.
- Anything else (tables, images, code blocks, `###`) is not supported. Rewrite it as paragraphs,
  a list, or a new section before rendering.

## Workflow

1. Read the source document. If it is prose without structure, restructure it into the shape
   above first, and show the Markdown before rendering it.
2. Render with `--max-pages 1` and `--preview`. Look at the preview.
3. If the page budget fails or the page looks crowded or empty, adjust parameters in this order:
   cut copy, then `type.body.size` / `type.body.leading`, then `type.body.space_after_mm`, then
   `page.margins_mm`. Re-render and look again.
4. Report the output path, the page count, and any parameter you changed from the theme default.

## Parameters you control

Every key below is settable in a theme file or with `--set`. Run `--emit-theme` to see current
values.

| Group | Keys | What it controls |
| --- | --- | --- |
| `page` | `size` (`A4`, `LETTER`, or `[width_mm, height_mm]`), `background`, `margins_mm.{left,right,top,bottom}`, `lead_in_mm` | sheet, margins, space above the title |
| `palette` | `paper`, `paper_light`, `ink`, `muted`, `accent`, `accent_dark`, `hairline`, `wash`, `highlight` | named colours; every other colour field takes a palette key or a `#rrggbb` literal |
| `fonts` | `search_dirs`, `roles.<role>.files`, `roles.<role>.fallback`, `families` | which TTF each role uses and what it falls back to when the file is absent |
| `type.<role>` | `font`, `size`, `leading`, `color`, `align`, `space_before_mm`, `space_after_mm`, `left_indent_mm`, `first_line_indent_mm`, `keep_with_next` | roles: `title`, `subtitle`, `heading`, `body`, `bullet`, `band_label`, `band_text` |
| `band` | `columns` (`null` = one per item), `label_transform`, `label_strip_trailing`, `text_strip_trailing`, `background`, `box_width`, `box_color`, `rule_above_width`, `rule_above_color`, `padding_mm`, `space_after_mm` | the boxed row of labelled cells |
| `bullets` | `marker`, `space_after_mm` | ordinary bullet lists |
| `sections` | `default_list_style` (`band`/`bullets`), `overrides.<heading>.list_style`, `subtitle_transform`, `subtitle_separator` | per-section behaviour and subtitle casing |
| `ornaments.shapes[]` | `type` (`circle`/`rect`), `cx_rel`/`cy_rel` or `x_rel`/`y_rel`, `radius_mm` or `width_mm`/`height_mm`, `color`, `alpha` | background washes, positioned relative to the page |
| `corner_marks` | `enabled`, `inset_mm`, `arm_mm`, `color`, `alpha`, `line_width` | registration marks at the four corners |
| `footer` | `rule.{enabled,y_mm,inset_mm,color,alpha,line_width}`, `text.{font,size,color,y_mm,inset_mm,left,right}` | footer rule and the two contact lines |
| `metadata` | `title`, `author`, `subject` | PDF document properties; `null` falls back to the document title |

## Rules

- Do not edit `typeset.py` to change how one document looks. If a document needs
  something the parameters cannot express, say so and propose the parameter to add.
- A recurring look belongs in its own theme file under `themes/`, not in a long chain of `--set`.
- Never invent facts, contacts, or credentials to fill a layout slot. Leave `footer.text.left`
  and `footer.text.right` empty and ask.
- Missing fonts are not an error: the renderer substitutes a built-in face. Mention the
  substitution when it happened, because the page will not match the reference look.
