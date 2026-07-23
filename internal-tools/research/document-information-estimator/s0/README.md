# Assay S0 — gzip-only, confound-guarded redundancy audit

First functional build of Assay. Built exactly to
[`../discovery/assay-discovery.md`](../discovery/assay-discovery.md) §3
(S0). Stdlib-only Python 3 (`zlib`, `pathlib`, `csv`, `json`, `re`,
`argparse`) — no third-party deps, no LLM, no network. Read-only: it never
modifies a skill or README file.

## What it does

1. Segments each `.claude/skills/*/SKILL.md` into a `SkillUnit` (body = text
   after the closing frontmatter `---`, stripped).
2. Scores each unit's body against a leave-one-out corpus of every other
   unit's body with a fixed `zlib.compress(data, level=9)` codec, producing
   three columns per unit: `A` (raw self-compressibility), `B` (conditioned
   rate), `Δ = A − B`.
3. Applies **P-GUARD**: a unit near-duplicate of ≥ 2 distinct other units
   (`pair_B(u, v) ≤ NEARDUP_TAU`) is `protected` and lifted out of the cut
   ranking.
4. Applies **MinLengthFloor**: units under ~100 word-proxy tokens are
   reported, not ranked.
5. Emits a `RankedRedundancyMap` (CSV + JSON + human digest), ranked
   ascending by `B` (tie: ascending `Δ`).

## Run it

```sh
# Normal run: writes CSV/JSON/digest to ./out/
python assay_s0.py

# Acceptance test (the S0 -> S1 gate): body-identical SKILL<->README pairs
# must score pair_B ~= 0 and be caught by P-GUARD. Prints PASS/FAIL.
python assay_s0.py --acceptance
```

If `python` isn't on PATH, try `py -3` or `python3`. Run from anywhere —
the script auto-detects the repo root by walking up from its own location
to find `.claude/skills`; override with `--root`.

### Outputs (normal run)

Written under `./out/` next to the script:

- `assay_s0_map.csv` — `unit_path, n_bytes, A, B, Delta, merge_partner, protected_flag, verdict_hint`
- `assay_s0_map.json` — same rows plus a `manifest` block recording the tau
  values and gzip level actually used for that run (taus are calibrated
  pins, never asserted optimal — discovery §3.4/§3.5).
- `assay_s0_digest.txt` — human-readable: top-N most-redundant units, all
  `protected` units with their near-dup partners, all `below-floor` units.

### CLI knobs (all pinned defaults, all overridable)

| Flag | Default | Meaning |
|---|---|---|
| `--neardup-tau` | 0.25 | P-GUARD near-duplicate threshold on `pair_B` |
| `--cut-tau` | 0.15 | `verdict_hint = cut` threshold on `B` |
| `--merge-tau` | 0.5 | `verdict_hint = merge` threshold on `B` |
| `--tighten-a-tau` | 0.35 | `verdict_hint = tighten` threshold on `A` |
| `--tighten-delta-tau` | 0.10 | `verdict_hint = tighten` threshold on `Δ` |
| `--min-length-floor` | 100 | word-proxy tokens; below this, `below-floor` |
| `--acceptance-tau` | 0.05 | acceptance-test "`pair_B ≈ 0`" threshold |
| `--top-n` | 20 | rows shown in the digest's top-redundant list |
| `--skills-glob` | `.claude/skills/*/SKILL.md` | unit discovery glob |
| `--out-dir` | `./out` | where CSV/JSON/digest are written |
| `--root` | auto-detected | repo root the glob is resolved against |

## The acceptance gate, and one real deviation worth knowing

Discovery §3.7 states `pair_B(u, partner)` is "always inside the 32KB LZ77
window" for a body-identical `SKILL.md`↔`README.md` pair, because `pair_B`
concatenates the partner directly before `u`. That guarantee only holds
when the body itself is **≤ 32768 bytes** — DEFLATE's back-reference
window. On this corpus, `necronomicon`'s body is ~51.8 KB (the one skill
whose SKILL.md/README.md pair exceeds the window), so its `pair_B` lands
at ~0.236 instead of ~0 — the same accepted DEFLATE blind spot §3.2 pins
for the leave-one-out corpus, now visible inside a single oversized unit.

The harness therefore scopes Assertion 1/2's PASS/FAIL gate to
body-identical pairs whose body fits inside the 32KB window (12 of 13 on
this corpus) and reports the oversized pair (`necronomicon`) separately as
informational — it still happens to clear `NEARDUP_TAU` (0.25) and get
caught by P-GUARD, just not the tighter `≈0` acceptance threshold. This is
a corpus fact, not a script bug: rerun `--acceptance` after any corpus
change and check the reported window-exceeded count.

## Scope

S0 measures redundancy, not cut-safety. The `RankedRedundancyMap` is a
review shortlist for a human, never an autocut. Section-tier scoring, the
LM kernel, and the behavioral-equivalence falsifier are later rungs (S1–S5)
— not built here. See discovery §4–§6.
