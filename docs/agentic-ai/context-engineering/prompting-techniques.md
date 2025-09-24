# Técnicas de Prompt Engineering

O **Prompt Engineering** é a arte de comunicar efetivamente com modelos de linguagem para obter os melhores resultados. Para sistemas agentivos, estas técnicas são fundamentais para orientar o comportamento dos agentes.

## 🎭 Role-based Prompts

Criar prompts eficazes baseados em papéis vai além de simplesmente dizer "Aja como um especialista". Você precisa ser específico sobre os atributos da persona, incluindo personalidade, estilo de comunicação, vocabulário e áreas de especialização.

### Componentes de um Prompt Baseado em Papéis

- **[Papel]**: A persona que o LLM deve adotar
- **[Tarefa]**: A instrução ou pergunta específica
- **[Formato de Saída]**: Como a resposta deve ser estruturada
- **[Exemplos]**: Exemplos de pares de entrada/saída
- **[Contexto]**: Informações adicionais necessárias

### Exemplo Completo

```markdown
# Papel
Você é um Sr. Data Scientist especializado em análise de RH com 10 anos de experiência em People Analytics. Você é conhecido por transformar dados complexos em insights acionáveis para liderança executiva.

# Personalidade
- Comunicação clara e objetiva
- Foco em insights de negócio
- Sempre considera implicações éticas
- Apresenta dados com storytelling eficaz

# Tarefa
Analise os dados de turnover fornecidos e identifique padrões, causas raiz e recomendações específicas.

# Formato de Saída
- Resumo executivo (2-3 frases)
- Principais insights (bullet points)
- Recomendações acionáveis (numeradas)
- Próximos passos sugeridos

# Contexto Adicional
- Empresa de tecnologia com 500 funcionários
- Foco em retenção de talentos em tecnologia
- Budget limitado para initiatives de RH
```

## 🎯 Zero-shot vs Few-shot Learning

### Zero-shot Learning

O modelo recebe apenas instruções, sem exemplos específicos:

```python
prompt = """
Classifique o sentimento do seguinte texto como Positivo, Negativo ou Neutro:

Texto: "O produto chegou mais rápido que o esperado e a qualidade é excelente!"

Sentimento:
"""
```

### Few-shot Learning

O modelo recebe alguns exemplos para contextualizar o padrão:

```python
prompt = """
Classifique o sentimento dos textos como Positivo, Negativo ou Neutro:

Exemplo 1:
Texto: "Adorei o atendimento, muito profissional!"
Sentimento: Positivo

Exemplo 2:
Texto: "O produto chegou com defeito e o suporte não ajudou."
Sentimento: Negativo

Exemplo 3:
Texto: "O produto é ok, nada excepcional."
Sentimento: Neutro

Agora classifique:
Texto: "O produto chegou mais rápido que o esperado e a qualidade é excelente!"
Sentimento:
"""
```

### Quando Usar Cada Abordagem

**Zero-shot:**
- Tarefas simples e diretas
- Quando você tem poucos exemplos
- Para exploração inicial de capacidades

**Few-shot:**
- Tarefas complexas ou específicas
- Quando você quer um formato específico
- Para melhorar consistência de respostas

## 🧠 Chain-of-Thought (CoT) Prompting

O **Chain-of-Thought** encoraja o modelo a expor seu raciocínio intermediário, melhorando respostas em tarefas complexas[^1].

### CoT Básico

```python
prompt = """
Preciso resolver este problema passo a passo:

Problema: Uma empresa tem 120 funcionários. 30% trabalham remotamente, 
40% trabalham híbrido, e o resto trabalha presencial. Se 15 funcionários 
remotos deixaram a empresa, qual é a nova distribuição?

Vamos pensar passo a passo:
"""
```

### CoT com Exemplos

```python
prompt = """
Resolva problemas matemáticos mostrando seu raciocínio:

Exemplo:
Problema: Uma loja tinha 150 produtos. Vendeu 60 no primeiro dia e 40 no segundo. Quantos restaram?
Pensamento: 
1. Produtos iniciais: 150
2. Vendidos total: 60 + 40 = 100
3. Produtos restantes: 150 - 100 = 50
Resposta: 50 produtos

Agora resolva:
Problema: Uma empresa tem 120 funcionários. 30% trabalham remotamente, 40% trabalham híbrido, e o resto trabalha presencial. Se 15 funcionários remotos deixaram a empresa, qual é a nova distribuição?

Pensamento:
"""
```

### CoT para Agentes

```python
agent_prompt = """
Você é um agente de análise de dados. Para cada tarefa, siga este processo de raciocínio:

1. **Compreensão**: O que está sendo pedido?
2. **Planejamento**: Quais passos preciso seguir?
3. **Execução**: Como vou realizar cada passo?
4. **Validação**: Os resultados fazem sentido?

Tarefa: {user_query}

Pensamento:
1. Compreensão:
"""
```

## 🔄 Meta-Prompting

**Meta-prompting** foca na estrutura abstrata da tarefa, usando instruções ou modelos sintáticos que guiam o formato da resposta[^2].

### Template de Meta-Prompt

```python
meta_prompt_template = """
Você é um sistema que segue padrões estruturados. Para qualquer tarefa, use este template:

## ANÁLISE
- **Objetivo**: [Defina claramente o objetivo]
- **Dados**: [Identifique os dados necessários]
- **Método**: [Escolha a abordagem]

## EXECUÇÃO
- **Passo 1**: [Primeira ação]
- **Passo 2**: [Segunda ação]
- **Passo N**: [Ação final]

## RESULTADO
- **Insights**: [Principais descobertas]
- **Recomendações**: [Ações sugeridas]
- **Confiança**: [Nível de confiança 1-10]

Tarefa: {task_description}
"""
```

### Meta-Prompt para Diferentes Tipos de Tarefa

```python
def generate_meta_prompt(task_type: str) -> str:
    templates = {
        "analysis": """
        Use este padrão para análises:
        1. CONTEXTO: Situação atual
        2. DADOS: Informações disponíveis  
        3. ANÁLISE: Processamento dos dados
        4. INSIGHTS: Descobertas principais
        5. AÇÕES: Próximos passos
        """,
        
        "problem_solving": """
        Use este padrão para resolução de problemas:
        1. PROBLEMA: Definição clara
        2. CAUSAS: Possíveis causas raiz
        3. SOLUÇÕES: Alternativas disponíveis
        4. AVALIAÇÃO: Prós e contras
        5. DECISÃO: Recomendação final
        """,
        
        "creative": """
        Use este padrão para tarefas criativas:
        1. INSPIRAÇÃO: Fontes de ideias
        2. CONCEITO: Ideia central
        3. DESENVOLVIMENTO: Elaboração
        4. REFINAMENTO: Melhorias
        5. APRESENTAÇÃO: Resultado final
        """
    }
    
    return templates.get(task_type, templates["analysis"])
```

## 🔧 Técnicas Avançadas de Prompting

### 1. Self-Consistency

Execute o mesmo prompt múltiplas vezes e use votação majoritária:

```python
def self_consistency_prompting(prompt: str, n_iterations: int = 5):
    responses = []
    
    for _ in range(n_iterations):
        response = llm.generate(prompt)
        responses.append(response)
    
    # Analisa consistência e retorna resposta mais comum
    return analyze_consistency(responses)
```

### 2. Tree of Thoughts

Explora múltiplos caminhos de raciocínio:

```python
tree_prompt = """
Vamos explorar diferentes abordagens para este problema:

Problema: {problem}

Caminho 1: Abordagem Analítica
- Passo A1: [Análise quantitativa]
- Passo A2: [Modelagem estatística]

Caminho 2: Abordagem Qualitativa  
- Passo B1: [Pesquisa qualitativa]
- Passo B2: [Análise de padrões]

Caminho 3: Abordagem Híbrida
- Passo C1: [Combinação de métodos]
- Passo C2: [Validação cruzada]

Avalie cada caminho e escolha o melhor:
"""
```

### 3. Constitutional AI

Use princípios para orientar o comportamento:

```python
constitutional_prompt = """
Princípios que devem orientar suas respostas:
1. Precisão: Informações devem ser factualmente corretas
2. Transparência: Indique quando há incerteza
3. Ética: Considere implicações éticas das recomendações
4. Praticidade: Foque em soluções implementáveis
5. Inclusividade: Considere impacto em todos os stakeholders

Tarefa: {task}

Siga os princípios acima para responder:
"""
```

## 🎨 Prompt Engineering para Agentes

### System Prompt para Agentes

```python
system_prompt = """
Você é um agente de análise de dados especializado em People Analytics.

IDENTIDADE:
- Nome: DataAgent
- Expertise: Análise de RH, estatística, visualização
- Personalidade: Analítico, preciso, orientado a soluções

CAPABILITIES:
- Análise exploratória de dados
- Visualizações e dashboards
- Modelagem preditiva
- Relatórios executivos

TOOLS DISPONÍVEIS:
- query_database: Consulta bases de dados SQL
- create_visualization: Cria gráficos e dashboards
- statistical_analysis: Executa análises estatísticas
- generate_report: Gera relatórios formatados

PROCESSO DE TRABALHO:
1. Compreenda completamente a solicitação
2. Identifique dados necessários
3. Execute análise apropriada
4. Crie visualizações relevantes
5. Forneça insights acionáveis

DIRETRIZES:
- Sempre valide qualidade dos dados
- Explique metodologia utilizada
- Considere limitações e vieses
- Forneça recomendações específicas
"""
```

### Prompt Dinâmico para Contexto

```python
def build_dynamic_prompt(user_query: str, context: dict) -> str:
    base_prompt = "Você é um assistente de análise de dados."
    
    # Adiciona contexto do usuário
    if context.get("user_role"):
        base_prompt += f"\nUsuário: {context['user_role']} com interesse em {context.get('focus_area', 'análise geral')}."
    
    # Adiciona dados disponíveis
    if context.get("available_data"):
        base_prompt += f"\nDados disponíveis: {', '.join(context['available_data'])}"
    
    # Adiciona restrições
    if context.get("constraints"):
        base_prompt += f"\nRestrições: {context['constraints']}"
    
    # Adiciona query do usuário
    base_prompt += f"\n\nSolicitação: {user_query}"
    
    # Adiciona instruções de formato
    base_prompt += "\n\nForneça resposta estruturada com insights claros e recomendações acionáveis."
    
    return base_prompt
```

## 📊 Avaliação de Prompts

### Métricas de Qualidade

```python
class PromptEvaluator:
    def __init__(self):
        self.metrics = [
            'relevance',
            'clarity', 
            'completeness',
            'actionability',
            'accuracy'
        ]
    
    def evaluate_prompt_response(self, prompt: str, response: str, expected_outcome: str = None) -> Dict[str, float]:
        scores = {}
        
        # Relevância: Quão relevante é a resposta para o prompt
        scores['relevance'] = self._score_relevance(prompt, response)
        
        # Clareza: Quão clara e compreensível é a resposta
        scores['clarity'] = self._score_clarity(response)
        
        # Completude: Se a resposta aborda todos os aspectos solicitados
        scores['completeness'] = self._score_completeness(prompt, response)
        
        # Acionabilidade: Se a resposta contém insights acionáveis
        scores['actionability'] = self._score_actionability(response)
        
        # Precisão: Se disponível, compara com resultado esperado
        if expected_outcome:
            scores['accuracy'] = self._score_accuracy(response, expected_outcome)
        
        scores['overall'] = sum(scores.values()) / len(scores)
        return scores
```

### A/B Testing de Prompts

```python
class PromptABTester:
    def __init__(self):
        self.experiments = {}
    
    def create_experiment(self, name: str, prompt_a: str, prompt_b: str):
        self.experiments[name] = {
            'prompt_a': prompt_a,
            'prompt_b': prompt_b,
            'results_a': [],
            'results_b': []
        }
    
    def run_test(self, experiment_name: str, test_queries: List[str], evaluator: PromptEvaluator):
        experiment = self.experiments[experiment_name]
        
        for query in test_queries:
            # Testa prompt A
            response_a = llm.generate(experiment['prompt_a'].format(query=query))
            score_a = evaluator.evaluate_prompt_response(experiment['prompt_a'], response_a)
            experiment['results_a'].append(score_a)
            
            # Testa prompt B  
            response_b = llm.generate(experiment['prompt_b'].format(query=query))
            score_b = evaluator.evaluate_prompt_response(experiment['prompt_b'], response_b)
            experiment['results_b'].append(score_b)
        
        return self._analyze_results(experiment_name)
```

## 🚀 Boas Práticas

### 1. Iteração e Refinamento

```python
def iterative_prompt_development(initial_prompt: str, test_cases: List[dict], max_iterations: int = 5):
    current_prompt = initial_prompt
    
    for iteration in range(max_iterations):
        # Testa prompt atual
        results = test_prompt(current_prompt, test_cases)
        
        # Analisa falhas
        failures = [case for case in results if case['score'] < 0.7]
        
        if not failures:
            break  # Prompt está bom o suficiente
            
        # Refina prompt baseado em falhas
        current_prompt = refine_prompt_based_on_failures(current_prompt, failures)
    
    return current_prompt
```

### 2. Versionamento de Prompts

```python
class PromptVersionManager:
    def __init__(self):
        self.versions = {}
        self.current_versions = {}
    
    def save_prompt_version(self, prompt_id: str, prompt: str, metadata: dict = None):
        if prompt_id not in self.versions:
            self.versions[prompt_id] = []
        
        version = {
            'version': len(self.versions[prompt_id]) + 1,
            'prompt': prompt,
            'timestamp': datetime.now(),
            'metadata': metadata or {}
        }
        
        self.versions[prompt_id].append(version)
        self.current_versions[prompt_id] = version['version']
        
        return version['version']
    
    def get_prompt(self, prompt_id: str, version: int = None) -> str:
        if version is None:
            version = self.current_versions[prompt_id]
        
        return self.versions[prompt_id][version - 1]['prompt']
```

### 3. Prompt Libraries

```python
class PromptLibrary:
    def __init__(self):
        self.prompts = {
            'data_analysis': {
                'exploratory': "Realize uma análise exploratória dos dados fornecidos...",
                'statistical': "Execute análise estatística detalhada...",
                'predictive': "Desenvolva modelo preditivo para..."
            },
            'reporting': {
                'executive': "Crie relatório executivo resumindo...",
                'technical': "Prepare documentação técnica detalhada...",
                'dashboard': "Gere especificações para dashboard..."
            },
            'problem_solving': {
                'root_cause': "Identifique as causas raiz do problema...",
                'solution_design': "Projete soluções para o desafio...",
                'impact_analysis': "Analise o impacto das mudanças propostas..."
            }
        }
    
    def get_prompt(self, category: str, type: str, **kwargs) -> str:
        template = self.prompts[category][type]
        return template.format(**kwargs)
```

---

[^1]: [Chain-of-Thought Prompting - Prompt Engineering Guide](https://www.promptingguide.ai/techniques/cot)
[^2]: [Meta Prompting - Prompt Engineering Guide](https://www.promptingguide.ai/techniques/meta-prompting)