# Skill Protocol Compilation — Initial Definitions

## Context

O Cyberalchemy Orchestrator busca permitir que uma pessoa peça um trabalho por meio de uma skill e
receba uma execução multiagente compreensível, governada e verificável. Hoje, a intenção expressa
pela skill, a escolha da estratégia de subagentes e a topologia efetivamente executada ainda não
formam um único contrato reutilizável.

Para o usuário, o problema central não é escolher estruturas internas do runtime. É poder dizer o
que precisa ser feito, compreender como o sistema pretende realizar o trabalho e confiar que a
estrutura apresentada será a estrutura executada. Resolver isso evita redesenhar manualmente a
orquestração toda vez que a mesma skill é usada.

## Purpose

Este documento estabelece o significado inicial de um protocolo de execução de skill antes de
qualquer schema ou experimento ser desenhado. Ele servirá de contexto para decidir posteriormente
qual é a menor representação legível por pessoas que também possa ser transformada em uma execução
determinística.

## Experiment Question (Can be refined)

Como representar o significado de execução de uma skill, suas variações permitidas e sua ligação
com uma execução concreta de maneira simples o bastante para uma pessoa compreender e precisa o
bastante para o sistema validar, persistir e executar?

## Confirmed Product Constraints

- O protocolo deve começar pelo significado de negócio da skill e da execução, não por nós,
  arestas, tabelas ou detalhes do bus.
- A representação deve ser tão simples quanto possível para uma pessoa ler e revisar.
- Parâmetros aparecem depois do significado estável e permitem variar a execução sem reescrever
  toda a definição.
- O protocolo de uma skill deve poder ser persistido e reutilizado entre invocações.
- Uma mudança relevante na skill não pode reutilizar silenciosamente um protocolo incompatível.
- A execução concreta deve poder ser registrada e posteriormente transformada em instruções
  determinísticas para a infraestrutura de agentes.
- Uma visualização, como Mermaid, pode ser derivada, mas não precisa ser a representação principal.

## Current Evidence Baseline

- A discovery candidata já descreve a ideia de um `SkillExecutionProfile` ligado a uma revisão da
  skill e compilado para um `DispatchSpec`.
- O repositório já registra dispatches em um ledger e já possui conceitos de grupos, conexões,
  rounds, agents, sessions e receipts.
- A infraestrutura de comunicação já separa coordenação determinística de respostas de modelos,
  que continuam sendo observações não determinísticas.
- `domainspec-subagents-strategy` já representa propostas estruturais e concretas, mas ainda não
  resolve um protocolo persistente para toda skill.
- A skill existente `skill-decomposer` extrai capacidades reutilizáveis de fontes maiores; ela não
  define atualmente um protocolo de execução para uma revisão de skill.
- A conversa identificou possíveis variações de custo ou rigor, provisoriamente chamadas de Light,
  Medium e Hard, mas ainda não decidiu como representá-las.

## Known Gaps

- Ainda não definimos a menor unidade de significado que um protocolo precisa preservar.
- Ainda não sabemos se Light, Medium e Hard são presets, perfis ou outra abstração.
- Ainda não definimos quais mudanças da skill tornam um protocolo incompatível.
- Ainda não definimos como encontrar de forma segura todas as dependências relevantes da skill.
- Ainda não definimos a forma canônica persistida nem sua projeção para tabelas ou para a UI.
- Ainda não definimos quem cria, revisa, confirma, ativa, substitui ou revoga um protocolo.
- Ainda não definimos a fronteira exata entre protocolo da skill, estratégia de subagentes,
  `DispatchSpec`, scheduler, bus e telemetry.
- Ainda não definimos quais parâmetros são universais e quais pertencem ao significado específico
  de cada skill.
- Ainda não demonstramos que uma decomposição automática preserva corretamente as obrigações da
  skill.
