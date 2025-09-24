# MLflow para Observabilidade de IA

O **MLflow** é uma plataforma open-source que revolucionou o gerenciamento de projetos de machine learning. Com a versão 3.x, introduziu recursos especializados para observabilidade de aplicações GenAI, incluindo rastreamento detalhado de LLMs e agentes multi-step 🚀

## 🎯 Por que MLflow para Agentes de IA?

O MLflow resolve três desafios críticos na observabilidade de agentes:

### 🔍 **Observabilidade**
- Monitora cada etapa de execução em tempo real
- Visualiza logs estruturados e traces hierárquicos  
- Captura inputs, outputs e metadados de cada operação

### 🤖 **Explicabilidade**  
- Identifica exatamente qual prompt foi enviado ao modelo
- Rastreia o processo de tomada de decisão do agente
- Facilita debugging quando resultados são inesperados

### 📈 **Rastreabilidade**
- Reproduz issues específicas com contexto completo
- Mantém histórico de performance e comportamento
- Permite análise comparativa entre diferentes versões

## 🛠️ Configuração Inicial

### Instalação e Setup

```python
# Instalação
!pip install mlflow[genai]

import mlflow
import os
from mlflow.tracing import trace
from datetime import datetime

# Configuração básica
mlflow.set_tracking_uri("http://localhost:5000")  # Local
# ou mlflow.set_tracking_uri("databricks")  # Databricks

# Criar experimento
experiment_name = "agentic-ai-workshop"
mlflow.set_experiment(experiment_name)
```

### Configuração de Ambiente

```python
# Configurar variáveis de ambiente para diferentes provedores
os.environ["OPENAI_API_KEY"] = "sua-chave-openai"
os.environ["ANTHROPIC_API_KEY"] = "sua-chave-anthropic"

# Habilitar autolog para integração automática
mlflow.llm.autolog(
    log_inputs_outputs=True,
    log_models=True,
    log_traces=True,
    disable=False
)
```

## 📊 Tracing Básico de Agentes

### Decorator @trace para Funções

```python
from mlflow.tracing import trace

@trace(name="agent_execution")
def executar_agente(query: str, user_id: str) -> dict:
    """Executa agente com tracing automático"""
    
    # MLflow captura automaticamente inputs/outputs
    resultado = {
        "query": query,
        "user_id": user_id,
        "timestamp": datetime.now(),
        "response": processar_query(query),
        "metadata": {"model": "gpt-4", "temperature": 0.7}
    }
    
    return resultado

# Uso
response = executar_agente("Qual é a previsão do tempo?", "user123")
```

### Context Managers para Controle Granular

```python
def agente_complexo(input_data: dict):
    with mlflow.start_run(run_name="agente_multimodal"):
        
        # Etapa 1: Análise de entrada
        with mlflow.start_span(name="analise_entrada") as span1:
            span1.set_inputs({"user_input": input_data})
            
            entrada_processada = processar_entrada(input_data)
            
            span1.set_outputs({"processed_input": entrada_processada})
            span1.set_attributes({
                "input_type": type(input_data).__name__,
                "processing_time": 0.5
            })
        
        # Etapa 2: Geração LLM
        with mlflow.start_span(name="llm_generation") as span2:
            span2.set_inputs({"prompt": entrada_processada})
            
            resposta_llm = chamar_llm(entrada_processada)
            
            span2.set_outputs({"llm_response": resposta_llm})
            span2.set_attributes({
                "model": "gpt-4",
                "tokens_input": 150,
                "tokens_output": 200,
                "cost": 0.012
            })
        
        # Etapa 3: Pós-processamento
        with mlflow.start_span(name="pos_processamento") as span3:
            resultado_final = pos_processar(resposta_llm)
            
            span3.set_outputs({"final_result": resultado_final})
        
        # Métricas do run geral
        mlflow.log_metrics({
            "total_tokens": 350,
            "total_cost": 0.012,
            "execution_time": 2.1,
            "user_satisfaction": 0.85
        })
        
        return resultado_final
```

## 🔧 Integrações com Frameworks Populares

### LangChain + MLflow

```python
from langchain.llms import OpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
import mlflow.langchain

# Auto-instrumentação do LangChain
mlflow.langchain.autolog()

@trace(name="langchain_agent")
def criar_agente_langchain():
    # Definir tools
    def calculadora(expression: str) -> str:
        """Calcula expressões matemáticas"""
        try:
            return str(eval(expression))
        except:
            return "Erro no cálculo"
    
    tools = [
        Tool(
            name="Calculadora",
            func=calculadora,
            description="Útil para cálculos matemáticos"
        )
    ]
    
    # Criar agente
    llm = OpenAI(temperature=0)
    agent = create_react_agent(llm, tools)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

# Uso com tracing automático
agente = criar_agente_langchain()
resultado = agente.invoke({
    "input": "Calcule a raiz quadrada de 144 e multiplique por 3"
})
```

### AutoGen + MLflow

```python
import autogen
from mlflow.tracing import trace

# Configuração de agentes AutoGen
config_list = [
    {
        "model": "gpt-4",
        "api_key": os.environ["OPENAI_API_KEY"]
    }
]

@trace(name="autogen_multiagent")
def criar_sistema_multiagente():
    """Sistema com múltiplos agentes especializados"""
    
    # Agente Assistente
    assistente = autogen.AssistantAgent(
        name="assistente",
        llm_config={"config_list": config_list},
        system_message="Você é um assistente especializado em análise de dados."
    )
    
    # Agente Crítico  
    critico = autogen.AssistantAgent(
        name="critico",
        llm_config={"config_list": config_list},
        system_message="Você revisa e melhora análises, identificando pontos fracos."
    )
    
    # Usuário Proxy
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_execution_config={"work_dir": "autogen_workspace"}
    )
    
    return assistente, critico, user_proxy

# Execução com tracing
assistente, critico, user_proxy = criar_sistema_multiagente()

with mlflow.start_run(run_name="analise_multiagente"):
    user_proxy.initiate_chat(
        assistente,
        message="Analise as vendas do último trimestre e identifique tendências."
    )
```

## 🎨 Dashboard e Visualização

### Interface Web do MLflow

```python
# Iniciar servidor MLflow UI
# No terminal: mlflow ui --host 0.0.0.0 --port 5000

# Ou programaticamente
import subprocess

def iniciar_mlflow_ui(port: int = 5000):
    """Inicia interface web do MLflow"""
    subprocess.Popen([
        "mlflow", "ui", 
        "--host", "0.0.0.0",
        "--port", str(port),
        "--backend-store-uri", "sqlite:///mlflow.db"
    ])
    
    print(f"MLflow UI disponível em http://localhost:{port}")

# Iniciar dashboard
iniciar_mlflow_ui()
```

### Consultas e Análises Programáticas

```python
from mlflow import MlflowClient
import pandas as pd

def analisar_experimentos(experiment_name: str):
    """Analisa resultados de experimentos"""
    client = MlflowClient()
    
    # Buscar experimento
    experiment = client.get_experiment_by_name(experiment_name)
    
    # Buscar runs do experimento
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
        max_results=100
    )
    
    # Converter para DataFrame
    runs_data = []
    for run in runs:
        run_data = {
            "run_id": run.info.run_id,
            "status": run.info.status,
            "start_time": run.info.start_time,
            "duration": run.info.end_time - run.info.start_time if run.info.end_time else None,
            **run.data.params,
            **run.data.metrics
        }
        runs_data.append(run_data)
    
    df = pd.DataFrame(runs_data)
    
    # Análises básicas
    print(f"Total de runs: {len(df)}")
    if 'precisao' in df.columns:
        print(f"Precisão média: {df['precisao'].mean():.3f}")
    if 'latencia_media' in df.columns:
        print(f"Latência média: {df['latencia_media'].mean():.3f}s")
    if 'custo_total_usd' in df.columns:
        print(f"Custo total: ${df['custo_total_usd'].sum():.4f}")
    
    return df

# Usar análise
df_resultados = analisar_experimentos("agentic-ai-workshop")
```

## 🚀 Padrões de Produção

### Monitoramento Contínuo

```python
import schedule
import time
from datetime import datetime

class MonitorAgente:
    """Classe para monitoramento contínuo de agentes em produção"""
    
    def __init__(self, agente, alertas_config: Dict):
        self.agente = agente
        self.alertas = alertas_config
        self.metricas_buffer = []
    
    @trace(name="health_check")
    def verificar_saude(self):
        """Verifica saúde do agente"""
        try:
            start_time = time.time()
            
            # Query de teste padrão
            resultado = self.agente.run("Teste de saúde - responda 'OK'")
            
            latencia = time.time() - start_time
            
            # Log métricas de saúde
            with mlflow.start_run(run_name="health_check"):
                mlflow.log_metrics({
                    "latencia_health_check": latencia,
                    "status": 1 if "OK" in resultado else 0,
                    "timestamp": time.time()
                })
            
            # Verificar alertas
            if latencia > self.alertas.get("max_latencia", 10.0):
                self.enviar_alerta(f"Latência alta: {latencia:.2f}s")
            
            return True
            
        except Exception as e:
            # Log erro
            with mlflow.start_run(run_name="health_check_error"):
                mlflow.log_param("error", str(e))
                mlflow.log_metric("status", 0)
            
            self.enviar_alerta(f"Falha no health check: {e}")
            return False
    
    def enviar_alerta(self, mensagem: str):
        """Envia alertas (implementar integração com Slack, email, etc.)"""
        print(f"🚨 ALERTA: {mensagem} - {datetime.now()}")
        
        # Integração com Slack (exemplo)
        # slack_webhook_url = "https://hooks.slack.com/services/..."
        # requests.post(slack_webhook_url, json={"text": mensagem})

# Configurar monitoramento
monitor = MonitorAgente(
    agente=meu_agente,
    alertas_config={
        "max_latencia": 5.0,
        "min_precisao": 0.8
    }
)

# Agendar verificações periódicas
schedule.every(5).minutes.do(monitor.verificar_saude)

# Loop de monitoramento
while True:
    schedule.run_pending()
    time.sleep(60)
```

## 🎓 Melhores Práticas

### ✅ **Faça**
- Use nomes descritivos para spans e traces
- Registre inputs/outputs de todas as operações críticas  
- Configure alertas baseados em métricas de negócio
- Mantenha histórico de experimentos para análise comparativa
- Use tags consistentes para facilitar buscas

### ❌ **Evite**  
- Logging excessivo que impacta performance
- Expor informações sensíveis nos logs
- Ignorar custos de armazenamento de traces
- Misturar experimentos sem organização clara
- Depender apenas de métricas técnicas (ignorar UX)

## 🔗 Recursos Adicionais

- [Documentação Oficial MLflow](https://mlflow.org/docs/latest/tracing.html)
- [MLflow GenAI Examples](https://github.com/mlflow/mlflow/tree/master/examples/genai)
- [Tutorial Avançado de Tracing](https://mlflow.org/docs/latest/llms/tracing/tutorials/)

---

**Próximo:** [Langfuse - Observabilidade Open Source](langfuse.md) 🚀
        
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
