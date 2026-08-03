# Pair 05 — Integridade de handoffs

## Resposta executiva

O runtime já consegue preservar um handoff até a fronteira de entrega: sela bytes exatos, registra produtor e destinatário declarados, mantém ordem, rejeita retry divergente e permite reconstruir o input aceito. Ele ainda não prova consumo nem uso pelo agente.

Há dois limites adicionais importantes. No handoff genérico por arquivo, um output é associado a um produtor terminal, mas o produtor não comprometeu aqueles bytes no seu próprio encerramento. No BUS, “quórum de duas cadeiras” hoje significa duas mensagens; uma única cadeira conseguiu publicar duas mensagens oficiais e produzir quórum. Portanto, esse quórum não é prova confiável de julgamento independente.

Também não existe ainda um ciclo genérico, de ponta a ponta, em que um agente compromete seu resultado, o sistema o entrega e o destinatário o aceita. Reference Scout e BUS são caminhos especializados.

## O que cada handoff preserva

| Caminho | Conteúdo | Produtor | Destinatário | Autoridade | Integridade e retry | Lacuna restante |
|---|---|---|---|---|---|---|
| WorkflowInputManifest | Hash, tamanho, bytes e ordem exatos | Binding terminal declarado; autoria dos bytes não provada | Dispatch, grupo, cadeira, turno e attempt exatos | Parcial; ator externo não autenticado aqui | Artefatos persistidos; retry idêntico converge e divergente falha | Compromisso atômico do output pelo produtor e aceite pelo destinatário |
| Reference Scout | Bundle, membros, ordinal e effective input exatos | Cadeia commit→delivery do Scout | Attempt, cadeira e instância derivados do binding | Capacidade interna precisamente cercada | Grupo atômico; drift/cross-scope falham; leitura é reconstruível | Entrega ao provider, acesso, uso e suporte a claims |
| BUS | Mensagens oficiais, hashes, autores e ordem do reveal | Cadeira ligada à publicação e recibos | Cadeira/attempt derivados do plano e binding | Parcial: identidade por mensagem funciona, quórum coletivo não | Materialização determinística; atomicidade; retry estável | Validar cadeiras distintas elegíveis e depois provar entrega ao provider |

## Falha material encontrada

O fechamento da coleta usa o número de mensagens como número de cadeiras. O reviewer publicou, pela mesma `seat-a`, uma mensagem `position` e outra `vote`, ambas oficiais. O resultado foi:

```text
{'received_seat_count': 2, 'quorum_status': 'quorum', 'message_count': 2}
```

O menor conserto com valor sistêmico é validar o conjunto de cadeiras elegíveis e a cardinalidade/tipo permitido por cadeira. Isso compra uma propriedade central do harness: uma pessoa ou agente não consegue fabricar a aparência de concordância independente.

## Próximos passos e o que compram

1. Corrigir quórum por cadeira distinta e perfil de mensagem. Compra autoridade coletiva confiável.
2. Fazer o produtor encerrar seu turno comprometendo atomicamente ids/hashes dos outputs. Compra autoria defensável dos bytes.
3. Criar um handoff genérico com publicação, destinatário, entrega e aceite. Compra garantias uniformes para qualquer dupla, não apenas BUS e Scout.
4. Implementar claim/start/ack/fail reconciliável do efeito no provider. Compra prova de entrega executada, sem fingir que entrega significa uso cognitivo.
5. Registrar separadamente “foi entregue”, “o agente declarou uso” e “suporta esta claim”. Compra reconstrução honesta das decisões e de suas evidências.
6. Corrigir o wrapper de launch e executar um smoke fixado por host/versão. Compra prova de adoção naquele ambiente; não prova adoção universal.

## Estado operacional desta investigação

Os 17 testes de binding, Reference Scout e BUS passaram no store isolado, e os 4 testes do evidence reader também passaram. O contraexemplo de quórum foi executado em fixture isolada e confirmou a falha.

As seats desta própria investigação não receberam o marcador obrigatório `ACI-WORKFLOW-BINDING-V1` na primeira linha e não têm recibos de host binding. Os achados são válidos como evidência de código e testes, mas não como prova de que o wrapper está oficialmente adotado. O missed-hook deve constar no fechamento do dispatch; nenhum stdout do bridge foi persistido no working folder.

## Convergência da dupla

Houve uma rodada de robot-talk. O worker aceitou o contraexemplo de quórum, a diferença entre associação de produtor e compromisso de output, a ausência do ciclo genérico e a falta de binding operacional deste dispatch. Não restou dissenso.

Fronteira de fonte: `implementations/as-built/source-manifest-current.json`, SHA-256 `82447f792685d81a6a2481c9b70b42dba2bf27a1326066a145407629ab9c330b`, commit `63777abd838995c8512bcea806546c3f2ab6add6`. O drift de `service.py` tem autoria desconhecida e não é atribuído a esta dupla.
