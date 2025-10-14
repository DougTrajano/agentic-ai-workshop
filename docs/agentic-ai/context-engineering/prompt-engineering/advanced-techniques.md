# 🔧 Técnicas Avançadas de Prompting

Além das técnicas fundamentais, existem estratégias avançadas que podem melhorar significativamente a qualidade e confiabilidade das respostas de modelos de linguagem. Estas técnicas são especialmente úteis para tarefas complexas que exigem raciocínio sofisticado ou alta precisão.

## 🔁 Self-Consistency

**Self-Consistency** envolve executar o mesmo prompt múltiplas vezes e usar votação majoritária ou análise de consenso para determinar a resposta mais confiável. Esta técnica é particularmente eficaz para tarefas com respostas determinísticas.

### Implementação Básica

```python
def self_consistency_prompting(prompt: str, n_iterations: int = 5):
    """
    Executa o mesmo prompt múltiplas vezes e retorna a resposta mais comum
    """
    responses = []
    
    for _ in range(n_iterations):
        response = llm.generate(prompt)
        responses.append(response)
    
    # Analisa consistência e retorna resposta mais comum
    return analyze_consistency(responses)


def analyze_consistency(responses: list) -> dict:
    """
    Analisa as respostas e retorna a mais consistente
    """
    from collections import Counter
    
    # Conta frequência de cada resposta
    response_counts = Counter(responses)
    
    # Resposta mais comum
    most_common_response, count = response_counts.most_common(1)[0]
    
    # Calcula confiança baseado em consenso
    confidence = count / len(responses)
    
    return {
        'response': most_common_response,
        'confidence': confidence,
        'all_responses': responses,
        'distribution': dict(response_counts)
    }
```

### Exemplo Prático

```python
# Prompt para classificação
classification_prompt = """
Classifique o seguinte feedback de funcionário como:
- Positivo
- Negativo  
- Neutro
- Construtivo

Feedback: "A liderança poderia melhorar a comunicação sobre mudanças organizacionais."

Classificação:
"""

# Executa 5 vezes e usa votação
result = self_consistency_prompting(classification_prompt, n_iterations=5)

# Resultado:
# {
#   'response': 'Construtivo',
#   'confidence': 0.8,  # 4 de 5 respostas concordaram
#   'all_responses': ['Construtivo', 'Construtivo', 'Neutro', 'Construtivo', 'Construtivo'],
#   'distribution': {'Construtivo': 4, 'Neutro': 1}
# }
```

### Self-Consistency com Chain-of-Thought

Combine self-consistency com CoT para maior precisão:

```python
cot_consistency_prompt = """
Resolva passo a passo:

Problema: Uma empresa tem taxa de turnover de 15% ao ano. 
Se começaram o ano com 200 funcionários e não fizeram novas contratações, 
quantos funcionários aproximadamente terão ao final do ano?

Raciocínio passo a passo:
"""

# Executa múltiplas vezes
results = self_consistency_prompting(cot_consistency_prompt, n_iterations=7)

# Analisa não só a resposta final, mas também os passos de raciocínio
```

## 🌳 Tree of Thoughts (ToT)

**Tree of Thoughts** explora múltiplos caminhos de raciocínio em paralelo, avaliando e selecionando as melhores rotas para a solução. É como fazer brainstorming estruturado com o modelo.

### Estrutura Básica

```python
tree_prompt = """
Vamos explorar diferentes abordagens para este problema:

Problema: {problem}

Caminho 1: Abordagem Analítica
- Passo A1: [Análise quantitativa]
- Passo A2: [Modelagem estatística]
- Avaliação: [Prós e contras desta abordagem]

Caminho 2: Abordagem Qualitativa  
- Passo B1: [Pesquisa qualitativa]
- Passo B2: [Análise de padrões]
- Avaliação: [Prós e contras desta abordagem]

Caminho 3: Abordagem Híbrida
- Passo C1: [Combinação de métodos]
- Passo C2: [Validação cruzada]
- Avaliação: [Prós e contras desta abordagem]

Agora avalie cada caminho e escolha o melhor, justificando sua decisão:
"""
```

### Implementação Iterativa

```python
class TreeOfThoughts:
    def __init__(self, problem: str, max_depth: int = 3):
        self.problem = problem
        self.max_depth = max_depth
        self.tree = {}
    
    def generate_thoughts(self, current_state: str, depth: int = 0) -> list:
        """Gera múltiplos próximos pensamentos possíveis"""
        prompt = f"""
        Estado atual do problema: {current_state}
        
        Gere 3 possíveis próximos passos de raciocínio:
        
        Opção 1: [descrição]
        Opção 2: [descrição]
        Opção 3: [descrição]
        """
        
        response = llm.generate(prompt)
        return self.parse_thoughts(response)
    
    def evaluate_thought(self, thought: str) -> float:
        """Avalia a qualidade de um pensamento"""
        prompt = f"""
        Avalie a qualidade deste passo de raciocínio em uma escala de 0 a 1:
        
        Pensamento: {thought}
        
        Considere:
        - Relevância para o problema
        - Lógica e coerência
        - Probabilidade de levar à solução
        
        Score (0.0 a 1.0):
        """
        
        score = llm.generate(prompt)
        return float(score)
    
    def solve(self) -> str:
        """Resolve o problema explorando a árvore de pensamentos"""
        current_state = self.problem
        path = []
        
        for depth in range(self.max_depth):
            # Gera possíveis próximos pensamentos
            thoughts = self.generate_thoughts(current_state, depth)
            
            # Avalia cada pensamento
            scores = [(thought, self.evaluate_thought(thought)) for thought in thoughts]
            
            # Escolhe o melhor pensamento
            best_thought, best_score = max(scores, key=lambda x: x[1])
            
            path.append(best_thought)
            current_state = f"{current_state}\n{best_thought}"
        
        return "\n".join(path)
```

### Exemplo de Uso

```python
# Define o problema
problem = """
Como reduzir o turnover em 30% nos próximos 6 meses com budget limitado?
"""

# Explora árvore de pensamentos
tot = TreeOfThoughts(problem, max_depth=3)
solution = tot.solve()

# Resultado será um caminho estruturado através de múltiplas opções
```

## 🏛️ Constitutional AI

**Constitutional AI** usa princípios explícitos para orientar o comportamento e as respostas do modelo. Isso garante alinhamento com valores, ética e diretrizes específicas.

### Template Básico

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

### Implementação para People Analytics

```python
people_analytics_constitution = """
PRINCÍPIOS CONSTITUCIONAIS PARA ANÁLISE DE DADOS DE RH:

1. PRIVACIDADE E CONFIDENCIALIDADE
   - Nunca exponha dados individuais identificáveis
   - Agregue dados em grupos de no mínimo 5 pessoas
   - Respeite regulamentações de proteção de dados (LGPD, GDPR)

2. EQUIDADE E NÃO-DISCRIMINAÇÃO
   - Evite vieses em análises e recomendações
   - Considere impacto em grupos diversos
   - Não faça suposições baseadas em características protegidas

3. TRANSPARÊNCIA METODOLÓGICA
   - Explique como chegou às conclusões
   - Indique limitações dos dados e análises
   - Seja claro sobre nível de confiança

4. FOCO NO BEM-ESTAR
   - Priorize bem-estar dos colaboradores
   - Considere impacto humano das recomendações
   - Balance eficiência com qualidade de vida

5. AÇÃO RESPONSÁVEL
   - Recomendações devem ser éticas e legais
   - Considere consequências não intencionais
   - Sugira pilotagem e monitoramento

Análise: {query}

Responda seguindo rigorosamente estes princípios:
"""
```

### Auto-Verificação Constitucional

```python
def constitutional_verification(response: str, constitution: dict) -> dict:
    """
    Verifica se uma resposta está alinhada com os princípios constitucionais
    """
    verification_prompt = f"""
    Resposta a ser verificada:
    {response}
    
    Princípios constitucionais:
    {constitution}
    
    Para cada princípio, avalie se a resposta está alinhada:
    
    Princípio 1: [ALINHADO / NÃO ALINHADO] - Justificativa
    Princípio 2: [ALINHADO / NÃO ALINHADO] - Justificativa
    ...
    
    Conclusão: [APROVADO / REQUER REVISÃO]
    """
    
    verification = llm.generate(verification_prompt)
    
    # Se não aprovado, solicita revisão
    if "REQUER REVISÃO" in verification:
        revision_prompt = f"""
        Resposta original: {response}
        
        Problemas identificados: {verification}
        
        Revise a resposta para alinhar com todos os princípios:
        """
        
        revised_response = llm.generate(revision_prompt)
        return revised_response
    
    return response
```

## 🎲 Maieutic Prompting

Inspirado no método socrático, **Maieutic Prompting** faz o modelo questionar suas próprias respostas e explorar inconsistências.

### Implementação

```python
maieutic_prompt = """
Responda a seguinte pergunta, mas depois questione sua própria resposta:

Pergunta: {question}

Resposta inicial:
[Sua resposta]

Agora questione sua resposta:
- Que premissas você assumiu?
- Há evidências contra esta conclusão?
- Que perspectivas alternativas existem?
- Quão confiante você está?

Resposta refinada considerando as questões acima:
[Versão melhorada]
"""
```

### Exemplo Prático

```python
question = "Por que o turnover aumentou no último trimestre?"

maieutic_analysis = """
Pergunta: Por que o turnover aumentou no último trimestre?

Resposta inicial:
O turnover aumentou devido a mudanças na liderança e aumento de oportunidades no mercado.

Questionamento:
- Premissa: Assumimos correlação entre mudança de liderança e turnover, mas verificamos se isso é causal?
- Evidência contrária: Há departamentos com mudança de liderança que não tiveram aumento de turnover?
- Perspectivas alternativas: Poderia ser sazonalidade? Mudanças em compensação? Cultura organizacional?
- Confiança: Moderada - precisamos de análise mais profunda para confirmar causas

Resposta refinada:
O aumento de turnover coincide com mudanças de liderança em alguns departamentos, 
mas precisamos de análise mais granular para confirmar causalidade. Fatores adicionais 
a investigar incluem:
1. Comparação com sazonalidade histórica
2. Análise por departamento e nível
3. Exit interviews para entender motivações reais
4. Benchmarking com mercado

Recomendação: Realizar análise diagnóstica detalhada antes de implementar intervenções.
"""
```

## 🔄 Iterative Refinement

Refine progressivamente a resposta através de múltiplas iterações:

```python
class IterativeRefinement:
    def __init__(self, initial_prompt: str, max_iterations: int = 3):
        self.initial_prompt = initial_prompt
        self.max_iterations = max_iterations
    
    def refine(self) -> str:
        current_response = llm.generate(self.initial_prompt)
        
        for i in range(self.max_iterations):
            refinement_prompt = f"""
            Resposta atual:
            {current_response}
            
            Iteração {i+1}: Melhore esta resposta considerando:
            - Clareza e concisão
            - Precisão e completude
            - Estrutura e organização
            - Acionabilidade das recomendações
            
            Versão melhorada:
            """
            
            current_response = llm.generate(refinement_prompt)
        
        return current_response
```

## 🎯 Directional Stimulus Prompting

Use palavras-chave ou frases específicas para guiar o modelo em direção a tipos específicos de respostas:

```python
# Guiar para resposta mais criativa
creative_stimulus = """
{task}

Pense de forma inovadora e não convencional.
Palavras-chave para guiar: criatividade, inovação, disruptivo, único
"""

# Guiar para resposta mais analítica
analytical_stimulus = """
{task}

Use raciocínio lógico e rigoroso.
Palavras-chave para guiar: dados, evidências, metodologia, precisão
"""

# Guiar para resposta mais prática
practical_stimulus = """
{task}

Foque em aplicabilidade imediata.
Palavras-chave para guiar: acionável, implementável, prático, quick wins
"""
```

## 🔗 Recursive Prompting

Decomponha problemas complexos recursivamente:

```python
def recursive_solve(problem: str, depth: int = 0, max_depth: int = 3) -> str:
    """
    Resolve problemas complexos recursivamente
    """
    if depth >= max_depth:
        return llm.generate(f"Resolva diretamente: {problem}")
    
    # Verifica se o problema é simples o suficiente
    complexity_check = f"""
    Este problema é simples o suficiente para ser resolvido diretamente?
    
    Problema: {problem}
    
    Responda apenas SIM ou NÃO:
    """
    
    is_simple = llm.generate(complexity_check).strip().upper()
    
    if is_simple == "SIM":
        return llm.generate(f"Resolva: {problem}")
    
    # Decompõe em sub-problemas
    decomposition = f"""
    Decomponha este problema em 2-3 sub-problemas mais simples:
    
    Problema: {problem}
    
    Sub-problemas:
    1.
    2.
    3.
    """
    
    sub_problems = llm.generate(decomposition)
    sub_solutions = []
    
    # Resolve cada sub-problema recursivamente
    for sub_problem in parse_sub_problems(sub_problems):
        solution = recursive_solve(sub_problem, depth + 1, max_depth)
        sub_solutions.append(solution)
    
    # Combina soluções
    synthesis = f"""
    Problema original: {problem}
    
    Soluções dos sub-problemas:
    {chr(10).join(sub_solutions)}
    
    Combine estas soluções para resolver o problema original:
    """
    
    return llm.generate(synthesis)
```

## 🧪 Analogical Prompting

Use analogias para facilitar o raciocínio:

```python
analogical_prompt = """
Tarefa: {task}

Primeiro, pense em um problema análogo mais simples ou familiar:
Analogia: [Problema similar mais simples]

Resolva a analogia:
Solução da analogia: [Como resolver o problema análogo]

Agora aplique o mesmo raciocínio ao problema original:
Solução: [Aplique os insights da analogia]
"""

# Exemplo
example = """
Tarefa: Como implementar programa de mentoria em organização de 500 pessoas?

Analogia: É como organizar um torneio esportivo - você precisa:
1. Definir regras claras
2. Parear participantes de forma justa
3. Estabelecer cronograma
4. Ter sistema de acompanhamento
5. Reconhecer participação

Aplicando ao programa de mentoria:
1. Definir objetivos e expectativas claras
2. Fazer matching mentor-mentee baseado em critérios
3. Estabelecer duração e frequência de encontros
4. Criar sistema de acompanhamento de progresso
5. Reconhecer e celebrar sucessos
"""
```

## 🎭 Perspective Taking

Analise problemas de múltiplas perspectivas:

```python
multi_perspective_prompt = """
Analise a seguinte situação de múltiplas perspectivas:

Situação: {situation}

PERSPECTIVA 1: Liderança / Executivos
[Como eles veriam isso? Quais suas prioridades?]

PERSPECTIVA 2: Colaboradores
[Como eles veriam isso? Quais suas preocupações?]

PERSPECTIVA 3: RH / People Ops
[Como eles veriam isso? Quais suas considerações?]

PERSPECTIVA 4: Stakeholders Externos
[Como eles veriam isso? Qual o impacto?]

SÍNTESE:
[Combine insights de todas as perspectivas]

RECOMENDAÇÃO BALANCEADA:
[Solução que considera todas as perspectivas]
"""
```

## 📊 Combinando Técnicas

As técnicas mais poderosas surgem da combinação:

```python
# Self-Consistency + Chain-of-Thought
combined_prompt = """
Problema: {problem}

Vamos pensar passo a passo:
[Raciocínio estruturado]
"""
# Execute 5 vezes e use votação


# Tree of Thoughts + Constitutional AI
tot_constitutional = """
Explore múltiplos caminhos de solução, mas cada caminho 
deve respeitar os seguintes princípios:
{constitution}

Problema: {problem}

Caminho 1: [Respeitando princípios]
Caminho 2: [Respeitando princípios]
Caminho 3: [Respeitando princípios]

Melhor caminho: [Escolha justificada]
"""


# Recursive + Maieutic
recursive_maieutic = """
Para cada sub-problema:
1. Resolva
2. Questione sua solução
3. Refine

Problema: {problem}
[Decomponha e aplique maieutic a cada parte]
"""
```

## Próximos Passos

Explore como integrar estas técnicas avançadas:

- **[Agent Prompting](agent-prompting.md)**: Use técnicas avançadas em agentes
- **[Evaluation](evaluation.md)**: Meça o impacto de técnicas avançadas
- **[Best Practices](best-practices.md)**: Aprenda quando usar cada técnica

## Recursos Adicionais

- Experimente com diferentes combinações de técnicas
- Documente quais técnicas funcionam melhor para quais tipos de problemas
- Considere o trade-off entre complexidade e benefício
- Monitore custos (tokens) versus ganhos de qualidade
