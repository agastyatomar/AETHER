# AETHER Architecture

## Overview

AETHER is a meta-orchestration framework built on five core principles:

1. **Nothing at Boot (AP-26)** — No initialization on import; lazy singletons only
2. **Tool-Executor Gated (AP-3)** — All agent actions go through `ToolExecutor.execute()`
3. **Scheduler Privilege (AP-5/14)** — Only the scheduler spawns workers; no spawn tools in agent sets
4. **Five-Layer Parity (AP-4)** — Enums sync across Python ↔ SQL ↔ Pydantic ↔ TypeScript ↔ UI
5. **No Harm at Scale** — No capability messages/probes/acts on non-consenting parties

## Package Structure

```
aether/
├── core/                 # Core infrastructure
│   ├── config.py         # Configuration management
│   ├── events.py         # Event system
│   ├── protocols.py      # Communication protocols
│   ├── bus.py            # Event bus
│   ├── process_utils.py  # Process utilities
│   ├── process_tree.py   # Process tree management
│   ├── path_augment.py   # Path augmentation
│   ├── chat_turn.py      # Chat turn management
│   ├── model_selection.py # Model selection
│   ├── runtime_refs.py   # Runtime references
│   ├── task_agent.py     # Task agent
│   ├── turn_language.py  # Language detection
│   ├── response_style.py # Response styling
│   └── interactive_terminal.py
├── society/              # Agent society substrate
│   ├── events.py         # Society events & enums
│   ├── failure_reasons.py # Failure reason vocabulary
│   ├── store.py          # SQLite persistence (society.db)
│   ├── bus.py            # In-process event fan-out
│   ├── roster.py         # Agent registry
│   ├── capabilities.py   # Capability catalog
│   ├── focus.py          # Deterministic focus
│   ├── rooms.py          # Bounded discussions
│   ├── scheduler.py      # Trusted Python scheduler
│   ├── bridge.py         # Mission → society events
│   ├── runtime.py        # Lazy singleton runtime
│   ├── approvals.py      # Approval queue
│   ├── routines.py       # Per-agent routines
│   ├── surface.py        # Chat surface
│   ├── memory_books.py   # USER.md / MEMORY.md
│   ├── memory.py         # Personal memory
│   ├── checkpoints.py    # Agent checkpoints
│   ├── agent_tools.py    # Agent tool set
│   ├── shell.py          # Shell backend
│   ├── learning.py       # Automatic learning
│   ├── quests.py         # Quest board
│   ├── seeds.py          # Starter team
│   ├── chat_binding.py   # Session binding
│   ├── companion.py      # Companion agents
│   ├── review.py         # Review system
│   ├── proposals.py      # Proposals
│   ├── inherit.py        # Creator inheritance
│   ├── coding_tool.py    # Coding tools
│   ├── coding_supervision.py
│   ├── browser/          # Managed browser automation
│   │   ├── install.py    # One-click venv + browser install
│   │   ├── runner.py     # In-venv script
│   │   ├── session.py    # Per-agent profiles
│   │   ├── tool.py       # society_browser tool
│   │   ├── llm.py        # Provider → LLM class
│   │   ├── live.py       # Live runner
│   │   ├── live_runner.py # Live runner impl
│   │   ├── bridge.py     # Browser bridge
│   │   ├── bootstrap.py  # UV bootstrap
│   │   ├── native_window.py
│   │   ├── page_cursor.py
│   │   └── pointer.py
│   └── mars/             # Mars station contracts
│       ├── definition.json
│       ├── models.py
│       ├── store.py
│       ├── service.py
│       ├── navigation.py
│       └── rover_service.py
├── skills/               # Skill system
│   ├── schema.py         # Skill schema
│   ├── loader.py         # Skill loader
│   ├── registry.py       # Skill registry
│   ├── runner.py         # Skill runner
│   ├── creator_service.py # Skill creation
│   ├── authoring_request.py
│   ├── origin.py         # Skill origin tracking
│   └── bootstrap.py      # Bootstrap skills
├── docs/                 # Documentation layer
│   ├── schema.py         # Doc frontmatter schema
│   ├── loader.py         # Doc parser
│   ├── registry.py       # Doc registry (watchdog)
│   └── search.py         # FTS5 search
├── google_cli/           # Google CLI integration
│   ├── resolver.py       # CLI resolver
│   ├── auth_service.py   # Auth service
│   ├── pty_runner.py     # PTY runner
│   └── isolated_home.py  # Isolated home dir
├── telemetry/            # Flight recorder
│   ├── recorder.py       # JSONL flight recorder
│   ├── replay.py         # Replay CLI
│   ├── latency.py        # Latency tracking
│   └── latency_log.py
├── missions/             # Mission system
├── agent_chat/           # Agent chat
├── agentic_ide/          # IDE integration
├── brain/                # Brain module
├── clis/                 # CLI tools
├── local_models/         # Local model integration
├── mcp/                  # MCP servers
├── memory/               # Memory system
├── safety/               # Safety checks
├── tasks/                # Task scheduling
├── terminal/             # Terminal backend
├── plugins/              # Plugin system
├── gui/                  # GUI installer
│   ├── __init__.py
│   └── installer.py
├── cli.py                # Main CLI
└── gui_install.py        # GUI entry point
```

## Data Flow

```
User Request
    ↓
AETHER Orchestrator (cli.py)
    ↓
Society Runtime (society/runtime.py)
    ↓
Scheduler (society/scheduler.py) → spawns workers
    ↓
Agent Tools (society/agent_tools.py) → execute actions
    ↓
Browser (society/browser/) → web automation
    ↓
Telemetry (telemetry/recorder.py) → flight recorder
```

## Key Design Decisions

### Isolated Browser Runtime
- Browser-use and Playwright live in a managed venv under data dir
- Runner script (`live_runner.py`) is dependency-free, speaks JSONL over stdin/stdout
- Zero import-time side effects (AP-26)

### Agent Society
- Durable named agents with persistent SQLite storage
- Capability ceilings, approval gates, kill switches
- Deterministic focus derivation (no model call)

### Skill System
- Skills as markdown + frontmatter
- Hot-reload via watchdog
- Automatic learning: digest → skill

### Telemetry
- JSONL flight recorder with daily rotation
- Replay CLI for debugging
- Latency phase tracking

## Extensibility Points

1. **Plugins** — Entry points under `aether.tool`
2. **Skills** — Markdown files in skills directory
3. **MCP Servers** — Custom tool servers
4. **CLIs** — Connected command-line tools
5. **Custom Capabilities** — Register via `capabilities.py`