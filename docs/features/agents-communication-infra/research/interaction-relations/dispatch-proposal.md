---
tags: [agents-communication-infra, agent-interaction, workflow-relations, research-dispatch]
node_type: research-dispatch-proposal
is_session: false
layer: [architecture, domain, application]
nature: [planning, informational]
status: proposed
veracity: medium
conviction: high
version: 0.1.0
last_updated: 2026-08-15
---

# Interaction Relations — Research Dispatch Proposal

## Decision requested

Approve or decline this research shape. Approval authorizes resolution of the complete governed
dispatch and a separate lifecycle confirmation before launch. Decline means that the sweep must be
simplified, not abandoned.

## Dispatch identity

- `dispatch_id`: `2026-08-15-interaction-relations-invariants-research`
- `dispatch_type`: `research`
- `working_folder`: `docs/features/agents-communication-infra/research/interaction-relations/`
- `execution_authority_mode`: `legacy-managed`
- `capability_route`: `research`
- `route_digest`: `sha256:455b246eb9c0da49ee27d42ef6a5ecedd4a9bd7b9046bc6f5ad0ed57183e6767`
- `max_loops`: `1`
- `final_approver`: `Lamport, Leslie`

## One question

Nas quatro superfícies observadas — `connections` legadas, `ProtocolRecipe` V1,
bindings/follow-ups `legacy-managed` e contratos do Work Bus — quais características são realmente
invariantes, quais diferenças alteram dependência, evidência, autoridade, coordenação ou efeito
executável, e que estruturas reutilizáveis, se alguma, podem representá-las sem transferir
ownership nem antecipar mecanismo de runtime?

## Research shape

| Group | Agent | Role | Perspective or gate | Token budget |
|---|---|---|---|---:|
| `explorers` | Wirth, Niklaus | `explorer` | Inventário as-built: confrontar schema, specs, código e testes; separar rótulo declarado de comportamento executável. | 2,500 |
| `explorers` | Milner, Robin | `explorer` | Semântica comportamental: construir traços mínimos e comparar direção, causalidade, ordenação, cardinalidade, iteração, término e falha sem impor um formalismo. | 2,500 |
| `explorers` | Follett, Mary Parker | `explorer` | Autoridade e coordenação: mapear quem propõe, confirma, entrega, executa e aceita evidência; detectar transferência indevida de owner. | 2,500 |
| `explorers` | Simon, Herbert | `explorer` | Utilidade de produto: encontrar cenários em que configurar relações muda uma decisão ou resultado e separar diferenças semânticas de aliases históricos. | 2,500 |
| `synthesizer` | Nonaka, Ikujiro | `writer` | Preservar os retornos, reconciliar somente equivalências sustentadas e escrever `research.md` e `findings.md`. | 4,500 |
| `skeptics` | Parnas, David | `skeptic` | Gate `precedent`: atribuir owner local ou externo a cada estrutura candidata. Owned implica `build-from-owned` ou `already-deployed`, nunca KILL. | 2,200 |
| `skeptics` | Meadows, Donella H. | `skeptic` | Gate `non-vacuity`: exigir um traço observável mínimo para cada invariância ou estrutura. O único KILL possível é `no-witness`. | 2,200 |
| `skeptics` | Dijkstra, Edsger W. | `skeptic` | Gate `definitional-soundness`: impedir colapso entre relação, protocolo, política, coordenação e mecanismo. O único KILL possível é `tautological`. | 2,200 |
| `final-audit` | Lamport, Leslie | `auditor` | Auditor dedicado: verificar rastreabilidade, owners, resolução de findings e a matriz de veredictos sem gerar novas hipóteses. | 1,800 |

Total máximo previsto: 9 agentes e 22,900 tokens.

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
[`research-initial-definitions.md`](research-initial-definitions.md) e pelas fontes diretamente
citadas nele. Uma referência local adicional só deve ser seguida quando necessária para verificar
um claim load-bearing, registrando o motivo.

Somente o gate `precedent` amplia a busca para fontes externas primárias, e apenas para atribuir
estruturas que já tenham emergido da evidência. Ele não deve importar uma taxonomia pronta nem usar
precedente como KILL.

## Required outputs

### `research.md`

- retornos dos quatro explorers preservados com provenance;
- retornos dos três gates preservados sem reescrita silenciosa;
- resultado do auditor e dissensos restantes.

### `findings.md`

- resposta de uma linha à pergunta do dispatch;
- matriz comparativa das quatro superfícies;
- entidades relacionadas, direção, causalidade, temporalidade, autoridade, evidência, efeito,
  término/falha e owner por superfície;
- invariâncias testemunhadas e discriminadores semanticamente consequentes;
- estruturas reutilizáveis candidatas sem promovê-las a elementos primitivos;
- diferenças que precisam permanecer em famílias separadas;
- crosswalk entre rótulos atuais e comportamentos observados;
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
- cada invariância tiver testemunho em pelo menos duas superfícies;
- nenhuma diferença específica tiver sido promovida a invariância;
- cada claim load-bearing apontar para um retorno e uma fonte verificável;
- os owners arquiteturais permanecerem intactos;
- cada candidato tiver owner, witness, soundness, verdict e use-mode;
- KILL aparecer apenas como `no-witness` ou `tautological`;
- não houver `BLOCK` aberto.

## Risks

- A lente comportamental pode introduzir um formalismo antes da evidência; sua instrução deve
  exigir descrições observáveis antes de qualquer nome teórico.
- O corpus as-built pode transformar limitações da lane `legacy-managed` em propriedades gerais;
  toda generalização deve registrar de qual superfície partiu.
- A lente de produto pode favorecer exemplos desejados em vez de ocorrências demonstradas; cenários
  prospectivos devem ser separados dos casos já observados.
- A ausência de feedback executável torna este primeiro run mais frágil: findings corrigíveis ainda
  causam rejeição e um segundo dispatch, em vez de revisão no mesmo grafo.

## Connections

| Document | Type | Description |
|---|---|---|
| [Research Initial Definitions](research-initial-definitions.md) | `depends-on` | Fornece a pergunta refinável, constraints confirmadas, baseline e gaps sem selecionar método. |
| [Research skill](../../../../../.agents/skills/research/SKILL.md) | `conforms-to` | Define funções epistêmicas, gates, outputs e matriz de veredictos. |
| [Agent pool](../../../../../telemetry/agents/agent-pool.yaml) | `depends-on` | Autoriza os nomes e orienta o fit de papéis. |
