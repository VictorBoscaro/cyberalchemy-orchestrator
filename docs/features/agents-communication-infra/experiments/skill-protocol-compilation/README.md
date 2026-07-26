# Skill Protocol Compilation — Experiment Notes

Este diretório prepara uma futura investigação sobre protocolos de execução reutilizáveis para
skills. Ele contém agora um **protótipo não ratificado** que transforma
`domainspec-spec-feature` em um grafo de protocolo e aplica dois níveis de assurance. Ainda não
existe compilador, registry, banco de dados, fixture de execução ou integração runtime.

Comece por:

- [`experiment-initial-definitions.md`](experiment-initial-definitions.md) — significado do problema
  para o produto, propósito, restrições já confirmadas, evidência disponível e lacunas conhecidas.
- [`prototypes/domainspec-spec-feature/README.md`](prototypes/domainspec-spec-feature/README.md) —
  explicação do primeiro protocolo-grafo e dos níveis `medium` e `high`.
- [`prototypes/domainspec-spec-feature/protocol-design.md`](prototypes/domainspec-spec-feature/protocol-design.md) —
  design compacto dos grafos Medium e High e de sua transformação futura em dispatch.

## Estado

O trabalho continua experimental. O grafo e os dois perfis são material de aprendizagem: eles
permitem testar a separação entre semântica estável, assurance selecionada e `DispatchSpec` concreto,
mas não constituem schema, preset ou contrato runtime ratificado.

Quando as definições estiverem suficientemente claras, um documento posterior poderá propor uma
pergunta experimental, critérios pré-registrados e o menor probe capaz de responder a essa
pergunta. Esses artefatos não devem ser antecipados aqui.

## Relações

- [Design notebook temporário](../../../../temps/agent-dispatch-protocol/README.md)
- [Discovery candidata de protocolos](../../discovery/agents-communication-protocols/README.md)
- [Infraestrutura de comunicação entre agentes](../../README.md)
