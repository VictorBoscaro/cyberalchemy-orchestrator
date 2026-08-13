from pathlib import Path
from math import atan2, cos, sin

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parent
FONT_DIR = ROOT.parent / "tools" / "fonts"
OUT = ROOT / "systems-and-categories-drawings.pdf"

PAGE_W, PAGE_H = A4
INK = colors.HexColor("#25292D")
BLUE = colors.HexColor("#52677A")
GOLD = colors.HexColor("#A58A63")
QUIET = colors.HexColor("#BCC5CA")
PALE = colors.HexColor("#E8ECEE")
WHITE = colors.white

pdfmetrics.registerFont(TTFont("EBG", str(FONT_DIR / "EBGaramond.ttf")))
pdfmetrics.registerFont(TTFont("EBGI", str(FONT_DIR / "EBGaramond-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Inter", str(FONT_DIR / "Inter.ttf")))


NOTES = [
    (
        "SUCCESSIVE DESCRIPTIONS",
        "REPRESENTATION / ONE",
        [
            ("PURPOSE", "Let one concrete situation carry the reader from representation to reframing."),
            ("WHY IT MATTERS", "Inquiry changes when different relations become consequential, before formal language begins."),
            ("CLAIM", "An episode can remain recognizable while different selections make different questions and actions plausible."),
            ("DRAWING", "One network appears three times. Acquisition, retention, then promise and capacity become salient; the rest stays visible."),
        ],
    ),
    (
        "ANALOGY AND TRANSLATION",
        "PRESERVATION / ONE",
        [
            ("PURPOSE", "Show the threshold between productive resemblance and an inspectable translation."),
            ("WHY IT MATTERS", "Analogy directs attention, but trust requires stating what a proposed correspondence must preserve."),
            ("CLAIM", "Analogy suggests a correspondence. Translation adds preservation obligations that can be tested and can fail."),
            ("DRAWING", "Two structured descriptions face each other. The hollow gate marks an obligation to check, never a successful preservation."),
        ],
    ),
    (
        "EARNED FORMALIZATION",
        "DOMAIN LANGUAGE / ONE",
        [
            ("PURPOSE", "Show how a domain language can acquire structure without following a compulsory ladder."),
            ("WHY IT MATTERS", "Formal structure matters only when it preserves a consequential distinction or constrains a real relation."),
            ("CLAIM", "Vocabulary may become typed and compositional as obligations arise. Any adequate stage can be a legitimate stopping point."),
            ("DRAWING", "A path gains gates as obligations appear. Quiet exits show that further formalization remains conditional."),
        ],
    ),
    (
        "RUPTURE AND REVISION",
        "REVISION / ONE",
        [
            ("PURPOSE", "Distinguish a limitation of the language from an incorrect instance and from its possible repairs."),
            ("WHY IT MATTERS", "A useful representation can reach a new boundary without becoming retroactively useless."),
            ("CLAIM", "A new task can expose a distinction the language cannot express. Rupture constrains revision but selects no repair."),
            ("DRAWING", "A sustained route reaches a hollow interruption. Earlier use remains visible; two candidate revisions leave the break unresolved."),
        ],
    ),
    (
        "DIFFERENT LENSES",
        "INVESTIGATION / ONE",
        [
            ("PURPOSE", "Show how modes of investigation reorganize attention around the same episode."),
            ("WHY IT MATTERS", "A lens changes which relations govern the next question without claiming to exhaust the episode."),
            ("CLAIM", "Systemic inquiry foregrounds relations over time; categorical inquiry foregrounds descriptions, composition, mappings, and preservation."),
            ("DRAWING", "One field follows promise, capacity, delay, and return. The other compares descriptions and asks what mappings and composed paths preserve."),
        ],
    ),
    (
        "LANGUAGES ACROSS WORK",
        "INFRASTRUCTURE / ONE",
        [
            ("PURPOSE", "Show several languages participating unevenly across intention, orchestration, bounded work, and effect."),
            ("WHY IT MATTERS", "A domain language is not confined to local execution; recoverability is not universal presence."),
            ("CLAIM", "Languages cross different parts of work with different scope and precision. Their limits and mismatches must remain recoverable."),
            ("DRAWING", "Language fields cross selected moments. Filled junctions mark translation; open ones mark unresolved mismatch; context remains reachable below."),
        ],
    ),
]


def arrow(c, x1, y1, x2, y2, color=BLUE, width=1.15, head=5, dash=None):
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(width)
    if dash:
        c.setDash(*dash)
    c.line(x1, y1, x2, y2)
    angle = atan2(y2 - y1, x2 - x1)
    c.line(x2, y2, x2 - head * cos(angle - .48), y2 - head * sin(angle - .48))
    c.line(x2, y2, x2 - head * cos(angle + .48), y2 - head * sin(angle + .48))
    c.restoreState()


def node(c, x, y, color=BLUE, radius=4, hollow=False, quiet=False):
    c.saveState()
    c.setLineWidth(1.1)
    c.setStrokeColor(color if not quiet else QUIET)
    c.setFillColor(WHITE if hollow else (color if not quiet else PALE))
    c.circle(x, y, radius, fill=1, stroke=1)
    c.restoreState()


def label(c, text, x, y, color=BLUE, size=9, align="center"):
    c.saveState()
    c.setFillColor(color)
    c.setFont("Inter", size)
    if align == "left":
        c.drawString(x, y, text)
    elif align == "right":
        c.drawRightString(x, y, text)
    else:
        c.drawCentredString(x, y, text)
    c.restoreState()


def paragraph(c, text, x, y_top, width, style):
    p = Paragraph(text, style)
    _, h = p.wrap(width, 200)
    p.drawOn(c, x, y_top - h)
    return h


BODY = ParagraphStyle(
    "note", fontName="EBG", fontSize=11.2, leading=13.4,
    textColor=INK, spaceAfter=0,
)


def page_frame(c, number, title, family, notes):
    c.setFillColor(WHITE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setStrokeColor(PALE)
    c.setLineWidth(.45)
    c.line(40, PAGE_H - 40, 63, PAGE_H - 40)
    c.line(40, PAGE_H - 40, 40, PAGE_H - 63)
    c.line(PAGE_W - 40, 40, PAGE_W - 63, 40)
    c.line(PAGE_W - 40, 40, PAGE_W - 40, 63)

    label(c, family, 60, PAGE_H - 66, GOLD, 8.2, "left")
    display_title = title.title().replace(" And ", " and ").replace(" Across ", " across ")
    c.setFillColor(INK)
    c.setFont("EBG", 27)
    c.drawString(60, PAGE_H - 101, display_title)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(60, PAGE_H - 117, 148, PAGE_H - 117)

    col_w = 210
    positions = [(60, 273), (326, 258), (72, 147), (326, 133)]
    for (heading, copy), (x, y) in zip(notes, positions):
        c.setStrokeColor(GOLD)
        c.setLineWidth(.75)
        c.line(x, y + 25, x + 58, y + 25)
        label(c, heading, x, y + 9, GOLD, 8.2, "left")
        paragraph(c, copy, x, y - 2, col_w, BODY)

    label(c, f"{number:02d} / {title.upper()}", PAGE_W - 72, 26, QUIET, 7.2, "right")


def network(c, cx, cy, accents, stage):
    pts = {
        "acquisition": (cx - 42, cy + 22),
        "promise": (cx + 2, cy + 43),
        "capacity": (cx + 44, cy + 12),
        "delay": (cx + 25, cy - 35),
        "return": (cx - 33, cy - 28),
    }
    edges = [
        ("acquisition", "promise"), ("promise", "capacity"),
        ("capacity", "delay"), ("delay", "return"),
        ("return", "acquisition"), ("promise", "delay"),
    ]
    for a, b in edges:
        active = (a, b) in accents
        arrow(c, *pts[a], *pts[b], GOLD if active else QUIET, 1.45 if active else .65, 4)
    for name, (x, y) in pts.items():
        active = any(name in pair for pair in accents)
        node(c, x, y, GOLD if active else QUIET, 3.8, hollow=not active, quiet=not active)
    label(c, stage, cx, cy - 62, INK, 9.2)


def drawing_successive(c):
    y = 535
    c.setStrokeColor(PALE)
    c.ellipse(55, 420, 540, 650, fill=0, stroke=1)
    network(c, 139, y, {("acquisition", "promise"), ("return", "acquisition")}, "ACQUISITION")
    network(c, 298, y, {("delay", "return"), ("return", "acquisition")}, "RETENTION")
    network(c, 457, y, {("promise", "capacity"), ("capacity", "delay"), ("promise", "delay")}, "PROMISE / CAPACITY")
    label(c, "same episode; a different relation governs the next question", PAGE_W / 2, 425, BLUE, 9)


def small_graph(c, x, y, color):
    pts = [(x, y + 35), (x + 46, y + 50), (x + 86, y + 8), (x + 30, y - 19)]
    for a, b in [(0, 1), (1, 2), (0, 3), (3, 2)]:
        arrow(c, *pts[a], *pts[b], color, 1, 4)
    for px, py in pts:
        node(c, px, py, color, 4)


def drawing_analogy(c):
    y = 515
    small_graph(c, 82, y, BLUE)
    small_graph(c, 427, y, GOLD)
    label(c, "DESCRIPTION A", 125, 444, BLUE, 9)
    label(c, "DESCRIPTION B", 470, 444, GOLD, 9)
    arrow(c, 218, 558, 375, 558, QUIET, 1, 5, (5, 5))
    label(c, "analogy suggests a correspondence", PAGE_W / 2, 573, BLUE, 9)
    arrow(c, 218, 497, 375, 497, INK, 1.2, 5)
    node(c, PAGE_W / 2, 497, GOLD, 4.2, hollow=True)
    label(c, "declared structure must be preserved", PAGE_W / 2, 477, INK, 9)
    label(c, "OBLIGATION TO CHECK - NOT A RESULT", PAGE_W / 2, 427, GOLD, 9)


def gate(c, x, y):
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(x, y - 9, x, y - 3)
    c.line(x, y + 3, x, y + 9)
    c.line(x - 4, y - 3, x + 4, y - 3)
    c.line(x - 4, y + 3, x + 4, y + 3)
    c.restoreState()


def drawing_formalization(c):
    y = 530
    xs = [105, 280, 463]
    stages = ["ORDINARY DISTINCTIONS", "TYPED RELATIONS", "COMPOSITIONAL LAWS"]
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.15)
    c.line(xs[0], y, xs[-1], y)
    arrow(c, xs[0], y, xs[-1], y, BLUE, 1.15, 5)
    gate(c, 194, y)
    gate(c, 372, y)
    for x, stage in zip(xs, stages):
        node(c, x, y, BLUE if x != xs[-1] else GOLD, 4.5, hollow=True)
        label(c, stage, x, y + 24, BLUE if x != xs[-1] else GOLD, 9)
        c.setStrokeColor(QUIET)
        c.setLineWidth(.75)
        c.line(x, y - 6, x, y - 48)
        node(c, x, y - 53, QUIET, 3.4, hollow=True, quiet=True)
        label(c, "adequate here", x, y - 72, BLUE, 9)
    label(c, "new obligations justify the next gate", PAGE_W / 2, 422, GOLD, 9)


def drawing_rupture(c):
    y = 520
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.35)
    c.line(75, y, 276, y)
    node(c, 75, y, BLUE, 4)
    node(c, 187, y, BLUE, 4)
    node(c, 283, y, GOLD, 5, hollow=True)
    node(c, 306, y, GOLD, 5, hollow=True)
    label(c, "NEW TASK EXPOSES AN UNEXPRESSIBLE DISTINCTION", 293, y + 31, GOLD, 9)
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.setDash(5, 5)
    c.bezier(311, y + 4, 350, y + 8, 390, y + 54, 515, y + 54)
    c.bezier(311, y - 4, 350, y - 8, 390, y - 54, 515, y - 54)
    c.restoreState()
    node(c, 515, y + 54, GOLD, 4, hollow=True)
    node(c, 515, y - 54, GOLD, 4, hollow=True)
    label(c, "candidate revision", 456, y + 72, BLUE, 9)
    label(c, "candidate revision", 456, y - 78, BLUE, 9)
    label(c, "earlier adequacy remains visible", 168, 435, BLUE, 9)


def drawing_lenses(c):
    c.setStrokeColor(PALE)
    c.roundRect(57, 425, 225, 205, 8, fill=0, stroke=1)
    c.roundRect(313, 425, 225, 205, 8, fill=0, stroke=1)
    label(c, "SYSTEMIC LENS", 75, 606, BLUE, 9, "left")
    label(c, "CATEGORICAL LENS", 331, 606, GOLD, 9, "left")

    pts = [(90, 540), (150, 570), (220, 536), (205, 472), (125, 474)]
    names = ["promise", "capacity", "delay", "return", "retention"]
    for i in range(len(pts) - 1):
        arrow(c, *pts[i], *pts[i + 1], BLUE, 1.2, 4)
    arrow(c, *pts[-1], *pts[0], BLUE, 1.2, 4)
    for (x, y), name in zip(pts, names):
        node(c, x, y, BLUE, 3.5)
        label(c, name, x, y - 14, BLUE, 9)
    arrow(c, 134, 518, 204, 518, GOLD, 1, 5)
    label(c, "TIME", 169, 526, GOLD, 9)
    label(c, "relations unfold and return", 169, 443, INK, 9)

    left = [(337, 548), (368, 568), (391, 530)]
    right = [(460, 555), (496, 570), (510, 523)]
    for pts2, color in [(left, BLUE), (right, GOLD)]:
        arrow(c, *pts2[0], *pts2[1], color, 1, 4)
        arrow(c, *pts2[1], *pts2[2], color, 1, 4)
        arrow(c, *pts2[0], *pts2[2], QUIET, .8, 4)
        for x, y in pts2:
            node(c, x, y, color, 3.5)
    for (x1, y1), (x2, y2) in zip(left, right):
        c.setStrokeColor(QUIET)
        c.setLineWidth(.7)
        c.line(x1, y1, x2, y2)
    # Preservation gate is attached directly to the central mapping trace.
    node(c, 424, 549, GOLD, 4.2, hollow=True)
    c.setStrokeColor(QUIET)
    c.ellipse(326, 516, 405, 583, fill=0, stroke=1)
    c.ellipse(448, 516, 521, 583, fill=0, stroke=1)
    label(c, "promise", 348, 511, BLUE, 9)
    label(c, "capacity / delay", 486, 511, GOLD, 9)
    c.setStrokeColor(QUIET)
    c.line(424, 544, 424, 491)
    label(c, "WHAT DOES THE MAPPING PRESERVE?", 424, 463, GOLD, 9)
    label(c, "descriptions, composed paths, obligation", 424, 443, INK, 9)


def drawing_languages(c):
    xs = [85, 229, 373, 517]
    names = ["INTENTION", "ORCHESTRATION", "BOUNDED WORK", "EFFECT"]
    for i, (x, name) in enumerate(zip(xs, names)):
        c.setStrokeColor(BLUE if i < 3 else GOLD)
        c.setFillColor(WHITE)
        c.roundRect(x - 47, 487, 94, 42, 5, fill=1, stroke=1)
        label(c, name, x, 503, BLUE if i < 3 else GOLD, 9)
        if i < 3:
            arrow(c, x + 47, 508, xs[i + 1] - 52, 508, QUIET, .8, 4)

    bands = [
        ("HUMAN LANGUAGE", 61, 536, 330, BLUE),
        ("DOMAIN LANGUAGE A", 61, 567, 530, GOLD),
        ("SHARED RELATIONAL LANGUAGE", 250, 597, 524, BLUE),
        ("DOMAIN LANGUAGE B", 356, 458, 526, GOLD),
    ]
    for text, x1, y, x2, color in bands:
        c.setStrokeColor(color)
        c.setLineWidth(2)
        c.line(x1, y, x2, y)
        label(c, text, x1, y + 8, color, 9, "left")
    c.setStrokeColor(QUIET)
    c.setLineWidth(.8)
    c.line(229, 536, 229, 567)
    c.line(373, 567, 373, 597)
    node(c, 229, 551.5, GOLD, 3.7)
    node(c, 373, 582, GOLD, 3.7, hollow=True)
    label(c, "translation", 245, 548, INK, 9, "left")
    label(c, "unresolved mismatch", 373, 617, GOLD, 9)

    c.setFillColor(colors.HexColor("#F7F8F8"))
    c.setStrokeColor(PALE)
    c.roundRect(83, 396, 429, 49, 5, fill=1, stroke=1)
    label(c, "RECOVERABLE CONTEXT", 101, 424, BLUE, 9, "left")
    label(c, "scope, versions, translations, limits, mismatches", 101, 406, INK, 9, "left")
    c.setStrokeColor(QUIET)
    c.setDash(2, 4)
    for x in xs:
        c.line(x, 487, x, 445)
    c.setDash()


DRAWINGS = [
    drawing_successive,
    drawing_analogy,
    drawing_formalization,
    drawing_rupture,
    drawing_lenses,
    drawing_languages,
]


def build():
    c = canvas.Canvas(
        str(OUT), pagesize=A4,
        pageCompression=1,
        title="Systems and Categories - Drawings",
        author="Victor Boscaro",
        subject="Six visual studies for Systems and Categories: Toward Domain Languages",
    )
    c.setTitle("Systems and Categories - Drawings")
    c.setAuthor("Victor Boscaro")
    c.setSubject("Six visual studies for Systems and Categories: Toward Domain Languages")
    for number, ((title, family, notes), draw) in enumerate(zip(NOTES, DRAWINGS), 1):
        page_frame(c, number, title, family, notes)
        draw(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    build()
