from copy import copy
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "plans"
    / "governed-agent-work-infrastructure"
    / "essays"
    / "work-context-system-view"
    / "pdf-version"
    / "work-context-system-view.html"
)
OUTPUT = SOURCE.parent

SLICES = [
    (0, 7, "Opening and first section"),
    (15, 29, "Problem, Reading Map, and scope proposal"),
    (29, 38, "Five paths and complementary traversal"),
    (105, 115, "Recursive work and lineage"),
    (180, 184, "Candidate invariants"),
    (201, 213, "First vertical slice"),
    (219, 221, "Open questions"),
    (232, 234, "System-view result"),
]

COMMON = r"""
.sample-note {
  margin: 0 0 7mm;
  color: #6f2519;
  font: 700 7.4pt/1 Arial, sans-serif;
  letter-spacing: 1.15pt;
  text-transform: uppercase;
}
.sample-panel {
  break-before: page;
}
.sample-panel:first-of-type {
  break-before: auto;
}
.sample-panel > :first-child {
  margin-top: 0;
}
.sample-panel .result-heading {
  break-before: auto;
}
.sample-panel:last-child {
  min-height: 120mm;
}
"""

THEMES = {
    "quiet-corners": r"""
@page {
  size: A4;
  margin: 19mm 22mm 16mm;
  background: #f4eadc;
  @top-left-corner {
    content: "";
    background:
      linear-gradient(rgba(23,16,12,.72), rgba(23,16,12,.72))
      left 8mm top 8mm / 6mm .28pt no-repeat,
      linear-gradient(rgba(23,16,12,.72), rgba(23,16,12,.72))
      left 8mm top 8mm / .28pt 5mm no-repeat;
  }
  @top-right-corner {
    content: "";
    background:
      linear-gradient(rgba(23,16,12,.72), rgba(23,16,12,.72))
      right 8mm top 8mm / 6mm .28pt no-repeat,
      linear-gradient(rgba(23,16,12,.72), rgba(23,16,12,.72))
      right 8mm top 8mm / .28pt 5mm no-repeat;
  }
  @bottom-left-corner {
    content: "";
    background:
      linear-gradient(rgba(23,16,12,.72), rgba(23,16,12,.72))
      left 8mm bottom 8mm / 6mm .28pt no-repeat,
      linear-gradient(rgba(23,16,12,.72), rgba(23,16,12,.72))
      left 8mm bottom 8mm / .28pt 5mm no-repeat;
  }
  @bottom-right-corner {
    content: "";
    background:
      linear-gradient(rgba(23,16,12,.72), rgba(23,16,12,.72))
      right 8mm bottom 8mm / 6mm .28pt no-repeat,
      linear-gradient(rgba(23,16,12,.72), rgba(23,16,12,.72))
      right 8mm bottom 8mm / .28pt 5mm no-repeat;
  }
}
body::before { opacity: .58; }
h2 { border-top-width: .45pt; }
pre { box-shadow: none; border-radius: 0 .7mm .7mm 0; }
.concept-figure { box-shadow: none; border-width: .55pt; }
table { border-width: .5pt; }
""",
    "side-stitches": r"""
@page {
  size: A4;
  margin: 19mm 22mm 16mm;
  background: #f7eee2;
  @left-middle {
    content: "";
    background:
      linear-gradient(rgba(101,64,48,.62), rgba(101,64,48,.62))
      center top 36% / .32pt 9mm no-repeat,
      linear-gradient(rgba(180,63,39,.58), rgba(180,63,39,.58))
      center bottom 36% / .32pt 5mm no-repeat;
  }
  @right-middle {
    content: "";
    background:
      linear-gradient(rgba(101,64,48,.62), rgba(101,64,48,.62))
      center top 36% / .32pt 9mm no-repeat,
      linear-gradient(rgba(180,63,39,.58), rgba(180,63,39,.58))
      center bottom 36% / .32pt 5mm no-repeat;
  }
}
html, body { background: #f7eee2; }
body::before {
  background: linear-gradient(180deg, #faf3e9 0%, #f5eadc 100%);
}
h2 {
  padding: 0 0 0 4mm;
  border-top: 0;
  border-left: 1.15pt solid #a43824;
  color: #201713;
}
h3 { color: #702215; }
blockquote {
  padding-left: 5mm;
  border-left: 0;
  border-top: .6pt solid #a43824;
  border-bottom: .35pt solid rgba(112,34,21,.35);
  background: transparent;
}
pre { box-shadow: none; border-left-width: 2px; border-radius: 0; }
th { background: #742619; }
.concept-figure {
  box-shadow: none;
  border-color: rgba(112,76,58,.52);
  border-radius: .8mm;
}
""",
    "center-signals": r"""
@page {
  size: A4;
  margin: 19mm 22mm 16mm;
  background: #f6ecdf;
  @top-center {
    content: "";
    background:
      radial-gradient(circle, #a83a26 0 1.1px, transparent 1.3px)
      center 8mm / 4mm 4mm no-repeat,
      linear-gradient(rgba(23,16,12,.55), rgba(23,16,12,.55))
      center 10mm / 13mm .28pt no-repeat;
  }
  @bottom-center {
    content: "";
    background:
      radial-gradient(circle, #a83a26 0 1.1px, transparent 1.3px)
      center bottom 8mm / 4mm 4mm no-repeat,
      linear-gradient(rgba(23,16,12,.55), rgba(23,16,12,.55))
      center bottom 10mm / 13mm .28pt no-repeat;
  }
}
html, body { background: #f6ecdf; }
body::before {
  background:
    radial-gradient(circle at 50% 0%, rgba(181,64,39,.055), transparent 24%),
    linear-gradient(145deg, #f9f1e6 0%, #f3e7d8 100%);
}
h1::before {
  width: 23mm;
  height: 1.5mm;
  border-radius: 0;
}
h2 {
  border-top: .35pt solid rgba(106,56,38,.48);
  color: #772416;
}
h2::after {
  content: "";
  display: block;
  width: 2.2mm;
  height: 2.2mm;
  margin-top: 2mm;
  border: .45pt solid #9e3421;
  border-radius: 50%;
}
pre {
  box-shadow: none;
  border-left-width: 1.8px;
  border-radius: 0;
  background: #27201c;
}
.concept-figure {
  padding-left: 0;
  padding-right: 0;
  border-left: 0;
  border-right: 0;
  border-radius: 0;
  box-shadow: none;
  background: rgba(255,250,241,.32);
}
table {
  border-left: 0;
  border-right: 0;
}
td {
  border-left: 0;
  border-right: 0;
}
"""
}


def build_sample(slug: str, theme_css: str) -> Path:
    source = BeautifulSoup(SOURCE.read_text(encoding="utf-8"), "html.parser")
    children = list(source.main.find_all(recursive=False))

    document = BeautifulSoup(
        "<!doctype html><html lang='en'><head></head><body><main></main></body></html>",
        "html.parser",
    )
    for tag in source.head.find_all(recursive=False):
        document.head.append(copy(tag))

    document.title.string = f"{source.title.string} - design sample: {slug}"
    style = document.new_tag("style")
    style.string = COMMON + theme_css
    document.head.append(style)

    for index, (start, end, label) in enumerate(SLICES):
        panel = document.new_tag("section")
        panel["class"] = ["sample-panel", f"sample-panel-{index + 1}"]
        if index == 0:
            note = document.new_tag("div")
            note["class"] = ["sample-note"]
            note.string = f"Design study / excerpt, not a complete edition / {slug}"
            panel.append(note)
        for child in children[start:end]:
            panel.append(copy(child))
        document.main.append(panel)

    output = OUTPUT / f"work-context-system-view-sample-{slug}.html"
    output.write_text(str(document), encoding="utf-8")
    return output


def main() -> None:
    for slug, css in THEMES.items():
        print(build_sample(slug, css))


if __name__ == "__main__":
    main()
