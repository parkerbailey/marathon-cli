# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Marathon CLI is a terminal-based monitoring tool for Bungie's Marathon game on Steam. It provides real-time player counts from the Steam API and server status from marathonstatus.com, with an animated cyberpunk aesthetic using Marathon Graphic Realism color palette (lime, cyan, orange, slate).

The application is a single-file Python CLI built with Click, featuring:
- Live monitoring with auto-refresh (default 60s intervals)
- In-place TUI updates using ANSI escape sequences
- Animated ASCII art banner, loading bars, and status transitions
- Vertical bar chart showing player count history (last 16 data points)
- Background data fetching thread with foreground display updates
- Graceful Ctrl+C handling

## Development Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install requests click pyfiglet
```

## Running the Application

```bash
# Default: live monitor with 60s refresh
python main.py

# Specific commands
python main.py players      # Single snapshot of player count
python main.py status       # Full system status check
python main.py status --json  # JSON output
python main.py monitor -i 30  # Live monitor with 30s interval
```

## Architecture

### Threading Model
- **Main thread**: Handles initial setup, MOTD animation, and periodic display updates (1s tick for "Last Sync" counter)
- **Background thread** (`data_fetcher`): Fetches data from APIs every N seconds (configurable interval)
- **Synchronization**: `data_lock` protects shared data (`current_data`, `history_points`), `display_lock` protects stdout writes

### Display Rendering
- Uses ANSI cursor positioning (`\033[s`, `\033[u`, `\033[{N}A`) to update stats box in-place without clearing screen
- `STATS_BOX_HEIGHT = 7` constant defines the stats box vertical size for cursor navigation
- `render_stats_box()` redraws the entire box with current data + player count graph
- Terminal width is dynamically detected; layout is split 50/50 between stats box and graph

### Data Flow
1. Background thread fetches Steam API + marathonstatus.com API
2. Results stored in `current_data` dict (protected by `data_lock`)
3. Player count appended to `history_points` (max 16 entries, FIFO)
4. Main loop calls `update_display()` every 1s to redraw stats box with fresh data
5. Status changes trigger ripple + blink animations

### Animation System
- `animate_banner()`: Prints ASCII art line-by-line with glitch effects
- `animate_loading_bar()`: Progress bar with self-cleanup
- `animate_status_ripple()`: Wave effect across status line on state change
- `blink_status_text()`: Flashes status line 3 times
- Animations check `running` global for early exit on Ctrl+C

### API Integrations
- **Steam API**: `https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/` with `appid=3065800` (Marathon's app ID)
- **MarathonStatus API**: `https://marathonstatus.com/index.php?action=status` with cache-busting timestamp param
- Both have 10s timeouts; failures are handled gracefully with error display

## Key Constants

- `MARATHON_APP_ID = 3065800`: Steam app ID for Marathon
- `MAX_HISTORY_POINTS = 16`: Number of historical data points retained for chart
- `STATS_BOX_HEIGHT = 7`: Vertical lines occupied by stats box (used for cursor math)
- Color palette defined in `COLORS` dict (lime/cyan/orange/slate with ANSI RGB codes)

## Testing Strategy

Manual testing in a terminal emulator:
- Run default monitor mode, verify animations play correctly
- Test Ctrl+C interruption (should print graceful exit message)
- Test single-shot commands (`players`, `status`, `status --json`)
- Verify layout adapts to terminal width changes
- Test with API failures (disconnect network to trigger error states)
- Check thread cleanup on exit (no orphaned threads)

## Color Palette Reference

```python
COLORS = {
    'lime': '\033[38;2;194;254;11m',        # Bright accent
    'cyan': '\033[38;2;1;255;255m',         # Primary UI borders/text
    'orange': '\033[38;2;255;13;26m',       # Errors/warnings/outages
    'slate': '\033[38;2;41;50;79m',         # Muted/secondary text
    'bright_green': '\033[38;2;89;180;29m', # Success states
}
```

## Gotchas

- ANSI escape sequences break `len()` — always use `visible_len()` helper for padding calculations
- Cursor save/restore (`\033[s`/`\033[u`) must be paired; nested calls will corrupt positioning
- Display updates must hold `display_lock` to prevent race conditions in multi-threaded stdout writes
- Status change detection compares `previous_status` — first fetch initializes this to prevent false animation trigger
- Graph rendering normalizes to data range (min/max) — all-zero data results in flat line at bottom
