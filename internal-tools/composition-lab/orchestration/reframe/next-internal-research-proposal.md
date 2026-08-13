---
artifact_kind: research-advice
status: proposed
track: internal
last_updated: 2026-08-13
---

# Proposta — pesquisa interna comparativa sobre composição

> **Parecer pré-design:** recomenda o recorte da próxima pesquisa, mas não é um dispatch pronto
> para confirmação. A `research-initial-definitions.md` local deve ser criada e aceita antes que
> corpus, perspectivas, hipóteses, outputs e gates sejam reemitidos como desenho governado.

## Pergunta

> Quais formas de composição o repositório declara ou realiza em lentes, skills, workflows,
> artefatos/conhecimento e interfaces; o que reaparece entre esses domínios; e o que colapsa em
> agregação, sequência, configuração, integração, coordenação ou interpretação posterior?

## Corpus

Congelar manifest com commit/digest, path, hash e identidade do caso. Cobrir por máxima variação:

- lentes: ledger, skills de multiagentes, Robot-Talks, reviews e outputs preservados;
- capabilities: `paired-views`, harnesses, `spellcraft`, `invoke` e runs disponíveis;
- artefatos/conhecimento: operational knowledge language, ontologias, views e textos compostos;
- interfaces/software: workflow graph, arquiteturas, implementações, fixtures e testes relevantes;
- controles: listas, concatenação, co-localização, sequência sem transformação, configuração não
  executada e uso apenas retórico de “composição”.

Fontes canônicas prevalecem sobre cópias geradas. A pesquisa não é um censo lexical.

## Perspectivas

Quatro explorers independentes:

1. forma declarada: partes, regras, interfaces, objetivos e relações;
2. realização: instanciação, interação, transformação, contribuição e traços do todo;
3. travessia: mecanismos que aparecem em lentes e em casos não-lente;
4. colapso: explicações suficientes por fenômenos vizinhos.

Depois: writer único; skeptics separados para precedent interno, non-vacuity e
definitional-soundness; auditor downstream para corpus, duplicatas, citações e extrapolações.

## Hipóteses a desafiar

- interface ou regra válida basta para composição;
- transformação é necessária;
- contribuição marginal de partes caracteriza o todo;
- composição é um julgamento situado por objetivo;
- os domínios formam uma família, não uma essência única;
- “composição” não acrescenta trabalho explicativo ao vocabulário já existente.

## Outputs

Em `research/composition-internal-comparison/`:

- `research-initial-definitions.md` antes do desenho final do dispatch;
- `research.md` com retornos preservados;
- `findings.md` com manifest, casos e controles, níveis de evidência, operações observadas, matriz
  de hipóteses e verdicts, diferenças específicas de lentes, candidatos transversais e mudanças
  justificadas para o documento progressivo.

## Gates

- composição geral é o objeto; lentes são apenas o caso-âncora;
- alegado, prescrito, configurado, executado e efeito observado permanecem separados;
- nenhum candidato transversal avança sem testemunha não-lente;
- cada hipótese tem witness, não-exemplo, vizinho e collapse-test;
- toda claim load-bearing aponta ao retorno coletado e ao `path:line` original;
- findings não editam diretamente `research-program.md`.

## Relação com o documento progressivo

O bundle aceito fornece a seção factual “como o repositório compõe hoje”, os limites do caso de
lentes e candidatos — ainda não conclusões gerais — para comparação com precedentes externos.

## Gate humano seguinte

Antes da execução: aprovar pergunta, manifest inicial, identidades dos casos, perspectivas,
exclusões, topologia realizável e condição de parada. Esta proposta não autoriza o dispatch.
