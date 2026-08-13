# document-pdf-typesetter

Renders a Markdown document as a typeset one-page PDF. The layout is data: a JSON theme holds the
page, palette, fonts, type scale, label band, ornaments, and footer, so a new look is a new theme
file rather than a new script.

## Install

```
pip install reportlab        # required
pip install pymupdf          # optional, only for --preview
```

## Use

```
python typeset.py -i examples/anton-introduction.md -o out/anton.pdf \
    --preview out/anton.png --max-pages 1

python typeset.py --emit-theme > themes/my-theme.json
python typeset.py -i doc.md -o doc.pdf -t themes/my-theme.json
python typeset.py -i doc.md -o doc.pdf \
    --set page.size='"LETTER"' --set palette.accent='"#1f5f4a"' --set type.body.size=10.5
```

`--set` takes JSON values, so strings need inner quotes. `--emit-theme` prints the theme after
overrides, which is the fastest way to see every available key.

## Layout

- `typeset.py` — CLI and renderer, the only code
- `themes/quiet-paper.json` — default theme (warm paper, Palatino/Constantia, rust accent)
- `examples/anton-introduction.md` — a document in the supported Markdown subset
- `SKILL.md` — agent-facing instructions; copy the folder into `.claude/skills/` to use it as a skill

## Notes

- Fonts are looked up by filename in `fonts.search_dirs` and fall back to built-in faces when
  missing, so the render works on a machine without Palatino or Constantia — it just looks
  different.
- `--max-pages 1` turns "it must fit on one page" into a non-zero exit code, which makes the
  constraint checkable in a script instead of by eye.
- The default theme reproduces the hand-written `*_introduction.py` scripts (kept in `examples/`). Rendering
  `anton-introduction.md` through this tool yields text extraction identical to
  `examples/anton_introduction_handwritten.py`. The Victor pair differs by one clause, because that clause
  already differs between its `.md` and its `.py` — not because the renderer diverges.
