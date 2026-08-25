# Research corpus — experiment recommendation trigger

This file preserves the six frozen scout reports verbatim. The source headings below are editorial separators and are not part of the reports.

## Source 1 — `scout-domainspec-authority.md`

# Scout — autoridade e precedentes de transição em `domainspec-core`

## Veredito

O corpus sustenta **recomendar a proposta de um experimento quando a pesquisa deixou uma hipótese importante ainda não testemunhada, mas tornou possível pré-registrar uma prova discriminante**. Ele não sustenta usar "várias pesquisas" nem "nenhum build" como gatilhos suficientes.

A autoridade LIVE do tipo `experiment` define um experimento como **pré-registro**, não execução: uma hipótese falsificável, um critério congelado antes do resultado, ataque de validade e uma rodada posterior separada. O melhor precedente histórico encontrado recomendou um teste não porque havia muita pesquisa, mas porque evento, fronteira, fontes, papéis e resultados mensuráveis já podiam ser pré-registrados, enquanto valor e demanda continuavam sem testemunho.

Portanto, a transição defendida por este corpus é:

`pesquisa acumulada` → `lacuna decisória ainda aberta` + `hipótese falsificável` + `probe pré-registrável` + `ambos os resultados informativos` → **oferecer desenho/pré-registro** → `gate humano` → rodada posterior.

Ela não é:

`N pesquisas` + `nenhum dispatch de code` → experimento automático.

## Escopo e hierarquia de autoridade

Inspecionei apenas `C:/Users/victo/domainspec-core`, nas famílias repo-locais de estratégia/tipo, contratos e templates MARS, políticas/decisões CyberAlchemy v2 e skills Arcanum diretamente relacionadas a experimento e decisão. Não houve busca web nem escrita no corpus.

Hierarquia usada:

1. **Autoridade operacional repo-local:** o router manda preferir os owners sob `implementation/domainspec/internal_tools/subagents-dispatch-hooks/` às cópias geradas (`.../domainspec-subagents-strategy/SKILL.md:30-31`). O router declara `experiment` LIVE e `code`, `plan` e `suggestion` RESERVED (`.../domainspec-subagents-strategy/SKILL.md:188-202`).
2. **Autoridade limitada ao programa MARS:** `implementation/mars/definitions/MARS-PIPELINE.md:1-5` se declara pipeline canônico **do programa MARS**, não do orchestrator inteiro.
3. **Precedentes históricos:** findings, decisões e receipts completos mostram como as regras foram aplicadas, mas não legislam o trigger atual.
4. **Política candidata:** `cyberAlchemy-v2/authority/promotion-policy.md:1-6` diz explicitamente `Status: candidate local policy`; é sinal útil, não norma estabilizada.

## Achados

### A1 — O tipo LIVE começa no pré-registro, não na contagem de pesquisas

**Prova.** O owner do tipo diz que `experiment` é usado quando se pré-registra um probe contra critério fixado antes da rodada, distinguindo-o de `research` por seu grader (`implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/experiment/SKILL.md:3`, `:16-35`). O artefato precisa conter uma hipótese falsificável, condição de falsificação, regra mecânica, o que ambos os resultados ensinariam e categorias pré-registradas (`:72-95`). Critério não falsificável é `INVALID` antes de congelar (`:100-124`).

**Owner/status.** Owner: skill repo-local `experiment`; status: `LIVE` no router (`.../domainspec-subagents-strategy/SKILL.md:188-200`).

**Condição de transição.** Já é possível formular uma afirmação única e uma observação que a enfraqueceria, com resultado `SURVIVED` e `FALSIFIED` ambos informativos. "Muitas pesquisas" e "nada construído" não aparecem no contrato.

**Dono da decisão.** O designer e o skeptic preparam o critério; o `final_approver` aceita o `criterion.md` congelado (`.../experiment/SKILL.md:121-126`, `:161-173`). O gate universal permanece humano; não é autorização inferida do ledger.

**Falsificador.** Uma observação nomeada e regra mecânica que leve a `FALSIFIED`; se nada pode falsificar ou se o probe não discrimina a hipótese, o próprio desenho é `INVALID` (`:78-91`, `:100-119`).

**Próxima ação.** Oferecer **pré-registro**; se aceito, produzir `criterion.md`. Rodar/adjudicar é dispatch posterior (`:131-156`, `:169-179`). Rodada que exige execução de código espera o tipo `code` ficar LIVE (`:149-156`).

### A2 — O router não contém gatilho epistemológico de "pesquisa sem build"

**Prova.** Os únicos triggers universais de dispatch são síntese de 3+ fontes/retornos, proteção de contexto, isolamento e paralelismo (`implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md:33-42`). O mesmo router declara que não faz julgamento específico de research/review/experiment (`:1-18`) e remete o julgamento de tipo ao owner (`:188-202`). Busca textual nas famílias de owners, MARS, Decision Gate e autoridade v2 não encontrou regra por número de pesquisas nem por ausência de implementação.

**Owner/status.** Owner: `domainspec-subagents-strategy`; operacional repo-local. Status de `experiment`: LIVE; `suggestion`, `plan` e `code`: RESERVED.

**Condição de transição.** O router apenas decide se vale um dispatch e exige confirmação; ele não decide quando uma sequência de pesquisas amadureceu epistemicamente.

**Dono da decisão.** Usuário no gate de confirmação; silêncio ou discussão não são confirmação (`.../domainspec-subagents-strategy/SKILL.md:84-97`).

**Falsificador.** Este achado cai se existir outro owner vigente que defina explicitamente um trigger por histórico do ledger ou por ausência de build e tenha precedência sobre estes arquivos.

**Próxima ação.** A nova recomendação precisa ser uma política separada de detecção/oferta; não deve ser apresentada como semântica já existente do tipo `experiment`.

### A3 — MARS fornece critérios fortes para promover candidato, mas só dentro de MARS

**Prova.** O template exige dono da decisão, questão, sinal primário, rival forte, resultado desconfirmador, bloqueios, gates e próximo passo (`implementation/mars/templates/experiment-candidates-template.md:12-26`). A sequência prefere o experimento que separa hipóteses rivais, rejeita candidato sem dono e proíbe promover a design de protocolo sem resultado desconfirmador explícito (`:28-32`).

**Owner/status.** Owner de programa: MARS; status do template não é declarado no arquivo. O pipeline ao qual pertence se declara canônico apenas para MARS (`implementation/mars/definitions/MARS-PIPELINE.md:1-5`). Último precedente Git do template: commit de 2026-04-26; por isso não o tratei como regra global atual.

**Condição de transição.** Há duas ou mais hipóteses concorrentes relevantes, um teste diferencia entre elas, um dono precisa da resposta e o resultado desconfirmador é explícito.

**Dono da decisão.** Campo obrigatório `Decision owner` (`.../experiment-candidates-template.md:12-15`); o template não fixa uma função universal.

**Falsificador.** Campo obrigatório `Disconfirming outcome` e rival mais forte (`:21-24`).

**Próxima ação.** Uma das quatro, conforme prontidão: `scope more`, `design protocol`, `source data` ou `do not run yet` (`:24-26`). Isso é uma boa taxonomia de recomendação, não uma autorização automática.

### A4 — Passar de protocolo para execução requer prontidão, não entusiasmo

**Prova.** MARS bloqueia execução quando qualquer hard gate falha (`implementation/mars/definitions/MARS-PIPELINE.md:48-59`): fundações, protocolo mensurável, seleção de fontes, inventário e integridade. G3 pertence ao Inventorist e, quando falha, para a execução e devolve remediação (`implementation/mars/definitions/INVENTORY-READINESS-GATE.md:1-7`); suas saídas distinguem `PASS`, `NEEDS-REVISION` e `BLOCKED` (`:27-43`).

**Owner/status.** Owner de G3: Inventorist; status: contrato obrigatório MARS. Aplicabilidade: execução MARS, não trigger global do orchestrator.

**Condição de transição.** Só de protocolo/fontes para execução após gates G1-G3; G4 adjudica integridade depois da captura.

**Dono da decisão.** Protocol Designer em S3, Sourcer em S4-S5, Inventorist em S6 e Scientist em S7 (`.../MARS-PIPELINE.md:9-22`).

**Falsificador.** Falha de mensurabilidade, versão/pin, cobertura de inventário ou campos obrigatórios não falsifica a hipótese; falsifica **prontidão de execução** e devolve `BLOCKED`.

**Próxima ação.** Remediar o gate específico; não executar enquanto bloqueado (`.../INVENTORY-READINESS-GATE.md:16-43`).

### A5 — Precedente positivo: pesquisa recomendou teste porque o probe ficou especificável

**Prova.** `cyberAlchemy-v2/development/research/2026-07-11-investor-language-customer-value/findings.md` é `governing-research-findings`, `status: complete` (`:1-8`). O veredito foi `GO` para experimento comercial bounded, mas matou afirmações não sustentadas (`:13-25`). A justificativa explícita não foi volume de pesquisa: evento, fronteira, tipos de fonte, papéis de autoridade e resultados mensuráveis podiam ser pré-registrados (`:117-132`).

**Owner/status.** Owner formal não consta; artifact role: governing research findings; status: complete. O customer-authorized release owner retém autoridade operacional (`:17-25`, `:123-130`).

**Condição de transição.** Oferta coerente e mensurável, ainda comercialmente não testemunhada; baseline, contrafactual, métricas e autoridade já especificáveis.

**Dono da decisão.** Hipótese de buyer/payor: VP Engineering ou equivalente, com signer autorizado; autoridade de deploy permanece no release owner (`:121-130`). O próprio documento marca essas funções econômicas como não testemunhadas.

**Falsificador.** Menos de 2 aceitações pagas em 10 ofertas qualificadas; ou, após 3 pilotos pagos, menos de 2 atingirem thresholds pré-registrados, nenhuma recompra, burden inaceitável ou requisito material perdido (`:131-132`).

**Próxima ação.** `GO TO TEST`, inicialmente em paralelo ao processo competente existente, medindo benefício líquido do burden e confounds (`:129-132`, `:180-210`).

### A6 — Precedente negativo: pesquisa resolvida pode ir direto a plano/task-session

**Prova.** A decisão `cyberAlchemy-v2/development/research/2026-07-02-validators-as-moat/DECISION.md` está `resolved`, foi decidida pelo usuário via Decision Gate e deriva de uma pesquisa tensionada (`:1-10`). Ela registra nenhum blocker e encaminha productização e hardening para `invoke plan`/`task-session`, não para experimento (`:55-62`). O AGENTS atual delimita `invoke` como autor de define/design/plan/handoff/refresh e `task-session` como executor de um task/SWU (`AGENTS.md:112-114`).

**Owner/status.** Decidido pelo usuário via Decision Gate; status resolved.

**Condição de transição.** A pesquisa já resolveu a escolha load-bearing e o follow-on é implementação concreta.

**Dono da decisão.** Usuário, explicitamente registrado.

**Falsificador.** Nenhum falsificador explícito para a decisão; o documento registra pressupostos, logo é precedente limitado, não experimento.

**Próxima ação.** Planejar/executar o hardening. Este caso refuta a regra "pesquisa acumulada sem build sempre pede experimento".

### A7 — Esperar e parar precisam continuar opções legítimas

**Prova.** Decision Gate é usado quando trabalho consequencial deve parar até decisão explícita (`arcanum/arcana/decision-gate/SKILL.md:12-28`). Ele continua até resolução ou até o usuário deferir/parar, e bloqueia mutação enquanto a escolha seguir aberta (`:90-91`). O contrato manda preservar `defer` e `stop` como opções legítimas e considera erro descartá-las (`:179-209`).

**Owner/status.** Owner: Arcanum Decision Gate na working copy; skill limpa nos paths inspecionados, mas o submódulo Arcanum está globalmente divergente no worktree, portanto não promovo isso a regra do orchestrator atual sem reconciliação.

**Condição de transição.** Existe decisão blocker-level com duas ou mais opções admissíveis.

**Dono da decisão.** Usuário/humano; o agente estrutura opções e recomendação, não presume consentimento.

**Falsificador.** Não aplicável como falsificação de hipótese; o gate é de governança decisória. A recomendação fica inválida se não houver escolha consequencial real.

**Próxima ação.** `proceed`, `ask remaining decision` ou `stop` (`:229-237`). Para o novo mecanismo, "não sugerir agora" e "adiar até sinal X" devem ser resultados de primeira classe.

## Matriz compacta de precedentes

| Precedente | Autoridade/status | Condição observável de transição | Dono da decisão | Resultado que derruba/bloqueia | Próxima ação suportada |
|---|---|---|---|---|---|
| Tipo `experiment` | Repo-local, LIVE | Hipótese única + critério congelável + ambos os resultados informativos | final approver no gate humano | hipótese não falsificável, confound ou não-discriminação → `INVALID` | pré-registrar `criterion.md`; rodar depois |
| Router | Repo-local, operacional | 3+ retornos, contexto, isolamento ou paralelismo justificam **dispatch**, não o tipo | usuário confirma | nenhum trigger P1 ou falta de confirmação | inline/stop ou dispatch confirmado |
| Candidate template MARS | Canônico só no programa MARS | teste separa hipóteses, dono existe, desconfirmação explícita | decision owner nomeado | sem dono ou sem disconfirming outcome | scope / protocolo / fontes / não rodar |
| Gates MARS | Obrigatório só no MARS | protocolo/fontes/inventário prontos | owners S3-S7 | hard gate falha | remediar; execução bloqueada |
| Release-review 2026-07-11 | Histórico, complete | valor segue unwitnessed, mas probe ficou pré-registrável | buyer/signatário + release owner | critérios pagos/operacionais em `:132` | GO TO TEST em shadow mode |
| Validators-as-moat 2026-07-02 | Histórico, resolved | decisão já fechada e follow-on implementation-shaped | usuário | não explicitado | invoke plan / task-session |
| Decision Gate | Arcanum atual na working copy | decisão consequencial multi-opção | usuário | opção real ausente ou blocker não resolvido | proceder, deferir ou parar |

## Implicação para o trigger a pesquisar

O sinal promissor não é um contador; é uma **mudança de forma da incerteza**. Uma recomendação passa a ser defensável quando o histórico mostra simultaneamente:

1. uma decisão relevante ainda não resolvida;
2. uma hipótese explícita cujo contrário mudaria o próximo passo;
3. uma observação/fixture/probe possível e delimitada;
4. critério e categorias fixáveis antes de olhar o resultado;
5. resultados favorável e desfavorável ambos informativos;
6. dono humano da decisão e alternativa legítima de deferir/parar;
7. ausência de evidência de que a decisão já está pronta para `invoke plan`/`task-session`.

"Várias pesquisas" pode servir como **sinal de busca** para avaliar esses sete itens. "Nada construído" pode servir como aviso de estagnação. Nenhum dos dois deve ser o veredito.

## Drift e limites

- O owner repo-local do router ainda declara schema `0.7.0` (`.../domainspec-subagents-strategy/SKILL.md:84-97`), enquanto a cópia gerada `.claude/skills/domainspec-subagents-strategy/SKILL.md` está modificada no worktree e declara `0.8.0` com semântica de equivalência material (`:95-130`). Como o próprio router manda preferir o owner repo-local, não importei a regra nova. Isso precisa ser reconciliado antes de reutilizar mecânica de dispatch no orchestrator atual.
- `promotion-policy.md` é apenas candidate local; seu princípio "promove por owner route, não por entusiasmo" é coerente, mas não foi usado como autoridade (`cyberAlchemy-v2/authority/promotion-policy.md:1-6`).
- MARS governa experimentos de pesquisa estruturados; Experiment Harness governa validação repetível de spells/sigils. Nenhum dos dois deve ser confundido com o tipo LIVE `dispatch_type: experiment` sem um adaptador explícito.
- A busca de ausência foi restrita às famílias declaradas. Ela não prova que o repositório inteiro nunca contém outra proposta de trigger.

## Fato que mais invalidaria esta interpretação

O fato mais forte seria encontrar um **owner vigente com precedência sobre o tipo LIVE e o router repo-local** que defina explicitamente: (a) um limiar observável no ledger para "pesquisa suficiente sem construção", (b) autorização para recomendar ou abrir automaticamente um experimento e (c) a semântica de execução correspondente. Isso derrubaria tanto a conclusão de que o trigger ainda não existe quanto a separação aqui proposta entre detecção, oferta, pré-registro e rodada.


## Source 2 — `scout-domainspec-cases.md`

# DomainSpec-core historical cases: research-to-action transitions

## Scope and method

This is a bounded, read-only reconstruction of transition episodes in
`C:/Users/victo/domainspec-core`. It uses the append-only dispatch ledger as the
starting index, then checks the linked findings, specifications, run results,
validation receipts, and implementation artifacts. Repository sources were not
modified and commands or tests described by historical receipts were not rerun.

The current ledger is strongly asymmetric: a mechanical count of opening rows
finds 190 `research`, 89 `review`, four `experiment`, one `code`, and one `plan`
dispatch. Consequently, absence of a `code` row is not credible evidence that
nothing was built. The single `code` row is
`2026-06-15-research-md-lean-permguard-edit`; the four experiment rows are the
three Mint rows around [the first criterion and run](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L1739)
and the later [intent-population run](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L3769).

## Direct answer

The corpus supports recommending an experiment after research, but not from a
dispatch count or the absence of `code`. The strongest historical pattern is:

1. linked research narrows a load-bearing claim rather than merely closing;
2. a surviving uncertainty is expressed as a falsifiable criterion;
3. a named decision would change under either result;
4. prerequisite owners, inputs, and claim ceilings are settled; and
5. no current artifact or prior run has already answered the question.

If (4) is false, the recommendation should be the missing decision, specification,
or build step required to make the experiment admissible. If (5) is unknown, the
system should abstain and ask for or perform an artifact-state check. The cases
below are evidence for that distinction.

## Episode 1 — Machine-map research to a falsifying Mint experiment

**Originating objective.** The `2026-06-24-machine-map-and-moat` research asked
for a reconciled system map, first-build sequence, and moat verdict
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L1505)).
It corrected the original framing: the “foundry” claim depends on keeping outer
meta-authority distinct from the minted domain's object-authority
([findings](../../../domainspec-core/development/machine-map/findings.md#L39)),
and the overall machine remained a roadmap, “mostly unbuilt”
([findings](../../../domainspec-core/development/machine-map/findings.md#L15)).

**Research sequence and epistemic advance.** The advance was not closure alone:
the research converted a broad “make the machine” thesis into a narrower,
discriminating claim about whether Mint actually preserves the meta/object
boundary. The following experiment froze one hypothesis and explicitly rejected
self-confirming evidence such as “files exist in the right folders”
([criterion](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-foundry-boundary/criterion.md#L62),
[circularity guard](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-foundry-boundary/criterion.md#L75)).

**Next action and build state.** The criterion was preregistered before the run
([criterion](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-foundry-boundary/criterion.md#L23));
the run then minted and scored three domain spines. It falsified the strong
uniform foundry-boundary claim because the research domain failed Obs-A
([run findings](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-foundry-boundary/run/findings.md#L16),
[verdict](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-foundry-boundary/run/findings.md#L23)).
A corrected content-autonomy criterion later survived all nine cells while
retaining an explicit weakness in one lexical discriminator
([second run](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-content-autonomy/run-findings.md#L109),
[caveat](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-content-autonomy/run-findings.md#L116)).
Concrete minted artifacts were built inside the experiment folders, but this was
experimental evidence, not a shipped runtime.

**Linkage quality: high but not ledger-native.** The criterion cites the
machine-map synthesis and the experiment follows it chronologically; neither row
contains a machine-readable parent/objective edge. The linkage is therefore
artifact-backed, not derivable from row type and time alone.

**Plausible counterinterpretation.** This is evidence that an experiment was a
productive next step, not evidence that the ledger itself could have known when
to suggest it. The decisive bridge—the falsifiable foundry-boundary claim—lives
in artifacts.

## Episode 2 — Two high-attention researches to a specification, not yet a run

**Originating objective.** The first research asked whether small-parameter
models can have unusually large usable context and requested testable hypotheses
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L1726)).
Its substantive result separated visible context from usable context and selected
a parameter-normalized measurement harness as the best lane
([findings](../../../domainspec-core/research/high-attention-low-parameter-models/findings.md#L7),
[verdict](../../../domainspec-core/research/high-attention-low-parameter-models/findings.md#L38)).

**Research sequence and epistemic advance.** A second research dispatch explicitly
started from the first one's unresolved methodology and sought a reproducible,
resource-bounded protocol
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L3548)).
It selected concrete comparison families, fixture classes, controls, measures,
and a staged escalation policy. Its own verdict is unusually useful telemetry:
the research is “decision-ready input” for a later specification, while the
runnable-witness gate is KILL and execution remains blocked
([protocol findings](../../../domainspec-core/research/high-attention-low-parameter-models/experiment-protocol-research/findings.md#L7),
[verdict matrix](../../../domainspec-core/research/high-attention-low-parameter-models/experiment-protocol-research/findings.md#L86)).

**Next action and build state.** A complete specification/work-pack package was
subsequently authored, but it declares `executionReadiness: blocked`
([spec](../../../domainspec-core/research/high-attention-low-parameter-models/experiment-protocol/SPEC.md#L4))
and lists immutable artifacts and human decisions required before a run
([execution boundary](../../../domainspec-core/research/high-attention-low-parameter-models/experiment-protocol/SPEC.md#L136)).
No executable experiment result was found in this bounded folder.

**Linkage quality: high.** The second goal names the existing findings, its folder
is nested below the first, and the specification points back to the research as
its discovery artifact. Again, that continuity is visible in prose and paths,
not a parent field.

**Plausible counterinterpretation.** “Several resolved researches and no code”
would suggest an experiment too early here. The evidence-backed recommendation at
the second close was to author/freeze the specification and resolve owner choices,
not to run. The later specification still says the run is blocked.

## Episode 3 — IOLM research led to implementation without a `code` dispatch

**Originating objective.** `2026-07-22-iolm-workable-example-research` asked for
the fastest governed route to a runnable local graph UI while preserving the
blocked compiler proof boundary
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L3710)).

**Epistemic advance.** The findings selected an exact fixture-backed SWU, write
boundary, input bundle, native-web stack, and claim ceiling. At research close it
said the UI did not yet exist and could be built after proposal approval
([findings](../../../domainspec-core/cyberAlchemy-v2/development/research/2026-07-22-iolm-workable-example/findings.md#L7),
[verdict](../../../domainspec-core/cyberAlchemy-v2/development/research/2026-07-22-iolm-workable-example/findings.md#L17)).

**Next action and build state.** The implementation now exists at the exact
selected path, with server, HTML/CSS/ES modules, binding schemas, Python and Node
tests, and run receipts. Its README provides runnable commands and preserves the
non-authority boundary
([README](../../../domainspec-core/cyberAlchemy-v2/development/iolm-workable-example/README.md#L1),
[checks](../../../domainspec-core/cyberAlchemy-v2/development/iolm-workable-example/README.md#L30)).
`git log -- <research-folder> <implementation-folder>` attributes both surfaces
to commit `3e31c8e79` on 2026-07-23, immediately after the research. A later replay
is currently BLOCK because the pinned source fixture drifted, which is evidence
that something was built and later became stale—not that nothing was built
([validation receipt](../../../domainspec-core/cyberAlchemy-v2/development/iolm-workable-example/generated/runs/20260722T182915Z-firefox-replay/validation-summary.json)).

**Linkage quality: high.** Exact path and interface correspondence plus a shared
commit connect findings to implementation. There is no corresponding `code`
opening in the ledger.

**Plausible counterinterpretation.** The later BLOCK could be mistaken for
“unbuilt.” It actually reports a fail-closed hash mismatch in an existing system.
Recommending an experiment from ledger-type absence would be strictly worse than
recommending repair/revalidation.

## Episode 4 — Research contract to an admitted experiment and owner decision

**Originating objective.** `2026-07-22-agent-reasoning-engine-contract` began as
research into the smallest non-vacuous pre-action reasoning-engine contract
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L3723)).
The later experiment row explicitly records that definition, experiment design,
planning, and evidence mechanics were complete before the clean rerun
([experiment](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L3769)).

**Epistemic advance and next action.** The pre-registered 15-sample population
run executed rather than merely proposing a witness. All 15 source locks and
structural validations passed, including 3/3 unchanged-rule holdouts
([result](../../../domainspec-core/cyberAlchemy-v2/development/agent-reasoning-engine/experiments/intent-schema/runs/2026-07-22-intent-schema-02/RESULT.md#L11)).
It exposed consequential missingness in 15/15 records and replacement risk in
11/15, then stopped at an explicit owner gate rather than promoting its result
([pressure findings](../../../domainspec-core/cyberAlchemy-v2/development/agent-reasoning-engine/experiments/intent-schema/runs/2026-07-22-intent-schema-02/RESULT.md#L38),
[next gate](../../../domainspec-core/cyberAlchemy-v2/development/agent-reasoning-engine/experiments/intent-schema/runs/2026-07-22-intent-schema-02/RESULT.md#L67)).
The experiment folder contains the populated records, manifests, reducer, audit
script, metrics, evidence cards, and adjudication packet.

**Linkage quality: medium-high.** The experiment context names completion of the
upstream stages, but the ledger does not persist their individual artifact links
or a parent ID. The result itself provides strong executed evidence.

**Plausible counterinterpretation.** A clean structural pass might look like
validation of the schema. The result explicitly limits itself to bounded shape
evidence and leaves schema selection pending; the experiment recommended a human
decision, not implementation.

## Episode 5 — Ontology research advanced, but owner selection and build came first

**Originating objective.** The July 26 gap research asked for the smallest
defensible working ontology prototype and a falsifiable acceptance contract
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L4054)).

**Research sequence and epistemic advance.** It found that the repository did not
yet contain a working ontology prototype, separated present narrow machinery from
stale bindings, and specified a finite positive/fail/indeterminate witness
([findings](../../../domainspec-core/cyberAlchemy-v2/development/research/2026-07-26-ontology-working-prototype-gap/findings.md#L7),
[current execution state](../../../domainspec-core/cyberAlchemy-v2/development/research/2026-07-26-ontology-working-prototype-gap/findings.md#L18)).
Its ordered route begins with contract freeze and implementation of a closed-world
validator, not an experiment run
([build slices](../../../domainspec-core/cyberAlchemy-v2/development/research/2026-07-26-ontology-working-prototype-gap/findings.md#L136)).

Four days later, ontology-runtime API research narrowed the reusable runtime
contract further. It classified every endpoint as designed and owner-absent and
blocked implementation until runtime-contract and implementation owners are
selected
([findings](../../../domainspec-core/cyberAlchemy-v2/ontology/development/2026-07-30-ontology-runtime-api-research/findings.md#L30),
[endpoint boundary](../../../domainspec-core/cyberAlchemy-v2/ontology/development/2026-07-30-ontology-runtime-api-research/findings.md#L357)).
The folder then accumulated Define/Design/Plan/Work-Pack artifacts, but the
research itself says these do not authorize or prove a runtime.

**Next action and build state.** The justified next action was owner selection and
bounded implementation of the finite witness. Suggesting “run an experiment” at
the first or second research close would skip the missing apparatus and owner.

**Linkage quality: medium.** Topic, sources, and dates support a chain, but no
machine-readable parent/objective edge proves that the two dispatches are the
same lineage. A trigger must not silently infer identity from “ontology” words.

**Plausible counterinterpretation.** The finite witness could itself be called an
experiment in casual language. In this repository's typed workflow it is first a
validator/runtime implementation with acceptance tests; relabeling it would
collapse `code` and `experiment` rather than improve routing.

## Episode 6 — Research after an existing build

**Originating objective.** The Body War gap research explicitly opened after the
SuggestedTrack API/UI and validation already existed
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L4268)).

**Epistemic advance.** It distinguished a current fake-provider developer path
from consent, route-binding, retry, hosted-provider, and participant evidence.
The attached current-validation receipt records successful build/validation,
unit, Postgres e2e, and Chromium runs
([receipt](../../../domainspec-core/projects/body-war/development/research/20260727-suggested-track-testable-prototype-gap/CURRENT-VALIDATION.md#L13))
while sharply limiting what those passes prove
([proof ceiling](../../../domainspec-core/projects/body-war/development/research/20260727-suggested-track-testable-prototype-gap/CURRENT-VALIDATION.md#L37)).

**Next action and build state.** The findings select LP-01, a bounded product fix,
before moderated local participant sessions; they explicitly do not authorize or
execute it
([findings](../../../domainspec-core/projects/body-war/development/research/20260727-suggested-track-testable-prototype-gap/findings.md#L24)).
Something substantial was already built even though no `code` dispatch describes
that build in this ledger.

**Linkage quality: high for current state, low for original build provenance.**
The receipt binds tests to commit `b7d60c96...`; the ledger does not explain the
build's complete history.

**Plausible counterinterpretation.** Multiple research rows around Body War might
look like pre-build analysis when they are actually post-build gap analysis.
After LP-01 passes, a bounded participant test may be appropriate, but the correct
recommendation before that is implementation.

## Counterexamples to the proposed shortcut

The rule “multiple resolved research dispatches plus no code dispatch means
recommend experiment” fails in at least four distinct ways:

| Failure mode | Concrete case | What the shortcut gets wrong |
|---|---|---|
| Build exists without `code` telemetry | IOLM and Body War | Infers non-construction from a nearly unused dispatch type. |
| Research is decision-ready but execution apparatus is absent | High-attention protocol | Recommends a run before owner decisions, fixtures, scorer, runtime, and admission. |
| The next uncertainty is an implementation/ownership gap | Ontology prototype/runtime | Calls acceptance-contract construction an experiment and skips the owner gate. |
| A prior experiment already answered or narrowed the claim | Mint; intent-population | Risks recommending a duplicate run instead of consuming the result and routing its residue. |

`resolved` is also too weak: it says the dispatch closed successfully, not that a
claim survived, a decision became ready, or the same objective continued. The
high-attention findings expose richer local states—`decision-ready`, runnable
witness `KILL`, and execution `blocked`—that are absent from the close row.

## Candidate transition signals, ranked

### 1. Explicit decision-bearing experiment handoff — strongest

**Signal.** A linked research artifact names (a) one surviving falsifiable claim,
(b) the decision owner, (c) outcomes that would change the decision, (d) frozen or
admissible inputs, and (e) a recommendation to test. Mint and the intent-population
run are the positive precedents.

**Why strong.** It observes epistemic readiness and action relevance directly,
rather than inferring them from counts.

**Strongest invalidator.** Any required criterion, owner, input lock, admission
gate, or claim ceiling is still unresolved. In that case recommend the missing
precondition, not the experiment.

### 2. Surviving claim plus closed negative and an unspent decision — strong

**Signal.** Reviewer/auditor artifacts preserve a non-vacuous claim, state its
collapse-test, and show that no existing run or implementation evidence answers
it. Both possible outcomes have explicit downstream consequences.

**Why strong.** It distinguishes “research accumulated” from “research produced a
testable fork.”

**Strongest invalidator.** A current artifact, prior run, or accepted owner
decision already resolves the fork; recommend consuming/revalidating that evidence
instead.

### 3. Explicit research-to-specification readiness with prerequisites satisfied — medium-strong

**Signal.** Findings mark research as decision-ready for an experiment
specification, and the later specification's readiness/admission checklist is now
fully satisfied.

**Why not stronger.** High-attention shows that decision-ready research and a
written specification can coexist with a blocked run. The trigger needs the later
state, not only the research close.

**Strongest invalidator.** The current specification still says `blocked`,
`decision-gated`, `NOT_RUN`, or lists unresolved human choices.

### 4. Repeated linked research with stable objective and diminishing new residue — medium

**Signal.** Two or more research artifacts share an explicit objective/parent,
each consumes the previous result, the surviving claim remains stable, and later
work mostly refines test mechanics rather than opening new conceptual questions.

**Why only medium.** The present ledger lacks reliable lineage fields; folder
nesting, wording, and temporal adjacency can misjoin unrelated work.

**Strongest invalidator.** The later dispatch changes the objective, introduces a
new owner boundary, or records materially new open questions. Continued research
may then be productive rather than inertial.

### 5. No current construction found after artifact-level verification — weak supporting signal

**Signal.** A bounded current-byte check across the declared write surface and
linked repositories finds no implementation, run receipt, or accepted witness.

**Why weak.** It can support signals 1–4 but cannot justify a recommendation by
itself. IOLM and Body War show why ledger-type absence is insufficient.

**Strongest invalidator.** Any unregistered, cross-repository, externally hosted,
stale-but-real, or differently typed build is found.

### Rejected signal: count/time threshold

“N resolved researches” or “T days without `code`” has no defensible evidential
rank in this corpus. Its strongest invalidator is already observed: successful
builds exist without `code` rows, while long research sequences can correctly end
in owner decisions, specifications, or further research.

## Implication for a future recommendation trigger

The ledger can cheaply nominate candidates, but artifact evidence must adjudicate
them. A defensible trigger would therefore be two-stage:

1. **Nominate:** cluster explicitly linked research under the same objective and
detect a surviving experiment-shaped handoff.
2. **Adjudicate:** read the latest findings/spec/result plus declared write surfaces
to confirm decision relevance, readiness, no prior answer, and no existing build
that changes the route.

The recommendation should carry its evidence and abstention reason, for example:
“Research R1/R2 leaves hypothesis H untested; criterion C is frozen; decision D
changes under either outcome; no run receipt was found. Suggest experiment E.”
If any clause is unsupported, the system should name the missing evidence rather
than imply that an experiment is due.


## Source 3 — `scout-superinterviewer-policy.md`

# Superinterviewer scout — interaction policy for recommending a test

## Scope and disposition

This is a bounded, read-only extraction from `C:/Users/victo/superinterviewer`. No external literature or independent empirical corpus was examined. The repository contains a proposed product and research foundation, so the result below is a **candidate interaction policy**, not a validated trigger or product authority.

The strongest supported conclusion is negative: **“several research runs and no observed construction” is not, by itself, enough to recommend an experiment**. The corpus supports a suggestion only when a live decision-relevant distinction can be named, an observable result could change a live alternative or next step, and a reversible candidate can produce that result at acceptable burden and risk. Lack of construction may instead reflect deliberate exploration, missing authorization, a world-owned signal that should be retrieved rather than tested, a direct-answer preference, a named reason to wait, or a legitimate decision not to act.

## Authority separation

### Ratified repository authority

The governing repository policy requires claims no stronger than evidence, preserves counterevidence and typed residue, and forbids silently promoting inferred intention, assent, reduced uncertainty, a proposed next step, or execution completion into user intention, consent, benefit, authorized action, or accepted evidence (`C:/Users/victo/superinterviewer/AGENTS.md:3-18`). Consequently, the system may **offer** a test but cannot infer that the person wants experimentation, treat uptake as broad consent, launch the test, or count completion as validation without separate authority and evidence.

### Proposed product and research policy

The product charter is explicitly proposed and unratified. It says the person retains authority to correct, refuse, restore a frame, and decide what follows; direct answer, deferral, branching, and stopping are legitimate outcomes (`product/CHARTER.md:3-24`). Its learning condition requires independent episodes, attributable decision-relevant change, preserved agency, superiority to simpler baselines, and acceptable burden and risk (`product/CHARTER.md:30-32`).

The research plan proposes testing asking, informing, suggesting, reframing, waiting, and advancing rather than assuming their taxonomy or policy is settled (`research/research-plan.md:290-305`). It also requires comparison against direct answers and simpler baselines and permits stopping or reframing when those baselines win (`research/research-plan.md:474-505`). These are research obligations, not evidence that the candidate policy works.

### Internal synthesis

The internal synthesis proposes the source-of-signal rule: ask when the person likely owns the signal; retrieve or test when the world owns it; suggest when a reversible candidate could unlock learning; reframe when representation is the bottleneck. Waiting, silence, direct answer, referral, branching, and stopping remain first-class alternatives (`research/foundation-game-framing/research.md:21-27`). The proposed turn grammar is `prior state → missing distinction → intervention → signal → contestable delta → next step or typed residue`, but it is an observation candidate, not a settled ontology (`research/foundation-game-framing/research.md:5-13`).

### Open residue

No independent corpus, literature review, or controlled comparison has validated the product framing (`research/foundation-game-framing/research-initial-definitions.md:26-41`). The relative weighting of decision relevance, discriminating power, reversibility, burden, privacy, induction risk, and cost is unknown and may vary by person, domain, and risk (`research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:96-104`). Also unresolved are what observable evidence separates autonomous revision from compliance, when waiting/direct answer/stopping count as success, what constitutes permission to recommend, and who validates an appropriate next step (`research/foundation-game-framing/lanes/03-agency-governance.md:137-152`).

## Candidate constraints for a test suggestion

### Minimum eligibility

A test suggestion is eligible only if all of the following are present:

1. **Live consequence:** at least one plausible result could change a live alternative, next action, safeguard, or stop decision (`docs/game/THINKING-THE-GAME.md:28-32`). “More knowledge” without a named consequence is insufficient.
2. **Named missing distinction:** the proposed test distinguishes something that blocks a choice, understanding, action, test, or legitimate deferral. If that distinction cannot be named prospectively, the system should ask or preserve uncertainty rather than retrospectively invent the test's purpose (`research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:56-66`; `research/foundation-game-framing/lanes/01-auditable-transition.md:42-50`).
3. **World-owned observable:** the decisive signal is in evidence, comparison, calculation, observation, or the result of action—not merely in the person's unelicited preference or authorization (`docs/game/QUESTION-LANDSCAPE.md:5-19`). If the person owns the signal, ask; if an existing source owns it, retrieve before experimenting.
4. **Recoverable probe:** the candidate is small and reversible, and its assumptions and disconfirming result can be exposed. The local landscape explicitly prefers reversible, low-cost probes when expected value is similar (`docs/game/QUESTION-LANDSCAPE.md:21-29`).
5. **Contestable offer:** identify that it is a proposal, whose proposal it is, what assumptions it makes, what permission it requires, what result would change, and how the person can decline or amend it. Suggestion introduces a candidate commitment and carries anchoring, compliance, and disguised-decision risks (`research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:69-80`).
6. **Proportionate burden:** among eligible moves, a test should beat asking, retrieving, reframing, waiting, or directly answering on a local ordinal comparison: greater decision relevance, discrimination, answerability, and reversibility; lower cognitive load, time, privacy exposure, induction risk, cost, and irreversibility (`docs/game/THINKING-THE-GAME.md:28-32`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:96-104`).

### Autonomy and authorization boundary

Declared intention, system inference, proposed revision, confirmed revision, operational commitment, and system intervention intent must remain distinct; confirming one does not authorize recommending, executing, remembering, or sharing another (`authority/AUTHORITY-MODEL.md:19-21`). Therefore:

- the ledger may support a system inference such as “research appears to have reached a decision boundary,” but the prompt must expose that inference and invite correction;
- a recommendation should not claim that experimentation is the user's objective merely because research accumulated or construction did not occur;
- accepting the recommendation authorizes neither execution nor persistence unless separately scoped;
- a refusal, correction, request for a direct answer, or silence is a valid counter-move, not failure (`research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:78-80`).

### Integration after the move

If a suggestion is offered, the interaction should preserve: what changed, what did not, who accepted or contested it, and what remains unresolved. A result may end in a next step or typed residue; execution is not required (`research/foundation-game-framing/lanes/01-auditable-transition.md:93-105`). An observed run proves neither causation nor benefit: acceptance may arise from fatigue, deference, persuasion, or a desire to finish (`research/foundation-game-framing/lanes/01-auditable-transition.md:62-70`).

## Implication for a ledger-based trigger

The ledger should be treated as a **candidate detector**, not a decision maker. A safe recommendation needs evidence for at least these distinctions:

| Needed signal | Likely owner | What the system may infer | What still needs confirmation or observation |
|---|---|---|---|
| A live choice or blocked next possibility | person, sometimes joint | repeated research may indicate a boundary | whether any choice is actually live and whether action is desired |
| A discriminating uncertainty | person and/or world | unresolved, conflicting, or repeatedly revisited findings may nominate one | which result would materially change the person's decision |
| Existing evidence versus absent evidence | world/corpus | whether the ledger links a source or only a gap | whether retrieval is sufficient before a new test |
| Permission and hard constraints | person/authority | none from silence or prior assent | whether suggestions are welcome and what must not be sacrificed |
| Reversibility, cost, and risk | world plus person | provisional estimate | acceptability and domain-specific competence/safety boundary |
| Experiment outcome | world | observed result only | interpretation, acceptance, and authorization of the next action |

Thus the correct interaction is usually a **conditional offer**, for example: “The research appears to leave X as the distinction blocking Y. A small reversible test Z could distinguish A from B. If that is not the decision you are making—or you prefer a direct answer, more evidence, waiting, or stopping—we should not run it.” This wording is an inference from the candidate policy, not a ratified script.

## Decision table

| Observed condition | Preferred move | Why | Abstain/suppress condition | Citation |
|---|---|---|---|---|
| The person owns the missing preference, experience, constraint, interpretation, or authorization | **Ask** one decision-changing question | The system cannot recover a user-owned signal from external evidence or ledger history | No plausible answer changes a live alternative, safeguard, next move, or stop decision; question is high-burden, invasive, concealed-purpose, or difficult to refuse | `docs/game/QUESTION-LANDSCAPE.md:7-19,21-31`; `docs/game/THINKING-THE-GAME.md:19-32` |
| The missing signal exists in a source, calculation, comparison, or observation | **Retrieve / inform** | World-owned evidence should not be displaced by further introspection | Retrieval cannot discriminate the alternatives, source authority would be laundered into truth, or information overload exceeds local value | `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:69-76,96-104` |
| A live decision-relevant distinction requires a new observable, and a small recoverable action can produce it | **Suggest a bounded test** | A reversible candidate can unlock learning without claiming the action or interpretation is established | No named decision-changing result; existing evidence is sufficient; candidate is irreversible, costly, unsafe, outside competence, difficult to refuse, or lacks permission; “no construction” is the only trigger | `docs/game/QUESTION-LANDSCAPE.md:5-19,21-29`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:73-101` |
| The current representation hides or collapses the decisive distinction | **Offer a contestable reframe** | Changing the representation may reveal alternatives that another question or test would miss | The old frame, trade-offs, excluded alternatives, and route back cannot be exposed; reframe risks goal substitution or capture | `docs/game/THINKING-THE-GAME.md:19-32`; `research/foundation-game-framing/lanes/03-agency-governance.md:52-66` |
| The user asks for an answer and a concise answer is sufficient to enable the choice | **Answer directly** | Inquiry or experimentation adds burden without discriminating value | A direct answer would conceal material uncertainty, exceed competence, or authorize a consequential action the user has not chosen | `product/CHARTER.md:5-15`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:116-126` |
| More inquiry has lower expected value than a named future event, evidence source, or permission | **Wait / deliberately defer** | Non-action preserves option value and avoids manufacturing urgency | There is an immediate safety or time-critical duty requiring referral or qualified help | `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:106-114`; `research/foundation-game-framing/lanes/03-agency-governance.md:99-104` |
| The person can state an authorized, proportionate next step and its decisive reasons or remaining uncertainty | **Advance** | The selected next possibility is no longer blocked; another intervention has lower marginal value | The apparent commitment is only inferred, induced, or accepted under pressure; risks or authority remain unresolved | `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:106-114`; `authority/AUTHORITY-MODEL.md:15-21` |
| Two consecutive moves fail to change alternatives, constraints, authorization, or next step | **Change mode or stop** | Continuing produces burden without observed decision value | The person explicitly chooses open exploration and its burden/risk remains acceptable | `docs/game/QUESTION-LANDSCAPE.md:21-31`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:96-104` |
| Ambiguity is productive, authority is missing, risks dominate, no witness exists, or a simpler baseline wins | **Preserve residue, refer, branch, or stop** | Closure and action are not automatic successes; safety, refusal, and unresolved conflict are legitimate outcomes | Do not use residue as an unfalsifiable dumping ground: name an owner/reopen trigger where one exists | `docs/game/THINKING-THE-GAME.md:42-48`; `research/foundation-game-framing/lanes/01-auditable-transition.md:72-80` |

## Strongest overturning fact

The table should be overturned, not merely tuned, if preregistered comparisons on independent bounded episodes show that its source/eligibility/agency routing cannot be coded reliably **or** that a simpler user-selected mode (especially concise direct answer or ordinary competent conversation) yields equal or better decision quality, correction/refusal, and later reversibility with materially lower burden. The corpus itself names those results as collapse conditions (`docs/game/THINKING-THE-GAME.md:46-48`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:116-129`).


## Source 4 — `scout-superinterviewer-evaluation.md`

# Scout — avaliação do momento de recomendar um experimento

## Escopo e força da evidência

**Conclusão:** o `superinterviewer` contém um desenho interno coerente para avaliar a recomendação, mas não contém validação empírica de que ele funciona. O desenho mais forte combina: (1) uma unidade de episódio auditável, (2) seleção prospectiva entre movimentos concorrentes, (3) comparação com baselines simples, (4) guardrails de agência e carga e (5) uma tabela pré-declarada de `resultado → ação`.

O status importa:

- `research/research-plan.md` é **proposed** e possui apenas autoridade sobre sequência, expectativas de evidência, gates e condições de parada; não possui resultados nem verdade de produto (`research/research-plan.md:1-6, 11-26`; `authority/AUTHORITY-MODEL.md:5-13`).
- `research/foundation-game-framing/research.md` é **internal synthesis with residue**; declara que não examinou literatura externa nem corpus independente (`research/foundation-game-framing/research.md:1-3`).
- `docs/game/THINKING-THE-GAME.md` e `docs/game/QUESTION-LANDSCAPE.md` são **propostas**, não scripts nem políticas validadas (`docs/game/THINKING-THE-GAME.md:1-3`; `docs/game/QUESTION-LANDSCAPE.md:1-3`).
- A lane do episódio auditável terminou `completed_with_residue` e mantém não validadas a confiabilidade entre avaliadores e o valor comparativo (`research/foundation-game-framing/lanes/01-auditable-transition.md:8-21`).
- Promoção para autoridade de produto exige decisão humana explícita; assentimento, execução ou ausência de objeção não bastam (`authority/AUTHORITY-MODEL.md:15-22`).

Portanto, a formulação defensável é: **há um protocolo candidato pronto para um primeiro teste de baixa vinculação; não há ainda uma regra comprovada para recomendar experimentos no momento correto.**

## O que “momento correto” pode significar neste corpus

O corpus não sustenta “várias pesquisas sem construção” como gatilho. Contagem de pesquisas, duração e ausência aparente de artefato não demonstram bloqueio, necessidade de teste nem benefício esperado. O plano diz explicitamente que número de documentos, agentes, turnos, probes ou dispatches não é progresso (`research/research-plan.md:520-529`).

O candidato mais forte é um gate prospectivo e local:

1. Há uma decisão, alternativa, salvaguarda ou escolha de parada viva que continua bloqueada.
2. A incerteza bloqueadora é discriminável: resultados incompatíveis levariam a ações diferentes.
3. O sinal necessário está principalmente no mundo e pode ser obtido por um passo pequeno, recuperável e proporcional. Se a pessoa possui o sinal, perguntar compete melhor; se falta informação, buscar/informar compete; se o frame é o gargalo, reframe contestável compete; esperar, resposta direta e parar continuam admissíveis.
4. Pelo menos um resultado plausível do experimento mudaria uma alternativa, próximo passo, salvaguarda ou decisão de parar.
5. A recomendação expõe que é uma proposta, suas premissas, reversibilidade, permissão necessária, riscos e o que ocorrerá se o resultado for inconclusivo.
6. Entre movimentos elegíveis, ela tem maior valor discriminante esperado a carga, custo, privacidade, indução e irreversibilidade aceitáveis.

Esses critérios derivam dos gates de elegibilidade, fonte, agência e comparação da proposta (`docs/game/THINKING-THE-GAME.md:18-31`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:97-106`) e da família “reversibilidade e probe” (`docs/game/QUESTION-LANDSCAPE.md:13-29`). Eles não fornecem pesos nem um score validado; a comparação é deliberadamente ordinal e contextual.

**Collapse-test do timing:** se avaliadores não conseguem prever, a partir do estado anterior à intervenção, por que recomendar um experimento supera perguntar, informar, responder diretamente, esperar ou parar, “momento correto” vira justificativa retrospectiva. Nesse caso, não há trigger avaliável.

## Requisitos para episódios históricos

O episódio deve ser limitado por um antes/depois e anotado sem preencher lacunas com a teoria desejada. O núcleo explicitamente proposto na lane é (`research/foundation-game-framing/lanes/01-auditable-transition.md:93-107`):

1. identidade e fronteiras do episódio;
2. estado anterior, separando declaração da pessoa e inferência do sistema;
3. distinção possivelmente ausente e sua proveniência (`prospective`, `emergent` ou `retrospective`);
4. intervenção observável, intenção declarada e eventual bundle de movimentos;
5. sinal observável, mantendo separada a interpretação do sistema;
6. delta antes/depois e seu alvo;
7. evento de contestabilidade — aceitar, emendar, rejeitar, adiar ou retirar;
8. consequência: próximo passo habilitado/corrigido **ou** resíduo tipado;
9. explicação causal alternativa.

Para avaliar especificamente uma recomendação de experimento, o protocolo precisa ainda tornar explícitos, antes da recomendação:

- possibilidade/decisão bloqueada e alternativas vivas;
- incerteza que o experimento pretende discriminar;
- movimentos concorrentes considerados e a razão local para escolher `suggestion`;
- descrição do experimento, resultados possíveis, reversibilidade, custo, autorização e stop rule;
- resultado esperado de cada alternativa e sua consequência decisória;
- carga e riscos previstos;
- sinal posterior de aprendizado, correção, não mudança ou dano, idealmente com follow-up suficiente para detectar retirada ou rejeição tardia.

Os quatro últimos itens são uma **especialização proposta** a partir do admission contract do plano, que exige decisão consumidora, alternativas, baseline, evidência discriminante, tabela `resultado → ação`, falsificador, limites e stop condition (`research/research-plan.md:78-90`). Não são campos já ratificados de produto.

Casos negativos devem permanecer no conjunto: `no delta`, delta contestado, delta confundido e efeito apenas global (`research/foundation-game-framing/lanes/01-auditable-transition.md:115-120`). Rejeição, não mudança, indução danosa, vitória do baseline e ambiguidade preservada são observações válidas, não dados a descartar (`research/foundation-game-framing/lanes/01-auditable-transition.md:107`).

## O que conta como aprendizagem útil

Aceitação ou execução do experimento não basta. O episódio precisa mostrar uma mudança observável e relevante, por exemplo:

- uma alternativa foi eliminada, revisada ou mantida por uma razão observável;
- um próximo passo foi corrigido, habilitado, deliberadamente adiado ou abandonado;
- uma salvaguarda ou stop decision mudou;
- a incerteza foi preservada porque o resultado foi inconclusivo;
- a pessoa corrigiu ou recusou a proposta e essa contestação evitou uma mudança não autorizada.

O aprendizado deve ser distinguido de confiança, fluência, velocidade, coerência narrativa, satisfação, cumprimento ou mera articulação. O corpus proíbe promovê-los silenciosamente a benefício ou autonomia (`research/foundation-game-framing/lanes/03-agency-governance.md:170-189`). Gate B1 requer uma distinção relevante alterada e um próximo passo habilitado/corrigido, com contraste plausível contra baseline simples (`research/research-plan.md:360-370`).

**Collapse-test de utilidade:** se a recomendação apenas aumenta aceitação, confiança, coerência ou movimento, sem alterar uma decisão relevante melhor que o baseline, a alegação de aprendizagem útil colapsa.

## Baselines necessários

Há dois níveis que não devem ser misturados:

### Baseline da representação

Comparar a gramática de transição com **transcrição + decision/change log ordinário**. Medir confiabilidade entre codificadores, detecção de reframe silencioso, recuperação da razão do próximo passo, carga de representação e efeitos relevantes não representados. Casos históricos podem gerar e calibrar a gramática; validação requer conjunto independente/held-out (`research/foundation-game-framing/lanes/01-auditable-transition.md:122-133`).

### Baselines da intervenção

No mesmo estado pré-intervenção, comparar a recomendação de experimento com:

- resposta direta concisa;
- mais uma pergunta ou entrevista fixa;
- informação/recuperação de evidência;
- conversa genérica competente;
- espera, preservação de ambiguidade ou stop quando cabíveis.

Replay, codificação cega, Wizard-of-Oz, comparação manual e mockups não executáveis são os métodos de menor compromisso preferidos antes de prototipar (`research/research-plan.md:385-395`). A lane recomenda ao menos resposta direta, sequência fixa e conversa genérica competente (`research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:141-148`).

**Collapse-test dos baselines:** se uma alternativa simples obtém aprendizado/decisão equivalente ou melhor, com menor carga ou risco, a recomendação especializada é `baseline_sufficient` e deve ser demovida; não pode reivindicar valor incremental (`research/research-plan.md:497-507`).

## Probes discriminantes de baixa vinculação

Em ordem de compromisso crescente:

1. **Codificação retrospectiva cega:** dois ou mais codificadores aplicam, sem conhecer o desfecho desejado, a gramática candidata e o baseline de transcrição + log a episódios delimitados.
2. **Replay contrafactual:** congelar o estado imediatamente anterior à recomendação e pedir a avaliadores ou facilitadores cegos que escolham entre recomendar experimento, perguntar, informar, responder, esperar ou parar, registrando a razão e a previsão.
3. **Wizard-of-Oz/manual pareado:** apresentar variantes do mesmo episódio com movimentos concorrentes, congelando outcomes e guardrails antes da comparação.
4. **Follow-up de contestabilidade:** oferecer rota barata de rejeitar, corrigir ou restaurar o frame anterior e observar se a mudança persiste após a pressão imediata da interação.

Os três primeiros métodos são diretamente previstos pelo plano e pelas lanes. O quarto é uma **inferência operacional mínima** exigida pelas ameaças de compliance, indução e retirada tardia; o corpus diz que aceitação momentânea não prova durabilidade, autonomia, benefício ou causalidade (`research/foundation-game-framing/lanes/01-auditable-transition.md:62-70`).

Resultados primários candidatos:

- concordância sobre fronteira, movimento, distinção e delta;
- proporção de episódios nos quais a recomendação muda corretamente uma decisão/next step ou preserva uma incerteza relevante;
- recuperação da razão do próximo passo;
- correção/recusa e restauração de frame;
- detecção de reframe silencioso;
- carga cognitiva, tempo, abandono e custo de anotação/interação;
- efeitos não representados e sinais posteriores de retirada ou contradição.

Nenhum threshold numérico é suportado pelo corpus; ele precisa ser pré-declarado no protocolo, não escolhido após os resultados.

## Explicações causais alternativas obrigatórias

O campo mínimo já propõe `multiple interventions`, `external event`, `mere articulation`, `compliance` e `unknown` (`research/foundation-game-framing/lanes/01-auditable-transition.md:97-105`). Para esta pergunta, registrar também:

- fadiga ou desejo de encerrar;
- deferência ao sistema/efeito de autoridade;
- demand characteristics e pressão social;
- sugestão/anchoring ou preferência induzida;
- ordem dos movimentos e path dependence;
- informação obtida fora da interação;
- maturação temporal ou trabalho já em andamento;
- seleção retrospectiva de episódios favoráveis;
- atribuição indevida ao movimento mais próximo quando houve bundle;
- narrativa mais coerente sem decisão melhor.

O resíduo causal já tem owner proposto: `WS4`, via experimento discriminante com baseline simples e casos independentes (`research/foundation-game-framing/lanes/03-agency-governance.md:155-168`).

## Carga, agência e segurança

Guardrails mínimos:

- propósito da sugestão visível e permissão distinta de autorização para executar;
- recusa, correção, deferimento, branch, resposta direta e stop sem penalidade;
- reversibilidade e rota de volta ao frame anterior;
- não registrar mais dados do que o necessário para contestabilidade;
- não recomendar quando custo, privacidade, manipulação, dependência ou irreversibilidade superam o valor decisório esperado;
- em contextos médicos, legais, financeiros, de saúde mental ou segurança interpessoal, preservar referral, ajuda qualificada, resposta direta ou ausência de deliberação como alternativas superiores possíveis (`research/foundation-game-framing/lanes/03-agency-governance.md:91-104`).

**Collapse-test de agência:** se uptake sobe enquanto correção/recusa cai, há relato de pressão, ou revisões path-dependent são depois rejeitadas, o resultado é compatível com compliance/indução, não com governança bem-sucedida (`research/foundation-game-framing/lanes/01-auditable-transition.md:124-130`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:118-128`).

**Collapse-test de carga:** se a seleção/explicação/registro custa tanto quanto o benefício decisório, ou se um baseline simples tem resultado equivalente com menor custo/risco, interromper ou demover o mecanismo.

## Tabela mínima `resultado → ação`

Esta tabela é uma proposta derivada do gate do plano; deve ser congelada antes do teste.

| Resultado observado | Classificação | Ação permitida |
|---|---|---|
| A recomendação supera baseline pré-declarado em aprendizado/next-step e respeita guardrails | sinal positivo limitado | avançar para teste independente/held-out; não promover ainda a política |
| Resultado equivalente ao baseline com maior carga/risco | `baseline_sufficient` | demover a recomendação especializada e usar o baseline |
| Uptake/assentimento sem mudança decisória posterior | `no_witness` ou `mere_articulation` | não alegar benefício; revisar ou parar |
| Mais aceitação com menos recusa/correção, pressão ou rejeição tardia | `compliance` / `harmful_induction` | restringir ou abandonar o trigger; preservar contestação |
| Reframe/objetivo muda sem delta visível ou rota de restauração | `silent_reframe` | invalidar o episódio como sucesso e corrigir o protocolo antes de novo teste |
| Vários movimentos/evento externo impedem atribuição | `causal_attribution_unresolved` | resultado inconclusivo; redesenhar comparação, não creditar a recomendação |
| Codificadores não concordam ou campos só são preenchíveis retrospectivamente | `boundary_unreliable` / `circular` | simplificar/redefinir a unidade; não medir timing com ela |
| Outcome indeterminado, mas guardrails intactos | `inconclusive` | preservar incerteza, nomear owner/reopen trigger e escolher evidência seguinte ou stop |
| Guardrail de segurança/privacidade falha | `risk_block` | parar; referral ou decisão humana conforme o contexto |

Gate B4a exige identidade congelada do protocolo, comparação observada, thresholds/guardrails, aplicação da tabela pré-declarada, resultado inconclusivo tipado e proposta explícita de atualização da claim (`research/research-plan.md:397-401`). Só decisão humana posterior pode aceitar, restringir, reframar ou abandonar a claim (`research/research-plan.md:408-416`).

## Resíduo preservado

O corpus ainda não resolve: thresholds, população/contexto, horizonte de follow-up, peso entre benefício e carga, quando uma incerteza está madura para teste, nem quais direitos de agência são universais. Também não demonstra que um ledger contém os campos necessários para observar o gate. Essas lacunas pertencem respectivamente a WS2/WS4, decisão humana de WS5 e investigação separada de observabilidade; não podem ser fechadas por este relatório.

## Esquema mínimo de episódio avaliável

**Owner/status:** candidato de pesquisa pertencente a WS0/WS2/WS3/WS4; a gramática-base é síntese interna com resíduo e a especialização abaixo é **proposta deste scout**, sem autoridade de produto.

```yaml
episode_id: string
boundary: {before_ref: string, after_ref: string}
prior_state:
  declared_intention: string | absent
  system_inference: string | absent
  blocked_possibility_or_decision: string
  live_alternatives: [string]
missing_distinction:
  statement: string
  provenance: prospective | emergent | retrospective
candidate_moves:
  considered: [ask, inform, suggest_experiment, reframe, direct_answer, wait, stop]
  chosen: string
  stated_local_reason: string
experiment_candidate:
  discriminating_uncertainty: string
  possible_results: [{result: string, decision_consequence: string}]
  reversibility: string
  burden_and_risk: string
  permission_required: string
  inconclusive_consequence: string
observed_intervention:
  content_ref: string
  bundled_moves: [string]
signal:
  observable: string
  system_interpretation: string | absent
delta:
  before_after_proposition: string | no_delta
  target: intention | goal | value | constraint | belief | option | commitment | uncertainty
  status: proposed | accepted | amended | contested | deferred | withdrawn | unresolved
contestability:
  authorized_owner: string | unknown
  low_cost_refusal_or_restore_path: string
consequence:
  next_step_or_residue: string
  later_follow_up: string | unavailable
alternatives_and_guardrails:
  baseline_observation: string
  burden: string
  safety_privacy_result: string
causal_alternatives: [string]
coder_confidence: string
```

**Collapse-test:** se os campos de timing só puderem ser preenchidos após conhecer o desfecho, se codificadores não concordarem sobre fronteira/distinção/movimento/delta, ou se transcrição + decision log recuperar as mesmas decisões com menor carga, o esquema não adiciona valor avaliativo e deve ser simplificado ou abandonado.

## Menor protocolo de validação crível

**Owner/status:** desenho de `WS4 — Evaluation, causal attribution, and discriminating experiments`, sob o plano **proposed**; requer adjudicação humana e não autoriza implementação.

1. Separar um conjunto pequeno de episódios históricos em **calibração** e **held-out**. Incluir positivos aparentes, não construção deliberada, pesquisa ainda produtiva, no-delta, recusa, confusão causal e baseline suficiente.
2. Congelar o esquema, as categorias, os thresholds qualitativos/quantitativos, guardrails e a tabela `resultado → ação` antes de ver o held-out.
3. Fazer codificação cega independente com (A) esquema acima e (B) transcrição + decision log. Testar confiabilidade, detecção de reframe silencioso, recuperação da razão do próximo passo, carga e efeitos não representados.
4. Nos episódios em que o estado anterior é recuperável, executar replay/manual Wizard-of-Oz cego com pelo menos quatro opções: recomendar experimento, resposta direta, movimento informacional/interrogativo simples e esperar/parar. Não executar experimentos reais nesta etapa.
5. Comparar decisão/next-step ou incerteza preservada, correção/recusa, restauração de frame, carga, risco e explicações causais. Uptake isolado não é outcome.
6. Aplicar mecanicamente a tabela `resultado → ação`; registrar inconclusivo e owner/reopen trigger quando causalidade ou timing não forem identificáveis.
7. Somente se o held-out mostrar valor incremental e guardrails preservados, propor um próximo teste independente e limitado. Promoção da regra continua sendo decisão humana explícita.

**Collapse-test:** o protocolo falha se usa os mesmos episódios para gerar e validar a regra, se o evaluator conhece a condição desejada, se não compara uma alternativa simples, se muda outcomes após observar os resultados, se aceitação substitui aprendizagem, ou se não admite resultado inconclusivo/negativo. O mecanismo deve ser demovido se a recomendação não superar o baseline a carga e risco aceitáveis, e abandonado/restrito se produzir compliance, reframe silencioso ou dano.


## Source 5 — `scout-ledger-observability.md`

# Scout — observabilidade do ledger para recomendar experimento

## Resposta curta

O ledger atual pode localizar **candidatos para inspeção**, mas não sustenta sozinho uma recomendação de experimento. Ele observa que dispatches de pesquisa foram declarados, quando abriram e fecharam, seu resultado operacional, a pasta de trabalho declarada e, raramente, uma relação parental explícita. Ele não registra o avanço epistemológico, as alegações que sobreviveram, uma decisão ainda aberta, a inexistência de construção nem a prontidão de uma hipótese falsificável.

Portanto, um gatilho responsável precisa de duas etapas:

1. o ledger seleciona uma sequência candidata, com confiança explicitamente limitada;
2. um leitor de artefatos e evidência de construção confirma o estado epistemológico antes de sugerir qualquer experimento.

Collapse-test da conclusão: se houver no schema ou nas APIs correntes um campo tipado e validado que ligue uma sequência de pesquisas a seus resultados epistemológicos, decisão bloqueada e evidência positiva de construção, esta conclusão precisa ser refeita. A inspeção abaixo não encontrou esse campo.

## Escopo e base examinada

Corpus limitado a `cyberalchemy-orchestrator`, sem web e sem mutação de fonte ou ledger. Foram confrontados:

- contrato e mecânica de escrita: `.codex/skills/register-dispatch/SKILL.md`, `.codex/skills/register-dispatch/append-dispatch.cjs`;
- registry vigente: `implementations/contracts/dispatch-type-registry.v1.json`;
- leitor e APIs: `implementations/server/ledger.py`, `implementations/server/main.py`, `implementations/server/control_center/sources.py`;
- convenções de artefato: `.codex/skills/research/SKILL.md`, `.codex/skills/experiment/SKILL.md`, `.codex/skills/domainspec-implement/SKILL.md`;
- ledger real: `telemetry/agents/subagents-dispatch.yaml`, snapshot local lido em 2026-08-18/19 UTC;
- amostra de oito openings: dois dispatches Kahneman–Thaler, quatro tentativas do inventário de problemas irredutíveis e duas etapas de typed-interaction.

No snapshot havia 366 opening rows e 348 close rows: 58 `research`, 11 `code`, 251 `review`, 46 `others` históricos e nenhum `experiment`. Apenas sete openings tinham `parent_dispatch_id`. Esses são fatos do snapshot, não garantias do contrato para outros repositórios ou datas.

## O que é realmente registrado

### Campos brutos

O registry vigente declara schema `0.6.4` e tipos live `research`, `code`, `review` e `experiment` (`implementations/contracts/dispatch-type-registry.v1.json:3`, `:15`, `:25`, `:65`). O appender aceita, em uma opening row:

- identidade e tipo: `dispatch_id`, `schema_version`, `dispatch_type`;
- intenção declarada: `goal`, `context`;
- plano: `max_loops`, `final_approver`, `groups`, `connections` e configuração anti-bias;
- vínculo e destino opcionais: `parent_dispatch_id`, `working_folder`, `output_mode`;
- para `code`, o `code_contract` pré-execução;
- `created` e `invoked_by`, estampados/resolvidos durante o append.

Isso é confirmado pelo conjunto fechado de chaves em `.codex/skills/register-dispatch/append-dispatch.cjs:146-159` e pela serialização efetiva em `:665-684`. `topic_slug` e `session`, que poderiam auxiliar agrupamento, são chaves legadas rejeitadas (`:163-169`).

A close row contém somente `close_of`, `closed`, `invoked_by`, `exit_reason`, `agents_spawned` e, opcionalmente, `feedback_prompts` (`append-dispatch.cjs:499-524`, `:646-654`). Não há campo de resultado epistemológico, artefato entregue, decisão, claim, próxima ação ou diff construído.

### Derivações seguras do leitor

O leitor:

- casa opening e close exclusivamente por igualdade `dispatch_id == close_of`;
- deriva `_state = open|closed`, `_legacy`, `_live` e `_agent_count`;
- mantém orphan closes visíveis;
- deriva o dia por `created`, depois `_close.closed`, depois prefixo do id.

Essas regras estão em `implementations/server/ledger.py:163-221` e `:497-525`. Assim, são computáveis com boa confiança:

- existência de opening/close e estado operacional;
- duração aproximada `closed - created`, quando ambos são timestamps válidos;
- contagens por tipo, dia, papel e topologia declarada;
- parentage apenas quando `parent_dispatch_id` está presente;
- co-localização textual por `working_folder` exato.

Não é seguro converter co-localização, proximidade temporal ou similaridade de `goal/context` em “mesma linha de investigação” sem assumir uma heurística. O próprio Control Center diz que normaliza linhas “without inventing parentage” e só cria uma aresta quando encontra `parent_dispatch_id` (`implementations/server/control_center/sources.py:105-160`).

### O que as APIs expõem

- `/api/dispatch/{repo}/{id}` devolve a linha completa já unida ao close (`implementations/server/main.py:156-171`).
- `/api/snapshot` devolve apenas a janela recente configurada, preservando os campos mas truncando prompts (`main.py:139-153`; `ledger.py:432-463`).
- `/api/repo/{repo}` lista todo o histórico em forma `slim` (`main.py:259-303`). Essa forma inclui tipo, data, pasta, estado e resumo do close, mas omite `context`, `parent_dispatch_id`, `groups`, `connections`, `code_contract`, `output_mode`, `agents_spawned` e `feedback_prompts` (`ledger.py:650-697`).
- o Control Center usa as linhas completas para materializar as poucas arestas parentais explícitas (`control_center/sources.py:139-160`).

Nenhum desses caminhos calcula cluster temático, avanço, decisão pendente, construção ou readiness de experimento.

## O que cada sinal permite afirmar

### Pesquisa repetida e relacionada

“Repetida” é computável por contagem de `dispatch_type: research`. “Relacionada” só é forte com `parent_dispatch_id`; pasta idêntica é evidência de co-localização, não de causalidade. Objetivos semelhantes, ids com `-r2/-r3` e proximidade temporal são classificadores candidatos, não fatos.

A amostra Kahneman–Thaler é o caso forte: a segunda pesquisa declara explicitamente a primeira como parent e reutiliza a pasta (`telemetry/agents/subagents-dispatch.yaml:170-180`). Porém essa relação é excepcional: somente sete de 366 openings no snapshot tinham parent. A sequência typed-interaction é semanticamente clara para um leitor humano — exploração e síntese — mas não contém `parent_dispatch_id` (`subagents-dispatch.yaml:6356-6392`). Um detector ledger-only precisaria inferir o vínculo dos textos, pastas aninhadas e intervalo de dois minutos.

### Avanço epistemológico e claims sobreviventes

Não estão no ledger. `exit_reason: resolved` diz que o dispatch fechou sob a semântica operacional do tipo; não carrega o veredito de pesquisa. O skill de pesquisa inclusive permite fechar `resolved` após um KILL confirmado (`.codex/skills/research/SKILL.md:100`).

O avanço torna-se visível apenas nos artefatos. Em typed-interaction, `findings.md` registra cinco candidatos GO e um KILL (`docs/features/agents-communication-infra/research/interaction-relations/findings.md:268-277`), limita explicitamente o alcance da conclusão (`:354-360`) e preserva hipóteses para gates posteriores (`:380-416`). Nada disso aparece nas rows `resolved` correspondentes (`subagents-dispatch.yaml:6375-6399`).

As convenções ajudam a localizar o conteúdo, mas não o tornam parte do ledger: pesquisa com `n >= 2` deve produzir `research.md` e `findings.md`; com `n = 1`, somente `findings.md` (`.codex/skills/research/SKILL.md:127-137`). Não há digest, manifest ou identidade de artefato na opening/close row de pesquisa.

### Decisões não resolvidas

`_state: open` significa apenas ausência de close; não significa decisão em aberto. `resolved` também não significa que todas as decisões de domínio foram tomadas.

O contraexemplo aparece nos artefatos do inventário de problemas: `findings.md` contém cinco perguntas não resolvidas e exige uma próxima etapa de síntese e ataque cético (`research/repository-irreducible-problem-inventory/stages/exploration/findings.md:45-55`). As quatro rows associadas, entretanto, fecharam como três `error` e um `user_abort` (`subagents-dispatch.yaml:5677-5759`). O ledger não consegue dizer qual tentativa produziu quais bytes, pois todas apontam para a mesma pasta.

### Ausência de construção

O máximo que o ledger pode afirmar é “não encontrei dispatch `code` registrado dentro de um recorte definido”. Isso não equivale a “nada foi construído”.

Mesmo para `code`, o `code_contract` registra readiness e intenção pré-execução — `write_scope` e `validation_commands` — não o diff nem os resultados pós-execução (`append-dispatch.cjs:290-355`). A close row não pode carregar esses resultados. O skill de implementação exige como bundle de sucesso diff, inventário de símbolos, rastreabilidade, comandos/resultados e riscos (`.codex/skills/domainspec-implement/SKILL.md:57-66`), mas o ledger não persiste esse bundle.

Além disso:

- construção manual, inline, em outro repositório ou fora do workflow não gera necessariamente uma row local;
- rows históricas podem obedecer schemas anteriores;
- `working_folder` é obrigatório para pesquisa/experimento, não para `code` (`append-dispatch.cjs:133-137`, `:265-275`);
- a existência de uma pasta não prova que o artefato foi produzido pelo dispatch, está íntegro ou permaneceu imutável.

Na amostra, os dois dispatches Kahneman–Thaler estão `resolved` e apontam para a mesma pasta (`subagents-dispatch.yaml:124-153`, `:170-187`), mas essa pasta não existe hoje no repositório. No sentido oposto, a pasta das quatro tentativas `error/user_abort` contém hoje `research.md` e `findings.md`. Portanto, `resolved`, `working_folder` e existência de arquivo falham separadamente como provas de resultado.

### Readiness para experimento

Não há sinal direto. O tipo `experiment` é live no registry, mas a própria semântica vigente é de **proposta/pré-registro**, não de execução: seu resultado é um `criterion.md` congelado; o run posterior produz `experiment.md` e `findings.md` (`.codex/skills/experiment/SKILL.md:134-159`, `:185-193`). Um `experiment` fechado como `resolved` significaria “critério pronto para rodar”, não “hipótese validada”.

Para recomendar a criação dessa proposta, seria necessário obter fora do ledger pelo menos:

- claim ou decisão específica que precisa ser discriminada;
- hipótese única e observação falsificadora candidata;
- evidência de que pesquisa adicional tem retorno menor que um probe;
- dono da decisão e ação que cada resultado desbloqueia;
- verificação positiva do que já foi construído, em vez de inferência por ausência.

O snapshot local tinha zero rows `experiment`, portanto este ledger também não oferece episódios históricos positivos para calibrar o momento da transição.

## Implicação para um recomendador

O desenho defensável com os dados atuais é um **gerador de candidatos**, não um decisor:

1. selecionar clusters por parent explícito; aceitar pasta exata + texto/tempo somente como hipótese de cluster;
2. abrir e validar os artefatos canônicos, preservando autoria, versão e ambiguidade de pasta compartilhada;
3. extrair apenas claims/vereditos/questões/próxima etapa explicitamente escritos;
4. procurar evidência positiva de construção ou de um dispatch posterior relacionado; nunca provar ausência por contagem zero;
5. só então oferecer ao usuário uma sugestão contestável, incluindo por que agora, qual decisão ela desbloqueia e qual fato suprimiria a sugestão.

Suprimir a recomendação quando faltar artefato, houver apenas repetição operacional, a última etapa pedir mais síntese/review, a pasta for compartilhada entre tentativas não atribuíveis, já existir construção/experimento relacionado ou não houver hipótese falsificável e dono da decisão.

## Matriz final

| signal | source | computable now? | confidence | missing evidence | collapse-test |
|---|---|---:|---|---|---|
| Quantidade de pesquisas em um recorte | `dispatch_type`, `created` | Sim | Alta | Definição do recorte temático | Uma row classificada incorretamente ou fora da janela altera a contagem relevante. |
| Relação explícita entre pesquisas | `parent_dispatch_id` | Sim | Alta quando presente | Cobertura é muito baixa; ausência não significa independência | Encontrar parent ausente no ledger mas vínculo obrigatório em outro contrato invalida tratá-lo como fonte única. |
| Co-localização de pesquisas | `working_folder` exato | Sim | Média-baixa | Identidade de objetivo e autoria dos arquivos | Dois objetivos independentes na mesma pasta colapsam o sinal. |
| Relação por texto/tempo/id | `goal`, `context`, `dispatch_id`, timestamps | Sim, heuristicamente | Baixa | Subject/thread id governado | Um par lexicalmente parecido mas causalmente independente colapsa o cluster. |
| Estado operacional | opening + close unidos por id | Sim | Alta | Semântica epistemológica do fechamento | Um `resolved` com KILL ou sem artefato colapsa “closed = advanced”. |
| Cadência/duração | `created`, `_close.closed` | Sim | Alta para tempo; baixa para significado | Causa da repetição e tempo real de trabalho | Retries de infraestrutura rápidos colapsam “cadência = progresso”. |
| Artefatos esperados de pesquisa | `working_folder` + convenção `research.md`/`findings.md` | Parcial | Média | Manifest, digest, autoria por dispatch, imutabilidade | Pasta ausente após `resolved`, ou pasta compartilhada após erros, colapsa atribuição. |
| Avanço epistemológico | Conteúdo citado de `findings.md` | Não pelo ledger; sim por inspeção | Média-alta quando explícito e versionado | Vínculo durável row→artefato e aceitação do approver | Um arquivo posterior, sobrescrito ou não atribuível colapsa a conclusão. |
| Claims sobreviventes | Matriz GO/KILL e collapse-tests no artefato | Não pelo ledger; sim por inspeção | Alta somente para o que está escrito | Estado tipado por claim e versão | Ausência de verdict explícito ou claim mais forte que a citação colapsa o sinal. |
| Decisão não resolvida | Questões/next stage no artefato | Não pelo ledger | Média | Decision id, owner, opções, status e autoridade | “Open question” sem decisão bloqueada colapsa readiness. |
| Construção registrada | Presença de row `code`; `code_contract` em schema atual | Sim | Alta para intenção registrada, não para resultado | Diff, resultados, commit/artefato e vínculo temático | `code` sem bundle aceito colapsa “row = construção”. |
| Ausência de construção | Ausência de row `code` | Não | Muito baixa | Evidência positiva sobre workspace, commits, outros repos e trabalho inline/manual | Qualquer artefato construído fora de dispatch colapsa imediatamente. |
| Critério de experimento já proposto | `experiment` + `working_folder/criterion.md` | Parcial | Média | Digest/freeze e validade atribuível | Criterion ausente, mutado ou não atribuível colapsa pré-registro. |
| Readiness para recomendar experimento | Nenhuma fonte ledger suficiente | Não | Indisponível | Claim, decisão, falsifier, custo, ação pós-resultado, dono e alternativa | Se qualquer resultado não mudar uma decisão, a recomendação não está pronta. |

## Conclusão

O momento correto não é observável como um único estado do ledger. O ledger pode dizer “há uma sequência que merece exame”; os artefatos precisam dizer “o que sobreviveu e o que continua bloqueado”; evidência de workspace precisa dizer “o que já foi construído”. Só a conjunção pode sustentar “talvez seja hora de propor um experimento”, e ainda como recomendação reversível ao dono da decisão, nunca como promoção automática.


## Source 6 — `scout-ledger-counterexamples.md`

# Scout — contraexemplos no ledger para recomendação de experimento

## Resposta curta

O ledger pode localizar **candidatos para inspeção**, mas não sustenta sozinho a conclusão
“pesquisou, avançou e não construiu”. No corpus observado, contagem de pesquisas, `resolved`,
`parent_dispatch_id`, pasta compartilhada e ausência de `code`/`experiment` falham como gatilhos
isolados. O uso seguro é uma conjunção em duas etapas:

1. o ledger recupera uma sequência possivelmente relacionada;
2. findings e artefatos ligados demonstram que existe uma incerteza empírica decidível, um próximo
   gate experimental explícito e nenhuma construção ou preparação equivalente já em andamento.

A segunda etapa não é opcional. A maior evidência contrária é Assay: quatro pesquisas `resolved` e
nenhum dispatch `code`/`experiment` relacionado no ledger, mas um primeiro build funcional existe e
está versionado. O caso Schema Service acrescenta outra distinção: um pacote de experimento pode já
estar em preparação sem que exista uma linha `experiment`.

## Escopo e método

- Corpus: somente `C:/Users/victo/cyberalchemy-orchestrator`; sem web e sem leitura dos repositórios
  externos apontados por algumas linhas.
- Ledger: `telemetry/agents/subagents-dispatch.yaml`, lido e unido pelo leitor local
  `implementations/server/ledger.py` (`parse_ledger` + `join_rows`), sem mutação.
- Artefatos: somente famílias ligadas por identificador, objetivo ou `working_folder`: Assay,
  Schema Service, interaction-relations, runtime-v2, irreducible-problems, transferências SWI e
  local-global-continuous-discrete.
- Construção: presença atual de arquivos e, quando possível, histórico Git do caminho. Presença
  sem commit demonstra estado atual, mas não autoria nem momento de criação.

O snapshot observado contém 714 linhas brutas, unidas em 368 dispatches. Destes, 58 são
`research`: 46 `resolved`, 6 `error`, 5 abertos e 1 `user_abort`. Há 11 dispatches `code` e **zero
dispatches `experiment`**. Apenas 7/368 dispatches têm `parent_dispatch_id`; entre pesquisas, apenas
1/58. Oito pesquisas apontam para `working_folder` iniciado por `..`, portanto para construção fora
do corpus local.

Essas contagens descrevem este snapshot, não uma propriedade eterna do sistema.

## Casos delimitados

### C1 — Assay: falso positivo comprovado para “sem `code` = não construiu”

O ledger registra quatro pesquisas relacionadas em 2026-07-23 — `assay-readme-framings`,
`assay-first-approach-probe`, `assay-forward-research` e `assay-discovery` — todas fechadas como
`resolved` (`telemetry/agents/subagents-dispatch.yaml:884-1006`). A busca por `assay` e
`document-information-estimator` no ledger não encontrou dispatch `code` ou `experiment`.

Porém, `internal-tools/document-information-estimator/s0/assay_s0.py` existe, e o README o declara
“First functional build of Assay”, com execução e acceptance test concretos
(`internal-tools/document-information-estimator/s0/README.md:1-38`). O commit
`51008dfc8d5d10dd9cc88aa72016d6c80fedb005`, de 2026-07-24, adicionou o script, seus documentos e os
artefatos de pesquisa. Logo, a ausência de `code` no ledger não demonstra ausência de build.

Ao mesmo tempo, este caso sustenta uma pista semântica melhor: os findings disseram `GO`,
`build-from-owned` e “S0 can ship ... today”, mantendo obrigações empíricas para rungs posteriores
(`internal-tools/document-information-estimator/discovery/research/forward-research/findings.md:9-47`).
Foi o conteúdo do resultado — não o `resolved` — que tornou a construção seguinte defensável.

### C2 — Schema Service: pesquisa avançou e um experimento já está sendo preparado

O ledger contém três pesquisas `resolved` da mesma iniciativa: prior-art, precedentes de famílias de
artefatos e regra de staging experimental
(`telemetry/agents/subagents-dispatch.yaml:6343-6461`). Não há linha `experiment` no ledger.

Os findings dão um próximo movimento empírico preciso: construir dois pacotes de conformidade,
executando primeiro o documental, e proíbem um runtime universal antes das provas
(`projects/schema-service/research/concrete-artifact-family-precedents/findings.md:23-27,115-123`).
Isso é evidência a favor de **oferecer** um experimento.

Mas o estado atual já contém `projects/schema-service/experimentation-plans/artifact-types-v0/`.
O primeiro pacote tem `status: preparing`, manifesto e candidate types; ainda não tem critério,
fixtures, run ou veredito, e nomeia como próxima ação um dispatch `experiment`
(`projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/README.md:1-32`).
Esses arquivos estão atualmente não rastreados pelo Git. Portanto:

- “nenhum `experiment` no ledger” não significa “ninguém começou a preparar o experimento”;
- presença de uma pasta `experiments/` também não significa que o experimento rodou;
- uma recomendação útil teria de reconhecer a preparação existente e sugerir o gate exato ainda
  ausente (`criterion.md`), não repetir genericamente “faça um experimento”.

### C3 — interaction-relations: duas pesquisas resolvidas, mas ainda é uma base candidata

Exploração e síntese aparecem como dois dispatches `research` `resolved`
(`telemetry/agents/subagents-dispatch.yaml:6356-6395`). Os findings têm `status: draft`, dizem
explicitamente que não autorizam implementação e listam áreas ainda não resolvidas
(`docs/features/agents-communication-infra/research/interaction-relations/findings.md:351-372`).
Eles também materializam hipóteses P/N/D para os próximos gates
(`docs/features/agents-communication-infra/research/interaction-relations/findings.md:380-410`).

Este é um candidato plausível para desenho de validação, mas somente porque as hipóteses e os
collapse-tests são explícitos. A mesma sequência numérica sem esses artefatos não sustentaria a
recomendação. O status `draft` e a frase de não autorização devem impedir que `resolved` seja lido
como “pronto para implementar”.

### C4 — runtime-v2: repetição causada por retry; o próximo gate é review, não experimento

Há dois dispatches de pesquisa com o mesmo objetivo e pasta: o primeiro fechou `error` sem agentes;
o retry fechou `resolved` com três agentes (`telemetry/agents/subagents-dispatch.yaml:5288-5317`).
Contar “duas pesquisas” inflaria artificialmente o avanço.

Os findings separam capacidades já implantadas, lacunas e itens `KILL`/`BLOCK`; para o
skill-to-DAG compiler, registram `BLOCK — proposal-only`. A ação prescrita é passar os artefatos pelo
gate canônico de `review` antes de uma discovery de arquitetura
(`docs/features/agents-communication-infra/research/runtime-v2-migration-inventory/findings.md:52-67,91-98`).
Um recomendador baseado só em repetição + `resolved` sugeriria o tipo errado de próximo passo.

### C5 — irreducible-problems: quatro pesquisas não significam quatro avanços

Quatro dispatches compartilham objetivo e pasta: três fecharam `error`; o quarto, `user_abort`
(`telemetry/agents/subagents-dispatch.yaml:5677-5755`). O close do quarto explica que os três scouts
terminaram, mas `close-session` ocorreu antes de persistir/sintetizar tudo. Os artefatos hoje existem,
porém seus findings permanecem `status: exploratory`, não encontraram um único problema fundamental
defensável e exigem síntese e skeptics como próximo estágio
(`research/repository-irreducible-problem-inventory/stages/exploration/findings.md:1-22,45-55`).

Este caso refuta três inferências: número de tentativas não mede avanço; `user_abort` não prova
fracasso epistemológico; e artefato recuperado depois não transforma retroativamente o close em
`resolved`. Também é o único sinal semelhante a uma decisão humana de interrupção encontrado neste
recorte, mas ele registra encerramento da sessão, não recusa de uma sugestão de experimento.

### C6 — transferências SWI: ausência local de construção é desconhecida

Cinco pesquisas `resolved` de transferência apontam para cinco pastas sob
`../subagent-work-infrastructure/` (`telemetry/agents/subagents-dispatch.yaml:5790-5875`). Dentro da
fronteira autorizada não é possível verificar seus outputs nem eventual construção no repositório
alvo. Logo, “não encontrei build neste repo” significa **não observável**, não “não construiu”. Todo
`working_folder` externo deve suspender esse componente do gatilho ou exigir evidência do repo-alvo.

### C7 — local-global: falso negativo para limiar de “várias pesquisas”

Há apenas um dispatch de pesquisa `resolved`
(`telemetry/agents/subagents-dispatch.yaml:6230-6242`), mas os findings nomeiam diretamente o
primeiro experimento prático e seu efeito mensurável
(`research/local-global-continuous-discrete/findings.md:41-55`). Um limiar de duas ou três pesquisas
não o sinalizaria, embora o conteúdo tenha mais prontidão experimental que vários casos repetidos.

### C8 — verdicts mistos não podem virar um único escore de “avanço”

Os findings de precedentes do Schema Service matam quatro alegações de witness completo (`KILL`) e
mantêm uma mecânica como `GO condicionado`
(`projects/schema-service/research/concrete-artifact-family-precedents/findings.md:29-39`). Os
findings de runtime-v2 combinam `GO`, `KILL` e `BLOCK` no mesmo documento. “Findings existe” ou
“contém GO” é insuficiente: o recomendador precisa vincular o experimento a um candidato/veredito
específico, preservando condições e negativos tipados.

## Observabilidade de sugestões recusadas

O ledger não possui, no snapshot examinado, um campo estruturado para `suggestion_offered`,
`accepted`, `declined`, razão da recusa ou snooze. `feedback_prompts` mistura correções de reviewers,
diagnósticos de runtime e decisões do approver; não é um log confiável de resposta do usuário.
Consequentemente, “não repetir uma sugestão já recusada” não é calculável pelo ledger atual. A
ausência de registro não deve ser interpretada como ausência de recusa.

## Tabela orientada a confusão

| proxy | supporting cases | countercases | safe use | unsafe inference |
|---|---|---|---|---|
| `>= 2` pesquisas | Assay; interaction-relations; Schema Service | runtime-v2 e irreducible contam retries/falhas; local-global tem uma pesquisa e experimento explícito | Recuperar famílias candidatas depois de deduplicar retries e provar coerência temática | “Quantidade = avanço” ou “uma pesquisa nunca basta” |
| mesmo `working_folder` | runtime-v2 e irreducible identificam famílias reais | Assay usa caminhos históricos divergentes; Schema Service usa subpastas; SWI aponta para fora do repo | Evidência corroborativa, normalizada e combinada com objetivo/artefatos | Usar igualdade exata como identidade ou tratar caminho externo como inspecionado |
| `parent_dispatch_id` | gapclose de Kahneman e poucos follow-ons têm lineage explícita | só 1/58 pesquisas e 7/368 dispatches têm o campo; Assay e Schema Service não o usam | Sinal forte quando presente | Ausência = trabalhos não relacionados; requisito obrigatório de agrupamento |
| close `resolved` | Assay e Schema Service produziram resultados utilizáveis | runtime-v2 `resolved` pede review; interaction-relations continua draft; o label não contém avanço semântico | Confirmar término operacional antes de ler o resultado | “A hipótese avançou”, “está pronto” ou “o próximo passo é experimento” |
| ausência de `code` | Pode indicar que nenhum build governado foi registrado | Assay tem build funcional versionado sem linha `code`; construção manual pode existir | Pergunta para busca de artefatos e histórico | “Não construiu” |
| ausência de `experiment` | Nenhum caso no snapshot possui linha desse tipo | O ledger inteiro tem zero linhas `experiment`; Schema Service já prepara pacote experimental | Detectar somente que nenhuma execução desse tipo foi registrada neste ledger | Usar como variável discriminante ou negar preparação/run externo |
| findings presentes | Todos os casos aprofundados têm decisão mais rica que o close | irreducible é exploratório; interaction-relations é draft; runtime-v2 manda review | Abrir o artefato e extrair standing, candidato, condição e próximo gate | “Findings = conclusão favorável” |
| `GO` / `build-from-owned` | Assay e parte do Schema Service dão direção acionável | Documentos misturam `GO`, `KILL`, `BLOCK` e condições | Vincular ao candidato exato e carregar suas condições | Colapsar o documento num único sentimento positivo |
| próximo experimento explícito | local-global nomeia probe mensurável; Schema Service nomeia pacote e gate | runtime-v2 exige review; irreducible exige síntese/skeptic | Melhor sinal disponível, desde que haja decisão, falsificador e owner | Inferir experimento apenas de linguagem como “next” ou “build” |
| presença de artefato | Assay prova build; pacote Schema prova preparação | Uma pasta `experiments/` pode estar apenas `preparing`; findings não são implementação | Classificar artefato por conteúdo/status e, se necessário, Git | Contagem de arquivos = construção concluída |
| tempo desde a pesquisa | Pode ajudar a ordenar inspeção | open work, trabalho deliberadamente fundacional e cross-repo tornam idade ambígua | Critério de prioridade depois dos gates semânticos | “Ficou velho = está parado” |

## Limite seguro sugerido por estes casos

Uma recomendação automática só deveria ser **elegível para oferta**, não disparada como conclusão,
quando todas as condições abaixo forem demonstradas:

1. uma família coerente foi reconstruída por evidência positiva — lineage explícita ou combinação de
   objetivo, artefatos e pasta — com retries colapsados;
2. não há pesquisa aberta, erro ainda não recuperado, `user_abort` pendente ou gate anterior exigido;
3. findings identificam um candidato específico com standing favorável/condicionado e uma incerteza
   que só evidência empírica resolve;
4. existe uma hipótese ou critério falsificável, decisão que o resultado muda e próximo gate
   experimental explícito ou reconstruível sem inventar autoridade;
5. uma busca nos artefatos e no histórico não encontra build, run ou pacote equivalente já ativo; e
6. o escopo de construção é observável — ou a recomendação declara honestamente que o repo externo
   não foi verificado.

Mesmo essa conjunção não permite inferir “a pessoa não construiu”; permite apenas dizer: “há uma
incerteza empírica madura e não encontrei, no escopo observado, uma validação equivalente; quer que
eu proponha o menor experimento?”. Para suportar abstinência após recusa, o ledger precisaria de um
evento estruturado separado para oferta, resposta, razão e validade temporal da decisão.

