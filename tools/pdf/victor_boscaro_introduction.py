from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "pdf" / "victor-boscaro-introduction-one-pager" / "victor-boscaro-introduction.pdf"

PAPER = HexColor("#f4eadc")
PAPER_LIGHT = HexColor("#f8f0e4")
INK = HexColor("#160f0c")
MUTED = HexColor("#5b4a40")
RUST = HexColor("#a93622")
RUST_DARK = HexColor("#792719")
HAIRLINE = HexColor("#b89b84")


def register_fonts():
    fonts = Path("C:/Windows/Fonts")
    pdfmetrics.registerFont(TTFont("Palatino", str(fonts / "pala.ttf")))
    pdfmetrics.registerFont(TTFont("Palatino-Bold", str(fonts / "palab.ttf")))
    pdfmetrics.registerFont(TTFont("Constantia", str(fonts / "constan.ttf")))
    pdfmetrics.registerFont(TTFont("Constantia-Bold", str(fonts / "constanb.ttf")))


def draw_page(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)

    # Quiet page atmosphere inherited from the Work Context editions.
    canvas.setFillColor(Color(0.71, 0.25, 0.15, alpha=0.025))
    canvas.circle(width * 0.77, height * 0.22, 72 * mm, fill=1, stroke=0)
    canvas.setFillColor(Color(1, 1, 1, alpha=0.10))
    canvas.circle(width * 0.82, height * 0.89, 46 * mm, fill=1, stroke=0)

    # Registration-like corner marks.
    canvas.setStrokeColor(Color(0.37, 0.29, 0.24, alpha=0.28))
    canvas.setLineWidth(0.6)
    inset, arm = 10 * mm, 7 * mm
    for x, y, sx, sy in [
        (inset, height - inset, 1, -1),
        (width - inset, height - inset, -1, -1),
        (inset, inset, 1, 1),
        (width - inset, inset, -1, 1),
    ]:
        canvas.line(x, y, x + sx * arm, y)
        canvas.line(x, y, x, y + sy * arm)

    # Footer rule and contact line.
    canvas.setStrokeColor(Color(0.47, 0.13, 0.08, alpha=0.45))
    canvas.setLineWidth(0.55)
    canvas.line(22 * mm, 15.5 * mm, width - 22 * mm, 15.5 * mm)
    canvas.setFont("Constantia", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(22 * mm, 10.7 * mm, "Sao Paulo, Brazil")
    canvas.drawRightString(
        width - 22 * mm,
        10.7 * mm,
        "victorboscaro@gmail.com  /  github.com/VictorBoscaro",
    )
    canvas.restoreState()


def build():
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=17 * mm,
        bottomMargin=20 * mm,
        title="Victor Boscaro - A brief introduction",
        author="Victor Boscaro",
        subject="Professional introduction and current research",
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
    doc.addPageTemplates([PageTemplate(id="one-page", frames=[frame], onPage=draw_page)])

    title = ParagraphStyle(
        "title",
        fontName="Palatino-Bold",
        fontSize=29,
        leading=31,
        textColor=INK,
        spaceAfter=2.4 * mm,
    )
    subtitle = ParagraphStyle(
        "subtitle",
        fontName="Constantia",
        fontSize=10,
        leading=12,
        textColor=RUST_DARK,
        tracking=0.6,
        spaceAfter=8.4 * mm,
    )
    heading = ParagraphStyle(
        "heading",
        fontName="Palatino-Bold",
        fontSize=16,
        leading=18,
        textColor=RUST_DARK,
        spaceBefore=2.5 * mm,
        spaceAfter=2.3 * mm,
        keepWithNext=True,
    )
    body = ParagraphStyle(
        "body",
        fontName="Constantia",
        fontSize=11,
        leading=16,
        textColor=INK,
        alignment=TA_LEFT,
        spaceAfter=4.2 * mm,
        splitLongWords=False,
        allowWidows=0,
        allowOrphans=0,
    )
    skill_label = ParagraphStyle(
        "skill-label",
        fontName="Constantia-Bold",
        fontSize=8.5,
        leading=10.2,
        textColor=RUST_DARK,
        spaceAfter=0.7 * mm,
    )
    skill_text = ParagraphStyle(
        "skill-text",
        fontName="Constantia",
        fontSize=8.3,
        leading=11.2,
        textColor=MUTED,
    )

    story = [
        Spacer(1, 4 * mm),
        Paragraph("Victor Boscaro", title),
        Paragraph("PRODUCT & SYSTEMS BUILDER  /  AI, DATA & EXPERIMENTATION", subtitle),
        Paragraph("How I got here", heading),
        Paragraph(
            "I came to software through experimentation. Game LiveOps taught me to observe, change, and measure "
            "products. Performance marketing taught me to make decisions with noisy data, incomplete attribution, "
            "and external constraints.",
            body,
        ),
        Paragraph(
            "That led me to build analytical and operational tools, including a small ads-operations platform "
            "for Meta Ads. "
            "AI-assisted development expanded what I can build; my strength is connecting business understanding, "
            "experimentation, system design, and implementation.",
            body,
        ),
        Paragraph("What I do", heading),
        Paragraph(
            "I turn uncertain business problems into useful systems that can be tested and improved.",
            body,
        ),
        Table(
            [[
                [Paragraph("CLARIFY", skill_label), Paragraph("Define the business outcome and the decision that matters", skill_text)],
                [Paragraph("ANALYZE", skill_label), Paragraph("Separate causes from symptoms and identify constraints and opportunities", skill_text)],
                [Paragraph("BUILD", skill_label), Paragraph("Create the smallest useful solution and collect the right data from the start", skill_text)],
                [Paragraph("IMPROVE", skill_label), Paragraph("Find bottlenecks, automate work, and allocate resources more effectively", skill_text)],
            ]],
            colWidths=[doc.width / 4.0] * 4,
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), PAPER_LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.55, HAIRLINE),
                ("LINEABOVE", (0, 0), (-1, -1), 1.4, RUST),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.4 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5 * mm),
            ]),
        ),
        Spacer(1, 4 * mm),
        Paragraph("What I am building now", heading),
        Paragraph(
            "With <b>Vladimir</b>, I am developing a domain language for coordinating "
            "work across AI agents. The research brings together systems thinking, category theory, and epistemology.",
            body,
        ),
        Paragraph(
            "The goal is a system that incorporates a framework for how to think, represent, investigate, decide, "
            "optimize, coordinate, and revise. It would determine what each agent needs at each moment, keeping "
            "local work connected to the larger purpose.",
            body,
        ),
        Paragraph(
            "Rather than treating knowledge as static context, the system would preserve how understanding and "
            "decisions evolve. Today, the system exists as fragmented parts that still need to be "
            "connected, while important parts have yet to be built. It is not a finished platform, "
            "but it already shapes how I design products and multi-agent workflows.",
            body,
        ),
    ]

    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
