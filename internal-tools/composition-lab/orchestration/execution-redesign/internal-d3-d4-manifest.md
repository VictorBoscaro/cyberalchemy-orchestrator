---
artifact_kind: internal-small-batch-dispatch-manifest
status: prepared-not-authorized
date: 2026-08-13
semantic_mode: bounded-source-read-only-scouts
registered_capability: none
source_repository: C:/Users/victo/domainspec-core
source_revision: 9bfec22712e4675d39c4cf1c21b36dc66614136c
source_branch: master
---

# Manifests e folhas exatas — lotes internos D3 e D4

## Objetivo e limite desta preparação

Este documento prepara dois dispatches nativos, independentes e connectionless para observar
fontes internas do DomainSpec v2. Ele não executa scouts, não produz findings e não classifica
qualquer ocorrência como composição. D3 e D4 reutilizam exatamente o contrato não-presuntivo do
`internal-small-batch-plan.md`; nenhum lote recebe resultados do outro.

Estado: **PREPARED / NOT LAUNCH-AUTHORIZED**. Antes de cada lançamento, o orquestrador deve
revalidar o baseline mecânico descrito abaixo. Se o transporte for convertido em dispatch Arcanum
governado, esta folha deixa de estar pronta até que o binding/open seja produzido e a primeira linha
do prompt efetivamente enviado seja `ACI-WORKFLOW-BINDING-V1:<base64>`.

## Autoridade e bases congeladas

Fontes de controle lidas para esta preparação:

| path | SHA-256 | bytes | estado no host em 2026-08-13 |
|---|---|---:|---|
| `internal-tools/composition-lab/orchestration/execution-redesign/internal-small-batch-plan.md` | `1de448af05f7b8bc0d93738d1f7b4273cec610661cfa43a64f909921b1d6a700` | 14428 | untracked |
| `internal-tools/composition-lab/orchestration/dispatch-proposals/internal/domainspec-v2/corpus-manifest.md` | `cd9af19f84cdb8b924f386984cdbc7e0a320d03d9e60776c9193833fc139de7f` | 7964 | untracked |

Estado mecânico capturado:

- `domainspec-core`: branch `master`, revisão
  `9bfec22712e4675d39c4cf1c21b36dc66614136c`; checkout globalmente sujo (12.124 linhas em
  `git status --porcelain=v1`), porém `git status --porcelain=v1 -- <os seis paths D3/D4>` não
  retornou entradas. Portanto, **somente os seis paths estão confirmados limpos**; não há alegação
  de limpeza global.
- `cyberalchemy-orchestrator`: branch `master`, revisão
  `48d5f7b830fc52773da8ce5191131ec2e05274f4`; checkout globalmente sujo (56 linhas em
  `git status --porcelain=v1` antes da criação desta folha). As duas fontes de controle acima já
  eram untracked. Mudanças preexistentes não podem ser atribuídas aos scouts.
- O annex é autoridade de seleção; revision + path + bytes + SHA-256 são a autoridade dos bytes.
  A revisão, sozinha, não prova o conteúdo de um checkout sujo.

O estado acima documenta a preparação, não substitui o baseline imediatamente anterior a cada
scout e auditor.

## Pergunta comum, não-presuntiva

Cada scout deve responder, para cada fonte e sem decidir se há composição:

1. Quais partes ou unidades o texto declara, prescreve, configura ou registra?
2. Quais relações entre elas aparecem literalmente, e em que direção ou ordem?
3. Que transformação, resultado, preservação, perda, falha ou ausência é explicitamente alegada ou
   observada?
4. Qual é o estado da evidência: descrição, prescrição, configuração, execução registrada, efeito
   observado, ausência, ambiguidade ou contradição?
5. O que a fonte não permite concluir?

Ocorrência lexical, proximidade e totalidade alegada não contam como prova de composição. O scout
não classifica o caso como composição, agregação, sequência, configuração, integração ou
coordenação.

## Baseline obrigatório por tarefa

Imediatamente antes de lançar cada scout, o orquestrador deve preservar no registro de lançamento:

1. `git -C C:/Users/victo/domainspec-core rev-parse HEAD` e branch;
2. `git status --porcelain=v1 --untracked-files=all -- <os três paths do lote>`;
3. existência, bytes e SHA-256 de cada fonte;
4. `git -C C:/Users/victo/cyberalchemy-orchestrator rev-parse HEAD` e branch;
5. `git status --porcelain=v1 --untracked-files=all` do host;
6. inventário recursivo de todos os arquivos visíveis no host, com path relativo e SHA-256, antes
   da tarefa; depois da tarefa, repetir o mesmo inventário e preservar o diff path/hash;
7. existência e hash de todos os arquivos já presentes no diretório exato do lote.

Qualquer divergência em revisão, path, status scoped, bytes ou SHA-256 bloqueia leitura semântica e
obriga o scout a escrever somente `BLOCK: SOURCE DRIFT` em seu output exclusivo. Um baseline de
auditor é capturado novamente após o scout terminar e antes de o auditor começar, também com
`--untracked-files=all` e inventário recursivo path/hash. O auditor compara os inventários
antes/depois, não apenas o resumo Git; ele não atribui ao scout mudanças preexistentes ou
concorrentes sem evidência.

## D3 — composability, typed artifacts e design de unificação

### Manifest congelado

Repository: `C:/Users/victo/domainspec-core`  
Revision: `9bfec22712e4675d39c4cf1c21b36dc66614136c`  
Denominador: **3 fontes / 3 linhas terminais obrigatórias**

| path relativo | SHA-256 | bytes | limpeza scoped em 2026-08-13 |
|---|---|---:|---|
| `projects/domainspec-v2/research/2026-07-01-composability-edges-taxonomy-synthesis.md` | `bf2a5a45f7214e36eda2048251315571a6d8d27be7a1e59c1c8f0ce23963fc0d` | 10798 | clean |
| `projects/domainspec-v2/research/typed-artifacts-precedent/findings.md` | `597bdf17b876b2d4ab68b91e6c748cdb849214cd36cec011d3e83b75dc59606f` | 9923 | clean |
| `projects/domainspec-v2/research/spec-ontology-unification/DESIGN.md` | `e5410e893314d0c000d291e02a527b4535e5f689f9862ab0b1259e1d78138432` | 6410 | clean |

Run directory:
`internal-tools/composition-lab/orchestration/execution-redesign/runs/d3-domainspec-composability-typed-unification/`

Write allowlist por papel:

- scout, exclusivamente: `scout-return.md`;
- auditor posterior, exclusivamente: `audit.md`.

O scout não pode criar `audit.md`, arquivos auxiliares ou outro output. A criação do diretório exato
e de `scout-return.md` constitui toda a sua write allowance.

### Prompt exato — scout D3

> Você é o scout bounded e source-read-only do lote D3 da pesquisa interna do Composition Lab. Leia
> `C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/execution-redesign/internal-small-batch-plan.md`,
> `C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/execution-redesign/internal-d3-d4-manifest.md`
> e inspecione semanticamente somente as três fontes D3 enumeradas nesta folha, em
> `C:/Users/victo/domainspec-core`, após confirmar revision, path, status scoped, bytes e SHA-256.
> Se qualquer binding divergir, não leia semanticamente: escreva `BLOCK: SOURCE DRIFT` no único
> output autorizado e pare. Responda, para cada fonte, à mesma Pergunta comum, não-presuntiva desta
> folha. Para cada afirmação material, cite path e seletor verificável. Separe descrição,
> prescrição, configuração, execução registrada, efeito observado, ausência, ambiguidade e
> contradição. Inclua identidade, source kind, authority state, observações literais, limites,
> exclusões e resíduos, e uma linha terminal por fonte, inclusive `NO RELEVANT OBSERVATION`. Não
> defina composição ou lente; não importe teoria externa; não classifique fenômenos vizinhos; não
> infira causalidade; não faça síntese entre lotes; não recomende produto, arquitetura ou
> governance. Escreva somente em
> `C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/execution-redesign/runs/d3-domainspec-composability-typed-unification/scout-return.md`.
> Não altere qualquer outro arquivo.

Budget do scout D3: **12.000 tokens**. Um attempt inicial. Eventual segundo attempt exige novo
dispatch, `BOUNDED_CORRECTIONS` prévio e `scout-return-attempt-2.md` explicitamente allowlisted em
nova folha; não está autorizado aqui.

### Prompt exato — auditor D3

> Você é o auditor independente e source-read-only do lote D3. Só comece depois de o scout terminar.
> Leia o plano small-batch, esta folha, o annex de corpus e o retorno congelado D3. Recalcule revisão,
> branch, status scoped, bytes e SHA-256 das três fontes; confira cobertura 3/3, seletores, estados de
> evidência, limites e proibições contra definição, classificação, síntese e recomendação. Compare os
> baselines anterior e posterior e confirme que o único write atribuível ao scout foi
> `runs/d3-domainspec-composability-typed-unification/scout-return.md`. Não corrija, complete,
> sintetize ou reinterprete o retorno. Escreva somente em
> `C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/execution-redesign/runs/d3-domainspec-composability-typed-unification/audit.md`,
> com denominador, checks, evidência de cada defeito e verdict terminal `PASS`,
> `BOUNDED_CORRECTIONS` ou `BLOCK`.

Budget do auditor D3: **6.000 tokens**. Um attempt, sem reparo silencioso.

## D4 — work-pack, componente UI e relações tipadas

### Manifest congelado

Repository: `C:/Users/victo/domainspec-core`  
Revision: `9bfec22712e4675d39c4cf1c21b36dc66614136c`  
Denominador: **3 fontes / 3 linhas terminais obrigatórias**

| path relativo | SHA-256 | bytes | limpeza scoped em 2026-08-13 |
|---|---|---:|---|
| `projects/domainspec-v2/development/ds-d1-improvement-plan/WORK-PACK.md` | `c70bca7310ac0e3e06046f88a978e85edb82b6ba8fbe4d40f29f3f8526029d81` | 18242 | clean |
| `projects/domainspec-v2/impl/spec/meta-types/ui/component.schema.yml` | `46540796103bac845fc78aee3deceb8fe905a85968b76f7edb7d987efc8deca0` | 1286 | clean |
| `projects/domainspec-v2/definitions/relationships/relationships.yml` | `7757884f599bb18707f105add8b9de92fb2ea58d78e216d3aa228b0ad25ea013` | 27039 | clean |

Run directory:
`internal-tools/composition-lab/orchestration/execution-redesign/runs/d4-domainspec-workpack-ui-relations/`

Write allowlist por papel:

- scout, exclusivamente: `scout-return.md`;
- auditor posterior, exclusivamente: `audit.md`.

O scout não pode criar `audit.md`, arquivos auxiliares ou outro output. A criação do diretório exato
e de `scout-return.md` constitui toda a sua write allowance.

### Prompt exato — scout D4

> Você é o scout bounded e source-read-only do lote D4 da pesquisa interna do Composition Lab. Leia
> `C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/execution-redesign/internal-small-batch-plan.md`,
> `C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/execution-redesign/internal-d3-d4-manifest.md`
> e inspecione semanticamente somente as três fontes D4 enumeradas nesta folha, em
> `C:/Users/victo/domainspec-core`, após confirmar revision, path, status scoped, bytes e SHA-256.
> Se qualquer binding divergir, não leia semanticamente: escreva `BLOCK: SOURCE DRIFT` no único
> output autorizado e pare. Responda, para cada fonte, à mesma Pergunta comum, não-presuntiva desta
> folha. Para cada afirmação material, cite path e seletor verificável. Separe descrição,
> prescrição, configuração, execução registrada, efeito observado, ausência, ambiguidade e
> contradição. Inclua identidade, source kind, authority state, observações literais, limites,
> exclusões e resíduos, e uma linha terminal por fonte, inclusive `NO RELEVANT OBSERVATION`. Não
> defina composição ou lente; não importe teoria externa; não classifique fenômenos vizinhos; não
> infira causalidade; não faça síntese entre lotes; não recomende produto, arquitetura ou
> governance. Escreva somente em
> `C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/execution-redesign/runs/d4-domainspec-workpack-ui-relations/scout-return.md`.
> Não altere qualquer outro arquivo.

Budget do scout D4: **12.000 tokens**. Um attempt inicial. Eventual segundo attempt exige novo
dispatch, `BOUNDED_CORRECTIONS` prévio e `scout-return-attempt-2.md` explicitamente allowlisted em
nova folha; não está autorizado aqui.

### Prompt exato — auditor D4

> Você é o auditor independente e source-read-only do lote D4. Só comece depois de o scout terminar.
> Leia o plano small-batch, esta folha, o annex de corpus e o retorno congelado D4. Recalcule revisão,
> branch, status scoped, bytes e SHA-256 das três fontes; confira cobertura 3/3, seletores, estados de
> evidência, limites e proibições contra definição, classificação, síntese e recomendação. Compare os
> baselines anterior e posterior e confirme que o único write atribuível ao scout foi
> `runs/d4-domainspec-workpack-ui-relations/scout-return.md`. Não corrija, complete, sintetize ou
> reinterprete o retorno. Escreva somente em
> `C:/Users/victo/cyberalchemy-orchestrator/internal-tools/composition-lab/orchestration/execution-redesign/runs/d4-domainspec-workpack-ui-relations/audit.md`,
> com denominador, checks, evidência de cada defeito e verdict terminal `PASS`,
> `BOUNDED_CORRECTIONS` ou `BLOCK`.

Budget do auditor D4: **6.000 tokens**. Um attempt, sem reparo silencioso.

## Confirmação separada e ordem

D3 e D4 são duas decisões separadas. Autorizar um não autoriza o outro, seus auditores, retries,
comparação, síntese, Inventory ou atualização do documento progressivo. Podem ser lançados em
paralelo somente se cada scout tiver output exclusivo, baseline próprio e nenhum acesso ao retorno
do outro. Cada auditor continua bloqueado até o término do respectivo scout.

Folha de decisão D3: `AUTHORIZE D3 SCOUT` ou `REVISE D3` ou `STOP D3`.  
Folha de decisão D4: `AUTHORIZE D4 SCOUT` ou `REVISE D4` ou `STOP D4`.

Após eventual `PASS`, cada lote autoriza somente um dispatch posterior de decisão. Não autoriza
generalização sobre composição nem afirmação de cobertura do corpus interno.
