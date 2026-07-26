# Skill graph — frontend constitution check

Authority: `vault/constitution/frontend-constitution.md` (`CONST-FE`, candidate).

## Applied to the graph

| Rule | Implementation evidence |
|---|---|
| FE-1 | “Quem chama / o que chama” is compact by default; weak mentions and relationship evidence expand per element. |
| FE-2 | Secondary explanation uses the single `#tt` tooltip and `data-tip`; primary evidence remains keyboard/touch reachable by click. |
| FE-3 | Interactive nodes and relationships have hover/focus physics; relationship evidence closes immediately on outside click or `Esc`. |
| FE-4 | Each edge reveals direction, relation strength, and source evidence through one quiet marker. |
| FE-5 | Loading, error, empty, no-match, and bounded-absence states are explicit and operator copy is pt-BR. |
| FE-6 | One `expandedRelationship` key owns the only open relationship-evidence panel. |
| FE-7 | Path depth/count limits and evidence semantics are declared on-screen. |
| FE-8 | A/B/C remain explicitly labelled candidates; this change promotes no variant. |
| FE-9 | Explain mode is opt-in and uses the constitutional 3-second dwell; `Esc` dismisses immediately. |
| FE-10 | FE-1…FE-10 have query flags, stable `data-fe-rule`/`data-testid` anchors, and browser-visible metric counters under `window.__CC_FE__`. |

## Semantic boundary

- `explicit_path` is shown as a **declared call/reference**, never as proof that runtime
  execution occurred.
- `named_reference` is shown only as a **weak textual mention** and is collapsed separately.
- The runtime call graph remains unavailable until invocation telemetry can prove caller/callee
  execution. Unknown evidence is never rendered as zero.

