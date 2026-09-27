import importlib


def test_public_demo_blocks_execution(monkeypatch):
    monkeypatch.setenv("AETHER_DEMO_MODE", "1")
    import aether.web.server as server
    server = importlib.reload(server)

    from fastapi.testclient import TestClient

    client = TestClient(server.app)
    response = client.post("/api/command", json={"command": "aether", "args": ["--version"]})
    assert response.json()["returncode"] == 403

    response = client.post("/api/run", json={"request": "anything"})
    assert response.json()["returncode"] == 403

    monkeypatch.delenv("AETHER_DEMO_MODE", raising=False)
    importlib.reload(server)
