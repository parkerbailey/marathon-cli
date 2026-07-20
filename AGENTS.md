# Agent Instructions — marathon-cli

Single-file Python CLI that monitors Bungie's Marathon player counts (Steam API) and server status (marathonstatus.com). Cyberpunk TUI with ANSI art, charts, and animations.

## Structure

- Entry point: `marathon_cli/__init__.py` (entire application lives here — 575 lines)
- Package config: `pyproject.toml` (setuptools, entry point `marathon-cli = "marathon_cli:cli"`)
- Framework: Click group with subcommands

## Setup & Running

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .          # installs click, requests, pyfiglet from pyproject.toml
```

Commands (uses installed CLI entry point, NOT `python main.py`):

```bash
marathon-cli              # live monitor, 60s refresh (default)
marathon-cli players      # single snapshot of Steam player count
marathon-cli status       # full system status box
marathon-cli status --json  # JSON output
marathon-cli monitor -i 30  # live monitor with custom interval
```

For dev without install: `python -m marathon_cli` works too.

## Architecture

### Threading
- **Main thread**: MOTD animation, then 1-second display-update loop (`update_display`)
- **Background daemon thread** (`data_fetcher`): fetches both APIs every N seconds (configurable)
- `data_lock`: protects `current_data`, `history_points`
- `display_lock`: protects all stdout writes

### Display
- ANSI cursor save/restore (`\033[s` / `\033[u`) for in-place stats-box redraw
- `STATS_BOX_HEIGHT = 7` — used for cursor math when positioning over the box
- Layout: left half is a boxed stats panel, right half is a vertical bar chart of history
- Terminal width dynamically detected; split ~50/50 between stats and graph

### Data flow
1. `data_fetcher` polls Steam API + marathonstatus.com API on interval
2. Results stored in `current_data` (under `data_lock`)
3. Player count appended to `history_points` (max 100, FIFO)
4. Main loop redraws stats box every 1s via `update_display()`

### Chart rendering
- `render_vertical_bar_chart()`: status-colored bars (`▇`) with smart scaling — expands range for small variations so differences remain visible
- All-equal data renders in the middle; all-zero/empty renders flat at bottom

## Key constants (in source, not all obvious from name)

| Constant | Value | Purpose |
|---|---|---|
| `MARATHON_APP_ID` | `3065800` | Steam app ID |
| `MAX_HISTORY_POINTS` | `100` | History buffer (was 16, bumped for wider terminals) |
| `STATS_BOX_HEIGHT` | `7` | Box row count for cursor navigation math |

## Gotchas

- **ANSI breaks `len()`** — use `visible_len()` helper for all string width calculations
- **Cursor save/restore must be paired** — unbalanced `\033[s`/`\033[u]` corrupts positioning
- **All stdout goes through `display_lock`** in the monitor loop — race-free terminal writes
- **`is_refreshing` flag**: managed behind `data_lock`, drives a refresh spinner icon in the stats box title
- **`running` global**: checked by animation loops and main thread for early exit on Ctrl+C
- **Signal handler** (`signal_handler`) sets `running = False` and calls `sys.exit(0)` — background daemon threads terminate automatically

## APIs

| API | URL | Timeout |
|---|---|---|
| Steam player count | `api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=3065800` | 10s |
| Marathon status | `marathonstatus.com/index.php?action=status` (+ cache-bust `_` param) | 10s |

Failures handled gracefully — stats box shows ERROR state, monitor keeps running.

## COLORS dict

Full palette in source includes: `lime`, `cyan`, `orange`, `yellow`, `slate`, `bright_green`, plus formatting codes (`reset`, `bold`, `dim`). Status coloring maps: outage→orange, degraded→yellow, online/operational→bright_green, maintenance→orange, unknown/checking→cyan.
