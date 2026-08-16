# Revalidação de definitional-soundness — estruturas etárias

## 1. Escopo e método

Esta revisão reaplica somente o gate de **definitional-soundness** ao `findings.md` reparado. `research.md` serve como corpus de apoio; o novo `review-non-vacuity.md` é usado apenas para distinguir falta de testemunho de colapso conceitual. Não há nova pesquisa nem reavaliação do gate empírico.

Para cada alegação realmente usada, o teste exige: referente e medida distinguíveis; separação entre forma visual, proporção, contagem e taxa; separação entre período e coorte; rótulos históricos não usados como causa; identidade contábil não promovida a explicação causal; e condição observável capaz de distinguir ou zerar a contribuição. `LIMIT` é julgado na formulação condicional adotada. Candidatos `KILL: tautological | do-not-use` podem passar como governança de exclusão, nunca como contribuição positiva.

## 2. Matriz conceitual

| claim | conceito alegado | distinção necessária | resultado PASS/FAIL | colapso ou reparo mínimo |
|---|---|---|---|---|
| Estrutura etária é a distribuição do estoque; pirâmide etária é sua representação (`findings.md` 5) | estrutura etária / pirâmide etária | distribuição medida × gráfico; percentagem × contagem; estoque × taxa | PASS | Não há colapso: território, data, idade, sexo e denominadores são explicitados. O collapse-test usa medidas japonesas incompatíveis para mostrar que a distinção faz trabalho (`research.md` 39–44). |
| Envelhecimento é aumento da idade mediana ou da participação 65+, não EVN, queda de 0–14 ou número absoluto de idosos (`findings.md` 7, 94) | envelhecimento populacional | composição × longevidade; participação × número absoluto; grupo etário × forma visual | PASS | A definição e o collapse-test separam as quatro dimensões. “Base/centro/topo” é evitado quando há percentuais; a conclusão usa idade mediana/65+ separadamente de EVN (`findings.md` 7, 94; `research.md` 124–139). |
| Coorte difere de período; cicatriz é descontinuidade contra referência que se desloca com a coorte (`findings.md` 9, 49) | coorte / cicatriz de coorte | evento de período × experiência acumulada; desvio contra baseline × mera saliência; adiamento × fecundidade completada | PASS | Há baseline, deslocamento esperado e teste de recuperação. O baby boom é usado para rejeitar mero adiamento; chamar sua saliência de cicatriz permanece condicionado ao acompanhamento (`findings.md` 49; `research.md` 239–245, 304–307). |
| Choque é ruptura localizada; mudança estrutural exige afastamento pós-evento da trajetória de referência (`findings.md` 11, 53, 55) | choque temporário / mudança estrutural | duração do evento × duração do efeito; taxa de período × distribuição; ruptura × novo nível/tendência | PASS | A regra exige referência e persistência e proíbe alegação estrutural sem horizonte. COVID é corretamente classificada apenas como choque; recessão exige fecundidade completada posterior (`findings.md` 53–55). |
| Razão de dependência etária tem fórmula convencional e não mede dependência econômica (`findings.md` 13, 61) | dependência etária | razão de grupos etários × atividade econômica; composição × ônus econômico | PASS | Numerador, denominador e limites etários estão definidos, e o texto proíbe inferir emprego ou renda. |
| Janela é intervalo de razão de dependência em queda/baixa; dividendo exige ganho econômico atribuído (`findings.md` 13, 61) | janela demográfica / dividendo demográfico | trajetória composicional × nível isolado de 15–64; oportunidade × resultado econômico | PASS | A equivalência janela=dividendo foi removida e nenhuma janela empírica é afirmada. Para uso futuro de “baixa”, declarar limiar ou comparador; isso não é reparo residual deste texto porque a categoria não é aplicada positivamente. |
| Nascimentos, mortes e migração decompõem a variação do estoque, mas não explicam as causas sociais dos fluxos (`findings.md` 15) | identidade de balanço / mecanismo causal | decomposição contábil × explicação causal; fluxos compatíveis × estoques com território alterado | PASS | O texto chama explicitamente a relação de identidade e reconhece que o corpus não executa decomposição conjunta. O collapse-test ataca sua aplicação empírica, não tenta provar causalidade. |
| Sob componentes mantidos constantes, mudanças de mortalidade/fecundidade têm efeitos condicionais sobre coortes e composição (`findings.md` 31; matriz 83) | cenário demográfico condicional | efeito absoluto × participação; condição ceteris paribus × história observada; identidade local × sequência causal completa | PASS | Como `LIMIT`, não colapsa: explicita constantes, defasagem, denominador e compensações, e nega que Japão/WPP testem a sequência completa. A condição de zeragem é composição integralmente compensada. Não usar como atribuição causal histórica. |
| Hipóteses sanitárias e sociais devem seguir exposição → taxa por idade → composição, sem usar “transição” como causa (`findings.md` 33, 65) | transição demográfica / mecanismo subjacente | rótulo descritivo × causa; lista de fatores × encadeamento testado | PASS | “Transição” não desempenha papel causal; o relógio universal é rejeitado por cronologias e medidas independentes. As causas são chamadas de hipóteses, não efeitos estimados. |
| Transição epidemiológica não é usada como explicação positiva no findings reparado | transição epidemiológica | mudança de causas de morte × queda da mortalidade; quadro descritivo × causa | PASS | O rótulo foi retirado da explicação efetivamente usada. No corpus ele permanece explicitamente como quadro descritivo, não lei sequencial (`research.md` 50–52, 101). |
| Golfo sustenta somente hipótese qualitativa de seletividade adulta, sem rapidez, magnitude ou reversibilidade afirmadas (`findings.md` 35) | seletividade migratória / forma etário-sexual | hipótese por idade/nacionalidade × medida nacional; “rápido/reversível” × contraste temporal | PASS | Os adjetivos não operacionalizados foram retirados da alegação usada. O candidato quantitativo permanece `KILL: no-witness | do-not-use` (`findings.md` 85). |
| Ritmos de Suécia, Japão e Coreia são diferenças em pontos percentuais no mesmo intervalo (`findings.md` 39, 80) | ritmo de mudança / estrutura etária | adjetivo “comprimido” × variação mensurada; topo/base × grupos 65+/0–14 | PASS | Países, intervalo, unidade e variações estão declarados. O texto não usa “comprimido” como medida nem atribui causa isolada. |
| Política chinesa pode ter contribuído para limitar nascimentos, sem quantificar contribuição ao envelhecimento (`findings.md` 41, 84) | contribuição causal parcial / envelhecimento | limitar nascimentos × causar todo envelhecimento; intervenção × rótulo de transição | PASS | A alegação nomeia desfecho proximal, alternativas e limite de quantificação; envelhecimento não é inferido apenas da política. |
| COVID prova choque de mortalidade de período, não mudança estrutural da distribuição (`findings.md` 53, 86) | choque de período / EVN / estrutura | EVN de período × biografia de coorte; mortalidade × forma persistente | PASS | O uso preserva as três distinções e seu collapse-test exige ruptura contra baseline e pares, não mera aparência visual. |
| Uma assinatura visual não identifica sua causa (`findings.md` 67) | identificação causal por forma | assinatura × mecanismo; hipótese diagnóstica × atribuição | PASS | Guerra, migração, nascimentos, mortes, deslocamento e registro fornecem alternativas; coorte, nacionalidade, fluxos e comparação temporal são discriminadores observáveis (`research.md` 204–223, 302–317). |
| “Cicatriz é marca persistente” e “mudança estrutural é mudança durável”, sem baseline/horizonte (`findings.md` 89–90) | tautologias excluídas | repetição nominal × operador observável | PASS | Passam somente como governança: estão `KILL: tautological | do-not-use`. As definições usadas nas linhas 9–11 acrescentam baseline, deslocamento, horizonte e trajetória de referência; os candidatos mortos não contribuem para a conclusão. |

## 3. Conceitos sólidos

- **Estrutura e representação:** pirâmide, distribuição, forma, percentagem, estoque e taxa agora têm papéis distintos (`findings.md` 5).
- **Envelhecimento:** idade mediana/65+, EVN, 0–14 e absolutos são explicitamente separados (`findings.md` 7, 94).
- **Coorte e cicatriz:** há trajetória de referência, deslocamento temporal e teste por fecundidade completada (`findings.md` 9, 49).
- **Choque e mudança estrutural:** a classificação depende do efeito pós-evento contra referência, não da duração ou do nome do evento (`findings.md` 11, 53–55).
- **Dependência, janela e dividendo:** composição, intervalo favorável e resultado econômico não são equivalentes (`findings.md` 13, 61).
- **Balanço demográfico:** a identidade contábil é declarada como tal; o cenário derivado é limitado por constantes, compensações e falta de teste causal completo (`findings.md` 15, 31).
- **Forma visual:** adjetivos foram substituídos por grupos, percentuais, pontos percentuais e intervalos onde há alegação positiva (`findings.md` 7, 35, 39, 67).

## 4. Falhas e reparos mínimos

Nenhuma alegação efetivamente usada apresenta colapso definicional. Os reparos anteriores foram incorporados: envelhecimento não equivale a longevidade ou crescimento absoluto; cicatriz tem baseline e deslocamento; mudança estrutural tem referência e exigência de horizonte; janela não equivale a dividendo; contabilidade não é apresentada como causa social; e os contrastes visuais positivos foram operacionalizados.

Há uma cautela não bloqueante: se “janela demográfica” vier a ser aplicada empiricamente em versão futura, “razão baixa” deverá receber limiar ou comparador e intervalo explícitos (`findings.md` 13). No texto atual não há alegação positiva de que um país esteja nessa janela, portanto não existe reparo residual obrigatório.

## 5. KILLs tipados

- `KILL: tautological | do-not-use` — **“Cicatriz é uma marca persistente” sem baseline ou acompanhamento** (`findings.md` 89). A contribuição pretendida seria distinguir marca de coorte de oscilação de período; o fato observável distintivo é a descontinuidade reaparecer na idade esperada ou a fecundidade completada não recuperar a diferença. O candidato morto não é usado; a definição operacional da linha 9 contém esses operadores.
- `KILL: tautological | do-not-use` — **“Mudança estrutural é mudança durável” sem horizonte ou trajetória de referência** (`findings.md` 90). A contribuição pretendida seria distinguir ruptura temporária de alteração persistente; o fato observável distintivo é retorno à trajetória de referência, ou afastamento após o evento dentro de horizonte fixado. O candidato morto não é usado; a definição limitada da linha 11 exige esses operadores.

Os KILLs tautológicos passam apenas como governança honesta de exclusão. Não sustentam conceitos, evidência ou conclusão. Os `KILL: no-witness` das linhas 85 e 88 pertencem ao gate anterior e tampouco são usados positivamente.

## Veredicto global

**GATE: PASS**

Nenhuma alegação usada colapsa no próprio conceito ou em tautologia; não há reparo conceitual residual obrigatório.
