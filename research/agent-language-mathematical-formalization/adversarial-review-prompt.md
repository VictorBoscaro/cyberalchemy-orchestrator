---
tags: [agents, architecture, lean, formalization, review-prompt]
node_type: review-prompt
status: draft
version: 0.3.0
last_updated: 2026-07-25
target_document: docs/architecture/agent-language-system-view.md
target_version: 0.8.1
target_sha256: 32c2d8d2fa612ba4909e0ddf6f8390836ea40a006323caa0c5faeb46686a0479
---

# Adversarial Review Prompt

Faça uma revisão crítica, source-first e adversarial de **“A Composable Language for Governed
Agent Work”**, usando exclusivamente esta revisão congelada:

- caminho: `docs/architecture/agent-language-system-view.md`;
- versão: `0.8.1`;
- SHA-256: `32c2d8d2fa612ba4909e0ddf6f8390836ea40a006323caa0c5faeb46686a0479`.

Confirme o hash antes da análise. Se ele divergir, interrompa e peça que o alvo seja novamente
congelado; não misture revisões. Leia o documento inteiro. Material externo pode fornecer
contramodelos ou precedentes, mas não pode ser atribuído ao documento.

O alvo é uma proposta de pesquisa, não uma arquitetura aceita. Kernel, metacontrato, tipos
dependentes e Lean permanecem hipóteses. “Solução mais simples” significa a alternativa que
satisfaz uma obrigação e seu limiar de risco com a menor combinação declarada de:

- semântica nova;
- base confiável;
- código e infraestrutura;
- custo de evolução e migração;
- proof plumbing;
- operação e revisão humana.

Declare pressupostos e pesos quando esses critérios apontarem para soluções diferentes.

## Regras de evidência

Todo achado sobre o documento deve conter:

1. ID da obrigação relacionada;
2. seção e citação curta, literal;
3. classificação como `explícito`, `inferido` ou `ausente`;
4. interpretação e risco;
5. contramodelo ou tentativa de refutação;
6. correção mínima;
7. confiança.

Uma crítica sem citação do alvo pode ser uma hipótese do revisor, mas não um achado documental.
Não trate os resultados da pesquisa anterior nem este prompt como decisões do produto.

Quando o alvo atribuir prova, verificação ou evidência a outra fonte, registre:

| Claim | Fonte indicada | Versão/digest vinculados no alvo | Verificável no corpus congelado | Status |
|---|---|---|---|---|

Uma referência externa não congelada preserva a atribuição feita pelo alvo, mas não permite ao
revisor promover seu conteúdo a prova ou evidência confirmada.

# Fase A — revisão do documento

## 1. Reconstrução e ledger de obrigações

Antes de avaliar soluções, reconstrua do alvo:

- problema central e falhas concretas a impedir;
- distinções e compromissos semânticos;
- decisões abertas;
- propriedades globais e locais;
- termos ambíguos.

Não introduza ainda tipos dependentes, Lean ou `kernel-of-kernels`.

A partir dessa reconstrução, crie um ledger de **5 a 7 obrigações**, `OB-01` a no máximo `OB-07`.
Cada obrigação deve registrar:

| ID | Obrigação | Falha a impedir | Evidência no alvo | Escopo | Critério observável | Origem do critério |
|---|---|---|---|---|---|---|

Priorize obrigações por impacto, probabilidade e dependência arquitetural. Todas as análises
seguintes devem reutilizar esses IDs. Questões fora do ledger vão para `Open Questions`; não
expanda o ledger durante a execução sem justificar a substituição de um item.

Classifique a origem de cada critério como `explícito`, `inferido` ou `RH-*`. Um critério criado
pelo revisor não pode ser apresentado como deficiência documental.

## 2. Auditoria epistemológica

Teste se o documento mantém separadas:

\[
\text{declaração}
\neq
\text{bem-formação}
\neq
\text{prova}
\neq
\text{correspondência com o produto}
\neq
\text{evidência de runtime}
\neq
\text{autoridade de execução}.
\]

Teste primeiro as cinco fronteiras adjacentes da sequência acima. Use no máximo um contramodelo
citado por fronteira. Uma fronteira está coberta quando recebe um achado ou é classificada
`ausente`; examine colapsos não adjacentes somente quando houver evidência literal que os motive.

## 3. Gate de grounding e auditoria do kernel

Antes de analisar a decomposição formal, preencha:

| Símbolo | Referente demonstrável no alvo | Evidência | Status |
|---|---|---|---|
| \(M\): metacontrato |  |  | `sustentado` / `parcial` / `não sustentado` / `não aplicável` |
| \(G\): leis globais |  |  |  |
| \(K_i\): contrato ou kernel local |  |  |  |
| \(Q\): checker |  |  |  |
| \(C_{ij}\): evidência de composição |  |  |  |
| \(B_0\): bootstrap/base de confiança |  |  |  |

Não reifique símbolos `não sustentados` ou `não aplicáveis`. Para os demais, pergunte:

- qual `OB-*` atendem e qual problema resolvem;
- se são linguagem, dado, regra, programa, prova, evidência ou autoridade;
- o que se perde ao removê-los;
- se podem ser derivados, combinados ou descentralizados;
- se pertencem à base confiável;
- qual alternativa mais simples atende à mesma obrigação.

Compare, sem presumir exclusividade: nenhum kernel central, contrato comum mínimo, kernel universal,
kernels especializados, microkernel operacional, protocolo de interoperabilidade, metacontrato,
checker comum ou especializado e composição governada entre contratos. Julgue também se
`kernel-of-kernels` tem referente claro ou agrupa responsabilidades distintas.

## 4. Argumentos adversarialmente opostos

Produza duas análises **adversarialmente opostas**, não chamadas de independentes quando forem
produzidas pelo mesmo revisor. Revele pressupostos compartilhados.

### Contestação forte

Defenda que a formalização é prematura; schemas, grafos e validators comuns preservam as
distinções; o metacontrato replica a complexidade; `kernel-of-kernels` não tem referente claro; a
analogia com Lean cria falsa segurança; e o custo não evita falhas relevantes.

### Defesa forte

Defenda que os colapsos são reais; relações e evidências tipadas aumentam auditabilidade; kernels
locais evitam ontologia universal prematura; um checker pequeno pode reduzir a base confiável
quando seu escopo e implementação realmente forem menores; certas autoridades
implícitas podem ser estruturalmente eliminadas; e certificados ainda são úteis quando separados
do enforcement físico.

Para cada argumento, cite o alvo, declare pressupostos, dê contraexemplo, confiança e condição de
rejeição. Não produza consenso nesta seção. Independência epistemológica, se desejada, exige
revisores separados fora deste prompt.

## 5. Matriz de mecanismos

Para cada `OB-*`, compare apenas mecanismos plausíveis entre:

- schema e constraints de banco;
- validator;
- máquina de estados;
- policy engine;
- grafo tipado;
- sistema de tipos simples;
- tipos dependentes;
- model checking;
- property testing;
- revisão humana;
- combinações.

| ID | Falha | Mínimo sob os critérios declarados | Ganho de mecanismo mais forte | Custo/TCB | Evidência faltante |
|---|---|---|---|---|---|

Não presuma que tipos dependentes sejam superiores. Uma solução mínima deve nomear o risco residual
e o pressuposto sob o qual permanece suficiente.

## 6. Tipos dependentes e a aposta Lean

Somente após a matriz, avalie famílias indexadas como:

```lean
Obj : Kind → Type
Kernel : Scope → Version → Type
WorkItem : WorkState → Type
RelationSig : Kind → Kind → Type
DirectEdge : RelationSig a b → Obj a → Obj b → Type
```

O pseudocódigo não é proposta aceita. Para cada índice, avalie estabilidade, decidibilidade,
capacidade discriminativa, evolução, necessidade em runtime, proof plumbing, elaboração e
alternativa mais simples. Tipos dependentes só vencem quando tornam uma invariante crítica
inconstruível ou substancialmente mais segura por custo justificável.

Trate Lean como **aposta favorecida, não decisão**. O alvo estabelece sua relevância contextual,
mas não uma restrição confirmada nem um papel selecionado. A aposta é plausível apenas na medida em
que obrigações sustentadas pelo ledger sejam puras, finitas e propícias a contramodelos ou provas.

Registre:

- qual `OB-*` Lean poderia atender melhor;
- evidência que fortaleceria a aposta: cone pequeno compilado, auditoria sem `sorry`/axiomas
  indevidos, contramodelos úteis, rechecagem independente, correspondência revisada e conexão
  verificável com validator ou checker;
- evidência que a rebaixaria ou falsificaria: nenhum ganho crítico sobre schema/testes, índices
  instáveis, proof plumbing dominante, TCB maior que o benefício, impossibilidade de manter
  correspondência ou ausência de falhas reais detectadas;
- custo de oportunidade e ponto de parada.

Se Lean permanecer `testar` ou `aposta favorecida`, a Fase B deve incluir `EX-L-01`: uma aposta
pré-registrada que nomeie uma única `OB-*`, um cone Lean finito, o contramodelo ou teorema-alvo, um
baseline em schema/validator/testes, teto de tempo e dependências, e critérios explícitos para
`favorecer` ou `rebaixar` Lean.

Mantenha separadas quatro decisões:

1. usar conceitos de teoria dos tipos dependentes;
2. construir um type system para a linguagem do produto;
3. formalizar partes do modelo em Lean;
4. usar artefatos verificados por Lean em processos do produto.

Não derive uma da outra. Compare Lean como notação, ambiente experimental, verificador de
propriedades puras, gerador de validators, checker independente, produtor de evidência governada ou
sem papel no runtime.

## 7. Casos discriminantes

Use **exatamente quatro casos** e vincule cada um a `OB-*`:

1. **Relações distintas:** `generated-by`, `authorized-by`, `contained-in` e `reviewed-by` entre os
   mesmos objetos; teste o que `parent_id` perde.
2. **Projeção sem autoridade:** `DispatchCandidate` aparece `ready`, mas não há confirmação aceita.
3. **Contratos locais:** documentos permitem herança de conteúdo; execução proíbe herança
   automática de capabilities.
4. **Caso favorável a mecanismos simples:** parta de uma propriedade local, estável e decidível
   candidata a proteção por schema/constraint/validator convencional; teste tanto a suficiência
   desse baseline quanto uma variação inter-registro, evolutiva ou com efeito que poderia exigir
   escalada.

Em cada caso compare schema/validators, grafo tipado, tipos dependentes e enforcement de runtime.
Use uma `OB-*` primária por caso, referências cruzadas para a matriz e justificativas curtas, sem
repetir a análise completa. Cada caso deve declarar o resultado que favorece o mecanismo simples e
a mudança no cenário que justificaria escalar.

## 8. Disciplina formal

Classifique qualquer trecho Lean como `pseudocódigo conceitual`, `código não verificado`, `código
compilado` ou `código compilado e auditado`. Não use axiomas, `sorry` ou definições vazias para
simular a propriedade investigada.

Não chame um grafo de categoria sem identidades, composição, fechamento e coerência. Não introduza
matemática avançada sem nomear o `OB-*` que uma estrutura mais simples falhou em satisfazer.
Separe sempre model soundness, correspondência, evidência de runtime e autoridade.

## 9. Síntese da Fase A

Não escolha uma arquitetura final. Classifique separadamente:

- `DP-*`: proposta feita pelo documento;
- `RH-*`: hipótese introduzida pelo revisor;
- `NP-*`: candidata a decisão normativa de produto, pendente de autoridade nomeada.

Para cada item, use `manter`, `simplificar`, `reformular`, `rejeitar`, `testar` ou `deixar aberta`,
com evidência e `OB-*`. Separe consenso forte, consenso provisório, desacordo persistente, questão
empiricamente testável e decisão normativa. Priorize por impacto, probabilidade, reversibilidade,
custo e dependência.

Para cada `NP-*`, registre a autoridade ausente e o estado `proposta`, `aceita` ou `autorizada`;
não trate uma candidata como decisão já tomada.

# Fase B — experimentos opcionais

Execute esta fase somente se a Fase A deixar hipóteses `RH-*` **empíricas**, prioritárias e
discriminantes. Questões conceituais, provas matemáticas e decisões normativas não são convertidas
artificialmente em experimentos.

Proponha de **zero a três** experimentos `EX-*`. Para cada um, registre:

- `RH-*` e `OB-*` correspondentes;
- hipótese pré-registrada e alternativas;
- implementação mínima e caso de teste;
- resultado que favorece cada alternativa;
- resultado que falsifica ou rebaixa a hipótese;
- custo, limite e aprendizado esperado.

Experimentos são propostas posteriores à revisão, não achados do documento nem decisões do
produto. Não proponha formalização ampla antes desses testes.

## Entrega

Entregue, nesta ordem:

1. identidade e hash confirmado do alvo;
2. ledger `OB-*`;
3. achados documentais citados;
4. gate de grounding;
5. argumentos opostos;
6. matriz de mecanismos;
7. avaliação de tipos dependentes e da aposta Lean;
8. quatro casos discriminantes;
9. síntese tipada (`DP-*`, `RH-*`, `NP-*`);
10. Fase B, se aplicável;
11. `Open Questions`, preservando também itens rejeitados, adiados ou fora de escopo.
