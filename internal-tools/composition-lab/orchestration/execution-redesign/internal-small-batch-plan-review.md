---
artifact_kind: internal-small-batch-plan-review
date: 2026-08-13
verdict: FIX
---

# Review — plano interno em pequenos lotes

## Veredito

**FIX**, aplicado. O plano está apto a lançar D1 como tarefa nativa bounded de subagente, não como
dispatch Arcanum governado. Se o owner escolher o transporte governado, o launch continua bloqueado
até binding first-line, open e close válidos.

## Cobertura

Foram verificados: objetivo científico, perguntas não-presuntivas, corpus e hashes D1, boundaries,
topologia connectionless, mecanismo de launch, prompts, budgets, outputs, estados evidenciais,
auditoria, critérios de avanço, primeiro lote e separação de comparação/síntese.

Os três paths D1 existem no `domainspec-core`; HEAD é
`9bfec22712e4675d39c4cf1c21b36dc66614136c`; o status scoped está limpo; bytes e SHA-256 conferem
com o annex e o plano.

## Findings e correções

1. **MAJOR — identidade de launch ambígua.** O texto alternava `helper` e `dispatch`, embora não
   houvesse capability/registro governado nem binding preparado. Corrigido para tarefa nativa de
   subagente; promoção a dispatch governado agora bloqueia até `ACI-WORKFLOW-BINDING-V1` first-line
   e lifecycle honestos.
2. **MAJOR — auditoria de writes sem baseline.** O auditor não tinha como atribuir mudanças em
   worktrees já sujos. Corrigido com baseline scoped antes de cada tarefa e comparação posterior.
3. **MINOR — `read-only` contradizia outputs.** Corrigido para `source-read-only` com único output
   allowlisted e criação explícita da pasta exata.
4. **MINOR — prompts dependiam de “este plano” e “o annex”.** Substituído por paths absolutos.

## Findings não sobreviventes

- As perguntas preservam composição como pergunta aberta e proíbem classificações prematuras.
- D1 é connectionless; auditoria ocorre somente após término, sem handoff em memória.
- Budgets e outputs são explícitos e proporcionais ao lote de três fontes.
- Comparação e síntese permanecem novos dispatches/tarefas, sem promoção automática.
- Inventory, runtime, skills, registry, observabilidade e fontes permanecem fora do write boundary.

## Critério terminal

- `READY`: D1 como tarefa nativa bounded, após baseline mecânico.
- `BLOCK`: qualquer source drift, binding incompleto caso governado, source write, escape de
  autoridade ou cobertura menor que 3/3.
