# Estratégias de Observabilidade para Sistemas Agentivos

A implementação bem-sucedida de observabilidade em sistemas agentivos requer uma abordagem estratégica que equilibre profundidade de insights com eficiência operacional. Este guia apresenta estratégias comprovadas para monitoramento, alertas e otimização contínua 📊

## 🎯 Definindo Métricas de Sucesso

### Framework RATE + Business

Adapte o framework RATE (Rate, Errors, Duration) para sistemas agentivos:

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta

@dataclass
class AgentMetricsFramework:
    """Framework de métricas para sistemas agentivos"""
    
    # RATE Metrics
    request_rate: float  # Requests por segundo
    error_rate: float    # Porcentagem de erros
    duration_p50: float  # Mediana de tempo de resposta
    duration_p95: float  # 95º percentil de latência
    
    # Agent-Specific Metrics
    token_usage_rate: float      # Tokens por request
    tool_usage_rate: float       # Ferramentas por request
    success_rate: float          # Taxa de conclusão de tarefas
    hallucination_rate: float    # Taxa de alucinações detectadas
    
    # Business Metrics
    cost_per_request: float      # Custo médio por request
    user_satisfaction: float     # Score de satisfação
    resolution_rate: float       # Taxa de resolução completa
    escalation_rate: float       # Taxa de escalação humana

class MetricsCalculator:
    """Calculadora de métricas para agentes"""
    
    def __init__(self):
        self.window_size = timedelta(minutes=5)
        self.alerts_thresholds = {
            'error_rate_critical': 0.05,    # 5% de erros
            'latency_p95_warning': 10.0,    # 10s no P95
            'cost_anomaly_factor': 2.0,     # 2x acima da média
            'success_rate_critical': 0.85   # Abaixo de 85%
        }
    
    def calculate_real_time_metrics(
        self, 
        traces: List[Dict], 
        window: timedelta = None
    ) -> AgentMetricsFramework:
        """Calcula métricas em tempo real"""
        
        window = window or self.window_size
        cutoff_time = datetime.now() - window
        
        # Filtrar traces recentes
        recent_traces = [
            t for t in traces 
            if datetime.fromisoformat(t['timestamp']) > cutoff_time
        ]
        
        if not recent_traces:
            return self._empty_metrics()
        
        # Calcular métricas RATE
        total_requests = len(recent_traces)
        error_count = sum(1 for t in recent_traces if t.get('error'))
        durations = [t['duration_ms'] for t in recent_traces if t.get('duration_ms')]
        
        # Métricas específicas de agentes
        tokens_used = [t.get('tokens', 0) for t in recent_traces]
        tools_used = [len(t.get('tools_called', [])) for t in recent_traces]
        successful_tasks = sum(1 for t in recent_traces if t.get('task_completed'))
        
        # Calcular custos
        costs = [t.get('cost', 0) for t in recent_traces]
        
        return AgentMetricsFramework(
            request_rate=total_requests / window.total_seconds(),
            error_rate=error_count / total_requests if total_requests > 0 else 0,
            duration_p50=self._percentile(durations, 50) if durations else 0,
            duration_p95=self._percentile(durations, 95) if durations else 0,
            token_usage_rate=sum(tokens_used) / total_requests if total_requests > 0 else 0,
            tool_usage_rate=sum(tools_used) / total_requests if total_requests > 0 else 0,
            success_rate=successful_tasks / total_requests if total_requests > 0 else 0,
            hallucination_rate=self._calculate_hallucination_rate(recent_traces),
            cost_per_request=sum(costs) / total_requests if total_requests > 0 else 0,
            user_satisfaction=self._calculate_satisfaction(recent_traces),
            resolution_rate=self._calculate_resolution_rate(recent_traces),
            escalation_rate=self._calculate_escalation_rate(recent_traces)
        )
    
    def _percentile(self, values: List[float], p: int) -> float:
        """Calcula percentil de uma lista de valores"""
        if not values:
            return 0
        sorted_values = sorted(values)
        index = int((p / 100.0) * (len(sorted_values) - 1))
        return sorted_values[index]
    
    def _calculate_hallucination_rate(self, traces: List[Dict]) -> float:
        """Calcula taxa de alucinação baseada em validação"""
        # Implementação simples - na prática usaria modelos de detecção
        hallucinations = sum(1 for t in traces if t.get('hallucination_detected'))
        return hallucinations / len(traces) if traces else 0
    
    def _calculate_satisfaction(self, traces: List[Dict]) -> float:
        """Calcula satisfação baseada em feedback"""
        ratings = [t.get('user_rating') for t in traces if t.get('user_rating')]
        return sum(ratings) / len(ratings) if ratings else 0
    
    def _calculate_resolution_rate(self, traces: List[Dict]) -> float:
        """Taxa de resolução completa de tarefas"""
        resolved = sum(1 for t in traces if t.get('task_resolved'))
        return resolved / len(traces) if traces else 0
    
    def _calculate_escalation_rate(self, traces: List[Dict]) -> float:
        """Taxa de escalação para humanos"""
        escalated = sum(1 for t in traces if t.get('escalated_to_human'))
        return escalated / len(traces) if traces else 0
    
    def _empty_metrics(self) -> AgentMetricsFramework:
        """Retorna métricas vazias"""
        return AgentMetricsFramework(
            request_rate=0, error_rate=0, duration_p50=0, duration_p95=0,
            token_usage_rate=0, tool_usage_rate=0, success_rate=0,
            hallucination_rate=0, cost_per_request=0, user_satisfaction=0,
            resolution_rate=0, escalation_rate=0
        )

# Uso prático
calculator = MetricsCalculator()

# Simular traces
traces_example = [
    {
        'timestamp': datetime.now().isoformat(),
        'duration_ms': 1200,
        'tokens': 150,
        'cost': 0.012,
        'error': False,
        'task_completed': True,
        'tools_called': ['web_search', 'calculator'],
        'user_rating': 4.5
    },
    # ... mais traces
]

metrics = calculator.calculate_real_time_metrics(traces_example)
print(f"Taxa de sucesso: {metrics.success_rate:.2%}")
print(f"Custo médio: ${metrics.cost_per_request:.4f}")
```

## 🚨 Sistema de Alertas Inteligentes

### Alertas Baseados em Anomalias

```python
import numpy as np
from typing import Tuple, List
from enum import Enum

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class AlertCondition(Enum):
    THRESHOLD_EXCEEDED = "threshold_exceeded"
    ANOMALY_DETECTED = "anomaly_detected"
    TREND_NEGATIVE = "trend_negative"
    PATTERN_BROKEN = "pattern_broken"

@dataclass
class Alert:
    severity: AlertSeverity
    condition: AlertCondition
    metric_name: str
    current_value: float
    threshold: float
    description: str
    timestamp: datetime
    suggested_actions: List[str]

class IntelligentAlertingSystem:
    """Sistema de alertas inteligente para agentes"""
    
    def __init__(self):
        self.baseline_window = timedelta(days=7)  # Baseline de 7 dias
        self.sensitivity = 2.0  # Desvios padrão para anomalias
        self.alert_cooldown = timedelta(minutes=15)  # Cooldown entre alertas
        self.recent_alerts = []
    
    def analyze_metrics(
        self, 
        current_metrics: AgentMetricsFramework,
        historical_data: List[AgentMetricsFramework]
    ) -> List[Alert]:
        """Analisa métricas e gera alertas inteligentes"""
        
        alerts = []
        
        # 1. Alertas de threshold estático
        alerts.extend(self._check_static_thresholds(current_metrics))
        
        # 2. Detecção de anomalias
        alerts.extend(self._detect_anomalies(current_metrics, historical_data))
        
        # 3. Análise de tendências
        alerts.extend(self._analyze_trends(historical_data))
        
        # 4. Padrões quebrados
        alerts.extend(self._check_pattern_breaks(current_metrics, historical_data))
        
        # Filtrar alertas em cooldown
        filtered_alerts = self._filter_cooldown_alerts(alerts)
        
        # Atualizar histórico
        self.recent_alerts.extend(filtered_alerts)
        
        return filtered_alerts
    
    def _check_static_thresholds(
        self, 
        metrics: AgentMetricsFramework
    ) -> List[Alert]:
        """Verifica thresholds estáticos"""
        
        alerts = []
        
        # Taxa de erro crítica
        if metrics.error_rate > 0.05:
            alerts.append(Alert(
                severity=AlertSeverity.CRITICAL,
                condition=AlertCondition.THRESHOLD_EXCEEDED,
                metric_name="error_rate",
                current_value=metrics.error_rate,
                threshold=0.05,
                description=f"Taxa de erro alta: {metrics.error_rate:.2%}",
                timestamp=datetime.now(),
                suggested_actions=[
                    "Verificar logs de erro recentes",
                    "Analisar padrões de falha",
                    "Considerar rollback se deployment recente"
                ]
            ))
        
        # Latência P95 alta
        if metrics.duration_p95 > 10000:  # 10 segundos
            alerts.append(Alert(
                severity=AlertSeverity.WARNING,
                condition=AlertCondition.THRESHOLD_EXCEEDED,
                metric_name="duration_p95",
                current_value=metrics.duration_p95,
                threshold=10000,
                description=f"Latência P95 alta: {metrics.duration_p95:.0f}ms",
                timestamp=datetime.now(),
                suggested_actions=[
                    "Analisar traces de requests lentos",
                    "Verificar performance de APIs externas",
                    "Considerar otimização de prompts"
                ]
            ))
        
        # Taxa de sucesso baixa
        if metrics.success_rate < 0.85:
            alerts.append(Alert(
                severity=AlertSeverity.CRITICAL,
                condition=AlertCondition.THRESHOLD_EXCEEDED,
                metric_name="success_rate",
                current_value=metrics.success_rate,
                threshold=0.85,
                description=f"Taxa de sucesso baixa: {metrics.success_rate:.2%}",
                timestamp=datetime.now(),
                suggested_actions=[
                    "Revisar system prompts",
                    "Analisar casos de falha",
                    "Verificar integrações de ferramentas"
                ]
            ))
        
        return alerts
    
    def _detect_anomalies(
        self,
        current: AgentMetricsFramework,
        historical: List[AgentMetricsFramework]
    ) -> List[Alert]:
        """Detecta anomalias usando análise estatística"""
        
        if len(historical) < 10:  # Dados insuficientes
            return []
        
        alerts = []
        
        # Analisar custo por request
        historical_costs = [m.cost_per_request for m in historical]
        mean_cost = np.mean(historical_costs)
        std_cost = np.std(historical_costs)
        
        if current.cost_per_request > mean_cost + (self.sensitivity * std_cost):
            alerts.append(Alert(
                severity=AlertSeverity.WARNING,
                condition=AlertCondition.ANOMALY_DETECTED,
                metric_name="cost_per_request",
                current_value=current.cost_per_request,
                threshold=mean_cost + (self.sensitivity * std_cost),
                description=f"Custo anômalo: ${current.cost_per_request:.4f} (média: ${mean_cost:.4f})",
                timestamp=datetime.now(),
                suggested_actions=[
                    "Verificar se modelo foi alterado",
                    "Analisar requests com alto token usage",
                    "Revisar configurações de temperatura"
                ]
            ))
        
        # Analisar uso de tokens
        historical_tokens = [m.token_usage_rate for m in historical]
        mean_tokens = np.mean(historical_tokens)
        std_tokens = np.std(historical_tokens)
        
        if current.token_usage_rate > mean_tokens + (self.sensitivity * std_tokens):
            alerts.append(Alert(
                severity=AlertSeverity.INFO,
                condition=AlertCondition.ANOMALY_DETECTED,
                metric_name="token_usage_rate",
                current_value=current.token_usage_rate,
                threshold=mean_tokens + (self.sensitivity * std_tokens),
                description=f"Uso de tokens elevado: {current.token_usage_rate:.0f} tokens/request",
                timestamp=datetime.now(),
                suggested_actions=[
                    "Analisar tamanho de contexto",
                    "Verificar se prompts foram expandidos",
                    "Considerar otimização de context window"
                ]
            ))
        
        return alerts
    
    def _analyze_trends(
        self,
        historical: List[AgentMetricsFramework]
    ) -> List[Alert]:
        """Analisa tendências ao longo do tempo"""
        
        if len(historical) < 20:  # Dados insuficientes
            return []
        
        alerts = []
        
        # Analisar tendência de satisfação do usuário
        recent_satisfaction = [m.user_satisfaction for m in historical[-10:]]
        older_satisfaction = [m.user_satisfaction for m in historical[-20:-10]]
        
        if recent_satisfaction and older_satisfaction:
            recent_avg = np.mean(recent_satisfaction)
            older_avg = np.mean(older_satisfaction)
            
            # Tendência negativa significativa
            if recent_avg < older_avg - 0.5:  # Queda de 0.5 pontos
                alerts.append(Alert(
                    severity=AlertSeverity.WARNING,
                    condition=AlertCondition.TREND_NEGATIVE,
                    metric_name="user_satisfaction",
                    current_value=recent_avg,
                    threshold=older_avg,
                    description=f"Tendência negativa na satisfação: {recent_avg:.1f} vs {older_avg:.1f}",
                    timestamp=datetime.now(),
                    suggested_actions=[
                        "Analisar feedback recente dos usuários",
                        "Verificar mudanças recentes no sistema",
                        "Considerar A/B test para melhorias"
                    ]
                ))
        
        return alerts
    
    def _check_pattern_breaks(
        self,
        current: AgentMetricsFramework,
        historical: List[AgentMetricsFramework]
    ) -> List[Alert]:
        """Verifica quebras de padrão comportamental"""
        
        alerts = []
        
        # Padrão de uso de ferramentas
        if len(historical) >= 5:
            avg_tools = np.mean([m.tool_usage_rate for m in historical[-5:]])
            
            # Mudança drástica no uso de ferramentas
            if abs(current.tool_usage_rate - avg_tools) > avg_tools * 0.5:
                alerts.append(Alert(
                    severity=AlertSeverity.INFO,
                    condition=AlertCondition.PATTERN_BROKEN,
                    metric_name="tool_usage_rate",
                    current_value=current.tool_usage_rate,
                    threshold=avg_tools,
                    description=f"Padrão de uso de ferramentas alterado: {current.tool_usage_rate:.1f} vs {avg_tools:.1f}",
                    timestamp=datetime.now(),
                    suggested_actions=[
                        "Verificar se agente está acessando ferramentas corretamente",
                        "Analisar tipos de queries recebidas",
                        "Revisar configuração de ferramentas disponíveis"
                    ]
                ))
        
        return alerts
    
    def _filter_cooldown_alerts(self, alerts: List[Alert]) -> List[Alert]:
        """Filtra alertas que estão em cooldown"""
        
        filtered = []
        cutoff_time = datetime.now() - self.alert_cooldown
        
        for alert in alerts:
            # Verificar se já existe alerta recente do mesmo tipo
            recent_similar = any(
                a.metric_name == alert.metric_name and
                a.condition == alert.condition and
                a.timestamp > cutoff_time
                for a in self.recent_alerts
            )
            
            if not recent_similar:
                filtered.append(alert)
        
        return filtered

# Exemplo de uso
alerting = IntelligentAlertingSystem()

# Simular dados históricos
historical_metrics = [
    # ... dados históricos simulados
]

current_metrics = calculator.calculate_real_time_metrics(traces_example)
alerts = alerting.analyze_metrics(current_metrics, historical_metrics)

for alert in alerts:
    print(f"🚨 [{alert.severity.value.upper()}] {alert.description}")
    print(f"   Ações sugeridas: {', '.join(alert.suggested_actions)}")
```

## 📊 Dashboards e Visualizações

### Dashboard Executivo para Agentic AI

```python
from dataclasses import dataclass, asdict
from typing import Dict, Any
import json

@dataclass
class ExecutiveDashboard:
    """Dashboard executivo com KPIs de alto nível"""
    
    # KPIs de Negócio
    total_interactions_24h: int
    user_satisfaction_score: float
    cost_per_interaction: float
    revenue_impact: float
    
    # Eficiência Operacional
    automation_rate: float        # % de tarefas resolvidas sem intervenção humana
    resolution_time_avg: float    # Tempo médio de resolução (minutos)
    escalation_rate: float        # % de casos escalados para humanos
    
    # Qualidade e Confiabilidade
    success_rate_24h: float
    error_rate_24h: float
    uptime_percentage: float
    
    # Tendências (comparação com período anterior)
    satisfaction_trend: str       # "up", "down", "stable"
    cost_trend: str
    usage_trend: str
    
    def to_json(self) -> str:
        """Converte para JSON para APIs de dashboard"""
        return json.dumps(asdict(self), indent=2)

class DashboardGenerator:
    """Gerador de dashboards personalizados"""
    
    def __init__(self):
        self.refresh_interval = timedelta(minutes=5)
    
    def generate_executive_dashboard(
        self,
        current_metrics: AgentMetricsFramework,
        historical_data: List[AgentMetricsFramework],
        business_context: Dict[str, Any]
    ) -> ExecutiveDashboard:
        """Gera dashboard executivo"""
        
        # Calcular KPIs de negócio
        total_interactions = self._calculate_24h_interactions(historical_data)
        cost_per_interaction = current_metrics.cost_per_request
        
        # Revenue impact (exemplo - ajustar para seu caso)
        revenue_impact = total_interactions * business_context.get('value_per_interaction', 2.5)
        
        # Eficiência operacional
        automation_rate = 1.0 - current_metrics.escalation_rate
        resolution_time = current_metrics.duration_p50 / 1000 / 60  # ms para minutos
        
        # Tendências
        satisfaction_trend = self._calculate_trend(
            [m.user_satisfaction for m in historical_data[-7:]],
            [m.user_satisfaction for m in historical_data[-14:-7:]]
        )
        
        cost_trend = self._calculate_trend(
            [m.cost_per_request for m in historical_data[-7:]],
            [m.cost_per_request for m in historical_data[-14:-7:]]
        )
        
        usage_trend = self._calculate_trend(
            [m.request_rate for m in historical_data[-7:]],
            [m.request_rate for m in historical_data[-14:-7:]]
        )
        
        return ExecutiveDashboard(
            total_interactions_24h=total_interactions,
            user_satisfaction_score=current_metrics.user_satisfaction,
            cost_per_interaction=cost_per_interaction,
            revenue_impact=revenue_impact,
            automation_rate=automation_rate,
            resolution_time_avg=resolution_time,
            escalation_rate=current_metrics.escalation_rate,
            success_rate_24h=current_metrics.success_rate,
            error_rate_24h=current_metrics.error_rate,
            uptime_percentage=self._calculate_uptime(historical_data),
            satisfaction_trend=satisfaction_trend,
            cost_trend=cost_trend,
            usage_trend=usage_trend
        )
    
    def _calculate_24h_interactions(
        self,
        historical_data: List[AgentMetricsFramework]
    ) -> int:
        """Calcula total de interações nas últimas 24h"""
        # Simplificado - na prática usaria dados de trace reais
        recent_data = historical_data[-288:]  # Assumindo 5min intervals = 288 points/24h
        return sum(int(m.request_rate * 300) for m in recent_data)  # 300s = 5min
    
    def _calculate_trend(
        self,
        recent_values: List[float],
        older_values: List[float]
    ) -> str:
        """Calcula tendência entre dois períodos"""
        if not recent_values or not older_values:
            return "stable"
        
        recent_avg = sum(recent_values) / len(recent_values)
        older_avg = sum(older_values) / len(older_values)
        
        change_percentage = (recent_avg - older_avg) / older_avg if older_avg != 0 else 0
        
        if change_percentage > 0.05:  # 5% de aumento
            return "up"
        elif change_percentage < -0.05:  # 5% de redução
            return "down"
        else:
            return "stable"
    
    def _calculate_uptime(
        self,
        historical_data: List[AgentMetricsFramework]
    ) -> float:
        """Calcula uptime baseado em taxa de erro"""
        if not historical_data:
            return 100.0
        
        # Considerar uptime como períodos com error_rate < 50%
        uptime_periods = sum(1 for m in historical_data if m.error_rate < 0.5)
        return (uptime_periods / len(historical_data)) * 100.0

# Exemplo de uso
dashboard_gen = DashboardGenerator()

business_context = {
    'value_per_interaction': 3.2,  # Valor médio por interação
    'sla_target_resolution_time': 2.0,  # SLA de 2 minutos
    'cost_budget_daily': 500.0,  # Budget diário de $500
}

executive_dash = dashboard_gen.generate_executive_dashboard(
    current_metrics,
    historical_metrics,
    business_context
)

print("📊 Dashboard Executivo:")
print(f"💬 Interações 24h: {executive_dash.total_interactions_24h:,}")
print(f"⭐ Satisfação: {executive_dash.user_satisfaction_score:.1f}/5.0 ({executive_dash.satisfaction_trend})")
print(f"💰 Custo/interação: ${executive_dash.cost_per_interaction:.4f} ({executive_dash.cost_trend})")
print(f"🤖 Taxa automação: {executive_dash.automation_rate:.1%}")
print(f"✅ Taxa sucesso: {executive_dash.success_rate_24h:.1%}")
print(f"🔄 Uptime: {executive_dash.uptime_percentage:.1f}%")
```

## 🔧 Implementação com Ferramentas Populares

### Integração com Prometheus + Grafana

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

class PrometheusMetrics:
    """Métricas Prometheus para agentes"""
    
    def __init__(self):
        # Contadores
        self.agent_requests_total = Counter(
            'agent_requests_total',
            'Total de requests para agentes',
            ['agent_id', 'user_id', 'status']
        )
        
        self.agent_tokens_total = Counter(
            'agent_tokens_total',
            'Total de tokens utilizados',
            ['agent_id', 'model', 'type']  # type: input/output
        )
        
        # Histogramas para latência
        self.agent_duration_seconds = Histogram(
            'agent_duration_seconds',
            'Duração de execução do agente',
            ['agent_id', 'operation'],
            buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0]
        )
        
        # Gauges para métricas instantâneas
        self.agent_active_sessions = Gauge(
            'agent_active_sessions',
            'Sessões ativas no momento',
            ['agent_id']
        )
        
        self.agent_cost_per_request = Gauge(
            'agent_cost_per_request_dollars',
            'Custo médio por request',
            ['agent_id', 'model']
        )
        
        # Iniciar servidor de métricas
        start_http_server(8000)
        
    def track_request(self, agent_id: str, user_id: str, status: str):
        """Registra request do agente"""
        self.agent_requests_total.labels(
            agent_id=agent_id,
            user_id=user_id,
            status=status
        ).inc()
    
    def track_tokens(self, agent_id: str, model: str, input_tokens: int, output_tokens: int):
        """Registra uso de tokens"""
        self.agent_tokens_total.labels(
            agent_id=agent_id,
            model=model,
            type="input"
        ).inc(input_tokens)
        
        self.agent_tokens_total.labels(
            agent_id=agent_id,
            model=model,
            type="output"
        ).inc(output_tokens)
    
    def track_duration(self, agent_id: str, operation: str, duration_seconds: float):
        """Registra duração de operação"""
        self.agent_duration_seconds.labels(
            agent_id=agent_id,
            operation=operation
        ).observe(duration_seconds)
    
    def update_active_sessions(self, agent_id: str, count: int):
        """Atualiza número de sessões ativas"""
        self.agent_active_sessions.labels(agent_id=agent_id).set(count)
    
    def update_cost_per_request(self, agent_id: str, model: str, cost: float):
        """Atualiza custo médio por request"""
        self.agent_cost_per_request.labels(
            agent_id=agent_id,
            model=model
        ).set(cost)

# Decorator para instrumentação automática
def track_agent_metrics(agent_id: str, operation: str = "execute"):
    """Decorator para tracking automático de métricas"""
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                # Registrar sucesso
                prometheus_metrics.track_request(
                    agent_id=agent_id,
                    user_id=kwargs.get('user_id', 'unknown'),
                    status='success'
                )
                
                return result
                
            except Exception as e:
                # Registrar erro
                prometheus_metrics.track_request(
                    agent_id=agent_id,
                    user_id=kwargs.get('user_id', 'unknown'),
                    status='error'
                )
                raise
                
            finally:
                # Registrar duração
                duration = time.time() - start_time
                prometheus_metrics.track_duration(
                    agent_id=agent_id,
                    operation=operation,
                    duration_seconds=duration
                )
        
        return wrapper
    return decorator

# Instância global
prometheus_metrics = PrometheusMetrics()

# Uso em agentes
@track_agent_metrics(agent_id="customer_support", operation="query_processing")
def processar_consulta_cliente(query: str, user_id: str) -> str:
    """Processa consulta do cliente com tracking automático"""
    
    # Simular processamento
    time.sleep(1.2)
    
    # Tracking manual de tokens (exemplo)
    prometheus_metrics.track_tokens(
        agent_id="customer_support",
        model="gpt-4",
        input_tokens=50,
        output_tokens=120
    )
    
    # Tracking manual de custo
    prometheus_metrics.update_cost_per_request(
        agent_id="customer_support",
        model="gpt-4",
        cost=0.0085
    )
    
    return "Resposta processada com sucesso"

# Exemplo de query Grafana/PromQL
grafana_queries = {
    "requests_per_second": 'rate(agent_requests_total[5m])',
    "error_rate": 'rate(agent_requests_total{status="error"}[5m]) / rate(agent_requests_total[5m])',
    "p95_latency": 'histogram_quantile(0.95, rate(agent_duration_seconds_bucket[5m]))',
    "cost_per_hour": 'increase(agent_cost_per_request_dollars[1h]) * increase(agent_requests_total[1h])',
    "tokens_per_second": 'rate(agent_tokens_total[5m])'
}

print("🚀 Métricas Prometheus disponíveis em http://localhost:8000/metrics")
print("📊 Queries Grafana sugeridas:")
for name, query in grafana_queries.items():
    print(f"  {name}: {query}")
```

## 🎓 Melhores Práticas e Lições Aprendidas

### ✅ **Faça**

1. **Comece pequeno, escale gradualmente**
   - Implemente observabilidade básica primeiro
   - Adicione métricas conforme necessário
   - Use sampling inteligente para reduzir custos

2. **Foque em métricas acionáveis**
   - Toda métrica deve ter uma ação associada
   - Evite "métricas vaidade" sem valor real
   - Priorize métricas de impacto no usuário

3. **Configure alertas inteligentes**
   - Use anomalia detection, não apenas thresholds
   - Implemente cooldown entre alertas similares
   - Forneça ações sugeridas em cada alerta

4. **Mantenha contexto de negócio**
   - Conecte métricas técnicas a KPIs de negócio
   - Use segmentação por usuário/feature
   - Monitore custos vs. valor entregue

### ❌ **Evite**

1. **Over-instrumentation**
   - Não trace cada função/método
   - Evite logs excessivos em produção
   - Balance insights vs. performance

2. **Alertas desnecessários**
   - Falsos positivos degradam confiança
   - Alertas sem ação geram fadiga
   - Thresholds muito baixos causam ruído

3. **Dados sem contexto**
   - Métricas isoladas são pouco úteis
   - Falta de correlação entre eventos
   - Ausência de metadata relevante

## 🔗 Integração com Ferramentas Específicas

### Configuração Rápida por Ferramenta

```bash
# MLflow
pip install mlflow[extras]
export MLFLOW_TRACKING_URI="your-tracking-server"

# Langfuse
pip install langfuse
export LANGFUSE_PUBLIC_KEY="pk-..."
export LANGFUSE_SECRET_KEY="sk-..."

# Langtrace
pip install langtrace-python-sdk
export LANGTRACE_API_KEY="your-api-key"

# Logfire
pip install logfire
logfire auth
```

### Exemplo de Dashboard Unificado

```python
class UnifiedObservability:
    """Observabilidade unificada usando múltiplas ferramentas"""
    
    def __init__(self):
        # Configurar todas as ferramentas
        self.setup_mlflow()
        self.setup_langfuse()
        self.setup_prometheus()
        
    def setup_mlflow(self):
        """Configurar MLflow para tracing"""
        import mlflow
        mlflow.set_tracking_uri("your-tracking-server")
        mlflow.langchain.autolog()
    
    def setup_langfuse(self):
        """Configurar Langfuse para analytics"""
        from langfuse import Langfuse
        self.langfuse = Langfuse()
    
    def setup_prometheus(self):
        """Configurar Prometheus para real-time metrics"""
        self.prometheus = PrometheusMetrics()
    
    @contextmanager
    def trace_agent_execution(self, agent_id: str, operation: str):
        """Context manager para tracing unificado"""
        
        # MLflow span
        with mlflow.start_run(run_name=f"{agent_id}_{operation}"):
            # Langfuse trace
            trace = self.langfuse.trace(name=f"{agent_id}_{operation}")
            
            # Prometheus timing
            start_time = time.time()
            
            try:
                yield {
                    'mlflow_run': mlflow.active_run(),
                    'langfuse_trace': trace,
                    'start_time': start_time
                }
                
                # Log sucesso
                self.prometheus.track_request(agent_id, "user", "success")
                
            except Exception as e:
                # Log erro
                mlflow.log_param("error", str(e))
                trace.update(status="ERROR", status_message=str(e))
                self.prometheus.track_request(agent_id, "user", "error")
                raise
                
            finally:
                # Registrar duração
                duration = time.time() - start_time
                mlflow.log_metric("duration_seconds", duration)
                trace.update(end_time=datetime.now())
                self.prometheus.track_duration(agent_id, operation, duration)

# Uso da observabilidade unificada
unified_obs = UnifiedObservability()

def execute_agent_with_full_observability(query: str):
    """Executa agente com observabilidade completa"""
    
    with unified_obs.trace_agent_execution("support_agent", "customer_query") as ctx:
        # Seu código do agente aqui
        result = agent.run_sync(query)
        
        # Log adicional para cada ferramenta
        mlflow.log_param("query", query)
        mlflow.log_param("model", "gpt-4")
        mlflow.log_metric("tokens_used", result.usage().total_tokens if result.usage() else 0)
        
        ctx['langfuse_trace'].update(
            input=query,
            output=result.data,
            metadata={"model": "gpt-4", "tokens": result.usage().total_tokens if result.usage() else 0}
        )
        
        return result
```

## 📈 Próximos Passos para Implementação

### Roadmap de 30 Dias

#### Semana 1: Setup Básico

- [ ] Escolher ferramenta principal (Langfuse/MLflow/etc.)
- [ ] Instrumentar 1-2 agentes críticos
- [ ] Configurar métricas básicas (latência, erros)
- [ ] Setup de alertas simples

#### Semana 2: Expansão de Métricas

- [ ] Adicionar tracking de custos
- [ ] Implementar métricas de qualidade
- [ ] Configurar dashboards básicos
- [ ] Testar alertas em staging

#### Semana 3: Análise Avançada

- [ ] Implementar detecção de anomalias
- [ ] Configurar análise de tendências
- [ ] Setup de relatórios automatizados
- [ ] Otimizar sampling e retention

#### Semana 4: Produção e Refinamento

- [ ] Deploy completo em produção
- [ ] Ajustar thresholds baseado em dados reais
- [ ] Implementar feedback loop de melhorias
- [ ] Documentar playbooks de resposta

Esta estratégia garante que você tenha visibilidade completa de seus sistemas agentivos, permitindo otimização contínua e resposta rápida a problemas! 🚀

---

**Próximo:** [Setup do Workshop](../../workshop/setup.md) para aplicar estes conceitos na prática!
