# Pair 06 — Reconstrução

## Resposta executiva

O sistema já tem um esqueleto durável e ligado por integridade. Quando algo entra no runtime, ele consegue preservar a sessão, o dispatch declarado, identidades, alguns inputs, o retorno bruto de pesquisa, fatos extraídos, recibos e projeções reconstruíveis.

Isso ainda não equivale à reconstrução completa do trabalho. Hoje não há garantia de que todo turno real passe pelo registro, não há saída terminal exata para cada agente, nem uma disposição obrigatória para cada contribuição esperada. Também falta a ponte que diz por que uma referência sustenta ou contradiz uma conclusão.

O próprio trabalho deste AS-BUILT torna o limite visível: o Dispatch está registrado em arquivo, mas no snapshot vivo consultado ele tinha zero links de sessão, bindings, ingestions, Scouts e capturas. Os arquivos produzidos existem, porém um terceiro não consegue atribuí-los aos assentos a partir do runtime.

## O grafo que pode ser reconstruído

```text
Dispatch em YAML
  objetivo/contexto/topologia/prompts declarados
        |
        v  [ausente neste AS-BUILT]
Session-to-Dispatch link + digest do snapshot
        |
        v  [ausente neste AS-BUILT]
binding do turno: grupo/assento/turno/Attempt/agente/estado
        |
        v  [ainda não existe como obrigação geral]
input efetivo selado -> saída terminal/efeitos exatos
        |
        v
contribuição: captured | partial | missing + disposição
        |
        v
retorno bruto + pergunta/resposta/referência/problema/claim/formalização
        |
        v  [claim-support checks ainda não implementados]
evidência independente: delivered/observed/claimed_consulted/supports/contradicts
        |
        v
journal/recibos -> projeções reconstruíveis -> visão fria agregada
```

Esse grafo deve ser lido como um esqueleto de declarações e evidências admitidas. Ele não contém raciocínio não registrado, ações não capturadas ou autoridade externa que o runtime ainda não saiba verificar.

## O que o store vivo demonstra

No instante da consulta read-only:

- 180 Dispatch links;
- 22 bindings, todos resolvidos para uma identidade de agente;
- 415 ingestions: 130 `exact`, 36 `metadata_only`, 249 `opaque`;
- 1 Scout e 1 recommendation;
- 1 captura APT com 6 fatos: pergunta, resposta, referência, problema, claim e formalização;
- 0 Agent Attempts, 0 execution requests e 0 agent-reference deliveries;
- para este AS-BUILT: 0 links, bindings, ingestions, Scouts e capturas.

Esses números demonstram população parcial. Eles não demonstram cobertura. `exact` significa que bytes, tamanho e digest foram preservados; não significa que o conteúdo foi entregue, lido, usado ou que sustenta uma conclusão.

## O que ainda não pode ser inferido

- `claimed_consulted` não prova acesso ou leitura.
- Um locator não prova suporte a um claim.
- Um prompt no Dispatch não prova que o host o entregou.
- Um binding não prova execução correta nem autoria de um arquivo posterior.
- Estado terminal não identifica a saída produzida.
- Uma captura ou resposta não prova verdade, aprovação ou autoridade.
- `answer_ids` ligado a um claim não é evidência externa de suporte.
- `invoked_by` ou outro identificador declarado não prova autenticação ou entitlement.
- Testes aprovados não provam adoção universal pelos hosts.
- Código atual não prova qual código governou trabalho passado.
- Ausência de registro não prova ausência de trabalho.
- Um arquivo com campo de autor não é autoria autenticada pelo runtime.

## Perguntas que um terceiro ainda não consegue responder

1. Qual decisão e qual pessoa legitimamente autorizaram cada trabalho e cada limite?
2. Qual input efetivo cada assento deste AS-BUILT recebeu?
3. Qual saída e quais mudanças cada Attempt produziu?
4. Quais fontes foram apenas listadas, quais foram entregues, observadas ou consultadas?
5. Qual checagem independente sustenta ou contradiz cada claim?
6. Por que alternativas foram rejeitadas e onde esse raciocínio foi ligado ao resultado?
7. Qual porcentagem do trabalho real dos hosts foi capturada de ponta a ponta?

## Próximas tarefas — na ordem que compra reconstrução real

### 1. Tornar a adoção do host obrigatória e reconciliável

Primeiro elo ausente: Dispatch → Session/Dispatch link → bindings de todos os turnos.

Isso compra a certeza de que trabalho esperado não aconteceu fora da memória sem ser detectado. A prova de conclusão é uma reconciliação que mostre, para cada assento e turno, exatamente um binding e um estado terminal, além de categorias explícitas para faltantes, órfãos e extras.

### 2. Persistir a saída terminal exata por turno

Primeiro elo ausente: binding/Attempt → artefato de saída/efeitos exatos.

Isso compra a resposta a “quem fez o quê” e impede atribuir ao agente um arquivo que apenas apareceu depois de sua terminação. A saída precisa ser content-addressed e comprometida junto com o estado terminal.

### 3. Exigir uma disposição para cada contribuição esperada

Primeiro elo ausente: contribuição esperada → `captured`, `partial` ou `missing`, com checagem/disposição.

Isso compra completude mensurável. Silêncio deixa de significar, indistintamente, falha, esquecimento ou ausência intencional.

### 4. Separar autoridade declarada e evidência epistemológica

Primeiros elos ausentes: Dispatch → decisor declarado/evidência/status de verificação; claim → evidência checada.

Isso compra duas propriedades diferentes: explicar por que o trabalho foi permitido sem fingir entitlement externo, e explicar por que uma conclusão merece confiança. A checagem precisa preservar separadamente `delivered`, `observed`, `claimed_consulted`, `supports` e `contradicts`, sempre com checker, método/versão, outcome e selector exato.

### 5. Só então criar a visão fria agregada

Primeiro elo ausente: join de binding/saída/contribuição na superfície de leitura.

Isso compra usabilidade: uma pessoa de fora consegue reconstruir o trabalho sem conhecer todos os stores e APIs. Essa visão deve continuar não-autoritativa e mostrar cada elo ausente como desconhecido, nunca inventá-lo.

## Convergência worker/reviewer

Na primeira rodada, o reviewer estreitou as alegações: o grafo é um esqueleto declarado e ligado por integridade; bindings não têm saída terminal; input efetivo não é selado universalmente; ingestão exata não implica consulta; não existe uma query agregada; e os recibos de 5 e 23 testes devem permanecer separados.

Na segunda rodada, o reviewer corrigiu a prioridade. A ordem aceita foi: adoção do host, saída terminal, disposição das contribuições, semântica de decisão/autoridade e checagens de claims, e somente depois a visão agregada. Também substituímos “autoridade verificada” por decisor declarado, evidência e status de verificação separados.

Não restou dissenso.

## Evidência de prova

- Worker: 5 testes selecionados, 6.402s, `OK`.
- Reviewer: 23 testes direcionados, 34.938s, `OK`.
- Os recibos são independentes; não representam uma única suíte de 28 testes.
- Os testes escreveram somente em `C:/tmp/cyberalchemy-as-built/pair-06-reconstruction`.
- O store vivo foi aberto em modo read-only.

Detalhes atômicos, comandos, dimensões de confiança e referências de linha estão em `pair-06-reconstruction.json`.
