# 🧩 Outras Opções de Frameworks

Além dos frameworks principais, existem várias outras opções especializadas para diferentes casos de uso.

## Crew AI

Framework para coordenar múltiplos agentes especializados trabalhando em equipe.

```python
from crewai import Agent, Task, Crew

# Define agentes especializados
researcher = Agent(
    role='Pesquisador',
    goal='Coletar informações relevantes',
    backstory='Especialista em pesquisa...'
)

analyst = Agent(
    role='Analista',
    goal='Analisar dados coletados',
    backstory='Especialista em análise...'
)

# Define tarefas
research_task = Task(
    description='Pesquisar sobre agentic AI',
    agent=researcher
)

analysis_task = Task(
    description='Analisar informações coletadas',
    agent=analyst
)

# Coordena trabalho em equipe
crew = Crew(
    agents=[researcher, analyst],
    tasks=[research_task, analysis_task]
)
```

### Quando usar Crew AI

- **Multi-agent workflows**: Quando você precisa de agentes especializados
- **Colaboração**: Tarefas que se beneficiam de diferentes perspectivas
- **Role-playing**: Simulação de equipes com papéis específicos

## AutoGen (Microsoft)

Framework para conversas multi-agente com diferentes papéis.

```python
from autogen import AssistantAgent, UserProxyAgent

# Agente assistente
assistant = AssistantAgent(
    name="assistant",
    system_message="Você é um assistente útil.",
    llm_config={"model": "gpt-4"}
)

# Agente proxy do usuário
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding"}
)

# Inicia conversa
user_proxy.initiate_chat(
    assistant,
    message="Analise dados de vendas e crie um relatório"
)
```

### Quando usar AutoGen

- **Conversas estruturadas**: Diálogos entre agentes
- **Code execution**: Quando precisa executar código gerado
- **Iterative refinement**: Melhorias iterativas através de feedback

## Haystack

Plataforma para construir aplicações de busca e QA com LLMs.

```python
from haystack import Pipeline
from haystack.components.retrievers import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator

# Pipeline de RAG
pipeline = Pipeline()
pipeline.add_component("retriever", InMemoryBM25Retriever(document_store))
pipeline.add_component("generator", OpenAIGenerator(model="gpt-4"))

pipeline.connect("retriever", "generator")

# Executa pipeline
result = pipeline.run({
    "retriever": {"query": "Como implementar RAG?"},
    "generator": {"prompt": "Responda baseado no contexto: {documents}"}
})
```

### Quando usar Haystack

- **Search applications**: Aplicações focadas em busca
- **Document QA**: Sistemas de perguntas e respostas
- **Pipeline flexibility**: Necessidade de pipelines customizáveis

## Comparação Rápida

| Framework | Foco Principal | Complexidade | Ideal Para |
|-----------|----------------|--------------|------------|
| **Crew AI** | Multi-agent teams | Média | Colaboração entre agentes |
| **AutoGen** | Agent conversations | Média | Diálogos estruturados |
| **Haystack** | Search & QA | Alta | Aplicações de busca |
