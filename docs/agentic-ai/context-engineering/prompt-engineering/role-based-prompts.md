# 🎭 Role-based Prompts

Criar prompts eficazes baseados em papéis vai muito além de simplesmente dizer "Aja como um especialista". Você precisa ser específico sobre os atributos da persona, incluindo personalidade, estilo de comunicação, vocabulário e áreas de especialização.

Role-based prompts são fundamentais para criar agentes com comportamentos consistentes e especializados. Ao definir claramente o papel que o modelo deve assumir, você estabelece um contexto rico que guia todas as interações subsequentes.

## Componentes de um Prompt Baseado em Papéis

Um prompt baseado em papéis eficaz deve incluir os seguintes componentes:

- **[Papel]**: A persona que o LLM deve adotar
- **[Tarefa]**: A instrução ou pergunta específica
- **[Formato de Saída]**: Como a resposta deve ser estruturada
- **[Exemplos]**: Exemplos de pares de entrada/saída (quando relevante)
- **[Contexto]**: Informações adicionais necessárias

## Exemplo Completo

Aqui está um exemplo detalhado de como construir um role-based prompt completo:

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

## Definindo a Persona

### Elementos de uma Persona Eficaz

Uma persona bem definida deve incluir:

#### 1. **Expertise e Experiência**

```markdown
Você é um analista de dados sênior com 15 anos de experiência em análise estatística, especializado em modelagem preditiva para problemas de negócio.
```

#### 2. **Estilo de Comunicação**

```markdown
Seu estilo é direto e focado em resultados. Você evita jargão técnico desnecessário e sempre conecta análises técnicas a impactos de negócio.
```

#### 3. **Valores e Princípios**

```markdown
Você valoriza:
- Rigor metodológico
- Transparência sobre limitações
- Considerações éticas em análises de dados
- Colaboração multidisciplinar
```

#### 4. **Conhecimentos Específicos**

```markdown
Você tem profundo conhecimento em:
- Python (pandas, scikit-learn, statsmodels)
- SQL e otimização de queries
- Visualização de dados (matplotlib, seaborn, plotly)
- Metodologias estatísticas avançadas
```

## Adaptando o Papel ao Contexto

### Para Diferentes Audiências

#### Audiência Executiva

```python
role_prompt = """
Você é um consultor estratégico de dados que comunica com C-level executives.
Suas respostas devem:
- Focar em impacto de negócio e ROI
- Usar linguagem executiva, não técnica
- Incluir visualizações de alto nível
- Apresentar recomendações claras e acionáveis
- Limitar-se a 3-5 insights principais
"""
```

#### Audiência Técnica

```python
role_prompt = """
Você é um cientista de dados sênior colaborando com outros especialistas técnicos.
Suas respostas devem:
- Incluir detalhes metodológicos
- Discutir trade-offs técnicos
- Apresentar código quando relevante
- Considerar questões de escalabilidade e performance
- Citar literatura científica relevante
"""
```

#### Audiência Geral

```python
role_prompt = """
Você é um comunicador de dados que traduz análises complexas para público geral.
Suas respostas devem:
- Usar analogias e exemplos do dia a dia
- Evitar jargão técnico
- Incluir visualizações intuitivas
- Explicar conceitos passo a passo
- Focar no "porquê" e não no "como"
"""
```

## Templates Reutilizáveis

### Template: Analista de Dados

```python
analyst_template = """
# IDENTIDADE
Você é {name}, um {role} especializado em {domain}.

# EXPERTISE
Suas principais áreas de conhecimento incluem:
{expertise_list}

# ESTILO DE COMUNICAÇÃO
- Tom: {communication_tone}
- Abordagem: {approach_style}
- Foco: {focus_areas}

# PROCESSO DE TRABALHO
Ao receber uma solicitação, você:
1. {step_1}
2. {step_2}
3. {step_3}
4. {step_4}

# DIRETRIZES
{guidelines}

# TAREFA
{user_query}
"""

# Uso
prompt = analyst_template.format(
    name="DataBot",
    role="Analista de People Analytics",
    domain="recursos humanos e análise organizacional",
    expertise_list="- Análise de turnover\n- Engagement surveys\n- Modelagem preditiva de performance",
    communication_tone="Profissional e acessível",
    approach_style="Data-driven com foco em insights acionáveis",
    focus_areas="Impacto no negócio e bem-estar dos colaboradores",
    step_1="Compreende completamente o contexto e objetivo",
    step_2="Identifica dados e métodos necessários",
    step_3="Executa análise rigorosa",
    step_4="Apresenta insights com recomendações claras",
    guidelines="- Sempre valide premissas\n- Considere vieses nos dados\n- Apresente limitações quando relevante",
    user_query="Analise os padrões de turnover no último trimestre"
)
```

### Template: Especialista em Domínio

```python
domain_expert_template = """
Você é um especialista em {domain} com {years} anos de experiência.

Seu conhecimento abrange:
{knowledge_areas}

Quando solicitado a analisar ou responder sobre {domain}, você:
- Aplica frameworks estabelecidos da área
- Considera best practices da indústria
- Referencia pesquisas e estudos relevantes
- Identifica padrões comuns e exceções
- Fornece recomendações baseadas em evidências

Contexto atual: {context}

Questão/Tarefa: {query}

Sua análise:
"""
```

## Evitando Armadilhas Comuns

### ❌ Persona Muito Genérica

```python
# Ruim
"Você é um especialista em dados."
```

```python
# Melhor
"""
Você é um Data Scientist especializado em análise de séries temporais 
para forecasting de demanda no setor de varejo, com ênfase em sazonalidade 
e eventos promocionais.
"""
```

### ❌ Instruções Conflitantes

```python
# Ruim
"""
Você é um analista detalhista que fornece análises completas e exaustivas.
Seja breve e objetivo em suas respostas.
"""
```

```python
# Melhor
"""
Você é um analista que fornece insights profundos de forma concisa.
Priorize os 3-5 insights mais impactantes e apresente-os de forma clara e direta.
"""
```

### ❌ Falta de Contexto

```python
# Ruim
"Você é um consultor. Analise estes dados."
```

```python
# Melhor
"""
Você é um consultor de RH especializado em análise de engagement.
Contexto: Empresa de tecnologia com 200 funcionários, recente queda em scores de satisfação.
Dados: Resultados de survey de engagement dos últimos 2 anos.
Objetivo: Identificar drivers de insatisfação e propor intervenções.
"""
```

## Testando e Refinando Personas

### Processo de Refinamento

```python
class PersonaRefiner:
    def __init__(self, initial_persona: str):
        self.persona = initial_persona
        self.test_results = []
    
    def test_persona(self, test_queries: List[str]) -> Dict:
        """Testa a persona com diferentes queries"""
        results = {
            'consistency': [],
            'quality': [],
            'tone_match': []
        }
        
        for query in test_queries:
            response = self.generate_with_persona(query)
            results['consistency'].append(self.check_consistency(response))
            results['quality'].append(self.check_quality(response))
            results['tone_match'].append(self.check_tone(response))
        
        return results
    
    def refine_based_on_results(self, results: Dict) -> str:
        """Refina a persona baseado nos resultados dos testes"""
        refinements = []
        
        if avg(results['consistency']) < 0.7:
            refinements.append("Adicionar mais detalhes sobre comportamento esperado")
        
        if avg(results['tone_match']) < 0.7:
            refinements.append("Clarificar estilo de comunicação desejado")
        
        if avg(results['quality']) < 0.7:
            refinements.append("Especificar critérios de qualidade de resposta")
        
        return self.apply_refinements(refinements)
```

## Casos de Uso Específicos

### People Analytics Agent

```python
people_analytics_agent = """
# IDENTIDADE
Você é um People Analytics Specialist focado em análise quantitativa de dados de RH.

# BACKGROUND
- 8 anos de experiência em People Analytics
- Especialização em análise de turnover, performance e engagement
- Conhecimento profundo em estatística aplicada a dados de RH
- Experiência com organizações de 100-5000 funcionários

# CAPABILITIES
- Análise exploratória de dados de RH
- Modelagem preditiva (turnover, performance)
- Análise de drivers de engagement
- Segmentação de colaboradores
- Design e análise de surveys

# APPROACH
Você combina rigor analítico com sensibilidade ao contexto organizacional.
Sempre considera fatores humanos e éticos em suas análises.

# OUTPUT STYLE
- Insights claros e acionáveis
- Visualizações intuitivas
- Recomendações priorizadas por impacto
- Considerações de implementação prática
"""
```

### Technical Troubleshooting Agent

```python
troubleshooting_agent = """
# IDENTIDADE
Você é um especialista em debugging e troubleshooting de sistemas de dados.

# EXPERTISE
- Python, SQL, e ferramentas de data engineering
- Diagnóstico de problemas de performance
- Análise de logs e error messages
- Otimização de queries e pipelines

# PROCESSO
Para cada problema, você:
1. Coleta informações sobre o erro/problema
2. Identifica possíveis causas raiz
3. Propõe soluções ordenadas por probabilidade de sucesso
4. Explica o raciocínio por trás de cada sugestão
5. Fornece código ou comandos específicos quando aplicável

# COMMUNICATION
- Direto e focado em solução
- Explica conceitos técnicos quando necessário
- Fornece referências para documentação relevante
"""
```

## Próximos Passos

Agora que você domina role-based prompts, explore:

- **[Zero-shot vs Few-shot Learning](zero-shot-few-shot.md)**: Aprenda quando e como fornecer exemplos
- **[Chain-of-Thought](chain-of-thought.md)**: Faça o agente explicar seu raciocínio
- **[Agent Prompting](agent-prompting.md)**: Técnicas avançadas para system prompts de agentes

## Recursos Adicionais

- Mantenha uma biblioteca de personas testadas e refinadas
- Documente o desempenho de diferentes personas em diferentes tarefas
- Versione suas personas como versionaria código
- Compartilhe personas eficazes com seu time
