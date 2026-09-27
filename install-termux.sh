#!/data/data/com.termux/files/usr/bin/bash
# AETHER - Fast Termux (Android) Installer
# Fast mode is the default. Use --full for the slower full setup.
# Usage: ./install-termux.sh [options]

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

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
SKIP_STORAGE=true
FAST=true

log() { [[ "$QUIET" != true ]] && echo -e "${BLUE}[AETHER]${NC} $*" || true; }
log_ok() { [[ "$QUIET" != true ]] && echo -e "${GREEN}[✓]${NC} $*" || true; }
log_warn() { [[ "$QUIET" != true ]] && echo -e "${YELLOW}[!]${NC} $*" || true; }
log_err() { echo -e "${RED}[✗]${NC} $*" >&2; }
die() { log_err "$*"; exit 1; }

setup_termux() {
    log "Checking Termux environment..."

    command -v pkg >/dev/null 2>&1 || die "This installer is for Termux. Run it inside Termux."
    command -v git >/dev/null 2>&1 || { log "Installing git..."; pkg install -y git; }
    command -v python >/dev/null 2>&1 || { log "Installing Python..."; pkg install -y python; }

    if [[ "$SKIP_STORAGE" != true ]]; then
        command -v termux-setup-storage >/dev/null 2>&1 && termux-setup-storage || true
    fi

    # Fast mode deliberately does NOT run pkg update/upgrade.
    # Install only missing runtime/build tools.
    local missing=()
    for cmd in clang make pkg-config rustc cargo; do
        command -v "$cmd" >/dev/null 2>&1 || missing+=("$cmd")
    done

    if (( ${#missing[@]} > 0 )); then
        log "Installing missing build tools..."
        pkg install -y clang make pkg-config rust
    fi

    if ! command -v rustc >/dev/null 2>&1; then
        log "Installing Rust toolchain required by Pydantic 2 on Android..."
        pkg install -y rust
    fi

    log_ok "Termux environment ready"
}

detect_python() {
    for py in python3.13 python3.12 python3.11 python3 python; do
        if command -v "$py" >/dev/null 2>&1; then
            local version
            version=$("$py" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || true)
            if "$py" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
                PYTHON="$py"
                PYTHON_VERSION="$version"
                log_ok "Found Python $PYTHON_VERSION"
                return 0
            fi
        fi
    done
    die "Python 3.11+ not found. Run: pkg install python"
}

create_venv() {
    [[ "$CREATE_VENV" != true ]] && return 0

    if [[ -x "$VENV_DIR/bin/python" ]]; then
        log_ok "Reusing existing virtual environment"
        return 0
    fi

    log "Creating virtual environment..."
    "$PYTHON" -m venv "$VENV_DIR" || die "Could not create venv. Try: pkg reinstall python"
    log_ok "Virtual environment created"
}

install_package() {
    log "Installing AETHER and required dependencies..."
    log "Android/Termux note: Pydantic 2 may build pydantic-core from Rust source on Python 3.14."

    # Do not force old Pydantic on Termux. AETHER uses Pydantic 2.
    if [[ "$CREATE_VENV" == true ]]; then
        "$VENV_DIR/bin/python" -m pip install -e "$INSTALL_DIR"
    else
        "$PYTHON" -m pip install -e "$INSTALL_DIR"
    fi

    if [[ "$INSTALL_DEV" == true ]]; then
        log "Installing development dependencies..."
        if [[ "$CREATE_VENV" == true ]]; then
            "$VENV_DIR/bin/python" -m pip install -r "$INSTALL_DIR/requirements-dev.txt"
        else
            "$PYTHON" -m pip install -r "$INSTALL_DIR/requirements-dev.txt"
        fi
    fi

    log_ok "AETHER package installed"
}

install_browser() {
    [[ "$INSTALL_BROWSER" != true ]] && return 0

    log "Installing optional browser dependencies..."
    log_warn "Browser automation is limited on Android."
    "$VENV_DIR/bin/python" -m pip install browser-use==0.13.10 --no-deps 2>/dev/null || true
    log_ok "Optional browser package installed"
}

create_symlinks() {
    mkdir -p "$BIN_DIR"
    local bin_source="$VENV_DIR/bin"

    [[ "$CREATE_VENV" != true ]] && bin_source="$(dirname "$(command -v "$PYTHON")")"

    for cmd in aether aether-browser-install aether-society; do
        if [[ -f "$bin_source/$cmd" ]]; then
            ln -sf "$bin_source/$cmd" "$BIN_DIR/$cmd"
        fi
    done

    for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
        [[ -f "$rc" ]] || continue
        if ! grep -Fq "$BIN_DIR" "$rc"; then
            echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$rc"
        fi
    done
}

verify_install() {
    log "Verifying installation..."
    local python_cmd="$VENV_DIR/bin/python"
    [[ "$CREATE_VENV" != true ]] && python_cmd="$PYTHON"

    "$python_cmd" -c "import aether; print(f'AETHER {aether.__version__}')" || die "Core import failed"
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
    echo
    echo -e "${BOLD}Run:${NC} ${CYAN}aether --help${NC}"
    echo -e "${BOLD}Activate:${NC} ${CYAN}source $VENV_DIR/bin/activate${NC}"
    echo
    if [[ "$FAST" == true ]]; then
        echo -e "${YELLOW}Fast mode: no full pkg update/upgrade was performed.${NC}"
    else
        echo -e "${YELLOW}Full mode: Termux packages were updated/upgraded.${NC}"
    fi
    echo
}

usage() {
    cat <<EOF
Usage: $0 [options]

Fast mode is the default.

Options:
  --fast             Use fast installation (default)
  --full             Full setup: update/upgrade Termux packages
  --dev              Install development dependencies
  --browser          Install optional browser package
  --no-venv          Skip virtual environment creation
  --prefix DIR       Install to custom directory (default: ~/aether)
  --bin-dir DIR      Custom bin directory (default: ~/.local/bin)
  --branch BRANCH    Git branch to clone (default: main)
  --force            Force reinstall
  --storage          Request Termux storage permission
  --quiet            Suppress non-error output
  --help             Show this help
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --fast) FAST=true ;;
            --full) FAST=false ;;
            --dev) INSTALL_DEV=true ;;
            --browser) INSTALL_BROWSER=true ;;
            --no-venv) CREATE_VENV=false ;;
            --prefix) [[ $# -ge 2 ]] || die "--prefix requires a directory"; INSTALL_DIR="$2"; shift ;;
            --bin-dir) [[ $# -ge 2 ]] || die "--bin-dir requires a directory"; BIN_DIR="$2"; shift ;;
            --branch) [[ $# -ge 2 ]] || die "--branch requires a branch"; BRANCH="$2"; shift ;;
            --force) FORCE=true ;;
            --storage) SKIP_STORAGE=false ;;
            --quiet) QUIET=true ;;
            --help) usage; exit 0 ;;
            *) die "Unknown option: $1" ;;
        esac
        shift
    done
}

main() {
    echo -e "${BOLD}${CYAN}AETHER Termux Installer — FAST MODE${NC}"
    echo

    parse_args "$@"

    if [[ "$FAST" != true ]]; then
        log "Full mode enabled: updating Termux packages..."
        command -v pkg >/dev/null 2>&1 || die "Run this inside Termux."
        pkg update -y
        pkg upgrade -y
    fi

    setup_termux
    detect_python

    if [[ "$FORCE" == true && -d "$INSTALL_DIR" ]]; then
        log "Removing existing installation..."
        rm -rf "$INSTALL_DIR"
    fi

    if [[ -d "$INSTALL_DIR/.git" ]]; then
        log "Updating existing repository..."
        cd "$INSTALL_DIR"
        git fetch --depth 1 origin "$BRANCH"
        git checkout "$BRANCH"
        git reset --hard "origin/$BRANCH"
    else
        log "Cloning AETHER..."
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
