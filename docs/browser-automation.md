# Browser Automation

## Overview

AETHER provides managed, per-agent browser automation via Playwright and browser-use, running in an isolated virtual environment.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  AETHER Main Process                                     │
│  ├── Society Runtime                                     │
│  └── Agent Tools → society_browser                      │
└─────────────────────────────────────────────────────────┘
                          │
                    JSONL over stdin/stdout
                          │
┌─────────────────────────────────────────────────────────┐
│  Managed Browser Venv (data/society/browser/)           │
│  ├── browser-use 0.13.10                                │
│  ├── Playwright 1.62.0 + Chromium                       │
│  └── live_runner.py (dependency-free script)            │
└─────────────────────────────────────────────────────────┘
```

## Installation

```bash
# Install with system dependencies (Linux/macOS)
aether-browser-install --system-deps

# Install without system deps (Windows, or if already installed)
aether-browser-install

# Verify installation
aether-browser-install --probe

# Repair broken installation
aether-browser-install --repair
```

## Usage

### As Agent Tool

Agents use the `society_browser` tool:

```python
# In agent tool set
result = await society_browser(
    task="Navigate to GitHub and find the latest release",
    mode="headless",
    caps=["click", "scroll", "text", "download"]
)
```

### Direct API

```python
from aether.society.browser import BrowserSession

session = BrowserSession(agent_id="researcher")
await session.login("https://github.com", credentials={"username": "user", "password": "pass"})
result = await session.run("Go to trending page and extract top 5 repos")
```

## Configuration

### Browser Install Options

```bash
aether-browser-install [OPTIONS]

Options:
  --system-deps      Install Playwright system dependencies (requires sudo)
  --repair           Force repair of existing installation
  --probe            Run render check and exit
  --status           Show installation status
  --data-dir PATH    Custom data directory
```

### Per-Agent Profiles

Each agent gets isolated browser profile:
```
data/society/browser/profiles/<agent_id>/
├── cookies.sqlite
├── localStorage/
├── sessionStorage/
└── preferences.json
```

## Capabilities

| Capability | Description |
|------------|-------------|
| `click` | Click elements |
| `scroll` | Scroll pages |
| `text` | Input text |
| `download` | Download files |
| `upload` | Upload files |
| `screenshot` | Take screenshots |
| `pdf` | Save as PDF |

## Modes

- `headless` — No visible UI (default)
- `headed` — Visible browser window
- `persistent` — Persistent profile with login state

## Troubleshooting

### Browser not found
```bash
aether-browser-install --repair --system-deps
```

### Render check fails
```bash
aether-browser-install --probe
# Check output for missing system deps
```

### Permission denied (Linux)
```bash
# Ensure user in render/video groups
sudo usermod -a -G render,video $USER
```

### Termux/Android
Browser automation is limited on Android. Use proot-distro:
```bash
pkg install proot-distro
proot-distro install ubuntu
proot-distro login ubuntu -- aether-browser-install --system-deps
```

## Security

- Browser runs in isolated venv — no access to main process deps
- No inference credentials passed to browser process
- Per-agent profile isolation
- Capability-based tool grants