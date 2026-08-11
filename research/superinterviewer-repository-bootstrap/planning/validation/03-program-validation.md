# Validação do programa de pesquisa — `research-plan.md`

## Initial verdict

**FAIL — superseded by the revalidation below**

O draft preserva o Superinterviewer como produto central, cobre suficientemente as perguntas
essenciais sem reproduzir os 19 capítulos do Prompt-Mestre, apresenta workstreams, dependências e
ondas coerentes e mantém boa separação entre decisão, hipótese, evidência e analogia. O FAIL decorre
de dois findings MAJOR corrigíveis localmente: ordem ambígua do gate de protótipo e ausência do
contrato mínimo pelo qual branches retornam ao programa.

Após as duas correções MAJOR abaixo, o plano pode passar esta validação sem reestruturação ampla.

## Cobertura

| critério | resultado | verificação |
|---|---|---|
| Superinterviewer como produto central | PASS | A pergunta-mãe, WS1–WS6 e os protected questions mantêm o produto humano no centro; WS7 e WS8 permanecem subordinados. |
| Perguntas essenciais | PASS | Intenção, comparadores, movimentos, sinais/probes/lentes, estado, métricas, autonomia, localidade, resíduos, execução e formalização aparecem como perguntas refutáveis. Não é necessário copiar a estrutura integral do Prompt-Mestre. |
| Dependências e ondas | PASS com correção | O grafo e Waves 0–4 têm precedência razoável; a redação de Wave 3 precisa obedecer inequivocamente ao gate B4. |
| Retorno de branches | FAIL | O plano exige um promotion path e promete criar um return contract, mas ainda não define o retorno mínimo de initial definitions e findings. |
| Decisão × hipótese × analogia | PASS | Confirmed decisions estão separadas; completude dos movimentos permanece aberta; formalização só é promovida por consequência e, sem ela, permanece analogia. |
| Fidelidade às decisões aceitas | PASS com correção | Separação de autoridades, `mint` proporcional, SWI peer/provider, pins estreitos e gate pré-implementação estão preservados; a ambiguidade de Wave 3 deve ser removida. |

## Findings por severidade

### CRITICAL

Nenhum.

### MAJOR

#### M1 — Wave 3 admite leitura de protótipo anterior ao gate que deveria autorizá-lo

**Evidência no draft:**

> “Prefer replay, blinded coding, Wizard-of-Oz, manual comparison, and reversible prototypes.”

Logo depois:

> “Gate B4 authorizes one bounded prototype only when it names a discriminating uncertainty...”

O plano também confirma que “Product implementation requires a prior discriminating research or
experiment gate”. Assim, “reversible prototypes” dentro da Wave 3, antes da passagem por B4, cria
duas ordens possíveis. A leitura permissiva contradiz a decisão aceita e a tensão T3 dos findings:
um protótipo só pode existir depois de declarar a incerteza, a evidência e os limites que ele não
pode resolver acidentalmente.

**Correção mínima:** retirar “and reversible prototypes” da lista pré-gate ou substituí-la por
“non-executable interaction mockups”. Acrescentar uma frase após B4: “Only after B4 may the bounded
prototype be created or run.” Não alterar o restante da Wave 3.

#### M2 — O retorno de branches é adiado, não definido pelo plano atual

**Evidência no draft:**

> “A research branch enters the plan only when it declares [...] output authority and promotion
> path.”

e, entre os outputs futuros de Wave 0:

> “branch opening/return contract”

O texto define entrada, authorities e revisão do plano, mas não estabelece o pacote mínimo de
retorno nem diferencia operacionalmente como scoped initial definitions e findings afetam o
programa. Isso deixa uma função declarada no propósito — conectar pesquisa a decisões — dependente
de um contrato ainda por criar. A separação documental está correta, mas a reintegração ainda não é
executável como regra de programa.

**Correção mínima:** adicionar um único parágrafo ou lista com estas três regras:

1. scoped initial definitions retornam refinamentos de pergunta, constraints e gaps como delta de
   contexto; não promovem claims nem alteram o charter;
2. findings retornam resposta citada, contraevidência, negativa tipada, incerteza restante, impacto
   em dependências/resíduos e a decisão que podem informar;
3. findings atualizam matriz de evidências e resíduos imediatamente, mas apenas um decision record
   aceita, rejeita, reenquadra ou altera autoridade vinculante.

Não é necessário definir formato físico, runtime ou lifecycle de dispatch.

### MINOR

#### m1 — “Planning inputs are evidence” enfraquece a disciplina epistêmica

**Evidência no draft:**

> “The planning inputs are evidence and critique, not parallel plan authorities.”

Inputs de planejamento podem conter evidência, interpretação e proposta; não são automaticamente
evidência das claims de produto. A frase pode reclassificar recomendações como suporte empírico,
apesar da boa separação feita no restante do plano.

**Correção mínima:** substituir por: “The planning inputs are planning basis and critique, not
parallel plan authorities; claims within them retain the epistemic status and source of their
underlying support.”

## Correção mínima consolidada

1. Tornar B4 inequivocamente anterior a qualquer protótipo de produto.
2. Incluir o contrato semântico mínimo de retorno de initial definitions, findings e decisions.
3. Reservar “evidence” para suporte que carrega fonte e status, não para todo input de planejamento.

Essas correções não exigem copiar capítulos do Prompt-Mestre, alterar os nove workstreams, mudar o
grafo, redesenhar as ondas ou detalhar scaffold/runtime.

## Revalidation — M1, M2 e m1

**PASS**

Escopo desta revalidação: somente as três correções solicitadas. Nenhum outro aspecto do plano foi
reaberto.

| finding | resultado | evidência no plano corrigido |
|---|---|---|
| M1 — protótipo antes do gate | RESOLVED | Wave 3 agora limita o trabalho pré-gate a “non-executable interaction mockups before the prototype gate” e declara: “Only after B4 may that bounded product prototype be created or run.” |
| M2 — retorno de branches indefinido | RESOLVED | A nova seção “Branch return contract” define o pacote de retorno e separa o efeito de scoped initial definitions, findings e decision records. |
| m1 — planning inputs chamados de evidence | RESOLVED | A seção final agora diz: “The planning inputs are planning basis and critique, not parallel plan authorities. Claims within them retain the epistemic status and source of their underlying support.” |

### Current verdict

**PASS** — M1, M2 e m1 foram corrigidos sem introduzir, no escopo observado, nova ambiguidade sobre
o gate de protótipo, a promoção de resultados de branches ou o status epistêmico dos inputs de
planejamento.
