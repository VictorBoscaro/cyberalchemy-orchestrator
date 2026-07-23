#!/usr/bin/env python3
"""Assay S0 -- gzip-only, confound-guarded prolixity/redundancy audit.

Segments each ``.claude/skills/*/SKILL.md`` into a scorable ``SkillUnit``
(body = text after the closing frontmatter ``---``), scores every unit
against a leave-one-out corpus of the other units' bodies with a fixed
``zlib.compress(data, level=9)`` codec, guards deliberate repetition with
P-GUARD, applies a MinLengthFloor, and emits a ``RankedRedundancyMap`` as
CSV + JSON + a human-readable digest.

Stdlib only. Read-only over the corpus: no skill or README file is ever
modified. Reference: internal-tools/research/document-information-estimator/
discovery/assay-discovery.md (S0, sections 2, 3.1-3.7, 6).

Usage
-----
    python assay_s0.py                       # normal run, writes CSV/JSON/digest
    python assay_s0.py --acceptance          # S0->S1 acceptance gate (prints PASS/FAIL)
    python assay_s0.py --top-n 15            # digest shows top 15 most-redundant units

See README.md in this directory for the full CLI.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import zlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Pinned defaults (discovery §3.4, §3.5) -- all CLI-overridable, never hardcoded
# as ground truth; each run records the values it actually used.
# ---------------------------------------------------------------------------

DEFAULT_NEARDUP_TAU = 0.25
DEFAULT_CUT_TAU = 0.15
DEFAULT_MERGE_TAU = 0.5
DEFAULT_TIGHTEN_A_TAU = 0.35
DEFAULT_TIGHTEN_DELTA_TAU = 0.10
DEFAULT_MIN_LENGTH_FLOOR = 100  # whitespace-word-proxy tokens
DEFAULT_ACCEPTANCE_TAU = 0.05  # "pair_B approx 0" gate threshold (discovery §3.7)

DEFAULT_SKILLS_GLOB = ".claude/skills/*/SKILL.md"
GZIP_LEVEL = 9

# DEFLATE's LZ77 back-reference window (discovery §3.2). pair_B(u, v) places
# v directly before u, so v is "always inside the window" *only* when
# len(v_bytes) <= this many bytes -- otherwise the leading portion of v (and
# correspondingly the leading portion of u, since positions are offset by
# len(v)) falls outside the 32KB lookback by the time the compressor reaches
# it. This is the same accepted blind spot §3.2 pins for the leave-one-out
# corpus, applied to a single oversized body.
LZ77_WINDOW_BYTES = 32768

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?\r?\n)---\r?\n", re.DOTALL)
DESCRIPTION_RE = re.compile(r"^description:\s*(.*)\s*$", re.MULTILINE)


# ---------------------------------------------------------------------------
# Segmentation (discovery §3.1)
# ---------------------------------------------------------------------------


def split_frontmatter(text: str) -> Tuple[str, bool, str]:
    """Split YAML frontmatter from the body.

    Returns (frontmatter_raw, frontmatter_present, body). The body is
    ``.strip()``-ed. If there is no frontmatter, the whole file is the body.
    """
    m = FRONTMATTER_RE.match(text)
    if m:
        frontmatter_raw = m.group(1)
        body = text[m.end():].strip()
        return frontmatter_raw, True, body
    return "", False, text.strip()


def parse_description(frontmatter_raw: str) -> Optional[str]:
    m = DESCRIPTION_RE.search(frontmatter_raw)
    if not m:
        return None
    desc = m.group(1).strip()
    if len(desc) >= 2 and desc[0] == desc[-1] and desc[0] in ("'", '"'):
        desc = desc[1:-1]
    return desc


def word_count(body: str) -> int:
    return len(body.split())


def gzip_len(data: bytes, level: int = GZIP_LEVEL) -> int:
    """Fixed codec for every call, per discovery §3.3: zlib.compress(level=9)."""
    return len(zlib.compress(data, level))


class Unit:
    """A single scorable text unit (a SkillUnit, or a README companion at
    --acceptance time). Only ``body`` is ever scored."""

    __slots__ = (
        "path", "frontmatter_raw", "frontmatter_present", "frontmatter_bytes",
        "description", "body", "body_bytes", "n_bytes", "n_tokens",
        "gz_alone",
    )

    def __init__(self, path: str, raw_text: str):
        self.path = path
        frontmatter_raw, present, body = split_frontmatter(raw_text)
        self.frontmatter_raw = frontmatter_raw
        self.frontmatter_present = present
        self.frontmatter_bytes = len(frontmatter_raw.encode("utf-8"))
        self.description = parse_description(frontmatter_raw) if present else None
        self.body = body
        self.body_bytes = body.encode("utf-8")
        self.n_bytes = len(self.body_bytes)
        self.n_tokens = word_count(body)
        self.gz_alone: Optional[int] = None  # len(gzip(body)) -- filled lazily


def load_units(skills_glob: str, root: Path) -> List[Unit]:
    """Glob `.claude/skills/*/SKILL.md` (discover the set at run time) and
    build one Unit per file, sorted by path (discovery §3.1, §3.2)."""
    paths = sorted(root.glob(skills_glob), key=lambda p: p.as_posix())
    units = []
    for p in paths:
        text = p.read_text(encoding="utf-8")
        rel = p.relative_to(root).as_posix()
        units.append(Unit(rel, text))
    return units


# ---------------------------------------------------------------------------
# Metrics (discovery §2 ConditionedGzipRatio, §3.3)
# ---------------------------------------------------------------------------


def compute_alone_lengths(units: List[Unit]) -> None:
    for u in units:
        if u.gz_alone is None:
            u.gz_alone = gzip_len(u.body_bytes)


def compute_A_B_delta(units: List[Unit]) -> Dict[str, Dict[str, float]]:
    """Leave-one-out A/B/Delta for every unit in `units`, in the deterministic
    path-sorted order (units already sorted by caller). Returns unit_path ->
    {A, B, Delta, gz_alone, gz_corpus, gz_corpus_plus_u}."""
    compute_alone_lengths(units)
    n = len(units)
    results: Dict[str, Dict[str, float]] = {}
    for i, u in enumerate(units):
        others = [units[j].body_bytes for j in range(n) if j != i]
        c_u = b"\n\n".join(others)
        gz_c = gzip_len(c_u)
        gz_c_plus_u = gzip_len(c_u + u.body_bytes)
        nb = u.n_bytes
        if nb == 0:
            A = B = 0.0
        else:
            A = u.gz_alone / nb
            B = (gz_c_plus_u - gz_c) / nb
        results[u.path] = {
            "A": A,
            "B": B,
            "Delta": A - B,
            "gz_alone": u.gz_alone,
            "gz_corpus": gz_c,
            "gz_corpus_plus_u": gz_c_plus_u,
        }
    return results


def pair_B(u: Unit, v: Unit) -> float:
    """pair_B(u, v) = (len(gzip(v+u)) - len(gzip(v))) / len(u) -- discovery §3.4.
    v is concatenated directly before u so v is always inside the 32KB LZ77
    window (the window-safe check)."""
    if v.gz_alone is None:
        v.gz_alone = gzip_len(v.body_bytes)
    if u.n_bytes == 0:
        return 0.0
    gz_vu = gzip_len(v.body_bytes + u.body_bytes)
    return (gz_vu - v.gz_alone) / u.n_bytes


def compute_pair_matrix(units: List[Unit]) -> Dict[str, Dict[str, float]]:
    """pair_B(u, v) for every ordered pair u != v. Returns
    unit_path_u -> {unit_path_v: pair_B}."""
    compute_alone_lengths(units)
    matrix: Dict[str, Dict[str, float]] = {u.path: {} for u in units}
    for u in units:
        for v in units:
            if u.path == v.path:
                continue
            matrix[u.path][v.path] = pair_B(u, v)
    return matrix


# ---------------------------------------------------------------------------
# P-GUARD, MinLengthFloor, verdict_hint (discovery §3.4, §3.5)
# ---------------------------------------------------------------------------


class Taus:
    def __init__(self, neardup, cut, merge, tighten_a, tighten_delta, floor):
        self.neardup = neardup
        self.cut = cut
        self.merge = merge
        self.tighten_a = tighten_a
        self.tighten_delta = tighten_delta
        self.floor = floor

    def as_dict(self) -> dict:
        return {
            "NEARDUP_TAU": self.neardup,
            "CUT_TAU": self.cut,
            "MERGE_TAU": self.merge,
            "TIGHTEN_A_TAU": self.tighten_a,
            "TIGHTEN_DELTA_TAU": self.tighten_delta,
            "MIN_LENGTH_FLOOR": self.floor,
        }


def build_ranked_map(units: List[Unit], taus: Taus) -> List[dict]:
    metrics = compute_A_B_delta(units)
    pair_matrix = compute_pair_matrix(units)

    rows = []
    for u in units:
        m = metrics[u.path]
        A, B, Delta = m["A"], m["B"], m["Delta"]
        pairs = pair_matrix[u.path]  # v_path -> pair_B(u, v)

        # merge_partner = argmin_v pair_B(u, v); always recorded.
        merge_partner, merge_partner_pb = None, None
        if pairs:
            merge_partner, merge_partner_pb = min(pairs.items(), key=lambda kv: kv[1])

        # P-GUARD: near-dup of v iff pair_B(u, v) <= NEARDUP_TAU; protected if
        # >= 2 distinct such v.
        near_dup_partners = sorted(v for v, pb in pairs.items() if pb <= taus.neardup)
        protected_flag = len(near_dup_partners) >= 2

        # cut: B <= CUT_TAU and exactly one dominant partner with pair_B <= CUT_TAU
        dominant_partners = [v for v, pb in pairs.items() if pb <= taus.cut]

        # verdict_hint precedence: below-floor -> protected -> cut -> merge -> tighten -> keep
        if u.n_tokens < taus.floor:
            verdict = "below-floor"
        elif protected_flag:
            verdict = "protected"
        elif B <= taus.cut and len(dominant_partners) == 1:
            verdict = "cut"
        elif B <= taus.merge and merge_partner is not None:
            verdict = "merge"
        elif A <= taus.tighten_a and Delta <= taus.tighten_delta:
            verdict = "tighten"
        else:
            verdict = "keep"

        rows.append({
            "unit_path": u.path,
            "n_bytes": u.n_bytes,
            "n_tokens": u.n_tokens,
            "A": round(A, 6),
            "B": round(B, 6),
            "Delta": round(Delta, 6),
            "merge_partner": merge_partner,
            "merge_partner_pair_B": round(merge_partner_pb, 6) if merge_partner_pb is not None else None,
            "protected_flag": protected_flag,
            "near_dup_partners": near_dup_partners,
            "verdict_hint": verdict,
            "frontmatter_present": u.frontmatter_present,
            "frontmatter_bytes": u.frontmatter_bytes,
            "description": u.description,
        })

    # Ranked ascending by B; ties broken by ascending Delta. below-floor units
    # are reported but sort after the ranked units (they are "outside the
    # ranking" per discovery §3.4/§3.5, still emitted in the same table).
    def sort_key(row):
        outside_ranking = row["verdict_hint"] == "below-floor"
        return (outside_ranking, row["B"], row["Delta"])

    rows.sort(key=sort_key)
    return rows


# ---------------------------------------------------------------------------
# Output (discovery §3.6)
# ---------------------------------------------------------------------------

CSV_COLUMNS = [
    "unit_path", "n_bytes", "A", "B", "Delta", "merge_partner",
    "protected_flag", "verdict_hint",
]


def write_csv(rows: List[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r[k] for k in CSV_COLUMNS})


def write_json(rows: List[dict], taus: Taus, path: Path, extra_manifest: Optional[dict] = None) -> None:
    manifest = {"taus": taus.as_dict(), "gzip_level": GZIP_LEVEL, "n_units": len(rows)}
    if extra_manifest:
        manifest.update(extra_manifest)
    payload = {"manifest": manifest, "ranked_redundancy_map": rows}
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def render_digest(rows: List[dict], taus: Taus, top_n: int) -> str:
    ranked = [r for r in rows if r["verdict_hint"] != "below-floor"]
    below_floor = [r for r in rows if r["verdict_hint"] == "below-floor"]
    protected = [r for r in rows if r["protected_flag"]]

    lines = []
    lines.append("Assay S0 -- RankedRedundancyMap digest")
    lines.append("=" * 60)
    lines.append(f"units: {len(rows)}  ranked: {len(ranked)}  "
                  f"below-floor: {len(below_floor)}  protected: {len(protected)}")
    lines.append("taus: " + json.dumps(taus.as_dict()))
    lines.append("")
    lines.append(f"Top {min(top_n, len(ranked))} most-redundant (ascending B, tie ascending Delta):")
    lines.append("-" * 60)
    for r in ranked[:top_n]:
        lines.append(
            f"  B={r['B']:.4f}  A={r['A']:.4f}  d={r['Delta']:+.4f}  "
            f"[{r['verdict_hint']:8s}]  {r['unit_path']}  "
            f"(merge_partner={r['merge_partner']})"
        )
    lines.append("")
    lines.append(f"Protected (P-GUARD, >=2 distinct near-dup partners, tau={taus.neardup}):")
    lines.append("-" * 60)
    if protected:
        for r in protected:
            lines.append(f"  {r['unit_path']}  B={r['B']:.4f}  partners={r['near_dup_partners']}")
    else:
        lines.append("  (none)")
    lines.append("")
    lines.append(f"Below MinLengthFloor ({taus.floor} word-proxy tokens), reported not ranked:")
    lines.append("-" * 60)
    if below_floor:
        for r in below_floor:
            lines.append(f"  {r['unit_path']}  n_tokens={r['n_tokens']}")
    else:
        lines.append("  (none)")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Acceptance test (discovery §3.7)
# ---------------------------------------------------------------------------


def find_readme_partner(skill_path: Path) -> Optional[Path]:
    readme = skill_path.parent / "README.md"
    return readme if readme.exists() else None


def run_acceptance(root: Path, skills_glob: str, taus: Taus, acceptance_tau: float) -> bool:
    skill_paths = sorted(root.glob(skills_glob), key=lambda p: p.as_posix())

    pairs = []  # (skill_unit, readme_unit)
    identical_pairs = []
    for sp in skill_paths:
        rp = find_readme_partner(sp)
        if rp is None:
            continue
        skill_unit = Unit(sp.relative_to(root).as_posix(), sp.read_text(encoding="utf-8"))
        readme_unit = Unit(rp.relative_to(root).as_posix(), rp.read_text(encoding="utf-8"))
        pairs.append((skill_unit, readme_unit))
        if skill_unit.body == readme_unit.body:
            identical_pairs.append((skill_unit, readme_unit))

    # Split identical pairs into window-safe (body fits inside the 32KB LZ77
    # lookback, so §3.2/§3.4's "partner is always inside the window" claim
    # actually holds) vs. window-exceeded (body itself > 32KB, so the leading
    # portion of the pair falls outside the lookback by construction -- the
    # same accepted DEFLATE blind spot §3.2 pins, now visible inside pair_B
    # for an oversized single unit). This split is computed from n_bytes, not
    # cherry-picked per file.
    window_safe_pairs = [p for p in identical_pairs if p[0].n_bytes <= LZ77_WINDOW_BYTES]
    window_exceeded_pairs = [p for p in identical_pairs if p[0].n_bytes > LZ77_WINDOW_BYTES]

    print(f"Acceptance harness: {len(skill_paths)} SKILL.md files, "
          f"{len(pairs)} with a paired README.md, "
          f"{len(identical_pairs)} body-identical (computed at runtime, not hardcoded); "
          f"{len(window_safe_pairs)} within the {LZ77_WINDOW_BYTES}-byte LZ77 window, "
          f"{len(window_exceeded_pairs)} exceed it.")
    print()

    # --- Assertion 1: window-safe gate. pair_B(u, partner) approx 0 for every
    # body-identical pair whose body fits inside the LZ77 window (discovery
    # §3.2's accepted blind spot applies, not gated, to any pair that doesn't). ---
    a1_rows = []
    a1_pass = True
    for skill_unit, readme_unit in window_safe_pairs:
        pb_su = pair_B(skill_unit, readme_unit)  # partner (readme) directly before u (skill)
        pb_us = pair_B(readme_unit, skill_unit)  # partner (skill) directly before u (readme)
        ok = pb_su <= acceptance_tau and pb_us <= acceptance_tau
        a1_pass = a1_pass and ok
        a1_rows.append((skill_unit.path, readme_unit.path, pb_su, pb_us, ok))

    print(f"Assertion 1 (window-safe gate, pair_B <= {acceptance_tau}):")
    for skill_path, readme_path, pb_su, pb_us, ok in a1_rows:
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] pair_B(SKILL, README)={pb_su:.6f}  "
              f"pair_B(README, SKILL)={pb_us:.6f}   {skill_path} <-> {readme_path}")
    print(f"=> Assertion 1: {'PASS' if a1_pass else 'FAIL'} "
          f"({sum(1 for r in a1_rows if r[4])}/{len(a1_rows)} window-safe pairs within tau)")
    if window_exceeded_pairs:
        print(f"  (excluded from the gate, reported separately -- body exceeds the "
              f"{LZ77_WINDOW_BYTES}-byte LZ77 window, so §3.2's window-safety premise "
              f"does not hold for these):")
        for skill_unit, readme_unit in window_exceeded_pairs:
            pb_su = pair_B(skill_unit, readme_unit)
            pb_us = pair_B(readme_unit, skill_unit)
            print(f"    [window-exceeded, n_bytes={skill_unit.n_bytes}] "
                  f"pair_B(SKILL, README)={pb_su:.6f}  pair_B(README, SKILL)={pb_us:.6f}   "
                  f"{skill_unit.path} <-> {readme_unit.path}")
    print()

    # --- Assertion 2: P-GUARD near-dup predicate fires on those same
    # window-safe pairs. ---
    a2_rows = []
    a2_pass = True
    for skill_unit, readme_unit in window_safe_pairs:
        pb_su = pair_B(skill_unit, readme_unit)
        pb_us = pair_B(readme_unit, skill_unit)
        neardup_su = pb_su <= taus.neardup
        neardup_us = pb_us <= taus.neardup
        ok = neardup_su and neardup_us
        a2_pass = a2_pass and ok
        a2_rows.append((skill_unit.path, readme_unit.path, pb_su, pb_us, ok))

    print(f"Assertion 2 (P-GUARD near-dup predicate fires, NEARDUP_TAU={taus.neardup}):")
    for skill_path, readme_path, pb_su, pb_us, ok in a2_rows:
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] pair_B(SKILL, README)={pb_su:.6f} <= {taus.neardup}  "
              f"pair_B(README, SKILL)={pb_us:.6f} <= {taus.neardup}   {skill_path}")
    print(f"=> Assertion 2: {'PASS' if a2_pass else 'FAIL'} "
          f"({sum(1 for r in a2_rows if r[4])}/{len(a2_rows)} window-safe pairs caught by P-GUARD)")
    if window_exceeded_pairs:
        for skill_unit, readme_unit in window_exceeded_pairs:
            pb_su = pair_B(skill_unit, readme_unit)
            still_caught = pb_su <= taus.neardup
            print(f"  [window-exceeded, informational] {skill_unit.path}: "
                  f"pair_B={pb_su:.6f} vs NEARDUP_TAU={taus.neardup} -> "
                  f"{'still caught' if still_caught else 'NOT caught by P-GUARD at this size'}")
    print()

    # --- Assertion 1b (diagnostic only, NOT a gate): full-corpus leave-one-out
    # B over the SKILL-units + README-units combined corpus; a body-identical
    # pair's B only tops the map when its partner falls within the trailing
    # 32KB of the path-sorted corpus. ---
    all_units = []
    for sp in skill_paths:
        all_units.append(Unit(sp.relative_to(root).as_posix(), sp.read_text(encoding="utf-8")))
    for _, readme_unit in pairs:
        all_units.append(readme_unit)
    all_units.sort(key=lambda u: u.path)

    metrics = compute_A_B_delta(all_units)
    ranked_paths = sorted(metrics.keys(), key=lambda p: (metrics[p]["B"], metrics[p]["Delta"]))
    rank_of = {p: i for i, p in enumerate(ranked_paths)}

    identical_paths = set()
    for skill_unit, readme_unit in identical_pairs:
        identical_paths.add(skill_unit.path)
        identical_paths.add(readme_unit.path)

    top_k = len(identical_paths)
    top_k_set = set(ranked_paths[:top_k]) if top_k else set()
    tops_map = identical_paths.issubset(top_k_set) if top_k else True

    print(f"Assertion 1b (diagnostic, NOT gated -- full-corpus B, 32KB LZ77 window limit):")
    print(f"  {len(all_units)} units in combined SKILL+README corpus.")
    print(f"  body-identical units occupy top-{top_k} of ascending-B rank: {tops_map}")
    for skill_unit, readme_unit in identical_pairs:
        print(f"    {skill_unit.path}: B={metrics[skill_unit.path]['B']:.4f} rank={rank_of[skill_unit.path]}   "
              f"{readme_unit.path}: B={metrics[readme_unit.path]['B']:.4f} rank={rank_of[readme_unit.path]}")
    print("  (expected to be false when the partner falls outside the trailing "
          "32KB of the path-sorted corpus -- not a failure, this is why the S0 "
          "gate uses window-safe pair_B, not full-corpus B.)")
    print()

    overall = a1_pass and a2_pass
    print("=" * 60)
    print(f"S0 -> S1 GATE: {'PASS' if overall else 'FAIL'} "
          f"(Assertion 1: {'PASS' if a1_pass else 'FAIL'}, "
          f"Assertion 2: {'PASS' if a2_pass else 'FAIL'}; "
          f"Assertion 1b is diagnostic only, not gated)")
    return overall


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def find_repo_root(start: Path) -> Path:
    """Walk up from `start` looking for a `.claude/skills` directory."""
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".claude" / "skills").is_dir():
            return candidate
    return cur


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", type=Path, default=None,
                         help="Repo root (default: auto-detected by walking up "
                              "from this script to find .claude/skills).")
    parser.add_argument("--skills-glob", default=DEFAULT_SKILLS_GLOB)
    parser.add_argument("--out-dir", type=Path, default=None,
                         help="Where to write CSV/JSON/digest (default: ./out "
                              "next to this script).")
    parser.add_argument("--top-n", type=int, default=20)
    parser.add_argument("--acceptance", action="store_true",
                         help="Run the S0->S1 acceptance gate instead of a normal map run.")

    parser.add_argument("--neardup-tau", type=float, default=DEFAULT_NEARDUP_TAU)
    parser.add_argument("--cut-tau", type=float, default=DEFAULT_CUT_TAU)
    parser.add_argument("--merge-tau", type=float, default=DEFAULT_MERGE_TAU)
    parser.add_argument("--tighten-a-tau", type=float, default=DEFAULT_TIGHTEN_A_TAU)
    parser.add_argument("--tighten-delta-tau", type=float, default=DEFAULT_TIGHTEN_DELTA_TAU)
    parser.add_argument("--min-length-floor", type=int, default=DEFAULT_MIN_LENGTH_FLOOR)
    parser.add_argument("--acceptance-tau", type=float, default=DEFAULT_ACCEPTANCE_TAU,
                         help="Assertion-1 threshold for 'pair_B approx 0' (default 0.05).")

    args = parser.parse_args(argv)

    script_dir = Path(__file__).resolve().parent
    root = args.root or find_repo_root(script_dir)
    taus = Taus(args.neardup_tau, args.cut_tau, args.merge_tau,
                args.tighten_a_tau, args.tighten_delta_tau, args.min_length_floor)

    if args.acceptance:
        ok = run_acceptance(root, args.skills_glob, taus, args.acceptance_tau)
        return 0 if ok else 1

    units = load_units(args.skills_glob, root)
    if not units:
        print(f"No units found for glob {args.skills_glob!r} under {root}", file=sys.stderr)
        return 2

    rows = build_ranked_map(units, taus)

    out_dir = args.out_dir or (script_dir / "out")
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "assay_s0_map.csv"
    json_path = out_dir / "assay_s0_map.json"
    digest_path = out_dir / "assay_s0_digest.txt"

    write_csv(rows, csv_path)
    write_json(rows, taus, json_path, extra_manifest={"skills_glob": args.skills_glob, "root": str(root)})
    digest = render_digest(rows, taus, args.top_n)
    digest_path.write_text(digest, encoding="utf-8")

    print(digest)
    print(f"Wrote: {csv_path}")
    print(f"Wrote: {json_path}")
    print(f"Wrote: {digest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
