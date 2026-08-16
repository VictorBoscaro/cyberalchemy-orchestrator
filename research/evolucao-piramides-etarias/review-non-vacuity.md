# Revalidação de non-vacuity — suficiência do testemunho empírico

## 1. Escopo e método

Esta revalidação aplica somente o gate de **non-vacuity** ao novo `findings.md`. Não avalia ownership/precedente nem definitional-soundness e não usa o parecer anterior como prova. Para cada alegação efetivamente usada, exige: lugar ou população identificável, período, métrica definida, valor ou direção comparável e fonte rastreável em `research.md`. Para alegações causais, exige também ordem temporal e exame da principal alternativa ou contrafactual; sem isso, só passa formulação associativa, descritiva ou explicitamente condicional.

Na matriz, `GO` é avaliado como afirmação positiva; `LIMIT`, na formulação limitada realmente adotada; e `KILL`, como regra honesta de não uso. Um candidato `KILL: no-witness` pode passar como governança justamente porque reconhece a ausência e não é usado como evidência positiva. Suporte parcial fora de uma formulação `LIMIT` explícita seria `FAIL`.

## 2. Matriz de claims e testemunhos

| claim | witness exigido | witness encontrado | resultado PASS/FAIL | reparo mínimo |
|---|---|---|---|---|
| **GO —** Percentagens, estoques e taxas não são intercambiáveis; o Japão ilustra denominadores distintos (`findings.md` 5) | Lugar, data, medidas, valores e denominadores | Japão: estoque de 83,20 milhões em 1950; natalidade/mortalidade por 1.000 habitantes e mortalidade infantil por 1.000 nascidos vivos em 1899/1950; MHLW/IPSS (`research.md` 39–44) | PASS | Nenhum |
| **GO —** Envelhecimento é medido por idade mediana ou participação 65+, separadamente de EVN e 0–14 (`findings.md` 7) | Séries com métricas definidas, lugar e período | WPP define e fornece 0–14, 65+, idade mediana e EVN para oito países, 1950 E–2025 P (`research.md` 124–139) | PASS | Nenhum |
| **GO —** Baby boom americano excedeu mero adiamento: coortes 1931–35 completaram 3,2 filhos versus 2,4 nas 1911–15 (`findings.md` 9, 49) | População/coortes, períodos, fecundidade completada, valores e fonte | Mulheres dos EUA nas coortes indicadas, valores 3,2/2,4 e discussão de alternativas; Sander & Taylor (`research.md` 237–245) | PASS | Nenhum |
| **LIMIT —** Mudança estrutural exige afastamento persistente de trajetória de referência; sem horizonte, usar apenas choque/compatível com persistência (`findings.md` 11) | Para afirmar persistência: baseline e observações posteriores; para o limite: demonstração de que o corpus não os fornece | COVID tem ruptura 2019–20, mas o corpus declara ausência de base para estrutura persistente; recessão requer fecundidade completada posterior (`research.md` 273–287) | PASS | Nenhum |
| **LIMIT —** Razão de dependência descreve composição; o corpus não permite inferir dividendo/renda (`findings.md` 13, 61) | Série da razão para “janela”; desfecho econômico e contraste para “dividendo” | WPP fornece grupos etários, mas não renda nem efeito institucional; o texto não afirma janela empírica nem dividendo (`research.md` 151–153, 177–183) | PASS | Nenhum |
| **LIMIT —** Nascimentos, mortes e migração são identidade de balanço, mas o corpus não os decompõe conjuntamente (`findings.md` 15) | Para aplicação empírica: território/intervalo e três componentes compatíveis | Japão mede taxas vitais; Golfo é apenas descrição etário-sexual; ausência conjunta é explicitada (`research.md` 39–44, 213–223, 257–263) | PASS | Nenhum |
| **GO —** WPP 1950–2023 é estimativa e 2024–25 projeção; reconstruções não são censos (`findings.md` 17, 73) | Metadados de status e período | Metodologia WPP e lacunas explicitam E/P e modelagem (`research.md` 114–116, 177–188) | PASS | Nenhum |
| **LIMIT —** Para 1750–1800 não há idade×sexo comparável para todos; quantitativamente, França mostra queda de nupcialidade 1740–1820 e transição conjugal desde 1790 (`findings.md` 21) | Caso, período, medida reprodutiva, direção e fonte; ausência reconhecida para generalização | Reconstrução Weir separa nupcialidade/fecundidade conjugal e data a transição (`research.md` 34, 57–60, 81) | PASS | Nenhum |
| **GO —** Inglaterra cresceu 5,57 mi→11,58 mi (1741–1821) antes do contraste de fecundidade conjugal >6→<3 (coortes casadas 1860/1910); fatos incompatíveis com relógio universal (`findings.md` 23, 65, 81) | Território, datas, estoques, métrica de coorte, valores e fonte; formulação não monocausal | Wrigley–Schofield e Szreter & Garrett fornecem os valores; ONS relata mortalidade infantil alta 1850–1900 (`research.md` 36–38, 61–63) | PASS | Nenhum; “incompatíveis” preserva o alcance correto |
| **GO —** Japão 1899–1950: mortalidade e mortalidade infantil caíram mais que natalidade, compatível com maior sobrevivência, sem medir 0–14 (`findings.md` 25, 82) | Mesmo território/período, taxas definidas, valores e fonte | Mortalidade 21,5→10,9; infantil 153,8→60,1; natalidade 32,0→28,2; MHLW (`research.md` 39–44, 64–65) | PASS | Nenhum |
| **GO —** Oito países têm menor 0–14 e maior EVN entre 1950 E e 2025 P (`findings.md` 27, 79, 94–96) | Oito populações, dois pontos com status, métricas e direções comparáveis | Tabela WPP traz 0–14 e EVN para Suécia, Japão, Coreia do Sul, China, Brasil, México, Nigéria e Etiópia (`research.md` 124–139, 169–175) | PASS | Nenhum |
| **LIMIT —** Efeitos de mortalidade/fecundidade são cenário condicional; Japão/WPP apenas ilustram compatibilidade, não testam sequência causal completa (`findings.md` 31, 83) | Condições explícitas; testemunho ilustrativo; proibição de inferência causal plena | Taxas japonesas e séries WPP fornecem direções; o corpus reconhece que faltaria extração idade×sexo e decomposição (`research.md` 39–55, 103–105, 124–167) | PASS | Nenhum |
| **LIMIT —** Fatores sociais/sanitários são hipóteses, sem contribuição causal independente estimada (`findings.md` 33) | Para causalidade: exposição, sequência, taxa por idade, comparação e alternativas | O corpus os chama de plausíveis e declara que taxas nacionais não identificam contribuições (`research.md` 48–55, 159–167, 183) | PASS | Nenhum |
| **LIMIT —** Golfo sustenta somente hipótese qualitativa de seletividade adulta; não sustenta rapidez, magnitude, razão quantificada ou reversibilidade nacional (`findings.md` 35) | Para alegação quantitativa: país, ano, valor, denominador e contraste temporal | ESCWA/GCC/ONU descrevem idade, sexo e nacionalidade, mas sem país/ano/valor reproduzido (`research.md` 257–263) | PASS | Nenhum; a ausência está corretamente delimitada |
| **GO —** Suécia, Japão e Coreia tiveram variações distintas de 0–14/65+ em 1950 E–2025 P (`findings.md` 39, 80) | Países, intervalo comum, percentuais e diferenças comparáveis | WPP: Suécia −6/+10 pp; Japão −23/+25; Coreia −32/+16, calculáveis diretamente da tabela (`research.md` 128–149) | PASS | Nenhum |
| **GO —** Política chinesa pode ter contribuído para limitar nascimentos, sem contribuição quantificada ao envelhecimento (`findings.md` 41, 84) | Ordem temporal, intervenção, desfecho, alternativa/contrafactual e limite de magnitude | Política desde fim dos anos 1970; queda prévia; censo 2020 com TFT 1,3 e 60+ 18,7%; implementação desigual e alternativas examinadas (`research.md` 247–255, 296) | PASS | Nenhum; manter “pode” e confiança média |
| **GO —** Brasil/México aumentam 15–64; Nigéria/Etiópia projetam 41/38% em 0–14 e 3% em 65+ em 2025; TFT/EVN são consistentes com calendários diferentes (`findings.md` 43) | Quatro países, 1950 E/2025 P, grupos definidos, valores, TFT/EVN e linguagem não causal | Todos os valores e direções aparecem na tabela WPP (`research.md` 128–139, 151–157) | PASS | Nenhum |
| **GO —** Alemanha: razão H/M 15–45 caiu 0,96→0,72, 1939–46; contraste regional liga escassez a casamento/fecundidade com confiança média (`findings.md` 47, 59) | Lugar/período, razão definida, exposição anterior, contraste e alternativas | Kesternich et al. e Bethmann & Kvasnicka; migração, fronteiras, destruição e seleção são tratadas (`research.md` 227–235, 293) | PASS | Nenhum; não extrapolar além da Alemanha Ocidental |
| **LIMIT —** KwaZulu-Natal mostra mortalidade por idade/sexo/causa associada à Aids; regionalmente mortes Aids caem 49% em 2010–19; programas são associação temporal, não efeito isolado (`findings.md` 51) | Local/população, métricas, período/valor e alternativas para causalidade | Vigilância rural local mede perfil; UNAIDS fornece direção e 49%; TARV, diagnóstico, prevenção e qualidade de dados são alternativas (`research.md` 265–271, 298) | PASS | Nenhum |
| **GO/LIMIT —** EUA: EVN caiu 1,5 ano em 2019–20, quase 3/4 atribuídos à COVID; prova choque de período, não estrutura durável (`findings.md` 53, 86) | Lugar/período, EVN, valor, comparação de baseline/pares e limite estrutural | NCHS e Woolf et al.; excesso contra baseline e comparação com pares, com efeitos indiretos reconhecidos (`research.md` 273–279, 299) | PASS | Nenhum |
| **GO —** Em 251 regiões UE, 2002–14, desemprego associou-se à queda da fecundidade, sem magnitude/causalidade agregada (`findings.md` 55, 87) | População/regiões, período, direção, desenho e alternativas | Painel multinível de 251 regiões; associação e confundidores/endogeneidade explicitados (`research.md` 281–287, 300) | PASS | Nenhum |
| **GO —** Assinatura visual não identifica causa (`findings.md` 67) | Pelo menos duas causas plausíveis para assinatura e regra de discriminação | Guerra e migração podem produzir déficit masculino; catálogo inclui mortes, nascimentos, deslocamento e registro; exige coorte/fluxos/comparação (`research.md` 205–223, 302–317) | PASS | Nenhum |
| **GO —** Limites históricos e territoriais: reconstruções, revisões SCB, Japão pré-1899/Okinawa (`findings.md` 71) | Caso, período e metadado rastreável | Documentados para França, Inglaterra, Suécia e Japão (`research.md` 18, 33–40, 57–78) | PASS | Nenhum |
| **KILL: no-witness / do-not-use —** Migração laboral alterou rapidamente uma pirâmide nacional do Golfo em magnitude mensurada (`findings.md` 85) | País, ano, valor, denominador e contraste temporal | Não encontrado; o próprio findings registra a ausência e não usa o candidato positivamente (`research.md` 257–263) | PASS | Nenhum; governança honesta, não evidência positiva |
| **KILL: no-witness / do-not-use —** Maior 15–64 produz ganho de renda sob certas instituições (`findings.md` 88) | Desfecho econômico, período, comparação e identificação do efeito | Não encontrado; o findings proíbe essa inferência (`research.md` 151–153, 177–183) | PASS | Nenhum; governança honesta, não evidência positiva |
| **KILL: tautological / do-not-use —** “Cicatriz é marca persistente” e “mudança estrutural é mudança durável” sem baseline/horizonte (`findings.md` 89–90) | Baseline, horizonte e observações posteriores para uso positivo | Não aplicável como evidência positiva; candidatos são excluídos e definições operacionais exigem baseline/horizonte (`findings.md` 9–11) | PASS | Nenhum |

## 3. Alegações que passam

- Passam todos os `GO` quantitativos: Japão 1899–1950; oito países WPP 1950 E–2025 P; contrastes Suécia/Japão/Coreia; Brasil/México/Nigéria/Etiópia; Alemanha; baby boom americano; COVID-19; e Grande Recessão.
- Passam os `GO` causais delimitados: a contribuição possível da política chinesa, com queda prévia e alternativas; e o efeito regional da escassez masculina na Alemanha Ocidental, com confiança média.
- Passam os `LIMIT`: cenário demográfico condicional, hipóteses sociais não identificadas, evidência qualitativa do Golfo, associação Aids/programas e ausência de consequência econômica mensurada.
- Passam como governança — não como evidência positiva — os dois `KILL: no-witness` e os dois `KILL: tautological`, todos marcados `do-not-use`.
- A conclusão (`findings.md` 94–96) permanece dentro do testemunho: restringe a convergência quantitativa aos oito países WPP, nomeia corretamente estimativa/projeção e descreve mecanismos como associações condicionais, sem causa universal.

## 4. Falhas e reparos mínimos

Nenhuma alegação efetivamente usada excede o testemunho disponível. Os reparos anteriores foram incorporados: não há mistura de percentagem com estoque, de período com coorte ou de observado com projetado; interpretações sem medida aparecem como limites; e atribuições causais reconhecem ordem temporal, alternativas e força do desenho.

Reparos residuais obrigatórios: **nenhum**.

## 5. KILLs tipados

- `KILL: no-witness` — magnitude/rapidez nacional da migração laboral no Golfo: corretamente `do-not-use`; faltam país, ano, valor e contraste (`findings.md` 85; `research.md` 257–263).
- `KILL: no-witness` — ganho de renda produzido por maior participação 15–64: corretamente `do-not-use`; falta desfecho econômico (`findings.md` 88; `research.md` 151–153).
- `KILL: tautological` — cicatriz sem baseline/acompanhamento: corretamente `do-not-use` (`findings.md` 89).
- `KILL: tautological` — mudança estrutural sem horizonte/trajetória de referência: corretamente `do-not-use` (`findings.md` 90).

Os KILLs não são convertidos em evidência por owner, precedente ou mera citação. Eles passam neste gate apenas porque governam a exclusão dos candidatos sem testemunho.

## Veredicto global

**GATE: PASS**

Nenhuma alegação efetivamente usada excede seu testemunho; não há reparo residual obrigatório.
