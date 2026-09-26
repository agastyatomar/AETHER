# AETHER

> **AETHER** — voice-driven meta-orchestrator that turns one spoken request into a fleet of self-checking AI agents.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://github.com/agastyatomar/AETHER/workflows/CI/badge.svg)](https://github.com/agastyatomar/AETHER/actions)
[![Coverage](https://img.shields.io/badge/coverage-80%25%2B-brightgreen.svg)](https://github.com/agastyatomar/AETHER/actions)

---

## 🎯 Overview

AETHER is a meta-orchestration framework that transforms natural language requests into coordinated teams of AI agents. Each agent operates with defined capabilities, permissions, and memory — all under a unified society layer that ensures safety, traceability, and deterministic behavior.

### Key Features

- **🗣️ Voice-Driven**: Natural language input → structured agent delegation
- **🤖 Agent Society**: Durable, named agents with persistent memory and relationships
- **🔒 Safety-First**: Capability ceilings, approval gates, kill switches, audit trails
- **🌐 Browser Automation**: Isolated, per-agent browser profiles via Playwright/browser-use
- **📦 Self-Contained**: Zero-config managed runtimes for browser automation
- **🔧 Extensible**: Plugin system, custom skills, MCP server integration
- **📊 Observable**: Flight recorder telemetry, latency tracking, replay CLI

---

## 📺 Demo

<!-- TODO: Add demo video/GIF here -->
<p align="center">
  <img src="assets/demo.gif" alt="AETHER Demo" width="800"/>
</p>

*Video: [AETHER in action](https://github.com/agastyatomar/AETHER/wiki/Demo)*

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (3.12 recommended)
- **Git**
- **Platform-specific**:
  - **Windows**: PowerShell 5.1+ or PowerShell 7+
  - **Linux**: `build-essential`, `python3-dev`, `libsqlite3-dev`
  - **macOS**: Xcode Command Line Tools
  - **Termux**: `pkg install python build-essential libsqlite`

### One-Line Install (All Platforms)

```bash
# Linux / macOS / Termux / WSL
curl -fsSL https://raw.githubusercontent.com/agastyatomar/AETHER/main/install.sh | bash

# Windows (PowerShell)
irm https://raw.githubusercontent.com/agastyatomar/AETHER/main/install.ps1 | iex
```

### Manual Install

```bash
# Clone the repository
git clone https://github.com/agastyatomar/AETHER.git
cd AETHER

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install core package
pip install -e .

# Install development dependencies (optional)
pip install -r requirements-dev.txt

# Install browser automation (optional, creates isolated venv)
aether-browser-install --system-deps
```

### Verify Installation

```bash
# Check core package
aether --version

# Check browser automation
aether-browser-install --status
```

---

## 📦 Installation Scripts

### Linux / macOS / Termux / WSL

```bash
# Download and run
curl -fsSL https://raw.githubusercontent.com/agastyatomar/AETHER/main/install.sh | bash

# Or with options
curl -fsSL https://raw.githubusercontent.com/agastyatomar/AETHER/main/install.sh | bash -s -- --dev --browser
```

**Options:**
- `--dev` — Install development dependencies
- `--browser` — Install browser automation (requires system deps)
- `--no-venv` — Skip virtual environment creation
- `--prefix DIR` — Install to custom directory

### Windows (PowerShell)

```powershell
# Download and run
irm https://raw.githubusercontent.com/agastyatomar/AETHER/main/install.ps1 | iex

# Or with options
irm https://raw.githubusercontent.com/agastyatomar/AETHER/main/install.ps1 | iex -ArgumentList @('--dev', '--browser')
```

**Options:**
- `-Dev` — Install development dependencies
- `-Browser` — Install browser automation
- `-NoVenv` — Skip virtual environment creation
- `-Prefix DIR` — Install to custom directory

### Termux (Android)

```bash
# Termux-optimized install
pkg update && pkg install -y git python build-essential libsqlite openssl
git clone https://github.com/agastyatomar/AETHER.git
cd AETHER
./install-termux.sh
```

---

## 🖥️ GUI Installer

For a graphical installation experience:

```bash
# Linux / macOS / Windows (requires tkinter)
python -m aether.gui_install

# Or download standalone installer
# Windows: AETHER-Installer.exe
# Linux: AETHER-Installer.AppImage
# macOS: AETHER-Installer.dmg
```

**GUI Installer Features:**
- Visual progress tracking
- Component selection (core, browser, dev tools)
- Automatic dependency detection
- Platform-specific optimizations
- Uninstaller integration

---

## 📖 Usage

### CLI Commands

```bash
# Core orchestrator
aether --help                    # Show all commands
aether run "your request"        # Execute a voice/text request
aether society --help            # Agent society management

# Browser automation
aether-browser-install           # Install managed browser runtime
aether-browser-install --probe   # Verify browser rendering
aether-browser-install --repair  # Repair broken installation

# Agent society
aether-society roster            # List agents
aether-society chat <agent>      # Chat with an agent
```

### Python API

```python
from aether import Aether
from aether.society import SocietyRuntime

# Initialize orchestrator
app = Aether()

# Run a request
result = await app.run("Research the latest AI papers and summarize key findings")

# Access agent society
society = SocietyRuntime.current()
agents = society.roster.list_agents()
```

---

## 🏗️ Architecture

```
AETHER/
├── aether/
│   ├── core/              # Core infrastructure (config, events, protocols)
│   ├── society/           # Agent society substrate
│   │   ├── browser/       # Managed browser automation
│   │   ├── mars/          # Mars station contracts
│   │   └── ...            # Roster, rooms, scheduler, approvals, etc.
│   ├── skills/            # Skill system (authoring, registry, runner)
│   ├── docs/              # Documentation layer (FTS5 search, hot-reload)
│   ├── google_cli/        # Google CLI integration (Antigravity/agy)
│   ├── telemetry/         # Flight recorder + replay
│   └── cli.py             # Main CLI entry point
├── install.sh             # Linux/macOS/Termux installer
├── install.ps1            # Windows PowerShell installer
├── install-termux.sh      # Termux-optimized installer
├── gui_install.py         # GUI installer (tkinter)
├── pyproject.toml         # Modern packaging config
├── setup.py               # Legacy packaging config
├── requirements.txt       # Core dependencies
├── requirements-dev.txt   # Development dependencies
└── README.md              # This file
```

### Core Principles

1. **Nothing at Boot** (AP-26): No initialization on import; lazy singletons only
2. **Tool-Executor Gated** (AP-3): All agent actions go through `ToolExecutor.execute()`
3. **Scheduler Privilege** (AP-5/14): Only the scheduler spawns workers; no spawn tools in agent sets
4. **Five-Layer Parity** (AP-4): Enums sync across Python ↔ SQL ↔ Pydantic ↔ TypeScript ↔ UI
5. **No Harm at Scale**: No capability messages/probes/acts on non-consenting parties

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=aether --cov-report=html

# Run specific test suite
pytest tests/unit/society/
pytest tests/contract/
```

### Test Structure

```
tests/
├── unit/              # Unit tests (fast, isolated)
│   ├── society/       # Society substrate tests
│   ├── core/          # Core infrastructure tests
│   └── skills/        # Skill system tests
├── contract/          # Contract tests (parity, schema)
│   └── test_society_substrate.py
└── integration/       # Integration tests (slower, real deps)
    └── test_browser_install.py
```

---

## 🔧 Development

### Environment Setup

```bash
# Fork and clone your fork
git clone https://github.com/YOUR_USERNAME/AETHER.git
cd AETHER

# Create dev environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install  # optional
```

### Code Quality

```bash
# Lint
ruff check .

# Format
ruff format .

# Type check
mypy aether/

# All checks
ruff check . && mypy aether/ && pytest
```

### Adding a New Skill

```bash
# Create skill template
aether skill create my-skill

# Edit skill manifest
# aether/skills/builtin/my-skill/skill.yaml

# Test skill
aether skill test my-skill

# Publish to registry
aether skill publish my-skill
```

---

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [Agent Society Guide](docs/agent-society.md)
- [Browser Automation](docs/browser-automation.md)
- [Skill Development](docs/skills.md)
- [Telemetry & Debugging](docs/telemetry.md)
- [API Reference](docs/api.md)
- [Contributing](CONTRIBUTING.md)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`ruff check . && mypy aether/ && pytest`)
5. Commit with conventional commits (`git commit -m "feat: add amazing feature"`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [browser-use](https://github.com/browser-use/browser-use) — Browser automation
- [Playwright](https://playwright.dev/) — Browser engine
- [Pydantic](https://pydantic.dev/) — Data validation
- [aiosqlite](https://github.com/omnilib/aiosqlite) — Async SQLite
- [filelock](https://github.com/tox-dev/pyfilelock) — Cross-platform file locking

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/agastyatomar/AETHER/issues)
- **Discussions**: [GitHub Discussions](https://github.com/agastyatomar/AETHER/discussions)
- **Wiki**: [Documentation Wiki](https://github.com/agastyatomar/AETHER/wiki)

---

<div align="center">
  <strong>Built with ❤️ by the AETHER team</strong>
</div>