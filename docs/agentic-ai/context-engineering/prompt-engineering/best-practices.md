# 🎯 Boas Práticas em Prompt Engineering

Desenvolver prompts eficazes é tanto arte quanto ciência. Este guia consolida as melhores práticas para criar, manter e evoluir seus prompts de forma sistemática e sustentável.

## Princípios Fundamentais

### 1. Clareza Acima de Tudo

```python
# ❌ Ruim: Ambíguo e vago
prompt = "Analise isso"

# ✅ Bom: Claro e específico
prompt = """
Como analista de People Analytics, examine os dados de turnover abaixo.

Forneça:
1. Taxa de turnover por departamento
2. Tendências nos últimos 12 meses
3. Fatores de risco identificados
4. Recomendações prioritárias

Dados: {data}
"""
```

### 2. Seja Específico nas Instruções

```python
# ❌ Ruim: Instruções vagas
prompt = "Faça um relatório bom"

# ✅ Bom: Instruções precisas
prompt = """
Crie um relatório executivo com:

Formato:
- Máximo 2 páginas
- Seções: Resumo, Análise, Recomendações
- Tom: Profissional e objetivo
- Incluir 2-3 visualizações

Estrutura do resumo:
- 3-5 bullet points
- Foco em insights acionáveis
- Quantificar impacto quando possível
"""
```

### 3. Forneça Contexto Adequado

```python
# ❌ Ruim: Sem contexto
prompt = "Classifique este feedback: {feedback}"

# ✅ Bom: Contexto rico
prompt = """
Contexto: Você está analisando feedback de saída de ex-funcionários de uma empresa de tecnologia com 500+ pessoas.

Objetivo: Identificar padrões que possam indicar problemas sistêmicos que afetam retenção.

Tarefa: Classifique o seguinte feedback nas categorias:
- Cultura
- Liderança
- Compensação
- Desenvolvimento de carreira
- Work-life balance
- Outros

Feedback: {feedback}

Categoria:
"""
```

## Desenvolvimento Iterativo

### Framework de Iteração

```python
class PromptDevelopmentCycle:
    def __init__(self):
        self.iterations = []
        self.current_version = None
    
    def iterate(self, prompt: str, test_results: dict, changes_made: str):
        """Registra uma iteração do desenvolvimento"""
        version = len(self.iterations) + 1
        
        self.iterations.append({
            'version': version,
            'prompt': prompt,
            'test_results': test_results,
            'changes_made': changes_made,
            'timestamp': datetime.now()
        })
        
        self.current_version = prompt
    
    def analyze_progress(self) -> dict:
        """Analisa evolução ao longo das iterações"""
        if len(self.iterations) < 2:
            return {'insufficient_data': True}
        
        # Compara scores entre versões
        scores = [iter['test_results']['overall_score'] for iter in self.iterations]
        
        return {
            'total_iterations': len(self.iterations),
            'score_improvement': scores[-1] - scores[0],
            'best_version': max(self.iterations, key=lambda x: x['test_results']['overall_score']),
            'iteration_history': [
                {
                    'version': iter['version'],
                    'score': iter['test_results']['overall_score'],
                    'changes': iter['changes_made']
                }
                for iter in self.iterations
            ]
        }
    
    def rollback_to_version(self, version: int):
        """Reverte para uma versão anterior"""
        if version < 1 or version > len(self.iterations):
            raise ValueError(f"Invalid version: {version}")
        
        self.current_version = self.iterations[version - 1]['prompt']
        return self.current_version
```

### Processo de Iteração

```python
# Exemplo de desenvolvimento iterativo
dev_cycle = PromptDevelopmentCycle()

# Versão 1: Baseline
v1_prompt = "Analise os dados de turnover: {data}"
v1_results = {'overall_score': 0.5}
dev_cycle.iterate(v1_prompt, v1_results, "Versão inicial")

# Versão 2: Adiciona estrutura
v2_prompt = """
Analise os dados de turnover e forneça:
1. Taxa geral
2. Tendências
3. Recomendações

Dados: {data}
"""
v2_results = {'overall_score': 0.7}
dev_cycle.iterate(v2_prompt, v2_results, "Adicionou estrutura clara")

# Versão 3: Adiciona contexto e papel
v3_prompt = """
Como analista sênior de People Analytics, analise os dados de turnover abaixo.

Forneça uma análise estruturada:

1. **Métricas-chave**
   - Taxa de turnover geral
   - Breakdown por departamento
   - Comparação com período anterior

2. **Análise de Tendências**
   - Padrões temporais
   - Segmentações relevantes
   
3. **Recomendações Prioritárias**
   - Top 3 ações
   - Impacto esperado
   - Quick wins

Dados: {data}
"""
v3_results = {'overall_score': 0.85}
dev_cycle.iterate(v3_prompt, v3_results, "Adicionou papel e detalhamento")

# Analisa progresso
progress = dev_cycle.analyze_progress()
print(f"Melhoria total: {progress['score_improvement']}")
```

## Versionamento de Prompts

### Sistema de Versionamento

```python
from typing import Optional
import hashlib

class PromptVersionManager:
    def __init__(self):
        self.versions = {}
        self.tags = {}
    
    def save_version(
        self, 
        prompt_id: str,
        prompt: str,
        description: str,
        metadata: Optional[dict] = None
    ) -> str:
        """Salva uma nova versão do prompt"""
        
        # Gera hash do conteúdo
        content_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        
        # Define número de versão
        if prompt_id not in self.versions:
            self.versions[prompt_id] = []
            version_num = 1
        else:
            version_num = len(self.versions[prompt_id]) + 1
        
        version_id = f"{prompt_id}_v{version_num}_{content_hash}"
        
        version_data = {
            'id': version_id,
            'version_number': version_num,
            'prompt': prompt,
            'description': description,
            'metadata': metadata or {},
            'created_at': datetime.now(),
            'hash': content_hash
        }
        
        self.versions[prompt_id].append(version_data)
        
        return version_id
    
    def tag_version(self, version_id: str, tag: str):
        """Marca uma versão com tag (e.g., 'production', 'staging')"""
        self.tags[tag] = version_id
    
    def get_version(self, version_id: str) -> dict:
        """Recupera uma versão específica"""
        for prompt_id, versions in self.versions.items():
            for version in versions:
                if version['id'] == version_id:
                    return version
        
        raise ValueError(f"Version not found: {version_id}")
    
    def get_by_tag(self, tag: str) -> dict:
        """Recupera versão por tag"""
        if tag not in self.tags:
            raise ValueError(f"Tag not found: {tag}")
        
        return self.get_version(self.tags[tag])
    
    def list_versions(self, prompt_id: str) -> list:
        """Lista todas as versões de um prompt"""
        return self.versions.get(prompt_id, [])
    
    def compare_versions(self, version_id1: str, version_id2: str) -> dict:
        """Compara duas versões"""
        v1 = self.get_version(version_id1)
        v2 = self.get_version(version_id2)
        
        return {
            'version_1': {
                'id': v1['id'],
                'created': v1['created_at'],
                'description': v1['description']
            },
            'version_2': {
                'id': v2['id'],
                'created': v2['created_at'],
                'description': v2['description']
            },
            'prompt_diff': self._get_diff(v1['prompt'], v2['prompt'])
        }
    
    def _get_diff(self, text1: str, text2: str) -> str:
        """Gera diff entre dois textos"""
        import difflib
        
        diff = difflib.unified_diff(
            text1.splitlines(keepends=True),
            text2.splitlines(keepends=True),
            lineterm=''
        )
        
        return ''.join(diff)
```

### Exemplo de Uso

```python
# Inicializa gerenciador
vm = PromptVersionManager()

# Salva primeira versão
v1_id = vm.save_version(
    prompt_id="turnover_analysis",
    prompt="Analise turnover: {data}",
    description="Versão inicial simples"
)

# Salva versão melhorada
v2_prompt = """
Como analista de People Analytics, analise o turnover:

Forneça:
1. Métricas principais
2. Tendências
3. Recomendações

Dados: {data}
"""

v2_id = vm.save_version(
    prompt_id="turnover_analysis",
    prompt=v2_prompt,
    description="Adicionou estrutura e papel",
    metadata={'tested': True, 'avg_score': 0.85}
)

# Marca versão aprovada para produção
vm.tag_version(v2_id, "production")

# Recupera versão de produção
prod_version = vm.get_by_tag("production")
print(f"Prompt de produção (v{prod_version['version_number']}):")
print(prod_version['prompt'])

# Compara versões
comparison = vm.compare_versions(v1_id, v2_id)
print("\nDiferenças:")
print(comparison['prompt_diff'])
```

## Biblioteca de Prompts

### Estrutura de Biblioteca

```python
from typing import Dict, List, Callable

class PromptLibrary:
    def __init__(self):
        self.prompts = {}
        self.categories = {}
        self.templates = {}
    
    def register_prompt(
        self,
        name: str,
        prompt: str,
        category: str,
        description: str,
        parameters: List[str],
        examples: List[dict] = None,
        metadata: dict = None
    ):
        """Registra um prompt na biblioteca"""
        
        self.prompts[name] = {
            'prompt': prompt,
            'category': category,
            'description': description,
            'parameters': parameters,
            'examples': examples or [],
            'metadata': metadata or {},
            'usage_count': 0
        }
        
        # Organiza por categoria
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(name)
    
    def get_prompt(self, name: str, **kwargs) -> str:
        """Recupera e formata um prompt"""
        
        if name not in self.prompts:
            raise ValueError(f"Prompt not found: {name}")
        
        prompt_data = self.prompts[name]
        
        # Valida parâmetros
        missing = [p for p in prompt_data['parameters'] if p not in kwargs]
        if missing:
            raise ValueError(f"Missing parameters: {missing}")
        
        # Incrementa contador de uso
        prompt_data['usage_count'] += 1
        
        # Formata prompt
        return prompt_data['prompt'].format(**kwargs)
    
    def search_prompts(self, query: str) -> List[str]:
        """Busca prompts por palavra-chave"""
        results = []
        
        query_lower = query.lower()
        
        for name, data in self.prompts.items():
            if (query_lower in name.lower() or 
                query_lower in data['description'].lower() or
                query_lower in data['category'].lower()):
                results.append(name)
        
        return results
    
    def list_by_category(self, category: str) -> List[str]:
        """Lista prompts por categoria"""
        return self.categories.get(category, [])
    
    def get_popular_prompts(self, top_n: int = 10) -> List[tuple]:
        """Retorna os prompts mais utilizados"""
        sorted_prompts = sorted(
            self.prompts.items(),
            key=lambda x: x[1]['usage_count'],
            reverse=True
        )
        
        return [(name, data['usage_count']) for name, data in sorted_prompts[:top_n]]
    
    def register_template(self, name: str, generator: Callable):
        """Registra um gerador de prompts"""
        self.templates[name] = generator
    
    def generate_from_template(self, template_name: str, **kwargs) -> str:
        """Gera prompt a partir de template"""
        if template_name not in self.templates:
            raise ValueError(f"Template not found: {template_name}")
        
        return self.templates[template_name](**kwargs)
```

### Populando a Biblioteca

```python
# Inicializa biblioteca
library = PromptLibrary()

# Registra prompts comuns
library.register_prompt(
    name="classification_basic",
    prompt="""
Classifique o seguinte item na categoria mais apropriada.

Categorias possíveis: {categories}

Item: {item}

Categoria:
""",
    category="Classification",
    description="Classificação básica com categorias predefinidas",
    parameters=["categories", "item"],
    examples=[
        {
            "input": {"categories": "Positivo, Negativo, Neutro", "item": "Adorei!"},
            "output": "Positivo"
        }
    ]
)

library.register_prompt(
    name="data_analysis_structured",
    prompt="""
Como analista de {domain}, analise os dados abaixo.

Forneça uma análise estruturada:

1. **Resumo Executivo**
   - Principais findings
   - Impacto no negócio
   
2. **Análise Detalhada**
   - Métricas-chave
   - Tendências identificadas
   - Segmentações relevantes
   
3. **Recomendações**
   - Ações prioritárias
   - Próximos passos
   - Métricas de acompanhamento

Dados: {data}
""",
    category="Data Analysis",
    description="Análise estruturada de dados com foco em insights acionáveis",
    parameters=["domain", "data"],
    metadata={"recommended_for": ["people_analytics", "business_intelligence"]}
)

library.register_prompt(
    name="summarization_executive",
    prompt="""
Crie um resumo executivo do seguinte conteúdo.

Requisitos:
- Máximo {max_length} palavras
- Foco em {focus_areas}
- Tom: {tone}
- Audiência: {audience}

Conteúdo: {content}

Resumo:
""",
    category="Summarization",
    description="Resumo executivo customizável",
    parameters=["max_length", "focus_areas", "tone", "audience", "content"]
)

# Uso da biblioteca
prompt = library.get_prompt(
    "data_analysis_structured",
    domain="People Analytics",
    data="Turnover Q1: 12%, Q2: 15%, Q3: 18%"
)

print(prompt)

# Busca prompts
results = library.search_prompts("analysis")
print(f"\nPrompts de análise: {results}")

# Prompts mais populares
popular = library.get_popular_prompts(top_n=5)
print(f"\nMais usados: {popular}")
```

### Templates Dinâmicos

```python
# Registra template gerador
def generate_multi_step_analysis(steps: List[str], context: str) -> str:
    """Gera prompt de análise multi-etapa"""
    
    steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
    
    return f"""
Contexto: {context}

Execute a análise nas seguintes etapas:

{steps_text}

Para cada etapa:
- Apresente findings claros
- Justifique sua análise
- Conecte com a etapa seguinte

Dados: {{data}}
"""

library.register_template("multi_step_analysis", generate_multi_step_analysis)

# Usa template
prompt = library.generate_from_template(
    "multi_step_analysis",
    steps=[
        "Calcule taxa de turnover por departamento",
        "Identifique departamentos com turnover acima da média",
        "Analise causas potenciais para turnover elevado",
        "Proponha ações corretivas específicas"
    ],
    context="Análise trimestral de turnover para identificar áreas de risco"
)

print(prompt)
```

## Testes e Validação

### Checklist de Validação

```python
class PromptValidator:
    def __init__(self):
        self.checks = [
            self._check_clarity,
            self._check_specificity,
            self._check_context,
            self._check_structure,
            self._check_examples
        ]
    
    def validate(self, prompt: str) -> dict:
        """Executa todos os checks de validação"""
        results = {}
        
        for check in self.checks:
            check_name = check.__name__.replace('_check_', '')
            results[check_name] = check(prompt)
        
        results['passed'] = all(r['passed'] for r in results.values())
        results['score'] = sum(r['score'] for r in results.values()) / len(results)
        
        return results
    
    def _check_clarity(self, prompt: str) -> dict:
        """Verifica clareza das instruções"""
        issues = []
        
        # Check: Evita palavras vagas
        vague_words = ['bom', 'melhor', 'adequado', 'apropriado', 'isso', 'aquilo']
        found_vague = [w for w in vague_words if w in prompt.lower()]
        if found_vague:
            issues.append(f"Palavras vagas encontradas: {found_vague}")
        
        # Check: Tem instruções claras
        if '?' not in prompt and 'forneça' not in prompt.lower() and 'analise' not in prompt.lower():
            issues.append("Sem instrução clara identificada")
        
        return {
            'passed': len(issues) == 0,
            'score': 1.0 if len(issues) == 0 else 0.5,
            'issues': issues
        }
    
    def _check_specificity(self, prompt: str) -> dict:
        """Verifica especificidade"""
        issues = []
        
        # Check: Define formato esperado
        format_indicators = ['formato:', 'estrutura:', 'forneça:', 'inclua:']
        has_format = any(ind in prompt.lower() for ind in format_indicators)
        if not has_format:
            issues.append("Formato de saída não especificado")
        
        return {
            'passed': len(issues) == 0,
            'score': 1.0 if len(issues) == 0 else 0.7,
            'issues': issues
        }
    
    def _check_context(self, prompt: str) -> dict:
        """Verifica se há contexto adequado"""
        issues = []
        
        # Check: Fornece contexto
        context_indicators = ['contexto:', 'background:', 'situação:', 'como']
        has_context = any(ind in prompt.lower() for ind in context_indicators)
        if not has_context:
            issues.append("Contexto não fornecido")
        
        return {
            'passed': len(issues) == 0,
            'score': 1.0 if len(issues) == 0 else 0.6,
            'issues': issues
        }
    
    def _check_structure(self, prompt: str) -> dict:
        """Verifica estrutura"""
        issues = []
        
        # Check: Usa quebras de linha para legibilidade
        lines = prompt.split('\n')
        if len(lines) < 3:
            issues.append("Prompt muito compacto, considere estruturar melhor")
        
        return {
            'passed': len(issues) == 0,
            'score': 1.0 if len(issues) == 0 else 0.8,
            'issues': issues
        }
    
    def _check_examples(self, prompt: str) -> dict:
        """Verifica se inclui exemplos quando apropriado"""
        # Este é opcional dependendo do caso de uso
        has_example = 'exemplo:' in prompt.lower()
        
        return {
            'passed': True,  # Não falha, apenas informa
            'score': 1.0 if has_example else 0.9,
            'issues': [] if has_example else ["Considere adicionar exemplos"]
        }
```

### Uso do Validador

```python
validator = PromptValidator()

# Valida prompt ruim
bad_prompt = "Analise isso e faça um relatório bom"
results = validator.validate(bad_prompt)

print(f"Passou: {results['passed']}")
print(f"Score: {results['score']:.2f}")
print("\nProblemas encontrados:")
for check, result in results.items():
    if check not in ['passed', 'score'] and result['issues']:
        print(f"  {check}: {result['issues']}")

# Valida prompt bom
good_prompt = """
Contexto: Análise trimestral de turnover para liderança executiva.

Como analista sênior de People Analytics, analise os dados de turnover abaixo.

Forneça um relatório estruturado:

1. **Resumo Executivo** (3-5 bullets)
2. **Análise Detalhada** (métricas e tendências)
3. **Recomendações** (top 3 ações prioritárias)

Formato: Profissional, objetivo, máximo 2 páginas.

Dados: {data}
"""

results = validator.validate(good_prompt)
print(f"\n\nPrompt melhorado - Score: {results['score']:.2f}")
```

## Documentação

### Template de Documentação

```python
class PromptDocumentation:
    def __init__(self, prompt_id: str):
        self.prompt_id = prompt_id
        self.sections = {
            'overview': None,
            'use_cases': [],
            'parameters': {},
            'examples': [],
            'performance': {},
            'notes': []
        }
    
    def document(
        self,
        overview: str,
        use_cases: List[str],
        parameters: Dict[str, str],
        examples: List[dict],
        performance: dict = None,
        notes: List[str] = None
    ):
        """Documenta um prompt"""
        self.sections['overview'] = overview
        self.sections['use_cases'] = use_cases
        self.sections['parameters'] = parameters
        self.sections['examples'] = examples
        self.sections['performance'] = performance or {}
        self.sections['notes'] = notes or []
    
    def generate_markdown(self) -> str:
        """Gera documentação em Markdown"""
        md = f"# {self.prompt_id}\n\n"
        
        # Overview
        md += f"## Overview\n\n{self.sections['overview']}\n\n"
        
        # Use Cases
        md += "## Use Cases\n\n"
        for uc in self.sections['use_cases']:
            md += f"- {uc}\n"
        md += "\n"
        
        # Parameters
        md += "## Parameters\n\n"
        for param, desc in self.sections['parameters'].items():
            md += f"- `{param}`: {desc}\n"
        md += "\n"
        
        # Examples
        md += "## Examples\n\n"
        for i, ex in enumerate(self.sections['examples'], 1):
            md += f"### Example {i}\n\n"
            md += f"**Input:**\n```\n{ex['input']}\n```\n\n"
            md += f"**Output:**\n```\n{ex['output']}\n```\n\n"
        
        # Performance
        if self.sections['performance']:
            md += "## Performance Metrics\n\n"
            for metric, value in self.sections['performance'].items():
                md += f"- {metric}: {value}\n"
            md += "\n"
        
        # Notes
        if self.sections['notes']:
            md += "## Notes\n\n"
            for note in self.sections['notes']:
                md += f"- {note}\n"
        
        return md
```

## Otimização de Custos

### Estratégias de Economia

```python
class PromptOptimizer:
    def __init__(self):
        self.cache = {}
    
    def optimize_for_cost(self, prompt: str) -> str:
        """Otimiza prompt para reduzir tokens"""
        
        optimized = prompt
        
        # Remove espaços extras
        optimized = ' '.join(optimized.split())
        
        # Remove quebras de linha desnecessárias
        optimized = '\n'.join(line.strip() for line in optimized.split('\n') if line.strip())
        
        # Substitui frases longas por versões mais curtas
        replacements = {
            'Por favor, forneça': 'Forneça',
            'Você poderia': '',
            'Seria possível': '',
            'da seguinte forma': 'assim'
        }
        
        for old, new in replacements.items():
            optimized = optimized.replace(old, new)
        
        return optimized
    
    def cache_response(self, prompt: str, response: str):
        """Cacheia respostas para prompts repetidos"""
        import hashlib
        
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
        self.cache[prompt_hash] = response
    
    def get_cached(self, prompt: str) -> Optional[str]:
        """Recupera resposta cacheada se existir"""
        import hashlib
        
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
        return self.cache.get(prompt_hash)
```

## Próximos Passos

Continue aprimorando suas habilidades:

- **[Evaluation](evaluation.md)**: Implemente avaliação sistemática
- **[Advanced Techniques](advanced-techniques.md)**: Explore técnicas sofisticadas
- **[Agent Prompting](agent-prompting.md)**: Aplique em agentes autônomos

## Checklist de Lançamento

Antes de colocar um prompt em produção:

- [ ] Testado com casos de uso diversos
- [ ] Avaliado sistematicamente (score > 0.8)
- [ ] Documentado adequadamente
- [ ] Versionado e commitado
- [ ] Revisado por pares
- [ ] Tem fallback para casos de erro
- [ ] Monitoramento configurado
- [ ] Custos estimados e aprovados

## Recursos Adicionais

- Mantenha um changelog de prompts
- Realize code reviews de prompts importantes
- Estabeleça SLAs de qualidade
- Crie playbooks para casos comuns
- Automatize testes sempre que possível
- Compartilhe aprendizados com o time
