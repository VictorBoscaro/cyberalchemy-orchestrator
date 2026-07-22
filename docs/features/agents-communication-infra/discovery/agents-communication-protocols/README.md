---
tags: [agents-communication-infra, discovery, protocols, research, review, workers]
node_type: discovery
is_session: false
layer: [application, orchestration]
nature: [research, design]
status: draft
version: 0.1.0
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

O discovery também deve decidir se esses protocolos pertencem integralmente a
`agents-communication-infra` ou se a infraestrutura deve cuidar apenas de transporte e persistência,
enquanto uma feature separada governa pesquisa, execução e revisão.

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

## Perguntas principais

1. Qual feature é dona dos protocolos de pesquisa, síntese, trabalho e revisão?
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

## Pesquisas necessárias

### 1. Inventário do funcionamento atual

Levantar o comportamento real das skills e dos registros existentes:

- [research](../../../../../.claude/skills/research/SKILL.md);
- [review](../../../../../.claude/skills/review/SKILL.md);
- [domainspec-subagents-strategy](../../../../../.claude/skills/domainspec-subagents-strategy/SKILL.md);
- [register-dispatch](../../../../../.claude/skills/register-dispatch/SKILL.md);
- skills e agentes de discovery, SPEC e implementação;
- registros reais em `telemetry/agents/`;
- [test-derivation-engine](../../../../../tools/test-derivation-engine/README.md).

A pesquisa deve distinguir regras efetivamente aplicadas, regras apenas documentadas e convenções
que hoje dependem do agente pai.

### 2. Independência, discussão e decisão coletiva

Pesquisar evidência sobre:

- julgamento independente antes da interação;
- feedback controlado e métodos semelhantes ao Delphi;
- risco de conformidade, cascata informacional e groupthink;
- discussão depois do registro das posições iniciais;
- nova decisão privada depois da discussão;
- unanimidade, objeção bloqueante e tratamento de dissenso;
- limites de ciclos como controle de custo, não como aprovação automática.

O resultado deve recomendar quando agentes podem conversar e quais posições precisam permanecer
registradas antes e depois da conversa.

### 3. Protocolo de pesquisa e síntese

Comparar pelo menos estes modos:

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
forneça apenas:

- referência e hash do artefato analisado;
- parecer `aprovado` ou `precisa de correção`;
- problema e evidência;
- indicação de que o problema impede ou não a aprovação.

Identidade, modelo/provider, tarefa, ciclo, horário, prompt, arquivos alterados, testes executados e
estado do finding devem ser avaliados como metadados capturados automaticamente, não campos que o
revisor precisa preencher manualmente.

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

Antes da promoção para SPEC, executar probes pequenos e reproduzíveis:

- pesquisa com e sem discussão posterior;
- um versus dois sintetizadores;
- criação coordenada de uma SPEC com ownership por arquivo ou por conjunto coerente;
- dois workers tentando escrever em caminhos sobrepostos;
- reviewer avaliando uma versão que muda depois do parecer;
- revisão final reabrindo somente um grupo e depois vários grupos;
- repetição de mensagens e recuperação após interrupção;
- término do limite de ciclos com objeção ainda aberta.

## Resultados esperados do discovery

O discovery deve produzir recomendações, não código. Seu resultado precisa incluir:

- decisão de ownership entre infraestrutura de comunicação e protocolo de trabalho;
- vocabulário mínimo;
- contratos mínimos de atribuição, submissão, discussão, revisão e rework;
- diagramas dos fluxos de pesquisa e workers;
- regras de versionamento e invalidação;
- política de caminhos autorizados;
- política de ciclos e escalonamento;
- fronteira entre barramento e journal;
- experimentos necessários antes da SPEC;
- mapa dos documentos, skills e componentes que precisariam mudar.

## Fora de escopo neste momento

- alterar a SPEC existente;
- implementar o runtime ou o barramento;
- mudar as skills atuais;
- escolher valores definitivos para todos os limites de ciclo;
- criar schemas finais de eventos ou banco de dados;
- assumir que consenso implica correção;
- assumir que modelos ou providers diferentes garantem independência.

## Critério para avançar

O discovery poderá ser promovido somente depois de revisão independente que confirme:

- cobertura dos fluxos de pesquisa e execução;
- separação clara entre transporte e autoridade;
- ausência de campos sem necessidade demonstrada;
- ausência de decisões inventadas pelo agente pai;
- tratamento explícito de versão, rework, invalidação e não convergência;
- recomendação clara sobre a feature responsável pelo protocolo.
