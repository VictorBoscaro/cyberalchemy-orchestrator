---
artifact_kind: research-findings
status: candidate
date: 2026-08-17
topic: concrete-artifact-family-precedents
---

# Findings — precedentes concretos para famílias de artefatos

## Resposta executiva

A ideia do Schema Service continua fazendo sentido como **modelo a ser provado**, mas os corpora
examinados não sustentam ainda um serviço universal nem uma cadeia operacional completa. Há peças
reutilizáveis e usadas de verdade: o vault possui governança documental; o BTE do DomainSpec v2
possui schemas, identidade lógica, handles, digests, recibos e validação; e o pacote `inventory`
possui skill, executável, runtime manifest, sincronização e testes. Nenhuma dessas peças, isolada ou
por simples renomeação, implementa `Type -> SchemaDefinitionRevision -> Artifact -> ManifestRevision
-> Representation -> RepresentationSnapshot` com publicação e enforcement explícitos
([relatório 01](reports/01-ontology-conventions.md),
[relatório 02](reports/02-domainspec-core.md),
[revisão de não vacuidade](reports/03-non-vacuity-review.md)).

O melhor próximo movimento não é criar quatro schemas independentes. É construir **dois pacotes de
conformidade**: um documento simples e um pacote composto `inventory` que force a distinção entre
skill, tool, instalação/pasta e recibo de operação. O BTE deve ser tratado como precedente de
mecanismos, não importado como núcleo validado até que sua suíte focada seja portátil e verde
([verificação](verification.md)).

## Veredito por candidato

| candidato | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict | use-mode |
| --- | --- | --- | --- | --- | --- |
| Documento governado | `vault/ontology-conventions.md`; Anime.js agent knowledge vault | Parcial: schema, frontmatter/JSONL, digest e validação existem, mas não fecham identidade durável, manifest revision e schema consumido na mesma cadeia. | Sim como governança documental; não como modelo completo do Schema Service. | **KILL** | `typed-negative: no-witness` para a cadeia completa; reutilizar classificação, relações e proveniência. |
| Skill | Arcanum `inventory` skill e runtime manifest | Parcial: fonte canônica, pacote gerado, manifest, sync e testes; não há `TypeId`/`SchemaId`/manifest revision da skill. | Sim como pacote operacional; chamar `SKILL.md` de schema seria tautológico por renomeação. | **KILL** | `typed-negative: no-witness`; usar como caso de conformidade composto. |
| Agent tool | executável `inventory append` e schema de recibo | Parcial: carrier, operação, recibo fechado, determinismo e testes; falta identidade/revisão do tool e publicação do contrato do tool. | Sim como tool e contrato de operação; não como artefato governado completo. | **KILL** | `typed-negative: no-witness`; separar tool definition, instalação, invocação e receipt. |
| Folder | `.arcanum/inventory/` e runtime sync | Parcial: layout gerenciado, drift e reparo; path é a única identidade e não há manifesto revisionado do diretório. | Sim como representação/layout; não necessariamente como artefato semântico. | **KILL** | `typed-negative: no-witness`; admitir folder como artefato apenas quando tiver owner/lifecycle/interface próprios. |
| Mecânica de schema para código | BTE contract publication e semantic validation | Sim para publicação/validação de schemas, handles, digests e recibos; não para todo o lifecycle do Schema Service. | Sim, sem colapsar `$id` em `Type` nem digest em snapshot. | **GO condicionado** | `build-from-owned`; portar invariantes depois de resolver as falhas de LF/symlink e demonstrar compatibilidade. |

`KILL` aqui mata somente a alegação de que a família já possui um witness operacional completo. Não
mata a família nem o modelo proposto. O fato que reabre qualquer linha é um pacote que percorra a
cadeia sem equivalências inventadas.

## O que já é possuído e deve ser reutilizado

1. **Governança documental.** `ontology-conventions` já separa papel epistemológico, maturidade,
   formato, confiança e relações, com uso local parcial. Isso é precedente para propriedades e
   relações de documentos, não para identidade longitudinal ou snapshots
   ([relatório 01](reports/01-ontology-conventions.md#veredito-de-precedente)).
2. **Mecânica de contratos.** O BTE já possui definição de schema com `$id`, identidade lógica
   separada de digest, artifact handles, receipts, validação de filesystem e negativos. Essas são
   peças concretas para resolver e validar representações
   ([relatório 02](reports/02-domainspec-core.md#veredito-de-precedente)).
3. **Pacote operacional composto.** `inventory` oferece o melhor material para distinguir uma skill
   fonte, sua representação gerada, um tool executável, um folder instalado, um manifest de bytes e
   recibos de operações. A revisão demonstra que esses papéis existem, embora ainda não estejam
   ligados pelo protocolo do Schema Service
   ([revisão](reports/03-non-vacuity-review.md#collapse-test-final)).

## Correções necessárias no enquadramento

- **Skill não é uma coisa só.** Separar ao menos identidade semântica da capability, revisão
  publicada da definição, pacote/release, instalação e invocação. Um `SKILL.md` pode representar a
  definição; não é automaticamente o schema da família.
- **Tool não é sua execução.** Tool definition/release, instalação, invocation e operation receipt
  precisam de identidades e relações distintas. O receipt prova uma execução; não identifica a
  revisão semântica do tool sozinho.
- **Folder é condicional.** Diretório comum deve permanecer representação ou container. Só se torna
  `Artifact` quando possui owner, lifecycle e interface próprios; caso contrário, exigir identidade
  durável cria burocracia sem semântica.
- **Schema e contrato não são sinônimos.** O precedente CAV2-D56 limita schema à estrutura
  inspecionável; meaning, owner, authority e promotion pertencem a contratos e rotas separados. O
  Schema Service deve preservar essa separação.
- **Ortogonalidade não pode ser alegada como fato estatístico.** O vault não mede independência e
  contém correlação admitida entre labels; use-a como heurística de desenho até existir evidência
  corpus-level ([revisão](reports/03-non-vacuity-review.md#controle-contra-prova-vazia)).

## Menor prova recomendada

### Pacote A — documento

Use um único documento governado e materialize explicitamente:

1. `TypeId` estável para a categoria documental e `SchemaId` revision-exact;
2. `ArtifactId` que sobreviva a rename;
3. `ManifestRevision` que referencie o `SchemaId`;
4. representação Markdown/YAML e snapshot com digest/proveniência;
5. uma mudança e uma reclassificação que preservem o estado anterior;
6. `ValidationReport` versionado interpretado por um `EnforcementProfile`.

### Pacote B — `inventory` como grafo composto

Modele, sem colapsar:

```text
SkillDefinitionRevision
    -> representedBy SkillSourcePackage
    -> releasedAs SkillPackageRevision
        -> installedAs InstalledSkill
            -> contains/uses ToolRevision
                -> invokedAs ToolInvocation
                    -> produces OperationReceipt
```

O folder instalado é representação/aggregate por padrão; só ganha `ArtifactId` próprio se o caso
demonstrar lifecycle independente. Esse único pacote cobre skill, agent tool e folder com relações
reais, em vez de três exemplos artificiais.

## Estado dos testes

O teste focado do BTE encontrou **5 passes e 5 falhas**. Quatro falhas são incompatibilidade entre
CRLF do checkout Windows e a exigência de LF do publicador; uma falha é `EPERM` ao criar symlink no
Windows. Logo, o BTE é precedente executável, mas não deve ser descrito como atualmente validado no
ambiente desta pesquisa ([verificação](verification.md)).

## Próximos passos

1. Refinar os dois pacotes de conformidade acima e decidir os identificadores e owners mínimos.
2. Executar primeiro o pacote documental; ele é o caminho mais barato para provar o lifecycle
   completo e revelar se o envelope universal é útil.
3. Executar o pacote composto `inventory`; só depois decidir se a mecânica comum merece serviço,
   biblioteca ou contrato de interoperabilidade.

Não criar runtime universal, registry definitivo ou ledger do Schema Service antes dessas provas.
