---
artifact_kind: dispatch-compliance-check
status: operational-check
date: 2026-08-13
scope:
  - 01-evidence-strategy.md
  - 02-composition-strategy.md
  - 03-governance-strategy.md
---

# Checagem operacional dos dispatches do Milestone 1

## Resultado

O programa é executável por partes, mas **nenhuma proposta governada em 01/02/03 está pronta para
`open` tal como escrita**. As três rotas governadas necessárias (`research`, `experiment` e
`review`) resolvem hoje em `legacy-managed` com `tool_profile_ref: host/inherited@1`. O que falta não
é um tipo no registry: faltam precondições locais, um record concreto, confirmação humana desse
record e, em alguns pontos, separação entre contratos incompatíveis.

O menor primeiro dispatch governado válido é uma **research delimitada de inventário do
repositório**, precedida por seu `research-initial-definitions.md` local. Robot-Talks pode vir depois
do inventário, quando houver findings de concerns distintos para confrontar. Isso é mais aderente ao
próprio contrato de Robot-Talks, que manda inspecionar diretamente quando a pergunta ainda é apenas
“como X funciona?”.

## Autoridades operacionais verificadas

- `domainspec-subagents-strategy` decide delegação, capability e overlay anti-bias; não abre, fecha
  nem define topologia.
- `research`, `experiment` e `review` possuem rotas LIVE resolvíveis pelo comando canônico, todas em
  `legacy-managed`.
- `subagents-dispatch-lifecycle` exige: route receipt intacto, record completo, confirmação humana
  explícita, compile, um único open, seats ligados ao parent, verificação terminal e um único close.
- `register-dispatch` é usado indiretamente por `dispatch_workflow open/close`; não deve haver append
  paralelo ou edição manual do ledger.
- O resolver aponta para `.claude/skills/*`. As cinco skills solicitadas são byte a byte idênticas
  entre `.agents` e `.claude`; `register-dispatch` **não é**. A cópia ativa `.claude` exige
  `anti_bias_mode` em toda abertura. Portanto, usar sempre a rota resolvida e o contrato ativo, não
  reconstruir records a partir da cópia `.agents`.

## Matriz de conformidade

| proposta | modalidade correta | estado operacional | requisito antes de executar |
|---|---|---|---|
| inventário/censo do uso real (01 D1; 02 D1; 03 Onda 2) | `research` | executável, mas ainda não abrível | initial definitions dentro do `working_folder`; corpus delimitado; shape de sweep aceita; record completo e confirmado |
| vocabulário, modelos, hipóteses e síntese (01 D2/D4/D6; 02 D3/D6; 03 Ondas 3/4) | `research` | executável downstream | inputs anteriores congelados; initial definitions próprios em cada pasta; matriz de verdicts; lifecycle completo |
| confronto de tensões (01 D3; 02 D2; 03 Onda 1) | Robot-Talks direto | executável após gate específico; não é ledger dispatch | pergunta + assumptions dadas pelo usuário; concerns, perguntas, exclusões e alternativa rejeitada aprovados; criar `dialogue.md` antes do primeiro spawn |
| backlog de protocolos experimentais (01 D5; parte de 03 Onda 4) | `research` | executável | tratá-lo como comparação/priorização de candidatos; não chamar isso de pré-registro nem produzir `criterion.md` |
| pré-registro de um teste (02 D4) | `experiment` | executável apenas como vários dispatches separados | um `experiment-initial-definitions.md` por pasta; uma hipótese por dispatch; designer + skeptic; `criterion.md` congelado antes de qualquer resultado |
| execução/adjudicação de pilotos (02 D5) | downstream ainda não padronizado pela skill `experiment` | **não executável como `experiment` de proposta** | dispatch separado consumindo criterion read-only; se houver código, rota `code` com readiness DomainSpec; não inventar uma rota de run |
| review final (01 D7; 02 D7; 03 Onda 5) | `review` persistido | executável somente quando o bundle existir | corpus exato path/hash; quatro lentes no máximo; output mode e folder confirmados; record completo; `review.md` como único artefato |
| correção após review | capability depende do change request | não pode ser roteada genericamente agora | rotear cada correção pelo seu dono real; review não implementa e `research` não é fallback universal |

## Confirmações humanas ainda necessárias

Uma autorização geral para “seguir até o milestone” não substitui os gates específicos abaixo:

1. **Research longa:** primeiro aceitar a forma proposta (perspectivas, grupos, conexões, outputs e
   pergunta); depois confirmar o record exato do lifecycle com nomes, prompts, modelos, budgets,
   destino, approver e `anti_bias_mode`.
2. **Robot-Talks:** aprovar explicitamente a decomposição concreta e a alternativa rejeitada antes
   de qualquer agente. As estratégias divergem entre três/quatro concerns e na ordem
   inventário↔Robot-Talks; essa escolha não está congelada.
3. **Experiment:** confirmar cada hipótese/criterion como dispatch distinto. O freeze acontece na
   confirmação anterior ao run.
4. **Review:** confirmar `output_mode: persisted`, `working_folder`, corpus congelado e sheet exato.
5. **Anti-bias:** o modo é por abertura e não é herdado. Sem opt-in explícito, materializar
   `anti_bias_mode: disabled`; nesse modo `angle`, `anti_bias`, `anti_bias_pairs` e
   `anti_bias_global` são proibidos no record. Perspectivas/lentes normais continuam nos prompts.

## Initial definitions e artefatos faltantes

- Existe apenas `internal-tools/composition-lab/research/research-initial-definitions.md`. Ele dá o
  contexto amplo, mas **não satisfaz automaticamente** a precondição de uma research cujo
  `working_folder` será uma subpasta diferente. Cada pasta de research proposta em 01/03 precisa
  primeiro de seu próprio `research-initial-definitions.md`.
- Nenhuma pasta experimental contém `experiment-initial-definitions.md`; portanto nenhum D4 de
  `experiment` pode ser desenhado ainda.
- Os três documentos não contêm um opening record fechado: faltam pelo menos `dispatch_id`,
  `schema_version`, `goal`, `context`, `max_loops`, `final_approver`, `working_folder`/`output_mode`,
  grupos com agents, modelos, token budgets, prompts, nomes, conexões e `anti_bias_mode`.
- Para research com `n >= 2`, a pasta deve terminar com `research.md` (retornos coletados) e
  `findings.md` (síntese citada). Não criar artefatos paralelos que substituam esses dois.
- Para Robot-Talks, criar `dialogue.md` imediatamente após aprovação e antes dos agentes; depois
  `reports/<NN-role>.md` e `findings.md`. Não criar record/receipt de dispatch nessa pasta.
- Para review persistido, a pasta contém somente `review.md`. Não persistir `attacks.md`,
  `findings.md` ou transcript.

## Misturas contratuais a corrigir

1. **Helpers invisíveis dentro de um dispatch governado.** A regra de 03 segundo a qual cada
   work-owner chama um helper não pode produzir seats não declarados. Todo seat de um dispatch
   governado deve vir do launch plan compilado e abrir com o binding do parent. Ajuda decisória deve
   ser um seat explícito do graph ou um output da onda anterior; um helper órfão não deve ser
   escondido apenas no contador `helpers`.
2. **Robot-Talks embutido em research/review.** Robot-Talks é sessão autônoma, sem ledger. Research
   pode usar `robot_talks` como dinâmica de grupo quando seu próprio contrato pedir confronto, mas
   isso não cria a sessão persistida definida pela skill Robot-Talks. Review exige attackers
   independentes com `robot_talks: false`.
3. **Backlog versus pré-registro.** 01 D5 e 03 Onda 4 podem produzir backlog por research. 02 D4 só
   pode produzir um `criterion.md` por dispatch experimental. Um catálogo de vários protocolos não
   é um único `experiment` válido.
4. **Proposal versus run.** 02 D5 não pode continuar o dispatch experimental. `SURVIVED` e
   `FALSIFIED` pertencem ao run posterior; a proposta fecha com criterion aceito ou INVALID.
5. **Lentes compostas no review.** 01 combina “fidelidade/proveniência” e
   “operabilidade/gaming”; 02 enumera cinco lentes, acima do grupo canônico de 2–4 attackers. Cada
   attacker guarda uma lente. Adotar as quatro simples de 03 ou abrir review adicional se gaming
   tiver risco concreto.
6. **Approver acumulando trabalho.** Em research, um auditor dedicado pode ser approver somente se
   não executar outra tarefa. Em review, o coverage auditor faz trabalho e não pode aprovar; manter
   um approver separado, como 03 propõe.
7. **Rework tipado antecipadamente.** Um FIX de review é deliverable resolvido, mas não autoriza
   automaticamente “uma research de correção”. A capability do rework depende da mudança pedida.
8. **Paths concorrentes.** 01 usa `research/milestone-1/...`; 03 usa pastas datadas diretamente sob
   `research/`. Escolher um layout antes do primeiro record e congelá-lo; o path confirmado não pode
   mudar sem nova confirmação.

## Menor primeiro dispatch governado válido

### Recomendação

Abrir uma research curta chamada provisoriamente **`repository-lens-composition-inventory`**, sem
pesquisa externa e sem alegações de efeito. Pergunta única:

> Onde o corpus interno delimitado instancia perspectivas distinguíveis, e que evidência preservada
> permite classificá-las como menção, pluralidade declarada, operação relacional ou efeito ainda
> não demonstrado?

Forma mínima recomendada:

- um grupo de 2 explorers, ambos lendo o mesmo corpus delimitado, com perspectivas declaradas nos
  prompts: (a) representação/declaração e (b) execução/artefatos;
- 1 writer downstream para produzir `research.md` e `findings.md`;
- 1 skeptic de `definitional-soundness` em zig-zag com o writer;
- 1 auditor dedicado apenas à aprovação final, fora de grupos de trabalho;
- `anti_bias_mode: disabled`, salvo opt-in específico do usuário;
- sem feedback edge inicialmente; se o skeptic demonstrar material faltante, reconfirmar qualquer
  mudança material e respeitar o loop cap;
- corpus inicial explicitamente congelado: ledger/manifests, sessões Robot-Talks preservadas,
  skills ativas de research/Robot-Talks/review e probes de provenance já citados nas estratégias.

Antes de montar o record, criar no `working_folder` escolhido um
`research-initial-definitions.md` delimitado ao inventário. Como há um único explorer group, um gate
skeptic e corpus bounded, a forma pode ser apresentada diretamente como dispatch completo para o
gate final da lifecycle. Os documentos 01/02/03/06 já constituem ajuda subagente anterior para
decidir essa primeira forma; não é necessário inventar um pseudo-dispatch `plan`.

## Checklist de abertura

- [ ] Selecionar `research` via `domainspec-subagents-strategy` e justificar delegação.
- [ ] Fixar um único `working_folder` e criar/ler integralmente seu
      `research-initial-definitions.md`.
- [ ] Congelar corpus e hashes; distinguir source read-only de artefatos graváveis.
- [ ] Resolver `research` pelo registry em `legacy-managed`; preservar o route receipt intacto.
- [ ] Escolher nomes existentes em `telemetry/agents/agent-pool.yaml`, sem repetição e por role fit.
- [ ] Construir o record completo com schema version do registry, prompts integrais, modelos,
      budgets, groups, connections, approver e `max_loops`.
- [ ] Materializar `anti_bias_mode`; se disabled, remover todos os campos de overlay; se enabled,
      preencher todas as posições e pares exigidos.
- [ ] Garantir que o approver dedicado não esteja em working group nem produza outro artefato.
- [ ] Mostrar ao usuário o record exato, efeitos, custos e destinos; obter confirmação explícita.
- [ ] Compilar sem editar os envelopes gerados.
- [ ] Executar um único `open`; exigir `launch-authorized`, `session_id` e receipts.
- [ ] Lançar somente seats do `launch-plan.json`, com prompt iniciando pelo binding exato. Nunca
      usar `followup_task` não ligado nem persistir stdout do bridge no working folder.

## Checklist de fechamento

- [ ] Aguardar todos os seats e verificar bindings terminais e artefatos reais.
- [ ] Confirmar `research.md` verbatim e `findings.md` citado; cada claim load-bearing aponta para
      retorno/fonte e a matriz usa owner/witness/soundness/verdict/use-mode.
- [ ] Tratar owner encontrado como `build-from-owned`/`already-deployed`, nunca como KILL.
- [ ] Aceitar KILL apenas por `no-witness` ou `tautological`, preservando o negativo tipado.
- [ ] Obter aprovação do approver declarado; não substituí-lo silenciosamente.
- [ ] Contar agents reais, árvore por role, helpers efetivamente autorizados e `loops_used`.
- [ ] Registrar todos os prompts de feedback verbatim, se houver.
- [ ] Construir somente as chaves permitidas do close record e executar um único `close`.
- [ ] Exigir `status=closed` e receipts YAML/orchestration; nunca editar a row de abertura.
- [ ] Só então congelar paths/hashes como input da próxima onda e preparar, por seats explícitos ou
      outputs anteriores, o próximo decision packet.

## Decisão operacional imediata

Não abrir Robot-Talks, research ou review a partir dos documentos estratégicos ainda. A próxima
ação válida é delegar a criação das initial definitions locais e do **record concreto da research
de inventário**, então apresentar esse record ao usuário. O primeiro `open` só ocorre após essa
confirmação.
