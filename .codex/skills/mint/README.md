# Mint

**Mint casts the cav2 authority spine onto a specific domain, producing a new domain-specialized
repository that can author its own governed authority.** It composes the `domainspec-new-repo`
scaffolder for the doc-tree (the smaller half) and owns the authority-spine casting (the core).

- **Tier rationale:** arcana-class — a signed governance act with owner-ratification and gates, not a
  file drop. Installed as a **cav2-native, private** skill (beside `constitution-governance`,
  `definitions-governance`, `decision-gate`, `invoke`), **not** under public `arcanum/`.
- **Status:** candidate · intended-**not**-shipped. The sigil *contract* is authored; the emit-template
  set + the 2026-07-01 committed additions are being built (WORK-PACK SWU-2/5–10). Invoking Mint today
  will **block** at the spine-seed stage with a named gap, by design.

## Use it when
Starting a new domain / research / project repo that needs a governed authority spine (kinds,
definitions, constitutions, promotion lifecycle) and has an owner to ratify the proposed kinds.

## Do not use it when
- editing an existing repo's authority → route to `definitions-governance` / `constitution-governance` / `decision-gate`;
- the mint would emit a **public-attached** repo → blocked by `BLK-CAV2-PUBLIC-PRIVATE-001`;
- you would seed cav2's own object kinds/rows as the domain's governing base → circularity (the mold casting itself).

## Inputs / Outputs
Inputs: `domain`, `target-repo-path`, `--source <framework>`, `--attach submodule|copy|symlink`.
Outputs: a minted repo's `authority/`, `definitions/`, `constitutions/`, crosswalk, and a signed
`authority/decisions/<date>-mint.md` — owned by the *new* repo's lifecycle (Mint is the authoring capability).

## The inherit / localize rule (load-bearing)
Inherit the **MOLD** (how authority is made — rules, formats, lifecycles, routes); localize the
**casting** (what this domain holds — its own kind rows, definitions, decisions). Never inherit cav2's
object rows as a governing base. The 2026-07-01 audit confirmed the ontology/artifact package is
correctly withheld on exactly this ground.

## Lifecycle
`invoke` (authoring, done) → **`sigil-development`** (this build) → `task-session` (execute SWUs). Next:
build the emit-template set + Tier-1 additions (SWU-5/6/7 first — they close live defects #8/#11/#13),
validated by `experiment-harness` against the resonantos golden fixture. Design authority and the full
build backlog live in `cyberAlchemy-v2/development/mint/`.
