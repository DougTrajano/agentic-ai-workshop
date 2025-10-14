# AI Agents vs. AI Workflows

Uma distinção fundamental na Agentic AI é entre **workflows** e **agents**.

Embora ambos utilizem LLMs como base, eles funcionam de maneiras muito diferentes e servem a propósitos distintos.[^1][^2][^3][^4]

![Workflows & agents - LangGraph Documentation](https://langchain-ai.github.io/langgraph/concepts/img/agent_workflow.png)
///Caption
[Workflows & agents - LangGraph Documentation](https://langchain-ai.github.io/langgraph/tutorials/workflows/)
///

## Workflows

**Workflows** são sistemas com fluxo de execução **predefinido e determinístico**. O LLM é usado em pontos específicos para tarefas bem definidas, mas o caminho geral de execução é conhecido antecipadamente.

**Características:**

- Fluxo de controle explícito e previsível
- Menor complexidade de implementação e depuração (debug)
- Mais confiáveis e fáceis de testar (fluxos restritos)
- Ideal para processos bem estruturados com etapas conhecidas

**Exemplo:** A geração de um dataset de RH sintético com base em etapas predefinidas. :sunglasses:

```mermaid
flowchart TD
    Start([User Input]) --> A[dataset_workflow]
    A --> B[get_company_spec<br/>LLM: gpt-4o]
    A --> C[get_demographic_ratios<br/>LLM: gpt-4o]
    B --> C
    A --> D[create_database]
    C --> D
    
    D --> E{For each<br/>Business Unit}
    E --> F[add_business_unit_to_db]
    F --> G[generate_employee<br/>Director]
    
    G --> H[get_education_fields<br/>LLM: gpt-5-nano]
    G --> I[get_employee_compensation<br/>LLM: gpt-5-nano]
    H --> J[add_employee_to_db]
    I --> J
    
    J --> K{For each<br/>Department}
    K --> L[add_department_to_db]
    L --> M[generate_department]
    
    M --> N[generate_employee<br/>Manager]
    N --> O[get_education_fields<br/>LLM: gpt-5-nano]
    N --> P[get_employee_compensation<br/>LLM: gpt-5-nano]
    O --> Q[add_employee_to_db]
    P --> Q
    
    Q --> R{For each<br/>Job/Employee}
    R --> S[generate_employee<br/>Staff]
    S --> T[get_education_fields<br/>LLM: gpt-5-nano]
    S --> U[get_employee_compensation<br/>LLM: gpt-5-nano]
    T --> V[add_employee_to_db]
    U --> V
    
    V --> R
    R --> K
    K --> E
    E --> End([Dataset Complete])
    
    style B fill:#ff9966,stroke:#333,stroke-width:2px
    style C fill:#ff9966,stroke:#333,stroke-width:2px
    style H fill:#ff9966,stroke:#333,stroke-width:2px
    style I fill:#ff9966,stroke:#333,stroke-width:2px
    style O fill:#ff9966,stroke:#333,stroke-width:2px
    style P fill:#ff9966,stroke:#333,stroke-width:2px
    style T fill:#ff9966,stroke:#333,stroke-width:2px
    style U fill:#ff9966,stroke:#333,stroke-width:2px
    
    style D fill:#6699ff,stroke:#333,stroke-width:2px
    style F fill:#6699ff,stroke:#333,stroke-width:2px
    style J fill:#6699ff,stroke:#333,stroke-width:2px
    style L fill:#6699ff,stroke:#333,stroke-width:2px
    style Q fill:#6699ff,stroke:#333,stroke-width:2px
    style V fill:#6699ff,stroke:#333,stroke-width:2px
    
    style G fill:#99ccff,stroke:#333,stroke-width:2px
    style M fill:#99ccff,stroke:#333,stroke-width:2px
    style N fill:#99ccff,stroke:#333,stroke-width:2px
    style S fill:#99ccff,stroke:#333,stroke-width:2px
```

## Agents

**Agentes** são sistemas **autônomos** onde o LLM decide dinamicamente quais ações tomar e em que ordem, baseado no **contexto (ambiente)** e nos **objetivos**.

![ReAct Agent Architecture](https://miro.medium.com/v2/resize:fit:1172/1*vNzirY9nRjWcYvhUD7sg7g.png)

**Características:**

- Tomada de decisão autônoma e adaptativa
- Capacidade de lidar com situações imprevistas
- Maior complexidade de implementação
- Podem ser menos previsíveis

**Exemplo:** Um assistente de análise de dados que:

1. Recebe uma pergunta do usuário
2. Decide autonomamente quais ferramentas usar (SQL, Python, visualização)
3. Ajusta sua estratégia baseado nos resultados intermediários
4. Iterativamente refina a resposta até atingir o objetivo

## Quando Usar Cada Um?

| Critério | Workflow | Agent |
|----------|----------|-------|
| **Processo** | Bem definido e estruturado | Aberto e exploratório |
| **Previsibilidade** | Alta (mesma sequência de passos) | Baixa (decisões dinâmicas) |
| **Complexidade** | Menor | Maior |
| **Manutenção** | Mais fácil | Mais desafiadora |
| **Casos de uso** | Pipelines de dados, automações, fluxos definidos | Tarefas complexas, objetivos dinâmicos |

## Máquina de estados finita

Ambos são frequentemente implementados como [**máquinas de estados finitas (FSM - Finite State Machines)**](https://pt.wikipedia.org/wiki/M%C3%A1quina_de_estados_finita), onde o sistema transita entre diferentes estados com base em entradas e condições definidas. A diferença está na rigidez do fluxo de controle: workflows têm transições fixas, enquanto agentes podem ter transições mais flexíveis e condicionais.

!!! tip "Combinando Workflows e Agentes"
    Na prática, muitos sistemas combinam ambas as abordagens: workflows para estruturar o processo geral e agentes para tarefas específicas que requerem autonomia.[^3]

---

[^1]: [Building Effective AI Agents - Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
[^2]: [Introduction to generative AI apps on Databricks - Databricks on AWS](https://docs.databricks.com/aws/en/generative-ai/guide/introduction-generative-ai-apps)
[^3]: [Workflows & agents - LangGraph Documentation](https://langchain-ai.github.io/langgraph/tutorials/workflows/)
[^4]: [Agents vs. Workflows - Hugging Face Blog](https://huggingface.co/blog/VirtualOasis/agents-vs-workflows-en)
