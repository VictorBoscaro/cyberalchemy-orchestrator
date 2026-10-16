---
tags: [dispatch, handoff, orchestration, runtime-architecture]
artifact_kind: audit
layer: project
version: 0.2.0
created_at: 2026-09-02T11:57:40-03:00
updated_at: 2026-09-02T13:28:11-03:00
---

# Retrospectiva técnica da arquitetura de dispatch

**Data da análise:** 2026-09-02

**Escopo:** construção, abertura, handoff, acompanhamento e fechamento de dispatches de subagentes

**Estado:** diagnóstico do repositório atual; não é uma nova especificação

## Resumo

O problema central não foi escolher YAML, SQLite, hooks ou arquivos. Cada uma dessas escolhas
respondia a uma necessidade real. O problema foi resolver incidentes locais acrescentando uma nova
camada sem retirar autoridade das anteriores. Ao final, nenhum componente passou a ser dono do
ciclo completo: o LLM monta o registro, uma skill descreve o procedimento, um compilador produz
bindings, um appender escreve YAML, uma bridge coordena YAML e SQLite, hooks interceptam o host e o
runtime registra parte do estado. Cada fronteira é defensiva localmente, mas o conjunto não oferece
uma única transação, uma única máquina de estados nem um único responsável por recuperação.

Isso explica por que o sistema parece muito mais complexo do que a operação que deveria realizar.
Hoje não existe um serviço que *monte* o dispatch. O agente pai aplica as skills e escreve
manualmente um `opening.json`. O código valida, resolve uma rota, compila arquivos derivados, abre o
registro em dois stores, autoriza chamadas do host e tenta reconciliar o fechamento. O trabalho de
decidir a forma do dispatch continua no LLM; a complexidade de garantir a execução foi distribuída
por vários componentes.

O defeito de handoff que motivou esta análise é, portanto, um sintoma de uma incompatibilidade maior:
o compilador foi concebido como compilação antecipada de todos os seats, enquanto um handoff
sequencial só existe depois que o produtor termina. A alteração local atual tenta ligar os dois
mundos exigindo o receipt do produtor durante a compilação inicial. Isso cria uma dependência
circular: para compilar o plano que lançaria o produtor, o output do produtor já precisa existir.
Consertar somente a spec não resolve essa contradição; ela exige mudar o modelo de execução para
scheduling incremental ou dividir cada etapa em dispatches independentes.

## Como o fluxo funciona hoje

O fluxo governado pretendido é este:

```text
usuário
  ↓
agente pai aplica a capability e escreve opening.json
  ↓
resolve(capability-ref) → rota canônica
  ↓
compile(opening.json, capability-ref, output-dir)
  └─→ manifests por seat + launch-plan.json + prompts com binding
  ↓
open(opening.json)
  └─→ appender YAML → link de sessão SQLite → evento de abertura
  ↓
agente pai chama spawn_agent com o prompt compilado
  └─→ hook decodifica ACI-WORKFLOW-BINDING-V1
      → runtime cria host_workflow_turn_binding
      → host executa o subagente
  ↓
hooks correlacionam término e runtime fecha o binding
  ↓
agente pai escreve close.json e chama close
  └─→ preflight SQLite → appender YAML → evento de fechamento
```

Esse diagrama é uma composição de instrução e código, não uma operação atômica implementada
por um serviço. A skill de entrada decide se deve delegar, escolhe a capability e resolve sua rota;
depois entrega um registro concreto à skill de lifecycle
([entrada](../.agents/skills/domainspec-subagents-strategy/SKILL.md),
[lifecycle](../.agents/skills/subagents-dispatch-lifecycle/SKILL.md)). O lifecycle manda o agente pai
confirmar, compilar, abrir, chamar o host, verificar e fechar. Não há nesse caminho um construtor de
dispatch independente do LLM.

Existem, na realidade, dois caminhos de launch:

1. **Launch ligado ao pai.** O prompt começa com `ACI-WORKFLOW-BINDING-V1:`. O hook decodifica o
   envelope, chama `bind_host_workflow_turn` e persiste um estado `aci-host-workflow-state/v1`
   ([hook, linhas 438–524](../implementations/server/runtime/host_dispatch_hook.py#L438)). Esse é o
   caminho que preserva dispatch, grupo, seat, turno, tentativa, prompt e manifest.
2. **Launch de compatibilidade.** Se um `spawn_agent` não traz o envelope, o hook cria
   automaticamente outro dispatch, com ID `*-auto-<host>-agent-*`, um grupo e um seat
   ([hook, linhas 350–436](../implementations/server/runtime/host_dispatch_hook.py#L350)). Antes de
   abrir, grava um arquivo local com status `preparing`; depois passa pela bridge e muda para
   `opened` ([linhas 529–590](../implementations/server/runtime/host_dispatch_hook.py#L529)). Um
   `followup_task` sem binding é negado.

O segundo caminho nasceu para impedir launches invisíveis, mas também permitiu que o sistema
continuasse funcionando sem o primeiro. A compatibilidade deixou de ser apenas uma borda de migração
e permaneceu no caminho causal normal.

### O que significam os arquivos e argumentos

`opening.json` é o registro concreto de abertura. Ele contém o dispatch confirmado: objetivo,
grupos, agentes, prompts, conexões, tipo e metadados. Ele é escrito pelo agente pai e consumido por
`compile` e `open`. Não é o banco de dados e não é um arquivo gerado pelo compilador.

Não há etapa de exclusão na skill de lifecycle nem nos comandos `compile`, `open` e `close`.
Durante a execução, o arquivo funciona como a entrada congelada a partir da qual rota, manifests e
digests podem ser verificados. Preservá-lo pode servir à provenance, mas o lifecycle não define uma
política clara de retenção, arquivamento ou garbage collection. O resultado é uma mistura de
evidência durável com working files em `.codex/workflow-inputs/`. Portanto, "não apagar" não é, por
si só, o bug; o bug é não haver um dono e uma regra explícita para o ciclo de vida desses artefatos.

`capability-ref` é o identificador da capability instalada que possui o tipo de trabalho, como
`research`, `review` ou `domainspec-implement`. O comando `resolve` transforma essa referência numa
rota que inclui tipo de dispatch, projeção no ledger, modo de autoridade e perfil de ferramentas.
No `compile`, a mesma referência é resolvida de novo e o compilador verifica se o `dispatch_type` do
registro coincide com a rota
([`compile_bound_launch_plan`, linhas 424–447](../implementations/server/runtime/dispatch_workflow.py#L424)).
Ela não é um arquivo nem o agente a ser lançado. O fato de o registro e o argumento carregarem
informação relacionada é uma defesa contra drift, mas também mostra que a autoridade foi repartida
entre o JSON e o registry.

`output-dir` é somente o diretório, relativo ao repositório, onde o compilador deposita seus
artefatos derivados. Ele não é o diretório de resultado dos subagentes. Para cada seat, o compilador
escreve um manifest; depois escreve `launch-plan.json`
([linhas 454–548](../implementations/server/runtime/dispatch_workflow.py#L454)).

`launch-plan.json` é a representação executável derivada do `opening.json`: contém a rota e os
`spawn_arguments` com o envelope base64 que liga a chamada do host ao dispatch pai. Ele existe para
que o agente pai não tenha de montar manualmente o binding. Essa separação é justificável, mas hoje
ela não vem acompanhada de um scheduler: o pai ainda precisa ler o plano, decidir o que está pronto,
fazer cada chamada e controlar os retornos.

## Como chegamos aqui

Não há evidência de um único commit no qual a arquitetura "deu errado". A história mostra uma
sequência cumulativa de correções locais:

- Em 20 de julho, o commit
  [`7fedf6d`](https://github.com/VictorBoscaro/cyberalchemy-orchestrator/commit/7fedf6d26ecc2628492721cdfeb12417ec5bcd1f)
  introduziu o reader/control plane sobre o ledger. O problema resolvido era visibilidade e auditoria.
- Em 24 de julho, o commit
  [`c987db8`](https://github.com/VictorBoscaro/cyberalchemy-orchestrator/commit/c987db89ee495fcda5ea3c58c3a71f592f19c37c)
  tornou obrigatória a bridge de logging para launches do host. O problema resolvido era a
  possibilidade de um agente ser lançado sem registro. A partir daqui YAML, journal/SQLite e arquivos
  de estado passaram a participar da mesma operação.
- Em 25 de julho, o commit
  [`814192a`](https://github.com/VictorBoscaro/cyberalchemy-orchestrator/commit/814192aeb0dc2f2d932d7fbcd54bedfb692d5028)
  ligou turns do host a um dispatch pai confirmado. A ADR da época registra que cada launch estava
  sendo embrulhado como um dispatch de compatibilidade e que o pipeline geral ainda não existia
  ([estado verificado](decisions/host-agent-dispatch-input-binding.md#L15)). A
  solução aceita foi explicitamente descrita como uma bridge temporária e limitada
  ([opção A](decisions/host-agent-dispatch-input-binding.md#L30)).
- Em 3 de agosto, o commit
  [`f309972`](https://github.com/VictorBoscaro/cyberalchemy-orchestrator/commit/f30997237529a333959c11b9bed13a3b047409f8)
  adicionou `dispatch_workflow.py` e `subagents-dispatch-lifecycle`. O autor registrado é Victor
  Boscaro; a mensagem do commit é `qualquer coisa`, portanto o Git identifica autoria, mas não
  preserva a intenção da decisão.
- Em 13 de agosto, o commit
  [`70d0b2c`](https://github.com/VictorBoscaro/cyberalchemy-orchestrator/commit/70d0b2c2bbae17cdbbfd3ea3c26ab36c1b46f755)
  passou a rotear dispatches pelo registry de capabilities. O problema resolvido era drift de tipo e
  rota.
- Em 1º de setembro, o commit
  [`f981397`](https://github.com/VictorBoscaro/cyberalchemy-orchestrator/commit/f9813974810a7ae2baea943c72adc1d904450f1c)
  reforçou compilação autoritativa do grafo. A arquitetura continuou ganhando controles antes de um
  único golden path cobrir, de ponta a ponta, criação, dependência, launch, continuação, recovery e
  fechamento.

Cada passo é defensável isoladamente. O efeito sistêmico foi acúmulo: a bridge que deveria ser
temporária ganhou bindings, manifestação de inputs, outputs, correlação de eventos, compatibilidade,
capabilities e fechamento cross-store sem que a arquitetura geral a substituísse.

## O que falhou

### 1. Não existe um dono do lifecycle completo

A skill possui routing; a capability possui o julgamento do trabalho; o registry possui tipos; o
agente pai possui o `opening.json` e o scheduling; o compilador possui manifests e bindings; o
appender possui a mutação do YAML; o runtime possui fatos em SQLite; o hook possui a intercepção e
arquivos de correlação. Quando a operação cruza todas essas fronteiras, nenhuma delas consegue
garantir sozinha que o todo foi concluído ou recuperado.

O próprio contrato de cutover reconhece a dificuldade. Ele diz que o estado atual é `C0`, que
produção, materialização e cutover permanecem bloqueados
([linhas 54–61](features/agents-communication-infra/discovery/dispatch-audit-ledger-cutover-contract.md#L54)).
O documento tem status `proposed`, `runtimeGate: contract-only` e `productionCutoverGate: block`.
Logo, esse contrato é evidência da intenção e dos riscos conhecidos, não prova de que a solução
esteja implementada.

### 2. Compilação antecipada e dependências de runtime são modelos incompatíveis

No `HEAD`, os manifests eram compilados com `slots: []`. A alteração ainda não commitada em
`dispatch_workflow.py` adiciona `_sequential_handoffs`, lê conexões sequenciais e exige, dentro do
`output-dir`, um `handoff-<origem>-<destino>.json` com receipts e bytes imutáveis dos produtores. Essa
validação ocorre antes do loop que gera os launches
([linhas 471–478](../implementations/server/runtime/dispatch_workflow.py#L471)).

Para um dispatch novo, o produtor ainda não rodou; portanto seu output e seu receipt não existem.
Se existe uma conexão sequencial, a compilação bloqueia antes de produzir o launch do próprio
produtor. Isso não é uma falta de campo na spec. É a tentativa de resolver uma dependência dinâmica
em uma fase estática.

Há duas soluções coerentes. Um scheduler incremental compila/libera apenas os seats prontos e,
depois do término do produtor, materializa o manifest dos consumidores. Alternativamente, cada
estágio vira um dispatch separado, com o output anterior congelado como source do seguinte. A ADR
de julho já registrava essa segunda opção
([linhas 55–63](decisions/host-agent-dispatch-input-binding.md#L55)). Tentar manter compilação total
e handoff dinâmico ao mesmo tempo produz a circularidade atual.

### 3. Strictness local não produz atomicidade cross-store

A bridge abre primeiro no YAML, depois cria o link de sessão em SQLite e só então registra o evento
de abertura ([linhas 274–329](../implementations/server/runtime/orchestration_bridge.py#L274)). No
fechamento, executa um preflight, anexa o close ao YAML e depois aceita o fechamento no runtime
([linhas 352–390](../implementations/server/runtime/orchestration_bridge.py#L352)). Há failpoints
explícitos entre essas etapas, o que confirma que o próprio código reconhece janelas de falha.

Existe ainda uma janela concreta: `require_orchestration_dispatch_can_close`, chamado antes de
escrever o YAML, verifica link, Scout pendente e journal head, mas não verifica bindings em execução
([linhas 2328–2374](../implementations/server/runtime/service.py#L2328)). A verificação de binding em
execução acontece somente em `record_orchestration_dispatch_closed`, depois do append YAML
([linhas 2239–2261](../implementations/server/runtime/service.py#L2239)). Assim, o preflight pode
passar, o close pode entrar no YAML e a aceitação SQLite pode falhar em seguida.

O contrato de cutover descreve a recuperação correta como intent durável, appender único, releitura
exata e acknowledgement pelo digest
([linhas 118–130](features/agents-communication-infra/discovery/dispatch-audit-ledger-cutover-contract.md#L118),
[linhas 147–159](features/agents-communication-infra/discovery/dispatch-audit-ledger-cutover-contract.md#L147)).
Mas o mesmo documento diz que essa etapa materializadora ainda não está habilitada. A especificação
correta existe; o caminho atual ainda não a realiza.

### 4. A continuidade está especificada, mas não demonstrada no uso observado

O runtime aceita `followup_task` somente com um envelope governado. Ele exige que o turno anterior
esteja terminal e compara o target ao `agent_id` anterior quando esse ID existe
([linhas 6468–6501](../implementations/server/runtime/service.py#L6468)). Entretanto,
`complete_host_workflow_turn` permite concluir sem `agent_id` quando não há producer output
([linhas 6680–6723](../implementations/server/runtime/service.py#L6680)). Quando o `agent_id` anterior
é `NULL`, a comparação do target não roda. A regra "follow-up vai ao agente previamente ligado" fica,
nesse caso, mais fraca do que o contrato declara.

A fotografia do SQLite local em 2026-09-02 mostra `39` linhas em
`host_workflow_turn_bindings`: `37` Codex e `2` Claude; todas são `spawn`; `0` têm
`turn_ordinal > 0`; `36` estão `resolved` e `3` em `error`. Isso não prova que follow-up seja
impossível, mas prova que o piloto persistido não demonstra um único follow-up ligado.

### 5. Compatibilidade virou substituto operacional do caminho governado

O [ledger atual](../telemetry/agents/subagents-dispatch.yaml) contém `164` aberturas automáticas
Claude e `160` fechamentos correspondentes, além
de `17` aberturas e `17` fechamentos automáticos Codex. Os arquivos de estado locais contêm `177`
estados de compatibilidade `closed`, `40` ainda em `preparing` e somente `17` estados bound-seat
`closed`. São contagens de uma fotografia local, sujeitas a registros históricos e retries; não
devem ser interpretadas como métricas de produção. Mesmo com essa limitação, elas mostram que o
envelope sintético foi muito mais usado do que o binding ao pai.

O hook também precisa inferir correlação no término. Se não encontra um `agent_id`, ele associa um
`SubagentStop` a um único estado ainda não reclamado e compatível com `agent_type`
([linhas 714–742](../implementations/server/runtime/host_dispatch_hook.py#L714)). Isso é uma
heurística necessária porque o protocolo do host não fornece uma identidade causal completa em
todas as fases.

### 6. Governança e contratos cresceram mais rápido que o golden path

O repositório acumulou registry, versions, authority modes, capability routes, tool profiles,
digests, manifests, launch plans, receipts, hook states, ledger rows e journal events. Vários desses
controles preservam propriedades importantes. O problema é que a unidade de progresso passou a ser
"mais uma fronteira formalizada", e não "um dispatch sequencial completo executado e recuperado por
um único caminho".

O teste focado executado nesta análise reforça esse diagnóstico, com uma limitação importante. O
comando abaixo executou 40 testes e terminou com 37 passes e 3 errors:

```powershell
python -B -m unittest implementations.tests.runtime.test_dispatch_workflow `
  implementations.tests.runtime.test_host_dispatch_hook `
  implementations.tests.runtime.test_orchestration_bridge `
  implementations.tests.runtime.test_host_ingestion_hook -v
```

Os três erros não vieram de assertions sobre handoff: todos falharam antes, tentando copiar
`C:\Users\implementation\domainspec\...\append-dispatch.cjs`, caminho absoluto que não existe nesta
máquina. Portanto, o resultado não prova uma regressão funcional nesses três casos. Ele prova que
parte da suite de autoridade `root-v0.8.0` não é portável e que o conjunto focado não está verde no
worktree atual.

## O que não devemos concluir

YAML não é, sozinho, a causa. Um ledger append-only pode ser uma boa projeção de auditoria. O
problema é ele participar como barreira operacional enquanto SQLite também aceita fatos, sem uma
materialização transacional completa.

Hooks também não são, sozinhos, a causa. Eles são uma fronteira útil para negar launches não
autorizados. O erro foi dar ao hook responsabilidades de construção de dispatch de compatibilidade,
correlação, recovery e fechamento que deveriam pertencer a um lifecycle owner.

Nem toda a arquitetura deve ser descartada. Devem ser preservados:

- prompts, manifests e outputs ligados por digest;
- fail-closed em divergência, identidade duplicada ou bytes diferentes;
- receipts idempotentes e releitura exata depois de efeitos externos;
- separação entre evidência, projeção e autoridade;
- um único writer físico para qualquer projeção append-only;
- non-goals honestos: o host não pode alegar que observou inputs ocultos do provider.

## Lições para o recomeço

O novo repositório deve começar com um caminho executável pequeno, e não com a migração das
abstrações atuais.

1. **Uma entrada pública.** Na primeira versão, o agente pai pode continuar escrevendo manualmente
   um único JSON de dispatch. Um único comando/serviço deve receber esse JSON e possuir validação,
   abertura, scheduling, bindings, recovery e fechamento. Não deve exigir que o pai coordene quatro
   CLIs e arquivos derivados.
2. **Um lifecycle owner e uma máquina de estados.** Estado confirmado, grupo pronto, seat em
   execução, output aceito, dependente liberado e dispatch encerrado devem viver sob uma mesma
   autoridade transacional. Isso inclui serializar a admissão de novos launches com a decisão de
   fechar: depois que o fechamento é aceito, nenhum novo binding pode entrar; o close só pode
   confirmar quando não houver trabalho em execução. Colocar essas operações no mesmo store não é
   suficiente se elas ainda puderem intercalar checks e mutações independentes.
3. **Scheduling incremental.** O grafo é confirmado inteiro, mas somente o frontier pronto é
   materializado. Outputs aceitos liberam consumidores e geram seus manifests. Nenhum consumidor
   precisa de um receipt que ainda não pode existir.
4. **Um store autoritativo.** Projeções JSON/YAML podem existir para leitura e auditoria, mas não
   autorizam execução. Se um efeito externo for inevitável, ele parte de uma intent durável e termina
   em acknowledgement verificável. A intent deve carregar uma identidade estável do efeito entre
   retries. Se o host executar e a resposta se perder, o recovery precisa deduplicar o pedido,
   impedir repetições concorrentes ou reconciliar esse efeito antes de tentar novamente. Após um cold
   restart, o sistema ainda deve demonstrar que ocorreu no máximo um launch físico. Se o host não
   oferecer uma garantia suficiente,
   o resultado permanece desconhecido e não pode ser repetido automaticamente.
5. **Sem fallback silencioso.** Depois que um dispatch é confirmado no caminho governado, uma falha
   não pode transformá-lo em dispatches sintéticos independentes. Compatibilidade, se necessária,
   deve ser uma entrada explicitamente escolhida e observável, nunca um mecanismo de recovery. O
   contrato deve injetar uma falha no caminho governado e provar que nenhum dispatch sintético foi
   criado e que o dispatch original permaneceu falho ou recuperável sob a mesma identidade.
6. **Retenção explícita.** O JSON confirmado é evidência imutável; launch plans e manifests são
   derivados; outputs têm ownership e prazo definidos. O sistema deve declarar o que arquiva, o que
   regenera e o que remove.
7. **Golden path antes de expansão.** O primeiro gate deve executar um dispatch real com dois grupos
   sequenciais, persistir o output do primeiro, liberar o segundo, fazer pelo menos um follow-up,
   simular crash em cada efeito externo, reconciliar e fechar sem intervenção manual. Só depois
   entram registry extensível, modos adicionais, overlays e migração de hosts. Esse gate atravessa a
   única API pública e o boundary durável real; não pode pré-gravar receipts, manifests ou estado que
   o lifecycle deveria produzir.

   O teste precisa tornar as garantias observáveis onde o desenho anterior falhou. Um follow-up só é
   autorizado quando a identidade anterior é conhecida e coincide com o target; identidade ausente
   ou divergente falha fechada. A injeção de falhas inclui perda da resposta depois de o host aceitar
   um launch, seguida de cold restart, e uma corrida entre novo bind e fechamento. O resultado aceito
   é no máximo um launch físico, nenhum bind depois da decisão de fechar e nenhum dispatch sintético
   como fallback.

Atualizar uma spec será necessário apenas depois que essas decisões forem tomadas. Escrever primeiro
uma spec maior sobre o modelo atual provavelmente cristalizaria a decomposição que causou o
problema. O próximo artefato útil no novo repositório é um contrato curto do golden path e seus
invariantes, acompanhado imediatamente por um teste end-to-end executável. O contrato não precisa
antecipar toda a especificação do scheduler, mas precisa transformar essas garantias em oracles que
possam reprovar uma implementação nominalmente correta.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Host Agent Dispatch Input Binding](decisions/host-agent-dispatch-input-binding.md) | `contextualizes` | Situa a bridge temporária aceita em 2026-07-25 dentro da evolução e dos problemas sistêmicos posteriores. |
| [Dispatch audit-ledger cutover contract](features/agents-communication-infra/discovery/dispatch-audit-ledger-cutover-contract.md) | `contextualizes` | Compara o contrato de autoridade e recovery proposto com o caminho cross-store efetivamente implementado. |

## Registro de evidência e limites

| Constatação | Evidência | Limite da evidência |
|---|---|---|
| O agente pai, não um serviço, forma o dispatch | As skills mandam selecionar a capability, construir o registro concreto e entregá-lo ao lifecycle; o CLI só resolve, compila, abre e fecha. | Instrução e código do repositório atual; outro cliente externo pode construir JSONs. |
| A bridge de binding nasceu como solução temporária | [ADR aceita de 2026-07-25](decisions/host-agent-dispatch-input-binding.md#L75). | A ADR registra intenção, não a adoção efetiva de todos os non-goals. |
| O cutover para autoridade runtime não foi autorizado | [Contrato proposto, linhas 1–9 e 54–61](features/agents-communication-infra/discovery/dispatch-audit-ledger-cutover-contract.md#L1). | Documento de contrato; a fotografia local não prova estado de hosts externos. |
| A bridge cruza YAML e SQLite em etapas separadas | [`orchestration_bridge.py`](../implementations/server/runtime/orchestration_bridge.py#L274). | Análise estática do worktree atual, corroborada pelos testes de failpoint existentes. |
| O preflight de close não testa running bindings | [`service.py`, preflight](../implementations/server/runtime/service.py#L2328) versus [aceitação](../implementations/server/runtime/service.py#L2209). | Janela demonstrada pelo código; esta análise não reproduziu o incidente em um teste dedicado. |
| O handoff sequencial local cria uma dependência circular | Diff não commitado de `dispatch_workflow.py`: receipt exigido antes da geração dos launches. | Refere-se ao worktree de 2026-09-02, não ao `HEAD`; pode mudar antes de commit. |
| O piloto persistido não demonstra follow-up bound | Query read-only em `telemetry/runtime/local-pilot/aci-apt-stage-c.sqlite3`: 39 bindings, todos spawn, 0 com turno > 0. | Fotografia local e histórica; ausência de evidência não prova impossibilidade. |
| O caminho de compatibilidade domina a fotografia local | Contagem do ledger e de `telemetry/runtime/local-pilot/orchestration-hooks/**/*.json`. | Contém histórico, retries e possíveis estados abandonados; não é telemetria de produção. |
| A suite focada não está verde | 40 testes: 37 passes, 3 errors por fixture com caminho absoluto inexistente. | Não é a suite completa e os errors não exercitaram a assertion funcional pretendida. |
| A autoria de `subagents-dispatch-lifecycle` é rastreável, mas a decisão não | `git log --follow --diff-filter=A`: commit `f309972`, Victor Boscaro, mensagem `qualquer coisa`. | Autoria Git não prova autoria intelectual exclusiva nem motivação. |

Esta retrospectiva atribui causas ao desenho e ao processo, não a uma pessoa. A própria história
mostra decisões razoáveis tomadas sob necessidades imediatas. O erro repetido foi aceitar cada
bridge como adição sem definir qual camada anterior ela tornava desnecessária. O recomeço deve
inverter essa regra: uma nova abstração só entra se reduzir o número de autoridades e tornar o
golden path mais curto, observável e recuperável.
