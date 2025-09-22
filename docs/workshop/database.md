# HR Synthetic Database

## 📊 Visão Geral do Dataset

Neste workshop, utilizaremos o **HR Synthetic Database** - um dataset sintético de recursos humanos criado especificamente para demonstrar capacidades de Agentic AI em análises de People Analytics. O dataset está disponível no Hugging Face e modela a estrutura organizacional de uma empresa global de varejo e atacado.

!!! info "Dataset Seguro e Realista"
    Todos os dados são 100% sintéticos, gerados por AI usando o framework LangGraph, garantindo privacidade total enquanto mantém realismo para análises práticas.

## 🏢 Contexto da Empresa

O dataset modela uma **empresa global de varejo e atacado** que opera uma rede diversificada de lojas físicas e plataformas digitais, com as seguintes características:

- **Divisões Principais**: Operações domésticas, mercados internacionais, clubes de atacado por associação
- **Serviços Compartilhados**: RH, Finanças, TI e outras funções corporativas centralizadas  
- **Formatos de Loja**: Supercentros, supermercados, clubes de atacado, outlets cash-and-carry, lojas de desconto
- **Presença Digital**: Múltiplas plataformas de eCommerce, aplicativos móveis, marketplaces regionais e serviços de pagamento digital
- **Produtos**: Foco em mantimentos, produtos essenciais e mercadorias gerais

## 🗄️ Estrutura do Dataset

O dataset é composto por **5 tabelas relacionais** que modelam um sistema de RH completo:

### 📋 Tabelas Principais

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| **business_units** | ~4 | Unidades de negócio de alto nível |
| **departments** | ~15 | Departamentos funcionais dentro das unidades |
| **jobs** | ~200 | Definições e classificações de cargos |
| **employees** | ~1.000 | Dados demográficos e organizacionais dos funcionários |
| **compensations** | ~1.000 | Informações de salário, bônus e remuneração total |

## 📑 Esquema Detalhado das Tabelas

### 🏢 Business Units
Divisões organizacionais principais da empresa.

```
business_units:
├── id (string)               # Identificador único
├── name (string)             # Nome da unidade de negócio
├── description (string)      # Descrição da unidade
└── director_job_id (string)  # Referência ao cargo do diretor
```

### 🏬 Departments  
Unidades funcionais dentro das business units.

```
departments:
├── id (string)               # Identificador único
├── name (string)             # Nome do departamento
├── description (string)      # Descrição do departamento
├── manager_job_id (string)   # Referência ao cargo do gerente
└── business_unit_id (string) # Chave estrangeira para business_units
```

### 💼 Jobs
Definições de cargos e classificações hierárquicas.

```
jobs:
├── id (string)               # Identificador único
├── name (string)             # Título do cargo
├── description (string)      # Descrição do cargo
├── job_level (string)        # Nível hierárquico (Entry, Mid, Senior, Executive)
├── job_family (string)       # Categoria funcional (Engineering, Sales, etc.)
├── contract_type (string)    # Tipo de contrato (Full-time, Part-time, Contract)
└── workplace_type (string)   # Arranjo de trabalho (On-site, Remote, Hybrid)
```

### 👥 Employees
Informações demográficas e organizacionais dos funcionários.

```
employees:
├── id (string)               # Identificador único
├── job_id (string)           # Chave estrangeira para jobs
├── department_id (string)    # Chave estrangeira para departments (nullable)
├── business_unit_id (string) # Chave estrangeira para business_units (nullable)
├── first_name (string)       # Primeiro nome
├── last_name (string)        # Sobrenome
├── birth_date (string)       # Data de nascimento (YYYY-MM-DD)
├── gender (string)           # Identidade de gênero
├── ethnicity (string)        # Origem étnica
├── education_level (string)  # Nível de educação
├── education_field (string)  # Área de estudo
└── generation (string)       # Coorte geracional (Gen Z, Millennial, etc.)
```

### 💰 Compensations
Informações de remuneração e benefícios.

```
compensations:
├── id (string)                      # Identificador único
├── employee_id (string)             # Chave estrangeira para employees
├── annual_base_salary (float)       # Salário base anual
├── annual_bonus_amount (float)      # Bônus anual (nullable)
├── annual_commission_amount (float) # Comissão anual (nullable)
├── rate_type (string)               # Tipo de remuneração (Salary ou Hourly)
└── total_compensation (float)       # Remuneração total anual
```

## 🎯 Casos de Uso no Workshop

### 📈 Análises que Realizaremos

1. **Distribuição Demográfica**: Análise de gênero, etnia, faixa etária, nível e área de educação dos funcionários por unidade de negócio, departamento e cargo.
2. **Remuneração e Benefícios**: Comparação de salários, bônus e comissões por cargo, departamento, unidade de negócio, gênero e geração.
3. **Diversidade e Inclusão**: Avaliação da representatividade de grupos étnicos e de gênero em diferentes níveis hierárquicos e áreas funcionais.
4. **Análise de Contratos e modelos de Trabalho**: Proporção de funcionários em diferentes tipos de contrato (full-time, part-time, contract) e modelos de trabalho (on-site, remoto, híbrido).

## 📦 Como Acessar o Dataset

O dataset está disponível em: [https://huggingface.co/datasets/dougtrajano/hr-synthetic-database](https://huggingface.co/datasets/dougtrajano/hr-synthetic-database)

Para carregar o dataset no Python, você pode usar o seguinte código:

```python
from datasets import load_dataset


# Carregar todas as tabelas
business_units = load_dataset("dougtrajano/hr-synthetic-database", "business_units")
departments = load_dataset("dougtrajano/hr-synthetic-database", "departments")
jobs = load_dataset("dougtrajano/hr-synthetic-database", "jobs")
employees = load_dataset("dougtrajano/hr-synthetic-database", "employees")
compensations = load_dataset("dougtrajano/hr-synthetic-database", "compensations")
```

Para converter as tabelas de employees e compensations em Pandas DataFrames:

```python
import pandas as pd


df_employees = pd.DataFrame(employees['train'])
df_compensations = pd.DataFrame(compensations['train'])
```

### 🗃️ Setup Local do Database

No workshop, configuraremos um database DuckDB local para facilitar as consultas SQL:

```python
import duckdb
import pandas as pd
from datasets import load_dataset


def setup_hr_database():
    """Configura database local com os dados do Hugging Face"""
    
    # Conecta ao DuckDB
    conn = duckdb.connect('data/hr_data.db')
    
    # Carrega e insere cada tabela
    tables = ['business_units', 'departments', 'jobs', 'employees', 'compensations']
    
    for table_name in tables:
        # Carrega dados do Hugging Face
        dataset = load_dataset("dougtrajano/hr-synthetic-database", table_name)
        df = pd.DataFrame(dataset['train'])
        
        # Cria tabela no DuckDB
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
        
    print("✅ Database HR configurado com sucesso!")
    conn.close()
```

## 🧠 Processo de Geração por IA

### 🔬 Metodologia

O dataset foi criado usando um **workflow avançado de IA** com o framework LangGraph, seguindo 5 fases:

1. **Especificação da Empresa** - Conversão de descrição em linguagem natural para especificações estruturadas
2. **Demografia** - Geração de distribuições realistas de gênero, etnia, educação e faixa etária
3. **Setup do Database** - Criação de esquema HR com relacionamentos e restrições
4. **Geração de Funcionários** - Construção de hierarquia top-down com geração paralela em lotes
5. **Detalhes dos Funcionários** - Atribuição de educação, remuneração e demografia usando reasoning de IA

### 🤖 Modelos Utilizados

- **GPT-4o**: Raciocínio complexo (especificação da empresa, proporções demográficas)
- **GPT-4o-mini**: Tarefas focadas (informações educacionais, remuneração)
- **Framework**: LangGraph para orquestração
- **Validação**: Modelos Pydantic para type safety

## ⚖️ Considerações Éticas e Limitações

### ✅ Benefícios Sociais

- **Democratização**: Acesso seguro a dados de RH para pesquisa e desenvolvimento.
- **Privacidade**: Zero risco de exposição de dados pessoais reais.
- **Educação**: Suporte a iniciativas educacionais em data science e HR analytics.

### ⚠️ Limitações Conhecidas

- **Dados Sintéticos**: Podem não capturar todas as nuances do comportamento organizacional real.
- **Bias de Amostragem**: O processo de geração pode não refletir perfeitamente distribuições do mundo real.
- **Simplificação**: Relacionamentos entre variáveis podem ser simplificados comparado à complexidade real.
