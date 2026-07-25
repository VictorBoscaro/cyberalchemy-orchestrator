# APÊNDICE TÉCNICO (camada técnica: exposta, honesta, auditável)

> Esta seção existe para dar rastreabilidade e credibilidade. As páginas de negócio acima se sustentam sozinhas na leitura, mas todo número que aparece nelas nasce aqui. Se algum valor lá em cima não puder ser reconstruído a partir daqui, é erro nosso, não licença poética. Modelo reprodutível: `model/motor.py` gera `model/model.json`, e é contra esse arquivo que cada linha abaixo pode ser conferida.

## T1. Natureza dos dados

Começamos pela ressalva que condiciona tudo o que vem depois. O Excel do briefing (as abas "Pricelist e Projeção", "Features" e "Histórico de Vendas") não foi fornecido. Portanto, nenhum número deste apêndice é medição: todos são modelados sinteticamente, calibrados em ordens de grandeza plausíveis para CPG de alimentos em q-commerce na Rappi Brasil. Isso não enfraquece o modelo, delimita o que ele é. Cada premissa está isolada e é substituível: trocar um valor sintético pelo número real da FOODSToGo ajusta a magnitude do resultado sem tocar na lógica que o produz. O que estamos entregando é o motor, não a verdade sobre o mercado.

## T2. Premissas centrais

As quatro premissas abaixo são as entradas de que todo o resto depende. Vale saber o que cada uma significa antes de vê-la operar nas seções seguintes.

- **Ticket médio:** 18 USD por pedido. Converte GMV em número de pedidos e vice-versa.
- **Margem de contribuição:** 38%. É a fração da venda que sobra para cobrir a mídia e gerar retorno; não é margem líquida de DRE (ver T6).
- **Histórico orgânico de 12 meses:** 3.240.000 USD, com base mensal em torno de 250k e picos claros de ocasião em junho (305k), outubro (310k) e dezembro (380k).
- **Spend de referência:** 700k, usado como ponto de ancoragem da curva de saturação. **Elasticidade de saturação:** 0,18, o expoente que governa o quão rápido o retorno decresce quando o investimento sobe.

## T3. Catálogo de features (Pricelist sintético, preço-teto anual a negociar)

A tabela lista o inventário RappiAds que o modelo considera. As colunas são: o teto anual de investimento por feature (limite comercial, ainda a negociar), o ROAS base atribuído a cada uma (retorno em GMV por USD, antes de cenário e saturação) e o papel de funil que ela cumpre. É desse catálogo que as estratégias de T4 tiram seus ROAS ponderados.

| Feature | Funil | Teto anual (USD) | ROAS base | Papel |
|---|---|---|---|---|
| Banner Home | Topo | 140.000 | 2,6 | Alcance |
| Banner Categoria | Meio | 90.000 | 3,2 | Alcance |
| Push Segmentado | Meio | 70.000 | 4,1 | Momentos |
| Sponsored Products | Fundo | 160.000 | 5,2 | Performance |
| Cupom Cofinanciado | Fundo | 120.000 | 4,6 | Performance |
| Brand Page / Loja | Topo | 80.000 | 2,9 | Alcance |
| Ativação de Momento | Fundo | 130.000 | 5,6 | Momentos |
| Vídeo / Rich Media | Topo | 60.000 | 2,4 | Alcance |

Leitura: o ROAS base cresce conforme se desce o funil (alcance no topo rende menos por USD, performance e momentos no fundo rendem mais). Nenhuma feature é descartada; o que muda entre estratégias é o peso que cada papel recebe.

## T4. As três estratégias (mix de alocação do investimento por papel)

Cada estratégia é um jeito de dividir o mesmo investimento entre os três papéis de funil. As colunas Alcance, Momentos e Performance somam 100% e mostram para onde vai o dinheiro; o ROAS ponderado na última coluna é a consequência direta desse mix, calculado sobre os ROAS base de T3.

| Estratégia | Alcance | Momentos | Performance | ROAS ponderado |
|---|---|---|---|---|
| Alcance | 65% | 10% | 25% | 3,51× |
| Performance | 15% | 20% | 65% | 4,57× |
| Momentos | 20% | 55% | 25% | 4,45× |
| **Blend Recomendado** | 25% | 40% | 35% | **4,35×** |

Comparação a 700k, cenário Base, em ROMI: Alcance +34%, Performance +74%, Momentos +69%, **Blend +65%**. O Blend não é a estratégia de maior ROMI puro (Performance é). Ele abre mão de alguns pontos de eficiência em troca de duas coisas que uma métrica pontual não captura: diversificação de risco entre papéis e construção de território de marca, já que a fatia de Alcance sustenta a presença da FOODSToGo no horizonte plurianual, não só na conversão do ano 1.

## T5. Como o retorno é modelado (a cadeia)

Aqui está o motor inteiro, em cinco passos. Partindo do investimento de um tier, cada linha é uma multiplicação ou subtração explícita, sem etapa escondida. Quem quiser refazer a conta a mão consegue.

```
investimento (tier)
  → ROAS_efetivo = ROAS_ponderado × fator_cenário × fator_saturação
  → GMV_incremental = investimento × ROAS_efetivo
  → margem_contrib_incremental = GMV_incremental × 38%
  → retorno_líquido_margem = margem_contrib_incremental menos investimento
  → ROMI = retorno_líquido_margem / investimento
```

Os dois fatores que modulam o ROAS ponderado:

- **Fator de cenário:** Conservador 0,75, Base 1,00, Otimista 1,25. É o estresse aplicado uniformemente para cima e para baixo.
- **Fator de saturação:** (700k / investimento)^0,18, limitado ao intervalo [0,70; 1,15]. Modela retornos decrescentes: quanto mais o spend passa de 700k, mais o fator cai; abaixo de 700k ele premia, mas o teto de 1,15 impede que o modelo prometa milagre em investimento baixo.

## T6. Aviso de nomenclatura (importante)

Este é o ponto que mais protege a credibilidade do plano, então não abreviamos. `retorno_líquido_margem` não é lucro líquido. É a margem de contribuição incremental menos o investimento em mídia, e portanto fica antes de custos fixos, opex, impostos e logística. A métrica de retorno que reportamos é o **ROMI** (Return on Marketing Investment), calculada sobre base de margem de contribuição, e não um ROI de fundo de DRE. Quem ler "+65%" como lucro contábil estará lendo o número errado; ele é retorno de marketing, e é assim que deve ser tratado em qualquer decisão de aprovação.

## T7. Matriz completa de resultados (resumo por estratégia a 700k)

A tabela recorta os resultados no tier de 700k, que é o objeto da recomendação. As três primeiras linhas mostram o Blend Recomendado estressado nos três cenários (o intervalo de risco do plano); as três últimas fixam o cenário Base e trocam a estratégia, para situar o Blend contra as alternativas. As colunas são GMV incremental gerado, retorno líquido de margem (na definição de T6) e ROMI.

| Estratégia | Cenário | GMV incremental | Ret. líq. de margem | ROMI |
|---|---|---|---|---|
| Blend | Conservador | 2.283.094 | 167.576 | +24% |
| Blend | Base | 3.044.125 | 456.768 | +65% |
| Blend | Otimista | 3.805.156 | 745.959 | +107% |
| Performance | Base | 3.199.875 | 515.952 | +74% |
| Momentos | Base | 3.113.250 | 483.035 | +69% |
| Alcance | Base | 2.459.625 | 234.658 | +34% |

Leitura: nas linhas do Blend, o piso (Conservador) já é positivo, +24% de ROMI, e o intervalo até o Otimista é largo mas sempre acima de zero. Nas linhas de Base, Performance entrega o maior ROMI isolado (+74%), o que confirma o custo assumido de propósito ao escolher o Blend (+65%) em nome de risco e território, conforme T4. A matriz integral das 36 combinações de estratégia por tier por cenário está em `model/model.json`.

## T8. Limitações declaradas

Fechamos pelo que o modelo não faz, porque um apêndice honesto precisa marcar suas próprias bordas.

- Os dados são sintéticos. Substituí-los pelos reais valida ou ajusta as magnitudes, não a lógica da cadeia de T5.
- ROAS e margem são premissas de entrada, não observações medidas. Todo o resultado herda a incerteza dessas duas escolhas.
- O modelo não estima canibalização de outros canais nem custos operacionais além da margem de contribuição. Ele mede retorno de marketing sobre margem incremental, e nada além disso.

---

*Leonardo Stonoga · RappiAds · JBP FOODSToGo 2025*
