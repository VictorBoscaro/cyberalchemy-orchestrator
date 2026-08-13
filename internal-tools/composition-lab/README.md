---
tags: [internal-tool, composition, research, experiments]
node_type: readme
layer: application, research
nature: reference
status: proposed
version: 0.2.0
last_updated: 2026-08-13
---

# Composition Lab *(nome provisório)*

> **Estado: incubação de pesquisa.** Ainda não existe uma teoria aceita, uma interface definida ou
> uma ferramenta executável. Este diretório separa e preserva a investigação antes que seus
> resultados sejam convertidos em arquitetura.

## O que é

Composition Lab é um internal tool em formação para investigar **como a composição acontece e como
ela deve ser tratada** quando pessoas formam maneiras de trabalhar a partir de materiais
heterogêneos: skills, interfaces, artefatos, tarefas, métodos e conhecimento. 

Seu primeiro trabalho não é oferecer um editor visual, um catálogo de componentes ou um motor de
workflow. É tornar a composição observável e investigável: distinguir fenômenos, formular
hipóteses concorrentes, construir casos e contracasos, executar experimentos e preservar o que as
evidências realmente sustentam.

O primeiro caso empírico é a **composição de lentes no trabalho de agentes**, porque o repositório
já preserva exemplos, prescrições e tensões desse uso. Esse caso inicia a investigação; não define
o campo. Qualquer mecanismo candidato a geral terá de ser confrontado com outros casos, como
skills, workflows, interfaces, artefatos e conhecimento.

O principal produto intelectual do laboratório será um documento progressivo, curto e legível,
que explique o problema, o que as pesquisas sustentam, o que permanece hipótese e quais decisões
se tornam possíveis. Evidência bruta, matrizes e pareceres permanecem em artefatos próprios.

## Por que está separado

O repositório já emprega composição em vários contextos, mas isso não demonstra que eles
compartilham uma única estrutura. Manter esta investigação em um internal tool próprio evita três
colapsos prematuros:

- reduzir composição à arquitetura do orquestrador existente;
- transformar uma definição provisória em contrato de produto;
- confundir coordenação, agregação ou configuração com composição antes de compará-las.

O diretório pode futuramente conter instrumentos de pesquisa e superfícies experimentais. Ele não
recebe autoridade sobre os demais internal tools apenas por estudar composição.

## Pergunta central

> Como a composição acontece, o que torna uma ocorrência genuinamente composicional e como a
> composição deve ser compreendida e tratada em sistemas que permitem formar maneiras de trabalhar?

A formulação é deliberadamente refinável. “Composição” ainda pode revelar-se uma operação, um
processo, uma relação, um julgamento, uma realização, uma família de fenômenos ou alguma combinação
dessas possibilidades.

## Modo de trabalho

O laboratório deverá manter separados:

1. contexto e restrições confirmadas;
2. precedentes e evidências coletadas;
3. hipóteses e seus testes de colapso;
4. experimentos, controles e resultados observados;
5. sínteses provisórias;
6. decisões posteriores de produto ou arquitetura.

Pesquisas internas e externas mantêm seus conceitos separados durante a coleta. Findings aceitos
são comparados antes de entrar no documento progressivo; discordâncias, negativos e limites de
transferência não são apagados pela síntese.

Uma hipótese bem formulada precisa poder perder. Um experimento precisa discriminar entre
explicações concorrentes, não apenas produzir uma demonstração atraente. Descobrir que um conceito
já tem dono é resultado positivo; descobrir que uma hipótese é vazia ou apenas renomeia outro
fenômeno também é resultado útil.

## Limites atuais

- Nenhum kernel, álgebra ou vocabulário de composição está ratificado.
- Nenhum domínio — software, trabalho, conhecimento, texto, música ou sistemas — é assumido como
  modelo universal dos demais.
- A ferramenta externa que eventualmente coordene composições permanece uma questão adjacente, não
  a resposta pressuposta por esta investigação.
- Protótipos futuros serão instrumentos para produzir evidência; sua existência não validará a
  teoria que os motivou.

## Estrutura

```text
composition-lab/
├── README.md
├── research-program.md
├── research/
│   ├── research-initial-definitions.md
│   └── milestone-1/                    # caso 1: composição de lentes
└── orchestration/
    └── reframe/                        # pareceres e propostas, não findings
```

O ponto de partida está em
[`research/research-initial-definitions.md`](research/research-initial-definitions.md). O programa
editorial e investigativo está em [`research-program.md`](research-program.md). Planos, evidências,
hipóteses, experimentos e findings permanecem artefatos distintos.
