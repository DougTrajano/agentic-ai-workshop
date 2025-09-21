# Pydantic Logfire

O **Pydantic Logfire** oferece observabilidade nativa para aplicações Pydantic AI usando OpenTelemetry[^28].

## 🔧 Integração Automática

```python
import logfire
from pydantic_ai import Agent

# Configuração do Logfire
logfire.configure(
    send_to_logfire='if-token-present',
    console=True,
    service_name='agentic-ai-workshop'
)

# Instrumentação automática
logfire.instrument_pydantic()
logfire.instrument_openai()
logfire.instrument_anthropic()

# Agente com observabilidade automática
agent = Agent(
    'openai:gpt-4',
    system_prompt="Você é um assistente de análise de dados."
)

# Execução automaticamente instrumentada
with logfire.span('agent_execution'):
    result = agent.run_sync("Analise as vendas do último trimestre")
    
    # Logs estruturados automáticos
    logfire.info(
        'Agent execution completed',
        result=result.data,
        cost=result.cost(),
        tokens=result.usage()
    )
```

## 📊 Observabilidade Avançada

```python
import logfire
from pydantic import BaseModel
from typing import List

class AgentMetrics(BaseModel):
    execution_time: float
    token_usage: int
    tool_calls: List[str]
    success: bool
    cost: float

class ObservableAgent:
    def __init__(self):
        self.agent = Agent('openai:gpt-4')
    
    @logfire.instrument('agent_run')
    def run_with_metrics(self, query: str) -> AgentMetrics:
        start_time = time.time()
        
        with logfire.span('agent_execution', query=query) as span:
            try:
                result = self.agent.run_sync(query)
                
                metrics = AgentMetrics(
                    execution_time=time.time() - start_time,
                    token_usage=result.usage().total_tokens,
                    tool_calls=[call.tool_name for call in result.tool_calls],
                    success=True,
                    cost=result.cost()
                )
                
                span.set_attribute('metrics', metrics.model_dump())
                logfire.info('Agent execution succeeded', metrics=metrics)
                
                return metrics
                
            except Exception as e:
                span.set_attribute('error', str(e))
                logfire.error('Agent execution failed', error=str(e))
                raise
```

## 🎯 Instrumentação Customizada

### Decorador @logfire.instrument

```python
import logfire
from typing import Dict, Any
import time

class CustomInstrumentedAgent:
    def __init__(self, model: str):
        self.model = model
        self.agent = Agent(model)
    
    @logfire.instrument('planning_phase')
    def plan_actions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fase de planejamento instrumentada"""
        
        with logfire.span('context_analysis') as span:
            span.set_attribute('context_size', len(str(context)))
            
            # Análise do contexto
            complexity = self._analyze_complexity(context)
            span.set_attribute('complexity_score', complexity)
            
            logfire.info('Context analyzed', complexity=complexity)
        
        with logfire.span('plan_generation') as span:
            plan = self._generate_plan(context, complexity)
            
            span.set_attribute('plan_steps', len(plan['steps']))
            span.set_attribute('estimated_time', plan['estimated_time'])
            
            logfire.info('Plan generated', 
                        steps=len(plan['steps']),
                        estimated_time=plan['estimated_time'])
        
        return plan
    
    @logfire.instrument('tool_execution')
    def execute_tool(self, tool_name: str, params: Dict) -> Any:
        """Execução de ferramenta instrumentada"""
        
        start_time = time.time()
        
        with logfire.span(f'tool_{tool_name}') as span:
            span.set_attribute('tool_name', tool_name)
            span.set_attribute('params', params)
            
            try:
                result = self._call_tool(tool_name, params)
                execution_time = time.time() - start_time
                
                span.set_attribute('execution_time', execution_time)
                span.set_attribute('success', True)
                
                logfire.info('Tool executed successfully',
                           tool=tool_name,
                           execution_time=execution_time,
                           result_type=type(result).__name__)
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                span.set_attribute('execution_time', execution_time)
                span.set_attribute('success', False)
                span.set_attribute('error', str(e))
                
                logfire.error('Tool execution failed',
                            tool=tool_name,
                            execution_time=execution_time,
                            error=str(e))
                
                raise
```

## 📈 Logging Estruturado

### Contexto e Metadados

```python
import logfire
from contextlib import contextmanager

class StructuredAgentLogger:
    def __init__(self, agent_id: str, version: str):
        self.agent_id = agent_id
        self.version = version
    
    @contextmanager
    def conversation_context(self, user_id: str, session_id: str):
        """Context manager para conversas"""
        
        with logfire.span('conversation',
                         user_id=user_id,
                         session_id=session_id,
                         agent_id=self.agent_id,
                         agent_version=self.version) as span:
            
            logfire.info('Conversation started',
                        user_id=user_id,
                        session_id=session_id)
            
            try:
                yield span
                
                logfire.info('Conversation completed successfully',
                           user_id=user_id,
                           session_id=session_id)
                
            except Exception as e:
                logfire.error('Conversation failed',
                            user_id=user_id,
                            session_id=session_id,
                            error=str(e))
                raise
    
    def log_user_interaction(self, interaction_type: str, data: Dict):
        """Log de interações do usuário"""
        
        logfire.info('User interaction',
                    interaction_type=interaction_type,
                    agent_id=self.agent_id,
                    **data)
    
    def log_business_event(self, event_type: str, metrics: Dict):
        """Log de eventos de negócio"""
        
        logfire.info('Business event',
                    event_type=event_type,
                    agent_id=self.agent_id,
                    metrics=metrics)

# Uso do logger estruturado
logger = StructuredAgentLogger("sales_agent", "2.1.0")

def handle_sales_query(query: str, user_id: str, session_id: str):
    with logger.conversation_context(user_id, session_id) as conv_span:
        
        # Log da interação inicial
        logger.log_user_interaction('query_received', {
            'query_length': len(query),
            'query_type': classify_query(query)
        })
        
        # Processamento da query
        result = process_query(query)
        
        # Log do evento de negócio
        logger.log_business_event('sales_query_processed', {
            'processing_time': result.processing_time,
            'tools_used': result.tools_used,
            'confidence_score': result.confidence
        })
        
        return result
```

## 🔍 Análise e Debugging

### Query e Filtragem de Logs

```python
import logfire
from datetime import datetime, timedelta

class LogfireAnalyzer:
    def __init__(self):
        self.client = logfire.Client()
    
    def analyze_agent_performance(self, hours: int = 24):
        """Analisa performance do agente nas últimas horas"""
        
        # Query para buscar spans de execução de agente
        query = f"""
        SELECT 
            span_name,
            attributes,
            duration_ms,
            status_code,
            start_time
        FROM spans 
        WHERE span_name = 'agent_execution'
        AND start_time >= datetime('now', '-{hours} hours')
        ORDER BY start_time DESC
        """
        
        results = self.client.query(query)
        
        # Análise dos resultados
        total_executions = len(results)
        successful_executions = len([r for r in results if r['status_code'] == 'OK'])
        avg_duration = sum([r['duration_ms'] for r in results]) / total_executions if total_executions > 0 else 0
        
        return {
            'total_executions': total_executions,
            'success_rate': successful_executions / total_executions if total_executions > 0 else 0,
            'avg_duration_ms': avg_duration,
            'failed_executions': total_executions - successful_executions
        }
    
    def find_error_patterns(self, days: int = 7):
        """Identifica padrões de erro"""
        
        query = f"""
        SELECT 
            attributes.error AS error_message,
            COUNT(*) as error_count,
            span_name
        FROM spans 
        WHERE status_code = 'ERROR'
        AND start_time >= datetime('now', '-{days} days')
        GROUP BY attributes.error, span_name
        ORDER BY error_count DESC
        """
        
        results = self.client.query(query)
        
        error_patterns = {}
        for result in results:
            pattern = {
                'count': result['error_count'],
                'span_name': result['span_name'],
                'error_message': result['error_message']
            }
            error_patterns[result['error_message']] = pattern
        
        return error_patterns
    
    def get_user_journey_analysis(self, user_id: str, session_id: str = None):
        """Analisa jornada específica do usuário"""
        
        where_clause = f"attributes.user_id = '{user_id}'"
        if session_id:
            where_clause += f" AND attributes.session_id = '{session_id}'"
        
        query = f"""
        SELECT 
            span_name,
            attributes,
            duration_ms,
            start_time,
            parent_span_id
        FROM spans 
        WHERE {where_clause}
        ORDER BY start_time ASC
        """
        
        results = self.client.query(query)
        
        # Reconstrói a árvore de spans
        journey = self._reconstruct_span_tree(results)
        
        return journey
```

## 📊 Dashboards e Visualização

### Métricas Customizadas

```python
import logfire
from typing import Dict, List

class LogfireDashboard:
    def __init__(self):
        self.metrics = {}
    
    def create_agent_dashboard(self):
        """Cria dashboard para agente"""
        
        dashboard_config = {
            "name": "Agent Performance Dashboard",
            "widgets": [
                {
                    "type": "time_series",
                    "title": "Request Rate",
                    "query": """
                        SELECT 
                            date_trunc('minute', start_time) as time,
                            COUNT(*) as requests_per_minute
                        FROM spans 
                        WHERE span_name = 'agent_execution'
                        AND start_time >= datetime('now', '-24 hours')
                        GROUP BY time
                        ORDER BY time
                    """,
                    "chart_type": "line"
                },
                {
                    "type": "histogram",
                    "title": "Response Time Distribution", 
                    "query": """
                        SELECT duration_ms
                        FROM spans 
                        WHERE span_name = 'agent_execution'
                        AND start_time >= datetime('now', '-24 hours')
                    """,
                    "buckets": [100, 500, 1000, 2000, 5000, 10000]
                },
                {
                    "type": "pie_chart",
                    "title": "Tool Usage",
                    "query": """
                        SELECT 
                            attributes.tool_name as tool,
                            COUNT(*) as usage_count
                        FROM spans 
                        WHERE span_name LIKE 'tool_%'
                        AND start_time >= datetime('now', '-24 hours')
                        GROUP BY tool
                    """
                },
                {
                    "type": "single_stat",
                    "title": "Success Rate",
                    "query": """
                        SELECT 
                            (COUNT(CASE WHEN status_code = 'OK' THEN 1 END) * 100.0 / COUNT(*)) as success_rate
                        FROM spans 
                        WHERE span_name = 'agent_execution'
                        AND start_time >= datetime('now', '-24 hours')
                    """
                }
            ]
        }
        
        return dashboard_config
    
    def setup_alerts(self):
        """Configura alertas baseados em logs"""
        
        alerts = [
            {
                "name": "High Error Rate",
                "query": """
                    SELECT COUNT(*) as error_count
                    FROM spans 
                    WHERE status_code = 'ERROR'
                    AND start_time >= datetime('now', '-5 minutes')
                """,
                "condition": "error_count > 5",
                "severity": "critical"
            },
            {
                "name": "Slow Response Time",
                "query": """
                    SELECT AVG(duration_ms) as avg_duration
                    FROM spans 
                    WHERE span_name = 'agent_execution'
                    AND start_time >= datetime('now', '-5 minutes')
                """,
                "condition": "avg_duration > 10000",  # > 10 segundos
                "severity": "warning"
            },
            {
                "name": "Low Success Rate",
                "query": """
                    SELECT 
                        (COUNT(CASE WHEN status_code = 'OK' THEN 1 END) * 100.0 / COUNT(*)) as success_rate
                    FROM spans 
                    WHERE span_name = 'agent_execution'
                    AND start_time >= datetime('now', '-10 minutes')
                """,
                "condition": "success_rate < 90",
                "severity": "warning"
            }
        ]
        
        return alerts
```

## 🎯 Melhores Práticas

### 1. Logging Semântico

```python
# ✅ Boa prática: Use logs semânticos estruturados
import logfire

def process_customer_request(request_data: dict):
    with logfire.span('customer_request_processing') as span:
        # Atributos semânticos
        span.set_attribute('customer.id', request_data['customer_id'])
        span.set_attribute('request.type', request_data['type'])
        span.set_attribute('request.priority', request_data.get('priority', 'normal'))
        
        # Log estruturado de início
        logfire.info('Processing customer request',
                    customer_id=request_data['customer_id'],
                    request_type=request_data['type'],
                    priority=request_data.get('priority', 'normal'))
        
        # Processamento...
        result = handle_request(request_data)
        
        # Log estruturado de resultado
        logfire.info('Customer request completed',
                    customer_id=request_data['customer_id'],
                    processing_time=result.processing_time,
                    satisfaction_score=result.satisfaction_score)
        
        return result
```

### 2. Sampling e Performance

```python
import logfire
from random import random

# Configuração de sampling para reduzir overhead
logfire.configure(
    sampling_rate=0.1,  # 10% das traces
    console=False,  # Disable console output em produção
    service_name='production-agent'
)

# Sampling condicional
def conditional_logging(importance_level: str):
    """Log baseado na importância"""
    
    sample_rates = {
        'debug': 0.01,    # 1%
        'info': 0.1,      # 10%
        'warning': 0.5,   # 50%
        'error': 1.0      # 100%
    }
    
    should_log = random() < sample_rates.get(importance_level, 0.1)
    
    if should_log:
        return logfire.span
    else:
        # No-op context manager
        from contextlib import nullcontext
        return nullcontext
```

### 3. Integração com Pydantic Models

```python
import logfire
from pydantic import BaseModel, Field
from typing import Optional

class AgentExecutionModel(BaseModel):
    """Model para dados de execução do agente"""
    
    agent_id: str = Field(..., description="ID único do agente")
    query: str = Field(..., description="Query do usuário")
    execution_time: float = Field(..., description="Tempo de execução em segundos")
    token_usage: int = Field(..., description="Tokens utilizados")
    success: bool = Field(..., description="Se a execução foi bem-sucedida")
    error_message: Optional[str] = Field(None, description="Mensagem de erro se houver")
    
    def log_execution(self):
        """Log estruturado da execução"""
        
        if self.success:
            logfire.info('Agent execution completed',
                        agent_id=self.agent_id,
                        execution_time=self.execution_time,
                        token_usage=self.token_usage)
        else:
            logfire.error('Agent execution failed',
                         agent_id=self.agent_id,
                         execution_time=self.execution_time,
                         error_message=self.error_message)

# Uso com instrumentação automática
@logfire.instrument('agent_run')
def run_agent_with_model(agent_id: str, query: str) -> AgentExecutionModel:
    start_time = time.time()
    
    try:
        result = execute_agent(query)
        
        execution_data = AgentExecutionModel(
            agent_id=agent_id,
            query=query,
            execution_time=time.time() - start_time,
            token_usage=result.token_usage,
            success=True
        )
        
    except Exception as e:
        execution_data = AgentExecutionModel(
            agent_id=agent_id,
            query=query,
            execution_time=time.time() - start_time,
            token_usage=0,
            success=False,
            error_message=str(e)
        )
    
    # Log automático via model
    execution_data.log_execution()
    
    return execution_data
```

## Próximos Passos

- Explore **[Estratégias de Monitoramento](strategies.md)** para alertas e otimizações
- Compare com **[MLflow](mlflow.md)** e **[Langfuse](langfuse.md)** para diferentes casos de uso
- Veja **[Langtrace](langtrace.md)** para integração com OpenTelemetry

---

[^28]: [Pydantic Logfire - Pydantic AI](https://ai.pydantic.dev/logfire/)
