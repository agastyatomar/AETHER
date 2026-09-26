# Telemetry & Debugging

## Overview

AETHER includes a flight recorder for production debugging and a replay CLI for post-mortem analysis.

## Flight Recorder

### Features
- JSONL format, daily rotation
- Structured events with trace IDs
- Latency phase tracking
- Configurable retention

### Event Types
- `request_start` / `request_end` — Request lifecycle
- `tool_call` / `tool_result` — Tool execution
- `latency_phase` — Latency phases (queue, exec, network)
- `error` — Errors with context
- `agent_spawn` / `agent_complete` — Agent lifecycle

### Configuration

```python
from aether.telemetry import FlightRecorder

recorder = FlightRecorder(
    data_dir=Path("data/flight_recorder"),
    rotation="daily",
    retention_days=30,
    buffer_size=1000,
)
```

### Writing Events

```python
recorder.record(
    kind="tool_call",
    trace_id="abc-123",
    agent_id="researcher",
    tool="web_search",
    params={"query": "AI news"},
    latency_ms=150,
)
```

## Replay CLI

```bash
# List traces
python -m aether.telemetry.replay --list

# Replay a trace
python -m aether.telemetry.replay <trace_id>

# Replay with JSON output
python -m aether.telemetry.replay <trace_id> --json

# Replay from custom data dir
python -m aether.telemetry.replay <trace_id> --data-dir data/flight_recorder
```

## Latency Tracking

### Phases
- `queue` — Time waiting for scheduler
- `exec` — Tool execution time
- `network` — External API calls
- `model` — LLM inference
- `browser` — Browser automation

### Usage

```python
from aether.telemetry.latency import LatencyTracker, LatencyPhase

tracker = LatencyTracker.get()

with tracker.span("web_search", LatencyPhase.NETWORK):
    result = await search_web(query)

# Or manual
span = tracker.start_span("custom_op", LatencyPhase.EXEC)
try:
    result = await custom_operation()
finally:
    span.end()
```

## Debugging Tips

### Enable Debug Logging

```bash
export AETHER_LOG_LEVEL=DEBUG
aether run "your request"
```

### Inspect Flight Recorder

```bash
# View recent events
tail -f data/flight_recorder/flight-$(date +%Y-%m-%d).jsonl | jq .

# Filter by trace
grep "trace_id.*abc-123" data/flight_recorder/flight-*.jsonl | jq .

# Filter by agent
grep "agent_id.*researcher" data/flight_recorder/flight-*.jsonl | jq .
```

### Replay Failed Request

```bash
# Find failed trace
grep "error" data/flight_recorder/flight-*.jsonl | tail -5

# Replay
python -m aether.telemetry.replay <trace_id> --json | jq .
```

## Metrics

Key metrics to monitor:
- Request latency (p50, p95, p99)
- Tool success rate
- Agent spawn time
- Browser render time
- Error rate by type

## Privacy

- No PII in flight recorder by default
- Configure `redact_fields` in recorder config
- Local-only, no external transmission