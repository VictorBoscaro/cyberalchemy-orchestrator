# Avaliação independente — próximo foco para integração com a SPEC

## Conclusão executiva

O próximo foco deve ser uma única feature estreita: **Publication-to-Contribution Bridge para
outputs read-only de pesquisa** (`ACI-X1`). Ela congela e prova o caminho:

```text
output semântico do agente
  -> BusPublication autenticada
  -> PublicationCandidate persistida
  -> PublicationReceipt
  -> verificação independente pelo parent/runtime
  -> Contribution oficial
```

Essa não é a implementação de todo o Work Bus, de routing/rework ou do Skill Execution Profile.
É o menor ponto em que os dois discoveries realmente encontram contratos já ratificados na SPEC:
ACP exige que o retorno do worker compile para `Contribution` com `Artifact` imutável
([ACP, linhas 369–398](../agents-communication-protocols/README.md#input-contracts-submiss%C3%B5es-e-review));
BC define o lifecycle candidate→receipt→accepted
([BC, linhas 62–94](../bus-contracts/README.md#lifecycle-de-publica%C3%A7%C3%A3o-oficial)); e a SPEC já possui
`PublicationCandidate`, `BusPublication`, `PublicationReceipt`, `PublishBusContribution` e
`VerifyPublicationReceipt` como conceitos normativos
([SPEC, linhas 130–156 de domain.md](../../specs/domain.md#publicationcandidate),
[linhas 324–355](../../specs/domain.md#buspublication) e
[operations.md, linhas 289–406](../../specs/operations.md#publishbuscontribution)).

O trabalho imediato é de contrato, fixture e probe. Ele **não autoriza runtime code**: a SPEC tem
`runtimeGate: block` ([SPEC.md, linhas 7–22](../../specs/SPEC.md#what-this-module-owns)) e o work pack
autoriza somente documentos/ADRs enquanto W0 não fechar
([WORK-PACK.md, linhas 17–42](../../WORK-PACK.md#control-fields)). ACI-X1 deve ficar preparado para
ser o primeiro wiring do bus dentro de S-001 depois do gate W0, não virar uma exceção a ele.

## 1. O que existe hoje, autoridade e maturidade

| Camada | O que existe | Maturidade e autoridade |
|---|---|---|
| Fluxo legado | Ledger append-only, appender validado, reader/FastAPI/SSE e protocolo humano; o confirm marker foi construído somente para a UI linear. | Implementado parcialmente, mas não é o runtime alvo. O README diz expressamente que faltam bus durável, retries, recovery, state machines e contrato multi-provider ([README.md, linhas 94–119](../../README.md#estado-atual)); o handoff de confirmação ainda deixa a sessão executar a cadeia ([phase-2-confirm-handoff.md, linhas 12–20](../../phase-2-confirm-handoff.md#phase-2--the-confirm-handoff-control-plane--orchestrator)). |
| SPEC modular | Autoridade de runtime, journal, attempts, publicação com receipt, reveal, commit, replay e projeções. | `status: draft`, porém `specAuthoringGate: pass`; contratos estão ratificados, mas são claims não implementadas ([SPEC.md, linhas 1–24](../../specs/SPEC.md#what-this-module-owns) e [66–86](../../specs/SPEC.md#authority-locked-from-discovery-v021)). `runtimeGate: block`. |
| Planejamento de entrega | L0–L4, S-000–S-007, tasks e waves. | Autoridade executável de planejamento, ainda `block`; S-001 depende de S-000 ([WORK-PACK.md, linhas 60–71](../../WORK-PACK.md#delivery-slices)). TASK-000/SWU-ACI-002 e demais obrigações W0 ainda faltam ([WORK-PACK.md, linhas 101–109](../../WORK-PACK.md#blockers); [TASK-000, linhas 37–62](../../work-pack/tasks/TASK-000.md#swu-aci-002--compatibility-ledger-and-protocol-adr-set)). |
| ADR-001 | SQLite/WAL, transação atômica, replay e bytes canônicos. | `accepted-by-independent-review` somente no escopo decisório W0; não prova código, recovery ou migrations e não muda o gate ([ADR-001, linhas 1–27](../../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#status-and-decision-boundary)). |
| Probe de publicação | MCP `bus_publish`, contexto derivado, append JSONL antes do receipt e verificação pelo parent. | Evidência experimental real e estreita. A suite local passou 10/10 nesta avaliação; os casos declarados estão nas linhas 17–35 do [README do probe](../../experiments/bus-publication-probe/README.md#run-the-contract-tests). Não prova SQLite, sandbox, multi-writer, reveal ou runtime completo ([linhas 78–88](../../experiments/bus-publication-probe/README.md#what-this-provesand-what-it-does-not)). |
| ACP | Semântica ampla: Skill Execution Profile, decomposição, roles, julgamento, review e rework. | Discovery `draft`, `veracity: low`, versão 0.3.0 ([ACP, linhas 1–12](../agents-communication-protocols/README.md)). O próprio documento proíbe tratar suas hipóteses como schema ratificado ([linhas 58–68](../agents-communication-protocols/README.md#hip%C3%B3tese-de-superf%C3%ADcie-%C3%BAnica-para-skills)) e exclui alterar SPEC/runtime ([linhas 724–733](../agents-communication-protocols/README.md#fora-de-escopo-neste-momento)). |
| BC | Contratos candidatos de submissão, consumo, artifacts, routing, review, rework e workspace. | Discovery `draft`, versão 0.3.0, sem autoridade para alterar a SPEC ([BC, linhas 1–39](../bus-contracts/README.md#rela%C3%A7%C3%A3o-com-os-documentos-existentes)). O review existente terminou `FIX` com oito gaps ([review, linhas 17–46](../bus-contracts/review/review.md#docsfeaturesagents-communication-infradiscoverybus-contractsreadmemd)); o texto atual incorpora remediações, mas não há receipt posterior de PASS no diretório. |
| Acordo ACP↔BC | ACP fica owner da semântica; BC, da publicação/materialização/routing/consumo; interface cruzada estreita e fail-closed. | Decisão consensual de debate, não emenda da SPEC. Ela manda não fundir agora e criar depois um integrador versionado ([common-agreement, linhas 10–19](../document-unification-debate/common-agreement.md#participantes-e-decis%C3%A3o)); o próprio acordo diz que schema, matriz, owners e probes ainda não existem ([linhas 71–94](../document-unification-debate/common-agreement.md#estatuto-do-futuro-artefato-integrador)). |

Conclusão de maturidade: há um **núcleo normativo bem definido e um probe funcional**, mas não
há runtime nem base probatória para promover a superfície ampla dos discoveries.

## 2. A única feature prioritária: ACI-X1

### Escopo exato

ACI-X1 aceita somente um output read-only de pesquisa, com um `message_type`/schema fechado (por
exemplo `research.individual_report@1`). O agente fornece apenas conteúdo semântico; identidade,
attempt, seat, phase e routing não são campos agent-authored. A publicação cria candidata durável e
receipt; apenas verificação independente cria a `Contribution` oficial. `Contribution` aceita ainda
não é `GroupResult` comprometido e não pode liberar handoff/downstream.

Isso especializa contratos que já existem, sem criar um segundo runtime:

- autoridade derivada e rejeição de identity spoof já são ACI-R2
  ([rules.md, linhas 35–48](../../specs/rules.md#aci-r2--runtime-derived-authority));
- append-before-receipt e parent verification já são ACI-R3
  ([rules.md, linhas 50–67](../../specs/rules.md#aci-r3--append-before-receipt-and-parent-verification));
- a persistência já separa candidata de mensagem oficial e executa CAS de aceitação
  ([persistence-and-replay.md, linhas 320–364](../../specs/persistence-and-replay.md#7-publication-reveal-and-artifact-persistence));
- BC já distingue `submission.accepted` de `work_result.committed`
  ([BC, linhas 96–109](../bus-contracts/README.md#release-gates-por-classe-de-consumidor));
- ACP requer submissão histórica imutável, review da versão exata e nunca autoaprovação no
  loop ceiling ([ACP, linhas 377–398](../agents-communication-protocols/README.md#input-contracts-submiss%C3%B5es-e-review)).

### Por que vem antes das alternativas

1. **Maior interseção de autoridade existente.** ACI-X1 exige quase nenhum vocabulário novo; a
   maior parte do caminho já está na SPEC e no probe. Routing/rework e Skill Execution Profile são
   majoritariamente hipóteses dos discoveries.
2. **Fecha o primeiro risco de wiring real.** Um final de subagente pode existir sem ter virado fato
   oficial; o probe mostra que prompt não basta e que o gate do parent é a barreira efetiva
   ([probe README, linhas 3–15](../../experiments/bus-publication-probe/README.md)).
3. **É uma fatia recomponível de S-001.** S-001 quer uma run determinística que abre, executa,
   compromete, fecha e faz replay exatamente uma vez ([WORK-PACK.md, linhas 60–66](../../WORK-PACK.md#delivery-slices));
   a publicação oficial é um elo necessário desse trace, não uma topologia paralela.
4. **Não puxa L4 para L0.** Recipes `research`/`review` e compiler só entram no L4
   ([IMPLEMENTATION-LAYERING.md, linhas 35–41](../../IMPLEMENTATION-LAYERING.md#layer-decision-table)).
   ACI-X1 usa um schema fixture fixo; não cria registry, recipe genérica ou `work_kind` branch no kernel.
5. **Tem falsificadores baratos.** Missing/forged receipt, retry divergente, duplicate logical key e
   late publication já são exercitáveis. Em contraste, workspace isolado e promote atômico exigem
   infraestrutura mutante deliberadamente posterior ([README.md, linhas 1114–1121](../../README.md#fase-2--robustez-e-topologias)).

## 3. O que promover à SPEC agora

"Promover agora" significa preparar uma emenda normativa revisável, ainda sem mudar o runtime gate.

### Promover/clarificar

1. **Um mapping cruzado, não tipos duplicados:**

   | Termo de BC/ACP | Termo owner na SPEC | Decisão |
   |---|---|---|
   | output/submission manifest semântico | payload schema de `BusPublication` | especializar por schema; não criar envelope de autoridade novo |
   | `WorkPublicationCandidate` | `PublicationCandidate` | alias de mapping, não nova entidade |
   | `WorkSubmission` aceita | `Contribution` | mapping parcial somente após receipt verification |
   | `WorkArtifact` | `Artifact` | usar artifact boundary existente |
   | `ConsumerInputManifest` | `EffectiveInputArtifact` + `RevealManifest`/entries | primeiro provar que a composição existente basta; novo conceito somente se um fixture mostrar perda semântica |

   Acordo comum exige exatamente uma interface estreita sem duplicar owners
   ([common-agreement, linhas 71–90](../document-unification-debate/common-agreement.md#estatuto-do-futuro-artefato-integrador)).

2. **Schema fixture `research.individual_report@1`** contendo somente semântica que o agente conhece
   (summary/findings/conclusions/limitations/evidence refs visíveis). BC fornece a hipótese concreta
   ([linhas 199–228](../bus-contracts/README.md#schemas-candidatos-m%C3%ADnimos)); a SPEC já permite payload
   inline ou artifact ref, schema-validado e bounded
   ([interfaces.md, linhas 129–165](../../specs/interfaces.md#bus_publish)).
3. **Invariante de release:** `Contribution` aceita pode contar apenas para o protocolo local
   explicitamente confirmado; não é `GroupResult`, commit ou handoff. Esse é o principal `X` entre
   semântica e transporte.
4. **Matriz negativa `role/capability × operation × schema` para esta única operação.** Rejeitar
   campos de autoridade, schema errado, phase fechada e receipt não verificável. Não introduzir ainda
   os roles amplos ou `submit_review`.
5. **Trace canônico e test IDs** ligando cada passo aos eventos já ratificados
   `publication.persisted` e `position.accepted`/aceitação oficial
   ([events.md, linhas 149–235](../../specs/events.md#group-and-bus-events)).

### Não promover agora

- **Skill Execution Profile, registry, trust anchor, protocol compiler, active binding e
  supersession/revocation.** ACP os declara hipóteses e reconhece que recipes arbitrárias estão fora
  da SPEC atual ([ACP, linhas 51–68](../agents-communication-protocols/README.md#hip%C3%B3tese-de-superf%C3%ADcie-%C3%BAnica-para-skills)); supply chain/overrides ainda são OQs de recipes
  ([README.md, linhas 1268–1287](../../README.md#bloqueiam-recipes-abertas-e-topologias-posteriores)).
- **`RoutingPlan`/`RoutingState`, assignment generations, leases e `ConsumerInputManifest` como novos
  tipos normativos.** São candidatos úteis, mas o gate de BC exige probes de release/consumo e routing
  antes da promoção ([BC, linhas 570–600](../bus-contracts/README.md#probes-propostos) e
  [626–642](../bus-contracts/README.md#crit%C3%A9rio-para-promo%C3%A7%C3%A3o)).
- **`submit_review`, `ReviewProfile`, rework/replacement e final approval.** O review local ainda
  depende de routing e invalidation; feedback e loops ricos estão explicitamente excluídos do work
  pack atual ([WORK-PACK.md, linhas 44–58](../../WORK-PACK.md#delivery-boundary)).
- **`JudgmentRound` universal e sealed re-vote.** A proposta é relevante, mas ACP ainda a trata como
  candidata ([ACP, linhas 330–367](../agents-communication-protocols/README.md#rodadas-de-julgamento-e-higiene-de-decis%C3%A3o)); sealed voting foi diferido para pós-MVP
  ([README.md, linhas 1286–1287](../../README.md#bloqueiam-recipes-abertas-e-topologias-posteriores)).
- **Implementation output, `ChangeSetArtifact`, workspaces isolados e atomic promote.** Necessários
  para mutação, mas conscientemente pertencem à fase posterior de recipe `code`
  ([README.md, linhas 1114–1121](../../README.md#fase-2--robustez-e-topologias)).
- **Novo `work_kind` no kernel.** A SPEC proíbe branches de workflow/provider
  ([SPEC.md, linhas 66–86](../../specs/SPEC.md#authority-locked-from-discovery-v021)); ACI-X1 é um
  schema fixture, não um enum decisório do kernel.

## 4. Dependências e riscos

### Dependências obrigatórias

1. Pins e projeção canônica do ADR-001; receipts/digests do probe não podem substituir a regra
   `aci-cjson-1` ratificada ([ADR-001, linhas 248–297](../../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#6-pydantic-and-canonical-acceptance-bytes)).
2. Conclusão documental de SWU-ACI-002 e do gate W0 antes de qualquer wiring no runtime
   ([TASK-000, linhas 37–62](../../work-pack/tasks/TASK-000.md#swu-aci-002--compatibility-ledger-and-protocol-adr-set)).
3. Review independente de BC pós-remediação e da interface ACI-X1; o review registrado atualmente
   ainda tem verdict `FIX` ([review, linhas 30–46](../bus-contracts/review/review.md#change-requests)).
4. Um owner explícito para a interface `X` e refs/digests dos dois owners, como exige o acordo
   ([common-agreement, linhas 75–90](../document-unification-debate/common-agreement.md#estatuto-do-futuro-artefato-integrador)).

### Riscos principais

- **Dois vocabulários virarem duas autoridades.** Mitigação: mapping, nunca cópia de entidades.
- **Confundir persistência com aceitação oficial.** O probe atual retorna `status: accepted`, enquanto
  a SPEC exige `persisted_candidate` e verificação posterior
  ([probe bus.mjs, linhas 169–206](../../experiments/bus-publication-probe/src/bus.mjs) versus
  [domain.md, linhas 339–355](../../specs/domain.md#publicationreceipt)). Esse drift deve ser corrigido
  no probe/fixture antes de usá-lo como conformance evidence.
- **JSONL ser promovido acidentalmente.** O próprio probe o classifica como mecanismo experimental
  ([probe README, linhas 78–88](../../experiments/bus-publication-probe/README.md#what-this-provesand-what-it-does-not)); a autoridade de produção é SQLite/WAL do ADR-001.
- **Release cedo demais.** Uma candidata ou Contribution não pode liberar handoff; somente resultado
  comprometido o faz. Esse bug quebraria a distinção BC linhas 96–109 e o lifecycle da SPEC.
- **Scope creep semântico.** Se ACI-X1 precisar de `RoutingPlan`, rework, compiler ou workspace
  mutante para passar, a fatia deixou de ser mínima e deve parar, não absorver L4/Fase 2.

## 5. Falsificadores e critérios verificáveis de saída

ACI-X1 passa somente se todos os itens abaixo forem demonstrados:

1. **Mapping total no escopo:** todo campo do fixture possui exatamente um owner; termos ACP/BC
   mapeiam para conceitos da SPEC sem duas entidades oficiais. Termo ambíguo fica `unresolved` e
   bloqueia, conforme a regra fail-closed do acordo
   ([common-agreement, linhas 79–90](../document-unification-debate/common-agreement.md#estatuto-do-futuro-artefato-integrador)).
2. **Golden happy trace:** publish persiste candidata + receipt antes de retornar; parent verifica os
   bytes/campos exatos; somente então existe uma `Contribution`; replay produz o mesmo estado/hash e
   zero efeitos.
3. **Golden negative trace:** missing/forged/mismatched receipt, authority field, schema incompatível,
   phase fechada, retry divergente e duplicate logical key falham sem Contribution nem consumer
   liberado.
4. **Crash matrix:** antes do commit não há receipt; depois do commit/antes da resposta, retry
   idêntico devolve os mesmos bytes; acceptance e abandonment têm no máximo um vencedor. Essas são
   obrigações já definidas para TASK-010
   ([ADR-001, linhas 299–315](../../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#crash-boundaries-and-recovery-obligations)).
5. **Release safety:** candidata nunca libera nada; Contribution aceita não produz handoff; somente
   `GroupResult` comprometido pode produzir delivery downstream.
6. **Kernel genericity:** a implementação futura não contém branch `if research`; schema/phase/policy
   confirmados governam a aceitação. Se precisar de branch, ACI-X1 é refutada.
7. **Conformance do probe:** o receipt do probe passa a usar a semântica
   `persisted_candidate`, deixando acceptance para o verificador, e todos os testes continuam verdes.
8. **Review independente:** PASS explícito sobre BC remediado, mapping ACI-X1, fixtures e ausência de
   promoção retroativa dos contratos adiados.

Falsificador forte: se o trace de pesquisa read-only não puder ser expresso apenas com
`DispatchSpec/schema_refs`, `Attempt`, `BusPublication`, `PublicationCandidate`, `PublicationReceipt`,
`Contribution`, `Artifact` e eventos existentes, deve-se registrar a perda semântica concreta antes
de criar um novo tipo. Conveniência nominal não é evidência suficiente.

## 6. Sequência prática curta

1. **Congelar ACI-X1 em um artefato de interface draft:** matriz `ACP/BC -> SPEC`, pins, owner,
   invariante de release e itens explicitamente adiados. Nenhuma mudança de runtime gate.
2. **Produzir fixtures e golden traces:** schema `research.individual_report@1`, happy path, negativos,
   lost-response retry e replay esperado, reutilizando os IDs/test obligations da SPEC.
3. **Alinhar o probe à semântica da SPEC:** receipt significa candidata persistida, parent verifier
   significa aceitação oficial; manter JSONL claramente experimental. Rodar a suite.
4. **Review independente duplo:** um review do BC remediado e outro da interface/fixtures. Qualquer
   drift de autoridade, release cedo ou novo tipo não justificado bloqueia a emenda.
5. **Emenda mínima da SPEC:** apenas mappings, schema refs, regra de release e TEST-SPEC. Não adicionar
   routing/rework/profile/compiler.
6. **Respeitar o caminho de execução:** terminar SWU-ACI-002/W0; depois selecionar ACI-X1 como parte
   do wiring de S-001/TASK-010→030, com receipt de execução e falsificadores do ADR-001.

## Decisão recomendada

Focar agora em **provar uma publicação read-only como fato oficial, e nada além disso**. Essa feature
é relevante porque testa a fronteira de autoridade real entre agente e runtime, usa o que já foi
ratificado, aproveita evidência existente e compõe diretamente o Slice 0. Profiles de skill,
routing/rework, review agregado e mutação de workspace devem permanecer visíveis no roadmap, mas não
devem disputar o primeiro wiring.
