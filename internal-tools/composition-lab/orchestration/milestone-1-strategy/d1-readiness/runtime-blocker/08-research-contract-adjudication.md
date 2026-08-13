---
artifact_kind: research-contract-adjudication
status: decided
date: 2026-08-13
scope: n-1-research-findings-contract-and-descriptive-inventory-fit
---

# Adjudicação do contrato de `research` para o inventário D1

## Pergunta

Sob o contrato vigente da capability `research`, uma pesquisa `n = 1` pode produzir apenas um
inventário descritivo de ocorrências, sem candidatos e sem a matriz
`candidate | owner | witnessed? | sound? | verdict | use-mode`; e o precedente local
`2026-08-06-irreducible-research-team-design` autoriza essa forma?

## Veredito estrito

**Não.** `n = 1` altera explicitamente apenas o conjunto de arquivos exigidos: requer
`findings.md` e dispensa `research.md`. Não há qualificador por cardinalidade na regra seguinte,
que exige uma linha da matriz de veredito por candidato
([`.claude/skills/research/SKILL.md:127-153`](../../../../../../.claude/skills/research/SKILL.md#L127)).

Isso não implica que toda pesquisa `n = 1` deva lançar exatamente três skeptics. O contrato exige
que as dimensões `owner`, `witnessed?` e `sound?` sejam resolvidas para cada candidato, e diz que um
skeptic guarda um único gate; ele não equipara as três dimensões a uma cardinalidade universal de
três agentes
([`.claude/skills/research/SKILL.md:46-78`](../../../../../../.claude/skills/research/SKILL.md#L46)).
Há uma obrigação operacional mais estreita: nenhum veredito de novidade pode sair antes de um
skeptic de precedent
([`.claude/skills/research/SKILL.md:158-165`](../../../../../../.claude/skills/research/SKILL.md#L158)).

Um inventário puramente descritivo que proíbe `candidates` e `verdicts` está, portanto, fora do fit
atual de `research`. Ele deve ser reroteado para uma capability que possua esse trabalho, ou aguardar
uma mudança formal do contrato. Confirmação humana, `meta: true`, `n = 1` e precedente de execução
não criam exceção.

## Texto normativo

1. A capability declara possuir julgamento, topologia, evidência, outputs e vereditos de research
   ([`.claude/skills/research/SKILL.md:20-31`](../../../../../../.claude/skills/research/SKILL.md#L20)).
   Logo, schema ou ledger não podem relaxar sua epistemologia.
2. `n >= 2` exige `research.md` e `findings.md`; `n = 1` exige somente `findings.md`. A frase
   imediatamente posterior explicita que a exigência é sobre arquivos, não sobre quem os escreve
   ([`.claude/skills/research/SKILL.md:127-137`](../../../../../../.claude/skills/research/SKILL.md#L127)).
   Essa é a única redução expressa para `n = 1`.
3. A findings shape é universal em sua redação: "per candidate, a row", com owner sempre
   preenchido, testemunha, soundness, veredito e use-mode
   ([`.claude/skills/research/SKILL.md:139-153`](../../../../../../.claude/skills/research/SKILL.md#L139)).
   Um arquivo chamado `findings.md` não satisfaz o contrato quando omite essa substância.
4. As três dimensões têm gates distintos e, quando vários skeptics rodam, seus gates devem ser
   distintos. O texto "one gate per skeptic" impede acumular dois gates em um skeptic, mas não diz
   "one skeptic per matrix column in every dispatch"
   ([`.claude/skills/research/SKILL.md:64-78`](../../../../../../.claude/skills/research/SKILL.md#L64)).
5. O roteador deve ler integralmente a capability selecionada, que possui papéis, evidência,
   artefatos e vereditos; se nenhuma capability instalada possui o trabalho, deve parar em vez de
   inferir um tipo porque o ledger aceita o nome
   ([`.codex/skills/domainspec-subagents-strategy/SKILL.md:20-34`](../../../../../../.codex/skills/domainspec-subagents-strategy/SKILL.md#L20)).

## Precedente histórico

O registro `2026-08-06-irreducible-research-team-design` é `dispatch_type: research`, `meta: true`,
com um explorer, `n = 1`, nenhum skeptic/auditor e close `resolved`
([`telemetry/agents/subagents-dispatch.yaml:5880-5897`](../../../../../../telemetry/agents/subagents-dispatch.yaml#L5880)).
Seu `findings.md` é uma proposta de desenho de time: define um decision frame, assentos, topologia,
fallback e recomendação, mas não contém a matriz GO/KILL exigida
([`research/repository-irreducible-problem-inventory/team-design/findings.md:13-28`](../../../../../../research/repository-irreducible-problem-inventory/team-design/findings.md#L13),
[`research/repository-irreducible-problem-inventory/team-design/findings.md:30-121`](../../../../../../research/repository-irreducible-problem-inventory/team-design/findings.md#L30),
[`research/repository-irreducible-problem-inventory/team-design/findings.md:145-157`](../../../../../../research/repository-irreducible-problem-inventory/team-design/findings.md#L145)).

Esse precedente não antecede o contrato relevante. A skill com gates e verdict matrix já estava no
repositório desde `98b27c13c7c311941abd0d340ce0af03bd8128c7` (2026-07-20); a versão imediatamente
anterior ao dispatch, em `f30997237529a333959c11b9bed13a3b047409f8` (2026-08-03), mantinha as
mesmas obrigações relevantes. Portanto o precedente registra uma prática historicamente aceita,
mas não uma exceção contratual. A classificação sustentável é **drift/não conformidade anterior**,
não waiver. O review posterior, registrado em
[`telemetry/agents/subagents-dispatch.yaml:5898-5916`](../../../../../../telemetry/agents/subagents-dispatch.yaml#L5898),
não altera retroativamente o contrato do research nem supre a matriz ausente.

## Inferências e limites

- **Inferência sustentada:** o contrato separa cardinalidade de outputs e validade epistemológica
  dos findings. A primeira varia com `n`; a segunda não.
- **Inferência sustentada:** os gates são dimensões de julgamento por candidato, enquanto skeptics
  são uma forma de atribuir ataques. Não se pode apagar dimensões, mas também não se deve inventar
  a regra "sempre três skeptics".
- **Inferência sustentada:** `meta: true` descreve o record; nenhuma cláusula da skill o trata como
  waiver.
- **Inferência sustentada:** transformar cada ocorrência em "candidato" apenas para preencher a
  matriz seria conformidade nominal e violaria a regra `claim <= proof`; o próprio desenho D1 proíbe
  fabricar candidates/verdicts
  ([`04-epistemic-replan.md:117-125`](04-epistemic-replan.md#L117)).
- **Limite:** este parecer não decide qual capability deve possuir a coleta descritiva nem propõe o
  novo contrato. Decide apenas que o contrato atual de `research` não a admite nessa forma.

## Disposição de 04 e 06

### `04-epistemic-replan.md` — KEEP como bloqueio, com uma precisão

O artefato identifica corretamente a incompatibilidade entre sua matriz observacional e a findings
shape de research, bloqueia o preparo até mudança vinculante ou reroteamento e recusa verdicts
fictícios
([`04-epistemic-replan.md:94-125`](04-epistemic-replan.md#L94)). Seu gate de GO repete corretamente
que é necessária mudança aceita da capability ou redesenho sob outra capability
([`04-epistemic-replan.md:270-281`](04-epistemic-replan.md#L270)).

Precisão: a admissão de `n = 1` citada nas linhas 60-63 sustenta somente `findings.md` sem
`research.md`; não sustenta que a forma descritiva seja "executável em tese" sob `research`.
Essa frase deve ser lida sob o bloqueio explícito das linhas 117-125, não como um GO parcial.

### `06-replan-compliance.md` — FIX; não usar como plano executável

O artefato afirma que vários dispatches independentes `n = 1` são válidos
([`06-replan-compliance.md:10-31`](06-replan-compliance.md#L10)) e propõe seis records cujos
explorers e writer devem extrair/sintetizar sem classificar candidatos ou efeitos
([`06-replan-compliance.md:152-161`](06-replan-compliance.md#L152)). Isso resolve colisão de arquivos
e limitação de handoff, mas não satisfaz a findings shape. Um auditor final emitindo uma matriz
genérica `PASS-or-bounded-corrections` não transforma retroativamente os cinco findings anteriores
em matrizes por candidato.

Logo, as declarações de validade nas linhas 15-17, 23-27 e 111-115 e a decisão de adoção nas linhas
230-236 ficam **rejeitadas sob `research`** até reroteamento ou mudança formal. As análises de
runtime, isolamento, arquivos e embed de bytes podem ser reaproveitadas como constraints de um novo
desenho; não autorizam os records propostos.

## Owner e processo de mudança

Há duas rotas legítimas, sem exceção ad hoc:

1. **Reroute:** o owner de roteamento é `domainspec-subagents-strategy`. Ele deve selecionar uma
   capability instalada que possua inventário descritivo; se nenhuma existir, deve parar
   ([`.codex/skills/domainspec-subagents-strategy/SKILL.md:10-34`](../../../../../../.codex/skills/domainspec-subagents-strategy/SKILL.md#L10)).
   Depois disso, o programa D1 deve ser redesenhado e voltar ao gate com records novos; não se
   reaproveita a confirmação de `research`.
2. **Mudança de capability:** o owner semântico é o próprio contrato da skill `research`, que
   declara possuir evidência, outputs e vereditos. Uma mudança aceita deve editar explicitamente a
   skill para definir quando o modo descritivo dispara, quais artefatos produz, quais gates o
   aceitam e como evita sobreposição de routing. Alterar o que uma skill faz também exige atualizar
   sua description e verificar sobreposição com skills irmãs
   ([`.codex/skills/create-skill/SKILL.md:59-62`](../../../../../../.codex/skills/create-skill/SKILL.md#L59)).

Até uma dessas rotas ser concluída e aceita em artefato vinculante, a disposição é:
**04 permanece bloqueante; 06 não pode ser executado como research; o precedente n = 1 não concede
waiver.**
