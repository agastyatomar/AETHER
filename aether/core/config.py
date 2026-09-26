"""Core configuration management."""

from __future__ import annotations

import os
from pathlib import Path

__all__ = ["DATA_DIR", "get_provider_secret", "get_aether_agent_secret", "override_provider_secrets"]


def _default_data_dir() -> Path:
    """Get default data directory."""
    if "AETHER_DATA_DIR" in os.environ:
        return Path(os.environ["AETHER_DATA_DIR"])
    return Path.home() / ".local" / "share" / "aether"


DATA_DIR: Path = _default_data_dir()


def get_provider_secret(provider: str) -> str | None:
    """Get API secret for a provider."""
    env_var = f"AETHER_{provider.upper()}_API_KEY"
    return os.environ.get(env_var)


def get_aether_agent_secret(provider: str) -> str | None:
    """Get Aether agent secret for a provider."""
    return get_provider_secret(provider)


def override_provider_secrets(secrets: dict[str, str]) -> None:
    """Override provider secrets (for testing)."""
    for provider, secret in secrets.items():
        env_var = f"AETHER_{provider.upper()}_API_KEY"
        os.environ[env_var] = secret