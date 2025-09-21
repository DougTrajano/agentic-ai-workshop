# MLflow Tracing

O **MLflow Tracing** é uma ferramenta open-source que aprimora a observabilidade de LLMs registrando inputs, outputs e metadados de cada passo[^23].

## 🛠️ Configuração Básica

```python
import mlflow
from mlflow.tracing import trace

# Configuração do MLflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("agentic_ai_workshop")

@trace(name="agent_execution")
def run_agent(query: str, user_id: str):
    with mlflow.start_run():
        # Log da query inicial
        mlflow.log_param("query", query)
        mlflow.log_param("user_id", user_id)
        
        # Execução do agente com tracing
        result = agent.run(query)
        
        # Log dos resultados
        mlflow.log_metric("response_time", result.execution_time)
        mlflow.log_metric("token_count", result.token_usage)
        mlflow.log_text(result.response, "agent_response.txt")
        
        return result
```

## 📊 Tracing Detalhado de Agentes

```python
from mlflow.tracing import trace
from typing import Any, Dict

class TracedAgent:
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
    
    @trace(name="agent_planning")
    def plan_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Traces the planning phase"""
        with mlflow.start_span(name="planning") as span:
            span.set_inputs({"context": context})
            
            # Lógica de planejamento
            plan = self._generate_plan(context)
            
            span.set_outputs({"plan": plan})
            span.set_attribute("plan_complexity", len(plan["steps"]))
            
            return plan
    
    @trace(name="tool_execution")
    def execute_tool(self, tool_name: str, params: Dict) -> Any:
        """Traces tool execution"""
        with mlflow.start_span(name=f"tool_{tool_name}") as span:
            span.set_inputs({"tool": tool_name, "params": params})
            
            try:
                result = self.tools[tool_name].execute(params)
                span.set_outputs({"result": result})
                span.set_attribute("execution_status", "success")
                return result
            except Exception as e:
                span.set_attribute("execution_status", "error")
                span.set_attribute("error_message", str(e))
                raise
```

## 📈 Dashboard no MLflow UI

```python
# Visualização de métricas agregadas
def log_aggregate_metrics():
    # Calcula métricas dos últimos 100 runs
    recent_runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        max_results=100
    )
    
    # Métricas agregadas
    avg_response_time = recent_runs['metrics.response_time'].mean()
    total_cost = recent_runs['metrics.cost'].sum()
    success_rate = (recent_runs['tags.status'] == 'success').mean()
    
    # Log no dashboard
    with mlflow.start_run(run_name="dashboard_metrics"):
        mlflow.log_metrics({
            "avg_response_time_last_100": avg_response_time,
            "total_cost_last_100": total_cost,
            "success_rate_last_100": success_rate
        })
```

## 🔍 Análise de Traces

### Busca e Filtragem

```python
class MLflowAnalyzer:
    def __init__(self):
        self.client = mlflow.tracking.MlflowClient()
    
    def analyze_failed_runs(self, experiment_id: str):
        """Analisa runs que falharam"""
        failed_runs = mlflow.search_runs(
            experiment_ids=[experiment_id],
            filter_string="tags.status = 'failed'"
        )
        
        failure_patterns = {}
        for _, run in failed_runs.iterrows():
            error_type = run.get('tags.error_type', 'unknown')
            if error_type not in failure_patterns:
                failure_patterns[error_type] = 0
            failure_patterns[error_type] += 1
        
        return failure_patterns
    
    def get_performance_insights(self, experiment_id: str):
        """Obtém insights de performance"""
        runs = mlflow.search_runs(experiment_ids=[experiment_id])
        
        insights = {
            'avg_response_time': runs['metrics.response_time'].mean(),
            'p95_response_time': runs['metrics.response_time'].quantile(0.95),
            'avg_token_usage': runs['metrics.token_count'].mean(),
            'total_cost': runs['metrics.cost'].sum(),
            'success_rate': (runs['tags.status'] == 'success').mean()
        }
        
        return insights
```

## ⚙️ Configuração Avançada

### Custom Spans e Atributos

```python
import mlflow
from mlflow.tracing import trace
import time

class AdvancedTracedAgent:
    def __init__(self):
        self.conversation_history = []
    
    @trace(name="conversation_turn")
    def handle_conversation_turn(self, user_input: str, session_id: str):
        with mlflow.start_span("input_processing") as span:
            span.set_attribute("input_length", len(user_input))
            span.set_attribute("session_id", session_id)
            
            # Processa entrada
            processed_input = self._process_input(user_input)
            span.set_outputs({"processed_input": processed_input})
        
        with mlflow.start_span("context_retrieval") as span:
            start_time = time.time()
            context = self._retrieve_context(processed_input, session_id)
            retrieval_time = time.time() - start_time
            
            span.set_attribute("context_size", len(context))
            span.set_attribute("retrieval_time", retrieval_time)
            span.set_outputs({"context": context})
        
        with mlflow.start_span("response_generation") as span:
            start_time = time.time()
            response = self._generate_response(processed_input, context)
            generation_time = time.time() - start_time
            
            span.set_attribute("generation_time", generation_time)
            span.set_attribute("response_length", len(response))
            span.set_outputs({"response": response})
        
        return response
```

## 🎯 Melhores Práticas

### 1. Estrutura de Spans

```python
# ✅ Boa prática: Hierarquia clara de spans
@trace(name="agent_execution")
def execute_agent(query: str):
    with mlflow.start_span("planning"):
        plan = create_plan(query)
    
    with mlflow.start_span("execution"):
        for step in plan.steps:
            with mlflow.start_span(f"step_{step.name}"):
                result = execute_step(step)
    
    with mlflow.start_span("response_formatting"):
        response = format_response(result)
    
    return response
```

### 2. Logging de Metadados Relevantes

```python
# ✅ Capture metadados importantes
@trace(name="llm_call")
def call_llm(prompt: str, model: str):
    with mlflow.start_span("llm_call") as span:
        span.set_attribute("model", model)
        span.set_attribute("prompt_length", len(prompt))
        span.set_attribute("temperature", 0.7)
        
        start_time = time.time()
        response = llm.generate(prompt)
        execution_time = time.time() - start_time
        
        span.set_attribute("execution_time", execution_time)
        span.set_attribute("tokens_used", response.usage.total_tokens)
        span.set_attribute("cost", calculate_cost(response.usage))
        
        return response
```

### 3. Tratamento de Erros

```python
@trace(name="safe_agent_execution")
def safe_execute_agent(query: str):
    with mlflow.start_span("agent_execution") as span:
        try:
            result = agent.execute(query)
            span.set_attribute("status", "success")
            return result
        except Exception as e:
            span.set_attribute("status", "error")
            span.set_attribute("error_type", type(e).__name__)
            span.set_attribute("error_message", str(e))
            
            # Log do stack trace
            mlflow.log_text(traceback.format_exc(), "error_stacktrace.txt")
            
            raise
```

## 📊 Integração com Dashboards

### Métricas Customizadas

```python
def setup_custom_metrics():
    """Configura métricas customizadas para o dashboard"""
    
    # Métricas de negócio
    mlflow.log_metric("customer_satisfaction", 4.2)
    mlflow.log_metric("task_completion_rate", 0.95)
    mlflow.log_metric("escalation_rate", 0.03)
    
    # Métricas técnicas
    mlflow.log_metric("avg_context_length", 1500)
    mlflow.log_metric("tool_usage_diversity", 0.8)
    mlflow.log_metric("hallucination_rate", 0.02)
    
    # Métricas de custo
    mlflow.log_metric("cost_per_interaction", 0.15)
    mlflow.log_metric("tokens_per_dollar", 6667)
```

## Próximos Passos

- Explore **[Langfuse](langfuse.md)** para análises mais avançadas
- Confira **[Langtrace](langtrace.md)** para integração com OpenTelemetry
- Veja **[Estratégias de Monitoramento](strategies.md)** para alertas e otimizações

---

[^23]: [MLflow Tracing for LLM Observability](https://mlflow.org/docs/latest/genai/tracing/)
