#!/usr/bin/env pwsh
# Marathon CLI Installer for Windows
# Usage: irm https://raw.githubusercontent.com/yourusername/marathon-cli/main/install.ps1 | iex

$ErrorActionPreference = "Stop"

Write-Host "🎮 Marathon CLI Installer" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+ from python.org" -ForegroundColor Red
    exit 1
}

# Check Python version
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $major = [int]$Matches[1]
    $minor = [int]$Matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Host "✗ Python 3.8+ required. Found: $pythonVersion" -ForegroundColor Red
        exit 1
    }
}

# Ask user for installation method
Write-Host ""
Write-Host "Select installation method:" -ForegroundColor Yellow
Write-Host "1. pipx (recommended - isolated installation)"
Write-Host "2. pip --user (install for current user)"
Write-Host "3. pip (global installation - may require admin)"
Write-Host ""
$choice = Read-Host "Enter choice (1-3)"

switch ($choice) {
    "1" {
        # Install with pipx
        Write-Host ""
        Write-Host "Installing with pipx..." -ForegroundColor Cyan

        # Check if pipx is installed
        try {
            & pipx --version | Out-Null
            Write-Host "✓ pipx found" -ForegroundColor Green
        } catch {
            Write-Host "Installing pipx..." -ForegroundColor Yellow
            & python -m pip install --user pipx
            & python -m pipx ensurepath
            Write-Host "✓ pipx installed. You may need to restart your terminal." -ForegroundColor Green
        }

        Write-Host "Installing marathon-cli..." -ForegroundColor Cyan
        & pipx install git+https://github.com/yourusername/marathon-cli.git
    }
    "2" {
        # Install with pip --user
        Write-Host ""
        Write-Host "Installing with pip --user..." -ForegroundColor Cyan
        & python -m pip install --user git+https://github.com/yourusername/marathon-cli.git
    }
    "3" {
        # Install with pip (global)
        Write-Host ""
        Write-Host "Installing globally..." -ForegroundColor Cyan
        & python -m pip install git+https://github.com/yourusername/marathon-cli.git
    }
    default {
        Write-Host "Invalid choice. Exiting." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✓ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Run 'marathon-cli' to start monitoring." -ForegroundColor Cyan
Write-Host "Run 'marathon-cli --help' for more options." -ForegroundColor Cyan
Write-Host ""
Write-Host "Note: If 'marathon-cli' is not found, you may need to:" -ForegroundColor Yellow
Write-Host "  1. Restart your terminal" -ForegroundColor Yellow
Write-Host "  2. Add Python Scripts to PATH" -ForegroundColor Yellow
Write-Host ""
