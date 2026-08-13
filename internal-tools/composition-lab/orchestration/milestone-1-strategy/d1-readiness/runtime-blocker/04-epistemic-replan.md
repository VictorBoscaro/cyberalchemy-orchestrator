---
artifact_kind: d1-epistemic-replan
status: blocked-pending-contract-or-capability-change
date: 2026-08-13
scope: repository-lens-inventory reduced execution design
supersedes_execution_shape: d1a-connected-topology
---

# D1: replanejamento epistêmico sem topologia conectada

## Veredito

**GO condicionado** para um piloto reduzido composto por duas pesquisas `n = 1` independentes e
uma terceira pesquisa `n = 1` posterior de síntese/adjudicação, todas com `connections: []`, mas
somente após mudança vinculante do contrato da capability ou resolução de outra capability com
redesenho completo. **Hoje o desenho recebe KILL sob `research` e não é executável nessa rota.**
**KILL** para qualquer afirmação de que esse desenho executa ou preserva o D1a conectado atual.

O ganho é uma estimativa útil de estabilidade procedural do inventário contra denominadores
pré-declarados. A perda é material: não
há handoff governado, prova de input efetivo, writer alimentado por slots upstream, feedback,
auditor downstream ou approver dedicado. O compilador atual só produz assentos turn-zero com
`slots: []`, e um path citado no prompt não prova que seus bytes foram input efetivo
([diagnóstico contratual, linhas 35–54](02-contract-analysis.md#L35)). Logo, o piloto só pode alegar
que artefatos fechados existiam antes da adjudicação e que o artefato final os cita; nunca que o
runtime os entregou, que foram efetivamente lidos ou que a topologia causou a síntese.

## Objetivo, decisão e critério de sucesso

**Objetivo servido:** obter um inventário inicial, protocol-complete e contestável dos usos de
perspectivas/lentes no corpus congelado, sem esperar pela implementação de handoffs conectados e
sem promover configuração, multiplicidade ou fechamento a evidência de efeito composicional.

**Decisão:** substituir, somente para este piloto, o record preparado de D1a por três records novos,
connectionless e separadamente confirmados. O record atual permanece `prepared-not-opened`; não é
editado, aberto nem representado como executado. O diagnóstico já exige mantê-lo nesse estado
([01-runtime-diagnosis.md, linhas 246–249](01-runtime-diagnosis.md#L246)).

**Critério de sucesso:** duas extrações comparáveis inspecionam os denominadores declarados — 22
fontes e oito controles, cada qual com resultado ou ausência explícita — e permitem uma
adjudicação rastreável que preserva acordo, desacordo, ausência e ambiguidade por `occurrence_id`,
com cada afirmação load-bearing citando tanto a fonte original quanto a extração que a sustenta.
As ocorrências são a união adjudicada das encontradas por A e B; não há claim de exaustividade
substantiva. Sucesso não exige concordância, testemunha positiva de composição nem efeito observado.

## Redução contratual explícita

O piloto abandona estas propriedades do D1a original:

- quatro superfícies de coleta com owners distintos;
- `research.md` contendo retornos verbatim;
- writer com quatro inputs upstream governados;
- coverage/provenance auditor separado;
- feedback limitado e approver agente dedicado;
- prova runtime de quais bytes alimentaram a etapa posterior.

Ele preserva apenas: corpus enumerado e hashado, duas observações independentes do mesmo frame,
matriz comum, fontes `path:line`, separação entre prescrição/instanciação/execução/efeito, controles
negativos, dissent e uma adjudicação posterior. Isso é uma nova forma de D1, não uma compilação
equivalente do record antigo. A própria capability admite `n = 1` com somente `findings.md`
([research/SKILL.md, linhas 129–136](../../../../../../.claude/skills/research/SKILL.md#L129)); a
análise contratual já classificou essa forma como executável em tese, porém não equivalente ao D1a
([02-contract-analysis.md, linhas 146–151](02-contract-analysis.md#L146)).

## Invariantes

1. **Precondição informacional por dispatch.** Antes de preparar qualquer record, deve existir um
   `research-initial-definitions.md` integralmente lido e hashado no respectivo research-folder:
   `replica-a/`, `replica-b/` e `adjudication/`. As três cópias são byte-for-byte idênticas à
   initial definition já aceita; sua localização é registrada no record, não alterada no conteúdo.
   Qualquer diferença exige novo gate. Ausência bloqueia o preparo, conforme a precondição da capability.
2. **Claim ≤ proof.** Nenhum output afirma efeito, causalidade, composição demonstrada,
   independência garantida ou input efetivo sem a evidência correspondente; a regra normativa é
   demover, nunca inflar ([research/SKILL.md, linha 160](../../../../../../.claude/skills/research/SKILL.md#L160)).
3. **Mesmo frame observacional.** Réplicas usam o mesmo corpus, pergunta, matriz, regras de
   identidade, controles, budget, modelo solicitado e tool profile. Só mudam `dispatch_id`,
   `working_folder`, `agent_name` e marcador A/B.
4. **Cegueira procedural.** A e B não recebem advice, output, prompt, identidade ou resultado uma
   da outra. Não há mensagens entre seats.
5. **Corpus fechado.** Permanecem os 22 arquivos, commit e SHA-256 já congelados no sheet D1a.
   Outputs do piloto, artefatos de advice e `runtime-blocker/` são excluídos do corpus de ocorrência.
6. **Uma escrita por dispatch.** Cada pesquisa escreve apenas seu `findings.md` no próprio
   `working_folder`; a capability exige pesquisa read-only fora dele
   ([research/SKILL.md, linha 166](../../../../../../.claude/skills/research/SKILL.md#L166)).
7. **Dissent é dado.** A adjudicação não resolve divergência por maioria, confiança ou escolha do
   texto mais eloquente. Mantém A, B, classificação adjudicada ou `unresolved`, razão e observação
   que discriminaria.
8. **Zero é permitido.** `not-observed`, `unknown`, ausência de composição e ausência de efeito são
   resultados válidos.
9. **Nenhuma topologia implícita.** Ordem temporal entre dispatches é uma decisão de orquestração,
   não uma edge executada. O runtime não agenda nem materializa `connections`
   ([01-runtime-diagnosis.md, linhas 81–93](01-runtime-diagnosis.md#L81)).

## Matriz comum de cobertura

Cada réplica deve emitir uma linha por ocorrência ou por controle procurado, com estas colunas
exatas:

| campo | obrigação |
|---|---|
| `occurrence_id` | identidade estável e regra de deduplicação |
| `source` | `path:line` e hash do arquivo no corpus |
| `source_kind` | normativa, configuração, proposta, trace, report, review ou probe |
| `event_identity` | liga representações do mesmo evento sem contá-las novamente |
| `literal_fields` | `concern`, `angle`, role, persona, prompt ou termos presentes, sem inferência |
| `information_access` | acesso declarado/observado e `unknown` quando não demonstrável |
| `ordering_or_relation` | paralela, sequencial, feedback, confronto, síntese ou não observada |
| `preserved_trace` | contribuição, tensão, perda, resíduo ou apenas close/configuração |
| `evidence_level` | `prescribed`, `instantiated`, `executed`, `effect-observed` ou `unknown` |
| `control_status` | controle aplicável, witness ou `not-observed` |
| `ambiguity` | alternativas compatíveis e evidência mínima que as separaria |

`effect-observed` exige delta atribuível, controle/contrafactual ou avaliação independente.
Configuração, frequência, pluralidade, síntese e `resolved` não bastam. As oito verificações de
controle do sheet D1a permanecem obrigatórias.

Essa matriz observacional não substitui silenciosamente a shape canônica de research
`candidate | owner | witnessed? | sound? | verdict | use-mode`. Há incompatibilidade real: D1-R1 e
D1-R2 extraem ocorrências e estão proibidos de fabricar candidates ou verdicts. A skill `research`
atual exige a verdict matrix; portanto o desenho recebe KILL normativo nessa capability. Aceite
humano do dispatch não suspende nem reinterpreta a skill. O GO só pode ser reaberto por uma revisão
aceita da própria skill/contrato, atribuída ao owner identificado em artefato vinculante, ou pela
resolução de outra capability adequada pelo router, seguida de redesenho integral e records novos
que voltem ao gate. Não se
preenchem `GO`, `KILL`, owner ou soundness fictícios para passar conformidade.

## Sequência exata

### 0. Freeze e confirmação conjunta

Um subagente conselheiro independente red-teama os dois records propostos antes da confirmação.
Esse advice orienta desenho, mas não entra no corpus nem nos prompts de execução. Depois:

1. materializar, ler integralmente e hash-ar as initial definitions nos research-folders A/B;
2. verificar que uma revisão vinculante da capability resolveu a incompatibilidade da findings
   shape, ou resolver outra capability e refazer integralmente o desenho; sem isso, KILL e nenhum
   record é preparado;
3. confirmar que ambos têm `n = 1`, um `explorer`, `connections: []`, um template comum
   byte-idêntico e envelopes que diferem somente em `dispatch_id`, `working_folder`, `agent_name` e
   marcador A/B; nenhum inclui output, hash, horário ou metadado contingente do outro;
   e os mesmos 22 paths/hashes;
4. confirmar simultaneamente os dois records exatos antes de qualquer launch;
5. exigir working folders vazios salvo `research-initial-definitions.md` idêntico e
   previamente hashado.

### 1. D1-R1 — réplica A

- `dispatch_id`: `2026-08-13-repository-lens-inventory-replica-a`
- `working_folder`:
  `internal-tools/composition-lab/research/milestone-1/01-repository-inventory/replica-a`
- shape: um `explorer`, `connections: []`, `findings.md` somente
- pergunta: preencher a matriz comum sobre todo o corpus, registrando ausências e ambiguidades sem
  definir “lente” ou decidir efeito composicional.

### 2. D1-R2 — réplica B

- `dispatch_id`: `2026-08-13-repository-lens-inventory-replica-b`
- `working_folder`:
  `internal-tools/composition-lab/research/milestone-1/01-repository-inventory/replica-b`
- shape, pergunta e critérios: idênticos a D1-R1; agente distinto e sem acesso autorizado ao
  working folder A.

Os `findings.md` de A e B são outputs canônicos de seus próprios dispatches; são intermediários
somente em relação ao agregado de D1-R3. Depois do launch, cada pasta A/B é read-only para todos os
demais atores. Antes de cada launch, os 22 arquivos e a initial definition local são rehashados;
depois de cada close, output e inputs são rehashados. Qualquer drift invalida o dispatch — uma
reconfirmação retroativa não cura uma execução sobre bytes diferentes.
Esse read-only é obrigação contratual, não garantia técnica do tool profile.

D1-R1 e D1-R2 devem ser abertos e lançados no mesmo wave, somente depois de ambos estarem
confirmados, para reduzir contaminação temporal. Cada um fecha separadamente. Nenhum output é
repassado por mensagem ao outro.

### 3. Congelamento interstage

Somente após ambos fecharem:

1. cessar qualquer write nos dois working folders;
2. registrar path, bytes e SHA-256 de cada `findings.md` no record/prompt exato de D1-R3;
3. rejeitar output ausente, mutado, vazio ou com citações fora do corpus;
4. criar, ler e hash-ar a initial definition do research-folder de D1-R3;
5. submeter o record D1-R3 a novo red-team conselheiro e a confirmação separada;
6. como último passo após red-team e confirmação, rehash A e B, comparar com os hashes congelados e
   lançar D1-R3 imediatamente, sem operação intermediária.

Esse registro é provenance documental. Como o compiler connectionless gera `slots: []`, ele não é
manifesto de input efetivo nem `binding-output` ([03-test-precedent-scout.md, linhas 19–26](03-test-precedent-scout.md#L19)).

### 4. D1-R3 — síntese/adjudicação

- `dispatch_id`: `2026-08-13-repository-lens-inventory-adjudication`
- `working_folder`:
  `internal-tools/composition-lab/research/milestone-1/01-repository-inventory/adjudication`
- shape: um `writer`, `connections: []`, `findings.md` somente
- fontes documentais declaradas: corpus original e os dois outputs fechados com path/bytes/hash;
- tarefa: revalidar citações na fonte original, produzir matriz A × B, preservar dissent e emitir
  uma adjudicação por linha: `agree`, `source-resolved`, `unresolved` ou `invalid-evidence`.

O `findings.md` canônico deve abrir com a ressalva: “D1-R3 foi instruído a inspecionar os artefatos
identificados abaixo; o runtime não prova entrega nem leitura efetiva porque o launch teve zero
slots.” Citações e correspondência textual são evidência documental de uso alegado, não binding.
Após o close de D1-R3, rehash A, B, a initial definition de R3 e o output de R3; qualquer drift
invalida a adjudicação.

## Isolamento, contaminação e comparabilidade

### Prevenção

- confirmar e lançar A/B antes que qualquer output de réplica exista;
- agentes, dispatch IDs e working folders distintos;
- prompt e allowlist proíbem ler `replica-a`/`replica-b`, orchestration advice, `runtime-blocker/`,
  diálogo desta decisão ou outputs produzidos depois do freeze;
- nenhuma conexão, follow-up, mensagem ou feedback entre A e B;
- mesmo modelo efetivo, budget, tool profile, corpus e schema de resposta. Divergência de modelo
  efetivo demove formalmente a comparabilidade ou exige rerun limpo; reconfirmar depois não a cura.

### Detecção possível

- toda citação deve pertencer à allowlist; citar a outra réplica ou advice invalida a réplica;
- comparar frases idiossincráticas, ordem de erros e classificações não ancoradas para sinalizar
  possível contaminação;
- exigir no final de cada output declaração de paths consultados e de ausência de comunicação;
- registrar horários de abertura/fechamento e hashes dos outputs antes de D1-R3.

Esses controles não provam isolamento. O tool profile herdado permite acesso ao workspace e não há
telemetria apresentada que demonstre todos os arquivos lidos. Portanto a independência é
**procedural e refutável**, não criptográfica nem causal. Se independência forte for critério do
milestone, este desenho recebe KILL e espera sandbox/telemetria apropriados.

### Comparabilidade

Comparabilidade requer igualdade byte-for-byte do template comum e do corpus; os envelopes podem
diferir apenas nos quatro campos enumerados; modelo efetivo e
tool surface registrados; cobertura calculada por `occurrence_id` e campo, não por tamanho do
texto; e divergências classificadas em omissão, identidade/deduplicação, transcrição, status de
evidência ou interpretação. Agentes diferentes e amostragem do modelo impedem atribuir divergência
a uma “lente” específica. Este piloto mede estabilidade do procedimento, não efeito causal de
lentes.
Qualquer divergência de corpus, protocolo ou modelo efetivo descoberta depois do launch exige
demotion explícita da comparabilidade ou rerun limpo. Reconfirmação retroativa nunca cura a execução.

## Provenance e separação do advice

O dispatch autoral deste replanejamento recebeu red-team prévio independente do
`scope_advisor`, incorporado pelo orchestrator antes desta escrita. A tentativa de duplicar o
conselheiro foi bloqueada pelo limite de concorrência; isso não transforma o autor em seu próprio
revisor. O advice decide a forma do piloto, mas:

- não é input de D1-R1 ou D1-R2;
- fica fora do corpus e da matriz de evidência;
- não conta como réplica, audit, adjudicação ou resultado;
- pode ser citado apenas como provenance da decisão de desenho;
- qualquer advice posterior deve ser congelado à parte e não repassado aos investigadores cegos.

Do mesmo modo, a existência anterior de outputs não autoriza alegar consumo. O precedente testado
é somente de manifesto manual; não prova mapping derivado pelo compiler, handoff automático nem a
atribuição aceita pelo spec atual ([03-test-precedent-scout.md, linhas 31–37](03-test-precedent-scout.md#L31)).

Há disjointness nominal obrigatória: advisors, investigator A, investigator B e adjudicator R3 usam
nomes distintos do agent pool, sem reuso entre funções. Advice permanece em pasta de orchestration,
fora dos três research-folders e fora dos prompts A/B; R3 pode receber apenas a decisão de desenho
registrada e os dois outputs congelados, nunca conversa privada ou retorno não preservado do advisor.

## Gate GO/KILL

### GO para executar o piloto

Todos devem ser verdadeiros:

1. o usuário aceita explicitamente a redução contratual e os três records exatos;
2. A/B têm protocolo e corpus byte-identical, agentes distintos e launch no mesmo wave;
3. uma revisão aceita da skill/contrato, com owner identificado em artefato vinculante, tornou a
   findings shape admissível; ou outra capability foi resolvida, o desenho foi integralmente refeito
   e records novos foram confirmados antes do preparo;
4. nenhuma réplica cita output, advice ou path fora da allowlist;
5. ambos os outputs são protocol-complete contra denominadores explícitos ou registram ausência por
   item/controle;
6. hashes permanecem estáveis entre rehash pré-launch, imediatamente antes de R3, close de R3 e
   rehash pós-close;
7. D1-R3 revalida as fontes originais, preserva dissent e mantém a ressalva de provenance;
8. nenhuma conclusão excede estimativa de estabilidade procedural contra os denominadores.

### KILL ou retorno ao runtime roadmap

Qualquer um basta:

- o objetivo exigir equivalência ao D1a conectado, input binding exato, feedback, audit downstream,
  approver dedicado ou prova forte de independência;
- corpus, protocolo ou modelo efetivo divergir após launch sem demotion explícita ou rerun limpo;
  reconfirmação retroativa nunca é suficiente;
- uma réplica demonstrar acesso à outra ou ao advice;
- output mudar depois do close ou não poder ser identificado por hash;
- a adjudicação apagar dissent, não revalidar fontes ou promover configuração a efeito;
- alguém descrever paths documentais como handoff governado ou input efetivo.

KILL aqui é do desenho reduzido para a claim desejada, não dos dados coletados. Negativos e outputs
parciais permanecem banked com seus limites.

## Efeito sobre os outputs canônicos e próximo passo

O contrato canônico reduzido passa a ser:

```text
01-repository-inventory/
├── research-initial-definitions.md   # preservado
├── replica-a/
│   ├── research-initial-definitions.md
│   └── findings.md                    # canônico de D1-R1; intermediário do agregado
├── replica-b/
│   ├── research-initial-definitions.md
│   └── findings.md                    # canônico de D1-R2; intermediário do agregado
└── adjudication/
    ├── research-initial-definitions.md
    └── findings.md                    # canônico de D1-R3 e agregado reduzido
```

Não criar `research.md`: para `n = 1`, a capability exige apenas `findings.md`. Não copiar retornos
para fingir o contrato `n ≥ 2`. O sheet e opening record conectados continuam como histórico
`prepared-not-opened` e devem receber, em decisão posterior separada, um marcador de supersessão;
este replanejamento não os modifica.

Se o piloto receber GO e o canônico passar, o próximo dispatch pode preparar D1b sobre a tabela
adjudicada, mantendo suas categorias provisórias e gates. Se receber KILL, o caminho volta à
extensão de runtime: o corpus mostra que não existe precedente executável de topologia conectada,
apenas compilação isolada, manifesto manual e fence fail-closed
([03-test-precedent-scout.md, linhas 7–15](03-test-precedent-scout.md#L7)).

## Por que as alternativas não bastam

### Robot-Talks

Robot-Talks serve para descobrir tensões cross-layer por investigadores com concerns distintos,
seguido de gate humano; não é um dispatch governado nem ledger entry
([robot-talks/SKILL.md, linhas 64–69 e 98–102](../../../../../../.claude/skills/robot-talks/SKILL.md#L64)).
Ele preservaria relatórios e tensões, mas não satisfaria a pergunta de estabilidade procedural de um
inventário comum, o contrato `findings.md` de research ou a comparação cega A × B. Também não
resolveria provenance de input: sua sessão direta explicitamente não usa a infraestrutura de
dispatch.

### Dois seats paralelos em um único dispatch

Um único dispatch connectionless pode lançar ambos turn-zero, mas não tem writer downstream,
slots, readiness ou materialização de retornos. Como o parent está restrito a orquestrar, ninguém
teria autoridade e input governado para produzir o canônico. Ordenar launches ou mencionar paths
no prompt não cria espera nem binding; os launch plans históricos conectados com slots vazios já
demonstram esse falso precedente ([03-test-precedent-scout.md, linhas 61–72](03-test-precedent-scout.md#L61)).
Separar A e B em dispatches `n = 1` produz dois artefatos fecháveis sob o contrato atual; D1-R3 os
adjudica depois sob uma claim documental explicitamente menor.
