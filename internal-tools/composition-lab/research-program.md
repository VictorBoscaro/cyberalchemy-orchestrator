---
artifact_kind: research-program
status: active
last_updated: 2026-08-13
---

# Programa de pesquisa sobre composição

## Estado atual

- **Evidência externa aceita:** dois mapas de precedentes — estruturas formais e sistemas de
  engenharia — e uma comparação adversarial. A síntese passou por revisão independente.
  ([findings](research/external-composition-precedents/comparison/findings.md);
  [aceitação](research/external-composition-precedents/comparison/review.md))
- **Evidência interna aceita, ainda parcial:** D1 cobre três documentos de `domainspec-v2` e foi
  aceito como um lote interno limitado. Ele não representa o repositório nem permite classificar
  composição. ([findings](research/internal-composition-uses/runs/d1-domainspec-research-structure/accepted-rerun/findings.md);
  [aceitação](research/internal-composition-uses/runs/d1-domainspec-research-structure/accepted-rerun/review.md))
- **Decisões de produto e arquitetura:** nenhuma está autorizada por esta pesquisa.

O status `active` qualifica este programa de pesquisa. Ele não ratifica o internal tool, que
permanece `proposed` no README, nem uma teoria, interface ou autoridade para composição.

## O problema

O projeto quer permitir que pessoas formem maneiras de trabalhar a partir de skills, interfaces,
artefatos, tarefas, conhecimento e agentes. Ainda não sabemos o que torna essa formação uma
composição, em vez de agregação, sequência, configuração, integração, coordenação ou uma
interpretação posterior de que as partes formam um todo.

Sem essa distinção, podemos generalizar um padrão local, construir uma interface para uma ideia mal
definida ou atribuir ao conjunto efeitos que vieram de uma parte, do ambiente ou do sintetizador.

## Pergunta geral

> Como a composição acontece, quais diferenças a separam de fenômenos vizinhos, o que ela produz,
> preserva ou perde e como devemos representá-la e avaliá-la sem exceder a evidência?

A resposta pode ser um mecanismo comum, uma família de mecanismos ou a conclusão de que alguns usos
do termo devem permanecer separados.

## Caso 1: composição de lentes

O programa investigará como **hipótese** se práticas associadas a lentes — distribuir perspectivas,
controlar informação, confrontar resultados e sintetizar tensões — realizam composição. Isso ainda
não é uma classificação do repositório. Lentes são o primeiro caso por oferecerem um corpus local
para teste; não são sinônimo nem modelo geral de composição.

## O que a pesquisa externa sustenta

**Sustentado:** as fontes aceitas descrevem operações e relações diferentes para formar, admitir,
conectar, resolver, interpretar ou verificar totalidades. Elas não estabelecem uma operação compartilhada
nem uma teoria geral de composição.

**Caveat:** as recorrências são condicionadas pela seleção do corpus e pelo schema usado para
coletá-lo. Sua presença não demonstra prevalência independente entre domínios.

**Restrições candidatas:** sob esse limite, nos casos admitidos, copresença não basta; combinações
dependem de alguma relação de admissibilidade; falhas ajudam a distinguir operações; afirmações
sobre o todo exigem evidência adicional; e preservação precisa nomear uma propriedade e suas
condições. Servem como campos de investigação, não como universais.

**Transferências rejeitadas:** “interface” não nomeia um único objeto; composição não equivale a
dependência, conexão, configuração, resolução, integração ou coordenação; leis formais não migram
por semelhança; emergência não é um resultado comum; formação, execução e avaliação não são um só
evento.

Esses limites e afirmações estão documentados na
[síntese externa aceita](research/external-composition-precedents/comparison/findings.md). O
[review](research/external-composition-precedents/comparison/review.md) registra apenas sua
aceitação, não funciona como fonte da evidência.

## O que D1 sustenta

Nos três documentos examinados, D1 encontrou cinco observações locais sobre o que está
**declarado ou configurado**: uma progressão dirigida entre unidades e artefatos, sem execução
registrada nesses bytes; o problema subjacente como invariante pretendido entre duas lanes; um
join que pretende reter adjudicação e resíduo, em vez de apenas agregar resultados; autoridade
separada entre decisões locais e promoção posterior; e observabilidade enumerada, mas não
instanciada por eventos ou receipts concluídos.

Isso torna inspecionáveis handoffs, claims de preservação, limites de autoridade e a diferença
entre estrutura projetada e efeito observado. Não demonstra que preservação ocorreu, que o
workflow funciona ou que lanes ou lentes sejam composição. Os
[findings aceitos de D1](research/internal-composition-uses/runs/d1-domainspec-research-structure/accepted-rerun/findings.md)
são a evidência; o [review](research/internal-composition-uses/runs/d1-domainspec-research-structure/accepted-rerun/review.md)
registra somente `PASS / KEEP`.

## Vocabulário provisório de comparação

Os termos abaixo são campos para descrever e contrastar casos. Não são componentes obrigatórios de
uma definição:

- unidade participante;
- tipo de resultado;
- tipo de operação;
- relação de admissibilidade;
- ambiente ou estado;
- estágio da evidência: admitido, formado/configurado, realizado/executado ou avaliado;
- invariante ou efeito alegado;
- limite de falha;
- resíduo ou recuperabilidade.

## O que permanece desconhecido

- se os casos externos formam uma família, várias famílias incompatíveis ou apenas um conjunto útil
  para comparação;
- se as identidades das partes precedem a composição ou são transformadas por ela;
- quando ordem e agrupamento alteram o resultado;
- o que é perdido, preservado ou recuperável;
- quando uma novidade do todo é produzida pela interação, em vez de selecionada, agregada, executada
  ou atribuída;
- se e como esses campos aparecem nas demais práticas do repositório, além das declarações e
  configurações locais observadas em D1;
- se execuções, traces, receipts ou outputs observados confirmam, alteram ou contradizem a
  estrutura declarada em D1.

## Gates de decisão deferidos

1. **Unidade conceitual:** decidir se “composição” será um modelo comum, uma família tipada ou termos
   separados. Uma escolha errada criaria falsa interoperabilidade entre fenômenos incompatíveis ou
   impediria comparação entre casos relacionados.
2. **Representação:** decidir o que precisa tornar explícito sobre partes, operação,
   admissibilidade, ambiente, estágio, preservação, perda e falha. Uma escolha errada apagaria
   causalidade, perda ou condições necessárias à interpretação do resultado.
3. **Evidência sobre o todo:** decidir quais alegações exigem prova, execução, observação ou
   julgamento. Uma escolha errada confundiria formação com realização ou validação.
4. **Autoridade:** decidir onde residem admissão, execução, avaliação e revisão, inclusive se uma
   ferramenta externa deve coordená-las. Uma escolha errada centralizaria autoridade que pertence
   ao domínio ou ao usuário, ou deixaria responsabilidades sem owner.

Nenhum gate está resolvido. Eles só podem avançar quando evidência comparável permitir declarar o
que cada alternativa preserva, perde e impede.

## Próximo passo

Selecionar, obter e aprovar o próximo lote interno comparável, sem pressupor agora qual corpus o
fornecerá. D1 é o primeiro lote aceito, mas não completa nem avança sozinho qualquer gate de
decisão. Ampliar a pesquisa externa pode ocorrer em paralelo, mas não substitui a cobertura interna.
A rota de execução interna segue operacionalmente bloqueada, e os harnesses e snapshots rejeitados
não devem ser reabertos como parte deste passo.

**Condição de saída:** corpus e revisão identificam explicitamente lentes, skills, workflows,
artefatos/conhecimento, interfaces e `domainspec-v2`; preservam casos positivos, negativos e
incertezas; não predeterminam a classificação pelo vocabulário externo; e recebem review
independente `KEEP`.

## Disciplina de atualização

Este arquivo é o núcleo curto e legível do programa. Cada atualização deve distinguir o que foi
observado, sustentado, inferido, hipotetizado ou deixado desconhecido. Evidência bruta, matrizes,
citações e controles permanecem nos respectivos artefatos de pesquisa. Findings aceitos de uma
linha podem entrar como resultados limitados àquela linha; afirmações cruzadas ou gerais exigem
comparação interna–externa. Reviews registram aceitação ou pedidos de mudança.
