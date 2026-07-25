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
   (`pair_B(u, v) ≤ NEARDUP_TAU` **and** `pair_B(u, v) ≤ NEARDUP_K · A(u)`) is
   `protected` and lifted out of the cut ranking. The second clause is a
   scale-invariant companion, calibrated 2026-07-23 to `NEARDUP_K = 0.65`
   (was disabled at `1.0`) — see [CALIBRATION.md](CALIBRATION.md) and
   discovery OQ-AS6 for the labelled set, the ratio finding, and the honest
   gzip ceiling it did not close.
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
| `--neardup-k` | 0.65 | P-GUARD scale-invariant companion: also require `pair_B ≤ k·A(u)` (calibrated 2026-07-23; `1.0` disables it) |
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

## P-GUARD calibration (OQ-AS6) and its honest ceiling

At the pinned absolute `NEARDUP_TAU = 0.25` alone, `protected` over-triggers:
`pair_B(u, v)` is upper-bounded by `A(u)`, so a dense, low-`A` unit whose own
rate happens to sit near `NEARDUP_TAU` (e.g. `repository-harness`, `A≈0.25`)
registers as a near-duplicate of nearly the whole corpus (68/68 on this
run). The `--neardup-k` companion (`pair_B ≤ k·A(u)`) is now enabled by
default at `k = 0.65`, calibrated against a small in-repo labelled set (see
[CALIBRATION.md](CALIBRATION.md)). This drops `protected` from 12 to 5 units
on the current corpus and removes the flagship artifact
(`repository-harness`) along with five others. **Ceiling, stated honestly:**
no single `k` cleanly separates every genuine cross-skill repetition from
every artifact — the ratio distributions overlap — so this default is a
defensible reduction, not a solved calibration. It still loses one
paraphrase-only genuine case (`whisper`) that gzip cannot reliably
distinguish from noise, and it cannot recover `ontology-view` (its `pair_B`
to its own siblings exceeds `NEARDUP_TAU` outright, a `pair_B` asymmetry
independent of `k`). Separating template-conformance boilerplate (shared
"Composed Arcanum spell" generator scaffolding) from deliberate rule
restatement is out of gzip's reach; both currently look identical to a
byte-length compressor. That distinction needs the S2 LM kernel.

## Scope

S0 measures redundancy, not cut-safety. The `RankedRedundancyMap` is a
review shortlist for a human, never an autocut. Section-tier scoring, the
LM kernel, and the behavioral-equivalence falsifier are later rungs (S1–S5)
— not built here. See discovery §4–§6.
