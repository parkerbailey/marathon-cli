# Marathon CLI

A terminal-based monitoring tool for Bungie's Marathon game on Steam. Features real-time player counts, server status monitoring, and an animated cyberpunk aesthetic using the Marathon Graphic Realism color palette.

![Marathon CLI Screenshot](https://via.placeholder.com/800x400?text=Marathon+CLI+Screenshot)

## Features

- 🎮 **Real-time Steam player count** tracking
- 🌐 **Server status monitoring** from marathonstatus.com
- 📊 **Status-colored history graph** showing player counts over time
- 🎨 **Cyberpunk aesthetic** with Marathon-themed colors
- ⚡ **Live updates** with configurable refresh intervals
- 🔄 **In-place TUI updates** using ANSI escape sequences

## Installation

### Quick Install (One-Liner)

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/yourusername/marathon-cli/main/install-simple.ps1 | iex
```

**Linux/macOS:**
```bash
curl -sSL https://raw.githubusercontent.com/yourusername/marathon-cli/main/install.sh | bash
```

### From PyPI (once published)

```bash
pip install marathon-cli
```

### From GitHub

```bash
pip install git+https://github.com/yourusername/marathon-cli.git
```

### From Source

```bash
git clone https://github.com/yourusername/marathon-cli.git
cd marathon-cli
pip install -e .
```

## Usage

### Default Monitor Mode

Run the live monitor with 60-second refresh:

```bash
marathon-cli
```

### Commands

**Single snapshot of player count:**
```bash
marathon-cli players
```

**Full system status check:**
```bash
marathon-cli status
```

**JSON output:**
```bash
marathon-cli status --json
```

**Live monitor with custom interval:**
```bash
marathon-cli monitor --interval 30  # 30 second refresh
```

## Display

The application shows:

```
════════════════════════════════════
SERVER STATUS: ONLINE
════════════════════════════════════

┌─────────────────────────────┐  Player Count History
│  RUNNER STATS           ⟳   │  ·················
├─────────────────────────────┤  ·················
│  Active: 4,401              │  ············▇▇▇▇▇
│  App ID: 3065800            │  ·········▇▇▇▇▇▇▇▇
│  Last Sync: 0s ago          │  ······▇▇▇▇▇▇▇▇▇▇▇
└─────────────────────────────┘  ···▇▇▇▇▇▇▇▇▇▇▇▇▇▇
```

### Status Colors

The graph bars are colored based on server status when data was recorded:
- 🟢 **Green** - Server ONLINE
- 🟡 **Yellow** - Server DEGRADED
- 🔴 **Red/Orange** - Server OUTAGE
- 🟠 **Orange** - Server MAINTENANCE

## Requirements

- Python 3.8+
- Terminal with ANSI color support
- Internet connection

## Dependencies

- `requests` - API calls
- `click` - CLI framework
- `pyfiglet` - ASCII art banner

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/marathon-cli.git
cd marathon-cli

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Run
marathon-cli
```

## License

MIT License - see LICENSE file for details

## Credits

- Marathon™ is a trademark of Bungie, Inc.
- Uses Steam Web API for player count data
- Uses MarathonStatus.com for server status data

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
