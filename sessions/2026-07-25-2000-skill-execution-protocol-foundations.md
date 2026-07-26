---
tags: [orchestration, agents, dispatch, anti-bias, skills]
node_type: constitution
is_session: true
layer: [architecture, domain]
nature: explanatory
status: active
created: 2026-07-25
timestamp: 2026-07-25T20:00:11-03:00
expires: 2026-09-23
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "A sessão instituiu um novo pré-requisito informacional reutilizável para research e experiment, afetando futuros workflows, embora a infraestrutura de compilação permaneça não ratificada."
---

# Skill Execution Protocol Foundations

## Summary

A sessão começou para esclarecer como uma topologia multiagente declarada pode se tornar execução determinística sobre o bus. A discovery candidata já propõe `skill-protocol-compiler` e `SkillExecutionProfile`, mas registry, binding e compilador ainda não estão ratificados nem implementados. A direção provisória passou a ser um protocolo reutilizável por revisão transitiva da skill, começando pelo significado de negócio e só depois expondo parâmetros e uma execução concreta. A conversa separou cobertura, controle de viés e interação, e questionou a regra workflow-level de tensão pairwise universal sem alterá-la. Um notebook temporário foi criado para registrar decisões e lacunas. Um probe técnico foi criado prematuramente e depois removido integralmente por orientação do usuário, restando somente um README e definições iniciais informacionais. Foi criada a skill `experiment-initial-definitions`, e `research` e `experiment` agora exigem seus respectivos initial definitions antes de desenhar propostas, papéis ou critérios. Nenhum schema, compilador, registry ou integração runtime foi ratificado.

## Open questions

- Qual é a menor representação business-first que preserva o significado da skill e ainda pode gerar uma execução concreta?
- Light, Medium e Hard devem ser presets, perfis ou outra forma de variação?
- Quais mudanças na skill ou em suas dependências tornam um protocolo incompatível?
- Em quais grupos o controle de viés deve exigir cobertura diversa, tensão pareada ou tensão pairwise completa?

## Next steps

- Aplicar `experiment-initial-definitions` a `domainspec-spec-feature` como skill candidata e estabilizar primeiro seu significado de negócio.
- Decidir as variações permitidas somente depois que responsabilidades, resultados e qualidade forem compreensíveis para uma pessoa.
- Pré-registrar o menor experimento de representação apenas depois das definições iniciais, sem antecipar schema ou runtime.
- Harmonizar a regra workflow-level de tensão pairwise somente após uma decisão explícita sobre os modos de controle de viés.

## Recommendation

Como a sessão decidiu que significado de negócio deve preceder parâmetros e mecanismos, priorizar o primeiro Next step: aplicar as definições iniciais a `domainspec-spec-feature` antes de discutir tabelas, hashes ou compilação.

## Files touched

- `.claude/skills/experiment-initial-definitions/SKILL.md`
- `.claude/skills/experiment-initial-definitions/agents/openai.yaml`
- `.claude/skills/experiment/SKILL.md`
- `.claude/skills/research/SKILL.md`
- `.agents/skills/experiment-initial-definitions/SKILL.md`
- `.agents/skills/experiment-initial-definitions/agents/openai.yaml`
- `.agents/skills/experiment/SKILL.md`
- `.agents/skills/research/SKILL.md`
- `docs/features/agents-communication-infra/experiments/skill-protocol-compilation/README.md`
- `docs/features/agents-communication-infra/experiments/skill-protocol-compilation/experiment-initial-definitions.md`
- `docs/temps/agent-dispatch-protocol/README.md`
- `sessions/2026-07-25-2000-skill-execution-protocol-foundations.md`

## User direction

O protocolo deve usar o schema mais simples possível, começar sempre pelo significado de negócio para que uma pessoa entenda e apresentar parâmetros somente depois desse significado estável.
