---
artifact_kind: internal-small-batch-execution-plan
status: ready-first-batch
date: 2026-08-13
semantic_mode: bounded-source-read-only-scouts
registered_capability: none
supersedes: monolithic-35-source-280-obligation-exact-run-route
---

# Plano em pequenos lotes — pesquisa interna sobre composição

## Objetivo servido

Produzir observações rastreáveis sobre como partes, relações, transformações, resultados e perdas
aparecem no ecossistema interno, sem decidir antecipadamente que um caso é composição e sem fazer
da composição de lentes o modelo geral. O resultado alimentará, depois, uma pesquisa comparativa e
o documento progressivo do Composition Lab.

## Decisão de execução

Substituir o pacote monolítico de 35 fontes e 280 obrigações por uma série de coletas pequenas,
congeladas e independentes. Cada lote tem seu próprio denominador, prompt, retorno preservado e
auditoria. Não existe conexão ou handoff declarado entre assentos. Um agente posterior só pode ler
retornos já terminados e congelados, em um novo dispatch.

O mecanismo é uma **tarefa de subagente nativa, bounded e source-read-only, com um único output
allowlisted**, não a capability registrada
`research` e não um dispatch de `Inventory`. `research` seria semanticamente prematuro porque seu
contrato exige adjudicação de candidatos. `Inventory` continua sendo um possível consumidor
posterior, mas seu lifecycle bounded e unregistered permanece bloqueado. O wrapper genérico do
host, quando ocorrer, é apenas evidência de transporte; não deve ser renomeado como identidade do
estudo, de Inventory ou de Research.

Neste plano, `dispatch` significa o lançamento nativo dessa tarefa via subagente, sem registro como
dispatch Arcanum governado. Se o lançamento for colocado sob um dispatch governado, deixa de estar
READY até que o wrapper produza o binding e o prompt efetivamente enviado comece, na primeira
linha, com `ACI-WORKFLOW-BINDING-V1:<base64>`. O stdout de binding/open/close permanece apenas no
journal. Não é permitido omitir o binding e depois descrever a execução como governada.

## O que esta decisão muda

- O freeze anterior de 35 fontes / 280 obrigações fica **superseded como rota de execução**. Seus
  manifests e reviews continuam sendo evidência histórica e fonte dos hashes já verificados.
- Não haverá escrita em `.arcanum/inventory`, `.arcanum/observability`, runtime, skills, registry,
  fontes do `cyberalchemy-orchestrator` ou fontes do `domainspec-core`.
- Cada lote pode falhar sem invalidar ou reabrir todos os demais.
- Cobertura total deixa de ser pré-condição para começar; qualquer afirmação de cobertura permanece
  bloqueada até todos os lotes planejados e seus auditores terminarem.
- Síntese, comparação com fenômenos vizinhos, formação de hipóteses e atualização do documento são
  trabalhos posteriores e separados.

## Recortes do corpus

Cada recorte só se torna `FROZEN` após um helper de preparação confirmar path, bytes, SHA-256,
revisão e status local. A preparação é mecânica; não lê semanticamente nem extrai findings.

| lote | superfície | fontes | estado |
|---|---|---:|---|
| D1 | DomainSpec v2: estrutura declarada de pesquisa e workflow | 3 | **FROZEN / READY** pelo annex revisado |
| D2 | DomainSpec v2: três documentos chamados de lentes e seu findings | 4 | frozen no annex; aguarda dispatch próprio |
| D3 | DomainSpec v2: composability, typed artifacts e design de unificação | 3 | frozen no annex; aguarda dispatch próprio |
| D4 | DomainSpec v2: work-pack, componente UI e relações tipadas | 3 | frozen no annex; aguarda dispatch próprio |
| C1 | Orchestrator: lentes, concerns, angles e perspectivas | parte do legado de 22 fontes | **BLOCK** até mini-manifest exato |
| C2 | Orchestrator: skills e capabilities | parte do legado de 22 fontes | **BLOCK** até mini-manifest exato |
| C3 | Orchestrator: workflow, topologia e handoffs | parte do legado de 22 fontes | **BLOCK** até mini-manifest exato |
| C4 | Orchestrator: artefatos, conhecimento e interfaces | parte do legado de 22 fontes | **BLOCK** até mini-manifest exato |
| C5 | Orchestrator: controles negativos deliberados | parte do legado de 22 fontes | **BLOCK** até mini-manifest exato |

Os recortes C1–C5 são uma fila de preparação, não um corpus implicitamente autorizado. Um agente
deverá reconstruir os mini-manifests a partir das fontes atuais; nenhum count ou hash do antigo
pacote 22/176 pode ser herdado sem revalidação.

## Ordem operacional

1. Executar D1 com um único scout read-only.
2. Depois de sua terminação, executar um auditor independente sobre o manifest e o retorno D1.
3. Se o auditor retornar `PASS`, abrir um novo dispatch de decisão de próximo lote. Ele pode propor
   D2, D3, D4 ou um lote C já manifestado; não pode sintetizar findings.
4. Repetir scout → auditor por lote, sem o auditor reparar o retorno.
5. Quando houver cobertura suficiente em mais de uma superfície, abrir um **novo dispatch de
   comparação interna** sobre os retornos aceitos e congelados.
6. Somente depois abrir um **novo dispatch de síntese**, com seu próprio objetivo, prompt, budget,
   revisão e autorização para propor mudanças no documento progressivo.

Não há handoff em memória. A única entrada de um dispatch posterior são paths e hashes de artefatos
terminados. O principal apenas lança, espera e reporta estados.

## Contrato comum dos scouts

### Perguntas

- Quais partes ou unidades o texto declara, prescreve, configura ou registra?
- Quais relações entre elas aparecem literalmente, e em que direção ou ordem?
- Que transformação, resultado, preservação, perda, falha ou ausência é explicitamente alegada ou
  observada?
- Qual é o estado da evidência: descrição, prescrição, configuração, execução registrada, efeito
  observado, ausência, ambiguidade ou contradição?
- O que a fonte não permite concluir?

Essas perguntas não usam ocorrência lexical, proximidade ou uma totalidade alegada como prova de
composição. O scout não deve classificar o caso como composição, agregação, sequência,
configuração, integração ou coordenação.

### Formato obrigatório do retorno

Para cada fonte:

1. identidade: repository, revision, path, SHA-256 e seletores;
2. source kind e authority state;
3. observações literais sobre partes, relações, ordem e transformação;
4. evidence state de cada observação;
5. execução ou efeito somente quando houver traço direto citado;
6. ausências, ambiguidades, contradições, exclusões e resíduos;
7. limites: conclusões que os bytes inspecionados não sustentam;
8. coverage ledger: uma linha terminal por fonte, inclusive `NO RELEVANT OBSERVATION`.

Cada afirmação material precisa de seletor verificável. Paráfrases devem permanecer reconhecíveis
como paráfrases; citações são mínimas. Inferência deve ser marcada e não pode virar finding.

## Preservação e write boundary

Cada lote escreve somente sob:

`internal-tools/composition-lab/orchestration/execution-redesign/runs/<batch-id>/`

Allowlist por lote:

- `scout-return.md` — escrito apenas pelo scout;
- `audit.md` — escrito apenas por auditor posterior;
- `decision.md` — opcional, escrito apenas por novo helper de decisão após a auditoria.

A criação do diretório exato do lote e do arquivo allowlisted correspondente faz parte da mesma
write allowance. Antes de cada tarefa, o orquestrador registra status e hashes dos paths-fonte e o
estado da pasta do lote; depois, o auditor compara esses baselines com o estado final. Mudanças
preexistentes fora dos paths-fonte e da pasta do lote são fora de escopo e não podem ser atribuídas
ao scout.

O manifest de entrada é o annex existente ou um mini-manifest futuro separado. O scout e o auditor
não o alteram. É proibida qualquer escrita em fontes, Inventory, observabilidade, research program,
RID, proposal, runtime, skills, registry ou checkout irmão. Stdout de open/close/binding permanece
somente no journal do bridge e nunca entra na pasta do lote.

## Auditoria por lote

O auditor é um novo helper connectionless iniciado somente após a terminação do scout. Ele confere:

- todos os itens do denominador têm linha terminal;
- path, revision e SHA-256 batem com o manifest;
- afirmações materiais têm seletores;
- claim, prescription, configuration, execution e observed effect não foram colapsados;
- ausência, ambiguidade, contradição, exclusão e resíduo foram preservados;
- nenhuma definição de composição, hipótese geral, classificação vizinha ou recomendação de
  produto foi introduzida;
- o diff está limitado ao único `scout-return.md` autorizado.

Vereditos: `PASS`, `BOUNDED_CORRECTIONS` ou `BLOCK`. `BOUNDED_CORRECTIONS` não autoriza edição pelo
auditor; exige novo attempt do scout, preservando o retorno anterior. Drift de fonte, source write,
authority escape ou cobertura incompleta resulta em `BLOCK`.

## Primeiro lote exato — D1

Repository: `C:/Users/victo/domainspec-core`  
Revision declarada: `9bfec22712e4675d39c4cf1c21b36dc66614136c`  
Privacidade: fonte interna do ecossistema; nenhuma cópia para superfície pública.

| path relativo | SHA-256 | bytes |
|---|---|---:|
| `projects/domainspec-v2/README.md` | `ca5cfbc0a467e3f14e459236d373db4c046f428930c0fae7571246bfe0aeefff` | 6246 |
| `projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md` | `cb09d2412e53288ae891ad6d1f03ff5d56c10808824bf0d7e025fc233cd93557` | 2575 |
| `projects/domainspec-v2/research/domainspec-v2-research-towers.dispatch.json` | `83206a57f4ed8d05a1c623ede6db17ae058e74fcfdc184150d20f2f7096147fd` | 15381 |

Saída do scout:

`internal-tools/composition-lab/orchestration/execution-redesign/runs/d1-domainspec-research-structure/scout-return.md`

Saída do auditor:

`internal-tools/composition-lab/orchestration/execution-redesign/runs/d1-domainspec-research-structure/audit.md`

### Prompt pronto — scout D1

> Você é o scout bounded e source-read-only do lote D1 da pesquisa interna do Composition Lab. Leia
> `C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/execution-redesign/internal-small-batch-plan.md`
> e inspecione somente as três fontes D1 ali enumeradas, em `C:/Users/victo/domainspec-core`, após confirmar
> revision, path, bytes e SHA-256. Se qualquer binding divergir, não leia semanticamente: escreva
> `BLOCK: SOURCE DRIFT` no único output autorizado e pare. Responda às perguntas do Contrato comum
> dos scouts sem pressupor que qualquer caso seja composição. Para cada afirmação material, cite
> path e seletor verificável. Separe descrição, prescrição, configuração, execução registrada,
> efeito observado, ausência, ambiguidade e contradição. Não defina composição ou lente; não importe
> teoria externa; não classifique fenômenos vizinhos; não infira causalidade; não faça síntese entre
> lotes; não recomende produto, arquitetura ou governance. Inclua todas as seções do Formato
> obrigatório e uma linha terminal para cada uma das três fontes. Escreva somente em
> `internal-tools/composition-lab/orchestration/execution-redesign/runs/d1-domainspec-research-structure/scout-return.md`.
> Não altere qualquer outro arquivo.

Budget do scout: **12.000 tokens**. Um attempt inicial; no máximo um novo attempt após
`BOUNDED_CORRECTIONS`, mediante novo dispatch e arquivo `scout-return-attempt-2.md` previamente
allowlisted.

### Prompt pronto — auditor D1

> Você é o auditor independente, source-read-only, do lote D1. Só comece depois de o scout terminar.
> Leia `C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/execution-redesign/internal-small-batch-plan.md`,
> `C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/dispatch-proposals/internal/domainspec-v2/corpus-manifest.md`
> e o retorno congelado do scout. Recalcule revision, status local,
> bytes e SHA-256 das três fontes; verifique o retorno contra todos os critérios da seção Auditoria
> por lote e confira que o único source write do scout foi o output allowlisted. Não corrija,
> complete, sintetize ou reinterprete o retorno. Escreva apenas
> `internal-tools/composition-lab/orchestration/execution-redesign/runs/d1-domainspec-research-structure/audit.md`,
> com denominador, checks, evidência de cada defeito e verdict terminal `PASS`,
> `BOUNDED_CORRECTIONS` ou `BLOCK`.

Budget do auditor: **6.000 tokens**. Um attempt, sem reparo silencioso.

## Critério de avanço

D1 autoriza somente o próximo dispatch de decisão quando:

- os três bindings forem revalidados;
- o scout terminar com cobertura 3/3;
- o auditor emitir `PASS`;
- os únicos writes novos do scout e do auditor, em relação aos baselines registrados antes de cada
  tarefa, forem a criação da pasta exata do lote e os dois outputs allowlisted;
- nenhum resultado for promovido a definição, hipótese geral, Inventory ou documento progressivo.

Um `PASS` prova disciplina de coleta no lote, não que composição ocorreu nem que o corpus interno
está coberto.

## Status

- Plano de pequenos lotes: **READY**.
- Primeiro scout D1: **READY AS NATIVE BOUNDED TASK**, condicionado ao registro mecânico do baseline
  pelo orquestrador e à revalidação feita pelo próprio scout. Se for lançado como dispatch Arcanum
  governado, permanece **BLOCKED ON BINDING/OPEN** até o prompt first-line e lifecycle exigidos.
- Auditor D1: **BLOCKED ON SCOUT TERMINATION**.
- Lotes C1–C5: **BLOCKED ON EXACT MINI-MANIFESTS**.
- Escrita ou promoção em Inventory: **BLOCKED** pelo lifecycle não resolvido e fora deste plano.
- Comparação interna e síntese: **BLOCKED** até retornos aceitos; cada uma exige um novo dispatch.
- Atualização do documento progressivo: **BLOCKED** até síntese revisada e autorização própria.

## Consequência para o projeto

O projeto começa a obter evidência sobre composição sem primeiro construir infraestrutura nova ou
forçar um contrato incompatível. O custo é aceitar progresso incremental e cobertura inicialmente
parcial. O ganho é que cada observação mantém origem, estado de evidência e limite; uma falha local
não contamina uma suposta execução total, e nenhuma topologia é declarada sem ter acontecido.
