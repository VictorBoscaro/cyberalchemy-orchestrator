# Meta-orchestration research — verbatim returns

## `skill_control_center_meta__operator_projection`

Integridade: os 10 SHA-256 conferem exatamente com o manifest.

**Recomendação — adotar `MiniWave` como projeção derivada, identificável e estritamente read-only.** Ela deve tornar a sequência `research → review → discovery → spec → backend → frontend → validation` navegável sem representar autorização, execução, fila, reconfiguração ou estado de runtime. Isso está alinhado ao contrato APT: UI/projeção/cache não é autoridade e não possui borda UI→Operation nem poder de append/retry/rebuild ([UI-SPEC, §§Data Flow e Re-entry](../../../docs/features/agent-provenance-telemetry/UI-SPEC.md); [observability, §Non-Authority Contract](../../../docs/features/agent-provenance-telemetry/specs/observability.md)).

Menor view-model sugerido:

```json
{
  "schema_version": "miniwave.v0.1",
  "projection_id": "sha256:…",
  "derived_from": [{"path":"…","sha256":"…"}],
  "effective_as_of": "…|null",
  "root": {"id":"feature-or-question","label":"…"},
  "steps": [{
    "id":"research|review|discovery|spec|backend|frontend|validation",
    "order": 10,
    "depth": 0,
    "kind":"workflow|artifact|implementation|gate",
    "label":"…",
    "status":"not_started|available|blocked|complete|partial",
    "artifact_refs":[{"path":"…","sha256":"…"}],
    "depends_on":["…"],
    "disclosure":"one-line summary",
    "authority":"derived_read_only"
  }]
}
```

`root` fixa a pergunta/feature; `depth` expressa aninhamento visual, nunca prioridade/autorização; `order` é somente a ordem narrativa/tiebreak. Não inferir ordem de chegada: as projeções APT exigem coleções determinísticas/canônicas e reconhecem somente ordens semânticas declaradas ([queries, §§Common Deterministic Query Contract e Query Coverage](../../../docs/features/agent-provenance-telemetry/specs/queries.md)). `projection_id`, pins de origem e `effective_as_of` tornam a derivação reidentificável e impedem que “atual” seja fingido.

Navegação/progressive disclosure:

- Visão inicial: uma faixa linear de sete etapas, backend e frontend como irmãos distintos; mostrar só status, gate e um resumo.
- Clique/URL estável em uma etapa abre detalhe com entradas pinadas, artefato resultante, dependências e risco; não expor corpos de prompts, logs ou artefatos brutos. Isso coincide com a vedação de conteúdo bruto e a exigência de tabelas/projeções semanticamente identificadas ([UI-SPEC, §§Future Table Boundaries, Accessibility e Privacy](../../../docs/features/agent-provenance-telemetry/UI-SPEC.md)).
- Perguntas do usuário devem operar como intenção de leitura: “o que bloqueia frontend?”, “qual evidência sustenta review?”, “mostrar validação”. Sem botões de execução. Estados `empty/error/profile-blocked` devem dizer se a projeção está vazia, indisponível ou inválida, sem sugerir recuperação com alteração de autoridade ([UI-SPEC, §State Mapping](../../../docs/features/agent-provenance-telemetry/UI-SPEC.md)).
- Banner C1 permanente: “Projeção derivada — não executa nem autoriza”; se houver agregados, declarar exclusões/denominador ([dashboard-contracts-constitution, R-4 e C1](../../../../maestro-trama/vault/constitution/dashboard-contracts-constitution.md)).

Sequência e artefatos mínimos:

| Ordem | Etapa | Artefato/gate | Uso permitido |
|---:|---|---|---|
| 10 | research | findings/captura pinada | `research` é LIVE |
| 20 | review | único `review.md` | `review` é LIVE |
| 30 | discovery | discovery ratificada | `discovery-writing`; bootstrap controlado, não mascarar como dispatch |
| 40 | spec | feature SPEC | `domainspec-spec-feature` |
| 50 | backend | implementação/testes backend | `task-session` + `implementation-layering` |
| 60 | frontend | três variantes originais + testes | `task-session`; não copiar as variantes ruins |
| 70 | validation | relatório final + screenshots | `ux-evidence-validator` / `implementation-readiness` |

Não usar `code`, `plan` ou `suggestion` como dispatch types: são RESERVED; somente `research`, `review`, `experiment` são LIVE ([domainspec-subagents-strategy, Routing by dispatch_type](../../../.claude/skills/domainspec-subagents-strategy/SKILL.md)). O grafo de skills confirma caminhos explícitos `research → strategy/register-dispatch/review`, `discovery-writing → strategy/review`, além das capacidades existentes `task-session`, `implementation-layering`, `implementation-readiness` e `ux-evidence-validator` ([skill graph](../../skill-relationship-graph/graph.json); [viewer](../../skill-relationship-graph/viewer.html)).

Gates necessários: (1) research/review evidenciados; (2) discovery e SPEC ratificadas antes de qualquer implementação; (3) backend aprovado antes do frontend depender de API/contrato; (4) as três variantes frontend devem cumprir o mesmo contrato funcional/testids, com estética original — o contrato UI prevê teste Playwright comum e proíbe escrita ([UI-CONTRACT, início e §§Required testids/Rules](../../../implementations/UI-CONTRACT.md)); (5) gate final deve rodar testes e capturar screenshots, julgando explicitamente clareza, usabilidade, consistência visual e eficiência operacional, não só “passou”.

Riscos/gaps:

- O UI-SPEC APT está explicitamente “deferred” e sem host/navegação implementados; MiniWave deve ser artefato de design/projeção até o gate de aplicabilidade, não promessa de runtime.
- Falta contrato explícito para `MiniWave`: schema, produtor autorizado, retenção, política de cache e regra de invalidação quando um artefato pinado muda. Sem isso, mostrá-la somente como snapshot datado.
- Há tensão entre a exigência de três variantes e a proibição de copiar variantes ruins: fixar antes um rubric visual e evidência screenshot por variante, mantendo API/testids idênticos.
- A pesquisa event-driven já identifica como aberta a altitude/default de dashboard, contratos de navegação, frescor e modelos read-only seguros; MiniWave deve registrar isso como `blocked/unknown`, nunca preencher por inferência.

## `skill_control_center_meta__governance_review`

- **PASS — integridade do corpus.** Os 10 SHA-256 conferem exatamente com o manifest fornecido.

- **BLOCKER — `MiniWave` não possui definição nem autoridade.** O termo não ocorre no corpus. Criar `MiniWaveId`, inclusive derivado, produziria uma segunda identidade sem owner, lifecycle ou regra de replay. A árvore já dispõe de `Dispatch` e `parent_dispatch_id`; projeções não autorizam execução.  
  **Correção:** eliminar `MiniWave` de schema, API, UI, fixtures e nomes derivados. Representar a “onda” somente como agrupamento projetado pela árvore de Dispatch, marcado `derived/non-authoritative`. Novo conceito só seria admissível mediante witness concreto de uma relação impossível de expressar por ancestralidade/arestas de Dispatch e posterior ratificação em discovery/SPEC/ACI.

- **BLOCKER — a sequência proposta mistura dispatches LIVE com workflows sem tipo LIVE.** O único routing autorizado é: `research`, `review`, `experiment` LIVE; `code`, `plan`, `suggestion` RESERVED. O próprio contrato afirma que não há tipo LIVE `discovery`.  
  **Correção concreta da rota:**
  - `research`: dispatch LIVE `research`;
  - `review`: dispatch LIVE `review`, somente para atacar artefato já existente;
  - `discovery`: bootstrap não registrado de `discovery-writing`, sem row e sem fingir `research/review/experiment`;
  - `spec`: workflow `domainspec-spec-feature`, não `dispatch_type`;
  - `backend` e `frontend`: são trabalho de código; `code` está RESERVED. Podem permanecer separados como work units executadas inline via `task-session`, mas não como dispatches;
  - `validation`: não é tipo. Para UI pronta, usar `ux-evidence-validator`/`task-session` inline; para red-team do artefato, `review` LIVE.

- **HIGH — lineage deve seguir P13 exatamente.** `parent_dispatch_id` existe somente em Dispatch filho planejado por um meta-dispatch; o filho reentra no confirm gate. Discovery, spec e work units inline não são Dispatches e não recebem esse campo.

- **BLOCKER — fontes adjacentes estão sendo promovidas além da autoridade que possuem.** `graph.json` não prova correção semântica nem aprova execução. O material `maestro-trama` é referência não autoritativa. A APT UI continua deferred.  
  **Correção:** declarar grafo, viewer e material maestro como evidência/projeção; autoridade permanece no Dispatch confirmado, journal/ledger e artefatos ratificados.

- **HIGH — “3 variantes originais” conflita com o contrato atual e carece de semântica verificável.** `UI-CONTRACT.md` exige dez variantes, API/testids comuns e somente estética variável.  
  **Correção:** aprovar antes uma revisão que reduza a cardinalidade para três. Congelar que “original” significa distinção estética demonstrável sem alteração de comportamento, API, conteúdo obrigatório ou testids.

- **HIGH — screenshots e critérios qualitativos não bastam para aprovação.** Os critérios não têm escala, limiar, fixture ou assessor definidos.  
  **Correção:** congelar matriz versionada antes do build, executar o mesmo Playwright em todas as variantes, testes de backend/contrato, navegação por teclado/acessibilidade, fixture e viewport idênticos, screenshots identificados por commit/hash e teste de carga representativa.

**Condição de aprovação — REPROVADO até:** zero identificadores MiniWave; rota reclassificada; uso estrito de `parent_dispatch_id`; decisão ratificada entre dez versus três variantes; matriz de aceitação congelada; bundle com testes executados, screenshots versionados e proveniência; e decisão do `final_approver` sobre o corpus completo.
