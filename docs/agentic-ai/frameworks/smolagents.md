# 🐍 SmolAgents (Hugging Face)

O **SmolAgents** é uma biblioteca minimalista da Hugging Face lançada em dezembro de 2024 para agentes que "pensam em código", oferecendo uma abordagem programática com apenas ~1.000 linhas de código core.

## 🚀 Principais Características

- **Code-based reasoning**: Agentes geram e executam código Python diretamente
- **Ultra-lightweight**: Apenas ~1.000 linhas de código no arquivo principal
- **Tool integration**: Integração nativa com Hugging Face Hub e tools
- **Model agnostic**: Suporte para 40+ LLMs via LiteLLM
- **Transparent**: Abordagem minimalista e fácil de entender
- **Hub integration**: Compartilhamento de tools no Hugging Face Hub

## 📦 Instalação

```bash
pip install smolagents huggingface_hub transformers

# Para usar modelos do Hugging Face
pip install smolagents[hf]

# Para usar OpenAI e outros providers
pip install smolagents[openai]
```

## 💡 Exemplo Básico

```python
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

# Configurar com modelo do HuggingFace (gratuito)
agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()], 
    model=HfApiModel()
)

# Execução direta
result = agent.run(
    "Pesquise sobre 'agentic AI' e me dê um resumo das principais tendências"
)
print(result)
```

## 🔧 Code Agents em Ação

```python
from smolagents import CodeAgent, PythonInterpreterTool, DuckDuckGoSearchTool

# Agente com múltiplas ferramentas
tools = [
    DuckDuckGoSearchTool(),
    PythonInterpreterTool()
]

agent = CodeAgent(
    tools=tools,
    model="openai:gpt-4",  # ou usar HfApiModel() para gratuito
    add_base_tools=True
)

# Tarefa complexa que requer código
result = agent.run("""
Pesquise dados sobre o mercado de IA em 2024, 
crie um DataFrame com os principais insights e 
gere um gráfico de barras mostrando o crescimento por setor
""")

# O agente irá:
# 1. Usar DuckDuckGoSearchTool para pesquisar
# 2. Gerar código Python para processar dados  
# 3. Criar DataFrame e gráfico usando matplotlib
# 4. Executar código e retornar resultados

## Ferramentas Customizadas

```python
from smolagents import Tool
import pandas as pd

class DataAnalysisTool(Tool):
    name = "data_analysis"
    description = "Analisa dados CSV e retorna insights estatísticos"
    inputs = {
        "file_path": {"type": "string", "description": "Caminho para arquivo CSV"},
        "analysis_type": {"type": "string", "description": "Tipo de análise: 'summary', 'correlation', 'distribution'"}
    }
    output_type = "string"

    def forward(self, file_path: str, analysis_type: str = "summary"):
        """Executa análise de dados"""
        try:
            df = pd.read_csv(file_path)
            
            if analysis_type == "summary":
                return str(df.describe())
            elif analysis_type == "correlation":
                return str(df.corr())
            elif analysis_type == "distribution":
                return str(df.dtypes.value_counts())
            else:
                return "Tipo de análise não suportado"
        
        except Exception as e:
            return f"Erro na análise: {str(e)}"

# Registra ferramenta customizada
agent = CodeAgent(
    tools=[DataAnalysisTool(), PythonInterpreterTool()],
    model="gpt-4"
)
```

## Agente Multi-Step

```python
class MultiStepAgent(CodeAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execution_history = []
    
    def run_with_steps(self, task: str):
        """Executa tarefa com log detalhado de cada passo"""
        print(f"🎯 Iniciando tarefa: {task}")
        
        # Planeja os passos
        planning_prompt = f"""
        Analise a tarefa: "{task}"
        Liste os principais passos necessários para completá-la.
        Seja específico sobre que código Python será necessário.
        """
        
        plan = self.llm_engine(planning_prompt)
        print(f"📋 Plano:\n{plan}")
        
        # Executa a tarefa
        result = self.run(task)
        
        # Armazena histórico
        self.execution_history.append({
            "task": task,
            "plan": plan,
            "result": result,
            "timestamp": datetime.now()
        })
        
        return result

# Uso do agente multi-step
agent = MultiStepAgent(
    tools=[PythonInterpreterTool(), DuckDuckGoSearchTool()],
    model="gpt-4"
)

result = agent.run_with_steps(
    "Analise dados de vendas, identifique tendências e crie visualizações"
)
```

## Ferramentas de Sistema

```python
class FileSystemTool(Tool):
    name = "file_operations"
    description = "Operações seguras com sistema de arquivos"
    inputs = {
        "operation": {"type": "string", "description": "Operação: 'read', 'write', 'list'"},
        "path": {"type": "string", "description": "Caminho do arquivo/diretório"},
        "content": {"type": "string", "description": "Conteúdo (para write)"}
    }
    output_type = "string"

    def forward(self, operation: str, path: str, content: str = None):
        """Executa operações do sistema de arquivos"""
        import os
        from pathlib import Path
        
        # Validação de segurança
        safe_path = Path(path).resolve()
        if not str(safe_path).startswith(os.getcwd()):
            return "Erro: Acesso fora do diretório atual não permitido"
        
        try:
            if operation == "read":
                return safe_path.read_text()
            elif operation == "write":
                safe_path.write_text(content or "")
                return f"Arquivo {path} escrito com sucesso"
            elif operation == "list":
                if safe_path.is_dir():
                    files = [f.name for f in safe_path.iterdir()]
                    return f"Arquivos em {path}: {files}"
                else:
                    return f"{path} não é um diretório"
            else:
                return "Operação não suportada"
        
        except Exception as e:
            return f"Erro: {str(e)}"

class APICallTool(Tool):
    name = "api_request"
    description = "Faz requisições HTTP para APIs"
    inputs = {
        "url": {"type": "string", "description": "URL da API"},
        "method": {"type": "string", "description": "Método HTTP (GET, POST, etc.)"},
        "headers": {"type": "dict", "description": "Headers da requisição"},
        "data": {"type": "dict", "description": "Dados da requisição"}
    }
    output_type = "string"

    def forward(self, url: str, method: str = "GET", headers: dict = None, data: dict = None):
        """Faz requisição HTTP"""
        import requests
        
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers or {},
                json=data
            )
            response.raise_for_status()
            return str(response.json())
        
        except Exception as e:
            return f"Erro na requisição: {str(e)}"
```

## Debugging e Logging

```python
class DebuggableAgent(CodeAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug_mode = kwargs.get('debug', False)
        self.execution_trace = []
    
    def run(self, task: str, **kwargs):
        """Executa com debugging detalhado"""
        if self.debug_mode:
            print(f"🐛 DEBUG: Iniciando tarefa: {task}")
        
        # Hook para capturar execuções de código
        original_python_tool = None
        for tool in self.tools:
            if isinstance(tool, PythonInterpreterTool):
                original_python_tool = tool
                break
        
        if original_python_tool and self.debug_mode:
            # Wrapper para logging
            original_forward = original_python_tool.forward
            
            def debug_forward(code: str):
                print(f"🐍 Executando código:\n{code}")
                result = original_forward(code)
                print(f"📤 Resultado: {result}")
                
                self.execution_trace.append({
                    "code": code,
                    "result": result,
                    "timestamp": datetime.now()
                })
                
                return result
            
            original_python_tool.forward = debug_forward
        
        # Executa tarefa
        result = super().run(task, **kwargs)
        
        if self.debug_mode:
            print(f"✅ Tarefa concluída. Trace disponível em .execution_trace")
        
        return result

# Uso com debugging
debug_agent = DebuggableAgent(
    tools=[PythonInterpreterTool(), DataAnalysisTool()],
    model="gpt-4",
    debug=True
)
```

## Integração com Jupyter

```python
class JupyterAgent(CodeAgent):
    """Agente otimizado para uso em Jupyter Notebooks"""
    
    def run_interactive(self, task: str):
        """Execução interativa com feedback"""
        from IPython.display import display, Markdown, Code
        
        display(Markdown(f"### 🎯 Tarefa: {task}"))
        
        # Planeja
        planning_prompt = f"Analise e planeje: {task}"
        plan = self.llm_engine(planning_prompt)
        
        display(Markdown("### 📋 Plano:"))
        display(Markdown(plan))
        
        # Pergunta se deve continuar
        user_input = input("Continuar com a execução? (s/n): ")
        if user_input.lower() != 's':
            return "Execução cancelada pelo usuário"
        
        # Executa
        result = self.run(task)
        
        display(Markdown("### ✅ Resultado:"))
        display(Markdown(f"```\n{result}\n```"))
        
        return result

# Uso em Jupyter
jupyter_agent = JupyterAgent(
    tools=[PythonInterpreterTool()],
    model="gpt-4"
)

# jupyter_agent.run_interactive("Analise dados de vendas")
```

## Quando Usar SmolAgents

### ✅ Ideal para

- Tarefas que se beneficiam de geração de código
- Análise de dados e visualização
- Prototipagem rápida
- Casos que requerem transparência total
- Automação de tarefas programáticas

### ❌ Não ideal para

- Aplicações que não podem executar código arbitrário
- Ambientes com restrições de segurança rigorosas
- Casos que requerem interfaces conversacionais complexas
- Sistemas que precisam de workflows state-based

## Melhores Práticas

### 1. Segurança

```python
# Sempre valide entradas
def safe_code_execution(code: str) -> str:
    # Lista de operações perigosas
    dangerous_patterns = [
        'import os',
        'subprocess',
        'eval(',
        'exec(',
        '__import__'
    ]
    
    for pattern in dangerous_patterns:
        if pattern in code:
            return f"Código rejeitado: contém '{pattern}'"
    
    # Execute apenas se seguro
    return execute_code(code)
```

### 2. Monitoramento

```python
class MonitoredAgent(CodeAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'total_runtime': 0
        }
    
    def run(self, task: str, **kwargs):
        start_time = time.time()
        self.metrics['total_executions'] += 1
        
        try:
            result = super().run(task, **kwargs)
            self.metrics['successful_executions'] += 1
            return result
        except Exception as e:
            self.metrics['failed_executions'] += 1
            raise
        finally:
            self.metrics['total_runtime'] += time.time() - start_time
    
    def get_performance_report(self):
        success_rate = (self.metrics['successful_executions'] / 
                       self.metrics['total_executions'] * 100)
        avg_runtime = (self.metrics['total_runtime'] / 
                      self.metrics['total_executions'])
        
        return f"""
        Performance Report:
        - Execuções totais: {self.metrics['total_executions']}
        - Taxa de sucesso: {success_rate:.1f}%
        - Tempo médio: {avg_runtime:.2f}s
        """
```

## Pr ximos Passos

- **[Pydantic AI](pydantic-ai.md)**: Explore frameworks type-safe
- **[Outras Op   ](other-frameworks.md)**: Descubra mais alternativas
- **[Compara   ](index.md)**: Compare diferentes frameworks
