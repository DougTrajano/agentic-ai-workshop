# 🧠 Memória em Agentes de IA

A **memória** é um dos componentes mais críticos de um agente de IA, permitindo que ele mantenha contexto e aprenda com interações passadas.

## Tipos de Memória

### Memória de Curto Prazo

- **Contexto da conversa atual**
- **Estado da sessão**
- **Resultados de ferramentas recentes**
- **Planos intermediários**

!!! example "Exemplo"
    Em uma conversa sobre análise de dados, o agente lembra que você mencionou trabalhar com dados de vendas do último trimestre.

### Memória de Longo Prazo

- **Preferências do usuário**
- **Histórico de interações**
- **Conhecimento acumulado**
- **Padrões identificados**

!!! example "Exemplo"
    O agente lembra que você sempre prefere gráficos em formato SVG e relatórios em português.

## Implementação de Memória

```python
class AgentMemory:
    def __init__(self):
        self.short_term = {}  # Sessão atual
        self.long_term = {}   # Persistente
        self.working_memory = []  # Buffer de trabalho
    
    def store_short_term(self, key, value):
        self.short_term[key] = value
    
    def store_long_term(self, key, value):
        # Persiste em banco de dados
        self.long_term[key] = value
    
    def recall(self, query):
        # Busca relevante em ambas as memórias
        pass
```

## Estratégias de Implementação

### 1. Memória Baseada em Vetores

```python
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorMemory:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.memories = []
        self.embeddings = []
    
    def store(self, memory_text, metadata=None):
        embedding = self.encoder.encode([memory_text])[0]
        self.memories.append({
            'text': memory_text,
            'metadata': metadata or {},
            'timestamp': time.time()
        })
        self.embeddings.append(embedding)
    
    def recall(self, query, k=5):
        query_embedding = self.encoder.encode([query])[0]
        
        # Calcula similaridade
        similarities = []
        for emb in self.embeddings:
            sim = np.dot(query_embedding, emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(emb)
            )
            similarities.append(sim)
        
        # Retorna top-k mais similares
        top_indices = np.argsort(similarities)[-k:][::-1]
        return [self.memories[i] for i in top_indices]
```

### 2. Memória Hierárquica

```python
class HierarchicalMemory:
    def __init__(self):
        self.episodic = []      # Eventos específicos
        self.semantic = {}      # Conhecimento geral
        self.procedural = {}    # Como fazer coisas
    
    def store_episode(self, event):
        self.episodic.append({
            'event': event,
            'timestamp': time.time(),
            'context': self._get_current_context()
        })
    
    def store_semantic(self, concept, information):
        if concept not in self.semantic:
            self.semantic[concept] = []
        self.semantic[concept].append(information)
    
    def store_procedure(self, task, steps):
        self.procedural[task] = steps
```

## Boas Práticas para Memória

### 1. Gestão de Capacidade

- Implemente estratégias de esquecimento (não armazene tudo)
- Use índices eficientes para busca rápida
- Considere políticas de retenção baseadas em relevância

### 2. Privacidade e Segurança

- Considere regulamentações como LGPD
- Implemente anonização quando necessário
- Use criptografia para dados sensíveis

### 3. Otimização de Performance

- Cache memórias frequentemente acessadas
- Use índices apropriados para busca
- Considere compressão para grandes volumes

!!! tip "Dica"
    A memória eficaz é um equilíbrio entre relevância, capacidade e performance. Nem tudo precisa ser lembrado para sempre.

## Padrões de Memória

### Sliding Window

Mantém apenas os N elementos mais recentes:

```python
class SlidingWindowMemory:
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.memories = deque(maxlen=window_size)
    
    def store(self, memory):
        self.memories.append(memory)
```

### Frequency-Based

Mantém memórias baseadas na frequência de acesso:

```python
class FrequencyMemory:
    def __init__(self):
        self.memories = {}
        self.access_count = {}
    
    def recall(self, key):
        self.access_count[key] = self.access_count.get(key, 0) + 1
        return self.memories.get(key)
    
    def cleanup(self, threshold=5):
        # Remove memórias pouco acessadas
        to_remove = [k for k, v in self.access_count.items() if v < threshold]
        for key in to_remove:
            del self.memories[key]
            del self.access_count[key]
```

## Integração com RAG

A memória pode ser integrada com sistemas RAG para fornecer contexto histórico:

```python
class MemoryRAGSystem:
    def __init__(self):
        self.memory = VectorMemory()
        self.knowledge_base = RAGSystem()
    
    def query_with_memory(self, query):
        # 1. Busca na memória pessoal
        relevant_memories = self.memory.recall(query)
        
        # 2. Busca na base de conhecimento
        relevant_docs = self.knowledge_base.retrieve(query)
        
        # 3. Combina contextos
        context = self._combine_contexts(relevant_memories, relevant_docs)
        
        return context
```

## Próximos Passos

- **[RAG (Retrieval-Augmented Generation)](rag.md)**: Aprenda a implementar sistemas de recuperação de conhecimento
- **[Gerenciamento de Estado](state.md)**: Explore como gerenciar o estado dos agentes
- **[Ferramentas e MCP](tools.md)**: Descubra como integrar ferramentas aos agentes
