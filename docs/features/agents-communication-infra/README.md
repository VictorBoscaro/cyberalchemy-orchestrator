---
feature: agents-communication-infra
title: Infraestrutura de comunicação e deliberação entre agentes
status: draft
authority: candidate
created: 2026-07-21
last_updated: 2026-07-21
---

> Probe executável: [`experiments/bus-publication-probe/`](experiments/bus-publication-probe/) testa
> publicação obrigatória por um bus MCP e validação do receipt pelo agente pai.

# Infraestrutura de comunicação e deliberação entre agentes

> Este documento é uma proposta de arquitetura, não uma descrição de runtime já
> implementado. Ele define fronteiras e invariantes para que o sistema possa evoluir sem
> transformar um agente central em autoridade sobre as conclusões dos demais.

## Plano de implementação

- [`IMPLEMENTATION-LAYERING.md`](IMPLEMENTATION-LAYERING.md) — camadas e decisões que cada corte deve provar;
- [`WORK-PACK.md`](WORK-PACK.md) — plano executável, blockers, tarefas e Smallest Working Units;
- [`EXECUTION-PACK.md`](EXECUTION-PACK.md) — waves, dependências, gates e obrigações de encerramento.

O plano começa bloqueado para código: a Wave W0 precisa resolver os ADRs do Slice 0 e a garantia
de writer único do audit ledger antes da primeira mutação do runtime.

## 1. Objetivo

Construir a infraestrutura canônica para que grupos de agentes deliberem com independência,
troquem resultados entre estágios e registrem conhecimento relevante com proveniência, enquanto o
usuário acompanha a execução em tempo real. O sistema deve executar agentes OpenAI e Anthropic
simultaneamente, inclusive dentro do mesmo grupo, por meio do mesmo protocolo e sem transformar um
modelo central em autoridade intelectual.

O resultado desejado é um runtime capaz de:

- impedir tecnicamente que agentes vejam avaliações dos pares antes da barreira de revelação;
- executar e recuperar workflows sem duplicar mensagens, decisões ou handoffs;
- executar `research`, `review`, `code` e outras ações por recipes versionadas, sem especializar o
  kernel para cada tipo;
- permitir que cada usuário registre rotinas próprias como tipos namespaced, sem editar o kernel;
- mostrar ao usuário progresso e conteúdo autorizado conforme os eventos são persistidos;
- permitir buses lógicos com responsabilidades e schemas configuráveis;
- agregar julgamentos privados de forma reproduzível;
- promover definições, premissas, decisões e outras unidades de contexto para uma memória
  permanente, tipada e rastreável;
- combinar Codex CLI e Claude Code CLI no mesmo run — ou trocar um pelo outro — sem alterar a
  máquina de estados ou os contratos dos buses.

Este documento define a arquitetura-alvo, seus invariantes e os critérios que deverão ser testados. Ele não afirma
que o runtime já existe, não escolhe automaticamente qual conclusão é verdadeira e não exige que
toda a memória contextual seja implementada no primeiro corte.

### 1.1 Escopo das garantias

As palavras **DEVE**, **NÃO DEVE**, **DEVERIA** e **PODE**, em qualquer combinação de maiúsculas e
minúsculas, têm força normativa neste documento.
Trechos marcados como **CANDIDATO** ainda dependem de decisão; itens em **QUESTÃO ABERTA** não são
contrato de implementação.

O runtime pretende garantir isolamento de protocolo, reconstrução de estado e aceitação lógica
idempotente. Ele não promete reproduzir o conteúdo gerado por um modelo, provar que agentes são
estatisticamente independentes nem executar efeitos externos exatamente uma vez. Respostas de
modelos, resultados de ferramentas, relógio e estado de fornecedores são observações
nondeterminísticas: quando afetarem o protocolo, precisam ser registradas como eventos antes de uma
transição depender delas.

No primeiro corte, o sistema é single-host e single-tenant. Isso não elimina a separação entre
principais: agentes, adapters, ferramentas, usuário e kernel continuam sujeitos a identidades e
permissões distintas. Multi-tenancy, workers distribuídos e alta disponibilidade ficam fora do MVP.

## 2. Resumo

A proposta separa seis responsabilidades que hoje aparecem misturadas sob o nome de
“orquestração”:

1. um **kernel coordenador determinístico**, responsável apenas pelo protocolo;
2. uma camada de **adapters de agentes**, independente e heterogênea por fornecedor;
3. um **bus de deliberação por grupo**, onde agentes formam e revisam julgamentos;
4. conexões entre grupos, que encaminham resultados comprometidos para estágios seguintes;
5. uma visão **realtime** para acompanhamento humano;
6. uma **memória rica de negócio e contexto**, permanente, tipada e com proveniência.

O kernel não interpreta qual resposta é “melhor”. Ele controla identidade, fases, barreiras,
visibilidade, deadlines, idempotência e transições. A inteligência permanece nos agentes; a
coordenação permanece verificável em código.

O primeiro runtime pode ser construído sem implementar toda a memória rica. Porém, IDs,
envelopes de eventos e proveniência precisam ser previstos desde o início. Sem isso, adicionar
a memória depois exigiria inferir a origem de afirmações históricas ou migrar mensagens sem uma
identidade estável.

## 3. Estado atual e estado-alvo

### Estado atual

Hoje o repositório possui:

- um ledger append-only com uma linha de abertura e outra de fechamento por dispatch;
- um appender que valida registros novos e é o caminho de escrita pretendido
  ([`append-dispatch.cjs`](../../../.claude/skills/register-dispatch/append-dispatch.cjs));
- `groups` e `connections` tipadas (`sequential`, `zig-zag`, `feedback`) no schema;
- um leitor tolerante a histórico e uma API FastAPI somente leitura
  ([`ledger.py`](../../../implementations/server/ledger.py) e
  [`main.py`](../../../implementations/server/main.py));
- uma UI atualizada por SSE: `/api/stream` verifica mudanças em disco e envia novamente um
  snapshot ([`UI-CONTRACT.md`](../../../implementations/UI-CONTRACT.md));
- um protocolo humano de investigação chamado `robot-talks`, hoje baseado em exploração
  independente, síntese e gate humano
  ([`SKILL.md`](../../../.claude/skills/robot-talks/SKILL.md)).

Isso ainda **não** constitui um runtime de comunicação entre agentes. As `connections` são
instruções de scheduling, não canais; o FastAPI não lança agentes; o SSE não é um event bus;
não há barreira técnica de revelação, entrega durável, retries, recuperação após restart nem
máquina de estados dos grupos. Também não existe um contrato de execução que normalize OpenAI e
Anthropic; a sessão que conduz o trabalho ainda exerce essa integração implicitamente. A hipótese
anterior que investiga esse espaço está em
[`orchestration-infra.md`](../../../vault/hypothesis/orchestration-infra.md).

### Estado-alvo

```text
                         comandos humanos
                               │
                      ┌────────▼────────┐
                      │ control plane   │
                      └────────┬────────┘
                               │
                      ┌────────▼────────┐
                      │ kernel          │
                      │ determinístico │
                      └───┬─────────┬──────────┐
                          │         │          │ comandos/publicações autenticados
                 ┌────────▼──────┐  │   ┌──────▼────────┐
                 │ AgentAdapter  │  │   │ Bus API       │
                 └───┬───────┬───┘  │   └──────┬────────┘
                     │       │      │          │ aceita e persiste
              Codex CLI   Claude CLI│   ┌──────▼────────┐
                     │       │      └──►│ event journal │──► projeção realtime ──► UI
                     └───┬───┘          └──────┬────────┘
                         └── resultados/eventos normalizados
                                            resultado comprometido ──► próximo grupo
                                            registros contextuais ──► knowledge/provenance store
```

O “bus geral” é uma superfície lógica para publicar fatos contextuais relevantes, não uma
conversa global irrestrita que todos os agentes leem automaticamente. A visibilidade desses
registros continua sendo concedida por snapshots e políticas explícitas.

### Da skill atual às entradas do runtime

Hoje a capacidade começa em `domainspec-subagents-strategy`: a skill interpreta o pedido, propõe
grupos e conexões, conduz o gate humano e depende da sessão ativa para registrar, lançar, coordenar e
fechar os agentes. Isso a torna simultaneamente interface, planejador e executor.

No estado-alvo, a **capacidade pertence ao runtime**, não à skill. Todas as superfícies produzem o
mesmo `DispatchSpec` canônico e enviam comandos ao mesmo serviço:

```text
skill Claude ────────┐
skill/plugin Codex ──┤
UI ──────────────────┼──► command API/MCP ──► draft ──► validate ──► confirm ──► kernel
CLI/SDK ─────────────┤                                      │
integração externa ──┘                                      └──► run_id + realtime
```

A skill continua útil como experiência conversacional: extrai objetivo e contexto, propõe a
decomposição, explica tensões e pede confirmação. Depois chama ferramentas como:

- `dispatch.create_draft`;
- `dispatch.validate`;
- `dispatch.confirm`;
- `run.get` / `run.watch`;
- `run.cancel`.

Ela não escreve diretamente no ledger, não inicia processos de agentes e não decide que um estágio
terminou. Essas responsabilidades passam ao kernel e ao único write path canônico. O mesmo vale para
uma futura skill/plugin do Codex: muda a interface de autoria, não a semântica do dispatch.

O `DispatchSpec` é a fronteira estável entre intenção e execução. Ele carrega objetivo, contexto,
grupos, agentes, providers/adapters/modelos, conexões, políticas de consenso, budgets, ferramentas e
gates. Drafts podem ser editáveis; após `confirm`, a versão confirmada é imutável e recebe um
`run_id`. Alterações posteriores criam nova versão ou comando explícito, nunca uma edição silenciosa
do spec em execução.

Isso permite migração gradual: a skill existente primeiro troca seu appender direto pela command
API; depois UI e outros clientes passam a criar o mesmo spec. Enquanto o runtime não existir, ela
continua sendo o caminho operacional legado, claramente marcado como tal.

### Tipos de dispatch e recipes de execução

`dispatch` é o envelope universal de uma execução; não é um único comportamento. A ação desejada é
expressa em duas camadas:

- `dispatch_type`: identificador semântico aberto, namespaced e versionado; `research`, `review`,
  `code`, `experiment`, `plan` e `suggestion` formam apenas o catálogo inicial, não um enum final;
- `recipe_ref`: protocolo executável e versionado que implementa um modo daquela categoria, como
  `research/evidence-synthesis@1` ou `review/adversarial@2`.

Isso descreve o estado-alvo. O appender atual ainda valida um enum fechado no schema `0.6.1`; migrar
do enum embutido para um registry governado é parte do novo runtime, sem reinterpretar registros
históricos.

Um tipo pode possuir várias recipes. Uma research bibliográfica e uma investigação de arquitetura
compartilham a natureza `research`, mas podem usar grafos, ferramentas e critérios de saída
diferentes. O kernel não contém branches como `if research` ou `if code`: ele carrega a recipe,
valida seus parâmetros e compila o grafo em um `DispatchSpec` executável.

Uma recipe declara:

- objetivo e contrato do artefato final;
- parâmetros que a skill, UI ou usuário precisa preencher;
- estágios, dependências e papéis dos agentes;
- buses e tipos de mensagem usados em cada estágio;
- templates de instrução e schemas de saída por papel;
- ferramentas, sandbox e permissões de escrita;
- política de independência, reveal, quorum, consenso e dissenso;
- budgets, retries, deadlines e limites de rodada;
- verificações, gates humanos e regra de aprovação final;
- política de artefatos, conhecimento contextual e `exit_reason`.

O comportamento de um agente não deve existir apenas como prosa escondida em um prompt. Cada papel
possui um contrato: entradas visíveis, objetivo local, schema de saída, ferramentas permitidas,
capacidade de escrita e condição de término. O prompt materializa esse contrato para o provider; o
runtime continua capaz de validá-lo sem interpretar livremente a resposta.

| Tipo | Exemplo de recipe | Comportamento característico |
|---|---|---|
| `research` | `research/evidence-synthesis@1` | Exploração independente, síntese, auditoria de evidência, tags agregadas e artefato de research. |
| `review` | `review/adversarial@1` | Revisores read-only por lentes distintas, normalização/deduplicação de findings, severidade e veredito. |
| `code` | `code/plan-implement-review@1` | Planejamento, escrita isolada, testes, revisão e um único materializador/merge authority. |
| `experiment` | `experiment/falsification@1` | Pré-registro, execução, coleta de evidência, adjudicação contra critério e reprodutibilidade. |
| `plan` | `plan/dependency-roadmap@1` | Planos concorrentes, síntese por dependências, crítica de viabilidade e aprovação. |

Recipes são pacotes instalados, versionados e validados, não código arbitrário fornecido por um
agente durante o run. O usuário pode sobrescrever parâmetros permitidos — número de agentes,
providers, budgets ou gates — mas não remover invariantes de segurança ou proveniência. A versão e
os overrides efetivos ficam congelados no `DispatchSpec` confirmado.

O fluxo de entrada passa a ser:

```text
intenção → dispatch_type → recipe_ref → parâmetros/overrides
        → DispatchSpec compilado → validate → confirm → run
```

As skills específicas de `research`, `review` ou `experiment` podem continuar como assistentes de
autoria das respectivas recipes. Elas deixam de possuir uma implementação paralela do runtime. Um
novo tipo só se torna LIVE quando sua recipe, schemas, permissões e testes de contrato estiverem
instalados; até lá permanece reservado.

### Tipos personalizados e o núcleo comum

Usuários e organizações podem registrar tipos próprios, inclusive uma rotina específica que não
caiba nas categorias iniciais:

```yaml
type_id: user.victor/monthly-knowledge-routine
version: 1
owner: user:victor
scope: user
traits: [reads-repository, produces-artifact, proposes-knowledge]
default_recipe_ref: user.victor/monthly-knowledge-routine@1
input_schema_ref: schema:user.victor/monthly-routine-input@1
output_schema_ref: schema:user.victor/monthly-routine-result@1
```

Namespaces evitam colisão entre um tipo pessoal, um tipo da organização e um tipo distribuído pelo
sistema. O registry possui escopos explícitos (`system`, `organization`, `workspace`, `user`), e a
resolução grava o identificador e a versão completos no `DispatchSpec`; precedência implícita não
pode trocar uma recipe silenciosamente.

O que todos os tipos têm em comum não é a finalidade de negócio. É o **contrato operacional mínimo**:

1. identidade, owner, versão e schema de configuração;
2. entrada e resultado final tipados;
3. recipe compilável para um grafo finito de grupos/estágios e conexões conhecidas;
4. papéis com inputs visíveis, output schema, ferramentas e permissões;
5. mensagens pelo envelope canônico, com IDs, ordem, causação e proveniência;
6. loops, retries, budgets e deadlines limitados ou governados explicitamente;
7. condições observáveis de conclusão e mapeamento para o `exit_reason` comum;
8. regras de idempotência, cancelamento, recuperação e commit único;
9. política de visibilidade, retenção, artifacts e conhecimento contextual;
10. capabilities de adapter necessárias, validadas antes do run.

O kernel precisa entender somente esse núcleo. Semântica específica — “fazer revisão mensal dos
projetos, atualizar tags e produzir um relatório executivo”, por exemplo — vive nos schemas,
estágios e contratos da recipe do usuário.

`traits` opcionais descrevem capacidades transversais, como `writes-repository`,
`requires-human-gate` ou `produces-artifact`. Eles ajudam UI, busca, políticas e analytics, mas não
substituem a recipe nem fazem o kernel interpretar o nome do tipo.

Customização começa declarativa: composição de estágios, schemas, prompts, policies e ferramentas
já instaladas. Código executável arbitrário não entra numa recipe não confiável. Quando um tipo
precisar de um novo tool ou hook executável, isso é instalado separadamente como extensão confiável,
com permissões e versão próprias; a recipe apenas declara a dependência.

Existe um limite deliberado. Uma rotina que não possa declarar fronteiras, estado observável,
condição de término, proveniência ou limites de interação não é automaticamente um novo
`dispatch_type`. Pode ser um serviço contínuo externo ou pode exigir ampliar explicitamente o
contrato comum. Forçar qualquer processo dentro do dispatch transformaria a generalidade em ausência
de garantias.

A extensibilidade, portanto, tem três anéis:

```text
núcleo fechado       estados, eventos, segurança, idempotência e proveniência
extensões confiáveis novos tools, materializers e tipos de estágio instalados
registry aberto      tipos e recipes declarativas de sistema, organização, workspace ou usuário
```

O anel externo é fácil de configurar porque não pode enfraquecer os invariantes do núcleo. Quando
uma necessidade ultrapassa as primitivas existentes, ela sobe para o anel de extensão confiável em
vez de injetar comportamento arbitrário no kernel.

## 4. Kernel coordenador determinístico

O kernel substitui um “superagente orquestrador” como autoridade intelectual. Suas decisões
devem ser reproduzíveis a partir do estado persistido e da configuração do protocolo.

Responsabilidades do kernel:

- criar identidades de run, grupo, agente, mensagem, rodada e tentativa;
- entregar a cada agente um snapshot de entrada identificável e congelado;
- controlar quais tipos de mensagem podem ser publicados em cada fase;
- impedir a leitura das posições dos pares antes da barreira de revelação;
- detectar quorum, deadline e limite de rodadas;
- aplicar regras declaradas de consenso, dissenso e encerramento;
- aceitar e publicar logicamente uma única versão do resultado por grupo/conexão, mesmo sob
  reentrega física;
- aplicar retry, cancelamento e recuperação sem duplicar efeitos lógicos aceitos;
- emitir eventos de transição para auditoria e para a experiência realtime.

Não são responsabilidades do kernel:

- redigir a síntese sem que o protocolo atribua esse papel a um agente;
- escolher silenciosamente qual argumento é verdadeiro;
- alterar a posição inicial de um agente;
- esconder dissenso para produzir uma saída aparentemente consensual;
- usar o conteúdo semântico da resposta como condição implícita de scheduling.

### 4.1 Identidades e unidade de idempotência

Identidade lógica e identidade de execução não são intercambiáveis:

| Identidade | Duração e finalidade |
|---|---|
| `dispatch_id` | pedido confirmado e sua trilha de auditoria de alto nível |
| `run_id` | execução de uma versão imutável do `DispatchSpec` |
| `group_id` / `group_version` | agregado de protocolo e sua revisão imutável |
| `seat_id` | vaga lógica que participa de quorum e possui no máximo uma contribuição aceita por rodada/tipo |
| `agent_instance_id` | agente/modelo/profile escolhido para ocupar uma vaga |
| `operation_id` | contribuição lógica esperada, estável através de retries |
| `attempt_id` | uma execução física de uma operação; retry sempre cria nova tentativa |
| `round_id` | rodada identificada; não deve ser inferida apenas de um inteiro local |
| `command_id` | pedido idempotente de mudança ou efeito |
| `event_id` | fato imutável aceito pelo journal |
| `message_id` | identidade de uma mensagem aceita; referencia conteúdo e eventos que a aceitaram |
| `artifact_id` | conteúdo imutável ou versão content-addressed referenciada pelo protocolo |

Substituição cria nova `agent_instance_id`; a policy registra explicitamente se ela herda a mesma
`seat_id`. Retry mantém `operation_id` e cria nova `attempt_id`. Unicidade lógica é aplicada sobre
chaves como `(aggregate_id, seat_id, round_id, message_type)`, não sobre a tentativa física.

### 4.2 Comandos, eventos e efeitos

O runtime DEVE separar pedidos de fatos e de trabalho externo:

```text
command
   │ valida identidade, policy e expected aggregate_version
   ▼
evento aceito + effect_requested/outbox (mesma transação local)
   │
   ├──► reducer avança o estado
   └──► worker executa efeito pelo menos uma vez
                 │
                 └──► effect_succeeded | effect_failed | effect_unknown
```

- comandos podem ser rejeitados e são deduplicados por `command_id`/`idempotency_key`;
- eventos são fatos e nunca são reexecutados durante replay;
- efeitos retryable de provider ou ferramenta são entregues **at-least-once**, salvo contrato mais
  forte; efeito `non_retryable` pode terminar `effect_unknown` para não arriscar repetição;
- mensagens, votos, commits e handoffs têm aceitação lógica única por constraint no journal;
- ferramenta mutável precisa declarar idempotency key, compensação ou política `non_retryable`;
- timeout, cancelamento, troca de agente, mudança de quorum e decisão humana viram eventos aceitos;
  o reducer nunca redescobre essas decisões consultando o relógio ou o provider durante replay.

Mesmo no MVP single-host, append usa compare-and-set sobre `aggregate_version`. Comandos
concorrentes que observaram versão antiga falham com conflito e precisam reler o agregado. Deadline,
cancelamento, conclusão e quorum podem competir; vence a primeira transição válida na ordem do
journal, e observações tardias são preservadas como ignoradas, nunca apagadas.

Ownership de execução no MVP usa claim durável single-host: o worker adquire por CAS
`(operation_id, attempt_id, worker_epoch)` na mesma outbox antes de `start`; epoch antigo não pode
aceitar completion nem renovar claim. Não há lease temporal/multi-host no MVP. Leases distribuídos,
failover e fencing entre hosts permanecem Fase 4.

### 4.3 Máquina de estados mínima

As recipes podem compor grupos e conexões, mas todo grupo do núcleo instancia a mesma máquina de
estados. Novos tipos de máquina exigem extensão confiável versionada; uma recipe declarativa não
injeta estados ou transições arbitrários.

| Estado | Comando/fato | Guarda principal | Evento | Próximo estado |
|---|---|---|---|---|
| `pending` | iniciar grupo | dependências comprometidas e spec válido | `group.started` | `collecting` |
| `collecting` | submeter posição | principal/seat/round válidos; contribuição ainda ausente | `position.accepted` | `collecting` |
| `collecting` | fechar coleta | conjunto elegível congelado e quorum ou `deadline.fired` registrado | `collection.closed` | `revealing` |
| `revealing` | publicar manifest | hash do conjunto congelado persistido | `reveal.published` | `deliberating` ou `voting` |
| `deliberating` | fechar rodada | limite/critério observável satisfeito | `round.closed` | `deliberating` ou `voting` |
| `voting` | aceitar voto | uma contribuição por seat/round e schema válido | `vote.accepted` | `voting` |
| `voting` | aplicar regra | quorum e regra versionada satisfeitos | `verdict.computed` | `committing` |
| `committing` | comprometer resultado | `result_payload_ref` tipado e verdict persistido | `group.committed` | `completed` |
| qualquer não terminal | solicitar cancelamento | comando autorizado e versão atual | `cancellation.requested` | `cancelling` |
| `cancelling` | confirmar término | tentativas encerradas ou deadline de cancelamento | `group.cancelled` | `cancelled` |
| qualquer não terminal | falha irrecuperável | retries/policy esgotados | `group.failed` | `failed` |

Outputs inválidos não avançam a máquina. A policy decide entre rejeitar, reparar com nova tentativa,
registrar abstention ou falhar; cada escolha é evento explícito. Estados `completed`, `cancelled` e
`failed` são terminais. Pausa/gate humano, replacement e timeout detalhados permanecem extensões da
mesma tabela e precisam ser resolvidos antes do Slice 1.

O kernel constrói o envelope protocolar de `group_result`: regra aplicada, verdict, participantes,
quorum, dissensos e referências. A narrativa ou síntese semântica é um artefato imutável produzido
por papel declarado e citado pelo envelope quando a recipe a exigir; o kernel não a redige. No
Slice 0, `result_payload_ref` pode apontar para envelope determinístico que referencia posições e
verdict, sem papel de síntese. Replay reutiliza o payload e nunca chama novamente o agente para
reinterpretá-lo.

Eventos observados não geram novos eventos por magia durante replay. Um policy reactor lê o fato
aceito, envia command com `causation_id` e `expected aggregate_version`, e a transição só existe se o
conditional append vencer. Reducers permanecem puros.

### 4.4 Contrato de adapters independente de fornecedor

O runtime deve operar, no mínimo, com modelos da OpenAI e da Anthropic, ao mesmo tempo. O kernel não chama SDKs,
CLIs ou APIs de fornecedor diretamente; ele conversa com um contrato `AgentAdapter`. Implementações
iniciais candidatas são `codex-cli` e `claude-code-cli`, com adapters de API podendo ser adicionados
sem alterar o protocolo de grupos.

Fornecedor, adapter e modelo são escolhidos por **instância de agente**, não por run ou por grupo.
Um único grupo pode conter dois agentes Codex e dois Claude, todos recebendo o mesmo snapshot e
publicando no mesmo canal lógico. Essa heterogeneidade é uma fonte potencial de diversidade, mas não
prova independência: modelos diferentes ainda podem compartilhar dados, vieses ou padrões de
raciocínio. O protocolo mede o desacordo observado sem presumir independência estatística.

O contrato normaliza cinco operações:

- `start(operation_id, attempt_id, request_digest)`: inicia de forma idempotente uma tentativa com
  prompt, snapshot, modelo, ferramentas, sandbox e deadline;
- `events(attempt_id, after_cursor)`: entrega eventos incrementais identificados e deduplicáveis;
- `result(attempt_id)`: devolve o resultado terminal estruturado;
- `cancel(attempt_id, command_id)`: solicita cancelamento idempotente;
- `status(attempt_id)`: reconcilia estado depois de restart ou outcome local desconhecido.

`cancel_requested`, `cancel_acknowledged` e o estado terminal são fatos distintos. Resultado recebido
depois de timeout/cancelamento permanece observável, mas só altera o protocolo se a máquina ainda
aceitar essa transição. Um resultado terminal válido é único por tentativa; output parcial ou
schema-invalid segue a policy explícita de retry, repair, abstention ou failure.

Repetir `start` com a mesma `attempt_id` e o mesmo `request_digest` reconcilia/devolve a tentativa
existente. A mesma identidade com digest diferente é conflito permanente e evento de segurança.

| Estado da tentativa | Observação/comando | Evento/resultado |
|---|---|---|
| `requested` | worker adquire claim CAS com `worker_epoch` válido | `attempt.starting` |
| `starting` | provider confirma identidade ou status | `attempt.running` |
| `starting/running` | output terminal válido | `attempt.completed` e candidato único a resultado da operation |
| `starting/running` | falha conhecida | `attempt.failed`; policy pode criar nova attempt sob a mesma operation |
| `starting/running` | outcome não reconciliável | `attempt.unknown`; policy não repete efeito `non_retryable` |
| não terminal | cancel command | `attempt.cancel_requested`, depois ack/terminal quando observável |

Late result permanece ligado à attempt original. Somente um resultado por `operation_id` pode ser
aceito como contribuição lógica; os demais são registrados como superseded/ignored conforme a
ordem e a policy.

Cada adapter declara capacidades como `streaming`, `resume`, `structured_output`, `mcp_tools` e
`usage_reporting`. O scheduler consulta essas capacidades em vez de presumir que todos os
fornecedores suportam exatamente os mesmos recursos. Uma capability ausente provoca fallback
explícito ou torna a combinação inválida antes do dispatch; nunca muda silenciosamente a semântica
do protocolo.

Capabilities são classificadas como: **obrigatórias**, **emuláveis sem mudança semântica** ou
**semantics-changing**. A última classe invalida a combinação, salvo se uma nova versão do spec for
confirmada. O digest do adapter, modelo efetivo, recipe, schemas, prompt, snapshot e resolução de
capabilities fica congelado no `DispatchSpec`; um nome/version string sem digest não basta para
replay auditável.

O envelope canônico preserva campos comuns (`provider`, `model`, `provider_run_id`, timestamps,
status e uso reportado) e permite `provider_metadata` namespaced para detalhes não portáveis. Tokens
serão consumidos normalmente; a preocupação é medi-los sem forçar falsa equivalência. Contagens como
input, output, cache e reasoning ficam opcionais quando o fornecedor não as reporta ou usa outra
semântica — ausência vira `null`, não zero inventado.

Autenticação pertence à configuração de execução gerida pelo credential broker, nunca a configuração
controlada pelo adapter, prompt, journal ou ledger. Segredos duráveis permanecem dentro do broker; o
adapter recebe apenas capability/credencial mínima provider-scoped definida por OQ-CREDENTIALS. O
contrato-alvo exige credencial curta tanto para CLI quanto para API. Reuso de profile/sessão do host
só pode existir como modo local de
desenvolvimento explicitamente não conforme e fora das garantias de sealing/isolation. Os agentes
recebem as mesmas ferramentas do bus por uma interface MCP ou equivalente, e nenhum agente escreve
diretamente no armazenamento.

Um request canônico não carrega flags específicas de CLI:

```jsonc
{
  "attempt_id": "...",
  "provider": "openai",
  "adapter": "codex-cli",
  "model": "...",
  "prompt_ref": "artifact:...",
  "input_snapshot_id": "...",
  "response_schema_ref": "schema:group-position@1",
  "tool_profile": "group-participant",
  "deadline": "..."
}
```

O adapter traduz esse contrato para seu fornecedor e emite estados comuns como `queued`,
`running`, `waiting_tool`, `completed`, `failed` e `cancelled`. Eventos nativos permanecem anexos
para diagnóstico, mas a máquina de estados e a UI dependem somente dos estados canônicos.

O scheduler mantém concorrência, rate limits, credenciais e circuit breakers separados por adapter.
A indisponibilidade de um fornecedor não deve corromper o outro: a política do grupo decide se espera,
faz retry, substitui a instância, reduz quorum ou encerra com resultado incompleto. A substituição fica
registrada e nunca se apresenta como se o agente originalmente planejado tivesse respondido.

## 5. Bus de deliberação por grupo

Cada grupo possui um canal lógico isolado. “Bus” aqui significa uma interface de publicação,
leitura e assinatura governada pelo estado do grupo; não implica Kafka, Redis ou outro produto.
No MVP, ele pode ser implementado sobre persistência local e polling transacional.

### 5.1 Fases

#### `collect`

Todos os agentes recebem o mesmo snapshot-base, salvo diferenças deliberadas e registradas de
papel ou ângulo. Cada agente publica uma `position` imutável. Posições já recebidas ficam seladas
para os pares.

#### `reveal`

Quando todos os agentes elegíveis responderem, ou quando a política de deadline/quorum for
acionada, o kernel fecha a coleta e revela o conjunto congelado de posições. A mudança de fase é
um evento explícito; não decorre apenas de uma convenção no prompt.

#### `deliberate`

Os agentes publicam críticas, respostas e propostas de síntese referenciando mensagens
anteriores por ID. O número de rodadas é limitado. Cada rodada preserva o que mudou e por quê,
em vez de sobrescrever a posição inicial.

#### `vote`

Cada participante autorizado publica um veredito imutável. Quando a independência do voto for
importante, uma recipe futura pode aplicar barreira equivalente à de posições. Voto selado fica fora
dos primeiros slices até seu manifest, capability transition e testes serem definidos. A regra de
decisão é parte da configuração do grupo, não uma interpretação posterior.

#### `commit`

O kernel aplica a regra declarada e publica um `group_result`. O resultado deve distinguir
`consensus`, `qualified_consensus` e `dissent`; deve carregar referências para evidências,
posições, votos, objeções não resolvidas e a regra de encerramento usada.

Um consenso entre modelos é uma decisão do protocolo, não uma garantia de verdade. O sistema
deve permitir que `dissent` seja uma saída válida.

### 5.2 Envelope comum

Eventos e mensagens devem compartilhar um envelope mínimo desde o MVP:

```jsonc
{
  "event_id": "uuid",
  "event_type": "position.accepted",
  "schema_ref": "schema:group-position@1",
  "schema_digest": "sha256:...",
  "aggregate_type": "group",
  "aggregate_id": "...",
  "aggregate_version": 17,
  "journal_offset": 1042,
  "recorded_at": "...",
  "observed_at": "...",
  "run_id": "...",
  "dispatch_id": "...",
  "group_id": "...",
  "group_version": 1,
  "seat_id": "...",
  "agent_instance_id": "...",
  "operation_id": "...",
  "attempt_id": "...",
  "round_id": "...",
  "message_id": "...",
  "reply_to_message_ids": ["..."],
  "actor_principal_id": "...",
  "command_id": "...",
  "idempotency_key": "...",
  "causation_id": "...",
  "correlation_id": "...",
  "policy_version": "...",
  "input_snapshot_id": "...",
  "payload_ref": "artifact:...",
  "payload_hash": "sha256:..."
}
```

Nem todo campo será aplicável a todo evento, mas os identificadores centrais não devem ser
deduzidos de nomes humanos. `agent_name` é uma persona; não é identidade de execução.

`aggregate_version` é contígua por agregado e alocada pelo journal writer mediante conditional
append. `journal_offset` ordena replay dentro de um stream declarado. `observed_at` pode vir de um
provider; apenas `recorded_at` e a posição do journal governam transições. Campos de autoridade como
run, group, seat, attempt e actor são derivados da sessão/capability autenticada, não confiados ao
payload enviado pelo agente.

`group_version` identifica a revisão imutável do protocolo; `aggregate_version` é somente a versão
CAS/event-stream daquela revisão. `aggregate_id` identifica `(run_id, group_id, group_version)`.
Mensagem e evento são objetos distintos: `message_id` identifica a publicação lógica e `event_id`
identifica o fato de sua aceitação, rejeição ou entrega. Referências discursivas usam `message_id`.

### 5.3 Registros privados de julgamento e agregação

Esta subseção descreve arquitetura-alvo pós-MVP; não é requisito de conformidade dos Slices 0–4.

Além de posições longas, os agentes tomam pequenas decisões estruturadas: quais tags descrevem
uma research, quais tags caracterizam um agente, qual classificação atribuir a um artefato ou qual
nível de confiança registrar. Essas decisões devem ser tratadas como **julgamentos individuais
selados**, não como edições diretas no documento final.

Cada dimensão de julgamento declara um contrato versionado: o objeto avaliado, o vocabulário
permitido, o schema da resposta, quem participa, quando ocorre a revelação e qual regra de agregação
será aplicada. Um agente publica em sua caixa lógica privada:

```jsonc
{
  "judgment_id": "uuid",
  "judgment_type": "research_tags",
  "subject_ref": "research:agent-events-infra-hypothesis",
  "agent_instance_id": "...",
  "input_snapshot_id": "...",
  "values": [
    { "tag": "orchestration", "confidence": 0.91 },
    { "tag": "event-bus", "confidence": 0.74 }
  ],
  "rationale": "...",
  "evidence_refs": ["..."],
  "schema_version": "..."
}
```

Durante a coleta, cada agente acessa apenas seus próprios julgamentos; os demais recebem no máximo
o progresso agregado, como “3 de 4 enviados”, **quando a policy permitir essa metadata**. Depois que
todos enviarem, expirarem ou abstiverem,
o kernel sela a rodada e concede ao papel `aggregator` acesso somente-leitura ao conjunto completo.
O agregador não pode alterar avaliações individuais. Ele produz um novo registro de agregação com
o método utilizado, participantes esperados/recebidos, distribuição, resultado e dissensos.

“Tirar uma média” só é correto para medidas numéricas numa escala compatível. Tags são decisões
categóricas e devem produzir, por exemplo, frequência por tag, distribuição de confiança,
concordância entre avaliadores e tags sem quorum. A função estatística deve ser determinística e
versionada; o papel `aggregator` interpreta os resultados em artifact imutável e schema-validado e
adjudica ambiguidades, mas não refaz contas
livremente em prosa. Tags fora do vocabulário viram `tag.proposed`, nunca entram silenciosamente no
catálogo.

O resultado segue uma trilha explícita:

```text
julgamentos privados e imutáveis
              ↓ barreira
agregação determinística + interpretação do aggregator
              ↓
tag_assignment.proposed
              ↓ gate configurado
document writer/materializer atualiza a research
```

O documento é uma projeção do resultado aceito. Avaliações individuais e a agregação permanecem
referenciáveis, permitindo explicar depois por que determinada tag foi adicionada.

## 6. Comunicação entre estágios

Grupos não precisam observar diretamente o bus interno de outros grupos. Uma conexão consome
um `group_result` comprometido e produz um novo snapshot de entrada para o estágio de destino.

- `sequential`: libera o destino após o resultado requerido;
- fan-out (**CANDIDATO/Fase 2**): um resultado pode liberar vários destinos;
- fan-in (**CANDIDATO/Fase 2**): o destino aguarda todos os resultados requeridos ou uma policy de quorum;
- `feedback`: **CANDIDATO**, fora do contrato do MVP até decidir se cria nova rodada,
  `group_version` ou execução do estágio; nunca altera eventos anteriores;
- `zig-zag` (**CANDIDATO/Fase 2**): alterna grupos conforme uma regra de turnos e um limite explícito.

O handoff deve incluir o resultado, seus dissensos e referências de proveniência. O texto
sintetizado sozinho não basta: ele perde a trilha que permite ao estágio seguinte avaliar a
força e os limites da conclusão.

## 7. Realtime para o usuário

Realtime é uma projeção observável do estado, não a fonte de verdade. A interface precisa
mostrar transições assim que elas forem persistidas, inclusive quando o conteúdo de uma
mensagem ainda estiver selado.

Eventos úteis para a UI incluem:

- run criado, iniciado, pausado, cancelado ou encerrado;
- agente aguardando, iniciado, respondido, falhou ou entrou em retry;
- provider, adapter e modelo de cada instância, permitindo acompanhar Codex e Claude em paralelo;
- contagem de posições recebidas sem revelar seu conteúdo;
- contagem de julgamentos privados recebidos, sem revelar valores antes da barreira;
- barreira aberta e posições reveladas;
- rodada de deliberação iniciada ou encerrada;
- votos recebidos, quando permitido pela política de visibilidade;
- consenso, consenso qualificado ou dissenso;
- handoff publicado e próximo estágio liberado;
- registro contextual proposto, aceito, supersedido ou contestado.

O SSE atual é um ponto de partida para transporte servidor→navegador, mas hoje retransmite um
snapshot inteiro quando o fingerprint dos arquivos muda. O alvo deve oferecer:

1. um snapshot inicial consistente;
2. eventos incrementais ordenados após esse snapshot;
3. cursor ou `last_event_id` para reconexão;
4. heartbeat e estado explícito de conexão;
5. fallback para refazer o snapshot quando houver gap;
6. filtros por `run_id`, `group_id` e nível de detalhe;
7. redaction coerente com as fases seladas.

A UI não pode revelar por acidente uma `position` durante `collect`. A mesma política de leitura
deve governar API, SSE e qualquer endpoint de inspeção.

### 7.1 Segurança, privacidade e isolamento

A garantia de selagem é limitada e verificável: durante `collect`, um principal de agente não pode
obter conteúdo ou valores submetidos por outro seat através das superfícies controladas pelo
runtime. Ela não promete ocultar conteúdo de um operador autorizado ou do próprio fornecedor, nem
eliminar todos os canais laterais. Timing e contagens agregadas são metadata; a recipe declara se
podem ser mostrados aos participantes ou somente ao humano.

O trusted computing base do MVP contém kernel, journal writer, policy engine, authenticator/Bus API,
credential broker, sandbox launcher, tool mediation gateway, gateways de ingest/read/validation de
artifact, camada de response/UI security e os reducers que aplicam redaction em API/SSE. Modelo/provider,
recipe, prompt, output, artifact payload, adapter
process e tool server são tratados como potencialmente hostis ou falhos. O runtime DEVE:

- autenticar cada publicação e derivar `actor`, run, group, seat e attempt da sessão/capability;
- emitir capabilities curtas, revogáveis, audience-bound ao Bus API e scoped a
  `(run, group_version, seat, attempt, action, phase)` a partir do estado do journal; payload não
  pode ampliar scope e reconnect/restart revalida policy/phase;
- autorizar `(principal, action, resource, phase)` sob uma policy versionada;
- registrar decisões relevantes de allow/deny e tentativas de replay, impersonation ou break-glass;
- negar antes da barreira leitura, listagem, busca, export, SSE, artifact fetch e debug de conteúdo
  pertencente a outro seat;
- fechar a coleta atomicamente: congelar eligibilidade e manifest/hash, rejeitar late/duplicate e
  persistir `collection.closed`, sem mudar ACL de leitura; somente `reveal.published` concede a
  capability de peer-read para aquele manifest persistido;
- executar cada tentativa em identidade/processo e workspace isolados, sem herdar ambiente, cache,
  credential store ou sessão conversacional compartilhada;
- montar inputs read-only, liberar apenas scratch/artifact explícitos e aplicar network deny-by-default
  com allowlist por tool profile;
- mediar MCP/tools com argumentos tipados, quotas, provenance e validação contra SSRF, path traversal,
  symlink escape e elevação de capability;
- usar credenciais curtas, audience-bound e least-privilege por um broker; sessão CLI do host não é
  montada no sandbox do agente;
- validar hash, tamanho e MIME de artifacts, colocar conteúdo ativo em quarentena e renderizar output
  não confiável com escaping/CSP/download seguro;
- aplicar classificação, redaction e retenção também a logs, traces, provider metadata e UI.

O MVP single-tenant ainda precisa dessas fronteiras entre principais. Um deployment multi-tenant
também deverá particionar IDs, rows, caches, filas, artifacts, cursors e chaves por `tenant_id`, mas
essa ampliação não é condição do primeiro proof slice.

Approvals humanos vinculam `command_id`, `DispatchSpec` digest, versão esperada, recipe/dependency
digests, provider/model destination, classificação/policy de data egress/retention/residency,
tool/network diff e budget. Aprovação expira, pode ser revogada, não pode ser reaplicada a outro
estado e deixa evento de autoria. Policy define papéis aptos a aprovar e usar break-glass; operações
de maior risco podem exigir maker-checker/MFA e revisão posterior.

Imutabilidade não significa retenção ilimitada de conteúdo sensível. Payload pode ser removido por
crypto-erasure ou política legal, preservando somente tombstone, digest, autoria, razão e referências
permitidas pela classificação. Conteúdo sensível/baixa entropia usa keyed digest cuja chave pode ser
destruída; autoria pode ser pseudonimizada/removida quando exigido. Um evento redigido continua como
fato mínimo; projeções não devem fingir que o payload permanece disponível.

## 8. Quatro planos de observabilidade

“Log” não deve ser um único arquivo com todas as responsabilidades:

| Plano | Pergunta respondida | Retenção típica |
|---|---|---|
| **Audit ledger** | Que dispatch foi autorizado e qual foi seu desfecho oficial? | permanente |
| **Event journal** | Quais transições e mensagens compuseram a execução? | durável, conforme política |
| **Logs operacionais** | Por que um processo, adapter ou chamada falhou? | limitada |
| **Traces e métricas** | Onde houve latência, custo, tokens, retries ou filas? | agregada/amostrada |

O audit ledger registra fatos de negócio de alto nível. O event journal é mais granular e
permite reconstruir o estado do runtime. Logs não devem ser usados como banco de estado. Traces
e métricas podem perder detalhe por retenção sem apagar a trilha oficial do dispatch.

No ledger atual, `exit_reason` é o motivo terminal de um dispatch, não o resultado detalhado de
cada agente. O enum aceito pelo appender é `resolved`, `loop_ceiling_reached`,
`dissent_irreconcilable`, `user_abort` ou `error`. No estado-alvo ele continua sendo o resumo
oficial do encerramento; as causas e transições que levaram a ele vivem no event journal.

Todos compartilham os mesmos IDs de correlação. Conteúdo sensível, prompts e outputs completos
exigem política própria de acesso e retenção; observabilidade não é autorização para replicar
todo conteúdo em toda camada.

## 9. Autoridade canônica e `exit_reason`

O deployment do runtime definido por este repositório será a autoridade canônica para novos runs,
eventos, mensagens e registros contextuais. Repositórios de trabalho são identificados por
`project_id`/`repository_ref`, mas não
mantêm cópias autoritativas concorrentes do mesmo run. A auto-descoberta atual de ledgers irmãos
continua útil como compatibilidade de leitura e importação; ela não define autoridade de escrita.

“Canônico” não significa “um único store para todos os fatos”. Cada superfície possui autoridade
disjunta e um write path próprio:

| Superfície | Fatos pelos quais responde | Quem pode publicar | Write path físico |
|---|---|---|---|
| **Bus** | Nenhum fato permanente; transporte governado de mensagens e comandos dentro do run | agentes, kernel e humano conforme ACL/fase | Bus API valida e encaminha; agentes nunca escrevem arquivos ou banco diretamente |
| **Event journal** | Eventos aceitos do runtime: transições, mensagens, tentativas, rounds, entregas e commits | kernel e publicações aceitas pelo bus | journal writer transacional/idempotente |
| **Audit ledger** | Registro mais alto nível: dispatch confirmado, spec/version, autorização e desfecho oficial | command service/kernel nos pontos de abertura e fechamento | somente o appender do audit ledger |
| **Knowledge store** | Definições, premissas, decisões, claims e relações promovidas | propostas dos agentes/humano; promoção por policy, reviewer ou gate | knowledge promotion writer/materializer |
| **Artifact store** | Corpos grandes e imutáveis: outputs, patches, relatórios e snapshots | adapters, agentes via ferramenta e materializers autorizados | artifact service com hash e metadata |
| **Realtime/projeções** | Nenhum fato autoritativo; visão reconstruível para usuário e consultas | somente reducers/materializers | derivado do journal, ledger, knowledge e artifacts |

Agentes são **publishers lógicos** do bus: enviam diretamente suas posições, críticas, votos e
propostas contextuais por ferramentas autorizadas. Isso não os transforma em writers físicos dos
stores. O bus registra a publicação aceita no event journal antes de entregá-la; replay usa o
journal, não a memória da conexão. O appender permanece o único writer apenas do audit ledger de
alto nível existente em `telemetry/agents/subagents-dispatch.yaml`.

### 9.1 Consistência entre stores

Autoridades disjuntas não implicam transação distribuída. No MVP, o event journal é a fonte do
workflow; outbox/materializers tornam ledger, artifacts e futuras projeções convergentes. Cada fluxo
cross-store declara origem, boundary, retry key e reparo:

| Fluxo | Fato que governa | Regra de convergência |
|---|---|---|
| confirm → abertura no ledger | `run.created` + spec digest | materializer projeta spec/journal para a linha completa `0.6.1` e abre uma vez; ausência fica visível e reconciliável |
| artifact → referência | artifact temporário por hash + `artifact.committed` | evento só referencia conteúdo finalizado; upload órfão expira |
| group commit → handoff | `group.committed` | handoff deduplicado por `(source_aggregate_id, connection_id)`; connection id é resolvido no spec/run |
| terminal do run → fechamento | evento terminal único do run | close idempotente; divergência ledger/journal gera alerta e repair |
| proposta → knowledge store | `context_record.proposed` | promotion materializa nova versão e referencia o evento de origem |

Nenhum adapter/provider effect começa antes de o appender confirmar a linha de abertura do audit
ledger. O materializer persiste essa confirmação no journal e somente então o run se torna ready.
No fechamento, o acknowledgement só é persistido depois de a close row existir. Após crash, o
materializer reconcilia por `dispatch_id`/`close_of`: linha idêntica conta como já aplicada;
divergência vira `reconciliation_required`, nunca append duplicado ou autorização implícita.

Falha parcial não pode ser ocultada como sucesso. Projeções expõem estados como
`projection_pending` ou `reconciliation_required`; um reconciler reprocessa outbox pelo mesmo
idempotency key. Backup, restore e failover precisam preservar a unicidade do writer e a ordem do
journal; o MVP assume um writer single-host.

Uma importação histórica deve preservar `source_repo`, o payload original e sua versão de schema.
Projeções podem normalizar dados legados para consulta, mas nunca reescrever o evento de origem nem
apresentar a normalização como se fosse o valor originalmente validado. Depois do cutover, todo novo
registro deve obedecer ao schema vigente de seu store autoritativo; `0.6.1` governa somente novas
linhas do audit ledger atual, não eventos do journal ou records de knowledge/artifact.

Durante compatibilidade/MVP, `dispatch_id` e `run_id` têm cardinalidade 1:1 e o audit ledger mantém
uma abertura e um fechamento oficial por `dispatch_id`. Rerun exige nova versão confirmada e novo
dispatch/run, preservando referência causal ao anterior. O close
materializado inclui o contrato completo vigente, inclusive `agents_spawned` e demais campos
obrigatórios; `run.created` isoladamente não é a linha do ledger.

`exit_reason` classifica **por que a execução terminou**, não o mérito semântico da conclusão. Uma
hipótese falsificada, um parecer negativo ou um resultado `KILL` ainda são `resolved` quando o
protocolo chegou validamente a um resultado comprometido. Narrativa, resumo e qualidade do resultado
pertencem a campos ou artefatos separados, nunca ao enum.

| `exit_reason` | Semântica terminal |
|---|---|
| `resolved` | O protocolo chegou a um resultado comprometido, positivo, negativo ou qualificado. |
| `dissent_irreconcilable` | Restou objeção bloqueante após as rodadas permitidas; o dissenso é o resultado honesto. |
| `loop_ceiling_reached` | O limite de rodadas terminou sem resultado comprometido e sem um dissenso já classificado como irreconciliável. |
| `user_abort` | O usuário encerrou explicitamente a execução. |
| `error` | Uma falha técnica impediu a conclusão do protocolo. |

O fechamento deve ser idempotente e atômico: apenas uma razão terminal vence. Detalhes ficam em
`exit_detail` ou em um artefato referenciado. Para histórico legado, uma projeção pode expor
`raw_exit_reason` e `normalized_exit_reason`, acompanhados de `normalization_reason` e
`schema_violation`, sem alterar a fonte.

## 10. Memória rica de negócio e contexto

Esta seção descreve arquitetura-alvo da Fase 3. O MVP preserva IDs/eventos necessários para futura
proveniência, mas não implementa promoção ou consulta de knowledge.

Durante uma deliberação surgem objetos mais duradouros que uma mensagem: uma definição é
estabelecida, uma premissa é assumida, uma restrição é descoberta ou uma decisão é tomada. Eles
merecem um registro permanente, consultável e com proveniência.

Tipos iniciais candidatos:

- `definition`: significado adotado para um termo em certo escopo;
- `premise`: suposição usada no raciocínio, com status e condições;
- `decision`: escolha tomada, alternativas consideradas e justificativa;
- `constraint`: limite técnico, jurídico, operacional ou de negócio;
- `question`: questão aberta, bloqueada, respondida ou descartada;
- `claim`: afirmação verificável ainda não elevada a outro tipo;
- `evidence`: fonte ou artefato que sustenta ou contesta uma afirmação;
- `risk`: evento ou condição adversa, impacto e mitigação;
- `exception`: desvio explícito de uma regra ou padrão;
- `term_alias`: equivalência ou distinção terminológica.

Um registro contextual não é apenas texto com uma tag:

```jsonc
{
  "record_id": "uuid",
  "record_type": "premise",
  "scope": { "run_id": "...", "group_id": "...", "domain": "..." },
  "statement": "...",
  "status": "proposed",
  "proposed_by": "agent-instance-id",
  "source_message_ids": ["..."],
  "evidence_refs": ["..."],
  "valid_from": "...",
  "supersedes": null,
  "confidence": null,
  "created_at": "..."
}
```

Estados como `proposed`, `accepted`, `contested`, `superseded` e `rejected` preservam a
diferença entre algo mencionado por um agente e algo adotado pelo sistema ou pelo humano. Uma
definição não deve virar verdade canônica só porque apareceu em uma resposta.

### 10.1 Bus geral versus armazenamento permanente

O bus geral de contexto é o caminho de **submissão e notificação**. O
`knowledge/provenance store` é o sistema permanente de **registro, versão e consulta**.

```text
mensagem de agente
      │ propõe
      ▼
context stream ──► validação/adjudicação ──► knowledge/provenance store
      │                                             │
      └──── evento realtime                         └── projeções de busca e contexto
```

Essa separação evita dois problemas:

- tratar o transportador efêmero como banco canônico de conhecimento;
- colocar toda conversa bruta na memória de longo prazo sem seleção ou governança.

O transporte do bus pode ser efêmero: uma mensagem disponível numa fila, conexão ou projeção
live não precisa sobreviver indefinidamente. O fato aceito e sua proveniência, por outro lado,
precisam sobreviver no store permanente. Quando replay e recuperação forem necessários, o event
journal durável recompõe o fluxo; a fila ou conexão live não se torna fonte de verdade por isso.

Os agentes podem propor registros durante a conversa. Uma política determinística, um papel
revisor ou um gate humano decide sua promoção. Alterações produzem novas versões e relações como
`supersedes` ou `contradicts`; não reescrevem silenciosamente o passado.

### 10.2 A memória pode ser construída depois?

Sim. Ela não precisa bloquear o primeiro ciclo `collect → reveal → deliberate → vote → commit`.
Para manter essa opção barata, o MVP deve preservar desde já:

- IDs estáveis para eventos, mensagens, agentes, snapshots e artefatos;
- `causation_id` e `correlation_id`;
- referências das mensagens às evidências usadas;
- autoria e timestamps gerados pelo sistema;
- versão do schema;
- payloads imutáveis ou content-addressed;
- um tipo de evento reservado, como `context_record.proposed`, mesmo que sua materialização
  permanente ainda não exista;
- separação entre conteúdo, evento de transporte e projeção de UI.

Sem esses elementos, ainda será possível construir a memória depois, mas a proveniência do
histórico anterior será parcial ou especulativa.

### 10.3 Replay, checkpoints e retenção

Replay reconstrói estado a partir de checkpoint verificado mais eventos posteriores. O checkpoint
registra hash do estado, último `journal_offset`, versão do reducer/kernel e digests do spec/recipe.
Eventos não são descartados enquanto forem necessários para recuperar um run ativo, explicar um
commit retido ou validar um checkpoint. Compaction preserva as constraints de unicidade e tombstones
necessários para impedir reaceitação de comandos antigos.

Snapshots de entrada são manifests content-addressed: listam artifacts, hashes, versões de schema,
model/adapter efetivos e policy. Estado externo lido por tool/provider só se torna parte do replay
quando seu resultado imutável é registrado. Isso torna a redução do protocolo reproduzível; não
promete gerar novamente a mesma resposta do modelo.

Garbage collection de artifacts só remove payload sem referência por evento/checkpoint retido e
fora de legal hold. Retenção de metadata, payload e logs é separada; redaction/crypto-erasure deixa
tombstone auditável sem tornar o reducer dependente do conteúdo apagado.

## 11. Invariantes

1. **Independência antes da revelação.** Um agente não lê posições dos pares até o grupo persistir
   `reveal.published` para o manifest congelado. Submeter, abstain ou timeout individual não abre
   acesso antecipado.
2. **Imutabilidade.** Posições, votos, resultados e registros aceitos não são editados; correções
   criam novos eventos ou versões.
3. **Uma identidade por tentativa.** Persona, papel e instância de execução são conceitos
   separados.
4. **Portabilidade e composição de fornecedor.** Entre adapters que satisfazem o capability profile
   congelado, misturar ou trocar implementação não altera protocolo, schemas dos buses ou regra de
   decisão; capability semantics-changing exige novo spec confirmado.
5. **Extensão por registry e recipe.** Um tipo pessoal, organizacional ou de sistema adiciona
   identidade, contratos e grafo versionados sem alterar a máquina de estados genérica do kernel.
6. **Transição determinística.** A mesma configuração e o mesmo journal produzem o mesmo estado.
7. **Idempotência lógica.** Reentrega e retry podem repetir execução física, mas constraints por
   operação/seat/round não duplicam mensagens aceitas, votos, commits ou handoffs.
8. **Dissenso preservado.** Consenso não apaga objeções nem evidências minoritárias.
9. **Commit único por versão do grupo.** Um resultado comprometido é publicado uma única vez;
   revisão cria nova versão.
10. **Realtime é projeção.** Perder uma conexão SSE não perde o estado da execução.
11. **Visibilidade uniforme.** API, stream e UI aplicam a mesma política de selagem.
12. **Proveniência obrigatória.** Todo conhecimento promovido aponta para sua origem ou declara
    explicitamente que ela é externa/desconhecida.
13. **Logs não governam estado.** O runtime nunca depende de parsing de logs operacionais para
    decidir a próxima transição.
14. **Encerramento explícito.** Toda execução terminal registra a razão de saída; ausência de
    atividade não equivale a sucesso.
15. **Agregação reproduzível.** Dados individuais imutáveis mais a mesma função/versionamento
    produzem o mesmo agregado; interpretação do agente fica separada do cálculo.
16. **Privacidade por fase.** “Privado” significa inacessível aos pares durante a coleta, não
    ausência de auditoria: acesso posterior depende de papel, fase e política registrados.
17. **Comando não é evento.** Replay reduz fatos aceitos e nunca reexecuta comandos ou efeitos
    externos implicitamente.
18. **Relógio não governa replay.** Deadline e timeout só afetam estado através de evento persistido.
19. **Concorrência explícita.** Toda transição usa versão esperada; somente uma transição terminal
    válida vence, e observações tardias permanecem auditáveis.
20. **Autorização derivada.** Identidade e escopo são derivados de principal autenticado, nunca de
    campos de autoridade fornecidos pelo payload do agente.

## 12. MVP proposto

O MVP é uma sequência de proof slices. Cada slice tem um falsificador próprio; não se adiciona um
segundo provider antes de provar persistência, sealing e recovery com execução determinística.

### Slice 0 — prova do protocolo

- SQLite/WAL, um journal writer e reducer single-host;
- um run, um grupo e dois `seat_id` fixos;
- fake adapters determinísticos;
- `collect → reveal → vote → commit`, sem `deliberate`, replacement ou tools externos;
- regra fixa de decisão e schemas fechados;
- blob store local content-addressed mínimo, sem serviço de artifacts grandes;
- snapshots/manifests content-addressed sobre esse store;
- conditional append, command idempotency e replay após restart;
- claim durável single-host por `worker_epoch`, sem leases distribuídos;
- barreira mínima do audit ledger: opening row verificada antes do fake adapter e close row após o
  terminal, ambas pelo appender atual;
- endpoint de consulta, sem UI de operação.

### Slice 1 — falhas, selagem e observação

- uma rodada limitada de `deliberate`;
- policy de leitura por principal/fase e barreira atômica;
- regras para deadline, abstention e races cancel/completion/commit;
- sandbox read-only e credential broker mínimo;
- snapshot + SSE incremental com cursor e fallback consistente;
- outbox durável, estados pending, crash recovery e reconciliation para abertura/fechamento no audit ledger.

### Slice 2 — um provider real

- um adapter CLI exercitando start idempotente, cursor, status/reconciliation e cancel lifecycle;
- structured-output validation e policy para malformed/partial/late result;
- model/tool observations imutáveis e um tool profile somente leitura;
- limites de payload, tokens, tempo, fila, artifacts e disco.

### Slice 3 — portabilidade de fornecedor

- segundo adapter CLI e grupo misto;
- matriz de capabilities obrigatórias/emuláveis/incompatíveis;
- mesma suite de contrato por adapter e pelo grupo misto;
- equivalência operacional de estados/eventos, sem exigir conteúdo semanticamente idêntico.

### Slice 4 — composição e recipes

- handoff `sequential` entre dois grupos;
- duas recipes built-in com digests imutáveis, uma `research` e uma `review` read-only;
- somente então registry/compilador genérico.

Tipos namespaced de usuário entram depois de assinatura/digest, dependency lock, revogação,
compatibilidade e policy de instalação estarem definidos. Julgamentos selados, agregação de tags,
mutating `code`, knowledge promotion e topologias `feedback`/`zig-zag` também ficam fora desses
primeiros slices.

O MVP completo continua single-host e single-tenant. Kafka/NATS, workers distribuídos, edição de
ontologia, busca vetorial, promoção autônoma de contexto, loops irrestritos e governança
multi-tenant sofisticada ficam fora.

### 12.1 Gate de valor do produto

Antes do Slice 3, uma avaliação pre-registrada compara o protocolo com baseline de um único agente
em um conjunto fixo de tarefas. Critérios incluem qualidade por rubric, dissenso relevante capturado,
false consensus, latência, custo de tokens/tools, taxa de recovery e carga operacional. Thresholds e
regra de decisão são registrados antes do teste; se o ganho não compensar custo/latência de forma
consistente, a arquitetura deve ser simplificada ou interrompida.

## 13. Evolução

Fase 1 corresponde aos Slices 0–4 do MVP. As fases seguintes começam somente depois de seus gates.

### Fase 2 — robustez e topologias

- fan-out/fan-in, `feedback` e `zig-zag`;
- recipe `code/plan-implement-review`, com workspaces isolados, testes e merge authority;
- políticas adicionais de quorum, replacement e retry além do perfil fixo provado no MVP;
- adapters adicionais e limites de custo;
- replay histórico arbitrário, compaction avançada e projeções de UI mais específicas;
- armazenamento de artefatos grandes fora do journal.

### Fase 3 — memória contextual

- knowledge/provenance store materializado;
- workflow de proposta, revisão, aceitação e supersessão;
- consultas por tipo, escopo, validade e relação;
- composição controlada desses registros em snapshots futuros;
- detecção e exposição de definições ou premissas conflitantes.

### Fase 4 — escala e governança

- workers distribuídos e leases;
- autorização organizacional/multi-tenant e administração delegada, além da ACL mínima do MVP;
- retenção diferenciada, redaction e exportação;
- métricas de convergência, mudança de posição e qualidade do dissenso;
- avaliação de um broker externo somente quando o volume ou a distribuição justificarem.

## 14. Testes de aceitação e fault injection

Cada slice deve publicar fixtures, traces esperados e state hashes. A suite mínima cobre:

| Área | Teste | Critério |
|---|---|---|
| sealing | tentar ler posição de peer por API, SSE, artifact, busca, logs/debug e workspace durante `collect` | todas as superfícies negam/redigem; conteúdo próprio permitido |
| barreira | crash antes/depois de `collection.closed` e `reveal.published` | `collection.closed` sozinho não abre ACL; somente o manifest/hash de `reveal.published` é legível após restart |
| replay | crash após cada append boundary | reducer chega ao mesmo state hash sem nova contribuição/commit/handoff lógico |
| duplicação | reenviar command, provider result e delivery N vezes | constraints aceitam um único efeito lógico |
| races | última posição × deadline; cancel × completion; cancel × commit | cada ordenação termina em um trace permitido e um único terminal vencedor |
| relógio | replay de deadline | decisão usa `deadline.fired` persistido e não consulta wall clock |
| output inválido | malformed JSON, schema inválido, artifact ausente e resposta tardia | regra declarada rejeita/retry/abstém/falha sem transição ilegal |
| identidade/quorum | retry e replacement | um seat não obtém dois votos; denominator e autoria permanecem auditáveis |
| adapter | crash antes/depois de start e completion | reconciliation converge ou registra `effect_unknown`, sem fingir sucesso |
| stores | falha entre journal e ledger/artifact materialization | reconciler converge sem segundo close ou referência a payload incompleto |
| SSE | reconnect por cursor, cursor expirado e gap | stream ordenado sem gap lógico ou snapshot consistente obrigatório |
| segurança | identity spoof, cross-run publication, stale approval, prompt/tool escalation | comando negado e tentativa auditada |
| capability | replay/revogação/reconnect após mudança de phase | token antigo falha; capability reemitida deriva do journal atual |
| sandbox/egress | SSRF/DNS rebinding, traversal/symlink, cross-workspace e egress não autorizado | launcher/gateway falha fechado e registra tentativa |
| conteúdo hostil | HTML/SVG/provider metadata/log injection e artifact inválido | conteúdo é escapado, bloqueado ou colocado em quarentena sem secret leak |
| credenciais | inspecionar env, mounts, logs, outputs e artifacts | nenhum secret/profile do host é observável pelo agente |
| recursos | payload/token/time/disk/queue budget excedido | encerramento explícito conforme policy, sem bloquear outros runs |
| produto | baseline single-agent × protocolo | threshold pre-registrado decide continuar, simplificar ou abortar |

Os testes de sealing incluem alternate channels controlados pelo runtime. Ausência de vazamento em
uma UI não prova isolamento se filesystem, provider session ou tool server continuarem compartilhados.

Replay/duplicação/relógio são obrigatórios no Slice 0; sealing/barreira/SSE/capability/sandbox/stores
no Slice 1; adapter, conteúdo hostil, credenciais, recursos e gate de produto como exit gate no
Slice 2; conformance mista no Slice 3. Replacement só entra quando a capability correspondente for
implementada.

## 15. Critérios de falsificação

A arquitetura deve ser revista se:

- a barreira não puder impedir tecnicamente a leitura antecipada;
- o journal não permitir reconstruir o estado após uma queda;
- replay reexecutar command/tool/provider effect em vez de reduzir somente fatos persistidos;
- races de cancelamento, deadline e completion produzirem dois terminais ou contribuições duplicadas;
- o kernel precisar interpretar conteúdo livre para executar transições básicas;
- o mecanismo de consenso apagar dissenso relevante;
- uma agregação categórica for reduzida a uma média sem semântica ou esconder a distribuição
  individual que a produziu;
- a UI realtime exigir uma segunda fonte autoritativa de estado;
- adicionar a memória contextual exigir duplicar mensagens sem preservar sua origem;
- trocar entre adapters que satisfazem o mesmo capability profile exigir alterar máquina de estados,
  schemas dos buses ou regras de consenso, em vez de apenas selecionar outra implementação;
- executar Codex e Claude simultaneamente exigir ledgers, buses ou caminhos de realtime separados;
- adicionar `code`, `review` ou outra ação exigir branches específicos no kernel em vez de uma nova
  recipe e seus contratos;
- registrar uma rotina namespaced do usuário exigir editar o enum ou publicar uma nova versão do
  kernel;
- o sandbox, Bus API ou outra superfície controlada permitir que um agente leia conteúdo selado de
  um peer antes da barreira;
- o custo operacional do protocolo exceder de forma consistente o ganho de independência e
  auditabilidade.

## 16. Documentos relacionados

- [`discovery/feature-discovery/agents-communication-infra.md`](discovery/feature-discovery/agents-communication-infra.md) — discovery
  de aplicação derivada desta arquitetura candidata; preserva decisões/OQs como entrada rastreável
  para a futura SPEC DomainSpec.
- [`README.md`](../../../README.md) — visão geral, schema e control plane atuais.
- [`PLAN.md`](../../PLAN.md) — roadmap e obrigações do projeto.
- [`engine-constitution.md`](../../../vault/constitution/engine-constitution.md) — invariantes
  atuais do ledger e do leitor.
- [`orchestration-infra.md`](../../../vault/hypothesis/orchestration-infra.md) — hipótese anterior
  sobre bus, IDs, retenção e freeze-before-the-channel.
- [`anti-noise-orchestration.md`](../../../vault/hypothesis/anti-noise-orchestration.md) — tese
  conceitual sobre independência de julgamento e redução de ruído.
- [`findings.md`](../../../research/agent-events-infra-hypothesis/findings.md) — investigação de
  envelopes, tagging, proveniência e possíveis reutilizações.
- [`UI-CONTRACT.md`](../../../implementations/UI-CONTRACT.md) — contrato da UI somente leitura e
  comportamento SSE existentes.

## 17. Questões abertas

Questões abertas devem ser promovidas a ADRs antes do slice correspondente, com `id`, status
(`proposed`, `accepted`, `superseded`), owner, slice bloqueado, deadline, opções/evidências, decisão,
consequências e testes de aceitação. O diretório/template de ADR ainda será escolhido; esta seção é
o registro canônico provisório. Uma questão bloqueante precisa ser resolvida antes do código do slice.

### Bloqueiam Slice 0

1. **OQ-PERSISTENCE:** assumindo SQLite/WAL no proof slice, qual schema/boundary transacional reúne
   event append, aggregate version, constraints e outbox, e qual configuração de durability é aceita?
2. **OQ-DECISION — decisão aceita no corpus, receipt independente pendente:** o profile
   `fixed-two-seat-proof@1` exige dois votos; igualdade produz `consensus`, conflito produz
   `dissent`, e menos de dois produz `no_quorum`. O profile local-probe não executa votação.
3. **OQ-TERMINAL — decisão aceita no corpus, receipt independente pendente:** somente a causa
   terminal única do run mapeia para `resolved`, `dissent_irreconcilable`,
   `loop_ceiling_reached`, `user_abort` ou `error`,
   conforme [ADR-002](adrs/ADR-002-compatibility-terminal-snapshot-and-local-probe.md).
4. **OQ-STREAM:** qual é o escopo de `journal_offset`, e checkpoints usam um stream global, por run
   ou por aggregate?
5. **OQ-SNAPSHOT — decisão aceita no corpus, receipt independente pendente:** inputs, profiles,
   schemas, capabilities e bytes externos são artefatos imutáveis content-addressed; legacy
   dispatch usa snapshot estrito com identidade e dois digests, sem prometer reprodução do modelo.

### Bloqueiam Slice 1

6. **OQ-VISIBILITY:** metadata de progresso/timing é visível aos agentes, apenas ao humano ou a
   ninguém durante coleta? Quais atores humanos podem usar break-glass?
7. **OQ-TIMEOUT:** timeout registra abstention, altera quorum ou encerra sem decisão? Qual precedência
   vale entre `deadline.fired`, último submission, cancel e commit?
8. **OQ-CANCEL:** quando cancellation pode interromper commit, quanto tempo espera ack do provider e
   como representa completion tardia?
9. **OQ-RETENTION:** qual conjunto mínimo de eventos/payloads/checkpoints permanece para recovery e
   auditoria, e quais classes admitem TTL, redaction ou crypto-erasure?
10. **OQ-LEDGER-CONSISTENCY — contrato W0 congelado no corpus; prova física aberta:** o appender
    validado continua único writer; identidade igual + row idêntica é `verified`, divergência é
    `reconciliation_required`; TASK-020 ainda deve provar processo/ACL/inventário/bypass antes de
    materializer ou cutover.
11. **OQ-REALTIME:** assumindo SSE no MVP e command API separada, qual formato, assinatura,
    expiração, autorização e gap recovery rege cursors, e qual evidência futura justificaria trocar
    o transporte?
12. **OQ-SANDBOX:** qual mecanismo/launcher confiável impõe isolamento de processo, workspace,
    mounts e network; como separa provider/control-plane egress de agent-tool egress; e como falha
    fechado quando containment, DNS/proxy policy ou cleanup não puderem ser confirmados?
### Bloqueiam adapters reais e portabilidade

13. **OQ-CAPABILITIES:** quais capabilities são obrigatórias, emuláveis ou incompatíveis, e quais
    diferenças de provider invalidam a equivalência operacional?
14. **OQ-CREDENTIALS:** qual mecanismo implementa a policy já decidida de credencial curta sem montar
    profile/cache do host, e como revogação, provider retention, residency e conversation isolation
    são verificadas?
15. **OQ-UNKNOWN-EFFECT:** como reconciliar provider/tool cujo efeito ocorreu mas cujo resultado não
    pode ser consultado com certeza?
16. **OQ-RESOURCE-LIMITS:** quais budgets de tokens, custo, tool calls, payload, artifact, fila, tempo
    e disco são obrigatórios por run/attempt?
17. **OQ-PRODUCT-EVAL:** qual corpus/ground truth, rubric, avaliadores cegos, sample size, efeito
    mínimo e trade-off custo/latência governam o gate do Slice 3, e quem responde pela decisão?

### Bloqueiam recipes abertas e topologias posteriores

18. **OQ-RECIPE-SUPPLY-CHAIN:** qual formato, assinatura/digest, dependency lock, revogação,
    compatibilidade e rollout governam instalação de recipes e extensões confiáveis?
19. **OQ-OVERRIDES:** quais parâmetros o usuário pode sobrescrever sem enfraquecer sealing,
    provenance, sandbox, budgets ou regra de decisão?
20. **OQ-NAMESPACE:** quais regras de owner, resolução e acesso governam tipos `system`,
    `organization`, `workspace` e `user` sem confundir namespace com autorização?
21. **OQ-PROTOCOL-MODULES:** recipes personalizadas apenas instanciam a máquina comum ou podem
    selecionar novos módulos de protocolo instalados? Qual parte permanece kernel fechado?
22. **OQ-FEEDBACK:** `feedback` cria nova rodada, nova `group_version` ou nova execução do estágio?
    Até decidir, `feedback` não pertence ao contrato normativo do MVP.
23. **OQ-AGGREGATION:** por dimensão, qual agregador e schema de interpretação são válidos, e quando
    aggregator e materializer devem ser papéis separados?
24. **OQ-KNOWLEDGE:** quem promove `context_record.proposed`, como tipos/escopos evoluem e como
    accepted, contested, superseded, sensitive e deleted preservam provenance?
25. **OQ-MULTITENANCY:** quais partitions de storage/cache/queue/artifact/key e quais testes de
    cross-tenant isolation são exigidos antes de oferecer um deployment compartilhado?
26. **OQ-SEALED-VOTE:** em qual slice pós-MVP votos selados entram e qual
    manifest/barreira/capability/teste equivalente ao reveal de posições governa sua abertura?
27. **OQ-SPEC-SPLIT:** depois dos ADRs dos Slices 0–1, quais detalhes normativos saem deste README
    para specs versionadas de protocolo/eventos, adapters, segurança, persistence/recovery e testes,
    mantendo este arquivo como índice arquitetural estável?
