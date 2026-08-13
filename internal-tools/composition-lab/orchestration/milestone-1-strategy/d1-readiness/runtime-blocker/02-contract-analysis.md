# Análise contratual do bloqueio de runtime de D1a

## Veredito

O bloqueio é real, mas precisa ser descrito com mais precisão. O runtime atual rejeita qualquer
`connections` não vazio antes de escrever o launch plan
(`implementations/server/runtime/dispatch_workflow.py:120-126`) e, quando não há conexões, gera todos
os assentos com `slots: []` (`dispatch_workflow.py:151-160`) numa única lista sem dependências
(`dispatch_workflow.py:181-201`). Portanto, o record atual de D1a não é compilável e remover suas
arestas não preservaria sua execução: writer, auditor e approver seriam lançáveis sem inputs
upstream e sem ordem governada.

Isso não significa que `connections`, writer, skeptics, auditor e approver dedicado sejam todos
obrigatórios para qualquer research. Significa que os handoffs e os papéis downstream escolhidos
são obrigações do **contrato concreto de aceitação de D1a**. Esse contrato pode ser revisado antes
da confirmação, mas não pode ser silenciosamente achatado para passar no compilador.

## O que é obrigatório, e por qual autoridade

| Elemento | Schema/registry | capability `research` | D1a atual |
|---|---|---|---|
| `connections` | opcional (`register-dispatch/SKILL.md:60`) | dá posição operacional aos grupos (`research/SKILL.md:57`); necessário quando há consumo downstream real | necessário para a topologia escolhida, não por mera tipagem |
| handoff `extractors -> writer` | não exigido pelo appender | necessário se o writer deve consumir retornos dos explorers | necessário; o prompt do writer afirma receber os quatro retornos |
| writer como assento | nenhuma cardinalidade por role | convencionalmente um, mas a obrigação são os arquivos; não há maquinaria obrigatória de writer (`research/SKILL.md:54,136-137`) | necessário porque o parent foi proibido de fazer trabalho e Knuth é o único owner de `research.md` e `findings.md` |
| skeptic | role permitido, não requerido | necessário para o gate que a pesquisa realmente reivindica; `precedent` é obrigatório antes de verdict de novidade (`research/SKILL.md:162-164`) | não é obrigatório em D1a: D1a proíbe classificação, novidade e verdicts; os gates foram deliberadamente adiados para D1b |
| auditor | role permitido, não requerido | grupo explicitamente opcional (`research/SKILL.md:93-95`) | coverage/provenance audit é critério local de aceitação, logo Hamming é obrigatório para este sheet |
| `final_approver` | campo obrigatório; aceita `parent` ou agente dedicado (`register-dispatch/SKILL.md:52`) | auditor dedicado é a escolha natural, não universal | aprovação é obrigatória; Parnas como assento separado é obrigação do desenho atual e da independência escolhida, não do schema |

Assim, a resposta curta é: **sequential handoffs não são obrigatórios pelo schema, mas algum
handoff governado é obrigatório para o D1a atual; writer, coverage auditor e approver dedicado são
obrigatórios pelo sheet atual; skeptics não são obrigatórios em D1a e pertencem a D1b.** A aresta
writer → coverage está tipada como `feedback`, não `sequential`, porque autoriza correção limitada;
coverage → approver e extractors → writer são sequenciais.

## O que `connections: []` violaria

Um record sem arestas pode passar pela validação estrutural e pelo compilador, mas não seria uma
implementação equivalente de D1a:

1. **Falsidade do briefing efetivo.** O writer é instruído a ler “all four extractor returns supplied
   through governed handoffs”, mas seu manifesto teria zero slots.
2. **Ausência de readiness.** O launch plan não representa predecessores; auditor e approver podem
   abrir antes de `research.md`, `findings.md` e do audit return existirem.
3. **Perda de proveniência de inputs.** O runtime não ligaria bytes/hash/produtor dos retornos ao
   assento consumidor. Um path citado em prompt não prova que aquele conteúdo foi o input efetivo.
4. **Perda do loop declarado.** O `feedback` cap 2 e seus prompts verbatim deixariam de existir como
   eventos governados e como evidência de fechamento.
5. **Quebra da semântica da capability.** A função operacional de writer/auditor/approver deixaria
   de ser legível por `connections`; restariam apenas nomes de grupos lançados em paralelo.
6. **Risco de corrida e aprovação vazia.** Terminalidade global no close não prova que o approver
   observou o bundle final nem que o auditor precedeu sua decisão.

Isso não viola automaticamente a forma JSON do ledger. Viola a correspondência sheet → launch
plan → effective inputs → evidência de aceitação. Registrar/abrir essa versão seria uma execução
formalmente válida de outro desenho, não de D1a.

## Alternativas legítimas

### A. Extensão governada do compilador para o DAG atual — preserva melhor o desenho

É a solução com menor deriva epistemológica, mas não é apenas remover a guarda de
`dispatch_workflow.py:121`. A extensão precisa:

- validar o grafo e produzir ready sets/topologia, incluindo `feedback` e seu `loop_cap`;
- lançar inicialmente apenas `extractors`;
- depois da terminalidade, materializar manifestos exatos para o writer com fontes
  `binding-output`, paths, bytes, hashes e `producer_binding_id`;
- materializar de modo análogo writer → coverage e coverage → approver;
- gerar/regerar envelopes somente pela extensão governada, nunca por edição manual;
- preservar attempt/turn ordinals, binding receipts, feedback prompts e terminalidade antes do
  close;
- reconfirmar qualquer instrução ou source boundary alterada.

O validator de manifestos já aceita `repository` e `binding-output`; para `binding-output`, exige um
produtor terminal do mesmo `dispatch_id` (`implementations/server/runtime/service.py:5367-5415`). Há,
portanto, substrato de binding, mas não compilação/scheduling de `connections`. Como hashes, paths e
binding IDs upstream só existem após execução, um launch plan estático com todos os envelopes
pré-gerados não basta; a extensão deve governar materialização por estágio.

### B. Split em vários dispatches — legítimo, mas exige manifestos governados entre estágios

Pode-se substituir o DAG intradispatch por uma cadeia de dispatches fechados, por exemplo:

1. dispatches de extração independentes, cada um com output próprio;
2. dispatch de merge/writer consumindo os outputs congelados;
3. dispatch de coverage audit;
4. dispatch de aprovação ou uma decisão humana explicitamente confirmada.

Isso é compatível com `register-dispatch`: há uma row e um close por dispatch, não por agente ou
grupo (`register-dispatch/SKILL.md:8-22`). Mas as seguintes propriedades são obrigatórias:

- cada dispatch resolve sua própria capability, record, confirmação, open e close;
- working folders não colidem e cada research satisfaz seu próprio contrato de outputs;
- o próximo dispatch só é preparado após paths/hashes/resultados anteriores estarem congelados;
- outputs anteriores entram como fontes `repository`, com `producer_binding_id: null`, pois
  `binding-output` rejeita produtor de outro `dispatch_id`;
- a linhagem até o dispatch produtor permanece citada no artifact/record, embora o runtime veja a
  fonte já congelada como repositório;
- nenhum `feedback` entre dispatches é fingido como loop do dispatch anterior;
- `parent_dispatch_id` só aparece se existir um meta-dispatch real.

Mesmo essa opção requer uma extensão governada capaz de compilar manifestos não vazios para fontes
upstream. O lifecycle manda substituir o manifesto vazio por um
`aci-workflow-input-manifest/v1` exato **através de extensão governada** e reconfirmar mudanças de
source boundary; editar JSON/envelope à mão não é permitido. Split reduz a necessidade de scheduler
DAG e de `binding-output` intradispatch, mas não elimina a lacuna de input binding.

### C. Extensão mínima de manifestos + split — menor incremento de runtime plausível

Se a prioridade for chegar a D1a sem implementar feedback/scheduler completo, esta é a menor rota
tecnicamente coerente:

- adicionar ao compilador uma entrada governada de source manifests por assento, validada e
  incluída no launch-plan digest;
- executar dispatches connectionless estritamente stageados;
- congelar/fechar cada estágio antes de confirmar o seguinte;
- usar apenas fontes de repositório no estágio seguinte.

Ela custa mais dispatches, confirmações e artefatos, e transforma o feedback cap 2 em novos
dispatches de correção explicitamente roteados. Portanto, requer um novo sheet aprovado; não é uma
compilação equivalente do record atual.

### D. Bounded helper — não disponível para este trabalho

`register-dispatch` permite pular registro quando a capability selecionada **possui** um helper
limitado; isso não autoriza o orchestrator a inventá-lo. `research` não possui tal helper. O helper
de `discovery-writing` é restrito ao bootstrap/probe daquela capability e seu retorno não é
evidência persistível separadamente. Usá-lo para D1a seria apropriação indevida de autoridade e um
fallback independente proibido.

### E. Outras capabilities instaladas — nenhuma substitui D1a

- `robot-talks` é uma sessão direta para tensões cross-layer e manda inspeção direta quando a
  pergunta é apenas “como X funciona?”; não possui o contrato de inventário reproduzível nem pode
  ser apresentado como dispatch governado.
- `review` ataca um artefato já existente; não coleta nem sintetiza o inventário inicial.
- `experiment` pré-registra uma hipótese; D1a não testa uma hipótese.
- `domainspec-implement` pode ser a rota para **implementar** uma extensão aceita, após sua própria
  readiness, mas não é uma rota alternativa para executar a pesquisa.

Não há capability LIVE `others`, `plan` ou runtime-managed utilizável: `others` não é routable e o
registry anuncia apenas `legacy-managed` para `research`.

### F. Redução real de escopo — executável em tese, mas não equivalente

Uma research connectionless de um único assento poderia inspecionar todo o corpus e produzir
`findings.md`; a própria capability permite `n = 1`. Isso elimina independência, merge, coverage
audit e aprovação dedicada. Pode ser um novo trabalho menor se o usuário aceitar explicitamente
essa perda e confirmar outro sheet. Não satisfaz os critérios atuais do milestone e não deve ser
vendido como “D1a preservado”. Vários assentos paralelos connectionless também não resolvem a
síntese: o parent foi proibido de trabalhar e nenhum downstream recebe retornos governados.

## Recomendação

Escolher entre duas decisões honestas:

1. **Preservar D1a:** implementar a extensão DAG/materialização intradispatch (Alternativa A).
2. **Minimizar o incremento de runtime:** implementar primeiro compilação governada de manifestos
   de fontes de repositório e refazer D1a como cadeia de dispatches stageados (Alternativa C).

A alternativa C provavelmente chega antes ao inventário, mas altera o desenho e exige nova ajuda
estratégica, novo record e nova confirmação. A alternativa A é a única que torna executável o
record atual sem degradar suas propriedades. Até uma delas existir, o estado correto permanece
**bloqueado antes de confirmação/open**, sem append, launch independente ou handoff manual.
