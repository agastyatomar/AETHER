#!/usr/bin/env python3
"""AETHER GUI Installer - Cross-platform graphical installer using tkinter."""

from __future__ import annotations

import asyncio
import os
import platform
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Optional

import urllib.request


class InstallerApp:
    """Main GUI installer application."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AETHER Installer")
        self.root.geometry("640x520")
        self.root.resizable(False, False)
        self.root.minsize(600, 480)

        # State
        self.install_dir = Path.home() / ".local" / "share" / "aether"
        self.venv_dir = self.install_dir / "venv"
        self.bin_dir = Path.home() / ".local" / "bin"
        self.create_venv = True
        self.install_dev = False
        self.install_browser = False
        self.system_deps = False
        self.install_thread: Optional[threading.Thread] = None
        self.cancelled = False

        # Detect OS
        self.os_name = platform.system().lower()
        self.is_windows = self.os_name == "windows"
        self.is_macos = self.os_name == "darwin"
        self.is_linux = self.os_name == "linux"
        self.is_termux = "TERMUX_VERSION" in os.environ or "com.termux" in os.environ.get("PREFIX", "")

        # Python detection
        self.python_cmd = self._detect_python()

        self._setup_ui()
        self._center_window()

    def _detect_python(self) -> str:
        """Detect available Python 3.11+."""
        for cmd in ["python3.13", "python3.12", "python3.11", "python3", "python"]:
            if shutil.which(cmd):
                try:
                    result = subprocess.run(
                        [cmd, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
                        capture_output=True, text=True, timeout=5
                    )
                    if result.returncode == 0:
                        version = result.stdout.strip()
                        major, minor = map(int, version.split("."))
                        if major > 3 or (major == 3 and minor >= 11):
                            return cmd
                except Exception:
                    continue
        return "python3"

    def _setup_ui(self):
        """Setup the user interface."""
        # Style
        style = ttk.Style()
        style.theme_use("clam" if not self.is_windows else "vista")
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1e3a5f")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10), foreground="#555")
        style.configure("Heading.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

        # Main container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Logo/Icon placeholder
        logo_label = ttk.Label(header_frame, text="🌌", font=("Segoe UI", 32))
        logo_label.pack(side=tk.LEFT, padx=(0, 15))

        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(title_frame, text="AETHER", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(title_frame, text="Voice-driven meta-orchestrator for AI agents", style="Subtitle.TLabel").pack(anchor=tk.W)
        ttk.Label(title_frame, text="Version 0.1.0", style="Subtitle.TLabel").pack(anchor=tk.W)

        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 15))

        # Installation options
        options_frame = ttk.LabelFrame(main_frame, text=" Installation Options ", padding=15)
        options_frame.pack(fill=tk.X, pady=(0, 15))

        # Install directory
        dir_frame = ttk.Frame(options_frame)
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(dir_frame, text="Install Directory:").pack(anchor=tk.W)
        dir_entry_frame = ttk.Frame(dir_frame)
        dir_entry_frame.pack(fill=tk.X, pady=(5, 0))
        self.dir_var = tk.StringVar(value=str(self.install_dir))
        self.dir_entry = ttk.Entry(dir_entry_frame, textvariable=self.dir_var, width=50)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(dir_entry_frame, text="Browse", command=self._browse_dir).pack(side=tk.LEFT, padx=(5, 0))

        # Checkboxes
        check_frame = ttk.Frame(options_frame)
        check_frame.pack(fill=tk.X)

        self.venv_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(check_frame, text="Create virtual environment (recommended)", variable=self.venv_var).pack(anchor=tk.W, pady=2)

        self.dev_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(check_frame, text="Install development dependencies", variable=self.dev_var).pack(anchor=tk.W, pady=2)

        self.browser_var = tk.BooleanVar(value=False)
        self.browser_check = ttk.Checkbutton(check_frame, text="Install browser automation (requires system deps)", variable=self.browser_var)
        self.browser_check.pack(anchor=tk.W, pady=2)

        self.sysdeps_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(check_frame, text="Install system dependencies (requires sudo/admin)", variable=self.sysdeps_var).pack(anchor=tk.W, pady=2)

        # Platform-specific notes
        if self.is_windows:
            note = "Note: Browser automation requires Visual Studio Build Tools"
        elif self.is_macos:
            note = "Note: Browser automation requires Xcode Command Line Tools"
        elif self.is_termux:
            note = "Note: Browser automation is limited on Android; use proot-distro for full support"
        else:
            note = "Note: Browser automation requires build-essential and system libraries"

        ttk.Label(options_frame, text=note, style="Subtitle.TLabel", foreground="#888").pack(anchor=tk.W, pady=(10, 0))

        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text=" Progress ", padding=15)
        progress_frame.pack(fill=tk.X, pady=(0, 15))

        self.status_var = tk.StringVar(value="Ready to install")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.pack(anchor=tk.W)

        self.progress = ttk.Progressbar(progress_frame, mode="determinate", maximum=100)
        self.progress.pack(fill=tk.X, pady=(5, 0))

        self.detail_var = tk.StringVar(value="")
        self.detail_label = ttk.Label(progress_frame, textvariable=self.detail_var, style="Subtitle.TLabel", foreground="#666")
        self.detail_label.pack(anchor=tk.W, pady=(5, 0))

        # Log area
        log_frame = ttk.LabelFrame(main_frame, text=" Log ", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 8))
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT, padx=(5, 0))
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        self.cancel_btn = ttk.Button(button_frame, text="Cancel", command=self._cancel_install, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT)

        ttk.Button(button_frame, text="Quit", command=self.root.quit).pack(side=tk.RIGHT, padx=(5, 0))

        self.install_btn = ttk.Button(button_frame, text="Install AETHER", command=self._start_install, style="Accent.TButton")
        self.install_btn.pack(side=tk.RIGHT)

    def _center_window(self):
        """Center window on screen."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")

    def _browse_dir(self):
        """Browse for install directory."""
        from tkinter import filedialog
        dir_path = filedialog.askdirectory(initialdir=str(self.install_dir.parent), title="Select Install Directory")
        if dir_path:
            self.install_dir = Path(dir_path) / "aether"
            self.venv_dir = self.install_dir / "venv"
            self.dir_var.set(str(self.install_dir))

    def _log(self, message: str):
        """Add message to log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _update_status(self, status: str, detail: str = "", progress: int = -1):
        """Update status labels and progress bar."""
        self.status_var.set(status)
        self.detail_var.set(detail)
        if progress >= 0:
            self.progress["value"] = progress
        self.root.update_idletasks()

    def _set_installing(self, installing: bool):
        """Enable/disable controls during installation."""
        self.install_btn.config(state=tk.DISABLED if installing else tk.NORMAL)
        self.cancel_btn.config(state=tk.NORMAL if installing else tk.DISABLED)
        self.dir_entry.config(state=tk.DISABLED if installing else tk.NORMAL)
        self.venv_check.config(state=tk.DISABLED if installing else tk.NORMAL) if hasattr(self, 'venv_check') else None
        self.dev_check.config(state=tk.DISABLED if installing else tk.NORMAL) if hasattr(self, 'dev_check') else None
        self.browser_check.config(state=tk.DISABLED if installing else tk.NORMAL)
        self.sysdeps_check.config(state=tk.DISABLED if installing else tk.NORMAL) if hasattr(self, 'sysdeps_check') else None

    def _start_install(self):
        """Start installation in background thread."""
        self.install_dir = Path(self.dir_var.get())
        self.venv_dir = self.install_dir / "venv"
        self.create_venv = self.venv_var.get()
        self.install_dev = self.dev_var.get()
        self.install_browser = self.browser_var.get()
        self.system_deps = self.sysdeps_var.get()
        self.cancelled = False

        self._set_installing(True)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

        self.install_thread = threading.Thread(target=self._run_install, daemon=True)
        self.install_thread.start()

    def _cancel_install(self):
        """Cancel ongoing installation."""
        self.cancelled = True
        self._update_status("Cancelling...", "Please wait")

    def _run_install(self):
        """Run installation steps."""
        try:
            steps = [
                (5, "Preparing", self._step_prepare),
                (15, "Cloning repository", self._step_clone),
                (30, "Installing system dependencies", self._step_system_deps),
                (50, "Creating virtual environment", self._step_venv),
                (70, "Installing Python package", self._step_install_package),
                (85, "Installing browser automation", self._step_install_browser),
                (95, "Creating shortcuts", self._step_create_shortcuts),
                (100, "Verifying installation", self._step_verify),
            ]

            for progress, status, step_func in steps:
                if self.cancelled:
                    self._update_status("Cancelled", "Installation cancelled by user", 0)
                    self._log("Installation cancelled")
                    self.root.after(0, lambda: self._set_installing(False))
                    return

                self._update_status(status, "", progress)
                step_func()

            self._update_status("Complete!", "AETHER installed successfully", 100)
            self._log("✓ Installation complete!")
            self.root.after(0, self._show_success)

        except Exception as e:
            self._log(f"✗ Error: {e}")
            self._update_status("Failed", str(e), 0)
            self.root.after(0, lambda: messagebox.showerror("Installation Failed", str(e)))
        finally:
            self.root.after(0, lambda: self._set_installing(False))

    def _step_prepare(self):
        """Prepare installation directory."""
        self._log(f"Install directory: {self.install_dir}")
        self._log(f"Python: {self.python_cmd}")
        self._log(f"OS: {platform.system()} {platform.release()}")
        self.install_dir.mkdir(parents=True, exist_ok=True)

    def _step_clone(self):
        """Clone or update repository."""
        repo_dir = self.install_dir
        git_dir = repo_dir / ".git"

        if git_dir.exists():
            self._log("Updating existing repository...")
            subprocess.run(["git", "-C", str(repo_dir), "fetch", "origin"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(repo_dir), "checkout", "main"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(repo_dir), "pull", "origin", "main"], check=True, capture_output=True)
        else:
            self._log("Cloning repository...")
            subprocess.run(
                ["git", "clone", "--branch", "main", "--depth", "1", "https://github.com/agastyatomar/AETHER.git", str(repo_dir)],
                check=True, capture_output=True
            )
        self._log("Repository ready")

    def _step_system_deps(self):
        """Install system dependencies."""
        if not self.system_deps:
            self._log("Skipping system dependencies (not selected)")
            return

        self._log("Installing system dependencies...")
        try:
            if self.is_windows:
                self._install_windows_deps()
            elif self.is_macos:
                self._install_macos_deps()
            elif self.is_linux or self.is_termux:
                self._install_linux_deps()
            self._log("System dependencies installed")
        except subprocess.CalledProcessError as e:
            self._log(f"Warning: System deps install had issues: {e}")
            # Don't fail, continue

    def _install_windows_deps(self):
        """Install Windows dependencies."""
        # Check for winget/choco/scoop
        for pkg_mgr in ["winget", "choco", "scoop"]:
            if shutil.which(pkg_mgr):
                self._log(f"Found {pkg_mgr}, attempting to install build tools...")
                # Non-blocking, best effort
                break

    def _install_macos_deps(self):
        """Install macOS dependencies."""
        if shutil.which("brew"):
            self._log("Homebrew found, installing dependencies...")
            subprocess.run(["brew", "install", "python", "sqlite", "openssl", "libffi"], check=False)
        else:
            self._log("Homebrew not found, skipping system deps")

    def _install_linux_deps(self):
        """Install Linux/Termux dependencies."""
        if self.is_termux:
            self._log("Termux detected, installing packages...")
            subprocess.run(["pkg", "update", "-y"], check=False)
            subprocess.run(["pkg", "install", "-y", "build-essential", "python", "libsqlite", "openssl", "libffi"], check=False)
        else:
            # Try common package managers
            for pm, pkgs in [
                ("apt-get", ["build-essential", "python3-dev", "libsqlite3-dev", "libssl-dev", "libffi-dev", "zlib1g-dev"]),
                ("dnf", ["gcc", "gcc-c++", "make", "python3-devel", "sqlite-devel", "openssl-devel", "libffi-devel", "zlib-devel"]),
                ("pacman", ["base-devel", "python", "sqlite", "openssl", "libffi", "zlib"]),
            ]:
                if shutil.which(pm):
                    self._log(f"Found {pm}, installing dependencies...")
                    cmd = ["sudo", pm, "install", "-y"] + pkgs if pm != "pacman" else ["sudo", pm, "-S", "--needed", "--noconfirm"] + pkgs
                    subprocess.run(cmd, check=False)
                    break

    def _step_venv(self):
        """Create virtual environment."""
        if not self.create_venv:
            self._log("Skipping virtual environment (not selected)")
            return

        self._log(f"Creating virtual environment at {self.venv_dir}...")
        subprocess.run([self.python_cmd, "-m", "venv", str(self.venv_dir)], check=True)
        pip_cmd = self.venv_dir / "Scripts" / "pip.exe" if self.is_windows else self.venv_dir / "bin" / "pip"
        subprocess.run([str(pip_cmd), "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)
        self._log("Virtual environment created")

    def _step_install_package(self):
        """Install AETHER package."""
        self._log("Installing AETHER package...")
        pip_cmd = self.venv_dir / "Scripts" / "pip.exe" if self.is_windows and self.create_venv else (self.venv_dir / "bin" / "pip" if self.create_venv else Path("pip"))
        subprocess.run([str(pip_cmd), "install", "-e", str(self.install_dir)], check=True)
        if self.install_dev:
            self._log("Installing development dependencies...")
            subprocess.run([str(pip_cmd), "install", "-r", str(self.install_dir / "requirements-dev.txt")], check=True)
        self._log("Package installed")

    def _step_install_browser(self):
        """Install browser automation."""
        if not self.install_browser:
            self._log("Skipping browser automation (not selected)")
            return

        self._log("Installing browser automation runtime...")
        python_cmd = self.venv_dir / "Scripts" / "python.exe" if self.is_windows and self.create_venv else (self.venv_dir / "bin" / "python" if self.create_venv else Path("python"))
        cmd = [str(python_cmd), "-m", "aether.society.browser.install"]
        if self.system_deps:
            cmd.append("--system-deps")
        subprocess.run(cmd, check=True)
        self._log("Browser automation installed")

    def _step_create_shortcuts(self):
        """Create command shortcuts."""
        self._log("Creating shortcuts...")
        self.bin_dir.mkdir(parents=True, exist_ok=True)

        bin_source = self.venv_dir / ("Scripts" if self.is_windows else "bin") if self.create_venv else Path(shutil.which(self.python_cmd)).parent

        for cmd in ["aether", "aether-browser-install", "aether-society"]:
            src = bin_source / (cmd + (".exe" if self.is_windows else ""))
            dst = self.bin_dir / (cmd + (".exe" if self.is_windows else ""))
            if src.exists():
                try:
                    if self.is_windows:
                        shutil.copy2(src, dst)
                    else:
                        if dst.exists() or dst.is_symlink():
                            dst.unlink()
                        dst.symlink_to(src)
                    self._log(f"Linked {cmd}")
                except Exception as e:
                    self._log(f"Warning: Could not link {cmd}: {e}")

        self._log("Shortcuts created")

    def _step_verify(self):
        """Verify installation."""
        self._log("Verifying installation...")
        python_cmd = self.venv_dir / "Scripts" / "python.exe" if self.is_windows and self.create_venv else (self.venv_dir / "bin" / "python" if self.create_venv else Path("python"))
        result = subprocess.run([str(python_cmd), "-c", "import aether; print(f'AETHER {aether.__version__}')"], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Import verification failed: {result.stderr}")
        self._log(f"✓ {result.stdout.strip()}")

    def _show_success(self):
        """Show success dialog."""
        msg = (
            f"AETHER installed successfully!\n\n"
            f"Install directory: {self.install_dir}\n"
            f"Virtual environment: {self.venv_dir}\n"
            f"Commands available in: {self.bin_dir}\n\n"
            f"Next steps:\n"
            f"1. Add {self.bin_dir} to your PATH\n"
            f"2. Run 'aether --help' to get started\n"
        )
        if self.install_browser:
            msg += "\n3. Run 'aether-browser-install --probe' to verify browser\n"

        messagebox.showinfo("Installation Complete", msg)


def main():
    """Entry point for GUI installer."""
    root = tk.Tk()
    app = InstallerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()