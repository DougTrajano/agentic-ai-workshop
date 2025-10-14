# Setup do Ambiente

Este guia ajudará você a configurar o ambiente necessário para o workshop "Agentic AI Workshop PUCRS 2025". Siga os passos abaixo para garantir que tudo esteja funcionando corretamente.

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/DougTrajano/agentic-ai-workshop-pucrs25.git
   cd agentic-ai-workshop-pucrs25
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -e .
   pip install -e .[dev]  # Dependências de desenvolvimento
   ```

4. **Configure variáveis de ambiente**:
   ```bash
   cp .env.example .env
   # Edite .env com suas API keys
   ```

## Verificação da Instalação

```bash
python -c "import pydantic_ai; print('✅ Setup bem-sucedido!')"
```

## Estrutura do Projeto

```
agentic-ai-workshop-pucrs25/
├── src/
│   ├── agents/           # Agentes especializados
│   ├── tools/           # Ferramentas para agentes
│   ├── data/            # Scripts de dados
│   └── observability/   # Logging e métricas
├── data/
│   ├── hr_data.db      # Database DuckDB
│   └── sample_data/    # Dados de exemplo
├── notebooks/          # Jupyter notebooks
└── docs/              # Documentação
```