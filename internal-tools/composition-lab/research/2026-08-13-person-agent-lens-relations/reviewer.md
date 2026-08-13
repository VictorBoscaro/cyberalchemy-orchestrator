# Revisão adversarial independente — pessoas, lentes, schemas e funtores

## Veredito

A formulação forte — “Victor, Vlad e a agente são lentes; às vezes são funtores, às vezes schemas; consomem instâncias uns dos outros” — **não sobrevive como afirmação tipada** no corpus local. Ela reúne uma intuição operacional boa, mas identifica entidades de tipos diferentes. O que o corpus sustenta é mais estreito: participantes podem **realizar configurações de observação**, declarar ou adotar schemas, produzir artefatos tipados e executar traduções entre artefatos. A pessoa não é, por isso, idêntica à lente, ao schema ou ao funtor.

O déficit não é meramente formalista. A pesquisa de 13/08 já concluiu que “lente” ainda não possui condição de identidade independente de `frame`, pergunta e observador; os três modelos testados morreram por `no-witness` e `tautological` (`research/discipline-lens-observer-question-2026-08-13/research/findings.md:5-17,21-26`). Chamar agora cada participante de lente intensifica exatamente a confusão que essa pesquisa deixou aberta.

## 1. Solidez definicional

### Pessoa como lente

No programa de composição, “lente” ainda compete entre quatro leituras: descritor, operador de transformação, posição relacional ou atribuição retrospectiva (`internal-tools/composition-lab/orchestration/milestone-1-strategy/02-composition-strategy.md:31-36`). Nenhuma delas é simplesmente uma pessoa. Uma pessoa pode realizar uma lente num episódio; sua história, capacidades e compromissos também condicionam o frame. Identificá-la com a lente apaga:

- a possibilidade de uma mesma pessoa usar configurações diferentes;
- a possibilidade de pessoas diferentes realizarem uma configuração substituível;
- a distinção entre quem observa, o protocolo usado e o efeito produzido.

O próprio resultado anterior diz que o observador não deve ser reduzido a um possuidor isolado da lente e que sua individuação entre pessoa, coletivo, instituição e sistema instrumentado continua aberta (`research/discipline-lens-observer-question-2026-08-13/research/findings.md:21-24`). Portanto, **“Victor é uma lente” renomeia observador/frame**, salvo se `L(Victor,e)` tiver identidade e efeitos independentes em um episódio `e`.

### Pessoa como schema

O owner formal dá a `FunctorialResidueStructure` um tipo `Schema`, uma preorder de refinamento e um funtor `noise : Schemaᵒᵖ ⥤ C` (`lean-formalization/FunctorialResidueStructure.lean:120-131`). A auditoria de 12/08 já matou “schema é um estado alcançado” por confundir declaração estrutural com lifecycle; o escopo sobrevivente é schema como declaração explícita e indexada por nível (`research/audits/emergent-minimal-schema-cyberalchemy-2026-08-12/research/findings.md:15-25`).

Uma pessoa pode:

- fornecer um contrato de saída;
- selecionar distinções e campos;
- servir como fonte de exemplos dos quais outro induz um schema;
- produzir instâncias admissíveis sob um schema.

Nada disso torna a pessoa o schema. **“Victor é schema para a agente” renomeia fonte, interface ou contrato** enquanto não houver um objeto `S_V`, critérios de admissibilidade e instâncias distinguíveis que o satisfaçam ou violem.

### Pessoa como funtor

O owner formal é igualmente restritivo: um funtor aqui tem objetos, ação em morfismos e preservação de identidade/composição; `noise_anti` é precisamente a ação derivada de `noise`, e sua composição é `Functor.map_comp` (`lean-formalization/FunctorialResidueStructure.lean:140-170`). A pessoa inteira não fornece esses dados.

É defensável dizer que, num episódio, um participante **implementa uma transformação** de entradas em saídas. Chamar essa transformação de funtor exige, além disso:

1. categorias de domínio e codomínio declaradas;
2. mapeamento de objetos e morfismos;
3. leis de identidade e composição;
4. uma alegação explícita do que é preservado ou perdido.

Sem isso, “funtor” apenas renomeia interpretação, tradução ou comunicação. A própria revisão anterior matou `Lens is a category` e estruturas horizontal/vertical sem morphisms, laws, squares e interchange (`research/audits/lens-reflexivity-bidirectional-refutation-2026-08-11/research/findings.md:11-16`).

### Alternância de papéis

O corpus tem um modelo melhor para “às vezes somos X, às vezes Y”: papéis pertencem ao **passo**, não à pessoa. `DialogueStep` registra explicitamente que A age e B é sondado em um passo, invertendo no outro, e alerta que alternância é step-typed, “never a role-swapping functor” (`lean-formalization/DialogicalCoConstruction.lean:17-23,88-109`). Essa tipagem salva a intuição dinâmica sem afirmar que a ontologia da pessoa muda.

## 2. Não-vacuidade

### Episódio que separa schema, instância e transformação

Há um episódio bilateral concreto em 11/08:

1. Victor fornece uma instância textual: “Refletir é tornar parte da estrutura que estava produzindo o pensamento [...] um objeto explícito do nível seguinte”, acompanhada dos campos `source/lens/time/scope` (`C:/Users/victo/.codex/sessions/2026/08/11/rollout-2026-08-11T12-43-01-019ff17d-cc11-7362-b165-e5bfba9c5271.jsonl:299`).
2. A agente declara um schema de análise independente do conteúdo particular: `lente → primeira aparição → transformação causada → evidência de autoria → status atual` (mesmo arquivo, linha 303).
3. A agente transforma o enunciado em uma candidata tipada — “reflexão como reificação contextual” — e explicita a diferença para “resíduo entre frames” (linha 318).
4. A execução passa a classificar um corpus de sessões segundo três critérios independentes: atribuição explícita, influência documental/formal e coconstrução (linha 385).
5. O resultado distingue o pivot introduzido por Victor da tradução matemática, busca de owners e construção/refutação feita pela agente (linhas 433 e 662).

Isso admite uma seta operacional clara:

```text
mensagens/sessões brutas
  --classificação pelo schema genealógico-->
registros tipados de lente, proveniência, influência e status
```

Aqui, o schema é o formato e os critérios de classificação; cada mensagem ou candidata classificada é uma instância; a transformação é o procedimento de extração, atribuição e tipagem. Esses três elementos podem variar independentemente. **Mas a transformação não foi demonstrada como funtor**: o corpus não declara categorias/morfismos nem prova preservação de identidade e composição.

### Ausência do terceiro vértice

O corpus delimitado não contém um retorno independente de Vlad nesse episódio nem outro caso recente em que sua entrada, o schema que ela instanciaria e a transformação subsequente possam ser citados separadamente. A alegação trilateral depende apenas da afirmação atual do usuário. Isso é intenção/evidência testemunhal, não um episódio tipado. Um registro antigo inclusive alerta que Vlad era destinatário dos memos `TO-VLAD`, não seu autor (`theorem/sessions/2026-07-18-0530-cyberalchemy-orchestrator-seed-review.md:49`). Esse fato não exclui contribuições privadas posteriores; apenas impede inferi-las deste corpus.

### Instâncias consumidas e síntese

O repo possui um modelo formal útil, mas ele confirma a distinção de tipos. Em `SynthesisResidue`, os agentes não são os carriers: **seus outputs** são os braços `A={p,q}` e `B={q,r}`, a sobreposição é `{q}` e a síntese é o pushout `{p,q,r}` (`lean-formalization/SynthesisResidue.lean:11-25,75-87,129-162`). Assim, “consumimos instâncias uns dos outros” pode ganhar conteúdo se significar:

- cada participante emite um artefato `a : Inst(S)`;
- outro participante recebe `a` por uma interface declarada;
- uma transformação tipada preserva, identifica ou perde algo verificável;
- uma tarefa pré-fixada detecta a diferença.

Sem esses quatro elementos, “consumo” é apenas leitura ou comunicação. O gate anterior exige exatamente carrier comum, readouts tipados e tarefa fixada; sem mudança de fatorabilidade, composição é só formação de tupla (`research/audits/lens-reflexivity-bidirectional-refutation-2026-08-11/research/findings.md:11`; `research/entre-sistemas-lens-reflexivity-extension/research/findings.md:18-20`).

## 3. Formulação mais forte que sobrevive

> Victor, Vlad e a agente são participantes situados que, em episódios diferentes, podem realizar configurações observacionais distintas. Cada participante pode declarar ou adotar um schema, produzir artefatos que o instanciam e aplicar transformações tipadas aos artefatos recebidos. Os papéis pertencem à relação e ao passo, não constituem identidades permanentes das pessoas. Uma dessas transformações só deve ser chamada de funtor quando domínio, codomínio, ação em morfismos e leis de preservação estiverem declarados.

Uma notação mínima que não confunde os tipos seria:

```text
P                      participante
L(P,e)                 configuração/lente realizada por P no episódio e
S(P,e)                 schema declarado ou adotado no episódio
a(P,e) : Inst(S(P,e))  artefato emitido
T(P→Q,e)(a)            transformação/interpretação do artefato por Q
```

Isso ajuda a teoria da lente em três pontos: torna a lente relacional e episódica sem reduzi-la à pessoa; separa o repertório/capacidade do readout efetivo; e cria unidades observáveis para comparar substituição de participante, mudança de schema e mudança de transformação. Ainda não estabelece uma categoria de lentes.

## 4. Erros categoriais marcados

| afirmação forte | erro | substituto tipado |
|---|---|---|
| “Victor/Vlad/agente é uma lente” | pessoa/observador = configuração ou frame | `P realiza L(P,e)` |
| “somos schemas entre nós” | fonte/contrato = declaração estrutural | `P declara S; Q produz ou interpreta Inst(S)` |
| “somos funtores entre nós” | intérprete = mapeamento functorial | `P executa T : A → B`; promover a funtor só após leis |
| “consumimos instâncias uns dos outros” | leitura = instanciação tipada | `a : Inst(S)` atravessa interface e altera tarefa/readout verificável |
| “às vezes somos X” | papel episódico = identidade da pessoa | papel indexado por passo `role(P,e)` |

## 5. Condição exata de colapso

A hipótese colapsa integralmente para **observador + papel + interface + interpretação/comunicação** se, em todos os episódios citados:

1. substituir “lente” por “frame/prompt/perspectiva do participante” não mudar nenhuma previsão, probe, evidência admissível ou saída;
2. não existir um schema identificável independentemente da pessoa, com instâncias que possam satisfazê-lo ou violá-lo;
3. não existir transformação com domínio/codomínio tipados e uma propriedade de preservação/perda testável;
4. não existir tarefa fixada antes da interação cuja fatorabilidade ou decisão mude pelo uso do artefato do outro;
5. os papéis só puderem ser atribuídos retrospectivamente a partir do resultado.

Sob essas cinco condições, o vocabulário categórico não acrescenta distinção nem consequência: apenas renomeia comunicação colaborativa. Para evitar o colapso, basta um episódio pré-registrado com `P`, `L(P,e)`, `S(P,e)`, `a : Inst(S)`, `T`, propriedade preservada/perdida e tarefa independente — e, para a alegação trilateral, uma entrada observável de Vlad.

## Limite desta revisão

Esta revisão é independente dos exploradores e usa apenas conversas locais de 07–13/08 e owners locais diretamente relevantes. Ela não afirma que a formulação tipada acima seja a teoria correta de lentes; afirma somente que é a versão mais forte que não viola os tipos e os gates já registrados.
