---
artifact_kind: research-advice
status: proposed
scope: next-internal-research
date: 2026-08-13
---

# Parecer — próxima pesquisa interna sobre composição

## Recomendação

Executar uma **pesquisa comparativa interna de ocorrências e alegações de composição no
repositório**. A composição de lentes será o caso-âncora porque já possui prescrições, configurações
e alguns traços preservados, mas deverá ser contrastada desde o início com composições de skills,
workflows, artefatos/conhecimento e interfaces de software.

O objetivo não é definir composição por indução lexical nem transformar o padrão de agentes em
modelo universal. É descobrir quais diferenças o próprio repositório trata como composicionais,
quais operações estão realmente demonstradas e quais supostos mecanismos comuns sobrevivem quando
aplicados a casos não-lente e a controles negativos.

## Pergunta única

> Quais formas de composição o repositório declara ou realiza em lentes, skills, workflows,
> artefatos/conhecimento e interfaces; quais relações ou transformações reaparecem entre esses
> domínios; e quais alegadas propriedades comuns colapsam em agregação, sequência, configuração,
> coordenação, integração ou simples interpretação posterior?

Essa pergunta deve ser registrada em uma nova `research-initial-definitions.md` local antes do
desenho do dispatch. As definições gerais existentes continuam sendo contexto; o programa antigo de
“modelo observável da composição de lentes” não deve continuar como autoridade de escopo.

## Corpus interno recomendado

Congelar manifest com commit/digest, path e hash. Usar fontes canônicas quando houver cópias
geradas; duplicatas em `.agents`, `.codex` e `.claude` não contam como casos independentes.

1. **Caso-âncora — lentes e perspectivas em agentes**
   - `telemetry/agents/subagents-dispatch.yaml`;
   - skills `research`, `review`, `robot-talks`, `experiment` e estratégia de subagentes;
   - sessões `**/robot-talks/**`, reviews persistidos e outputs ligados ao ledger;
   - `docs/features/agent-provenance-telemetry/**`.
2. **Composição de capabilities e modos de trabalho**
   - `.agents/skills/paired-views/SKILL.md`;
   - `.agents/skills/repository-harness/SKILL.md`;
   - `.agents/skills/ontology-harness/SKILL.md`;
   - `.agents/skills/observed-invocation-loop/SKILL.md`;
   - `.agents/skills/spellcraft/SKILL.md` e `.agents/skills/invoke/SKILL.md`;
   - runs ou artefatos produzidos por essas composições, quando existirem.
3. **Composição de artefatos e conhecimento**
   - `docs/temps/operational-knowledge-language/README.md` e seus casos preservados;
   - `vault/essays/evaluating-text-as-composition.md`;
   - ontologias, pares de views e grafos que afirmem integrar ou projetar conhecimento;
   - internal tools com documentos ou pacotes formados a partir de partes.
4. **Composição de software, interfaces e execução**
   - `docs/discovery/workflow-graph/workflow-graph.md`;
   - `docs/features/skill-control-center/architecture.md`;
   - `docs/features/agents-communication-infra/IMPLEMENTATION-LAYERING.md`;
   - implementações, fixtures e testes que permitam separar arquitetura prescrita de acoplamento
     executado.
5. **Controles negativos obrigatórios**
   - listas, catálogos ou registries sem relação entre itens;
   - concatenação de outputs;
   - sequência de etapas sem transformação ou contribuição ao todo demonstrável;
   - co-localização em uma pasta ou pacote;
   - configuração compatível que nunca foi executada;
   - uso puramente retórico das palavras `composition`, `compose` ou `composed`.

Não fazer censo de todo arquivo que contém a palavra “composição”. Fazer máxima variação
determinística por estrato e ampliar a amostra somente quando um novo caso adiciona uma operação,
uma falha ou um limite ainda não representado.

## Perspectivas e concerns

Usar quatro explorers independentes; cada um guarda uma diferença epistemológica, não apenas uma
pasta:

1. **Forma declarada:** quais partes, interfaces, regras, objetivos e relações são afirmados; não
   infere execução.
2. **Realização e transformação:** que traços mostram instanciação, interação, mudança, passagem de
   estado, contribuição ou formação de um todo; não infere causalidade.
3. **Travessia entre domínios:** testa cada mecanismo candidato em lentes e em casos não-lente,
   registrando invariantes aparentes e limites de transferência.
4. **Colapso e contracasos:** procura agregação, sequência, configuração, coordenação, integração,
   duplicação e interpretação posterior que possam explicar o caso sem invocar composição.

Depois: um writer único cruza os retornos; três skeptics separados aplicam `precedent` interno,
`non-vacuity` e `definitional-soundness`; um auditor downstream verifica corpus, citações,
duplicatas e extrapolações. O precedente acadêmico ou industrial amplo pertence à pesquisa externa,
não deve ser simulado por este corpus.

## Hipóteses a desafiar

Estas são candidatas concorrentes, não definições iniciais:

- **H1 — interface/relação:** diferenças tornam-se composição quando são conectadas por uma
  interface ou regra válida orientada a um todo.
- **H2 — transformação:** só há composição quando a relação transforma ao menos partes, estados,
  possibilidades ou resultados; mera compatibilidade não basta.
- **H3 — contribuição ao todo:** há composição quando contribuições das partes ao todo são
  distinguíveis e sua remoção ou substituição muda alguma propriedade relevante.
- **H4 — fechamento contextual:** composição é um julgamento situado de que um conjunto funciona
  como unidade para certo objetivo, e não uma propriedade intrínseca universal.
- **H5 — família, não essência:** lentes, skills, textos e software realizam mecanismos diferentes;
  “composição” pode nomear uma família com semelhanças parciais, não um kernel único.
- **H0 — colapso:** os casos do repositório podem ser explicados adequadamente por configuração,
  encadeamento, integração, coordenação, agregação ou seleção, tornando “composição” um rótulo sem
  trabalho próprio em parte ou em todo o corpus.

Cada hipótese só pode sobreviver provisoriamente se tiver: uma testemunha concreta, um não-exemplo,
um vizinho conceitual, um collapse-test e suporte em pelo menos dois estratos, dos quais um não pode
ser lentes. Frequência lexical, `resolved` e presença de múltiplos agentes não são testemunhas.

## Outputs

Conforme a skill `research`, com `n >= 2`:

- `research-initial-definitions.md` local, produzido antes do dispatch;
- `research.md`, com retornos preservados verbatim;
- `findings.md`, com:
  - manifest e protocolo de amostragem;
  - tabela de casos e controles por estrato;
  - separação entre alegado, prescrito, configurado, executado e efeito observado;
  - operações/relações observadas sem promoção ontológica;
  - matriz hipótese → testemunha → contracaso → collapse-test → estado;
  - matriz canônica de verdicts da pesquisa;
  - diferenças específicas de lentes versus candidatas a atravessar domínios;
  - seção final “mudanças justificadas no documento progressivo”.

Não criar ainda schema, UI, runtime, taxonomia canônica ou produto. O output é base de evidência e
hipóteses provisórias.

## Gates

1. **Gate de escopo:** a initial definition local afirma que composição geral é o objeto e lentes
   são caso-âncora, não fundamento universal.
2. **Gate de corpus:** manifest congelado, fontes canônicas identificadas, duplicatas controladas e
   ao menos quatro estratos mais controles negativos.
3. **Gate de evidência:** alegação, prescrição, configuração, execução e efeito não são promovidos
   uns aos outros por inferência.
4. **Gate comparativo:** nenhuma propriedade é chamada de transversal sem testemunha em lentes e
   em ao menos um domínio não-lente; casos ausentes ficam como lacuna.
5. **Gate de não-vacuidade:** toda hipótese sobrevivente possui testemunha e consequência
   observável; ausência produz `KILL/no-witness` tipado.
6. **Gate definicional:** se um mecanismo não se distingue de um vizinho já nomeado, registrar
   `KILL/tautological`, sem resgatá-lo por nova terminologia.
7. **Gate de rastreabilidade:** toda claim load-bearing em `findings.md` aponta para o retorno
   coletado e para `path:line` da fonte.
8. **Gate de escrita:** nenhum achado entra no documento progressivo antes de aceitação independente
   do bundle interno e confronto com o que a pesquisa externa sustenta.

## Relação com o documento progressivo

O documento principal deve ser curto, objetivo e orientado ao leitor; não deve virar depósito de
notas de pesquisa. Recomendo uma estrutura estável:

1. problema e relevância;
2. o que chamamos provisoriamente de composição;
3. distinções necessárias;
4. como o repositório compõe hoje;
5. o caso de lentes;
6. hipóteses sobre mecanismos gerais;
7. evidência, limites e perguntas abertas;
8. próximos experimentos e implicações possíveis.

Cada pesquisa preserva seus próprios `research.md` e `findings.md`. Um writer downstream, que não
foi explorer nem approver, atualiza somente as seções afetadas a partir da seção “mudanças
justificadas”, mantendo em cada claim o estado `observado`, `inferido`, `hipótese` ou `não
sustentado`. Descobertas negativas e limites entram no texto; detalhes de corpus e matrizes ficam
nos artefatos de pesquisa e são apenas citados.

## Riscos

- **Primazia das lentes:** o caso mais rico passa a definir as categorias dos demais. Mitigar com
  explorer transversal, testemunha não-lente obrigatória e H5/H0.
- **Busca lexical:** arquivos que usam o termo dominam práticas que compõem sem nomeá-lo. Mitigar
  com amostragem por estrutura e outputs, não apenas por palavra.
- **Doutrina auto-confirmatória:** textos conceituais do repo validam a própria teoria. Tratar esses
  textos como alegação; execução e efeitos exigem outros traços.
- **Confusão entre composição projetada e realizada:** separar os níveis de evidência por linha.
- **Duplicação de fontes geradas:** declarar canonicidade e identidade do caso no manifest.
- **Corpus excessivo:** máxima variação e saturação de operações, sem reivindicar saturação do repo.
- **Síntese inventa relações:** preservar retornos independentes e exigir citação para cada relação
  criada pelo writer.
- **Generalização prematura:** nenhuma conclusão transversal sai deste estudo sozinha; ela precisa
  sobreviver também aos owners e contraexemplos da pesquisa externa.

## Ordem recomendada

1. Atualizar o objetivo do programa e criar a initial definition local desta pesquisa.
2. Congelar corpus, identidade dos casos, controles e fontes canônicas.
3. Executar a pesquisa interna comparativa.
4. Executar a pesquisa externa como dispatch separado, usando a mesma pergunta de fronteira, sem
   deixar a taxonomia externa reclassificar retroativamente o corpus interno.
5. Fazer uma síntese cruzada independente: convergências, conflitos, empréstimos com owner e limites
   de transferência.
6. Atualizar a primeira versão do documento progressivo.
7. Somente então decidir Robot-Talks, experimentos ou uma formalização mais forte a partir das
   tensões que permanecerem.

As pesquisas interna e externa podem ser preparadas em paralelo, mas a síntese e a atualização do
documento devem esperar os dois bundles. Se houver pressão para executar em sequência, a interna
vem primeiro porque revela quais usos e ambiguidades do projeto a externa precisa explicar, e não
apenas quais teorias de composição estão disponíveis.

