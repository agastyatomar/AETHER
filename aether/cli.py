#!/usr/bin/env python3
"""AETHER CLI - Main command-line interface."""

from __future__ import annotations

import sys
from importlib.metadata import version as pkg_version

__version__ = "0.1.0"

try:
    __version__ = pkg_version("aether")
except Exception:
    pass


def main() -> int:
    """Main CLI entry point."""
    if len(sys.argv) > 1 and sys.argv[1] in ("-v", "--version", "version"):
        print(f"AETHER {__version__}")
        return 0

    print("AETHER - Voice-driven meta-orchestrator for AI agents")
    print(f"Version: {__version__}")
    print()
    print("Usage:")
    print("  aether [command] [options]")
    print()
    print("Commands:")
    print("  run <request>     Execute a voice/text request")
    print("  society           Agent society management")
    print("  skills            Skill management")
    print("  docs              Documentation tools")
    print("  browser           Browser automation tools")
    print("  config            Configuration management")
    print("  version           Show version")
    print()
    print("For more information, visit: https://github.com/agastyatomar/AETHER")
    return 0


if __name__ == "__main__":
    sys.exit(main())