# Source Coverage

This table checks that the prototype graph accounts for every material instruction in
`.agents/skills/domainspec-spec-feature/SKILL.md`. It is trace evidence, not proof that the
prototype is complete.

| Skill source | Obligation | Protocol disposition |
|---|---|---|
| Objective, lines 9–11 | Produce complete and consistent DomainSpec documentation before implementation | `protocol-design.md` → Stable meaning |
| Context, lines 13–20 | Use taxonomy, relationships, templates and the feature target folder | `protocol-design.md` → Compiler inputs |
| Process 0.1, line 24 | Resolve feature slug from invocation | Compiler binding before `discovery_gate` |
| Process 0.2, line 25 | Parse waiver and preserve its exact reason | `discovery_gate` compiler input |
| Process 0.3, lines 26–28 | Search both discovery locations | `discovery_gate`; exact lookup mechanics remain a compiler binding |
| Process 0.4–0.5, lines 29–31 | Proceed on discovery or explicit waiver; write waiver frontmatter | `discovery_gate` plus SPEC writer contract |
| Process 0.6, lines 32–37 | Stop and emit required guidance when discovery is absent | `discovery_gate:waiting_user`; exact message remains a compiler binding |
| Document check, lines 39–42 | Check every write immediately with one helper; same helper re-checks once; report helpers | Inline review and zig-zag are preserved; reviewer cardinality is explicitly superseded by the user-directed shared review contract |
| Step 1, line 44 | Create or update SPEC and concept table | `spec_writer` plus `spec_review` |
| Step 2, line 45 | Create/update architecture with all required sections | Medium `remaining_writer`; High `architecture_cell` |
| Step 3, line 46 | Create glossary with one definition per concept | Medium `remaining_writer`; High `glossary_cell`; High parallelism explicitly supersedes the source ordering |
| Step 4, line 47 | Generate applicable aspects one at a time and check each | Medium preserves the sequential bundle; High uses parallel `aspect_cells`, explicitly superseding one-at-a-time production while preserving per-artifact review |
| Step 5, line 48 | Link SPEC to architecture and glossary | Remaining/integration writer responsibility; exact mutation plan remains open |
| Step 6, line 49 | Add applicable formal material | Remaining/integration writer responsibility |
| Step 7, line 50 | Validate the complete architecture contract | `contract_validation` system node |
| Step 8, line 51 | Summarize ready and undefined work | `summary` system node |

## Candidate gaps exposed by graphing

1. The source skill does not define a deterministic rule for selecting “relevant” aspect files.
   The prototype therefore makes `applicable_aspects` compiler-derived but cannot yet define its
   algorithm.
2. Updating `SPEC.md` during link/formal reconciliation is another document write. The graph
   conservatively expands another complete document check; the source text does not explicitly
   discuss this second check.
3. The user-authorized multi-reviewer and layered-review topology supersedes the source skill's
   single-helper cardinality. The source skill must eventually be updated or the protocol must
   retain a durable supersession receipt.
4. “Complete and consistent” is refined by the architecture contract but remains partially
   judgment-based outside the mechanically listed checks.
5. The skill declares a writer agent and a helper rule, but not bounds for models, tokens, tools,
   source delivery or path-level enforcement.
6. Robot-talks, multi-reviewer SPEC review, complete-corpus review and the final high-level reviewer
   come from explicit user direction captured in `protocol-design.md`, not from the source skill.
7. High parallelism across architecture, glossary and aspects supersedes the source skill's current
   sequential steps and therefore requires durable authority before protocol activation.

These gaps must remain visible during compilation. A profile cannot silently resolve them as if the
source skill had already decided.
