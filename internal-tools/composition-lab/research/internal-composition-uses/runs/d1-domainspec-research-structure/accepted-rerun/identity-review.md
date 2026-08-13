---
artifact_kind: post-materialization-identity-review
target: d1-domainspec-research-structure/accepted-rerun
status: complete
date: 2026-08-13
authority: identity-and-provenance-review-only
verdict: PASS / KEEP
---

# Review independente de identidade e proveniência — D1 accepted rerun

## Escopo

Esta revisão verifica somente identidade dos bytes, proveniência da materialização, resolução dos
links do programa, separação do attempt antigo e clareza da autoridade documental. Ela não reabre
o conteúdo semântico de `findings.md` nem o mérito do review que o aceitou.

## Verificações

| Check | Resultado | Evidência |
|---|---|---|
| Trio byte-idêntico | PASS | Os hashes SHA-256 completos de `source-receipt.md`, `findings.md` e `review.md` no destino coincidem individualmente com os respectivos arquivos em `orchestration/execution-redesign/runs/d1-domainspec-research-structure/rerun/`. Os tamanhos também coincidem: 1.702, 21.057 e 9.379 bytes. |
| Receipt de materialização | PASS | `materialization-receipt.md` identifica corretamente origem e destino, registra os três hashes completos, limita a alegação de identidade ao trio e atribui autoridade semântica ao veredito terminal de `review.md`. |
| Quatro links do programa | PASS | Os links D1 nas linhas 17, 18, 85 e 86 de `internal-tools/composition-lab/research-program.md` resolvem, respectivamente, somente para `findings.md` e `review.md` sob `research/internal-composition-uses/runs/d1-domainspec-research-structure/accepted-rerun/`. Todos os quatro alvos existem. |
| Separação do attempt bloqueado | PASS | O programa não contém referência a `scout-return.md`, `audit.md` ou ao diretório antigo sob `internal-tools/composition-lab/orchestration/`. Nenhum link ou claim D1 do programa depende desse attempt. |
| Preservação da origem | PASS | O trio original continua presente sob `orchestration/execution-redesign/runs/d1-domainspec-research-structure/rerun/` com os mesmos hashes recomputados. A materialização não o substituiu. |
| Preservação do attempt antigo | PASS | `scout-return.md` e `audit.md` continuam presentes no diretório antigo, com SHA-256 `af309f88ad0d173a6263bed20f25d12ee4f5023ae4b744f13c15ff37e4a1640a` e `c3a4f978f09ec5d62633681560da454a1e66599d5ba44fc829db2d2b67c69e15`. Permanecem separados do bundle aceito. |
| Autoridade documental | PASS | O `review.md` materializado declara explicitamente que o re-review `PASS / KEEP` supersede o `FIX` inicial e termina com `Current terminal verdict: KEEP`. O receipt não reivindica autoridade própria. |

## Ledger de identidade do trio

| Arquivo | SHA-256 recomputado na origem e no destino |
|---|---|
| `source-receipt.md` | `4c935403ee6b2c8a26fe1853d200040828adfdd49f06324d9d412e9642339f87` |
| `findings.md` | `6012d98fee41c487c5f532befd56855d0ec7299ca2b9259c922b5ae86218bbf1` |
| `review.md` | `f1368df68cf4a433de19c52aca3509d7258fcd2895fa9693d9a27f2a0a58638f` |

## Veredito

**PASS / KEEP.** A materialização preserva integralmente a identidade do bundle aceito, registra
proveniência suficiente, direciona exclusivamente os quatro links D1 do programa ao bundle
co-localizado e não mistura nem sobrescreve o attempt antigo bloqueado. A autoridade semântica
permanece inequivocamente no `PASS / KEEP` terminal do review materializado.

