# Editor handoff

## Changes

- Added a pre-edit diagnosis for material restructuring: recover the attempted reader movement,
  find its first structural break, and revise from there.
- Tightened the opening contract with a problem-specific starting condition and a noun-substitution
  rejection test.
- Added an invisible transition test based on the new understanding or question earned by each
  passage.
- Added conditional autonomy for documents in a sequence: reconstruct only the minimum causal
  premise, avoid redundant recap, advance a new question, and test both reading contexts.
- Tightened closure so the ending must make the opening situation newly intelligible or judgeable,
  not merely recap the route.
- Compressed the overlapping collection examples while preserving the separate failures of process
  dependency and object binding.

## Findings addressed

- **F1:** implemented discriminating opening, transition, and ending tests.
- **F2:** implemented sequential autonomy as a conditional case without banning necessary references
  to a predecessor.
- **F3:** implemented structural diagnosis before material restructuring.
- **F5:** used as a size constraint by consolidating overlapping examples; preserved the terminology
  and presentation-structure examples.
- **F4, F6, F7, F8:** made no independent behavioral, metadata, routing, evidence-location, or
  forward-test change.

## Validation

- `quick_validate.py .codex/skills/write-need-driven-documents`: `Skill is valid!`
- Mirror comparison: byte-identical SHA-256
  `6DAFA82F20754C7CFC3460E898BFEFAAD20EBB80A0948E62D58AB421D4E982C0`.
- `git diff --check` on both `SKILL.md` copies: passed.

## Remaining risks

- Contract review does not establish behavioral transfer. F8 still requires blind executions before
  claiming that the revision reliably improves essay output.
- Evidence placement remains the human-gated policy tension recorded in F7.
- The compact tests intentionally leave rhetorical form open; zig-zag review should check whether
  they discriminate weak openings and transitions without inducing mechanical prose.
