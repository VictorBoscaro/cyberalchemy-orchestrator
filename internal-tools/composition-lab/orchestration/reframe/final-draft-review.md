# Review — Composition Lab reframe drafts

## Coverage

Corpus integral revisado sob quatro lentes: fidelidade de escopo; conformidade com
`research-initial-definitions`; independência epistemológica; autoridade, referências e
contradições. Todos os sete alvos foram lidos. Links Markdown relativos verificados: nenhum está
quebrado.

## Findings verificados

### 1. Propostas desenham a pesquisa antes da precondição informacional

- **Arquivos:** `orchestration/reframe/next-internal-research-proposal.md` e
  `orchestration/reframe/next-external-research-proposal.md`
- **Evidência:** ambas declaram “`research-initial-definitions.md` antes do desenho final do
  dispatch”, mas já especificam corpus/fontes, perspectivas, hipóteses, outputs e gates.
- **Severidade:** MAJOR
- **Fix exato:** criar e aceitar primeiro um `research-initial-definitions.md` próprio para cada
  trilha; somente depois reemitir estas propostas como desenho governado. Até lá, mudar
  `artifact_kind` para `research-advice`, declarar explicitamente que são pareceres pré-design e
  remover qualquer aparência de dispatch pronto para confirmação.

### 2. O programa afirma realização antes da pesquisa interna

- **Arquivo:** `research-program.md`
- **Evidência:** “Composição já participa do funcionamento do repositório” e “O repositório já
  compõe lentes”. O próprio programa ainda propõe investigar o que foi apenas alegado,
  configurado, realizado ou efetivo.
- **Severidade:** MAJOR
- **Fix exato:** substituir por “O repositório usa a linguagem e práticas candidatas de
  composição” e “O repositório trata como composição de lentes práticas de distribuição de
  perspectivas...; se e em que sentido elas realizam composição é questão do Caso 1”.

### 3. A definição inicial geral inclui prescrição metodológica

- **Arquivo:** `research/research-initial-definitions.md`
- **Evidência:** constraint: “The inquiry must proceed through research, explicit hypotheses, and
  experiments”. A skill de initial definitions proíbe métodos de pesquisa e planos.
- **Severidade:** MAJOR
- **Fix exato:** remover essa bullet do RID. Preservá-la em `research-program.md` como decisão de
  programa, fora da definição informacional.

### 4. O programa histórico ainda fala como plano executável

- **Arquivo:** `orchestration/milestone-1-strategy/04-integrated-program.md`
- **Evidência:** o banner diz “Histórico preservado”, porém o corpo mantém “O milestone será
  executado...” e vários gates/dispatches imperativos; “Seus contratos continuam úteis” não
  revoga autorização de modo inequívoco.
- **Severidade:** MAJOR
- **Fix exato:** acrescentar ao banner: “Este artefato está superseded e não autoriza execução;
  nenhuma onda, gate ou dispatch abaixo permanece ativo sem nova proposta e confirmação pelo
  programa atual.” Manter o restante como registro histórico.

## Verdict por artefato

| artefato | verdict | razão |
|---|---|---|
| `README.md` | KEEP | composição geral é o objeto; lentes são Caso 1; não autoriza arquitetura |
| `research/research-initial-definitions.md` | FIX | contém método proibido |
| `research-program.md` | FIX | duas afirmações excedem a evidência ainda não coletada |
| `next-internal-research-proposal.md` | FIX | desenho antecede o RID local obrigatório |
| `next-external-research-proposal.md` | FIX | desenho antecede o RID local obrigatório |
| RID histórico do inventário | KEEP | banner limita corretamente o artefato ao Caso 1 |
| programa integrado histórico | FIX | banner não revoga inequivocamente o plano imperativo |

## Independência interna/externa

KEEP. Os drafts exigem coleta separada, impedem reclassificação retroativa do corpus interno e
reservam a importação de conceitos para síntese posterior. Essa independência só é válida se os
dois RIDs e dispatches forem produzidos separadamente, sem findings cruzados como input durante a
coleta.

## Change requests

1. MAJOR — criar os dois RIDs antes de qualquer proposta governada ou reclassificar os drafts atuais
   como advice pré-design.
2. MAJOR — demover as duas alegações de composição já realizada em `research-program.md`.
3. MAJOR — retirar método do RID geral.
4. MAJOR — marcar o programa antigo como superseded e não autorizador de execução.

**Resultado:** FIX. Não há autorização de execução ou arquitetura nos drafts novos; porém o programa
histórico permanece operacionalmente ambíguo até a correção 4.

## Disposição das correções

As quatro change requests foram aplicadas em 2026-08-13:

1. os dois desenhos foram reclassificados como `research-advice` pré-design e subordinados à criação
   e aceitação de suas definições iniciais locais;
2. as alegações de realização no programa foram demovidas a linguagem e práticas candidatas;
3. a prescrição metodológica foi removida das definições iniciais gerais;
4. o programa histórico foi marcado como `superseded` e explicitamente não autorizador.

**Estado pós-disposição:** pronto para nova verificação; o verdict FIX acima descreve os drafts
anteriores às correções e não constitui autorização de execução.
