---
tags: [agents-communication-infra, agent-interaction, typed-graph, workflow-relations, research-dispatch]
node_type: research-dispatch-proposal
is_session: false
layer: [architecture, domain, application]
nature: [planning, informational]
status: proposed
veracity: medium
conviction: high
version: 0.2.0
last_updated: 2026-08-17
---

# Typed Interaction Graph Relations — Research Dispatch Proposal

## Decision requested

Approve or decline this research shape. Approval authorizes resolution of the complete governed
dispatch and a separate lifecycle confirmation before launch. Decline means that the sweep must be
simplified, not abandoned.

## Dispatch identity

- `dispatch_id`: `2026-08-17-typed-interaction-graph-basis-research`
- `dispatch_type`: `research`
- `working_folder`: `docs/features/agents-communication-infra/research/interaction-relations/`
- `execution_authority_mode`: `legacy-managed`
- `capability_route`: `research`
- `route_digest`: `sha256:455b246eb9c0da49ee27d42ef6a5ecedd4a9bd7b9046bc6f5ad0ed57183e6767`
- `max_loops`: `1`
- `final_approver`: `Lamport, Leslie`

## One question

Qual é, se existir, a menor base extensível de relações tipadas capaz de reconstruir em grafos os
padrões locais e contemporâneos de interação multiagente, quais tipos são necessários em vez de
meras conveniências nominais, e quais padrões precisam permanecer como subgrafos compostos ou
famílias distintas para preservar dependência, evidência, autoridade, coordenação, término, falha e
efeito executável?

## Research shape

| Group | Agent | Role | Perspective or gate | Token budget |
|---|---|---|---|---:|
| `explorers` | Wirth, Niklaus | `explorer` | Corpus local as-built: reconstruir traços observáveis de `sequential`, review, `zig-zag`, feedback e robot-talks a partir de workflows, código, testes e registros; separar protocolo vivido de sua projeção atual. | 3,000 |
| `explorers` | Milner, Robin | `explorer` | Base gerativa do grafo: buscar relações tipadas e regras de composição capazes de reconstruir os traços locais; testar direção, causalidade, cardinalidade, iteração, término e falha sem presumir que padrões nomeados sejam primitivos. | 3,000 |
| `explorers` | Follett, Mary Parker | `explorer` | Autoridade e evidência: testar, para cada tipo ou composição candidata, quem propõe, entrega, confirma, executa e aceita; impedir que igualdade topológica apague diferenças de autoridade, visibilidade ou prova. | 2,500 |
| `explorers` | Simon, Herbert | `explorer` | Soluções contemporâneas externas e utilidade de produto: comparar implementações atuais em fontes oficiais, registrar versão/maturidade/garantias e mapear o que suas primitivas permitem construir ou deixam para código específico. | 4,000 |
| `synthesizer` | Nonaka, Ikujiro | `writer` | Preservar os retornos, reconciliar somente equivalências sustentadas e escrever `research.md` e `findings.md`. | 5,000 |
| `skeptics` | Parnas, David | `skeptic` | Gate `precedent`: atribuir owner local ou externo a cada estrutura candidata. Owned implica `build-from-owned` ou `already-deployed`, nunca KILL. | 2,200 |
| `skeptics` | Meadows, Donella H. | `skeptic` | Gate `non-vacuity`: exigir um traço observável mínimo para cada invariância ou estrutura. O único KILL possível é `no-witness`. | 2,200 |
| `skeptics` | Dijkstra, Edsger W. | `skeptic` | Gate `definitional-soundness`: impedir colapso entre relação, protocolo, política, coordenação e mecanismo. O único KILL possível é `tautological`. | 2,200 |
| `final-audit` | Lamport, Leslie | `auditor` | Auditor dedicado: verificar rastreabilidade, owners, resolução de findings e a matriz de veredictos sem gerar novas hipóteses. | 1,800 |

Total máximo previsto: 9 agentes e 25,900 tokens.

## Executable topology

```text
explorers --sequential--> synthesizer --sequential--> skeptics --sequential--> final-audit
```

- `robot_talks: false`: os três gates precisam permanecer independentes.
- Não há edge `zig-zag` ou `feedback`: o adaptador `legacy-managed` atual os rejeita.
- Não haverá follow-up informal para simular uma back-edge não registrada.
- Se um skeptic emitir `BLOCK`, o auditor deve rejeitar a aceitação e o dispatch encerra com
  `loop_ceiling_reached`. A correção exigirá um novo dispatch governado, preservando o resultado
  deste run.

Essa topologia é uma concessão operacional, não uma conclusão sobre o domínio pesquisado.

## Source policy

Os explorers começam pelo
[`research-initial-definitions.md`](research-initial-definitions.md). O corpus local deve cobrir
ocorrências executadas ou especificadas de `sequential`, review, `zig-zag`, feedback e robot-talks,
além das superfícies que os representam: `connections`, `ProtocolRecipe`, bindings/follow-ups e
Work Bus. Cada generalização deve distinguir o comportamento observado de sua projeção documental
ou operacional.

A perspectiva de soluções contemporâneas deve cobrir pelo menos cinco sistemas ativamente mantidos
no momento da execução. OpenAI Agents SDK, LangGraph, AutoGen ou Microsoft Agent Framework, Google
ADK e outra implementação comparável formam o ponto de partida, não uma lista fechada. Para cada
sistema, usar documentação, código, especificação ou release oficial vigente; registrar fonte,
versão ou data de acesso, maturidade declarada, primitivas expostas, controle de fluxo, estado,
handoff, loops, durabilidade e garantias executáveis. Material de marketing pode localizar uma
solução, mas não sustenta claim sobre comportamento.

O gate `precedent` verifica e atribui ownership das estruturas que emergirem dos dois corpora. Ele
não deve importar uma taxonomia pronta, tratar popularidade como suficiência nem usar precedente
como KILL.

## Required outputs

### `research.md`

- retornos dos quatro explorers preservados com provenance;
- retornos dos três gates preservados sem reescrita silenciosa;
- resultado do auditor e dissensos restantes.

### `findings.md`

- resposta de uma linha à pergunta do dispatch;
- catálogo de traços observáveis dos padrões locais e seus casos de falha;
- matriz das soluções contemporâneas externas com fonte oficial, versão/data, maturidade,
  primitivas, composição, estado, autoridade, término, recuperação e garantias;
- base candidata de relações tipadas, declarando para cada tipo seus endpoints admissíveis,
  direção, payload/evidência, efeito semântico, autoridade, guarda, término e falha;
- regras de composição do grafo separadas dos tipos de relação, políticas e efeitos do runtime;
- reconstruções de `sequential`, review, `zig-zag`, feedback e robot-talks como grafos tipados;
- teste de necessidade por tipo: o comportamento que deixa de ser representável, ou a diferença
  semântica que é apagada, quando o tipo é removido;
- teste de suficiência por padrão: reconstruído integralmente, reconstruído com extensão explícita
  ou não reconstruível pela base candidata;
- diferenças que precisam permanecer em famílias separadas e padrões que são subgrafos compostos,
  não tipos primitivos;
- crosswalk entre rótulos locais, comportamentos observados e construções externas equivalentes;
- mecanismo de extensão para novos tipos sem fallback silencioso para lógica especial;
- matriz de boundaries e ownership;
- matriz `candidate | owner | witnessed? | sound? | verdict | use-mode`;
- typed negatives, dissensos e implicações para a discovery, sem propor serviço, schema ou runtime.

## Early stop

O dispatch pode parar cedo somente se todos os candidatos forem eliminados por `no-witness` ou
`tautological`. O resultado negativo deve ser preservado e ainda depende da aprovação do auditor.
Encontrar precedente ou não encontrar uma estrutura comum não constitui falha.

## Acceptance

Lamport só pode retornar `APPROVE` quando:

- as quatro superfícies estiverem cobertas ou sua indisponibilidade estiver registrada;
- os cinco padrões locais estiverem reconstruídos como grafos tipados ou possuírem impossibilidade
  explicitamente testemunhada;
- pelo menos cinco soluções externas contemporâneas estiverem verificadas em fontes oficiais com
  versão ou data de acesso e maturidade declarada;
- cada tipo candidato corresponder a uma diferença semântica observável, não apenas a um nome;
- cada tipo candidato possuir testemunho de necessidade, ou ser rebaixado a composição, política,
  efeito de runtime ou alias;
- composição do grafo, relação tipada, política, autoridade e efeito operacional permanecerem
  distintos;
- nenhuma alegação de completude exceder o corpus e existir uma regra explícita de extensão;
- cada claim load-bearing apontar para um retorno e uma fonte verificável;
- os owners arquiteturais permanecerem intactos;
- cada candidato tiver owner, witness, soundness, verdict e use-mode;
- KILL aparecer apenas como `no-witness` ou `tautological`;
- não houver `BLOCK` aberto.

## Risks

- A decisão confirmada de usar grafos pode levar a tratar toda diferença como tipo de aresta; cada
  candidato deve provar que não é apenas topologia, política, estado ou efeito operacional.
- A lente comportamental pode introduzir um formalismo antes da evidência; sua instrução deve
  exigir descrições observáveis antes de qualquer nome teórico.
- O corpus as-built pode transformar limitações da lane `legacy-managed` em propriedades gerais;
  toda generalização deve registrar de qual superfície partiu.
- O sweep externo pode confundir disponibilidade comercial, documentação e adoção real; a pesquisa
  deve afirmar apenas o que fontes primárias sustentam e registrar maturidade explícita.
- A busca por uma base mínima pode favorecer elegância sobre fidelidade; nenhuma redução é aceita se
  apagar autoridade, evidência, término ou falha observáveis.
- A expressão "todos os tipos possíveis" pode induzir uma universalidade não demonstrável; a
  conclusão deve limitar suficiência ao corpus e avaliar separadamente a extensibilidade.
- A ausência de feedback executável torna este primeiro run mais frágil: findings corrigíveis ainda
  causam rejeição e um segundo dispatch, em vez de revisão no mesmo grafo.

## Connections

| Document | Type | Description |
|---|---|---|
| [Research Initial Definitions](research-initial-definitions.md) | `depends-on` | Fornece a pergunta refinável, constraints confirmadas, baseline e gaps sem selecionar método. |
| [Research skill](../../../../../.agents/skills/research/SKILL.md) | `conforms-to` | Define funções epistêmicas, gates, outputs e matriz de veredictos. |
| [Agent pool](../../../../../telemetry/agents/agent-pool.yaml) | `depends-on` | Autoriza os nomes e orienta o fit de papéis. |
