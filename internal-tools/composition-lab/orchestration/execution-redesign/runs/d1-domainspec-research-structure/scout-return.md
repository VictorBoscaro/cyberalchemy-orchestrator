---
artifact_kind: bounded-internal-scout-return
batch_id: d1-domainspec-research-structure
status: completed
date: 2026-08-13
repository: C:/Users/victo/domainspec-core
revision: 9bfec22712e4675d39c4cf1c21b36dc66614136c
coverage: 3/3
---

# Scout D1 — estrutura declarada de pesquisa do DomainSpec v2

## Binding e escopo

Os três paths estavam sem alteração local e conferiram com o freeze em revisão, bytes e SHA-256 antes da leitura semântica. Este retorno descreve apenas o que os bytes inspecionados declaram, prescrevem ou configuram. Não trata nomes de estruturas, proximidade entre partes ou uma totalidade alegada como prova de composição; não classifica os casos como composição nem como fenômeno vizinho.

## 1. `projects/domainspec-v2/README.md`

### Identidade e autoridade

- Repository: `C:/Users/victo/domainspec-core`
- Revision: `9bfec22712e4675d39c4cf1c21b36dc66614136c`
- Path: `projects/domainspec-v2/README.md`
- SHA-256: `ca5cfbc0a467e3f14e459236d373db4c046f428930c0fae7571246bfe0aeefff`
- Bytes: `6246`
- Source kind: README de projeto; descrição de estado, convenções e boundaries.
- Authority state observado: identifica DomainSpec v2 como owner e `implementation home`, mas também distingue pesquisa local de promoção canônica posterior (linhas 3–4, 24–29). O próprio arquivo não é evidência de execução do programa descrito.

### Observações

| ID | Observação | Evidence state | Seletor |
|---|---|---|---|
| R1 | O projeto declara dois papéis simultâneos para v2: implementation home em migração e programa de research towers. | descrição de estado | linhas 3, 7–12 |
| R2 | A migração é declarada como congelar v1 como fonte de evidência e importar/reformular capacidades necessárias em v2; implementação e pesquisa ocupam superfícies diferentes (`impl/` e programa de towers). | descrição + prescrição de boundary | linhas 7–20 |
| R3 | Uma research tower é descrita como transformação de uma hipótese ou corpus em entendimento source-backed e auditável, incluindo decisões explícitas de borrow, analogy, block e promotion-candidate. | descrição do resultado alegado | linhas 22–29 |
| R4 | O resultado de uma tower é explicitamente impedido de se tornar canônico sem uma decisão governada posterior. | prescrição/guardrail | linhas 27–29 |
| R5 | Cada tower é prescrita a usar duas lanes: Lane Z alterna geração e crítica; Lane A fixa o problema subjacente e propõe uma solução diferente. | prescrição de partes, relações e diferença funcional | linhas 31–36 |
| R6 | O programa enumera quatro towers ativas com pares separados de hipótese/problema; isso declara unidades programáticas, mas não registra que as lanes ou a síntese tenham sido executadas. | descrição de estrutura; ausência de execução no recorte | linhas 38–45 |
| R7 | As duas towers iniciais são declaradas sequenciadas e gated por um dispatch; a rota é expressamente “designed and validated, not yet executed”. | descrição de configuração + ausência explícita de execução | linhas 53–62 |
| R8 | Artefatos pertencem a owners distintos: cada tower guarda seus próprios seed/README, lane receipts, learning pack e notas; artefatos transversais ficam no root `research/` com prefixo `PROGRAM-`. | prescrição de containment/ownership | linhas 64–71 |
| R9 | Uma tower anterior conserva quatro concern lanes e registra a ausência de alternatives lane. | descrição de exceção e gap | linhas 72–74 |
| R10 | O projeto mantém boundaries entre v1/v2, implementação/pesquisa e privado/público, e exclui quatro capacidades com verdict DROP do processo de importação. | prescrição + exclusão declarada | linhas 76–82 |

### Whole alegado, transformações e efeitos

- **Observado:** “DomainSpec v2” é apresentado como projeto/programa que abriga implementação migrada e research towers (linhas 3, 7–12). A tower é apresentada como unidade que transforma hipótese/corpus em entendimento e decisões explícitas (linhas 24–29).
- **Observado:** a estrutura da pesquisa conecta towers, lanes, síntese/decisões futuras e artefatos locais/program-level por referências e convenções (linhas 31–36, 53–71).
- **Desconhecido:** não há, nestes bytes, trace, receipt ou resultado direto mostrando que a transformação alegada por uma tower ocorreu. A rota inicial é declarada não executada (linhas 55–59).

### Ausências, ambiguidades, contradições, exclusões e resíduos

- A expressão “active research towers” (linha 38) coexiste com a declaração de que a rota das duas towers iniciais não foi executada (linhas 55–59). O recorte não define se “active” significa apenas existente/em andamento ou executado.
- O texto não mostra como resultados das duas lanes são combinados; apenas aponta para a Two-Lane Discipline (linha 31).
- Não há medida ou comparação observada de resultado com uma lane versus duas lanes.
- A tower `dcb-correctness` registra um gap de alternatives lane, mas o efeito desse gap não aparece (linhas 72–74).
- Exclusões explícitas: quatro capacidades DROP não são importadas; o moat privado não pode ser publicado; pesquisa não promove artefatos canônicos diretamente (linhas 17–20, 27–29, 78–82).

### Limites

Esta fonte sustenta uma arquitetura declarada e boundaries do programa. Não sustenta que as unidades tenham produzido o resultado alegado, que duas lanes sejam necessárias ou suficientes, que a estrutura seja causalmente responsável por melhor julgamento, nem uma classificação do fenômeno.

## 2. `projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md`

### Identidade e autoridade

- Repository: `C:/Users/victo/domainspec-core`
- Revision: `9bfec22712e4675d39c4cf1c21b36dc66614136c`
- Path: `projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md`
- SHA-256: `cb09d2412e53288ae891ad6d1f03ff5d56c10808824bf0d7e025fc233cd93557`
- Bytes: `2575`
- Source kind: documento de disciplina/convenção de projeto.
- Authority state observado: o cabeçalho declara “discipline (project convention for DomainSpec v2)” (linhas 1–4); o conteúdo prescreve condições para towers e promoção local, mas não registra uma execução.

### Observações

| ID | Observação | Evidence state | Seletor |
|---|---|---|---|
| T1 | Cada tower deve operar duas lanes “in tension” e só fechar após uma síntese que as adjudique. | prescrição de partes, relação e ordem | linhas 6–8 |
| T2 | Lane Z recebe a hipótese como dada e repete geração → ataque por contraexemplo → ajuste; honestidade requer ao menos um contraexemplo real. | prescrição de operação iterativa + critério | linhas 10–19 |
| T3 | Lane A mantém fixo o problema subjacente e deve produzir solução genuinamente diferente, não variante da proposta de Lane Z. | prescrição de invariância e diferença | linhas 21–30 |
| T4 | Cada SEED deve declarar o problema subjacente em uma frase independente da solução; ambas as lanes são medidas contra esse mesmo enunciado. | prescrição de entrada compartilhada e referência comum | linhas 32–38 |
| T5 | O fechamento exige síntese que compare problema resolvido versus reframed, emita uma bridge decision por claim e registre resíduos com owner. | prescrição de join/adjudicação e outputs | linhas 40–47 |
| T6 | Bridge decisions são locais; promoção para template, validator, ontology ou runtime contract requer task-session aprovada separada. | prescrição de boundary e etapa posterior | linhas 49–50 |
| T7 | Duas lanes são justificadas como mínimo que cria tensão e ainda permite join por uma parent synthesis; terceira lane só entra mediante alternativa distinta com owner. | rationale alegado + regra de cardinalidade | linhas 52–57 |

### Whole alegado, transformações e efeitos

- **Observado:** a “tower” é o whole operacional alegado. Ela contém duas lanes funcionalmente distintas, uma referência comum (problema), uma relação de tensão e uma síntese posterior que adjudica resultados e resíduos (linhas 6–8, 32–47).
- **Observado:** Lane Z transforma a formulação da ideia por ciclos de geração, contraexemplo e ajuste; Lane A produz uma solução diferente mantendo um elemento declarado invariável (linhas 12–27).
- **Alegado, não observado:** a razão declarada é evitar que a primeira ideia se torne conclusão inevitável e reduzir anchoring (linhas 7–8, 29–30). Não há trace comparativo ou efeito medido no arquivo.

### Ausências, ambiguidades, contradições, exclusões e resíduos

- A relação “in tension” é nomeada, mas não há protocolo de troca entre lanes antes da síntese (linhas 6–8).
- “Genuinely different”, “strongest counterexample” e “actually solved” funcionam como critérios, mas não recebem procedimento operacional de mensuração neste recorte (linhas 14, 23–24, 44).
- O texto exige registro de resíduos com owner, porém não define formato nem tratamento posterior (linha 47).
- Não há execução registrada, comparação com uma única lane, ou evidência de que duas sejam o mínimo efetivo; essa suficiência aparece como rationale (linhas 52–57).
- Exclusão explícita: Lane A não pode ser variante de Lane Z; terceira lane sem alternativa distintamente owned deve ser incorporada à Lane A (linhas 23–27, 54–57).

### Limites

Esta fonte sustenta um mecanismo prescrito de diferenciação, referência comum, iteração, adjudicação e preservação de resíduo. Não sustenta que o mecanismo tenha sido executado, que previna anchoring na prática, que seus outputs sejam melhores que alternativas, ou que a estrutura deva ser classificada como composição.

## 3. `projects/domainspec-v2/research/domainspec-v2-research-towers.dispatch.json`

### Identidade e autoridade

- Repository: `C:/Users/victo/domainspec-core`
- Revision: `9bfec22712e4675d39c4cf1c21b36dc66614136c`
- Path: `projects/domainspec-v2/research/domainspec-v2-research-towers.dispatch.json`
- SHA-256: `83206a57f4ed8d05a1c623ede6db17ae058e74fcfdc184150d20f2f7096147fd`
- Bytes: `15381`
- Source kind: configuração declarativa de dispatch.
- Authority state observado: configura uma rota de pesquisa, gates, boundaries e estratégia recomendada; `subagent_lifecycle.status` é `none` e `agents` está vazio (linhas 347–350), portanto o próprio arquivo não registra launch ou execução.

### Observações

| ID | Observação | Evidence state | Seletor |
|---|---|---|---|
| D1 | O objetivo configurado é produzir decisões source-backed sobre duas questões, com output final `PROGRAM-HANDOFF.md`, sem promoção canônica. | configuração de objetivo/output/boundary | linhas 2–18 |
| D2 | A rota enumera seis steps: duas tower routes, uma dialectic paralela, uma síntese, uma decisão e um handoff. | configuração de unidades e ordem declarada | linhas 35–263 |
| D3 | As duas tower routes são não paralelas e produzem learning packs distintos, cada qual declarado como evidence artifact. | configuração de steps e outputs | linhas 35–105 |
| D4 | O step dialectic é paralelo, atribui roles `lane_zigzag` e `lane_alternatives`, recebe os dois learning packs, produz dois lane ledgers e usa `parent_synthesis` como join policy. | configuração de paralelismo, papéis, inputs, outputs e join | linhas 106–158 |
| D5 | A convergência do dialectic exige contraexemplo para Lane Z, solução realmente diferente para Lane A e um join que distingue problema resolvido de reframed. | configuração de critérios | linhas 148–157 |
| D6 | A síntese recebe ambos os ledgers e produz `PROGRAM-SYNTHESIS.md`; seus critérios preservam distinções entre alternativas e pedem a menor unidade para trabalho posterior. | configuração de transformação posterior e output | linhas 160–195 |
| D7 | O decision gate recebe a síntese e produz bridge decisions; ele impede promoção direta e exige owner posterior para promotion-candidate. | configuração de adjudicação/boundary | linhas 197–229 |
| D8 | O handoff recebe síntese e decisões e produz `PROGRAM-HANDOFF.md`; não pode mutar templates, validators, ontology ou skill. | configuração de fechamento e boundary | linhas 231–262 |
| D9 | Gates limitam writes ao research scope, verificam a presença das duas lanes medidas contra o mesmo problema e impedem promoção sem task-session posterior. | configuração de gates | linhas 265–286 |
| D10 | A estratégia declara que towers podem rodar independentemente/em paralelo e que role-bound siblings devem evitar anchoring; também exige permissão do usuário e receipts de lifecycle. | configuração + rationale alegado | linhas 288–345 |
| D11 | O lifecycle está vazio, enquanto boundaries atribuem execução a uma future task-session e memory permanece `not promoted`. | ausência explícita de execução + configuração de autoridade futura | linhas 347–376 |
| D12 | O dispatch configura receipts, namespaces, promotion split e eventos observáveis, mas não contém instâncias desses receipts ou eventos. | configuração + ausência de traces | linhas 378–435 |

### Whole alegado, transformações e efeitos

- **Observado:** o whole configurado é um programa de pesquisa que transforma dois seeds em learning packs, depois em lane receipts, síntese, bridge decisions e handoff (linhas 35–263).
- **Observado:** as relações incluem dependência de artefatos entre steps, paralelismo no dialectic, join por parent synthesis, gates de authority e preservação prevista de residues/receipts (linhas 106–195, 265–345, 378–435).
- **Desconhecido:** o arquivo configura transformações e observabilidade, mas não demonstra que ocorreram. `subagent_lifecycle` vazio e a atribuição da execução a uma future task-session são evidência direta dessa ausência no documento (linhas 347–374).

### Ausências, ambiguidades, contradições, exclusões e resíduos

- A ordem entre as duas tower routes não é inequívoca: ambas têm `parallel: false`, enquanto a estratégia afirma que towers são independentes e podem rodar em paralelo (linhas 46, 81, 290–295). O recorte não fornece semântica suficiente do executor para resolver a aparente tensão.
- O dialectic recebe learning packs das duas towers e produz ledgers por tower, mas o arquivo não explicita como entradas são particionadas entre pares de lanes (linhas 128–147).
- `join_policy: parent_synthesis` aparece no dialectic, enquanto o step posterior de síntese usa `join_policy: none`; o recorte não demonstra como esse join é realizado (linhas 148, 160–187).
- Há requisitos extensos de receipt e trace, mas nenhuma ocorrência registrada; não se pode inferir execução a partir da configuração (linhas 328–345, 378–430).
- O residue ledger é listado como técnica e resíduos são exigidos nos receipts, mas seu conteúdo e tratamento não aparecem (linhas 20–33, 328–344).
- Exclusões explícitas: sem promoção canônica; writes limitados ao namespace de pesquisa; mutações de template, validator, ontology, runtime e skill requerem etapa posterior (linhas 265–286, 351–417, 432–435).

### Limites

Esta fonte sustenta que existe uma configuração detalhada de partes, dependências, paralelismo, join, gates, outputs e observabilidade. Não sustenta que a rota tenha rodado, que os handoffs configurados tenham ocorrido, que os efeitos alegados tenham sido observados, ou que a estrutura deva ser classificada como composição, agregação, sequência, configuração, coordenação, containment ou integração.

## Síntese estritamente local do recorte

### Observado

- Os três documentos apresentam a mesma estrutura em níveis diferentes: README do programa, disciplina prescritiva e configuração de uma rota. Eles declaram partes diferenciadas, referência comum, operações próprias por parte, outputs intermediários, relações de dependência/join, adjudicação, residues e boundaries de promoção.
- Os documentos distinguem resultados locais de autoridade canônica e separam explicitamente pesquisa, decisão e promoção posterior.

### Inferido — não finding

- A correspondência entre convenção e configuração sugere intenção de operacionalizar a disciplina, mas intenção e configuração não demonstram execução nem efeito.
- O recorte oferece candidatos a relações e operações para comparação futura; ele não resolve se essas relações constituem composição ou se uma explicação vizinha é mais adequada.

### Desconhecido

- Se a rota foi executada fora deste arquivo, se as lanes trocaram informação, se a parent synthesis integrou ou apenas selecionou resultados, o que foi perdido no join, e se o desenho melhorou qualquer outcome.
- Se os termos e estruturas aqui usados reaparecem de maneira estável em outros recortes do ecossistema.

## Coverage ledger

| Fonte | Binding | Cobertura terminal | Estado |
|---|---|---|---|
| `projects/domainspec-v2/README.md` | revision/bytes/SHA-256 conferidos; path sem alteração local | observações R1–R10, ausências e limites registrados | COMPLETE |
| `projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md` | revision/bytes/SHA-256 conferidos; path sem alteração local | observações T1–T7, ausências e limites registrados | COMPLETE |
| `projects/domainspec-v2/research/domainspec-v2-research-towers.dispatch.json` | revision/bytes/SHA-256 conferidos; path sem alteração local | observações D1–D12, ausências e limites registrados | COMPLETE |

Terminal: `COMPLETE 3/3`. Este estado prova apenas cobertura do lote D1 sob o contrato do scout; não prova cobertura do corpus interno, execução da rota ou ocorrência de composição.
