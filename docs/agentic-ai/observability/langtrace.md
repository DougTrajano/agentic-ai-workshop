# Langtrace - Observabilidade Nativa com OpenTelemetry

O **Langtrace** é uma ferramenta open-source que oferece tracing nativo para LLMs usando padrões OpenTelemetry. Ideal para desenvolvimento local e integração com ferramentas existentes de observabilidade 🔍

## 🎯 Vantagens do Langtrace

### 🌐 **Baseado em Padrões Abertos**
- Usa OpenTelemetry como base
- Compatível com qualquer sistema de observabilidade
- Exporta traces para Jaeger, Grafana, Datadog
- Sem vendor lock-in

### 🏠 **Desenvolvimento Local**
- Execução offline sem APIs externas
- Integração com Ollama para LLMs locais
- Performance mínima overhead
- Setup simples em minutos

### 🔧 **Flexibilidade Máxima**
- SDK Python e TypeScript
- Instrumentação automática de libraries
- Context managers para controle granular
- Integração com stacks existentes

## 🛠️ Configuração Inicial

### Instalação e Setup Básico

```python
# Instalação
!pip install langtrace-python-sdk

import os
from langtrace_python_sdk import langtrace, with_langtrace_root_span
from dotenv import load_dotenv

load_dotenv()

# Configuração básica
langtrace.init(
    api_key=os.getenv("LANGTRACE_API_KEY"),  # Opcional para cloud
    write_spans_to_console=True,  # Debug local
    batch=True  # Performance otimizada
)

# Auto-instrumentação de libraries populares
langtrace.auto_instrument()
```

### Configuração com OpenTelemetry

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup OpenTelemetry com múltiplos exporters
trace.set_tracer_provider(TracerProvider())

# Jaeger para visualização local
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

# OTLP para Grafana/Datadog/etc
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317",  # Grafana/OTEL Collector
    insecure=True
)

# Adicionar processadores
span_processor_jaeger = BatchSpanProcessor(jaeger_exporter)
span_processor_otlp = BatchSpanProcessor(otlp_exporter)

trace.get_tracer_provider().add_span_processor(span_processor_jaeger)
trace.get_tracer_provider().add_span_processor(span_processor_otlp)
```

## 📊 Instrumentação Automática

### Instrumentação de LLMs Populares

```python
import openai
import ollama
from anthropic import Anthropic

# Langtrace instrumenta automaticamente quando inicializado
langtrace.init(write_spans_to_console=True)

# OpenAI - tracing automático
def chat_openai(mensagens: list):
    client = openai.OpenAI()
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=mensagens,
        temperature=0.7
    )
    
    return response.choices[0].message.content

# Ollama - tracing automático para modelos locais  
def chat_ollama(prompt: str):
    response = ollama.chat(
        model='llama3',
        messages=[{
            'role': 'user',
            'content': prompt
        }]
    )
    
    return response['message']['content']

# Anthropic - tracing automático
def chat_claude(prompt: str):
    client = Anthropic()
    
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text
```

### Decorator para Root Spans

```python
@with_langtrace_root_span()
def agente_assistente_virtual(query: str, user_id: str):
    """
    Agente virtual com tracing completo
    Root span captura toda a execução
    """
    
    # Análise da query
    intent = analisar_intent(query)
    
    # Buscar contexto
    contexto = buscar_contexto_relevante(query)
    
    # Gerar resposta
    if intent == "weather":
        resposta = chat_ollama(f"Previsão do tempo para: {query}")
    elif intent == "calculation":
        resposta = chat_openai([
            {"role": "system", "content": "Você é uma calculadora"},
            {"role": "user", "content": query}
        ])
    else:
        resposta = chat_claude(query)
    
    # Log da execução
    resultado = {
        "user_id": user_id,
        "intent": intent,
        "resposta": resposta,
        "contexto_usado": len(contexto)
    }
    
    return resultado

# Uso - trace completo automaticamente capturado
resposta = agente_assistente_virtual("Como está o tempo hoje?", "user123")
```

## 🔧 Context Managers para Controle Granular

### Spans Manuais Detalhados

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def agente_complexo_manual(input_data: dict):
    """Agente com spans manuais para controle total"""
    
    with tracer.start_as_current_span("agente_principal") as main_span:
        # Atributos do span principal
        main_span.set_attribute("user_id", input_data.get("user_id"))
        main_span.set_attribute("query_length", len(input_data.get("query", "")))
        
        # Fase 1: Pré-processamento
        with tracer.start_as_current_span("pre_processamento") as prep_span:
            prep_span.set_attribute("input_type", type(input_data).__name__)
            
            processed_input = normalizar_input(input_data["query"])
            keywords = extrair_keywords(processed_input)
            
            prep_span.set_attribute("keywords_found", len(keywords))
            prep_span.add_event("preprocessing_complete", {
                "keywords": keywords,
                "processed_length": len(processed_input)
            })
        
        # Fase 2: Retrieval de contexto
        with tracer.start_as_current_span("context_retrieval") as retrieval_span:
            retrieval_span.set_attribute("keywords_count", len(keywords))
            
            start_time = time.time()
            documentos = buscar_documentos_relevantes(keywords)
            retrieval_time = time.time() - start_time
            
            retrieval_span.set_attribute("documents_found", len(documentos))
            retrieval_span.set_attribute("retrieval_time_ms", retrieval_time * 1000)
            
            if len(documentos) == 0:
                retrieval_span.add_event("no_documents_found", {"query": processed_input})
        
        # Fase 3: Geração LLM
        with tracer.start_as_current_span("llm_generation") as llm_span:
            llm_span.set_attribute("model", "llama3")
            llm_span.set_attribute("context_docs", len(documentos))
            
            # Construir prompt com contexto
            context_text = "\n".join([doc["content"] for doc in documentos])
            prompt = f"Contexto: {context_text}\n\nPergunta: {processed_input}"
            
            llm_span.add_event("prompt_created", {
                "prompt_length": len(prompt),
                "context_length": len(context_text)
            })
            
            # Chamada LLM (instrumentada automaticamente)
            resposta = ollama.chat(
                model='llama3',
                messages=[{
                    'role': 'user', 
                    'content': prompt
                }]
            )
            
            llm_span.set_attribute("response_length", len(resposta['message']['content']))
        
        # Fase 4: Pós-processamento
        with tracer.start_as_current_span("post_processamento") as post_span:
            resposta_final = formatar_resposta(
                resposta['message']['content'],
                documentos
            )
            
            post_span.set_attribute("final_response_length", len(resposta_final))
            post_span.add_event("processing_complete")
        
        # Métricas do span principal
        main_span.set_attribute("total_processing_time", time.time() - main_span.start_time)
        main_span.set_attribute("success", True)
        
        return {
            "resposta": resposta_final,
            "documentos_utilizados": len(documentos),
            "keywords": keywords
        }
```

## 🏠 Integração com Ollama (Local)

### Setup Completo para LLMs Locais

```python
import ollama
from langtrace_python_sdk import langtrace, with_langtrace_root_span

# Configuração para desenvolvimento local
langtrace.init(
    write_spans_to_console=True,  # Ver traces no console
    batch=False  # Envio imediato para debug
)

@with_langtrace_root_span()
def assistente_local(query: str, modelo: str = "llama3"):
    """
    Assistente completamente local usando Ollama
    Ideal para desenvolvimento e testes
    """
    
    try:
        resposta = ollama.chat(
            model=modelo,
            messages=[{
                'role': 'user',
                'content': query
            }]
        )
        
        return {
            "status": "sucesso",
            "resposta": resposta['message']['content'],
            "modelo_usado": modelo,
            "tokens_aprox": len(resposta['message']['content']) // 4  # Estimativa
        }
        
    except Exception as e:
        # Trace captura automaticamente exceções
        return {
            "status": "erro",
            "erro": str(e),
            "modelo_tentativa": modelo
        }

# Teste com diferentes modelos locais
modelos_disponiveis = ["llama3", "mistral", "codellama"]

for modelo in modelos_disponiveis:
    print(f"\n--- Testando {modelo} ---")
    resultado = assistente_local(
        "Explique machine learning em uma frase",
        modelo=modelo
    )
    print(f"Status: {resultado['status']}")
    if resultado['status'] == 'sucesso':
        print(f"Resposta: {resultado['resposta']}")
```

### Bot de Interface com Streamlit

```python
import streamlit as st
import ollama
from langtrace_python_sdk import langtrace, with_langtrace_root_span

# Configurar Langtrace para app web
langtrace.init(write_spans_to_console=False)

class ChatBotLocal:
    def __init__(self):
        self.modelo = "llama3"
        self.historico = []
    
    @with_langtrace_root_span()
    def processar_mensagem(self, mensagem: str, user_session: str):
        """Processa mensagem do usuário com tracing"""
        
        # Adicionar ao histórico
        self.historico.append({"role": "user", "content": mensagem})
        
        # Preparar contexto (últimas 5 mensagens)
        contexto = self.historico[-5:]
        
        try:
            resposta = ollama.chat(
                model=self.modelo,
                messages=contexto
            )
            
            resposta_texto = resposta['message']['content']
            self.historico.append({"role": "assistant", "content": resposta_texto})
            
            return {
                "sucesso": True,
                "resposta": resposta_texto,
                "session": user_session
            }
            
        except Exception as e:
            return {
                "sucesso": False,
                "erro": str(e)
            }

# Interface Streamlit
def main():
    st.title("🤖 ChatBot Local com Langtrace")
    st.write("Powered by Ollama + Observabilidade")
    
    # Inicializar bot
    if 'bot' not in st.session_state:
        st.session_state.bot = ChatBotLocal()
    
    # Input do usuário
    mensagem = st.text_input("Sua mensagem:")
    
    if st.button("Enviar") and mensagem:
        # Processar com tracing
        resultado = st.session_state.bot.processar_mensagem(
            mensagem, 
            st.session_state.get('session_id', 'default')
        )
        
        if resultado['sucesso']:
            st.success(resultado['resposta'])
        else:
            st.error(f"Erro: {resultado['erro']}")
    
    # Mostrar histórico
    st.subheader("Histórico")
    for msg in st.session_state.bot.historico[-10:]:  # Últimas 10
        emoji = "👤" if msg['role'] == 'user' else "🤖"
        st.write(f"{emoji} {msg['content']}")

if __name__ == "__main__":
    main()
```

## 📊 Integração com Elastic APM

### Configuração OpenTelemetry + Elastic

```python
import os
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from langtrace_python_sdk import langtrace

# Configurar variáveis de ambiente para Elastic APM
os.environ.update({
    "OTEL_SERVICE_NAME": "agentic-ai-workshop",
    "OTEL_RESOURCE_ATTRIBUTES": "service.name=agente-ia",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "https://seu-elastic-apm:443",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer seu-token",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "otlp",
})

# Configurar exportador OTLP
otlp_exporter = OTLPSpanExporter(
    endpoint=os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"],
    headers={"Authorization": os.environ["OTEL_EXPORTER_OTLP_HEADERS"]}
)

# Setup trace provider
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Inicializar Langtrace  
langtrace.init()

@with_langtrace_root_span()
def rag_system_com_observabilidade():
    """Sistema RAG com observabilidade completa no Elastic APM"""
    
    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
    
    # Carregar dados
    documents = SimpleDirectoryReader("data/").load_data()
    
    # Criar índice
    index = VectorStoreIndex.from_documents(documents)
    
    # Query engine
    query_engine = index.as_query_engine()
    
    # Query de teste
    resposta = query_engine.query("Como otimizar performance de agentes de IA?")
    
    return str(resposta)

# Executar com instrumentação OpenTelemetry
resultado = rag_system_com_observabilidade()
```

## 🚀 Monitoramento em Produção

### Health Checks Automatizados

```python
import schedule
import time
import requests
from datetime import datetime

class HealthMonitorLangtrace:
    """Monitor de saúde com alertas via Langtrace"""
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url
        langtrace.init()
    
    @with_langtrace_root_span()
    def verificar_saude_completa(self):
        """Verifica saúde de todos os componentes"""
        
        resultados = {
            "timestamp": datetime.now().isoformat(),
            "componentes": {}
        }
        
        # Verificar Ollama
        resultados["componentes"]["ollama"] = self._verificar_ollama()
        
        # Verificar APIs externas (se configuradas)
        resultados["componentes"]["openai"] = self._verificar_openai()
        
        # Verificar RAG system
        resultados["componentes"]["rag"] = self._verificar_rag_system()
        
        # Calcular status geral
        todos_ok = all(
            comp["status"] == "ok" 
            for comp in resultados["componentes"].values()
        )
        
        resultados["status_geral"] = "healthy" if todos_ok else "unhealthy"
        
        # Enviar alerta se necessário
        if not todos_ok:
            self._enviar_alerta(resultados)
        
        return resultados
    
    def _verificar_ollama(self) -> dict:
        """Verifica saúde do Ollama"""
        try:
            start_time = time.time()
            
            resposta = ollama.chat(
                model='llama3',
                messages=[{
                    'role': 'user',
                    'content': 'Health check - responda apenas OK'
                }]
            )
            
            latencia = time.time() - start_time
            
            return {
                "status": "ok",
                "latencia_ms": latencia * 1000,
                "response": resposta['message']['content'][:20]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "erro": str(e)
            }
    
    def _verificar_openai(self) -> dict:
        """Verifica APIs externas"""
        if not os.getenv("OPENAI_API_KEY"):
            return {"status": "skipped", "motivo": "API key não configurada"}
        
        try:
            import openai
            client = openai.OpenAI()
            
            start_time = time.time()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Health check"}],
                max_tokens=5
            )
            latencia = time.time() - start_time
            
            return {
                "status": "ok", 
                "latencia_ms": latencia * 1000,
                "tokens_used": response.usage.total_tokens
            }
            
        except Exception as e:
            return {"status": "error", "erro": str(e)}
    
    def _verificar_rag_system(self) -> dict:
        """Verifica sistema RAG"""
        try:
            # Simular query RAG simples
            start_time = time.time()
            
            # Aqui você verificaria seu sistema RAG real
            # resultado = seu_rag_system.query("test query")
            
            latencia = time.time() - start_time
            
            return {
                "status": "ok",
                "latencia_ms": latencia * 1000
            }
            
        except Exception as e:
            return {"status": "error", "erro": str(e)}
    
    def _enviar_alerta(self, resultados: dict):
        """Envia alertas via webhook"""
        if not self.webhook_url:
            print(f"🚨 ALERTA SAÚDE: {resultados}")
            return
        
        try:
            requests.post(self.webhook_url, json={
                "text": f"🚨 Sistema não está saudável: {resultados['status_geral']}",
                "attachments": [{
                    "color": "danger",
                    "fields": [
                        {
                            "title": comp_name,
                            "value": comp_data["status"],
                            "short": True
                        }
                        for comp_name, comp_data in resultados["componentes"].items()
                    ]
                }]
            })
        except Exception as e:
            print(f"Erro ao enviar alerta: {e}")

# Configurar monitoramento
monitor = HealthMonitorLangtrace(
    webhook_url="https://hooks.slack.com/services/..."  # Seu webhook
)

# Agendar verificações
schedule.every(5).minutes.do(monitor.verificar_saude_completa)

# Loop de monitoramento
print("🔍 Iniciando monitoramento Langtrace...")
while True:
    schedule.run_pending()
    time.sleep(60)
```

## 🎓 Melhores Práticas

### ✅ **Faça**
- Configure múltiplos exportadores (local + produção)
- Use o decorator `@with_langtrace_root_span` para entry points
- Implemente health checks automáticos
- Configure sampling para alta escala
- Use context propagation entre serviços

### ❌ **Evite**
- Traces excessivos que impactam performance
- Exportar dados sensíveis sem filtros
- Dependência única de serviços externos
- Ignorar configuração de batching
- Traces síncronos em aplicações críticas

## 🔗 Recursos Adicionais

- [Documentação Oficial Langtrace](https://langtrace.ai/docs)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [Cookbook Langtrace](https://github.com/Scale3-Labs/langtrace-recipes)
- [Integração com Grafana](https://langtrace.ai/docs/integrations/grafana)

---

**Próximo:** [Logfire - Observabilidade Pydantic](logfire.md) 🚀
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
