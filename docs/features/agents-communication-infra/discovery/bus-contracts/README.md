---
tags: [agents-communication-infra, discovery, bus, contracts, workers, review, skills]
node_type: discovery
is_session: false
layer: [application, orchestration]
nature: [research, design]
status: draft
version: 0.3.0
created: 2026-07-22
last_updated: 2026-07-22
---

# Bus Contracts — Discovery

## Objetivo

Definir os contratos mínimos pelos quais agentes submetem outputs de trabalho, recebem informação
produzida por outros agentes e participam de ciclos de revisão. O agente deve fornecer somente o
conteúdo semântico que apenas ele conhece; identidade, autoridade, prompt, skills, arquivos
alterados, execução, persistência, destinatários e demais metadados devem ser derivados da
configuração ou capturados pelo runtime sempre que possível.

Este discovery cobre somente o **Work Bus** e suas operações de submissão de trabalho e revisão.
Knowledge, telemetria e controle não são buses adicionais deste contrato. O desenho deve preservar
uma extensão versionada para um futuro Knowledge Bus, mas sua operação, adjudicação, filtragem e
promoção pertencem a um discovery separado.

## Relação com os documentos existentes

- A SPEC atual possui um `DeliberationBus`, `bus_publish`, publicação com receipt e journal.
- O README arquitetural distingue bus de deliberação, bus geral de contexto, handoffs, artifact
  store e knowledge/provenance store.
- O discovery de `agents-communication-protocols` investiga o fluxo completo de pesquisa, workers,
  revisores, rework e aprovação.
- Este documento aprofunda a fronteira mais estreita entre atribuição, input materializado,
  submissão, artifact, roteamento e consumo.

O resultado poderá alterar o discovery de protocolos e, depois de revisão independente, promover
contratos para a SPEC. Este documento não altera a SPEC por si só.

## Distinção inicial: prompt, output, publicação e artifact

Estes objetos não devem ser confundidos:

| Objeto | Origem | Função | Persistência proposta |
|---|---|---|---|
| `PromptTemplate` | configuração/versionamento | Base reutilizável para construir uma invocação | versionado |
| `MaterializedAgentInvocation` | runtime | Registro da tentativa, configuração resolvida e referências de input | journal + referências |
| `EffectiveInputArtifact` | runtime | Snapshot dos inputs materializados antes da tentativa | artifact imutável/protegido |
| `ExecutionObservationManifest` | runtime | Manifest final de segmentos de observação append-only | artifact imutável/content-addressed |
| `WorkArtifact` | artifact service mediado | Relatório, patch ou outro corpo produzido | artifact imutável/content-addressed |
| `WorkPublicationCandidate` | agente via Work Bus | Candidata durável ainda inelegível para consumo | journal antes do receipt |
| `WorkSubmission` | runtime após verificação | Resultado oficial que pode liberar consumidores | journal após verificação |
| `PublicationReceipt` | runtime | Evidência canônica de persistência da candidata | bytes/identidade duráveis no journal |

Uma referência `artifact:sha256:...` identifica um corpo já finalizado. O agente, porém, não precisa
fabricar essa referência: `submit_work` recebe conteúdo inline ou um arquivo em scratch autorizado;
o runtime valida, finaliza e injeta a referência na candidata. Uma referência preexistente só é
aceita quando provenance, assignment produtor, classificação, capability de leitura e política de
reutilização autorizam seu uso.

### Lifecycle de publicação oficial

Toda submissão de work ou review usa o mesmo gate:

O estado da candidata e as observações de verificação são separados para que ausência de receipt,
falha de verificação, retry e tentativa stale não sejam colapsados:

```text
submit_* -> persisted_unverified
                  |
                  | exact receipt + active assignment/generation CAS
                  v
               accepted (terminal)
                  |
                  +-- orquestra apenas consumers liberados pelo release gate

persisted_unverified -- explicit abandon/expiry policy --> abandoned (terminal)
```

| Situação | Registro | Estado da candidata | Retry |
|---|---|---|---|
| append e receipt canônico persistidos | `candidate.persisted` | `persisted_unverified` | retry idêntico retorna o mesmo receipt |
| terminal não contém receipt | `verification.failed: missing_receipt` | permanece `persisted_unverified` até reconcile/abandon | permitido enquanto assignment/generation estiver ativa |
| receipt inválido ou forjado | `verification.failed: invalid_receipt` | permanece inelegível; policy pode abandonar | nunca aceita o receipt inválido; nova evidência só conforme policy |
| attempt/generation perdeu lease/CAS | `stale_observation` | não muda a candidata corrente | não pode publicar/aceitar naquela generation |
| verificação exata vence CAS | `submission.accepted` | `accepted` | retry retorna a aceitação original |
| expiração/cancelamento/replacement encerra candidata | `candidate.abandoned` | `abandoned` | terminal; late result é somente observação |

O gateway autentica a capability, finaliza artifacts e persiste candidata + receipt canônico antes
de responder. O agente retorna o receipt no resultado terminal. O parent/scheduler verifica receipt,
operação, assignment, attempt, generation, logical key, payload digest e artifacts. Só o comando de
verificação que vence o CAS cria `submission.accepted`; eventos de falha e stale nunca liberam
consumidores nem apagam a evidência original.

### Release gates por classe de consumidor

Aceitação de uma submissão não equivale a resultado comprometido do work item:

| Fato aceito | Pode liberar | Não pode liberar |
|---|---|---|
| `submission.accepted` de worker/researcher | reviewer local ou synthesizer explicitamente dependente no `RoutingPlan` | handoff, dispatch sucessor ou dependência que exige resultado final |
| `review.accepted: changes_required` | rework assignment da mesma topologia | tarefa downstream ou handoff |
| conjunto de reviews aprovado | avaliação kernel da regra de conclusão | handoff antes de commit |
| `work_result.committed` | work items downstream e handoff declarados | consumer ausente do plano confirmado |

O `RoutingPlan` declara, por edge, qual fato libera o consumer. Toda entrega entre work items ou
dispatches que exige resultado oficial depende de `work_result.committed`, não de uma submissão
individual aceita.

### Onde os artifacts operacionais devem viver

Artifacts operacionais não devem ser gravados no repositório por padrão. No MVP single-host, a
hipótese preferida é um `artifact_root` configurável sob o diretório de dados do runtime, fora do
worktree e fora do controle de versão. O journal persiste somente identidade, digest, tamanho,
classificação, lifecycle e um `storage_ref` opaco controlado pelo artifact service.

```text
runtime data directory/
  artifacts/
    sha256/<prefix>/<digest>   # bytes, fora do Git
  journal.sqlite              # fatos e referências

repository/
  ...                         # somente mudanças autorizadas da tarefa
```

O caminho concreto não é decidido neste discovery. Em desenvolvimento ele pode ser um diretório
local ignorado; em uso normal deve preferencialmente ficar no diretório de dados da aplicação; uma
implantação futura pode trocar os blobs por object storage sem mudar o `artifact_id`.

Há duas classes que não devem ser confundidas:

- **output operacional:** prompt, relatório de pesquisa, raw output, transcript e diff capturado;
  fica no artifact store e segue retenção/tombstone;
- **mudança no produto/repositório:** código, teste ou documentação que a tarefa autorizou criar ou
  editar; permanece no worktree e pode posteriormente ser versionada pelo fluxo normal do usuário.

Os bytes canônicos de `PublicationReceipt` permanecem como evidência durável do journal e não seguem
a retenção ordinária de corpos operacionais. Artifacts referenciados por assignments, reviews,
handoffs ou dispatches retidos ficam pinned; tombstone só é permitido depois que a política comprova
ausência de referências vivas e produz uma resposta determinística para leituras posteriores.

Somente uma ação explícita de promoção/exportação deve transformar um artifact operacional em
arquivo do repositório. O runtime nunca deve despejar automaticamente todos os outputs no Git.

## Hipóteses de trabalho

### H1 — O agente fornece apenas o resultado semântico

O payload manual contém somente a semântica definida pelo `OutputContract`; os schemas candidatos
completos aparecem abaixo. `submit_work` converte output inline ou arquivo autorizado em
`WorkArtifact`; a referência é resultado da operação, não campo que o agente preenche. Para
implementation, a aceitação também exige exatamente um modo de evidência:

- `observed_change_set`: captura confiável pelo runtime;
- `declared_change_set`: fallback validado e explicitamente marcado quando a superfície não observa;
- `no_change_evidence`: prova tipada de que a tarefa não produziu mudança no workspace.

O runtime deve capturar, sem preenchimento manual pelo agente:

- identidade de run, grupo, tarefa, operação, agente e tentativa;
- prompt materializado, inputs e respectivos digests;
- skills efetivamente fornecidas e seus digests;
- caminhos autorizados;
- arquivos criados, modificados, removidos ou movidos;
- hashes/diff antes e depois;
- comandos e testes executados, status e test receipts;
- horário, modelo/provider e relações causais;
- destinatários e política de visibilidade.

Antes da tentativa, o runtime congela um baseline por assignment e o ownership/lease dos paths.
Ao submeter, finaliza um `ChangeSetArtifact` com baseline, paths, hashes before/after, diff, deltas
preexistentes, próprios e concorrentes. Sobreposição ou atribuição ambígua bloqueia a aceitação. Uma
lista manual é somente fallback declarado, nunca apresentada como observação autoritativa.

Bloquear a submissão não desfaz mutações já feitas. Por isso, uma implementation assignment não
escreve diretamente no worktree canônico compartilhado. Ela recebe um workspace isolado derivado do
baseline — por exemplo, worktree/sandbox por assignment — ou usa um write gateway que valida o lease
antes de cada mutação. O resultado aceito ainda não altera o produto: ele produz um
`ChangeSetArtifact` candidato.

```text
canonical baseline -> isolated assignment workspace -> ChangeSetArtifact
                                                     |
                                            accepted + approved
                                                     v
                                      atomic promote/merge gateway
```

Somente um promote/merge autorizado aplica o change set ao target canônico depois dos release gates
configurados. Workspace ou side effect de attempt rejeitada, stale, cancelada ou órfã entra em
quarentena/reconciliação e nunca é atribuído implicitamente a outro worker. Conflito no promote gera
novo rework/rebase sobre baseline explícito; não faz merge silencioso.

Bloqueio que altera estado não pertence ao payload de uma submissão concluída. O agente usa um
comando de controle tipado; uma submissão pode apenas referenciar um blocker já registrado.

#### Schemas candidatos mínimos

Todo `OutputContract` declara `compatible_work_kind`, `output_subtype`, schema e limites. A
compilação do `DispatchSpec` e cada publicação rejeitam contrato incompatível com o `work_kind`
confirmado. “Outro output” significa apenas subtipo registrado do kind atual, nunca introdução de
outro kind.

```yaml
output_contract:
  id: research-report@1
  compatible_work_kind: research
  output_subtype: individual_report
  schema_ref: schema:research-report@1
```

Request agent-authored de research:

```yaml
summary: "Conclusão principal e limites"
output:                         # exactly one of the two keys
  inline_report:
    findings: []
    conclusions: []
    limitations: []
# ou:
# output:
#   scratch_file: "authorized-scratch/report.md"
evidence_refs: []               # somente referências já visíveis/autorizadas
blocker_ref: null               # referência opcional a blocker registrado
```

Request agent-authored de implementation:

```yaml
summary: "O que foi implementado e decisões relevantes"
decisions: []
declared_change_set: null       # permitido somente no fallback capability/profile
blocker_ref: null
```

O runtime serializa `summary` + `decisions` como um `ImplementationReport`/`WorkArtifact` sem exigir
um campo `output` redundante e anexa exatamente uma variante de evidência de mudança.
No modo observado, o agente não preenche `change_set_ref`: o runtime o injeta após congelar o
workspace isolado. No fallback, `declared_change_set` possui schema próprio de paths/actions/hashes e
fica marcado `evidence_mode=declared`, nunca como observado. `no_change_evidence` é uma variante
explícita do `OutputContract`, não ausência silenciosa de change set.

Request agent-authored de review:

```yaml
verdict: approved | changes_required
findings:
  - problem: "..."
    evidence_refs: []
    blocking: true
    remediation_scope: subject_owner
```

`approved` não pode conter finding bloqueante; `changes_required` exige ao menos um. Para review
local, ausência de `remediation_scope` normaliza para `subject_owner`; perfis finais que podem reabrir
múltiplos níveis exigem scope explícito allowlisted. Zero ou múltiplos destinos após normalização é
erro, nunca escolha livre do reviewer. Cada finding exige `problem` não vazio e ao menos uma
`evidence_ref` visível, salvo quando o `ReviewProfile` declara e justifica uma classe de finding cuja
evidência é a ausência verificável de um artifact obrigatório.

O agente não pode preencher campos derivados: IDs de run/dispatch/work item/assignment/agent/attempt,
`work_kind`, generation, recipients, routing, phase, timestamps, prompt/skill refs ou hashes
canônicos. O runtime rejeita, em vez de ignorar, qualquer tentativa de afirmar autoridade nesses
campos.

### H2 — Prompt é input capturado, não output declarado

O runtime compila uma invocação a partir de:

```text
PromptTemplate
+ WorkAssignment
+ referências autoritativas da SPEC
+ skill bundle aplicável
+ escopo de escrita
+ ferramentas disponíveis
+ outputs autorizados de predecessores
= EffectiveInputArtifact
```

Devem ser preservados tanto o template/versionamento quanto o input exato materializado para cada
tentativa. Conteúdo sensível pode permanecer em artifact protegido; o journal guarda referência,
digest, versão e classificação.

`EffectiveInputArtifact` afirma somente o snapshot inicial observável que o runtime materializou.
Respostas de tools, leituras mediadas, mensagens posteriores e outros inputs adquiridos durante a
execução são gravados como segmentos append-only content-addressed, em ordem causal e com
digest/redaction. Segmentos podem crescer durante a tentativa, mas não são o artifact oficial.
No terminal, o runtime congela um `ExecutionObservationManifest` imutável que ordena e hasheia os
segmentos; referências oficiais apontam somente para esse manifest final. O sistema não promete
observar canais que o runtime não mede; essa limitação acompanha a evidência.

### H3 — Skills são bindings configurados e congelados

Uma atribuição pode vincular qualquer skill compatível ao worker, ao reviewer ou a ambos:

```yaml
skill_bindings:
  - skill_ref: "skill:python-code-quality@3"
    applies_to: [worker, reviewer]
  - skill_ref: "skill:implementation-workflow@2"
    applies_to: [worker]
  - skill_ref: "skill:adversarial-review@1"
    applies_to: [reviewer]
```

O runtime deve resolver a referência antes da tentativa e registrar versão, origem, digest, ordem e
conteúdo efetivamente disponibilizado. Uma referência a um arquivo mutável sem snapshot ou digest
não é evidência suficiente.

Skills ajudam a executar ou avaliar a tarefa, mas não podem substituir nem contradizer a autoridade
da SPEC, da atribuição confirmada ou das políticas do runtime.

### H4 — A revisão possui um perfil explícito

O que deve ser considerado por um reviewer não deve depender somente de um prompt improvisado pelo
agente pai. Uma configuração candidata é:

```yaml
review_profile:
  lenses:
    - spec_conformance
    - code_quality
    - transaction_safety
    - test_adequacy
  normative_refs:
    - "specs/SPEC.md#receipt-gated-publication"
  review_lens_skill_refs:
    - "skill:python-code-quality@3"
    - "skill:sqlite-transaction-safety@2"
  verdicts: [approved, changes_required]
```

`normative_refs` apontam para SPEC, atribuição confirmada e runtime policy. Skills ficam em
`review_lens_skill_refs`: ensinam como executar uma lente, mas não criam requisitos de produto. Em
caso de conflito, a precedência é runtime/safety policy, SPEC confirmada, assignment e, por último,
skills/lentes.

O reviewer fornece apenas parecer e findings semânticos. O runtime vincula automaticamente o
parecer à versão/hash da submissão, prompt, skills, ciclo, identidade e evidência operacional.

### H5 — Roteamento é configuração, não escolha livre do agente

O produtor publica para uma operação e um tipo de output permitidos. `GroupSpec`, workflow/recipe,
papéis, dependências, fase, connections, ACL e assignments são inputs de compilação. Na confirmação,
o runtime produz um `RoutingPlan` imutável dentro do `DispatchSpec`. Ele contém apenas topologia,
templates de assignment, edges/release gates, responsibility matrix e visibility policy.

Instâncias, generations, leases, readiness, inbox/delivery e estado de rework vivem em
`RoutingState`, derivado do journal e alterado somente por comandos com CAS. Criar ou reabrir uma
operação instancia um template permitido; não muta o plano. Alterar topologia, responsabilidade ou
policy exige novo `RoutingPlan` versionado e nova confirmação.

```text
confirmed DispatchSpec
  + work graph + responsibilities + visibility policy
                              |
                              v
                    immutable RoutingPlan
                              |
                              v instantiate/reopen by journaled command
                    mutable RoutingState
```

O agente não deve preencher IDs arbitrários de destinatários. Feedback dirigido pode citar a
submissão alvo e um `remediation_scope` allowlisted. O `RoutingPlan` aplica uma matriz determinística
`subject_kind + remediation_scope -> responsible_work_item/role`. Zero ou múltiplos destinos sem
regra explícita são erro de roteamento; o reviewer nunca escolhe um `agent_id`.

### H6 — Um Work Bus, operações tipadas e mecanismos adjacentes

Há um único bus lógico de trabalho voltado aos agentes:

| Superfície | É bus? | Conteúdo | Autoridade/consumidor |
|---|---|---|---|
| Work Bus | sim | work submissions, reviews e deliberação autorizada | `RoutingPlan` e phase/ACL |
| command/control plane | não | atribuição, bloqueio, cancelamento, reabertura e escalonamento | command service/kernel |
| handoff workflow | não | entrega derivada de resultado comprometido | kernel + reconciler |
| realtime projection | não | visão autorizada para usuário/operador | projeção reconstruível |
| future knowledge extension | não implementado | reservado para discovery próprio | nenhum contrato ativo aqui |

#### Work Bus

- **Produtores lógicos:** workers, pesquisadores, sintetizadores e reviewers autorizados.
- **Operações:** `submit_work` e `submit_review`, com capabilities e schemas disjuntos.
- **Conteúdo manual:** resultado semântico mínimo; o runtime injeta artifacts e metadados.
- **Consumidores:** work items e papéis resolvidos pelo `RoutingPlan`.
- **Persistência:** submissão/evento no journal; corpos grandes no artifact store.
- **Aceitação:** lifecycle candidate→receipt→verified acceptance, assignment/generation ativa,
  schema, operation, attempt, idempotência, provenance e artifact authorization.

Agentes não leem livremente um stream ou inbox do Work Bus. Quando um release gate torna um
assignment ready, o runtime materializa um `ConsumerInputManifest` e o inclui numa nova
`MaterializedAgentInvocation`:

```yaml
consumer_input_manifest:
  target_assignment_id: "..."
  target_generation: 2
  release_event_id: "..."
  source_submissions:              # ordem canônica declarada pelo edge
    - submission_id: "..."
      generation: 1
      digest: "sha256:..."
      artifact_refs: []
  visibility_decision_ref: "..."
  ordering_policy_ref: "..."
  manifest_digest: "sha256:..."
```

O journal registra `delivery.materialized` com manifest digest e target generation. Retry idêntico
reutiliza o mesmo manifest; payload divergente para a mesma delivery key é conflito. A entrega é
considerada consumida somente quando a invocação aceita esse manifest como input; acknowledgement
perdido é reconciliado pelo journal, não por reenvio de conteúdo diferente. Cancelamento ou
replacement invalida a generation alvo e impede consumo tardio. Visibility/ACL é decidida antes da
resolução dos artifacts, e o manifest preserva IDs, digests, ordem e redactions usados.

`submit_work` produz um subtipo permitido pelo `OutputContract`; `compatible_work_kind` deve igualar
o `work_kind` confirmado na compilação e novamente na publicação.
`submit_review` exige uma `ReviewAssignment`, subject/version/digest exatos e `ReviewProfile`; produz
`approved` ou `changes_required` com findings. Um payload de crítica/deliberação não possui verdict
nem efeito de rework. Campos de review na capability de work, ou vice-versa, são rejeitados.

O reviewer solicita correção; ele não escolhe nem agenda diretamente um novo worker. O
orquestrador aplica o `RoutingPlan` e cria/reabre a operação para researcher, synthesizer,
coder/worker ou integrator responsável.

#### Command/control plane

Não é um bus de autoria. Atribuição, start, blocker, cancelamento, reabertura, escalonamento e decisão
humana entram pelo command service canônico com authority, policy, idempotência e CAS. Agentes comuns
recebem apenas comandos allowlisted, como `report_blocked` ou `request_clarification`; texto de uma
submissão nunca altera estado oficial.

Uma atribuição aceita é materializada no input do agente. O agente não republica o
prompt nem suas skills no work bus.

#### Handoff workflow

Não é uma publicação arbitrária de agente. Após um resultado oficialmente comprometido, o kernel
produz o intent/fato de handoff; o reconciler registra delivery. A chave lógica inclui
`source_commit_id` ou `result_digest`, `connection_id` e `connection_version`, permitindo um resultado
posterior sem colidir com um handoff anterior.

O agente não publica handoff arbitrário. Ele publica seu output; o kernel cria o handoff quando a
regra de conclusão do grupo for satisfeita.

#### Extension seam para knowledge futuro

Este discovery não define operação, schema, consumidor, adjudicação, filtragem ou promoção de
knowledge. Para permitir um discovery futuro sem quebrar o Work Bus, o envelope e o capability
registry devem ser versionados, namespaced e fail-closed: operação desconhecida ou capability de
outro namespace é rejeitada, e nenhum `submit_work` pode promover knowledge implicitamente.

#### Realtime/projection stream

Não é um bus de autoria dos agentes. É uma projeção reconstruível para usuário e operadores, com
cursor, ACL e redaction, derivada do journal, artifact metadata, audit ledger e knowledge store.

#### Princípio de separação

`message_type` sozinho não é barreira de autoridade. Operações com atores e efeitos diferentes usam
capabilities e schemas distintos, mesmo dentro do mesmo Work Bus:

```text
submit_work(...)
submit_review(...)
```

O command plane permanece fora desse envelope de autoria. Um futuro namespace de knowledge deve ser
adicionado por registro explícito, sem ampliar uma capability de work existente.

### H7 — Um run de trabalho possui um único `work_kind`

`work_kind` é parte do `DispatchSpec` confirmado e permanece imutável durante todo o run. Ele não é
o `dispatch_type` usado pela governança atual para escolher skills e registrar dispatches, nem
habilita tipos reservados. É uma classificação do workflow de produto que o runtime futuro deverá
compilar e validar.

```yaml
work_kind: research | implementation
```

Um dispatch de research pode conter pesquisadores, sintetizador e reviewers de research:

```text
researchers -> synthesizer -> research reviewers -> research result
```

Um dispatch de implementation pode conter workers/coders, integrador quando necessário e reviewers
de implementação:

```text
coders/workers -> optional integrator -> implementation reviewers -> implementation result
```

Review é uma fase/papel dentro do tipo confirmado, não autorização para introduzir outro tipo de
trabalho. Um final reviewer de research pode devolver um finding a um researcher ou ao synthesizer;
um final reviewer de implementation pode devolvê-lo a um coder/worker ou ao integrador. Ele não
roteia trabalho para papéis que não pertencem ao dispatch.

Quando research e implementation precisam se encadear, o resultado imutável de um dispatch é
referenciado como input de outro dispatch explicitamente criado e confirmado:

```text
research dispatch --research result ref--> implementation dispatch
```

Se um dispatch de implementation descobrir uma lacuna de research, ele termina ou bloqueia com uma
solicitação estruturada; o runtime não cria pesquisadores silenciosamente dentro do mesmo dispatch.
Da mesma forma, um dispatch de research não promove probes ou protótipos em mudança de produto. Um
novo dispatch preserva autoridade, escopo, prompts, skills, orçamento, revisão e audit trail próprios.

### H8 — Retry, rework e replacement têm identidades distintas

Cada output possui `logical_submission_id` e `submission_generation`. Retry idêntico da mesma
generation usa a mesma idempotency key/digest e retorna o receipt original. Rework cria uma nova
generation que referencia `supersedes`; replacement recebe novo attempt/agent, mas só publica se
possuir o lease/CAS da assignment e generation ativas.

```text
same generation + same digest      -> original receipt
same generation + different digest -> idempotency conflict
new accepted rework                -> generation + 1, supersedes prior
late/stale attempt                 -> retained observation, not accepted
```

Reviews vinculam `subject_submission_id`, `subject_generation`, `subject_digest` e versão corrente.
Publicação atrasada ou concorrente que perde o CAS não libera consumidores.

## Vocabulário candidato

- `WorkAssignment`: atribuição de uma unidade no `RoutingPlan` confirmado.
- `OutputContract`: tipos e schemas que uma operação pode submeter.
- `SkillBinding`: skill versionada aplicada a um papel.
- `ReviewProfile`: lentes, skill refs e pareceres permitidos, sem autoridade de routing.
- `MaterializedAgentInvocation`: tentativa resolvida e congelada pelo runtime.
- `EffectiveInputArtifact`: snapshot inicial materializado para a tentativa.
- `ObservationSegment`: lote append-only content-addressed de observações mediadas.
- `ExecutionObservationManifest`: manifest final imutável que ordena observation segments.
- `ConsumerInputManifest`: input autorizado, ordenado e content-addressed entregue a um consumer.
- `WorkArtifact`: corpo imutável produzido durante o trabalho.
- `WorkPublicationCandidate`: publicação durável ainda não oficial.
- `WorkSubmission`: resultado oficialmente aceito após receipt verification.
- `ReviewSubmission`: parecer e findings mínimos publicados pelo reviewer.
- `ChangeSetArtifact`: baseline e mudança de workspace imutáveis atribuídos a um assignment.
- `RoutingPlan`: topologia, templates, release gates e responsabilidades imutáveis.
- `RoutingState`: assignments, generations, leases, readiness e deliveries derivados do journal.

## Perguntas abertas

1. `summary` deve ser sempre obrigatório ou o artifact tipado pode ser suficiente?
2. Qual é o threshold e a policy que escolhem payload inline versus `WorkArtifact`?
3. O runtime persiste o prompt completo, uma composição segmentada ou ambos?
4. Como classificar, redigir e restringir prompts que contenham secrets ou dados privados?
5. Como resolver skills locais, plugins e skills remotas para uma forma imutável e auditável?
6. Uma mudança de skill invalida a atribuição confirmada ou cria somente uma nova tentativa?
7. Toda skill compartilhada com o worker deve virar lente de revisão, ou isso precisa ser explícito?
8. Como derivar checklists verificáveis de uma skill sem tratá-la como SPEC?
9. Como provar a atomicidade entre finalizar artifact, append da candidata e emissão do receipt?
10. Como validar integridade dos blobs em leitura e recuperar corrupção ou perda do `storage_ref`?
11. Como funcionam fan-out, quorum, conflito e timeout com múltiplos reviewers?
12. Qual evento e autoridade criam um dispatch sucessor quando o run identifica outro `work_kind`?
13. Quais `work_kind` adicionais serão necessários sem enfraquecer a regra de tipo único?
14. Qual retenção mínima é exigida para prompts, execution observations, reports e change sets?

## Probes propostos

1. **Research mínima:** materializar prompt + skill, chamar `submit_work` com relatório inline,
   finalizar o artifact automaticamente e reconstruir input, observation manifest e output.
2. **Lifecycle e crash:** interromper antes/depois da finalização do artifact, append, receipt e
   verificação; cobrir missing/invalid/stale, abandon/expiry e provar que retry converge sem liberar
   consumer cedo.
3. **Release gates e consumo:** provar que submission aceita libera apenas consumer local declarado,
   que handoff espera `work_result.committed` e que `ConsumerInputManifest` é estável em replay.
4. **Implementação isolada:** congelar baseline e path lease em workspace isolado, capturar um
   `ChangeSetArtifact`, rejeitar side effect stale e promover atomicamente somente após aprovação.
5. **Skill compartilhada:** dar uma skill de código ao worker e ao reviewer e verificar se o parecer
   referencia a mesma versão/digest.
6. **Skill assimétrica:** fornecer uma lente adversarial somente ao reviewer sem alterar o contrato
   de produto da tarefa.
7. **Roteamento:** instanciar/reabrir assignments em `RoutingState` sem mutar `RoutingPlan`; falhar em
   zero/múltiplos destinos e exigir nova versão para mudança topológica.
8. **Rework/replacement:** produzir nova generation, invalidar aprovação anterior e rejeitar retry
   divergente, worker substituído e resultado tardio.
9. **Schemas/work kind:** validar schemas mínimos e rejeitar `OutputContract` cujo
   `compatible_work_kind` difere do run.
10. **Artifact authorization:** tentar reutilizar artifact de outro assignment/classification sem
   capability e exigir rejeição; manter artifact pinned enquanto houver referência viva.
11. **Observation segments:** registrar segmentos append-only, finalizar manifest imutável e impedir
    que referência oficial aponte para staging incompleto.
12. **Prompt protegido:** preservar prova do input exato sem expor conteúdo sensível numa projeção
   comum.
13. **Capability matrix:** testar `producer role × operation × schema`, incluindo worker chamando
    `submit_review`, reviewer chamando `submit_work` e qualquer agente tentando comando não permitido
    pelo envelope do Work Bus.

## Resultados esperados

- schemas mínimos agent-authored e campos server-derived proibidos;
- lifecycle de candidata, verification observations, receipt, abandon e submissão oficial;
- release gates por consumer e contrato de `ConsumerInputManifest`;
- contrato de `WorkAssignment`, `OutputContract`, `SkillBinding`, `ReviewProfile`, `RoutingPlan` e
  `RoutingState`;
- regra para materialização e persistência do prompt exato;
- regra para observation segments e `ExecutionObservationManifest` final;
- regra para workspace isolado, `ChangeSetArtifact`, promote/quarantine, paths, comandos e testes;
- fronteira do Work Bus com command plane, handoff workflow, journal e artifact store;
- extension seam fail-closed para um futuro Knowledge Bus, sem contrato funcional de knowledge;
- roteamento e visibilidade compilados no `RoutingPlan`;
- regras de versionamento, invalidação, retry e rework;
- mapa das alterações futuras na SPEC, runtime, skills e test derivation engine.

## Fora de escopo neste momento

- implementar o bus ou o runtime;
- promover imediatamente estes nomes para a SPEC;
- definir operação, schema, adjudicação, filtragem, promoção ou store de knowledge;
- escolher um broker, fila ou produto de mensageria;
- exigir que agentes preencham metadados observáveis pelo runtime;
- tratar texto produzido pelo modelo como evidência suficiente de arquivos ou testes executados.

## Critério para promoção

Este discovery poderá propor mudanças na SPEC somente depois que os probes demonstrarem que:

- o payload manual é realmente mínimo;
- prompt, skills, observations mediadas e outputs são reconstruíveis por referência e digest;
- candidate/receipt/accepted converge sob crash e retry sem liberar consumidor cedo;
- cada classe de consumer é liberada somente pelo fato configurado e recebe manifest estável;
- o roteamento funciona sem destinatário arbitrário no payload do agente;
- `RoutingState` evolui sem mutar a topologia do `RoutingPlan`;
- worker e reviewer recebem as lentes configuradas corretas;
- implementation review fica ligada a um change set isolado, imutável e promovível atomicamente;
- schemas rejeitam campos de autoridade e `OutputContract` incompatível com `work_kind`;
- observation staging não pode ser confundido com manifest final oficial;
- artifacts e journal têm autoridade, authorization, pinning e lifecycle claramente separados;
- toda combinação não autorizada de papel, operation e schema falha explicitamente;
- revisão independente não encontrar campos manuais sem necessidade demonstrada.
