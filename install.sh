#!/usr/bin/env bash
# AETHER - Cross-platform installer for Linux, macOS, Termux, WSL
# Usage: curl -fsSL https://raw.githubusercontent.com/agastyatomar/AETHER/main/install.sh | bash
#        curl -fsSL https://raw.githubusercontent.com/agastyatomar/AETHER/main/install.sh | bash -s -- [options]

set -euo pipefail

# ─── Colors ───
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ─── Config ───
REPO_URL="https://github.com/agastyatomar/AETHER.git"
BRANCH="main"
INSTALL_DIR="${AETHER_INSTALL_DIR:-$HOME/.local/share/aether}"
VENV_DIR="${AETHER_VENV_DIR:-$INSTALL_DIR/venv}"
BIN_DIR="${AETHER_BIN_DIR:-$HOME/.local/bin}"
CREATE_VENV=true
INSTALL_DEV=false
INSTALL_BROWSER=false
SYSTEM_DEPS=false
FORCE=false
QUIET=false

# ─── Helpers ───
log() { [[ "$QUIET" != true ]] && echo -e "${BLUE}[AETHER]${NC} $*" || true; }
log_ok() { [[ "$QUIET" != true ]] && echo -e "${GREEN}[✓]${NC} $*" || true; }
log_warn() { [[ "$QUIET" != true ]] && echo -e "${YELLOW}[!]${NC} $*" || true; }
log_err() { echo -e "${RED}[✗]${NC} $*" >&2; }
die() { log_err "$*"; exit 1; }

command_exists() { command -v "$1" >/dev/null 2>&1; }

detect_os() {
    case "$(uname -s)" in
        Linux*)     OS="linux";;
        Darwin*)    OS="macos";;
        CYGWIN*|MINGW*|MSYS*) OS="windows";;
        *)          OS="unknown";;
    esac
    
    # Detect Termux
    if [[ -n "${TERMUX_VERSION:-}" ]] || [[ "$PREFIX" == *"com.termux"* ]]; then
        OS="termux"
    fi
    
    # Detect WSL
    if [[ -f /proc/version ]] && grep -qi microsoft /proc/version; then
        OS="wsl"
    fi
    
    log "Detected OS: $OS"
}

detect_python() {
    for py in python3.13 python3.12 python3.11 python3 python; do
        if command_exists "$py"; then
            local version=$("$py" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
            if [[ "$(echo "$version >= 3.11" | bc -l 2>/dev/null || python3 -c "import sys; print(int(sys.version_info >= (3, 11)))")" == "1" ]]; then
                PYTHON="$py"
                PYTHON_VERSION="$version"
                log_ok "Found Python $PYTHON_VERSION at $(command -v "$py")"
                return 0
            fi
        fi
    done
    die "Python 3.11+ not found. Please install Python 3.11 or newer."
}

install_system_deps() {
    [[ "$SYSTEM_DEPS" != true ]] && return 0
    
    log "Installing system dependencies for $OS..."
    
    case "$OS" in
        linux)
            if command_exists apt-get; then
                sudo apt-get update && sudo apt-get install -y \
                    build-essential python3-dev libsqlite3-dev \
                    libssl-dev libffi-dev zlib1g-dev \
                    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
                    libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
                    libxdamage1 libxfixes3 libxrandr2 libgbm1 \
                    libasound2 libpango-1.0-0 libcairo2
            elif command_exists dnf; then
                sudo dnf install -y \
                    gcc gcc-c++ make python3-devel sqlite-devel \
                    openssl-devel libffi-devel zlib-devel \
                    nss nspr atk at-spi2-atk cups-libs libdrm \
                    libxkbcommon libXcomposite libXdamage libXfixes \
                    libXrandr mesa-libgbm alsa-lib pango cairo
            elif command_exists pacman; then
                sudo pacman -S --needed --noconfirm \
                    base-devel python sqlite openssl libffi zlib \
                    nss nspr atk at-spi2-atk cups libdrm \
                    libxkbcommon libxcomposite libxdamage libxfixes \
                    libxrandr mesa alsa-lib pango cairo
            elif command_exists zypper; then
                sudo zypper install -y \
                    gcc gcc-c++ make python3-devel sqlite3-devel \
                    libopenssl-devel libffi-devel zlib-devel \
                    mozilla-nss nspr atk at-spi2-atk cups-libs libdrm \
                    libxkbcommon libXcomposite libXdamage libXfixes \
                    libXrandr Mesa-libgbm alsa pango cairo
            else
                log_warn "Unknown package manager. Please install build dependencies manually."
            fi
            ;;
        macos)
            if command_exists brew; then
                brew install python sqlite openssl libffi
                # Playwright deps
                brew install nss nspr atk at-spi2-atk cups libdrm \
                    libxkbcommon libxcomposite libxdamage libxfixes \
                    libxrandr mesa alsa-lib pango cairo
            else
                log_warn "Homebrew not found. Please install dependencies manually."
            fi
            ;;
        termux)
            pkg update && pkg install -y \
                build-essential python libsqlite openssl libffi \
                libandroid-support
            ;;
        wsl)
            # Use Linux deps
            install_system_deps
            ;;
        *)
            log_warn "Unknown OS. Skipping system dependencies."
            ;;
    esac
}

create_venv() {
    [[ "$CREATE_VENV" != true ]] && return 0
    
    log "Creating virtual environment at $VENV_DIR..."
    "$PYTHON" -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install --upgrade pip setuptools wheel
    log_ok "Virtual environment created"
}

install_package() {
    log "Installing AETHER package..."
    
    local pip_cmd="$VENV_DIR/bin/pip"
    [[ "$CREATE_VENV" != true ]] && pip_cmd="pip"
    
    # ARM64: install pydantic v1 (pure Python) first to avoid Rust compilation
    if [[ "$(uname -m)" == "aarch64" ]] || [[ "$OS" == "termux" ]]; then
        log "ARM64 detected: installing pydantic v1 (no Rust)..."
        "$pip_cmd" install "pydantic>=1.10,<2.0"
    fi
    
    # Install core package in editable mode
    "$pip_cmd" install -e "$INSTALL_DIR"
    
    if [[ "$INSTALL_DEV" == true ]]; then
        log "Installing development dependencies..."
        "$pip_cmd" install -r "$INSTALL_DIR/requirements-dev.txt"
    fi
    
    log_ok "Package installed"
}

install_browser() {
    [[ "$INSTALL_BROWSER" != true ]] && return 0
    
    log "Installing browser automation runtime..."
    
    local python_cmd="$VENV_DIR/bin/python"
    [[ "$CREATE_VENV" != true ]] && python_cmd="python"
    
    # Run the managed browser installer
    "$python_cmd" -m aether.society.browser.install ${SYSTEM_DEPS:+--system-deps}
    
    log_ok "Browser automation installed"
}

create_symlinks() {
    log "Creating symlinks in $BIN_DIR..."
    mkdir -p "$BIN_DIR"
    
    local bin_source="$VENV_DIR/bin"
    [[ "$CREATE_VENV" != true ]] && bin_source="$(dirname "$(command -v "$PYTHON")")"
    
    for cmd in aether aether-browser-install aether-society; do
        if [[ -f "$bin_source/$cmd" ]]; then
            ln -sf "$bin_source/$cmd" "$BIN_DIR/$cmd"
            log_ok "Linked $cmd -> $BIN_DIR/$cmd"
        fi
    done
    
    # Add to PATH if not already
    case ":$PATH:" in
        *":$BIN_DIR:"*) ;;
        *)
            log_warn "Add $BIN_DIR to your PATH:"
            echo "  export PATH=\"\$PATH:$BIN_DIR\""
            ;;
    esac
}

verify_install() {
    log "Verifying installation..."
    
    local python_cmd="$VENV_DIR/bin/python"
    [[ "$CREATE_VENV" != true ]] && python_cmd="python"
    
    # Test core import
    "$python_cmd" -c "import aether; print(f'AETHER {aether.__version__}')" 2>/dev/null || die "Core import failed"
    
    # Test CLI
    "$VENV_DIR/bin/aether" --version 2>/dev/null || log_warn "CLI not in PATH (add $BIN_DIR)"
    
    log_ok "Installation verified"
}

print_summary() {
    echo
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}   AETHER Installation Complete!${NC}"
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${NC}"
    echo
    echo -e "  ${BOLD}Install directory:${NC} $INSTALL_DIR"
    echo -e "  ${BOLD}Virtual env:${NC} $VENV_DIR"
    echo -e "  ${BOLD}Bin directory:${NC} $BIN_DIR"
    echo
    echo -e "${BOLD}Next steps:${NC}"
    echo -e "  1. Add to PATH: ${CYAN}export PATH=\"\$PATH:$BIN_DIR\"${NC}"
    echo -e "  2. Activate venv: ${CYAN}source $VENV_DIR/bin/activate${NC}"
    echo -e "  3. Run AETHER: ${CYAN}aether --help${NC}"
    echo
    [[ "$INSTALL_BROWSER" == true ]] && echo -e "  Browser automation: ${CYAN}aether-browser-install --probe${NC}"
    echo
    echo -e "  Documentation: ${CYAN}https://github.com/agastyatomar/AETHER/wiki${NC}"
    echo
}

# ─── Argument Parsing ───
usage() {
    cat <<EOF
Usage: $0 [options]

Options:
  --dev              Install development dependencies
  --browser          Install browser automation runtime
  --system-deps      Install system dependencies (requires sudo)
  --no-venv          Skip virtual environment creation
  --prefix DIR       Install to custom directory (default: ~/.local/share/aether)
  --bin-dir DIR      Custom bin directory (default: ~/.local/bin)
  --branch BRANCH    Git branch to clone (default: main)
  --force            Force reinstall (remove existing)
  --quiet            Suppress non-error output
  --help             Show this help

Examples:
  $0                          # Basic install
  $0 --dev --browser          # Full dev install with browser
  $0 --system-deps --browser  # With system deps (sudo)
  $0 --prefix /opt/aether     # Custom install location
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dev) INSTALL_DEV=true ;;
            --browser) INSTALL_BROWSER=true ;;
            --system-deps) SYSTEM_DEPS=true ;;
            --no-venv) CREATE_VENV=false ;;
            --prefix) INSTALL_DIR="$2"; shift ;;
            --bin-dir) BIN_DIR="$2"; shift ;;
            --branch) BRANCH="$2"; shift ;;
            --force) FORCE=true ;;
            --quiet) QUIET=true ;;
            --help) usage; exit 0 ;;
            *) die "Unknown option: $1" ;;
        esac
        shift
    done
}

# ─── Main ───
main() {
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}   AETHER Installer${NC}"
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${NC}"
    echo
    
    parse_args "$@"
    detect_os
    detect_python
    
    # Force reinstall
    if [[ "$FORCE" == true && -d "$INSTALL_DIR" ]]; then
        log "Removing existing installation..."
        rm -rf "$INSTALL_DIR"
    fi
    
    # Clone or update repository
    if [[ -d "$INSTALL_DIR/.git" ]]; then
        log "Updating existing repository..."
        cd "$INSTALL_DIR"
        git fetch origin
        git checkout "$BRANCH"
        git pull origin "$BRANCH"
    else
        log "Cloning repository..."
        git clone --branch "$BRANCH" --depth 1 "$REPO_URL" "$INSTALL_DIR"
    fi
    
    install_system_deps
    create_venv
    install_package
    install_browser
    create_symlinks
    verify_install
    print_summary
}

main "$@"