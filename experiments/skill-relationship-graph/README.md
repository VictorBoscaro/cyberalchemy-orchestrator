# Skill relationship graph experiment

Quick static probe over `.claude/skills/*/SKILL.md`. The recorded run in `experiment.md` read the
byte-identical `.agents/skills` host mirror, which is now a local, git-ignored copy.

## Run

```powershell
cd experiments/skill-relationship-graph
python build_graph.py --repo ../..
```

Outputs:

- `experiment.md`: probe inputs and raw-result summary.
- `findings.md`: adjudication and structural classes.
- `graph.json`: nodes, typed edges, evidence, degrees, and verdict.
- `viewer.html`: local interactive graph with definition drafts persisted in the browser.
- `graph.dot`: Graphviz projection of the inclusive graph.

The experiment deliberately distinguishes explicit `SKILL.md` path references from weaker
inline-code name mentions. It does not claim to observe runtime invocation.
