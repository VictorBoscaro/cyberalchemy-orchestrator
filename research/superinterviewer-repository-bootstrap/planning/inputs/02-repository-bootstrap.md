# Plano gateado — bootstrap do repositório Superinterviewer

## Status e limite

Este documento planeja o bootstrap. Ele não autoriza criar o repositório, provisionar remoto, importar
frameworks, executar o programa de pesquisa nem implementar o produto.

O objetivo servido é dar ao Superinterviewer uma casa limpa que possua sua identidade, seu programa de
pesquisa e suas decisões sem herdar a arquitetura de nenhum provedor. O bootstrap será considerado bem-sucedido
quando um clone limpo puder localizar as autoridades do produto e da pesquisa, reproduzir a origem de cada
material fundador e distinguir uma referência externa de uma dependência executável.

As disposições aceitas no Robot-Talks são a base do plano: repositório novo como decisão do owner com condição
de revisão; autoridades separadas; bootstrap menor que `mint`; SWI como peer/provider candidate; referências
estreitas e pinadas; implementação somente depois de um experimento discriminante.

## Três trabalhos que não devem ser colapsados

| trabalho | resultado | permitido nesta etapa | não permitido |
|---|---|---|---|
| Planejar | pacote fundador revisável e roteiro de criação | preparar, revisar e corrigir artefatos sob `research/superinterviewer-repository-bootstrap/` | inicializar outro Git repo ou declarar autoridade já vigente nele |
| Criar o repositório | Git repo local, portátil, com o casting mínimo aprovado | criar a árvore mínima, validar, fazer o primeiro commit e, se autorizado separadamente, provisionar/pushar o remoto | adicionar runtime, adapter, banco, ledger, submodule amplo ou código de produto |
| Implementar o produto | experimento/protótipo que responde a uma incerteza nomeada | somente após gate próprio com hipóteses concorrentes, evidência esperada e regra de aceitação | usar o bootstrap ou um protótipo para resolver silenciosamente questões de produto |

## Sequência gateada

### G0 — Aceitar este plano

O owner confirma a sequência e mantém em aberto os parâmetros que ainda não têm evidência suficiente: nome
canônico, localização local, host/organização do remoto, visibilidade, licença, branch padrão e identidade do
signer inicial. Aceitar G0 autoriza apenas preparar o pacote fundador neste repositório.

### P1 — Preparar o pacote fundador aqui

Preparar `research/superinterviewer-repository-bootstrap/founding-package/` como um pacote de transferência,
sem tratá-lo como authority do produto antes da revisão. O pacote deve conter:

- `TRANSFER-MANIFEST.md`: inventário, destino de cada arquivo, estado (`DRAFT` ou `ACCEPTED`), digest e ordem de
  instalação;
- `README.md`: identidade concisa do Superinterviewer, propósito do repo, estado research-first e mapa das
  autoridades;
- `product/CHARTER.md`: identidade, limites, proteções de interação e condição de revisão do repo separado;
- `research/research-initial-definitions.md`: contexto mestre informacional, restrições confirmadas, baseline e
  lacunas, sem método ou autoridade de implementação;
- `research/research-plan.md`: perguntas do programa mestre, prioridades, padrões de evidência, outputs, stopping
  conditions, síntese e handoffs;
- `authority/AUTHORITY-MODEL.md`: precedência, estados epistêmicos, regras de mutação e default-deny;
- `authority/DEFINITIONS.md`: somente termos já necessários para interpretar os outros arquivos;
- `decisions/0001-create-separate-repository.md`: decisão do owner, o que a limpeza protege e condição de revisita;
- `policies/DEPENDENCIES-AND-PROVENANCE.md`: política de referência, snapshot, import e execução externa;
- `manifests/sources.yaml`: fontes fundadoras com pins reproduzíveis;
- `manifests/dependencies.yaml`: dependências executáveis, inicialmente vazio ou contendo apenas ferramentas que
  a validação realmente executar;
- `contracts/execution-link.md`: contrato documental mínimo para ligar trabalho local a execução externa;
- `.gitignore`: apenas resíduos observados ou deliberadamente externos, sem esconder evidência aceita.

Não preparar Universal Governance Baseline, constitution packs, vault, inventário global, schemas não consumidos,
shims `.agents/.claude/.codex`, código, CI ou layout de conhecimento herdado. Diretórios vazios também não são
fundação: `research/investigations/`, `research/findings/` e novos decision records surgem com o primeiro consumidor.

### G1 — Review do pacote fundador

Fazer review read-only independente antes da criação. O review precisa responder, com finding por falha:

1. O charter preserva o Superinterviewer como interface e parceiro intelectual, e não como framework genérico?
2. Contexto, plano, investigação, finding, decisão e execução têm owners e precedência distintos?
3. Uma descoberta pode contradizer o frame sem alterar o charter até uma decisão explícita?
4. Toda afirmação fundadora externa tem locator e pin reproduzível, sem autoridade transitiva implícita?
5. Cada arquivo e termo tem consumidor imediato? O que não tiver deve ser removido.
6. Nenhuma referência a SWI, DomainSpec, Arcanum, Lean ou ao orchestrator foi convertida em import amplo?
7. O contrato de execução registra lineage sem exigir provider, hooks, journal, scheduler, database ou ledger?
8. O pacote permanece portátil em clone limpo e não contém caminho local como locator canônico?

G1 fecha somente quando findings bloqueantes forem corrigidos e o owner aceitar explicitamente `CHARTER`,
`AUTHORITY-MODEL`, a decisão `0001` e o programa mestre. Artefatos aceitos recebem estado e data; propostas
continuam não binding. Review não equivale a criação.

### G2 — Autorizar a criação

Antes de qualquer mutação fora deste repo, registrar uma autorização que resolva:

- nome e caminho local exatos, ambos fora de `cyberalchemy-orchestrator`;
- URL/owner do remoto, visibilidade e se o remoto será criado agora ou depois;
- licença ou decisão explícita de permanecer sem licença por enquanto;
- branch padrão, signer/autor do commit e política de proteção inicial;
- digest do `TRANSFER-MANIFEST.md` aprovado.

Ausência de qualquer item impede apenas a ação dependente: por exemplo, é possível autorizar repo local sem
autorizar remoto público. Não inferir defaults de `goldenquill`, `ui-evolution-studio`, `mint` ou DomainSpec.

### C1 — Criar o repo local

Sob G2, verificar que o destino resolvido é novo ou vazio, inicializar Git com a branch aprovada e instalar
somente os destinos listados no transfer manifest. Preservar os arquivos fundadores como conteúdo local do
Superinterviewer; preservar as fontes antecedentes apenas como referências/snapshots de proveniência, não como
árvore copiada de framework.

Criar um registro de bootstrap em `decisions/0002-bootstrap-receipt.md` com: autorização, digest do pacote,
arquivos emitidos, comandos materiais, resultado das validações, desvios e commit inicial. Esse registro é
proveniência de criação, não prova de correção do produto.

O primeiro commit ocorre somente após V1–V6 abaixo. Provisionamento do remoto e primeiro push são outra ação
externa: executá-los apenas se G2 os autorizou expressamente e registrar URL e commit observados no receipt.

### G3 — Aceitar a fundação criada

O owner compara o repo criado com o manifest aprovado e aceita ou rejeita o bootstrap. Um repo que inicializa
mas falha em autoridade, proveniência ou portabilidade não passa G3. Correções de scaffold podem ocorrer antes
do aceite; qualquer ampliação de escopo retorna a G1/G2.

### H1 — Entregar o programa mestre

Depois de G3, o repositório novo passa a ser o owner canônico do charter e do programa. O handoff deve:

1. apontar o corpus de bootstrap no orchestrator como antecedente pinado, não como authority ativa;
2. registrar quais perguntas, lacunas e decisões foram transferidas, rejeitadas ou deixadas no antecedente;
3. abrir a primeira investigação somente com `research-initial-definitions` próprio, escopo/exclusões e relação
   explícita com uma pergunta do programa mestre;
4. exigir que findings citem o que suportam e que uma síntese/decision record faça qualquer promoção;
5. manter o orchestrator, SWI, DomainSpec, Arcanum e formalizações como fontes ou providers externos até um gate
   de dependência específico.

O handoff termina quando a localização canônica do programa é inequívoca e não há duas cópias editáveis se
apresentando como master. O antecedente deve receber um ponteiro de encerramento para o repo/commit novo; não
deve continuar sendo atualizado como programa paralelo.

### G4 — Gate separado para qualquer implementação

Bootstrap e handoff não autorizam código de produto. A primeira implementação requer uma proposta que nomeie:
incerteza discriminada; alternativas reais; intervenção/observação mínima; evidência que favorece ou refuta cada
alternativa; critérios de aceitação e parada; escolhas arquiteturais deliberadamente não decididas; e forma de
descartar o protótipo. O aceite de um resultado exige decisão local; output, receipt, teste verde ou prova formal
isoladamente não promovem uma hipótese a product authority.

## Pins de proveniência e dependência

### Fontes

Cada entrada de `sources.yaml` deve ter, no mínimo: `id`, `role`, `repository_url`, `revision`, `worktree_state`,
`path`, `selector`, `sha256`, `captured_at`, `license_or_access` e `snapshot_path` quando necessário.

- Fonte tracked e clean: `repository_url + commit + path + selector + digest`.
- Fonte dirty ou untracked: não alegar que `HEAD` a contém; registrar o commit-base, estado, digest e incluir no
  pacote um snapshot identificável, ou primeiro publicá-la em commit durável e então atualizar o pin.
- Fonte sem locator durável/licenciado: snapshot mínimo permitido, com origem e limites; caso contrário, apenas
  registrar a claim como não reproduzível.
- Caminho sibling/local pode ser `observed_at`, nunca locator canônico clone-safe.

No momento deste plano, o corpus `research/superinterviewer-repository-bootstrap/` está untracked em relação ao
`HEAD c88f30740a177935158cf4431cf9c584b5089afc`; portanto esse commit não fixa seu conteúdo. Baseline observado
para conferência, a ser recalculado quando o pacote for congelado:

| fonte | SHA-256 observado |
|---|---|
| `research-initial-definitions.md` | `C806154DE4BF700270B4B7A5B79ED5857803E765738FD3C50B3EB366AC6776DF` |
| Robot-Talks `findings.md` | `8F322947CBDA814E0E9DB450EF9ECE00EB3AD6B292829D8EE29322BC829678D0` |
| report `01-product-research-authority.md` | `E4547AB0674F81DF4D1A5CA3AFEF5CA24CA19BCACC16D6BFFEF53F14F1748F37` |
| report `02-authority-scaffold.md` | `5249212FF4A607F5FBDF23995950509CD34B4306BEE287E6515126F8B84BF63C` |
| report `03-integration-execution-boundary.md` | `BD73D25337667F8019B12DA1467315ACB42CAD1625ABD6FA336E4ECE84CA29D4` |

### Dependências

`dependencies.yaml` representa somente algo necessário para operar ou validar o repo. Cada entrada exige:
`id`, `concern`, `provider`, `interface_or_capability`, `version_or_revision`, `artifact_digest`, `compatibility`,
`optional`, `allowed_surface` e `status`.

No dia zero, SWI, DomainSpec, `domainspec-core`, Lean e o orchestrator são `reference-only`, não dependências.
Arcanum só entra como dependência se uma validação ou workflow aprovado realmente o invocar; source, skill
instalada, adapter profile e schema de observabilidade recebem pins separados. É default-deny para submodules
amplos, junctions/symlinks locais, copied trees, imports transitivos e bundles de skills. Uma exceção precisa de
concern, consumidor, superfície mínima, pin, licença, remoção testável e decision record.

### Execution link mínimo

O contrato deve representar: artefato/pergunta local; executor, profile e versão; IDs externos de dispatch/run/
session quando existirem; inputs e outputs exatos com digests; timestamps; estado da execução; e decisão local de
aceitação (`unreviewed`, `accepted`, `rejected` ou `superseded`). IDs e receipts externos nunca substituem essa
decisão. O contrato não presume que SWI ou ACI já ofereçam uma interface estável.

## Autoridade mínima

O `AUTHORITY-MODEL.md` deve declarar, no mínimo:

1. uma decisão aceita do owner é binding dentro do seu escopo e pode ser superseded apenas por nova decisão;
2. o charter aceito governa identidade e proteções do produto;
3. o master initial definitions é contexto informacional e governa escopo/linhagem, não método ou verdade;
4. o research plan governa sequência, padrões de evidência e stopping conditions, sem sobrepor charter/decisões;
5. initial definitions de branch delimitam perguntas; findings suportam claims; nenhum dos dois decide sozinho;
6. receipts, sinais, inventários e resultados de ferramentas são evidência gerada, não autoridade aceita;
7. conteúdo `DRAFT` ou `PROPOSED` não é binding; ausência de autoridade é default-deny, não permissão implícita;
8. mudanças de precedência, status ou produto exigem decision record com fontes, impacto e supersession explícitos.

Não ratificar antecipadamente uma taxonomia universal de kinds. `DEFINITIONS.md` deve começar curto e crescer
somente quando ambiguidade observada afetar interpretação ou decisão.

## Validações antes do primeiro commit

- **V1 — Manifest:** todo arquivo instalado corresponde ao transfer manifest e ao digest aprovado; não há arquivo
  extra, ausente ou sobrescrito.
- **V2 — Proveniência:** todo source pin resolve ou possui snapshot justificado; nenhum arquivo untracked é
  representado como pertencente a um commit; seletores e digests são verificáveis.
- **V3 — Portabilidade:** um clone/cópia em diretório temporário não depende de path absoluto, junction, symlink
  local ou sibling checkout para ler suas autoridades.
- **V4 — Autoridade:** checagem de links e estados confirma que charter, plano, findings e decisões não se
  sobrepõem; uma proposal não aparece como binding.
- **V5 — Boundary:** busca por submodules, broad imports, copied frameworks, hooks obrigatórios e credenciais
  confirma que nenhum entrou silenciosamente; `git diff --no-index` pode comparar o pacote e os destinos.
- **V6 — Higiene Git:** branch, `.gitignore`, licença decidida, line endings, arquivos secretos, status e diff do
  commit são revisados; o bootstrap é repetível em destino scratch sem clobber.
- **V7 — Pós-commit:** em clone limpo do commit inicial, repetir V1–V5 e verificar que README resolve o mapa de
  autoridades e que o programa mestre pode abrir uma investigação sem instalar runtime.
- **V8 — Remoto, se autorizado:** URL, visibilidade, default branch e commit remoto observado coincidem com G2;
  nenhum push ocorre como efeito colateral de C1.

## Critério final de conclusão

O bootstrap está concluído somente com G3 aceito, V1–V7 verdes, V8 quando aplicável, receipt de criação e handoff
H1 sem dupla authority ativa. Isso entrega um repositório de produto e pesquisa utilizável. Não entrega um runtime,
uma plataforma de agentes, uma ontologia completa nem o Superinterviewer implementado.
