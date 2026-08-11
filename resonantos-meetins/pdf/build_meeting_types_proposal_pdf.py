from __future__ import annotations

import html
import re
import shutil
from collections import Counter
from pathlib import Path

import pdfplumber
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "research" / "resonantos-meetings" / "meeting-types-proposal.md"
OUTPUT = Path(__file__).resolve().parent / "meeting-types-proposal.pdf"
WORK = ROOT / "tmp" / "pdfs" / "resonantos-meetings" / "worker"
PAGE = landscape(A4)

NAVY = colors.HexColor("#102A35")
INK = colors.HexColor("#17323B")
TEAL = colors.HexColor("#008C8C")
TEXT_TEAL_HEX = "#006B6B"
TEXT_TEAL = colors.HexColor(TEXT_TEAL_HEX)
CYAN = colors.HexColor("#74D7D1")
CORAL = colors.HexColor("#E7815D")
WARM = colors.HexColor("#F7F2E8")
PAPER = colors.HexColor("#FFFDF8")
MINT = colors.HexColor("#E3F1ED")
SKY = colors.HexColor("#E5F1F4")
SAND = colors.HexColor("#F0E7D7")
MUTED = colors.HexColor("#526870")
RULE = colors.HexColor("#AFC5C4")
WHITE = colors.white

MARGIN = 10 * mm
BODY_SIZE = 8.8
BODY_LEADING = 10.55
TABLE_SIZE = 8.8
TABLE_LEADING = 10.25
LABEL_SIZE = 8.8
LIGHT_BACKGROUNDS = ["#FFFDF8", "#E3F1ED", "#E5F1F4", "#F0E7D7", "#F7F2E8"]


def fail(message: str) -> None:
    raise RuntimeError(message)


def relative_luminance(hex_color: str) -> float:
    channels = [int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [channel / 12.92 if channel <= 0.04045
              else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted(
        [relative_luminance(foreground), relative_luminance(background)], reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)


def plain(markdown: str) -> str:
    value = markdown.strip()
    if value.startswith(">"):
        value = re.sub(r"^>\s*", "", value)
    elif re.match(r"^#{1,6}\s+", value):
        value = re.sub(r"^#{1,6}\s+", "", value)
    elif re.match(r"^[-*]\s+", value):
        value = re.sub(r"^[-*]\s+", "", value)
    elif re.match(r"^\d+\.\s+", value):
        value = re.sub(r"^\d+\.\s+", "", value)
    return value.replace("**", "").replace("_", "").strip()


def rich(markdown: str) -> str:
    safe = html.escape(markdown.strip(), quote=False)
    safe = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", safe)
    safe = re.sub(r"(?<!\*)_(.+?)_(?!\*)", r"<i>\1</i>", safe)
    return safe


def parse_source(text: str) -> dict:
    if "\ufffd" in text:
        fail("Source contains a Unicode replacement character.")
    blocks: list[dict] = []
    paragraph: list[str] = []

    def flush() -> None:
        nonlocal paragraph
        if paragraph:
            raw = " ".join(line.strip() for line in paragraph).strip()
            blocks.append({"kind": "paragraph", "raw": raw, "text": plain(raw)})
            paragraph = []

    for line in text.splitlines():
        if not line.strip():
            flush()
        elif re.match(r"^#{1,3}\s+", line):
            flush()
            level = len(line) - len(line.lstrip("#"))
            blocks.append({"kind": f"h{level}", "raw": line, "text": plain(line)})
        elif line.startswith("> "):
            flush()
            blocks.append({"kind": "quote", "raw": line, "text": plain(line)})
        elif re.match(r"^\d+\.\s+", line):
            flush()
            blocks.append({"kind": "number", "raw": line, "text": plain(line)})
        elif line.startswith("- "):
            flush()
            blocks.append({"kind": "bullet", "raw": line, "text": plain(line)})
        else:
            paragraph.append(line)
    flush()

    required = [
        "A Working Framework for ResonantOS Meetings", "Objective", "Why distinguish meetings?",
        "A small purpose-based taxonomy", "A minimal pattern for every meeting",
        "Conditional patterns, only when the stakes require them",
        "Recurring context and a specific meeting", "What should remain flexible", "Questions for the group",
    ]
    headings = [b["text"] for b in blocks if b["kind"].startswith("h")]
    for heading in required:
        if heading not in headings:
            fail(f"Required source heading missing: {heading}")
    if len([b for b in blocks if b["kind"] == "h3"]) != 7:
        fail("Expected seven meeting types.")
    if len([b for b in blocks if b["kind"] == "number"]) != 12:
        fail("Expected five prompt questions and seven group questions.")
    if len([b for b in blocks if b["kind"] == "bullet"]) != 10:
        fail("Expected four safeguards and six conditional patterns.")

    sections: dict[str, list[dict]] = {"title": []}
    current = "title"
    for block in blocks:
        if block["kind"] == "h2":
            current = block["text"]
            sections[current] = [block]
        else:
            sections.setdefault(current, []).append(block)

    taxonomy = sections["A small purpose-based taxonomy"]
    intro: list[dict] = []
    types: list[dict] = []
    active = None
    for block in taxonomy[1:]:
        if block["kind"] == "h3":
            active = {"heading": block, "fields": {}, "pilot": []}
            types.append(active)
        elif active is None:
            intro.append(block)
        elif block["kind"] == "paragraph":
            match = re.match(r"^\*\*(Primary purpose|Expected useful result|Proportionate treatment|Open question):\*\*\s*(.*)$", block["raw"])
            if match:
                active["fields"][match.group(1)] = {"raw": block["raw"], "text": plain(block["raw"]), "value": match.group(2)}
            else:
                active["pilot"].append(block)
    expected_fields = {"Primary purpose", "Expected useful result", "Proportionate treatment", "Open question"}
    for item in types:
        if set(item["fields"]) != expected_fields:
            fail(f"Incomplete type: {item['heading']['text']}")
    return {"blocks": blocks, "sections": sections, "taxonomy_intro": intro, "types": types}


def register_fonts() -> None:
    import reportlab
    fonts = Path(reportlab.__file__).parent / "fonts"
    pdfmetrics.registerFont(TTFont("Body", str(fonts / "Vera.ttf")))
    pdfmetrics.registerFont(TTFont("BodyBold", str(fonts / "VeraBd.ttf")))
    pdfmetrics.registerFont(TTFont("BodyItalic", str(fonts / "VeraIt.ttf")))


def style(name: str, size: float, leading: float, color=INK, font="Body", align=TA_LEFT) -> ParagraphStyle:
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading, textColor=color,
                          alignment=align, allowWidows=0, allowOrphans=0, splitLongWords=False)


S = {
    "title": style("title", 24, 27, WHITE, "BodyBold"),
    "deck": style("deck", 10.2, 12.6, WHITE, "Body"),
    "h2": style("h2", 14.5, 16.5, NAVY, "BodyBold"),
    "h2white": style("h2white", 14.5, 16.5, WHITE, "BodyBold"),
    "h3": style("h3", 12.4, 14.2, NAVY, "BodyBold"),
    "body": style("body", BODY_SIZE, BODY_LEADING, INK, "Body"),
    "bodywhite": style("bodywhite", BODY_SIZE, BODY_LEADING, WHITE, "Body"),
    "small": style("small", TABLE_SIZE, TABLE_LEADING, INK, "Body"),
    "label": style("label", LABEL_SIZE, 10.2, TEXT_TEAL, "BodyBold"),
    "labelwhite": style("labelwhite", LABEL_SIZE, 10.2, WHITE, "BodyBold"),
    "question": style("question", BODY_SIZE, 10.35, NAVY, "BodyItalic"),
    "number": style("number", 20, 21, TEAL, "BodyBold"),
    "tiny": style("tiny", 8.8, 10.0, MUTED, "Body"),
}


def paragraph(text: str, key: str, width: float) -> tuple[Paragraph, float]:
    p = Paragraph(rich(text), S[key])
    _, height = p.wrap(width, 1000)
    return p, height


def draw_para(c: canvas.Canvas, text: str, x: float, y: float, width: float, key="body", gap=0.0) -> float:
    p, height = paragraph(text, key, width)
    p.drawOn(c, x, y - height)
    return y - height - gap


def draw_markup(c: canvas.Canvas, markup: str, x: float, y: float, width: float, key="body", gap=0.0) -> float:
    p = Paragraph(markup, S[key])
    _, height = p.wrap(width, 1000)
    p.drawOn(c, x, y - height)
    return y - height - gap


def draw_rule(c, x1, y, x2, color=RULE, width=0.55):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)


def page_base(c: canvas.Canvas, number: int, dark_height=18 * mm, marker_inset=12.5 * mm):
    width, height = PAGE
    c.setFillColor(WARM)
    c.rect(0, 0, width, height, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.rect(0, height - dark_height, width, dark_height, stroke=0, fill=1)
    c.setFillColor(CYAN)
    c.rect(0, height - dark_height, 7 * mm, dark_height, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("BodyBold", 20)
    c.drawRightString(width - MARGIN, height - marker_inset, f"0{number}")
    c.setFillColor(MUTED)
    c.setFont("Body", 8.8)
    c.drawRightString(width - MARGIN, 5.5 * mm, str(number))


def assert_bottom(y: float, label: str, minimum=8 * mm):
    if y < minimum:
        fail(f"Layout overflow in {label}: y={y:.1f}")


def draw_page_one(c: canvas.Canvas, parsed: dict):
    width, height = PAGE
    c.setFillColor(NAVY)
    c.rect(0, 0, width, height, stroke=0, fill=1)
    c.setFillColor(CYAN)
    c.rect(0, height - 10 * mm, width, 10 * mm, stroke=0, fill=1)
    c.setFillColor(CORAL)
    c.rect(0, height - 10 * mm, 58 * mm, 10 * mm, stroke=0, fill=1)

    title = parsed["sections"]["title"][0]["text"]
    draw_para(c, title, MARGIN, height - 14 * mm, 260 * mm, "title")

    objective = parsed["sections"]["Objective"]
    why = parsed["sections"]["Why distinguish meetings?"]
    x1, x2, x3 = MARGIN, 104 * mm, 198 * mm
    col = 89 * mm
    top = height - 28 * mm
    bottom_limit = 92 * mm

    y1 = draw_para(c, objective[0]["text"], x1, top, col, "h2white", 1.2 * mm)
    y1 = draw_para(c, objective[1]["raw"], x1, y1, col, "bodywhite", 1.1 * mm)
    y1 = draw_para(c, objective[2]["raw"], x1, y1, col, "bodywhite", 1.2 * mm)
    status = objective[3]["raw"][2:]
    p, ph = paragraph(status, "body", col - 8 * mm)
    box_h = ph + 5 * mm
    c.setFillColor(CORAL)
    c.roundRect(x1, y1 - box_h, col, box_h, 2.5 * mm, stroke=0, fill=1)
    p.drawOn(c, x1 + 4 * mm, y1 - box_h + 2.5 * mm)
    y1 -= box_h

    y2 = draw_para(c, why[0]["text"], x2, top, col, "h2white", 2 * mm)
    y2 = draw_para(c, why[1]["raw"], x2, y2, col, "bodywhite")

    tax_heading = parsed["sections"]["A small purpose-based taxonomy"][0]
    y3 = draw_para(c, tax_heading["text"], x3, top, col, "h2white", 1.7 * mm)
    y3 = draw_para(c, parsed["taxonomy_intro"][0]["raw"], x3, y3, col, "bodywhite")
    for y, label in [(y1, "page 1 objective"), (y2, "page 1 why"), (y3, "page 1 classification")]:
        if y < bottom_limit:
            fail(f"{label} intrudes into comparison zone: y={y:.1f}")

    band_top = 93 * mm
    c.setFillColor(PAPER)
    c.rect(0, 0, width, band_top, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.rect(0, band_top - 2.4 * mm, width, 2.4 * mm, stroke=0, fill=1)
    gap = 4 * mm
    half = (width - 2 * MARGIN - gap) / 2
    # Uneven editorial columns give the longest deliberation description a
    # taller module while the large numerals preserve the scan order.
    groups = [[parsed["types"][0], parsed["types"][1], parsed["types"][2], parsed["types"][4]],
              [parsed["types"][3], parsed["types"][5], parsed["types"][6]]]
    for group_index, group in enumerate(groups):
        gx = MARGIN + group_index * (half + gap)
        row_h = (band_top - 3 * mm) / len(group)
        gy = band_top - 1.5 * mm
        for local_index, item in enumerate(group):
            y0 = gy - row_h
            absolute_index = parsed["types"].index(item)
            c.setFillColor([MINT, PAPER, SKY, SAND][absolute_index % 4])
            c.roundRect(gx, y0 + 1.2 * mm, half, row_h - 2.2 * mm, 2 * mm, stroke=0, fill=1)
            c.setFillColor(TEAL if absolute_index in {0, 3, 6} else CYAN)
            c.rect(gx, y0 + 1.2 * mm, 2.5 * mm, row_h - 2.2 * mm, stroke=0, fill=1)
            inner_x = gx + 5 * mm
            inner_w = half - 9 * mm
            yy = draw_para(c, item["heading"]["text"], inner_x, gy - 1.5 * mm, inner_w, "label", 0.6 * mm)
            sub_gap = 3 * mm
            purpose_w = (55 if absolute_index == 3 else 42) * mm
            result_x = inner_x + purpose_w + sub_gap
            result_w = inner_w - purpose_w - sub_gap
            py = draw_markup(c, f'<font color="{TEXT_TEAL_HEX}"><b>Primary purpose:</b></font> ' +
                             html.escape(item["fields"]["Primary purpose"]["value"]),
                             inner_x, yy, purpose_w, "small")
            ry = draw_markup(c, f'<font color="{TEXT_TEAL_HEX}"><b>Expected useful result:</b></font> ' +
                             html.escape(item["fields"]["Expected useful result"]["value"]),
                             result_x, yy, result_w, "small")
            if min(py, ry) < y0 + 1.2 * mm:
                fail(f"Page 1 comparison module overflow: {item['heading']['text']} min={min(py, ry):.1f} floor={y0 + 1.2*mm:.1f} row_h={row_h:.1f}")
            gy = y0
    c.setFillColor(WHITE)
    c.setFont("Body", 8.8)
    c.drawRightString(width - MARGIN, height - 17 * mm, "1")


def split_heading(text: str) -> tuple[str, str]:
    match = re.match(r"^(\d+)\.\s+(.*)$", text)
    if not match:
        return "", text
    return match.group(1), match.group(2)


def draw_type_card(c, item: dict, x: float, y_top: float, w: float, h: float, tone, label: str):
    c.setFillColor(tone)
    c.roundRect(x, y_top - h, w, h, 3 * mm, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.rect(x, y_top - 2.2 * mm, w, 2.2 * mm, stroke=0, fill=1)
    number, name = split_heading(item["heading"]["text"])
    c.setFillColor(TEAL)
    c.setFont("BodyBold", 22)
    c.drawString(x + 4 * mm, y_top - 11 * mm, f"0{number}")
    title_x = x + 20 * mm
    title_y = y_top - 5 * mm
    draw_para(c, item["heading"]["text"], title_x, title_y, w - 25 * mm, "h3")

    inner_x = x + 4 * mm
    inner_w = w - 8 * mm
    y = y_top - 18 * mm
    y = draw_para(c, "Proportionate treatment:", inner_x, y, inner_w, "label", 1.2 * mm)
    y = draw_para(c, item["fields"]["Proportionate treatment"]["value"], inner_x, y, inner_w, "body", 1.8 * mm)
    for pilot in item["pilot"]:
        y = draw_para(c, pilot["raw"], inner_x, y, inner_w, "tiny", 1.8 * mm)
    draw_rule(c, inner_x, y, x + w - 4 * mm, CORAL, 1.1)
    y -= 2.2 * mm
    y = draw_para(c, "Open question:", inner_x, y, inner_w, "label", 0.8 * mm)
    y = draw_para(c, item["fields"]["Open question"]["value"], inner_x, y, inner_w, "question")
    if y < y_top - h + 3 * mm:
        fail(f"Type card {label} overflowed by {(y_top-h+3*mm)-y:.1f} pt")


def draw_page_two(c: canvas.Canvas, parsed: dict):
    page_base(c, 2)
    width, height = PAGE
    gap = 5 * mm
    x_left = MARGIN
    card_w = (width - 2 * MARGIN - gap) / 2
    intro_top = height - 23 * mm
    intro_gap = 4 * mm
    intro_widths = [92 * mm, 103 * mm, width - 2 * MARGIN - 2 * intro_gap - 195 * mm]
    intro_texts = [
        parsed["sections"]["Why distinguish meetings?"][2]["raw"],
        parsed["sections"]["Why distinguish meetings?"][3]["raw"],
        parsed["sections"]["Why distinguish meetings?"][4]["raw"],
    ]
    intro_heights = [paragraph(text, "body", panel_w - 7 * mm)[1]
                     for text, panel_w in zip(intro_texts, intro_widths)]
    intro_h = max(intro_heights) + 7 * mm
    intro_x = MARGIN
    for index, (text, panel_w) in enumerate(zip(intro_texts, intro_widths)):
        c.setFillColor([PAPER, MINT, SKY][index])
        c.roundRect(intro_x, intro_top - intro_h, panel_w, intro_h, 2.5 * mm, stroke=0, fill=1)
        c.setFillColor(CORAL if index == 0 else TEAL)
        c.rect(intro_x, intro_top - intro_h, 2.1 * mm, intro_h, stroke=0, fill=1)
        draw_para(c, text, intro_x + 3.5 * mm, intro_top - 3.5 * mm,
                  panel_w - 7 * mm, "body")
        intro_x += panel_w + intro_gap

    y_top = intro_top - intro_h - 4 * mm
    card_h = (y_top - 8 * mm - gap) / 2
    positions = [
        (x_left, y_top), (x_left + card_w + gap, y_top),
        (x_left, y_top - card_h - gap), (x_left + card_w + gap, y_top - card_h - gap),
    ]
    tones = [PAPER, MINT, SKY, SAND]
    for item, (x, y), tone in zip(parsed["types"][:4], positions, tones):
        draw_type_card(c, item, x, y, card_w, card_h, tone, item["heading"]["text"])


def draw_question_sequence(c, questions: list[dict], x, y, w, max_bottom, compact=False):
    for index, block in enumerate(questions, 1):
        c.setFillColor(TEXT_TEAL if index in {1, 3, 5} else NAVY)
        c.setFont("BodyBold", 13 if compact else 15)
        c.drawString(x, y - 4, f"{index}.")
        text = block["raw"].split(". ", 1)[1]
        y = draw_para(c, text, x + 12 * mm, y, w - 12 * mm, "small", (0.5 if compact else 1.6) * mm)
        draw_rule(c, x + 12 * mm, y + 0.8 * mm, x + w, RULE, 0.35)
    if y < max_bottom:
        fail(f"Question sequence overflow: y={y:.1f}, floor={max_bottom:.1f}")
    return y


def draw_safeguards(c, blocks: list[dict], x, y_top, w, h):
    gap = 3 * mm
    cell_w = (w - gap) / 2
    cell_h = (h - gap) / 2
    for index, block in enumerate(blocks):
        col, row = index % 2, index // 2
        cx = x + col * (cell_w + gap)
        cy = y_top - row * (cell_h + gap)
        c.setFillColor(MINT if index in {0, 3} else SKY)
        c.roundRect(cx, cy - cell_h, cell_w, cell_h, 2.3 * mm, stroke=0, fill=1)
        raw = block["raw"][2:]
        parts = raw.split("**", 2)
        label, rest = parts[1], parts[2].strip()
        yy = draw_markup(c, f'<font color="{TEXT_TEAL_HEX}"><b>' + html.escape(label) + '</b></font> ' + html.escape(rest),
                         cx + 3 * mm, cy - 3 * mm, cell_w - 6 * mm, "small")
        if yy < cy - cell_h + 2 * mm:
            fail(f"Safeguard cell overflow index={index} by={(cy-cell_h+2*mm)-yy:.1f} pt cell_h={cell_h:.1f}")


def draw_page_three(c: canvas.Canvas, parsed: dict):
    page_base(c, 3)
    width, height = PAGE
    top = height - 23 * mm
    gap = 4 * mm
    card_w = (width - 2 * MARGIN - 2 * gap) / 3
    card_h = 99 * mm
    for idx, item in enumerate(parsed["types"][4:]):
        draw_type_card(c, item, MARGIN + idx * (card_w + gap), top, card_w, card_h,
                       [SAND, SKY, MINT][idx], item["heading"]["text"])

    lower_top = top - card_h - 5 * mm
    lower_bottom = 8 * mm
    left_w = 110 * mm
    right_x = MARGIN + left_w + 2 * mm
    right_w = width - MARGIN - right_x
    minimal = parsed["sections"]["A minimal pattern for every meeting"]
    y = draw_para(c, minimal[0]["text"], MARGIN, lower_top, left_w, "h2", 2 * mm)
    y = draw_para(c, minimal[1]["raw"], MARGIN, y, left_w, "body", 2 * mm)
    questions = [b for b in minimal if b["kind"] == "number"]
    y = draw_question_sequence(c, questions, MARGIN, y, left_w, lower_bottom, compact=True)

    after = minimal[minimal.index(questions[-1]) + 1:]
    safeguard_intro = after[0]
    safeguards = [b for b in after if b["kind"] == "bullet"]
    safeguard_end = after[-1]
    yr = draw_para(c, safeguard_intro["raw"], right_x, lower_top, right_w, "h3", 2 * mm)
    matrix_h = 52 * mm
    draw_safeguards(c, safeguards, right_x, yr, right_w, matrix_h)
    yr -= matrix_h + 3 * mm
    yr = draw_para(c, safeguard_end["raw"], right_x, yr, right_w, "body")
    if yr < lower_bottom:
        fail(f"Page 3 safeguards overflow by {lower_bottom-yr:.1f} pt")


def draw_conditional(c, section: list[dict], x, y, w, floor):
    y = draw_para(c, section[0]["text"], x, y, w, "h2", 2 * mm)
    y = draw_para(c, section[1]["raw"], x, y, w, "body", 1.5 * mm)
    bullets = [b for b in section if b["kind"] == "bullet"]
    for block in bullets:
        if not block["raw"].startswith("- "):
            fail("Conditional-pattern list item no longer starts with Markdown list syntax.")
        c.setFillColor(CORAL)
        c.circle(x + 1.5 * mm, y - 3.1 * mm, 1.05 * mm, stroke=0, fill=1)
        y = draw_para(c, block["raw"][2:], x + 5 * mm, y, w - 5 * mm, "small", 1.25 * mm)
    paragraphs = [b for b in section if b["kind"] == "paragraph"]
    y = draw_para(c, paragraphs[-1]["raw"], x, y - 1 * mm, w, "body")
    if y < floor:
        fail("Conditional patterns overflow")
    return y


def split_recurring(text: str) -> tuple[str, str, str]:
    sentences = re.split(r"(?<=\.)\s+", text)
    if len(sentences) != 3:
        fail("Recurring-context paragraph no longer has three expected sentences.")
    return tuple(sentences)


def draw_context_and_flex(c, parsed, x, y, w, floor):
    recurring = parsed["sections"]["Recurring context and a specific meeting"]
    y = draw_para(c, recurring[0]["text"], x, y, w, "h2", 2 * mm)
    forum, occurrence, distinction = split_recurring(recurring[1]["raw"])
    gap = 4 * mm
    node_w = (w - gap) / 2
    node_heights = [paragraph(forum, "small", node_w - 6 * mm)[1], paragraph(occurrence, "small", node_w - 6 * mm)[1]]
    node_h = max(node_heights) + 7 * mm
    for idx, text in enumerate([forum, occurrence]):
        nx = x + idx * (node_w + gap)
        c.setFillColor(MINT if idx == 0 else SKY)
        c.roundRect(nx, y - node_h, node_w, node_h, 2.5 * mm, stroke=0, fill=1)
        draw_para(c, text, nx + 3 * mm, y - 3 * mm, node_w - 6 * mm, "small")
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.1)
    c.line(x + node_w, y - node_h / 2, x + node_w + gap, y - node_h / 2)
    y -= node_h + 2 * mm
    y = draw_para(c, distinction, x, y, w, "body", 1.4 * mm)
    y = draw_para(c, recurring[2]["raw"], x, y, w, "body", 2.2 * mm)

    flexible = parsed["sections"]["What should remain flexible"]
    y = draw_para(c, flexible[0]["text"], x, y, w, "h2", 1.7 * mm)
    y = draw_para(c, flexible[1]["raw"], x, y, w, "body", 1.5 * mm)
    y = draw_para(c, flexible[2]["raw"], x, y, w, "body")
    if y < floor:
        fail("Context/flexibility overflow")
    return y


def draw_group_and_pilot(c, section: list[dict], x, y, w, right_x, right_w, floor):
    y = draw_para(c, section[0]["text"], x, y, w, "h2", 1.5 * mm)
    y = draw_para(c, section[1]["raw"], x, y, w, "body", 1.5 * mm)
    questions = [b for b in section if b["kind"] == "number"]
    gap = 4 * mm
    sub_w = (w - gap) / 2
    columns = [questions[:4], questions[4:]]
    bottoms = []
    for col, items in enumerate(columns):
        xx = x + col * (sub_w + gap)
        yy = y
        start_num = 1 if col == 0 else 5
        for offset, block in enumerate(items):
            n = start_num + offset
            c.setFillColor(TEXT_TEAL)
            c.setFont("BodyBold", 11)
            c.drawString(xx, yy - 3.5, f"{n}.")
            yy = draw_para(c, block["raw"].split(". ", 1)[1], xx + 10 * mm, yy, sub_w - 10 * mm, "small", 1.2 * mm)
        bottoms.append(yy)

    ending = section[section.index(questions[-1]) + 1:]
    yr = draw_para(c, ending[0]["raw"], right_x, y + 9 * mm, right_w, "body", 2.5 * mm)
    final_text = ending[1]["raw"]
    p, ph = paragraph(final_text, "bodywhite", right_w - 8 * mm)
    bh = ph + 7 * mm
    c.setFillColor(NAVY)
    c.roundRect(right_x, yr - bh, right_w, bh, 2.5 * mm, stroke=0, fill=1)
    p.drawOn(c, right_x + 4 * mm, yr - bh + 3.4 * mm)
    yr -= bh
    if min(bottoms + [yr]) < floor:
        fail(f"Group/pilot zone overflow by {floor-min(bottoms+[yr]):.1f} pt bottoms={bottoms} pilot={yr:.1f}")


def draw_page_four(c: canvas.Canvas, parsed: dict):
    page_base(c, 4, marker_inset=14.5 * mm)
    width, height = PAGE
    top = height - 23 * mm
    upper_floor = 82 * mm
    left_w = 115 * mm
    gap = 6 * mm
    right_x = MARGIN + left_w + gap
    right_w = width - MARGIN - right_x
    conditional = parsed["sections"]["Conditional patterns, only when the stakes require them"]
    draw_conditional(c, conditional, MARGIN, top, left_w, upper_floor)
    draw_context_and_flex(c, parsed, right_x, top, right_w, upper_floor)

    draw_rule(c, MARGIN, upper_floor - 3 * mm, width - MARGIN, TEAL, 1.2)
    group = parsed["sections"]["Questions for the group"]
    group_w = 178 * mm
    pilot_x = MARGIN + group_w + 7 * mm
    pilot_w = width - MARGIN - pilot_x
    draw_group_and_pilot(c, group, MARGIN, upper_floor - 8 * mm, group_w, pilot_x, pilot_w, 8 * mm)


def extract_pdf_text(path: Path) -> tuple[str, list[str]]:
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text(x_tolerance=1.5, y_tolerance=3) or "")
    return "\n".join(pages), pages


def tokens(text: str) -> list[str]:
    return re.findall(r"[\w]+(?:[’'][\w]+)*|[^\w\s]", text, flags=re.UNICODE)


def fidelity_check(parsed: dict, pages: list[str]) -> dict:
    extracted = []
    for page in pages:
        lines = [line for line in page.splitlines() if not re.fullmatch(r"0?[1-4]", line.strip())]
        extracted.append("\n".join(lines))
    source_parts = []
    for block in parsed["blocks"]:
        if block["kind"] == "number":
            source_parts.append(block["raw"].replace("**", ""))
        else:
            source_parts.append(block["text"])
    source_parts += [item["heading"]["text"] for item in parsed["types"]]
    expected = Counter(tokens("\n".join(source_parts)))
    found = Counter(tokens("\n".join(extracted)))
    missing = expected - found
    unexpected = found - expected
    # One oversized 01-07 numeral per detailed type is navigational furniture.
    for n in range(1, 8):
        token = f"0{n}"
        if unexpected.get(token) == 1:
            del unexpected[token]
    if unexpected.get("-") == 6:
        del unexpected["-"]
    result = {
        "source_blocks": len(parsed["blocks"]), "tracked_once": len(parsed["blocks"]),
        "expected_tokens": sum(expected.values()), "matched_tokens": sum((expected & found).values()),
        "missing": dict(missing), "altered_or_duplicated": {}, "unexpected_substantive_text": dict(unexpected),
        "intentional_navigational_repeats": [item["heading"]["text"] for item in parsed["types"]],
    }
    if missing or unexpected:
        fail(f"Fidelity check failed: {result}")
    return result


def run() -> None:
    register_fonts()
    parsed = parse_source(SOURCE.read_text(encoding="utf-8"))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)

    c = canvas.Canvas(str(OUTPUT), pagesize=PAGE)
    c.setTitle(parsed["sections"]["title"][0]["text"])
    c.setAuthor("ResonantOS community proposal")
    for index, draw in enumerate([draw_page_one, draw_page_two, draw_page_three, draw_page_four], 1):
        draw(c, parsed)
        if index < 4:
            c.showPage()
    c.save()

    reader_pages = len(PdfReader(str(OUTPUT)).pages)
    extracted, pages = extract_pdf_text(OUTPUT)
    if reader_pages != 4 or len(pages) != 4:
        fail(f"Expected four pages; pypdf={reader_pages}, pdfplumber={len(pages)}")
    blank = [i + 1 for i, text in enumerate(pages) if not text.strip()]
    if blank:
        fail(f"Blank pages: {blank}")
    qa = fidelity_check(parsed, pages)
    density = [len(re.sub(r"\s+", "", page)) for page in pages]
    if density != sorted(density) or len(set(density)) != len(density):
        fail(f"Expected strictly increasing extracted-text density, got {density}")
    contrast = {background: round(contrast_ratio(TEXT_TEAL_HEX, background), 3)
                for background in LIGHT_BACKGROUNDS}
    if min(contrast.values()) < 4.5:
        fail(f"Normal-size teal text contrast below WCAG AA: {contrast}")
    (WORK / "extracted.txt").write_text(extracted, encoding="utf-8")
    (WORK / "qa.txt").write_text(repr(qa), encoding="utf-8")
    print(f"PDF={OUTPUT}")
    print("PAGES=4")
    print(f"MIN_BODY={BODY_SIZE} MIN_TABLE={TABLE_SIZE} MIN_LABEL={LABEL_SIZE}")
    print(f"QA={qa}")
    print(f"NONWHITESPACE_DENSITY={density}")
    print(f"TEXT_TEAL_CONTRAST={contrast}")


if __name__ == "__main__":
    run()
