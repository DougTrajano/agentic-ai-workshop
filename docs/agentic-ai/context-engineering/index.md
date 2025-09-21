# Context Engineering: Construindo Sistemas Dinâmicos Eficazes

A arte de fornecer contexto relevante para os AI Agents no formato e na hora certa.

**Context Engineering** é a disciplina de construir sistemas dinâmicos que forneçam ao LLM a informação certa e as ferramentas certas no formato adequado para executar a tarefa[^21]. É uma evolução natural do prompt engineering focada em sistemas agentivos.

## 🎯 O que é Context Engineering?

Enquanto o **prompt engineering** foca em escrever bons prompts estáticos, o **context engineering** se concentra em:

- **Montagem dinâmica** de contexto relevante
- **Seleção adaptativa** de ferramentas e informações
- **Formatação otimizada** para diferentes tipos de tarefa
- **Gestão de memória** e estado do agente

!!! quote "LangChain sobre Context Engineering"
    "Quando sistemas agentivos falham, geralmente é por falta ou formatação ruim do contexto"[^22]

## 🏗️ Componentes do Context Engineering

### 1. Context Assembly (Montagem de Contexto)

A montagem de contexto envolve coletar e organizar informações relevantes de múltiplas fontes:

```python
class ContextAssembler:
    def __init__(self):
        self.sources = {
            'user_profile': UserProfileProvider(),
            'conversation_history': HistoryProvider(),
            'knowledge_base': RAGProvider(),
            'real_time_data': APIProvider(),
            'system_state': StateProvider()
        }
    
    def assemble_context(self, query: str, user_id: str) -> Dict[str, Any]:
        context = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'user': self.sources['user_profile'].get(user_id),
            'history': self.sources['conversation_history'].get_relevant(query),
            'knowledge': self.sources['knowledge_base'].retrieve(query),
            'current_data': self.sources['real_time_data'].fetch_relevant(query),
            'system': self.sources['system_state'].get_current()
        }
        
        return self._filter_and_rank(context)
```

### 2. Information Prioritization (Priorização de Informação)

Nem toda informação disponível é relevante para cada tarefa:

```python
class InformationPrioritizer:
    def __init__(self):
        self.relevance_scorer = RelevanceModel()
        self.context_budget = 8000  # tokens disponíveis
    
    def prioritize(self, query: str, context_items: List[ContextItem]) -> List[ContextItem]:
        # Score de relevância para cada item
        scored_items = []
        for item in context_items:
            score = self.relevance_scorer.score(query, item.content)
            scored_items.append((item, score))
        
        # Ordena por relevância
        scored_items.sort(key=lambda x: x[1], reverse=True)
        
        # Seleciona até o budget
        selected_items = []
        current_tokens = 0
        
        for item, score in scored_items:
            if current_tokens + item.token_count <= self.context_budget:
                selected_items.append(item)
                current_tokens += item.token_count
            else:
                break
        
        return selected_items
```

### 3. Context Formatting (Formatação de Contexto)

Diferentes tipos de informação requerem formatação específica:

```python
class ContextFormatter:
    def format_for_task(self, context: Dict[str, Any], task_type: str) -> str:
        if task_type == "data_analysis":
            return self._format_for_analysis(context)
        elif task_type == "conversation":
            return self._format_for_chat(context)
        elif task_type == "code_generation":
            return self._format_for_coding(context)
        
        return self._format_generic(context)
    
    def _format_for_analysis(self, context: Dict[str, Any]) -> str:
        formatted = f"""
ANÁLISE DE DADOS - CONTEXTO

Dados Disponíveis:
{self._format_data_sources(context['data_sources'])}

Histórico de Análises:
{self._format_previous_analyses(context['history'])}

Ferramentas Disponíveis:
{self._format_tools(context['available_tools'])}

Objetivo: {context['objective']}
"""
        return formatted
```

## 🔄 Padrões de Context Engineering

### 1. Progressive Context Building

Construção incremental do contexto conforme a tarefa evolui:

```python
class ProgressiveContextBuilder:
    def __init__(self):
        self.context_layers = []
    
    def add_layer(self, layer_name: str, content: Any):
        self.context_layers.append({
            'name': layer_name,
            'content': content,
            'timestamp': datetime.now()
        })
    
    def build_context_for_step(self, step: str) -> str:
        relevant_layers = self._get_relevant_layers(step)
        return self._format_layers(relevant_layers)
    
    def _get_relevant_layers(self, step: str) -> List[Dict]:
        # Lógica para determinar quais camadas são relevantes
        # para o passo atual
        pass
```

### 2. Context Compression

Quando o contexto excede limites, use técnicas de compressão:

```python
class ContextCompressor:
    def __init__(self, summarizer_model):
        self.summarizer = summarizer_model
    
    def compress_context(self, context: str, target_length: int) -> str:
        if len(context) <= target_length:
            return context
        
        # Identifica seções comprimíveis
        sections = self._identify_sections(context)
        
        # Comprime seções menos críticas
        compressed_sections = []
        for section in sections:
            if section['importance'] < 0.7:
                compressed = self.summarizer.summarize(
                    section['content'], 
                    max_length=section['length'] // 3
                )
                compressed_sections.append(compressed)
            else:
                compressed_sections.append(section['content'])
        
        return '\n'.join(compressed_sections)
```

### 3. Dynamic Tool Selection

Seleção adaptativa de ferramentas baseada no contexto:

```python
class DynamicToolSelector:
    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.capability_matcher = CapabilityMatcher()
    
    def select_tools(self, query: str, context: Dict) -> List[Tool]:
        # Analisa requirements da tarefa
        requirements = self._analyze_requirements(query, context)
        
        # Encontra ferramentas que atendem requirements
        candidate_tools = []
        for tool in self.tool_registry.get_all():
            compatibility = self.capability_matcher.match(
                requirements, tool.capabilities
            )
            if compatibility > 0.5:
                candidate_tools.append((tool, compatibility))
        
        # Ordena por compatibilidade e retorna top-K
        candidate_tools.sort(key=lambda x: x[1], reverse=True)
        return [tool for tool, _ in candidate_tools[:5]]
```

## 📊 Context Engineering para Diferentes Domínios

### Data Analytics Context

```python
def build_analytics_context(query: str, datasets: List[str]) -> str:
    context = f"""
CONTEXTO DE ANÁLISE DE DADOS

Query do Usuário: {query}

Datasets Disponíveis:
"""
    
    for dataset in datasets:
        schema_info = get_dataset_schema(dataset)
        sample_data = get_sample_data(dataset, n=3)
        
        context += f"""
- {dataset}
  Schema: {schema_info}
  Sample: {sample_data}
"""
    
    context += f"""
Ferramentas Analíticas:
- pandas: Manipulação de dados
- matplotlib/seaborn: Visualização
- scipy: Análise estatística
- sklearn: Machine learning

Instruções:
1. Sempre valide a qualidade dos dados
2. Forneça interpretações dos resultados
3. Sugira próximos passos quando apropriado
"""
    
    return context
```

### Customer Support Context

```python
def build_support_context(customer_id: str, issue: str) -> str:
    customer = get_customer_profile(customer_id)
    history = get_support_history(customer_id)
    knowledge = search_knowledge_base(issue)
    
    context = f"""
CONTEXTO DE SUPORTE AO CLIENTE

Cliente: {customer['name']} (ID: {customer_id})
Plano: {customer['plan']}
Status: {customer['status']}

Histórico Recente:
{format_support_history(history)}

Base de Conhecimento Relevante:
{format_knowledge_articles(knowledge)}

Issue Atual: {issue}

Diretrizes:
- Seja empático e profissional
- Foque em soluções práticas
- Escale para humano se necessário
"""
    
    return context
```

### Code Generation Context

```python
def build_coding_context(task: str, codebase_info: Dict) -> str:
    context = f"""
CONTEXTO DE GERAÇÃO DE CÓDIGO

Tarefa: {task}

Codebase Info:
- Linguagem: {codebase_info['language']}
- Framework: {codebase_info['framework']}
- Estrutura: {codebase_info['structure']}

Padrões de Código:
{format_code_patterns(codebase_info['patterns'])}

Dependências Disponíveis:
{format_dependencies(codebase_info['dependencies'])}

Instruções:
1. Siga os padrões estabelecidos
2. Inclua tratamento de erros
3. Adicione documentação apropriada
4. Considere performance e segurança
"""
    
    return context
```

## 🎛️ Context Engineering Avançado

### 1. Multi-Agent Context Sharing

Em sistemas multi-agente, o contexto precisa ser compartilhado eficientemente:

```python
class SharedContextManager:
    def __init__(self):
        self.shared_context = {}
        self.agent_contexts = {}
    
    def update_shared_context(self, key: str, value: Any, source_agent: str):
        self.shared_context[key] = {
            'value': value,
            'source': source_agent,
            'timestamp': datetime.now()
        }
        
        # Notifica outros agentes sobre atualização
        self._notify_agents(key, source_agent)
    
    def get_context_for_agent(self, agent_id: str) -> Dict:
        # Combina contexto compartilhado com contexto específico do agente
        context = self.shared_context.copy()
        context.update(self.agent_contexts.get(agent_id, {}))
        return context
```

### 2. Context Versioning

Manter versões do contexto para debugging e rollback:

```python
class VersionedContext:
    def __init__(self):
        self.versions = []
        self.current_version = 0
    
    def update_context(self, updates: Dict) -> int:
        new_context = self.get_current_context().copy()
        new_context.update(updates)
        
        self.versions.append({
            'context': new_context,
            'timestamp': datetime.now(),
            'changes': updates
        })
        
        self.current_version = len(self.versions) - 1
        return self.current_version
    
    def rollback_to_version(self, version: int):
        if 0 <= version < len(self.versions):
            self.current_version = version
```

### 3. Context Quality Metrics

Métricas para avaliar a qualidade do contexto:

```python
class ContextQualityMetrics:
    def evaluate_context(self, context: str, query: str) -> Dict[str, float]:
        return {
            'relevance': self._calculate_relevance(context, query),
            'completeness': self._calculate_completeness(context, query),
            'conciseness': self._calculate_conciseness(context),
            'freshness': self._calculate_freshness(context),
            'consistency': self._calculate_consistency(context)
        }
    
    def _calculate_relevance(self, context: str, query: str) -> float:
        # Usa embeddings para calcular similaridade semântica
        context_embedding = self.encoder.encode(context)
        query_embedding = self.encoder.encode(query)
        similarity = cosine_similarity([context_embedding], [query_embedding])[0][0]
        return float(similarity)
```

## 🚀 Boas Práticas para Context Engineering

### 1. Context Budget Management

```python
class ContextBudgetManager:
    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self.token_counter = TokenCounter()
    
    def allocate_budget(self, components: Dict[str, int]) -> Dict[str, int]:
        total_requested = sum(components.values())
        
        if total_requested <= self.max_tokens:
            return components
        
        # Proporcional allocation se exceder budget
        ratio = self.max_tokens / total_requested
        return {k: int(v * ratio) for k, v in components.items()}
```

### 2. Context Caching

```python
class ContextCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get_or_build(self, cache_key: str, builder_func: Callable) -> Any:
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if datetime.now() - entry['timestamp'] < timedelta(seconds=self.ttl):
                return entry['context']
        
        # Rebuild context
        context = builder_func()
        self.cache[cache_key] = {
            'context': context,
            'timestamp': datetime.now()
        }
        
        return context
```

### 3. Context Validation

```python
class ContextValidator:
    def validate_context(self, context: str) -> List[str]:
        issues = []
        
        # Verifica tamanho
        if len(context) > 10000:
            issues.append("Context muito longo")
        
        # Verifica informações pessoais
        if self._contains_pii(context):
            issues.append("Context contém informações pessoais")
        
        # Verifica qualidade
        if self._calculate_quality_score(context) < 0.7:
            issues.append("Context com qualidade baixa")
        
        return issues
```

## 📈 Medição e Otimização

### Métricas Importantes

1. **Context Relevance Score**: Quão relevante é o contexto para a tarefa
2. **Token Efficiency**: Razão de tokens úteis vs total
3. **Context Build Time**: Tempo para montar o contexto
4. **Agent Performance**: Performance do agente com diferentes contextos

### A/B Testing para Context

```python
class ContextABTester:
    def __init__(self):
        self.experiments = {}
    
    def create_experiment(self, experiment_name: str, variants: List[str]):
        self.experiments[experiment_name] = {
            'variants': variants,
            'results': {variant: [] for variant in variants}
        }
    
    def log_result(self, experiment: str, variant: str, success: bool, metrics: Dict):
        self.experiments[experiment]['results'][variant].append({
            'success': success,
            'metrics': metrics,
            'timestamp': datetime.now()
        })
```

## Próximos Passos

Agora que você domina Context Engineering, vamos explorar:

1. **[Observabilidade](observability/index.md)**: Monitoramento detalhado de sistemas agentivos
2. **[Workshop Prático](../workshop/index.md)**: Implementação hands-on de todos os conceitos

---

[^21]: [The rise of "context engineering" - LangChain](https://blog.langchain.com/the-rise-of-context-engineering/)
[^22]: [The rise of "context engineering" - LangChain](https://blog.langchain.com/the-rise-of-context-engineering/)
