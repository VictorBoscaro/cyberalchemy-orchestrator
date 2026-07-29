# Attacker positions — dispatch 2026-07-29-short-version-pdf-pipeline-review

Workflow evidence only. NOT a review artifact. The review's single artifact is
`review.md`; this file exists so the synthesizer receives each attacker's INITIAL and
FINAL position (P14 collapse detection) without the parent filtering them.

Four attackers, four lenses, `robot_talks: true`. Round 1 = independent parallel attack.
Round 2 = confrontation across lenses, then final position.

---

## Rissanen, Jorma — lens: BYTE ECONOMY

### INITIAL position (round 1)

Corpus read in full; all 5 PDFs inspected at the xref/stream level (fitz `xref_stream_raw`, byte-for-byte, not estimated).

**1. Content streams shipped with no `/Filter` — the pypdf write pass, confirmed.**
`stamp-cyberalchemy.py:184-185`:
```python
with output_path.open("wb") as output:
    writer.write(output)
```
Object 127's dict is `<< ... /Length 129743 >>` with no `/Filter` key (verified via `xref_get_key(127,'Filter') == ('null','null')`); raw bytes start `q\n.23999999 0 0 -.23999999 0 841.91998 cm\n...` — plain-text operators. All four page content streams (objs 127/104/81/114) total 339,970 raw bytes, zero compressed.

Root-cause proof, not hypothesis: diffed the stamped deliverables against the un-stamped variant PDFs, which never go through `stamp_pdf()`. Variants carry only 7,069 uncompressed-stream bytes (1.6% of file); the two stamped outputs carry 339,970 and 270,241 (56.0% and 52.3%). `pypdf.PageObject.merge_page()` decompresses into a ContentStream/operations list and `PdfWriter.write()` serializes back without re-applying Flate; `compress_content_streams()` exists on PageObject and is never called.

Measured `zlib.compress(raw,9)` on actual bytes: obj127 129,743→20,403; obj104 100,634→16,770; obj81 69,025→8,950; obj114 39,597→5,077. Total 339,970 → 52,132, **saving 287,838 bytes (56.0% of the 514,178-byte file)**. Revision PDF: saves 232,241 bytes (52.3%).
Pixel-identity: holds by construction — FlateDecode is lossless.
Fix: in `stamp_pdf()`, after the merge loop and before `writer.write()`: `for p in writer.pages: p.compress_content_streams()`.

**2. ASCII85 wrapping on every embedded raster image.**
`stamp-cyberalchemy.py:96-132` (`create_overlay`, via reportlab canvas). Each image XObject stored as `[/ASCII85Decode /FlateDecode]`. Decoded the six image streams (vignette + footer-mark + watermark, RGB+SMask pairs, objs 59/60/61/62/63/64): stored 42,528 bytes vs inner-flate 34,011. **Saving 8,517 bytes**, from ReportLab's default `rl_config.useA85 = 1`.
Pixel-identity: holds — ASCII85 is a lossless transport codec being removed, not the compression.
Fix: `rl_config.useA85 = 0` before constructing the canvas.

**3. Duplicate RGB image data: footer mark vs watermark.**
`stamp-cyberalchemy.py:55-61` (`watermark_mark`) re-derives a second PNG from the same `mark_png` by scaling only alpha (`image.getchannel("A").point(lambda v: round(v * opacity))`), leaving RGB untouched. **xref 61 and xref 63 are bit-for-bit identical (7,322 bytes each)** — only their SMasks (62 vs 64) differ. **Saving 7,322 bytes.**
Fix: one ImageReader for the RGB plane with two alpha masks, or pikepdf dedupe by stream digest. Combined #2+#3 ≈14,373 bytes, not 15,839 — obj 63's own 1,466-byte ASCII85 share is eliminated by #3 too, not added on top.

**4. Corner-mark CSS gradients — ATTACKED, SURVIVED (negligible).**
`build-short-polished.ps1:63-88`:
```
@top-left-corner {
  background:
    linear-gradient(rgba(27,23,20,.56), rgba(27,23,20,.56)) left 8mm top 8mm / 7mm .4pt no-repeat,
    linear-gradient(rgba(27,23,20,.56), rgba(27,23,20,.56)) left 8mm top 8mm / .4pt 7mm no-repeat;
}
```
Solid-color-as-gradient hack. Checked whether it compiles into 32 separate Pattern/Shading objects (4 corners x 2 backgrounds x 4 pages): it does not — only 8 unique Pattern objects total, already shared across all 4 pages, 517 bytes combined decoded paint content. Not worth restructuring.

**5. Font subset overlap — ATTACKED, SURVIVED (no overlap).**
Six subsets: `AAAAAA+PalatinoLinotype-Bold`, `BAAAAA+Constantia`, `CAAAAA+Arial-BoldMT`, `DAAAAA+Georgia-Bold`, `EAAAAA+ArialMT`, `FAAAAA+Georgia`. Despite `build-short-polished.ps1:11-51` declaring four @font-face weights for "Essay Constantia", only the regular weight is embedded — bold/italic never triggered in the short edition. No two subsets share base font+weight; each font object already a single shared indirect object.

**6. Dead CSS — ATTACKED, SURVIVED (none found).**
Checked ~20 short-edition-only selectors (`.context-field`, `.infra-legend`, `.intention-map`, `.plane-reading`, `.short-status`, etc.) against the built HTML by direct occurrence count (after correcting a buggy first regex pass). All present and used.

**7. 4x SVG rasterization vs native vector — ATTACKED, FAILS the pixel-identity bar.**
`stamp-cyberalchemy.py:16` `render_mark(mark_path, scale=4.0)` rasterizes the 1,125-byte SVG to 480x480, embedded twice (footer 13pt, watermark 280pt @ 2.2% opacity). Native PDF vector would eliminate all six image objects, ~42,528 bytes — second-largest lever — but a renderer antialiases vector strokes at its own device resolution, not byte-identical to the pre-baked alpha-blended raster. Cannot certify pixel-identity; **inadmissible as specified**, reported only in case "pixel-identical" is ever relaxed to "visually equivalent".

### FINAL position (round 2)

**1. Baseline contradiction — measured on the revision, not guessed.** Ashby is right that `-revision.pdf` is untracked and newer; not contested. But the target wasn't self-selected — the dispatch gave the starting measurement on the base file explicitly. Re-ran the identical measurement on the revision rather than assert transfer:
- Content streams, no `/Filter`: revision **270,241 raw → 38,000 at Flate-9, saving 232,241 bytes (52.3% of its 443,651-byte file)**. Same defect, same root cause.
- ASCII85 overhead on the 6 image XObjects: **8,517 bytes, identical to base** — mark/vignette generation is independent of body text/font, so the three distinct text layers don't touch this lever.
- RGB duplicate (obj 61 = 63): **7,322 bytes, identical to base.**
Ranked list holds on the revision with #1's number substituted. Not conceding revision-over-base as "the" target — both are live deliverables sharing one defective code path; now reports both.

**2. Nyquist F10 — HOLDS.** The premise is wrong for the three admissible fixes: `stamp_pdf(input_path, output_path, mark_path)` never touches HTML or Skia. It opens an existing PDF and writes a new one — **it already is the PDF→PDF pass Nyquist wants.** None of the three fixes depend on rasterizer pinning or `/CreationDate`. #1 is proven lossless at the operator-token level (Flate round-trip verified by zlib compress/decompress producing the identical byte stream) — stronger than pixel-identity, since identical content-stream tokens guarantee identical raster output under any conforming interpreter, pinned or not. #2 and #3 proven by direct byte comparison of decoded pixel payloads. No rasterizer was invoked to establish any of this. The one place Nyquist's objection bites was already conceded in round 1: finding #7.

**3. Ordering — CONCEDES action order, HOLDS finding order.** Git hygiene changes no byte number and doesn't reorder findings by size — that ranking is arithmetic, not process. But concedes the dispatch ordering: `stamp-cyberalchemy.py` is untracked, so a fix landed today produces no reviewable diff against a prior committed state — the "fix" and the "first version" would be the same commit. Committing the baseline first is a precondition for the fix to exist as a reviewable delta. "That's an operability argument I don't have standing to overrule from the byte-economy lens." Action order: commit baseline → apply fix. Finding order: unchanged.

**4. Pohl idempotency — CONFIRMED empirically.** Ran `stamp_pdf()` twice, second pass consuming the first pass's output. On a 27-page test document: one stamp produced 2,053,248 bytes; stamping that output again produced 2,110,783 bytes (**+57,535 bytes**), image object count 30 → 36 — a fresh undeduplicated copy of the vignette/mark/watermark set embedded per pass, on top of the visual compounding Pohl flagged. **Not idempotent, and bytes do change with re-stamping.**
The compress fix is orthogonal — harmless, not curative, not aggravating: it operates at serialization time on whatever content stream exists after `merge_page()`. It doesn't touch merge logic, adds/removes no guard, and doesn't affect per-pass image duplication (a distinct defect: cross-pass image XObjects aren't hash-deduped against the input PDF's existing objects — related but different from the within-pass RGB dedupe in #3). Refuses to fold Pohl's guard into the recommendation: "it's a correctness fix, mine is a size fix, and conflating them would overstate what `compress_content_streams()` does."

**5. Nyquist F9 — agreed, not re-argued.**

FINAL RANKED LIST

| # | Finding | File | Base PDF | Revision PDF | Pixel-identity | Status |
|---|---|---|---|---|---|---|
| 1 | Content streams no `/Filter` | `stamp-cyberalchemy.py:184` | **287,838 B (56.0%)** | **232,241 B (52.3%)** | Holds — token-level lossless, no rasterizer needed | Admissible |
| 2 | ASCII85 on all 6 image XObjects | `stamp-cyberalchemy.py:96` | 8,517 B | 8,517 B | Holds — decoded pixels unchanged | Admissible |
| 3 | Duplicate RGB plane (obj 61=63) | `stamp-cyberalchemy.py:55-61` | 7,322 B | 7,322 B | Holds — streams proven byte-identical | Admissible (= Nyquist F9) |
| — | Combined #2+#3 (not additive) | — | ~14,373 B | ~14,373 B | — | Admissible |
| 4 | Corner-gradient CSS patterns | `build-short-polished.ps1:63-88` | ~500-2,000 B, already deduped | same CSS | N/A | Survived — negligible |
| 5 | Font subset overlap | embedded subsets | none | none | N/A | Survived |
| 6 | Dead CSS | `build-short-polished.ps1` | none | none | N/A | Survived |
| 7 | SVG raster → vector | `stamp-cyberalchemy.py:16` | ~42,528 B theoretical | same order | **Does not hold** | Inadmissible, flagged only |

---

## Nyquist, Harry — lens: FIDELITY AND REGRESSION

### INITIAL position (round 1)

**F1 — CRITICAL — `variants/INDEX.md:50` asserts an equality that is false against every candidate referent.**
> "All three PDFs passed the final organic-placement verification: four A4 pages, **extracted text identical to the source revision**, word geometry matching within 0.0001 pt"

Measured (pypdf extract_text, whitespace-normalized, SHA-1 prefix / char count):

| artifact | chars | sha1 |
|---|---:|---|
| base pdf | 6249 | `c0e4b7c099de` |
| revision pdf | 6404 | `3283146be4f0` |
| variants 01/02/03 | 6356 | `d89402c90907` (all three equal) |

Three distinct texts. Variants agree with each other and with neither base nor revision. First divergence at normalized offset 138: variants carry "…This makes focused work possible, but it changes what is visible…" which the base lacks. The referent (`INDEX.md:9` → "Current spacious revision") did not exist yet: variant PDFs carry `/CreationDate D:20260729003218`, the revision `D:20260729052027` — variants verified against a source produced 4h48m later.
Fix: retract the equality claim in INDEX.md and each rationale.txt, or re-derive variants from the current revision and re-run the comparison.

**F2 — CRITICAL — the frozen baseline's typography exists only in the uncommitted working tree and only on this machine.**
`build-short-polished.ps1:10-13`: `src: url("file:///C:/Windows/Fonts/pala.ttf") format("truetype");`
`git show HEAD:…-short-polished-diagrams.html | grep -c @font-face` → **0**. Committed base PDF is 162,219 bytes; working-tree one is 514,178. The entire Palatino/Constantia baseline — plus stamper, SVG, revision, all variants — is untracked or modified-uncommitted. No version-control recovery path for the frozen appearance; font resolution depends on absolute `C:/Windows/Fonts` paths whose glyph versions vary by Windows build.
Fix: commit the current five PDFs plus their HTML as the baseline before any optimization is discussed, and record exact `pala.ttf`/`constan.ttf` hashes alongside.

**F3 — MAJOR — the base PDF's text layer differs in characters, not merely glyph shapes.**
Page 1, base: "…an idea about something that could be **diﬀerent**." (U+FB00 LATIN SMALL LIGATURE FF). Revision and all variants: "…something that could be **different**."
Palatino/Constantia trigger the ff ligature; Georgia does not. Consequences: the base PDF is not searchable for "different"; and any fidelity test defined as extracted-text equality is structurally incapable of passing across this corpus, so it must not be the acceptance gate.
Fix: define the fidelity test on rasterized pages, not the text layer; note the ligature as an intentional baseline property.

**F4 — MAJOR — `review/review.md` predates the artifact it reviews.**
> "Lens coverage: every attacker read the complete bound HTML and semantic reference and **inspected all four frozen page renders**." (`review/review.md:47-48`)
> "## Artifact - `work-context-system-view-short-polished-diagrams-revision.pdf` and `.html`" (`:54`)

`review.md` mtime 2026-07-29 02:09; `-revision.pdf`/`.html` mtime 02:20 — the review is 11 minutes older than its stated artifact. The only `page-0*.png` sets are dated 2026-07-28 04:11–04:30, before the current base (00:40) and revision (02:20). No render in the folder depicts either artifact under review.
Fix: re-render the current revision to one dated `rendered/` set and re-anchor, or downgrade the verdict to "reviewed against a superseded render".

**F5 — MAJOR — no pinned render command for the two headline PDFs; the three that are pinned disagree.**
`variants/01/rationale.txt:34` and `03/rationale.txt:26`: `chrome.exe --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=…`
`variants/02/rationale.txt:35`: `chrome.exe --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=…`
Two headless modes across artifacts INDEX.md:3 claims "share the same … typography, margins, palette". `build-short-polished.ps1` emits HTML only — no Chrome or stamper invocation at all, so base and revision have no recorded generation command. Producer `Skia/PDF m150`, no version pin; Chrome auto-updates.
Fix: append the exact two-command recipe plus the Chrome build string; normalize all five to one headless mode.

**F6 — MAJOR — `scale=4.0` is one sampling choice serving two draws 21.5x apart; the watermark is under-sampled for print.**
`stamp-cyberalchemy.py:16,19`. SVG carries only `viewBox="0 0 120 120"`, so raster is 480x480 (confirmed in all five PDFs: `480 480 /DeviceRGB 8`).
- Footer, `mark_size = 13.0` (`:134`): 480px / 13pt = **2658 ppi** — 4.4x oversampled even at 600 dpi.
- Watermark, `watermark_size = 280.0` (`:124`): 480px / 280pt = **123 ppi** — below the 300 ppi print floor; its circle stroke and triangle vertices are visibly resampled at print resolution.
Invisible only because `opacity: float = 0.022` (`:55`) caps alpha at `round(255*0.022)` = 6/255. So yes: a sampling choice with a real consequence, masked by a second choice.
Fix: render the mark twice (scale 4.0 footer, ≥12 watermark) — but this changes antialiased alpha edges, so it is not lossless (see F9).

**F7 — MAJOR — the SVG's palette is dead code; colour truth is duplicated in Python.**
`cyberalchemy-mark.svg:14-16` declares `stop-color="#e60023"` / `#cc0000` / `#ea580c`. `stamp-cyberalchemy.py:21-27,49` keeps only `raster.getchannel("A")` and rebuilds every RGB value from `stops = ((0.0,(0xE6,0x00,0x23)), (0.62,(0xCC,0x00,0x00)), (1.0,(0xEA,0x58,0x0C)))`, then `gradient.putalpha(alpha)`. Editing the SVG's colours changes nothing in any PDF; editing the Python tuple changes all of them.
Fix: read stops from the SVG, or comment at `:23` that SVG stops are decorative and the Python tuple authoritative.

**F8 — MAJOR — stale duplicate render sets that would diverge further under any edit.**
MD5-identical across supposedly distinct generations: `short-polished-rendered-v2/page-01.png` = `v3/page-01.png` (`078d4e8c…`), `v2/page-02.png` = `v3/page-02.png` (`220080e7…`), `v2/page-04.png` = `v3/page-04.png` (`bcc577f6…`). v3 is a partial overwrite of v2, not an independent render; v4 absent entirely (folders `-rendered`, `-v2`, `-v3`, `-v5`). Page counts 4/6/6/4 don't match the current 4-page PDFs. `variants/variants-contact-sheet.png` (21:33) predates every current PDF.
Fix: delete the stale sets and regenerate one render set per current PDF with the PDF's SHA-256 beside it.

**F9 — MAJOR — taxonomy: only two of the proposed optimizations are provably lossless.**
> `/FormXob.82946bb3195a7ea43aafea5c780cfa6f 480 480 … raw 7322 sha1 390b23ecaadd`
> `/FormXob.dc6dbe5299f0c39f25aa4270d0cf430d 480 480 … raw 7322 sha1 390b23ecaadd`

Provably lossless (decoded sample values bit-identical, no rendering involved): (1) dedupe the two mark images — RGB streams byte-identical, only SMasks differ (8611 vs 14480 bytes), ~7.3 KB; (2) drop `/ASCII85Decode` — every image is `['/ASCII85Decode','/FlateDecode']`, ASCII85 costs ~25% for zero information; (3) Flate re-encoding at higher effort — same inflated bytes by definition.
Merely probably-invisible (changes decoded samples; provable only against a pinned rasterizer at stated DPI and tolerance): (4) re-rasterizing the mark at a different scale; (5) vectorizing the SVG; (6) font re-subsetting — Chrome already subsets, re-subsetting risks dropping U+FB00; (7) downsampling the footer mark to 108px.
Fix: permit classes 1–3 unconditionally; require F10's procedure for 4–7.

**F10 — CRITICAL — the verification procedure that must exist before any byte-reduction change is accepted.**
No such procedure exists today. Answer to "is there a reproducible way to prove pixel-identity": **no for HTML→PDF, yes for PDF→PDF.** Skia m150 unpinned and self-updating; `/CreationDate` and `/ModDate` are wall-clock, so no two runs are byte-equal even from identical input. Therefore the five PDFs — not the HTML — are the baseline, and every optimization must be a PDF→PDF transform. The gate:
1. Freeze: commit all five PDFs; record SHA-256 of each, and of `pala.ttf`, `palab.ttf`, `constan.ttf`, `constanb.ttf`, `cyberalchemy-mark.svg`, `stamp-cyberalchemy.py`.
2. Pin one rasterizer with version (e.g. PyMuPDF build string) and one DPI ≥ 600 — the only fixed point available, since MuPDF renders deterministically for a given build.
3. Acceptance: rasterize before/after at 600 dpi; require zero differing pixels for classes 1–3 (a lossless transform must produce a bit-identical raster; if it does not, it was not lossless). For 4–7 require a stated per-channel tolerance and max-differing-pixel count agreed before the change, plus a side-by-side of the mark region at 4x and of the four page corners.
4. Record `/Producer`, `/Creator`, page count, MediaBox, per-page font BaseFont list, per-page XObject `(width, height, filter)` before and after; any font-list change is an automatic reject.
5. Explicitly out of scope as acceptance signals: extracted-text equality (F3), file size, and re-rendering from HTML.

**F11 — MINOR — `render_mark` has no assertion on the raster it produced.**
`stamp-cyberalchemy.py:18-19` opens a viewBox-only SVG with no width/height and multiplies whatever PyMuPDF infers by 4.0. A PyMuPDF upgrade changing SVG default sizing silently changes the mark's resolution with no error.
Fix: `assert pixmap.width == pixmap.height == round(120 * scale)` after `:19`.

**F12 — MINOR — the vignette is a 72 ppi raster on a non-integer scale.**
`stamp-cyberalchemy.py:65-66` `pixel_width = round(width)` → 595 px across a 594.95996 pt page (`:115-122`), i.e. 72.005 ppi with a 1.000067 resample. Fade limit is `72.0` px (`:68`), so the smoothstep ramp has only 72 steps of ~3.5 alpha levels — the one place banding could become visible on a high-quality press.
Fix: generate the vignette at 4x and draw at page size, or state 72 ppi as a deliberate frozen property.

**F13 — MINOR — CRLF exposure on commit.**
`core.autocrlf=true` and no `.gitattributes` in the repo root. When the untracked HTML and PDFs are committed (F2), only explicit `*.pdf binary` / `*.png binary` rules guarantee the PDFs survive checkout byte-identical to what was hashed.
Fix: add `.gitattributes` with `*.pdf binary`, `*.png binary`, `*.html -text` before committing the baseline.

### FINAL position (round 2)

**Pre-emptive self-correction.** F9's sizing was scoped to page-level `/Contents` and read 69,025 uncompressed bytes. A full stream sweep of the base PDF gives **339,970 uncompressed of 486,344 total stream bytes** (`('None','None') 338,999` + `/Pattern 517` + `/Form None 454`), file 514,178. "Rissanen's 287,838-byte saving is consistent with that; my number was wrong, his is right. Conceded without qualification."

**1. F2 — NARROWED, not withdrawn. "Ashby is half right and his conclusion is wrong."**
Conceded: revision and all three variants need only Georgia/Arial + Skia m150. The `C:/Windows/Fonts` limb applies only to the base HTML, its PDF, and `build-short-polished.ps1`.
Not conceded, three ways:
- *"Superseded" is an assumption, not a fact in the corpus.* Nothing marks the base PDF as dead. `variants/INDEX.md:9` calls the revision "Current spacious revision" — yet all three variants carry the **old** title `<title>A High-Level View of Work Context Infrastructure</title>` and text matching neither. The corpus ships two live typographies and three artifacts derived from a third state. Which PDF is the baseline is an **owner decision that has not been made**, and it is the blocking question, not a settled premise.
- *Ashby's fix does not do what he claims.* Vendoring four TTFs changes `src:` URLs in the HTML, which requires a re-render. Re-rendering is class 4–7, not lossless: new `/CreationDate`, new subset tags, new glyph positioning. Vendoring can *reproduce* the appearance; it cannot "keep it byte-frozen". Byte-freezing is achieved by committing the PDF — exactly the thing not yet done.
- *The Georgia path is more machine-dependent, not less.* The revision has zero @font-face, so `font-family: Georgia, "Times New Roman", serif` resolves from the OS silently. The base at least declares its dependency. An undeclared dependency is worse for reproducibility than a declared absolute path.
F2 limb two — committed base HTML has 0 @font-face, committed PDF 162,219 vs 514,178 in tree, everything else untracked — **stands for all five PDFs regardless of which is the baseline**. Severity stays CRITICAL.

**2. Flate — ADMISSIBLE TODAY. One answer.**
F10's wording "any byte-reduction change" was over-broad; narrowed explicitly to **any change that alters decoded sample values, glyph outlines, or the text layer**. The Flate fix alters none: it changes only the `/Filter` on streams whose inflated bytes are unchanged by construction. Its acceptance test is self-executing and takes one command — decode every content stream before and after, assert byte-equality — and is strictly *stronger* than a rasterized comparison. Gating it behind a procedure built for unprovable changes would be a category error.
Ship it, with two fidelity conditions Rissanen did not state: (a) do **not** bundle it with the ASCII85 removal — the 42,528 image bytes are a separate change with a separate proof; (b) `/Pattern` (517 B) and `/Form None` (454 B) are also uncompressed and must be included in the round-trip assertion, not just `/Contents`.

**3. Helvetica-Bold — CONCEDED. "the strongest hit taken and it breaks my framing."**
Verified in all five PDFs: `/F1 /Helvetica /Type1 FontDescriptor False /WinAnsiEncoding`, `/F2 /Helvetica-Bold` likewise. The signature "Victor Boscaro" and the footer are drawn in a non-embedded base-14 font. Worse, `stamp-cyberalchemy.py:138-141` computes its x-position from `stringWidth(name, "Helvetica-Bold", font_size)` — AFM metrics the substitute may not match (Arial and Nimbus Sans do; arbitrary fallbacks do not).
Does F10's gate detect it? **No, and that is a defect in the gate.** Step 3 rasterizes with one pinned rasterizer, so before and after render identically and report zero diff — the gate is blind to cross-*viewer* variance because it holds the viewer fixed. Step 4 records BaseFont names but does not check embedding.
Amends F10 with **step 6: assert every `/Font` in the output has a `/FontDescriptor`, or record an explicit base-14 exemption list.** Restates the framing precisely: **the five PDFs are the fixed point for everything except the base-14 text, which is a fixed point only relative to a named viewer.**
New finding, **MAJOR**: the frozen appearance is not fully frozen; embedding Helvetica-Bold (or switching the signature to an already-embedded face) is the only close, and that change is class 4–7, so it goes behind F10.

**4. Agreement noted.** F1 = Ashby F3; F10's PDF→PDF conclusion = Ashby F11. One refinement his `add_metadata` point earns: because `stamp-cyberalchemy.py:178-181` propagates `/CreationDate` forward, the timestamp in every stamped PDF dates the **Chrome render**, not the stamp. That is provenance-positive and is what established the F1 chronology (variants 00:32 UTC ≺ base 03:40 ≺ revision 05:20). Keep the propagation.

**5. Ordering — CONCEDED. Commit precedes F10.**
"You cannot freeze a baseline you cannot restore, and you cannot define the acceptance target before naming which artifact is the target."
0. Commit everything untracked (5 PDFs, 5 HTMLs, stamper, SVG, build script) with `.gitattributes` `*.pdf binary` first. CRITICAL, blocks all else.
1. Owner names the baseline — base, revision, or "both, for different purposes". Blocks F2's disposition and the fate of `build-short-polished.ps1`, the four render folders, and the three variants.
2. Flate content-stream fix — admissible now, after step 0.
3. F10 procedure written, amended with the embedding assertion.
4. Everything class 4–7, including font vendoring, watermark re-rasterization, Helvetica embedding.

FINAL DISPOSITIONS

| # | position |
|---|---|
| F1 | STANDS, CRITICAL. Same finding as Ashby F3, measured independently. |
| F2 | **NARROWED.** Font-path limb applies only to the base artifact; committed-state limb stands for all five, CRITICAL. Vendoring rebutted as a freezing mechanism. |
| F3 | STANDS, MAJOR. Text-layer equality structurally unusable as a gate. |
| F4 | STANDS, MAJOR. review.md mtime 02:09 ≺ artifact 02:20. |
| F5 | STANDS, MAJOR, refined: `/CreationDate` dates the render, so it is usable provenance; the missing *command* is the gap. |
| F6 | STANDS, MAJOR. Watermark 123 ppi, masked only by alpha 6/255. |
| F7 | STANDS, MAJOR. SVG stop-colors inert. |
| F8 | STANDS, MAJOR. v2/v3 page-01/02/04 MD5-identical. |
| F9 | **CORRECTED** (339,970 uncompressed, not 69,025) and **narrowed**: class 1–3 ungated, 4–7 gated. |
| F10 | **NARROWED** in scope, **AMENDED** with step 6, **DEMOTED** below "commit" and "name the baseline". |
| F11 | STANDS, MINOR. |
| F12 | STANDS, MINOR. |
| F13 | STANDS, **PROMOTED** to MAJOR — now a precondition of step 0. |
| new | **F14, MAJOR:** base-14 Helvetica/Helvetica-Bold unembedded in all five PDFs. Credit Ashby. |

---

## Pohl, Ira — lens: MECHANICS AND CORRECTNESS

### INITIAL position (round 1)

Returned as a summary (11 findings: 2 CRITICAL, 4 MAJOR, 5 MINOR):
- CRITICAL: `build-short-polished.ps1:866` and `:879` — two `[regex]::Replace()` calls with no match-success check, unlike every `String.Replace()` in the file which is preceded by `.Contains()`/`throw`. A pattern miss silently no-ops and the script exits 0 with a wrong document.
- CRITICAL (corpus-level): `-revision.html` and all three `variants/*/*.html` are hand-forked, not producible by this script (zero references to "revision" or "variants" in it); all 5 documents carry independent full `<style>` blocks (1408–1534 lines each) with no shared source.
- MAJOR: both truncation points (lines 1016 and 1068) hardcode the discarded tail with no check on what is being cut.
- MAJOR: `stamp-cyberalchemy.py:169` — `stamp_pdf()` has no guard against `input_path == output_path`; pypdf's lazy PdfReader plus `open(path,"wb")` truncating the same file is a known corruption pattern.
- MAJOR: the `.ps1` is UTF-8 without BOM and contains a literal `→`; under classic `powershell.exe` this decodes via the ANSI code page, silently mojibaking the CSS `content` property.
- MINOR: `Replace("</style>", ...)` replaces all occurrences; unguarded anchor IndexOf makes the intended error message dead code; hardcoded absolute `$root` and Windows-only font paths; `stamp-cyberalchemy.py` not idempotent (no marker prevents double-stamping); `$ErrorActionPreference = 'Stop'` is a false safety signal for this script's actual risk class.

### FINAL position (round 2)

**1. Ashby "dead code" — partially concedes, then pushes back.** Confirmed independently: `$output` at line 5 is the only file this script ever writes, and grep for `chrome|python|stamp|weasyprint|playwright` returns nothing. So the blast radius of :866/:879 is narrower: it can only corrupt the one file the script owns, never the four hand-forked siblings. **Narrows :866 CRITICAL → MAJOR** (:879 stays MAJOR). But "dead relative to shipped output" overstates it: this is the only regeneration path for the base document, and the four forks were manually built from an earlier run of it (rationale.txt: "same four-page prose... as the frozen current revision"). "The moment anyone re-syncs — the exact maintenance motion this whole file exists for — the unguarded regex fires. A script that is the sole writer of the seed document isn't dead; it's a single point of failure with no seatbelt."

**2. Rissanen `compress_content_streams` — concedes the finding, reclassifies the lens.** A missing 56%-savings call is real, missed because the brief was correctness ("wrong document, exit 0"), not efficiency. Bloat isn't wrong output — the PDF still renders correctly — so under MECHANICS specifically it is **MINOR**, not "the biggest win". It does interact with the input==output finding: the natural way someone fixes the bloat is `writer.compress_content_streams()` right before `writer.write(output)` — and if that same refactor collapses the two-path call into an in-place stamp to save a step, the two defects compound. Worth a one-line caution, not a new severity.

**3. Nyquist F7 (mark colour duplicated) — CONCEDED FULLY, "exactly my lens and I missed it."** Verified: SVG stops `#e60023`/`#cc0000`(62%)/`#ea580c` vs the Python tuple `(0xE6,0x00,0x23)`/`(0xCC,0x00,0x00)` at 0.62/`(0xEA,0x58,0x0C)` — currently byte-identical, wired by hand with zero connecting mechanism. Same class as the five-`<style>`-blocks defect (independent hand-kept-in-sync duplicates, no error on drift), one tier down because it hasn't drifted yet and the blast radius is one small mark. Added as #13, MAJOR.

**4. Nyquist F11 (implicit SVG resolution) — CONFIRMED.** `cyberalchemy-mark.svg` has `viewBox="0 0 120 120"` and no `width=`/`height=` (verified by grep). Same silent-failure class as the .ps1 findings. Added as #14, MINOR.

**5. UTF-8/BOM — NARROWING REQUIRED, claim vs proof.** Exact location: `build-short-polished.ps1` line 568, column 13, the `→` (U+2192) inside `content: "→";`. Checked the shipped output directly: the HTML contains `content: "→";` — the correct glyph, not mojibake. So today's artifact is clean, proving the build did **not** hit the ANSI-codepage decode path (almost certainly `pwsh.exe`, not classic `powershell.exe`). "My original phrasing ('silently mis-decodes... into mojibake') overclaimed present-tense fact; the proof only supports a conditional/latent claim." **Downgraded MAJOR → MINOR**, reworded to "would," not "does."

FINAL FINDINGS

1. `build-short-polished.ps1:866-869` — unguarded `[regex]::Replace($html, $readingMapPattern, @'...'@)`, no `.Match().Success` check unlike every `String.Replace()` above it which is preceded by `.Contains()`+`throw`. Miss returns `$html` unchanged, exits 0. **MAJOR** (narrowed from CRITICAL per Ashby). Fix: `if (-not [regex]::IsMatch($html,$readingMapPattern)) { throw "..." }`.
2. `build-short-polished.ps1:879-880` — same defect, second instance: `[regex]::Replace($html, $fivePathsEndPattern, ('$1' + $inspectionClose))`. **MAJOR.** Same guard.
3. `build-short-polished.ps1:1016` / `:1068` — hardcoded truncation tail: `$html.Substring(0, $section4) + $part4 + "</main></body></html>`r`n"`, discards everything past the cut with no check. **MAJOR.** Fix: assert the discarded tail matches the expected literal first.
4. `build-short-polished.ps1:732` — `Replace("</style>", $extraCss + "`r`n</style>")` replaces all occurrences; upstream has exactly one today (verified), but SVG legally embeds its own `<style>`. **MINOR.** Fix: assert single occurrence, or target the last `</style>` before `</head>`.
5. `build-short-polished.ps1:856` — anchor IndexOf unguarded, custom error unreachable: if the inner search returns -1 the outer call throws `ArgumentOutOfRangeException` before the intended `throw "Section 3 framing table not found."`. **MINOR.** Fix: `.Contains()` check first.
6. `build-short-polished.ps1:568` — BOM-less UTF-8 + literal `→` (U+2192, col 13, confirmed by direct decode; file has no BOM, confirmed). Shipped HTML shows the correct glyph today; latent risk contingent on which PowerShell binary runs it. **MINOR** (downgraded). Fix: UTF-8 BOM, or escape the arrow.
7. `build-short-polished.ps1:3` — `$root = "C:\Users\victo\cyberalchemy-orchestrator"` plus `url("file:///C:/Windows/Fonts/pala.ttf")` at lines 13,20,27,34,41,48. **MINOR.** Fix: derive from `$PSScriptRoot`; parameterize font paths.
8. **Corpus-level — 4 of 5 shipped documents are hand-forked, not regenerable.** Script writes only `$output` (line 5); grep for `variants` returns zero matches. All 5 HTML files carry one independent full `<style>` block (1408–1534 lines), confirmed by direct count on each. **CRITICAL — "this is the actual structural defect; #1–2 are symptoms of trusting this script as if it were that source of truth."** Fix: no code fix inside this script closes it; needs a real shared stylesheet/generator with variant deltas.
9. `stamp-cyberalchemy.py:169-185` — no guard on `input_path == output_path`: `reader = PdfReader(str(input_path))` … `with output_path.open("wb") as output: writer.write(output)`. **MAJOR** (verdict: plausible, not directly reproduced). Fix: `if input_path.resolve() == output_path.resolve(): raise ValueError(...)`.
10. `stamp-cyberalchemy.py:96-162` — `create_overlay()` unconditionally draws vignette + watermark + mark/name on every page regardless of prior stamping. **MINOR.** Fix: check `reader.metadata` for a stamp marker.
11. `build-short-polished.ps1:1` — `$ErrorActionPreference = "Stop"` has no effect on .NET method calls succeeding-but-wrong, the file's real risk class. **MINOR.**
12. `stamp-cyberalchemy.py:184-185` — missing content-stream compression (credit Rissanen); ~56% output bloat. **MINOR** (efficiency, not correctness). Fix: `writer.compress_content_streams(); writer.write(output)`; verify it doesn't land before #9's guard, since a compress-motivated refactor is a plausible trigger for collapsing input/output into one path.
13. `stamp-cyberalchemy.py:23-27` vs `cyberalchemy-mark.svg` — duplicated colour source (credit Nyquist F7). **MAJOR** — same class as #8; values currently match so nothing is broken yet. Fix: parse `stop-color`/`offset` from the SVG at render time.
14. `stamp-cyberalchemy.py:16-19` — implicit SVG resolution (credit Nyquist F11). **MINOR.** Fix: add `width`/`height` to the SVG, or assert `pixmap.width == 120*scale`.

**Final position: harden or replace?** "Both, in sequence, not either/or." Hardening (#1–#7, #11) is cheap, mechanical, removes the exit-0-but-wrong mode for the one file the script still owns — do it regardless, because it is the only current regeneration path and someone will run it again. But hardening a script that produces 1 of 5 shipped documents does not fix #8: "there is no source of truth this script could be hardened *into* being, because 80% of the output family already bypassed it." The correct fix is structural — extract the shared CSS/prose skeleton into one generator with variant deltas (a real templating layer, not a PowerShell heredoc), so all 5 documents derive from one input and #8, #13 stop being possible by construction. "Until that exists, harden the script as a stopgap; don't mistake the stopgap for the fix."

---

## Ashby, W. Ross — lens: OPERABILITY AND PORTABILITY

### INITIAL position (round 1)

**Verdict.** A second operator on a second machine cannot reproduce these PDFs. What breaks first is not fonts or Chrome — it is that the baseline itself is not in the repository. `git status` shows the frozen artifacts are untracked. A fresh clone yields zero of the five PDFs, no stamper, no mark, no variants.

**F1 — The frozen baseline is untracked. CRITICAL.**
```
?? .../short-version/work-context-system-view-short-polished-diagrams-revision.html
?? .../short-version/work-context-system-view-short-polished-diagrams-revision.pdf
?? .../short-version/stamp-cyberalchemy.py
?? .../short-version/cyberalchemy-mark.svg
?? .../short-version/variants/
```
Only the older `...-diagrams.html/.pdf` and `build-short-polished.ps1` are tracked (both ` M` dirty). Fix: commit the baseline set before any byte-reduction work begins.

**F2 — `build-short-polished.ps1` renders no PDF and does not produce the current baseline HTML. CRITICAL.**
```powershell
$html = $html.Substring(0, $section3Start) + $shortTail + "</main></body></html>`r`n"
[IO.File]::WriteAllText($output, $html, [Text.UTF8Encoding]::new($false))
Write-Output $output
```
`$output` is `...short-polished-diagrams.html` — not `...-revision.html`, which is the frozen artifact. Grep confirms no `chrome`, `python`, or `stamp` token in its 1071 lines. Fix: add `build.ps1` that runs generate → render → stamp → verify and emits the `-revision` artifact.

**F3 — Variant QA claims are already false against today's baseline. CRITICAL.**
`variants/01/rationale.txt`: "Extracted text is exactly equal to the frozen source PDF on every page." `variants/INDEX.md`: "extracted text identical to the source revision". Measured: baseline page 1 begins `From Intention to\nRecoverable Continuity`; variant 01 page 1 begins `A High-Level View of Work\nContext Infrastructure`. `<title>` differs; the two HTMLs differ on 508 lines; baseline PDF rendered `D:20260729052027` vs variant `D:20260729003218`. "The baseline moved after verification and nothing detected it — exactly the failure mode an unreproducible build guarantees." Fix: make verification a committed script run in CI/pre-commit, not prose written once.

**F4 — `$root` hardcoded to one user's home. HIGH.** `$root = "C:\Users\victo\cyberalchemy-orchestrator"`. Violates the repo's standing portability principle. Fix: `$root = if ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR } else { (Resolve-Path "$PSScriptRoot/../../../../../..").Path }`.

**F5 — The render step exists only as prose, and the three copies disagree. HIGH.**
`01`: `chrome.exe --headless --disable-gpu ... --print-to-pdf='C:\Users\victo\...\01-revision-ledger.raw.pdf'`
`02`: `chrome.exe --headless=new ... '...\02-authority-containment-raw.pdf'`
`03`: `--headless ... '...-unstamped.pdf'`
Three flag/naming/path conventions for one operation; `--headless` and `--headless=new` are different renderers in some Chrome builds. Fix: one parameterized `render.ps1` taking `<in.html> <out.pdf>`; delete the prose commands.

**F6 — Chrome/Skia is an unpinned determinism dependency. HIGH.** All five PDFs: `/Producer: Skia/PDF m150`, `/Creator: ...HeadlessChrome/150.0.0.0...`. Version recorded only as an accidental byproduct in output metadata; nothing asserts it at build time. Fix: assert `Producer == Skia/PDF m150` in the verify step; record the pinned Chrome build in a `RENDER-ENV.md`.

**F7 — Font resolution is machine-local and has already silently drifted. HIGH.** `src: url("file:///C:/Windows/Fonts/pala.ttf") format("truetype");`. The tracked `...-diagrams.pdf` embeds `PalatinoLinotype-Bold`, `Constantia`. The untracked frozen baseline `...-revision.html` contains zero @font-face; its stack is `font-family: Georgia, "Times New Roman", serif` and the PDF embeds `Georgia`, `Georgia-Bold`, `Georgia-Italic`, `ArialMT`. On a Linux operator fontconfig substitutes DejaVu/Liberation with different metrics → reflow → the 4-page pagination and every mm-pinned ornament footprint become unverifiable. Fix: vendor licensed WOFF2 into a repo-local `fonts/` and reference path-relative.

**F8 — Stamper has four undeclared dependencies and no manifest. HIGH.** `import fitz`, `from PIL import Image`, `from pypdf import PdfReader, PdfWriter`, `from reportlab.lib.colors import HexColor`. No `requirements.txt`, `pyproject.toml`, or lockfile anywhere in the repo (checked repo-wide). `zip(..., strict=True)` additionally requires Python ≥ 3.10, undeclared. Fix: pinned `requirements.txt` beside the stamper; state minimum Python.

**F9 — Every intermediate and the only QA tool live in gitignored `tmp/`. HIGH.** `.gitignore:33` — `/tmp/`, commented "Regenerable from the tracked sources." `variants/03/rationale.txt` — "Validation command: `python 'C:\Users\victo\...\tmp\pdfs\work-context-variants\03-projection-family\validate_projection_family.py'`". That file exists on this disk and nowhere else. The gitignore's regenerability claim is unbacked: the regeneration procedure is itself untracked prose. Fix: move validators into the tracked corpus; keep only outputs in `tmp/`.

**F10 — The visual baseline evidence is also gitignored. MEDIUM.** `.gitignore:37` excludes all four `short-polished-rendered*/` sets and `variants/variants-contact-sheet.png` — the only rendered record of "the current appearance". Fix: track contact sheets or a per-page perceptual-hash manifest.

**F11 — "Pixel-identical" is undefinable as stated; PDFs are not byte-stable even locally. MEDIUM-HIGH.** `/CreationDate: D:20260729052027+00'00'`, `/ModDate` identical; the stamper propagates them: `writer.add_metadata({key: value for key, value in reader.metadata.items() if value is not None})`. Two runs one second apart differ in bytes. Fix: commit `verify.py` (fitz render at fixed DPI, per-page SHA-256 + bounded-diff report) and override dates from a fixed epoch.

**F12 — Signature text uses a non-embedded base-14 font. MEDIUM.** `overlay.setFont("Helvetica-Bold", font_size)`; all five PDFs carry `('/Helvetica-Bold', '/Type1')` unembedded. The author signature and footer render with a viewer/OS-supplied face — appearance is not frozen even for a reader, independent of the build. Fix: embed via `pdfmetrics.registerFont(TTFont(...))` from a repo-local `fonts/`.

**F13 — Generator keys on prose headings of the long essay. MEDIUM.** `$section3Start = $html.IndexOf("<h2>3. The problem the system must solve</h2>", ...)`; `$diagramMatch = [regex]::Match($part4, '(?s)<figure class="infra-figure".*?</figure>')`. Renaming a heading in the upstream 74 KB source silently mis-slices the short edition. The script also writes CRLF, which under `core.autocrlf=true` perturbs any content digest. Fix: anchor on stable `id=` attributes and write LF.

**F14 — Known race in the render step, unmitigated. MEDIUM.** `variants/02/rationale.txt`: "Chrome returned before its raw-PDF write completed on the first combined invocation; that initial stamp attempt failed cleanly." No wait-for-file or exit-code check exists, and the commands omit profile isolation. Compare `experiments/foodstogo-jbp-2025/render.sh`, which already solves both. Fix: reuse that script's shape.

**F15 — A near-miss skeleton exists but targets a different document. LOW.** `tools/build_system_view_pdf_versions.py`: `CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")` with an exists-check; its `SOURCE` is `docs/architecture/agent-language-system-view.md`. Closest thing to a committed renderer, same hardcoded-Chrome defect. Fix: generalize it rather than writing a third builder.

**Closing claim (round 1):** "Preserving today's bytes requires only Georgia/Arial metrics + Skia m150, not `C:\Windows\Fonts` and not `C:\Users\victo`. Vendoring the four TTFs into the repo and asserting the Skia version keeps the appearance byte-frozen while removing every machine-specific path. The absolute paths buy nothing the vendored fonts do not."

### FINAL position (round 2)

**1. Ligature challenge — "Nyquist is right on the glyph, wrong on the character; the baseline question settles it."**
Measured at char level (fitz rawdict, width of the two `ff` chars in "different"):
- base, font `Constantia`: `char widths [6.43, 0.0]` → one ligature glyph
- revision, font `Georgia`: `char widths [3.43, 3.43]` → two glyphs
But extracted text in **both** PDFs contains zero `U+FB00` (`ff-lig U+FB00 count: 0` for both; "different" extracts plain, 3x / 2x). "So this is a rendering difference invisible to text extraction — which strengthens F11's raster point rather than contradicting it."

**(a) The frozen baseline is the revision PDF.** The corpus says so itself — `variants/INDEX.md`: `## Source revision` → `- [Current spacious revision](../work-context-system-view-short-polished-diagrams-revision.pdf)`. It is also the newest render (`D:20260729052027` vs `D:20260729034040`). The Palatino/Constantia artifact is superseded; Nyquist's ligature attaches to a non-baseline file.

**(b) CONCEDES F7's fix and the closing claim with it.** Georgia and Arial are Microsoft-proprietary and bundled with Windows/Office — no more redistributable into a repo than Palatino Linotype. "My sentence 'vendoring the four TTFs keeps the appearance byte-frozen while removing every machine-specific path' is **withdrawn**. The tension the coordinator flagged is real and I understated it."
**F7 NARROWED (final):** the *build* can be made portable; the *appearance* cannot be made redistributable. Replace `file:///C:/Windows/Fonts/...` with a declared **font precondition manifest** (family, file, SHA-256) resolved from an operator-supplied path and hard-failed on mismatch. A second operator on Windows reproduces exactly; on Linux the build refuses to run rather than silently reflowing. The only route to a genuinely portable baseline is re-freezing on metric-compatible OFL faces (Gelasio for Georgia, Liberation Sans for Arial) — preserving advance widths and thus pagination, but changing glyph outlines. "That is an owner decision, not an operability fix, and it is not free."

**2. Flate — CONCEDES, narrowing F11.** Verified: `revision.pdf` has 140 streams, 44 Flate, **96 uncompressed**; variant 01 has 104 uncompressed of 156. Rissanen's saving is real and the mechanism lossless by construction.
**Answer: admissible without `verify.py`'s rasterizer — but not without *a* verifier.** The correct check is stronger and cheaper than rasterizing: decompress every stream and assert byte-equality of content streams plus isomorphism of the object graph. If that passes, pixel-identity is entailed, not sampled.
**F11 NARROWED:** raster verification required for *layout-affecting* changes (HTML, CSS, fonts, Chrome version); *representation-only* changes (stream filters, object ordering, metadata) verified by decoded-stream equality. "My original 'everything must be rasterizer-verified' was overbroad."

**3. Execution order for the full change-request set.**
1. **Hash-freeze the baseline** — SHA-256 manifest of the 5 PDFs and their HTMLs. No dependencies, seconds of work, every later claim references it.
2. **Commit the untracked artifacts (F1).** Non-negotiably first among real changes. "Rissanen's 56% edit rewrites a file git cannot diff, cannot restore, and has no recorded prior state; if the rewrite corrupts an object, the baseline is *gone from the world*. Cost of waiting: one commit."
3. **Declare the environment (F8, F6, F7-narrowed)** — `requirements.txt` with pins, Chrome/Skia m150 assertion, font manifest.
4. **Commit the verifier (F9, F11-narrowed)** — raster+text+geometry for layout changes, stream-equality for representation changes. "Verification precedes the first change or F3 recurs by construction."
5. **Commit render + build (F2, F5, F4, F14).** First runnable reproduction. **Hard gate:** rebuild must reproduce the baseline within tolerance *on this machine*. If it does not, stop — the baseline is not reproducible even at home and steps 6-7 are meaningless.
6. **Rissanen's Flate compression.** Independent of the renderer, verified per §2, revertable because of step 2.
7. **Pohl's regex hardening.**
8. **Second-machine trial**, then the owner's font decision.

*Against Rissanen-first:* the saving is real but it is an unrevertable edit to an unversioned file — "ordering it first trades a permanent risk to the only copy of the baseline against a two-commit delay."
*Against Pohl-first:* measured, `build-short-polished.ps1` writes `...short-polished-diagrams.html`, not the shipped `-revision.html`, and contains no chrome/python/stamp call. "Hardening its regex cannot affect the baseline artifact. Pohl's finding is valid and genuinely last among the real fixes; it becomes urgent only after step 5 makes the generator live again."

**4. F14 — VERIFIED, STANDS.** `experiments/foodstogo-jbp-2025/render.sh` exists (`-rwxr-xr-x 978 bytes, Jul 23 17:40`). Lines to reuse verbatim:
```bash
PROFILE="$(mktemp -d)"
"$CHROME" --headless --disable-gpu --no-sandbox \
  --user-data-dir="$PROFILE" \
  --no-pdf-header-footer \
  --print-to-pdf="$OUT_ABS" \
  "file:///$IN_ABS" 2>/dev/null
rm -rf "$PROFILE"
```
It also settles `--headless` vs `--headless=new` in favour of plain `--headless`; its `CHROME="/c/Program Files/..."` line is the one part **not** to copy. It lacks a wait-for-file check, so that must still be added.

**5. Build script — commits to a new one in `short-version/`.** Write a new `build.py` in `short-version/`, not a generalization of `tools/build_system_view_pdf_versions.py`: that builder is a Markdown→mistune→mermaid pipeline for a different source document; this corpus is hand-authored HTML, and generalizing means bending a monolith around two incompatible input shapes. Python, not PowerShell, so build and stamper share one runtime and one `requirements.txt`.
**Cost, stated plainly:** two Chrome call sites in the repo that will drift. Mitigate by factoring the invocation into `tools/render_html_pdf.py` and having `build.py` call it. This also makes the `.ps1` legacy — keep it tracked as provenance for the base artifact, but it stops being the build.

**6. Agreements noted.** F3 = Nyquist F1; F11 = Nyquist F10.

**FINAL POSITION.** Withdrawn: the closing "vendoring keeps it byte-frozen and portable" claim. Narrowed: F7 and F11. All other findings stand as filed, F1/F2/F3 CRITICAL and unmoved. "The single sentence that survives everything: **the baseline is not in the repository, so no reduction — Rissanen's included — is currently revertable.**"
