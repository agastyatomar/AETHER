# Contributing to AETHER

Thank you for your interest in contributing to AETHER! This guide will help you get started.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Issues

1. Check existing issues first
2. Use the issue template
3. Provide minimal reproduction case
4. Include environment details (OS, Python version, AETHER version)

### Suggesting Features

1. Open a discussion first for major features
2. Explain the use case and motivation
3. Consider backward compatibility

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests and linting
5. Commit with conventional commits
6. Push to your fork
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AETHER.git
cd AETHER

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

## Code Standards

### Python

- **Style**: Ruff (line length 100, double quotes)
- **Types**: MyPy (strict mode)
- **Tests**: Pytest with asyncio support
- **Coverage**: Minimum 80%

### Conventional Commits

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation
- `style` — Formatting
- `refactor` — Code restructuring
- `test` — Tests
- `chore` — Maintenance

Examples:
```
feat(society): add agent memory persistence
fix(browser): resolve playwright install on ARM
docs(api): update skill development guide
test(core): add event bus contract tests
```

### Running Checks

```bash
# Lint
ruff check .

# Format
ruff format .

# Type check
mypy aether/

# Tests
pytest

# All checks
ruff check . && mypy aether/ && pytest
```

## Project Structure

```
AETHER/
├── aether/                 # Main package
│   ├── core/              # Core infrastructure
│   ├── society/           # Agent society
│   ├── skills/            # Skill system
│   ├── docs/              # Documentation layer
│   ├── google_cli/        # Google CLI integration
│   ├── telemetry/         # Flight recorder
│   ├── gui/               # GUI installer
│   ├── cli.py             # Main CLI
│   └── gui_install.py     # GUI entry point
├── install.sh             # Linux/macOS/Termux installer
├── install.ps1            # Windows installer
├── install-termux.sh      # Termux installer
├── pyproject.toml         # Modern packaging
├── setup.py               # Legacy packaging
├── requirements.txt       # Core deps
├── requirements-dev.txt   # Dev deps
├── README.md              # Main readme
├── LICENSE                # MIT license
├── CONTRIBUTING.md        # This file
└── docs/                  # Documentation
```

## Testing Guidelines

### Unit Tests

- Test one thing per test
- Use descriptive names: `test_<what>_<expected>`
- Mock external dependencies
- Fast execution (<100ms each)

### Integration Tests

- Test real component interactions
- Use fixtures for setup/teardown
- Mark with `@pytest.mark.integration`

### Contract Tests

- Test parity across layers (Python/SQL/Pydantic/TS/UI)
- Located in `tests/contract/`

### Browser Tests

- Require browser installation
- Mark with `@pytest.mark.browser`
- Run in CI with `--browser` flag

## Documentation

- Update README for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Keep docs in sync with code

## Release Process

1. Update version in `pyproject.toml` and `setup.py`
2. Update CHANGELOG.md
3. Create release PR
4. Tag release: `git tag v0.x.x`
5. GitHub Actions builds and publishes

## Getting Help

- **Discussions**: [GitHub Discussions](https://github.com/agastyatomar/AETHER/discussions)
- **Issues**: [GitHub Issues](https://github.com/agastyatomar/AETHER/issues)
- **Wiki**: [Documentation Wiki](https://github.com/agastyatomar/AETHER/wiki)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.