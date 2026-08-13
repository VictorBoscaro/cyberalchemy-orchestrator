from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "out" / "anton" / "anton-introduction.pdf"

PAPER = HexColor("#f4eadc")
PAPER_LIGHT = HexColor("#f8f0e4")
INK = HexColor("#160f0c")
MUTED = HexColor("#5b4a40")
RUST = HexColor("#a93622")
RUST_DARK = HexColor("#792719")
HAIRLINE = HexColor("#b89b84")

# Left blank until Anton confirms them; the footer rule is drawn either way.
FOOTER_LOCATION = ""
FOOTER_CONTACT = ""


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
    if FOOTER_LOCATION:
        canvas.drawString(22 * mm, 10.7 * mm, FOOTER_LOCATION)
    if FOOTER_CONTACT:
        canvas.drawRightString(width - 22 * mm, 10.7 * mm, FOOTER_CONTACT)
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
        title="Anton - A brief introduction",
        author="Anton",
        subject="Professional introduction and current work",
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
        Paragraph("Anton", title),
        Paragraph("DOCUMENT CAPTURE & INTEGRATION ENGINEER  /  ABBYY FLEXICAPTURE, C#, LOCAL AI", subtitle),
        Paragraph("How I got here", heading),
        Paragraph(
            "I came to software through document capture. I worked at expert level with ABBYY FlexiCapture, a system "
            "that recognizes documents and extracts the attributes a business needs, from designing recognition "
            "templates to writing .NET C# libraries that integrate it with other automated systems. Those libraries "
            "run in high-load production at the largest bank in the Russian Federation.",
            body,
        ),
        Paragraph(
            "I am self-taught rather than a formally trained programmer, so I treat my code as improvable, not "
            "finished. ABBYY has left the country and I have not worked hands-on with its products for the last four "
            "years; the engineering judgment the work required stayed with me.",
            body,
        ),
        Paragraph("What I do", heading),
        Paragraph(
            "I make document and integration systems work in production, and I find out why they stop working.",
            body,
        ),
        Table(
            [[
                [Paragraph("CAPTURE", skill_label), Paragraph("Design recognition templates that extract the attributes the business actually needs", skill_text)],
                [Paragraph("INTEGRATE", skill_label), Paragraph("Write .NET C# libraries that connect capture to the surrounding automated systems", skill_text)],
                [Paragraph("DELIVER", skill_label), Paragraph("Ship with Ansible and Jenkins, mostly adapting existing pipelines rather than authoring them", skill_text)],
                [Paragraph("DIAGNOSE", skill_label), Paragraph("Debug, read logs, and analyze a failing situation as far as it takes to solve it", skill_text)],
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
            "I build and optimize local model inference on my own hardware, on both Linux and Windows: compiling "
            "<b>llama.cpp</b> from source, producing a working distribution, and running the server with a model for "
            "writing code or driving a general agent such as Hermes.",
            body,
        ),
        Paragraph(
            "AI is where I want to go next, and I am explicit about the gap. So far I have used ready-made agents and "
            "have not built one myself; closing that distance, from running someone else's agent to designing my own, "
            "is the work I want. Programming is the part I enjoy most, and agents are where I want to spend it.",
            body,
        ),
    ]

    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
