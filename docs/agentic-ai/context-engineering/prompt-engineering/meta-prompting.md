# 🔄 Meta-Prompting

**Meta-prompting** é uma técnica avançada que foca na estrutura abstrata da tarefa, usando instruções ou modelos sintáticos que guiam o formato e a qualidade da resposta[^2]. Em vez de instruções específicas para cada tarefa, meta-prompting cria templates reutilizáveis que podem ser aplicados a múltiplos contextos.

## O que é Meta-Prompting?

Meta-prompting opera em um nível de abstração superior ao prompting tradicional. Enquanto um prompt normal diz "faça X", um meta-prompt diz "sempre que você fizer algo do tipo Y, use esta estrutura Z".

### Diferença entre Prompting e Meta-Prompting

**Prompting Tradicional:**

```python
"Analise os dados de turnover e forneça insights."
```

**Meta-Prompting:**

```python
"""
Para qualquer tarefa de análise, use sempre esta estrutura:

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

Agora aplique esta estrutura para: analise os dados de turnover
"""
```

## Template Básico de Meta-Prompt

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

## Meta-Prompts para Diferentes Tipos de Tarefa

### Meta-Prompt para Análise

```python
analysis_meta_prompt = """
Use este padrão para todas as análises:

1. CONTEXTO: Situação atual
   - Background relevante
   - Stakeholders envolvidos
   - Objetivos do negócio

2. DADOS: Informações disponíveis
   - Fontes de dados
   - Período analisado
   - Limitações conhecidas

3. ANÁLISE: Processamento dos dados
   - Metodologia aplicada
   - Cálculos realizados
   - Validações executadas

4. INSIGHTS: Descobertas principais
   - Padrões identificados
   - Anomalias ou exceções
   - Correlações relevantes

5. AÇÕES: Próximos passos
   - Recomendações priorizadas
   - Quick wins
   - Iniciativas de longo prazo

Aplique este framework para: {task}
"""
```

### Meta-Prompt para Resolução de Problemas

```python
problem_solving_meta_prompt = """
Use este padrão para resolução de problemas:

1. PROBLEMA: Definição clara
   - Sintoma observado
   - Impacto atual
   - Urgência (baixa/média/alta)

2. CAUSAS: Possíveis causas raiz
   - Hipótese 1: [descrição + probabilidade]
   - Hipótese 2: [descrição + probabilidade]
   - Hipótese 3: [descrição + probabilidade]

3. SOLUÇÕES: Alternativas disponíveis
   - Solução A: [descrição + prós/contras]
   - Solução B: [descrição + prós/contras]
   - Solução C: [descrição + prós/contras]

4. AVALIAÇÃO: Prós e contras
   - Critérios de decisão
   - Scoring de cada solução
   - Análise de riscos

5. DECISÃO: Recomendação final
   - Solução escolhida
   - Justificativa
   - Plano de implementação

Problema a resolver: {problem}
"""
```

### Meta-Prompt para Tarefas Criativas

```python
creative_meta_prompt = """
Use este padrão para tarefas criativas:

1. INSPIRAÇÃO: Fontes de ideias
   - Referências existentes
   - Tendências relevantes
   - Insights do público-alvo

2. CONCEITO: Ideia central
   - Mensagem principal
   - Ângulo único
   - Proposta de valor

3. DESENVOLVIMENTO: Elaboração
   - Variações do conceito
   - Elementos visuais/textuais
   - Storytelling

4. REFINAMENTO: Melhorias
   - Feedback incorporado
   - Otimizações
   - Polimento final

5. APRESENTAÇÃO: Resultado final
   - Conceito finalizado
   - Rationale criativo
   - Próximos passos de execução

Tarefa criativa: {task}
"""
```

## Meta-Prompts Dinâmicos

Selecione automaticamente o template baseado no tipo de tarefa:

```python
def generate_meta_prompt(task_type: str, task_description: str) -> str:
    """
    Gera um meta-prompt apropriado baseado no tipo de tarefa
    """
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
        """,
        
        "comparison": """
        Use este padrão para comparações:
        1. OPÇÕES: Liste todas as alternativas
        2. CRITÉRIOS: Defina parâmetros de avaliação
        3. AVALIAÇÃO: Avalie cada opção
        4. MATRIZ: Crie comparação sistemática
        5. RECOMENDAÇÃO: Melhor escolha com justificativa
        """,
        
        "planning": """
        Use este padrão para planejamento:
        1. OBJETIVO: Meta clara e mensurável
        2. SITUAÇÃO ATUAL: Estado presente
        3. GAP ANALYSIS: Diferença entre atual e objetivo
        4. ESTRATÉGIA: Abordagem geral
        5. PLANO DE AÇÃO: Passos específicos com timeline
        """
    }
    
    template = templates.get(task_type, templates["analysis"])
    return f"{template}\n\nTarefa: {task_description}"


# Uso
prompt = generate_meta_prompt(
    task_type="analysis",
    task_description="Analise os dados de engagement do último trimestre"
)
```

## Sistema de Meta-Prompting em Camadas

Crie hierarquias de meta-prompts para diferentes níveis de abstração:

```python
class LayeredMetaPrompt:
    def __init__(self):
        # Camada 1: Princípios fundamentais
        self.principles = """
        PRINCÍPIOS FUNDAMENTAIS:
        - Precisão: Base as respostas em dados
        - Clareza: Comunique de forma acessível
        - Acionabilidade: Foque em insights implementáveis
        - Contexto: Considere sempre o contexto organizacional
        """
        
        # Camada 2: Estrutura geral
        self.general_structure = """
        ESTRUTURA GERAL:
        1. Compreensão da solicitação
        2. Análise sistemática
        3. Síntese de insights
        4. Recomendações práticas
        """
        
        # Camada 3: Templates específicos por tipo
        self.specific_templates = {
            "quantitative": """
            ANÁLISE QUANTITATIVA:
            - Estatísticas descritivas
            - Visualizações relevantes
            - Testes de significância
            - Intervalos de confiança
            """,
            
            "qualitative": """
            ANÁLISE QUALITATIVA:
            - Temas principais
            - Citações representativas
            - Padrões emergentes
            - Nuances contextuais
            """
        }
    
    def build_prompt(self, task: str, analysis_type: str) -> str:
        """Constrói um prompt usando todas as camadas"""
        return f"""
        {self.principles}
        
        {self.general_structure}
        
        {self.specific_templates[analysis_type]}
        
        TAREFA: {task}
        
        Execute seguindo os princípios, estrutura e template acima.
        """
```

## Meta-Prompts para Consistência

Use meta-prompts para garantir respostas consistentes:

```python
consistency_meta_prompt = """
FORMATO PADRÃO DE RESPOSTA:

Toda resposta deve seguir esta estrutura:

📊 RESUMO EXECUTIVO
[2-3 frases resumindo o principal]

🔍 ANÁLISE DETALHADA
[Desenvolvimento completo da análise]

💡 INSIGHTS PRINCIPAIS
• Insight 1
• Insight 2
• Insight 3

✅ RECOMENDAÇÕES
1. Recomendação prioritária [impacto: alto/médio/baixo]
2. Recomendação secundária [impacto: alto/médio/baixo]
3. Recomendação terciária [impacto: alto/médio/baixo]

⚠️ CONSIDERAÇÕES
[Limitações, riscos ou pontos de atenção]

📈 PRÓXIMOS PASSOS
[Ações concretas e timeline sugerido]

---

Agora aplique este formato para: {query}
"""
```

## Meta-Prompts Adaptativos

Ajuste automaticamente baseado no contexto:

```python
class AdaptiveMetaPrompt:
    def __init__(self):
        self.audience_styles = {
            "executive": {
                "tone": "Alto nível, focado em impacto de negócio",
                "length": "Conciso, máximo 3 insights principais",
                "format": "Bullet points e visualizações"
            },
            "technical": {
                "tone": "Detalhado, metodologicamente rigoroso",
                "length": "Completo, incluindo detalhes técnicos",
                "format": "Seções estruturadas com código/fórmulas"
            },
            "general": {
                "tone": "Acessível, evitando jargão",
                "length": "Moderado, explicações claras",
                "format": "Narrativo com exemplos práticos"
            }
        }
    
    def build_adaptive_prompt(self, task: str, audience: str, complexity: str) -> str:
        style = self.audience_styles[audience]
        
        prompt = f"""
        CONTEXTO:
        - Audiência: {audience}
        - Tom: {style['tone']}
        - Extensão: {style['length']}
        - Formato: {style['format']}
        - Complexidade da tarefa: {complexity}
        
        DIRETRIZES ESPECÍFICAS:
        """
        
        if audience == "executive":
            prompt += """
            - Comece com o bottom line
            - Foque em ROI e impacto de negócio
            - Use visualizações sempre que possível
            - Máximo 5 minutos de leitura
            """
        elif audience == "technical":
            prompt += """
            - Detalhe a metodologia
            - Inclua código ou fórmulas quando relevante
            - Discuta limitações e premissas
            - Cite referências técnicas
            """
        else:
            prompt += """
            - Use linguagem clara e acessível
            - Inclua exemplos práticos
            - Explique conceitos técnicos quando necessário
            - Mantenha foco em aplicabilidade prática
            """
        
        prompt += f"\n\nTAREFA: {task}\n"
        
        return prompt
```

## Meta-Prompts para Validação

Crie meta-prompts que incluem auto-validação:

```python
validation_meta_prompt = """
Execute a tarefa seguindo este processo com validação integrada:

1. EXECUÇÃO INICIAL
   [Realize a tarefa solicitada]

2. AUTO-VALIDAÇÃO
   Verifique:
   ✓ A resposta está completa?
   ✓ Os dados/cálculos estão corretos?
   ✓ A lógica está sólida?
   ✓ Há vieses ou premissas não declaradas?
   ✓ As recomendações são acionáveis?

3. REFINAMENTO
   [Se algum item da validação falhou, corrija]

4. RESPOSTA FINAL
   [Apresente a versão validada e refinada]

5. CONFIANÇA
   Nível de confiança: [1-10]
   Razão: [Justifique o nível]

Tarefa: {task}
"""
```

## Biblioteca de Meta-Prompts

Organize meta-prompts reutilizáveis:

```python
class MetaPromptLibrary:
    def __init__(self):
        self.library = {
            "data_analysis": {
                "exploratory": self._exploratory_analysis_template(),
                "diagnostic": self._diagnostic_analysis_template(),
                "predictive": self._predictive_analysis_template()
            },
            "communication": {
                "report": self._report_template(),
                "presentation": self._presentation_template(),
                "email": self._email_template()
            },
            "decision_support": {
                "comparison": self._comparison_template(),
                "prioritization": self._prioritization_template(),
                "risk_assessment": self._risk_assessment_template()
            }
        }
    
    def _exploratory_analysis_template(self) -> str:
        return """
        ANÁLISE EXPLORATÓRIA:
        1. Overview dos dados
        2. Distribuições e estatísticas descritivas
        3. Identificação de padrões
        4. Detecção de anomalias
        5. Correlações iniciais
        6. Hipóteses para investigação futura
        """
    
    def _diagnostic_analysis_template(self) -> str:
        return """
        ANÁLISE DIAGNÓSTICA:
        1. Definição do problema/pergunta
        2. Hipóteses de causas
        3. Testes de cada hipótese
        4. Evidências encontradas
        5. Conclusão sobre causa raiz
        6. Validação da conclusão
        """
    
    def get_meta_prompt(self, category: str, type: str, task: str) -> str:
        template = self.library[category][type]
        return f"{template}\n\nTarefa específica: {task}"


# Uso
library = MetaPromptLibrary()
prompt = library.get_meta_prompt(
    category="data_analysis",
    type="exploratory",
    task="Analise os dados de turnover do último ano"
)
```

## Meta-Prompts para Diferentes Domínios

### People Analytics

```python
people_analytics_meta = """
FRAMEWORK DE PEOPLE ANALYTICS:

Para qualquer análise de dados de RH, use esta estrutura:

1. CONTEXTO ORGANIZACIONAL
   - Tamanho da organização
   - Indústria/setor
   - Fase da empresa
   - Cultura organizacional relevante

2. MÉTRICA EM FOCO
   - Definição precisa
   - Como é calculada
   - Benchmark da indústria
   - Histórico interno

3. ANÁLISE MULTIDIMENSIONAL
   - Por departamento
   - Por nível hierárquico
   - Por tenure
   - Por localização
   - Por demografia (quando ético e legal)

4. FATORES INFLUENCIADORES
   - Fatores internos
   - Fatores externos
   - Correlações identificadas
   - Causalidade (quando comprovável)

5. IMPLICAÇÕES
   - Impacto em outras métricas
   - Implicações de negócio
   - Riscos associados
   - Oportunidades

6. AÇÕES RECOMENDADAS
   - Intervenções sugeridas
   - Priorização por impacto
   - Recursos necessários
   - Timeline esperado

Análise: {query}
"""
```

### Financial Analysis

```python
financial_meta = """
FRAMEWORK DE ANÁLISE FINANCEIRA:

1. CONTEXTO FINANCEIRO
   - Período analisado
   - Condições de mercado
   - Eventos relevantes

2. MÉTRICAS CHAVE
   - Valores absolutos
   - Variações percentuais
   - Comparação com período anterior
   - Comparação com budget/forecast

3. DRIVERS DE PERFORMANCE
   - Fatores que explicam variações
   - Impacto quantificado de cada fator
   - Tendências identificadas

4. ANÁLISE DE RISCOS
   - Riscos identificados
   - Probabilidade e impacto
   - Mitigações sugeridas

5. PROJEÇÕES
   - Cenário base
   - Cenário otimista
   - Cenário pessimista
   - Premissas de cada cenário

Análise: {query}
"""
```

## Testando e Refinando Meta-Prompts

```python
class MetaPromptTester:
    def test_meta_prompt(self, meta_prompt: str, test_cases: list) -> dict:
        """
        Testa um meta-prompt com múltiplos casos de teste
        """
        results = []
        
        for case in test_cases:
            # Aplica o meta-prompt ao caso de teste
            full_prompt = meta_prompt.format(task=case['input'])
            response = llm.generate(full_prompt)
            
            # Avalia a resposta
            evaluation = {
                'test_case': case['name'],
                'follows_structure': self._check_structure(response, meta_prompt),
                'quality': self._evaluate_quality(response),
                'consistency': self._check_consistency(response, previous_responses)
            }
            
            results.append(evaluation)
        
        return self._summarize_results(results)
    
    def _check_structure(self, response: str, meta_prompt: str) -> bool:
        """Verifica se a resposta seguiu a estrutura do meta-prompt"""
        # Extrai seções esperadas do meta-prompt
        expected_sections = self._extract_sections(meta_prompt)
        
        # Verifica presença de cada seção na resposta
        for section in expected_sections:
            if section not in response:
                return False
        
        return True
```

## Vantagens do Meta-Prompting

### 1. Reutilização

Um meta-prompt bem projetado pode ser usado para centenas de tarefas similares.

### 2. Consistência

Garante que todas as respostas sigam o mesmo formato e qualidade.

### 3. Escalabilidade

Permite que múltiplos usuários ou agentes produzam outputs padronizados.

### 4. Manutenibilidade

Atualizar um meta-prompt atualiza o comportamento em todas as aplicações.

### 5. Qualidade

A estrutura forçada frequentemente resulta em respostas mais completas e bem pensadas.

## Próximos Passos

Explore como meta-prompting se integra com outras técnicas:

- **[Chain-of-Thought](chain-of-thought.md)**: Integre CoT em seus meta-prompts para raciocínio estruturado
- **[Advanced Techniques](advanced-techniques.md)**: Combine meta-prompting com técnicas avançadas
- **[Best Practices](best-practices.md)**: Aprenda a versionar e manter bibliotecas de meta-prompts

## Recursos Adicionais

- Crie uma biblioteca de meta-prompts testados e validados
- Documente quando cada meta-prompt deve ser usado
- Estabeleça processo de revisão e atualização de meta-prompts
- Compartilhe meta-prompts eficazes com seu time

---

[^2]: [Meta Prompting - Prompt Engineering Guide](https://www.promptingguide.ai/techniques/meta-prompting)
