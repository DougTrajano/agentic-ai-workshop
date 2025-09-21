# 🔧 Pydantic AI

O **Pydantic AI** é um framework que facilita a criação de agentes Python tipados com observabilidade nativa.

## Características Principais

- **Type Safety**: Tipos Python nativos para inputs/outputs
- **Structured Outputs**: Respostas estruturadas usando Pydantic models
- **Built-in Observability**: Integração com Logfire
- **Dependency Injection**: Sistema robusto de dependências

## Exemplo com Pydantic AI

```python
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List

class AnalysisResult(BaseModel):
    insights: List[str]
    recommendations: List[str]
    confidence_score: float

# Define agente tipado
data_analyst = Agent(
    'openai:gpt-4',
    result_type=AnalysisResult,
    system_prompt="Você é um analista de dados especializado."
)

@data_analyst.tool
def load_data(file_path: str) -> str:
    """Carrega dados de um arquivo CSV"""
    # Implementação de carregamento
    return "dados carregados"

# Executa com tipos seguros
result = data_analyst.run_sync(
    "Analise os dados de vendas e forneça insights",
    message_history=[]
)

# Resultado é automaticamente tipado
insights: List[str] = result.data.insights
```

## Agentes com Dependências

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str

class UserQuery(BaseModel):
    user_id: int
    query: str

sql_agent = Agent(
    'openai:gpt-4',
    deps_type=DatabaseConfig,
    result_type=str
)

@sql_agent.tool
async def execute_query(ctx: RunContext[DatabaseConfig], query: str) -> str:
    """Executa query SQL de forma segura"""
    db_config = ctx.deps
    # Conecta ao banco usando db_config
    # Executa query com validação
    return "resultados da query"

# Uso com dependências
db_config = DatabaseConfig(host="localhost", port=5432, database="sales")
result = await sql_agent.run("Liste os top 10 clientes", deps=db_config)
```

## Quando Usar Pydantic AI

### ✅ Ideal para

- Aplicações que requerem type safety
- Sistemas que precisam de outputs estruturados
- Integração com observabilidade
- Desenvolvimento em equipes grandes

### ❌ Não ideal para

- Prototipagem muito rápida
- Casos onde flexibilidade é mais importante que type safety
- Aplicações que não usam Python

## Próximos Passos

- **[Outras Opções](other-frameworks.md)**: Explore mais alternativas
- **[Comparação](index.md)**: Compare diferentes frameworks
