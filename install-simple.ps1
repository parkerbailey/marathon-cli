#!/usr/bin/env pwsh
# Marathon CLI - Simple One-Line Installer
# Usage: irm https://raw.githubusercontent.com/yourusername/marathon-cli/main/install-simple.ps1 | iex

Write-Host "🎮 Installing Marathon CLI..." -ForegroundColor Cyan
python -m pip install --user git+https://github.com/yourusername/marathon-cli.git
Write-Host "✓ Done! Run 'marathon-cli' to start." -ForegroundColor Green
Write-Host "If command not found, restart your terminal or add Python Scripts to PATH" -ForegroundColor Yellow
