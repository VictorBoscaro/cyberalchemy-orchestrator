# Checklist adversarial — opening record do D1

**Objeto:** record ainda não final de `repository-lens-composition-inventory`.

**Veredito de prontidão:** **BLOCK OPEN** até todos os bloqueadores abaixo estarem resolvidos no
record concreto e esse record exato passar pelo gate humano. A initial definition local passou nas
checagens de boundary/evidence; isso satisfaz uma precondição informacional, não valida rota,
schema, prompts, corpus, topologia ou aprovação.

## 1. Autoridade, rota e schema

- [ ] Resolver `research` novamente imediatamente antes de congelar o record. O receipt observado
  nesta checagem é `dispatch_type_ref: research`, `ledger_dispatch_type: research`,
  `capability_ref: research`, `capability_path: .claude/skills/research/SKILL.md`,
  `execution_authority_mode: legacy-managed`, `tool_profile_ref: host/inherited@1`.
- [ ] Materializar `schema_version: "0.6.3"` somente se ainda for o
  `ledger_schema_version` do registry no freeze; qualquer drift exige refazer o record e o gate.
- [ ] Tratar o receipt como unidade indivisível. Não copiar tipo, capability, authority mode ou tool
  profile dos documentos estratégicos, do ledger histórico ou das cópias `.agents`/`.codex`.
- [ ] Usar o contrato da capability resolvida em `.claude`. Diferenças de representação entre
  árvores de skills não podem ser “reconciliadas” dentro do record.
- [ ] Incluir somente chaves aceitas. Em particular, não adicionar `corpus`, `constraints`,
  `success_metric`, `status`, `agents` top-level, `topic_slug`, `session` ou `created`; corpus e
  limites pertencem aos prompts/manifests, não a extensões inventadas do schema.
- [ ] Não declarar `meta` nem `parent_dispatch_id` sem uma abertura meta real e rastreável. Pareceres
  auxiliares não criam por si um parent dispatch.
- [ ] Fixar `dispatch_id` único no formato `YYYY-MM-DD-<slug>` e verificar a unicidade no ledger sem
  editar o ledger.

**Bloqueia `open`:** receipt ausente, antigo, reconstruído ou divergente; capability fora de
`.claude/skills/research/SKILL.md`; schema diferente do registry; campo desconhecido; parent fictício;
ou tool profile que não forneça a superfície necessária aos prompts.

## 2. Anti-bias sem contrabando semântico

- [ ] Registrar a escolha humana específica para este D1. A autorização geral do milestone não é
  opt-in de anti-bias.
- [ ] Sem opt-in explícito, usar `anti_bias_mode: disabled` e remover **todos** os `angle`,
  `anti_bias`, `anti_bias_pairs` e `anti_bias_global`. As perspectivas de pesquisa continuam apenas
  nos prompts.
- [ ] Se houver opt-in posterior, reconstruir e reconfirmar o record inteiro: cada fan-out usa um
  único eixo declarado, angles concretos e distintos, todas as `n*(n-1)/2` pairs, posições exatas e
  evidência não vazia; `anti_bias_global` é obrigatório quando dois ou mais grupos forem fan-outs.
- [ ] Não aceitar conformidade estrutural como prova de independência. Cada pair precisa dizer qual
  desacordo observável distinguiria as posições; paráfrases da mesma pergunta não contam.

**Bloqueia `open`:** modo omitido ou herdado; campos de overlay presentes quando disabled; matriz
incompleta quando enabled; ou “diversidade” sustentada apenas por nomes, roles ou redação distinta.

## 3. Pergunta única, fronteiras e não sobreposição

- [ ] Todo seat responde à mesma pergunta refinável das initial definitions; subperguntas apenas
  repartem ataques/observações, não criam quatro pesquisas paralelas.
- [ ] Produzir uma matriz seat × questão × corpus × evidência esperada antes do record final. Cada
  questão load-bearing tem um owner; sobreposição intencional é marcada como replicação e possui
  regra de adjudicação.
- [ ] Corrigir as sobreposições atuais: A (declaração/configuração) cruza C
  (normas/mecanismos), e B (execução/preservação/closes) cruza D (propostas não executadas, closes,
  drift e dupla contagem). Não deixar dois seats classificarem a mesma ocorrência sem identidade e
  merge rule.
- [ ] Não transformar divisão por fontes em “lentes”: ledger/manifests, outputs, skills e casos
  históricos são segmentos de corpus. As perspectivas precisam ser diferenças de julgamento
  aplicáveis a um frame comum, ou ser descritas honestamente como partição de coleta.
- [ ] O seat de contracasos deve poder refutar candidatos encontrados pelos demais; não deve ser um
  depósito isolado de negativos sem acesso aos mesmos identificadores.

**Bloqueia `open`:** perguntas materialmente redundantes; quatro objetivos concorrentes; ausência
de owner/merge rule; ou source partition apresentada como diversidade epistemológica — exatamente
um dos controles negativos que D1 pretende detectar.

## 4. Prompts que não definem o resultado de antemão

- [ ] Todo prompt chama os itens de **ocorrências candidatas** e preserva a possibilidade de nenhum
  caso sobreviver. “Lente”, “perspectiva”, “operação relacional” e “efeito composicional” não podem
  aparecer como propriedades já demonstradas.
- [ ] Separar explicitamente menção, prescrição, instanciação, execução e efeito. Nenhum seat pode
  promover um caso por multiplicidade de agentes, presença de `angle`/`role`, `resolved`, síntese ou
  frequência.
- [ ] Tratar a unidade observacional de cinco itens e as classificações do programa como protocolo
  provisório a testar, não como definição canônica.
- [ ] Exigir tentativa de colapso para role, prompt, método, view, partição, agregação, seleção ou
  coordenação; discordância e síntese não são composição por definição.
- [ ] Proibir universalização para trabalho, conhecimento, interfaces ou produto e qualquer claim
  causal sem delta, controle, contrafactual ou avaliação independente.

**Bloqueia `open`:** prompt que pede para “encontrar composições”, pressupõe que perspectivas são
distinguíveis, trata relação/síntese como prova, ou transforma os rótulos provisórios em ontologia.

## 5. Corpus reproduzível, não inflado

- [ ] Congelar um manifest antes do lançamento com commit/digest, path, hash, tipo de fonte,
  período/schema, regra de inclusão/exclusão e identidade de ocorrência.
- [ ] Separar **corpus de ocorrência** de **fontes normativas/contextuais**. README, initial
  definitions e programa limitam claims; não contam automaticamente como ocorrências positivas.
- [ ] Enumerar os paths realmente existentes. Globs amplos (`**/robot-talks/**`, `**/review.md`,
  `.codex/workflow-inputs/**`, “outputs referenciados”) não são um corpus congelado.
- [ ] Quantificar tamanho e duplicação antes de fixar budgets. Duplicatas `.agents`/`.codex`,
  proposal/manifest/ledger/output da mesma sessão e revisões históricas recebem uma provenance key
  comum; ausência de output permanece dado, não vira exclusão silenciosa.
- [ ] Fixar amostragem determinística por estrato e o critério de expansão. “Duas inclusões sem
  novidade” só pode encerrar saturação descritiva da amostra, nunca provar exaustividade.
- [ ] Excluir os outputs gerados pelo próprio D1 do corpus de ocorrência e impedir expansão dinâmica
  depois do freeze. Mudança de corpus requer versão/reconfirmação, não edição silenciosa.
- [ ] Preservar controles de sobrevivência: propostas não executadas, closes sem outputs, outputs
  ausentes e casos históricos incompatíveis com o schema atual.

**Bloqueia `open`:** glob não enumerado; hash/commit ausente; corpus maior que o que budgets e
prompts conseguem ler; duplicação sem identity rule; mistura de autoridade normativa com
testemunhas; ou corpus mutável/self-referential.

## 6. Graph, roles, writes e approver

- [ ] Representar apenas roles válidas. `collector owner` não é role do schema. Ou um único
  `writer` possui `research.md` e `findings.md`, ou o record justifica uma forma compatível com a
  capability sem inventar `collector`.
- [ ] Manter o shape research reconhecível: explorers (2–4) → um writer ↔ skeptics, auditor
  downstream; feedback só se material faltante for plausível e com `loop_cap`. Não embutir
  Robot-Talks nem advisers invisíveis.
- [ ] Declarar todos os seats no graph compilável. Helpers/advisers anteriores entram como inputs
  congelados; se fizerem trabalho dentro do dispatch, precisam ser seats ligados, com role, prompt,
  budget e artifact boundary próprios.
- [ ] Atribuir um único owner por arquivo. Explorers e skeptics retornam material; não editam
  `research.md`, `findings.md` ou `research-initial-definitions.md` em paralelo. O writer preserva
  retornos verbatim antes da síntese e não sobrescreve as initial definitions.
- [ ] Tornar o approver executável, não apenas nominal. Um agent approver deve ser seat singleton
  ligado ao graph, receber o bundle completo e fazer **somente** aprovação. O coverage auditor faz
  trabalho e não pode acumular aprovação.
- [ ] Se o runtime não puder representar esse approver separado, voltar ao gate para escolher uma
  alternativa legítima; não usar um `agent_name` solto que nunca será lançado. `parent` também não
  pode ser substituição silenciosa nem effective approver quando tiver autoria material.
- [ ] Escolher nomes do agent pool, sem reuso e sem self-verification; modelos e budgets devem ser
  concretos e compatíveis com leitura efetiva do corpus.

**Bloqueia `open`:** role `collector`; segundo writer sem ownership não sobreposto justificado;
write collision; helper órfão; graph incompatível com research; final approver fora do launch plan,
fazendo coverage/síntese, ou substituído pelo parent sem novo gate.

## 7. Controles, collapse-tests e aceitação

- [ ] Incluir os seis controles obrigatórios: divisão apenas por arquivos/fontes; instruções
  nominais distintas com o mesmo julgamento; uso isolado de “lens”; concatenação de retornos;
  proposta não executada; close sem output de interação.
- [ ] Para cada categoria/candidate claim, preregistrar testemunha mínima, contraexemplo esperado e
  collapse-test inline. Categoria sem witness fecha como `KILL/no-witness`; categoria indistinguível
  de vizinho nomeado fecha como `KILL/tautological`.
- [ ] Incluir gates distintos e não acumulados: precedent/ownership, non-vacuity e
  definitional-soundness. Owner encontrado vira `build-from-owned`/`already-deployed`, nunca KILL.
- [ ] Exigir matriz final `candidate | owner | witnessed? | sound? | verdict | use-mode`, além da
  tabela de ocorrências. Contagens e frequência não substituem witness/soundness.
- [ ] Definir antecipadamente que ausência de evidência de execução/efeito é resultado legítimo e
  limita a claim; não autoriza o writer a inferir relações novas.
- [ ] Preservar positivos, negativos e ambiguidades em `findings.md`, com cada claim load-bearing
  citando o retorno verbatim em `research.md` e o source `path:line`.

**Bloqueia `open`:** controle obrigatório ausente; categoria sem falsificador/collapse-test;
skeptic com dois gates; precedente tratado como kill; acceptance baseada em cobertura nominal;
ou inexistência de regra que permita “nenhuma composição demonstrada”.

## 8. Condição final de abertura

`open` só pode ocorrer quando existir **um record concreto único** contendo goal/context concisos,
working folder confirmado, mode anti-bias, grupos/agents completos, nomes, prompts integrais,
modelos, budgets, conexões, loops e approver; quando seu route receipt atual estiver intacto; quando
o corpus enumerado e o ownership de artefatos estiverem congelados; e quando o usuário confirmar
esse record exato, seus efeitos, custos e destinos.

Depois do gate, qualquer mudança material em prompt, corpus, graph, mode, approver, budget ou path
invalida a confirmação. Compile somente o record congelado, não edite envelopes/manifests gerados,
e não faça `open` se a compilação exigir reparo manual.

## Base da checagem

- `internal-tools/composition-lab/research/milestone-1/01-repository-inventory/research-initial-definitions.md`
- `internal-tools/composition-lab/orchestration/milestone-1-strategy/04-integrated-program.md`
- `internal-tools/composition-lab/orchestration/milestone-1-strategy/06-dispatch-compliance.md`
- `.claude/skills/domainspec-subagents-strategy/SKILL.md`
- `.claude/skills/research/SKILL.md`
- `.claude/skills/subagents-dispatch-lifecycle/SKILL.md`
- `.claude/skills/register-dispatch/SKILL.md`
- `implementations/contracts/dispatch-type-registry.v1.json`
