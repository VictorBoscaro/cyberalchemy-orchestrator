# Systems and Categories: Toward Domain Languages

This folder exists to refine one essay until it is ready to circulate in the ResonantOS group. The aim is not to expand its scope. It is to make the argument, sequence, language, diagrams, and page feel as exact as the underlying idea deserves.

`pdf/systems-and-categories.md` is the canonical text and lives beside `pdf/systems-and-categories.pdf`. They are one source/output pair and must never be separated. `drawings/` contains only image sources used by the essay and the visual questions still under consideration. `research/` holds only findings that can change an editorial decision. `tools/build.py` rebuilds, checks, and renders the pair in place.

## Current editorial direction

- Preserve the title and the central discovery: a domain begins to need a language when consequential distinctions must remain available beyond the situation in which they became clear.
- Keep systems thinking and category theory as lenses with different obligations, not as competing total explanations.
- Let domain languages participate across intention, orchestration, bounded work, and effect; do not confine them to local work.
- Prefer phenomenological progression: show what becomes difficult or visible before naming the concept that responds to it.
- Preserve the restrained blue, gray, and gold identity while improving type size, spacing, and diagram legibility.

## Open questions

1. Does section 0 reveal the need for a domain language quickly enough, without explaining the whole essay before it begins?
2. Does each conceptual term arrive because the preceding phenomenon demands it, or does any section still begin by listing abstractions?
3. Does the lenses figure show a genuine difference in what governs inquiry, or merely recolor the same network?
4. Can the infrastructure figure show transversal, non-uniform languages without implying a hierarchy or a single enclosing language?
5. Which relations in the diagrams are sustained, uncertain, or absent, and is that distinction visible without a legend-heavy figure?
6. Are the body size, line length, leading, contrast, and page background comfortable both on screen and in print? This still needs real evidence and reader testing.
7. Which claims would a systems thinker, category theorist, domain practitioner, or critical reader find stronger than the essay's evidence permits?

## Next pass

Read the PDF in sequence and record only consequential friction: where attention stalls, a term arrives too early, a diagram overclaims, or a page becomes visually tiring. Resolve those findings in `pdf/systems-and-categories.md`, the drawing sources, or the style controls near the top of `tools/build.py`; rebuild with:

```powershell
python essays/systems-and-categories/tools/build.py all
```

The PDF is an output, not the editing surface. Direct PDF patching is reserved for recovery when no source exists.
