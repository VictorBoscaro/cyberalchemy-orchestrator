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
