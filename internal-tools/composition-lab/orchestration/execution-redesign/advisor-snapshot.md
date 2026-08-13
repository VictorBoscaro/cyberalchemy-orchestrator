---
artifact_kind: immutable-source-snapshot-advice
status: ready
date: 2026-08-13
verdict: READY
source_repository: C:/Users/victo/domainspec-core
source_revision: 9bfec22712e4675d39c4cf1c21b36dc66614136c
---

# Parecer — snapshot materializado do corpus DomainSpec v2

## Veredito

**READY**, condicionado a materializar e verificar o snapshot antes de qualquer novo scout. A rota
recomendada é `git archive` da revisão fixada, restrito aos nove paths D1/D3/D4, seguido de extração
em diretório novo e content-addressed. Não reutilizar o checkout vivo e não criar `git worktree`.

O KILL do baseline harness permanece válido. O snapshot elimina a necessidade de provar que um
scout não alterou e reverteu fontes em um checkout sujo: o objeto de leitura passa a ser uma cópia
fechada de blobs já endereçados pelo commit. Ele não autoriza pesquisa, scout, runtime, lifecycle ou
mudança nas fontes.

## Por que archive, não worktree

- `git archive <revision> -- <paths>` lê a árvore do commit, não o index nem os milhares de writes
  locais do checkout `domainspec-core`.
- Um worktree temporário ainda é uma árvore mutável, cria metadados em
  `domainspec-core/.git/worktrees`, exige cleanup coordenado e reabre a pergunta de write
  attribution que bloqueou D1.
- O archive preserva exatamente os bytes dos blobs Git. A prova é simples: para cada arquivo,
  comparar SHA-256 e tamanho do extraído com o manifest aprovado e, adicionalmente, comparar o
  SHA-256 do extraído com bytes emitidos por `git cat-file blob <revision>:<path>`.
- A revisão existe localmente como `commit`; portanto, a materialização não depende de rede nem do
  estado da branch.

## Forma mínima proposta

Diretório dedicado, separado de outputs de execução:

`internal-tools/composition-lab/orchestration/execution-redesign/snapshots/domainspec-v2/9bfec22712e4675d39c4cf1c21b36dc66614136c-d1-d3-d4/`

Conteúdo permitido:

1. `source.tar` — archive restrito aos nove paths;
2. `tree/` — extração preservando paths relativos;
3. `snapshot-manifest.json` — revisão, tree id, paths ordenados, blob ids, bytes e SHA-256 de cada
   fonte, SHA-256 do tar, comando/versões usados e verdict terminal;
4. `README.md` — contrato curto: snapshot append-never/replace-never; consumidores só leem `tree/`;
   qualquer divergência bloqueia e exige um novo diretório de snapshot.

Não colocar scout returns, audits, receipts de bridge ou logs nessa árvore. Eles continuam somente
em `execution-redesign/runs/<batch-id>/` (e stdout do bridge apenas no journal).

## Procedimento mecânico proposto

1. Falhar se o diretório final já existir. Criar primeiro um staging sibling com nome aleatório.
2. Confirmar `git cat-file -t 9bfec... == commit` e registrar o tree id
   `8fec9a49d0314213380358dfa4a874f50b5fba1f`.
3. Executar `git -C C:/Users/victo/domainspec-core archive --format=tar --output=<staging>/source.tar
   9bfec... -- <nove paths exatos>`.
4. Extrair com `tar -xf` para `<staging>/tree`; rejeitar qualquer membro absoluto, `..`, symlink,
   hardlink ou path fora de `tree/` antes de aceitar a extração. Os nove alvos esperados são arquivos
   regulares.
5. Para cada path, obter o blob id com `git rev-parse 9bfec...:<path>`, verificar tipo `blob`, e
   comparar bytes/tamanho/hash do arquivo extraído com o blob e com os manifests D1/D3/D4. Exigir
   conjunto exato 9/9: nenhum arquivo adicional.
6. Escrever o manifest no staging, calcular seu próprio digest por um envelope separado ou declarar
   explicitamente que ele não se auto-autentica, e então renomear atomicamente o staging para o
   diretório final no mesmo volume.
7. Marcar arquivos como read-only no Windows apenas como defesa acidental. Isso não é prova de
   imutabilidade; a identidade real é commit + blob ids + hashes, revalidada por cada consumidor
   antes e depois da leitura.

Não é necessário criar código permanente: um helper mecânico pode executar comandos Git/tar e
produzir o manifest. Se houver script reutilizável, ele exigirá review próprio; não ressuscitar o
baseline genérico.

## Critério de aceitação

O snapshot fica `READY FOR READ` somente se:

- commit e tree id conferem;
- o tar possui digest registrado;
- o conjunto extraído é exatamente os nove paths declarados;
- cada item confere em blob id, bytes e SHA-256 com Git e com os manifests aprovados;
- o diretório final não existia e foi publicado uma única vez;
- nenhuma alteração ocorreu em `domainspec-core`, runtime, skills, Inventory ou lifecycle;
- um verificador independente reproduz 9/9 e confirma a separação snapshot/output.

Scouts devem receber paths do snapshot, não paths do checkout irmão, e citar a identidade lógica
original (`repository`, `revision`, `path`, `blob`) junto do path materializado. Antes e depois de
cada scout, basta revalidar os nove hashes do snapshot e auditar somente seu diretório de output.

## Cleanup e recuperação

- Falha antes da publicação: apagar apenas o staging resolvido e confirmado sob o diretório
  `snapshots/domainspec-v2/`; o diretório final não é criado.
- Falha ou drift depois da publicação: nunca reparar ou sobrescrever. Marcar o snapshot rejeitado e
  materializar outro diretório com nova identidade/sufixo.
- Após o milestone, `source.tar` e `tree/` são removíveis juntos somente por decisão explícita; o
  manifest pode ser preservado como provenance. Não tocar no checkout irmão.

## Riscos residuais

1. ACL/read-only não impede um agente com acesso irrestrito de editar o snapshot; por isso hashes
   antes/depois continuam obrigatórios.
2. `git archive` não inclui alterações locais — isso é intencional. A pesquisa descreve a revisão
   fixada, não o estado vivo atual de DomainSpec v2.
3. Git pode aplicar atributos de export; a dupla comparação com os blobs detecta qualquer alteração
   de bytes. Se houver divergência, bloquear em vez de normalizar.
4. D1 anterior permanece `BLOCK`; o snapshot habilita um novo attempt, não legitima
   retroativamente o attempt sem baseline.
5. Manifests/prompts atuais que apontam para `C:/Users/victo/domainspec-core` precisam de uma revisão
   mecânica separada antes do launch; este parecer não os modifica.

## Disposição

**READY para um helper de materialização seguido de verificador independente. BLOCK para lançar
D1/D3/D4 diretamente antes dessa verificação e antes de atualizar os prompts para os paths do
snapshot.**
