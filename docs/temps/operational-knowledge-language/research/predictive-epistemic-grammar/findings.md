# Findings finais — gramática epistemológica preditiva

## Pergunta de pesquisa

> Em que condições, se alguma, a gramática epistemológica provisória permite antecipar distinções,
> rupturas, resíduos, probes úteis ou consequências estruturais antes da observação relevante, de
> modo que sua contribuição possa ser distinguida de reinterpretação retrospectiva e de alternativas
> mais simples?

## Resposta de uma linha

**No estado atual, a gramática é uma linguagem integradora e heurística, não uma teoria preditiva incremental.**

## Resultado dos gates

O gate de non-vacuity encontrou witnesses formais ou operacionais para seis candidatos, mas nenhum
witness de vantagem incremental sobre os baselines; três candidatos receberam NO-WITNESS
([retorno non-vacuity](./research.md#retorno-verbatim--skeptic-non-vacuity)). O gate de
definitional-soundness preservou como SOUND somente a seleção de probe guiada por perfil residual;
os outros oito candidatos são TAUTOLOGICAL em sua formulação corrente
([gate definitional-soundness](./research.md#gate-definitional-soundness)).

Nenhum candidato sobrevive aos dois gates. Isto produz um **confirmed-kill early-stop**: os KILLs
abaixo decorrem somente de no-witness ou tautological. A existência de owners determina
procedência e use-mode; não é motivo de KILL.

## Matriz final

| candidate | owner | witnessed? | sound? | verdict | use-mode |
|---|---|---|---|---|---|
| Seleção de probe guiada por perfil residual | Bayesian experimental design; active learning; Blackwell comparison | **no** — negativo fechado sob paridade de informação | **yes**, condicional à independência de ρ | **KILL — no-witness** | build-from-owned; reabrir somente sob restrição computacional/representacional e paridade de informação |
| Discriminador de enriquecimento e limite expressivo | reduct/expansion; forgetful structure; invariantes; definability/ablation | **yes** — witness do fenômeno, não de ganho incremental | **no — tautological** | **KILL — tautological** | build-from-owned como teste de expressividade/estrutura esquecida |
| Falha composicional/local–global | assume-guarantee; compositional verification; CSP; sheaf obstructions; system dynamics | **yes** — witness do fenômeno, não de ganho incremental | **no — tautological** | **KILL — tautological** | build-from-owned, escolhendo o owner específico do domínio |
| Ruptura de analogia | structure-mapping; metamorphic/property testing | **yes** — witness de falha composicional, não de ganho incremental | **no — tautological** | **KILL — tautological** | build-from-owned como obrigação de preservação testável |
| Fronteira minimalidade–generatividade–residualidade | MDL; rate-distortion; information bottleneck; Pareto/bias–variance | **no** | **no — tautological** | **KILL — no-witness; tautological** | build-from-owned apenas como trade-off de complexidade e perda |
| Enriquecimento prospectivo por risco | FMEA; hazard analysis; causal risk assessment | **yes** — witness temporal, não de ganho incremental | **no — tautological** | **KILL — tautological** | build-from-owned como análise prospectiva de risco |
| Diagnóstico residual e classe de reparo | diagnóstico diferencial; root-cause analysis; fault trees; ablation | **yes** — witness de perda por transformação, não de ganho incremental | **no — tautological** | **KILL — tautological** | build-from-owned como diagnóstico/round-trip; subsumido à seleção de teste |
| Limite reflexivo/diagonalização | Lawvere; Gödel; Turing; esquemas clássicos de fixed point | **no** | **no — tautological** | **KILL — no-witness; tautological** | build-from-owned somente após satisfazer as hipóteses formais do owner |
| Prediction ledger | preregistration; Registered Reports; criterion congelado do repositório | **yes**, metodológico somente | **no — tautological como contribuição preditiva** | **KILL — tautological como candidato teórico** | already-deployed como controle auxiliar; não atribuir poder preditivo ao ledger |

## Typed negatives

### 1. Seleção de probe guiada por perfil residual

**O que teria contribuído:** uma variável incremental que, mantendo iguais hipóteses, informação,
probes, custos e orçamento, restringisse a política e melhorasse discriminação, decisão ou custo.

**Fato que a zerou — no-witness:** para input congelado D, se ρ(D) é derivável de D,
qualquer política π(D,ρ(D)) pode ser reproduzida por π′(D); se ρ não é derivável, o
treatment recebeu informação adicional e a comparação não isola a gramática
([negativo fechado](./research.md#1-seleção-de-probe-guiada-por-perfil-residual--no-witness)).

**Única reabertura legítima:** congelar uma restrição computacional, representacional ou de
amostragem sob a qual ρ seja uma compressão operacional de D; comparar políticas com a
**mesma informação bruta, orçamento e probes admissíveis**; demonstrar ganho que desaparece na
ablação de ρ. Sem essa paridade, não há reabertura.

### 2. Discriminador de enriquecimento e limite expressivo

**O que teria contribuído:** uma regra própria da gramática que escolhesse antecipadamente uma
classe estritamente menor de enriquecimentos e previsse qual estrutura quebraria a equivalência.

**Fato que o zerou — tautological:** na formulação atual, restaurar estrutura esquecida e testar
um invariante dependente dela é exatamente reduct/expansion, forgetful structure e definability; a
gramática não fornece regra própria para selecionar E
([witness formal](./research.md#2-discriminador-de-enriquecimentolimite-expressivo--witnessed);
[gate soundness](./research.md#gate-definitional-soundness)).

### 3. Falha composicional/local–global

**O que teria contribuído:** uma transformação comum e tipada que preservasse semânticas locais e
antecipasse qual interface ou obrigação global falharia, ou selecionasse o formalismo apropriado.

**Fato que a zerou — tautological:** “partes passam localmente, composição falha globalmente” já
é o problema dos owners; nomear o contraexemplo ou obstrução como resíduo não acrescenta regra
([witness formal](./research.md#3-falha-composicionallocalglobal--witnessed);
[gate soundness](./research.md#gate-definitional-soundness)).

### 4. Ruptura de analogia

**O que teria contribuído:** uma assinatura independente que restringisse região e tipo de ruptura
para além das correspondências e leis de preservação declaradas.

**Fato que a zerou — tautological:** structure-mapping acompanhado de teste
metamórfico/property-based já contém correspondência, obrigação de preservação e witness de
violação; “resíduo de analogia” apenas renomeia a falha
([witness](./research.md#4-ruptura-de-analogia--witnessed);
[gate soundness](./research.md#gate-definitional-soundness)).

### 5. Fronteira minimalidade–generatividade–residualidade

**O que teria contribuído:** uma quantidade ou lei adicional que previsse mudança de regime fora da
amostra e não fosse redutível a complexidade versus perda/relevância.

**Fatos que a zeraram — no-witness e tautological:** não existem gerador, métricas, curvas,
tarefas retidas ou replicação congelados; além disso, a formulação corrente é o trade-off já
possuído por MDL, rate-distortion e information bottleneck
([gate non-vacuity](./research.md#5-fronteira-minimalidadegeneratividaderesidualidade--no-witness);
[gate soundness](./research.md#gate-definitional-soundness)).

### 6. Enriquecimento prospectivo por risco

**O que teria contribuído:** uma regra derivada do kernel que selecionasse estrutura prospectiva e
alterasse uma decisão além do que produz análise de risco com as mesmas informações.

**Fato que o zerou — tautological:** introduzir tempo, causalidade ou outra estrutura antes de
ação arriscada por causa de mecanismo omitido já é FMEA/hazard/causal risk assessment
([witness temporal](./research.md#6-enriquecimento-prospectivo-por-risco--witnessed);
[gate soundness](./research.md#gate-definitional-soundness)).

### 7. Diagnóstico residual e classe de reparo

**O que teria contribuído:** um mapa transportável e pré-declarado
tipo residual -> causas próprias -> classe própria de intervenção que reduzisse busca sob
informação e custos igualados.

**Fato que o zerou — tautological:** usar sintomas para reduzir causas e selecionar o próximo
teste é diagnóstico ordinário; nenhum mapa próprio liga hoje os eixos residuais a reparos
([witness round-trip](./research.md#7-diagnóstico-residual-e-classe-de-reparo--witnessed);
[gate soundness](./research.md#gate-definitional-soundness)).

### 8. Limite reflexivo/diagonalização

**O que teria contribuído:** uma limitação específica derivada de objetos, avaliação,
autorrepresentação e mapas construídos internamente pela gramática.

**Fatos que o zeraram — no-witness e tautological:** o corpus não fornece sistema que satisfaça
as hipóteses formais, e o enunciado disponível é apenas o conteúdo dos teoremas clássicos
renomeado como resíduo reflexivo
([gate non-vacuity](./research.md#8-limite-reflexivodiagonalização--no-witness);
[gate soundness](./research.md#gate-definitional-soundness)).

### 9. Prediction ledger

**O que teria contribuído:** controle prospectivo contra reconstrução retrospectiva; nunca, por si,
poder preditivo.

**Fato que o zerou como candidato teórico — tautological:** preregistration, Registered Reports e
criterion congelado já desempenham essa função. O ledger sobrevive somente como infraestrutura
already-deployed; as regras registradas, não o registro, teriam de carregar qualquer contribuição
([witness metodológico](./research.md#9-prediction-ledger--witnessed-metodológico-somente);
[gate soundness](./research.md#gate-definitional-soundness)).

## Ativos preservados

O early-stop mata a alegação de **teoria preditiva incremental no estado atual**, não o uso dos
mecanismos encontrados. Permanecem reutilizáveis, com atribuição explícita:

- criterion preregistrado e preservação de negativos — already-deployed;
- CEGAR e abstração/refinamento;
- Bayesian design, active learning e comparação informacional;
- causal models para intervenção;
- structure-mapping e metamorphic testing;
- assume-guarantee, CSP e sheaf obstructions;
- system dynamics;
- MDL, rate-distortion e information bottleneck;
- invariantes e property-based testing;
- teoremas de Lawvere/Gödel/Turing quando suas hipóteses forem satisfeitas.

Esses ativos sustentam build-from-owned e podem fortalecer a gramática como interface integradora,
heurística editorial e disciplina de investigação. Não sustentam, sem resultado adicional, novidade
ou poder preditivo incremental.

## Encerramento

**Confirmed-kill early-stop:** nenhum candidato é simultaneamente witnessed e sound. O resultado
negativo é resolvido, informativo e preservado; uma nova rodada só se justifica pela reabertura
restrita do candidato de probe descrita acima, não por renomeação dos candidatos mortos.
