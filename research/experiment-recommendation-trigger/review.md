# Review adversarial — recomendação de experimento

## Veredito

**FIX, aplicado.** A síntese tinha a direção correta — o ledger só nomeia candidatos e não autoriza um experimento —, mas fazia três afirmações mais fortes que a evidência: tratava o timing como resolvido, chamava componentes retrospectivos de witness completo e confundia construção habilitadora com validação equivalente. `findings.md` foi corrigido antes deste encerramento.

## Cobertura

| Lens | Corpus inspecionado | Achados |
|---|---|---:|
| Não-vacuidade / witness prospectivo | definições iniciais, seis relatórios de scout, `research.md` e `findings.md` | 2 major, 1 minor |
| Fronteira definicional / colapso | definições iniciais, seis relatórios de scout, `research.md` e `findings.md` | 3 major, 1 minor |

O agente principal conferiu as passagens citadas e decidiu cada ataque contra o corpus. Nenhum lens retornou zero achados.

## Achados que sobreviveram

1. **MAJOR — timing não testemunhado prospectivamente.** A frase “pode recomendar no momento correto” excedia a evidência: nenhum episódio observa, antes da intervenção, estado, alternativas concorrentes, oferta, resposta e consequência. Correção: a conclusão agora diz “procedimento candidato” e exige protocolo held-out antes de implementação.
2. **MAJOR — witness conjuntivo ausente.** “Sim: Mint e intent-population” confundia casos que testemunham componentes com uma linha em que os sete predicados estão positivos antes da oferta. Correção: os casos foram reclassificados como parciais e retrospectivos; o protocolo exige `true|false|unknown` por item e aceita como positivo apenas a conjunção integral.
3. **MAJOR — novidade positiva não demonstrada.** “Regra candidata em duas etapas” sugeria um novo gatilho, quando os critérios positivos vêm de contratos DomainSpec e da política candidata do Superinterviewer. O resíduo próprio do ledger é nomeação para inspeção. Correção: renomeado para “procedimento candidato de roteamento e inspeção” e adicionada comparação com inspeção direta por custo, latência e perda de casos.
4. **MAJOR — construção não equivale a validação.** A condição que suprimia diante de qualquer “build, run, receipt...” eliminaria justamente aparatos e objetos necessários para experimentar. Correção: os artefatos agora são classificados entre resolução da claim, validação equivalente, aparato habilitador e irrelevante; apenas as duas primeiras classes suprimem.
5. **MAJOR — limiar `dois movimentos` sem owner ou evidência.** O corpus não sustenta esse numeral. Correção: movimentos sem delta viraram sinal de reavaliação de modo/carga, sem threshold automático; qualquer janela deve ser validada prospectivamente.
6. **MINOR — `draft/exploratory` usado como proxy de conteúdo.** O rótulo não prova falta de decisão, claim, owner ou aparato. Correção: o status agora inicia verificação de conteúdo e só suprime quando os requisitos faltam.
7. **MINOR — checagem negativa classificada como candidato `GO`.** “Nenhuma construção encontrada” é somente evidência escopada de supressão. Correção: removida da matriz de candidatos e preservada como checagem negativa fora de `GO/KILL`.

## Ataques que não sobreviveram

- Contagem de pesquisas, tempo decorrido e ausência de row `code` já estavam explicitamente rejeitados e acompanhados de contraexemplos.
- A proposta já impedia execução automática, preservava recusa/adiamento e comparava experimentar com perguntar, recuperar, responder, reframar, esperar e parar.
- A redução completa a “próximo passo genérico” não se sustenta: a conjunção herdada ainda distingue uma oferta de pré-registro de outros movimentos. O que não estava demonstrado era seu timing empírico, agora tratado como hipótese.

## Aprovação

Com as correções acima, os achados são adequados como resultado de pesquisa e desenho de validação. Eles **não** autorizam implementar um recomendador nem afirmar que o ledger detecta prontidão. O próximo gate é executar o protocolo retrospectivo/held-out descrito em `findings.md`.
