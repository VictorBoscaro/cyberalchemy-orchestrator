---
tags: [agent-reasoning-engine, agents-communication-infra, canonical-form, journal, effect-intent, cross-repository]
artifact_kind: research-initial-definitions
layer: feature
version: 0.1.0
created_at: 2026-08-04T13:07:57-03:00
updated_at: 2026-08-04T13:07:57-03:00
veracity: medium
conviction: high
---

# Agent Reasoning Engine — ACI Integration Viability — Research Initial Definitions

## Context

O repositório `cyberalchemy-orchestrator` desenvolve infraestrutura para manter o trabalho de
agentes ligado aos objetivos, decisões, suposições, ações e evidências que lhe dão sentido. A
feature `agents-communication-infra` é onde essa infraestrutura vira runtime: um journal de fatos
aceitos, identidade canônica endereçada por conteúdo, replay, intenções de efeito e uma fronteira
de confirmação humana que separa o que é proposta do que é autoridade.

Um sistema irmão, o `agent-reasoning-engine`, foi construído no repositório privado
`domainspec-core` sob o projeto `cyberAlchemy-v2`. Ele produz um juízo semântico — uma
recomendação sobre o que deveria ser feito — e termina deliberadamente sem autorizar nada. O
trabalho dele nasceu apontando para este repositório: a pesquisa de origem foi conduzida contra
este código em 2026-07-22, e a decisão de arquitetura que se seguiu declarou que ciclo de comando e
evento, identidade canônica de aceitação, cursor de replay e intenções de efeito pertencem ao ACI.
Essa decisão registra este repositório como dependência externa aberta. O problema local, portanto,
não é escolher se vale integrar em abstrato: é estabelecer o que a integração exigiria do ACI, o
que ela já poderia apoiar hoje e o que permanece impossível de saber sob os portões atualmente
fechados. Sem isso, o repositório irmão fica bloqueado num compromisso que nunca foi avaliado deste
lado, e este repositório corre o risco de receber um segundo produtor de registros sem ter decidido
quem é o dono da fronteira que os dois compartilham.

## Purpose

Este documento estabelece o contexto informacional para uma pesquisa governada sobre a viabilidade
de integrar o `agent-reasoning-engine` ao runtime ACI. Seus resultados informarão uma decisão
posterior sobre a disposição de autoridade entre os dois sistemas, o desenho de qualquer seam
entre eles e a revisão — deste lado — do compromisso `ACI-BIND-A-SUBORDINATE` já registrado do
lado irmão.

Ele não configura a pesquisa. Vocabulário candidato, hipóteses, recorte de fontes, topologia de
agentes e contratos de saída pertencem ao desenho posterior, não a este documento.

## Research Question (Can be refined)

O que a integração do `agent-reasoning-engine` ao runtime ACI exigiria de journal, replay,
identidade canônica, artefatos e intenções de efeito; quanto disso é apoiável pelo estado atual do
ACI; e quais partes permanecem indecidíveis enquanto os portões de produção e de escritor único
seguem fechados?

## Confirmed Product Constraints

- O escopo desta pesquisa é a viabilidade da integração inteira — journal, replay, intenção de
  efeito e os mapeadores de fronteira — escolhido explicitamente pelo dono em 2026-08-04, com a
  objeção de cobertura parcial registrada e aceita.
- Pontos que dependem de portões fechados devem ser entregues nomeados como bloqueados, não
  resolvidos por suposição nem omitidos.
- `productionEnablement` permanece em **block**: rede externa, execução de provedor, materializer e
  cutover do audit-ledger estão fora de qualquer autorização
  ([WORK-PACK](../../WORK-PACK.md)).
- A prova de escritor único (EG-1) não está fechada; o materializer e o cutover continuam
  bloqueados até `SoleWriterEvidenceBundle` completo ([WORK-PACK](../../WORK-PACK.md), D-012).
- A compilação de protocolo termina num `DispatchCandidate` não-autoritativo; resolução de
  capacidade, `DispatchSpec` final, confirmação, `ConfirmedDispatch` e `Run` permanecem com a
  confirmação e o runtime
  ([ACI-PG-001](../../../../decisions/aci-protocol-governance-ownership.md)).
- Nenhuma ferramenta externa recebe posse do kernel ou de store autoritativo (D-010); nada vira
  segunda fonte de verdade nem segundo escritor.
- A pesquisa é conduzida sobre um repositório irmão privado; o moat privado do `domainspec-core`
  não pode ser publicado.

## Current Evidence Baseline

- A pesquisa de origem sobre o motor de raciocínio foi conduzida contra este repositório e já
  registrou a confrontação entre runtime replayável e contrato semântico, concluindo que registrar
  prompt e recibo não transfere posse de inferência ao repositório
  ([pesquisa 2026-07-22](../../../../research/2026-07-22-agent-reasoning-engine-contract/research.md)).
- O lado irmão registrou a decisão `G-ARE-ACI-BINDING-20260723` com veredito PASS e opção
  `ACI-BIND-A-SUBORDINATE`, declarando `Implementation authorized: false` e nomeando ACI, Bus, ACP e
  APT como dependências externas abertas
  (`domainspec-core/cyberAlchemy-v2/development/agent-reasoning-engine/decisions/aci-reasoning-binding/DECISION.md`).
- O mesmo conjunto registra uma opção perdedora já especificada, `ACI-BIND-D-STANDALONE-REROUTE`,
  que abandona a direção de integração e retém apenas o redutor semântico como biblioteca.
- A arquitetura candidata do lado irmão nomeia cinco mapeadores de fronteira — comando de execução,
  eventos de ator, referência de recibo, comando de efeito exato e ponte de replay — e um envelope
  cross-boundary com referências de dispatch, comando, run semântico, recibo e efeito
  (`domainspec-core/cyberAlchemy-v2/development/agent-reasoning-engine/design/aci-reasoning-binding/ARCHITECTURE.md`,
  225 linhas).
- O motor tem implementação executável de 1.890 linhas em `.mjs` sob
  `domainspec-core/cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/semantic-judgment-evaluator/`,
  com testes, e recibos gerados em `generated/runs/evaluator-v1-20260723T-session-001/`.
- Um `ReasoningReceipt` gerado carrega `runtime_journal_cut`, `entry_gate_decision_digest`,
  `input_digests` por documento, `claim_ceiling` em prosa e `terminal_outcome`
  `RecommendedUnderSnapshot`.
- Este repositório congelou sua forma canônica como `aci-cjson-1`
  ([canonical.py](../../../../../implementations/server/runtime/canonical.py)), com normalização NFC
  de strings e chaves, rejeição de colisão de chaves pós-NFC, rejeição de float binário, limite de
  inteiro em signed int64, ordenação de chaves por code point e digest qualificado `sha256:<hex>`.
- O motor de raciocínio usa uma canonicalização própria
  (`domainspec-core/cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/semantic-judgment-evaluator/src/canonical-json.mjs`,
  84 linhas) sem normalização Unicode, que aceita qualquer número finito, não impõe limite de
  inteiro, ordena chaves por code unit UTF-16 e emite digest em hex puro. As duas regras divergem
  nesses pontos quando lidas lado a lado; nenhuma execução conjunta dos dois sistemas ocorreu, e
  esta linha registra divergência observada em código-fonte, não um conflito reproduzido.
- O seam de persistência já existente neste repositório compara o hash calculado pelo ArtifactStore
  com o digest declarado e falha fechado em `artifact_content_conflict`
  ([protocol-compilation](../../specs/protocol-compilation.md), seam de artefato).
- O runtime local tem journal, migrations SQLite, artifacts, capabilities, projections, provenance
  e reveal/delivery implementados sob `implementations/server/runtime/`, com 131 testes de runtime
  passando em 2026-08-04.
- O inventário de migração runtime-v2 levantou o estado arquitetural do runtime do qual esta linha
  de trabalho parte
  ([inventário](../runtime-v2-migration-inventory/research-initial-definitions.md)).

## Known Gaps

- Não está estabelecido se os bytes de um recibo semântico efetivamente atravessam a fronteira de
  aceitação do ACI em algum caminho previsto, nem sob qual forma canônica eles atravessariam.
- Não está estabelecido se `ReasoningReceipt` e `DispatchCandidate` são dois tipos de registro com
  donos distintos ou um tipo com dois produtores.
- Não está estabelecido o que o journal do ACI exige de um escritor externo, nem se o motor precisa
  do journal ou apenas de artefatos endereçados por conteúdo.
- Não está estabelecido o que `runtime_journal_cut` denota em termos do offset e do cursor de
  replay realmente implementados aqui.
- Não está estabelecido quanto do caminho de intenção de efeito é sequer avaliável enquanto
  `productionEnablement` e EG-1 seguem fechados, nem quais perguntas ficam suspensas em vez de
  respondidas.
- Não está estabelecido se os cinco mapeadores propostos correspondem a fronteiras que existem
  neste repositório ou a fronteiras que ainda teriam de ser criadas.
- Não está estabelecido se as premissas que sustentaram `ACI-BIND-A-SUBORDINATE` em 2026-07-23
  permanecem válidas após a ratificação de ACI-PG-001 em 2026-08-03.
- Não está estabelecido se o `claim-graph` no vault já ocupa, deste lado, o papel semântico que o
  motor de raciocínio ocupa do outro.
- Não está estabelecido qual repositório sediaria qualquer seam resultante, nem sob qual
  disciplina de submódulo ou fronteira público/privado.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [pesquisa 2026-07-22](../../../../research/2026-07-22-agent-reasoning-engine-contract/research.md) | `derives-from` | Esta pesquisa parte do contrato semântico e da confrontação já registrados ali; a pergunta de viabilidade existe porque aquele trabalho terminou sem resolver a posse da fronteira. |
| [ACI-PG-001](../../../../decisions/aci-protocol-governance-ownership.md) | `depends-on` | O teto de autoridade do `DispatchCandidate` delimita o que um segundo produtor de registro não-autoritativo poderia reivindicar; sem esse teto as restrições deste documento não se sustentam. |
| [WORK-PACK](../../WORK-PACK.md) | `depends-on` | Os portões `productionEnablement` e EG-1 determinam quais partes do escopo são avaliáveis; a delimitação do que entra bloqueado vem daí. |
| [protocol-compilation](../../specs/protocol-compilation.md) | `depends-on` | A forma canônica `aci-cjson-1` e o seam de artefato especificados ali são a referência contra a qual a canonicalização do motor irmão foi lida. |
| [inventário runtime-v2](../runtime-v2-migration-inventory/research-initial-definitions.md) | `derives-from` | O estado arquitetural do runtime de que esta pesquisa parte foi levantado naquele inventário. |

As fontes do repositório irmão `domainspec-core` são citadas por caminho no corpo do documento e
não aparecem como arestas: elas estão fora deste repositório e um link relativo seria quebrado.
As linhas inversas ainda não foram escritas nos alvos — ver nota de autoria abaixo.

> Nota de autoria: `protocol-compilation.md` está fixado por SHA-256 no índice de contexto de
> `SWU-ACI-PROTOCOL-COMPILATION-001`, atestado pelo recibo de readiness reemitido em 2026-08-03;
> editá-lo para inserir a aresta inversa invalidaria esse pino. `ACI-PG-001`, `WORK-PACK.md` e o
> inventário runtime-v2 ainda não possuem seção `## Connections`, e a pesquisa de 2026-07-22 usa
> formato de lista sem frontmatter. As arestas recíprocas ficam pendentes de uma migração própria
> desses documentos.
