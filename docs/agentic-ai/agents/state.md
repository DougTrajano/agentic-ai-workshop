# ⚙️ Gerenciamento de Estado

O **gerenciamento de estado** permite que agentes monitorem o progresso de tarefas e tomem decisões baseadas no contexto atual.

## Estados Típicos de um Agente

```python
from enum import Enum

class AgentState(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING_INPUT = "waiting_input"
    ERROR = "error"
    COMPLETED = "completed"

class AgentStateManager:
    def __init__(self):
        self.current_state = AgentState.IDLE
        self.state_history = []
        self.task_progress = {}
    
    def transition_to(self, new_state):
        self.state_history.append(self.current_state)
        self.current_state = new_state
    
    def update_progress(self, task_id, progress):
        self.task_progress[task_id] = progress
```

## Padrões de Estado

### Estado Baseado em Tarefa

```python
task_state = {
    "task_id": "analyze_sales_data",
    "steps_completed": ["load_data", "clean_data"],
    "current_step": "analyze_trends",
    "remaining_steps": ["generate_report", "send_results"]
}
```

### Estado Baseado em Contexto

```python
context_state = {
    "user_preferences": {"language": "pt", "format": "detailed"},
    "current_dataset": "sales_q4_2024.csv",
    "analysis_type": "trend_analysis",
    "tools_used": ["pandas", "matplotlib"]
}
```

## Implementações Avançadas de Estado

### 1. State Machine com Transições

```python
from typing import Dict, List, Callable
from dataclasses import dataclass

@dataclass
class StateTransition:
    from_state: str
    to_state: str
    condition: Callable
    action: Callable = None

class StateMachine:
    def __init__(self, initial_state: str):
        self.current_state = initial_state
        self.transitions: List[StateTransition] = []
        self.state_data = {}
    
    def add_transition(self, transition: StateTransition):
        self.transitions.append(transition)
    
    def update(self, context):
        for transition in self.transitions:
            if (transition.from_state == self.current_state and 
                transition.condition(context)):
                
                # Executa ação da transição
                if transition.action:
                    transition.action(context)
                
                # Muda estado
                old_state = self.current_state
                self.current_state = transition.to_state
                
                print(f"Transição: {old_state} -> {self.current_state}")
                break
    
    def get_state(self):
        return self.current_state
    
    def set_state_data(self, key, value):
        self.state_data[key] = value
    
    def get_state_data(self, key):
        return self.state_data.get(key)
```

### 2. Estado Hierárquico

```python
class HierarchicalState:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.current_child = None
        self.data = {}
    
    def add_child(self, child_name: str):
        child = HierarchicalState(child_name, parent=self)
        self.children[child_name] = child
        return child
    
    def enter_child(self, child_name: str):
        if child_name in self.children:
            self.current_child = child_name
            return self.children[child_name]
        return None
    
    def exit_to_parent(self):
        if self.parent:
            self.parent.current_child = None
            return self.parent
        return self
    
    def get_full_path(self):
        path = [self.name]
        parent = self.parent
        while parent:
            path.insert(0, parent.name)
            parent = parent.parent
        return " -> ".join(path)

# Exemplo de uso
class AgentHierarchicalState:
    def __init__(self):
        # Estado raiz
        self.root = HierarchicalState("Agent")
        
        # Estados principais
        working = self.root.add_child("Working")
        idle = self.root.add_child("Idle")
        
        # Sub-estados de Working
        planning = working.add_child("Planning")
        executing = working.add_child("Executing")
        
        # Sub-estados de Executing
        data_processing = executing.add_child("DataProcessing")
        analysis = executing.add_child("Analysis")
        reporting = executing.add_child("Reporting")
        
        self.current_state = idle
    
    def transition_to(self, state_path: List[str]):
        current = self.root
        for state_name in state_path:
            current = current.enter_child(state_name)
            if not current:
                raise ValueError(f"Estado '{state_name}' não encontrado")
        self.current_state = current
```

### 3. Estado Baseado em Eventos

```python
from typing import Any
import json
from datetime import datetime

class Event:
    def __init__(self, event_type: str, data: Any = None):
        self.type = event_type
        self.data = data
        self.timestamp = datetime.now()
    
    def to_dict(self):
        return {
            'type': self.type,
            'data': self.data,
            'timestamp': self.timestamp.isoformat()
        }

class EventDrivenState:
    def __init__(self):
        self.state = {}
        self.event_handlers = {}
        self.event_history = []
    
    def register_handler(self, event_type: str, handler: Callable):
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def emit_event(self, event: Event):
        self.event_history.append(event)
        
        # Processa handlers para este tipo de evento
        if event.type in self.event_handlers:
            for handler in self.event_handlers[event.type]:
                handler(self.state, event)
    
    def get_state_snapshot(self):
        return {
            'state': self.state.copy(),
            'last_event': self.event_history[-1].to_dict() if self.event_history else None,
            'event_count': len(self.event_history)
        }

# Exemplo de uso
def handle_task_started(state, event):
    state['current_task'] = event.data['task_id']
    state['status'] = 'executing'
    state['start_time'] = event.timestamp

def handle_task_completed(state, event):
    state['last_completed_task'] = state.get('current_task')
    state['current_task'] = None
    state['status'] = 'idle'
    state['completion_time'] = event.timestamp

# Configuração
event_state = EventDrivenState()
event_state.register_handler('task_started', handle_task_started)
event_state.register_handler('task_completed', handle_task_completed)
```

## Persistência de Estado

### 1. Estado em Memória com Checkpoint

```python
import pickle
import json
from pathlib import Path

class PersistentState:
    def __init__(self, checkpoint_path: str):
        self.checkpoint_path = Path(checkpoint_path)
        self.state = {}
        self.load_checkpoint()
    
    def save_checkpoint(self):
        """Salva estado atual em arquivo"""
        self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.checkpoint_path, 'wb') as f:
            pickle.dump(self.state, f)
    
    def load_checkpoint(self):
        """Carrega estado de arquivo"""
        if self.checkpoint_path.exists():
            with open(self.checkpoint_path, 'rb') as f:
                self.state = pickle.load(f)
        else:
            self.state = {}
    
    def update_state(self, key: str, value: Any):
        self.state[key] = value
        self.save_checkpoint()  # Auto-save
    
    def get_state(self, key: str, default=None):
        return self.state.get(key, default)
```

### 2. Estado Distribuído com Redis

```python
import redis
import json
from typing import Any, Optional

class DistributedState:
    def __init__(self, redis_host='localhost', redis_port=6379, 
                 prefix='agent_state'):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, 
                                       decode_responses=True)
        self.prefix = prefix
    
    def _get_key(self, key: str) -> str:
        return f"{self.prefix}:{key}"
    
    def set_state(self, key: str, value: Any, expire: Optional[int] = None):
        """Define valor do estado"""
        redis_key = self._get_key(key)
        serialized_value = json.dumps(value)
        
        if expire:
            self.redis_client.setex(redis_key, expire, serialized_value)
        else:
            self.redis_client.set(redis_key, serialized_value)
    
    def get_state(self, key: str, default=None):
        """Obtém valor do estado"""
        redis_key = self._get_key(key)
        value = self.redis_client.get(redis_key)
        
        if value is None:
            return default
        
        return json.loads(value)
    
    def delete_state(self, key: str):
        """Remove chave do estado"""
        redis_key = self._get_key(key)
        return self.redis_client.delete(redis_key)
    
    def get_all_keys(self):
        """Lista todas as chaves do estado"""
        pattern = f"{self.prefix}:*"
        keys = self.redis_client.keys(pattern)
        return [key.replace(f"{self.prefix}:", "") for key in keys]
```

## Monitoramento de Estado

### 1. State Observer Pattern

```python
from abc import ABC, abstractmethod
from typing import List

class StateObserver(ABC):
    @abstractmethod
    def on_state_changed(self, old_state: Any, new_state: Any):
        pass

class StateLoggingObserver(StateObserver):
    def on_state_changed(self, old_state: Any, new_state: Any):
        print(f"Estado mudou: {old_state} -> {new_state}")

class StateMetricsObserver(StateObserver):
    def __init__(self):
        self.state_transitions = []
        self.state_durations = {}
    
    def on_state_changed(self, old_state: Any, new_state: Any):
        timestamp = datetime.now()
        self.state_transitions.append({
            'from': old_state,
            'to': new_state,
            'timestamp': timestamp
        })

class ObservableState:
    def __init__(self):
        self._state = None
        self._observers: List[StateObserver] = []
    
    def add_observer(self, observer: StateObserver):
        self._observers.append(observer)
    
    def remove_observer(self, observer: StateObserver):
        self._observers.remove(observer)
    
    def set_state(self, new_state):
        old_state = self._state
        self._state = new_state
        
        # Notifica observadores
        for observer in self._observers:
            observer.on_state_changed(old_state, new_state)
    
    def get_state(self):
        return self._state
```

### 2. Health Check de Estado

```python
class StateHealthChecker:
    def __init__(self):
        self.health_checks = []
    
    def add_check(self, name: str, check_func: Callable):
        self.health_checks.append({
            'name': name,
            'check': check_func
        })
    
    def run_health_checks(self, state):
        results = {}
        
        for check in self.health_checks:
            try:
                result = check['check'](state)
                results[check['name']] = {
                    'status': 'healthy' if result else 'unhealthy',
                    'details': result
                }
            except Exception as e:
                results[check['name']] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return results

# Exemplo de checks
def check_memory_usage(state):
    memory_keys = state.get('memory_keys', [])
    return len(memory_keys) < 1000  # Limite de memória

def check_task_timeout(state):
    start_time = state.get('task_start_time')
    if start_time:
        duration = datetime.now() - start_time
        return duration.total_seconds() < 3600  # 1 hora timeout
    return True

# Configuração
health_checker = StateHealthChecker()
health_checker.add_check('memory_usage', check_memory_usage)
health_checker.add_check('task_timeout', check_task_timeout)
```

## Integração com Agentes

```python
class StatefulAgent:
    def __init__(self):
        self.state_manager = StateMachine('idle')
        self.persistent_state = PersistentState('agent_state.pkl')
        self.observers = []
        
        # Configura transições
        self._setup_state_transitions()
    
    def _setup_state_transitions(self):
        # Idle -> Planning
        self.state_manager.add_transition(StateTransition(
            from_state='idle',
            to_state='planning',
            condition=lambda ctx: ctx.get('has_new_task', False),
            action=self._start_planning
        ))
        
        # Planning -> Executing
        self.state_manager.add_transition(StateTransition(
            from_state='planning',
            to_state='executing',
            condition=lambda ctx: ctx.get('plan_ready', False),
            action=self._start_execution
        ))
        
        # Executing -> Completed
        self.state_manager.add_transition(StateTransition(
            from_state='executing',
            to_state='completed',
            condition=lambda ctx: ctx.get('task_finished', False),
            action=self._finish_task
        ))
    
    def _start_planning(self, context):
        print("Iniciando planejamento...")
        self.persistent_state.update_state('last_planning_start', datetime.now())
    
    def _start_execution(self, context):
        print("Iniciando execução...")
        self.persistent_state.update_state('last_execution_start', datetime.now())
    
    def _finish_task(self, context):
        print("Finalizando tarefa...")
        self.persistent_state.update_state('last_completion', datetime.now())
    
    def process_context(self, context):
        old_state = self.state_manager.get_state()
        self.state_manager.update(context)
        new_state = self.state_manager.get_state()
        
        # Notifica observadores se houve mudança
        if old_state != new_state:
            for observer in self.observers:
                observer.on_state_changed(old_state, new_state)
```

## Boas Práticas para Gerenciamento de Estado

### 1. Mantenha Estado Mínimo

- Armazene apenas o estado essencial para funcionamento
- Use computed properties para dados derivados
- Implemente limpeza periódica de estado antigo

### 2. Implemente Checkpoints

- Salve estado em pontos críticos
- Permita recuperação após falhas
- Use versionamento de estado quando necessário

### 3. Use State Machines para Fluxos Complexos

- Defina claramente estados possíveis
- Implemente transições explícitas
- Valide transições antes de executar

### 4. Monitore Performance

- Acompanhe tamanho do estado
- Monitore tempo de serialização/deserialização
- Implemente alertas para estados problemáticos

## Próximos Passos

- **[Memória em Agentes](memory.md)**: Aprenda sobre diferentes tipos de memória
- **[RAG (Retrieval-Augmented Generation)](rag.md)**: Entenda como implementar sistemas RAG
- **[Ferramentas e MCP](tools.md)**: Descubra como integrar ferramentas aos agentes
