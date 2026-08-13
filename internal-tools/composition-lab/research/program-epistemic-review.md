# Review epistemológico — `research-program.md`

## Escopo e cobertura

| lente | alvo verificado | resultado |
|---|---|---|
| força dos claims | programa contra a síntese externa aceita | Um claim interno excede o corpus autorizado. |
| condicionamento por seleção/schema | uso das recorrências externas | O caveat existe, mas aparece depois do primeiro uso agregado das recorrências. |
| separação externa/interna | estado, Caso 1 e próximos passos | A separação é explícita, salvo pela caracterização factual das lentes. |
| estatuto do vocabulário | campos comparativos | Preservado como provisório; nenhum campo virou definição ou requisito. |
| deferimento decisório | produto, arquitetura e classificação | Preservado. |
| papel do review | citações da aceitação | Preservado: o review é citado apenas como registro de aceitação. |
| negativos e incompatibilidades | transferências rejeitadas e desconhecidos | Preservados sem conversão em convergência. |

O corpus desta revisão foi estritamente `research-program.md`,
`research/external-composition-precedents/comparison/findings.md` e a verificação final em
`research/external-composition-precedents/comparison/review.md`. Nenhum achado interno foi usado ou
presumido.

## Findings priorizados

| # | arquivo | evidência (citação do alvo) | severidade | correção proposta |
|---|---|---|---|---|
| 1 | `internal-tools/composition-lab/research-program.md` | “O repositório trata como composição de lentes práticas de distribuir perspectivas, controlar informação, confrontar resultados e sintetizar tensões.” | MAJOR | Reescrever como hipótese ou objeto de investigação atribuído ao programa, sem afirmar o que o repositório faz, até existirem findings internos aceitos. Preservar que lentes são o primeiro caso, mas não uma classificação já demonstrada. |
| 2 | `internal-tools/composition-lab/research-program.md` | “**Restrições candidatas:** nos casos admitidos, copresença não basta; combinações dependem de alguma relação de admissibilidade; falhas ajudam a distinguir operações; afirmações sobre o todo exigem evidência adicional; e preservação precisa nomear uma propriedade e suas condições. Essas recorrências são condicionadas pela seleção do corpus e pelo schema usado para coletá-lo.” | MAJOR | Antepor o caveat de seleção/schema à enumeração das recorrências, como faz a síntese aceita, e então apresentá-las explicitamente como restrições candidatas condicionadas. |

## Controles que passaram

- A evidência externa e a ausência de evidência interna aceita estão declaradas separadamente.
- O vocabulário é apresentado como campo comparativo, não como definição ou componente
  obrigatório.
- Definição geral, schema, runtime, UI, ferramenta e classificação interna permanecem deferidos.
- O programa declara corretamente que o review registra aceitação e não fornece a evidência.
- Permanecem explícitas as incompatibilidades entre interface, dependência, conexão,
  configuração, resolução, integração e coordenação; também permanecem bloqueadas a
  transferência de leis formais e a generalização de emergência.
- Os desconhecidos sobre família comum, identidade das partes, ordem, agrupamento, perda,
  recuperabilidade e novidade do todo foram preservados.

## Veredito

**FIX.** O programa preserva quase todos os limites epistemológicos da síntese externa aceita,
mas os dois findings MAJOR precisam ser corrigidos: um evita uma classificação interna antes da
evidência e o outro faz o condicionamento metodológico governar as recorrências antes de seu uso.

`exit_reason: resolved-with-change-requests`  
`agents_spawned: 0`

---

## Re-review estreito — 2026-08-13

### Escopo

Verificação limitada aos dois findings MAJOR anteriores e a possíveis regressões
epistemológicas introduzidas nos quatro gates deferidos e no próximo passo. O programa não foi
editado por esta revisão.

### Correções verificadas

- **MAJOR 1 resolvido.** O Caso 1 agora diz que o programa investigará “como **hipótese**” as
  práticas associadas a lentes e explicita: “Isso ainda não é uma classificação do
  repositório.” Nenhum finding interno foi presumido.
- **MAJOR 2 resolvido.** O caveat de seleção/schema agora antecede as recorrências e afirma que sua
  presença “não demonstra prevalência independente entre domínios”. As recorrências continuam
  qualificadas como restrições candidatas e não universais.

### Gates e próximo passo

- Os quatro gates permanecem perguntas de decisão deferidas. A enumeração de partes, operação,
  admissibilidade, ambiente, estágio, preservação, perda e falha aparece como objeto do que ainda
  deve ser decidido, não como definição ou conjunto obrigatório.
- As consequências dos gates estão formuladas como riscos de escolhas erradas, não como leis gerais
  demonstradas pela pesquisa externa.
- O próximo passo pede findings internos comparáveis e review independente sem usar o vocabulário
  externo para predeterminar a classificação. A condição de saída exige positivos, negativos e
  incertezas.
- A afirmação de que a rota interna está operacionalmente bloqueada e de que harnesses/snapshots
  foram rejeitados registra estado de execução do programa; não classifica uma prática interna
  como composição nem produz uma generalização externa.

### Veredito final

**PASS / KEEP.** Os dois findings anteriores estão resolvidos. Nenhum claim interno sobre
composição, universalismo indevido ou conversão dos campos candidatos em requisitos foi
introduzido pelos gates ou pelo próximo passo.

`exit_reason: resolved`  
`agents_spawned: 0`
