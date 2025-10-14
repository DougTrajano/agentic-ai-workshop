# 🧵 Strands Agents

Framework open-source desenvolvido pela AWS para construir sistemas multi-agente prontos para produção.

## O que é Strands Agents?

Strands Agents é um SDK Python que permite construir sistemas de IA agentica de nível empresarial com poucas linhas de código. Desenvolvido pela AWS, o framework oferece uma combinação única de simplicidade e recursos de nível empresarial.

### Características Principais

- **Orquestração guiada por modelo**: Usa raciocínio do LLM para planejar, orquestrar tarefas e refletir sobre objetivos
- **Agnóstico de modelo e provedor**: Funciona com qualquer provedor de LLM (Amazon Bedrock, OpenAI, Anthropic, modelos locais)
- **Primitivas multi-agente simples**: Suporte nativo para handoffs, swarms e workflows em grafo com A2A (Agent-to-Agent)
- **Integrações AWS de primeira classe**: Ferramentas nativas para serviços AWS e fácil deploy em EKS, Lambda, EC2
- **Suporte a MCP**: Integração nativa com Model Context Protocol

## Instalação

```bash
pip install strands-agents
```

## Exemplo Básico

```python
from strands_agents import Agent
from strands_agents.models import OpenAIModel

# Define o modelo
model = OpenAIModel(model_name="gpt-4")

# Cria um agente
agent = Agent(
    name="Assistente",
    model=model,
    instructions="Você é um assistente útil especializado em análise de dados."
)

# Executa o agente
response = agent.run("Analise as tendências de vendas do último trimestre")
print(response.content)
```

## Multi-Agent com Handoffs

```python
from strands_agents import Agent, Handoff
from strands_agents.models import BedrockModel

# Modelo do Amazon Bedrock
model = BedrockModel(model_id="anthropic.claude-3-sonnet-20240229-v1:0")

# Agente de pesquisa
researcher = Agent(
    name="Pesquisador",
    model=model,
    instructions="Você coleta informações relevantes sobre o tópico."
)

# Agente de análise
analyst = Agent(
    name="Analista",
    model=model,
    instructions="Você analisa dados e fornece insights.",
    handoffs=[
        Handoff(
            target=researcher,
            condition="quando precisar de mais informações"
        )
    ]
)

# Executa com handoff automático
response = analyst.run("Analise o mercado de IA em 2024")
```

## Swarm Pattern

```python
from strands_agents import Agent, Swarm
from strands_agents.tools import PythonTool

# Define ferramentas especializadas
@PythonTool
def calculate_metrics(data: dict) -> dict:
    """Calcula métricas de negócio."""
    return {"roi": 0.25, "cac": 150}

@PythonTool
def generate_report(metrics: dict) -> str:
    """Gera relatório formatado."""
    return f"ROI: {metrics['roi']}%, CAC: ${metrics['cac']}"

# Cria agentes especializados
calculator = Agent(
    name="Calculador",
    tools=[calculate_metrics],
    instructions="Calcula métricas financeiras."
)

reporter = Agent(
    name="Relator",
    tools=[generate_report],
    instructions="Gera relatórios formatados."
)

# Coordena com Swarm
swarm = Swarm(agents=[calculator, reporter])
result = swarm.run("Calcule e relate as métricas de Q4")
```

## Graph Workflow

```python
from strands_agents import Agent, Graph
from strands_agents.models import AnthropicModel

model = AnthropicModel(model_name="claude-3-opus-20240229")

# Define agentes para workflow
collector = Agent(name="Coletor", model=model)
processor = Agent(name="Processador", model=model)
reviewer = Agent(name="Revisor", model=model)

# Define grafo de workflow
graph = Graph()
graph.add_edge(collector, processor)
graph.add_edge(processor, reviewer)
graph.add_edge(reviewer, processor, condition="needs_revision")

# Executa workflow
result = graph.run(
    start_agent=collector,
    input_data="Processar relatório de vendas"
)
```

## Integração com AWS

### Deploy no Lambda

```python
# handler.py
from strands_agents import Agent
from strands_agents.models import BedrockModel

agent = Agent(
    name="LambdaAgent",
    model=BedrockModel(model_id="anthropic.claude-3-haiku-20240307-v1:0")
)

def lambda_handler(event, context):
    response = agent.run(event['query'])
    return {
        'statusCode': 200,
        'body': response.content
    }
```

### Ferramentas AWS Nativas

```python
from strands_agents import Agent
from strands_agents.tools.aws import S3Tool, DynamoDBTool

# Agente com ferramentas AWS
agent = Agent(
    name="AWSAgent",
    tools=[
        S3Tool(bucket_name="my-data-bucket"),
        DynamoDBTool(table_name="analytics")
    ],
    instructions="Você gerencia dados AWS."
)

response = agent.run("Liste os arquivos no bucket e salve metadados no DynamoDB")
```

## Observabilidade e Segurança

### Traces Nativos

```python
from strands_agents import Agent
from strands_agents.telemetry import enable_tracing

# Habilita tracing
enable_tracing(
    service_name="my-agent-system",
    export_to="cloudwatch"
)

agent = Agent(name="TracedAgent")
response = agent.run("Processar dados")  # Automaticamente traced
```

### Guardrails

```python
from strands_agents import Agent, Guardrail
from strands_agents.guardrails import BedrockGuardrail

# Integração com Bedrock Guardrails
agent = Agent(
    name="SecureAgent",
    guardrails=[
        BedrockGuardrail(
            guardrail_id="abc123",
            filters=["pii", "toxicity"]
        )
    ]
)
```

## Quando usar Strands Agents

### ✅ Ideal para

- **Aplicações empresariais AWS**: Integração nativa com serviços AWS
- **Sistemas multi-agente complexos**: Suporte robusto para swarms e graphs
- **Segurança e compliance**: Guardrails nativos e integração com Bedrock
- **Deploy em produção**: Projetado para escalabilidade empresarial
- **Flexibilidade de modelos**: Suporte para múltiplos provedores de LLM

### ⚠️ Considere alternativas se

- **Fora do ecossistema AWS**: Outros frameworks podem ser mais adequados
- **Prototipagem simples**: Pode ser mais complexo que necessário
- **Restrições de dependências**: Framework relativamente novo

## Recursos Adicionais

- [Documentação Oficial](https://strandsagents.com/latest/)
- [Repositório GitHub](https://github.com/strands-agents/sdk-python)
- [Guia de Início Rápido](https://strandsagents.com/latest/documentation/docs/user-guide/quickstart/)
- [Exemplos Multi-Agent](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/)
- [Deploy na AWS](https://strandsagents.com/latest/documentation/docs/user-guide/deploy/)

## Comparação com Outros Frameworks

| Aspecto | Strands Agents | LangGraph | Pydantic AI |
|---------|---------------|-----------|-------------|
| **Foco** | Enterprise AWS | Graph workflows | Type safety |
| **Multi-agent** | ⭐⭐⭐ Excelente | ⭐⭐⭐ Excelente | ⭐⭐ Bom |
| **Integrações AWS** | ⭐⭐⭐ Nativo | ⭐⭐ Suporte | ⭐⭐ Suporte |
| **Curva de aprendizado** | Média | Alta | Baixa |
| **Produção** | ⭐⭐⭐ Enterprise-ready | ⭐⭐⭐ Robusto | ⭐⭐ Crescendo |
