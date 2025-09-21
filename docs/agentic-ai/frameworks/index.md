# Frameworks de Agentes de IA

Para acelerar o desenvolvimento de sistemas agentivos, existem diversos frameworks que fornecem abstrações e ferramentas prontas. Esta seção explora as principais opções disponíveis atualmente.

## 📚 Frameworks Disponíveis

### 🔗 [LangGraph (LangChain)](langgraph.md)

Framework de baixo nível para orquestrar agentes e workflows complexos, ideal para aplicações que requerem controle fino sobre o fluxo de execução.

### 📚 [LlamaIndex](llamaindex.md)

Biblioteca especializada em ingestão de dados e RAG, facilitando a integração de LLMs com bases de conhecimento.

### 🐍 [SmolAgents (Hugging Face)](smolagents.md)

Biblioteca minimalista para agentes que "pensam em código", oferecendo uma abordagem mais programática.

### 🔧 [Pydantic AI](pydantic-ai.md)

Framework que facilita a criação de agentes Python tipados com observabilidade nativa.

### 🧩 [Outras Opções](other-frameworks.md)

Explore outras alternativas como Crew AI, AutoGen e Haystack.

## 🎯 [Comparação e Escolha](index.md)

Guia para escolher o framework ideal baseado em suas necessidades específicas, incluindo comparações detalhadas e padrões de arquitetura.

## 🚀 Escolhendo o Framework Ideal

### Para Iniciantes

- **SmolAgents**: Simplicidade e transparência
- **LlamaIndex**: Se o foco for RAG

### Para Produção

- **LangGraph**: Controle total e observabilidade
- **Pydantic AI**: Type safety e estrutura

### Para Pesquisa

- **SmolAgents**: Experimentação rápida
- **LangGraph**: Workflows experimentais

### Para Aplicações Específicas

- **RAG**: LlamaIndex
- **Multi-agente**: Crew AI ou AutoGen
- **Code generation**: SmolAgents

## 🔧 Integração e Observabilidade

Independente do framework escolhido, considere:

### Logging e Monitoramento

- **Logs estruturados** para todas as execuções
- **Métricas de performance** (latência, tokens, custos)
- **Alertas** para falhas ou comportamentos anômalos

### Testing

- **Unit tests** para componentes individuais
- **Integration tests** para fluxos completos
- **A/B testing** para diferentes versões de agentes

### Deployment

- **Containerização** para consistência
- **Auto-scaling** baseado em demanda
- **Blue-green deployment** para atualizações sem downtime

## Próximos Passos

Agora que você conhece os principais frameworks, vamos explorar:

1. **[Context Engineering](../context-engineering.md)**: Como otimizar o contexto para seus agentes
2. **[Observabilidade](../observability/index.md)**: Monitoramento e debugging detalhado
3. **[Workshop Prático](../../workshop/index.md)**: Implementação hands-on
