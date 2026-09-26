# API Reference

## Core Modules

### `aether.core.config`

```python
from aether.core.config import Config, DATA_DIR

# Get data directory
data_dir = DATA_DIR

# Load configuration
config = Config.load()
```

### `aether.core.events`

```python
from aether.core.events import Event, EventBus

# Create event
event = Event(kind="custom", payload={"key": "value"})

# Event bus
bus = EventBus.get()
bus.publish(event)
bus.subscribe("custom", handler)
```

### `aether.core.protocols`

```python
from aether.core.protocols import ToolResult, BrainMessage, BrainRequest

# Tool result
result = ToolResult(ok=True, data={"result": "success"})

# Brain message
msg = BrainMessage(role="user", content="Hello")
```

## Society Modules

### `aether.society.runtime`

```python
from aether.society.runtime import SocietyRuntime

# Get singleton runtime
runtime = SocietyRuntime.current()

# Access components
roster = runtime.roster
scheduler = runtime.scheduler
bus = runtime.bus
```

### `aether.society.roster`

```python
from aether.society.roster import AgentRecord, AgentRoster

roster = AgentRoster(store)

# Create agent
agent = roster.create_agent(
    name="researcher",
    title="Research Agent",
    provider="anthropic",
    model="claude-3-opus",
    permission_ceiling="ASK",
)

# List agents
agents = roster.list_agents()

# Get agent
agent = roster.get_agent("researcher")
```

### `aether.society.scheduler`

```python
from aether.society.scheduler import Scheduler, AssignRequest

scheduler = Scheduler(runtime)

# Submit assignment
request = AssignRequest(
    agent_id="researcher",
    task="Research AI trends",
    priority=5,
)
result = await scheduler.assign(request)
```

### `aether.society.browser`

```python
from aether.society.browser import BrowserSession, install_browser

# Install browser runtime
await install_browser(system_deps=True)

# Create session
session = BrowserSession(agent_id="researcher")

# Login
await session.login("https://site.com", credentials={...})

# Run task
result = await session.run("Navigate and extract data")
```

## Skill Modules

### `aether.skills.registry`

```python
from aether.skills.registry import SkillRegistry

registry = SkillRegistry(skills_dir=Path("skills"))

# Load skills
registry.load_all()

# Get skill
skill = registry.get_skill("my-skill")

# Execute
result = await skill.execute("my_action", {"param": "value"})
```

### `aether.skills.runner`

```python
from aether.skills.runner import SkillRunner

runner = SkillRunner(registry)

# Run skill action
result = await runner.run("my-skill", "my_action", {"param": "value"})
```

## CLI Commands

### `aether`

```bash
aether [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version   Show version
  --help          Show help

Commands:
  run         Execute a request
  society     Agent society management
  skills      Skill management
  docs        Documentation tools
  browser     Browser automation
  config      Configuration
```

### `aether run`

```bash
aether run "Research the latest AI papers and summarize"
```

### `aether society`

```bash
aether society [OPTIONS] COMMAND [ARGS]...

Commands:
  roster      List agents
  chat        Chat with agent
  rooms       Manage rooms
  quests      Manage quests
  approvals   View approvals
```

### `aether-browser-install`

```bash
aether-browser-install [OPTIONS]

Options:
  --system-deps   Install Playwright system dependencies
  --repair        Repair broken installation
  --probe         Run render check
  --status        Show status
  --data-dir      Custom data directory
```

### `aether-society`

```bash
aether-society [OPTIONS] COMMAND [ARGS]...

Commands:
  roster      List agents
  chat        Chat with agent
  run         Run society task
```

## Data Models

### `AgentRecord`

```python
class AgentRecord:
    agent_id: str
    name: str
    title: str
    provider: str
    model: str
    effort: str
    permission_ceiling: PermissionCeiling  # SAFE | MONITOR | ASK
    grant_mode: GrantMode                  # ALLOWLIST | DENYLIST
    grants: list[str]
    denies: list[str]
    parent_agent_id: str | None
    focus: list[str]
    budget: int
    avatar: str | None
    created_at: datetime
    updated_at: datetime
```

### `SocietyEnvelope`

```python
class SocietyEnvelope:
    event_id: str
    msg_type: MsgType
    from_agent: str
    to_agent: str | None
    room_id: str | None
    payload: dict
    trace_id: str
    timestamp: datetime
```

### `ToolResult`

```python
class ToolResult:
    ok: bool
    data: dict | None
    error: str | None
    trace_id: str
    latency_ms: int
```