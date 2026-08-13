# Key Findings

1. **The routing boundary is semantically strong but operationally split across two authorities.** The
   skill description names the artifact, the difficult condition, the positive action, and explicit
   exclusions (`.codex/skills/write-need-driven-documents/SKILL.md:2-3`), closely matching the
   repository essay route (`AGENTS.md:13-18`). However, the description says to use the skill
   "explicitly" and the UI policy disables implicit invocation
   (`.codex/skills/write-need-driven-documents/agents/openai.yaml:4-7`), while `AGENTS.md` makes use
   automatic by artifact type. This can be intentional—project routing compensating for conservative
   package routing—but the package does not state that design, so behavior outside this repository and
   behavior inside it are materially different.

2. **The body has an appropriate high degree of freedom, but too little operational leverage at the
   exact failure surfaces named by this investigation.** Its core procedure—establish the reader's
   starting point and intended change, introduce distinctions only when needed, and give each passage
   a necessary function—is compact and judgment-preserving
   (`.codex/skills/write-need-driven-documents/SKILL.md:17-28`). That altitude is right for variable
   conceptual essays. Yet the only final gate for openings and endings is that the opening establish a
   need the ending can answer (`SKILL.md:94-100`); there is no discriminating test for generic openings,
   false continuity, autonomous documents in a sequence, or endings that merely summarize. On those
   fragile behaviors, the skill currently supplies principles more readily than executable editorial
   decisions.

3. **Failure-mode coverage is dense but lopsided.** Four negative examples consume most of the applied
   guidance (`SKILL.md:59-93`), and three substantially target the same family of error: naming or
   grouping things without explaining their load-bearing relation (`SKILL.md:61-85`). This strongly
   blocks catalogue-shaped prose, but leaves the central evaluation concerns—opening, paragraph-to-
   paragraph progression, sequence-aware autonomy, ending, voice, and revision diagnosis—without one
   concrete counterexample or test. The skill is only 100 lines, so progressive disclosure is not yet
   needed for size; reallocating example density would be more justified than adding a broad style
   reference.

4. **The distributable package has sound UI metadata and mirror consistency, but contains process
   evidence that does not belong in a skill package.** `agents/openai.yaml` provides a matching display
   name, concise description, and default prompt (`agents/openai.yaml:1-4`), and the `.codex` and
   `.agents` copies of both `SKILL.md` and `agents/openai.yaml` are byte-identical in this review. In
   contrast, the nested `robot-talks/.../dialogue.md` is explicitly an investigation record and planned
   review workflow (`robot-talks/2026-08-13-need-driven-skill-evolution/dialogue.md:1-5,69-85`). The
   platform guidance says not to ship process and testing documentation as skill contents
   (`C:/Users/victo/.codex/skills/.system/skill-creator/SKILL.md:123-133`). Keeping governed evidence is
   valuable, but locating it beneath the skill directory weakens package purity and makes progressive
   disclosure accidental rather than intentional.

5. **Mechanical validation succeeds; behavioral validation is not yet demonstrated.** Running
   `quick_validate.py` against `.codex/skills/write-need-driven-documents` returns `Skill is valid!`,
   which supports frontmatter and naming correctness but nothing about writing behavior; the validator's
   documented scope is basic mechanics (`C:/Users/victo/.codex/skills/.system/skill-creator/SKILL.md:362-370`).
   The present Robot-Talks explicitly tells investigators to inspect the skill and its suspected concerns
   (`dialogue.md:49-67`), so it is review, not forward-testing. The prescribed forward-test instead gives
   a fresh agent the skill and a realistic task without revealing that the skill itself is under test
   (`C:/Users/victo/.codex/skills/.system/skill-creator/SKILL.md:386-416`). A revised skill therefore
   still needs blind task execution on at least the Part II opening problem and a materially different
   essay before claims of generalization are warranted.

# Gaps or Inconsistencies

- The package does not resolve whether explicit-only invocation is a deliberate portability boundary or
  stale metadata left behind after `AGENTS.md` made essay routing mandatory.
- "Begin with something the reader can recognize" (`SKILL.md:22`) is not falsifiable enough to reject a
  generic but grammatical opening.
- The scope promises material restructuring (`SKILL.md:3`), but the body does not distinguish composing
  from revising an existing reader movement or instruct the agent to diagnose the current break before
  rewriting.
- The central sequence requirement in the dialogue (`dialogue.md:18-20,28`) has no counterpart in the
  current behavioral contract.
- UI metadata is present and aligned, but the available mechanical validator does not establish that
  `agents/openai.yaml` conforms to its schema or that its `default_prompt` produces the intended route.
- The review plan includes several independent reviews and zig-zag revisions (`dialogue.md:69-77`) but no
  explicit blind forward-test stage. More reviewers will strengthen criticism, not substitute for use.

# Local Tensions

- **Conservative routing vs mandatory project behavior:** avoiding over-triggering is sensible, but two
  invocation policies make the package's true contract environment-dependent.
- **High freedom vs reliable openings:** prose requires contextual judgment, yet a few falsifiable tests
  can constrain predictable failure without imposing a visible template.
- **Conciseness vs coverage:** the body is admirably lean; adding every missing topic would create the
  general style manual the scope rejects. Existing example density should be rebalanced before the skill
  grows.
- **Evidence preservation vs package purity:** Robot-Talks records support traceability, but their current
  location makes development history part of the runtime skill folder.
- **Independent review vs validation integrity:** the planned reviewers can verify claims about the
  instructions; only agents performing realistic writing tasks without leaked diagnoses can test whether
  those instructions transfer into behavior.

# Questions for Synthesis

1. Is `allow_implicit_invocation: false` an intentional global policy, with `AGENTS.md` as the sole
   project-local trigger, or should package metadata and repository routing converge?
2. What is the smallest set of behavioral gates that can reject a generic opening, artificial paragraph
   progression, a sequence-dependent document, and a summary ending without turning the skill into a
   template?
3. Should revision receive one explicit diagnostic instruction distinct from composition, or is material
   restructuring outside the coherent scope implied by the current body?
4. Where should Robot-Talks and future test evidence live so they remain traceable without shipping inside
   the skill package?
5. Which two or three raw writing tasks and acceptance criteria will serve as blind forward-tests after
   editing, and who will judge outputs without leaking the intended fix?
