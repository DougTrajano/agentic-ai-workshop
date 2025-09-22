# Agentic AI Workshop by ADP Brazil Labs

Welcome to the Agentic AI Workshop! This repository contains all the materials, examples, and hands-on labs for the workshop on building intelligent agents.

## 📋 Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip

## 🚀 Installation

### Using uv (Recommended)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dougtrajano/agentic-ai-workshop.git
   cd agentic-ai-workshop
   ```

2. **Install the project with dependencies:**

   ```bash
   # Basic installation
   uv sync
   
   # With development dependencies
   uv sync --group dev
   
   # With documentation dependencies
   uv sync --group docs
   
   # Install everything at once
   uv sync --all-groups
   ```

3. **Activate the virtual environment:**

   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

### Using pip

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dougtrajano/agentic-ai-workshop.git
   cd agentic-ai-workshop
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install the project:**

   ```bash
   pip install -e .
   ```

## 📚 Usage

### Documentation

Once installed, you can use the following commands to work with the documentation:

- **Serve documentation locally:**

  ```bash
  # With uv
  uv run mkdocs serve
  
  # Or with activated virtual environment
  docs-serve
  # or directly: mkdocs serve
  ```

- **Build documentation:**

  ```bash
  # With uv
  uv run mkdocs build
  
  # Or with activated virtual environment  
  docs-build
  # or directly: mkdocs build
  ```

- **Deploy documentation:**

  ```bash
  # With uv
  uv run mike deploy
  
  # Or with activated virtual environment
  docs-deploy
  # or directly: mike deploy
  ```

### Development

The project includes several development tools configured. You can run them with uv or in an activated virtual environment:

- **Code formatting with Black:**

  ```bash
  # With uv
  uv run black .
  
  # Or with activated virtual environment
  black .
  ```

- **Linting with Ruff:**

  ```bash
  # With uv
  uv run ruff check .
  uv run ruff format .
  
  # Or with activated virtual environment
  ruff check .
  ruff format .
  ```

- **Type checking with Pyright:**

  ```bash
  # With uv
  uv run pyright
  
  # Or with activated virtual environment
  pyright
  ```

- **Running tests:**

  ```bash
  # With uv
  uv run pytest
  
  # Or with activated virtual environment
  pytest
  ```

### Jupyter Notebooks

Start JupyterLab for interactive development:

```bash
# With uv
uv run jupyter lab

# Or with activated virtual environment
jupyter lab
```

## 🏗️ Project Structure

```text
├── docs/                   # Documentation files
│   ├── workshop/          # Workshop content
│   └── assets/            # Images and static files
├── workshop/              # Main Python package
├── tests/                 # Test files
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Documentation](https://dougtrajano.github.io/agentic-ai-workshop/)
- [Issues](https://github.com/dougtrajano/agentic-ai-workshop/issues)
- [Releases](https://github.com/DougTrajano/agentic-ai-workshop/releases)
