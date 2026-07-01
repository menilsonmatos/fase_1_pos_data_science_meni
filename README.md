# Tech Challenge Fase 1 - Case NPS Preditivo

Projeto desenvolvido para o Tech Challenge da Fase 1 da Pós Tech FIAP, com foco em entendimento de negócio, análise exploratória e proposta de uso de Ciência de Dados para antecipar a satisfação de clientes em e-commerce.

## Objetivo do Projeto

Responder à pergunta de negócio:

> Quais fatores operacionais influenciam a satisfação do cliente e como a empresa pode agir de forma proativa para melhorar a experiência antes da aplicação da pesquisa de NPS?

O trabalho transforma dados de pedidos, logística e atendimento em insights acionáveis para áreas como logística, atendimento, produto, pricing e estratégia.

## Entendimento do Negócio

O problema resolvido é a dificuldade de antecipar clientes insatisfeitos antes da coleta formal de NPS. Atualmente, a empresa só mede satisfação após a jornada de compra, o que limita a capacidade de corrigir atrasos, reclamações e falhas de atendimento enquanto ainda há chance de recuperar a experiência.

O NPS é importante para e-commerce porque funciona como indicador de lealdade e reputação. Clientes promotores tendem a recomprar, indicar a marca e reduzir custo de aquisição. Clientes detratores, por outro lado, podem gerar churn, avaliações negativas e perda de market share.

Áreas beneficiadas:

- **Logística:** priorização de pedidos atrasados e gestão de tentativas de entrega.
- **Atendimento:** identificação de clientes com maior risco de insatisfação.
- **Produto:** entendimento de padrões de pedido associados a experiências ruins.
- **Pricing e comercial:** avaliação do efeito de frete, desconto e valor do pedido.
- **Estratégia:** acompanhamento de NPS previsto por região, operação e perfil de cliente.

Indicadores complementares recomendados:

- SLA logístico por região e transportadora.
- Tempo médio de resolução de chamados.
- Benchmarks de NPS por categoria de e-commerce.
- Taxa de recompra e churn.
- Reclamações em canais públicos e concorrência.

## Base de Dados

Fonte: arquivo `desafio_nps_fase_1.csv`, disponibilizado no material oficial do desafio.

A base contém **2.500 pedidos** e variáveis sobre:

- perfil do cliente;
- dados do pedido;
- logística e entrega;
- atendimento;
- recompra;
- score interno de satisfação;
- `nps_score`, nota de satisfação coletada após a experiência de compra.

## Definição da Target

A variável alvo principal é `nps_score`, pois representa diretamente a satisfação do cliente em escala de 0 a 10.

Para fins de análise gerencial, o NPS foi segmentado em:

- **Detrator:** `nps_score <= 6`
- **Neutro:** `6 < nps_score <= 8`
- **Promotor:** `nps_score > 8`

Para uma eventual modelagem futura, o alvo poderia ser binário:

- `1`: cliente detrator, com `nps_score <= 6`
- `0`: cliente não detrator

Essa formulação seria útil para priorizar ações preventivas. O principal cuidado seria evitar usar a previsão como verdade absoluta ou punir áreas sem contexto operacional. Um modelo deve apoiar decisões, não substituir análise humana.

## Metodologia

1. Leitura e validação da base.
2. Criação de classes de NPS.
3. Análise descritiva da distribuição de satisfação.
4. Análise por atraso de entrega, reclamações, atendimento e região.
5. Cálculo de correlações entre variáveis operacionais e NPS.
6. Reflexão conceitual sobre como um modelo preditivo poderia ser usado em fases futuras.
7. Geração de relatório e visualizações para storytelling gerencial.

## Principais Resultados

- NPS médio: **4,38**.
- Mediana do NPS: **4,40**.
- Distribuição:
  - **74,0% detratores**
  - **17,9% neutros**
  - **8,0% promotores**
- NPS calculado: **-66,0 p.p.**

Fatores mais críticos observados:

- atraso na entrega;
- quantidade de reclamações;
- quantidade de contatos com atendimento;
- tempo de resolução;
- score interno de satisfação;
- recompra em 30 dias.

## Insights de Negócio

### 1. Atraso logístico é um forte redutor de satisfação

Pedidos sem atraso têm NPS médio de **6,86** e taxa de detratores de **36,46%**. Com atraso de 4 dias ou mais, o NPS médio cai para **2,00** e a taxa de detratores sobe para **97,25%**.

### 2. Reclamações são o ponto de ruptura mais claro

Clientes sem reclamação têm NPS médio de **8,52**. Clientes com 6 ou mais reclamações têm NPS médio de **2,82** e taxa de detratores de **94,50%**.

### 3. Atendimento recorrente sinaliza fricção

Clientes sem contato com atendimento têm NPS médio de **5,54**. Clientes com 3 ou mais contatos têm NPS médio de **2,94** e taxa de detratores de **90,41%**.

### 4. Região tem menor poder explicativo que operação

As diferenças regionais existem, mas são menores que os efeitos de atraso, reclamações e atendimento. Isso sugere que a prioridade deve estar em processos operacionais, não apenas em segmentação geográfica.

## Reflexão sobre Modelo Preditivo

Neste projeto, a implementação do modelo preditivo não foi incluída, pois essa parte é opcional no desafio. Ainda assim, a análise indica como a empresa poderia evoluir para uma solução preditiva.

Uma estratégia possível seria construir um modelo de classificação para prever risco de cliente detrator:

- **Alvo:** cliente detrator, definido como `nps_score <= 6`.
- **Entradas:** atraso de entrega, reclamações, contatos com atendimento, tempo de resolução, frete, recompra, score interno de satisfação e região.
- **Uso prático:** priorizar clientes em risco em uma fila de atendimento preventivo.

Essa solução deveria ser validada antes de uso real, com separação entre treino e teste, avaliação de métricas e monitoramento contínuo para evitar decisões injustas ou enviesadas.

## Recomendações Práticas

- Criar alertas automáticos para pedidos com atraso, reclamação ou múltiplos contatos.
- Priorizar resolução antes da pesquisa NPS, especialmente em pedidos com 2 ou mais dias de atraso.
- Integrar logística e atendimento em uma fila única de recuperação de experiência.
- Usar o score interno de satisfação como sinal antecipado, mas sem substituir o NPS real.
- Monitorar taxa de detratores por faixa de atraso e volume de reclamações.
- Definir SLAs específicos para clientes de alto risco.

## Limitações

- A base é histórica e pode não capturar todos os fatores de experiência do cliente.
- Não há informações sobre categoria de produto, transportadora, canal de venda ou histórico completo de relacionamento.
- Uma solução preditiva futura precisaria ser validada antes de uso em produção.
- Correlação não implica causalidade; os achados devem orientar hipóteses e ações controladas.

## Estrutura do Projeto

```text
.
├── data/
│   ├── raw/
│   │   └── desafio_nps_fase_1.csv
│   └── processed/
│       └── desafio_nps_fase_1_enriched.csv
├── reports/
│   ├── figures/
│   ├── analysis_summary.json
│   ├── relatorio_analitico.md
├── scripts/
│   └── analyze_nps.py
├── README.md
└── requirements.txt
```

## Como Reproduzir

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute a análise:

```bash
python scripts/analyze_nps.py
```

3. Consulte os resultados gerados em:

```text
reports/relatorio_analitico.md
reports/analysis_summary.json
reports/figures/
```

## Entregáveis

- Código reproduzível de tratamento e EDA.
- Relatório analítico em Markdown.
- Visualizações em SVG.
- Material de storytelling gerencial.
- Roteiro de vídeo executivo de até 5 minutos.
