#!/usr/bin/env bash
# Marathon CLI Installer for Linux/macOS
# Usage: curl -sSL https://raw.githubusercontent.com/parkerbailey/marathon-cli/main/install.sh | bash

set -e

echo "🎮 Marathon CLI Installer"
echo "========================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python found: $PYTHON_VERSION"

# Check Python version
MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo "❌ Python 3.8+ required. Found: $PYTHON_VERSION"
    exit 1
fi

# Check if pipx is available
if command -v pipx &> /dev/null; then
    echo ""
    echo "Installing marathon-cli with pipx..."
    pipx install git+https://github.com/parkerbailey/marathon-cli.git
elif command -v apt &> /dev/null; then
    # Debian/Ubuntu system - recommend pipx
    echo ""
    echo "Installing pipx first (recommended for CLI tools)..."
    sudo apt install -y pipx
    pipx ensurepath
    echo ""
    echo "Installing marathon-cli with pipx..."
    pipx install git+https://github.com/parkerbailey/marathon-cli.git
else
    # Try pip with --user flag
    echo ""
    echo "Installing marathon-cli with pip..."
    python3 -m pip install --user git+https://github.com/parkerbailey/marathon-cli.git
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "Run 'marathon-cli' to start monitoring."
echo "Run 'marathon-cli --help' for more options."
echo ""

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "⚠️  Note: ~/.local/bin is not in your PATH"
    echo "Add this to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi
