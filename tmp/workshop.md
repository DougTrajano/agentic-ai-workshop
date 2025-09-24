## Objetivos

- Importar o [HR Synthetic Database](./database.md) do Hugging Face no DuckDB (database local).
- Desenvolver o **People Analytics Agent** como um único agente ou um **Multi-Agent System (MAS)**.
- Integrar o **People Analytics Agent** em uma interface conversacional.

## 🎭 Agentes que Vamos Construir

### 1. 📈 DataAnalyst Agent
**Especialidade**: Análise exploratória e estatística

**Capabilities**:
- Query databases usando SQL
- Análise estatística descritiva
- Identificação de padrões e outliers
- Validação de qualidade dos dados

### 2. 📊 Visualization Agent  
**Especialidade**: Criação de gráficos e dashboards

**Capabilities**:
- Gráficos interativos com Plotly
- Dashboards executivos
- Visualizações para diferentes audiências
- Export para diferentes formatos

### 3. 🔮 Prediction Agent
**Especialidade**: Modelagem preditiva

**Capabilities**:
- Previsão de turnover
- Identificação de funcionários em risco
- Análise de fatores de retenção
- Modelagem de cenários

### 4. 📋 Report Agent
**Especialidade**: Geração de relatórios

**Capabilities**:
- Relatórios executivos em múltiplos formatos
- Summaries para diferentes stakeholders
- Recomendações acionáveis
- Templates customizáveis

### 5. 🤝 Orchestrator Agent
**Especialidade**: Coordenação de outros agentes

**Capabilities**:
- Planejamento de análises complexas
- Coordenação entre agentes especializados
- Gestão de contexto compartilhado
- Síntese de resultados de múltiplos agentes

## 🏗️ Módulos do Workshop

### Módulo 1: Setup e Dados (30 min)

#### 1.1 Preparação do Database

```python
# data/prepare_hr_database.py
import duckdb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_hr_database():
    # Conecta ao DuckDB
    conn = duckdb.connect('data/hr_data.db')
    
    # Gera dados sintéticos de funcionários
    np.random.seed(42)
    n_employees = 1000
    
    employees_data = {
        'employee_id': range(1, n_employees + 1),
        'name': [f'Employee_{i}' for i in range(1, n_employees + 1)],
        'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance'], n_employees),
        'level': np.random.choice(['Junior', 'Mid', 'Senior', 'Principal'], n_employees),
        'hire_date': [datetime.now() - timedelta(days=np.random.randint(30, 1800)) for _ in range(n_employees)],
        'salary': np.random.normal(75000, 25000, n_employees),
        'satisfaction_score': np.random.uniform(1, 5, n_employees),
        'performance_rating': np.random.choice(['Below', 'Meets', 'Exceeds', 'Outstanding'], n_employees),
        'is_active': np.random.choice([True, False], n_employees, p=[0.85, 0.15])
    }
    
    # Cria tabela employees
    df_employees = pd.DataFrame(employees_data)
    conn.execute("CREATE TABLE employees AS SELECT * FROM df_employees")
    
    # Gera dados de turnover
    turnover_data = []
    for emp_id in df_employees[~df_employees['is_active']]['employee_id']:
        turnover_data.append({
            'employee_id': emp_id,
            'termination_date': datetime.now() - timedelta(days=np.random.randint(1, 365)),
            'termination_type': np.random.choice(['Voluntary', 'Involuntary']),
            'reason': np.random.choice(['Better opportunity', 'Compensation', 'Work-life balance', 'Management', 'Performance'])
        })
    
    df_turnover = pd.DataFrame(turnover_data)
    conn.execute("CREATE TABLE turnover AS SELECT * FROM df_turnover")
    
    print("✅ Database criado com sucesso!")
    conn.close()

if __name__ == "__main__":
    create_hr_database()
```

#### 1.2 Ferramentas Base

```python
# src/tools/database_tool.py
from typing import Any, Dict
import duckdb
import pandas as pd

class DatabaseTool:
    """Ferramenta para consultas SQL no database de RH"""
    
    name = "query_database"
    description = "Executa consultas SQL no database de RH"
    
    def __init__(self, db_path: str = "data/hr_data.db"):
        self.db_path = db_path
    
    def execute(self, params: Dict[str, Any]) -> str:
        """
        Executa query SQL no database
        
        Args:
            params: {"query": "SELECT * FROM employees LIMIT 5"}
        """
        query = params.get("query")
        if not query:
            return "Erro: Query SQL é obrigatória"
        
        try:
            conn = duckdb.connect(self.db_path)
            result = conn.execute(query).fetchdf()
            conn.close()
            
            # Retorna resultado formatado
            if len(result) > 10:
                return f"Query executada com sucesso. {len(result)} linhas retornadas.\n\nPrimeiras 10 linhas:\n{result.head(10).to_string()}"
            else:
                return f"Query executada com sucesso:\n{result.to_string()}"
                
        except Exception as e:
            return f"Erro na execução da query: {str(e)}"
```

### Módulo 2: Primeiro Agente - DataAnalyst (45 min)

#### 2.1 Implementação do DataAnalyst Agent

```python
# src/agents/data_analyst_agent.py
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any
import logfire

class AnalysisResult(BaseModel):
    query_used: str
    insights: List[str]
    recommendations: List[str]
    data_quality_notes: List[str]
    confidence_score: float

# Configuração do agente
data_analyst = Agent(
    'openai:gpt-4',
    result_type=AnalysisResult,
    system_prompt="""
    Você é um especialista em People Analytics com 10 anos de experiência.
    
    PERSONALIDADE:
    - Analítico e preciso
    - Foca em insights acionáveis
    - Sempre considera qualidade dos dados
    - Comunica de forma clara e objetiva
    
    PROCESSO DE ANÁLISE:
    1. Compreenda a solicitação
    2. Planeje a análise necessária
    3. Execute queries SQL apropriadas
    4. Analise os resultados
    5. Forneça insights e recomendações
    
    DIRETRIZES:
    - Sempre valide a qualidade dos dados
    - Explique limitações da análise
    - Forneça contexto de negócio
    - Sugira próximos passos
    """
)

# Registra ferramenta
@data_analyst.tool
def query_database(query: str) -> str:
    """Executa consultas SQL no database de RH"""
    from src.tools.database_tool import DatabaseTool
    db_tool = DatabaseTool()
    return db_tool.execute({"query": query})

# Exemplo de uso
if __name__ == "__main__":
    with logfire.span('data_analyst_execution'):
        result = data_analyst.run_sync(
            "Analise a distribuição de funcionários por departamento e identifique padrões interessantes"
        )
        
        print("=== ANÁLISE COMPLETA ===")
        print(f"Query: {result.data.query_used}")
        print(f"\nInsights: {result.data.insights}")
        print(f"\nRecomendações: {result.data.recommendations}")
        print(f"\nConfiança: {result.data.confidence_score}")
```

#### 2.2 Testando o DataAnalyst Agent

```python
# tests/test_data_analyst.py
import pytest
from src.agents.data_analyst_agent import data_analyst

def test_department_analysis():
    """Testa análise por departamento"""
    result = data_analyst.run_sync(
        "Analise a distribuição de funcionários por departamento"
    )
    
    assert result.data.confidence_score > 0.7
    assert len(result.data.insights) > 0
    assert result.data.query_used is not None

def test_turnover_analysis():
    """Testa análise de turnover"""
    result = data_analyst.run_sync(
        "Calcule a taxa de turnover por departamento e identifique tendências"
    )
    
    assert result.data.confidence_score > 0.7
    assert "turnover" in result.data.query_used.lower()
```

### Módulo 3: Agente de Visualização (45 min)

#### 3.1 Implementação do Visualization Agent

```python
# src/agents/visualization_agent.py
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any
import plotly.graph_objects as go
import plotly.express as px
import base64
import io

class VisualizationResult(BaseModel):
    chart_type: str
    title: str
    description: str
    insights: List[str]
    chart_data: str  # Base64 encoded chart
    recommendations: List[str]

visualization_agent = Agent(
    'openai:gpt-4',
    result_type=VisualizationResult,
    system_prompt="""
    Você é um especialista em visualização de dados para People Analytics.
    
    EXPERTISE:
    - Criação de gráficos eficazes para dados de RH
    - Storytelling com dados
    - Design de dashboards executivos
    - Visualizações para diferentes audiências
    
    PRINCÍPIOS DE DESIGN:
    - Clareza sobre complexidade
    - Cores adequadas para dados corporativos
    - Foco nos insights principais
    - Acessibilidade visual
    
    PROCESSO:
    1. Compreenda os dados e objetivo
    2. Escolha o tipo de gráfico mais apropriado
    3. Crie visualização clara e informativa
    4. Extraia insights dos padrões visuais
    5. Forneça recomendações baseadas na visualização
    """
)

@visualization_agent.tool
def create_chart(data_query: str, chart_type: str, title: str) -> str:
    """Cria gráfico a partir de dados do database"""
    from src.tools.database_tool import DatabaseTool
    import pandas as pd
    import plotly.graph_objects as go
    import plotly.express as px
    
    # Busca dados
    db_tool = DatabaseTool()
    result = db_tool.execute({"query": data_query})
    
    # Parse dos dados (simplificado para o exemplo)
    try:
        # Executa query para obter DataFrame
        conn = duckdb.connect("data/hr_data.db")
        df = conn.execute(data_query).fetchdf()
        conn.close()
        
        # Cria gráfico baseado no tipo
        if chart_type == "bar":
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], title=title)
        elif chart_type == "pie":
            fig = px.pie(df, values=df.columns[1], names=df.columns[0], title=title)
        elif chart_type == "line":
            fig = px.line(df, x=df.columns[0], y=df.columns[1], title=title)
        else:
            fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title=title)
        
        # Converte para base64
        img_bytes = fig.to_image(format="png")
        img_base64 = base64.b64encode(img_bytes).decode()
        
        return f"Gráfico criado com sucesso. Dados: {len(df)} registros"
        
    except Exception as e:
        return f"Erro na criação do gráfico: {str(e)}"
```

### Módulo 4: Orchestrator Agent (60 min)

#### 4.1 Agente Coordenador

```python
# src/agents/orchestrator_agent.py
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio

class AnalysisTask(BaseModel):
    task_type: str
    description: str
    assigned_agent: str
    priority: int

class AnalysisPlan(BaseModel):
    tasks: List[AnalysisTask]
    execution_order: List[str]
    estimated_time: int
    success_criteria: List[str]

class OrchestrationResult(BaseModel):
    plan: AnalysisPlan
    execution_summary: Dict[str, Any]
    final_insights: List[str]
    recommendations: List[str]
    confidence_score: float

orchestrator = Agent(
    'openai:gpt-4',
    result_type=OrchestrationResult,
    system_prompt="""
    Você é um Orchestrator Agent especializado em coordenar análises complexas de People Analytics.
    
    RESPONSABILIDADES:
    - Decompor solicitações complexas em tarefas específicas
    - Identificar qual agente é melhor para cada tarefa
    - Coordenar execução sequencial ou paralela
    - Sintetizar resultados de múltiplos agentes
    - Garantir qualidade e coerência dos resultados
    
    AGENTES DISPONÍVEIS:
    - DataAnalyst: Análise exploratória, SQL, estatísticas
    - Visualization: Gráficos, dashboards, storytelling visual  
    - Prediction: Modelos preditivos, forecasting
    - Report: Relatórios executivos, documentação
    
    PROCESSO:
    1. Analise a solicitação e quebre em componentes
    2. Crie plano de execução com agentes apropriados
    3. Execute tarefas na ordem correta
    4. Consolide resultados e insights
    5. Forneça síntese final com recomendações
    """
)

@orchestrator.tool
async def execute_agent_task(agent_type: str, task_description: str) -> str:
    """Executa tarefa em agente especializado"""
    # Simula execução de agente especializado
    if agent_type == "data_analyst":
        from src.agents.data_analyst_agent import data_analyst
        result = data_analyst.run_sync(task_description)
        return f"DataAnalyst: {result.data.insights}"
    
    elif agent_type == "visualization":
        from src.agents.visualization_agent import visualization_agent
        result = visualization_agent.run_sync(task_description)
        return f"Visualization: {result.data.insights}"
    
    # Adicionar outros agentes conforme implementados
    return f"Agente {agent_type} executou: {task_description}"
```

### Módulo 5: Observabilidade e Monitoramento (30 min)

#### 5.1 Setup de Observabilidade

```python
# src/observability/monitoring.py
import logfire
from datetime import datetime
import json
from typing import Dict, Any

# Configuração do Logfire
logfire.configure(
    send_to_logfire='if-token-present',
    console=True,
    service_name='hr-analytics-agents'
)

class AgentMonitor:
    def __init__(self):
        self.metrics = {}
    
    @logfire.instrument('agent_execution')
    def track_agent_execution(self, agent_name: str, query: str, result: Any):
        """Monitora execução de agentes"""
        with logfire.span('agent_execution', agent=agent_name, query=query) as span:
            start_time = datetime.now()
            
            # Métricas de execução
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Log estruturado
            logfire.info(
                'Agent execution completed',
                agent=agent_name,
                query=query,
                execution_time=execution_time,
                result_type=type(result).__name__
            )
            
            span.set_attribute('execution_time', execution_time)
            span.set_attribute('success', True)
    
    def log_error(self, agent_name: str, error: Exception, context: Dict[str, Any]):
        """Log de erros com contexto"""
        logfire.error(
            'Agent execution failed',
            agent=agent_name,
            error=str(error),
            context=context
        )

# Instância global do monitor
monitor = AgentMonitor()
```

#### 5.2 Dashboard de Métricas

```python
# src/observability/dashboard.py
import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

def create_monitoring_dashboard():
    """Cria dashboard de monitoramento dos agentes"""
    
    st.title("🤖 Agent Performance Dashboard")
    
    # Métricas em tempo real
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Requests", "1,234", "12%")
    
    with col2:
        st.metric("Avg Response Time", "2.3s", "-0.5s")
    
    with col3:
        st.metric("Success Rate", "97.8%", "0.2%")
    
    with col4:
        st.metric("Cost Today", "$45.67", "$12.34")
    
    # Gráficos de performance
    st.subheader("📊 Performance Over Time")
    
    # Simula dados de performance
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    performance_data = pd.DataFrame({
        'date': dates,
        'response_time': np.random.uniform(1.5, 3.5, len(dates)),
        'success_rate': np.random.uniform(0.95, 0.99, len(dates)),
        'requests': np.random.randint(50, 200, len(dates))
    })
    
    fig_response = px.line(performance_data, x='date', y='response_time', 
                          title='Response Time Trend')
    st.plotly_chart(fig_response)
    
    # Agent Usage
    st.subheader("🎭 Agent Usage")
    agent_usage = pd.DataFrame({
        'agent': ['DataAnalyst', 'Visualization', 'Orchestrator', 'Report'],
        'requests': [450, 320, 180, 284],
        'avg_time': [2.1, 3.4, 4.2, 5.1]
    })
    
    fig_usage = px.bar(agent_usage, x='agent', y='requests', 
                       title='Requests by Agent')
    st.plotly_chart(fig_usage)

if __name__ == "__main__":
    create_monitoring_dashboard()
```

## 🎯 Exercícios Práticos

### Exercício 1: Análise de Turnover
**Objetivo**: Use o DataAnalyst Agent para identificar padrões de turnover

**Tarefa**:
```python
result = data_analyst.run_sync("""
Analise a taxa de turnover da empresa nos últimos 12 meses.
Identifique:
1. Taxa geral de turnover
2. Departamentos com maior turnover
3. Correlação entre satisfação e turnover
4. Principais motivos de saída
""")
```

### Exercício 2: Dashboard Executivo
**Objetivo**: Crie visualizações para apresentação executiva

**Tarefa**:
```python
result = visualization_agent.run_sync("""
Crie um dashboard executivo com:
1. Distribuição de funcionários por departamento
2. Evolução do turnover por trimestre
3. Satisfaction score por nível hierárquico
4. Principais métricas de People Analytics
""")
```

### Exercício 3: Análise Complexa Orquestrada
**Objetivo**: Use o Orchestrator para coordenar análise complexa

**Tarefa**:
```python
result = orchestrator.run_sync("""
Realize uma análise completa de retenção de talentos incluindo:
1. Análise atual de turnover (DataAnalyst)
2. Visualizações de tendências (Visualization)
3. Previsão de funcionários em risco (Prediction)
4. Relatório executivo com recomendações (Report)
""")
```

## 🚀 Deploy e Produção

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### API REST

```python
# src/api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.orchestrator_agent import orchestrator
import logfire

app = FastAPI(title="HR Analytics API", version="1.0.0")

class AnalysisRequest(BaseModel):
    query: str
    user_id: str
    priority: str = "normal"

@app.post("/analyze")
async def analyze_hr_data(request: AnalysisRequest):
    """Endpoint principal para análises de RH"""
    try:
        with logfire.span('api_request', user_id=request.user_id):
            result = orchestrator.run_sync(request.query)
            return {
                "status": "success",
                "result": result.data,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logfire.error("API request failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

## 📈 Métricas de Sucesso

Ao final do workshop, você será capaz de:

1. ✅ **Construir agentes especializados** para diferentes tarefas de People Analytics
2. ✅ **Implementar observabilidade completa** com logging e métricas
3. ✅ **Coordenar agentes** para análises complexas
4. ✅ **Criar APIs REST** para sistemas agentivos
5. ✅ **Monitorar performance** em tempo real
6. ✅ **Deploy em produção** com Docker