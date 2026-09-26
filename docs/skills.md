# Skill Development

## Overview

AETHER's skill system allows creating reusable, versioned capabilities that agents can learn and execute.

## Skill Structure

```
skills/
├── builtin/
│   └── my-skill/
│       ├── skill.yaml          # Manifest
│       ├── main.py             # Implementation
│       ├── tests/
│       │   └── test_skill.py
│       └── README.md
└── user/
    └── custom-skill/
        ├── skill.yaml
        └── main.py
```

## Skill Manifest (skill.yaml)

```yaml
name: my-skill
version: "1.0.0"
description: "What this skill does"
author: "Your Name"
license: "MIT"
tags: ["category", "tags"]
capabilities:
  - name: my_action
    description: "Action description"
    params:
      param1:
        type: string
        description: "Parameter description"
        required: true
    returns:
      type: object
      description: "Return value description"
dependencies:
  - requests>=2.31.0
entry_point: main:MySkill
```

## Implementation (main.py)

```python
from aether.skills import Skill, SkillContext, skill_action

class MySkill(Skill):
    """Skill description."""
    
    @skill_action
    async def my_action(self, ctx: SkillContext, param1: str) -> dict:
        """Action description."""
        # Your implementation
        return {"result": f"Processed {param1}"}

# Entry point
def create_skill(config: dict) -> MySkill:
    return MySkill(config)
```

## Creating a Skill

```bash
# Create skill template
aether skill create my-skill

# Edit skill manifest and implementation
# skills/builtin/my-skill/skill.yaml
# skills/builtin/my-skill/main.py

# Test skill
aether skill test my-skill

# Publish to registry
aether skill publish my-skill
```

## Skill Registry

Skills are registered in `SkillRegistry`:
- Hot-reload via watchdog
- Parity with TypeScript registry
- Origin tracking (builtin/user/marketplace)

## Automatic Learning

Agents can learn skills from digests:
1. Digest created from agent interaction
2. `learning.py` converts digest → skill
3. Skill added to agent's namespace
4. Promotable to global registry as draft

## Testing

```python
# tests/test_skill.py
import pytest
from skills.builtin.my_skill.main import MySkill

@pytest.fixture
def skill():
    return MySkill({})

@pytest.mark.asyncio
async def test_my_action(skill):
    result = await skill.my_action(SkillContext(), "test")
    assert result["result"] == "Processed test"
```

Run tests:
```bash
pytest skills/builtin/my-skill/tests/
```

## Best Practices

1. **Single responsibility** — One skill, one domain
2. **Typed interfaces** — Use Pydantic for params/returns
3. **Idempotent actions** — Safe to retry
4. **Explicit capabilities** — Declare what the skill can do
5. **Minimal dependencies** — Only what's necessary
6. **Documentation** — README with examples