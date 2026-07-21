---
canonical_kind: review
title: "Review — adições frame/refine/citação à HYP-ORCH-NOISE"
description: "Review tensionado (n=2, eixo fit-interno vs solidez-externa) das edições de 2026-07-20 à hipótese anti-ruído: frame, refine, espinha de citação, OQ-6/7. Um achado ALTO factual (question é do discovery, não research) e um ALTO estrutural (frame precisa de braço de ruído). Todos os consertos aplicados."
evidence_for: [HYP-ORCH-NOISE]
created: 2026-07-20
last_updated: 2026-07-20
tags: [review, frame, refine, citacao, anti-ruido, claim-proof]
---

# Review — adições frame/refine/citação à HYP-ORCH-NOISE

Dispatch `2026-07-20-anti-ruido-frame-refine-review` (review, n=2, `output_mode` persistido).
Eixo de tensão: **fit-interno (consistência + claim≤proof)** vs **solidez-externa (ideias
verdadeiras ou decorativas)**. Os dois revisores discordaram no ponto de carga previsto — se o
frame pertence só ao eixo tensão — o que validou o desenho da tensão.

## Achados (severidade · verdito · conserto)

| # | Sev | Achado | Verdito | Conserto aplicado |
|---|---|---|---|---|
| 1 | **ALTO** | `question` foi citado como campo que "o kind `research` já exige"; na verdade é do kind `discovery` e **opcional**. Pior: ancorava no modelo `discovery` que a OQ-6 rejeita. | confirmado (ambos) | Reescrito como anotação de âncora honesta; removida a exigência falsa; reconciliado com `[[OQ-6]]`. |
| 2 | **ALTO** | Frame posto só no eixo tensão contradiz a ortogonalidade `viés ⊕ ruído` da própria tese; frames independentes dispersam (ruído), não se opõem — a máquina de tensão (`check-tension`) nem se aplica. O doc já tem o tratamento certo em OQ-4 e não o aplicou ao frame. | confirmado (cético); consistência disse "não quebra regra" — conciliável | Frame agora tem **dois braços**: tensão (viés) + dispersão-independente (ruído, à la OQ-4, PENDENTE). Collapse-test ganhou o modo de falha por dispersão. |
| 3 | MÉDIO | `refine` descrito como "operador universal com convergência do zig-zag"; a skill real é esteira fixa de ~10 estágios + budget, e `loop_cap`/`max_loops` são de dispatch, não de artefato solo. Critério do zig-zag fabricado. | confirmado (ambos) | Rebaixado: refine termina por esteira fixa + budget; convergência-solo marcada **PENDENTE**. |
| 4 | MÉDIO | Citação fail-closed cru fabrica viés de disponibilidade/Goodhart (descarta verdade-inancorável; cola chave só pra passar; cobertura VERDE mede conformidade). Falta `supports` vs `mentioned`; colide com ajuste 3. | confirmado (cético) | "Invariante" → "disciplina candidata"; duas salvaguardas: qualidade-do-vínculo (`supports`/`mentioned`) + válvula `reasoning` para verdade-por-raciocínio. |
| 5 | BAIXO | OQ-6 sub-enquadrada como taxonomia; o input-raiz (reconhecimento-de-problema) está sem dono = risco vivo. | confirmado (cético) | OQ-6 ganhou parágrafo "risco vivo: input-raiz não-auditado". |
| 6 | BAIXO | Âncora "codomínio C"/"fio comum" apontava PLAN/MAPPING (não literais lá); vivem em README/FRAMINGS. | confirmado (consistência) | Âncora corrigida para README/FRAMINGS. |

## Passou (sem conserto)

- Frame no eixo tensão **não** quebra a separação gerar→tensão / avaliar→independência (o
  conserto #2 *adiciona* o braço de ruído, não remove o de tensão).
- Espinha de citação **não** conflita com os 5 ajustes do ETE (reforça o ajuste 4).
- Higiene: OQ sem colisão, mermaid válido, frontmatter/tags coerentes, `derives-from` é âncora real.

## Nota de método

Dispatch registrada e fechada no ledger (`telemetry/agents/subagents-dispatch.yaml`) — a
disciplina anti-viés do repo aplicada ao próprio trabalho (auto-aplicação A6). `exit_reason:
resolved` — nenhum dissenso irreconciliável; a discordância dos revisores foi **conciliável**
(frame ganha os dois braços).
