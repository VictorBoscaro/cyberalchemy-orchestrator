---
tags: [orchestrator, dispatch, craft, scout, skill-observability]
artifact_kind: readme
layer: project
version: 0.2.0
created_at: 2026-08-14T17:24:19-03:00
updated_at: 2026-08-15T14:03:57-03:00
---

# CyberAlchemy MVP Proposal

> **Estado: definição inicial.** Este diretório preserva as decisões já confirmadas sobre um
> produto integrado de trabalho com agentes. Ele ainda não contém implementação, arquitetura
> fechada ou plano de MVP. `CyberAlchemy MVP Proposal` nomeia este projeto de proposta; não antecipa
> o nome definitivo do produto resultante.

## Ideia central

O produto oferece um Orchestrator no chat capaz de compreender a intenção do usuário, escolher
capacidades apropriadas e acompanhar trabalho delegado sem executar esse trabalho dentro da própria
janela de conversa.

Por trás do chat, uma infraestrutura determinística governa invocações, Dispatches, contexto,
identidade, lifecycle, evidências e receipts. O Craft preserva o estado durável do projeto.

A experiência pretendida deve manter a conversa útil e coerente enquanto o trabalho especializado
acontece fora da janela principal e retorna somente informação relevante, atribuível e recuperável.

## Decisões confirmadas

### Orchestrator

- O Orchestrator é o agente principal do chat; não existe um segundo “agente do chat” separado.
- Ele conversa com o usuário, interpreta intenção, pede confirmações, escolhe rotas e sintetiza
  retornos.
- Ele pode invocar skills, Superinterviewer, Scouts, conselhos e Dispatches.
- Ele não pesquisa arquivos, modifica código ou realiza tarefas especializadas dentro da própria
  janela. Invocar e acompanhar trabalho é diferente de executá-lo.
- Sua janela de contexto deve ser preservada para informação relevante. O mecanismo de seleção,
  recuperação e descarte de contexto ainda precisa ser definido.

### Coordination Runtime

- A infraestrutura de coordenação é separada do Orchestrator, mas não é outro agente conversacional.
- Ela materializa invocações, aplica escopo e permissões, acompanha lifecycle e registra grafo,
  evidências e receipts.
- Ela deve tornar a execução determinística e reconstruível sem ocupar a janela de contexto do
  Orchestrator com detalhes operacionais.

`Coordination Runtime` também é um nome provisório.

### Superinterviewer

- O Superinterviewer é uma capacidade independente do Orchestrator.
- Pode ser usado diretamente por uma pessoa ou invocado por outro agente, inclusive pelo
  Orchestrator.
- Seu trabalho é esclarecer intenção, formular perguntas, revelar assumptions, contradições e
  tensões, produzir reframings e indicar próximos movimentos.
- O Superinterviewer pode invocar Scouts quando precisa de evidência adicional.
- Sua integração neste produto não remove sua possibilidade de existir e evoluir como produto ou
  serviço independente.

### Scouts

- Scout é a única capacidade de subagente universalmente invocável por outros agentes.
- Um Scout executa uma investigação pequena e delimitada, como localizar um arquivo, inspecionar um
  repositório ou verificar uma afirmação.
- Scout é um nó terminal: não invoca agentes, skills ou outros Scouts.
- O formato de retorno, os limites de ferramentas, a política de mutação, orçamento e concorrência
  ainda precisam ser definidos.

### Dispatches e workers

- Workers especializados existem somente dentro de um Dispatch.
- Nenhum worker especializado é lançado isoladamente pelo Orchestrator ou por outro agente.
- `subagents-strategy` pode decompor o trabalho de qualquer skill e definir os workers, papéis,
  relações e controles necessários para o Dispatch.
- O Dispatch é a fronteira de execução, lifecycle e recomposição do trabalho especializado.
- O Dispatch admite modos de trabalho diferentes. `Research` é um desses modos: organiza uma
  investigação multiagente e retorna evidências e síntese governadas, sem constituir um serviço de
  execução paralelo ao Dispatch.
- O nome de produto para esse modo ainda precisa ser escolhido; `research` permanece como nome
  operacional provisório.
- O encaixe exato entre `subagents-strategy`, Dispatch e o runtime atual será verificado nos
  repositórios antes de se tornar contrato de arquitetura.

### Craft

- Craft é o sistema canônico de estado do projeto; não haverá um `Project State Service` concorrente.
- O estado deve preservar tarefas, decisões, contradições, perguntas, assumptions, evidências,
  próximos movimentos e suas relações.
- O schema atual do Craft precisará ser confrontado com essas necessidades. Tipos ausentes não serão
  disfarçados como tipos existentes apenas para evitar evolução do modelo.
- Um Craft Runtime/Engine operará esse estado automaticamente.
- O Craft Runtime será o único writer. Agentes enviam propostas tipadas e a infraestrutura envia
  receipts; nenhum agente edita o ledger diretamente.
- Fatos técnicos podem ser registrados automaticamente. Interpretações e decisões preservam estado,
  proveniência e confirmação apropriados.
- A relação entre `.craft/ledger.yml`, um possível journal de eventos e projeções derivadas ainda
  precisa ser decidida com base no que já existe.

### Inventory e ledgers

- O **Craft Ledger** preserva o estado governado do projeto: contextos, objetivos, decisões,
  blockers, gaps, definições candidatas, próximos movimentos e links para evidências e artefatos.
- O **Inventory** é uma camada local de conhecimento compilado e consultável. Ele indexa fontes,
  conceitos, decisões, padrões, contradições e evidências para reutilização, mas suas projeções não
  promovem significado nem substituem a autoridade das fontes ou do Craft Ledger.
- O **Dispatch Audit Ledger** registra fatos oficiais de abertura e encerramento dos Dispatches. Ele
  não deve absorver mensagens, tentativas ou todas as transições do runtime.
- Esses três mecanismos têm responsabilidades diferentes. O produto precisa conectá-los por
  identidades, links, proveniência e receipts sem fundi-los numa única store ou permitir autoridade
  concorrente.

## Topologia de invocação atual

```text
Humano
  <-> Orchestrator no chat
        |-> Superinterviewer
        |     `-> Scouts
        |-> Scouts
        |-> Skills sem workers
        |-> Conselhos
        `-> subagents-strategy
              `-> Dispatch
                    |-> Workers especializados
                    `-> receipts
                          `-> Craft Runtime
                                `-> estado do projeto

Outros agentes -> Scouts
Scout          -> ninguém
```

O diagrama registra somente as permissões e fronteiras discutidas até agora. Ele não afirma que
essas ligações já estejam implementadas.

## Skill service e observabilidade

Uma superfície de skills faz parte da hipótese atual do produto. Ela deverá permitir, ao menos:

- descobrir e resolver skills;
- conhecer versões, dependências e proveniência;
- verificar contratos e regras;
- observar invocações, tentativas, retries, duração e outcomes;
- relacionar caller, callee, Dispatch, projeto, outputs e evidências;
- separar métricas operacionais de avaliações de qualidade específicas para cada tarefa.

Ainda não está decidido se essa superfície será um serviço próprio, uma evolução do Skill Control
Center, uma capacidade do Coordination Runtime ou uma composição dessas partes.

## Preservação de contexto

O Orchestrator não deve carregar automaticamente arquivos completos, logs, históricos de tentativas
ou todos os estados do projeto. A hipótese de trabalho é que ele receba projeções pequenas contendo:

- objetivo e decisão atuais;
- tarefas, perguntas e contradições relevantes;
- evidências resumidas com handles recuperáveis;
- estado dos Dispatches que afetam a conversa;
- próximo movimento.

O mecanismo ainda precisa responder como relevância é determinada, quem pode remover contexto, como
resumos são invalidados e como o Orchestrator recupera detalhes sem perder proveniência.

## Próxima investigação

Depois de refinar conceitualmente a jornada mínima, será necessário examinar os repositórios que já
possuem partes desses serviços. A investigação deverá distinguir:

1. o que está implementado e alcançável;
2. o que está apenas testado ou prototipado;
3. o que existe somente como skill, especificação ou decisão;
4. o que pode ser reutilizado sem importar autoridade ou dependências acidentais;
5. o que está ausente ou conflita com as decisões deste documento.

Os primeiros candidatos de inspeção são `cyberalchemy-orchestrator`, `superinterviewer`, `Arcanum`
e `domainspec`. O corpus final ainda precisa ser confirmado.

## Questões abertas

- Qual deve ser o nome definitivo do produto resultante?
- Qual é a menor jornada que demonstra valor real de ponta a ponta?
- O que o Orchestrator pode fazer diretamente além de conversar, rotear e sintetizar?
- Quais ferramentas e efeitos são permitidos a um Scout?
- Como contexto relevante é selecionado, resumido, invalidado e recuperado?
- Quais tipos precisam ser adicionados ao Craft para tarefas, perguntas, assumptions e contradições?
- Como Craft Ledger, Inventory, journal do runtime e Dispatch Audit Ledger se ligam sem duplicar
  autoridade?
- `.craft/ledger.yml` permanece a fonte de verdade operacional ou passa a ser projeção de um journal?
- Quais ações do Craft Runtime são automáticas, propostas ou dependentes de confirmação humana?
- Como skills são empacotadas, versionadas, avaliadas e observadas entre projetos?
- Como um conselho se diferencia de outros perfis de Dispatch?
- Qual nome de produto deve substituir ou enquadrar o modo operacional hoje chamado `research`?
- Quais repositórios e revisões formam o corpus da investigação de estado atual?

## Limites atuais

- Nenhum componente é declarado pronto apenas por aparecer neste documento.
- Este README não transfere autoridade entre projetos ou repositórios.
- Não há decisão de implementação, stack, persistência, UI ou publicação.
- Não há plano de MVP aceito.
- A investigação posterior deve tratar código, testes, receipts e operação observada separadamente de
  especificações e intenção.

## Connections

No real connection was identified in this initial definition.
