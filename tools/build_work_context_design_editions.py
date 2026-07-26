from copy import copy
from pathlib import Path

from bs4 import BeautifulSoup

from build_work_context_design_samples import OUTPUT, SOURCE, THEMES


COMMON = r"""
.edition-note {
  margin: 0 0 7mm;
  color: #6f2519;
  font: 700 7.4pt/1 Arial, sans-serif;
  letter-spacing: 1.15pt;
  text-transform: uppercase;
}
"""


def build_edition(slug: str, theme_css: str) -> Path:
    source = BeautifulSoup(SOURCE.read_text(encoding="utf-8"), "html.parser")
    document = BeautifulSoup(
        "<!doctype html><html lang='en'><head></head><body></body></html>",
        "html.parser",
    )

    for tag in source.head.find_all(recursive=False):
        document.head.append(copy(tag))

    document.title.string = f"{source.title.string} - complete design edition: {slug}"
    style = document.new_tag("style")
    style.string = COMMON + theme_css
    document.head.append(style)

    main = copy(source.main)
    note = document.new_tag("div")
    note["class"] = ["edition-note"]
    note.string = f"Design study / complete edition / {slug}"
    main.insert(0, note)
    document.body.append(main)

    output = OUTPUT / f"work-context-system-view-complete-{slug}.html"
    output.write_text(str(document), encoding="utf-8")
    return output


def main() -> None:
    for slug, css in THEMES.items():
        print(build_edition(slug, css))


if __name__ == "__main__":
    main()
