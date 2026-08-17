---
node_type: robot-talks-findings
status: accepted
date: 2026-08-17
topic: universal-artifact-schema-role
---

# Findings — papel universal de schema para artefatos

## Resposta executiva

Os exemplos `Plan`, `Research` e `Discovery` não devem estruturar o núcleo. O modelo generalizável
que sobreviveu às três perspectivas é:

> Dentro de um boundary governado, cada artefato admitido possui identidade durável e uma revisão de
> manifesto que referencia uma revisão resolvível de schema — específica ou fallback. Um tipo é uma
> distinção semântica reutilizável; uma revisão de schema publica um contrato para essa distinção; o
> artefato concreto não ganha um schema próprio apenas por existir. Conteúdo humano, dados
> estruturados e carriers físicos são representações ou asserções coordenadas do artefato, não sua
> identidade.

Essa formulação é uma síntese proposta, não implementação existente. Ela combina o núcleo conceitual
([relatório 01](reports/01-conceptual-model.md#key-findings)), o contrato de admissão
([relatório 02](reports/02-admission-governance.md#key-findings)) e a separação entre identidade e
representação ([relatório 03](reports/03-representation.md#key-findings)).

## Convergências sustentadas

1. **O mínimo é semântico, não uma lista fechada de campos.** Identidade estável e referência a
   schema revision-exact são requisitos; `objective_ref` ainda é candidato e tags são descritivas
   ([relatório 02:5-13](reports/02-admission-governance.md#L5)).
2. **Novidade não exige um schema normativo imediato.** Fallback e `classification_label` admitem o
   artefato; uma definição reutilizável pode ser proposta depois
   ([relatório 02:15-22](reports/02-admission-governance.md#L15)).
3. **Tipo, schema, artefato e manifesto são papéis diferentes.** O tipo é a distinção reutilizável;
   o schema publica seu contrato; o artefato é o sujeito; o manifesto registra asserções sob esse
   contrato ([relatório 01:3-12](reports/01-conceptual-model.md#L3)).
4. **Manifesto e representação podem compartilhar serialização sem compartilhar identidade.** Front
   matter, sidecar ou registro são decisões físicas posteriores
   ([relatório 03:5](reports/03-representation.md#L5)).
5. **Propriedade e relação têm definição intensional e asserção extensional.** Estarem embutidas no
   arquivo é uma decisão de representação, não de ontologia
   ([relatório 01:34-42](reports/01-conceptual-model.md#L34)).
6. **Publicação e enforcement não são consequências automáticas do schema.** Descrição livre, regra
   publicada e consequência operacional permanecem distintas
   ([relatório 02:24-31](reports/02-admission-governance.md#L24)).

## Tensões para decisão humana

| ID | Layer A | Layer B | Impacto | Evidência | Disposição |
|---|---|---|---|---|---|
| T1 | “Cada artefato recebe uma representação mínima de schema.” | O modelo posterior separa `SchemaDefinition` de `InstanceManifest`. | **Alto:** pode induzir um schema por instância e explosão de tipos. | [Relatório 02:88-93](reports/02-admission-governance.md#L88) | Aceita: real e acionável no enquadramento |
| T2 | `SchemaId` parece identificar simultaneamente tipo e revisão normativa. | Revisões são imutáveis, mas não existe identidade longitudinal explícita de `Type`. | **Alto:** reclassificação, compatibilidade e evolução ficam ambíguas. | [Relatório 01:14-23](reports/01-conceptual-model.md#L14), [55-58](reports/01-conceptual-model.md#L55) | Aceita: real e acionável no enquadramento |
| T3 | Tipos “pertencem” a um domínio. | Domínios podem se sobrepor; `DomainPackage` ainda não tem lifecycle demonstrado. | **Alto:** uma árvore exclusiva não cobre artefatos que participam de vários domínios. | [Relatório 01:25-32](reports/01-conceptual-model.md#L25), [83-89](reports/01-conceptual-model.md#L83) | Aceita: real e acionável no enquadramento |
| T4 | O artefato é chamado de documento, pasta, skill ou code unit “real”. | Sua identidade deve sobreviver a path, digest e mudanças de carrier. | **Alto:** falta distinguir entidade semântica, representação e snapshot. | [Relatório 03:3](reports/03-representation.md#L3), [24-25](reports/03-representation.md#L24) | Aceita: real e acionável no enquadramento |
| T5 | Criar um schema customizado deve ser barato. | Publicar um tipo normativo exige owner, authority e lifecycle, ainda sem contrato de draft. | **Alto:** novidade pode adquirir autoridade acidental ou ficar bloqueada. | [Relatório 02:51-62](reports/02-admission-governance.md#L51), [95-99](reports/02-admission-governance.md#L95) | Aceita: real e acionável no enquadramento |
| T6 | Claims, passos ou evidências podem ser propriedades embutidas. | Alguns precisam de referência, proveniência ou lifecycle próprios. | **Médio:** escolher pelo formato físico produz fragmentação ou objetos demais. | [Relatório 03:11](reports/03-representation.md#L11), [20](reports/03-representation.md#L20) | Aceita como real; mantida aberta |
| T7 | O README chama constraints sobre paths de “composition rules”. | Composição propriamente dita exige operação, identidades e leis; uma regra pode apenas inspecionar paths. | **Médio:** o sistema pode alegar estrutura categórica que não possui. | [Relatório 01:44-51](reports/01-conceptual-model.md#L44), [103-107](reports/01-conceptual-model.md#L103) | Aceita: real e acionável no enquadramento |
| T8 | Um envelope universal pretende cobrir documentos, pastas, skills e tools. | Boundary, identidade e snapshot são fornecidos por runtimes/famílias diferentes e ainda estão abertos. | **Alto:** universalidade sem contrato de integração não é verificável. | [Relatório 02:81-84](reports/02-admission-governance.md#L81), [115-119](reports/02-admission-governance.md#L115); [relatório 03:28](reports/03-representation.md#L28) | Aceita como real; mantida aberta |
| T9 | Derivar informação automaticamente reduz custo. | Verdade semântica e divergência entre narrativa e campos não são decidíveis em geral. | **Alto:** uma inferência pode parecer declaração autoral. | [Relatório 03:7](reports/03-representation.md#L7), [17-18](reports/03-representation.md#L17), [26-27](reports/03-representation.md#L26) | Aceita como real; mantida aberta |

## Modelo provisório recomendado

| Conceito | Papel recomendado | Estado |
|---|---|---|
| `Domain` | Fronteira de significado e governança; pode se sobrepor a outras. | Hipótese a definir melhor. |
| `Type` | Distinção semântica reutilizável e longitudinal. | Necessário para não colapsar tipo e revisão. |
| `SchemaDefinitionRevision` | Contrato imutável que expressa um tipo em uma revisão. | Compatível com o README atual. |
| `Artifact` | Sujeito durável governado, independente de localização e digest. | Requisito já sustentado. |
| `ManifestRevision` | Asserções estruturadas sobre um artefato sob um schema exato. | Refinamento de `InstanceManifest`. |
| `Representation` | Forma humana ou machine-readable que realiza ou projeta o artefato. | Hipótese necessária para resolver T4. |
| `RepresentationSnapshot` | Observação versionada de uma representação concreta. | Hipótese; mecanismo varia por família. |
| `PropertyDefinition` / `PropertyAssertion` | Significado admissível versus valor concreto. | Distinção conceitual recomendada. |
| `RelationDefinition` / `RelationAssertion` | Assinatura admissível versus conexão concreta. | Distinção conceitual recomendada. |
| `Rule` | Restrição sobre configurações admissíveis. | Separar de enforcement e de composição. |
| `Composition` | Operação e leis justificadas por um domínio específico. | Capability opcional, não topo universal. |

`DomainPackage` não deve ser promovido a primitiva agora. Pode surgir depois como unidade versionada
de publicação/importação, se ownership, lifecycle ou interface próprios forem demonstrados
([relatório 01:25-32](reports/01-conceptual-model.md#L25)).

## Regra provisória para propriedades e objetos

- **Propriedade embutida:** não precisa de identidade, referência, proveniência ou lifecycle fora do
  artefato pai.
- **Valor local identificado:** precisa ser endereçado, como `artifact/X#claim-1`, mas continua com
  ownership e lifecycle do pai.
- **Artefato relacionado:** precisa de referência entre artefatos, reutilização, schema, proveniência
  ou lifecycle próprios.
- **Representação:** muda carrier ou view, não a entidade do domínio.

Essa regra é hipótese de design, não conclusão já implementada
([relatório 03:11](reports/03-representation.md#L11)).

## O que atualizar se o human gate aceitar

1. Trocar “cada artefato recebe uma representação mínima de schema” por “cada artefato admitido
   recebe identidade e uma revisão de manifesto que referencia um schema específico ou fallback”.
2. Introduzir explicitamente `Type` separado de `SchemaDefinitionRevision`.
3. Diferenciar `Artifact`, `ManifestRevision`, `Representation` e `RepresentationSnapshot`.
4. Descrever o fluxo de novidade como `fallback/classification label -> candidate -> published`, sem
   ainda inventar o lifecycle completo de draft.
5. Qualificar `structured -> relational -> compositional` como eixo de expressividade, não maturidade
   global.
6. Reservar `composition` para domínios que definam operação e leis; usar `path constraint` quando a
   regra apenas atravessa relações.
7. Declarar que “todo artefato” significa todo artefato **admitido no boundary governado**.
8. Acrescentar as lacunas de canonicalidade por datum, múltipla tipagem/domínios sobrepostos e
   contrato de integração dos produtores.

## O que não decidir ainda

- campos exatos do envelope universal;
- front matter versus sidecar versus registry;
- `DomainPackage` como primitiva;
- schema único versus múltiplas tipagens/capabilities;
- estados e poderes exatos de draft/candidate;
- critérios completos de promoção de conhecimento;
- mecanismos de snapshot para cada família;
- schemas concretos de Plan, Research, Discovery ou qualquer outro domínio.

## Human gate

O usuário aceitou T1–T5 e T7 como **reais e acionáveis no enquadramento** e T6, T8 e T9 como
**reais, mas ainda parcialmente abertos**. Autorizou a atualização do README com a exigência de
preservar explicitamente as questões abertas. O README foi atualizado; nenhuma implementação do
serviço ou decisão sobre os itens mantidos abertos foi realizada.
