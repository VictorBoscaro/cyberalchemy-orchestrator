---
artifact_kind: execution-redesign-adversarial-review
status: complete
date: 2026-08-13
verdict: BLOCK
---

# Review — checkpoint de redesenho da execução

## Coverage

| reviewer | lens | targets attacked | result |
|---|---|---|---|
| independent reviewer | mechanics / provenance / governance / operability | dois advisors; planos interno e externo; manifest D3/D4 e review; manifest de snapshot; helper e testes de snapshot; helper de baseline morto, seus testes e review; retorno/auditoria D1; diff/status do checkpoint | 5 findings sobreviventes; `BLOCK` |

Foram atacados: equivalência byte a byte, provenance pinned, source before/after, Windows e repositórios
dirty, separação snapshot/output, cleanup/recuperabilidade, principal-only-orchestrates, execução exata
D1/D3/D4 e risco de criar framework novo. Não foram executados scouts, pesquisa, lifecycle ou runtime.
O único teste executado foi `Test-SourceSnapshot.ps1`, em fixture temporária; resultado literal:
`RESULT: 0 passed, 4 failed`, exit code `1`. O primeiro erro foi
`Archive member set differs from manifest`.

## Helper de snapshot e testes

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---:|---|---|---|---|
| 1 | `tools/Invoke-SourceSnapshot.ps1` | A criação depende de `if (@($entryNames \| Sort-Object) -join "\`n" -ne @($paths \| Sort-Object) -join "\`n") { throw 'Archive member set differs from manifest' }`. O teste oficial falhou nessa linha; em consequência, nenhum snapshot foi criado e os quatro testes terminaram `FAIL`. | CRITICAL | Corrigir a comparação de conjuntos e exigir que a suíte passe integralmente antes de qualquer materialização ou launch. |
| 2 | `tools/Invoke-SourceSnapshot.ps1` | `Test-Snapshot` verifica apenas `foreach ($file in @($receipt.files))`; não enumera `tree/` nem exige conjunto exato. Um arquivo adicional no snapshot não seria observado, contrariando o requisito 9/9 e a prova before/after. | CRITICAL | Na verificação, comparar bidirecionalmente o conjunto completo de arquivos regulares em `tree/` com os paths do receipt e adicionar teste negativo de arquivo extra. |
| 3 | `tools/Invoke-SourceSnapshot.ps1` | O receipt é “autenticado” por um digest mutável ao lado dele: `$expectedReceiptHash = (Get-Content ... 'snapshot-manifest.sha256')`; depois o blob é recalculado apenas sobre o arquivo materializado e comparado a `$file.blob`. `Verify` não resolve novamente `source_revision:path`, não confere tree/revision com Git e não recebe o manifest aprovado. Receipt, arquivo e digest podem ser alterados coerentemente e ainda passar. | CRITICAL | Vincular `Verify` ao manifest aprovado por path/hash externo e recomputar commit, tree, blob id, bytes e SHA-256 contra `revision:path`; testar adulteração coordenada de tree + receipt + digest. |
| 4 | `tools/Test-SourceSnapshot.ps1` | A suíte declara somente quatro casos — `create from pinned commit`, `independent verification`, `tampering is detected` e `cleanup is bounded and recoverable` — e todos falharam. Não cobre membro adicional, receipt/digest adulterados juntos, revision/tree inexistente ou divergente, reparse/junction no snapshot, falha parcial após publicação nem igualdade do status dos repositórios antes/depois. | MAJOR | Completar os casos adversariais exigidos e registrar um run verde em Windows/PowerShell sobre repo dirty sem tocar source, runtime, lifecycle, Inventory ou skills. |

**Verdict:** FIX

## Planos, manifests e execução D1/D3/D4

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---:|---|---|---|---|
| 5 | `internal-small-batch-plan.md`; `internal-d3-d4-manifest.md`; `advisor-snapshot.md` | Os prompts ainda mandam ler diretamente `em C:/Users/victo/domainspec-core` (plano D1 e manifests D3/D4), enquanto o advisor determina: `Scouts devem receber paths do snapshot, não paths do checkout irmão` e registra que os prompts atuais `precisam de uma revisão mecânica separada antes do launch`. D1 anterior permanece `BLOCK`; D3/D4 estão explicitamente `PREPARED / NOT LAUNCH-AUTHORIZED`. Logo não existe execução exata pronta para D1, D3 ou D4 sobre o novo transporte. | CRITICAL | Após o helper passar review, materializar/verificar snapshots por lote, congelar seus receipts e substituir os três prompts por paths/identidades lógicas do snapshot; submeter cada launch a autorização separada. |

**Verdict:** FIX

## Checks que sobreviveram

- O manifest fonte fixa repository, commit, tree, 3 paths por lote, bytes e SHA-256 para D1/D3/D4.
- Snapshot e outputs são desenhados em raízes distintas; o helper restringe `SnapshotParent` ao temp e
  o cleanup usa `-LiteralPath` sobre filho direto prefixado.
- O plano atribui ao principal lançar, esperar e reportar; scouts não recebem autoridade para spawn.
- O helper é específico e pequeno; não há evidência de uma capability, lifecycle ou framework novo.
- O baseline global anterior foi corretamente mantido morto: seu próprio review termina
  `KILL desta rota`; ele não pode ser usado como evidência de prontidão.
- A auditoria D1 preserva honestamente `BLOCK` por ausência de baseline pré-scout; seu retorno não foi
  promovido a evidência aceita.

## Provenance e write-scope

O checkpoint não contém snapshot publicado, receipt de materialização independente nem receipt
before/after dos dois repositórios para uma execução D1/D3/D4. Portanto não há base para afirmar
byte-equivalence operacional ou source unchanged durante uma execução. O workspace já estava dirty;
este review não atribui mudanças preexistentes ao pivot. A execução da suíte temporária fez cleanup
da fixture, mas falhou antes de demonstrar o contrato do helper.

## Change requests

1. CRITICAL — fazer `Create` funcionar e obter suíte verde.
2. CRITICAL — verificar conjunto exato, rejeitando arquivos adicionais.
3. CRITICAL — reancorar `Verify` no manifest/commit, não em receipt e digest mutuamente alteráveis.
4. CRITICAL — atualizar D1/D3/D4 para consumir snapshots verificados e obter autorizações exatas.
5. MAJOR — ampliar a suíte Windows/dirty/reparse/tamper/cleanup e preservar receipts reproduzíveis.

## Verdict terminal

**BLOCK.** O checkpoint ainda não permite executar D1, D3 ou D4: o helper falha 0/4, sua verificação
não prova conjunto exato nem provenance pinned contra adulteração coordenada, e os prompts continuam
apontando para o checkout vivo. Nenhum scout ou pesquisa adicional deve ser lançado a partir deste
checkpoint.

`exit_reason: verified blocking findings`

`agents_spawned: 0`
