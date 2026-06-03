# Marathon CLI - Quick Start

## One-Line Installation

### Windows (PowerShell/Windows Terminal)
```powershell
irm https://raw.githubusercontent.com/parkerbailey/marathon-cli/main/install-simple.ps1 | iex
```

### Linux/macOS
```bash
curl -sSL https://raw.githubusercontent.com/parkerbailey/marathon-cli/main/install.sh | bash
```

### Any Platform (Python)
```bash
pip install git+https://github.com/parkerbailey/marathon-cli.git
```

---

## Quick Commands

```bash
# Start live monitor
marathon-cli

# Show status once
marathon-cli status

# JSON output
marathon-cli status --json

# Show help
marathon-cli --help
```

---

## Requirements

- Python 3.8+
- Internet connection
- Terminal with ANSI color support (Windows Terminal recommended for Windows)

---

## Links

- **Installation Guide**: [INSTALL.md](INSTALL.md)
- **Windows Guide**: [WINDOWS.md](WINDOWS.md)
- **Full README**: [README.md](README.md)
- **GitHub**: https://github.com/parkerbailey/marathon-cli
