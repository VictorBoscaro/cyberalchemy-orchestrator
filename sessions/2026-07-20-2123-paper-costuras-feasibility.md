---
tags: [category-theory, decision-theory, anti-noise-hypothesis, prior-art-research, subagent-dispatch]
node_type: discovery
is_session: true
layer: architecture
nature: explanatory
status: active
created: 2026-07-20
timestamp: 2026-07-20T21:23:06-03:00
expires: 2026-09-18
conversation_id: deed2a59-68c4-49bf-896f-b343ca99f201
decisions_made: true
contradictions_found: true
specs_updated: [vault/hypothesis/orquestracao-anti-ruido.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Settles the paper's novelty claim (empty intersection, nearest neighbor named) and formal viability (both seams real-under-conditions), the two facts that decide whether the essay is worth continuing."
---

# Paper "orquestrador anti-ruído" — novidade e feasibility das duas costuras

## Summary

A sessão virou a direção anti-ruído do repo (HYP-ORCH-NOISE) rumo a um paper publicável.
Reenquadrei o pedido de "Kahneman ⊕ Thaler ⊕ Categorias" de tríade simétrica para um
triângulo com uma aresta densa (Kahneman–Thaler) e uma região quase-vazia (teoria das
categorias × viés/nudge), e rodei três dispatches tensionados de prior-art (void adversarial,
cartografia de vizinhos, gap-close não-web) que estabeleceram, de forma auditável em cinco
bases, que a interseção está **desocupada** — com duas colisões de título a desarmar
("categorização ≠ categorias": Fryer–Jackson, Ellis–Masatlioglu) e o programa de statistical
games composicionais (Smithe et al.) como vizinho mais próximo. Montei o scaffold do paper e persisti o veredito do prior-art.
Por decisão do Victor, Thaler ficou como pilar **primário** (não rebaixado), o que exigiu
pesquisa de feasibility própria. Projetei, passei pelo gate (`check-tension` both PASS) e rodei
um dispatch tensionado sobre as duas costuras formais — decomposição viés⊕ruído (Kahneman×CT) e
nudge-como-morfismo (Thaler×CT) — cada uma um par construtor⊥colapsador com um synthesizer
adjudicando. Ambas voltaram **real-sob-condições** e convergem na mesma casa (probabilidade
categórica): a costura Kahneman é o Pitágoras de Amari (Bregman/dualmente-plano) licenciado por
**um** potencial de Legendre `F` — que é a própria "escala comum ancorada" da tese; a costura
Thaler é vacua na óptica de juízo único mas real na **fibra de acoplamento** de `D(A^N)`
(marginalização não-mônica). O synthesizer julgou os desacordos **dispersão, não dissenso**, e
nomeou **composicionalidade-através-da-composição-de-estágios** como o fork genuíno em aberto —
que é OBL-E3 um andar acima. Apliquei cinco revisões marcadas na HYP-ORCH-NOISE, que segue
`candidate`/`exploratory`.

## Contradictions

- validates `vault/hypothesis/orquestracao-anti-ruido.md` — o dispatch `costura-feasibility`
  (`docs/essays/orquestrador-anti-ruido/research/costura-feasibility/findings.md`) retornou
  "real-sob-condições" para as duas costuras (Bregman/dualmente-plano na Kahneman; fibra de
  acoplamento não-mônica na Thaler), evidência que aterrou as 5 revisões aplicadas ao nó.
- questions `OBLIGATIONS.md` (OBL-E3) — o synthesizer nomeou "composicionalidade através da
  composição de estágios" como o fork em aberto sob os desacordos das costuras, que a própria
  sessão identifica como OBL-E3 um andar acima; não descarrega OBL-E3, afia a pergunta contra ele.

## Next steps

1. Rodar o dispatch de feasibility de **composicionalidade** — testar se viés⊕ruído e o re-tipo
   do nudge são functoriais ao longo da composição de estágios/dispatch (a costura OBL-E3), no
   mesmo padrão tensionado construtor⊥colapsador, sob `docs/essays/orquestrador-anti-ruido/research/`.
2. Fechar o gap **MathSciNet** (paywall, único não-verificado) via acesso institucional AMS —
   query de ~2 min — para tornar a alegação de centro-vazio à prova de revisor.
3. Iniciar o rascunho do corpo do paper a partir do esqueleto do README + os dois `findings.md`.

## Recommendation

A pedra angular é o **fork de composicionalidade** (Next step 1). Licença: a validação da
HYP-ORCH-NOISE e o veredito do synthesizer de `costura-feasibility` (dispersão-não-dissenso),
que nomeou a composicionalidade como o único fork em aberto — a aresta `questions OBLIGATIONS.md`
(OBL-E3) acima. Como as duas costuras voltaram apenas "real-sob-condições" e o desacordo restante
é exatamente esse fork, resolvê-lo antes de rascunhar (Next step 3) de-risca a alegação central
do paper. Direção, não desfecho.

## Files touched

- vault/hypothesis/orquestracao-anti-ruido.md
- docs/essays/orquestrador-anti-ruido/README.md
- docs/essays/orquestrador-anti-ruido/research/prior-art-ct-kahneman-thaler/findings.md
- docs/essays/orquestrador-anti-ruido/research/costura-feasibility/findings.md
- telemetry/agents/subagents-dispatch.yaml
