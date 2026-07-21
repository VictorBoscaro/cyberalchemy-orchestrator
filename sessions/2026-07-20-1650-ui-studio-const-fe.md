---
tags: [frontend, ui, agent-orchestration, control-plane]
node_type: constitution
is_session: true
layer: architecture
nature: procedural, technical
status: active
created: 2026-07-20
timestamp: 2026-07-20T16:50:37-03:00
expires: 2026-09-18
conversation_id: ed535ed1-140e-4ce1-a5cb-c8fc04710b61
decisions_made: true
contradictions_found: true
specs_updated: [vault/constitution/frontend-constitution.md, docs/features/ui-studio/README.md, docs/features/ui-studio/verification.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Produz e emenda a constituição de frontend do repo (CONST-FE) e abre sua Promotion Boundary antes bloqueada com uma base de evidência corroborada 3× e verificada de 1ª-mão, mudando como todo trabalho futuro de UI/scoring deve ser construído aqui."
---

# Constituição de frontend (CONST-FE) + dossiê da feature UI Studio

## Summary

A sessão começou com o usuário achando a UI linear multinível "verbosa demais" e pedindo o
que trazer da frontend-constitution e do newspaper do ZefraHub para deixá-la mais clean e
intuitiva. Reenquadrou-se o problema como **tornar a densidade opt-in** (não remover
informação) e nasceu `vault/constitution/frontend-constitution.md` (CONST-FE) — nativa ao
repo, ancorando o eixo **densidade ⊥ fadiga** no lever próprio `resíduo = sombra ⊕ estrutura`,
com FE-1..FE-8, importando a "física de UI" do newspaper (hover ubíquo, fecho instantâneo,
tooltip universal) como o "item 3" pedido. Separou-se o **fundamental** da mecânica
específica-de-jornal: o tiering exec/tech/graph e a máquina de Gödel ficaram de fora como
instrumento, não princípio. O usuário então pediu a arquitetura de agentes do newspaper, um
sistema de **nota+comentário por-item + categorias + overall**, e um inventário de UI nos
repos irmãos. Um dispatch de pesquisa (3 explorers) achou **três prior arts** — o harness do
newspaper, o ui-prototyping-studio (CommentEvent por-elemento + rubrica critique de 5
categorias + revisão append-only) e o agents-telemetry — e revelou que os três **deferem ou
nunca dispararam** o engine evolutivo autônomo, evidenciando 3× que "substrato de medição
antes do engine" é o caminho. Consolidou-se o insight nativo: o harness **é a superfície de
validação do CONST-FE** (hard-gate/soft-gradient ≡ modos deterministic/review), com score =
sombra e comentário = estrutura. Criou-se o dossiê `docs/features/ui-studio/README.md`
(tabela de evidências citada E-1..E-19 + tabela de roteamento) seguindo a skill readme-pattern,
e um dispatch de review **pareado** (auditores de confirmação vs falsificação sobre o mesmo
corpus) verificou de 1ª-mão as citações reportadas por sweep: as 10 resolvem, E-11 a única
inflada (material de fitness numa subseção [DEFERRED], não no §3; "honesty rule" = honest-diff
mandate), correções aplicadas e `verification.md` escrito. Por fim o usuário elevou
"auto-explicativo + intuitivo/óbvio" a princípio, concretizado como **explain-mode + marcador
quieto + revelação por dwell** (mouse parado, padrão 3s configurável), levando a fortalecer
FE-4 e criar **FE-9**, com o insight de que score e auto-explicação são **duais** sobre o
mesmo `data-*-id`.

## Contradictions

- questions `vault/constitution/frontend-constitution.md` — se a regra "sinal action-bearing"
  (herdada de `../domainspec/PRODUCT-COMPONENTS-IDEA.md`) deve entrar como amendment do FE-8
  agora ou só após um ciclo real de uso do harness; a sessão a nomeou mas não decidiu.
- contradicts `../ZefraHub/docs/vault/constitution/frontend-constitution.md` (P1, "não encodar
  filtro na URL) — CONST-FE registra divergência consciente: esta UI usa `location.hash` para
  deep-link entre níveis de densidade, logado como intencional, não bug.
- validates `docs/features/ui-studio/README.md` — a auditoria pareada
  `2026-07-20-ui-studio-readme-verify` verificou de 1ª-mão todas as citações segunda-mão
  (E-5..E-14); todas resolvem, com E-11 corrigida por caracterização inflada.

## Open questions

- Como combinar as notas de categoria (soft-gradient) num **overall** sem inventar precisão —
  média + variância exposta, ou outra função? A sessão decidiu que o overall existe e é
  action-bearing, mas não a função de agregação (herda o espírito do OQ-5 do SPEC do studio,
  cuja decisão aqui é nossa).

## Next steps

1. Escrever `docs/features/ui-studio/spec.md` — o primeiro corte executável: `POST /api/vote`
   + `telemetry/fitness/votes.ndjson` validado (disciplina register-dispatch) + widget `#vote`
   + **explain-mode** (toggle `?`, marcador quieto, dwell configurável), todos sobre o mesmo
   `data-*-id`. Escopo **substrato-só**; engine autônomo fora.
2. Implementar no FastAPI atual (`implementations/server/main.py`), sem segundo servidor.

## Recommendation

O keystone é o Next step 1 (o `spec.md`). A licença é de 1ª-mão: a auditoria pareada passou
(todas as citações verificadas, E-11 corrigida) e a evidência 3× de que o substrato precede o
engine — o design convergiu e foi checado, só falta especificar. Atacar escopo substrato-só e
**dobrar o explain-mode junto**, porque ele compartilha o mesmo `data-*-id` do voto (score e
auto-explicação são duais) — especificar um sem o outro desperdiça o substrato comum.

## Files touched

- vault/constitution/frontend-constitution.md
- docs/features/ui-studio/README.md
- docs/features/ui-studio/verification.md
- telemetry/agents/subagents-dispatch.yaml
- telemetry/agents/agent-pool.yaml
