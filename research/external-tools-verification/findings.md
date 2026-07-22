---
tags: [external-tools, verification, findings, agents-communication-infra]
node_type: findings
is_session: false
layer: research
nature: critical-synthesis
status: complete
version: 0.1.1
last_updated: 2026-07-21
veracity: high
conviction: high
---

# Findings — External Tool Adoptions

## Goal

Determinar quais partes de Octopus Runtime, Eve, PydanticAI e Zod podem reduzir trabalho sem
transferir a autoridade do runtime, quebrar o isolamento dos agentes ou introduzir uma segunda
fonte de verdade na feature `agents-communication-infra`.

## TL;DR

Não adotar Octopus Runtime nem Eve no kernel. O runtime-alvo já existente é Python/FastAPI e já usa
Pydantic core; portanto, Pydantic core deve validar os contratos canônicos, enquanto versionamento,
canonicalização, imutabilidade e digest continuam pertencendo ao runtime. PydanticAI só merece uma
avaliação futura como adapter experimental de API de modelos, e Zod deve permanecer restrito a
boundaries Node já existentes. O primeiro provider real deve ser um adapter subprocess local,
atrás de `SandboxLauncher`, depois do fake adapter e dos gates previstos.

## Context

Os quatro documentos da investigação avaliaram as ferramentas por três invariantes úteis: uma
autoridade persistente não concorrente (I1), input congelado antes do canal (I2) e um único writer
validado do audit ledger (EG-1). A exploração foi necessária porque as ferramentas oferecem peças
parecidas com journal, approvals, evidence, durable execution e validação de outputs, mas cada peça
pode também sobrepor uma autoridade já atribuída pela SPEC.

A síntese precisou corrigir uma premissa factual comum ao [adopt-case](adopt-case.md#layer-3--schemas--judgment-adopt-zod-not-pydanticai)
e ao [build-case](build-case.md#layer-3--schemas--judgment-pydanticai-vs-zod): eles tratam o runtime
como TypeScript. O host existente importa FastAPI e Pydantic em
[`implementations/server/main.py`](../../implementations/server/main.py), linhas 22–25, e as
dependências Python são declaradas em
[`implementations/requirements.txt`](../../implementations/requirements.txt). Logo, o suposto custo
de criar um processo Python para validar schemas não existe; Python já é o processo hospedeiro.

## Síntese das evidências

### Acordos fortes

1. **Eve não fornece o adapter de CLI necessário.** O confirmer encontrou apenas peças de lifecycle
   e reconheceu a ausência de adapter e de cancel nativos
   ([fit-confirmer](fit-confirmer.md#eve-evedev--vercel-workflow-sdk)); o falsifier concluiu que Eve
   executa seu próprio loop de modelo, em vez de dirigir Codex/Claude CLI pelo contrato de cinco
   operações ([fit-falsifier](fit-falsifier.md#eve--evedev--githubcomverceleve--workflow-sdk-apache-20-ga-2026-06)).
   A SPEC já define `materialize/start/events/result/cancel/status` no
   [AgentAdapter](../../docs/features/agents-communication-infra/interfaces.md#internal-agentadapter).

2. **Octopus não prova EG-1.** Ambos os polos aceitam que `routeExecutes`/`governTool` estruturam o
   caminho governado, mas não tornam uma chamada direta ao writer fisicamente impossível
   ([fit-falsifier](fit-falsifier.md#octopus-runtime--githubcomoctorynoctopus-runtime-v070-apache-20),
   [build-case](build-case.md#layer-1--effect-governance-octopus-runtime)). Um lint de import único
   detecta alguns desvios no código conhecido, mas não constitui capability security, não bloqueia
   import dinâmico e não prova exclusividade em todos os processos. Portanto, o `single-import
   lint` pode ser evidência auxiliar, nunca o fechamento de EG-1.

3. **Schema validado não equivale a artefato selado.** Confirmer e falsifier concordam que
   schema-version e digest são composição do chamador, não garantia nativa de PydanticAI
   ([fit-confirmer](fit-confirmer.md#pydanticai-aipydanticdev--pydanticdevdocsai),
   [fit-falsifier](fit-falsifier.md#pydanticai--aipydanticdev-python)). Isso confirma a separação da
   SPEC entre materialização, input efetivo, request selado e resultado terminal.

4. **Um adapter local é inevitável.** Adopt-case e build-case convergem em construir o driver de
   subprocesso
   ([adopt-case](adopt-case.md#layer-2--runtime-host--adapters-do-not-adopt-eve-build-a-repo-local-subprocess-adapter),
   [build-case](build-case.md#layer-2--runtime-host--adapters-eve)). A diferença restante é apenas
   se outras bibliotecas justificam dependências adicionais; a evidência atual não demonstra essa
   necessidade.

### Disputas resolvidas

| Disputa | Posições | Resolução |
|---|---|---|
| Octopus como dependência | O constructor adotaria ports/evidence; o collapser considera essa superfície pequena demais e o guard insuficiente. | **Não adotar no kernel.** Os ports podem inspirar testes/nomes, mas a feature já possui interfaces próprias e Octopus não fecha EG-1. Reavaliar só diante de uma capacidade não contornável e compatível com Python. |
| Eve e I1 | O confirmer interpreta o log como checkpoint subordinável; o falsifier o identifica como fonte do replay do próprio runtime. | **Não adotar no kernel.** Mesmo que autoridades por fato possam coexistir, o log de Eve possuiria os mesmos fatos de execução/replay que o `EventJournal` já deve possuir, criando sobreposição material. |
| PydanticAI versus Zod | Ambos os casos assumem runtime TS e escolhem Zod ou código TS. | **Premissa rejeitada.** Usar Pydantic core no host Python. PydanticAI não é necessário para schemas; Zod só valida payloads em boundaries Node existentes. |
| “Um log” como critério de I1 | A pesquisa às vezes reduz I1 à quantidade de logs. | **Critério refinado.** A pergunta correta é qual store é autoridade para qual fato. Journal e audit ledger podem coexistir porque possuem fatos distintos e reconciliação explícita; dois stores que aleguem o mesmo lifecycle/replay não podem. |

## Matriz de decisão

| Opção | Decisão | Escopo permitido | Razão comprovada | Condição de reavaliação |
|---|---|---|---|---|
| Pydantic core | **ADOTAR** | Modelos e validação dos contratos Python | Já está no host FastAPI; evita novo runtime e se alinha aos contratos provider-neutral. | Pin de versão e testes de canonicalização/round-trip no W0. |
| Canonical JSON + SHA-256 local | **CONSTRUIR** | Seal/digest de requests, inputs, outputs e receipts | Nenhuma ferramenta avaliada entrega versionamento + canonicalização + imutabilidade + digest como contrato completo. | Apenas substituir por padrão aceito em ADR com vetores cross-language equivalentes. |
| Adapter subprocess local | **CONSTRUIR** | `AgentAdapter` real atrás de `SandboxLauncher` | Eve não fornece o papel; a interface já exige seis operações e observações sem mutação de estado. | Depois do fake adapter, W0/W1/W2 e fixtures negativas de sandbox. |
| Octopus Runtime | **NÃO ADOTAR** | Fora do kernel; referência arquitetural somente | Sobrepõe ports/governance e não fornece barreira de capability para EG-1. | Prova de valor exclusivo, integração Python e enforcement não contornável. |
| `octopus-evidence` | **NÃO ADOTAR AGORA** | Referência para vetores de canonicalização | É subordinável, mas sua utilidade demonstrada é pequena e não justifica um boundary Node. | Benchmark/prova de interoperabilidade que supere helper local revisado. |
| Eve | **NÃO ADOTAR** | Fora de journal, replay, sessão e adapters | Sobrepõe fatos de execução durável e não dirige os CLIs no contrato requerido. | Backend que delegue replay ao journal externo e implemente o contrato completo, inclusive cancel/recovery. |
| PydanticAI | **DEFERIR** | Adapter experimental futuro para APIs de modelos, nunca schema dependency do kernel | `output_type` ajuda em output estruturado, mas não sela o artefato e não é necessário para subprocess CLI. | Após um adapter API ter caso de uso, conformance e isolamento próprios. |
| Zod | **MANTER LOCAL** | Validação em boundary Node que já exista | É adequado a Node, mas duplicá-lo como schema canônico criaria duas implementações normativas. | Gerar bindings/testes a partir do schema canônico, sem autoridade própria. |
| Single-import lint | **EVIDÊNCIA AUXILIAR** | CI/arquitetura | Detecta imports conhecidos; não impede bypass em runtime. | Nunca promover sozinho a prova de EG-1. |

## Autoridade deve ser avaliada por fato

| Fato | Store/owner autoritativo | Papel permitido das ferramentas |
|---|---|---|
| Comandos, eventos, aggregate heads, intents e replay de workflow | `EventJournal` | Nenhum runtime externo pode reconstruir uma verdade concorrente desses fatos. |
| Abertura e fechamento oficiais | Audit ledger via appender validado | Materializer solicita e reconcilia; Octopus/lint não se tornam writer nem prova de exclusividade. |
| Bytes de input/output e manifests imutáveis | `ArtifactBoundary` | Bibliotecas podem validar, mas não atribuir autoridade ou alterar digests aceitos. |
| Estado nativo do processo/provider | Provider/adapter como observação externa | `status/result/events` retornam observações; apenas comando+journal as aceitam como fatos. |
| Projeções e custo derivado | Reducers/rollups reconstruíveis | Nunca autorizam efeito ou reescrevem usage bruto. |

Essa divisão é compatível com a arquitetura, que declara journal e audit ledger separados e exige
reconciliação exata entre eles
([architecture](../../docs/features/agents-communication-infra/architecture.md#trade-offs-and-guardrails)).
Portanto, a mera existência de dois logs não viola I1; a violação ocorre quando dois stores disputam
o mesmo fato ou quando não há regra verificável de precedência e reparo.

## Recomendação para a feature

1. Manter o kernel e os contratos em Python, usando `BaseModel`/Pydantic core nos boundaries.
2. Definir localmente canonicalização, versão e digest, com vetores determinísticos e testes de
   round-trip; não atribuir essas garantias a PydanticAI.
3. Implementar primeiro o fake adapter. Só então construir o adapter subprocess real com
   `materialize/start/events/result/cancel/status`, sempre lançado pelo
   [SandboxLauncher](../../docs/features/agents-communication-infra/interfaces.md#internal-sandboxlauncher).
4. Manter metadata/provider-native bytes namespaced e converter apenas para
   `AgentTerminalResult`, `RawProviderOutput` e observações canônicas.
5. Tratar Zod como validação de transporte Node, se um boundary Node já existir, com fixtures
   compartilhadas geradas do contrato canônico Python; Zod não é a fonte normativa.
6. Provar EG-1 com boundary de processo/permissões, busca de writers, testes negativos e auditoria
   de caminhos legados. Um lint de import pode compor essa evidência, mas não fechá-la.

Essas recomendações não autorizam código agora. O
[WORK-PACK](../../docs/features/agents-communication-infra/WORK-PACK.md#control-fields) mantém
`workPackGateStatus=block`, e a própria [SPEC](../../docs/features/agents-communication-infra/SPEC.md#gate-result)
exige W0, política de retenção/credenciais e evidência EG-1 antes do runtime.

## Connections

| edge | target | note |
|---|---|---|
| derives-from | `./research.md` | Agregado lógico do dispatch exigido pelo contrato da skill; não foi materializado nesta pasta. As quatro fontes concretas estão declaradas abaixo. |
| derives-from | [fit-confirmer.md](fit-confirmer.md) | Melhor caso de aderência verificado. |
| derives-from | [fit-falsifier.md](fit-falsifier.md) | Ataque adversarial às mesmas ferramentas e invariantes. |
| reconciles | [adopt-case.md](adopt-case.md) | Preserva as concessões, mas rejeita a premissa de runtime TypeScript. |
| reconciles | [build-case.md](build-case.md) | Adota o build local onde ele coincide com a arquitetura Python. |
| informs | [Agents Communication Infra SPEC](../../docs/features/agents-communication-infra/SPEC.md) | Entrada para emenda versionada, sem promover o gate. |
| constrains | [AgentAdapter e SandboxLauncher](../../docs/features/agents-communication-infra/interfaces.md#internal-agentadapter) | Adapter subprocess local, provider-neutral e sem autoridade de escrita. |
| grounds | [External Tool Adoptions discovery](../../docs/features/agents-communication-infra/discovery/external-tool-adoptions.md) | Promoção confirmada das recomendações para um boundary de adoção da feature. |

### Changelog

- **0.1.1 — 2026-07-21:** adicionada a aresta inversa para a discovery promovida; as conclusões e perguntas da v0.1.0 permanecem inalteradas.

## Open Questions

- **OQ-EXT-1 (BLOCKER)** — Qual versão de Pydantic e qual política de serialização canônica serão
  aceitas no W0? Recommendation: registrar ADR com pin, regras de `null`/Unicode/números, vetores
  de digest e testes cross-boundary. Owner: architecture owner.
- **OQ-EXT-2 (BLOCKER)** — Qual mecanismo no host prova que somente o appender validado possui
  capacidade física de escrever o audit ledger? Recommendation: combinar identidade de processo,
  ACL do arquivo/diretório, inventário de writers legados e testes negativos; manter lint apenas
  como defesa adicional. Owner: engine owner.
- **OQ-EXT-3 (BLOCKER para provider real)** — Quais primitivas Windows/Linux implementam o
  `SandboxPolicy` do subprocesso sem fallback silencioso? Recommendation: criar matriz por host e
  bloquear `launch` quando filesystem, network, process tree ou credential isolation não puderem
  ser impostos. Owner: sandbox owner.
- **OQ-EXT-4** — Existe algum boundary Node que precise consumir os contratos canônicos nesta
  feature? Recommendation: inventariar o MCP/appender atual; usar Zod somente se houver consumidor
  real e gerar fixtures a partir do schema normativo. Owner: integration owner.
- **OQ-EXT-5** — Há um caso de uso para adapter de API direta que justifique PydanticAI?
  Recommendation: deferir até depois do adapter subprocess e exigir comparação de custo,
  observabilidade, cancelamento e conformance. Owner: provider-adapter owner.
- **OQ-EXT-6** — A ausência de `research.md` é intencional ou falha do dispatch? Recommendation:
  materializar um índice/aggregate somente se o pipeline exigir o edge físico; até lá, tratar os
  quatro siblings citados como fontes concretas e não ocultar o dangling edge. Owner: research
  pipeline owner.
