## Workflows vs. Agentes

Uma distinção fundamental na Agentic AI é entre **workflows** e **agentes**[^10]:

### 📋 Workflows

- Orquestram chamadas a LLMs e ferramentas por **caminhos pré-definidos**
- Sequência determinística de passos
- Controle explícito do fluxo de execução
- Ideal para tarefas bem definidas e previsíveis

### 🤖 Agentes

- Sistemas onde o **LLM dirige dinamicamente** seu processo
- Tomada de decisão autônoma sobre próximos passos
- Uso adaptativo de ferramentas
- Ideal para tarefas abertas e complexas

!!! tip "Quando usar cada abordagem?"

    **Use Workflows quando:**
    - A tarefa tem passos bem definidos
    - O fluxo é previsível
    - Você precisa de controle determinístico

    **Use Agentes quando:**
    - A tarefa é aberta e exploratória
    - Múltiplos caminhos são possíveis
    - Adaptação dinâmica é necessária

## Componentes de um Agente de IA

A base de um agente de IA moderno normalmente envolve vários componentes principais:

### 🧠 Large Language Models (LLMs)

Serve como o "cérebro" do agente, fornecendo a capacidade de compreender, raciocinar e agir. Os LLMs processam e geram linguagem, habilitando as funções cognitivas do agente.

### 🛠️ Tools (Ferramentas)

São funções externas, APIs ou recursos que o agente pode acessar e utilizar para interagir com seu ambiente e aprimorar suas capacidades. As ferramentas permitem que os agentes executem tarefas específicas além da geração de texto.

### 📋 Instructions (Instruções)

Diretrizes explícitas, geralmente fornecidas por meio de um prompt do sistema, definem como o agente deve se comportar e orientar suas ações.

### 💭 Memory (Memória)

Os agentes podem possuir várias formas de memória:

- **Memória de curto prazo**: contexto da conversa atual
- **Memória de longo prazo**: interações históricas passadas

### ⚙️ Runtime/Orchestration Layer

Ambiente que permite que o agente ou o LLM controle seu fluxo de execução, decida quando usar ferramentas e processe observações.

## Padrões de Agentes Eficazes

Estudos da Anthropic mostram que sistemas de agentes eficazes usam **padrões simples e compostos**, não frameworks excessivamente complexos[^11].

### Bloco de Construção Básico

O bloco fundamental é um LLM "aumentado" com[^12]:

1. **🔍 Recuperação de Informação**: Acesso a bases de conhecimento
2. **🛠️ Ferramentas**: APIs e funções especializadas
3. **🧠 Memória**: Contexto de curto e longo prazo

### Capacidades Essenciais

- **Geração de consultas próprias**: O agente formula suas próprias perguntas
- **Seleção de ferramentas**: Escolha adaptativa de recursos
- **Gerenciamento de memória**: Decisão sobre o que manter/descartar

## Próximos Passos

Agora que você entende os fundamentos, vamos explorar:

1. **[Técnicas de Prompt Engineering](prompt-engineering.md)**: Como comunicar efetivamente com LLMs
2. **Construção de Agentes**: Implementação prática de sistemas agentivos
3. **Context Engineering**: Otimização do contexto para agentes eficazes

---

[^10]: [Building Effective AI Agents - Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
[^11]: [Building Effective AI Agents - Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
[^12]: [Building Effective AI Agents - Anthropic](https://www.anthropic.com/engineering/building-effective-agents)