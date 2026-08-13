# Package review

## Frozen digest

- Reviewed both `SKILL.md` mirrors at SHA-256
  `59B70A04856F8D2695C0980FA3270ECAD6348A661FD1B8CEABEEBD81B0ECE166`.
- Reviewed both `agents/openai.yaml` mirrors at SHA-256
  `6CDCFCFC89F0EF021C9FC933265BB0206CD8D89592B46DA9094ACACF2573D4DC`.
- Reviewed the status-marked `findings.md` and editor handoffs/responses 03, 05, and 07.
- No skill, metadata, evidence, or mirror file was changed.

## Verdict

**REVISE**

The runtime surface is acceptable, but the full `.codex` skill directory is not yet a cleanly
defined distributable package. This verdict is limited to the unresolved evidence/package boundary;
it does not reopen the accepted writing contract.

## Findings

### P1 - Runtime mirror integrity is proven; package mirror integrity is not

**Evidence:** The two `SKILL.md` files and the two `agents/openai.yaml` files are byte-identical. The
`.agents` tree contains only those two runtime files, while the `.codex` tree also contains eleven
Robot-Talks evidence files under `robot-talks/`. Platform guidance excludes creation and testing
records from a distributable runtime skill, while reviewed finding F7 preserves this investigation
beside its owning context unless a human authorizes a separate migration. `quick_validate.py`
accepts both trees, demonstrating that it does not adjudicate this distribution boundary.

**Impact:** LOW for runtime loading because `SKILL.md` does not reference the evidence; MODERATE if
the `.codex/skills/write-need-driven-documents` directory is copied or published wholesale.

**Minimum correction:** At the human gate, either define the distributable input explicitly as the
two runtime files (`SKILL.md` and `agents/openai.yaml`) or authorize a separate atomic migration of
the preserved Robot-Talks record to another owning context. Do not duplicate the evidence into the
`.agents` mirror merely to make the trees equal.

## Refuted concerns

- **Frontmatter and routing are too broad:** Refuted. The description names the artifact types and
  conceptual-ordering difficulty that trigger the skill, includes material restructuring, and
  excludes adjacent routine work. The body implements that promise without adding unrelated
  capabilities.
- **The skill is over-prescriptive:** Refuted. At 110 lines and 923 words, it uses compact private
  tests where structural failure is costly while leaving rhetorical form, paragraph count, voice,
  and technique open.
- **Progressive disclosure requires more resources:** Refuted. The core workflow is short enough to
  remain in `SKILL.md`; no variant-specific reference or deterministic script is currently needed.
  The Robot-Talks record is process evidence, not a runtime reference to expose through the skill.
- **UI metadata is stale or inconsistent:** Refuted. Display name and short description accurately
  summarize the narrow capability; the 44-character short description is within the documented
  25-64 character range; the default prompt names `$write-need-driven-documents`; and explicit-only
  invocation is compatible with the repository's separate mandatory essay route. Intent beyond
  that compatibility remains unproven, as F6 records.

## Validation results

- Expected frozen digest: **PASS** for both `SKILL.md` mirrors.
- Runtime mirror comparison: **PASS** for `SKILL.md` and `agents/openai.yaml`.
- `quick_validate.py` on `.codex/skills/write-need-driven-documents`: **PASS** (`Skill is valid!`).
- `quick_validate.py` on `.agents/skills/write-need-driven-documents`: **PASS** (`Skill is valid!`).
- YAML parse on both `agents/openai.yaml` files: **PASS**.
- Metadata constraints checked directly: **PASS** for quoted strings, required skill reference in
  `default_prompt`, short-description length, and boolean invocation policy.
- Full-tree mirror comparison: **NOT APPLICABLE AS PROOF** until P1's package boundary is decided;
  the source tree intentionally contains preserved evidence that the runtime mirror does not.
- Blind forward-testing: **NOT RUN**, consistent with this read-only package-review seat.

## Claim boundary

This review establishes that the frozen runtime contract is concise, mechanically valid,
metadata-aligned, and byte-identical across its two runtime mirrors. It does not establish that the
skill reliably improves essay output, generalizes to unrelated conceptual writing, or causes the
desired opening and progression behavior; F8 still requires uncontaminated forward tests before any
such behavioral claim. It also does not establish that the whole `.codex` directory is
distribution-ready until the human-gated F7 boundary is resolved.
