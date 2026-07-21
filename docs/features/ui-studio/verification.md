---
feature: ui-studio
title: Verificação de citações — README do UI Studio
status: complete
created: 2026-07-20
dispatch: 2026-07-20-ui-studio-readme-verify
verification: first-hand, paired (confirm + falsify)
---

# Verificação de citações — UI Studio README

> Retorno do dispatch de review **pareado** `2026-07-20-ui-studio-readme-verify`
> (ver [telemetry/agents/subagents-dispatch.yaml](../../../telemetry/agents/subagents-dispatch.yaml)).
> Dois auditores independentes leram **de 1ª-mão** o mesmo corpus de citações E-5…E-14 do
> [README.md](README.md), com **disposições opostas** (eixo anti-viés: *confirmação* vs
> *falsificação*), para o viés correlacionado cancelar. As correções foram aplicadas no README.

## Resultado consolidado

**As 10 citações (E-5…E-14) RESOLVEM de 1ª-mão. Nenhum FAIL.** As duas disposições
convergiram — apontaram exatamente as mesmas correções de caracterização, o que é o sinal
de que o par funcionou (um viés otimista sozinho não teria achado a inflação de E-11; um
falsificador sozinho poderia ter exagerado uma nuance de rótulo em FAIL).

| ID | Confirmador | Falsificador | Consolidado | Correção aplicada no README |
|----|-------------|--------------|-------------|------------------------------|
| E-5 | RESOLVES (models.ts L33-49,71-129) | RESOLVES | ✅ | — |
| E-6 | RESOLVES (run-cycle.ts L87-204) | RESOLVES | ✅ | — |
| E-7 | RESOLVES | RESOLVES | ✅ | categorias exatas: "Visual hierarchy", "Functionality"; evidência 30–80 palavras por nota |
| E-8 | RESOLVES (studio.ts L267/281; http-routes L231-357) | RESOLVES | ✅ | — |
| E-9 | RESOLVES (api.ts L59-60) | RESOLVES | ✅ | — |
| E-10 | RESOLVES | RESOLVES | ✅ | "Genetic Control Center" = `<title>`; H1 = "Genetic Platform"; ~19 `gen_*.html` |
| E-11 | RESOLVES **com ressalva** | **PARTIAL** (inflada) | ✅ **corrigida** | material está na subseção *UX-constraint fitness* **[DEFERRED]** ~L171-200, **não** no §3 (Scope); "honesty rule" = honest-diff mandate (`DiffSummaryHonest`), não cláusula titulada; os dois `SPEC.md` são byte-idênticos |
| E-12 | RESOLVES (L394/243/414) | RESOLVES | ✅ | nomes de superfície são paráfrase ("cockpit", "Fleet Telemetry"), não verbatim |
| E-13 | RESOLVES (schema.sql L6-27; log.sh L3,41-93) | RESOLVES | ✅ | — |
| E-14 | RESOLVES (openclaw.mjs L78,143; server.mjs L8,262-268) | RESOLVES | ✅ | path bare, caracterização composta correta |

## A única citação inflada — E-11

Ambos os auditores pegaram: o README atribuía o par hard-gate/soft-gradient + "honesty
rule" ao **§3** do `SPEC.md`. De fato:

- **§3 é a seção de Scope** ("L0→L2"). O material de fitness (hard gate descarta L180;
  soft gradient pontua-nunca-descarta L183; ML2 fitness L190; OQ-5 L200) vive numa
  **subseção posterior marcada `[DEFERRED]`** (~L171-200).
- **"honesty rule" não existe como cláusula titulada.** O conceito é o **honest-diff
  mandate**: os counts de diff derivam do before/after real, nunca do `changeType`
  declarado (`DiffSummaryHonest`, em §2b/§4/§5).

**Efeito colateral útil:** que a camada de fitness esteja literalmente `[DEFERRED]` no
studio é **confirmação de 1ª-mão** da decisão §6.5 do README (substrato antes do engine) —
some ao newspaper (P0) e ao OQ-5 aberto para dar as 3× que sustentam "o autônomo não paga
primeiro".

## Nuances de rótulo (não-bloqueantes, aplicadas por precisão)

- **E-7:** categoria #2 é "Visual hierarchy" (não "Hierarchy"), #4 é "Functionality" (não "Function").
- **E-10:** "Genetic Control Center" é o nome do `<title>`/descrição; o H1 na página diz "Genetic Platform".
- **E-12:** "Harness Cockpit"/"Agent Fleet Telemetry" são paráfrases de "cockpit humano" e "Fleet Telemetry".
- **E-11:** os dois caminhos `SPEC.md` citados são o mesmo arquivo (byte-idêntico) — dedup na citação.
