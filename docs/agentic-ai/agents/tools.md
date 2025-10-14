# 🛠️ Tools e Model Context Protocol (MCP)

As **ferramentas** permitem que agentes interajam com o mundo externo, executando tarefas específicas além da geração de texto.

## Tipos de Ferramentas

### 1. Ferramentas de Dados

- Consulta a bancos de dados
- Processamento de arquivos
- APIs de dados externos

### 2. Ferramentas de Análise

- Bibliotecas estatísticas
- Visualização de dados
- Machine learning

### 3. Ferramentas de Comunicação

- Envio de emails
- Notificações
- Integração com Slack/Teams

### 4. Ferramentas de Sistema

- Execução de comandos
- Manipulação de arquivos
- Monitoramento de recursos

## Implementação de Ferramentas

```python
from typing import Dict, Any
import pandas as pd

class DataAnalysisTool:
    name = "data_analysis"
    description = "Analisa dados e gera insights"
    
    def execute(self, params: Dict[str, Any]) -> str:
        """
        Executa análise de dados
        
        Args:
            params: {
                "data_path": "caminho/para/dados.csv",
                "analysis_type": "descriptive|correlation|trend",
                "columns": ["col1", "col2"]
            }
        """
        data_path = params.get("data_path")
        analysis_type = params.get("analysis_type", "descriptive")
        
        # Carrega dados
        df = pd.read_csv(data_path)
        
        if analysis_type == "descriptive":
            result = df.describe().to_string()
        elif analysis_type == "correlation":
            result = df.corr().to_string()
        else:
            result = "Análise não suportada"
        
        return f"Análise {analysis_type} concluída:\n{result}"

# Registro de ferramentas
available_tools = {
    "data_analysis": DataAnalysisTool(),
    # Outras ferramentas...
}
```

## Ferramentas Avançadas

### 1. Ferramenta de API Web

```python
import requests
from typing import Optional
import json

class WebAPITool:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def get(self, endpoint: str, params: Dict = None):
        """Executa GET request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, data: Dict):
        """Executa POST request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

class WeatherTool:
    def __init__(self, api_key: str):
        self.api = WebAPITool("https://api.openweathermap.org/data/2.5", api_key)
    
    def get_weather(self, city: str) -> str:
        try:
            data = self.api.get("weather", {
                "q": city,
                "appid": self.api.api_key,
                "units": "metric",
                "lang": "pt"
            })
            
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"Temperatura em {city}: {temp}°C, {description}"
        
        except Exception as e:
            return f"Erro ao obter clima: {str(e)}"
```

### 2. Ferramenta de Banco de Dados

```python
import sqlite3
import pandas as pd
from typing import List, Dict

class DatabaseTool:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Executa query SELECT e retorna resultados"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Executa query UPDATE/INSERT/DELETE"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def get_table_schema(self, table_name: str) -> List[Dict]:
        """Obtém schema de uma tabela"""
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
    
    def list_tables(self) -> List[str]:
        """Lista todas as tabelas"""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        results = self.execute_query(query)
        return [row['name'] for row in results]

class SQLAnalysisTool:
    def __init__(self, db_path: str):
        self.db = DatabaseTool(db_path)
    
    def analyze_table(self, table_name: str) -> str:
        """Analisa uma tabela específica"""
        try:
            # Obtém schema
            schema = self.db.get_table_schema(table_name)
            
            # Conta registros
            count_result = self.db.execute_query(f"SELECT COUNT(*) as count FROM {table_name}")
            record_count = count_result[0]['count']
            
            # Constrói relatório
            report = f"Análise da tabela '{table_name}':\n"
            report += f"Total de registros: {record_count}\n\n"
            report += "Colunas:\n"
            
            for col in schema:
                report += f"- {col['name']} ({col['type']})\n"
            
            return report
        
        except Exception as e:
            return f"Erro na análise: {str(e)}"
```

### 3. Ferramenta de Sistema de Arquivos

```python
import os
import shutil
from pathlib import Path
from typing import List, Optional

class FileSystemTool:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path).resolve()
    
    def _validate_path(self, path: str) -> Path:
        """Valida e resolve caminho"""
        full_path = (self.base_path / path).resolve()
        
        # Verifica se está dentro do diretório base
        if not str(full_path).startswith(str(self.base_path)):
            raise ValueError("Caminho fora do diretório permitido")
        
        return full_path
    
    def list_files(self, directory: str = ".", pattern: str = "*") -> List[str]:
        """Lista arquivos em um diretório"""
        dir_path = self._validate_path(directory)
        
        if not dir_path.exists():
            return []
        
        files = []
        for file_path in dir_path.glob(pattern):
            relative_path = file_path.relative_to(self.base_path)
            files.append(str(relative_path))
        
        return sorted(files)
    
    def read_file(self, file_path: str) -> str:
        """Lê conteúdo de arquivo"""
        full_path = self._validate_path(file_path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        return full_path.read_text(encoding='utf-8')
    
    def write_file(self, file_path: str, content: str) -> str:
        """Escreve conteúdo em arquivo"""
        full_path = self._validate_path(file_path)
        
        # Cria diretórios se necessário
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        full_path.write_text(content, encoding='utf-8')
        return f"Arquivo salvo: {file_path}"
    
    def delete_file(self, file_path: str) -> str:
        """Remove arquivo"""
        full_path = self._validate_path(file_path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        full_path.unlink()
        return f"Arquivo removido: {file_path}"
```

## Model Context Protocol (MCP)

O **Model Context Protocol (MCP)** é uma abordagem padronizada para integrar ferramentas e contexto aos LLMs de forma consistente[^16].

### Benefícios do MCP

1. **Padronização**: Interface consistente para todas as ferramentas
2. **Flexibilidade**: Fácil adição/remoção de capabilities
3. **Observabilidade**: Rastreamento completo de interações
4. **Segurança**: Controle granular de permissões

### Implementação de MCP

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
from datetime import datetime

class MCPTool(ABC):
    """Interface base para ferramentas MCP"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        pass
    
    @property
    @abstractmethod
    def schema(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def execute(self, parameters: Dict[str, Any]) -> Any:
        pass

class MCPContextProvider(ABC):
    """Interface para provedores de contexto"""
    
    @abstractmethod
    def get_context(self, query: str) -> Dict[str, Any]:
        pass

class MCPClient:
    def __init__(self):
        self.tools: Dict[str, MCPTool] = {}
        self.context_providers: Dict[str, MCPContextProvider] = {}
        self.execution_log = []
    
    def register_tool(self, tool: MCPTool):
        self.tools[tool.name] = tool
    
    def register_context_provider(self, name: str, provider: MCPContextProvider):
        self.context_providers[name] = provider
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """Lista todas as ferramentas disponíveis"""
        return [
            {
                'name': tool.name,
                'description': tool.description,
                'schema': tool.schema
            }
            for tool in self.tools.values()
        ]
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Executa uma ferramenta específica"""
        if tool_name not in self.tools:
            raise ValueError(f"Ferramenta '{tool_name}' não encontrada")
        
        tool = self.tools[tool_name]
        
        # Log da execução
        execution_entry = {
            'tool': tool_name,
            'parameters': parameters,
            'timestamp': datetime.now(),
            'status': 'started'
        }
        
        try:
            result = tool.execute(parameters)
            execution_entry['status'] = 'completed'
            execution_entry['result'] = result
            return result
        
        except Exception as e:
            execution_entry['status'] = 'error'
            execution_entry['error'] = str(e)
            raise
        
        finally:
            self.execution_log.append(execution_entry)
    
    def gather_context(self, query: str) -> Dict[str, Any]:
        """Coleta contexto de todos os provedores"""
        context = {}
        
        for name, provider in self.context_providers.items():
            try:
                provider_context = provider.get_context(query)
                context[name] = provider_context
            except Exception as e:
                context[name] = {'error': str(e)}
        
        return context
    
    def execute_with_context(self, query: str, tools_to_use: List[str] = None) -> Dict[str, Any]:
        """Executa query com contexto completo"""
        # 1. Coleta contexto relevante
        context = self.gather_context(query)
        
        # 2. Identifica ferramentas necessárias (simplificado)
        if tools_to_use is None:
            tools_to_use = self._identify_tools(query)
        
        # 3. Executa ferramentas
        tool_results = {}
        for tool_name in tools_to_use:
            if tool_name in self.tools:
                try:
                    # Aqui você precisaria de lógica para extrair parâmetros do query
                    params = self._extract_parameters(query, tool_name)
                    result = self.execute_tool(tool_name, params)
                    tool_results[tool_name] = result
                except Exception as e:
                    tool_results[tool_name] = {'error': str(e)}
        
        return {
            'query': query,
            'context': context,
            'tool_results': tool_results,
            'timestamp': datetime.now()
        }
    
    def _identify_tools(self, query: str) -> List[str]:
        """Identifica ferramentas necessárias (implementação simplificada)"""
        # Em uma implementação real, isso usaria NLP ou LLM
        identified_tools = []
        
        query_lower = query.lower()
        for tool_name, tool in self.tools.items():
            # Busca por palavras-chave na descrição
            if any(word in query_lower for word in tool.description.lower().split()):
                identified_tools.append(tool_name)
        
        return identified_tools
    
    def _extract_parameters(self, query: str, tool_name: str) -> Dict[str, Any]:
        """Extrai parâmetros do query (implementação simplificada)"""
        # Em uma implementação real, isso usaria NLP ou LLM
        return {}
```

### Exemplo de Ferramentas MCP

```python
class WeatherMCPTool(MCPTool):
    def __init__(self, api_key: str):
        self.weather_tool = WeatherTool(api_key)
    
    @property
    def name(self) -> str:
        return "weather"
    
    @property
    def description(self) -> str:
        return "Obtém informações meteorológicas para uma cidade"
    
    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Nome da cidade"
                }
            },
            "required": ["city"]
        }
    
    def execute(self, parameters: Dict[str, Any]) -> str:
        city = parameters.get("city")
        if not city:
            raise ValueError("Parâmetro 'city' é obrigatório")
        
        return self.weather_tool.get_weather(city)

class DataAnalysisMCPTool(MCPTool):
    @property
    def name(self) -> str:
        return "data_analysis"
    
    @property
    def description(self) -> str:
        return "Executa análise de dados em arquivos CSV"
    
    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Caminho para o arquivo CSV"
                },
                "analysis_type": {
                    "type": "string",
                    "enum": ["descriptive", "correlation", "trend"],
                    "description": "Tipo de análise a executar"
                }
            },
            "required": ["file_path"]
        }
    
    def execute(self, parameters: Dict[str, Any]) -> str:
        tool = DataAnalysisTool()
        return tool.execute(parameters)
```

### Provedor de Contexto

```python
class MemoryContextProvider(MCPContextProvider):
    def __init__(self, memory_system):
        self.memory = memory_system
    
    def get_context(self, query: str) -> Dict[str, Any]:
        relevant_memories = self.memory.recall(query, k=5)
        
        return {
            'type': 'memory',
            'memories': relevant_memories,
            'total_memories': len(self.memory.memories)
        }

class UserPreferencesProvider(MCPContextProvider):
    def __init__(self, preferences: Dict[str, Any]):
        self.preferences = preferences
    
    def get_context(self, query: str) -> Dict[str, Any]:
        return {
            'type': 'user_preferences',
            'preferences': self.preferences
        }
```

## Segurança em Ferramentas

!!! warning "Práticas de Segurança"
    - **Validação de Inputs**: Sempre valide todos os parâmetros
    - **Rate Limiting**: Implemente limites de taxa de execução
    - **Sandboxing**: Use ambientes isolados quando possível
    - **Logging**: Monitore todas as execuções de ferramentas
    - **Princípio de Menor Privilégio**: Conceda apenas permissões necessárias

### Sistema de Permissões

```python
from enum import Enum
from typing import Set

class Permission(Enum):
    READ_FILES = "read_files"
    WRITE_FILES = "write_files"
    NETWORK_ACCESS = "network_access"
    DATABASE_ACCESS = "database_access"
    SYSTEM_COMMANDS = "system_commands"

class SecureMCPTool(MCPTool):
    def __init__(self):
        self.required_permissions: Set[Permission] = set()
    
    def add_permission(self, permission: Permission):
        self.required_permissions.add(permission)
    
    def check_permissions(self, granted_permissions: Set[Permission]) -> bool:
        return self.required_permissions.issubset(granted_permissions)

class SecureMCPClient(MCPClient):
    def __init__(self):
        super().__init__()
        self.granted_permissions: Set[Permission] = set()
        self.execution_limits = {
            'max_executions_per_minute': 60,
            'max_execution_time': 30  # segundos
        }
        self.execution_count = {}
    
    def grant_permission(self, permission: Permission):
        self.granted_permissions.add(permission)
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        if tool_name not in self.tools:
            raise ValueError(f"Ferramenta '{tool_name}' não encontrada")
        
        tool = self.tools[tool_name]
        
        # Verifica permissões
        if isinstance(tool, SecureMCPTool):
            if not tool.check_permissions(self.granted_permissions):
                missing = tool.required_permissions - self.granted_permissions
                raise PermissionError(f"Permissões faltantes: {missing}")
        
        # Verifica rate limiting
        current_time = datetime.now()
        minute_key = current_time.strftime("%Y-%m-%d %H:%M")
        
        if minute_key not in self.execution_count:
            self.execution_count[minute_key] = 0
        
        if self.execution_count[minute_key] >= self.execution_limits['max_executions_per_minute']:
            raise RuntimeError("Rate limit excedido")
        
        self.execution_count[minute_key] += 1
        
        # Executa com timeout
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Execução excedeu tempo limite")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.execution_limits['max_execution_time'])
        
        try:
            return super().execute_tool(tool_name, parameters)
        finally:
            signal.alarm(0)  # Cancela timeout
```

## Integração com Agentes

```python
class ToolAwareAgent:
    def __init__(self):
        self.mcp_client = MCPClient()
        self.memory = AgentMemory()
        
        # Registra ferramentas
        self._setup_tools()
    
    def _setup_tools(self):
        # Ferramentas básicas
        self.mcp_client.register_tool(WeatherMCPTool("api_key"))
        self.mcp_client.register_tool(DataAnalysisMCPTool())
        
        # Provedores de contexto
        self.mcp_client.register_context_provider(
            "memory", 
            MemoryContextProvider(self.memory)
        )
    
    def process_request(self, request: str) -> str:
        # 1. Analisa request e identifica ferramentas necessárias
        tools_needed = self._analyze_request(request)
        
        # 2. Executa com contexto
        result = self.mcp_client.execute_with_context(request, tools_needed)
        
        # 3. Gera resposta baseada nos resultados
        response = self._generate_response(request, result)
        
        # 4. Armazena na memória
        self.memory.store_interaction(request, response)
        
        return response
    
    def _analyze_request(self, request: str) -> List[str]:
        # Análise simplificada - em produção usaria LLM
        tools = []
        
        if "clima" in request.lower() or "tempo" in request.lower():
            tools.append("weather")
        
        if "dados" in request.lower() or "análise" in request.lower():
            tools.append("data_analysis")
        
        return tools
    
    def _generate_response(self, request: str, mcp_result: Dict[str, Any]) -> str:
        # Geração simplificada - em produção usaria LLM
        response_parts = []
        
        for tool_name, result in mcp_result.get('tool_results', {}).items():
            if isinstance(result, dict) and 'error' in result:
                response_parts.append(f"Erro na ferramenta {tool_name}: {result['error']}")
            else:
                response_parts.append(str(result))
        
        return "\n".join(response_parts) if response_parts else "Não foi possível processar a solicitação."
```

---

[^16]: [Building Effective AI Agents - Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
