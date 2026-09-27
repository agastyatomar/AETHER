"""AETHER Web Server - FastAPI backend with simple UI."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


app = FastAPI(title="AETHER Web UI", version="0.1.0")


class RequestPayload(BaseModel):
    request: str
    async_mode: bool = False


class CommandPayload(BaseModel):
    command: str
    args: list[str] = Field(default_factory=list)


DEMO_MODE = os.getenv("AETHER_DEMO_MODE", "").lower() in {"1", "true", "yes"}
SAFE_COMMANDS = {"aether", "aether-society", "aether-browser-install"}
COMMAND_MODULES = {"aether": "aether", "aether-society": "aether.society.runtime", "aether-browser-install": "aether.society.browser.install"}


@app.get("/")
async def root() -> HTMLResponse:
    """Serve the main web UI."""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AETHER Web UI</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #e6edf3; min-height: 100vh; }
        .header { background: #161b22; border-bottom: 1px solid #30363d; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { font-size: 1.5rem; font-weight: 600; background: linear-gradient(90deg, #58a6ff, #a371f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; }
        .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1.5rem; }
        .card h2 { font-size: 1.1rem; margin-bottom: 1rem; color: #58a6ff; display: flex; align-items: center; gap: 0.5rem; }
        .input-group { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
        input, textarea { flex: 1; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 0.75rem; color: #e6edf3; font-family: inherit; font-size: 0.9rem; }
        input:focus, textarea:focus { outline: none; border-color: #58a6ff; }
        button { background: #238636; color: white; border: none; border-radius: 6px; padding: 0.75rem 1.5rem; font-weight: 600; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #2ea043; }
        button:disabled { background: #30363d; color: #8b949e; cursor: not-allowed; }
        .output { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 1rem; font-family: 'Monaco', 'Menlo', monospace; font-size: 0.85rem; max-height: 400px; overflow-y: auto; white-space: pre-wrap; word-wrap: break-word; }
        .output-line { margin: 0.25rem 0; }
        .output-line.error { color: #f85149; }
        .output-line.success { color: #3fb950; }
        .output-line.info { color: #58a6ff; }
        .status { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.85rem; }
        .status.connected { background: #1f3a2e; color: #3fb950; }
        .status.disconnected { background: #3a1f1f; color: #f85149; }
        .tabs { display: flex; gap: 0.5rem; margin-bottom: 1rem; border-bottom: 1px solid #30363d; padding-bottom: 0.5rem; }
        .tab { padding: 0.5rem 1rem; background: transparent; border: 1px solid transparent; border-radius: 6px 6px 0 0; color: #8b949e; cursor: pointer; }
        .tab.active { background: #161b22; border-color: #30363d; border-bottom-color: #161b22; color: #e6edf3; }
        .tab-panel { display: none; }
        .tab-panel.active { display: block; }
        .command-row { display: flex; gap: 0.5rem; margin-bottom: 0.5rem; }
        .command-row select { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 0.5rem; color: #e6edf3; }
    </style>
</head>
<body>
    <div class="header">
        <h1>AETHER</h1>
        <div class="status disconnected" id="status">Disconnected</div>
    </div>
    <div class="container">
        <div class="tabs">
            <button class="tab active" onclick="showTab('chat')">Chat</button>
            <button class="tab" onclick="showTab('society')">Society</button>
            <button class="tab" onclick="showTab('browser')">Browser</button>
            <button class="tab" onclick="showTab('tools')">Tools</button>
        </div>

        <div id="chat" class="tab-panel active">
            <div class="grid">
                <div class="card">
                    <h2>💬 Run Request</h2>
                    <div class="input-group">
                        <textarea id="requestInput" rows="4" placeholder="Enter your request...&#10;Example: Research the latest AI papers and summarize key findings"></textarea>
                    </div>
                    <button onclick="runRequest()">Run Request</button>
                    <div id="requestOutput" class="output"></div>
                </div>
                <div class="card">
                    <h2>📊 System Info</h2>
                    <button onclick="getVersion()">Get Version</button>
                    <button onclick="getHealth()">Health Check</button>
                    <div id="infoOutput" class="output"></div>
                </div>
            </div>
        </div>

        <div id="society" class="tab-panel">
            <div class="grid">
                <div class="card">
                    <h2>👥 Agent Society</h2>
                    <div class="command-row">
                        <select id="societyCmd">
                            <option value="roster">List Agents (roster)</option>
                            <option value="rooms">List Rooms</option>
                            <option value="quests">List Quests</option>
                            <option value="status">Society Status</option>
                        </select>
                        <button onclick="runSocietyCommand()">Execute</button>
                    </div>
                    <div id="societyOutput" class="output"></div>
                </div>
            </div>
        </div>

        <div id="browser" class="tab-panel">
            <div class="grid">
                <div class="card">
                    <h2>🌐 Browser Automation</h2>
                    <div class="command-row">
                        <select id="browserCmd">
                            <option value="status">Check Status</option>
                            <option value="probe">Probe Browser</option>
                            <option value="install">Install Browser</option>
                        </select>
                        <button onclick="runBrowserCommand()">Execute</button>
                    </div>
                    <div id="browserOutput" class="output"></div>
                </div>
            </div>
        </div>

        <div id="tools" class="tab-panel">
            <div class="grid">
                <div class="card">
                    <h2>🔧 Raw Commands</h2>
                    <div class="input-group">
                        <input type="text" id="rawCommand" placeholder="Command (e.g., aether --version)">
                        <input type="text" id="rawArgs" placeholder="Arguments (space-separated)">
                    </div>
                    <button onclick="runRawCommand()">Execute</button>
                    <div id="rawOutput" class="output"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const ws = new WebSocket(`ws://${location.host}/ws`);
        const statusEl = document.getElementById('status');
        const requestOutput = document.getElementById('requestOutput');
        const infoOutput = document.getElementById('infoOutput');
        const societyOutput = document.getElementById('societyOutput');
        const browserOutput = document.getElementById('browserOutput');
        const rawOutput = document.getElementById('rawOutput');

        ws.onopen = () => {
            statusEl.textContent = 'Connected';
            statusEl.className = 'status connected';
        };
        ws.onclose = () => {
            statusEl.textContent = 'Disconnected';
            statusEl.className = 'status disconnected';
        };
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            appendOutput(data.target, data.line, data.type);
        };

        function appendOutput(targetId, line, type = 'info') {
            const el = document.getElementById(targetId);
            if (!el) return;
            const div = document.createElement('div');
            div.className = `output-line ${type}`;
            div.textContent = line;
            el.appendChild(div);
            el.scrollTop = el.scrollHeight;
        }

        function showTab(tab) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.querySelector(`.tab[onclick="showTab('${tab}')"]`).classList.add('active');
            document.getElementById(tab).classList.add('active');
        }

        async function runRequest() {
            const input = document.getElementById('requestInput').value;
            if (!input.trim()) return alert('Enter a request');
            requestOutput.innerHTML = '';
            appendOutput('requestOutput', `> aether run "${input}"`, 'info');
            try {
                const res = await fetch('/api/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ request: input })
                });
                const data = await res.json();
                if (data.output) data.output.forEach(l => appendOutput('requestOutput', l, l.startsWith('Error') ? 'error' : 'success'));
            } catch (e) {
                appendOutput('requestOutput', `Error: ${e}`, 'error');
            }
        }

        async function getVersion() {
            infoOutput.innerHTML = '';
            appendOutput('infoOutput', '> aether --version', 'info');
            const res = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: 'aether', args: ['--version'] })
            });
            const data = await res.json();
            data.output.forEach(l => appendOutput('infoOutput', l, 'success'));
        }

        async function getHealth() {
            appendOutput('infoOutput', '> health check', 'info');
            const res = await fetch('/api/health');
            const data = await res.json();
            appendOutput('infoOutput', JSON.stringify(data, null, 2), 'success');
        }

        async function runSocietyCommand() {
            const cmd = document.getElementById('societyCmd').value;
            societyOutput.innerHTML = '';
            appendOutput('societyOutput', `> aether-society ${cmd}`, 'info');
            const res = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: 'aether-society', args: [cmd] })
            });
            const data = await res.json();
            data.output.forEach(l => appendOutput('societyOutput', l, l.startsWith('Error') ? 'error' : 'success'));
        }

        async function runBrowserCommand() {
            const cmd = document.getElementById('browserCmd').value;
            browserOutput.innerHTML = '';
            appendOutput('browserOutput', `> aether-browser-install ${cmd}`, 'info');
            const res = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: 'aether-browser-install', args: [cmd === 'status' ? '--status' : cmd === 'probe' ? '--probe' : '--system-deps'] })
            });
            const data = await res.json();
            data.output.forEach(l => appendOutput('browserOutput', l, l.startsWith('Error') ? 'error' : 'success'));
        }

        async function runRawCommand() {
            const cmd = document.getElementById('rawCommand').value;
            const args = document.getElementById('rawArgs').value.split(' ').filter(Boolean);
            rawOutput.innerHTML = '';
            appendOutput('rawOutput', `> ${cmd} ${args.join(' ')}`, 'info');
            const res = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: cmd, args })
            });
            const data = await res.json();
            data.output.forEach(l => appendOutput('rawOutput', l, l.startsWith('Error') ? 'error' : 'success'));
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html)


@app.get("/api/health")
async def health() -> dict[str, Any]:
    return {"status": "ok", "service": "aether-web"}


@app.get("/api/version")
async def version() -> dict[str, str]:
    return {"version": "0.1.0"}


@app.post("/api/run")
async def run_request(payload: RequestPayload) -> dict[str, Any]:
    """Run an AETHER request unless public-demo mode disables execution."""
    if DEMO_MODE:
        return {"output": ["Request execution is disabled in public demo mode."], "returncode": 403}
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "aether", "run", payload.request],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=Path(__file__).parents[2],
        )
        output = proc.stdout.strip().split("\n") if proc.stdout else []
        if proc.stderr:
            output.extend(proc.stderr.strip().split("\n"))
        return {"output": output, "returncode": proc.returncode}
    except subprocess.TimeoutExpired:
        return {"output": ["Error: Request timed out"], "returncode": -1}
    except Exception as e:
        return {"output": [f"Error: {e}"], "returncode": -1}


@app.post("/api/command")
async def run_command(payload: CommandPayload) -> dict[str, Any]:
    """Execute an allow-listed AETHER command."""
    if DEMO_MODE:
        return {"output": ["Command execution is disabled in public demo mode."], "returncode": 403}
    if payload.command not in SAFE_COMMANDS:
        return {"output": ["Command is not allow-listed."], "returncode": 403}
    try:
        proc = subprocess.run(
            [sys.executable, "-m", COMMAND_MODULES[payload.command], *payload.args],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=Path(__file__).parents[2]
        )
        output = proc.stdout.strip().split('\n') if proc.stdout else []
        if proc.stderr:
            output.extend(proc.stderr.strip().split('\n'))
        return {"output": output, "returncode": proc.returncode}
    except subprocess.TimeoutExpired:
        return {"output": ["Error: Command timed out"], "returncode": -1}
    except Exception as e:
        return {"output": [f"Error: {e}"], "returncode": -1}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass


def create_app() -> FastAPI:
    return app


def run_server(host: str = "127.0.0.1", port: int = 8080) -> None:
    import uvicorn
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    run_server()