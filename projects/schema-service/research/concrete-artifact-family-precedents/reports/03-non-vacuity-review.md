# Revisão de non-vacuity do modelo de artefatos

## Resultado do gate

**FAIL — o modelo permanece sem witness operacional.** Nenhuma das quatro famílias percorre, no
corpus autorizado, `identidade -> contrato/schema -> instância/manifesto -> representação ->
mudança -> validação` sem (a) renomear um conceito local para um papel mais forte do Schema Service,
(b) inventar uma autoridade de publicação, ou (c) promover um snapshot/digest a estado durável do
artefato. Isso não refuta o modelo; limita a conclusão a **non-vacuity ainda não demonstrada**.

Neste relatório, `O/` significa
`C:/Users/victo/cyberalchemy-orchestrator/` e `D/` significa
`C:/Users/victo/domainspec-core/`. Todas as referências abaixo incluem linhas.

O próprio alvo exige uma cadeia maior que mera validação de arquivo: identidade durável, manifesto
referindo schema revision-exact e representação observada (`O/projects/schema-service/README.md:27-36`),
culminando em relatório interpretado por um perfil de enforcement
(`O/projects/schema-service/README.md:64-84`). A revisão respeita também o limite declarado pelo alvo:
o serviço não está implementado (`O/projects/schema-service/README.md:11-16`), a serialização das
identidades continua aberta (`O/projects/schema-service/README.md:96-100`) e o envelope mínimo ainda
não é uma lista de campos congelada (`O/projects/schema-service/README.md:333-357`).

## Controle contra prova vazia

As convenções oferecem um contrato documental observável: frontmatter obrigatório
(`O/vault/ontology-conventions.md:67-83`), relações em `Connections`
(`O/vault/ontology-conventions.md:296-313`) e critérios de promoção por status
(`O/vault/ontology-conventions.md:429-437`). Elas não oferecem, por si, execução desse contrato.

- **[UNIVERSALIDADE NÃO SUSTENTADA]** “Rules every node in the vault must follow”
  (`O/vault/ontology-conventions.md:12-20`) não sobrevive ao próprio exemplo direto: a constituição
  de frontend possui `constitution_id`, `title`, `status`, `owner`, `authority_level` e `updated_at`,
  mas omite vários campos declarados obrigatórios pelas convenções
  (`O/vault/constitution/frontend-constitution.md:1-8`). Logo, o corpus demonstra uma intenção de
  contrato, não conformidade universal.
- **[UNIVERSALIDADE NÃO SUSTENTADA]** as convenções dizem que cada label deve ser estatisticamente
  independente (`O/vault/ontology-conventions.md:24-45`) e depois que conhecer um dos sete labels não
  informa os demais (`O/vault/ontology-conventions.md:323-340`), mas admitem explicitamente que
  `nature` é correlacionado com `node_type` (`O/vault/ontology-conventions.md:197-201`). Não há medição
  no corpus que sustente a universalidade estatística.
- **[DOCUMENTAL != USO]** o exemplo direto `frontend-constitution` define falsificadores e modos de
  validação (`O/vault/constitution/frontend-constitution.md:101-111`), porém declara que os
  validadores Playwright/pytest não existem e mostra apenas o comando pretendido
  (`O/vault/constitution/frontend-constitution.md:290-299`); a promoção ainda requer esses
  validadores e uma escolha ainda não realizada (`O/vault/constitution/frontend-constitution.md:303-317`).
- **[DOCUMENTAL != USO]** o precedente mais próximo de admissão de artefatos em `domainspec-core`
  se autodeclara “candidate contract; validator not implemented”
  (`D/cyberAlchemy-v2/validation/artifact-admission/README.md:1-5`) e separa JSON Schema de futuros
  checks de filesystem, proveniência e autoridade (`D/cyberAlchemy-v2/validation/artifact-admission/README.md:24-35`).
  A validação registrada prova o schema e uma matriz de treze casos, mas também registra que nenhum
  parser, CLI, evaluator ou fixture corpus foi implementado
  (`D/cyberAlchemy-v2/validation/development/artifact-admission-validator/task-sessions/20260711T223159Z-SWU-AAV-001/RESULT.md:50-63`,
  `D/cyberAlchemy-v2/validation/development/artifact-admission-validator/task-sessions/20260711T223159Z-SWU-AAV-001/RESULT.md:25-35`).

## Menores witnesses concretos por família

### 1. Document — tópico `/documentation/adapters/` do Anime.js vault

| Papel | Menor evidência concreta | Resultado estrito |
| --- | --- | --- |
| Identidade | A instância usa `canonical_path`; o schema o restringe como path (`D/projects/animejs/ontology/agent-knowledge-vault/schemas/documentation-topic.schema.json:2-8`) e o builder deriva o ID diretamente desse path (`D/projects/animejs/ontology/agent-knowledge-vault/scripts/build-views.mjs:24-26`). | **Falha. [RENOMEAÇÃO]** Path derivado não é identidade durável independente de localização, requisito explícito do alvo (`O/projects/schema-service/README.md:228-231`). |
| Contrato/schema | Existe `documentation-topic/2-0-0` com forma fechada e campos obrigatórios (`D/projects/animejs/ontology/agent-knowledge-vault/schemas/documentation-topic.schema.json:2-20`). | Presente como documento de schema. |
| Instância/manifesto | Há uma linha concreta com path, estado observado e `raw_sha256`; o manifesto agrega 418 linhas e digests do conjunto (`D/projects/animejs/ontology/agent-knowledge-vault/sources/documentation.jsonl:1`, `D/projects/animejs/ontology/agent-knowledge-vault/sources/documentation-manifest.json:1-36`). | **Falha. [RENOMEAÇÃO]** É snapshot agregado; a linha não referencia o `$id` do schema nem possui revisão de manifesto própria. |
| Representação | A representação observada é a página remota, materializada como JSONL com digest; o manifesto identifica a URL-fonte e a reprodução (`D/projects/animejs/ontology/agent-knowledge-vault/sources/documentation-manifest.json:2-5`, `D/projects/animejs/ontology/agent-knowledge-vault/sources/documentation-manifest.json:29-36`). | Presente como observação/projeção, sem identidade autônoma de `Representation`. |
| Mudança | A fonte é declarada `mutable-live-source` (`D/projects/animejs/ontology/agent-knowledge-vault/profile.json:15-19`) e a ingestão sobrescreve JSONL e manifesto com novos digests (`D/projects/animejs/ontology/agent-knowledge-vault/scripts/ingest-documentation.mjs:122-130`). | **N/A** para revisão durável: há refresh de snapshot, não preservação de manifest revisions anteriores. |
| Validação | O validator checa contagem/digests e executa ingestão em `--check` (`D/projects/animejs/ontology/agent-knowledge-vault/scripts/validate.mjs:56-64`, `D/projects/animejs/ontology/agent-knowledge-vault/scripts/validate.mjs:102-114`). | **Falha de fechamento. [DOCUMENTAL != USO]** Esse validator não carrega `documentation-topic.schema.json`; prova frescor/digest, não conformidade da instância com o schema nominal. |

O pacote põe o teto correto: documentação e presença de fonte não provam comportamento, testes e
exemplos estão “present-not-executed”, e o pacote não concede autoridade nem release
(`D/projects/animejs/ontology/agent-knowledge-vault/profile.json:43-48`,
`D/projects/animejs/ontology/agent-knowledge-vault/README.md:38-45`). **Veredito da família: FAIL.**

### 2. Skill — `inventory`

| Papel | Menor evidência concreta | Resultado estrito |
| --- | --- | --- |
| Identidade | A fonte canônica declara `name: inventory` e `version: 0.1.0` (`D/arcanum/arcana/inventory/SKILL.md:1-10`); o registry possui entrada apontando a pasta (`D/arcanum/registry/SIGILS.md:70-76`). | Parcial. Não há separação explícita entre identidade semântica da skill e identidade imutável de revisão. |
| Contrato/schema | `SKILL.md` define objetivo e modos operacionais (`D/arcanum/arcana/inventory/SKILL.md:12-35`). | **[RENOMEAÇÃO]** É contrato procedural; não é uma schema-definition revision resolvível. |
| Instância/manifesto | `runtime-manifest.json` versiona o formato, enumera membros, fixa digests e um bundle (`D/arcanum/arcana/inventory/runtime-manifest.json:1-41`). | **[RENOMEAÇÃO]** Manifesta bytes do runtime, não uma instância de skill que referencia `SchemaId`. |
| Representação | A cópia Codex declara `generated-native-runtime-package`, fonte canônica e política de regeneração (`D/.agents/skills/inventory/SKILL.md:1-16`). | Presente e distinguida da fonte canônica. |
| Mudança | O sync detecta `missing`, `drifted` e `extra_managed`, aplica cópias e reporta o estado final (`D/arcanum/arcana/inventory/scripts/sync-runtime.sh:127-141`, `D/arcanum/arcana/inventory/scripts/sync-runtime.sh:144-180`). | Presente para bytes gerados; não é lifecycle semântico da skill. |
| Validação | O recibo registra os arquivos tocados e `40 tests passed, 0 failed; 5 sync regimes` (`D/arcanum/arcana/inventory/development/runtime-faceted-layout/session-evidence/SWU-IFR-006/receipt.json:6-21`). | Evidência real de execução, limitada ao runtime sync. |

A cadeia é operacional, mas o próprio manifesto limita a autoridade a `generated-runtime-only`
(`D/arcanum/arcana/inventory/runtime-manifest.json:40-41`). Chamar `SKILL.md` de schema, o runtime
manifest de manifest revision e o registry de publicação autorizada seria renomear três papéis e
inventar o quarto. **Veredito da família: FAIL estrito; precedente operacional parcial.**

### 3. Agent tool — executável `inventory append`

| Papel | Menor evidência concreta | Resultado estrito |
| --- | --- | --- |
| Identidade | O binário expõe o comando `inventory append` (`D/arcanum/arcana/inventory/bin/inventory:30-44`); o contrato fixa `operation: append` (`D/arcanum/arcana/inventory/schemas/inventory.operation-receipt.v1.schema.json:27-37`). | **Falha. [RENOMEAÇÃO]** Nome de comando/operação não é identidade estável de tool nem revisão. |
| Contrato/schema | Há JSON Schema fechado para o recibo, com `$id`, estado, evidência, escrita, limite de autoridade e digest (`D/arcanum/arcana/inventory/schemas/inventory.operation-receipt.v1.schema.json:1-25`). | Presente para **recibos de operação**, não para o tool como tipo de artefato. |
| Instância/manifesto | O runtime manifest liga `bin/inventory` e o schema de recibo a digests concretos (`D/arcanum/arcana/inventory/runtime-manifest.json:14-30`). | **[RENOMEAÇÃO]** É bundle manifest; não existe tool manifest revision que referencie uma schema revision do tool. |
| Representação | O carrier executável resolve o runner, recebe record/timestamp e emite bytes/exit code (`D/arcanum/arcana/inventory/bin/inventory:37-58`). | Presente. |
| Mudança | O mesmo sync substitui bytes divergentes e remove apenas extras gerenciados (`D/arcanum/arcana/inventory/scripts/sync-runtime.sh:144-168`). | Presente como atualização de implantação, não como nova revisão semântica do tool. |
| Validação | Testes constroem recibos, validam a forma e exigem determinismo byte a byte (`D/arcanum/arcana/inventory/test/operation-receipt.test.cjs:176-193`); testes de sync distinguem missing/drift/extra e reparam drift (`D/arcanum/arcana/inventory/test/runtime-sync.test.cjs:94-129`). | Uso executável comprovado, mas do contrato de operação e do bundle, não do modelo de artefato. |

**Veredito da família: FAIL estrito; precedente operacional parcial.** O corpus tem tool, schema de
recibo, carrier, mutação e testes; falta a ligação não inventada entre identidade do tool,
schema-revision do tool e manifest revision de uma instância do tool.

### 4. Folder — `.arcanum/inventory/` instalado

| Papel | Menor evidência concreta | Resultado estrito |
| --- | --- | --- |
| Identidade | O schema de operação fixa `inventory_root` como `.arcanum/inventory` (`D/arcanum/arcana/inventory/schemas/inventory.operation-receipt.v1.schema.json:72-76`). | **Falha.** A única identidade é o path; o alvo rejeita path/digest como identidade durável (`O/projects/schema-service/README.md:61-62`). |
| Contrato/schema | O runtime manifest define raízes/arquivos gerenciados e digests (`D/arcanum/arcana/inventory/runtime-manifest.json:2-41`). | **[RENOMEAÇÃO]** Contrato de layout/sync, não schema de uma família `folder`. |
| Instância/manifesto | O teste cria um target temporário `.arcanum/inventory`, copia um consumer fixture e preserva paths do consumidor (`D/arcanum/arcana/inventory/test/runtime-sync.test.cjs:11-17`, `D/arcanum/arcana/inventory/test/runtime-sync.test.cjs:47-55`). | Instância concreta de diretório, sem artifact manifest próprio. |
| Representação | O diretório e seus membros são o carrier observado pelo sync; o fixture instalado declara que o runtime é instalado exclusivamente por esse mecanismo (`D/arcanum/arcana/inventory/test/fixtures/installed-consumer/README.md:1-6`). | Presente. |
| Mudança | O teste prova aplicação, detecção e reparo de drift sem alterar paths do consumidor (`D/arcanum/arcana/inventory/test/runtime-sync.test.cjs:80-91`, `D/arcanum/arcana/inventory/test/runtime-sync.test.cjs:115-129`). | Presente para layout gerenciado. **N/A** para reclassificação/revisão durável do folder como artefato. |
| Validação | O teste também prova que raízes consumer-owned ficam fora do manifesto canônico (`D/arcanum/arcana/inventory/test/runtime-sync.test.cjs:132-150`). | Presente para boundary de sync, não para conformance de `folder` sob schema revision. |

**Veredito da família: FAIL.** O folder é operacionalmente real, porém a transformação em artefato
governado exigiria inventar identidade além do path, schema de família, autoridade de publicação e
estado revisionado.

## Claims universais do alvo que o corpus não autoriza promover

- “Every artifact admitted ... receives a stable identity and a manifest revision” é uma intenção
  (`O/projects/schema-service/README.md:27-31`), enquanto o próprio alvo deixa abertas as fontes de
  identidade por família (`O/projects/schema-service/README.md:444-457`).
- “Every governed artifact can use the fallback schema”
  (`O/projects/schema-service/README.md:45-49`) não possui no corpus um registry publicado com
  `artifact/other@0`, resolução revision-exact e instância validada. O texto reconhece que quais
  famílias terão fallback continua aberto (`O/projects/schema-service/README.md:158-163`).
- “Schema definitions are themselves artifacts”
  (`O/projects/schema-service/README.md:233-242`) não tem witness de schema-definition revision
  acompanhada por seu próprio manifest revision, representation snapshot e validation report.
- O lifecycle completo descrito pelo alvo
  (`O/projects/schema-service/README.md:359-377`) não aparece unido em nenhuma família: cada
  precedente executa apenas subconjuntos (digest/frescor, runtime sync, receipt ou layout).

## Collapse-test final

O melhor precedente, `inventory`, só fecha execução depois de substituir:

1. nome/version de skill por identidade semântica + revision identity;
2. `SKILL.md` ou receipt schema por schema-definition revision da família;
3. runtime manifest por manifest revision da instância;
4. registry de navegação por publicação autorizada;
5. digest/sync report por representation snapshot + validation report sob enforcement profile.

Essas substituições não são equivalências demonstradas. Como document falha em identidade e schema
consumido, skill e agent tool dependem de renomeação de contrato/manifesto, e folder depende de path
como identidade, **nenhuma família atravessa a cadeia sem inventar autoridade, identidade ou estado**.
O collapse-test, portanto, dispara.

Para reabrir o gate basta um único pacote de conformidade de uma família que contenha: owner e
registro de publicação; `TypeId` e `SchemaId` revision-exact; `ArtifactId`; manifest revision que
referencie esse `SchemaId`; representation snapshot com proveniência; uma mudança que preserve a
revisão anterior; e invocação/relatório de validator com versão e enforcement profile. Esses são os
papéis já exigidos pelo próprio modelo (`O/projects/schema-service/README.md:137-156`,
`O/projects/schema-service/README.md:198-231`, `O/projects/schema-service/README.md:359-377`), não
novas exigências introduzidas por esta revisão.
