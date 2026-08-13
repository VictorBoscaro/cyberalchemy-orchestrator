"""Render a Markdown document as a typeset one-pager PDF.

Everything the layout can vary is a theme parameter: page size, margins, fonts,
palette, every type role, the label band, background ornaments, corner marks,
and the footer. The Markdown carries the words; the theme carries the design.

    python typeset.py --input doc.md --output doc.pdf
    python typeset.py --emit-theme > my-theme.json
    python typeset.py -i doc.md -o doc.pdf -t my-theme.json \
        --set type.title.size=26 --set palette.accent='"#1f5f4a"'
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

from reportlab.lib import pagesizes
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle

HERE = Path(__file__).resolve().parent
DEFAULT_THEME_PATH = HERE / "themes" / "quiet-paper.json"

ALIGNMENTS = {"left": TA_LEFT, "right": TA_RIGHT, "center": TA_CENTER, "justify": TA_JUSTIFY}


# --------------------------------------------------------------------------
# Theme
# --------------------------------------------------------------------------

def load_theme(path: Path | None) -> dict:
    with open(path or DEFAULT_THEME_PATH, encoding="utf-8") as handle:
        return json.load(handle)


def apply_overrides(theme: dict, overrides: list[str]) -> dict:
    """Apply `--set dotted.path=<json>` overrides onto the theme in place."""
    for raw in overrides:
        if "=" not in raw:
            raise SystemExit(f"--set expects dotted.path=value, got: {raw}")
        path, _, value = raw.partition("=")
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            parsed = value
        node = theme
        keys = path.strip().split(".")
        for key in keys[:-1]:
            if key not in node or not isinstance(node[key], dict):
                node[key] = {}
            node = node[key]
        node[keys[-1]] = parsed
    return theme


def resolve_color(theme: dict, value, alpha: float | None = None):
    """Accept a palette key, a #rrggbb literal, or an [r, g, b] triple."""
    if isinstance(value, (list, tuple)):
        red, green, blue = value[:3]
    else:
        literal = value if isinstance(value, str) and value.startswith("#") else theme["palette"][value]
        color = HexColor(literal)
        red, green, blue = color.red, color.green, color.blue
    if alpha is None:
        return Color(red, green, blue)
    return Color(red, green, blue, alpha=alpha)


def resolve_pagesize(theme: dict):
    size = theme["page"]["size"]
    if isinstance(size, str):
        try:
            return getattr(pagesizes, size.upper())
        except AttributeError as exc:
            raise SystemExit(f"unknown page size: {size}") from exc
    width, height = size
    return (width * mm, height * mm)


# --------------------------------------------------------------------------
# Fonts
# --------------------------------------------------------------------------

def resolve_fonts(theme: dict) -> dict:
    """Register each font role, falling back to a built-in face when absent.

    Anton's machines are Linux and Windows, so a missing TTF degrades the look
    instead of failing the render.
    """
    search_dirs = [Path(d).expanduser() for d in theme["fonts"].get("search_dirs", [])]
    index: dict[str, Path] = {}
    for directory in search_dirs:
        if not directory.is_dir():
            continue
        for candidate in directory.rglob("*.tt[fc]"):
            index.setdefault(candidate.name.lower(), candidate)

    resolved: dict[str, str] = {}
    for role, spec in theme["fonts"]["roles"].items():
        chosen = None
        for filename in spec.get("files", []):
            match = index.get(filename.lower())
            if match is not None:
                chosen = match
                break
        if chosen is None:
            resolved[role] = spec["fallback"]
            continue
        try:
            pdfmetrics.registerFont(TTFont(role, str(chosen)))
            resolved[role] = role
        except Exception:  # a broken or unsupported TTF must not stop the render
            resolved[role] = spec["fallback"]

    for family in theme["fonts"].get("families", []):
        normal = resolved.get(family.get("normal", ""))
        if not normal:
            continue
        pdfmetrics.registerFontFamily(
            normal,
            normal=normal,
            bold=resolved.get(family.get("bold", ""), normal),
            italic=resolved.get(family.get("italic", ""), normal),
            boldItalic=resolved.get(family.get("bold_italic", ""), normal),
        )
    return resolved


def build_styles(theme: dict, fonts: dict) -> dict:
    styles = {}
    for name, spec in theme["type"].items():
        styles[name] = ParagraphStyle(
            name,
            fontName=fonts[spec["font"]],
            fontSize=spec["size"],
            leading=spec["leading"],
            textColor=resolve_color(theme, spec.get("color", "ink")),
            alignment=ALIGNMENTS[spec.get("align", "left")],
            spaceBefore=spec.get("space_before_mm", 0) * mm,
            spaceAfter=spec.get("space_after_mm", 0) * mm,
            leftIndent=spec.get("left_indent_mm", 0) * mm,
            firstLineIndent=spec.get("first_line_indent_mm", 0) * mm,
            keepWithNext=spec.get("keep_with_next", False),
            splitLongWords=spec.get("split_long_words", False),
            allowWidows=0,
            allowOrphans=0,
        )
    return styles


# --------------------------------------------------------------------------
# Markdown
# --------------------------------------------------------------------------

INLINE_BOLD = re.compile(r"\*\*(.+?)\*\*", re.DOTALL)
INLINE_ITALIC = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", re.DOTALL)
INLINE_CODE = re.compile(r"`(.+?)`", re.DOTALL)
LIST_ITEM = re.compile(r"^[-*+]\s+(.*)$")
LABELLED_ITEM = re.compile(r"^\*\*(.+?)\*\*:?\s*(.*)$")


def inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = INLINE_CODE.sub(r"\1", text)
    text = INLINE_BOLD.sub(r"<b>\1</b>", text)
    text = INLINE_ITALIC.sub(r"<i>\1</i>", text)
    return text


def parse_markdown(source: str) -> dict:
    """Parse the supported subset into title, subtitle, and section blocks."""
    document = {"title": None, "subtitle": None, "blocks": []}
    chunks = [c.strip() for c in re.split(r"\n\s*\n", source.strip()) if c.strip()]

    for chunk in chunks:
        lines = [line.strip() for line in chunk.splitlines() if line.strip()]

        if lines[0].startswith("# ") and document["title"] is None:
            document["title"] = lines[0][2:].strip()
            continue

        if lines[0].startswith("## "):
            document["blocks"].append({"kind": "heading", "text": lines[0][3:].strip()})
            remainder = lines[1:]
            if remainder:
                lines = remainder
            else:
                continue

        if all(LIST_ITEM.match(line) for line in lines):
            items = []
            for line in lines:
                body = LIST_ITEM.match(line).group(1).strip()
                labelled = LABELLED_ITEM.match(body)
                if labelled:
                    items.append({"label": labelled.group(1).strip(), "text": labelled.group(2).strip()})
                else:
                    items.append({"label": None, "text": body})
            document["blocks"].append({"kind": "list", "items": items})
            continue

        paragraph = " ".join(lines)
        subtitle_only = re.fullmatch(r"\*\*(.+)\*\*", paragraph)
        if subtitle_only and document["subtitle"] is None and not document["blocks"]:
            document["subtitle"] = subtitle_only.group(1).strip()
            continue
        document["blocks"].append({"kind": "paragraph", "text": paragraph})

    return document


# --------------------------------------------------------------------------
# Page furniture
# --------------------------------------------------------------------------

def make_page_painter(theme: dict, fonts: dict, page_count: list):
    width, height = resolve_pagesize(theme)

    def draw(canvas, doc):
        page_count.append(canvas.getPageNumber())
        canvas.saveState()

        canvas.setFillColor(resolve_color(theme, theme["page"]["background"]))
        canvas.rect(0, 0, width, height, fill=1, stroke=0)

        for shape in theme.get("ornaments", {}).get("shapes", []):
            canvas.setFillColor(resolve_color(theme, shape["color"], shape.get("alpha", 1.0)))
            if shape["type"] == "circle":
                canvas.circle(
                    width * shape["cx_rel"],
                    height * shape["cy_rel"],
                    shape["radius_mm"] * mm,
                    fill=1,
                    stroke=0,
                )
            elif shape["type"] == "rect":
                canvas.rect(
                    width * shape["x_rel"],
                    height * shape["y_rel"],
                    shape["width_mm"] * mm,
                    shape["height_mm"] * mm,
                    fill=1,
                    stroke=0,
                )

        marks = theme.get("corner_marks", {})
        if marks.get("enabled"):
            canvas.setStrokeColor(resolve_color(theme, marks["color"], marks.get("alpha", 1.0)))
            canvas.setLineWidth(marks.get("line_width", 0.6))
            inset, arm = marks["inset_mm"] * mm, marks["arm_mm"] * mm
            for x, y, sx, sy in [
                (inset, height - inset, 1, -1),
                (width - inset, height - inset, -1, -1),
                (inset, inset, 1, 1),
                (width - inset, inset, -1, 1),
            ]:
                canvas.line(x, y, x + sx * arm, y)
                canvas.line(x, y, x, y + sy * arm)

        footer = theme.get("footer", {})
        rule = footer.get("rule", {})
        if rule.get("enabled"):
            canvas.setStrokeColor(resolve_color(theme, rule["color"], rule.get("alpha", 1.0)))
            canvas.setLineWidth(rule.get("line_width", 0.55))
            inset = rule["inset_mm"] * mm
            canvas.line(inset, rule["y_mm"] * mm, width - inset, rule["y_mm"] * mm)

        text = footer.get("text", {})
        if text.get("left") or text.get("right"):
            canvas.setFont(fonts[text.get("font", "text")], text.get("size", 7.5))
            canvas.setFillColor(resolve_color(theme, text.get("color", "muted")))
            inset = text.get("inset_mm", 22) * mm
            baseline = text.get("y_mm", 10.7) * mm
            if text.get("left"):
                canvas.drawString(inset, baseline, text["left"])
            if text.get("right"):
                canvas.drawRightString(width - inset, baseline, text["right"])

        canvas.restoreState()

    return draw


def build_band(theme: dict, styles: dict, doc_width: float, items: list):
    band = theme["band"]
    columns = band.get("columns") or len(items)
    label_case = band.get("label_transform", "upper")

    cells = []
    for item in items:
        label = (item["label"] or "").rstrip(band.get("label_strip_trailing", ""))
        if label_case == "upper":
            label = label.upper()
        elif label_case == "lower":
            label = label.lower()
        text = item["text"].rstrip(band.get("text_strip_trailing", ""))
        cell = []
        if label:
            cell.append(Paragraph(inline(label), styles[band["label_style"]]))
        cell.append(Paragraph(inline(text), styles[band["text_style"]]))
        cells.append(cell)

    rows = [cells[i:i + columns] for i in range(0, len(cells), columns)]
    for row in rows:
        while len(row) < columns:
            row.append([])

    style = [
        ("BACKGROUND", (0, 0), (-1, -1), resolve_color(theme, band["background"])),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), band["padding_mm"]["left"] * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), band["padding_mm"]["right"] * mm),
        ("TOPPADDING", (0, 0), (-1, -1), band["padding_mm"]["top"] * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), band["padding_mm"]["bottom"] * mm),
    ]
    if band.get("box_width"):
        style.append(("BOX", (0, 0), (-1, -1), band["box_width"], resolve_color(theme, band["box_color"])))
    if band.get("rule_above_width"):
        style.append(
            ("LINEABOVE", (0, 0), (-1, 0), band["rule_above_width"], resolve_color(theme, band["rule_above_color"]))
        )

    return Table(rows, colWidths=[doc_width / columns] * columns, style=TableStyle(style))


def build_story(theme: dict, styles: dict, document: dict, doc_width: float) -> list:
    sections = theme.get("sections", {})
    overrides = {k.lower(): v for k, v in sections.get("overrides", {}).items()}
    default_list_style = sections.get("default_list_style", "bullets")

    story = [Spacer(1, theme["page"].get("lead_in_mm", 0) * mm)]
    if document["title"]:
        story.append(Paragraph(inline(document["title"]), styles["title"]))
    if document["subtitle"]:
        subtitle = document["subtitle"]
        if sections.get("subtitle_transform") == "upper":
            subtitle = subtitle.upper()
        if sections.get("subtitle_separator"):
            subtitle = subtitle.replace(" / ", sections["subtitle_separator"])
        story.append(Paragraph(inline(subtitle), styles["subtitle"]))

    current_section = ""
    for block in document["blocks"]:
        if block["kind"] == "heading":
            current_section = block["text"]
            story.append(Paragraph(inline(block["text"]), styles["heading"]))
        elif block["kind"] == "paragraph":
            story.append(Paragraph(inline(block["text"]), styles["body"]))
        elif block["kind"] == "list":
            rule = overrides.get(current_section.lower(), {})
            list_style = rule.get("list_style", default_list_style)
            if list_style == "band":
                story.append(build_band(theme, styles, doc_width, block["items"]))
                story.append(Spacer(1, theme["band"].get("space_after_mm", 4) * mm))
            else:
                for item in block["items"]:
                    text = f"<b>{inline(item['label'])}:</b> {inline(item['text'])}" if item["label"] else inline(item["text"])
                    story.append(Paragraph(text, styles["bullet"], bulletText=theme["bullets"]["marker"]))
                story.append(Spacer(1, theme["bullets"].get("space_after_mm", 2) * mm))

    return story


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------

def render(source: str, output: Path, theme: dict) -> dict:
    fonts = resolve_fonts(theme)
    styles = build_styles(theme, fonts)
    document = parse_markdown(source)

    page_width, page_height = resolve_pagesize(theme)
    margins = theme["page"]["margins_mm"]
    metadata = theme.get("metadata", {})

    output.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(output),
        pagesize=(page_width, page_height),
        leftMargin=margins["left"] * mm,
        rightMargin=margins["right"] * mm,
        topMargin=margins["top"] * mm,
        bottomMargin=margins["bottom"] * mm,
        title=metadata.get("title") or document["title"] or output.stem,
        author=metadata.get("author") or "",
        subject=metadata.get("subject") or "",
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    pages: list[int] = []
    doc.addPageTemplates([PageTemplate(id="page", frames=[frame], onPage=make_page_painter(theme, fonts, pages))])
    doc.build(build_story(theme, styles, document, doc.width))

    return {
        "output": output,
        "pages": max(pages) if pages else 0,
        "fonts": fonts,
        "title": document["title"],
        "sections": [b["text"] for b in document["blocks"] if b["kind"] == "heading"],
    }


def write_preview(pdf: Path, preview: Path, dpi: int) -> Path | None:
    try:
        import fitz  # PyMuPDF, optional
    except ImportError:
        print("preview skipped: PyMuPDF is not installed (pip install pymupdf)", file=sys.stderr)
        return None
    preview.parent.mkdir(parents=True, exist_ok=True)
    with fitz.open(str(pdf)) as handle:
        handle[0].get_pixmap(dpi=dpi).save(str(preview))
    return preview


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Render a Markdown document as a one-pager PDF.")
    parser.add_argument("--input", "-i", type=Path, help="Markdown source file")
    parser.add_argument("--output", "-o", type=Path, help="destination PDF")
    parser.add_argument("--theme", "-t", type=Path, help=f"theme JSON (default: {DEFAULT_THEME_PATH.name})")
    parser.add_argument("--set", dest="overrides", action="append", default=[],
                        help="override a theme value: dotted.path=<json>, repeatable")
    parser.add_argument("--band-section", action="append", default=[],
                        help="render this section's bullet list as the column band, repeatable")
    parser.add_argument("--footer-left", help="shortcut for footer.text.left")
    parser.add_argument("--footer-right", help="shortcut for footer.text.right")
    parser.add_argument("--preview", type=Path, help="also write a PNG of page 1 (needs PyMuPDF)")
    parser.add_argument("--preview-dpi", type=int, default=110)
    parser.add_argument("--emit-theme", action="store_true", help="print the resolved theme JSON and exit")
    parser.add_argument("--max-pages", type=int, default=0, help="fail if the render exceeds this page count")
    args = parser.parse_args(argv)

    theme = copy.deepcopy(load_theme(args.theme))
    apply_overrides(theme, args.overrides)
    for section in args.band_section:
        theme.setdefault("sections", {}).setdefault("overrides", {})[section] = {"list_style": "band"}
    if args.footer_left is not None:
        theme.setdefault("footer", {}).setdefault("text", {})["left"] = args.footer_left
    if args.footer_right is not None:
        theme.setdefault("footer", {}).setdefault("text", {})["right"] = args.footer_right

    if args.emit_theme:
        json.dump(theme, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0

    if not args.input or not args.output:
        parser.error("--input and --output are required unless --emit-theme is used")

    result = render(args.input.read_text(encoding="utf-8"), args.output, theme)
    print(f"{result['output']}  ({result['pages']} page{'s' if result['pages'] != 1 else ''})")
    if args.preview:
        written = write_preview(result["output"], args.preview, args.preview_dpi)
        if written:
            print(written)
    if args.max_pages and result["pages"] > args.max_pages:
        print(
            f"page budget exceeded: {result['pages']} > {args.max_pages}. "
            "Cut copy, or lower type.body.size / type.body.leading / page.margins_mm.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
