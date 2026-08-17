# Verificação do agente principal

## Teste focado do precedente BTE

- Repositório: `C:/Users/victo/domainspec-core`
- Diretório: `projects/domainspec-v2/impl`
- Comando: `npx.cmd vitest run test-derivation-engine/src/bte/contract-publication.test.ts test-derivation-engine/src/bte/validation/validate-semantics.test.ts`
- Resultado observado em 2026-08-17: **5 passaram e 5 falharam** em 2 arquivos de teste.

Quatro falhas de `contract-publication.test.ts` têm a mesma causa: o publicador rejeitou
`artifact-handle.v1.schema.json` porque os bytes do checkout usam CRLF, enquanto o contrato exige LF
e newline final. A quinta falha ocorreu antes da asserção semântica porque o ambiente Windows negou
a criação de symlink com `EPERM`.

## Interpretação

Os testes e caminhos executáveis confirmam que existe código consumidor para publicação de
contratos e validação semântica. Porém, a suíte focada **não está verde no checkout/ambiente atual**.
Portanto, a evidência sustenta “precedente executável com testes existentes”, não “implementação
atualmente validada de ponta a ponta”. As falhas de LF e symlink também mostram um requisito de
portabilidade que deve ser resolvido antes de reutilizar o BTE como núcleo do Schema Service.

Nenhum arquivo do repositório irmão foi editado por esta pesquisa.
