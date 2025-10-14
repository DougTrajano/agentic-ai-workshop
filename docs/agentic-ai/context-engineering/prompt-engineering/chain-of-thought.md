# 🧠 Chain-of-Thought (CoT) Prompting

**Chain-of-Thought (CoT)** é uma técnica poderosa que encoraja o modelo a expor seu raciocínio intermediário, passo a passo, antes de chegar à resposta final. Esta abordagem melhora significativamente a performance em tarefas complexas que requerem raciocínio lógico, matemática, planejamento ou análise multi-etapas[^1].

## Por que Chain-of-Thought Funciona?

Ao forçar o modelo a "pensar em voz alta", você:

1. **Decompõe problemas complexos** em passos gerenciáveis
2. **Reduz erros de raciocínio** ao tornar cada etapa explícita
3. **Permite debugging** do processo de pensamento
4. **Melhora a interpretabilidade** das respostas
5. **Aumenta a precisão** em tarefas que requerem múltiplos passos lógicos

## CoT Básico

A forma mais simples de CoT é simplesmente pedir ao modelo para pensar passo a passo:

```python
prompt = """
Preciso resolver este problema passo a passo:

Problema: Uma empresa tem 120 funcionários. 30% trabalham remotamente, 
40% trabalham híbrido, e o resto trabalha presencial. Se 15 funcionários 
remotos deixaram a empresa, qual é a nova distribuição?

Vamos pensar passo a passo:
"""
```

**Resposta esperada:**

```
Vamos pensar passo a passo:

1. Total de funcionários inicial: 120
2. Funcionários remotos (30%): 120 × 0.30 = 36 funcionários
3. Funcionários híbrido (40%): 120 × 0.40 = 48 funcionários
4. Funcionários presencial (resto): 120 - 36 - 48 = 36 funcionários
5. Funcionários remotos que saíram: 15
6. Novos funcionários remotos: 36 - 15 = 21 funcionários
7. Total de funcionários atual: 120 - 15 = 105 funcionários

Nova distribuição:
- Remotos: 21 funcionários (20%)
- Híbrido: 48 funcionários (45.7%)
- Presencial: 36 funcionários (34.3%)
```

## CoT com Exemplos (Few-shot CoT)

Para tarefas mais complexas ou específicas, combine CoT com few-shot learning:

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
Problema: Uma empresa tem 120 funcionários. 30% trabalham remotamente, 40% trabalham híbrido, 
e o resto trabalha presencial. Se 15 funcionários remotos deixaram a empresa, qual é a nova distribuição?

Pensamento:
"""
```

## CoT para Diferentes Tipos de Tarefas

### Análise de Dados

```python
data_analysis_cot = """
Analise os seguintes dados de turnover e identifique padrões:

Dados:
- Q1: 12% turnover, 80% engagement
- Q2: 18% turnover, 72% engagement  
- Q3: 25% turnover, 65% engagement
- Q4: 15% turnover, 75% engagement

Processo de análise:

1. Observação inicial:
   [O que você nota nos dados brutos?]

2. Identificação de padrões:
   [Quais tendências ou correlações aparecem?]

3. Hipóteses:
   [Quais podem ser as causas?]

4. Insights acionáveis:
   [O que pode ser feito com base nisso?]

Vamos pensar através de cada etapa:
"""
```

### Resolução de Problemas

```python
problem_solving_cot = """
Problema: Taxa de turnover está 30% acima da média da indústria.

Use este framework para analisar:

1. Definição do problema:
   - Qual é especificamente o problema?
   - Quais são os números exatos?
   - Qual o impacto?

2. Identificação de causas possíveis:
   - Fatores internos
   - Fatores externos
   - Hipóteses baseadas em dados

3. Priorização de causas:
   - Quais causas são mais prováveis?
   - Quais têm maior impacto?

4. Soluções propostas:
   - Para cada causa principal
   - Viabilidade e custo
   - Impacto esperado

5. Plano de ação:
   - Próximos passos imediatos
   - Responsáveis
   - Métricas de sucesso

Análise passo a passo:
"""
```

### Tomada de Decisão

```python
decision_making_cot = """
Decisão: Escolher entre três fornecedores de software de RH

Opções:
A) Fornecedor A: $50k/ano, rico em features, implementação 6 meses
B) Fornecedor B: $30k/ano, features básicas, implementação 2 meses
C) Fornecedor C: $70k/ano, features premium + IA, implementação 8 meses

Processo de decisão:

1. Critérios importantes:
   [Liste e pondere os critérios de decisão]

2. Análise de cada opção:
   [Avalie cada opção contra os critérios]

3. Trade-offs:
   [Identifique os compromissos de cada escolha]

4. Riscos e mitigações:
   [Quais riscos cada opção apresenta?]

5. Recomendação:
   [Qual é a melhor escolha e por quê?]

Vamos analisar sistematicamente:
"""
```

## CoT para Agentes

Integrar CoT em agentes torna o processo de raciocínio transparente e auditável:

```python
agent_cot_prompt = """
Você é um agente de análise de dados. Para cada tarefa, siga este processo de raciocínio:

1. **Compreensão**: O que está sendo pedido?
   - Reformule a pergunta em suas próprias palavras
   - Identifique os objetivos principais
   - Liste premissas necessárias

2. **Planejamento**: Quais passos preciso seguir?
   - Quebre a tarefa em sub-tarefas
   - Identifique dados necessários
   - Determine ferramentas apropriadas

3. **Execução**: Como vou realizar cada passo?
   - Execute cada sub-tarefa em ordem
   - Documente resultados intermediários
   - Valide cada etapa antes de prosseguir

4. **Validação**: Os resultados fazem sentido?
   - Verifique consistência dos resultados
   - Compare com expectativas
   - Identifique limitações ou incertezas

5. **Síntese**: Como apresentar a resposta?
   - Resuma insights principais
   - Forneça recomendações acionáveis
   - Indique próximos passos

Tarefa: {user_query}

Pensamento:

1. Compreensão:
"""
```

## Variações de CoT

### Zero-shot CoT

Simplesmente adicione "Let's think step by step" (ou "Vamos pensar passo a passo"):

```python
zero_shot_cot = """
Pergunta: {question}

Vamos pensar passo a passo:
"""
```

Esta abordagem surpreendentemente simples frequentemente melhora resultados significativamente.

### Auto-CoT

O modelo gera seus próprios exemplos de raciocínio:

```python
auto_cot = """
Primeiro, gere 3 exemplos de como resolver problemas similares, mostrando o raciocínio.

Depois, use o mesmo processo para resolver:
{actual_problem}

Exemplos gerados:
"""
```

### Least-to-Most CoT

Decomponha problemas do mais simples ao mais complexo:

```python
least_to_most = """
Vamos resolver este problema começando com as partes mais simples:

Problema: {complex_problem}

Decomposição:
1. Qual é a parte mais simples deste problema?
   [Resolva primeiro]

2. Qual é a próxima parte mais simples?
   [Use resultado anterior para resolver]

3. Combine os resultados:
   [Chegue à solução final]
"""
```

### Self-Ask CoT

O modelo faz perguntas a si mesmo e as responde:

```python
self_ask_cot = """
Pergunta principal: {question}

Processo Self-Ask:

Eu preciso saber: [Primeira sub-pergunta necessária]
Resposta: [Resposta à sub-pergunta]

Eu preciso saber: [Segunda sub-pergunta necessária]
Resposta: [Resposta à sub-pergunta]

...

Portanto, a resposta à pergunta principal é: [Resposta final]
"""
```

## Otimizando CoT

### Estruturando o Raciocínio

```python
structured_cot = """
Analise esta métrica de RH:

[OBSERVAÇÃO]
O que os dados mostram?
- ...

[CONTEXTO]
Qual é o contexto histórico e setorial?
- ...

[ANÁLISE]
Quais fatores podem explicar isso?
- ...

[IMPLICAÇÕES]
O que isso significa para o negócio?
- ...

[RECOMENDAÇÕES]
Quais ações devem ser tomadas?
- ...
"""
```

### Templates de Raciocínio

```python
class CoTTemplate:
    @staticmethod
    def analytical(question: str) -> str:
        return f"""
Questão: {question}

PASSO 1 - Dados disponíveis:
[Liste os dados relevantes]

PASSO 2 - Análise:
[Processe os dados]

PASSO 3 - Padrões identificados:
[Identifique tendências ou anomalias]

PASSO 4 - Interpretação:
[O que os padrões significam?]

PASSO 5 - Conclusão:
[Resposta final com justificativa]
"""
    
    @staticmethod
    def diagnostic(problem: str) -> str:
        return f"""
Problema: {problem}

DIAGNÓSTICO:

1. Sintomas observados:
   [O que está acontecendo?]

2. Possíveis causas:
   [Liste hipóteses]

3. Evidências para cada causa:
   [Avalie cada hipótese]

4. Causa mais provável:
   [Identifique a causa raiz]

5. Solução proposta:
   [Como resolver?]
"""
    
    @staticmethod
    def comparative(options: list) -> str:
        return f"""
Opções: {', '.join(options)}

COMPARAÇÃO:

1. Critérios de avaliação:
   [Liste critérios importantes]

2. Análise opção por opção:
   {chr(10).join(f'   - {opt}: [Avalie]' for opt in options)}

3. Matriz de decisão:
   [Compare sistematicamente]

4. Recomendação:
   [Qual opção e por quê?]
"""
```

## Debugging com CoT

CoT torna mais fácil identificar onde o raciocínio falha:

```python
debugging_example = """
Pergunta: Se 30% dos funcionários são mulheres e há 45 mulheres, quantos funcionários há no total?

Pensamento incorreto (para debugging):
1. 30% são mulheres = 45
2. Então 70% são homens = 105
3. Total = 45 + 105 = 150 ✗ (Erro: não precisamos calcular homens)

Pensamento correto:
1. 30% = 45 funcionárias
2. Seja x o total de funcionários
3. 0.30 × x = 45
4. x = 45 / 0.30
5. x = 150 ✓

Resposta: 150 funcionários
"""
```

## CoT para Tarefas Criativas

Mesmo tarefas criativas se beneficiam de raciocínio estruturado:

```python
creative_cot = """
Tarefa: Crie uma estratégia de employer branding para atrair talentos tech.

Processo criativo:

1. PESQUISA:
   - Quem são nossos competidores?
   - O que talentos tech valorizam?
   - Quais são nossos diferenciais?

2. IDEAÇÃO:
   - Brainstorm de possíveis mensagens
   - Canais potenciais
   - Formatos de conteúdo

3. SELEÇÃO:
   - Avalie ideias contra critérios
   - Escolha as 3 melhores

4. DESENVOLVIMENTO:
   - Desenvolva as ideias selecionadas
   - Crie exemplos concretos

5. PLANO DE AÇÃO:
   - Como implementar?
   - Métricas de sucesso?

Vamos desenvolver passo a passo:
"""
```

## Medindo Qualidade do CoT

```python
class CoTEvaluator:
    def evaluate_reasoning(self, cot_response: str) -> dict:
        """Avalia a qualidade do raciocínio Chain-of-Thought"""
        
        scores = {}
        
        # 1. Completude: Todos os passos necessários estão presentes?
        scores['completeness'] = self._check_completeness(cot_response)
        
        # 2. Lógica: Os passos seguem logicamente um do outro?
        scores['logic'] = self._check_logic_flow(cot_response)
        
        # 3. Precisão: Cada passo intermediário está correto?
        scores['accuracy'] = self._check_step_accuracy(cot_response)
        
        # 4. Clareza: O raciocínio é fácil de seguir?
        scores['clarity'] = self._check_clarity(cot_response)
        
        # 5. Relevância: Todos os passos são necessários?
        scores['relevance'] = self._check_relevance(cot_response)
        
        scores['overall'] = sum(scores.values()) / len(scores)
        
        return scores
```

## Limitações e Considerações

### Quando CoT Pode Não Ajudar

1. **Tarefas muito simples**: Overhead desnecessário
2. **Respostas criativas abertas**: Estrutura pode limitar criatividade
3. **Limitações de tokens**: CoT consome mais contexto
4. **Tarefas que requerem intuição**: Nem tudo é decomponível

### Cuidados

```python
# ❌ Evite CoT excessivamente rígido
overly_rigid = """
Siga EXATAMENTE estes 15 passos específicos...
[Pode ser muito restritivo]
"""

# ✓ Prefira CoT flexível mas orientado
flexible_cot = """
Pense através do problema usando estas diretrizes:
1. Compreenda o contexto
2. Identifique componentes-chave
3. Analise sistematicamente
4. Sintetize insights
[Permite adaptação ao problema específico]
"""
```

## Combinando CoT com Outras Técnicas

### CoT + Few-shot

```python
combined = """
Veja como resolver problemas similares:

Exemplo 1:
Problema: [problema simples]
Raciocínio: [passos]
Resposta: [solução]

Exemplo 2:
Problema: [problema médio]
Raciocínio: [passos]
Resposta: [solução]

Agora use o mesmo processo de raciocínio:
Problema: {novo_problema}
Raciocínio:
"""
```

### CoT + Role-based

```python
combined_role_cot = """
Você é um analista sênior de dados de RH.

Para cada análise, você segue este processo mental:
1. Contextualização do problema no domínio de RH
2. Identificação de métricas e dados relevantes
3. Aplicação de frameworks de People Analytics
4. Interpretação com sensibilidade organizacional
5. Recomendações alinhadas com estratégia de RH

Análise: {query}

Meu processo de pensamento:
"""
```

## Próximos Passos

Explore como CoT se integra com outras técnicas:

- **[Meta-Prompting](meta-prompting.md)**: Estruture o raciocínio com templates
- **[Advanced Techniques](advanced-techniques.md)**: Tree of Thoughts e outras variações avançadas
- **[Agent Prompting](agent-prompting.md)**: Integre CoT em agentes para raciocínio transparente

## Recursos Adicionais

- Experimente com diferentes níveis de estrutura no CoT
- Documente quais formatos de raciocínio funcionam melhor para diferentes tarefas
- Considere usar CoT especialmente para tarefas críticas onde auditabilidade é importante
- Monitore se o CoT realmente melhora os resultados ou apenas adiciona verbosidade

---

[^1]: [Chain-of-Thought Prompting - Prompt Engineering Guide](https://www.promptingguide.ai/techniques/cot)
