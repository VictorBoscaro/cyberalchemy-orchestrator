from __future__ import annotations

import html
import re
import shutil
import subprocess
import tempfile
import time
import unicodedata
from pathlib import Path

import mistune
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "docs"
    / "architecture"
    / "agent-language-system-view.md"
)
OUTPUT = SOURCE.parent / "pdf-versions"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


BASE_CSS = """
@page { size: A4; margin: 18mm 17mm 20mm; }
* { box-sizing: border-box; }
html { print-color-adjust: exact; -webkit-print-color-adjust: exact; }
body { margin: 0; hyphens: none; }
main { position: relative; }
h1, h2, h3 { break-after: avoid; }
p, li { orphans: 3; widows: 3; }
table, pre, blockquote { break-inside: avoid; }
table { width: 100%; border-collapse: collapse; }
thead { display: table-row-group; }
th, td { vertical-align: top; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; }
code { font-family: "Cascadia Mono", Consolas, monospace; }
a { color: inherit; text-decoration: none; }
.rendered-diagram { margin: 6mm 0; break-inside: avoid; color: inherit; }
.rendered-diagram svg { display: block; width: 100%; height: auto; overflow: visible; }
.rendered-diagram .node rect {
  fill: var(--diagram-node, #fff);
  stroke: var(--diagram-edge, #334155);
  stroke-width: 1.8;
  rx: 8;
}
.rendered-diagram .node text, .rendered-diagram .edge-label {
  fill: var(--diagram-text, currentColor);
  font-family: Arial, Helvetica, sans-serif;
}
.rendered-diagram .node text { font-size: 14px; font-weight: 700; }
.rendered-diagram .edge-label { font-size: 11px; font-weight: 600; }
.rendered-diagram .edge {
  fill: none;
  stroke: var(--diagram-edge, #334155);
  stroke-width: 2;
  marker-end: url(#arrow);
}
.rendered-diagram .feedback {
  fill: none;
  stroke: var(--diagram-accent, #b4442a);
  stroke-width: 1.8;
  stroke-dasharray: 7 5;
  marker-end: url(#arrow-accent);
}
"""


THEMES = {
    "01-editorial": """
@page { background: #f8f2e8; }
body { --diagram-node: #fffaf2; --diagram-edge: #332a22; --diagram-accent: #b4442a;
  --diagram-text: #211d18; color: #211d18; background: #f8f2e8;
  font: 10.4pt/1.56 Georgia, serif; }
main { padding-top: 8mm; }
main::before { content: ""; display: block; width: 34mm; height: 2.5mm;
  margin-bottom: 10mm; background: #b4442a; border-radius: 9px; }
h1 { font: 700 29pt/1.02 Georgia, serif; letter-spacing: -0.7pt; margin: 0 0 9mm; }
h2 { font: 700 18pt/1.12 Georgia, serif; margin: 11mm 0 4mm; color: #87321f; }
h3 { font: 700 12.5pt/1.2 Arial, sans-serif;
  letter-spacing: 0.8pt; margin: 8mm 0 3mm; }
p { margin: 0 0 3.5mm; }
ul, ol { padding-left: 6mm; }
li { margin: 1.2mm 0; }
table { margin: 5mm 0; font: 8.4pt/1.35 Arial, sans-serif; background: #fffaf2; }
th { background: #332a22; color: white; }
th, td { border: 0.25mm solid #c9b8a5; padding: 2.2mm; }
pre { padding: 4mm; background: #2b2520; color: #f8efe4; border-left: 2mm solid #b4442a; }
code:not(pre code) { color: #87321f; background: #eadfd1; padding: 0.2mm 0.7mm; }
blockquote { margin: 5mm 0; padding: 2mm 5mm; border-left: 1.5mm solid #b4442a; }
""",
    "02-swiss": """
@page { background: #fff; }
body { --diagram-node: #fff; --diagram-edge: #111; --diagram-accent: #ff3b30;
  --diagram-text: #111; color: #111; background: white;
  font: 9.8pt/1.48 Arial, Helvetica, sans-serif; }
main { border-top: 5mm solid #111; padding-top: 8mm; }
main::before { content: ""; position: absolute; top: -5mm; right: 0; width: 28mm;
  height: 5mm; background: #ff3b30; }
h1 { max-width: 145mm; font: 800 30pt/0.96 Arial, sans-serif; letter-spacing: -1.6pt;
  margin: 0 0 11mm; }
h2 { font: 800 17pt/1 Arial, sans-serif; letter-spacing: -0.4pt; margin: 11mm 0 4mm;
  padding-bottom: 2mm; border-bottom: 0.6mm solid #111; }
h3 { font: 700 11pt/1.2 Arial, sans-serif; margin: 7mm 0 2.5mm; }
p { margin: 0 0 3.2mm; }
ul, ol { padding-left: 5.5mm; }
li { margin: 1mm 0; }
table { margin: 5mm 0; font-size: 8.1pt; }
th { text-align: left; border-bottom: 1mm solid #111; }
td { border-bottom: 0.25mm solid #aaa; }
th, td { padding: 2mm 1.5mm; }
pre { padding: 4mm; background: #f1f1f1; border: 0.4mm solid #111; }
code:not(pre code) { background: #efefef; padding: 0.2mm 0.6mm; }
""",
    "03-blueprint": """
@page { background: #0c2f4f; }
body { --diagram-node: #0b2238; --diagram-edge: #7dd3fc; --diagram-accent: #f4b942;
  --diagram-text: #dcecff; color: #dcecff; background: #0c2f4f;
  font: 9.5pt/1.52 "Segoe UI", Arial, sans-serif; }
main { padding: 7mm; border: 0.35mm solid #72b6e8;
  background-image: linear-gradient(rgba(114,182,232,.10) .25mm, transparent .25mm),
  linear-gradient(90deg, rgba(114,182,232,.10) .25mm, transparent .25mm);
  background-size: 7mm 7mm; }
main::before, main::after { content: ""; position: absolute; width: 15mm; height: 15mm; }
main::before { top: -0.35mm; left: -0.35mm; border-top: 1.2mm solid #7dd3fc;
  border-left: 1.2mm solid #7dd3fc; }
main::after { right: -0.35mm; bottom: -0.35mm; border-right: 1.2mm solid #7dd3fc;
  border-bottom: 1.2mm solid #7dd3fc; }
h1 { font: 650 26pt/1.05 "Segoe UI", sans-serif; color: white; letter-spacing: -0.5pt;
  margin: 0 0 10mm; }
h2 { font: 650 16pt/1.1 "Segoe UI", sans-serif; color: #7dd3fc; margin: 10mm 0 4mm;
  border-left: 1.5mm solid #7dd3fc; padding-left: 3mm; }
h3 { font: 650 11pt/1.2 "Segoe UI", sans-serif; color: #bfe5ff; margin: 7mm 0 3mm; }
p { margin: 0 0 3.2mm; }
ul, ol { padding-left: 6mm; }
li { margin: 1mm 0; }
table { margin: 5mm 0; font-size: 7.9pt; background: rgba(4,24,43,.82); }
th { color: white; background: #145885; }
th, td { border: 0.25mm solid #4a8dbb; padding: 2mm; }
pre { padding: 4mm; color: #dff5ff; background: #061d31; border: 0.3mm solid #7dd3fc; }
code:not(pre code) { color: #b9edff; background: #174d70; padding: 0.2mm 0.6mm; }
""",
    "04-academic": """
@page { size: A4; margin: 22mm 21mm 23mm; background: #fff; }
body { --diagram-node: #fff; --diagram-edge: #222; --diagram-accent: #666;
  --diagram-text: #171717; color: #171717; background: #fff;
  font: 10.2pt/1.62 "Times New Roman", Times, serif; }
main { padding-top: 5mm; }
main::before { content: ""; display: block; width: 100%; height: 0.3mm; background: #111;
  box-shadow: 0 2.2mm 0 #111; margin-bottom: 10mm; }
h1 { text-align: center; font: 700 24pt/1.12 "Times New Roman", serif; margin: 0 7mm 11mm; }
h2 { font: 700 15pt/1.2 "Times New Roman", serif; margin: 10mm 0 3mm; }
h3 { font: italic 700 11.5pt/1.2 "Times New Roman", serif; margin: 7mm 0 2.5mm; }
p { margin: 0 0 3.5mm; text-align: justify; }
ul, ol { padding-left: 7mm; }
li { margin: 1mm 0; }
table { margin: 5mm 0; font-size: 8pt; }
th, td { border-top: 0.3mm solid #222; border-bottom: 0.3mm solid #222; padding: 2mm; }
th { font-weight: 700; }
pre { padding: 4mm; background: #f7f7f7; border-top: 0.3mm solid #222;
  border-bottom: 0.3mm solid #222; }
code:not(pre code) { font-size: 0.92em; }
""",
    "05-studio": """
@page { background: #eef5ed; }
body { --diagram-node: #f7fbf7; --diagram-edge: #336b52; --diagram-accent: #d96c4d;
  --diagram-text: #17231d; color: #17231d; background: #eef5ed;
  font: 9.7pt/1.5 "Trebuchet MS", Arial, sans-serif; }
main { padding: 9mm 8mm; background: white; border-radius: 5mm; box-shadow: inset 0 0 0 0.4mm #8ca891; }
main::before { content: ""; display: block; width: 24mm; height: 24mm; float: right;
  margin: -3mm -2mm 5mm 7mm; border-radius: 50%; background:
  radial-gradient(circle at 35% 35%, #f4b942 0 22%, transparent 23%),
  conic-gradient(#336b52 0 28%, #d96c4d 28% 58%, #8eb69b 58% 100%); }
h1 { font: 800 27pt/1.02 "Trebuchet MS", sans-serif; letter-spacing: -1pt;
  margin: 0 0 10mm; color: #24513d; }
h2 { clear: both; font: 800 16pt/1.1 "Trebuchet MS", sans-serif; color: #24513d;
  margin: 10mm 0 4mm; padding: 2.5mm 3mm; background: #dfece1; border-radius: 2mm; }
h3 { font: 700 11.5pt/1.2 "Trebuchet MS", sans-serif; color: #8f3f2f; margin: 7mm 0 2.5mm; }
p { margin: 0 0 3.2mm; }
ul, ol { padding-left: 6mm; }
li { margin: 1mm 0; }
table { margin: 5mm 0; font-size: 8pt; overflow: hidden; border-radius: 2mm; }
th { color: white; background: #336b52; }
th, td { border: 0.25mm solid #a9beae; padding: 2mm; }
tr:nth-child(even) td { background: #f1f6f1; }
pre { padding: 4mm; color: #f7fff9; background: #254c3a; border-radius: 2mm; }
code:not(pre code) { color: #853a2d; background: #f4e0d9; padding: 0.2mm 0.6mm; }
""",
}


WORK_GRAMMAR_SVG = """
<figure class="rendered-diagram" aria-label="Recursive grammar of work">
<svg viewBox="0 0 800 310" role="img" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
      markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--diagram-edge, #334155)"/>
    </marker>
    <marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5"
      markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--diagram-accent, #b4442a)"/>
    </marker>
  </defs>

  <g class="edge">
    <path d="M105 94 H125"/><path d="M210 94 H230"/>
    <path d="M315 94 H335"/><path d="M445 94 H465"/>
    <path d="M550 94 H570"/><path d="M655 94 H675"/>
  </g>

  <g class="feedback">
    <path d="M270 72 C255 20 185 20 170 72"/>
    <path d="M170 116 C185 166 255 166 270 116"/>
    <path d="M507 116 C505 160 515 196 535 220"/>
    <path d="M727 116 C735 155 730 190 715 220"/>
    <path d="M700 116 C660 180 565 180 520 116"/>
  </g>

  <g class="edge-label">
    <text x="220" y="18" text-anchor="middle">investigates or challenges</text>
    <text x="220" y="174" text-anchor="middle">requests</text>
    <text x="560" y="177" text-anchor="middle">exposes a local planning need</text>
    <text x="733" y="178" text-anchor="middle">reopens</text>
    <text x="615" y="197" text-anchor="middle">reopens</text>
  </g>

  <g class="node">
    <g><rect x="20" y="72" width="85" height="44"/><text x="62.5" y="99" text-anchor="middle">Intent</text></g>
    <g><rect x="125" y="72" width="85" height="44"/><text x="167.5" y="99" text-anchor="middle">Plan</text></g>
    <g><rect x="230" y="72" width="85" height="44"/><text x="272.5" y="99" text-anchor="middle">Research</text></g>
    <g><rect x="335" y="72" width="110" height="44"/><text x="390" y="91" text-anchor="middle"><tspan x="390">Discovery /</tspan><tspan x="390" dy="16">Design</tspan></text></g>
    <g><rect x="465" y="72" width="85" height="44"/><text x="507.5" y="99" text-anchor="middle">Spec</text></g>
    <g><rect x="570" y="72" width="85" height="44"/><text x="612.5" y="99" text-anchor="middle">Code</text></g>
    <g><rect x="675" y="72" width="105" height="44"/><text x="727.5" y="99" text-anchor="middle">Verification</text></g>
    <g><rect x="490" y="220" width="100" height="44"/><text x="540" y="247" text-anchor="middle">Local Plan</text></g>
    <g><rect x="665" y="220" width="100" height="44"/><text x="715" y="247" text-anchor="middle">Research</text></g>
  </g>
</svg>
</figure>
"""


def render_mermaid_blocks(body: str) -> str:
    pattern = re.compile(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        flags=re.DOTALL,
    )
    matches = pattern.findall(body)
    if len(matches) != 1 or "flowchart LR" not in html.unescape(matches[0]):
        raise RuntimeError("Expected exactly one recognized Mermaid flowchart")
    rendered = pattern.sub(WORK_GRAMMAR_SVG, body)
    if 'class="language-mermaid"' in rendered:
        raise RuntimeError("Unrendered Mermaid code remains")
    return rendered


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    return text[end + 5 :]


def normalized_pdf_text(path: Path) -> str:
    text = "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    text = unicodedata.normalize("NFKC", text)
    # PDF extractors may add or omit whitespace at visual line/page boundaries.
    # Removing whitespace verifies the exact ordered character stream while
    # remaining invariant to layout-only wrapping.
    return re.sub(r"\s+", "", text)


def main() -> None:
    if not CHROME.exists():
        raise SystemExit(f"Chrome not found: {CHROME}")

    source_text = strip_frontmatter(SOURCE.read_text(encoding="utf-8"))
    markdown = mistune.create_markdown(
        escape=False,
        plugins=["table", "strikethrough", "task_lists"],
    )
    body = markdown(source_text)
    body = render_mermaid_blocks(body)
    title = "A Composable Language for Governed Agent Work"
    OUTPUT.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(
        prefix="review-pdf-",
        ignore_cleanup_errors=True,
    ) as temp_name:
        temp = Path(temp_name)
        for slug, theme_css in THEMES.items():
            html_path = temp / f"{slug}.html"
            pdf_path = OUTPUT / f"{slug}.pdf"
            document = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>{BASE_CSS}\n{theme_css}</style>
</head>
<body><main>{body}</main></body>
</html>
"""
            html_path.write_text(document, encoding="utf-8")
            profile = temp / f"profile-{slug}"
            command = [
                str(CHROME),
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-extensions",
                f"--user-data-dir={profile}",
                "--no-pdf-header-footer",
                f"--print-to-pdf={pdf_path}",
                html_path.as_uri(),
            ]
            pdf_path.unlink(missing_ok=True)
            process = subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            deadline = time.monotonic() + 35
            previous_size = -1
            stable_checks = 0
            while time.monotonic() < deadline:
                if pdf_path.exists():
                    size = pdf_path.stat().st_size
                    stable_checks = stable_checks + 1 if size == previous_size else 0
                    previous_size = size
                    if size > 10_000 and stable_checks >= 3:
                        break
                if process.poll() is not None and not pdf_path.exists():
                    raise RuntimeError(f"Chrome exited without PDF: {pdf_path}")
                time.sleep(0.4)
            else:
                raise TimeoutError(f"Timed out generating {pdf_path}")

            if process.poll() is None:
                subprocess.run(
                    ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass
            if not pdf_path.exists() or pdf_path.stat().st_size < 10_000:
                raise RuntimeError(f"PDF generation failed: {pdf_path}")

    extracted = {path.name: normalized_pdf_text(path) for path in sorted(OUTPUT.glob("*.pdf"))}
    if len(extracted) != len(THEMES):
        raise RuntimeError(f"Expected {len(THEMES)} PDFs, found {len(extracted)}")
    reference_name, reference_text = next(iter(extracted.items()))
    mismatches = [name for name, text in extracted.items() if text != reference_text]
    if mismatches:
        raise RuntimeError(
            f"Extracted text differs from {reference_name}: {', '.join(mismatches)}"
        )

    for path in sorted(OUTPUT.glob("*.pdf")):
        pages = len(PdfReader(path).pages)
        print(f"{path.name}\t{pages} pages\t{path.stat().st_size} bytes")
    print(f"text_identity\tPASS\t{len(reference_text)} normalized characters")


if __name__ == "__main__":
    main()
