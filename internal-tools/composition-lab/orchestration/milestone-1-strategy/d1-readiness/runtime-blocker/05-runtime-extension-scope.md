# Escopo da extensão de runtime para `sequential` e `feedback`

Data: 2026-08-13  
Rota: avaliação técnica read-only; nenhuma implementação  
Base de evidência: diagnósticos D1a, compilador/hook/runtime/testes atuais e specs/design do handoff terminal

## Recomendação

**DEFER para o Milestone 1 de composição de lentes.** Implementar suporte honesto ao record atual de
D1a não é um reparo local: é um programa próprio de runtime. O menor incremento já especificado e
implementável cobre somente um produtor, um consumidor e um slot (`L0/L1`); D1a exige fan-in de
quatro extractors e um loop de feedback limitado. Atravessar essa distância agora misturaria dois
objetivos load-bearing — estudar composição e estabelecer autoridade de execução — e tornaria o
milestone de pesquisa dependente de uma migração de runtime ainda sem testes executáveis.

**Critério explícito para GO:** promover a extensão somente quando o owner decidir que evidência de
handoff intradispatch é requisito do experimento, aceitar um milestone de runtime separado e congelar
um contrato executável que inclua: (a) output terminal host-observed; (b) mapping source→slot
confirmado; (c) fan-in/cardinalidade; (d) lifecycle de feedback, supersessão e `loop_cap`; (e) corte
de autoridade legacy/runtime; e (f) testes de aceitação e rollback/fence. Sem os itens (c)-(e), há GO
possível apenas para um piloto sequencial 1→1, não para D1a.

## Posição atual suportada

- `compile_bound_launch_plan` rejeita qualquer `connections` não vazio antes de escrever o plano
  (`implementations/server/runtime/dispatch_workflow.py:120-126`).
- Quando não há conexões, todos os assentos são emitidos como turn-zero com `slots: []`
  (`dispatch_workflow.py:127-204`). Ordem no array não cria readiness ou entrega.
- O runtime valida manifests já escritos e aceita a fonte legada `binding-output` quando o binding
  produtor está apenas terminal (`service.py:5286-5425`); ele não captura nem aceita o output do
  produtor e não deriva manifests de uma conexão.
- O hook fecha o binding com estado/agent id, mas descarta os bytes de `tool_response` como evidência
  de output (`host_dispatch_hook.py:578-667`; `service.py:5736-5825`).
- A arquitetura aceita para terminal-output handoff é explícita, mas declara seus witnesses
  TOH-001–008 como planejados, não executados. O layering seed separa L0 evidência, L1 handoff 1→1,
  L2 fan-in e L3 rollout.
- A própria spec classifica o handoff como “specified for 1 producer → 1 required slot; not
  implemented” (`specs/SPEC.md:127`). Feedback não possui um equivalente implementável completo.

Consequência: remover a guarda ou ordenar launches produziria falsa execução conectada; aproveitar
o `binding-output` atual perpetuaria atribuição por path e terminalidade, expressamente rejeitada
pelas regras novas.

## Escopo real por camada

### R0 — decisão, fronteira e contrato executável

Objetivo: impedir que código invente semântica ausente.

- decidir se a extensão vive no adaptador `legacy-managed` ou inaugura o caminho
  `runtime-managed`;
- transformar `connections` em identidades estáveis e separar aresta de ordem de mapping de dados;
- definir slot schema, cardinalidade, política de visibilidade, sucesso/falha e ownership;
- resolver IDs de attempt/binding globalmente seguros (o attempt atual omite `dispatch_id`);
- definir para feedback: trigger, destinatário, produtor da crítica, nova tentativa/turno,
  supersessão, preservação de versões, o que `loop_cap` conta e condição de saída.

Arquivos prováveis: registry/contratos de dispatch, schemas/specs e fixtures; não deve começar por
`dispatch_workflow.py`. Invariante principal: a confirmação congela toda autoridade que poderá
causar entrega ou reexecução.

### R1 — evidência durável de output terminal (L0)

Objetivo: tornar um resultado de agente uma fonte atribuível sem confiar em path/prosa.

- hook captura os bytes exatos observados no terminal;
- artifact store finaliza conteúdo antes da aceitação SQL;
- migration adiciona terminal-response evidence/receipt e uniqueness por producer turn;
- runtime separa `completed+bytes` de `failed|cancelled|unknown`;
- eventos, validators, query/projection e receipts ficam replay/idempotency-safe.

Arquivos centrais estimados: nova migration; `host_dispatch_hook.py`; `service.py`; provavelmente
`artifacts.py`, `journal.py`, `projections.py` e `api.py`; 2–3 módulos de testes. **Estimativa:**
7–10 arquivos de produção/contrato e 3–5 arquivos de teste/fixture. A spec fornece TOH-001–005 como
base, mas não há cobertura executável correspondente.

Invariantes: bytes são host-observed; um receipt por turno; retry idêntico retorna o mesmo receipt;
drift conflita; completed e receipt commitam juntos; arquivo órfão ou state terminal não autoriza
consumo.

### R2 — handoff sequencial 1→1 (L1)

Objetivo: materializar e autorizar exatamente um consumidor a partir de exatamente um produtor.

- persistir `SourceToSlotMapping` confirmado, mapping version e policy ref;
- materializador cria manifest canônico e binding candidate;
- scheduler/launch intent verifica prerequisite heads em CAS;
- bridge/hook recebe apenas launch autorizado e preserva envelope existente;
- compiler relaxa a fence somente para a topologia comprovada;
- recovery repete fatos aceitos sem duplicar launch.

Arquivos centrais estimados: nova migration; novo módulo de materialização/scheduling (preferível a
inflar `service.py`); `service.py`; `dispatch_workflow.py`; `host_dispatch_hook.py`; possivelmente
`operator_recovery.py`, `api.py`/`cli.py`, projections; testes de compiler, binding, hook e restart.
**Incremento sobre R1:** 8–12 arquivos de produção/contrato e 4–6 arquivos de teste/fixture.

Invariantes: conexão sem mapping não entrega bytes; consumidor não aparece como launchable antes do
manifest completo; same-dispatch e source/target exatos; um manifest entry e um launch intent;
cancel/supersede vencem corrida; nenhuma edição manual de envelope.

### R3 — fan-in e DAG sequencial útil para D1a (L2)

Objetivo: suportar quatro extractors → writer e cadeias posteriores.

- validação de DAG/ciclos, ready sets e ordenação canônica;
- mappings 1:N/N:1, cardinalidade total, ordenação de slots e limites de bytes;
- política para predecessor failed/cancelled/unknown e partial fan-in;
- scheduling em ondas e close que não confunde assento ainda não liberado com ausente;
- dedupe/recovery por edge, mapping, manifest e launch.

Arquivos centrais estimados: compiler/graph validator, scheduler/materializer, migrations, service,
bridge/hook, recovery/projections e pelo menos quatro suites. **Incremento sobre R1/R2:** 6–10
arquivos de produção/contrato e 4–7 arquivos de teste/fixture.

Invariantes: todo required predecessor tem receipt verificado; ordem canônica é independente da
ordem de conclusão; nenhuma falha parcial libera o consumidor; restart produz os mesmos IDs,
digests e quantidade de launches.

### R4 — feedback limitado e rework

Objetivo: tornar `writer → coverage` com correção limitada uma máquina observável, não um rótulo.

Isso requer primeiro corrigir uma ambiguidade do record: uma aresta `writer -> coverage` tipada
`feedback` não diz se coverage recebe o draft, se seu retorno volta ao writer, nem qual artefato
depois segue ao approver. A implementação precisa modelar pelo menos:

- avaliação e prompt de feedback como output versionado;
- aresta/relação de retorno ao producer original;
- novo turn/attempt autorizado e identidade do agente alvo;
- artifact lineage e supersessão sem apagar draft, crítica ou revisão;
- contagem atômica de loops, stop condition e exhausted disposition;
- re-audit do output revisado e regra de qual versão pode liberar o approver;
- cancel, failure, duplicate feedback e restart em cada fronteira.

Arquivos prováveis: schema/validator de conexão, state machine/events, migrations, scheduler,
materializer, service, hook/followup bridge, projections/telemetry, recovery e suites específicas.
**Incremento sobre R1–R3:** 8–14 arquivos de produção/contrato e 5–8 arquivos de teste/fixture.

Invariantes: cada loop tem causa e prompt verbatim; `loop_cap` não pode ser excedido sob retry ou
corrida; follow-up só alcança o agent/binding autorizado; versões antigas permanecem evidência mas
não liberam downstream; approval só consome a versão vencedora explicitamente aceita.

### Ordem de grandeza total

Há sobreposição entre as listas; não se devem somar mecanicamente. Para `sequential` 1→1 honesto,
espere mudanças coordenadas em aproximadamente **12–18 arquivos** e uma nova migration, com quatro
fronteiras de teste. Para o **DAG com fan-in + feedback** exigido por D1a, a superfície sobe para
aproximadamente **20–30 arquivos** entre runtime, contracts/specs, migrations, recovery,
projections e testes, provavelmente em 3–4 increments revisáveis. A incerteza é alta até R0 fechar
authority mode e semântica de feedback; qualquer estimativa em linhas/dias seria falsa precisão.

## Matriz mínima de testes

| Área | Positivos obrigatórios | Negativos/races obrigatórios |
|---|---|---|
| Output terminal | resposta exata cria artifact+receipt; retry igual é estável | path arbitrário; bytes divergentes; completed sem receipt; failed/cancelled como source |
| Mapping/materialização | mapping confirmado gera manifest/digest estável | conexão sem mapping; cross-dispatch; source/target/slot/policy drift; slot faltante |
| Launch | exatamente um intent e um launch após heads válidos | launch precoce; duplicate; cancel/supersede race; stale head |
| Recovery | crash/restart em cada commit converge | arquivo órfão, receipt órfão, manifest parcial e ack perdido não liberam trabalho |
| Fan-in | N receipts em ordem canônica liberam uma vez | parcial, duplicate producer, completion order variável, predecessor failed |
| Feedback | revisão dentro do cap e versão final explicitamente escolhida | cap excedido, loop duplicado, prompt não confirmado, target errado, stale revision, approval do draft antigo |
| Compatibilidade | `connections: []` preserva comportamento atual; fence fica nos tipos não suportados | `zig-zag` e formas fora do slice rejeitam sem writes |

Além de unit/integration, é necessária uma prova end-to-end usando o hook real: producer termina,
runtime captura bytes, materializa consumer, emite um único launch, reinicia no meio e converge. A
review independente é **Required**, pois muda schema, autoridade de launch, provenance e recovery.

## Comparação com split em dispatches sem `connections`

| Critério | Extensão intradispatch | Split connectionless stageado |
|---|---|---|
| Preserva o record D1a atual | sim, somente após R1–R4 | não; requer novo sheet e nova confirmação |
| Custo de runtime imediato | alto | nenhum para execução básica; baixo/moderado se exigir manifests exatos |
| Ordem de execução | runtime/scheduler observável | parent espera cada close e abre o próximo dispatch |
| Handoff de bytes | producer receipt → mapping → manifest | arquivo de repo citado/lido no estágio seguinte; sem vínculo runtime produtor→consumidor |
| Fan-in | first-class após R3 | writer lê artefatos congelados de vários dispatches |
| Feedback | first-class após R4 | novo dispatch explícito de crítica/revisão por rodada |
| Evidência causal de composição | potencialmente forte | fraca: prova arquivos e sequência, não effective input nem consumo |
| Recovery/idempotência | governada pelo runtime | governada pelo orchestrator/records; mais gates e mais chances de drift |
| Adequação ao Milestone 1 | bloqueia a pesquisa até infraestrutura pronta | permite avançar se a claim for reduzida explicitamente |

O split é **honesto somente sob uma claim menor**: “dispatch B foi aberto depois que os artefatos de
A existiam e foi instruído a lê-los”. Ele não prova que bytes específicos foram materializados como
input efetivo, que foram lidos, nem que um loop `feedback` ocorreu dentro de um dispatch. Para usá-lo:

1. substituir o record atual por uma sequência nova, sem fingir equivalência;
2. fechar e congelar cada estágio antes de preparar o seguinte;
3. registrar paths, hashes e producer dispatch IDs no próximo sheet/artefato;
4. representar cada correção como novo dispatch, com cap controlado pelo orchestrator;
5. demover claims de “governed handoff/effective input” para “staged repository handoff”;
6. preservar returns e artifacts verbatim para que a pesquisa ainda possa auditar perdas.

Se o milestone exigir input binding exato, até o split precisa de uma extensão menor que compile
manifests `repository` não vazios e os inclua no envelope confirmado. Isso é bem menor que R1–R4,
mas não existe hoje e deve ser tratado como seu próprio slice, não como edição manual do JSON.

## Milestone próprio recomendado

### RT-H1 — Sequential host-output handoff demonstrado

**Objetivo:** provar uma única aresta sequencial 1 produtor → 1 consumidor com output terminal
host-observed, materialização confirmada e launch exatamente uma vez.

**Inclui:** R0 limitado + R1 + R2; migration; TOH-001–008 executáveis; restart test; dark capture;
piloto 1→1; review adversarial de authority/security/recovery.

**Não inclui:** D1a, fan-in, feedback, zig-zag, general DAG ou migração total para runtime-managed.

**Gate de conclusão:** todos os witnesses passam pelo hook real; nenhuma fonte path-based satisfaz
o slot; restart não duplica; fence continua em qualquer topologia fora do slice; review não deixa
CRITICAL/MAJOR.

Depois, dois milestones opcionais e dependentes:

- **RT-H2 — Bounded sequential DAG/fan-in:** R3, necessário aos quatro extractors de D1a.
- **RT-H3 — Feedback/rework lifecycle:** R4, necessário ao record D1a atual; só abre após definição
  humana da semântica e fixtures de colapso/limite.

## Decisão para D1a

Não alterar nem lançar o record atual. Para avançar o Milestone 1 agora, escolher um novo programa
de dispatches connectionless stageados e aceitar sua evidência mais fraca, ou reduzir D1a a uma
unidade independente que não reivindique synthesis/handoff governado. Abrir RT-H1 agora só é
justificado se o usuário priorizar tornar a própria composição operacionalmente observável antes
de estudar o corpus; ainda assim, D1a continuaria bloqueado até RT-H2 e RT-H3.

## Limite da avaliação

Esta estimativa deriva de contratos e código atuais; não executou testes nem validou o formato real
dos `tool_response` de todos os hosts. A maior incerteza não é técnica, mas de decisão: authority
mode e semântica precisa de feedback permanecem abertas. Elas podem mudar significativamente a
lista de arquivos, mas não eliminam R1–R4 nem permitem um patch seguro na guarda atual.
