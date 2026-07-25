# Findings — Assay Forward Research Synthesis

Dispatch: `2026-07-23-assay-forward-research`. Assay = document-information-estimator; one engine `marginal_information(unit | corpus)`. First use case = prolixity of our own instruction system, gzip-first. Sources: three verbatim explorer returns in `research.md` (X = Xiao/compression-ownership, L = Liu/eval-ownership, S = Shannon/in-repo S0).

Governing rule (P10, claim <= proof): a found owner is a WIN (build-from-owned), never a kill. Only **no-witness** (non-vacuity fails: nothing concrete exhibited) or **tautological** (definitional collapse: the candidate is true-by-restatement, measures nothing) yields KILL.

---

## Verdict Matrix

| candidate | owner/precedent | witnessed? (non-vacuity) | sound? (definitional) | verdict | use-mode |
|---|---|---|---|---|---|
| (1) Column-B compute kernel L(unit\|corpus) | Microsoft `llmlingua` `PromptCompressor.get_condition_ppl` [X-a] | YES — checked callable signature, per-token cross-entropy masked to unit-after-corpus [X-a] | YES — conditional pointwise MI, not a restatement of the input [X-a] | **GO** | build-from-owned |
| (2) behavioral-equivalence-on-instructions eval | Amazon info-preservation framework (arXiv:2503.19114) + AgentEvals trajectory-matching + SkillReducer [L-a,b] | YES — two halves each concretely exist and are cited; neither fuses them [L-b] | YES — measures tool/args/gate/trajectory identity, a real behavioral property [L-b] | **GO** | build-from-owned (novel fusion) |
| (3) P-GUARD genre-guard (shrink->tighten) | none — SecurityLingua is a technique, not the principle [L-c] | WEAK — no external instance states the principle; only an unverified medium-prompt claim, flagged non-load-bearing [L-c] | YES — a design stance, non-tautological | **GO (demoted)** | novel-attempt |
| (4) repo-asset readiness for S0 | in-repo: 66 SKILL.md, dispatch ledger, agent-pool-mcp [S-a,c,e] | YES — 12/48 byte-identical composed-spell pairs; repository-harness<->README exact copy [S-b] | YES — gzip ratio separates exact copies, a measurable signal [S-e] | **GO** | already-deployed (assets) / build-from-owned (harness) |

---

## Synthesis

**(1) Compute kernel — GO, build-from-owned.** The primitive Assay needs is owned and pip-installable, not hypothetical. `PromptCompressor.get_condition_ppl(text=<unit>, question=<corpus>, condition_in_question="before")` returns exactly per-token cross-entropy of a unit conditioned on a corpus prefix — Assay's `L(unit|corpus)` off the shelf, verified by reading `llmlingua/prompt_compressor.py`, a checked signature not an inferred paper claim [X-a]. This is the engine under LongLLMLingua's contrastive perplexity = conditional pointwise mutual information [X-a].
*Collapse-test (keystone):* if `get_condition_ppl` returned only a scalar compressed prompt (not per-token loss), the kernel would be unwitnessed and this collapses to KILL. It does not — `get_ppl` exposes `CrossEntropyLoss(reduction="none")` per-token [X-a]. Survives.
Wrap the primitive, build the corpus-serialization + unit-aggregation + threshold layer: causal single-prefix conditioning forces our own ordering/chunking; no unit-level redundancy score upstream; no gzip confound guard upstream [X-b]. Applying the wrapped kernel to a *self-instruction corpus* is itself non-owned — LLMLingua/Selective-Context are document/RAG-focused; no paper formalizes redundancy-of-an-instruction-given-the-rest [X-c].

**(2) Behavioral-equivalence eval — GO, build-from-owned (novel fusion).** Not a kill: both halves are witnessed owners. Amazon's arXiv:2503.19114 owns the fidelity-eval methodology (downstream EM/BERTScore, claim-faithfulness); SkillReducer owns agentic skill-file compression with pass-rate [L-a]. The gap is real and narrow: no external work measures *same tool, same args, same gate, same trajectory shape, before-vs-after instruction compression* — an unfused intersection of two covered areas [L-b].
*Collapse-test (keystone):* if AgentEvals trajectory-matching were already instrumented for pre/post-compression prompts, candidate (2) would be already-deployed, not build. Liu confirms AgentEvals is the right primitive but NOT instrumented for compression pairs [L-a #5] — so build-from-owned holds, not KILL and not already-deployed. Survives.

**(3) P-GUARD genre-guard — GO but demoted to novel-attempt.** The shrink->tighten principle (compressing an instruction corpus should tighten, not merely shorten, its guardrails) has no external owner: SecurityLingua is a specific security-aware compressor, not the general principle, and the only supporting empirical claim (medium 20-35w prompts maximize violations) is unverified and explicitly non-load-bearing [L-c]. Per P10 we do not inflate: this is an original design stance carried as a *novel-attempt*, not a witnessed principle. It is non-tautological (a falsifiable claim about compression's effect on compliance), so it is not a definitional KILL — but it earns nothing beyond "our own hypothesis to test."

**(4) Repo-asset readiness for S0 — GO, already-deployed assets + build harness.** The first use case (prolixity of our own instruction system) has a concrete, in-repo, gzip-detectable target *today*: 66 `.claude/skills/*/SKILL.md` files segment cleanly on frontmatter+body, and 12 of 48 composed-spell pairs are byte-identical-plus-frontmatter (e.g. repository-harness body == README.md) [S-a,b]. That is built-in ground-truth redundancy gzip's LZ77 will catch [S-b,e]. The dispatch ledger (56 dispatch rows) is directly replayable as a task set for candidate (2)'s eval [S-c]. Shipping vehicle: `tools/agent-pool-mcp/` is a working repo-local Node MCP template, though it carries no scoring logic to reuse [S-e].
*Known blind spot (must carry forward):* gzip cleanly separates exact copies but under-detects compositional paraphrase — paired-views restates its 3 components' single-owner invariant in different tokens, same claim; LZ77 misses most of it [S-b,e]. This is precisely the confound the LM kernel (candidate 1) exists to close, and it motivates the gzip->LM progression.

---

## BUILD-TIME obligations (out of THIS dispatch's scope)

Two obligations are flagged now and deferred to build:

- **Delta>0-on-private-content (S3/S4):** Assay must demonstrate strictly-positive marginal information on genuinely private/novel content — i.e. that it does not score all our own material as redundant. No explorer witnessed this; it is a build-time non-vacuity gate, not resolvable from prior art. (Compositional-paraphrase blind spot [S-b] is the near-term stressor.)
- **LM-vs-gzip bake-off (S3/S4):** the head-to-head that decides whether the owned LM kernel [X-a] beats gzip-first on the paraphrase cases gzip provably misses [S-e]. S0 ships gzip-only (lowest-risk, exact-copy target); the LM kernel earns its cost only by winning this bake-off. Out of scope here — this dispatch establishes ownership, not the empirical verdict.

---

## Dispatch goal — one-line answer

Every load-bearing piece of Assay is a GO: the `L(unit|corpus)` kernel is **build-from-owned** (Microsoft llmlingua [X-a]), the behavioral-equivalence eval is **build-from-owned novel fusion** (Amazon + AgentEvals + SkillReducer [L-a,b]), P-GUARD is a demoted **novel-attempt** [L-c], and S0 can ship gzip-first **today** against 12 byte-identical in-repo SKILL pairs [S-b] — with Delta>0-on-private-content and the LM-vs-gzip bake-off held as explicit S3/S4 build-time obligations.

---

## Gate outcomes & final recalibration (final_approver, 2026-07-23)

The reviewers (Tetlock/precedent [T], Gigerenzer/definitional [G]) and one feedback re-sweep [R = Liu re-sweep, loop_cap 1] revised the draft above. **No terminal KILL.** Net changes, authoritative over the matrix where they differ:

- **(1) kernel — build-from-owned SURVIVES; method attribution corrected.** [T] verified `llmlingua/prompt_compressor.py`: the load-bearing owned method is **`get_ppl(..., condition_mode="after", condition_pos_id=...)`** (per-token `CrossEntropyLoss(reduction="none")`, masked after a position), which the wrap-layer calls directly. `get_condition_ppl` is a thin wrapper whose exact signature could not be fully verified; do not cite it as the owned primitive — cite `get_ppl`. Ownership + coverage-HIGH unchanged.
- **(2) behavioral-eval — build-from-owned SURVIVES; NOT already-deployed; "novel fusion" sharpened, not retired.** [R] confirmed **ACON** (arXiv:2510.00615, Microsoft) owns the paired full-vs-compressed-trajectory *pattern* but on **observations/history only — NOT instruction-file compression** (checked github.com/microsoft/acon). CoACT (2607.02911) = fuzzy action-similarity, single-step, observations. AGORA (2605.26596) touches the instruction side only to **exclude it from compression** (always-keep floor), not to verify compressed-instruction equivalence. Residual gap **survives strictly**: (instruction-corpus compression) × (tool/args/gate/trajectory-shape identity). Recalibration: label **build-from-owned**, citing ACON's paired-diagnosis pattern + CoACT's operation-field scorer as **method donors (adjacent), not owners of the fused claim** — retire "novel *from scratch*", keep the fusion as the genuine, un-owned residual.
- **(3) P-GUARD — novel-attempt SURVIVES, precedent-clean at BOTH levels.** [T] cleared SecurityLingua (safety by intention-revelation, not shrinkage). [R] genre-aware-pruning probe found **no owner**: AGORA's always-keep is **role/structural**, not span-type/genre; TRACE/Squeez condition on task/attention, not content-type. Nearest structural neighbor = AGORA role-based always-keep (narrows, doesn't own). **Carry forward:** AGORA's 76-pt swing under meaning-preserving perturbation is **directional counter-evidence** to P-GUARD's "tighten" optimism — the first stressor to test against.
- **(3b / element decomposition) "self-corpus prolixity" is NOT an independent contribution — [G] KILL as re-skin.** The kernel call is byte-identical whether the tokens are a RAG passage or a `SKILL.md`; "self" is in the framing, not the operation, and gzip **already ships** the exact-copy case today [S-b]. Definitional residue of the *reading* alone = ∅; it is non-empty **only** by borrowing candidate (2)'s behavioral criterion. **Honest contribution of Assay = ONE object (behavioral-equivalence-on-instructions) + one falsifiable genre-hypothesis (P-GUARD).** The "relative-to-self-corpus" phrasing in §Synthesis(1)/(4) is owned-kernel + owned-gzip applied to renamed input — keep it as an *application*, never claim it as a distinct measurement object.
- **(4) repo-asset readiness — SURVIVES untouched** (no external precedent surface). S0 gzip-first against the 12 byte-identical pairs is confirmed as the correct, honest first build; [G] independently reinforces gzip already detects that regime.

**P9 citation check (final_approver):** every load-bearing claim in the matrix and synthesis cites a collected return (X/L/S in `research.md`) or a gate return (T/G/R, recorded here); the two keystone collapse-tests are inline (§Synthesis 1, 2). Accepted → dispatch closes `resolved`.

**Consequence for the build ladder:** S0 (gzip-only, confound-guarded, P-GUARD flag) is unaffected and remains the right first functional test — it ships exactly the owned, honest slice. The genuine contribution (behavioral falsifier) is a later rung, gated on the S3/S4 obligations above.
