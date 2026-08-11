# PDF source pipeline: *Entre Sistemas e Categorias* v0.2

The repository has no durable Writer/ODT source for the complete 60-page document. The reviewed
PDF is therefore the immutable source snapshot for version 0.2. Its required SHA-256 is
`d29e78998a12697b2fdcdebfab598439cca1a096251b069d65ac134446f8ecd8`; the builder refuses any
other input before applying a patch.

The builder performs real PDF redactions where text or figures are replaced, adds vector text and
diagrams, inserts four pages, completes the outline, and writes the release atomically through a
verified sibling temporary file and `os.replace`. Input and output must be different files, so the
immutable source cannot be overwritten accidentally.

```powershell
python tools/pdf/entre_sistemas_e_categorias_v02.py
```

Input: `output/pdf/entre_sistemas_e_categorias_revisado.pdf`

Output: `output/pdf/entre_sistemas_e_categorias_v0.2.pdf`

The current production guarantee is **semantic-visual reproducibility**, not byte-for-byte
reproducibility. It is tested with PyMuPDF `1.27.2.3`; equivalent rebuilds must preserve page count,
text, outline, metadata, marks, invisible attribution, geometry, and rendered appearance. The
second trailer `/ID` can vary between rebuilds, so a stable binary SHA-256 is not promised. Pinning
that identifier would be required only for a separate binary-reproducibility contract.

The pipeline pins Lato, Carlito, and Noto Serif downloads by SHA-256, uses pinned Lato rather than a
host-local Arial for new invisible attribution, and subsets eligible font programs before release.
It uses `tmp/pdfs/` only for its transient cache and performs structural checks before the atomic
replacement. Visual rendering and inspection remain a release step because extraction checks
cannot establish layout fidelity.

The source snapshot claims a Writer tag tree that cannot honestly include the four patch-generated
pages. Version 0.2 is therefore explicitly emitted as **untagged**. A tagged, accessible edition
requires reconstruction from a complete Writer/ODT or another source capable of producing a
single coherent structure tree and reading order; the PyMuPDF patch pipeline does not claim that
guarantee.
