# Langtrace

O **Langtrace** é uma ferramenta open-source que oferece tracing detalhado usando padrões OpenTelemetry[^26].

## 🚦 Integração com OpenTelemetry

```python
from langtrace_python_sdk import langtrace
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configuração do Langtrace
langtrace.init(
    api_key="your_api_key",
    batch=True,
    write_spans_to_console=False
)

# Setup OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Jaeger exporter para visualização local
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

class LangtraceAgent:
    def __init__(self):
        self.tracer = trace.get_tracer(__name__)
    
    def execute_with_tracing(self, query: str):
        with self.tracer.start_as_current_span("agent_execution") as span:
            span.set_attribute("query", query)
            span.set_attribute("agent.version", "1.0")
            
            # Planning phase
            with self.tracer.start_as_current_span("planning") as planning_span:
                plan = self._plan(query)
                planning_span.set_attribute("plan.steps", len(plan))
            
            # Execution phase
            with self.tracer.start_as_current_span("execution") as exec_span:
                result = self._execute(plan)
                exec_span.set_attribute("execution.success", result.success)
                exec_span.set_attribute("execution.tokens", result.tokens)
            
            return result
```

## 📊 Métricas em Tempo Real

```python
from langtrace_python_sdk.utils.metrics import get_metrics

class RealtimeMetrics:
    def __init__(self):
        self.metrics_client = get_metrics()
    
    def setup_real_time_monitoring(self):
        # Counter para requests
        self.request_counter = self.metrics_client.create_counter(
            name="agent_requests_total",
            description="Total number of agent requests"
        )
        
        # Histogram para latência
        self.latency_histogram = self.metrics_client.create_histogram(
            name="agent_latency_seconds",
            description="Agent response latency"
        )
        
        # Gauge para tokens ativos
        self.active_tokens_gauge = self.metrics_client.create_gauge(
            name="agent_active_tokens",
            description="Currently active tokens"
        )
    
    def record_request(self, latency: float, tokens: int, success: bool):
        self.request_counter.add(1, {"success": str(success)})
        self.latency_histogram.record(latency)
        self.active_tokens_gauge.set(tokens)
```

## 🔧 Instrumentação Automática

### Auto-instrumentação de Bibliotecas

```python
from langtrace_python_sdk import langtrace

# Instrumentação automática de bibliotecas populares
langtrace.init(
    api_key="your_api_key",
    auto_instrument={
        "openai": True,
        "anthropic": True,
        "langchain": True,
        "llamaindex": True,
        "pinecone": True,
        "chromadb": True
    }
)

# Agora todas as chamadas dessas bibliotecas são automaticamente rastreadas
import openai

client = openai.OpenAI()

# Esta chamada será automaticamente instrumentada
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Instrumentação Manual Detalhada

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
import time

class DetailedLangtraceAgent:
    def __init__(self):
        self.tracer = trace.get_tracer(__name__)
    
    def process_query_with_detailed_tracing(self, query: str, user_id: str):
        with self.tracer.start_as_current_span("agent_query_processing") as root_span:
            # Metadados do span raiz
            root_span.set_attribute("user_id", user_id)
            root_span.set_attribute("query_length", len(query))
            root_span.set_attribute("timestamp", time.time())
            
            try:
                # Span de pré-processamento
                with self.tracer.start_as_current_span("preprocessing") as prep_span:
                    prep_span.set_attribute("operation", "query_preprocessing")
                    
                    cleaned_query = self._clean_query(query)
                    prep_span.set_attribute("cleaned_query_length", len(cleaned_query))
                    prep_span.add_event("Query cleaned successfully")
                
                # Span de contextualização
                with self.tracer.start_as_current_span("contextualization") as ctx_span:
                    start_time = time.time()
                    context = self._get_relevant_context(cleaned_query, user_id)
                    context_time = time.time() - start_time
                    
                    ctx_span.set_attribute("context_retrieval_time", context_time)
                    ctx_span.set_attribute("context_items_count", len(context))
                    ctx_span.add_event("Context retrieved", {
                        "context_sources": list(context.keys()),
                        "relevance_scores": [c.get("score", 0) for c in context.values()]
                    })
                
                # Span de geração de resposta
                with self.tracer.start_as_current_span("response_generation") as gen_span:
                    gen_span.set_attribute("model", "gpt-4")
                    gen_span.set_attribute("temperature", 0.7)
                    
                    start_time = time.time()
                    response = self._generate_response(cleaned_query, context)
                    generation_time = time.time() - start_time
                    
                    gen_span.set_attribute("generation_time", generation_time)
                    gen_span.set_attribute("response_length", len(response))
                    gen_span.set_attribute("tokens_used", response.get("tokens", 0))
                    gen_span.add_event("Response generated successfully")
                
                # Span de pós-processamento
                with self.tracer.start_as_current_span("postprocessing") as post_span:
                    final_response = self._postprocess_response(response, user_id)
                    post_span.set_attribute("postprocessing_applied", True)
                    post_span.add_event("Response postprocessed")
                
                # Marca sucesso no span raiz
                root_span.set_status(Status(StatusCode.OK, "Query processed successfully"))
                root_span.set_attribute("total_processing_time", time.time() - start_time)
                
                return final_response
                
            except Exception as e:
                # Marca erro no span raiz
                root_span.set_status(Status(StatusCode.ERROR, str(e)))
                root_span.add_event("Error occurred", {
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                })
                raise
```

## 🔍 Análise de Performance com OpenTelemetry

### Coleta de Métricas Customizadas

```python
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader

# Setup do sistema de métricas
metric_reader = PeriodicExportingMetricReader(
    exporter=ConsoleMetricExporter(),
    export_interval_millis=10000  # 10 segundos
)

metrics.set_meter_provider(MeterProvider(metric_readers=[metric_reader]))
meter = metrics.get_meter(__name__)

class LangtraceMetricsCollector:
    def __init__(self):
        # Counters
        self.request_counter = meter.create_counter(
            name="agent_requests_total",
            description="Total number of agent requests",
            unit="1"
        )
        
        self.error_counter = meter.create_counter(
            name="agent_errors_total",
            description="Total number of agent errors",
            unit="1"
        )
        
        # Histograms
        self.latency_histogram = meter.create_histogram(
            name="agent_request_duration",
            description="Duration of agent requests",
            unit="s"
        )
        
        self.token_histogram = meter.create_histogram(
            name="agent_token_usage",
            description="Token usage per request",
            unit="tokens"
        )
        
        # Gauges
        self.active_sessions_gauge = meter.create_up_down_counter(
            name="agent_active_sessions",
            description="Number of active agent sessions",
            unit="1"
        )
    
    def record_request(self, duration: float, tokens: int, success: bool, user_type: str = "standard"):
        # Registra métricas com labels
        labels = {
            "success": str(success),
            "user_type": user_type
        }
        
        self.request_counter.add(1, labels)
        self.latency_histogram.record(duration, labels)
        self.token_histogram.record(tokens, labels)
        
        if not success:
            self.error_counter.add(1, labels)
    
    def track_session_start(self):
        self.active_sessions_gauge.add(1)
    
    def track_session_end(self):
        self.active_sessions_gauge.add(-1)
```

## 🎯 Integração com Sistemas de Monitoramento

### Grafana e Prometheus

```python
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

# Setup para exportar métricas para Prometheus
prometheus_reader = PrometheusMetricReader()
metrics.set_meter_provider(MeterProvider(metric_readers=[prometheus_reader]))

# Inicia servidor HTTP para Prometheus scraper
start_http_server(port=8000, addr="localhost")

class PrometheusIntegration:
    def __init__(self):
        self.meter = metrics.get_meter(__name__)
        self.setup_business_metrics()
    
    def setup_business_metrics(self):
        """Define métricas específicas de negócio"""
        
        # Métricas de qualidade
        self.quality_score = self.meter.create_histogram(
            name="agent_response_quality",
            description="Quality score of agent responses",
            unit="score"
        )
        
        # Métricas de custo
        self.cost_per_request = self.meter.create_histogram(
            name="agent_cost_per_request",
            description="Cost per agent request",
            unit="usd"
        )
        
        # Métricas de satisfação
        self.user_satisfaction = self.meter.create_histogram(
            name="agent_user_satisfaction",
            description="User satisfaction rating",
            unit="rating"
        )
    
    def record_business_metrics(self, interaction_data: dict):
        """Registra métricas de negócio"""
        
        labels = {
            "agent_type": interaction_data.get("agent_type", "general"),
            "task_category": interaction_data.get("task_category", "unknown")
        }
        
        if "quality_score" in interaction_data:
            self.quality_score.record(interaction_data["quality_score"], labels)
        
        if "cost" in interaction_data:
            self.cost_per_request.record(interaction_data["cost"], labels)
        
        if "user_rating" in interaction_data:
            self.user_satisfaction.record(interaction_data["user_rating"], labels)
```

### Jaeger para Distributed Tracing

```python
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

class JaegerIntegration:
    def __init__(self):
        self.setup_jaeger_exporter()
    
    def setup_jaeger_exporter(self):
        """Configura exportador Jaeger"""
        
        jaeger_exporter = JaegerExporter(
            agent_host_name="localhost",
            agent_port=6831,
            collector_endpoint="http://localhost:14268/api/traces",
        )
        
        span_processor = BatchSpanProcessor(jaeger_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)
    
    def create_distributed_trace(self, operation_name: str, trace_context: dict = None):
        """Cria trace distribuído"""
        
        tracer = trace.get_tracer(__name__)
        
        # Se há contexto de trace distribuído, usa ele
        if trace_context:
            parent_context = trace.set_span_in_context(
                trace.SpanContext(**trace_context)
            )
            with tracer.start_as_current_span(
                operation_name, 
                context=parent_context
            ) as span:
                return span
        else:
            return tracer.start_as_current_span(operation_name)
```

## 🔧 Alertas e Monitoramento Proativo

```python
from typing import Dict, List, Callable
import asyncio

class LangtraceAlerting:
    def __init__(self):
        self.alert_rules = []
        self.notification_channels = []
    
    def add_alert_rule(self, 
                      metric_name: str, 
                      threshold: float, 
                      condition: str = "greater_than",
                      window_size: int = 60):
        """Adiciona regra de alerta"""
        
        rule = {
            "metric_name": metric_name,
            "threshold": threshold,
            "condition": condition,
            "window_size": window_size,
            "last_triggered": None
        }
        
        self.alert_rules.append(rule)
    
    def check_alerts(self, current_metrics: Dict[str, float]):
        """Verifica se alguma regra de alerta foi violada"""
        
        triggered_alerts = []
        
        for rule in self.alert_rules:
            metric_value = current_metrics.get(rule["metric_name"])
            
            if metric_value is None:
                continue
            
            should_trigger = False
            
            if rule["condition"] == "greater_than" and metric_value > rule["threshold"]:
                should_trigger = True
            elif rule["condition"] == "less_than" and metric_value < rule["threshold"]:
                should_trigger = True
            
            if should_trigger:
                alert = {
                    "rule": rule,
                    "current_value": metric_value,
                    "timestamp": time.time()
                }
                triggered_alerts.append(alert)
        
        if triggered_alerts:
            self._send_alerts(triggered_alerts)
        
        return triggered_alerts
    
    def _send_alerts(self, alerts: List[Dict]):
        """Envia alertas através dos canais configurados"""
        for alert in alerts:
            for channel in self.notification_channels:
                channel.send_alert(alert)
```

## 🎯 Melhores Práticas

### 1. Sampling Inteligente

```python
from opentelemetry.sdk.trace.sampling import TraceIdRatioBasedSampler, ParentBased

# Configuração de sampling para reduzir overhead
sampling_rate = 0.1  # 10% das traces

sampler = ParentBased(
    root=TraceIdRatioBasedSampler(sampling_rate)
)

# Aplicar ao TracerProvider
trace_provider = TracerProvider(sampler=sampler)
trace.set_tracer_provider(trace_provider)
```

### 2. Atributos Padronizados

```python
# ✅ Boa prática: Use atributos semânticos padronizados
from opentelemetry.semconv.trace import SpanAttributes

def create_standardized_span(operation: str, **kwargs):
    tracer = trace.get_tracer(__name__)
    
    with tracer.start_as_current_span(operation) as span:
        # Atributos semânticos padrão
        span.set_attribute(SpanAttributes.SERVICE_NAME, "agentic-ai-agent")
        span.set_attribute(SpanAttributes.SERVICE_VERSION, "1.0.0")
        span.set_attribute(SpanAttributes.DEPLOYMENT_ENVIRONMENT, "production")
        
        # Atributos específicos do contexto
        if "user_id" in kwargs:
            span.set_attribute("user.id", kwargs["user_id"])
        
        if "model" in kwargs:
            span.set_attribute("llm.model", kwargs["model"])
        
        return span
```

## Próximos Passos

- Explore **[Pydantic Logfire](logfire.md)** para observabilidade nativa
- Confira **[Estratégias de Monitoramento](strategies.md)** para alertas avançados
- Retorne ao **[MLflow](mlflow.md)** para comparar diferentes abordagens

---

[^26]: [Introducing Langtrace - Langtrace](https://www.langtrace.ai/blog/introducing-langtrace)
