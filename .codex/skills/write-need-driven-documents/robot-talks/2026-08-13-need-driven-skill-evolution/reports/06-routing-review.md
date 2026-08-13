# Routing and scope review

## Frozen digest

- Reviewed `.codex/skills/write-need-driven-documents/SKILL.md` at SHA-256
  `59B70A04856F8D2695C0980FA3270ECAD6348A661FD1B8CEABEEBD81B0ECE166`.
- Reviewed the status-marked `findings.md`, `reports/03-editor-handoff.md`, and
  `reports/05-editor-response-reader.md`.
- Used `.agents/skills/create-skill/SKILL.md` as the engineering standard.
- No target file was edited.

## Verdict

**ACCEPT**

The frozen revision preserves a narrow, discoverable routing contract and implements every behavior
it promises without turning the body into a general style guide. The reader-review corrections
remove accidental novelty requirements while retaining operational transition tests; they do not
broaden the skill's trigger or purpose.

## Findings

No revision finding remains within this review's routing-and-scope boundary.

- **Description/body coherence:** The description routes only reader-facing overviews and
  explanatory essays whose central difficulty is conceptual ordering, while the body consistently
  governs that movement through opening, progression, relation, naming, claims, and final-read
  checks (`SKILL.md:3,10-15,17-70,102-110`). No body capability silently expands the routed task.
- **Triggers and exclusions:** The positive trigger names both writing and material restructuring;
  the exclusions separate those tasks from routine answers, summaries, specifications, research
  reports, plans, reference documents, and surface copyediting (`SKILL.md:3`). This is specific
  enough to avoid routing ordinary prose work into the skill without pretending that every essay
  needs it.
- **Material-restructuring promise:** The body now supplies a bounded structural diagnosis: recover
  the attempted movement, locate its first break, and revise from there (`SKILL.md:22-25`). This
  satisfies the description without adding a second editing framework.
- **Degree of freedom and imperatives:** The instructions prescribe observable constraints and
  private tests while leaving rhetorical form open (`SKILL.md:14-15,27-41,104-110`). Imperatives
  are actionable where failure is costly; the skill does not prescribe paragraph counts, stock
  openings, fixed sections, or a house voice.
- **Failure-mode coverage:** The contract directly covers generic openings, unearned concepts,
  inert transitions, sequence dependence, catalogue-like grouping, premature terminology,
  unsupported claims, decorative phrasing, and recap endings (`SKILL.md:22-41,43-70,72-110`). The
  examples clarify three recurring structural failures rather than attempting encyclopedic style
  coverage.

## Refuted concerns

- **The body is broader than the routing description because it mentions judgment and decision:**
  Refuted. These are possible destinations of an explanatory document, not additional artifact
  types or triggers (`SKILL.md:3,10-12`).
- **The restructuring trigger overpromises full editorial coverage:** Refuted. “Materially
  restructure” is explicitly limited to repairing reader movement, and the body supplies exactly
  that diagnosis (`SKILL.md:3,22-25`). Surface copyediting remains excluded.
- **The new opening and transition tests create a formula:** Refuted. They test specificity and
  earned movement but do not prescribe an anecdote, thesis shape, transition phrase, or rhetorical
  sequence (`SKILL.md:27-36,104-107`).
- **The revised sequence rule broadens the skill into series management:** Refuted. It activates
  only when the document already belongs to a sequence and governs local intelligibility, not
  publication planning or cross-document administration (`SKILL.md:38-41`).
- **The negative examples make this a style guide:** Refuted. They remain tightly tied to the
  skill's core failure modes—collections without relations, terminology without prepared meaning,
  and structure without reading need—and are bounded by the instruction to apply only relevant
  guidance (`SKILL.md:14-15,72-100`).
- **Explicit-only package routing conflicts with repository-mandated essay routing:** Refuted on the
  reviewed evidence. As recorded in `findings.md:F6`, the scopes are compatible and no metadata
  change is authorized; global invocation intent remains a separate product decision.

## Coverage

- Description/body coherence: reviewed; acceptable.
- Explicit positive triggers and exclusions: reviewed; acceptable.
- Material-restructuring behavioral support: reviewed; acceptable.
- Degree of freedom and imperative quality: reviewed; acceptable.
- Failure-mode coverage: reviewed; acceptable within the narrow conceptual-composition purpose.
- Risk of expansion into a general style guide: reviewed; controlled.
- Previously rejected findings: not reopened without new evidence.
- Behavioral transfer: not assessed. Acceptance is limited to routing and contract engineering;
  `findings.md:F8` still requires blind executions before any reliability claim.
