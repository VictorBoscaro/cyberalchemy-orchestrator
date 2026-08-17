---
node_type: agent-dialogue
status: closed
date: 2026-08-17
topic: universal-artifact-schema-role
---

# Robot-Talks — papel universal de schema para artefatos

## Escopo aprovado

Investigar qual modelo geral permite governar qualquer artefato — conhecido ou ainda não tipado —
por meio de domínios abertos, schemas reutilizáveis, propriedades, relações e regras, servindo
simultaneamente humanos e agentes. Esta sessão audita tensões e produz recomendações; não implementa
mudanças no Schema Service.

## Pergunta central

Qual modelo geral permite governar qualquer artefato — conhecido ou ainda não tipado — por meio de
domínios abertos, schemas reutilizáveis, propriedades, relações e regras, servindo simultaneamente
humanos e agentes?

## Assunções a desafiar

- Todo artefato deve possuir alguma representação mínima governada.
- Domínios podem ser definidos conforme a necessidade.
- Tipos pertencem a domínios e podem possuir subtipos.
- Schemas expressam propriedades, relações e regras.
- Tipos novos devem poder surgir sem bloquear a criação de artefatos.
- Propriedades estruturadas podem permanecer internas ao artefato.
- A mesma infraestrutura deve inicialmente governar arquivos, pastas, skills e tools.
- Relações como `derives_from`, `contradicts` e `informs` devem poder existir entre artefatos de
  qualquer tipo.
- Humanos e agentes devem acessar o mesmo conhecimento, ainda que por representações diferentes.

## Estratégia escolhida

Decomposição por preocupações independentes:

1. Modelo conceitual: domínio, schema, tipo, subtipo, instância, propriedade, relação e composição.
2. Admissão e governança: mínimo universal, fallback, tipos novos, schemas provisórios, publicação,
   identidade e versionamento.
3. Representação para humanos e agentes: manifesto, conteúdo, campos, relações, projeções e fontes
   de verdade.

## Alternativa rejeitada

Decompor por exemplos de artefatos — Plan, Research, Discovery, Skill e Tool. Essa divisão foi
rejeitada porque os exemplos são contingentes e poderiam transformar semânticas dos primeiros
domínios em arquitetura universal.

## Prompts e exclusões

### 01 — Modelo conceitual

Pergunta: qual é o menor modelo conceitual coerente e generalizável? Investigar as distinções e
tensões entre domínio, schema, tipo, subtipo, instância, propriedade, relação e composição. Excluir
armazenamento, UX e implementação do registry.

### 02 — Admissão e governança

Pergunta: como admitir qualquer artefato sem produzir explosão de tipos ou autoridade acidental?
Investigar mínimo universal, fallback, criação de tipos, schemas provisórios, publicação, identidade
e versionamento. Excluir semântica específica de Plan, Research ou Discovery.

### 03 — Representação para humanos e agentes

Pergunta: como representar uma única identidade de artefato em formas estruturadas e narrativas sem
duplicação ou drift? Investigar manifesto, conteúdo, campos, relações, documentos, projeções e
fontes de verdade. Excluir formalização categorial e política de publicação.

## Protocolo

- Os três agentes exploram de forma independente e escrevem apenas seu relatório designado.
- Cada finding material deve citar arquivo e linha ou ser marcado explicitamente como hipótese.
- Cada relatório deve conter: Key Findings, Gaps or Inconsistencies, Local Tensions e Questions for
  Synthesis.
- A síntese posterior procura contradições entre camadas, não apenas consenso ou resumo.
- Nenhuma mudança no README ou na arquitetura será feita antes do human gate.

## Resultado da exploração

- [01 — Modelo conceitual](reports/01-conceptual-model.md)
- [02 — Admissão e governança](reports/02-admission-governance.md)
- [03 — Representação para humanos e agentes](reports/03-representation.md)

Os três relatórios convergiram em um núcleo mínimo baseado em identidade durável, schema resolvível,
manifesto separado do artefato e fallback para novidade. Divergiram ou expuseram lacunas sobre a
identidade longitudinal de tipos, sobreposição de domínios, papel de representações, draft de novos
tipos, composição e canonicalidade de informação.

## Síntese

A síntese está preservada em [findings.md](findings.md). Ela registra nove tensões, um modelo
provisório e as mudanças recomendadas caso o human gate as aceite. O resultado não usa Plan,
Research ou Discovery como primitivas do núcleo.

## Human gate

O usuário aceitou a disposição recomendada: T1–T5 e T7 são reais e acionáveis no enquadramento;
T6, T8 e T9 são reais e permanecem parcialmente abertos. O usuário autorizou atualizar o README e
exigiu que as questões abertas permanecessem explícitas. A atualização documental foi realizada;
nenhuma implementação do serviço foi iniciada.
