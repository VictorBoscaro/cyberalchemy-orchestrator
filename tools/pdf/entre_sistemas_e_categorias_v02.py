"""Build version 0.2 of *Entre Sistemas e Categorias*.

The durable source available for this edition is the reviewed 60-page PDF. This
pipeline treats it as immutable, removes replaced regions with PDF redactions,
adds editorial seams, inserts four new chapter pages, and writes a new artifact.

Run from the repository root:

    python tools/pdf/entre_sistemas_e_categorias_v02.py

PyMuPDF is required. Open-source fonts are fetched into ``tmp/pdfs`` and pinned
by SHA-256. The cache is removed after a successful build unless ``--keep-temp``
is supplied.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
import urllib.request
from pathlib import Path

import fitz


REPO = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = REPO / "output" / "pdf" / "entre_sistemas_e_categorias_revisado.pdf"
DEFAULT_OUTPUT = REPO / "output" / "pdf" / "entre_sistemas_e_categorias_v0.2.pdf"
TEMP_ROOT = REPO / "tmp" / "pdfs" / "entre_sistemas_v02_build"
SOURCE_SHA256 = "d29e78998a12697b2fdcdebfab598439cca1a096251b069d65ac134446f8ecd8"

PAGE_W = 595.304
PAGE_H = 841.89
CREAM = (244 / 255, 234 / 255, 220 / 255)
NAVY = (19 / 255, 34 / 255, 56 / 255)
TEAL = (14 / 255, 143 / 255, 142 / 255)
BLUE = (52 / 255, 112 / 255, 165 / 255)
ORANGE = (221 / 255, 147 / 255, 34 / 255)
PURPLE = (112 / 255, 88 / 255, 126 / 255)
SLATE = (83 / 255, 105 / 255, 126 / 255)
PANEL = (250 / 255, 247 / 255, 241 / 255)
WHITE = (1, 1, 1)
RED = (214 / 255, 35 / 255, 35 / 255)
AUTHOR = "Victor Boscaro • Vladimir Rondelli"

FONTS = {
    "Lato-Regular.ttf": (
        "https://raw.githubusercontent.com/google/fonts/main/ofl/lato/Lato-Regular.ttf",
        "d636e4683231f931eda222d588e944d082bfd3bdba02f928bee461c0f185b251",
    ),
    "Lato-Bold.ttf": (
        "https://raw.githubusercontent.com/google/fonts/main/ofl/lato/Lato-Bold.ttf",
        "8a0aace75d33794eece4b28187bfc1df0bbd2888b5d8a56e01788c8d65d16be1",
    ),
    "Carlito-Bold.ttf": (
        "https://raw.githubusercontent.com/google/fonts/main/ofl/carlito/Carlito-Bold.ttf",
        "bb5d20f79b82599ec72983597437373a80f2d2085fa91fc144fd74e876a594db",
    ),
    "NotoSerif-Variable.ttf": (
        "https://raw.githubusercontent.com/google/fonts/main/ofl/notoserif/NotoSerif%5Bwdth,wght%5D.ttf",
        "4d8e6761424656867019081a1a01336f3cb086982682698714054fc33f782713",
    ),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def acquire_fonts(font_dir: Path) -> dict[str, Path]:
    font_dir.mkdir(parents=True, exist_ok=True)
    result: dict[str, Path] = {}
    for name, (url, expected) in FONTS.items():
        path = font_dir / name
        if not path.exists() or sha256(path) != expected:
            urllib.request.urlretrieve(url, path)
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"Font hash mismatch for {name}: {actual}")
        result[name] = path
    return result


def font_paths(fonts: dict[str, Path]) -> dict[str, str]:
    return {
        "lato": str(fonts["Lato-Regular.ttf"]),
        "lato_bold": str(fonts["Lato-Bold.ttf"]),
        "carlito_bold": str(fonts["Carlito-Bold.ttf"]),
        "noto": str(fonts["NotoSerif-Variable.ttf"]),
    }


def textbox(
    page: fitz.Page,
    rect: fitz.Rect,
    text: str,
    *,
    fontname: str,
    fontfile: str,
    fontsize: float,
    color=NAVY,
    align: int = fitz.TEXT_ALIGN_LEFT,
    lineheight: float = 1.25,
    render_mode: int = 0,
) -> float:
    spare = page.insert_textbox(
        rect,
        text,
        fontname=fontname,
        fontfile=fontfile,
        fontsize=fontsize,
        color=color,
        align=align,
        lineheight=lineheight,
        render_mode=render_mode,
        overlay=True,
    )
    if spare < -0.2:
        raise RuntimeError(f"Text overflow ({spare:.2f} pt): {text[:80]!r} in {rect}")
    return spare


def centered_text(
    page: fitz.Page,
    rect: fitz.Rect,
    text: str,
    *,
    fontname: str,
    fontfile: str,
    fontsize: float,
    color=NAVY,
) -> None:
    textbox(
        page,
        rect,
        text,
        fontname=fontname,
        fontfile=fontfile,
        fontsize=fontsize,
        color=color,
        align=fitz.TEXT_ALIGN_CENTER,
        lineheight=1.15,
    )


def add_redaction(page: fitz.Page, rect: fitz.Rect, fill=CREAM) -> None:
    page.add_redact_annot(rect, fill=fill)


def panel(page: fitz.Page, rect: fitz.Rect, stroke=BLUE, fill=PANEL, radius=6, width=1.1) -> None:
    # PyMuPDF expresses rounded-corner radius as a fraction of the shorter side.
    radius_fraction = radius / min(rect.width, rect.height) if radius > 0.5 else radius
    kwargs = {"color": stroke, "fill": fill, "width": width, "overlay": True}
    if radius_fraction > 0:
        kwargs["radius"] = min(radius_fraction, 0.5)
    page.draw_rect(rect, **kwargs)


def arrow(page: fitz.Page, start: tuple[float, float], end: tuple[float, float], color=SLATE) -> None:
    page.draw_line(start, end, color=color, width=1.1, overlay=True)
    ex, ey = end
    sx, sy = start
    dx, dy = ex - sx, ey - sy
    length = max((dx * dx + dy * dy) ** 0.5, 0.01)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    p1 = (ex - 5 * ux + 2.5 * px, ey - 5 * uy + 2.5 * py)
    p2 = (ex - 5 * ux - 2.5 * px, ey - 5 * uy - 2.5 * py)
    page.draw_polyline([p1, (ex, ey), p2], color=color, width=1.1, overlay=True)


def extract_logo(doc: fitz.Document) -> bytes:
    for item in doc[0].get_images(full=True):
        xref, smask, width, height = item[0], item[1], item[2], item[3]
        rects = doc[0].get_image_rects(xref)
        if width == 480 and height == 480 and any(r.width <= 20 and r.height <= 20 for r in rects):
            pix = fitz.Pixmap(doc, xref)
            if smask:
                pix = fitz.Pixmap(pix, fitz.Pixmap(doc, smask))
            return pix.tobytes("png")
    raise RuntimeError("CyberAlchemy mark not found in the immutable input")


def add_furniture(page: fitz.Page, number: int, fonts: dict[str, str], logo: bytes) -> None:
    page.draw_line((51.1, 31.5), (544.4, 31.5), color=(0.76, 0.81, 0.84), width=0.45)
    textbox(
        page,
        fitz.Rect(420, 15, 545, 29),
        "ENTRE SISTEMAS E CATEGORIAS",
        fontname="Lato",
        fontfile=fonts["lato"],
        fontsize=7.3,
        color=SLATE,
        align=fitz.TEXT_ALIGN_RIGHT,
        lineheight=1,
    )
    centered_text(
        page,
        fitz.Rect(280, 806, 315, 827),
        str(number),
        fontname="Noto",
        fontfile=fonts["noto"],
        fontsize=9.5,
        color=NAVY,
    )
    page.insert_image(fitz.Rect(547.304, 806.89, 562.304, 821.89), stream=logo, overlay=True)
    page.insert_text(
        (4, 7),
        AUTHOR,
        fontname="LatoInvisibleV02",
        fontfile=fonts["lato"],
        fontsize=1,
        color=NAVY,
        render_mode=3,
        overlay=True,
    )


def patch_opening(page: fitz.Page, fonts: dict[str, str]) -> None:
    add_redaction(page, fitz.Rect(82, 272, 310, 301))
    add_redaction(page, fitz.Rect(130, 516, 468, 534))
    add_redaction(page, fitz.Rect(158, 535, 437, 553))
    add_redaction(page, fitz.Rect(132, 489, 463, 507))
    page.apply_redactions()
    textbox(
        page,
        fitz.Rect(87, 276, 335, 301),
        "Três tradições complementares",
        fontname="LatoBoldV02",
        fontfile=fonts["lato_bold"],
        fontsize=16.5,
        color=NAVY,
        lineheight=1,
    )
    centered_text(
        page,
        fitz.Rect(132, 491, 463, 506),
        "A tese não é que as tradições sejam equivalentes; é que nenhuma delas basta sozinha.",
        fontname="LatoOpeningThesis",
        fontfile=fonts["lato"],
        fontsize=7.9,
        color=SLATE,
    )
    centered_text(
        page,
        fitz.Rect(132, 518, 465, 533),
        "Figura de abertura - três tradições que convergem sem perder suas diferenças.",
        fontname="LatoV02",
        fontfile=fonts["lato"],
        fontsize=7.9,
        color=SLATE,
    )
    centered_text(
        page,
        fitz.Rect(158, 538, 437, 552),
        "Documento de investigação • versão 0.2 • 11 de agosto de 2026",
        fontname="LatoV02b",
        fontfile=fonts["lato"],
        fontsize=8.0,
        color=SLATE,
    )


def draw_traditions_figure(page: fitz.Page, fonts: dict[str, str]) -> None:
    add_redaction(page, fitz.Rect(64, 46, 532, 329))
    page.apply_redactions()
    outer = fitz.Rect(65.5, 48, 529.8, 312)
    panel(page, outer, stroke=WHITE, fill=WHITE, radius=0, width=0.1)
    textbox(
        page,
        fitz.Rect(80, 62, 410, 84),
        "Três tradições complementares",
        fontname="LatoBoldFig",
        fontfile=fonts["lato_bold"],
        fontsize=17.0,
        color=NAVY,
        lineheight=1,
    )
    textbox(
        page,
        fitz.Rect(80, 83, 510, 98),
        "Dinâmica, estrutura e revisão convergem numa linguagem operacional.",
        fontname="LatoFig",
        fontfile=fonts["lato"],
        fontsize=8.5,
        color=SLATE,
        lineheight=1,
    )

    boxes = [
        (fitz.Rect(80, 109, 215, 187), TEAL, "PENSAMENTO SISTÊMICO", "feedback • estoques/fluxos\natrasos • fronteiras\ncausalidade • intervenção"),
        (fitz.Rect(230, 109, 365, 187), BLUE, "TEORIA DAS CATEGORIAS", "objetos/morfismos • composição\nfuntores/transporte • equivalência\ninvariantes/preservação\nconstruções universais"),
        (fitz.Rect(380, 109, 515, 187), ORANGE, "EPISTEMOLOGIA OPERACIONAL", "lentes/probes • sinais\nanalogias • hipóteses\nreframing • resíduos/revisão"),
    ]
    for index, (rect, color, title, body) in enumerate(boxes):
        panel(page, rect, stroke=color, fill=(0.96, 0.97, 0.96), radius=7, width=1.35)
        centered_text(
            page,
            fitz.Rect(rect.x0 + 4, rect.y0 + 10, rect.x1 - 4, rect.y0 + 25),
            title,
            fontname=f"CarlitoFig{index}",
            fontfile=fonts["carlito_bold"],
            fontsize=8.6 if index != 2 else 7.9,
            color=color,
        )
        centered_text(
            page,
            fitz.Rect(rect.x0 + 6, rect.y0 + 32, rect.x1 - 6, rect.y1 - 5),
            body,
            fontname=f"NotoFig{index}",
            fontfile=fonts["noto"],
            fontsize=7.4 if index == 1 else 7.8,
            color=NAVY,
        )

    arrow(page, (215, 148), (230, 148), PURPLE)
    arrow(page, (365, 148), (380, 148), PURPLE)
    lower = fitz.Rect(172, 214, 423, 274)
    panel(page, lower, stroke=PURPLE, fill=(0.97, 0.96, 0.97), radius=7, width=1.35)
    centered_text(
        page,
        fitz.Rect(178, 224, 417, 239),
        "LINGUAGEM OPERACIONAL DO CONHECIMENTO",
        fontname="CarlitoFigBottom",
        fontfile=fonts["carlito_bold"],
        fontsize=9.0,
        color=PURPLE,
    )
    centered_text(
        page,
        fitz.Rect(182, 242, 413, 270),
        "tipos/schemas • composição • provenance • grounding\ninstanciação/generatividade • governança",
        fontname="NotoFigBottom",
        fontfile=fonts["noto"],
        fontsize=7.5,
        color=NAVY,
    )
    for start in [(147, 187), (297, 187), (447, 187)]:
        arrow(page, start, (297, 214), SLATE)
    centered_text(
        page,
        fitz.Rect(90, 283, 505, 298),
        "As tradições contribuem operações diferentes; nenhuma delas basta sozinha.",
        fontname="LatoFigFoot",
        fontfile=fonts["lato"],
        fontsize=8.0,
        color=SLATE,
    )
    centered_text(
        page,
        fitz.Rect(100, 315, 495, 328),
        "Figura 1 - Três tradições complementares e sua convergência operacional.",
        fontname="LatoFigCap",
        fontfile=fonts["lato"],
        fontsize=7.8,
        color=SLATE,
    )


def patch_method_page(page: fitz.Page, fonts: dict[str, str]) -> None:
    """Replace the early enrichment ratchet with the later diagnostic branch."""
    add_redaction(page, fitz.Rect(48, 628, 544, 662))
    page.apply_redactions()
    textbox(
        page,
        fitz.Rect(51, 630, 540, 661),
        "adequação ou um testemunho global. Esse resíduo orienta o próximo diagnóstico; enriquecer é apenas uma resposta possível. O objetivo é chegar ao menor núcleo que sobreviva sem ocultar o que ficou de fora.",
        fontname="NotoMethodPatch",
        fontfile=fonts["noto"],
        fontsize=8.8,
        color=NAVY,
        lineheight=1.2,
    )


def add_summary_seam(page: fitz.Page, fonts: dict[str, str]) -> None:
    rect = fitz.Rect(51, 548, 544, 629)
    panel(page, rect, stroke=PURPLE, fill=(0.97, 0.96, 0.97), radius=5, width=0.9)
    textbox(
        page,
        fitz.Rect(62, 558, 532, 575),
        "HIPÓTESE DE PESQUISA • UMA PERGUNTA MAIS FUNDA",
        fontname="LatoBoldSummary",
        fontfile=fonts["lato_bold"],
        fontsize=8.8,
        color=PURPLE,
        lineheight=1,
    )
    textbox(
        page,
        fitz.Rect(62, 578, 532, 618),
        "Ao final, as três tradições também serão usadas para perguntar se existe um kernel candidato de operações mais fundamentais. O documento não demonstra sua minimalidade, suficiência ou independência.",
        fontname="NotoSummary",
        fontfile=fonts["noto"],
        fontsize=8.8,
        color=NAVY,
        lineheight=1.25,
    )


def patch_contents(page: fitz.Page, fonts: dict[str, str]) -> None:
    add_redaction(page, fitz.Rect(299, 224, 540, 350))
    add_redaction(page, fitz.Rect(80, 349, 520, 373))
    page.apply_redactions()
    textbox(page, fitz.Rect(303, 227, 510, 241), "PARTE VI", fontname="LatoBoldToc", fontfile=fonts["lato_bold"], fontsize=8.4, color=ORANGE, lineheight=1)
    textbox(page, fitz.Rect(303, 242, 535, 258), "Uma linguagem operacional do conhecimento", fontname="CarlitoToc", fontfile=fonts["carlito_bold"], fontsize=10.0, color=NAVY, lineheight=1)
    textbox(page, fitz.Rect(307, 262, 535, 276), "16  Natural language, category theory e systems thinking", fontname="NotoToc1", fontfile=fonts["noto"], fontsize=8.3, color=NAVY, lineheight=1)
    textbox(page, fitz.Rect(307, 278, 535, 292), "17  Em busca do kernel mínimo", fontname="NotoToc2", fontfile=fonts["noto"], fontsize=8.3, color=NAVY, lineheight=1)
    textbox(page, fitz.Rect(303, 299, 450, 313), "APÊNDICES", fontname="LatoBoldToc2", fontfile=fonts["lato_bold"], fontsize=8.4, color=ORANGE, lineheight=1)
    textbox(page, fitz.Rect(303, 314, 505, 329), "Auditoria e continuidade", fontname="CarlitoToc2", fontfile=fonts["carlito_bold"], fontsize=10.0, color=NAVY, lineheight=1)
    textbox(page, fitz.Rect(307, 333, 535, 377), "A  Ledger de claims, premissas e limites\nB  Questões abertas consolidadas\nC  Glossário mínimo\nReferências e nota final de método", fontname="NotoToc3", fontfile=fonts["noto"], fontsize=8.3, color=NAVY, lineheight=1.22)
    centered_text(page, fitz.Rect(80, 392, 520, 410), "A densidade cresce deliberadamente: intuição -> ponte formal -> motor epistemológico -> limites reflexivos.", fontname="LatoTocFoot", fontfile=fonts["lato"], fontsize=7.7, color=SLATE)


def add_residue_seam(page: fitz.Page, fonts: dict[str, str]) -> None:
    rect = fitz.Rect(51, 594, 544, 772)
    panel(page, rect, stroke=ORANGE, fill=(1.0, 0.97, 0.90), radius=6, width=1.0)
    textbox(page, fitz.Rect(63, 607, 530, 627), "OCORRÊNCIA EMERGENTE, REPRESENTAÇÃO DERIVADA", fontname="LatoBoldResidue", fontfile=fonts["lato_bold"], fontsize=10.1, color=ORANGE, lineheight=1)
    body = (
        "Duas estruturas podem cumprir separadamente suas obrigações e falhar somente quando combinadas. "
        "Nesse sentido estrito, algo residual emerge na interação. O resíduo representado, porém, é derivado: "
        "um evento de não fechamento produz um readout; o readout é comparado com uma expectativa sob um "
        "critério de relevância; a diferença julgada pode então ser tipada e preservada como resíduo. Emergência "
        "como ocorrência e derivabilidade como representação não se excluem.\n\n"
        "A classificação é multiaxial: o locus pode ser interno, de transformação, de composição/globalização ou "
        "de contato com o domínio; a ordem pode ser comum ou reflexiva. Os rótulos podem coexistir."
    )
    textbox(page, fitz.Rect(63, 635, 531, 758), body, fontname="NotoResidue", fontfile=fonts["noto"], fontsize=8.5, color=NAVY, lineheight=1.22)


def add_composition_seam(page: fitz.Page, fonts: dict[str, str]) -> None:
    textbox(page, fitz.Rect(51, 219, 420, 242), "13.7 Composição sem colapso", fontname="LatoBoldComposition", fontfile=fonts["lato_bold"], fontsize=14.2, color=NAVY, lineheight=1)
    body = (
        "Compor é conectar diferenças por interfaces válidas. Equivaler é julgar quando uma diferença pode ser "
        "ignorada relativamente a uma estrutura e a uma tarefa. Em operações de encaixe, substituição ou reuso, "
        "equivalências podem autorizar compatibilidade; não são, porém, condição universal de composição.\n\n"
        "Uma composição útil preserva distinções suficientes para que o resultado continue informativo. Simetria "
        "demais pode apagar estrutura relevante; distinção demais pode impedir reutilização e continuidade. O "
        "problema não é escolher um ponto abstrato entre os extremos, mas declarar interface, propósito, estrutura "
        "preservada e aquilo que não pode ser apagado.\n\n"
        "Uma lente boa pode buscar o menor conjunto de distinções que ainda sustenta as composições exigidas pela "
        "tarefa. Isso é uma compressão condicionada, não a identificação de tudo com tudo: colapsar o irrelevante, "
        "preservar o relevante e registrar o que permanece residual."
    )
    textbox(page, fitz.Rect(51, 252, 544, 470), body, fontname="NotoComposition", fontfile=fonts["noto"], fontsize=9.5, color=NAVY, lineheight=1.32)
    panel(page, fitz.Rect(83, 492, 512, 555), stroke=PURPLE, fill=(0.97, 0.96, 0.97), radius=5, width=1)
    centered_text(page, fitz.Rect(96, 505, 499, 543), "diferenças tipadas  ->  interface válida  ->  composição\n                 preserva uma obrigação explícita", fontname="LatoCompositionDiagram", fontfile=fonts["lato"], fontsize=9.2, color=PURPLE)


def add_minimalism_seam(page: fitz.Page, fonts: dict[str, str]) -> None:
    textbox(page, fitz.Rect(51, 211, 470, 235), "14.6 Minimalismo como hipótese epistemológica", fontname="LatoBoldMinimal", fontfile=fonts["lato_bold"], fontsize=14.0, color=NAVY, lineheight=1)
    body = (
        "O minimalismo relevante aqui não afirma que schemas menores sejam sempre melhores. Ele propõe começar "
        "com a linguagem menos carregada que ainda distingue o necessário para uma tarefa, um risco e um critério "
        "de preservação declarados. Estrutura adicional entra quando uma obrigação prospectiva ou um resíduo bem "
        "tipado mostra que diferenças relevantes foram colapsadas.\n\n"
        "Mismatch não prescreve enriquecimento. O diagnóstico pode mandar reparar o probe ou o readout, revisar a "
        "expectativa ou a lente, mover a fronteira, corrigir a interface, aceitar incerteza, de-enriquecer ou abster-se. "
        "E risco conhecido pode justificar estrutura antes de qualquer ruptura observada.\n\n"
        "Por enquanto, 'mínimo' nomeia uma heurística local de suficiência. Não existe ainda uma ordem formal única "
        "de comparação, e soluções diferentes podem permanecer incomparáveis."
    )
    textbox(page, fitz.Rect(51, 247, 544, 450), body, fontname="NotoMinimal", fontfile=fonts["noto"], fontsize=9.5, color=NAVY, lineheight=1.32)


def add_chapter_pointer(page: fitz.Page, fonts: dict[str, str]) -> None:
    panel(page, fitz.Rect(51, 209, 544, 260), stroke=PURPLE, fill=(0.97, 0.96, 0.97), radius=5, width=0.8)
    centered_text(page, fitz.Rect(65, 221, 530, 250), "O capítulo 17 retoma essas questões como hipótese de pesquisa: uma gramática candidata abaixo das três tradições.", fontname="LatoPointer", fontfile=fonts["lato"], fontsize=9.0, color=PURPLE)


def chapter_page(doc: fitz.Document, number: int, fonts: dict[str, str], logo: bytes) -> fitz.Page:
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.draw_rect(page.rect, color=CREAM, fill=CREAM, width=0, overlay=True)
    add_furniture(page, number, fonts, logo)
    return page


def add_chapter_pages(doc: fitz.Document, fonts: dict[str, str], logo: bytes) -> None:
    # Insert directly into the destination document. Importing a separately
    # generated PDF caused resource-name collisions with the Writer snapshot in
    # Poppler, despite correct extraction. Direct insertion avoids that defect.
    for offset in range(4):
        doc.new_page(pno=54 + offset, width=PAGE_W, height=PAGE_H)

    def prepared_page(index: int, number: int) -> fitz.Page:
        target = doc[index]
        target.draw_rect(target.rect, color=CREAM, fill=CREAM, width=0, overlay=True)
        add_furniture(target, number, fonts, logo)
        return target

    page = prepared_page(54, 55)
    textbox(page, fitz.Rect(51, 48, 545, 82), "17. Em busca do kernel mínimo", fontname="LatoBoldCh17", fontfile=fonts["lato_bold"], fontsize=24, color=NAVY, lineheight=1)
    textbox(page, fitz.Rect(51, 94, 540, 122), "Quanto precisamos assumir para que essa linguagem funcione?", fontname="NotoCh17Q", fontfile=fonts["noto"], fontsize=13.2, color=PURPLE, lineheight=1.1)
    body = (
        "Até aqui, pensamento sistêmico, teoria das categorias e epistemologia operacional apareceram como "
        "tradições complementares. A hipótese mais forte deste documento é que elas também possam funcionar como "
        "repertórios para investigar operações mais fundamentais: não uma quarta tradição, mas uma gramática "
        "candidata situada abaixo das três.\n\n"
        "O deslocamento muda a pergunta. A teoria das categorias ajuda a examinar tipagem, transformação, "
        "composição, equivalência e preservação. O pensamento sistêmico mantém visíveis dinâmica, fronteira, "
        "feedback, causalidade e intervenção. A epistemologia operacional fornece orientação, probes, evidência, "
        "reframing e revisão. O kernel candidato pergunta quais dependências precisam existir antes que esses "
        "repertórios sejam enriquecidos por estruturas próprias de um domínio e de uma tarefa.\n\n"
        "Essa hipótese não foi demonstrada. 'Mínimo' não nomeia aqui uma cardinalidade, uma ordem universal ou um "
        "resultado de independência. Nomeia uma disciplina de investigação: fixar somente o necessário para "
        "distinguir e compor sob obrigações explícitas; depois tentar quebrar a linguagem com casos em que ela perde "
        "estrutura, confunde readout com evidência ou não consegue representar o que a interação tornou relevante."
    )
    textbox(page, fitz.Rect(51, 145, 544, 432), body, fontname="NotoCh17Body", fontfile=fonts["noto"], fontsize=10.1, color=NAVY, lineheight=1.35)
    panel(page, fitz.Rect(66, 470, 529, 598), stroke=PURPLE, fill=(0.97, 0.96, 0.97), radius=7, width=1.2)
    textbox(page, fitz.Rect(82, 487, 513, 509), "HIPÓTESE DO KERNEL CANDIDATO", fontname="LatoBoldHyp", fontfile=fonts["lato_bold"], fontsize=10.4, color=PURPLE, lineheight=1)
    textbox(page, fitz.Rect(82, 520, 513, 579), "Uma linguagem operacional pode refinar suas distinções e transformações quando contatos especificados com um domínio produzem diferenças relevantes para uma tarefa.", fontname="NotoHyp", fontfile=fonts["noto"], fontsize=11.0, color=NAVY, lineheight=1.3)
    textbox(page, fitz.Rect(65, 640, 530, 701), "A integridade documental desta formulação foi verificada. Seu conteúdo conceitual permanece provisório, forte e arriscado.", fontname="LatoCaution", fontfile=fonts["lato"], fontsize=9.5, color=SLATE, align=fitz.TEXT_ALIGN_CENTER, lineheight=1.25)

    page = prepared_page(55, 56)
    textbox(page, fitz.Rect(51, 48, 545, 78), "17.1 Kernel, ground, contact e enrichments", fontname="LatoBoldCh171", fontfile=fonts["lato_bold"], fontsize=21, color=NAVY, lineheight=1)
    textbox(page, fitz.Rect(51, 90, 540, 121), "Quatro componentes provisórios que devem permanecer separados.", fontname="NotoCh171Lead", fontfile=fonts["noto"], fontsize=10.5, color=SLATE, lineheight=1.2)
    cards = [
        (fitz.Rect(51, 140, 287, 282), TEAL, "K • KERNEL", "orientação/contexto\ndistinção\nrelação/transformação\ncomposição", "Hipótese de dependências; não inclui por si só verdade, observação ou uma ontologia completa."),
        (fitz.Rect(308, 140, 544, 282), BLUE, "G • GROUND", "alvo • situação\nprocesso • fenômeno", "Aquilo sobre o qual a linguagem opera. Resistência é mismatch situado, não essência do domínio."),
        (fitz.Rect(51, 304, 287, 446), ORANGE, "C • CONTACT", "interpretação\nação/probe\nreadout", "Faz a interface entre representação e ground sem prometer acesso transparente ou força evidencial automática."),
        (fitz.Rect(308, 304, 544, 446), PURPLE, "E • ENRICHMENTS", "tempo • probabilidade • causalidade\nagência • normatividade • lógica\nmodalidade • geometria", "Estruturas adicionáveis e removíveis segundo obrigações explícitas; mais estrutura não é sempre melhor."),
    ]
    for idx, (rect, color, title, terms, note) in enumerate(cards):
        panel(page, rect, stroke=color, fill=PANEL, radius=6, width=1.1)
        textbox(page, fitz.Rect(rect.x0 + 13, rect.y0 + 13, rect.x1 - 13, rect.y0 + 33), title, fontname=f"LatoBoldCard{idx}", fontfile=fonts["lato_bold"], fontsize=10.2, color=color, lineheight=1)
        textbox(page, fitz.Rect(rect.x0 + 13, rect.y0 + 42, rect.x1 - 13, rect.y0 + 88), terms, fontname=f"NotoCardTerms{idx}", fontfile=fonts["noto"], fontsize=9.0, color=NAVY, lineheight=1.18)
        textbox(page, fitz.Rect(rect.x0 + 13, rect.y0 + 94, rect.x1 - 13, rect.y1 - 10), note, fontname=f"LatoCardNote{idx}", fontfile=fonts["lato"], fontsize=7.9, color=SLATE, lineheight=1.2)
    body = (
        "Duas dependências permanecem abertas. A orientação pode ser componente de K, parâmetro externo ou índice "
        "de uma família de kernels. Relação e transformação permanecem próximas, mas não foram reduzidas uma à "
        "outra: essa redução pode exigir carriers, direção, aridade, produtos, truth values ou outra estrutura."
    )
    panel(page, fitz.Rect(66, 485, 529, 596), stroke=NAVY, fill=(0.94, 0.95, 0.96), radius=5, width=0.9)
    textbox(page, fitz.Rect(82, 502, 513, 580), body, fontname="NotoDeps", fontfile=fonts["noto"], fontsize=9.3, color=NAVY, lineheight=1.3)
    centered_text(page, fitz.Rect(70, 635, 525, 690), "K + G + C (+ E)\n-> aplicação situada, nunca acesso neutro ao mundo", fontname="LatoKGCE", fontfile=fonts["lato"], fontsize=11.0, color=PURPLE)

    page = prepared_page(56, 57)
    textbox(page, fitz.Rect(51, 48, 545, 78), "17.2 Do contato ao resíduo", fontname="LatoBoldCh172", fontfile=fonts["lato_bold"], fontsize=21, color=NAVY, lineheight=1)
    lead = (
        "Considere uma decisão em que uma lente econômica e uma lente operacional sejam adequadas separadamente. "
        "A primeira preserva custo e retorno; a segunda preserva capacidade, segurança e tempo de recuperação. "
        "Nenhuma contém contradição interna. Quando as duas orientam a mesma intervenção, porém, uma economia local "
        "pode degradar uma obrigação operacional. O resíduo aparece na composição e no contato com a situação."
    )
    textbox(page, fitz.Rect(51, 96, 544, 207), lead, fontname="NotoCh172Lead", fontfile=fonts["noto"], fontsize=10.0, color=NAVY, lineheight=1.33)
    stages = [
        ("representação + expectativa", TEAL),
        ("contato / probe / readout", BLUE),
        ("diferença julgada relevante", ORANGE),
        ("resíduo representado", PURPLE),
        ("diagnóstico", NAVY),
    ]
    y = 238
    for idx, (label, color) in enumerate(stages):
        rect = fitz.Rect(125, y, 470, y + 38)
        panel(page, rect, stroke=color, fill=PANEL, radius=5, width=1)
        centered_text(page, fitz.Rect(135, y + 10, 460, y + 31), label, fontname=f"LatoStage{idx}", fontfile=fonts["lato"], fontsize=9.4, color=color)
        if idx < len(stages) - 1:
            arrow(page, (297.5, y + 38), (297.5, y + 51), SLATE)
        y += 51
    textbox(page, fitz.Rect(51, 516, 544, 538), "O diagnóstico abre alternativas; não aciona uma catraca de enriquecimento:", fontname="LatoBoldDiagnosis", fontfile=fonts["lato_bold"], fontsize=10.0, color=NAVY, lineheight=1)
    panel(page, fitz.Rect(51, 548, 544, 651), stroke=ORANGE, fill=(1.0, 0.97, 0.90), radius=6, width=1)
    centered_text(page, fitz.Rect(65, 562, 530, 636), "reparar probe/readout • revisar expectativa ou lente\nmover fronteira • reparar interface • enriquecer • de-enriquecer\naceitar incerteza • abster-se", fontname="NotoBranches", fontfile=fonts["noto"], fontsize=10.0, color=NAVY)
    textbox(page, fitz.Rect(65, 682, 530, 739), "O evento de não fechamento pode emergir apenas na interação. Sua representação como resíduo depende depois de readout, comparação, relevância e julgamento.", fontname="LatoCh172Foot", fontfile=fonts["lato"], fontsize=9.1, color=SLATE, align=fitz.TEXT_ALIGN_CENTER, lineheight=1.25)

    page = prepared_page(57, 58)
    textbox(page, fitz.Rect(51, 48, 545, 78), "17.3 Reconstruções e testes de ruptura", fontname="LatoBoldCh173", fontfile=fonts["lato_bold"], fontsize=21, color=NAVY, lineheight=1)
    lead = "O kernel candidato ganha valor apenas se conseguir reconstruir operações úteis sem esconder dependências importadas. Os itens abaixo são esboços, não derivações formais."
    textbox(page, fitz.Rect(51, 94, 544, 145), lead, fontname="NotoCh173Lead", fontfile=fonts["noto"], fontsize=10.0, color=NAVY, lineheight=1.3)
    recon = [
        ("Lente", "organização contextual de K, contatos, probes e enriquecimentos para uma orientação, tarefa e domínio"),
        ("Probe", "ação planejada para produzir um readout discriminante por um contato especificado"),
        ("Analogia", "correspondência tipada submetida a testes de preservação e ruptura"),
        ("Schema e instância", "tipos, relações e restrições estabilizados; realização sob um julgamento de satisfação"),
        ("Reframing", "transformação das distinções, relações, fronteiras ou perguntas que organizam um problema"),
    ]
    y = 163
    for idx, (term, desc) in enumerate(recon):
        color = [TEAL, BLUE, ORANGE, PURPLE, NAVY][idx]
        page.draw_line((51, y + 7), (61, y + 7), color=color, width=3)
        textbox(page, fitz.Rect(69, y, 180, y + 19), term, fontname=f"LatoBoldRecon{idx}", fontfile=fonts["lato_bold"], fontsize=9.5, color=color, lineheight=1)
        textbox(page, fitz.Rect(180, y, 544, y + 35), desc, fontname=f"NotoRecon{idx}", fontfile=fonts["noto"], fontsize=8.8, color=NAVY, lineheight=1.22)
        y += 52
    textbox(page, fitz.Rect(51, 440, 544, 462), "Como tentar quebrar a hipótese", fontname="LatoBoldBreak", fontfile=fonts["lato_bold"], fontsize=14.0, color=NAVY, lineheight=1)
    tests = (
        "1. Dependência - algum componente pressupõe estrutura que o kernel deveria explicar?\n"
        "2. Reconstrução - lens, probe, analogia e residue podem ser formados com regras explícitas?\n"
        "3. Contato - a linguagem distingue evento, readout, evidência, julgamento e representação?\n"
        "4. Fatoração - uma representação preserva exatamente os readouts exigidos por uma tarefa?\n"
        "5. Emergência composicional - partes localmente adequadas falham somente quando combinadas?"
    )
    panel(page, fitz.Rect(51, 475, 544, 625), stroke=PURPLE, fill=(0.97, 0.96, 0.97), radius=6, width=1)
    textbox(page, fitz.Rect(66, 491, 529, 610), tests, fontname="NotoTests", fontfile=fonts["noto"], fontsize=9.0, color=NAVY, lineheight=1.24)
    textbox(page, fitz.Rect(65, 661, 530, 730), "Se o kernel exigir todos os enriquecimentos desde o início, não for capaz de de-enriquecer ou não separar contato de julgamento, a hipótese terá falhado justamente onde pretendia ser mais econômica.", fontname="LatoCh173Foot", fontfile=fonts["lato"], fontsize=9.3, color=SLATE, align=fitz.TEXT_ALIGN_CENTER, lineheight=1.28)
    return None


def add_appendix_a(page: fitz.Page, fonts: dict[str, str]) -> None:
    textbox(page, fitz.Rect(51, 658, 544, 676), "ADENDO V0.2 • CLAIMS DO KERNEL CANDIDATO", fontname="LatoBoldAppA", fontfile=fonts["lato_bold"], fontsize=9.0, color=ORANGE, lineheight=1)
    text = (
        "• Kernel K/G/C/E: hipótese de pesquisa; minimalidade, suficiência e independência não demonstradas.\n"
        "• Resíduo pode emergir como ocorrência e ser derivado como representação; os dois estatutos não se excluem.\n"
        "• 'Mismatch exige enriquecimento': falso; diagnóstico admite reparo, reenquadramento, de-enriquecimento, incerteza ou abstenção.\n"
        "• A IR epistemológica pode ser instanciação situada e enriquecida do kernel; não é consequência dele."
    )
    textbox(page, fitz.Rect(51, 682, 544, 774), text, fontname="NotoAppA", fontfile=fonts["noto"], fontsize=8.3, color=NAVY, lineheight=1.18)


def add_appendix_b(page: fitz.Page, fonts: dict[str, str]) -> None:
    textbox(page, fitz.Rect(51, 687, 330, 708), "B.11 Kernel, contato e enriquecimentos", fontname="LatoBoldAppB", fontfile=fonts["lato_bold"], fontsize=11.2, color=NAVY, lineheight=1)
    text = (
        "• Orientação pertence a K, o indexa externamente ou define uma família?\n"
        "• Relação pode ser reduzida a transformação sem importar estrutura adicional?\n"
        "• Qual contrato separa evento, readout, evidência, julgamento e resíduo?\n"
        "• Quando enriquecer, de-enriquecer ou estruturar prospectivamente por risco?"
    )
    textbox(page, fitz.Rect(51, 716, 544, 786), text, fontname="NotoAppB", fontfile=fonts["noto"], fontsize=8.4, color=NAVY, lineheight=1.18)


def update_glossary(page: fitz.Page, fonts: dict[str, str]) -> None:
    add_redaction(page, fitz.Rect(54, 442, 542, 470))
    page.apply_redactions()
    # Reconstruct both glossary cells after redaction. Keeping the split and
    # row height explicit prevents the replacement from erasing the grid.
    row_fill = (244 / 255, 246 / 255, 246 / 255)
    row_rule = (201 / 255, 211 / 255, 215 / 255)
    left_cell = fitz.Rect(51, 445.7, 297.65, 469.55)
    right_cell = fitz.Rect(297.65, 445.7, 544.25, 469.55)
    page.draw_rect(left_cell, color=row_rule, fill=row_fill, width=0.35, overlay=True)
    page.draw_rect(right_cell, color=row_rule, fill=row_fill, width=0.35, overlay=True)
    textbox(page, fitz.Rect(56.5, 448, 292, 468), "Resíduo", fontname="NotoGlossTerm", fontfile=fonts["noto"], fontsize=8.5, color=NAVY, lineheight=1)
    textbox(page, fitz.Rect(303, 448, 539, 468), "Ver adendo v0.2 abaixo.", fontname="NotoGlossDef", fontfile=fonts["noto"], fontsize=8.1, color=NAVY, lineheight=1.1)
    textbox(page, fitz.Rect(51, 620, 544, 638), "ADENDO V0.2", fontname="LatoBoldGloss", fontfile=fonts["lato_bold"], fontsize=9.0, color=ORANGE, lineheight=1)
    text = (
        "Kernel  Hipótese provisória de orientação/contexto, distinção, relação/transformação e composição; não se afirma mínimo ou suficiente.\n"
        "Ground  Alvo, situação ou processo sobre o qual a linguagem opera.\n"
        "Contato  Interpretação, ação/probe e readout que ligam representação e ground.\n"
        "Enriquecimento  Estrutura adicionável ou removível para satisfazer uma obrigação explícita.\n"
        "Evento de não fechamento  Ocorrência em que uma expectativa de fechamento ou preservação deixa de se cumprir.\n"
        "Resíduo  Representação tipada do que não fechou após readout, comparação e julgamento; não é automaticamente o evento."
    )
    textbox(page, fitz.Rect(51, 647, 544, 784), text, fontname="NotoGlossAdd", fontfile=fonts["noto"], fontsize=8.2, color=NAVY, lineheight=1.2)


def update_final_note(page: fitz.Page, fonts: dict[str, str]) -> None:
    panel(page, fitz.Rect(68, 357, 527, 471), stroke=PURPLE, fill=(0.97, 0.96, 0.97), radius=6, width=1)
    textbox(page, fitz.Rect(84, 374, 511, 394), "NOTA DA EDIÇÃO 0.2", fontname="LatoBoldFinal", fontfile=fonts["lato_bold"], fontsize=10.0, color=PURPLE, lineheight=1)
    text = (
        "O kernel candidato não é um novo inventário nem uma conclusão formal. Ele é uma hipótese a ser quebrada "
        "por testes de dependência, contato, reconstrução e utilidade operacional. A integridade documental desta "
        "edição foi verificada; o estatuto conceitual de K/G/C/E, da orientação e da minimalidade permanece provisório."
    )
    textbox(page, fitz.Rect(84, 405, 511, 454), text, fontname="NotoFinal", fontfile=fonts["noto"], fontsize=8.8, color=NAVY, lineheight=1.25)


def renumber_shifted_appendices(doc: fitz.Document, fonts: dict[str, str]) -> None:
    for index, number in zip(range(58, 64), range(59, 65)):
        page = doc[index]
        add_redaction(page, fitz.Rect(278, 805, 317, 828))
        page.apply_redactions()
        centered_text(page, fitz.Rect(280, 806, 315, 827), str(number), fontname=f"NotoPage{number}", fontfile=fonts["noto"], fontsize=9.5, color=NAVY)


def rebuild_outline(doc: fitz.Document) -> None:
    """Complete the Writer outline with all v0.2 additions."""
    toc = doc.get_toc()

    def insert_after(title: str, page: int, entry: list[object]) -> None:
        for index, item in enumerate(toc):
            if item[1] == title and item[2] == page:
                toc.insert(index + 1, entry)
                return
        raise RuntimeError(f"Outline anchor not found: {title!r} on page {page}")

    insert_after("Questões abertas", 44, [2, "13.7 Composição sem colapso", 44])
    insert_after("Questões abertas", 47, [2, "14.6 Minimalismo como hipótese epistemológica", 47])

    appendix_index = next(
        index for index, item in enumerate(toc) if item[1] == "Apêndice A - Ledger de claims, premissas e limites"
    )
    toc[appendix_index:appendix_index] = [
        [1, "17. Em busca do kernel mínimo", 55],
        [2, "17.1 Kernel, ground, contact e enrichments", 56],
        [2, "17.2 Do contato ao resíduo", 57],
        [2, "17.3 Reconstruções e testes de ruptura", 58],
    ]
    insert_after("B.10 Produto e governança", 61, [2, "B.11 Kernel, contato e enriquecimentos", 61])
    doc.set_toc(toc)


def declare_untagged(doc: fitz.Document) -> None:
    """Do not claim a complete tag tree when patch pages are not structurally tagged."""
    catalog = doc.pdf_catalog()
    doc.xref_set_key(catalog, "MarkInfo", "null")
    doc.xref_set_key(catalog, "StructTreeRoot", "null")


def metadata(doc: fitz.Document) -> None:
    meta = doc.metadata
    meta.update(
        {
            "title": "Entre Sistemas e Categorias",
            "author": "Victor Boscaro; Vladimir Rondelli",
            "subject": "Pensamento sistêmico, teoria das categorias, epistemologia operacional e hipótese do kernel candidato",
            "keywords": "category theory, systems thinking, probes, lenses, residue, analogy, composition, epistemology, kernel, contact, enrichment",
            "creator": f"Writer; edição v0.2 por pipeline semântico-visual PyMuPDF {fitz.__version__}",
            "producer": f"CyberAlchemy PDF patch pipeline v0.2 / PyMuPDF {fitz.__version__}",
        }
    )
    doc.set_metadata(meta)


def _verify_document(doc: fitz.Document) -> None:
    if len(doc) != 64:
        raise RuntimeError(f"Expected 64 pages, found {len(doc)}")
    meta = doc.metadata
    if meta.get("author") != "Victor Boscaro; Vladimir Rondelli":
        raise RuntimeError(f"Incorrect author metadata: {meta.get('author')!r}")
    all_text = "\n".join(page.get_text() for page in doc)
    normalized_text = " ".join(all_text.replace("\u00a0", " ").split())
    forbidden = [
        "Três registros do problema",
        "versão 0.1",
        "os registros sejam equivalentes",
        "O residual aparece",
        "próximo enriquecimento",
    ]
    for phrase in forbidden:
        if phrase in normalized_text:
            raise RuntimeError(f"Superseded text remains extractable: {phrase!r}")
    page8_lines = {
        " ".join(line.replace("\u00a0", " ").split()) for line in doc[7].get_text().splitlines()
    }
    if "alogias • hipóteses" in page8_lines:
        raise RuntimeError("Page 8 still contains the typo 'alogias • hipóteses'")
    required = [
        "Três tradições complementares",
        "17. Em busca do kernel mínimo",
        "OCORRÊNCIA EMERGENTE, REPRESENTAÇÃO DERIVADA",
        "13.7 Composição sem colapso",
        "14.6 Minimalismo como hipótese epistemológica",
        "B.11 Kernel, contato e enriquecimentos",
        "analogias • hipóteses",
        "O resíduo aparece na composição",
        "Esse resíduo orienta o próximo diagnóstico",
        "Kernel Hipótese provisória",
    ]
    for phrase in required:
        if phrase not in normalized_text:
            raise RuntimeError(f"Required text missing: {phrase!r}")
    required_outline = {
        "13.7 Composição sem colapso": 44,
        "14.6 Minimalismo como hipótese epistemológica": 47,
        "17. Em busca do kernel mínimo": 55,
        "17.1 Kernel, ground, contact e enrichments": 56,
        "17.2 Do contato ao resíduo": 57,
        "17.3 Reconstruções e testes de ruptura": 58,
        "B.11 Kernel, contato e enriquecimentos": 61,
    }
    outline = {title: page for _, title, page in doc.get_toc()}
    for title, page in required_outline.items():
        if outline.get(title) != page:
            raise RuntimeError(f"Outline entry missing or incorrect: {title!r} -> {outline.get(title)!r}")
    catalog = doc.pdf_catalog()
    for key in ("MarkInfo", "StructTreeRoot"):
        if doc.xref_get_key(catalog, key)[0] != "null":
            raise RuntimeError(f"PDF must be honestly declared untagged; catalog still has {key}")
    for pno, page in enumerate(doc, 1):
        page_text = page.get_text().replace("\u00a0", " ")
        if "Victor Boscaro" not in page_text or "Vladimir Rondelli" not in page_text:
            raise RuntimeError(f"Invisible authorship missing from page {pno}")
        marks = []
        for image in page.get_images(full=True):
            for rect in page.get_image_rects(image[0]):
                if abs(rect.x0 - 547.304) < 0.8 and abs(rect.y0 - 806.89) < 0.8 and rect.width <= 16 and rect.height <= 16:
                    marks.append(rect)
        if not marks:
            raise RuntimeError(f"CyberAlchemy mark missing from page {pno}")
    glossary = doc[61]
    glossary_text = glossary.get_text().replace("\u00a0", " ")
    if "Ver adendo v0.2 abaixo." not in glossary_text:
        raise RuntimeError("Glossary residue row does not point to the v0.2 addendum")
    row_rects = [drawing["rect"] for drawing in glossary.get_drawings()]
    if not any(
        abs(rect.x0 - 51) < 0.8
        and abs(rect.x1 - 297.65) < 0.8
        and abs(rect.y0 - 445.7) < 0.8
        and abs(rect.y1 - 469.55) < 0.8
        for rect in row_rects
    ) or not any(
        abs(rect.x0 - 297.65) < 0.8
        and abs(rect.x1 - 544.25) < 0.8
        and abs(rect.y0 - 445.7) < 0.8
        and abs(rect.y1 - 469.55) < 0.8
        for rect in row_rects
    ):
        raise RuntimeError("Glossary residue row grid was not reconstructed")
    if doc.is_form_pdf:
        raise RuntimeError("Unexpected AcroForm in output")


def verify(doc_path: Path) -> None:
    with fitz.open(doc_path) as doc:
        _verify_document(doc)


def build(source: Path, destination: Path, keep_temp: bool) -> None:
    if source.resolve() == destination.resolve():
        raise ValueError("Input and output must be different files")
    if not source.exists():
        raise FileNotFoundError(source)
    actual_source_hash = sha256(source)
    if actual_source_hash != SOURCE_SHA256:
        raise RuntimeError(
            f"Immutable source hash mismatch: expected {SOURCE_SHA256}, found {actual_source_hash}"
        )
    TEMP_ROOT.mkdir(parents=True, exist_ok=True)
    fonts = font_paths(acquire_fonts(TEMP_ROOT / "fonts"))
    doc = fitz.open(source)
    if len(doc) != 60:
        raise RuntimeError(f"Immutable input must have 60 pages, found {len(doc)}")
    logo = extract_logo(doc)

    patch_opening(doc[0], fonts)
    patch_method_page(doc[6], fonts)
    add_summary_seam(doc[2], fonts)
    patch_contents(doc[3], fonts)
    draw_traditions_figure(doc[7], fonts)
    add_residue_seam(doc[39], fonts)
    add_composition_seam(doc[43], fonts)
    add_minimalism_seam(doc[46], fonts)
    add_chapter_pointer(doc[53], fonts)
    add_appendix_a(doc[54], fonts)
    add_appendix_b(doc[56], fonts)
    update_glossary(doc[57], fonts)
    update_final_note(doc[59], fonts)

    add_chapter_pages(doc, fonts, logo)
    renumber_shifted_appendices(doc, fonts)
    rebuild_outline(doc)
    declare_untagged(doc)
    metadata(doc)
    doc.subset_fonts(verbose=False, fallback=False)

    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.stem}.", suffix=".tmp.pdf", dir=destination.parent
    )
    os.close(fd)
    temporary = Path(temporary_name)
    temporary.unlink()
    try:
        # Do not merge duplicate objects: the source contains many font subsets
        # with similar descriptors but different encoding tables.
        doc.save(temporary, garbage=1, deflate=True)
        doc.close()
        verify(temporary)
        os.replace(temporary, destination)
    finally:
        if not doc.is_closed:
            doc.close()
        temporary.unlink(missing_ok=True)
    if not keep_temp:
        shutil.rmtree(TEMP_ROOT, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()
    build(args.input.resolve(), args.output.resolve(), args.keep_temp)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
