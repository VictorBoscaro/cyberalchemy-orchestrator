---
tags: [skills, ontology, orchestration]
node_type: discovery
is_session: true
layer: [ontology, architecture]
nature: explanatory
status: active
created: 2026-07-23
timestamp: 2026-07-23T18:03:44-03:00
expires: 2026-09-21
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 5
importance_rationale: "Estabelece a camada de tags de skill (reutilizável pelo futuro compilador) mas ainda inerte — não ratificada, não revisada, gated atrás de uma discovery veracity-low."
---

# skill-protocol-compiler — design + convenção de tags de skill

## Summary

A sessão começou localizando uma ideia registrada: uma skill que decompõe *outra* skill em etapas
quando invocada pela interface do subagents-strategy — identificada como o **skill-protocol-compiler
/ Skill Execution Profile** (hipótese no discovery `agents-communication-protocols`), distinta da
`skill-decomposer` já existente. Com o dono, o design foi afiado: uma skill-casca fina que roteia
para um agente read-only de decomposição, human-in-the-loop (claim ≤ proof, já que decomposição
automática é não provada), produzindo um Skill Execution Profile **cacheado pelo digest de conteúdo
da skill-alvo** (nova versão quando a skill muda). Fixou-se a saída dupla: um **grafo tipado
canônico** (fonte da verdade que o orquestrador consome) mais uma **vista mermaid derivada** (nunca
2ª fonte de verdade — P7/F1). A percepção-âncora: o profile é um `StructuralGraphProposal`
reutilizável e abstrato, ligado por digest a uma revisão da skill. O dono então pediu para coordenar
um orquestrador+reviewer para specar e implementar; ao entrar no contrato de dispatch, dois
bloqueios foram levantados honestamente — `code` dispatch está RESERVED (implementação só inline) e a
discovery do compilador está veracity-low/não-executada (specá-lo agora fura claim ≤ proof). O
trabalho foi partido em **Trilho A** (convenção de tags de skill, construível e independente) e
**Trilho B** (avançar a discovery do compilador antes de specar). Rascunhou-se
`vault/skill-tag-conventions.md` como um sistema de rótulos ortogonais de 4 eixos
(topology/effect/domain/meta), espelhado na ontology-conventions, como alvo de review do Trilho A.
O dono então corrigiu um overreach: o review tinha sido embrulhado em maquinaria de
`dispatch_type`/`meta`, confundindo a *skill sendo desenhada* com as *categorias do ledger de
orquestração* — e mandou fechar a sessão.

## Open questions

- Onde a fronteira "pensar a skill" vira "orquestrar via ledger de dispatch"? Esta sessão cruzou
  cedo demais; falta um sinal claro de quando o design ainda é trabalho inline do parent.

## Next steps

- Revisar `vault/skill-tag-conventions.md` de forma leve (tensão parcimônia ⊥ cobertura: colapsar
  eixos vs. faltam dimensões) — **sem** embrulhar em `dispatch_type`/maquinaria de ledger; settla os
  4 eixos e o formato footer↔sidecar.
- Avançar a discovery do compilador (`agents-communication-protocols`, veracity-low) antes de
  qualquer SPEC do Trilho B.
- Corrigir a aresta `depends-on` do draft: ela aponta para o memory `skill-protocol-compiler-direction`
  (fora do vault) — ou criar um stub in-vault, ou reetiquetar como referência de memória.
- Só depois de a convenção assentar: implementar inline via Arcanum `create-skill`/`sigil-development`
  e backfill das tags nas skills existentes.

## Recommendation

Manter a convenção de tags como a fatia concreta e barata; revisá-la de forma leve (o review já
listado) antes de tocar no compilador. Não specar o compilador enquanto a discovery dele não ganhar
veracity.
Keystone = o review leve da convenção; ele desbloqueia tanto o backfill quanto o consumo pelo
compilador, e nada abaixo dele depende do Trilho B.

## Files touched

- vault/skill-tag-conventions.md

## Extra section — a correção do dono (registrar)

`dispatch_type` **não é** a skill sendo usada. `dispatch_type` é um rótulo do ledger de orquestração
(`research`/`review`/`experiment` LIVE; `code`/`plan`/`suggestion` RESERVED) que classifica um
*fan-out de subagentes*; uma skill é a unidade de instrução que se invoca, e a maioria roda inline
sem virar dispatch. O erro desta sessão foi rotular o review como `dispatch_type: review, meta: true`
— embrulhando a tarefa de *desenhar uma skill* na maquinaria de ledger. Lição a aplicar: desenho de
skill é trabalho inline do parent até haver motivo real de fan-out; não invocar o contrato de
dispatch por reflexo.
