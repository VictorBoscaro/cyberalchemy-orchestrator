# Avaliação independente B — próximo foco de integração com a SPEC

Data: 2026-07-22  
Escopo: `agents-communication-protocols` (ACP), `bus-contracts` (BC), baseline DomainSpec, plano W0 e probe existente.  
Natureza: recomendação independente; não altera autoridade nem gates existentes.

## Recomendação executiva

O próximo foco deve ser uma única fatia read-only: **publicação oficial de um relatório de
trabalho por receipt**. Em forma operacional:

```text
um assignment fixo de pesquisa
  -> submit_work/bus_publish com um research report tipado
  -> PublicationCandidate persisted_candidate
  -> PublicationReceipt byte-stable
  -> verificação independente pelo parent
  -> CAS de aceitação oficial
  -> Contribution oficial, consumível apenas pelo parent declarado
```

Chamo esta fatia de **WP-1 — Official Work Publication**. Ela não inclui review, routing genérico,
rework, handoff, `Skill Execution Profile`, `JudgmentRound`, workspace mutável nem artifact service
completo.

A escolha não inventa um novo kernel: a SPEC já ratifica append-before-ack e verificação pelo parent
(`specs/SPEC.md`, linhas 81–83), já modela `PublicationCandidate` como diferente de `Contribution`
(`specs/domain.md`, linhas 108–156) e já define o workflow candidate -> receipt -> aceitação oficial
(`specs/workflows.md`, linhas 82–115). O trabalho novo é fechar a interface semântica entre ACP, BC e
esses contratos e fazer o probe obedecê-los.

## 1. O que existe hoje e qual é sua autoridade

| Superfície | Existe hoje | Maturidade / autoridade |
|---|---|---|
| Ledger/appender, leitor FastAPI e SSE por mudança em disco | Implementação real existente | É infraestrutura legada/parcial; não constitui runtime entre agentes e não oferece journal, retries, reveal ou state machine (`README.md`, linhas 94–117). |
| SPEC modular v0.2.0 | Contratos detalhados de dispatch, journal, attempts, receipt gate, reveal, replay e fechamento | É a baseline de especificação, mas continua `status: draft` e `runtimeGate: block`; a autoria passou, a implementação não foi autorizada (`specs/SPEC.md`, linhas 1–24). |
| W0 / TASK-000 | Plano de decisões pré-código | É o gate operacional vigente. `workPackGateStatus=block`, apenas W0 documental está autorizado (`WORK-PACK.md`, linhas 17–42). |
| ADR-001 e fixtures | Decisão de persistência, canonical bytes, replay e crash obligations | `SWU-ACI-001` foi aceito apenas em escopo de decisão; não prova runtime nem abre TASK-010 (`adrs/ADR-001-persistence-replay-and-canonical-contracts.md`, linhas 330–365; `reviews/2026-07-21-swu-aci-001-implementation/REPORT.md`, linhas 34–39). |
| Restante de W0 | SWU-ACI-002: decision/terminal/snapshot, reconciliação do ledger e cutover | Não está concluído. W0 só sai quando ADRs, golden trace, fixtures, drift/sole-writer guard e promoção deliberada do gate existirem (`work-pack/waves/W0.md`, linhas 8–16; `work-pack/tasks/TASK-000.md`, linhas 37–62). |
| Probe `bus-publication-probe` | MCP `bus_publish`, JSONL append-before-ack, receipt e verificador do parent | É experimento, não runtime. Seu README exclui SQLite, multi-writer safety, full state machine, reveal e sandbox (`experiments/bus-publication-probe/README.md`, linhas 78–88). A suite local executada nesta avaliação passou 10/10, cobrindo os casos enumerados nas linhas 17–35, mas isso prova somente o contrato do probe. |
| ACP v0.3.0 | Hipótese do ciclo completo e do `Skill Execution Profile` | Discovery `draft`, `veracity: low`; declara expressamente que o profile não é schema ratificado e que recipes mutantes estão fora da SPEC atual (`discovery/agents-communication-protocols/README.md`, linhas 1–10 e 51–68). |
| BC v0.3.0 | Hipótese aprofundada do Work Bus | Discovery `draft`; declara que não altera a SPEC e que nomes não devem ser promovidos imediatamente (`discovery/bus-contracts/README.md`, linhas 1–39 e 617–24). O review disponível teve verdict `FIX`, embora o texto atual aparente incorporar os pedidos (`reviews/2026-07-22-bus-contracts/review.md`, linhas 20–43 e 56–72); não encontrei receipt posterior de closure. |
| Interface ACP↔BC | Estatuto acordado, mas artefato ainda inexistente | O acordo rejeitou fusão imediata, dividiu ownership e exigiu integrador estreito/versionado para mappings e invariantes cruzados (`discovery/document-unification-debate/common-agreement.md`, linhas 10–19 e 71–94). |

Conclusão de maturidade: há contratos especificados e um probe útil, mas ainda não há um
runtime autorizado nem uma ponte revisada que diga como um "output de trabalho" de ACP/BC se torna
uma `Contribution` da SPEC.

## 2. Por que WP-1 é a menor fatia coerente

### 2.1 Ela fecha uma lacuna real e imediatamente observável

O probe atual conflita com a SPEC em um ponto de autoridade, não apenas de nomenclatura:

- ele cria receipt com `status: "accepted"` durante o append (`experiments/bus-publication-probe/src/bus.mjs`, linhas 169–206);
- seu verificador apenas localiza um evento e compara quatro campos, depois o declara aceito
  (`experiments/bus-publication-probe/src/bus.mjs`, linhas 214–237;
  `src/verify-result.mjs`, linhas 12–18);
- a SPEC exige receipt com `status=persisted_candidate`, que nunca afirma aceitação oficial
  (`specs/domain.md`, linhas 339–355; `specs/interfaces.md`, linhas 150–165);
- a aceitação oficial é uma segunda transação/CAS que cria a `Contribution`; candidate sozinho não
  conta (`specs/persistence-and-replay.md`, linhas 320–364).

Logo, os 10 testes verdes atuais não demonstram conformidade com a SPEC. A hipótese forte
"o wiring atual implementa o receipt gate normativo" já é refutada por inspeção: existe um trace em
que persistir a candidata retorna `accepted` sem o segundo fato oficial.

### 2.2 Ela é a interseção de maior valor entre os discoveries

ACP requer que retornos compilem para `Contribution` com artifact imutável e que reviews se liguem a
uma versão exata (`discovery/agents-communication-protocols/README.md`, linhas 369–398). BC define a
mesma fronteira em maior resolução: candidata durável, receipt, submissão oficial e release separado
(`discovery/bus-contracts/README.md`, linhas 41–109). O acordo comum reconhece exatamente esse
acoplamento e diz que testes locais não bastam para invariantes cruzados
(`discovery/document-unification-debate/common-agreement.md`, linhas 21–41).

WP-1 cria uma prova ponta a ponta que poderá governar já o tipo de trabalho feito por subagentes
read-only: relatórios. Não precisa resolver alteração de worktree, merge, adjudicação ou topologia.

### 2.3 Ela é menor e mais informativa que as alternativas

- **`Skill Execution Profile`: não agora.** ACP ainda o chama de hipótese, possui 34 perguntas abertas
  e exige trust anchor, registry, manifests, bindings, compiler e snapshots
  (`discovery/agents-communication-protocols/README.md`, linhas 165–226 e 437–485). A baseline adia
  recipes/compilador genérico para L4 (`IMPLEMENTATION-LAYERING.md`, linhas 37–41).
- **Routing/rework/review completo: não agora.** BC requer `RoutingPlan`, `RoutingState`, generations,
  manifests de consumo e release gates (`discovery/bus-contracts/README.md`, linhas 345–429 e
  517–551). Isso multiplica estados antes de provar o primeiro resultado oficial.
- **Implementation/workspace: não agora.** Baseline isolado, `ChangeSetArtifact`, promote atômico e
  quarentena são outro tema de risco (`discovery/bus-contracts/README.md`, linhas 172–194). A
  arquitetura também adia recipes mutantes (`README.md`, linhas 1087–1096).
- **`JudgmentRound`: não agora.** A policy exige freeze, sealed submission, reveal, agregação e nova
  rodada (`discovery/agents-communication-protocols/README.md`, linhas 330–367); julgamento selado
  genérico está fora dos primeiros slices (`README.md`, linhas 1093–1096).
- **Implementar todo L0: obrigatório depois, mas não é uma boa unidade de integração dos novos
  discoveries.** L0 prova uma run fixa completa, com journal, audit opening, fake adapters, reveal,
  vote, commit e replay (`README.md`, linhas 1044–1062). WP-1 é um probe contratual menor que reduz
  risco antes dessa implementação, sem alegar que abre seu gate.

Formalmente, seja `C` o custo/número de superfícies novas e `I` o número de invariantes cruzados
diretamente exercitados. WP-1 toca uma operação, um output schema, uma candidata, um receipt, uma
aceitação e um consumer fixo, enquanto exercita os invariantes centrais de ACP↔BC↔SPEC. Routing,
profiles e review acrescentam superfícies sem serem necessários para falsificar o receipt gate. Até
existir evidência contrária, WP-1 domina essas alternativas na razão qualitativa `I/C`.

## 3. Contratos a promover agora — e contratos a manter em discovery

### 3.1 Promover primeiro para o integrador ACP↔BC, não duplicar conceitos na SPEC

O primeiro artefato normativo deve ser a interface estreita prevista no acordo, inicialmente `draft`.
Ele deve conter somente este mapping:

| Origem ACP | Operação BC | Conceito SPEC | Invariante cruzado WP-1 |
|---|---|---|---|
| uma atividade read-only de pesquisa, um assignment e seu output tipado | fachada `submit_work` com um único `OutputContract` `research-report@1` | `BusPublication` + `PublicationCandidate` | o agente fornece somente o relatório semântico; autoridade vem do contexto autenticado |
| submissão persistida | candidate persistida | `PublicationReceipt(status=persisted_candidate)` | append-before-ack não equivale a aceitação oficial |
| retorno terminal do worker | verificação independente | `VerifyPublicationReceipt` | igualdade de todos os campos, scope autenticado e candidate ativa |
| output oficial | work submission aceita | `Contribution` | só o segundo fato/CAS libera o parent fixo |

Esse formato segue o estatuto acordado: mapping pinado, status/compatibility/probe, fail-closed e sem
reexplicar os donos locais (`common-agreement.md`, linhas 71–94).

### 3.2 Contratos elegíveis para ratificação nesta fatia

1. **Payload semântico mínimo e autoridade server-derived.** BC linhas 149–170; já é consistente
   com `BusPublication`, que exclui campos de autoridade (`specs/domain.md`, linhas 324–337).
2. **Candidate != receipt != official contribution.** BC linhas 62–94; já coincide com
   `PublicationCandidate` e o workflow da SPEC (`specs/domain.md`, linhas 130–156;
   `specs/workflows.md`, linhas 91–105).
3. **Receipt canônico persistido e retry byte-idêntico.** BC linhas 81–94 e 139–142; já coincide
   com `PublicationReceipt` (`specs/domain.md`, linhas 339–355).
4. **Uma capability/operation/schema fail-closed para WP-1.** BC separa operações por capabilities e
   schemas (`discovery/bus-contracts/README.md`, linhas 373–425). Nesta fatia, registrar apenas
   `submit_work:research-report@1`; não registrar `submit_review` ainda.
5. **Um único release gate fixo:** somente a aceitação oficial libera o parent declarado. A taxonomia
   genérica de consumers permanece fora, mas a distinção entre candidate e resultado consumível é
   promovida (BC linhas 96–109).

Esses itens não precisam criar `WorkSubmission` paralelo a `Contribution`. Para WP-1, `submit_work`
é fachada semântica compilada para os contratos ratificados da SPEC. Um novo tipo de domínio só se
justifica se um probe demonstrar semântica que `Contribution` não consegue preservar.

### 3.3 Não promover nesta fatia

- schema completo de `Skill Execution Profile`, `skill_id`, compiler, registry/binding,
  supersession/revocation e trust anchor;
- activity descriptor genérico e taxonomia final de roles;
- `JudgmentRound`, consensus, final approver e policy universal de eligibility;
- `submit_review`, `ReviewProfile`, remediation routing, rework generations e replacement;
- `RoutingPlan`, `RoutingState`, `ConsumerInputManifest` e fan-out/quorum;
- `work_kind` genérico e encadeamento research -> implementation;
- `ExecutionObservationManifest`, retenção/pinning geral e knowledge seam funcional;
- implementation payloads, `ChangeSetArtifact`, workspaces isolados e promote/merge;
- nomes novos que apenas renomeiem `Artifact`, `Contribution`, `DispatchSpec` ou `PublicationReceipt`.

O motivo não é que sejam irrelevantes; é que os próprios discoveries condicionam promoção a
probes e review. ACP exige review independente antes da promoção (`agents-communication-protocols`,
linhas 735–751) e BC exige crash/retry, reconstruction, routing, isolation e capability-matrix probes
antes de propor mudanças (`bus-contracts`, linhas 626–642).

## 4. Dependências e riscos

### Dependências duras

1. **Não mudar o gate por inferência.** Runtime continua bloqueado até o W0 completo; o ADR-001
   sozinho não autoriza TASK-010 (`WORK-PACK.md`, linhas 101–109 e 152–157).
2. **Criar o integrador X antes da emenda da SPEC.** O acordo diz explicitamente que schema,
   população, owners e probes ainda não foram feitos (`common-agreement.md`, linhas 89–94).
3. **Usar canonical bytes da autoridade, não o canonicalizer simplificado do probe.** O probe apenas
   ordena chaves e usa `JSON.stringify` (`src/bus.mjs`, linhas 13–25); ADR-001 define NFC, omissão vs
   null, números, encoding e digest completo (`ADR-001`, linhas 248–297).
4. **Fixar um único schema e um único consumer.** Isso impede que routing e registry entrem
   implicitamente na fatia.

### Riscos principais

- **Falso verde:** repetir os 10 testes existentes e chamar o probe de conformante, mesmo com
  `accepted` prematuro.
- **Terceira autoridade:** criar `WorkSubmission` ou receipt alternativo que duplique `Contribution`
  ou `PublicationReceipt`.
- **Scope creep:** incorporar review/routing porque o documento BC os descreve na mesma página.
- **Gate laundering:** chamar código experimental de runtime para contornar W0.
- **JSONL como prova de atomicidade:** o probe reconhece que não prova SQLite/multi-writer safety
  (`experiments/bus-publication-probe/README.md`, linhas 78–88).
- **Cobertura retroativa:** o review BC tem `FIX` e não deve ser convertido em `PASS` porque o texto
  parece remediado; precisa closure sobre bytes/digest exatos.

## 5. Falsificadores e critérios verificáveis de saída

WP-1 falha se qualquer um destes traces for possível:

1. `persist(candidate)` produz receipt que afirma `accepted`/official.
2. candidate ou receipt sozinho libera o parent antes do segundo fato de aceitação.
3. receipt missing, forjado, alterado, cross-scope, stale ou de candidate abandonada cria
   `Contribution`.
4. retry idêntico produz bytes/evento diferentes; mesmo key com digest diferente não conflita.
5. payload do agente consegue afirmar run/seat/attempt/phase/recipient.
6. segunda idempotency key contorna unicidade lógica.
7. crash/restart entre candidate e aceitação duplica a contribuição ou a perde como evidência.
8. output de outro schema/operação é aceito por `submit_work:research-report@1`.
9. consumidor não declarado consegue ler o report.
10. replay/projeção é necessário para inventar um fato ausente do journal.

Critérios de saída verificáveis:

- interface X possui uma única linha WP-1, refs com digest, status, compatibilidade, probe e decisão;
- todos os nomes ACP/BC estão mapeados a conceitos SPEC existentes ou marcados `unresolved`, nunca
  aceitos por semelhança textual;
- receipt exato usa `status=persisted_candidate`, e replay metadata fica fora dos bytes canônicos;
- aceitação oficial é um fato separado e idempotente, com teste negativo que prova que candidate
  não conta;
- os dez falsificadores acima possuem nomes estáveis e passam no harness;
- há um piloto real com um subagente read-only publicando um report, e o parent rejeita uma resposta
  terminal equivalente sem receipt;
- review independente fecha a linha X e o probe em baseline exata;
- a emenda da SPEC adiciona somente a especialização/mapping necessária; nenhum conceito local de
  ACP ou BC é copiado;
- `runtimeGate` e `workPackGateStatus` permanecem `block` até a saída independente de W0.

## 6. Sequência prática curta

1. **Definir WP-1 no integrador ACP↔BC.** Uma linha de mapping, pins exatos, precedência e os dez
   falsificadores; status inicial `draft/unresolved`.
2. **Escrever o contrato de teste antes do wiring.** Congelar `research-report@1`, payload
   agent-authored, contexto server-derived, receipt e dois fatos: `candidate.persisted` e
   `submission/contribution.accepted`.
3. **Evoluir o probe para v2 em escopo experimental.** Substituir `accepted` prematuro, implementar a
   aceitação separada e ampliar verificação para todos os campos/scope; manter um consumer parent
   fixo. Não alegar atomicidade de produção enquanto usar JSONL.
4. **Executar harness + piloto real + review independente.** Preservar a baseline exata e registrar
   limitações. Se qualquer falsificador falhar, WP-1 permanece discovery.
5. **Promover somente a interface provada.** Emendar SPEC/mappings/interfaces e o plano de testes;
   não promover os contratos listados em 3.3.
6. **Em paralelo administrativo, concluir SWU-ACI-002/W0.** Só depois de W0 deliberadamente `pass`
   o contrato WP-1 pode entrar como implementação de runtime; até lá, ele é evidência de
   integração e wiring experimental.

## Decisão em uma frase

**Não tentar integrar os dois discoveries inteiros: primeiro tornar um único research report
oficial somente depois de candidate persistida, receipt exato e aceitação independente, alinhando o
probe com a SPEC e usando a interface ACP↔BC como única nova autoridade cruzada.**
