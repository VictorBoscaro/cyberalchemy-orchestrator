from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path

import fitz
from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


def render_mark(mark_path: Path, scale: float = 4.0) -> bytes:
    source = mark_path.read_bytes()
    document = fitz.open(stream=source, filetype="svg")
    pixmap = document[0].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=True)
    raster = Image.open(BytesIO(pixmap.tobytes("png"))).convert("RGBA")
    alpha = raster.getchannel("A")
    width, height = raster.size
    stops = (
        (0.0, (0xE6, 0x00, 0x23)),
        (0.62, (0xCC, 0x00, 0x00)),
        (1.0, (0xEA, 0x58, 0x0C)),
    )

    def gradient_color(x: int, y: int) -> tuple[int, int, int, int]:
        position = ((x / (width - 1)) + (y / (height - 1))) / 2
        for index in range(len(stops) - 1):
            start_position, start_color = stops[index]
            end_position, end_color = stops[index + 1]
            if position <= end_position:
                ratio = (position - start_position) / (
                    end_position - start_position
                )
                color = tuple(
                    round(start + ((end - start) * ratio))
                    for start, end in zip(start_color, end_color, strict=True)
                )
                return (*color, 255)
        return (*stops[-1][1], 255)

    gradient = Image.new("RGBA", raster.size)
    gradient.putdata(
        [gradient_color(x, y) for y in range(height) for x in range(width)]
    )
    gradient.putalpha(alpha)
    output = BytesIO()
    gradient.save(output, format="PNG")
    return output.getvalue()


def watermark_mark(mark_png: bytes, opacity: float = 0.022) -> bytes:
    image = Image.open(BytesIO(mark_png)).convert("RGBA")
    alpha = image.getchannel("A").point(lambda value: round(value * opacity))
    image.putalpha(alpha)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def edge_vignette(width: float, height: float) -> bytes:
    pixel_width = round(width)
    pixel_height = round(height)
    # Let the lighter warm edge settle imperceptibly into the paper colour.
    left_fade = right_fade = top_fade = bottom_fade = 72.0

    def fade(distance: float, limit: float) -> float:
        if distance >= limit:
            return 0.0
        position = 1.0 - (distance / limit)
        return position**3 * (position * ((6.0 * position) - 15.0) + 10.0)

    pixels: list[tuple[int, int, int, int]] = []
    for y in range(pixel_height):
        top_strength = fade(y, top_fade)
        bottom_strength = fade(pixel_height - 1 - y, bottom_fade)
        for x in range(pixel_width):
            strength = max(
                top_strength,
                bottom_strength,
                fade(x, left_fade),
                fade(pixel_width - 1 - x, right_fade),
            )
            pixels.append((241, 229, 214, round(255 * strength)))

    image = Image.new("RGBA", (pixel_width, pixel_height))
    image.putdata(pixels)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def create_overlay(reader: PdfReader, mark_png: bytes) -> BytesIO:
    overlay_stream = BytesIO()
    overlay = canvas.Canvas(overlay_stream)
    footer_mark = ImageReader(BytesIO(mark_png))
    watermark = ImageReader(BytesIO(watermark_mark(mark_png)))
    vignette_cache: dict[tuple[float, float], ImageReader] = {}

    page_count = len(reader.pages)

    for page_index, page in enumerate(reader.pages):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        overlay.setPageSize((width, height))

        page_size = (width, height)
        if page_size not in vignette_cache:
            vignette_cache[page_size] = ImageReader(
                BytesIO(edge_vignette(width, height))
            )
        overlay.drawImage(
            vignette_cache[page_size],
            0,
            0,
            width=width,
            height=height,
            mask="auto",
        )

        watermark_size = 280.0
        overlay.drawImage(
            watermark,
            (width - watermark_size) / 2,
            (height - watermark_size) / 2,
            width=watermark_size,
            height=watermark_size,
            mask="auto",
        )

        mark_size = 13.0
        font_size = 6.6
        name = "Victor Boscaro"
        is_final_page = page_index == page_count - 1
        name_width = (
            stringWidth(name, "Helvetica-Bold", font_size)
            if is_final_page
            else 0.0
        )
        gap = 5.0
        total_width = mark_size + (gap + name_width if is_final_page else 0.0)
        right_edge = width - 62.0
        x = right_edge - total_width
        y = 29.5

        overlay.drawImage(
            footer_mark,
            x,
            y - 2.2,
            width=mark_size,
            height=mark_size,
            mask="auto",
        )
        if is_final_page:
            text_x = x + mark_size + gap
            overlay.setFont("Helvetica-Bold", font_size)
            overlay.setFillColor(HexColor("#17100c"))
            overlay.drawString(text_x, y, name)
        overlay.showPage()

    overlay.save()
    overlay_stream.seek(0)
    return overlay_stream


def stamp_pdf(input_path: Path, output_path: Path, mark_path: Path) -> None:
    reader = PdfReader(str(input_path))
    overlay = PdfReader(create_overlay(reader, render_mark(mark_path)))
    writer = PdfWriter()

    for page, overlay_page in zip(reader.pages, overlay.pages, strict=True):
        page.merge_page(overlay_page)
        writer.add_page(page)

    if reader.metadata:
        writer.add_metadata(
            {key: value for key, value in reader.metadata.items() if value is not None}
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as output:
        writer.write(output)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add a mark-only footer, a final-page author signature, and a faint watermark."
    )
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_pdf", type=Path)
    parser.add_argument(
        "--mark",
        type=Path,
        default=Path(__file__).with_name("cyberalchemy-mark.svg"),
    )
    args = parser.parse_args()
    stamp_pdf(args.input_pdf.resolve(), args.output_pdf.resolve(), args.mark.resolve())


if __name__ == "__main__":
    main()
