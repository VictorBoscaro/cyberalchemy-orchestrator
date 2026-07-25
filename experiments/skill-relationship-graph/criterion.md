# Frozen criterion

Status: frozen before the first probe run.

## Hypothesis

The repository's `SKILL.md` files contain enough explicit cross-skill references to produce a
non-empty relationship graph that identifies structurally distinct skills.

## Non-goals

- Prove that a skill was invoked at runtime.
- Infer dynamic calls hidden in scripts, hooks, prompts, or telemetry.
- Decide that a structurally isolated skill is useless.
- Mutate any skill package.

## Pre-registered categories

- `source`: incoming degree 0 and outgoing degree greater than 0.
- `sink`: incoming degree greater than 0 and outgoing degree 0.
- `isolated`: incoming degree 0 and outgoing degree 0.
- `connected`: incoming and outgoing degrees greater than 0.
- `explicit_path`: a reference whose target is another `SKILL.md`.
- `named_reference`: a known skill name appearing as Markdown inline code.

The inclusive graph uses both relation types. The strong graph uses only `explicit_path`.

## Mechanical verdict rule

- `INVALID` if fewer than 95% of discovered `SKILL.md` files can be parsed into uniquely named
  nodes, or if any explicit path reference to a local skill cannot be resolved.
- Otherwise `SURVIVED` if the inclusive graph has at least one edge and at least two of the four
  pre-registered structural categories are non-empty.
- Otherwise `FALSIFIED`.

## Discrimination check

- `SURVIVED` means a cheap static graph is already informative enough to expose repository
  structure and justify a more authoritative runtime graph later.
- `FALSIFIED` means textual declarations are too sparse or homogeneous; the next probe must use
  scripts, hooks, dispatch records, or invocation telemetry instead.

## Reproducibility

Run `python build_graph.py --repo ../..` from this directory. The same repository state and the
same frozen criterion must produce the same node, edge, and category sets.
