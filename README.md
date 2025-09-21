# Agentic AI Workshop by ADP Brazil Labs

Welcome to the Agentic AI Workshop! This repository contains all the materials, examples, and hands-on labs for the workshop on building intelligent agents.

## 📋 Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip

## 🚀 Installation

### Using uv (Recommended)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dougtrajano/agentic-ai-workshop-pucrs25.git
   cd agentic-ai-workshop-pucrs25
   ```

2. **Create and activate a virtual environment:**

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install the project:**

   ```bash
   # Basic installation
   uv pip install -e .
   
   # With development dependencies
   uv pip install -e . --group dev
   
   # With documentation dependencies
   uv pip install -e . --group docs
   
   # Install everything at once
   uv pip install -e . --group dev --group docs
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
  docs-serve
  # or directly: mkdocs serve
  ```

- **Build documentation:**

  ```bash
  docs-build
  # or directly: mkdocs build
  ```

- **Deploy documentation:**

  ```bash
  docs-deploy
  # or directly: mike deploy
  ```

### Development

The project includes several development tools configured:

- **Code formatting with Black:**

  ```bash
  black .
  ```

- **Linting with Ruff:**

  ```bash
  ruff check .
  ruff format .
  ```

- **Type checking with Pyright:**

  ```bash
  pyright
  ```

- **Running tests:**

  ```bash
  pytest
  ```

### Jupyter Notebooks

Start JupyterLab for interactive development:

```bash
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
