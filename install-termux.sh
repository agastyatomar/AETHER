#!/data/data/com.termux/files/usr/bin/bash
# AETHER - Termux (Android) Optimized Installer
# Usage: ./install-termux.sh [options]

set -euo pipefail

# ─── Colors ───
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ─── Config ───
REPO_URL="https://github.com/agastyatomar/AETHER.git"
BRANCH="main"
INSTALL_DIR="${AETHER_INSTALL_DIR:-$HOME/aether}"
VENV_DIR="${AETHER_VENV_DIR:-$INSTALL_DIR/venv}"
BIN_DIR="${AETHER_BIN_DIR:-$HOME/.local/bin}"
CREATE_VENV=true
INSTALL_DEV=false
INSTALL_BROWSER=false
FORCE=false
QUIET=false
SKIP_STORAGE=false

# ─── Helpers ───
log() { [[ "$QUIET" != true ]] && echo -e "${BLUE}[AETHER]${NC} $*" || true; }
log_ok() { [[ "$QUIET" != true ]] && echo -e "${GREEN}[✓]${NC} $*" || true; }
log_warn() { [[ "$QUIET" != true ]] && echo -e "${YELLOW}[!]${NC} $*" || true; }
log_err() { echo -e "${RED}[✗]${NC} $*" >&2; }
die() { log_err "$*"; exit 1; }

setup_termux() {
    log "Setting up Termux environment..."
    
    # Grant storage permission if not skipped
    if [[ "$SKIP_STORAGE" != true ]]; then
        log "Requesting storage permission..."
        termux-setup-storage || log_warn "Storage permission denied (continuing anyway)"
    fi
    
    # Update packages
    log "Updating Termux packages..."
    pkg update -y && pkg upgrade -y
    
    # Install essential packages
    log "Installing essential packages..."
    pkg install -y \
        git python build-essential libsqlite openssl libffi \
        libandroid-support clang binutils \
        termux-api termux-tools
    
    # Fix Python symlink if needed
    if ! command -v python3.11 &>/dev/null && ! command -v python3.12 &>/dev/null; then
        log_warn "Python 3.11+ not available in Termux repos yet. Using default python3."
    fi
    
    log_ok "Termux environment ready"
}

detect_python() {
    for py in python3.13 python3.12 python3.11 python3 python; do
        if command -v "$py" &>/dev/null; then
            local version=$("$py" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null)
            if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
                PYTHON="$py"
                PYTHON_VERSION="$version"
                log_ok "Found Python $PYTHON_VERSION at $(command -v "$py")"
                return 0
            fi
        fi
    done
    die "Python 3.11+ not found. Run 'pkg install python' and ensure version >= 3.11"
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
    
    # ARM64/Termux: install pydantic v1 (pure Python) first to avoid Rust compilation
    if [[ "$(uname -m)" == "aarch64" ]] || [[ "$OS" == "termux" ]]; then
        log "ARM64 detected: installing pydantic v1 (no Rust)..."
        "$pip_cmd" install "pydantic>=1.10,<2.0"
    fi
    
    # Install core package
    "$pip_cmd" install -e "$INSTALL_DIR"
    
    if [[ "$INSTALL_DEV" == true ]]; then
        log "Installing development dependencies..."
        "$pip_cmd" install -r "$INSTALL_DIR/requirements-dev.txt"
    fi
    
    log_ok "Package installed"
}

install_browser() {
    [[ "$INSTALL_BROWSER" != true ]] && return 0
    
    log "Installing browser automation (limited on Android)..."
    log_warn "Note: Full browser automation requires rooted device or proot-distro"
    log_warn "Installing minimal browser-use dependencies only..."
    
    local python_cmd="$VENV_DIR/bin/python"
    [[ "$CREATE_VENV" != true ]] && python_cmd="python"
    
    # Install browser-use without playwright (use system webview if available)
    "$pip_cmd" install browser-use==0.13.10 --no-deps 2>/dev/null || true
    
    log_ok "Browser dependencies installed (limited functionality)"
}

create_symlinks() {
    log "Creating symlinks..."
    mkdir -p "$BIN_DIR"
    
    local bin_source="$VENV_DIR/bin"
    [[ "$CREATE_VENV" != true ]] && bin_source="$(dirname "$(command -v "$PYTHON")")"
    
    for cmd in aether aether-browser-install aether-society; do
        if [[ -f "$bin_source/$cmd" ]]; then
            ln -sf "$bin_source/$cmd" "$BIN_DIR/$cmd"
            log_ok "Linked $cmd"
        fi
    done
    
    # Add to PATH in shell config
    for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
        [[ -f "$rc" ]] || continue
        if ! grep -q "$BIN_DIR" "$rc"; then
            echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$rc"
            log_ok "Added $BIN_DIR to PATH in $rc"
        fi
    done
}

verify_install() {
    log "Verifying installation..."
    
    local python_cmd="$VENV_DIR/bin/python"
    [[ "$CREATE_VENV" != true ]] && python_cmd="python"
    
    "$python_cmd" -c "import aether; print(f'AETHER {aether.__version__}')" 2>/dev/null || die "Core import failed"
    
    log_ok "Installation verified"
}

print_summary() {
    echo
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}   AETHER Termux Installation Complete!${NC}"
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${NC}"
    echo
    echo -e "  ${BOLD}Install directory:${NC} $INSTALL_DIR"
    echo -e "  ${BOLD}Virtual env:${NC} $VENV_DIR"
    echo -e "  ${BOLD}Bin directory:${NC} $BIN_DIR"
    echo
    echo -e "${BOLD}Next steps:${NC}"
    echo -e "  1. Restart Termux or run: ${CYAN}source ~/.bashrc${NC}"
    echo -e "  2. Activate venv: ${CYAN}source $VENV_DIR/bin/activate${NC}"
    echo -e "  3. Run AETHER: ${CYAN}aether --help${NC}"
    echo
    echo -e "${BOLD}Termux Notes:${NC}"
    echo -e "  • Browser automation is limited on Android"
    echo -e "  • For full browser support, use proot-distro:"
    echo -e "    ${CYAN}pkg install proot-distro && proot-distro install ubuntu${NC}"
    echo -e "  • Keep Termux awake: ${CYAN}termux-wake-lock${NC}"
    echo
    echo -e "  Documentation: ${CYAN}https://github.com/agastyatomar/AETHER/wiki${NC}"
    echo
}

usage() {
    cat <<EOF
Usage: $0 [options]

Options:
  --dev              Install development dependencies
  --browser          Install browser automation (limited on Android)
  --no-venv          Skip virtual environment creation
  --prefix DIR       Install to custom directory (default: ~/aether)
  --bin-dir DIR      Custom bin directory (default: ~/.local/bin)
  --branch BRANCH    Git branch to clone (default: main)
  --force            Force reinstall (remove existing)
  --skip-storage     Skip termux-setup-storage
  --quiet            Suppress non-error output
  --help             Show this help

Examples:
  $0                          # Basic install
  $0 --dev --browser          # Full dev install
  $0 --prefix /data/data/com.termux/files/home/aether
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dev) INSTALL_DEV=true ;;
            --browser) INSTALL_BROWSER=true ;;
            --no-venv) CREATE_VENV=false ;;
            --prefix) INSTALL_DIR="$2"; shift ;;
            --bin-dir) BIN_DIR="$2"; shift ;;
            --branch) BRANCH="$2"; shift ;;
            --force) FORCE=true ;;
            --skip-storage) SKIP_STORAGE=true ;;
            --quiet) QUIET=true ;;
            --help) usage; exit 0 ;;
            *) die "Unknown option: $1" ;;
        esac
        shift
    done
}

main() {
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}   AETHER Termux Installer${NC}"
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${NC}"
    echo
    
    parse_args "$@"
    setup_termux
    detect_python
    
    if [[ "$FORCE" == true && -d "$INSTALL_DIR" ]]; then
        log "Removing existing installation..."
        rm -rf "$INSTALL_DIR"
    fi
    
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
    
    create_venv
    install_package
    install_browser
    create_symlinks
    verify_install
    print_summary
}

main "$@"