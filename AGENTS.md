# Agentic AI Workshop - Agent Instructions

This file provides context and instructions for AI coding agents working on the Agentic AI Workshop project by ADP Brazil Labs.

## Project Overview

This repository contains a hands-on workshop for building intelligent agents using modern AI frameworks. The project includes:

- **Educational Content**: MkDocs-based documentation covering agentic AI concepts, frameworks, and best practices
- **Sample Application**: A Chainlit-based chat application with a LangGraph ReAct agent for HR data analysis
- **Synthetic Dataset**: AI-powered workflow for generating realistic HR datasets using Pydantic models
- **Databricks Integration**: Workflows and apps configured for Databricks deployment

**Tech Stack**:

- Python 3.13+ with `uv` package manager
- Frameworks: LangGraph, LangChain, Chainlit
- Database: PostgreSQL (Databricks Lakebase) with SQLAlchemy
- Documentation: MkDocs Material with custom plugins
- Deployment: Databricks Apps

## Development Environment Setup

### Initial Setup

1. **Clone and install dependencies:**

   ```bash
   git clone https://github.com/dougtrajano/agentic-ai-workshop.git
   cd agentic-ai-workshop
   uv sync --all-groups  # Install all dependencies including dev and docs
   source .venv/bin/activate  # Activate virtual environment
   ```

2. **Configure pre-commit hooks:**

   ```bash
   pre-commit install
   ```

### Package Manager

- **Primary**: Use `uv` for all package management (faster, more reliable)
- **Alternative**: Standard `pip` is supported but `uv` is recommended
- **Install packages**: `uv add <package>` or `uv sync` to sync from pyproject.toml
- **Run scripts**: `uv run <command>` or activate the venv first

### Project Structure Navigation

- **Application code**: `src/app/` - Chainlit chat app with LangGraph agent
  - `main.py`: Chainlit app entry point with auth and UI setup
  - `backend/agent.py`: LangGraph ReAct agent with SQL tools and calculator
  - `backend/database/`: Database connections (Lakebase and Chainlit data layer)
  - `backend/auth/`: Authentication handlers (header-based and password)
  
- **Dataset generation**: `src/dataset/` - AI workflow for synthetic HR data
  - `workflow.py`: LangGraph workflow using OpenAI to generate company specs
  - `models/`: Pydantic models (Employee, Company, Compensation, etc.)
  - `database.py`: Database operations for HR data storage
  
- **Documentation**: `docs/` - MkDocs source files
  - Workshop guides in `docs/workshop/`
  - Agentic AI concepts in `docs/agentic-ai/`
  - Framework comparisons in `docs/agentic-ai/frameworks/`

- **Databricks configs**: `databricks/` - Bundle and workflow YAML files
- **Jobs**: `src/jobs/` - Standalone scripts for Databricks workflows

## Code Style and Standards

### Python Conventions

Follow the guidelines in `.github/instructions/python.instructions.md`:

- **Style Guide**: PEP 8 compliant, 99 character line length (see `pyproject.toml`)
- **Type Hints**: Always use type hints; prefer built-in types (`list[str]`) over `typing` module
- **Docstrings**: Google-style or NumPy-style, immediately after `def` or `class`
- **Formatting**: Use `black` and `ruff` for automatic formatting
- **Import Order**: Use `isort` (configured in `pyproject.toml`)

### Code Quality Tools

```bash
# Format code
uv run black .
uv run ruff check --fix .
uv run isort .

# Type checking
uv run mypy src/
uv run pyright src/

# Linting
uv run flake8 src/
uv run ruff check .

# Run all checks (recommended before commit)
pre-commit run --all-files
```

### Naming Conventions

- **Files/Modules**: `snake_case.py`
- **Classes**: `PascalCase` (e.g., `AgentOutput`, `CompanySpec`)
- **Functions/Variables**: `snake_case` (e.g., `create_data_agent`, `user_input`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `AGENT_SCHEMA`, `BASE_NAME`)
- **Pydantic Models**: `PascalCase` with descriptive Field definitions

## Testing

### Test Structure

- Tests located in `tests/` (create if needed)
- Use `pytest` for all testing
- Test files follow pattern: `test_*.py`
- Async tests require `pytest-asyncio`

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_agent.py

# Run tests matching pattern
uv run pytest -k "test_agent_creation"

# Run with verbose output
uv run pytest -v
```

### Writing Tests

- Mock external dependencies (OpenAI API, database connections)
- Use `pytest-mock` for mocking
- Test edge cases: empty inputs, invalid data types, large datasets
- Include docstrings explaining test cases
- Use fixtures for common test setup

## Documentation

### Local Development

```bash
# Serve docs locally (auto-reload on changes)
uv run mkdocs serve
# Or use script alias:
docs-serve

# Open browser to http://localhost:8000
```

### Building and Deploying

```bash
# Build static site
uv run mkdocs build  # Output to site/

# Deploy to GitHub Pages with versioning
uv run mike deploy --push --update-aliases 0.0.1 latest
uv run mike set-default --push latest
```

### Documentation Guidelines

- Use Markdown with MkDocs Material extensions
- Place images in `docs/images/`
- Use custom CSS in `docs/stylesheets/` for styling
- Add JavaScript enhancements in `docs/javascripts/`
- Use admonitions for callouts: `!!! note`, `!!! warning`, etc.
- Include code examples with proper syntax highlighting

## Agent Implementation

### LangGraph Agent Architecture

The main agent (`src/app/backend/agent.py`) follows this pattern:

1. **Create LLM**: Uses OpenAI ChatGPT-4.1
2. **Database Connection**: PostgreSQL (Lakebase) with SQLAlchemy
3. **Tools Setup**:
   - `calculator`: Math operations via numexpr
   - SQL tools from `SQLDatabaseToolkit` (query, schema inspection)
4. **Agent Creation**: `create_react_agent` with structured output (`AgentOutput`)
5. **Response Format**: Always returns JSON with `content`, `sql_query`, `dataset`, and `plotly_json_fig`

### Adding New Tools

```python
def my_custom_tool(param: str) -> str:
    """Tool description for the agent.
    
    Args:
        param: Description of parameter
        
    Returns:
        Result description
    """
    # Implementation
    return result

# Add to tools list in create_data_agent()
tools = [calculator, my_custom_tool]
```

### Agent Output Structure

Always use the `AgentOutput` Pydantic model:

- `content`: Natural language answer (required)
- `sql_query`: Formatted SQL query (optional, auto-formatted)
- `dataset`: JSON-serializable data for pandas (optional)
- `plotly_json_fig`: Plotly chart JSON (optional, include data labels)

## Database Operations

### Lakebase (PostgreSQL) Connection

```python
from backend.database.lakebase import create_lakebase_engine
from backend.settings import Settings

engine = create_lakebase_engine(
    engine_url=Settings().pg_connection_string,
    connect_args={'options': f'-csearch_path={Settings().AGENT_SCHEMA}'},
)
```

### Schema Structure

The HR database (`human_resources` schema) contains tables:

- `employees`: Employee demographic and organizational data
- `compensation`: Salary and bonus information
- `departments`: Department details
- `business_units`: Business unit information
- `jobs`: Job title and level definitions

### Dataset Generation

Generate synthetic HR data using the LangGraph workflow:

```python
from src.dataset.workflow import workflow

# Define company description
company_desc = """
A tech company with 500 employees, 3 business units...
"""

# Generate dataset
result = workflow.invoke({"user_input": company_desc})
```

## Databricks Integration

### Bundle Configuration

- **Main config**: `databricks.yml` defines bundle variables
- **Workflows**: `databricks/download_dataset.yml` and `databricks/app.yml`
- **Deployment targets**: Dev environment configured for Azure Databricks

### Deploying to Databricks

```bash
# Validate bundle
databricks bundle validate

# Deploy to dev
databricks bundle deploy -t dev

# Run workflow
databricks bundle run download_dataset -t dev

# Deploy app
databricks bundle deploy -t dev
databricks apps start agentic_ai_workshop_app
```

### Environment Variables

Required for Databricks Apps (set in app.yml):

- `OPENAI_API_KEY`: OpenAI API key
- `PG_HOST`, `PG_PORT`, `PG_DATABASE`: PostgreSQL connection
- `PG_USER`, `PG_PASSWORD`: Database credentials
- `AGENT_SCHEMA`: Schema name (default: `human_resources`)

## Common Tasks

### Adding a New Framework to Documentation

1. Create new file in `docs/agentic-ai/frameworks/<framework-name>.md`
2. Follow existing structure (Overview, Key Features, Example, Resources)
3. Update `mkdocs.yml` navigation
4. Add comparison points to `docs/agentic-ai/frameworks/index.md`

### Modifying the Agent System Prompt

Edit `get_system_prompt()` in `src/app/backend/agent.py`:

- Keep instructions clear and specific
- Emphasize SQL query safety (no DML statements)
- Always include schema inspection steps
- Limit results to top_k unless specified

### Creating New Pydantic Models

Follow the pattern in `src/dataset/models/`:

- Inherit from `BaseModel`
- Use descriptive `Field()` with description parameter
- Add validation with `@field_validator` when needed
- Group related models in the same file
- Import from `models/__init__.py` for clean imports

### Updating Dependencies

```bash
# Add new dependency
uv add <package>

# Add dev dependency
uv add --group dev <package>

# Add docs dependency
uv add --group docs <package>

# Update all dependencies
uv sync --upgrade

# Update specific package
uv add --upgrade <package>
```

## Security and Best Practices

### Secrets Management

- **Never commit secrets** to the repository
- Use environment variables for sensitive data
- Use Databricks secrets for production deployments
- `.env` files are gitignored; use `.env.example` for templates

### Authentication

The app supports two auth modes (configured in `backend/settings.py`):

1. **Header Auth** (`ENABLE_HEADER_AUTH=true`): For Databricks Apps with SSO
2. **Password Auth** (`ENABLE_PASSWORD_AUTH=true`): For local development

### SQL Injection Prevention

- Use SQLAlchemy's parameterized queries
- Never construct raw SQL from user input
- The agent uses LangChain's SQL toolkit which handles escaping
- Validate all user inputs in Pydantic models

### Agent Safety

- Agent has read-only database access (no DML operations)
- Calculator tool uses `numexpr` with restricted globals
- System prompt explicitly forbids destructive operations
- All agent responses validated through `AgentOutput` model

## Troubleshooting

### Common Issues

**Import errors after adding dependencies:**

```bash
uv sync  # Re-sync environment
```

**Documentation not updating:**

```bash
# Clear MkDocs cache
rm -rf site/
uv run mkdocs build --clean
```

**Database connection issues:**

- Verify `PG_*` environment variables are set
- Check network connectivity to Databricks
- Ensure schema exists: `CREATE SCHEMA IF NOT EXISTS human_resources;`

**Agent not returning structured output:**

- Verify OpenAI API key is valid
- Check model supports structured outputs (GPT-4+)
- Review agent logs in Chainlit data layer

**Pre-commit hooks failing:**

```bash
# Update hooks
pre-commit autoupdate

# Skip hooks temporarily (not recommended)
git commit --no-verify
```

## Resources and References

- **Workshop Documentation**: https://dougtrajano.github.io/agentic-ai-workshop/
- **Pydantic AI Docs**: https://ai.pydantic.dev/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Chainlit Docs**: https://docs.chainlit.io/
- **Databricks Apps**: https://docs.databricks.com/en/dev-tools/bundles/apps.html
- **MkDocs Material**: https://squidfunk.github.io/mkdocs-material/

## Contributing

### Pull Request Guidelines

- **Branch naming**: `feature/<description>`, `fix/<description>`, `docs/<description>`
- **Commit messages**: Follow conventional commits format
  - `feat: Add new agent tool for data export`
  - `fix: Resolve SQL formatting issue in agent output`
  - `docs: Update LangGraph framework guide`
- **Pre-commit checks**: Ensure all hooks pass before pushing
- **Tests**: Add tests for new features
- **Documentation**: Update docs for user-facing changes

### Code Review Checklist

- [ ] Code follows Python conventions in `.github/instructions/python.instructions.md`
- [ ] Type hints included for all functions
- [ ] Docstrings added for public APIs
- [ ] Tests pass: `pytest`
- [ ] Formatting correct: `black`, `ruff`, `isort`
- [ ] No secrets or sensitive data committed
- [ ] Documentation updated if needed
- [ ] Pre-commit hooks pass

## Special Notes for AI Agents

### File Reading Priorities

When working on tasks:

1. **Always read** `.github/instructions/*.instructions.md` files first for coding standards
2. **Check** `pyproject.toml` for dependency constraints before adding packages
3. **Review** existing similar code before implementing new features
4. **Consult** `docs/` content for domain-specific context

### Response Patterns

When implementing agents or workflows:

- Use Pydantic models for all structured data
- Implement type validation with `@field_validator`
- Include detailed docstrings with examples
- Return structured outputs (not raw strings)
- Log important operations using `backend.utils.logger`

### Testing Expectations

Always include:

- Unit tests for new functions
- Mock external API calls (OpenAI, database)
- Edge case validation
- Async test support when needed
- Clear test docstrings
