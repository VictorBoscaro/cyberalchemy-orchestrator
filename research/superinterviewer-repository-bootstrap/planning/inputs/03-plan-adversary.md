# Crítica adversarial do planejamento do Superinterviewer

## Posição

O maior risco é copiar a amplitude do Prompt-Mestre para um `research-plan` e chamar cobertura de planejamento. As 20 partes do documento fundador e as 15 refutações são um inventário de claims e tensões; não são uma ordem de execução. Um plano real reduz incertezas que bloqueiam decisões, explicita resultados que mudariam o caminho e encerra trabalhos quando a evidência já basta.

Há dois horizontes que não devem ser colapsados:

- **bootstrap do repositório:** autoridade, provenance, fronteiras e condições para pesquisar;
- **programa do produto:** validade do Superinterviewer, comportamento, avaliação, governança, integração e formalização.

O bootstrap deve habilitar o programa. Não deve exigir sua decomposição completa nem responder suas perguntas por meio do scaffold.

## Dez riscos e testes de realidade

### 1. Taxonomia disfarçada de plano

**Risco:** criar um workstream para intenção, lentes, probes, métricas, DAO, categorias etc., sem decisão consumidora.

**Teste:** cada unidade deve completar a frase “decidir entre A e B para permitir C”. Se só admite “investigar/mapear/explorar”, é tema, não trabalho planejado.

### 2. Pesquisa não discriminante

**Risco:** literatura e experimentos cujos resultados possíveis sempre preservam a direção preferida.

**Teste:** pré-declarar ao menos dois resultados plausíveis e ações diferentes para cada um. Se o próximo passo não muda, a pesquisa é cerimonial.

### 3. Programa infinito por ausência de corte

**Risco:** cada resíduo abre novas lentes e branches, enquanto tudo permanece “prioritário”.

**Teste:** o plano deve ter caminho crítico, timebox, temas adiados e triggers de abertura. Um resultado antecipado precisa poder cancelar ou reduzir trabalho posterior.

### 4. Ratificação de decisões já aceitas

**Risco:** usar pesquisa para “provar” as seis disposições aceitas no Robot-Talks, ou reabri-las continuamente.

**Teste:** cada disposição aparece como decisão com racional, força e condição de revisão. Pesquisa só a reabre quando o trigger ocorre; não coleta justificativas retroativas.

### 5. Promoção silenciosa de autoridade

**Risco:** uma síntese viva voltar a colapsar charter, contexto, plano, initial definitions, findings e decisões.

**Teste:** todo output declara autoridade, consumidor e relação permitida. Findings suportam propostas; somente um gate nomeado altera charter ou autoriza implementação.

### 6. Arquitetura decidida sem código

**Risco:** nomes, diretórios, templates, schemas, métricas e mocks congelarem produto mesmo sob uma postura “research-first”.

**Teste:** cada artefato estrutural lista as perguntas abertas que incorpora, sua validade local, reversibilidade e expiração. Nenhum schema experimental é promovido automaticamente.

### 7. Arqueologia de repositórios capturando o produto

**Risco:** DomainSpec, Arcanum, SWI, `mint` e formalização virarem a decomposição do Superinterviewer porque já existem.

**Teste:** pesquisa de reuso começa por uma necessidade local e pergunta qual contrato a satisfaz sem transferir autoridade. Trocar o provider por stub ou alternativa deve preservar a pergunta e o modelo local.

### 8. Autovalidação autobiográfica

**Risco:** a história dos últimos quatro meses gerar a taxonomia e depois “validá-la” ao ser recodificada pela mesma taxonomia.

**Teste:** usar o caso histórico apenas para gerar hipóteses e schema inicial; validar em casos retidos, tarefas ou usuários distintos, admitindo classe aberta/“nenhuma” e comparadores.

### 9. Pesquisa-first virando no-prototype

**Risco:** proteger perguntas abertas com documentação indefinida, sem testar se o produto supera um chatbot/busca com boa memória.

**Teste:** a primeira onda contém um protótipo reversível com baseline, outcome pré-definido e kill criterion; ele testa uma incerteza e não sua própria arquitetura.

### 10. Formalismo sem consequência

**Risco:** Yoneda, Selmer, pullbacks, categorias ou lenses formais ganharem branch por saliência, sem tipagem nem decisão afetada.

**Teste:** o ramo só abre quando um claim operacional está delimitado e o formalismo gera previsão, restrição, teste ou compressão melhor que grafos, constraints ou modelos probabilísticos simples. Se removê-lo não altera decisão do primeiro horizonte, deve ser adiado.

## Critérios de não-vacuidade por investigação

Uma investigação só entra no plano se tiver:

1. decisão consumidora e incerteza bloqueadora;
2. alternativas incompatíveis, incluindo baseline simples;
3. evidência ou experimento capaz de discriminá-las;
4. tabela “resultado → ação”, incluindo inconclusivo;
5. falsificador ou kill criterion;
6. fonte/amostra independente do material que gerou a hipótese;
7. força máxima de claim permitida pelo método;
8. dependências, timebox e stop condition;
9. output, autoridade e caminho explícito de promoção.

No nível do programa, deve existir caminho crítico. Toda branch precisa mapear para decisão ou refutação prioritária, e nenhum trabalho pode existir apenas para completar o sumário do futuro documento fundador.

## Decisões que implementação pode responder acidentalmente

O plano deve manter um registro de perguntas protegidas. Antes de scaffold, schema, adapter, métrica ou protótipo, registrar ao menos:

- se “principal interface” significa exclusiva, padrão ou apenas contínua;
- o que “companheiro” exige: memória, iniciativa, identidade relacional ou só estilo;
- se perguntar/informar/reenquadrar são completos e onde “sugerir” pertence;
- qual objeto é refinado e quem valida a intenção operacional;
- o que é próximo passo, quem julga sua qualidade e se avançar recomenda, handoffa ou executa;
- quando inferir, perguntar, preservar ambiguidade, retornar ou ramificar;
- se lentes e resíduos são objetos persistentes, instrumentos analíticos ou detalhes de runtime;
- qual objetivo seleciona intervenções e quais riscos/direitos são constraints, não termos de score;
- qual baseline e proxy definem melhoria sem confundir confiança, velocidade ou coerência com boa decisão;
- quais eventos, consentimentos, recusas e dados sensíveis são registrados;
- se DAO é requisito ou apenas candidato de governança;
- precedência dos artefatos, taxonomia de authority kinds, layout, toolchain, licença e visibilidade;
- mecanismo de dependência e status de SWI/Arcanum como providers substituíveis;
- se observabilidade exige somente execution links ou já impõe ledger, hooks e database.

Proteção mínima: toda implementação experimental referencia um ID de incerteza, declara escolhas incorporadas, prazo de revisão/descarte e proibição de promoção automática.

## Dependências e ciclos perigosos

| Ciclo | Falha | Quebra exigida |
|---|---|---|
| Charter → pesquisa → findings → charter | Findings reescrevem a identidade que definiu sua relevância. | Finding termina em proposta; gate nomeado altera charter. |
| “Refinar intenção” ↔ métrica | Uma definição arbitrária cria a métrica que depois a valida. | Comparar constructos rivais e validar medida antes de otimizar. |
| Taxonomia ↔ anotação | O codebook só enxerga as classes que pretende provar. | Classe aberta, concordância e taxonomias alternativas. |
| Lentes → probes → sinais → lentes | A lente escolhe os únicos sinais que podem confirmá-la. | Probes negativos/externos e frames concorrentes. |
| Protótipo ↔ avaliação | Affordances construídas passam a definir sucesso. | Baselines e outcomes antes de implementar; protótipos descartáveis. |
| Governança ↔ observabilidade | O stack registra apenas o que reconhece e passa a definir autoridade. | Requisitos de consentimento/contestabilidade antes da telemetria. |
| Scaffold ↔ consumidores | Artefatos existem porque o scaffold prevê e justificam o próprio scaffold. | Nenhum artifact sem consumidor e decisão atuais. |
| Provider ↔ contrato | Adapter baseado em um provider o torna inevitável. | Contrato local mínimo e teste de substituição. |
| Formalização ↔ ontologia | O formalizável ganha status de entidade real. | Claim operacional primeiro; formalismos competem com alternativas simples. |

Ordem mínima: autoridade e perguntas protegidas antes de scaffold vinculante; decisão antes de pesquisa de reuso; constructo antes de métrica; métrica/baseline antes de política; comportamento discriminável antes de produção; requisitos de governança antes de DAO/telemetria; claim operacional antes de formalização; contrato local antes de provider.

## Condições de parar, dividir ou reenquadrar

### Parar

Parar uma investigação quando a condição decisória pré-registrada for atingida; quando nova evidência independente não mudar a decisão marginalmente; quando o baseline vencer dentro do limiar; ou quando o método não puder sustentar a força de claim necessária. “Ainda há literatura” não basta.

Parar o planejamento e iniciar trabalho limitado quando as branches da primeira onda tiverem decisão, alternativas, dependências, evidência, stop condition e handoff; as perguntas protegidas estiverem registradas; e houver um experimento reversível. Esperar decomposição completa é falha de planejamento.

### Dividir

Dividir quando decisão consumidora, método, evidência ou autoridade diferirem. Separações necessárias: bootstrap versus produto; autoridade de produto versus governança da pesquisa; comportamento conversacional versus runtime; outcome versus telemetria; pesquisa empírica versus formalização; governança do usuário versus DAO; provenance de fontes versus observabilidade de runs. Não dividir apenas por disciplina ou repositório-fonte.

### Reenquadrar

Reenquadrar a tese se uma baseline simples igualar outcomes; usuários preferirem resposta direta sem perda relevante; as três intervenções não forem confiavelmente distinguíveis; “refinamento” não puder ser medido sem indução; reframing aumentar dependência sem melhorar decisões; `local first` ocultar riscos globais; lenses não superarem prompts/adapters simples; seleção de probes exigir complexidade sem benefício; ou a governança necessária tornar a interação impraticável.

Reenquadrar o bootstrap se sua fundação custar mais que a primeira onda de pesquisa, se um operador novo não entender a autoridade, se artifacts não tiverem consumers imediatos, ou se o primeiro estudo passar a depender de um runtime geral ainda contestado.

## Barra para a primeira onda

A primeira onda deveria responder apenas a três classes de decisão:

1. qual fundação mínima permite pesquisar com provenance sem taxonomia pesada nem provider obrigatório;
2. qual experimento separa refinamento de intenção de uma baseline simples fora do caso que originou a tese;
3. quais perguntas protegidas e gates impedem scaffold, métricas e protótipos de virarem produto por acidente.

Formalização ampla, DAO, runtime geral, política aprendida, composição completa de lentes e arquitetura de produção permanecem condicionais. Entram quando um resultado anterior demonstrar necessidade decisória, não porque aparecem no documento fundador desejado.
