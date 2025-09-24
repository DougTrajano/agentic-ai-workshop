# Langfuse - Observabilidade Open Source para LLMs

O **Langfuse** é a plataforma de observabilidade open-source que mais rapidamente cresce no ecossistema de LLMs. Oferece rastreamento profundo, análise de custos e avaliação automatizada de aplicações GenAI 🚀

## 🎯 Por que Langfuse?

### 🔍 **Observabilidade Completa**
- Captura inputs, outputs, metadados de cada interação LLM
- Suporte multimodal (texto, imagens, áudio)
- Traces hierárquicos para agentes complexos
- Dashboard intuitivo para análise visual

### 💰 **Rastreamento de Custos**
- Monitor custos por modelo, usuário ou sessão
- Análise detalhada de uso de tokens
- Alertas automáticos de budget
- ROI tracking para features

### 📊 **Fundação para Avaliações**
- Coleta dados para datasets de avaliação
- Integração com ferramentas de evaluation
- A/B testing de diferentes modelos
- Feedback loops automatizados

## 🛠️ Configuração Inicial

### Instalação e Setup

```python
# Instalação
!pip install langfuse

import os
from langfuse import Langfuse
from langfuse.decorators import observe
from datetime import datetime

# Configuração das credenciais
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"  # EU
# os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com"  # US

# Inicialização do cliente
langfuse = Langfuse()
```

### Configuração com Context Managers

```python
from langfuse import get_client

# Cliente singleton para aplicação
client = get_client()

# Context manager para traces
with client.start_as_current_span(name="user_request") as span:
    span.update(input={"query": "Como está o tempo hoje?"})
    
    # Span aninhado para chamada LLM
    with client.start_as_current_generation(
        name="weather_response", 
        model="gpt-4"
    ) as generation:
        response = chamar_llm("Como está o tempo hoje?")
        generation.update(output={"content": response})
    
    span.update(output="Resposta sobre o tempo fornecida")

# Flush em aplicações de curta duração
client.flush()
```

## 📊 Decorator @observe - Instrumentação Simples

### Uso Básico

```python
from langfuse.decorators import observe

@observe()
def processar_query_usuario(query: str, user_id: str) -> dict:
    """
    Função instrumentada automaticamente pelo Langfuse
    Captura inputs, outputs, timing e exceptions
    """
    
    # Processamento da query
    resultado = {
        "query_original": query,
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "resposta": gerar_resposta(query),
        "metadata": {
            "modelo": "gpt-4",
            "temperatura": 0.7,
            "tokens_utilizados": 245
        }
    }
    
    return resultado

# Uso - tracing automático
resposta = processar_query_usuario("Qual a capital do Brasil?", "user123")
```

### Instrumentação de Classes

```python
class AgenteIA:
    """Agente com instrumentação completa"""
    
    def __init__(self, nome: str):
        self.nome = nome
        self.historico = []
    
    @observe(name="agente_planejamento")
    def planejar_acao(self, contexto: dict) -> dict:
        """Fase de planejamento do agente"""
        
        # Lógica de planejamento
        plano = {
            "etapas": [
                "analisar_contexto",
                "buscar_informacoes", 
                "gerar_resposta"
            ],
            "prioridade": "alta",
            "tempo_estimado": 30
        }
        
        return plano
    
    @observe(name="agente_execucao")
    def executar_plano(self, plano: dict) -> dict:
        """Executa o plano gerado"""
        
        resultados = []
        for etapa in plano["etapas"]:
            resultado_etapa = self._executar_etapa(etapa)
            resultados.append(resultado_etapa)
        
        return {
            "status": "sucesso",
            "resultados": resultados,
            "tempo_execucao": 28.5
        }
    
    @observe(name="etapa_individual")
    def _executar_etapa(self, etapa: str) -> dict:
        """Executa uma etapa específica"""
        # Simulação de processamento
        import time
        time.sleep(0.1)
        
        return {
            "etapa": etapa,
            "status": "concluida",
            "output": f"Resultado da {etapa}"
        }

# Uso do agente instrumentado
agente = AgenteIA("AssistenteIA")
plano = agente.planejar_acao({"usuario": "João", "query": "Análise de vendas"})
resultado = agente.executar_plano(plano)
```

## 🔧 Integração com Frameworks Populares

### LangChain + Langfuse

```python
from langfuse.callback import CallbackHandler
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Configurar callback handler
langfuse_handler = CallbackHandler(
    secret_key="sk-lf-...",
    public_key="pk-lf-...",
    host="https://cloud.langfuse.com"
)

# Chain com instrumentação automática
@observe()
def criar_chain_langchain():
    """Cria chain LangChain com observabilidade"""
    
    template = """
    Você é um assistente especializado em {dominio}.
    
    Pergunta: {pergunta}
    Resposta detalhada:
    """
    
    prompt = PromptTemplate(
        input_variables=["dominio", "pergunta"],
        template=template
    )
    
    llm = OpenAI(
        temperature=0.7,
        callbacks=[langfuse_handler]  # Instrumentação automática
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return chain

# Uso com tracing automático
chain = criar_chain_langchain()
resposta = chain.run(
    dominio="tecnologia",
    pergunta="Como funciona machine learning?"
)
```

### OpenAI SDK + Langfuse

```python
from langfuse.openai import OpenAI

# Cliente OpenAI instrumentado
client = OpenAI()  # Usa automaticamente credenciais Langfuse

@observe()
def chat_com_openai(mensagens: list, modelo: str = "gpt-4") -> str:
    """Chat com OpenAI e tracing automático"""
    
    response = client.chat.completions.create(
        model=modelo,
        messages=mensagens,
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

# Uso - traces automáticos incluem tokens, custos, latência
mensagens = [
    {"role": "system", "content": "Você é um assistente útil"},
    {"role": "user", "content": "Explique quantum computing"}
]

resposta = chat_com_openai(mensagens)
```

### LlamaIndex + Langfuse

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.callbacks import LlamaDebugHandler, CallbackManager
from langfuse.llama_index import LlamaIndexCallbackHandler

# Configurar callback para LlamaIndex
langfuse_callback = LlamaIndexCallbackHandler(
    secret_key="sk-lf-...",
    public_key="pk-lf-...",
    host="https://cloud.langfuse.com"
)

callback_manager = CallbackManager([langfuse_callback])

@observe(name="rag_system")
def criar_sistema_rag():
    """Sistema RAG com observabilidade completa"""
    
    # Carregar documentos
    documents = SimpleDirectoryReader("data/").load_data()
    
    # Criar índice com callback
    index = VectorStoreIndex.from_documents(
        documents,
        callback_manager=callback_manager
    )
    
    # Query engine
    query_engine = index.as_query_engine(
        callback_manager=callback_manager
    )
    
    return query_engine

# Uso - traces incluem retrieval, generation, scores
rag_system = criar_sistema_rag()
resposta = rag_system.query("Como otimizar performance de LLMs?")
```

## 📈 Análise de Custos e Performance

### Dashboard de Custos

```python
from langfuse import Langfuse
import pandas as pd
from datetime import datetime, timedelta

class AnaliseCustomizada:
    """Classe para análises customizadas no Langfuse"""
    
    def __init__(self):
        self.client = Langfuse()
    
    @observe(name="analise_custos")
    def analisar_custos_periodo(self, dias: int = 30) -> dict:
        """Analisa custos dos últimos N dias"""
        
        # Buscar traces do período
        data_inicio = datetime.now() - timedelta(days=dias)
        
        # Usar API do Langfuse para buscar dados
        traces = self.client.get_traces(
            from_timestamp=data_inicio,
            to_timestamp=datetime.now()
        )
        
        custos_por_modelo = {}
        custos_por_usuario = {}
        total_tokens = 0
        
        for trace in traces:
            # Analisar generations (chamadas LLM)
            for generation in trace.generations:
                modelo = generation.model
                usuario = trace.user_id
                
                # Calcular custos
                tokens_input = generation.usage.input_tokens
                tokens_output = generation.usage.output_tokens
                custo = self._calcular_custo(modelo, tokens_input, tokens_output)
                
                # Agregar por modelo
                if modelo not in custos_por_modelo:
                    custos_por_modelo[modelo] = 0
                custos_por_modelo[modelo] += custo
                
                # Agregar por usuário
                if usuario not in custos_por_usuario:
                    custos_por_usuario[usuario] = 0
                custos_por_usuario[usuario] += custo
                
                total_tokens += tokens_input + tokens_output
        
        return {
            "periodo_dias": dias,
            "custo_total": sum(custos_por_modelo.values()),
            "custos_por_modelo": custos_por_modelo,
            "custos_por_usuario": custos_por_usuario,
            "total_tokens": total_tokens,
            "custo_medio_por_request": sum(custos_por_modelo.values()) / len(traces)
        }
    
    def _calcular_custo(self, modelo: str, tokens_input: int, tokens_output: int) -> float:
        """Calcula custo baseado no modelo e tokens"""
        precos = {
            "gpt-4": {"input": 0.00003, "output": 0.00006},
            "gpt-3.5-turbo": {"input": 0.000001, "output": 0.000002},
            "claude-3": {"input": 0.000015, "output": 0.000075}
        }
        
        if modelo not in precos:
            return 0.0
        
        custo_input = tokens_input * precos[modelo]["input"]
        custo_output = tokens_output * precos[modelo]["output"]
        
        return custo_input + custo_output

# Análise de custos
analise = AnaliseCustomizada()
relatorio = analise.analisar_custos_periodo(7)  # Últimos 7 dias

print(f"Custo total: ${relatorio['custo_total']:.4f}")
print(f"Modelo mais caro: {max(relatorio['custos_por_modelo'], key=relatorio['custos_por_modelo'].get)}")
```

### Métricas de Performance

```python
@observe(name="performance_analysis")
def analisar_performance_agente(agente_id: str):
    """Analisa performance de um agente específico"""
    
    client = Langfuse()
    
    # Buscar traces do agente
    traces = client.get_traces(
        tags=["agent_id:" + agente_id],
        limit=1000
    )
    
    latencias = []
    taxa_sucesso = []
    custos = []
    
    for trace in traces:
        # Calcular latência
        if trace.end_time and trace.start_time:
            latencia = (trace.end_time - trace.start_time).total_seconds()
            latencias.append(latencia)
        
        # Taxa de sucesso (sem errors)
        sucesso = len([s for s in trace.spans if s.level == "ERROR"]) == 0
        taxa_sucesso.append(sucesso)
        
        # Custos
        custo_trace = sum(
            calcular_custo_generation(gen) 
            for gen in trace.generations
        )
        custos.append(custo_trace)
    
    # Estatísticas
    stats = {
        "total_execucoes": len(traces),
        "latencia_media": np.mean(latencias),
        "latencia_p95": np.percentile(latencias, 95),
        "taxa_sucesso": np.mean(taxa_sucesso),
        "custo_medio": np.mean(custos),
        "custo_total": sum(custos)
    }
    
    return stats
```

## 🎯 Avaliação e Feedback

### Coleta de Feedback

```python
@observe(name="chat_com_feedback")
def chat_com_coleta_feedback(query: str, user_id: str):
    """Chat que coleta feedback automaticamente"""
    
    # Gerar resposta
    resposta = gerar_resposta_llm(query)
    
    # Simular coleta de feedback (seria via UI)
    feedback_score = simular_feedback_usuario()  # 1-5 stars
    
    # Registrar no trace atual
    langfuse.score(
        name="user_satisfaction",
        value=feedback_score,
        comment=f"Feedback para query: {query[:50]}..."
    )
    
    return resposta

def simular_feedback_usuario():
    """Simula feedback do usuário"""
    import random
    return random.randint(1, 5)
```

### A/B Testing

```python
import random
from typing import Literal

@observe(name="ab_test_agent")
def executar_ab_test(query: str, user_id: str) -> dict:
    """Executa A/B test entre diferentes configurações"""
    
    # Determinar variante
    variante: Literal["A", "B"] = random.choice(["A", "B"])
    
    # Configurações diferentes
    config = {
        "A": {"model": "gpt-4", "temperature": 0.7},
        "B": {"model": "gpt-3.5-turbo", "temperature": 0.9}
    }
    
    # Tag no trace para análise posterior
    langfuse.current_span().update(
        tags=["ab_test", f"variant_{variante}"]
    )
    
    # Executar com configuração
    resposta = executar_agente(query, config[variante])
    
    return {
        "resposta": resposta,
        "variante": variante,
        "config": config[variante]
    }

# Análise de resultados A/B
def analisar_resultados_ab():
    """Analisa resultados do A/B test"""
    client = Langfuse()
    
    traces_a = client.get_traces(tags=["variant_A"])
    traces_b = client.get_traces(tags=["variant_B"])
    
    # Comparar métricas
    scores_a = [t.scores[0].value for t in traces_a if t.scores]
    scores_b = [t.scores[0].value for t in traces_b if t.scores]
    
    print(f"Variante A - Satisfação média: {np.mean(scores_a):.2f}")
    print(f"Variante B - Satisfação média: {np.mean(scores_b):.2f}")
```

## 🚀 Produção e Monitoramento

### Alertas Automáticos

```python
from langfuse import Langfuse
import schedule
import time

class MonitorLangfuse:
    """Sistema de monitoramento com alertas"""
    
    def __init__(self):
        self.client = Langfuse()
        self.thresholds = {
            "latencia_max": 10.0,  # segundos
            "taxa_erro_max": 0.05,  # 5%
            "custo_diario_max": 100.0  # USD
        }
    
    @observe(name="health_monitoring")
    def verificar_saude_sistema(self):
        """Verifica saúde do sistema"""
        
        # Últimas 100 execuções
        traces_recentes = self.client.get_traces(limit=100)
        
        # Calcular métricas
        latencias = self._extrair_latencias(traces_recentes)
        taxa_erro = self._calcular_taxa_erro(traces_recentes)
        custo_recente = self._calcular_custos_recentes()
        
        # Verificar thresholds
        alertas = []
        
        if np.mean(latencias) > self.thresholds["latencia_max"]:
            alertas.append(f"Latência alta: {np.mean(latencias):.2f}s")
        
        if taxa_erro > self.thresholds["taxa_erro_max"]:
            alertas.append(f"Taxa de erro alta: {taxa_erro:.2%}")
        
        if custo_recente > self.thresholds["custo_diario_max"]:
            alertas.append(f"Custo diário alto: ${custo_recente:.2f}")
        
        # Enviar alertas se necessário
        if alertas:
            self._enviar_alertas(alertas)
        
        return {
            "status": "healthy" if not alertas else "warning",
            "alertas": alertas,
            "metricas": {
                "latencia_media": np.mean(latencias),
                "taxa_erro": taxa_erro,
                "custo_recente": custo_recente
            }
        }
    
    def _enviar_alertas(self, alertas: list):
        """Envia alertas via webhook/email"""
        for alerta in alertas:
            print(f"🚨 ALERTA LANGFUSE: {alerta}")
            # Implementar integração com Slack/Discord/Email

# Configurar monitoramento automático
monitor = MonitorLangfuse()

# Verificar a cada 10 minutos
schedule.every(10).minutes.do(monitor.verificar_saude_sistema)

# Loop de monitoramento
while True:
    schedule.run_pending()
    time.sleep(60)
```

## 🎓 Melhores Práticas

### ✅ **Faça**
- Use o decorator `@observe` para instrumentação fácil
- Configure tags consistentes para queries eficientes
- Implemente coleta de feedback dos usuários
- Monitore custos por usuário/feature
- Use traces para criar datasets de avaliação

### ❌ **Evite**
- Expor dados sensíveis nos traces
- Ignorar configuração de sampling em alta escala
- Misturar experimentos sem tags claras
- Depender apenas de métricas técnicas
- Não definir alertas de custo

## 🔗 Recursos Adicionais

- [Documentação Oficial Langfuse](https://langfuse.com/docs)
- [Integrações Suportadas](https://langfuse.com/docs/integrations)
- [Cookbook de Exemplos](https://langfuse.com/docs/cookbook)
- [Self-Hosting Guide](https://langfuse.com/docs/deployment)

---

**Próximo:** [Langtrace - Observabilidade Nativa](langtrace.md) 🚀

## 🔍 Análise Avançada com Langfuse

```python
class LangfuseAnalytics:
    def __init__(self):
        self.langfuse = Langfuse()
    
    def analyze_agent_performance(self, days: int = 7):
        """Análise de performance dos últimos N dias"""
        
        # Busca traces recentes
        traces = self.langfuse.get_traces(
            from_timestamp=datetime.now() - timedelta(days=days)
        )
        
        analytics = {
            'total_requests': len(traces),
            'avg_latency': np.mean([t.latency for t in traces]),
            'success_rate': len([t for t in traces if t.status == 'success']) / len(traces),
            'most_used_tools': self._get_tool_usage(traces),
            'error_patterns': self._analyze_errors(traces),
            'cost_analysis': self._analyze_costs(traces)
        }
        
        return analytics
    
    def create_custom_dashboard(self):
        """Cria dashboard customizado"""
        dashboard = self.langfuse.create_dashboard(
            name="Agent Performance",
            charts=[
                {
                    'type': 'time_series',
                    'metric': 'latency',
                    'title': 'Response Time Over Time'
                },
                {
                    'type': 'bar_chart',
                    'metric': 'tool_usage',
                    'title': 'Most Used Tools'
                },
                {
                    'type': 'funnel',
                    'steps': ['planning', 'execution', 'response'],
                    'title': 'Agent Execution Funnel'
                }
            ]
        )
        return dashboard
```

## 🎯 Decoradores para Observabilidade Automática

### Decorator @observe

```python
from langfuse.decorators import observe
from typing import Dict, Any

class ObservableAgent:
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
    
    @observe(name="agent_planning")
    def plan_actions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Planejamento observado automaticamente"""
        # Langfuse captura automaticamente inputs e outputs
        plan = {
            "steps": ["analyze_context", "select_tools", "execute"],
            "context_size": len(str(context)),
            "estimated_tokens": 150
        }
        return plan
    
    @observe(name="tool_execution")
    def execute_tool(self, tool_name: str, params: Dict) -> Any:
        """Execução de ferramenta observada"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
        
        result = self.tools[tool_name].run(params)
        
        # Metadados adicionais podem ser logados
        self.langfuse.log_metadata({
            "tool_name": tool_name,
            "success": True,
            "execution_time": result.get("execution_time", 0)
        })
        
        return result
    
    @observe(name="response_generation")
    def generate_response(self, plan: Dict, context: Dict) -> str:
        """Geração de resposta observada"""
        response = f"Executed {len(plan['steps'])} steps based on context"
        
        # Log de métricas customizadas
        self.langfuse.score(
            name="response_quality",
            value=0.85,
            comment="Good contextual response"
        )
        
        return response
```

## 📈 Análise de Conversas e Sessões

```python
class ConversationAnalyzer:
    def __init__(self):
        self.langfuse = Langfuse()
    
    def track_conversation_flow(self, session_id: str):
        """Analisa o fluxo de uma conversa"""
        
        # Busca todos os traces de uma sessão
        session_traces = self.langfuse.get_traces(
            session_id=session_id
        )
        
        conversation_metrics = {
            'total_turns': len(session_traces),
            'avg_response_time': np.mean([t.latency for t in session_traces]),
            'user_satisfaction': self._calculate_satisfaction(session_traces),
            'conversation_length': sum([t.input_tokens + t.output_tokens for t in session_traces]),
            'topics_covered': self._extract_topics(session_traces)
        }
        
        return conversation_metrics
    
    def identify_conversation_patterns(self):
        """Identifica padrões em conversas"""
        
        all_sessions = self.langfuse.get_sessions(limit=1000)
        
        patterns = {
            'common_conversation_flows': self._analyze_flows(all_sessions),
            'drop_off_points': self._find_drop_offs(all_sessions),
            'successful_resolutions': self._analyze_resolutions(all_sessions),
            'escalation_triggers': self._find_escalation_patterns(all_sessions)
        }
        
        return patterns
    
    def _calculate_satisfaction(self, traces):
        """Calcula satisfação baseada em scores"""
        satisfaction_scores = []
        for trace in traces:
            scores = self.langfuse.get_scores(trace_id=trace.id)
            user_scores = [s for s in scores if s.name == "user_satisfaction"]
            if user_scores:
                satisfaction_scores.append(user_scores[-1].value)
        
        return np.mean(satisfaction_scores) if satisfaction_scores else None
```

## 🔧 Integração com Diferentes Frameworks

### LangChain Integration

```python
from langfuse.langchain import LangfuseCallbackHandler

# Setup do callback handler
langfuse_handler = LangfuseCallbackHandler(
    secret_key="sk-...",
    public_key="pk-...",
    host="https://cloud.langfuse.com"
)

# Uso com LangChain
from langchain.chains import LLMChain
from langchain.llms import OpenAI

llm = OpenAI()
chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    callbacks=[langfuse_handler]
)

# Execução automaticamente observada
result = chain.run(input_text)
```

### OpenAI Integration

```python
from langfuse.openai import openai

# Patch automático da biblioteca OpenAI
client = openai.OpenAI()

# Todas as chamadas são automaticamente observadas
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    # Metadados adicionais para Langfuse
    langfuse_prompt="chatbot-prompt",
    langfuse_metadata={"user_id": "123", "session_id": "abc"}
)
```

## 📊 Dashboards e Relatórios

### Métricas de Performance

```python
class LangfuseReporting:
    def __init__(self):
        self.langfuse = Langfuse()
    
    def generate_performance_report(self, timeframe: str = "7d"):
        """Gera relatório de performance"""
        
        # Busca dados do período
        traces = self.langfuse.get_traces(
            from_timestamp=self._parse_timeframe(timeframe)
        )
        
        report = {
            "summary": {
                "total_requests": len(traces),
                "avg_latency": f"{np.mean([t.latency for t in traces]):.2f}s",
                "success_rate": f"{self._calculate_success_rate(traces):.1%}",
                "total_cost": f"${sum([t.cost for t in traces]):.2f}"
            },
            "performance_trends": self._calculate_trends(traces),
            "top_errors": self._get_top_errors(traces),
            "cost_breakdown": self._analyze_costs(traces),
            "user_feedback": self._summarize_feedback(traces)
        }
        
        return report
    
    def export_analytics_data(self, format: str = "csv"):
        """Exporta dados para análise externa"""
        
        traces = self.langfuse.get_traces(limit=10000)
        
        data = []
        for trace in traces:
            data.append({
                "trace_id": trace.id,
                "timestamp": trace.timestamp,
                "latency": trace.latency,
                "input_tokens": trace.input_tokens,
                "output_tokens": trace.output_tokens,
                "cost": trace.cost,
                "user_id": trace.user_id,
                "session_id": trace.session_id,
                "status": trace.status
            })
        
        if format == "csv":
            df = pd.DataFrame(data)
            return df.to_csv(index=False)
        elif format == "json":
            return json.dumps(data, indent=2)
```

## 🎯 Melhores Práticas

### 1. Estruturação de Traces

```python
# ✅ Boa prática: Hierarquia clara e metadados relevantes
def execute_agent_with_proper_tracing(user_query: str):
    trace = langfuse.trace(
        name="agent_execution",
        input={"query": user_query},
        metadata={
            "agent_version": "1.2.0",
            "environment": "production",
            "user_type": "premium"
        }
    )
    
    # Span para cada fase principal
    planning_span = trace.span(
        name="planning",
        input={"query": user_query}
    )
    
    plan = create_plan(user_query)
    planning_span.update(output=plan)
    
    # Execução com spans aninhados
    execution_span = trace.span(name="execution")
    
    for i, step in enumerate(plan.steps):
        step_span = execution_span.span(
            name=f"step_{i}_{step.type}",
            input=step.params
        )
        
        result = execute_step(step)
        step_span.update(output=result)
    
    execution_span.update(output={"completed_steps": len(plan.steps)})
    
    return result
```

### 2. Scoring e Avaliação

```python
# Sistema de scoring para qualidade
def score_agent_response(trace_id: str, response: str, user_feedback: Dict):
    # Score automático baseado em métricas
    auto_score = calculate_response_quality(response)
    
    langfuse.score(
        trace_id=trace_id,
        name="response_quality_auto",
        value=auto_score,
        comment="Automated quality assessment"
    )
    
    # Score baseado em feedback do usuário
    if user_feedback.get("rating"):
        langfuse.score(
            trace_id=trace_id,
            name="user_satisfaction",
            value=user_feedback["rating"] / 5.0,
            comment=user_feedback.get("comment", "")
        )
```

## 🔍 Debugging e Troubleshooting

```python
class LangfuseDebugger:
    def __init__(self):
        self.langfuse = Langfuse()
    
    def debug_failed_interactions(self, error_type: str = None):
        """Debug de interações que falharam"""
        
        failed_traces = self.langfuse.get_traces(
            filter={"status": "error"}
        )
        
        if error_type:
            failed_traces = [
                t for t in failed_traces 
                if error_type in str(t.metadata.get("error", ""))
            ]
        
        debug_info = {
            "total_failures": len(failed_traces),
            "failure_patterns": self._analyze_failure_patterns(failed_traces),
            "common_error_messages": self._get_common_errors(failed_traces),
            "affected_users": list(set([t.user_id for t in failed_traces if t.user_id])),
            "recovery_suggestions": self._suggest_fixes(failed_traces)
        }
        
        return debug_info
```

---

[^25]: [What is LLM Observability & Monitoring? - Langfuse](https://langfuse.com/faq/all/llm-observability)
