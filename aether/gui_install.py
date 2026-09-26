#!/usr/bin/env python3
"""AETHER GUI Installer - Entry point for python -m aether.gui_install"""

from __future__ import annotations

import sys
import tkinter as tk

from aether.gui.installer import main as installer_main


def main() -> int:
    """Entry point for GUI installer."""
    try:
        installer_main()
        return 0
    except Exception as e:
        print(f"GUI Installer error: {e}", file=sys.stderr)
        # Fallback to CLI
        try:
            root = tk.Tk()
            root.withdraw()
            from tkinter import messagebox
            messagebox.showerror("AETHER GUI Installer", f"Failed to start GUI installer:\n{e}\n\nPlease use the CLI installer instead.")
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(main())