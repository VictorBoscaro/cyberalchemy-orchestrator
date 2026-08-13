---
artifact_kind: execution-primitive-advice
status: ready
date: 2026-08-13
advisor: independent-b
scope: D1-D3-D4-source-transport
---

# Parecer B — primitivas existentes para D1, D3 e D4

## Veredito

**READY**, com `git archive` da revisão fixada como transporte de leitura dos sources de
`domainspec-core`, extração em diretório temporário exclusivo por lote e outputs mantidos no
`cyberalchemy-orchestrator`.

Isso substitui o baseline global do checkout, não o manifest por lote nem a auditoria do retorno.
Não há evidência de uma primitive local pronta que entregue simultaneamente snapshot pinned,
isolamento, cleanup e receipt; construir um harness novo agora seria desproporcional.

## Evidência local encontrada

- Há precedente explícito para criação e remoção de worktrees em
  `C:/Users/victo/domainspec-core/.github/get-shit-done/workflows/new-workspace.md:143-149` e
  `remove-workspace.md:67-70`. O precedente cria branch e possui lifecycle de remoção.
- Há precedente de projeção staged com hashes em
  `projects/domainspec-v2/development/first-production-release/backend-type-test-engine-completeness/refreshes/2026-07-23-l0a-evidence-reconciliation/projections/build-projection-package.py`:
  `STAGED_PREFIX` nas linhas 13-14, SHA-256 na linha 56 e mapeamento target→staged nas linhas 63-64.
  É um exemplo específico daquele work-pack, não uma primitive genérica reutilizável sem adaptação.
- O contrato CVR documenta o desenho desejável — diretório temporário efêmero, hashes, comandos e
  cleanup (`docs/features/agents-communication-infra/work-pack/tasks/TASK-CVR.md:367-369`) — mas é
  especificação/work-pack, não uma ferramenta pronta para estes scouts.
- Ambos os repositórios estão globalmente dirty. O source repo observado estava em
  `9bfec22712e4675d39c4cf1c21b36dc66614136c`; o host estava em
  `48d5f7b830fc52773da8ce5191131ec2e05274f4`. Logo, copiar do working tree não prova os bytes da
  revisão, mesmo quando os paths selecionados aparecem scoped-clean.

## Comparação

| opção | vantagens | custos/riscos | decisão |
|---|---|---|---|
| `git archive <rev> -- <paths>` | lê objetos do commit, ignora dirty worktree, não cria branch, não toca index, produz conjunto mínimo e reproduzível | inclui apenas paths tracked; extração é gravável e ainda depende de disciplina de acesso do agente | **usar** |
| worktree detached temporário | snapshot completo em revisão exata; padrão de add/remove já existe | cria metadata Git, materializa repo inteiro, cleanup mais delicado no Windows; o novo worktree continua gravável | não usar para scouts de 3 arquivos |
| projeção staged local | outputs e hashes explícitos; precedentes fortes | scripts encontrados são específicos a work-packs; adaptação seria código novo e duplicaria `git archive` | não reutilizar diretamente |
| leitura do checkout + before/after global | nenhum setup | checkout muito dirty; diff global é caro e atribuição concorrente é fraca | rejeitar |

## Receita mínima por lote (PowerShell/Windows)

O principal cria e retém um diretório temporário exclusivo; o scout não cria snapshots, não lança
agentes e recebe apenas o path extraído e o único output allowlisted.

```powershell
$sourceRepo = 'C:\Users\victo\domainspec-core'
$sourceRev = '9bfec22712e4675d39c4cf1c21b36dc66614136c'
$batchId = 'd1-domainspec-research-structure' # trocar para D3/D4
$snapshotRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("composition-lab-$batchId-" + [guid]::NewGuid())
$archivePath = "$snapshotRoot.zip"
New-Item -ItemType Directory -Path $snapshotRoot | Out-Null

git -C $sourceRepo archive --format=zip --output=$archivePath $sourceRev -- <exact-path-1> <exact-path-2> <exact-path-3>
Expand-Archive -LiteralPath $archivePath -DestinationPath $snapshotRoot
Get-FileHash -Algorithm SHA256 -LiteralPath <each-extracted-path>
```

Antes do launch, o principal exige: `git rev-parse "$sourceRev^{commit}"` igual à revisão fixada;
`git cat-file -e "$sourceRev^{commit}"`; exit code zero do archive; exatamente três arquivos
extraídos; e SHA-256/bytes iguais ao manifest do lote. Qualquer falha produz `BLOCK: SOURCE DRIFT`
sem leitura semântica.

Para reduzir erro acidental, o principal pode aplicar `Set-ItemProperty -Name IsReadOnly -Value
$true` aos três arquivos extraídos. Isso é uma barreira local conveniente, não uma sandbox de
segurança. A prova relevante é mais simples:

1. os inputs vieram dos objetos do commit, não do checkout;
2. hashes dos extraídos batem com o manifest antes do scout;
3. hashes dos extraídos são recalculados depois do scout;
4. os três blobs originais no Git continuam endereçados pela mesma revisão;
5. o único write esperado fica no run directory separado do host.

O auditor recebe o snapshot retido, o retorno e o manifest. Cleanup ocorre somente após auditoria.
Para recuperação, registrar o path temporário; em crash, não reutilizar o diretório, marcar o lote
incompleto e criar outro GUID. Ao remover, primeiro resolver o path absoluto e comprovar que seu nome
começa por `composition-lab-` dentro de `[System.IO.Path]::GetTempPath()`; só então usar
`Remove-Item -LiteralPath <validated-path> -Recurse -Force` e remover o `.zip` irmão. Cleanup
desconhecido não deve virar PASS.

## Limites que permanecem

- `git archive` protege contra contaminação do checkout dirty; não impede tecnicamente o agente de
  abrir o checkout original. O prompt deve proibir isso e o auditor só pode afirmar confinamento
  observado, não sandbox enforcement.
- A separação de output é por path e papel, não por ACL. Cada scout escreve somente seu
  `runs/<batch>/scout-return.md`; o principal é o único que prepara snapshot, lança, espera e decide
  o próximo dispatch. Prompts devem proibir spawn/delegação pelo scout.
- Arquivos de controle untracked no host não entram em `git archive`. Devem ser fornecidos como
  inputs de controle com hashes registrados, ou seu contrato necessário deve estar integralmente no
  prompt. Não copiá-los para o snapshot como se pertencessem à revisão do sibling.
- Se um lote precisar de submodules, symlinks, geração ou contexto amplo não enumerado, `git archive`
  deixa de bastar; nesse caso, reavaliar um worktree detached. D1/D3/D4, como manifests de três
  arquivos tracked, não demonstram essa necessidade.

## Recomendação

Executar D1, D3 e D4 como tarefas nativas independentes sobre snapshots `git archive` separados,
com auditor posterior por lote. Remover do critério de admissão o inventário hash global do host:
ele é caro e não prova atribuição em um workspace concorrente. Substituí-lo por (a) archive pinned,
(b) hash exato de três inputs, (c) allowlist de um output e (d) auditoria desse output. Não criar
harness, branch, worktree ou capability nova antes de evidência de que essa receita falha.
