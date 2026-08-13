---
tags: [agents, ephemeral-infrastructure, work, provenance, observability]
node_type: essay
nature: [explanatory]
status: draft
version: 0.1.0
last_updated: 2026-08-13
authority: proposal-only
owning_plan: plans/governed-agent-work-infrastructure/PLAN.md
derives_from:
  - plans/governed-agent-work-infrastructure/essays/work-and-knowledge-system-overview.md
---

# Infraestrutura efêmera para trabalho com agentes de IA

> Este texto explica uma ideia da arquitetura proposta. Ele não afirma que o ciclo completo de
> provisionamento e remoção já esteja implementado.

## A ideia

Agentes precisam de uma estrutura para trabalhar juntos. Alguém precisa definir o resultado
buscado, dividir o trabalho, fornecer contexto, estabelecer limites, conectar participantes e
acompanhar o que acontece. Sem essa estrutura, aumentar o número de agentes apenas transfere para
uma pessoa o esforço de coordená-los.

Essa estrutura, porém, não precisa permanecer inteira depois que o trabalho termina. Ela existe
para tornar executável um objetivo específico. Quando deixa de cumprir essa função, seus recursos
operacionais podem ser liberados. O que não pode desaparecer é aquilo que permite compreender o
resultado: o que foi autorizado, o que aconteceu, quais decisões foram tomadas e quais evidências
as sustentam.

Chamamos essa combinação de **infraestrutura efêmera de trabalho**: a montagem operacional é
temporária; a história necessária para compreender e avaliar o trabalho é persistente.

## Uma infraestrutura que nasce com o trabalho

O ponto de partida não é um conjunto permanente de agentes esperando tarefas. É uma intenção que
ainda precisa ganhar forma. O sistema propõe como avançar: relaciona o objetivo às partes do
trabalho, define quais participantes assumem cada responsabilidade, distribui o contexto necessário
e explicita até onde cada participante pode decidir. Quando essa proposta é autorizada, ela se torna
o dispatch que delimita a execução.

É a partir desse limite que a infraestrutura operacional pode ser montada. Instâncias de agentes
são iniciadas para ocupar papéis específicos. Canais são abertos para as interações permitidas.
Contextos, ferramentas e recursos são disponibilizados conforme a responsabilidade de cada papel.
A execução mantém estado suficiente para encaminhar mensagens, observar dependências e devolver
decisões que ultrapassem a autoridade concedida.

Esses elementos pertencem à execução porque sua configuração responde àquele trabalho. Outro
objetivo pode exigir outros agentes, conexões, contextos, ferramentas ou limites. Manter a montagem
anterior como se ela fosse universal confundiria uma configuração local com a infraestrutura
compartilhada que permite criá-la.

## O que termina e o que continua

Quando o trabalho chega a um estado terminal, agentes podem ser encerrados, canais fechados e
recursos liberados. Sandboxes, worktrees, sessões de modelo, credenciais temporárias e filas locais
são exemplos possíveis dessa camada operacional. A arquitetura final ainda precisa decidir quais
desses mecanismos usará; o princípio não depende de uma tecnologia específica.

Encerrar a operação não deve apagar seu significado. O dispatch autorizado precisa continuar
ligado à tentativa que o executou. Os eventos da tentativa precisam mostrar o que ocorreu. Decisões
devem preservar quem podia tomá-las e por quê. Resultados precisam permanecer relacionados às
evidências que permitem avaliá-los. Sem essas ligações, guardar apenas o artefato final preservaria
uma resposta, mas perderia a base para confiar nela ou reutilizá-la.

A fronteira pode ser resumida assim:

| Pode terminar com a execução | Precisa sobreviver quando relevante |
|---|---|
| instâncias de agentes e sessões | dispatch e limites autorizados |
| canais e estado de entrega | eventos e decisões atribuíveis |
| ambientes e recursos temporários | resultados, evidências e proveniência |
| contexto operacional derivado | conhecimento aceito, com versão e escopo |

Persistir não significa promover tudo a conhecimento. Eventos registram o que aconteceu; não
garantem que uma afirmação seja verdadeira. Um resultado somente se torna conhecimento reutilizável
quando uma decisão o aceita com evidência, versão, estado e escopo definidos.

## O que não é efêmero

“Infraestrutura efêmera” não significa que o sistema inteiro desaparece. Alguma infraestrutura
compartilhada precisa continuar disponível para receber uma intenção, registrar a autorização,
provisionar a execução, preservar sua história e recuperar o que foi aprendido. O kernel de
orquestração, os registros duráveis, os mecanismos de identidade e os serviços de conhecimento são
candidatos a essa camada persistente.

A distinção correta, portanto, não é entre um sistema efêmero e outro permanente. É entre duas
responsabilidades do mesmo sistema:

```text
infraestrutura compartilhada e persistente
        ↓ provisiona
ambiente temporário para um trabalho delimitado
        ↓ produz
história, resultados e evidências persistentes
        ↓ podem alimentar
conhecimento aceito para trabalhos futuros
```

O ambiente temporário absorve a complexidade local da execução. A infraestrutura compartilhada
garante que encerrá-lo não rompa a continuidade entre objetivo, trabalho, resultado e conhecimento.

## Um ciclo completo

Considere uma investigação que exige dois agentes independentes e um revisor. Depois que a pessoa
autoriza o dispatch, o sistema inicia três participantes com contextos e autoridades diferentes.
Os investigadores trabalham sem ler a resposta um do outro. Quando ambos terminam, o revisor
recebe os resultados e as evidências permitidas, compara as conclusões e registra seu parecer.

Encerrada a tentativa, aquelas sessões e seus canais não precisam continuar ativos. Permanecem o
dispatch que autorizou a independência, os registros que demonstram a ordem de revelação, as
contribuições produzidas, o parecer do revisor e as evidências associadas. Se uma conclusão for
aceita para uso futuro, ela permanece também como conhecimento dentro de um escopo explícito.

O exemplo mostra por que as duas metades dependem uma da outra. Sem recursos temporários, cada
trabalho carregaria indefinidamente sua maquinaria. Sem história persistente, encerrar a maquinaria
apagaria justamente o que torna seu resultado compreensível.

## A fronteira ainda aberta

O princípio está definido em nível conceitual, mas sua fronteira técnica ainda não. É preciso
decidir quais recursos nascem por tentativa, quais são compartilhados entre trabalhos, por quanto
tempo registros operacionais permanecem e quando um artefato pode ser removido sem prejudicar
auditoria, recuperação ou conhecimento aceito.

O repositório já preserva parte do trabalho de agentes e alguns eventos sem reescrever o histórico.
Ainda não oferece de ponta a ponta o provisionamento, a execução e o encerramento descritos aqui.
Por isso, **infraestrutura efêmera de trabalho** nomeia hoje uma responsabilidade proposta: permitir
que a operação termine sem permitir que o significado do trabalho desapareça com ela.

## Referência

Esta ideia foi extraída de [Um sistema para ampliar o trabalho com agentes de
IA](work-and-knowledge-system-overview.md), especialmente das relações entre trabalho delimitado,
execução verificável, continuidade do conhecimento e infraestrutura temporária.
