# AS-BUILT — Harness de trabalho governado

Estado observado em 31 de julho de 2026. Este documento descreve o que o código atual efetivamente entrega, o que foi provado em testes, o que foi visto em operação e o que ainda é apenas intenção. Código é a autoridade sobre o estado atual; documentos entram como contexto, decisão declarada ou evidência histórica, nunca como substituto do que está implementado.

## 1. O objetivo do harness

Queremos que um trabalho feito por humanos e agentes não perca o vínculo com o motivo pelo qual existe. Ao final — ou depois de uma interrupção — deve ser possível responder: qual objetivo originou o trabalho; quais decisões foram tomadas; quem declarou ou exerceu autoridade; quais limites valiam; quem recebeu qual contexto; o que cada participante produziu; que evidência sustenta cada conclusão; e como continuar sem inventar a história que falta.

O harness, portanto, não é apenas um executor nem um arquivo de logs. Ele é a infraestrutura que preserva a cadeia **objetivo → decisão → autoridade → trabalho → contexto → resultado → evidência → continuidade**. Seu sucesso não é “ter muitos registros”; é permitir que outra pessoa reconstrua o trabalho, distinga fatos de declarações e retome a partir do ponto certo. [RECON-01, RECON-02, RECON-07; evidência: `implementations/as-built/pairs/pair-06-reconstruction.json`]

O código atual já contém partes importantes dessa cadeia, mas ainda não a fecha de ponta a ponta. Ele preserva bem fatos que entram no runtime; não garante que todo trabalho real entre nele. Ele verifica integridade local; não autentica, sozinho, a legitimidade humana. Ele consegue selar alguns inputs; não liga todo turno à sua saída exata. Essa diferença é o centro do estado atual. [HA-01, AUTH-02, RECON-03; evidência: pacotes 02, 03 e 06]

## 2. O que pode ser confiado hoje

### Integridade do que é aceito

Dentro do banco governado, um comando aceito é transacional: fatos, artefatos, eventos, estado e recibo convergem juntos; uma repetição idêntica recupera o mesmo resultado e uma repetição divergente falha. O journal detecta grupos parciais, corrupção, sobreposição e divergência estrutural, e as projeções podem ser reconstruídas. Essa é hoje a propriedade mais madura. Ela vale para fatos que efetivamente passaram pelo runtime, não para todo o trabalho do repositório. [MEM-01, MEM-02; evidência: `implementations/as-built/pairs/pair-04-memory-recovery.json`]

### Memória e transporte delimitados

Os caminhos especializados de Reference Scout e BUS conseguem preservar bytes, ordem, produtor e destinatário declarados, hashes e input efetivo. O binding de follow-up também consegue exigir template congelado e continuidade do agente anterior quando existe uma identidade não nula. Isso permite reconstruir certos handoffs antes do consumo. Não prova que o provider entregou, que o agente leu, que usou, nem que a fonte sustenta uma conclusão. [HA-04, HANDOFF-02, HANDOFF-03, HANDOFF-05; evidência: pacotes 02 e 05]

### Operação local conservadora

O piloto local tem verificação, backup online verificado e aposentadoria que preserva bytes. O HTTP de produção permanece fechado e servir o piloto exige preflight explícito. Porém, mutações via CLI confiável continuam alcançáveis fora desse gate, e não existe comando suportado de restauração. Podemos confiar na conservação local e nos limites do servidor; ainda não em recuperação operacional completa ou autorização uniforme de toda mutação. [P01-C02, MEM-03, HC-04; evidência: pacotes 01, 04 e 07]

### Visibilidade humana, com limites honestos

Uma pessoa pode ler propostas e dispatches, navegar objetivo, contexto, topologia e evidências, e usar seis superfícies de consulta do Control Center. A confirmação no Linear é somente um marcador local de reconhecimento: não autentica a pessoa, não congela autoridade e não faz o runtime aceitar o trabalho. O Control Center não oferece mutação autoritativa, o que hoje é uma proteção real. [P01-C01, HC-01, HC-02, HC-03; evidência: pacotes 01 e 07]

### O que ainda não merece confiança

Não podemos afirmar que todo agente foi lançado pelo caminho governado; que a autoridade humana foi autenticada; que limites de filesystem, ferramenta, modelo, rede ou delegação foram tecnicamente aplicados; que um binding terminal prova a autoria de um output; que duas mensagens do BUS representam duas perspectivas independentes; nem que a história inteira pode ser reconstruída por um terceiro. [HA-06, AUTH-04, HANDOFF-01, HANDOFF-04, RECON-07; evidência: pacotes 02, 03, 05 e 06]

Esta própria investigação é o contraexemplo mais claro: seu Dispatch e sua topologia existem em arquivos, mas o store inspecionado tinha zero links de Session, bindings de host, ingestions, Scouts ou captures para ele. Os sete resultados existem; o runtime não consegue provar que foram produzidos pelos assentos declarados. A aparência de governança excedeu a governança operacional. [AUTH-05, RECON-01, HC-06; evidência: pacotes 03, 06 e 07]

## 3. A fronteira atual e o que as próximas tarefas compram

O próximo salto não é uma tela agregada nem mais entidades. Primeiro precisamos impedir trabalho invisível e falsa confiança; depois ligar cada turno ao que produziu; em seguida medir se todas as contribuições esperadas chegaram; só então aprofundar autoridade, evidência e a visão reconstruída. Essa ordem evita construir uma narrativa elegante sobre dados incompletos. [RECON-G1 a RECON-G5; evidência: `implementations/as-built/pairs/pair-06-reconstruction.json`]

1. **Tornar o binding do host obrigatório e reconciliável.** Compra um denominador real: cada assento e turno esperado aparece exatamente uma vez, ou é mostrado como faltante, órfão ou extra. É o que impede trabalho fora da memória de parecer governado. [HA-01, HC-06, RECON-G1]
2. **Corrigir o falso quórum do BUS.** Compra independência verificável: um participante deixa de poder fabricar concordância coletiva com duas mensagens. [HANDOFF-04, G-05-01]
3. **Comprometer a saída terminal exata de cada turno.** Compra a resposta defensável para “quem produziu quais bytes e efeitos”, em vez de associar arquivos posteriores a um agente apenas porque ele terminou. [HANDOFF-01, RECON-03, RECON-G2]
4. **Dar uma disposição a toda contribuição esperada.** Compra completude mensurável: silêncio passa a ser `captured`, `partial` ou `missing`, não uma ambiguidade. [RECON-G3]
5. **Autenticar a decisão humana e separar declaração de verificação.** Compra uma cadeia confiável de “quem autorizou exatamente o quê”, sem transformar nomes e digests declarados em legitimidade. [AUTH-02, HC-02, HC-G1]
6. **Completar o handoff até entrega e aceite, preservando as diferenças entre entregue, acessado, usado e suporte de claim.** Compra continuidade entre agentes sem fingir que transporte equivale a raciocínio ou evidência. [HANDOFF-05, HANDOFF-06, G-05-03 a G-05-05]
7. **Criar recuperação de todo o checkpoint e um restore suportado.** Compra continuidade operacional entre YAML, SQLite, artefatos e fonte, em vez de cópias recuperáveis que ainda exigem improviso. [MEM-04, HC-04, G-04-02, HC-G4]
8. **Somente depois, oferecer uma visão fria agregada.** Compra compreensão por terceiros sem duplicar autoridade: a visão junta os donos existentes e mostra elos ausentes como desconhecidos. [RECON-07, RECON-G5]

## 4. A jornada real do trabalho

O caminho pretendido começa com um Dispatch confirmado, abre uma Session, liga a Session ao snapshot exato do Dispatch, cria um binding por assento/turno, sela o input, acompanha o encerramento e fecha o ciclo com recibos. Quando o hook confiável carrega e recebe um evento reconhecido, o prelaunch bloqueia falhas de política, preflight, capacidade e binding. [HA-02; evidência: `implementations/as-built/pairs/pair-02-host-adoption.json`]

Esse caminho é condicional. No Codex embutido `0.146.0-alpha.3.1`, um filho real foi criado sem evento `PreToolUse`, estado do hook, linhas de ciclo de vida, link, binding ou recibo. A adoção no binário substituto permanece desconhecida; Claude não tem evidência de launch real pelo modelo. Configuração no repositório disponibiliza o caminho, mas não obriga o host a adotá-lo. [HA-01, HA-06]

Mesmo quando invocados, fechamento e ingestão posterior não são globalmente fail-closed: falhas podem ocorrer depois que o trabalho já aconteceu, e a configuração dos eventos terminais difere entre Codex e Claude. Follow-up governado está implementado e testado, mas não há recibo operacional real de follow-up nos hosts. [HA-03, HA-04, HA-05]

## 5. Sistema real e fronteiras oficiais ou experimentais

Não existe uma única base soberana para todos os fatos. A fronteira aceita distribui autoridade por classe: YAML registra abertura e fechamento oficiais do Dispatch; o journal SQLite governa fatos aceitos do runtime; projeções são derivadas; arquivos e artefatos guardam conteúdo; o navegador mantém preferências e drafts auxiliares. Essa federação é intencional, mas ainda depende de reconciliação entre fronteiras. [P01-C03, MEM-04]

O processo HTTP principal é majoritariamente leitor. Ele expõe o Linear e seis rotas do Control Center. O `LocalControlCenterStore` é construído e testado isoladamente, mas não é chamado pelo serviço ou pela API; a interface visível usa `localStorage`. Portanto, o backend local store não deve ser contado como funcionalidade alcançável. [P01-C01, HC-03]

O runtime oficial possui outra composição executável. HTTP de runtime, provenance e health está fechado no reader; o piloto requer opt-in e preflight; comandos CLI mutáveis continuam alcançáveis. Dizer apenas “o runtime é gated” esconderia essa diferença. [P01-C02]

`implementations/agent-runtime` é um segundo runtime SQLite, empacotado como experimental, com journal, recibos, projeções e replay próprios. Ele é implementado e testado, mas não há evidência de operação atual, autoridade, adoção oficial ou convergência com `server/runtime`. Precisa de uma decisão de retenção como oráculo, mineração antes de aposentadoria ou convergência governada. [P01-C04]

O appender validado é declarado como writer pretendido do YAML oficial, mas seu executável não está em nenhum dos dois manifestos desta investigação. Assim, a autoridade pretendida está documentada; implementação congelada e exclusividade implantada não foram provadas. [P01-C03, AUTH-01]

## 6. Autoridade e identidade

O runtime impõe escopo lógico, expiração, digests de contexto, uso único, continuidade e retry semântico. Isso prova integridade do grant apresentado, não a legitimidade de quem o emitiu. Hoje o caller escolhe principal e escopo, e a política valida forma e digests declarados sem autenticar um signatário ou resolver uma raiz de confiança externa. [AUTH-01, AUTH-02]

Follow-up para agente diferente é rejeitado quando o turno anterior terminou com identidade não nula. Se `agent_id` for nulo, a igualdade de destinatário é pulada; além disso, a rejeição não gera recibo durável. [AUTH-03]

Os limites declarados por assento — filesystem, ferramenta, modelo, rede e proibição de spawn — são pedidos no payload, não cercas observadas no runtime do provider ou no sistema operacional. [AUTH-04]

Para esta investigação, a consulta read-only feita em `2026-07-31T18:54:56Z` encontrou zero bindings no store inspecionado. Isso é evidência pontual: não prova que nunca houve binding nem que nenhum outro store existiu. Ainda assim, combinada à ausência do prefixo obrigatório nos prompts, impede afirmar adoção governada deste dispatch. [AUTH-05, HC-06]

## 7. Memória, handoffs e recuperação

No interior do SQLite, atomicidade, idempotência, verificação estrutural e rebuild são sólidos e cobertos por testes focados. A verificação ainda não recomputa o significado completo: o resultado JSON genérico não tem digest independente, e o `state_hash` do aggregate head não é recalculado por reducer replay. [MEM-01, MEM-02, MEM-05]

Entre YAML e SQLite, o bridge escreve YAML primeiro. Se for interrompido, uma repetição externa idêntica converge, mas não há intenção pendente durável, scanner no startup ou reconciliação automática. A memória global ainda depende de um operador lembrar a operação exata. [MEM-04]

Na entrega, três contratos coexistem. `WorkflowInputManifest` sela arquivo e ordem, mas associa o output a um binding terminal sem provar que o produtor comprometeu aqueles bytes. Reference Scout entrega bundles exatos a um destinatário derivado. BUS preserva mensagens e ordem, porém seu quórum conta linhas de mensagem, não assentos distintos. [HANDOFF-01, HANDOFF-03, HANDOFF-04]

O contraexemplo executável publicou `position` e `vote` pela mesma `seat-a`; o fechamento retornou `received_seat_count: 2`, `quorum_status: quorum`, `message_count: 2`. Portanto, o quórum atual não sustenta a propriedade de julgamento independente. [HANDOFF-04; evidência: `implementations/as-built/pairs/pair-05-handoff-integrity.json`]

Não há ciclo genérico de resultado comprometido pelo produtor, publicação, entrega, aceite pelo destinatário e reconciliação do efeito no provider. Os caminhos especializados terminam em efeito pendente e inclusão no input. [HANDOFF-05, HANDOFF-06]

Backup e aposentadoria são conservadores, mas cobrem o banco local e não um checkpoint lógico de YAML, journal, artefatos, fonte e autoridades externas. Drafts do Control Center são auxiliares e locais; sua perda não corrompe o trabalho oficial, mas quebra a continuidade da deliberação humana. [MEM-03, MEM-06]

## 8. Proveniência e reconstrução

Quando um fato entra no runtime, o sistema pode preservar Session, snapshot imutável do Dispatch, ator declarado, binding, alguns inputs, retorno bruto de research, seis tipos de fatos e projeções reconstruíveis. Isso é um esqueleto ligado por integridade, não uma captura completa do raciocínio ou do trabalho. [RECON-01, RECON-02, RECON-06]

No instante observado, o store tinha 180 links de Dispatch, 22 bindings resolvidos, 415 ingestions, um Scout e uma captura com seis fatos, mas zero Agent Attempts e zero reference deliveries. Esses números demonstram população parcial, não cobertura. Para este Dispatch, todos esses contadores eram zero. [RECON-03 a RECON-06; evidência detalhada: `implementations/as-built/pairs/pair-06-reconstruction.json`]

`exact ingestion` prova bytes, tamanho e digest retidos. Não prova inclusão no prompt, entrega, leitura, uso ou suporte epistemológico. `claimed_consulted` é uma declaração do produtor. Um binding terminal prova estado e identidade registrada, mas não contém o output exato. [RECON-03, RECON-05]

As APIs permitem consultas separadas por especialistas. Não há uma superfície fria que una motivo declarado, autoridade, input, binding, output, contribuição e evidência, mostrando os elos ausentes. Criá-la agora esconderia falta de cobertura; ela deve vir depois dos quatro elos anteriores. [RECON-07]

## 9. Controle humano

O humano hoje consegue observar bastante e agir pouco — intencionalmente. O Linear cria um marcador para uma sheet legível; não registra identidade autenticada, bytes imutáveis da decisão, rationale, limites ou aceite do runtime. Reconfirmar atualiza o timestamp e não existe unconfirm. Nenhum consumidor automático do marcador foi encontrado. [HC-02]

O Control Center tem seis rotas de leitura e não possui apply, approve, retry, reconcile ou promotion. A UI salva draft no navegador e chama texto com oito caracteres de válido; o store local com revisão, conflito e validação existe apenas em processo e não é exposto. A segurança de não mutar é real; a preparação recuperável é mais fraca do que o backend sugere. [HC-03]

Evidência UX deve ser temporalmente separada. A rodada histórica preserva 204 screenshots e ausência de erros de console/rede naquele revisionamento. A seleção atual rodou 28 testes: 26 passaram e dois expuseram que a fonte atual é corretamente `partial/truncated`, enquanto as expectativas antigas ainda exigem `complete/success`. Nenhum browser novo foi aberto com sucesso nesta investigação; compreensão humana, confiança, screen reader e WCAG completo permanecem desconhecidos. [HC-01, HC-05]

O operador pode verificar, copiar e aposentar o banco preservando bytes, mas não há restore/reinstate suportado nem jornada integrada à UI. Isso é armazenamento recuperável, não recuperação operacional garantida. [HC-04]

## 10. Drift entre documentos e código

- A afirmação documental de que todo launch de agente é wrapped é falsa para o Codex embutido observado. O código do matcher pode estar correto sem que o host invoque o hook. [HA-01, HA-06]
- O plano que diz que journal/store ainda não foram construídos está atrasado: existe um slice local implementado e testado; o que permanece aberto é recuperação do harness inteiro. [MEM-01 a MEM-04]
- Especificações de research descrevem ReferenceChecks, relações claim-fonte e dispositions que não existem no runtime atual. [RECON-06]
- Documentos do Control Center descrevem proposta local versionada; a UI entregue usa `localStorage` e uma heurística de tamanho. [HC-03]
- A cópia do Linear sugere que o orchestrator observa o marcador, mas nenhum consumidor automático foi encontrado. [HC-02]
- Qualquer texto que chame o quórum do BUS de duas perspectivas independentes excede o código e é refutado pelo contraexemplo executado. [HANDOFF-04]
- “Runtime gated” precisa distinguir HTTP fechado, serving do piloto com preflight e CLI mutável alcançável. [P01-C02]

## 11. Próximo programa de trabalho

As duplas 05, 06 e 07 produziram três ordens complementares. Elas são preservadas abaixo, sem fingir que formam uma única lista consensual.

### Trilha de reconstrução — ordem exata da dupla 06

1. Fazer adoção do host ser obrigatória e reconciliar todos os assentos e turnos.
2. Persistir output/efeitos terminais exatos por turno.
3. Exigir disposição para cada contribuição esperada.
4. Depois, separar decisor declarado, evidência de autorização e status de verificação; implementar checks tipados de suporte/contradição de claims.
5. Somente então criar a visão fria agregada, não autoritativa. [RECON-G1 a RECON-G5]

### Trilha de handoff — ordem exata da dupla 05

1. Corrigir quórum por assento distinto e perfil de mensagem.
2. Fazer o produtor comprometer ids/hashes dos outputs no encerramento.
3. Criar handoff genérico de publicação, destinatário, entrega e aceite.
4. Implementar `claim/start/ack/fail` reconciliável para o efeito no provider.
5. Registrar separadamente entregue, acesso/uso declarado e suporte de claim.
6. Corrigir o wrapper de launch e fazer smoke fixado por host e versão. [G-05-01 a G-05-06]

### Trilha de controle humano — ordem exata da dupla 07

1. Ligar confirmação a principal autenticado, bytes imutáveis e aceite do runtime.
2. Falhar fechado sem binding e mostrar declarado versus bound versus terminal.
3. Conectar a UI a um draft/validator versionado ou remover o store não exposto e estreitar a promessa.
4. Criar e ensaiar restore/reinstate com recibo.
5. Resolver a fonte parcial, atualizar evidência de browser e concluir reviews independente, assistivo e humano. [HC-G1 a HC-G5]

Além dessas trilhas, há três decisões estruturais: incluir o appender e dependências no próximo manifesto; decidir o destino de `agent-runtime`; e criar um checkpoint de recuperação que ligue as autoridades sem fundi-las. Isso compra prova executável completa, uma única fronteira inteligível de runtime e continuidade além do SQLite. [P01-C03, P01-C04, G-04-02]

## 12. Método, temporalidade e índice de claims

Sete duplas independentes investigaram perguntas distintas, com worker, reviewer e até três rodadas de robot-talk. Todos os sete pacotes JSON passaram em `pair-output-schema.json`. Não restou dissenso aberto nos pacotes finais. Os digests exatos e o índice completo de 40 claims estão em `implementations/as-built/synthesis-report.json`.

A dupla 03 teve duas rodadas de robot-talk. O worker responsável pela finalização travou; o agente pai finalizou o pacote preservando a convergência registrada e declarando `finalizer: parent after worker finalizer stalled`. Isso é parte da proveniência do relatório, não uma atribuição silenciosa ao worker. [AUTH-01 a AUTH-05; evidência: `implementations/as-built/pairs/pair-03-authority.json`]

### Fronteira temporal de fonte

O freeze inicial (`implementations/as-built/source-manifest.json`) tinha SHA-256 `af35da963497918340ca7c74fa1a9e7a27d1a7027420e6edb517e55fd903cd11`. Durante a investigação, `implementations/server/runtime/service.py` mudou de `8b46ef...` para `4e1ad9...`: foram adicionadas 43 linhas que expõem bindings e recibos no snapshot do Dispatch. A autoria é desconhecida e não é atribuída a nenhum agente. O registro do Dispatch no YAML foi a outra mudança esperada. [AUTH-05, RECON-03; evidência: `implementations/as-built/source-drift-record.json`]

O código atual é a autoridade desta síntese. Por isso, as duplas afetadas e este documento usam também `implementations/as-built/source-manifest-current.json`, SHA-256 `82447f792685d81a6a2481c9b70b42dba2bf27a1326066a145407629ab9c330b`. O freeze original continua preservado para tornar o drift visível, não para substituir o estado atual.

### Como ler uma claim

Cada claim atômica separa seis dimensões: implementação, prova, operação, autoridade, adoção oficial e reconstruibilidade. “Implementado e testado” não significa “operando”; “operando” não significa “autorizado”; “digest-bound” não significa “verdadeiro”; “entregue” não significa “usado”; e “declarado no Dispatch” não significa “host-bound”. O índice em `implementations/as-built/synthesis-report.json` aponta cada `claim_id` para seu pacote, onde estão as linhas de código, testes, evidência contrária, confiança e lacunas.
