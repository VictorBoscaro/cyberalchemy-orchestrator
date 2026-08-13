# Editor response: reader review

## Decisions

### R1 — ACCEPT

The existing contribution test admits changes in precision and trust as valid movement, while
“could not before” and “new understanding or question” can be read as requiring novelty. Reframing
the test around what changed preserves F1's discriminating state transition and admits earned
deepening rather than only conceptual addition.

Changed both the composition instruction and final-read test to ask what changed in what the reader
can understand or ask. Retained the requirement that this change earn what follows.

### R2 — ACCEPT

The skill's destination includes understanding, judgment, or decision, so requiring every document
in a sequence to advance a new question is narrower than the governing movement contract. F2's
necessary behavior is that local grounding support a new contribution rather than recap or
dependence.

Changed the sequence instruction to use the minimum causal premise to advance the document's own
movement. Retained the explicit prohibition on redundant recap and the tests both alone and after
the predecessor.

## Boundary

The corrections refine F1 and F2 only. They add no rhetorical form, framework, example, metadata,
routing change, evidence move, or behavioral-reliability claim. F3 and F5 remain unchanged; F4 and
F6-F8 retain their reviewed dispositions.

## Validation

- `quick_validate.py .codex/skills/write-need-driven-documents`: `Skill is valid!`
- Mirror comparison: byte-identical SHA-256
  `59B70A04856F8D2695C0980FA3270ECAD6348A661FD1B8CEABEEBD81B0ECE166`.
- `git diff --check` on both `SKILL.md` copies: passed.
