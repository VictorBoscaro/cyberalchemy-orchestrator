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
OUTPUT = ROOT / "output" / "pdf" / "expert-led-delivery-playbook" / "expert-led-delivery-playbook.pdf"

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

    canvas.setFillColor(Color(0.71, 0.25, 0.15, alpha=0.025))
    canvas.circle(width * 0.80, height * 0.20, 74 * mm, fill=1, stroke=0)
    canvas.setFillColor(Color(1, 1, 1, alpha=0.10))
    canvas.circle(width * 0.84, height * 0.90, 48 * mm, fill=1, stroke=0)

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

    canvas.setStrokeColor(Color(0.47, 0.13, 0.08, alpha=0.45))
    canvas.setLineWidth(0.55)
    canvas.line(22 * mm, 15.5 * mm, width - 22 * mm, 15.5 * mm)
    canvas.setFont("Constantia", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(22 * mm, 10.7 * mm, "FIXED-SCOPE OPPORTUNITIES")
    canvas.drawRightString(width - 22 * mm, 10.7 * mm, "Platform mechanics checked August 2026")
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
        title="Where to Find Fixed-Scope Contracts",
        author="Victor Boscaro",
        subject="Platforms for Greg-led technology, data, and business contracts",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, 0, 0, 0, 0)
    doc.addPageTemplates([PageTemplate(id="one-page", frames=[frame], onPage=draw_page)])

    title = ParagraphStyle(
        "title", fontName="Palatino-Bold", fontSize=25, leading=27, textColor=INK, spaceAfter=2.4 * mm
    )
    subtitle = ParagraphStyle(
        "subtitle", fontName="Constantia", fontSize=10, leading=12, textColor=RUST_DARK,
        tracking=0.6, spaceAfter=7 * mm
    )
    heading = ParagraphStyle(
        "heading", fontName="Palatino-Bold", fontSize=14.5, leading=16, textColor=RUST_DARK,
        spaceBefore=2 * mm, spaceAfter=2 * mm, keepWithNext=True
    )
    body = ParagraphStyle(
        "body", fontName="Constantia", fontSize=9.5, leading=13.2, textColor=INK,
        alignment=TA_LEFT, spaceAfter=3.2 * mm, allowWidows=0, allowOrphans=0
    )
    priority_style = ParagraphStyle(
        "priority", fontName="Constantia-Bold", fontSize=8.3, leading=10.5, textColor=RUST_DARK
    )
    platform_name = ParagraphStyle(
        "platform-name", fontName="Constantia-Bold", fontSize=8.5, leading=10.5, textColor=INK
    )
    platform_text = ParagraphStyle(
        "platform-text", fontName="Constantia", fontSize=8.3, leading=10.8, textColor=MUTED
    )
    rule = ParagraphStyle(
        "rule", fontName="Constantia-Bold", fontSize=10.2, leading=14, textColor=RUST_DARK,
        alignment=TA_LEFT
    )

    platforms = [
        ("START HERE", "UPWORK", "Largest project volume. Use fixed-price milestones and an agency structure when needed."),
        ("PACKAGED WORK", "FIVERR TEAM", "Sell repeatable data, automation, dashboard, or Meta Ads services."),
        ("DIRECT CLIENTS", "CONTRA", "Contracts, milestones, invoices, and payments for clients Greg finds elsewhere."),
        ("HIGHER VALUE", "CATALANT / A.TEAM", "Business, product, and operations projects. Better pay; slower, selective entry."),
        ("BOUNTIES", "ALGORA / TOPCODER / KOLABTREE", "Concrete deliverables and quick wins; less reliable as a pipeline."),
        ("LONGER WORK", "BRAINTRUST / TOPTAL / MERCOR", "Better-paying technical work, often centered on the screened individual."),
        ("GREG ONLY", "GLG / ALPHASIGHTS / THIRD BRIDGE", "Paid expert calls. Fast income, but the work cannot be distributed."),
    ]

    platform_rows = []
    for priority, name, text in platforms:
        platform_rows.append([
            Paragraph(priority, priority_style),
            Paragraph(name, platform_name),
            Paragraph(text, platform_text),
        ])

    story = [
        Spacer(1, 4 * mm),
        Paragraph("Find Fixed-Scope Contracts", title),
        Paragraph("TECHNOLOGY  /  DATA  /  BUSINESS", subtitle),
        Paragraph("The model", heading),
        Paragraph(
            "Greg finds the contract, works directly on it, and owns the final delivery. Trusted collaborators can "
            "execute clearly defined parts when the contract allows it.",
            body,
        ),
        Paragraph(
            "Target short, fixed-price projects with an accepted deliverable - not open-ended hourly work.",
            body,
        ),
        Paragraph("Where to look", heading),
        Table(
            platform_rows,
            colWidths=[31 * mm, 51 * mm, doc.width - 82 * mm],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), PAPER_LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.55, HAIRLINE),
                ("LINEABOVE", (0, 0), (-1, 0), 1.4, RUST),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, HAIRLINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.4 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4 * mm),
            ]),
        ),
        Spacer(1, 5 * mm),
        Table(
            [[Paragraph(
                "Accept only work with a clear deliverable, acceptance criteria, funded payment, and permission "
                "to involve collaborators.",
                rule,
            )]],
            colWidths=[doc.width],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), PAPER_LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.8, RUST),
                ("LINEBEFORE", (0, 0), (0, 0), 3, RUST),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3.2 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2 * mm),
            ]),
        ),
    ]

    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
