---
tags: [ui, ontology, vault, architecture]
node_type: constitution
is_session: true
layer: ontology, application
nature: explanatory, reference
status: active
created: 2026-07-20
timestamp: 2026-07-20T21:24:11-03:00
expires: 2026-09-18
conversation_id: unknown
decisions_made: true
contradictions_found: true
specs_updated: [vault/constitution/frontend-constitution.md, vault/ontology-conventions.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Estabelece a lei de classificação do próprio vault (ontology-conventions.md) e reescreve a constituição primária de UI (CONST-FE) como regras-hipótese falsificáveis, tornando ambos infraestrutura load-bearing a que todo nó e superfície futura terá de se conformar."
---

# CONST-FE reconstruída como regras-hipótese + ontology-conventions no vault

## Summary

A sessão auditou e depois reconstruiu a constituição de frontend (CONST-FE). Começou com o
usuário pegando dois defeitos no Purpose: `dispatch_type: 6` fora usado como contagem escalar
quando `dispatch_type` é um enum categórico (research|code|review|…), e o enquadramento
sombra⊕estrutura vazara o domínio de dispatch de subagentes para dentro de uma constituição de
UI genérica; ambos foram corrigidos e o Purpose reescrito genérico e ancorado nas regras. Por
direção do usuário, CONST-FE foi reestruturada no layout do frontend-constitution do ZefraHub —
Objective, Index, regras como headings `### FE-n` —, traduzida para inglês, e ganhou uma seção
Connections-and-Falsifiability que liga cada constituição à hipótese de que ela promove. O
`ontology-conventions.md` do ZefraHub foi então portado para `vault/ontology-conventions.md`,
adaptado e não copiado: o sistema de 7 labels, o par de confiança veracidade⊥convicção e o
princípio de ortogonalidade (informação-mútua-zero) foram mantidos, enquanto os specifics de
domínio do ZefraHub foram re-aterrados neste repo e amarrados ao lever nativo
`resíduo = sombra ⊕ estrutura`. Uma divergência deliberada foi codificada nos dois docs: o
ZefraHub omite veracidade/convicção para constituições, mas aqui cada regra é uma hipótese
falsificável que carrega os dois labels inline mais uma linha "Falsified if", a ser promovida a
premissa quando sobreviver ao uso real. As regras FE-1..FE-9 foram reescritas nessa forma. Por
fim o usuário fixou o princípio "build as law, test as bet" — a arquitetura tem de permitir
adicionar, remover e medir cada regra de forma barata —, que virou FE-10: toda regra é uma
unidade ablável e instrumentada presa a um `data-*-id` estável que é ao mesmo tempo âncora de
explicação (FE-9), chave de score do harness (FE-8) e handle de ablação — o princípio de
ortogonalidade aplicado a intervenções, não a labels.

## Contradictions

- questions `vault/constitution/frontend-constitution.md` (FE-5) — a própria regra admite que seu
  falseador é fraco demais para funcionar como teste de hipótese ("closer to axiom than
  hypothesis"), em tensão com a convenção hipótese-por-regra (veracidade/convicção/"Falsified if")
  que `vault/ontology-conventions.md` prescreve; FE-5 é candidata a promoção antecipada a
  axioma/premissa em vez de seguir como hipótese.

## Open questions

- Se os sinais de **densidade** e **fadiga cognitiva** são separáveis em princípio por regra, ou
  tão emaranhados que os deltas de ablação dos toggles de FE-10 ficam ininterpretáveis — a
  conjectura não-testada em que todo o programa de medição FE-8/FE-10 se apoia.

## Next steps

1. Extrair a tese **densidade ⊥ fadiga** para `vault/hypothesis/` (espelhando HYP-ORCH-NOISE:
   claim, matriz 2×2, collapse-tests) para que a aresta `promotes-from` de CONST-FE aponte para
   um nó real, não só FRAMINGS F1.

## Recommendation

A pedra angular é o **harness de fitness de UI** — a tool pendente de FE-8, agora concretizada por
FE-10 como um registry por-regra `{id, toggle, metric}` cuja ablação executa o "Falsified if" de
cada regra. FE-10 fixa o contrato exato a construir (uma flag + um emissor de métrica no
`data-*-id` estável), o que licencia começar o scaffold — mas faça antes a extração barata do doc
de hipótese (Next step 1) para desbloquear o `promotes-from`. Se o harness consegue de fato
separar densidade de fadiga é um palpite pendente da Open question; então construa o registry
primeiro e trate a separação da métrica como a primeira coisa a validar.

## Files touched

- vault/constitution/frontend-constitution.md
- vault/ontology-conventions.md
