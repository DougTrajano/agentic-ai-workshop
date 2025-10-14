# 🎯 Zero-shot vs Few-shot Learning

Uma das decisões mais importantes ao construir prompts é determinar se você deve fornecer exemplos ao modelo. Esta escolha impacta diretamente a qualidade, consistência e formato das respostas.

## O que é Zero-shot Learning?

**Zero-shot learning** é quando você fornece instruções ao modelo sem incluir exemplos específicos da tarefa. O modelo usa apenas seu conhecimento pré-treinado para completar a tarefa.

### Exemplo de Zero-shot

```python
prompt = """
Classifique o sentimento do seguinte texto como Positivo, Negativo ou Neutro:

Texto: "O produto chegou mais rápido que o esperado e a qualidade é excelente!"

Sentimento:
"""
```

### Características do Zero-shot

**Vantagens:**

- Mais rápido de criar e iterar
- Economiza tokens (context window menor)
- Flexível para tarefas variadas
- Ideal para tarefas simples e diretas

**Desvantagens:**

- Menos controle sobre formato de saída
- Pode gerar respostas inconsistentes
- Limitado para tarefas muito específicas ou complexas
- Resultados podem variar entre diferentes execuções

## O que é Few-shot Learning?

**Few-shot learning** é quando você fornece alguns exemplos (tipicamente 2-10) de pares entrada/saída antes de apresentar a tarefa real. Esses exemplos servem como guia para o modelo entender exatamente o que você espera.

### Exemplo de Few-shot

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

### Características do Few-shot

**Vantagens:**

- Maior controle sobre formato de saída
- Respostas mais consistentes
- Melhor performance em tarefas específicas
- Permite ensinar padrões complexos

**Desvantagens:**

- Requer mais tempo para criar exemplos de qualidade
- Consome mais tokens do context window
- Exemplos ruins podem degradar performance
- Pode criar viés se exemplos não forem representativos

## Quando Usar Cada Abordagem

### Use Zero-shot quando

1. **A tarefa é simples e clara**

```python
prompt = """
Traduza o seguinte texto para inglês:

"Olá, como você está?"

Tradução:
"""
```

2. **Você está explorando capacidades do modelo**

```python
prompt = """
Resuma em uma frase o seguinte artigo:

[artigo aqui]

Resumo:
"""
```

3. **Você tem limitações de context window**

```python
# Quando você precisa economizar tokens para dados volumosos
prompt = f"""
Analise os seguintes {len(data)} registros e identifique anomalias:

{data}

Anomalias encontradas:
"""
```

4. **A tarefa requer raciocínio geral**

```python
prompt = """
Explique por que a diversidade é importante em equipes de dados.

Resposta:
"""
```

### Use Few-shot quando

1. **Você precisa de um formato específico**

```python
prompt = """
Converta descrições em dados estruturados:

Exemplo 1:
Descrição: "João Silva, 35 anos, trabalha como desenvolvedor"
JSON: {"nome": "João Silva", "idade": 35, "cargo": "desenvolvedor"}

Exemplo 2:
Descrição: "Maria Santos, 28 anos, trabalha como designer"
JSON: {"nome": "Maria Santos", "idade": 28, "cargo": "designer"}

Agora converta:
Descrição: "Pedro Costa, 42 anos, trabalha como gerente"
JSON:
"""
```

2. **A tarefa envolve padrões específicos do seu domínio**

```python
prompt = """
Classifique tickets de suporte por prioridade:

Exemplo 1:
Ticket: "Sistema fora do ar, ninguém consegue acessar"
Prioridade: CRÍTICA

Exemplo 2:
Ticket: "Sugestão de melhoria na interface"
Prioridade: BAIXA

Exemplo 3:
Ticket: "Erro ao salvar dados, afeta alguns usuários"
Prioridade: ALTA

Classifique:
Ticket: "Dashboard apresentando dados desatualizados"
Prioridade:
"""
```

3. **Você quer ensinar um estilo específico**

```python
prompt = """
Escreva descrições de insights de dados:

Exemplo 1:
Dado: "Turnover aumentou 15% no Q2"
Descrição: "Observamos um aumento significativo de 15 pontos percentuais no turnover durante o segundo trimestre, sugerindo a necessidade de investigação das causas subjacentes."

Exemplo 2:
Dado: "Engagement score: 7.2/10"
Descrição: "A pontuação de engagement de 7.2 indica um nível moderadamente alto de satisfação, porém há espaço para melhoria através de iniciativas direcionadas."

Agora escreva:
Dado: "Tempo médio de contratação: 45 dias"
Descrição:
"""
```

4. **Você precisa de consistência entre múltiplas execuções**

```python
# Few-shot garante que todas as classificações sigam o mesmo padrão
prompt = """
Categorize feedbacks de funcionários:

Exemplo 1:
Feedback: "Adoraria ter mais oportunidades de desenvolvimento"
Categoria: Desenvolvimento Profissional
Sentimento: Construtivo

Exemplo 2:
Feedback: "A comunicação da liderança precisa melhorar urgentemente"
Categoria: Liderança
Sentimento: Crítico

Agora categorize:
Feedback: "{user_feedback}"
Categoria:
"""
```

## Estratégias de Few-shot

### 1. Número Ideal de Exemplos

```python
# Muito poucos (1-2): Pode não estabelecer padrão claro
few_shot_weak = """
Exemplo:
Input: "excelente"
Output: Positivo

Classifique: "terrível"
"""

# Ideal (3-5): Estabelece padrão sem consumir muito contexto
few_shot_ideal = """
Exemplo 1: "excelente" -> Positivo
Exemplo 2: "terrível" -> Negativo  
Exemplo 3: "ok" -> Neutro
Exemplo 4: "fantástico" -> Positivo
Exemplo 5: "horrível" -> Negativo

Classifique: "razoável"
"""

# Muitos (10+): Pode ser necessário para tarefas muito complexas,
# mas consome muito context window
```

### 2. Qualidade sobre Quantidade

```python
# Bons exemplos são diversos e representativos
good_examples = """
Exemplo 1 (curto e positivo): "Ótimo!" -> Positivo
Exemplo 2 (longo e negativo): "Tive uma experiência muito ruim, produto de baixa qualidade" -> Negativo
Exemplo 3 (neutro com nuance): "É aceitável para o preço" -> Neutro
Exemplo 4 (positivo com ressalva): "Bom produto, mas a entrega demorou" -> Positivo
"""

# Exemplos ruins são muito similares
bad_examples = """
Exemplo 1: "Bom" -> Positivo
Exemplo 2: "Muito bom" -> Positivo
Exemplo 3: "Excelente" -> Positivo
"""
```

### 3. Ordem dos Exemplos

```python
# A ordem pode importar - considere ordenar por complexidade
prompt_ordered = """
# Começe com casos simples
Exemplo 1: "Ótimo" -> Positivo
Exemplo 2: "Ruim" -> Negativo

# Progrida para casos mais complexos
Exemplo 3: "Bom, mas poderia ser melhor" -> Neutro
Exemplo 4: "Não atendeu expectativas apesar da boa qualidade" -> Negativo
"""
```

### 4. Balanceamento de Classes

```python
# Certifique-se de ter exemplos de todas as categorias
balanced_examples = """
# 2 exemplos de cada categoria
Positivo:
- "Excelente produto!"
- "Muito satisfeito com a compra"

Negativo:
- "Péssima experiência"
- "Não recomendo"

Neutro:
- "É ok"
- "Atende o básico"
"""
```

## Técnicas Avançadas

### One-shot Learning

Às vezes, um único exemplo muito bem escolhido é suficiente:

```python
one_shot_prompt = """
Converta descrições em SQL:

Exemplo:
Descrição: "Mostre todos os funcionários do departamento de TI contratados em 2023"
SQL: SELECT * FROM employees WHERE department = 'TI' AND YEAR(hire_date) = 2023;

Agora converta:
Descrição: "{user_query}"
SQL:
"""
```

### Dynamic Few-shot

Selecione exemplos dinamicamente baseado na entrada do usuário:

```python
from typing import List, Tuple

class DynamicFewShotSelector:
    def __init__(self, example_bank: List[Tuple[str, str]]):
        self.examples = example_bank
    
    def select_relevant_examples(self, query: str, n: int = 3) -> List[Tuple[str, str]]:
        """
        Seleciona os N exemplos mais relevantes para a query
        usando similaridade semântica
        """
        # Calcula similaridade entre query e cada exemplo
        similarities = [
            (example, self.calculate_similarity(query, example[0]))
            for example in self.examples
        ]
        
        # Retorna os N mais similares
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [ex[0] for ex in similarities[:n]]
    
    def build_prompt(self, query: str) -> str:
        examples = self.select_relevant_examples(query)
        
        prompt = "Classifique o sentimento:\n\n"
        
        for i, (text, sentiment) in enumerate(examples, 1):
            prompt += f"Exemplo {i}:\nTexto: {text}\nSentimento: {sentiment}\n\n"
        
        prompt += f"Agora classifique:\nTexto: {query}\nSentimento:"
        
        return prompt
```

### Progressive Few-shot

Comece com zero-shot e adicione exemplos se necessário:

```python
class ProgressiveFewShot:
    def __init__(self, examples: List[Tuple[str, str]]):
        self.examples = examples
    
    def classify(self, text: str, confidence_threshold: float = 0.8):
        # Tenta zero-shot primeiro
        prompt_zero = f"Classifique o sentimento: {text}\nSentimento:"
        response, confidence = llm.generate_with_confidence(prompt_zero)
        
        if confidence >= confidence_threshold:
            return response
        
        # Se confiança baixa, tenta com 3 exemplos
        prompt_few = self.build_few_shot_prompt(text, n_examples=3)
        response, confidence = llm.generate_with_confidence(prompt_few)
        
        if confidence >= confidence_threshold:
            return response
        
        # Se ainda baixa confiança, usa todos os exemplos
        prompt_many = self.build_few_shot_prompt(text, n_examples=len(self.examples))
        response, _ = llm.generate_with_confidence(prompt_many)
        
        return response
```

## Casos de Uso Práticos

### Extração de Informações Estruturadas

```python
# Few-shot é ideal para ensinar formatos estruturados
extraction_prompt = """
Extraia informações de descrições de vagas:

Exemplo 1:
Texto: "Buscamos desenvolvedor Python sênior com 5+ anos de experiência em São Paulo"
Output:
{
  "cargo": "Desenvolvedor Python Sênior",
  "experiencia_minima": 5,
  "localizacao": "São Paulo"
}

Exemplo 2:
Texto: "Vaga para analista de dados júnior, remoto, conhecimento em SQL"
Output:
{
  "cargo": "Analista de Dados Júnior",
  "experiencia_minima": 0,
  "localizacao": "Remoto"
}

Agora extraia:
Texto: "{job_description}"
Output:
"""
```

### Análise de Sentimento Contextual

```python
# Few-shot captura nuances do domínio
sentiment_prompt = """
Analise o sentimento de feedbacks de funcionários:

Exemplo 1:
Feedback: "O trabalho remoto melhorou minha qualidade de vida"
Sentimento: Positivo
Aspecto: Modelo de trabalho
Intensidade: Alta

Exemplo 2:
Feedback: "Poderiam melhorar a comunicação sobre mudanças"
Sentimento: Construtivo
Aspecto: Comunicação interna
Intensidade: Média

Exemplo 3:
Feedback: "Estou extremamente insatisfeito com a falta de reconhecimento"
Sentimento: Negativo
Aspecto: Reconhecimento
Intensidade: Alta

Analise:
Feedback: "{employee_feedback}"
"""
```

### Classificação Multi-label

```python
# Few-shot para classificações complexas
multilabel_prompt = """
Classifique tickets de RH por categoria (pode ter múltiplas):

Exemplo 1:
Ticket: "Gostaria de saber sobre as opções de plano de saúde e se posso incluir dependentes"
Categorias: [Benefícios, Plano de Saúde]

Exemplo 2:
Ticket: "Quando receberei o reembolso de despesas da conferência que participei?"
Categorias: [Financeiro, Desenvolvimento Profissional, Reembolso]

Exemplo 3:
Ticket: "Preciso ajustar minha carga horária por motivos de saúde"
Categorias: [Saúde, Jornada de Trabalho]

Classifique:
Ticket: "{ticket_text}"
Categorias:
"""
```

## Medindo Eficácia

### Comparando Zero-shot vs Few-shot

```python
class ApproachComparator:
    def __init__(self):
        self.results = {'zero_shot': [], 'few_shot': []}
    
    def compare_approaches(self, test_cases: List[dict]):
        for case in test_cases:
            # Zero-shot
            zero_prompt = f"Classifique: {case['input']}\nClasse:"
            zero_result = llm.generate(zero_prompt)
            self.results['zero_shot'].append({
                'prediction': zero_result,
                'actual': case['expected'],
                'correct': zero_result == case['expected']
            })
            
            # Few-shot
            few_prompt = self.build_few_shot_prompt(case['input'])
            few_result = llm.generate(few_prompt)
            self.results['few_shot'].append({
                'prediction': few_result,
                'actual': case['expected'],
                'correct': few_result == case['expected']
            })
        
        return self.analyze_results()
    
    def analyze_results(self):
        zero_accuracy = sum(r['correct'] for r in self.results['zero_shot']) / len(self.results['zero_shot'])
        few_accuracy = sum(r['correct'] for r in self.results['few_shot']) / len(self.results['few_shot'])
        
        return {
            'zero_shot_accuracy': zero_accuracy,
            'few_shot_accuracy': few_accuracy,
            'improvement': few_accuracy - zero_accuracy
        }
```

## Boas Práticas

### ✅ Do's

1. **Comece com zero-shot** - teste se é suficiente antes de adicionar complexidade
2. **Use exemplos diversos** - cubra edge cases e variações
3. **Mantenha exemplos concisos** - foque no essencial
4. **Teste com diferentes números de exemplos** - encontre o ponto ideal
5. **Versione seus exemplos** - trate como código

### ❌ Don'ts

1. **Não use exemplos contraditórios** - confunde o modelo
2. **Não sobrecarregue com exemplos** - há retorno decrescente
3. **Não use exemplos de baixa qualidade** - "garbage in, garbage out"
4. **Não ignore o custo de tokens** - few-shot pode ser caro
5. **Não assuma que mais exemplos é sempre melhor** - qualidade > quantidade

## Próximos Passos

Agora que você entende zero-shot e few-shot learning, explore:

- **[Chain-of-Thought](chain-of-thought.md)**: Combine few-shot com raciocínio explícito
- **[Meta-Prompting](meta-prompting.md)**: Use templates estruturados
- **[Evaluation](evaluation.md)**: Meça sistematicamente qual abordagem funciona melhor

## Recursos Adicionais

- Mantenha um banco de exemplos de qualidade para reutilização
- Documente qual abordagem funciona melhor para cada tipo de tarefa
- Considere criar ferramentas para geração automática de exemplos
- Monitore o desempenho ao longo do tempo e ajuste conforme necessário
