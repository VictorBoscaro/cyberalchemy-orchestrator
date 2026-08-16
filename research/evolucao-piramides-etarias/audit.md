VERDICT: APPROVE

# Auditoria final independente — evolução das pirâmides etárias

## Escopo

Reauditoria standalone após o reparo formal das duas células `owner` dos KILLs tautológicos. Foram rechecados o novo `findings.md`, a inclusão literal dos três retornos em `research.md`, os dois reviews e os requisitos cumulativos. Não houve nova pesquisa; os spot-checks reutilizam exclusivamente locadores já presentes no corpus.

## Checks de integridade

- Os conteúdos integrais dos retornos `01-longa-duracao.md` (22.761 caracteres), `02-comparacao-regional.md` (13.734) e `03-choques-e-causalidade.md` (25.090) ocorrem literalmente em `research.md`. PASS.
- A síntese cobre longa duração (França, Suécia, Inglaterra/País de Gales e Japão) e casos contrastantes em Europa, Leste Asiático, América Latina e África Subsaariana; rejeita explicitamente lei ou relógio universal. PASS.
- Observado, estimado e projetado permanecem separados: o WPP trata 1950–2023 como estimativas retrospectivas e 2024–2025 como projeções. PASS.
- Forma visual, percentagem, estoque absoluto e taxa, bem como período e coorte, permanecem conceitualmente e operacionalmente separados. PASS.
- Linguagem causal continua limitada por desenho, alternativas e collapse-tests; hipóteses não identificadas são apresentadas como hipóteses, associação, `LIMIT` ou exclusão. PASS.

## Rastreabilidade e claims

As alegações load-bearing de `findings.md` mapeiam para trechos identificáveis de `research.md` e a fontes externas já coletadas: WPP para séries comparativas e status temporal; Weir, Wrigley e MHLW para longa duração; NCHS, Kesternich/Bethmann, UNAIDS e Matysiak para episódios. A conclusão e a resposta de uma linha permanecem dentro desses limites: descrevem direções e associações condicionais, não uma causa social única.

## Spot-checks

| Retorno | Locador já no corpus | Resultado do acesso | Conteúdo confirmado / limite |
|---|---|---|---|
| 01 | WPP 2024 Methodology PDF | acessível | Confirmado: a ONU define estimativas de 1 jan. 1950 a 1 jan. 2024 e projeções de 1 jan. 2024 a 2101; descreve o método de componentes por idade e sexo. Sustenta a separação E/P, não os valores tabulados específicos sem reextraí-los. |
| 01 | MHLW, `E02.pdf` | não acessível: 404 no locador registrado | O PDF/URL é citado no corpus, mas nesta auditoria não foi possível confirmar externamente as taxas japonesas de 1899/1950. Isto não é tratado como confirmação substantiva. |
| 01 | DOI `10.1080/0032472031000147816` (Weir) | identificador plausível e citado; resolvedor indisponível no ambiente | Não foi feita confirmação substantiva externa da cronologia francesa; confirma-se somente o mapeamento local do DOI. |
| 01 | PMC `PMC3865739` | acesso interrompido por verificação anti-bot | O locador foi alcançado, mas conteúdo não ficou disponível; não se declara validação independente da evidência inglesa. |
| 03 | NCHS/CDC, release 2021-07-21 | acessível | Confirmado: EVN dos EUA caiu 1,5 ano de 2019 a 2020 (78,8 para 77,3) e COVID respondeu por 74% da queda. Sustenta choque de período, não mudança estrutural. |
| 02 | WPP 2024 Methodology PDF | acessível | Confirmado o regime metodológico de estimativas/projeções e a incerteza das trajetórias futuras; os oito valores nacionais não foram reextraídos nesta auditoria. |

## Reconciliação dos reviewers

`review-non-vacuity.md` e `review-definitional.md` terminam ambos em `GATE: PASS`. Os quatro KILLs continuam limitados e `do-not-use`: dois `no-witness` e dois `tautological`. Não há reintrodução deles como evidência positiva.

## Falhas bloqueantes e não bloqueantes

Não há falha bloqueante. A matriz tem exatamente as seis colunas exigidas — `candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict | use-mode` — e todos os owners estão preenchidos.

Em particular, os dois KILLs tautológicos agora indicam `síntese, definições operacionais/collapse-test` com linhas 9 e 11 e declaram `sem precedente externo`. Isso é um owner interno rastreável, não uma alegação fictícia de precedente ou evidência externa. Os `GO` continuam somente onde `witnessed?` e `sound?` são positivos; o único `LIMIT` permanece honesto; os KILLs são somente `no-witness` ou `tautological` e permanecem `do-not-use`.

Não bloqueante: o locador MHLW retorna 404, e DOI/PMC não tiveram conteúdo substantivo recuperável nesta sessão. Esses limites foram documentados como acessibilidade/validação incompleta, não convertidos em novas evidências nem em alegações adicionais.

## Veredicto

VERDICT: APPROVE
