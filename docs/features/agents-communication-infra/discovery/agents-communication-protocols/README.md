---
tags: [agents-communication-infra, protocols, skills, dispatch, anti-bias]
node_type: discovery
is_session: false
layer: [architecture, domain]
nature: [explanatory, technical]
status: draft
veracity: low
conviction: high
version: 0.3.0
last_updated: 2026-07-22
---

# Agents Communication Protocols — Discovery

## Objetivo

Este discovery deve definir como agentes pesquisam, discutem, sintetizam, executam tarefas,
revisam artefatos, solicitam correções e aprovam um resultado usando a infraestrutura de
comunicação entre agentes.

O problema não é apenas transportar mensagens. Precisamos preservar a independência das avaliações,
registrar versões e discussões sem sobrescrever evidência, limitar ciclos de correção e garantir que
cada aprovação se refira à versão exata que foi analisada.

O ownership da mecânica runtime já está ratificado: `agents-communication-infra` possui o protocolo
que transforma um dispatch confirmado em fatos, efeitos controlados e um resultado oficial. Este
discovery deve decidir onde vivem a **semântica de trabalho** e os protocolos compilados que decompõem
skills em tarefas, workers, reviewers e gates, sem criar um runtime paralelo.

## Contexto

O repositório já possui skills para pesquisa, revisão, estratégia de subagentes, registro de
dispatches, criação de SPEC e implementação. Também possui uma proposta de barramento, journal,
artefatos imutáveis, receipts e geração determinística de testes. Essas superfícies ainda não formam
um protocolo único e explícito para o ciclo completo de trabalho.

As conversas que motivaram este discovery indicam, entre outras, as seguintes necessidades:

- relatórios individuais de pesquisa são imutáveis;
- discussões geram novos relatórios, também registrados;
- uma síntese possui um escritor responsável e outro agente que a revisa;
- workers podem receber uma ou mais tarefas coerentes;
- a tarefa aponta para trechos autoritativos da SPEC, em vez de copiar critérios inventados pelo pai;
- o escopo de escrita é declarado por caminhos e permite criação de arquivos;
- cada worker possui revisão local com ciclos limitados;
- feedback de revisão é publicado pelo barramento e persistido pelo journal;
- a revisão final pode reabrir um worker, um grupo ou toda a integração;
- nenhuma aprovação é produzida automaticamente quando o limite de ciclos é atingido.

## Hipótese de superfície única para skills

Este discovery deve testar uma superfície única: o usuário invoca uma skill existente,
e o orquestrador transforma essa intenção em um dispatch governado por um protocolo previamente
compilado, confirmado e persistido. O usuário não deveria precisar operar separadamente a skill, o
registro de protocolos e o runtime.

A hipótese de integração é um **Skill Execution Profile** versionado: o protocolo de tarefas
compilado para uma revisão exata de uma skill. Toda skill deve possuir um perfil confirmado antes de
ser executada; não existe caminho "one-time" sem protocolo persistido. O perfil liga a identidade e
o digest transitivo da skill ao vocabulário existente de `recipe_ref` e `DispatchSpec`, preserva a
decomposição semântica em tarefas, dependências, critérios de decisão, separação entre workers e
reviewers e parâmetros permitidos. O orquestrador, e não a skill original, consome esse perfil para produzir o
`DispatchSpec` concreto; o `DispatchSpec` confirmado continua sendo a autoridade executável da run.

Esta é uma hipótese de discovery, não um schema ratificado. Recipes arbitrárias e workflows que
alteram arquivos continuam fora do escopo da SPEC atual de `agents-communication-infra`; sua
promoção exige evidência, mudança de governança e atualização das autoridades aplicáveis.

### Ownership e precedência propostos

A skill permanece dona da intenção de domínio, dos entregáveis, das fontes autoritativas e do que
significa trabalho de qualidade. Ela é fonte para a compilação, mas não controla a execução. O
perfil confirmado possui a decomposição semântica reutilizável dessas instruções, incluindo:

- tarefas obrigatórias, dependências de domínio, critérios de conclusão e decisões que precisam de gate;
- regras para formar bundles coerentes e separar workers de reviewers;
- requisitos de role para cada classe de tarefa;
- contratos de entrada e saída e capabilities necessárias;
- invariantes, constraints e regras para inferir parâmetros em cada disparo.

O perfil não congela a quantidade nem a atribuição concreta de agentes. Em cada disparo, esses
valores são fornecidos pelo usuário ou inferidos pelo orquestrador a partir da complexidade da
invocação, dentro das constraints confirmadas. A proposta de `DispatchSpec` deve mostrar a origem de
cada valor (`user` ou `inferred`) e, para inferências, a justificativa usada.

A `recipe_ref` selecionada e digest-pinned é a única autoridade sobre o grafo executável: estágios,
transições, dependências runtime, roles executáveis, visibilidade, mensagens, ferramentas,
permissões, gates, review/rework e resultados terminais. O perfil fornece requisitos, tarefas de
domínio, constraints e bindings skill-specific permitidos pela recipe. Uma compilação determinística
deve provar que a recipe realiza todos os requisitos `preserved` ou `compiled`; conflito ou
capacidade ausente vira `unsupported` e bloqueia o dispatch. O perfil nunca sobrescreve a recipe.

Cada mapeamento do perfil deve apontar para sua origem na skill ou em outra autoridade exata. O
discovery deve testar um vocabulário candidato de disposições — `preserved`, `compiled`, `superseded`
e `unsupported` — em vez de tratá-lo como schema final. Na hipótese, uma instrução material marcada
como `unsupported` bloqueia o dispatch, enquanto `superseded` exige autoridade explícita e não pode
ser inferido pelo orquestrador. Depois da confirmação, os bytes e digests do `DispatchSpec`, e não o
perfil reutilizável, governam aquela execução.

Cada skill deve possuir um `skill_id` opaco, lógico e estável, separado de nome, path e revisão. Uma
forma candidata é `skill:<authority-id>:<uuid>`, atribuída por um registry dentro de um namespace de
sistema, plugin, organização ou workspace. Nome e `source` são aliases mutáveis: rename ou move
preserva o ID; fork/import recebe novo ID, salvo continuidade explicitamente autorizada pelo owner.

O `skill_revision_digest` é o hash dos bytes canônicos de um `skill_source_manifest`: entrypoint
(`SKILL.md`) e closure transitiva das dependências **intrínsecas e alcançáveis a partir da definição
da skill**, como agentes, templates, skills auxiliares e contratos referenciados. Escolhas feitas
durante a compilação — recipe selecionada, versão do compilador, taxonomias e schemas de protocolo —
pertencem a um `protocol_dependency_manifest`, nunca à identidade da revisão de entrada da skill.

O perfil confirmado referencia exatamente `(skill_id, skill_revision_digest)` e possui seu próprio
`protocol_revision_digest`, calculado sobre uma projeção canônica do protocolo, o digest da skill e o
`protocol_dependency_manifest`. Essa projeção exclui o próprio `protocol_revision_digest`, receipts,
o binding mutável e metadados de armazenamento; o digest é anexado ao envelope somente depois do
hash. Metadados de confirmação ficam em um receipt/evento separado e não participam do digest que o
usuário aprova.

Pode haver mais de uma revisão imutável de protocolo para a mesma revisão da skill, mas um binding
append-only deve selecionar **exatamente uma** como `active`. Ativar outra revisão exige confirmação,
compare-and-swap contra o binding anterior e registra `supersedes`; revisões anteriores tornam-se
`superseded` ou `revoked`. Revisões superseded permanecem disponíveis por referência histórica;
revisões revoked permanecem auditáveis, mas seu uso depende da política de revogação. Todo
`DispatchSpec` carrega o `protocol_revision_digest` ativo exato.

Quando o digest observado da skill não possui binding compatível, o resolver retorna
`compatibility: stale`; isso não altera o estado histórico do binding, que continua ativo para a
revisão antiga. A skill de compilação pode usar o protocolo anterior como entrada de migração para
propor uma revisão ligada ao novo `skill_revision_digest`, mas ela precisa de confirmação humana e
nova ativação antes de ser usada. Mudanças de recipe, compilador, taxonomia ou schema não tornam a
skill stale: elas produzem outra revisão do protocolo ou uma revogação administrativa explícita.

Forma candidata do vínculo persistido:

```yaml
skill_ref:
  skill_id: "skill:workspace-7f3a:<uuid>"
  source: ".claude/skills/domainspec-spec-feature/SKILL.md"
  skill_revision_digest: "sha256:<skill-source-manifest-digest>"
  intrinsic_dependencies:
    - kind: agent
      source: ".claude/agents/domainspec-spec-writer.agent.md"
      digest: "sha256:<content-digest>"
    - kind: template
      source: "domainspec/templates/spec.md"
      digest: "sha256:<content-digest>"
protocol_ref:
  protocol_id: "skill-protocol:<uuid>"
  protocol_revision_digest: "sha256:<canonical-protocol-digest>"
  skill_revision_digest: "sha256:<skill-source-manifest-digest>"
  recipe_ref: "recipe:<id>@sha256:<digest>"
  compiler_ref: "skill-protocol-compiler@sha256:<digest>"
binding:
  state: active
  active_protocol_revision_digest: "sha256:<canonical-protocol-digest>"
  supersedes: "sha256:<previous-protocol-digest>"
confirmation_receipt:
  confirmed_by: "user:<principal-id>"
  confirmed_at: "<timestamp>"
```

Nome, versão declarada, commit Git, mtime ou digest isolado de `SKILL.md` não bastam: nenhum deles
captura sozinho uma mudança local ou transitiva capaz de alterar o protocolo executado.

### Onboarding quando o perfil não existe ou é incompatível

Na ausência de perfil compatível, a execução da skill fica bloqueada. Uma **skill de sistema para
compilação de protocolos** inicia um lifecycle de autoria separado do lifecycle do dispatch. Para
encerrar a regressão de bootstrap, ela é instalada com um protocolo raiz digest-pinned, assinado e
admitido pelo trust store da instalação. Atualizar a compiladora ou seu protocolo raiz exige uma
cerimônia administrativa/humana que confirma o novo digest antes de ativá-lo; a compiladora nunca
autoriza a própria raiz.

A autoria começa por um `ProtocolAuthoringCommand` humano que fixa a skill-alvo, a revisão do
compilador, budget e policy read-only. O runtime precisa registrar e abrir esse comando antes de
qualquer efeito de provider/tool; isso requer uma extensão explícita da autoridade de abertura atual,
não uma exceção implícita. O compilador é read-only sobre a skill e o workspace, não executa a
skill-alvo, não amplia permissões e não registra sua proposta como protocolo confirmado. Antes de
persistir ou usar o protocolo, o usuário vê:

1. as interpretações e os pontos não suportados;
2. o manifesto de identidade e dependências da skill;
3. o perfil reutilizável proposto, com tarefas, roles, reviewers e gates;
4. os parâmetros que o usuário pode fornecer e os que o orquestrador pode inferir;
5. o digest exato que será congelado.

Decompor automaticamente qualquer skill continua sendo uma hipótese não provada. A proposta do
compilador é material para confirmação humana, não prova de compatibilidade. Se o usuário rejeitar
ou se houver instrução material `unsupported`, nenhum perfil é registrado e a skill não executa.

Antes de confirmar o protocolo, o runtime re-resolve o `skill_source_manifest`, recalcula seu digest
e faz `compare-and-bind` contra os bytes analisados pelo compilador. Divergência invalida a proposta.
O protocolo confirmado referencia um snapshot imutável/content-addressed da skill e de suas
dependências, é persistido de forma imutável e passa a ser obrigatório para toda execução daquela
revisão. O fluxo possui duas confirmações sobre objetos diferentes:

Em toda **nova invocação**, antes de selecionar o perfil, o resolver recalcula o
`skill_source_manifest`, procura o binding `active` do digest observado e materializa o snapshot
imutável que será usado. A confirmação do dispatch faz compare-and-swap sobre o binding ativo e
congela no `DispatchSpec` os digests e artifact refs; troca concorrente do binding ou drift dos bytes
suspende a proposta em vez de reutilizar silenciosamente o protocolo.

Replay não é uma nova invocação: ele referencia o `DispatchSpec`, os digests, receipts e snapshots do
dispatch histórico, sem selecionar o protocolo ativo atual. A política de revogação ainda deve
decidir separadamente se o replay é apenas reconstrução auditável, simulação sem efeitos ou nova
execução autorizada.

```text
skill sem perfil ou com digest novo
  -> ProtocolAuthoringCommand aberto com compiladora raiz confiável
  -> autoria read-only do protocolo sobre snapshot identificado
  -> re-hash + compare-and-bind
  -> confirmação, persistência e ativação do Skill Execution Profile
  -> resolução dos parâmetros da invocação
  -> confirmação do DispatchSpec com digests e snapshot exatos
  -> launch fence
  -> execução do DispatchSpec confirmado
```

A primeira confirmação pertence ao lifecycle de autoria do protocolo; a segunda continua sendo o
gate único do dispatch. Elas não são dois gates dentro da mesma execução. Na abertura da run, a
launch fence verifica que os digests de skill, protocolo, recipe e snapshot coincidem com o
`DispatchSpec`. O snapshot é evidência e fonte congelada para materializar instruções compiladas; não
é uma segunda autoridade de controle. O runtime executa somente o `DispatchSpec`. Se o adapter
precisar ler bytes do workspace vivo para materializar uma entrada, ele revalida o manifesto
imediatamente antes do primeiro efeito e suspende em caso de drift.

### Identidade e contrato de cada agente

O perfil e sua compilação devem preservar, sem colapsar, as camadas de identidade já existentes ou
planejadas:

- um campo candidato, provisoriamente chamado `agent_ref`: referência e digest da definição
  executável e versionada do agente; o nome definitivo ainda precisa ser resolvido;
- `agent_name`: persona opcional, nullable e não única; nunca identidade de execução;
- `role`: vocabulário fechado hoje em `explorer`, `synthesizer`, `skeptic`, `writer`, `auditor`,
  `planner` e `coder`; extensibilidade futura deve ser testada antes de ser promovida;
- `angle`: posição no eixo de anti-bias, preservando seu significado atual e obrigatoriedade em
  grupos com `n >= 2`;
- IDs distintos de seat, instância e attempt, sem deduzi-los de role ou persona;
- modelo, budget de tokens e outros recursos, prompt inicial, ferramentas/capabilities e
  permissões efetivas.

O perfil não pode predefinir valores concretos dos parâmetros declarados variáveis por invocação,
nem assignments ou identidades runtime de seats. Referências estruturais congeladas, como recipe,
tarefas obrigatórias, critérios e constraints, pertencem ao perfil. O dispatch concreto resolve os
valores exatos dos parâmetros variáveis e de cada seat antes da confirmação. Um perfil não pode
apagar diferenças relevantes entre o agente
executável, a persona escolhida e a identidade autenticada da tentativa. A proveniência do nome da
definição executável, suas ferramentas e seu allowlist de child agents deve sobreviver à compilação,
separada dos IDs runtime-authenticated de seat, instância e attempt.

O protocolo também precisa derivar o **role de trabalho** da semântica da skill. Uma skill de pesquisa
pode exigir `researcher`/`explorer`, uma skill de implementação exige `coder`, e uma skill de autoria
documental exige `writer`; reviewers e aprovadores permanecem separados desses workers. Como
`researcher` ainda não pertence ao enum vigente, o discovery deve decidir se ele é apenas um alias
de domínio para `explorer` ou uma extensão formal do vocabulário. O compilador não pode atribuir um
role genérico que apague capabilities, formato de retorno ou critérios específicos da skill.

### Decomposição e distribuição de trabalho

O protocolo identifica os pontos em que a skill pode ser quebrada: tarefas obrigatórias, unidades
de ownership, dependências de domínio, decisões que exigem gate, critérios de decisão e quais
resultados precisam de review. Ele declara o espaço válido de decomposição, mas não fixa uma
atribuição universal nem define a mecânica executável desses gates; a recipe realiza essa semântica.

Para o MVP existe **um único protocolo ativo e exatamente uma `recipe_ref` digest-pinned por revisão
da skill**. Não há modos ou variantes de execução. `distribution_strategy` é apenas um parâmetro do
disparo, fornecido pelo usuário ou inferido pelo orquestrador dentro das constraints do protocolo;
se uma estratégia exigir outro grafo ou outros gates, ela exige nova revisão do protocolo. Suporte a
múltiplos modos ou recipes fica fora do MVP e deve ser introduzido por uma decisão de schema própria.

`worker_count` declara capacidade, mas não define sozinho o significado da distribuição. Em cada
disparo, o usuário pode fornecer a quantidade e a divisão; campos ausentes podem ser inferidos pelo
orquestrador conforme complexidade, coesão, dependências, isolamento e custo. A precedência é:

1. invariantes e constraints não sobrescrevíveis do protocolo delimitam o espaço válido;
2. valores explícitos do usuário são usados quando válidos;
3. todo campo concreto ausente é inferido e justificado pelo orquestrador segundo complexidade.

Uma `distribution_strategy` candidata pode ser `partitioned` ou `independent_replicas`. Quando for
`partitioned`, o orquestrador analisa a invocação antes da confirmação, forma bundles coerentes com
uma ou mais tarefas e, quando houver escrita, com um ou mais arquivos, declara dependências e atribui
ownership exclusivo. Um agente pode cuidar de várias tarefas relacionadas; uma tarefa pode ter um
worker dedicado quando sua complexidade ou independência justificar. Nenhum caminho pode ter dois
escritores concorrentes.

A proposta deve mostrar a atribuição exata, a origem de cada parâmetro e a justificativa de cada
inferência. O orquestrador pode usar menos workers que o limite pedido somente quando o parâmetro
for um máximo, nunca quando o usuário tiver exigido uma cardinalidade exata. Ele não pode fragmentar
trabalho artificialmente apenas para ocupar seats. Sob o P5 atual, workers particionados sem tensão
entre si devem compilar como grupos singleton conectados por dependências, e não como um único grupo
com `n > 1`.

O runtime deve impedir que um agente filho criado durante a execução escape do grafo confirmado.
Spawn aninhado deve ser desabilitado ou interceptado e transformado em solicitação ao orquestrador;
a helper rule atual não pode funcionar como bypass de ownership, permissão ou confirmação.

Transferência de ownership deve ser explícita. Arquivos compartilhados ou mudanças de integração
precisam de uma única autoridade de materialização/integração. Toda edição de integração deve
produzir uma nova versão e invalidar os pareceres cujo subject foi alterado.

### Descritor tipado de atividade

As características que orientam a decomposição não devem ser `tags` livres. No frontmatter do repo,
`tags` continuam reservadas a tópicos; no protocolo, localização, ação, objetivo, pergunta e função
epistêmica são dimensões independentes e precisam de campos tipados. Cada unidade de trabalho deve
compilar de uma forma candidata como:

```yaml
activity_id: "task:<stable-local-id>"
subject_ref: "<artifact/path/section/entity + exact version>"
layer: [ontology | architecture | domain | application | external]
operation: produce | transform | investigate | evaluate | decide | approve
objective: "<resultado verificável>"
question: "<pergunta exata ou null>"
input_refs: ["<digest-pinned-ref>"]
output_contract_ref: "<schema-id>@sha256:<digest>"
epistemic_kind: evidence | proposal | judgment | decision
properties: {}
```

`subject_ref` identifica **onde e sobre o quê** se trabalha; `layer` identifica a camada conceitual;
`operation` identifica a ação; `objective` define o resultado verificável; `question` fixa o frame
quando houver uma pergunta; `epistemic_kind` determina como o resultado participa de uma decisão.
`properties` não é um saco livre de labels: aceita somente extensões schema-validadas que tenham
passado pelo teste de ortogonalidade. O descritor deve compilar para `task_ref`, `policy_ref`,
`decision_policies`, Contributions, Artifacts e GroupResults existentes, sem criar outro runtime.

### Rodadas de julgamento e higiene de decisão

Qualquer atividade que peça avaliação de claims, escolha entre propostas, definição de arquitetura,
review de documento ou código, classificação de severidade, aprovação/reprovação, ranking, seleção
de estratégia, votação, consenso ou outro julgamento deve declarar `epistemic_kind: judgment` e um
contrato adicional:

```yaml
judgment:
  kind: claim_evaluation | proposal_selection | architecture_decision | artifact_review |
        severity_classification | approval | ranking | strategy_selection | vote | consensus
  response_shape: binary | single_choice | multi_choice | ordinal | ranking
  criteria_ref: "<digest-pinned>"
  independence_policy_ref: "<digest-pinned>"
  aggregation_rule_ref: "<digest-pinned>"
```

`kind` diz o que está sendo julgado; `response_shape` define a forma discreta da posição. Toda posição
também carrega rationale e referências de evidência, mas texto livre não participa da agregação como
se fosse um voto. Se a decisão agregar duas ou mais posições, a recipe **deve** compilar uma
`JudgmentRound` com o seguinte lifecycle não desabilitável:

1. congelar subject e versão, pergunta, critérios, schema de resposta, regra de agregação e seats
   elegíveis;
2. coletar posições independentes e seladas, sem revelar conteúdo, contagem parcial ou tendência;
3. fechar a rodada atomicamente e somente então revelar as posições;
4. agregar deterministicamente e preservar rationale, evidência, abstenções e dissenso;
5. permitir discussão somente após o registro imutável das posições iniciais;
6. quando houver reconsideração, abrir uma **nova** rodada selada e preservar posições inicial e final;
7. produzir um `GroupResult` que não apague dissenso e não se confunda com a decisão do
   `final_approver`.

Uma única posição pode ser um julgamento, mas não é agregado, votação nem consenso. A separação de
seats sozinha também não prova independência: eligibility precisa considerar autoria do subject,
principal, definição/persona do agente, capabilities e conflito de interesse. ACI possui a mecânica
de submit selado, close, reveal, persistência e agregação; uma policy universal de higiene possui a
semântica de independência, critérios, quorum, forma discreta e regra de agregação. O perfil marca as
atividades de julgamento e referencia a policy; a recipe a realiza e não pode desabilitá-la.

### Input contracts, submissões e review

O `input_contract` proposto não valida se o artefato de domínio está correto. Ele verifica, antes de
invocar um agente, se estão presentes as entradas exatas que a skill exige: objetivo, referências e
versões autoritativas, outputs upstream, caminhos-alvo, permissões e formato esperado de retorno.
Esses requisitos são derivados da skill e rastreados pelo perfil; a infraestrutura apenas valida o
contrato compilado.

O retorno de um worker deve compilar para a `Contribution` tipada existente cujo payload referencia
um `Artifact` imutável. O discovery deve testar um schema candidato de submission manifest para esse
Artifact, capaz de representar caminhos, hashes e base snapshot submetidos; esses itens não são
campos hoje ratificados na entidade `Artifact`. Imutabilidade aqui significa que a submissão
histórica não é sobrescrita; o arquivo de trabalho pode ser corrigido, mas a correção cria outro
manifesto. Reviewers avaliam uma submissão exata, e seus pareceres ficam vinculados ao respectivo
manifesto e versão.

`reviewer_count` é independente de `worker_count`. Uma implementação com três writers pode ter um,
três ou outro número confirmado de reviewers. Review é apenas uma espécie de julgamento e herda a
`JudgmentRound` transversal quando agrega duas ou mais posições. Três separações diferentes devem
ser preservadas:

1. **producer↔reviewer:** quem revisa uma submissão ou versão do pacote não pode compartilhar com
   seu produtor o seat, a instância/attempt do agente nem autoridade de autoria sobre o subject;
2. **reviewer↔reviewer:** reviewers em um grupo com `n >= 2` submetem posições iniciais seladas e
   precisam ser tensionados conforme P5; suas diferenças não podem ser
   justificadas apenas pela partição dos arquivos;
3. **grupos de trabalho/review↔aprovação final:** o `GroupResult` de review é evidência para a
   decisão e, sob P12, o `final_approver` continua separado dos grupos de trabalho e review.

Atingir o limite de rework encerra como não resolvido; nunca aprova automaticamente.

### Um protocolo confirmado por skill, recipes reutilizáveis

O alvo é um conjunto pequeno de patterns reutilizáveis entre skills, por exemplo autoria
particionada seguida de review independente, ou pesquisa independente seguida de síntese. Cada skill
recebe obrigatoriamente seu próprio perfil confirmado, mas esse perfil deve selecionar e parametrizar
uma recipe reutilizável sempre que a álgebra existente expressar seu protocolo. "Um perfil por skill"
não significa "uma recipe ou um branch de kernel por skill". Se a skill exigir uma interação que a
álgebra atual não expressa, isso é evidência para avaliar uma nova recipe ou primitive, não autoriza
um branch ad hoc no kernel.

Todo planejamento contextual deve acontecer antes da confirmação. Descobrir depois um novo
artefato, ampliar caminhos, trocar uma autoridade ou alterar materialmente bundles, agents,
permissões ou policies suspende a execução e exige uma proposta emendada e nova confirmação.

### Exemplo candidato: `domainspec-spec-feature`

Uma invocação poderia pedir três agentes de implementação que produzam coletivamente o pacote:

- writer 1: `SPEC.md`, `domain.md` e `rules.md`;
- writer 2: `events.md`, `states.md` e `workflows.md`;
- writer 3: `architecture.md`, `interfaces.md` e os demais aspectos coerentes identificados;
- uma autoridade explícita integra `glossary.md`, links e ajustes transversais quando esses arquivos
  dependerem do pacote completo;
- reviewers independentes avaliam os manifests exatos e o pacote integrado; o `final_approver`
  toma a decisão final conforme P12.

Cada caminho tem um writer por vez, embora cada writer possua vários arquivos. O orquestrador
decide a divisão concreta por coerência, dependências, isolamento de escrita e carga; o usuário vê
essa divisão antes de confirmar.

A skill atual, porém, manda escrever um documento por vez, revisá-lo imediatamente e reutilizar o
mesmo helper no re-check. Portanto, o exemplo acima não é uma execução fiel da skill atual sem
mudanças: usando o vocabulário candidato, o perfil teria de marcar a orquestração embutida como
explicitamente `superseded`, ao
mesmo tempo que preserva sua semântica de domínio e seus critérios de qualidade. Isso requer
alteração da skill/governança e promoção do workflow mutante antes de se tornar comportamento live.

## Perguntas principais

1. Qual feature é dona da compilação e do registro dos protocolos de trabalho, preservando em
   `agents-communication-infra` a mecânica runtime já ratificada?
2. Qual é o conteúdo mínimo de uma atribuição de trabalho?
3. Como uma tarefa referencia partes da SPEC sem reinterpretar seus critérios?
4. Como caminhos autorizam criação e alteração sem permitir escrita fora do escopo?
5. Exclusão e movimentação exigem uma autorização separada?
6. Quando um worker pode receber várias tarefas e quando elas precisam ser separadas?
7. Como dividir a criação de uma SPEC entre agentes sem gerar divergência entre seus arquivos?
8. Como relatórios individuais, discussões, sínteses e revisões são versionados e relacionados?
9. Qual informação deve ser fornecida por um agente e qual deve ser registrada automaticamente?
10. Qual é o parecer mínimo que um revisor precisa publicar?
11. Como funcionam os ciclos escritor–revisor, worker–revisor e integração–revisores finais?
12. Como alterações invalidam aprovações anteriores e determinam o alcance da nova revisão?
13. Como revisores finais solicitam trabalho a grupos específicos sem se tornarem orquestradores?
14. Quais mensagens são apenas transporte e quais fatos precisam ser persistidos no journal?
15. O que acontece quando um ciclo não converge dentro do limite?
16. Qual é a forma mínima do `Skill Execution Profile` e como cada mapeamento preserva sua origem?
17. Como distinguir `compatibility: stale` por mudança da skill, nova revisão disponível de uma
    dependência do protocolo e revogação administrativa?
18. Quais recipes atendem várias skills sem criar branches por skill no kernel?
19. Como o orquestrador propõe bundles e assignments reproduzíveis sem inventar requisitos?
20. Quais mudanças tardias são materiais e obrigam uma nova confirmação?
21. Como `skill_id`, `skill_revision_digest` e `protocol_revision_digest` são gerados e resolvidos
    para skills locais, de sistema e de plugins?
22. Quais parâmetros devem vir do usuário e quais o orquestrador deve inferir conforme a complexidade
    da invocação?
23. Como o protocolo deriva roles específicos de workers sem misturá-los com reviewers e aprovadores?
24. Como instalar, atualizar e auditar o trust anchor da skill compiladora sem autorização circular?
25. Como o registry garante exatamente um protocolo ativo por revisão da skill e registra
    supersessão/revogação sem reescrever história?
26. Em quais fronteiras o runtime recalcula ou compara digests para impedir TOCTOU entre autoria,
    confirmação e primeiro efeito?
27. Qual algoritmo fecha dependências intrínsecas da skill diante de globs, symlinks, ciclos,
    includes dinâmicos e dependências externas não snapshotáveis?
28. Quem pode registrar skills, administrar aliases e bindings, resolver colisões e recuperar o
    registry após falha parcial ou concorrência?
29. Como persistência, receipt e ativação tornam-se idempotentes e transacionais?
30. Qual a semântica de `superseded` e `revoked` para dispatch proposto, confirmado, não iniciado,
    in-flight, retry e replay?
31. Quais tipos, normalizações, conflitos e evidências tornam parâmetros inferidos validáveis e
    reproduzíveis?
32. Quais critérios provam independência, qualificação e ausência de conflito de interesse de
    avaliadores e do `final_approver` além da separação de seats?
33. Qual schema mínimo do descritor de atividade preserva localização, ação, objetivo, pergunta e
    função epistêmica sem duplicar o frontmatter documental?
34. Em que nível vive a policy universal de higiene de decisão e como a recipe prova que toda
    agregação de julgamentos foi compilada para uma `JudgmentRound` selada?

## Pesquisas necessárias

### 1. Inventário do funcionamento atual

Levantar o comportamento real das skills e dos registros existentes:

- [research](../../../../../.claude/skills/research/SKILL.md);
- [review](../../../../../.claude/skills/review/SKILL.md);
- [domainspec-subagents-strategy](../../../../../.claude/skills/domainspec-subagents-strategy/SKILL.md);
- [register-dispatch](../../../../../.claude/skills/register-dispatch/SKILL.md);
- skills e agentes de discovery, SPEC e implementação;
- registros reais em `telemetry/agents/`;
- [test-derivation-engine](../../../../../tools/test-derivation-engine/README.md);
- [arquitetura de agents-communication-infra](../../README.md);
- [feature discovery vigente](../feature-discovery/agents-communication-infra.md);
- [SPEC e seus aspects](../../specs/SPEC.md);
- [implementation layering](../../IMPLEMENTATION-LAYERING.md);
- [work pack e gates vigentes](../../WORK-PACK.md).

A pesquisa deve distinguir regras efetivamente aplicadas, regras apenas documentadas e convenções
que hoje dependem do agente pai. Toda conclusão sobre ownership, entidades ou gates deve registrar
uma matriz `claim -> autoridade -> status/versão -> evidência`.

### 2. Independência, discussão e decisão coletiva

Pesquisar evidência sobre:

- julgamento independente antes da interação;
- feedback controlado e métodos semelhantes ao Delphi;
- risco de conformidade, cascata informacional e groupthink;
- discussão depois do registro das posições iniciais;
- nova decisão privada depois da discussão;
- formas discretas de resposta, rationale e evidência sem transformar texto livre em voto;
- detecção explícita de julgamento em pesquisa de claims, comparação de propostas, arquitetura,
  review, severidade, aprovação, ranking e seleção de estratégia;
- unanimidade, objeção bloqueante e tratamento de dissenso;
- limites de ciclos como controle de custo, não como aprovação automática.

O resultado deve recomendar quando agentes podem conversar, quais posições precisam permanecer
registradas antes e depois da conversa e como impedir que uma recipe contorne a higiene apenas
renomeando um julgamento como pesquisa, review ou planejamento.

### 3. Protocolo de pesquisa e síntese

Comparar pelo menos estas configurações experimentais de recipes distintas:

1. pesquisadores independentes sem discussão, seguidos por um sintetizador;
2. pesquisadores registram seus relatórios, discutem e publicam um relatório complementar;
3. dois sintetizadores produzem versões independentes antes de um deles integrar;
4. um sintetizador escreve e outro executa um ciclo de revisão da síntese.

A pesquisa deve avaliar qualidade, preservação de dissenso, custo, número de ciclos, facilidade de
auditoria e risco de o sintetizador omitir evidências.

### 4. Granularidade das atribuições de trabalho

Investigar como decompor trabalho sem usar nem tarefas pequenas demais nem pedidos abertos como
“implemente todo o `architecture.md`”. Devem ser avaliados:

- uma tarefa por worker;
- várias tarefas relacionadas por worker;
- uma capability ou fatia vertical por worker;
- um arquivo por agente na criação de SPEC;
- conjuntos de arquivos relacionados com um responsável único;
- planejamento obrigatório antes de executar uma arquitetura ampla.

O objetivo é propor critérios de coesão e revisabilidade, sem fazer o agente pai inventar requisitos
que deveriam vir da SPEC.

### 5. Escopo de escrita por caminhos

Pesquisar e testar um contrato de escrita baseado em caminhos, incluindo:

- criação e alteração dentro de raízes autorizadas;
- autorização separada para excluir ou mover;
- contenção por caminho absoluto resolvido;
- traversal e symlinks;
- caminhos sobrepostos entre workers;
- ownership de arquivos compartilhados;
- comportamento quando uma implementação precisa sair do escopo inicialmente concedido.

### 6. Contrato mínimo de revisão

Determinar o menor payload de revisão que continue auditável. A hipótese inicial é que o revisor
forneça:

- referência e hash do artefato analisado;
- parecer `aprovado` ou `precisa de correção`;
- arquivo ou subject exato e citação literal da evidência;
- problema, severidade e correção proposta;
- indicação de que o problema impede ou não a aprovação;
- dados suficientes para projetar o verdict e a lista de change requests exigidos pela recipe.

Identidade, modelo/provider, tarefa, ciclo, horário, prompt, arquivos alterados, testes executados e
estado do finding devem ser avaliados como metadados capturados automaticamente, não campos que o
revisor precisa preencher manualmente. Se arquivo, severidade, correção proposta ou verdict forem
derivados em vez de fornecidos, o protocolo precisa declarar a transformação determinística e
preservar a exigência original da skill.

### 7. Versionamento, discussão e invalidação

Definir como representar:

- relatório original e relatório complementar da discussão;
- posição inicial e posição final de cada participante;
- versões sucessivas da síntese ou implementação;
- parecer aplicável a uma versão exata;
- correção que fecha, refuta ou mantém um problema;
- mudança local que invalida apenas um parecer;
- mudança transversal que reabre vários grupos;
- risco aceito somente por autoridade autorizada.

### 8. Barramento, journal e roteamento

Pesquisar o contrato entre transporte e autoridade:

- o barramento entrega atribuições, findings e solicitações de correção;
- o journal persiste submissões, versões, discussões, pareceres, reaberturas e aprovações;
- agentes não escrevem diretamente o estado oficial da tarefa;
- mensagens repetidas são idempotentes;
- visibilidade é limitada ao worker, revisores, sintetizador e agente pai apropriados;
- o revisor final emite uma solicitação estruturada, enquanto o orquestrador valida e agenda o
  trabalho.

### 9. Ciclos locais e revisão final

Comparar limites separados para:

- escritor e revisor da síntese;
- worker e revisor local;
- integração e revisores finais.

A pesquisa deve definir convergência, escalonamento, troca de reviewer, reaproveitamento do mesmo
reviewer e efeito de atingir o limite. A hipótese inicial é que o limite encerre o fluxo como não
resolvido e nunca reduza o critério de aprovação.

### 10. Experimentos de validação

Os probes devem ser classificados pelo gate em que podem ser executados. Probes documentais ou em
harness read-only autorizado podem ocorrer durante o discovery; probes que dependem do kernel,
escrita isolada, replay ou invalidação runtime tornam-se gates de uma futura emenda à SPEC ou da
implementação correspondente. O discovery não pode exigir como pré-condição atual um mecanismo que
o work pack ainda bloqueia.

Probes de discovery/harness:

- pesquisa com e sem discussão posterior;
- um versus dois sintetizadores;
- simulação read-only, sobre fixtures, de uma SPEC com ownership por arquivo ou conjunto coerente;
- compilação da mesma skill sob diferentes complexidades e parâmetros fornecidos pelo usuário;
- comparação entre um worker por tarefa e um worker com várias tarefas coerentes;
- derivação de roles de workers para skills de pesquisa, escrita e código, mantendo reviewers
  independentes;
- geração determinística de `skill_id`, `skill_source_manifest`, `protocol_dependency_manifest` e
  digests de revisão sem circularidade;
- compilação da mesma skill para uma recipe compatível e uma incompatível, verificando que o perfil
  não sobrescreve o grafo ou os gates da recipe;
- compilar duas skills diferentes para a mesma recipe reutilizável, sem branch por skill no kernel;
- gerar uma proposta não persistida para uma skill não registrada, medindo correções humanas,
  omissões materiais e falsos `preserved`/`compiled`;
- alterar `SKILL.md` e cada dependência intrínseca separadamente, verificando novo
  `skill_revision_digest` e `compatibility: stale`, sem mudar o binding histórico;
- alterar recipe, compilador ou schema, verificando novo `protocol_revision_digest` sem mudar a
  identidade da revisão da skill;
- comparar uma autoria DomainSpec sequencial fiel à skill atual com uma simulação particionada,
  medindo consistência transversal, rework, custo e tempo;
- classificar atividades representativas e provar que avaliação de claims, seleção, arquitetura,
  review, severidade, aprovação, ranking, estratégia, voto e consenso acionam `JudgmentRound`;
- testar que `kind` e `response_shape` permanecem dimensões separadas e que uma única posição não é
  apresentada como consenso.

Gates pós-implementação ou de harness explicitamente autorizado:

- dois workers tentando escrever em caminhos sobrepostos;
- reviewer avaliando uma versão que muda depois do parecer;
- revisão final reabrindo somente um grupo e depois vários grupos;
- repetição de mensagens e recuperação após interrupção;
- término do limite de ciclos com objeção ainda aberta;
- gerar, confirmar e persistir um perfil obrigatório para uma skill não registrada;
- confirmar duas revisões de protocolo para o mesmo `skill_revision_digest` e demonstrar ativação
  unívoca, CAS e supersessão;
- reconstruir um dispatch histórico usando seus próprios digests e snapshots, sem consultar o
  binding ativo como autoridade de seleção;
- alterar uma dependência entre autoria, confirmação e launch, verificando rejeição pelo
  `compare-and-bind` ou pela launch fence;
- injetar falhas entre persistência, receipt e ativação, verificando retry idempotente e ausência de
  binding parcial;
- revogar um protocolo antes do launch, durante a execução, antes de retry e antes de replay,
  verificando a matriz de política aplicável;
- instalar e atualizar a skill compiladora, demonstrando que seu protocolo raiz vem do trust anchor
  e nunca de autoaprovação;
- confirmar que writers particionados viram grupos singleton sob P5 e que reviewers tensionados
  participam de uma `JudgmentRound` selada;
- tentar revelar posição ou contagem parcial antes do close atômico, discutir antes da submissão e
  editar julgamento inicial, verificando bloqueio; após discussão, exigir nova rodada selada;
- tentar ocupar seats de avaliação com o produtor, o mesmo principal/persona ou agente sem
  capability de domínio, verificando a policy de eligibility;
- tentar spawn de child agent, escrita sobreposta, transferência implícita de ownership e ampliação
  tardia de paths, verificando bloqueio ou retorno ao gate;
- modificar um arquivo durante integração e demonstrar invalidação somente dos reviews aplicáveis;
- atingir o loop ceiling com finding aberto e demonstrar que `GroupResult` não vira aprovação.

## Resultados esperados do discovery

O discovery deve produzir recomendações, não código. Seu resultado precisa incluir:

- decisão de ownership da compilação e do registro do protocolo de trabalho, preservando o
  ownership runtime já ratificado em `agents-communication-infra`;
- vocabulário mínimo;
- contratos mínimos de atribuição, submissão, discussão, revisão e rework;
- diagramas dos fluxos de pesquisa e workers;
- regras de versionamento e invalidação;
- política de caminhos autorizados;
- política de ciclos e escalonamento;
- fronteira entre barramento e journal;
- experimentos executáveis no discovery e gates que dependem de emenda à SPEC ou implementação;
- mapa dos documentos, skills e componentes que precisariam mudar;
- proposta do `Skill Execution Profile` obrigatório e imutável, incluindo `skill_id`, manifests
  separados de fonte e protocolo, digests, binding ativo, supersessão/revogação, resolução de
  compatibilidade e avaliação do vocabulário candidato
  `preserved | compiled | superseded | unsupported`;
- catálogo mínimo de recipes reutilizáveis e lacunas da álgebra atual;
- contrato da skill de compilação, do protocolo raiz/trust anchor e do lifecycle autorizado para
  skills sem perfil compatível, com confirmação e persistência obrigatórias;
- contrato de snapshot, `compare-and-bind` e launch fence contra mudanças concorrentes;
- schema candidato para parâmetros fornecidos pelo usuário e inferências de complexidade, incluindo
  precedência, provenance e justificativa;
- regras para derivar roles de workers por semântica da skill e separá-los de reviewers e aprovadores;
- schema candidato do descritor tipado de atividade e sua compilação para as entidades runtime
  existentes;
- policy transversal de `JudgmentRound`, incluindo freeze, eligibility, sealing, close, reveal,
  agregação discreta, dissenso e reavaliação em nova rodada;
- semântica transacional e de autorização do registry, bindings, receipts, revogação e replay;
- regras propostas para bundles, ownership, integração, spawn aninhado e mudanças tardias;
- resultado do piloto exemplificativo `domainspec-spec-feature`, sem tratá-lo como protocolo
  universal para as demais skills.

## Fora de escopo neste momento

- alterar a SPEC existente;
- implementar o runtime ou o barramento;
- mudar as skills atuais;
- escolher valores definitivos para todos os limites de ciclo;
- criar schemas finais de eventos ou banco de dados;
- suportar múltiplos modos ou múltiplas recipes no mesmo protocolo do MVP;
- assumir que consenso implica correção;
- assumir que modelos ou providers diferentes garantem independência.

## Critério para avançar

O discovery poderá ser promovido somente depois de revisão independente que confirme:

- cobertura dos fluxos de pesquisa e execução;
- separação clara entre transporte e autoridade;
- ausência de campos sem necessidade demonstrada;
- ausência de decisões inventadas pelo agente pai;
- tratamento explícito de versão, rework, invalidação e não convergência;
- recomendação clara sobre a feature responsável pela compilação e pelo registro do protocolo;
- bloqueio de execução quando não existir perfil confirmado para o `skill_revision_digest` atual;
- separação verificável entre workers, reviewers, gates de decisão e aprovação final;
- resolução rastreável dos parâmetros concretos entre valores do usuário e inferências;
- classificação tipada de toda atividade e acionamento obrigatório da higiene para qualquer agregado
  de julgamentos, independentemente do nome da tarefa ou role do agente;
- exatamente uma recipe por protocolo no MVP, sem modos implícitos;
- autoridade executável única no `DispatchSpec`, com snapshot tratado como evidência congelada.

## Connections

Nenhuma edge adicional é declarada neste estágio de discovery; as relações candidatas com a
arquitetura, a SPEC e o work pack permanecem referências de pesquisa até a decisão de ownership.
