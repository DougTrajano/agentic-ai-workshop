# Langfuse

O **Langfuse** é uma plataforma open-source de observabilidade especializada em LLMs, oferecendo recursos avançados de análise[^25].

## 📊 Setup e Configuração

```python
from langfuse import Langfuse
from langfuse.decorators import observe

# Inicialização
langfuse = Langfuse(
    secret_key="sk-...",
    public_key="pk-...",
    host="https://cloud.langfuse.com"
)

@observe()
def process_user_query(query: str, user_id: str):
    """Função observada pelo Langfuse"""
    # Automaticamente captura inputs, outputs, timing
    result = agent.process(query, user_id)
    return result

# Trace manual detalhado
def detailed_agent_trace():
    trace = langfuse.trace(
        name="agent_execution",
        user_id="user_123",
        session_id="session_456"
    )
    
    # Span de planejamento
    planning_span = trace.span(
        name="planning",
        input={"query": "Analyze sales data"},
        start_time=datetime.now()
    )
    
    # Execução do plano
    plan = generate_plan()
    planning_span.update(output=plan, end_time=datetime.now())
    
    # Span de execução
    execution_span = trace.span(name="execution")
    result = execute_plan(plan)
    execution_span.update(output=result)
    
    return result
```

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

## Próximos Passos

- Explore **[Langtrace](langtrace.md)** para integração com OpenTelemetry
- Confira **[Pydantic Logfire](logfire.md)** para observabilidade nativa
- Veja **[Estratégias de Monitoramento](strategies.md)** para alertas avançados

---

[^25]: [What is LLM Observability & Monitoring? - Langfuse](https://langfuse.com/faq/all/llm-observability)
