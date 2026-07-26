---
tags: [agents, orchestration, dispatch, architecture, ontology, ledger]
node_type: conceptual
is_session: true
layer: [architecture, domain, ontology]
nature: explanatory
status: active
created: 2026-07-25
timestamp: 2026-07-25T21:59:43-03:00
expires: 2026-09-23
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "A sessão estabeleceu distinções arquiteturais e uma restrição minimalista que orientarão o research, o discovery e os experimentos posteriores, sem ainda ratificar uma solução."
---

# Prompt, tags and graph research scope

## Summary

A sessão começou avaliando o repositório e o ensaio macro-to-micro como base para uma nova explicação de alto nível do sistema de linguagem de agentes. A contribuição conceitual distintiva identificada foi preservar os testes micro→macro de propósito e autoridade e macro→micro de realização e evidência, sem assumir que conexão implica contribuição. Foram desenhadas cinco lentes independentes para futuras versões do texto, mas essas cinco duplas não foram disparadas. Scouts e cadeias independentes de arquitetura e revisão examinaram tags e solicitações configuráveis, convergindo em emissões atribuídas por ativação e rejeitando um campo universal de tags ou decisões automáticas do agente. O trabalho separou prompt versionado, solicitação e trigger, invocação, resultado aceito, asserção de tags e projeções, sem ratificar quantos serviços existirão. O documento de definições iniciais do prompt control plane foi ampliado para cobrir solicitações configuráveis, limites de autoridade, tags, graph-schema, runtime graph e enforcement como questões de research, não como soluções. A conversa introduziu um possível serviço ou capacidade de grafos e distinguiu papéis semânticos de grafo das formas ortogonais como DAG, quiver e property graph, mantendo aberta a necessidade de outros papéis. Os experimentos existentes de grafo estático, publicação no bus e probes de telemetria foram inspecionados como evidência reutilizável, sem implementar uma nova arquitetura. Uma primeira proposta de research foi registrada no ledger, tentou lançar dois explorers e um skeptic e foi fechada com `exit_reason: error`; após verificar que o ledger preserva abertura e fechamento, suas cópias JSON redundantes e a proposta incompatível foram removidas da pasta de research. A direção escolhida passou a ser regenerar o research, depois produzir o discovery e somente então pré-registrar um experimento vertical mínimo; o usuário confirmou que nada deve existir sem propósito, consumidor e consequência verificável e que alternativas sem necessidade devem ser eliminadas.

## Open questions

- Qual é o menor conjunto de capacidades necessário para versionar prompts, configurar solicitações e triggers, aceitar resultados e tornar tags e relações consultáveis?
- Schema graph e runtime graph são os únicos papéis de grafo necessários, ou algum outro papel preserva informação que não pode ser derivada sem perda?
- Qual mecanismo mínimo torna constraints de graph-schema vinculantes sobre mutações runtime e relações executáveis?
- Onde termina o event journal existente e onde começam validação, materialização, inferência e projeção de grafos?
- Como aplicar tags amplamente sem criar campos universais, registros sem consumidor ou taxonomias prematuras?

## Next steps

- Regenerar a proposta de research a partir das definições iniciais atuais, incluindo os eixos de grafos e o teste de necessidade em todos os prompts e contratos de saída.
- Submeter a nova proposta ao workflow de confirmação antes de registrar ou disparar qualquer agente.
- Executar o research e usar seus achados como fonte de um discovery por capacidades e fronteiras de autoridade, sem antecipar a divisão em serviços.
- Pré-registrar somente depois do discovery um experimento vertical mínimo cuja hipótese teste uma única costura ainda incerta.
- Retomar as cinco versões independentes da introdução de alto nível quando os conceitos que elas devem apresentar estiverem suficientemente estabilizados.

## Recommendation

Priorizar a regeneração minimalista do research: cada componente candidato deve declarar propósito, consumidor, consequência de ausência e por que não pode ser omitido, derivado ou atendido por uma capacidade existente.

## Files touched

- `research/prompt-control-plane-foundations/research-initial-definitions.md`
- `research/prompt-control-plane-foundations/proposal-v1.json`
- `research/prompt-control-plane-foundations/dispatch-open-v1.json`
- `research/prompt-control-plane-foundations/dispatch-close-v1-error.json`
- `telemetry/agents/subagents-dispatch.yaml`
- `sessions/2026-07-25-2159-prompt-tags-and-graph-research-scope.md`

## User direction

Tudo deve permanecer mínimo e conectado a uma finalidade real. Nada deve existir solto: serviços, objetos, grafos, relações, propriedades, eventos, índices e artefatos só se justificam quando possuem propósito, consumidor e consequência verificável; a arquitetura deve eliminar o que puder ser omitido, derivado ou atendido por algo que já existe.
