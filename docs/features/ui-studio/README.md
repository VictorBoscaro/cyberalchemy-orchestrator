---
feature: ui-studio
title: UI Studio — control plane + harness de UI-fitness
status: draft
created: 2026-07-20
authority: candidate
verification: paired-audit-passed
---

# UI Studio

> **Nota de leitura.** Este README é **navegação, contexto e evidência** — não backlog
> nem ideias soltas (regra do `readme-pattern`). Toda linha das tabelas é **citada**.
> Caminhos sem prefixo são **relativos à raiz do repo** (`cyberalchemy-orchestrator`);
> caminhos com `../` apontam para **repos irmãos** (`../ZefraHub`, `../domainspec`,
> `../domainspec-core`, `../Arcanum`).
>
> **Status de verificação** (coluna `V`): **✅** = verificado de 1ª-mão. As linhas E-1…E-4
> e E-15…E-19 eu li nesta sessão; as linhas E-5…E-14 (antes segunda-mão) foram **confirmadas
> de 1ª-mão pelo dispatch de review pareado** `2026-07-20-ui-studio-readme-verify` — auditores
> de **confirmação e falsificação** sobre o corpus idêntico, ver [verification.md](verification.md).
> As 10 resolvem; as correções de caracterização que a auditoria pediu **já estão aplicadas
> abaixo**. Claim ≤ proof: nenhuma linha aqui é segunda-mão.

---

## 1. What is this?

O **UI Studio** é a feature que junta duas metades sob um mesmo teto: (a) o **control
plane** que organiza, dispara e observa subagentes, e (b) um **harness de UI-fitness** —
a superfície onde um humano **pontua e comenta cada elemento da UI** (nota por-item +
notas por categoria + uma nota geral), para escolher, entre as variantes, qual UI sobrevive.
O harness é a **rota de validação** que a `Promotion Boundary` da constituição de frontend
([vault/constitution/frontend-constitution.md](../../../vault/constitution/frontend-constitution.md),
`CONST-FE`) marcou como `none-yet`.

## 2. Business Context

Este repo é uma máquina de conhecimento cuja primeira peça concreta é um **orquestrador de
agentes** ([PLAN.md](../../../PLAN.md), [README.md](../../../README.md)). A Fase 1 entregou
uma UI linear multinível + endpoints de agregação sobre um ledger append-only
([sessions/2026-07-20-1352-linear-multilevel-ui.md](../../../sessions/2026-07-20-1352-linear-multilevel-ui.md)).
O humano avaliou a UI como **verbosa demais**; a resposta não é apagar informação, é
**tornar a densidade opt-in** e depois **medir** o resultado — daí o harness. Há **três
prior arts** nos repos irmãos que já modelaram exatamente esse problema; o objetivo do
primeiro corte é **reusar, não reinventar**.

## 3. Why it matters

Sem medida, "mais clean" é achismo. O harness converte "achei verbosa" em **delta
mensurável por regra da constituição**, fecha o laço com a camada de decisão do repo (MOGT
/ decision-receipt, [PLAN.md](../../../PLAN.md) §5 E4) e resolve o *next step* herdado de
**escolher 1 das 10 variantes e apagar 9**. Mitiga também o risco concreto observado nos
prior arts (§5): construir o engine evolutivo autônomo **antes** de o loop fechar uma vez —
os três o deferiram ou nunca o dispararam.

## 4. Objetivo & escopo do primeiro corte

**Primeiro corte = só o substrato de medição** (recomendado, evidenciado 3× em §5):

- voto **append-only validado** (não blob mutável) — disciplina do `register-dispatch`;
- **captura por-elemento**: comment + score 1–5, ligado ao elemento por um id estável;
- **agregação** por categoria (regras `CONST-FE`) e **overall** por variante;
- **humano faz a mutação** (decision-receipt). **Engine autônomo fica adiado.**

Fora de escopo no 1º corte: Multi-Armed Bandit / Darwin autônomo; geração automática de
variantes; fleet-telemetry de custo por agente (é a *outra* metade — ver E-13/E-14).

## 5. Evidência — o que temos e onde está

### 5a. Prior arts do harness (voto por-item + categorias + overall)

| ID | Evidência | Localização | V |
|----|-----------|-------------|---|
| E-1 | **Newspaper — schema de voto atômico**: `AtomicVote {generation_id, metric_name, score 1–5, comment}`, 9 métricas canônicas + `global_fitness`, `internal_score = score−3`, 5 handoffs do loop | [../ZefraHub/specs/newspaper/docs/protocol/data-exchange-protocol.md](../../../../ZefraHub/specs/newspaper/docs/protocol/data-exchange-protocol.md) | ✅ |
| E-2 | **Newspaper — arquitetura de 6 agentes** (Orchestrator, Platform Architect, Data/Backend, Darwin-Gödel, UI Evolution, Editor-in-Chief) + mermaid do laço genético | [../ZefraHub/specs/newspaper/docs/architecture/agent_ecosystem_overview.md](../../../../ZefraHub/specs/newspaper/docs/architecture/agent_ecosystem_overview.md) | ✅ |
| E-3 | **Newspaper — missão**: equilíbrio *densidade máxima ⊥ fadiga mínima*; regras imutáveis (hover ubíquo, fecho instantâneo, tooltip universal `#tt`+`data-tip`) | [../ZefraHub/specs/newspaper/agents/ui_evolution/manifesto.md](../../../../ZefraHub/specs/newspaper/agents/ui_evolution/manifesto.md) | ✅ |
| E-4 | **Newspaper — backend de voto**: `POST /api/vote` (`validate_vote` ~L346, `save_vote` ~L377) persistindo em `telemetry_db.json` (**blob mutável — o ponto que melhoramos**) | [../ZefraHub/specs/newspaper/evolution/evolution_server.py](../../../../ZefraHub/specs/newspaper/evolution/evolution_server.py) | ✅ |
| E-5 | **ui-prototyping-studio — data model**: `CommentEvent {target{selector,elementLabel,odId}, severity, intent, note, createdBy/At}`, `AnnotationTarget` (bind por `data-od-id`), `MutationBatch`, `RevisionManifestEntry`, `DiffSummaryHonest` (lineage append-only) | `../domainspec-core/arcanum/projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/domain/models.ts` | ✅ |
| E-6 | **ui-prototyping-studio — loop de fitness**: `CycleCandidate.score` (finito, winner=max, auto-accept top, append 1 revisão), explore/exploit, teto de ciclo | `../domainspec-core/arcanum/projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/run-cycle.ts` | ✅ |
| E-7 | **ui-prototyping-studio — rubrica `critique`**: 5 categorias (Philosophy consistency, **Visual hierarchy**, Detail execution, **Functionality**, Innovation) 0–10 + parágrafo de evidência 30–80 palavras por nota (nota sem evidência é rejeitada) + radar SVG + Keep/Fix/Quick-win | `../domainspec-core/arcanum/projects/ui-prototyping-studio/provenance/open-design-reference/skills-references/open-design/skills/critique/SKILL.md` | ✅ |
| E-8 | **ui-prototyping-studio — captura + rotas**: overlay `annotateClickScript` + `POST /comment` no CLI; rotas REST (`POST …/comments`, `…/mutation-batches/synthesize\|approve\|apply`, `…/handoff/export`) | `../domainspec-core/arcanum/projects/ui-prototyping-studio/backend/src/cli/studio.ts`, `.../interface/http-routes.ts` | ✅ |
| E-9 | **ui-prototyping-studio — frontend React** (a mesma feature com UI): `AnnotationPanel.tsx`, `MutationApprovalPanel.tsx`, `RevisionTimeline.tsx`; taxonomia de erro `AUTO_APPLY_FORBIDDEN` / `APPROVAL_STALE` em `src/lib/api.ts` | `../domainspec/apps/web/src/components/ui-prototyping-studio/`, `../domainspec/apps/web/src/lib/api.ts` | ✅ |
| E-10 | **Newspaper (espelho no domainspec)** — mesma harness (index.html — `<title>` "Genetic Control Center", H1 "Genetic Platform" — + ~19 `gen_*.html` + `evolution_server.py` + `telemetry_db.json` + `generations_manifest.json`) | `../domainspec/implementation/app-frontend/visualizations/newspaper/evolution/` | ✅ |

### 5b. Princípios de governança (o que evita virar "metrics wall")

| ID | Evidência | Localização | V |
|----|-----------|-------------|---|
| E-11 | **hard-gate vs soft-gradient** (subseção *UX-constraint exploit/explore fitness* **[DEFERRED]**, ~L171–200 — **não** o §3, que é o Scope): hard gate descarta (L180); soft gradient *pontua, nunca descarta* (L183); ML2 fitness = heurística + self-critique + objetivo humano (L190); OQ-5 = pesos do soft-score (L200). A "honesty rule" que citei **não é cláusula titulada** — é o **honest-diff mandate** (`DiffSummaryHonest`, counts do before/after real), em §2b/§4/§5. **Reforça a decisão §6.5**: a própria camada de fitness do studio está marcada [DEFERRED]. | `../Arcanum/.../ui-prototyping-studio/SPEC.md` (byte-idêntico ao de `../domainspec-core/...`) | ✅ |
| E-12 | **Sinal action-bearing**: todo sinal roteia para *owner + action + evidence* (L394, L243, L414); "avoid empty dashboards" / "not a global score" (L243, L394). Nomes de superfície são **paráfrase**, não verbatim: "cockpit" humano (Harness Graph + Calibration Queue, L403), "Fleet Telemetry" (L404) | `../domainspec/PRODUCT-COMPONENTS-IDEA.md` | ✅ |

### 5c. Observar os agentes (a outra metade — fleet telemetry)

| ID | Evidência | Localização | V |
|----|-----------|-------------|---|
| E-13 | **agents-telemetry** — `events` SQLite (`ts, session_id, agent_id, event dispatch.start/end, tool, tokens, duration_ms…`) + hook `log.sh` (Pre/PostToolUse) | `../domainspec/internal_tools/agents-telemetry/scripts/schema.sql`, `.../scripts/log.sh` | ✅ |
| E-14 | **Seam "dispatch a partir da UI"** — `openclaw.mjs` spawna processos de agente lendo seats de `router.yaml`, ligado ao `server.mjs` | `../domainspec-core/projects/goldenquill/apps/tilth_ui/src/openclaw.mjs` | ✅ |

### 5d. Base neste repo (onde o harness pluga)

| ID | Evidência | Localização | V |
|----|-----------|-------------|---|
| E-15 | **Constituição de frontend** `CONST-FE` — eixo densidade⊥fadiga; FE-1..FE-8; modos de validação (`deterministic`/`review`/`none-yet`); `Promotion Boundary` que **pede este harness** | [vault/constitution/frontend-constitution.md](../../../vault/constitution/frontend-constitution.md) | ✅ |
| E-16 | **Servidor FastAPI + SSE atual** — endpoints `/api/snapshot`, `/api/overview`, `/api/repo/{name}`, `/api/dispatch/...`, `/api/stream`; **sem `/api/vote` ainda** | [implementations/server/main.py](../../../implementations/server/main.py) | ✅ |
| E-17 | **Ledger append-only + validado** (disciplina a reusar para os votos) | [implementations/server/ledger.py](../../../implementations/server/ledger.py), [telemetry/agents/subagents-dispatch.yaml](../../../telemetry/agents/subagents-dispatch.yaml) | ✅ |
| E-18 | **Store de pendentes** ligado ponta-a-ponta mas sem produtor (só o fixture `_example`) — o gate observa aqui | [telemetry/agents/pending/2026-07-19-exemplo-ui-control-plane.json](../../../telemetry/agents/pending/2026-07-19-exemplo-ui-control-plane.json) | ✅ |
| E-19 | **10 variantes de UI** = as "gerações" candidatas do harness | [implementations/static/ui/](../../../implementations/static/ui/) (`aurora, blueprint, brutalist, cyberpunk, grimoire, linear, mission-control, radar, swiss, terminal`) | ✅ |

## 6. Decisões de design carregadas para cá

1. **O harness É a superfície de validação do `CONST-FE`.** Mapeamento direto (E-11 ≡ E-15):
   `deterministic` (FE-3/5/6) → **hard gate** (Playwright, descarta no fail); `review`
   (FE-1/4/7) → **soft gradient** (humano 1–5 + comment, nunca auto-descarta); `none-yet`
   (eixo densidade⊥fadiga, FE-8) → **resíduo human-objective**.
2. **Append-only sobre blob** (E-17 sobre E-4): voto nunca é editado, é apendado e validado.
3. **Três granularidades** que o humano pediu: `overall (sombra) ⊃ categoria (regra FE) ⊃
   item (comment+score = estrutura)`. Framing CT do repo: `resíduo = sombra ⊕ estrutura` —
   por isso comment *e* nota em cada item.
4. **Sinal action-bearing** (E-12): candidato a **amendment do FE-8** — o overall não pode
   ser número solto; roteia para dono + ação (qual regra, qual correção).
5. **Substrato antes do engine** (E-6/E-11 deferidos + newspaper P0): 3× confirmação de que
   o autônomo não paga primeiro.
6. **Auto-explicação dual, discreta** (`CONST-FE` FE-4/FE-9; raiz filosófica: *form ≡ content,
   radical legibility instead of enigma*, E-3): o **mesmo `data-*-id`** que deixa pontuar um
   elemento deixa ele **se explicar** — score é o julgamento externo, explicação é o relato do
   próprio elemento. Concretização decidida: **explain-mode** (toggle discreto) + **marcador
   quieto** sempre presente; no modo, *dwell* (mouse parado ~3s, **configurável**) revela o
   elemento. "Óbvio/intuitivo" entra como **categoria pontuada** no harness (soft-gradient de
   fricção + checks de a11y), não como boa-intenção.

## 7. Tabela de roteamento — referências por necessidade de build

| Precisamos de… | Referência canônica | ID | Papel na nossa build |
|----------------|---------------------|----|----------------------|
| Schema de voto (nota+comment+overall) | E-1 (newspaper) ⊕ E-5 (studio `CommentEvent`) | E-1, E-5 | **fonte do data model** — merge: bind por-elemento (studio) + score 1–5/comment (newspaper) |
| Categorias + overall + evidência por nota | E-7 (`critique`) | E-7 | forma das categorias; **substituir as 9 métricas de jornal pelas regras `CONST-FE`** |
| Física de captura por-elemento (`data-*-id`, overlay) | E-8 (`annotateClickScript`) ⊕ E-3 (`#tt`/`data-tip`) | E-8, E-3 | widget `#vote` irmão do `#tt`; id estável por elemento |
| Persistência sem perda | E-17 (ledger append-only) **melhorando** E-4 | E-17, E-4 | `telemetry/fitness/votes.ndjson` validado |
| Endpoint de voto/agregação | E-16 (FastAPI atual) | E-16 | `POST /api/vote`, `GET /api/fitness` no mesmo servidor |
| Gate humano antes de mutar | E-9 (`AUTO_APPLY_FORBIDDEN`) ⊕ E-11 (two-gate) | E-9, E-11 | mutação = decision-receipt confirmado |
| Não virar dashboard inerte | E-12 (action-bearing) | E-12 | regra: todo score → owner + action + evidence |
| Critério de sobrevivência das variantes | E-6 (fitness loop) + E-19 (10 variantes) | E-6, E-19 | overall por variante escolhe 1, mata 9 |
| Template visual de dashboard | E-7 vizinho `live-dashboard` | E-7 | referência visual (KPI/sparkline) — não copiar lógica |
| Observar os agentes (2ª metade) | E-13 (SQLite+hook), E-14 (openclaw seam) | E-13, E-14 | fleet telemetry — **fase posterior** |

## 8. Open questions

- **OQ-1** — Pesos do soft-gradient (herdada de E-11/OQ-5): como combinar as notas de
  categoria `review` num overall sem inventar precisão? Candidato: média + variância exposta,
  nunca um único escalar limpo.
- **OQ-2** — O bind por-elemento usa `data-od-id` (studio) ou um id nosso? Depende de
  verificar E-5 de 1ª-mão.
- **OQ-3** — Amendment do FE-8 (action-bearing) entra agora ou depois de 1 ciclo real?

## 9. Next steps

1. **Feito** — verificação de 1ª-mão via dispatch pareado `2026-07-20-ui-studio-readme-verify`; as 10 resolvem, correções aplicadas. Ver [verification.md](verification.md).
2. Destilar o **spec executável** do 1º corte (`vault/spec/ui-fitness-harness.md`) a partir
   desta evidência.
3. Implementar `POST /api/vote` + `votes.ndjson` validado + widget `#vote`.

## 📁 Navigation

- **[README.md](README.md)**: este mapa — objetivo, contexto, evidência citada e roteamento.
- *(planejado)* **`spec.md`**: o spec executável do primeiro corte (após verificação §9.1).
- **[verification.md](verification.md)**: retorno do dispatch pareado — veredicto por-ID (confirmação + falsificação) e as correções aplicadas.
