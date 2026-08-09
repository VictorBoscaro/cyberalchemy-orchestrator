# Collected explorer returns

Dispatch: `2026-08-09-resonantos-discord-api-intelligence-research`

These are the three upstream explorer returns collected for synthesis. They are preserved as returned; disagreements are resolved only in `findings.md`.

## Explorer 0 — technical capability inventory

Conclusion: Discord exposes useful primitives but almost no ready-made intelligence metrics. Current guild structure, members, messages, threads/forums, scheduled events and presence snapshots are accessible subject to permissions/intents; net growth, activity, responsiveness, onboarding, voice duration and retention must be derived, often prospectively.

Current snapshot:
- Guild: name/description/features/settings; with_counts=true gives approximate_member_count and approximate_presence_count; approximate and not historical. https://docs.discord.com/developers/resources/guild
- Channels: categories/text/announcement/voice/stage/forum/media, permissions/overwrites; Get Guild Channels excludes threads. https://docs.discord.com/developers/resources/guild and https://docs.discord.com/developers/resources/channel
- Roles: current roles and Get Guild Role Member Counts; evolution needs snapshots/events. Guild resource.
- Members: List Guild Members up to 1,000/page with user, roles, joined_at, pending; requires privileged GUILD_MEMBERS; excludes former members. Guild resource.
- Presence: approximate count via Guild; current Gateway presences require privileged GUILD_PRESENCES; offline/invisible indistinguishable and presence != participation. https://docs.discord.com/developers/events/gateway and /gateway-events
- Voice: current voice states and VOICE_STATE_UPDATE; no historical session-duration endpoint, so duration is prospective. Gateway events.
- Threads: active guild threads; archived public and accessible private threads; private access restricted; member_count approximate/capped at 50. https://docs.discord.com/developers/topics/threads and Channel resource.
- Forums: forum channels, posts as threads, tags and counters; message_count excludes starter/deleted messages; total_message_sent does not decrement on delete; no thematic aggregate. Channel resource.
- Scheduled events: current name/description/time/status/type/recurrence/user_count and subscriber list up to 100/page; user_count means interested/subscribed, not attendance; retention of completed events unclear. https://docs.discord.com/developers/resources/guild-scheduled-event
- Invites: active invites with uses/max_uses/created_at under admin permissions; join events do not identify invite, so attribution by uses delta is ambiguous inference. https://docs.discord.com/developers/resources/invite

Recoverable history:
- Get Channel Messages returns accessible persisted messages newest-first, paginated before/after/around, up to 100/call. Requires VIEW_CHANNEL and READ_MESSAGE_HISTORY. Content/embeds/attachments/components/polls require MESSAGE_CONTENT. Deleted/inaccessible messages unavailable; docs state no maximum historical window for existing persisted messages. https://docs.discord.com/developers/resources/message
- Search Guild Messages filters content/channels/authors/etc., 25/call, offset max 9,975; requires READ_MESSAGE_HISTORY and MESSAGE_CONTENT; 202 indexing state, incomplete old-message pages, imprecise totals, no reactions. Useful for queries, not exhaustive counting. Message resource.
- Archived public threads are enumerable with READ_MESSAGE_HISTORY; private threads depend on access. Threads docs.
- joined_at supports only partial join curves among current members; no prior leavers or full historical population.
- Audit log: up to 45 days, 100/page, VIEW_AUDIT_LOG; administrative changes only, not community telemetry. https://docs.discord.com/developers/resources/audit-log

Prospective collection via Gateway should persist member add/remove/update, message create/update/delete, reactions/polls, channel/thread lifecycle and membership, voice state, optional presence, scheduled-event lifecycle/subscriptions, and invite lifecycle. Gateway resume is not guaranteed historical retention. Gateway and Gateway Events docs.

Authorization/intents:
- Bot installed with OAuth2 bot scope; applications.commands only for commands; installer needs MANAGE_GUILD; permissions include guild and channel overwrites. https://docs.discord.com/developers/platform/oauth2-and-permissions
- Likely standard intents by chosen metrics: GUILDS, GUILD_MESSAGES, GUILD_MESSAGE_REACTIONS, GUILD_VOICE_STATES; VIEW_CHANNEL and READ_MESSAGE_HISTORY in included channels.
- Privileged GUILD_MEMBERS for complete member inventory and join/leave; MESSAGE_CONTENT for content/attachments/embeds/polls; GUILD_PRESENCES only if justified. Verified apps from 100 guilds require approval per current Gateway docs. https://docs.discord.com/developers/events/gateway

Pagination/cost:
- Members 1,000/page; messages 100; search 25 and max offset 9,975; event subscribers 100; audit log 100; thread members 100; archived threads cursor+has_more.
- REST route buckets and current global 50 requests/s per bot; interpret X-RateLimit, Retry-After, 429 dynamically; 10,000 invalid 401/403/429 in 10 min may trigger IP restriction. https://docs.discord.com/developers/topics/rate-limits
- Gateway send limit 120 events/connection/60s. Gateway docs.

Honest measurement classifications:
- Current members direct (exact enumeration or approximate REST count); current role distribution direct.
- Historical gross growth only partial from joined_at survivors; joins/leaves/net growth prospective.
- Active members, messages/channel, recurring contributors, first-response time, active channels/forums, emerging topics, retention/cohorts all derived.
- Event user_count direct interest, not attendance. Attendance only inferable for Discord voice/stage, not external events.
- Online now approximate/presence-based, not engagement. Invite origin not direct.

Policy constraints:
- Declared purpose and minimization; API Data only as necessary; no profiling users/relationships; message content cannot train ML/AI without express permission. https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy
- Privacy policy, correction/deletion mechanism, delete when unnecessary/requested, security/encryption at rest, limited third-party sharing. https://support-dev.discord.com/hc/en-us/articles/8562894815383-Discord-Developer-Terms-of-Service
- Model inference is not clearly resolved merely because training is prohibited; service-provider sharing and App Review remain open.

Unknowns: exact authorized guild/channel/private-thread scope; account population; completed-event retention; practical completeness/cost of large backfill; MESSAGE_CONTENT approval; retention granularity; external-model compatibility; Gateway gaps and permission changes.

Technical v0 recommendation from explorer_0: guild count; prospective joins/leaves; active authors by message metadata without content; volume/channel; threads/posts created; scheduled-event interest. Defer presence, individual voice, semantic content and invite attribution.

## Explorer 1 — measurement perspective

### Resultado principal

A API do Discord oferece bons blocos para um hub agregado, mas quase nenhuma “métrica de comunidade” pronta. Crescimento líquido, participação, ativação, responsividade e desempenho de iniciativas são designs derivados. A fronteira mais segura para o v0 é usar metadados agregados; análise semântica e perfis individuais devem ficar fora.

### Legenda de evidências oficiais

- **GUILD:** [Guild Resource](https://docs.discord.com/developers/resources/guild)
- **GATEWAY:** [Gateway Events](https://docs.discord.com/developers/events/gateway-events)
- **INTENTS:** [Gateway / Intents](https://docs.discord.com/developers/events/gateway)
- **MESSAGE:** [Message Resource](https://docs.discord.com/developers/resources/message)
- **CHANNEL:** [Channel Resource](https://docs.discord.com/developers/resources/channel)
- **THREADS:** [Threads](https://docs.discord.com/developers/topics/threads)
- **USER:** [User Resource](https://docs.discord.com/developers/resources/user)
- **EVENTS:** [Guild Scheduled Event](https://docs.discord.com/developers/resources/guild-scheduled-event)
- **LIMITS:** [Rate Limits](https://docs.discord.com/developers/topics/rate-limits)
- **POLICY:** [Discord Developer Policy](https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy)
- **INVITES:** [Invite Resource](https://docs.discord.com/developers/resources/invite)

### Matriz métrica–evidência

| Família e métrica candidata | Primitivas mínimas | Natureza e reconstrução | Denominador e armadilhas | Decisão apoiada |
|---|---|---|---|---|
| **Crescimento — membros humanos atuais** | `Get Guild(with_counts)` ou paginação de `List Guild Members`; `user.bot`, `user.system` | O total aproximado é direto; o total humano exato é derivado pela enumeração. Apenas estado atual. `List Guild Members` exige `GUILD_MEMBERS`. [GUILD], [USER] | Excluir bots e contas `system`; decidir se convidados e membros `pending` contam. O valor aproximado do guild não permite essa filtragem. | **Inferência de produto:** dimensionar alcance atual e contextualizar outras métricas. |
| **Crescimento — entradas, saídas e saldo por período** | `GUILD_MEMBER_ADD`, `GUILD_MEMBER_REMOVE`, IDs e estado local da associação | **Design inferido:** `entradas − saídas`. Necessita armazenamento prospectivo e `GUILD_MEMBERS`. O evento Add pode chegar para quem já é membro; é necessário deduplicar pelo estado. Remove agrega saída voluntária, kick e ban. [GATEWAY], [INTENTS] | Excluir bots/system; saldo deve usar a mesma fronteira populacional do início ao fim. Reentrada precisa de regra explícita: novo episódio ou mesma pessoa. | **Inferência de produto:** avaliar aquisição e perdas, sem alegar a causa das saídas. |
| **Crescimento — coortes ainda presentes** | `joined_at` dos membros atuais; idealmente log de Add/Remove | O `joined_at` é direto no membro. Uma fotografia atual consegue mostrar sobreviventes por data de entrada, mas não reconstrói quem já saiu. Retenção histórica confiável é prospectiva. [GUILD] | Denominador correto é toda a coorte que entrou, não apenas quem ainda está presente. Bots, convidados e reentradas distorcem. | **Inferência de produto:** identificar coortes com baixa permanência. |
| **Participação — mensagens e autores humanos únicos por canal/período** | Message `id`, `channel_id`, `author`, `timestamp`, `type`; `Get Channel Messages` ou `MESSAGE_CREATE/DELETE` | **Design inferido.** Há backfill paginado, máximo 100 por chamada, nos canais visíveis com `READ_MESSAGE_HISTORY`; não há garantia oficial de “histórico completo”. Mensagens apagadas não são recuperadas. Prospectivo é mais confiável. Conteúdo textual não é necessário para contar mensagens/autores. [MESSAGE], [GATEWAY] | Excluir `author.bot`, `system`, webhooks e tipos automáticos. Não chamar autores únicos de “membros ativos” sem definir atividade. “Taxa ativa” dividida por todos os membros subestima canais com acesso restrito. | **Inferência de produto:** decidir onde concentrar facilitação e quais canais estão subutilizados. |
| **Participação — reações e reatores humanos únicos** | Reações presentes nos messages ou `MESSAGE_REACTION_ADD/REMOVE`; `user_id`, `message_id`, autor da mensagem | Contagens atuais são parcialmente recuperáveis; sequência histórica de adições e remoções exige Gateway prospectivo. **Design inferido:** reatores únicos ou mensagens que receberam reação. [MESSAGE], [GATEWAY] | Uma pessoa pode reagir várias vezes; bots e auto-reações devem ser excluídos. Reação não equivale a concordância nem leitura. Mensagens apagadas desaparecem do backfill. | **Inferência de produto:** sinal leve de participação, complementar às mensagens. |
| **Participação — sessões humanas em voz** | `VOICE_STATE_UPDATE`, `user_id`, `channel_id`, `session_id`, timestamps armazenados | **Design inferido** por pareamento de entrada/saída/movimentação. Requer `GUILD_VOICE_STATES` e coleta prospectiva; não encontrei endpoint oficial de histórico de sessões. [GATEWAY], [INTENTS] | Reconexões, movimentos entre canais, convidados e bot users; ausência de evento pode deixar sessão aberta. Tempo conectado não significa atenção ou fala. | **Inferência de produto:** avaliar uso dos espaços síncronos. Não recomendado para v0. |
| **Integração — screening/onboarding concluído** | Member `pending`, `flags` como `STARTED_ONBOARDING`, `COMPLETED_ONBOARDING`, `STARTED_HOME_ACTIONS`, `COMPLETED_HOME_ACTIONS` | O estado atual é direto e retroativamente fotografável para membros presentes. Duração e funil histórico exigem armazenar `GUILD_MEMBER_UPDATE`; os flags não trazem timestamps. [GUILD], [GATEWAY] | Somente servidores com esses recursos habilitados; excluir bots, convidados e membros não elegíveis. `pending=false` significa screening concluído, não integração social. | **Inferência de produto:** localizar fricção configuracional no onboarding. |
| **Integração — tempo até primeira contribuição** | `joined_at` + primeira message humana; opcionalmente reação ou voz | **Design inferido:** `primeira_contribuição_at − joined_at`. Pode ser estimado para membros atuais usando backfill de mensagens, mas perde contribuições apagadas/inacessíveis e antigos membros. Prospectivo é confiável. [GUILD], [MESSAGE] | Definir “contribuição”: mensagem pública é o critério mais auditável. Denominador deve incluir somente coortes que já tiveram a janela inteira para ativar. Bots, reentradas e mensagens automáticas saem. | **Inferência de produto:** testar se mudanças no acolhimento reduzem tempo de ativação. |
| **Integração — ativação em N dias** | Log de joins + mensagens humanas no período | **Design inferido:** proporção da coorte com ≥1 mensagem pública em N dias. Backfill é incompleto para ex-membros; idealmente prospectivo. | Denominador: humanos que entraram e completaram N dias de observação. Não misturar coortes ainda imaturas. Uma mensagem é sinal mínimo, não prova de integração. | **Inferência de produto:** comparar experiências de onboarding entre períodos. |
| **Responsividade — tempo até primeira resposta explícita** | Message `timestamp`, `author`; `message_reference` de reply ou mensagens dentro de thread | **Design inferido.** Backfill possível onde o histórico permanece acessível. A referência identifica replies explícitos, mas respostas sem reply precisam de heurística. [MESSAGE] | Definir quais mensagens iniciam uma “solicitação”. Excluir resposta do próprio autor, bots e mensagens automáticas. Mediana e p90 são melhores que média. Se poucas pessoas usam reply, a cobertura colapsa. | **Inferência de produto:** ajustar plantão, documentação e atenção a canais de ajuda. |
| **Responsividade — posts/threads sem resposta humana no SLA** | Threads públicos/arquivados; `owner_id`; mensagens e autores | **Design inferido:** thread elegível com zero mensagens de outro humano após X horas. Threads públicos arquivados são enumeráveis; `total_message_sent` inclui mensagens apagadas e não distingue autores, portanto não basta sozinho. [CHANNEL], [THREADS], [MESSAGE] | Denominador: threads envelhecidas além do SLA. Excluir anúncios, threads fechadas intencionalmente, bots e auto-respostas. | **Inferência de produto:** gerar fila de conversas que precisam de atenção. |
| **Tópicos — distribuição de tags de fórum** | `available_tags` do fórum e `applied_tags` dos threads, inclusive arquivos públicos | Campo categórico direto; a distribuição é derivada. É possível fotografar o estado atual e enumerar threads públicas arquivadas; histórico de troca de tags exige armazenamento. [CHANNEL], [THREADS] | Tags precisam ser usadas consistentemente. Threads sem tag formam categoria própria. Mudanças na taxonomia quebram comparabilidade longitudinal. | **Inferência de produto:** orientar documentação, programação e estrutura dos fóruns sem ler conteúdo. |
| **Tópicos — assuntos semânticos emergentes** | `message.content`, canal, timestamp; `MESSAGE_CONTENT` | **Design inferido de alta sensibilidade.** Conteúdo pode ser recuperado onde acessível, mas o intent é privilegiado e mensagens têm campos de conteúdo vazios sem ele. Busca de guild também é restringida por esse intent. [MESSAGE], [INTENTS] | Classificação é incerta, multilíngue e sujeita a contexto. A política proíbe perfilar usuários e usar conteúdo para treinar modelos sem permissão do Discord. Trabalhar apenas com agregados não elimina todos os riscos. [POLICY] | **Inferência de produto:** identificar necessidades editoriais. Excluir do v0 até haver propósito, transparência, retenção e revisão de privacidade definidos. |
| **Iniciativas — eventos criados, status e inscritos** | Scheduled Event `name`, datas, `status`, `creator_id`, `user_count`; lista de inscritos; eventos Add/Remove | Campos e inscritos são diretos; séries históricas exigem armazenar creates/updates/deletes e snapshots. `user_count` significa inscritos, não presentes. [EVENTS], [GATEWAY] | Excluir bots dos inscritos quando enumerados. Eventos cancelados e recorrentes precisam de regra. Não chamar inscrição de comparecimento. | **Inferência de produto:** decidir cadência e formato dos eventos pela demanda declarada. |
| **Iniciativas — participação em canal/thread associado** | Mapeamento explícito iniciativa→canal/thread/evento; messages, autores, reações | **Design inferido.** Backfill parcial por mensagens; prospectivo preserva limites e deletes. Discord não fornece uma entidade genérica “iniciativa”. | O mapeamento manual é parte da métrica. Evitar atribuir toda atividade do canal à iniciativa quando o espaço é compartilhado. Denominador pode ser inscritos ou membros elegíveis, mas responde perguntas diferentes. | **Inferência de produto:** continuar, modificar ou encerrar uma iniciativa concreta. |

### Limites transversais

- Permissão de canal define o universo observável. `Get Channel Messages` requer `VIEW_CHANNEL` e `READ_MESSAGE_HISTORY`; um hub não pode tratar canais invisíveis ao bot como atividade zero. [MESSAGE]
- `GUILD_MEMBERS`, `GUILD_PRESENCES` e `MESSAGE_CONTENT` são intents privilegiados; devem ser habilitados e, quando aplicável, aprovados. [INTENTS]
- Backfill integral por canal pode ser caro: mensagens são paginadas em até 100, membros em até 1.000, e limites não devem ser codificados porque variam. [MESSAGE], [GUILD], [LIMITS]
- Contagem de presença aproximada não é participação e não deve entrar no v0.
- Uso de invites por código não oferece atribuição oficial direta `member join → invite`. Comparar incrementos de `uses` é heurística concorrente, especialmente com múltiplos joins; não recomendo expô-la como aquisição atribuída. [INVITES]
- A política limita coleta ao necessário para a funcionalidade declarada, permite melhoria com dados agregados/desidentificados, proíbe profiling de usuários e proíbe mineração/scraping. Portanto o produto deve ser agregado por padrão e não produzir ranking individual. [POLICY]

### Shortlist conservadora para o v0

1. **Membros humanos atuais**, com regra pública para bots, system, convidados e pending.
2. **Entradas, saídas e saldo semanal**, válido prospectivamente a partir da instalação.
3. **Mensagens humanas e autores humanos únicos por canal/semana**, sem armazenar conteúdo.
4. **Ativação em 7 ou 14 dias por primeira mensagem pública**, iniciando apenas para novas coortes.
5. **Posts de fórum sem resposta humana após SLA**, restrito a canais declarados de ajuda/discussão.
6. **Distribuição de tags de fórum**, se o ResonantOS já usar fóruns com taxonomia minimamente consistente.
7. **Eventos programados e inscritos**, rotulados explicitamente como interesse, não presença.

Eu excluiria do v0 presença, voz, tópicos semânticos, sentimento, rankings de pessoas, “engajamento score”, retenção reconstruída apenas dos sobreviventes e atribuição de joins por invite. Esses itens ou têm semântica enganosa, coleta sensível ou evidência histórica insuficiente.

## Explorer 2 — operational, privacy, and proportionality boundary

## Resultado: fronteira operacional e de privacidade

A recomendação é um v0 baseado em metadados agregados, somente em espaços comunitários explicitamente selecionados, sem `GUILD_MEMBERS`, `GUILD_PRESENCES` ou `MESSAGE_CONTENT`. Isso permite sinais úteis com uma superfície de risco bem menor.

### Requisitos explícitos do Discord

- A aplicação só pode acessar e usar dados necessários à funcionalidade declarada; é proibido usar API Data para perfilar usuários, suas identidades ou relações. Conteúdo de mensagens não pode ser usado para treinar modelos de ML/IA sem permissão expressa do Discord. [Developer Policy](https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy)
- A aplicação precisa ter política de privacidade pública, atualizada e facilmente acessível, descrevendo coleta, acesso, armazenamento, retenção, transmissão, compartilhamento e exclusão. Usuários precisam de um meio acessível para solicitar correção e exclusão. [Developer Terms, §5](https://support-dev.discord.com/hc/en-us/articles/8562894815383-Discord-Developer-Terms-of-Service)
- Dados devem ser apagados quando deixarem de ser necessários, quando o usuário ou Discord solicitar, ou quando a aplicação encerrar. Criptografia em repouso e salvaguardas administrativas e técnicas são exigidas. [Developer Terms, §5](https://support-dev.discord.com/hc/en-us/articles/8562894815383-Discord-Developer-Terms-of-Service)
- Compartilhamento com um fornecedor externo só cabe nas exceções dos Terms. Um `Service Provider` precisa assumir por escrito que usa os dados somente sob direção do operador e para operar a aplicação; o operador continua responsável por ele. Isso afeta diretamente o envio de mensagens a provedores externos de IA. [Developer Terms, §§5 e 12](https://support-dev.discord.com/hc/en-us/articles/8562894815383-Discord-Developer-Terms-of-Service)
- A aplicação deve respeitar bloqueio, opt-out e remoção de servidores ou canais. [Developer Policy](https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy)
- `GUILD_MEMBERS`, `GUILD_PRESENCES` e `MESSAGE_CONTENT` são privileged intents. A partir de junho de 2026, aplicações acessíveis a 10.000 usuários ou mais precisam de revisão e, se aprovadas, reaplicação anual; existe janela de 90 dias após notificação. [Gateway docs](https://docs.discord.com/developers/events/gateway), [mudança de 2026](https://support-dev.discord.com/hc/en-us/articles/40281523410967-Changes-to-Privileged-Intent-Access-for-Discord-Apps)
- `VIEW_CHANNEL` controla visibilidade; `READ_MESSAGE_HISTORY` habilita recuperação histórica. `MESSAGE_CONTENT` controla `content`, embeds, anexos, componentes e polls, mas não elimina o acesso a autor, canal, timestamp, tipo e outros metadados. [Permissions](https://docs.discord.com/developers/topics/permissions), [Message Resource](https://docs.discord.com/developers/resources/message)
- Bots já têm acesso básico a perfis, cargos, metadados de mensagens, reações e estados de voz nos servidores em que estão presentes. O perfil do bot expõe uma aba “Data Access”, mas ela não substitui a política e a comunicação do próprio produto. [Visibility of Bot Data Access](https://support.discord.com/hc/en-us/articles/7933951485975-Visibility-of-Bot-Data-Access)

### Recomendações prudenciais do produto

Estas são recomendações, não obrigações textuais adicionais do Discord:

- Permitir que administradores selecionem canais incluídos, com padrão deny-by-default.
- Excluir DMs, canais privados, moderação, suporte sensível e private threads do escopo inicial.
- Não conceder `ADMINISTRATOR`, `MANAGE_THREADS`, `VIEW_AUDIT_LOG` ou `MANAGE_MESSAGES`.
- Mostrar no próprio Discord um aviso curto com finalidade, canais incluídos, métricas, retenção e link para exclusão/privacidade.
- Não guardar texto, anexos, nomes, avatares ou IDs estáveis no v0.
- Agregar por canal e janela temporal; aplicar limiar mínimo antes de exibir contagens pequenas.
- Manter identificadores somente em memória ou por uma janela curta quando indispensáveis para deduplicação; apagar após formar o agregado.
- Restringir o dashboard a membros autorizados do servidor e nunca torná-lo público por padrão.
- Registrar mudanças de escopo, permissões e métricas como mudanças de finalidade.

A própria orientação oficial para privileged intents recomenda menor privilégio, acesso restrito, visibilidade conforme cargos e permissões, exclusão rápida de dados individuais — 30 dias como máximo recomendado, não como prazo obrigatório universal — e atenção à expectativa de privacidade dos membros. [Privileged Intents Best Practices](https://support-dev.discord.com/hc/es/articles/6177533521047-Privileged-Intents-Best-Practices)

### Fronteira dos espaços

Permissão técnica não equivale a expectativa social de uso analítico. Private threads só são visíveis a convidados ou a quem possui `MANAGE_THREADS`; conceder esse poder ao hub faria o bot atravessar uma fronteira que membros podem perceber como privada. [Threads](https://docs.discord.com/developers/topics/threads)

Recomendação:

- **Incluído:** canais públicos comunitários selecionados; public threads e fóruns que herdam essa seleção.
- **Fora por padrão:** canais com overwrites restritivos, private threads, canais de staff/moderação, denúncias, tickets, suporte pessoal, voz e DMs.
- **Nunca inferir inclusão:** um novo canal não entra automaticamente só porque o bot consegue vê-lo.
- **Revogação:** perda de acesso deve cessar ingestão imediatamente; como o Gateway não fornece um evento único de “perda de todos os threads”, a implementação precisa recalcular permissões após mudanças de canal, cargo e membro. [Threads — Losing Access](https://docs.discord.com/developers/topics/threads)

### Contas incluídas

Mensagens podem vir de humanos, bots, webhooks e mensagens de sistema. O objeto `User` possui flags `bot` e `system`; mensagens de webhook são identificáveis por `webhook_id`, e `type` distingue mensagens normais e de sistema. [User Resource](https://docs.discord.com/developers/resources/user), [Message Resource](https://docs.discord.com/developers/resources/message)

Assim, toda métrica de participação humana deve:

- excluir `author.bot == true`;
- excluir `author.system == true`;
- excluir `webhook_id != null`;
- limitar tipos de mensagem ao conjunto previamente declarado;
- apresentar separadamente automações, quando houver utilidade.

`member_count` representa contas no servidor, não “humanos ativos”. Um cartão de membros deve dizer “contas no servidor” até haver enumeração e filtragem comprovadas.

## Classificação das análises

| Análise | Decisão | Condições |
|---|---|---|
| Total de contas no servidor e tendência por snapshots | **v0** | Rotular corretamente; não afirmar “humanos”. |
| Volume de mensagens por canal/dia | **v0** | `GUILDS` + `GUILD_MESSAGES`, canais allowlisted, sem conteúdo, excluir bots/webhooks/sistema. |
| Número agregado de contribuidores únicos | **v0 condicional** | IDs efêmeros apenas para deduplicação, descarte após agregação e limiar mínimo de exibição. |
| Reações agregadas por canal/período | **v0** | `GUILD_MESSAGE_REACTIONS`, sem ranking individual. |
| Public threads/fóruns criados e atividade agregada | **v0** | Somente pais allowlisted e threads públicas visíveis. |
| Eventos agendados: criados, concluídos, cancelados e interesse agregado | **v0** | `GUILDS`; descartar IDs de inscritos. Os eventos têm status e `user_count`. [Scheduled Events](https://docs.discord.com/developers/resources/guild-scheduled-event) |
| Distribuição de cargos funcionais | **v0 condicional** | Allowlist de cargos não sensíveis, agregado, sem nomes individuais. |
| Entradas, saídas, coortes e conclusão de onboarding | **adiar** | Exigem `GUILD_MEMBERS`; justificar necessidade e definir exclusão/retenção antes. |
| Presença, horários online e timezone inferido | **excluir do v0** | `GUILD_PRESENCES` é privilegiado e padrões temporais individuais são invasivos; presença simples também tem baixo valor adicional. |
| Participação em voz e duração de sessões | **adiar** | Embora estados de voz sejam acessíveis, hábitos temporais podem revelar rotinas; requer comunicação e governança próprias. |
| Tempo até primeira resposta | **adiar** | Precisa definir o que é pergunta/resposta e evitar grafo relacional individual; versão futura deve ser agregada e limitada a canais de ajuda. |
| Assuntos emergentes e categorização temática | **adiar** | Exige conteúdo, finalidade específica, `MESSAGE_CONTENT`, governança comunitária e avaliação do fornecedor de IA. |
| Sentimento, personalidade, risco, influência ou qualidade por membro | **excluir** | Constitui ou se aproxima de perfil individual proibido. |
| Ranking de contribuidores ou “membros mais valiosos” | **excluir** | Incentiva perfil individual e interpreta quantidade como qualidade. |
| Grafo de relações, afinidade ou centralidade social | **excluir** | A política proíbe perfilar relações entre usuários. |
| Arquivo ou espelho pesquisável de conteúdo | **excluir do hub** | Não é necessário às métricas básicas; aumenta retenção, IP e exposição. |
| Retrocoleta integral do histórico | **adiar** | O endpoint existe, mas crawling analítico amplo tensiona a proibição de mineração/scraping e requer esclarecimento prévio. |

### Content analysis e IA

A política proíbe **treinamento** com conteúdo de mensagens sem permissão expressa; ela não declara de modo igualmente explícito que toda inferência por modelo preexistente seja proibida. Isso não torna o envio de conteúdo a uma API de IA automaticamente aceitável: finalidade necessária, `MESSAGE_CONTENT`, compartilhamento com Service Provider, política de privacidade, direitos sobre conteúdo e exclusão continuam aplicáveis. [Developer Policy](https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy), [Developer Terms](https://support-dev.discord.com/hc/en-us/articles/8562894815383-Discord-Developer-Terms-of-Service)

Portanto, análise temática só deveria avançar após:

1. aprovação comunitária e escopo de canais explícito;
2. confirmação de acesso a `MESSAGE_CONTENT`;
3. contrato de Service Provider sem uso próprio ou treinamento;
4. processamento transitório, preferencialmente sem armazenamento de texto;
5. saída agregada sem trechos atribuíveis;
6. resposta escrita do Discord Support se o uso continuar ambíguo.

### Questões legais ainda abertas

Não são respondidas pelas fontes técnicas e exigem avaliação jurídica apropriada, especialmente pela presença potencial de usuários brasileiros e menores:

- papel do ResonantOS e operadores como controlador/processador;
- base legal e necessidade de consentimento sob LGPD ou outras leis aplicáveis;
- tratamento de dados de menores;
- transferências internacionais e fornecedores de nuvem/IA;
- se agregados derivados continuam sujeitos a pedidos individuais de exclusão;
- direitos autorais e outras permissões sobre conteúdo processado;
- retenção necessária para segurança, auditoria ou defesa de direitos.

Isto não é aconselhamento jurídico.

## Condições de colapso

- **“O v0 dispensa privileged intents”** colapsa se a decisão de produto exigir lista humana exata, joins/leaves, presença ou conteúdo.
- **“Metadados agregados bastam para atividade básica”** colapsa se os campos `author`, `timestamp`, `channel_id`, `type` ou eventos de reação deixarem de ser disponíveis sem privileged intents.
- **“Contagem de contribuidores pode ficar no v0”** colapsa se não houver mecanismo confiável para exclusão de automações, descarte de identificadores e atendimento de solicitações durante a janela de processamento.
- **“Processar todos os canais visíveis é aceitável”** já colapsa diante da diferença entre permissão técnica e expectativa de privacidade; precisa existir allowlist explícita.
- **“Análise temática pode ser considerada depois”** colapsa se Discord negar `MESSAGE_CONTENT`, se o fornecedor usar dados para treinamento/finalidade própria, ou se a comunidade não aceitar o escopo.
- **“Inferência com modelo pronto não é treinamento”** não resolve a conformidade. Essa distinção deixa de sustentar a proposta se Discord interpretar o processamento como uso incompatível, mineração ou perfil; obter confirmação escrita é o teste.
- **“Agregado anônimo elimina obrigações de exclusão”** não está comprovado pelas fontes; deve permanecer uma questão aberta até orientação jurídica e/ou do Discord.
- **“Total de membros representa tamanho da comunidade humana”** colapsa porque a contagem inclui contas automatizadas enquanto não houver enumeração e filtragem.
- **“Retrocoleta histórica é permitida porque existe endpoint”** colapsa se Discord considerar o uso mineração proibida; existência técnica do endpoint não comprova autorização para analytics amplo.

Conclusão em uma linha: o v0 defensável mede estrutura e atividade agregada futura em canais públicos allowlisted, sem conteúdo nem intents privilegiados; presença, histórico amplo, perfis individuais e semântica ficam fora até haver finalidade, governança e autorização mais fortes.
