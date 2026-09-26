<# 
.SYNOPSIS
    AETHER - Windows PowerShell Installer
    
.DESCRIPTION
    Installs AETHER on Windows with optional browser automation and development dependencies.
    
.USAGE
    irm https://raw.githubusercontent.com/agastyatomar/AETHER/main/install.ps1 | iex
    irm https://raw.githubusercontent.com/agastyatomar/AETHER/main/install.ps1 | iex -ArgumentList @('--dev', '--browser')
#>

[CmdletBinding()]
param(
    [switch]$Dev,
    [switch]$Browser,
    [switch]$SystemDeps,
    [switch]$NoVenv,
    [string]$Prefix = "$env:LOCALAPPDATA\aether",
    [string]$BinDir = "$env:USERPROFILE\.local\bin",
    [string]$Branch = "main",
    [switch]$Force,
    [switch]$Quiet
)

# ─── Colors ───
$RED = [ConsoleColor]::Red
$GREEN = [ConsoleColor]::Green
$YELLOW = [ConsoleColor]::Yellow
$BLUE = [ConsoleColor]::Blue
$CYAN = [ConsoleColor]::Cyan
$WHITE = [ConsoleColor]::White

function Write-Log { param($msg) if (-not $Quiet) { Write-Host "[AETHER] $msg" -ForegroundColor $BLUE } }
function Write-Ok { param($msg) if (-not $Quiet) { Write-Host "[✓] $msg" -ForegroundColor $GREEN } }
function Write-Warn { param($msg) if (-not $Quiet) { Write-Host "[!] $msg" -ForegroundColor $Yellow } }
function Write-Err { param($msg) Write-Host "[✗] $msg" -ForegroundColor $RED }
function Write-Header { param($msg) Write-Host "`n$msg`n" -ForegroundColor $CYAN }

function Test-Command { param($name) Get-Command $name -ErrorAction SilentlyContinue }

# ─── Detect Python ───
function Get-Python {
    $candidates = @("python3.13", "python3.12", "python3.11", "python3", "python", "py -3.13", "py -3.12", "py -3.11", "py -3")
    foreach ($c in $candidates) {
        try {
            $version = & $c -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
            if ($version -match '^(\d+)\.(\d+)$') {
                $major = [int]$matches[1]; $minor = [int]$matches[2]
                if ($major -gt 3 -or ($major -eq 3 -and $minor -ge 11)) {
                    Write-Ok "Found Python $version at $(Get-Command $c).Source"
                    return @{ Command = $c; Version = $version }
                }
            }
        } catch { }
    }
    Write-Err "Python 3.11+ not found. Install from https://python.org or use winget install Python.Python.3.12"
    exit 1
}

# ─── Install System Dependencies ───
function Install-SystemDeps {
    if (-not $SystemDeps) { return }
    Write-Log "Installing system dependencies..."
    
    # Check for winget/choco/scoop
    if (Test-Command winget) {
        winget install --id Microsoft.VisualStudio.2022.BuildTools --silent --accept-source-agreements --accept-package-agreements 2>$null || true
    }
    if (Test-Command choco) {
        choco install -y python3 visualstudio2022buildtools 2>$null || true
    }
    if (Test-Command scoop) {
        scoop install python vsbuildtools 2>$null || true
    }
    
    # Playwright system deps (will be installed by browser installer)
    Write-Warn "For browser automation, run 'aether-browser-install --system-deps' after install (requires admin)"
}

# ─── Main ───
Write-Header "═══════════════════════════════════════════"
Write-Header "   AETHER Windows Installer"
Write-Header "═══════════════════════════════════════════"

$python = Get-Python
$PY_CMD = $python.Command
$PY_VERSION = $python.Version

$INSTALL_DIR = $Prefix
$VENV_DIR = Join-Path $INSTALL_DIR "venv"
$REPO_URL = "https://github.com/agastyatomar/AETHER.git"

# Force reinstall
if ($Force -and (Test-Path $INSTALL_DIR)) {
    Write-Log "Removing existing installation..."
    Remove-Item $INSTALL_DIR -Recurse -Force -ErrorAction SilentlyContinue
}

# Clone or update
if (Test-Path (Join-Path $INSTALL_DIR ".git")) {
    Write-Log "Updating existing repository..."
    Set-Location $INSTALL_DIR
    git fetch origin
    git checkout $Branch
    git pull origin $Branch
} else {
    Write-Log "Cloning repository..."
    git clone --branch $Branch --depth 1 $REPO_URL $INSTALL_DIR
}

Install-SystemDeps

# Create venv
if (-not $NoVenv) {
    Write-Log "Creating virtual environment at $VENV_DIR..."
    & $PY_CMD -m venv $VENV_DIR
    & "$VENV_DIR\Scripts\pip.exe" install --upgrade pip setuptools wheel
    Write-Ok "Virtual environment created"
    $PIP = "$VENV_DIR\Scripts\pip.exe"
    $PYTHON = "$VENV_DIR\Scripts\python.exe"
} else {
    $PIP = "pip"
    $PYTHON = $PY_CMD
}

# Install package
Write-Log "Installing AETHER package..."
& $PIP install -e $INSTALL_DIR
if ($Dev) {
    Write-Log "Installing development dependencies..."
    & $PIP install -r (Join-Path $INSTALL_DIR "requirements-dev.txt")
}
Write-Ok "Package installed"

# Install browser
if ($Browser) {
    Write-Log "Installing browser automation runtime..."
    & $PYTHON -m aether.society.browser.install @($SystemDeps ? "--system-deps" : "")
    Write-Ok "Browser automation installed"
}

# Create symlinks (add to PATH)
Write-Log "Setting up PATH..."
$BIN_SOURCE = if (-not $NoVenv) { "$VENV_DIR\Scripts" } else { Split-Path (Get-Command $PY_CMD).Source }
$BIN_DIR_PATH = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($BinDir)

if (-not (Test-Path $BIN_DIR_PATH)) {
    New-Item -ItemType Directory -Path $BIN_DIR_PATH -Force | Out-Null
}

foreach ($cmd in @("aether.exe", "aether-browser-install.exe", "aether-society.exe")) {
    $src = Join-Path $BIN_SOURCE $cmd
    $dst = Join-Path $BIN_DIR_PATH $cmd
    if (Test-Path $src) {
        Copy-Item $src $dst -Force
        Write-Ok "Copied $cmd to $BinDir"
    }
}

# Add to user PATH if not present
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$BIN_DIR_PATH*") {
    Write-Warn "Add to your PATH (run in new PowerShell):"
    Write-Host "  \$env:PATH += ';$BIN_DIR_PATH'" -ForegroundColor $CYAN
    Write-Host "  [Environment]::SetEnvironmentVariable('Path', \$env:PATH, 'User')" -ForegroundColor $CYAN
}

# Verify
Write-Log "Verifying installation..."
try {
    & $PYTHON -c "import aether; print(f'AETHER {aether.__version__}')" | Out-Null
    Write-Ok "Core import successful"
} catch {
    Write-Err "Core import failed: $_"
    exit 1
}

# Summary
Write-Header "═══════════════════════════════════════════"
Write-Header "   AETHER Installation Complete!"
Write-Header "═══════════════════════════════════════════"
Write-Host ""
Write-Host "  Install directory: $INSTALL_DIR" -ForegroundColor $WHITE
Write-Host "  Virtual env:       $VENV_DIR" -ForegroundColor $WHITE
Write-Host "  Bin directory:     $BIN_DIR_PATH" -ForegroundColor $WHITE
Write-Host ""
Write-Host "Next steps:" -ForegroundColor $CYAN
Write-Host "  1. Restart PowerShell or run: \$env:PATH += ';$BIN_DIR_PATH'" -ForegroundColor $WHITE
Write-Host "  2. Activate venv: & '$VENV_DIR\Scripts\Activate.ps1'" -ForegroundColor $WHITE
Write-Host "  3. Run AETHER: aether --help" -ForegroundColor $WHITE
if ($Browser) {
    Write-Host "  Browser automation: aether-browser-install --probe" -ForegroundColor $WHITE
}
Write-Host ""
Write-Host "Documentation: https://github.com/agastyatomar/AETHER/wiki" -ForegroundColor $CYAN
Write-Host ""