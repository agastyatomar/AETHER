# Agent Society Guide

## Overview

The Agent Society is AETHER's substrate for durable, named agents that message each other under a unified safety and governance layer.

## Core Concepts

### Agents
- **Durable identity** — Persistent roster rows with UUIDs
- **Capabilities** — One catalog over plugins, CLIs, MCP servers, skills, core tools
- **Memory** — Personal USER.md/MEMORY.md notebooks, journaled updates
- **Permissions** — Ceiling (SAFE/MONITOR/ASK), grant mode (ALLOWLIST/DENYLIST), grants/denies

### Society Events
All communication goes through typed envelopes (`SocietyEnvelope`) with:
- `MsgType`: ASSIGN, CLAIM, RESULT, VETO, MESSAGE, NOTE, APPROVAL, CHECKPOINT, QUEST, ROOM, ROSTER, DIGEST
- Parity-tested across Python ↔ SQL ↔ Pydantic ↔ TypeScript ↔ UI

### Roster
- Adopt-before-mint by name
- One lead agent (Aether)
- Typed validation
- No chat-session column (derived pure function)

### Scheduler
The **only** path from ASSIGN to work:
- Kill switch
- Tier wall
- Depth ≤ 2
- Target, budgets, caps
- Refusals are VETO envelopes

### Rooms
Bounded discussions:
- 2–6 members
- ≤3 rounds
- ≤10 messages
- Silence allowed
- Restart-safe

### Approvals
Unattended ask-queue:
- Require > always-allow > tier vs ceiling
- Expiry parks, never drops

### Browser Automation
Each agent gets:
- Persistent profile + login sessions
- One-click venv install of browser-use
- `society_browser` tool — the agent's hand

## Getting Started

```python
from aether.society import SocietyRuntime

# Get runtime (lazy singleton)
society = SocietyRuntime.current()

# List agents
agents = society.roster.list_agents()

# Chat with an agent
session = society.chat_binding.ensure_session(agent_id="researcher")
```

## Configuration

Agents are configured via roster rows:
- `provider`, `model`, `effort` — Model selection
- `permission_ceiling` — SAFE | MONITOR | ASK
- `grant_mode` — ALLOWLIST | DENYLIST
- `grants`, `denies` — Tool permissions
- `parent_agent_id` — Creator relationship
- `focus` — Deterministic focus tags

## Safety

Hard no-harm rule: no capability may message, probe, or act on non-consenting external parties at scale.