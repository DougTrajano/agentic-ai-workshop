# Pydantic Logfire - Observabilidade Nativa para Python

O **Pydantic Logfire** é uma plataforma de observabilidade criada pela equipe do Pydantic, oferecendo insights únicos para aplicações Python. Especialmente poderoso para agentes baseados em Pydantic AI 🔥

## 🎯 Por que Logfire para Agentes Python?

### 🐍 **Python-Centric**
- Display rico de objetos Python nativos
- Telemetria de event-loop específica
- Profiling de código Python e queries SQL
- Insights únicos em validação Pydantic

### 📊 **SQL para Análise**
- Query seus dados com SQL padrão
- Compatível com ferramentas BI existentes
- Análises customizadas sem aprender nova sintaxe
- Flexibilidade total de consulta

### 🌐 **OpenTelemetry Nativo**
- Wrapper opinativo sobre OpenTelemetry
- Suporte completo a traces, metrics, logs
- Integração com qualquer stack existente
- Export para ferramentas tradicionais

## 🛠️ Configuração Inicial

### Instalação e Autenticação

```bash
# Instalação
pip install logfire

# Autenticação (primeira vez)
logfire auth
```

### Setup Básico em Python

```python
import logfire
from datetime import date

# Configuração inicial
logfire.configure()

# Logging básico com contexto rico
logfire.info('Olá, {name}!', name='mundo')

# Spans com contexto automático
with logfire.span('Coletando dados do usuário'):
    user_input = input('Qual sua idade [YYYY-mm-dd]? ')
    dob = date.fromisoformat(user_input)
    
    # Debug com objetos Python nativos
    logfire.debug('{dob=} {age=!r}', dob=dob, age=date.today() - dob)
```

### Integração com FastAPI (Automática)

```python
import logfire
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

# Configurar Logfire
logfire.configure()

# Instrumentação automática do FastAPI
logfire.instrument_fastapi(app)

class QueryRequest(BaseModel):
    query: str
    user_id: str
    temperature: float = 0.7

class AgentResponse(BaseModel):
    response: str
    confidence: float
    processing_time: float

@app.post("/agent/query", response_model=AgentResponse)
async def processar_query_agente(request: QueryRequest):
    """Endpoint com observabilidade automática"""
    
    # Logfire captura automaticamente:
    # - Request/response models
    # - Validações Pydantic
    # - Tempo de processamento
    # - Status codes
    
    with logfire.span('Processamento do agente'):
        # Simular processamento
        resposta = await processar_com_llm(request.query)
        
        return AgentResponse(
            response=resposta,
            confidence=0.95,
            processing_time=1.23
        )
```

## 🤖 Instrumentação de Agentes Pydantic AI

### Agente Básico com Logfire

```python
import logfire
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import Optional

# Configurar instrumentação automática
logfire.configure()
logfire.instrument_openai()  # Auto-instrumenta OpenAI
logfire.instrument_anthropic()  # Auto-instrumenta Anthropic

class AgenteConfig(BaseModel):
    temperatura: float = 0.7
    max_tokens: int = 500
    modelo: str = "gpt-4"

class ResultadoAgente(BaseModel):
    resposta: str
    confianca: float
    tempo_processamento: float
    tokens_utilizados: int
    custo_estimado: float

# Agente instrumentado
agente = Agent(
    'openai:gpt-4',
    system_prompt="Você é um especialista em análise de dados empresariais."
)

@logfire.instrument('executar_agente')
def executar_agente_instrumentado(
    query: str, 
    user_id: str,
    config: Optional[AgenteConfig] = None
) -> ResultadoAgente:
    """Agente com instrumentação completa"""
    
    if config is None:
        config = AgenteConfig()
    
    # Context span para toda a execução
    with logfire.span(
        'Execução do agente', 
        query=query,
        user_id=user_id,
        config=config.model_dump()
    ):
        
        # Fase 1: Preparação
        with logfire.span('Preparação da query'):
            query_processada = preprocessar_query(query)
            logfire.info('Query preprocessada', original=query, processada=query_processada)
        
        # Fase 2: Execução do agente (auto-instrumentada)
        with logfire.span('Execução LLM'):
            resultado = agente.run_sync(query_processada)
            
            # Logfire automaticamente captura:
            # - Prompt enviado
            # - Response recebida  
            # - Tokens utilizados
            # - Custo estimado
            # - Latência
        
        # Fase 3: Pós-processamento
        with logfire.span('Pós-processamento'):
            resposta_final = pos_processar_resposta(resultado.data)
            
            # Calcular métricas
            confianca = calcular_confianca(resultado)
            
            logfire.info(
                'Execução completa',
                confianca=confianca,
                tokens=resultado.usage().total_tokens if resultado.usage() else 0,
                custo=resultado.cost()
            )
        
        return ResultadoAgente(
            resposta=resposta_final,
            confianca=confianca,
            tempo_processamento=1.5,  # Seria calculado automaticamente
            tokens_utilizados=resultado.usage().total_tokens if resultado.usage() else 0,
            custo_estimado=resultado.cost()
        )

# Uso do agente
resultado = executar_agente_instrumentado(
    "Analise as tendências de vendas do Q4",
    "user123",
    AgenteConfig(temperatura=0.8, max_tokens=1000)
)
```

### Sistema Multi-Agente com Coordenação

```python
from enum import Enum
from typing import List, Dict, Any
import asyncio

class TipoAgente(str, Enum):
    ANALISTA = "analista"
    CRITICO = "critico"
    SINTETIZADOR = "sintetizador"

class SistemaMultiAgente:
    """Sistema multi-agente com observabilidade completa"""
    
    def __init__(self):
        self.agentes = {
            TipoAgente.ANALISTA: Agent(
                'openai:gpt-4',
                system_prompt="Você é um analista especializado."
            ),
            TipoAgente.CRITICO: Agent(
                'openai:gpt-4',
                system_prompt="Você revisa e critica análises."
            ),
            TipoAgente.SINTETIZADOR: Agent(
                'openai:gpt-4',
                system_prompt="Você sintetiza múltiplas perspectivas."
            )
        }
    
    @logfire.instrument('sistema_multiagente')
    async def processar_query_colaborativa(
        self, 
        query: str, 
        user_id: str
    ) -> Dict[str, Any]:
        """Processamento colaborativo com múltiplos agentes"""
        
        with logfire.span('Sessão multi-agente', query=query, user_id=user_id):
            resultados = {}
            
            # Fase 1: Análise inicial
            with logfire.span('Fase 1: Análise inicial'):
                resultado_analista = await self._executar_agente(
                    TipoAgente.ANALISTA,
                    f"Analise a seguinte solicitação: {query}"
                )
                resultados['analise_inicial'] = resultado_analista
                
                logfire.info(
                    'Análise inicial completa',
                    agente=TipoAgente.ANALISTA,
                    tokens=resultado_analista.usage().total_tokens if resultado_analista.usage() else 0
                )
            
            # Fase 2: Crítica e revisão
            with logfire.span('Fase 2: Revisão crítica'):
                prompt_critico = f"""
                Analise criticamente esta análise:
                {resultado_analista.data}
                
                Identifique pontos fracos e sugestões de melhoria.
                """
                
                resultado_critico = await self._executar_agente(
                    TipoAgente.CRITICO,
                    prompt_critico
                )
                resultados['revisao_critica'] = resultado_critico
                
                logfire.info(
                    'Revisão crítica completa',
                    agente=TipoAgente.CRITICO,
                    tokens=resultado_critico.usage().total_tokens if resultado_critico.usage() else 0
                )
            
            # Fase 3: Síntese final
            with logfire.span('Fase 3: Síntese final'):
                prompt_sintese = f"""
                Sintetize as seguintes perspectivas em uma resposta final:
                
                Análise inicial: {resultado_analista.data}
                
                Revisão crítica: {resultado_critico.data}
                
                Query original: {query}
                """
                
                resultado_final = await self._executar_agente(
                    TipoAgente.SINTETIZADOR,
                    prompt_sintese
                )
                resultados['sintese_final'] = resultado_final
                
                # Calcular métricas agregadas
                total_tokens = sum(
                    r.usage().total_tokens if r.usage() else 0 
                    for r in resultados.values()
                )
                custo_total = sum(r.cost() for r in resultados.values())
                
                logfire.info(
                    'Síntese final completa',
                    agente=TipoAgente.SINTETIZADOR,
                    total_tokens=total_tokens,
                    custo_total=custo_total
                )
            
            return {
                'resposta_final': resultado_final.data,
                'etapas': {
                    'analise': resultado_analista.data,
                    'critica': resultado_critico.data,
                    'sintese': resultado_final.data
                },
                'metricas': {
                    'total_tokens': total_tokens,
                    'custo_total': custo_total,
                    'agentes_envolvidos': len(self.agentes)
                }
            }
    
    async def _executar_agente(self, tipo: TipoAgente, prompt: str):
        """Executa um agente específico com tracing"""
        with logfire.span(f'Execução {tipo.value}', tipo_agente=tipo.value):
            return await self.agentes[tipo].run(prompt)

# Uso do sistema multi-agente
sistema = SistemaMultiAgente()
resultado = await sistema.processar_query_colaborativa(
    "Como podemos melhorar a retenção de clientes?",
    "user456"
)
```

## 📊 Analytics e Consultas SQL

### Análises Customizadas com SQL

```python
# Logfire permite consultas SQL diretas nos dados
query_sql = """
SELECT 
    service_name,
    span_name,
    AVG(duration_ms) as avg_duration,
    COUNT(*) as execution_count,
    SUM(CASE WHEN level = 'error' THEN 1 ELSE 0 END) as error_count
FROM spans 
WHERE 
    start_timestamp >= NOW() - INTERVAL '24 HOURS'
    AND span_name LIKE '%agente%'
GROUP BY service_name, span_name
ORDER BY avg_duration DESC
"""

# Executar via dashboard Logfire ou API
```

### Dashboard Customizado

```python
import logfire
from typing import Dict, List
import pandas as pd

class LogfireAnalytics:
    """Classe para análises avançadas usando Logfire"""
    
    @logfire.instrument('analytics_relatorio')
    def gerar_relatorio_agentes(self, periodo_horas: int = 24) -> Dict:
        """Gera relatório de performance dos agentes"""
        
        with logfire.span('Coleta de dados', periodo=periodo_horas):
            # Coletar métricas dos traces
            metricas = self._coletar_metricas_periodo(periodo_horas)
            
            logfire.info('Dados coletados', total_spans=len(metricas))
        
        with logfire.span('Análise de dados'):
            analise = {
                'periodo_horas': periodo_horas,
                'total_execucoes': len(metricas),
                'tempo_medio_execucao': self._calcular_media_tempo(metricas),
                'taxa_erro': self._calcular_taxa_erro(metricas),
                'custos_totais': self._calcular_custos_totais(metricas),
                'agentes_mais_usados': self._agentes_populares(metricas),
                'picos_uso': self._identificar_picos(metricas)
            }
            
            logfire.info('Análise completa', resumo=analise)
        
        return analise
    
    def _coletar_metricas_periodo(self, horas: int) -> List[Dict]:
        """Simula coleta de métricas via API Logfire"""
        # Na implementação real, usaria API do Logfire
        return [
            {
                'span_name': 'executar_agente',
                'duration_ms': 1200,
                'tokens': 150,
                'cost': 0.012,
                'success': True,
                'timestamp': '2024-01-01T10:00:00Z'
            },
            # ... mais dados
        ]
    
    def _calcular_media_tempo(self, metricas: List[Dict]) -> float:
        """Calcula tempo médio de execução"""
        tempos = [m['duration_ms'] for m in metricas]
        return sum(tempos) / len(tempos) if tempos else 0
    
    def _calcular_taxa_erro(self, metricas: List[Dict]) -> float:
        """Calcula taxa de erro"""
        total = len(metricas)
        erros = sum(1 for m in metricas if not m.get('success', True))
        return erros / total if total > 0 else 0
    
    def _calcular_custos_totais(self, metricas: List[Dict]) -> float:
        """Calcula custos totais"""
        return sum(m.get('cost', 0) for m in metricas)

# Gerar relatórios automáticos
analytics = LogfireAnalytics()
relatorio = analytics.gerar_relatorio_agentes(24)

print(f"Execuções: {relatorio['total_execucoes']}")
print(f"Tempo médio: {relatorio['tempo_medio_execucao']:.2f}ms")
print(f"Taxa de erro: {relatorio['taxa_erro']:.2%}")
print(f"Custo total: ${relatorio['custos_totais']:.4f}")
```

## � Integração com Ferramentas DevOps

### CI/CD com Performance Testing

```python
import logfire
import pytest
import time

class TestPerformanceAgentes:
    """Testes de performance com observabilidade"""
    
    @pytest.fixture(autouse=True)
    def setup_logfire(self):
        """Setup Logfire para testes"""
        logfire.configure(
            send_to_logfire=False,  # Não enviar durante testes
            console=True
        )
    
    @logfire.instrument('performance_test')
    def test_latencia_agente_simples(self):
        """Testa latência de agente simples"""
        
        with logfire.span('Test: Latência agente simples'):
            start_time = time.time()
            
            resultado = executar_agente_instrumentado(
                "Teste simples",
                "test_user"
            )
            
            execution_time = time.time() - start_time
            
            # Assertions com logging
            assert execution_time < 5.0, f"Execução muito lenta: {execution_time}s"
            assert resultado.confianca > 0.8, f"Confiança baixa: {resultado.confianca}"
            
            logfire.info(
                'Performance test completo',
                execution_time=execution_time,
                confianca=resultado.confianca,
                status='PASS'
            )
    
    @logfire.instrument('load_test')
    def test_carga_multiplos_agentes(self):
        """Teste de carga com múltiplos agentes"""
        
        num_requests = 10
        
        with logfire.span(f'Load test: {num_requests} requests'):
            tempos = []
            
            for i in range(num_requests):
                with logfire.span(f'Request {i+1}'):
                    start = time.time()
                    
                    resultado = executar_agente_instrumentado(
                        f"Query de teste {i+1}",
                        f"test_user_{i}"
                    )
                    
                    tempo = time.time() - start
                    tempos.append(tempo)
                    
                    logfire.debug(f'Request {i+1} completo', tempo=tempo)
            
            # Análise dos resultados
            tempo_medio = sum(tempos) / len(tempos)
            tempo_max = max(tempos)
            
            logfire.info(
                'Load test results',
                requests=num_requests,
                tempo_medio=tempo_medio,
                tempo_max=tempo_max,
                all_times=tempos
            )
            
            assert tempo_medio < 3.0, f"Tempo médio muito alto: {tempo_medio}s"
            assert tempo_max < 10.0, f"Tempo máximo muito alto: {tempo_max}s"

# Executar testes com observabilidade
# pytest test_performance.py -v
```

### Monitoring em Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agente-ia-app
spec:
  template:
    spec:
      containers:
      - name: app
        image: agente-ia:latest
        env:
        - name: LOGFIRE_TOKEN
          valueFrom:
            secretKeyRef:
              name: logfire-secret
              key: token
        - name: OTEL_SERVICE_NAME
          value: "agente-ia-production"
        - name: OTEL_RESOURCE_ATTRIBUTES
          value: "environment=prod,version=1.0.0"
```

```python
# app_kubernetes.py
import logfire
import os

# Configurar para Kubernetes
logfire.configure(
    token=os.environ.get('LOGFIRE_TOKEN'),
    service_name=os.environ.get('OTEL_SERVICE_NAME', 'agente-ia'),
    environment=os.environ.get('ENVIRONMENT', 'production')
)

# Instrumentação automática para apps Kubernetes
logfire.instrument_requests()  # HTTP requests
logfire.instrument_psycopg2()  # PostgreSQL
logfire.instrument_redis()     # Redis

@logfire.instrument('health_check')
def health_check():
    """Health check para Kubernetes"""
    return {"status": "healthy", "service": "agente-ia"}

# App com observabilidade completa
from fastapi import FastAPI
app = FastAPI()
logfire.instrument_fastapi(app)

@app.get("/health")
def get_health():
    return health_check()
```

## 🎓 Melhores Práticas

### ✅ **Faça**
- Use `logfire.configure()` no início da aplicação
- Aproveite instrumentação automática de frameworks
- Configure environment/service names apropriados
- Use spans para operações lógicas importantes
- Implemente health checks observáveis

### ❌ **Evite**
- Logging excessivo que impacta performance
- Expor dados sensíveis nos logs
- Instrumentação manual quando existe automática
- Ignorar configuração de sampling em produção
- Misturar logs de diferentes ambientes

## 🔗 Recursos Adicionais

- [Documentação Oficial Logfire](https://pydantic.dev/logfire)
- [Integrações Suportadas](https://docs.pydantic.dev/logfire/integrations/)
- [Pydantic AI Integration](https://docs.pydantic.dev/logfire/integrations/pydantic-ai/)
- [SQL Query Examples](https://docs.pydantic.dev/logfire/guides/advanced/querying/)

---

**Próximo:** [Estratégias de Observabilidade](strategies.md) 🚀
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
