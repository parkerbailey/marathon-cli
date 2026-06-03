# marathon_cli/main.py
import requests
import click
import sys
import time
import random
from datetime import datetime
from pyfiglet import Figlet
import re
import signal
import threading

MARATHON_APP_ID = 3065800
MARATHON_STATUS_API = "https://marathonstatus.com/index.php?action=status"

# Marathon Graphic Realism color palette
COLORS = {
    'lime': '\033[38;2;194;254;11m',
    'cyan': '\033[38;2;1;255;255m',
    'orange': '\033[38;2;255;13;26m',
    'slate': '\033[38;2;41;50;79m',
    'bright_green': '\033[38;2;89;180;29m',
    'reset': '\033[0m',
    'bold': '\033[1m',
    'dim': '\033[2m',
}

# Global state
running = True
last_fetch_time = None
current_data = {"success": False, "count": 0, "marathon_status": "unknown", "reports_10m": 0, "platforms": {}}
history_points = []
MAX_HISTORY_POINTS = 16
STATS_BOX_HEIGHT = 7  # top border + separator + 4 rows + bottom border

data_lock = threading.Lock()
display_lock = threading.Lock()

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    global running
    running = False
    c = COLORS
    sys.stdout.write(f"\n{c['cyan']}>> Connection terminated by user{c['reset']}\n")
    sys.stdout.write(f"{c['slate']}{'='*60}{c['reset']}\n")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_current_players(app_id: int) -> dict:
    url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
    try:
        resp = requests.get(url, params={"appid": app_id}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data["response"].get("result") == 1:
            return {"success": True, "count": data["response"]["player_count"]}
        return {"success": False, "error": "Steam returned a non-success result"}
    except requests.RequestException as e:
        return {"success": False, "error": str(e)}

def visible_len(s: str) -> int:
    ansi_escape = re.compile(r'\033\[[0-9;]*m')
    return len(ansi_escape.sub('', s))

def rpad(text: str, width: int) -> str:
    padding = width - visible_len(text)
    return text + ' ' * max(padding, 0)

def clear_screen():
    """Clears the terminal screen and moves cursor to top-left."""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def update_refresh_indicator(message: str):
    """Write a temporary refresh status on the reserved footer line."""
    with display_lock:
        sys.stdout.write("\033[s")
        sys.stdout.write("\033[2K")
        sys.stdout.write(message)
        sys.stdout.write("\033[u")
        sys.stdout.flush()

def show_refresh_indicator():
    update_refresh_indicator(f"{COLORS['cyan']}  ⟳ Refreshing data...{COLORS['reset']}")

def clear_refresh_indicator():
    update_refresh_indicator("")


def render_vertical_bar_chart(values, height=5, width=8):
    """Render a vertical bar chart to fill the box height."""
    points = list(values[-width:])
    if not points:
        points = [0] * width
    clean_values = [v for v in points if v is not None]
    if not clean_values:
        clean_values = [0]
    min_v = min(clean_values)
    max_v = max(clean_values)
    span = max_v - min_v or 1
    heights = []
    for value in points:
        if value is None:
            heights.append(0)
        else:
            heights.append(int((value - min_v) / span * (height - 1)) + 1)
    rows = []
    for row in range(height, 0, -1):
        rows.append(''.join('█' if h >= row else ' ' for h in heights))
    return rows


def get_marathon_server_status() -> dict:
    """Fetch Marathon server status from MarathonStatus.com."""
    try:
        resp = requests.get(MARATHON_STATUS_API, params={"_": int(time.time() * 1000)}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("ok"):
            return {
                "success": True,
                "status": data.get("status", "unknown"),
                "reports_10m": data.get("reports_10m", 0),
                "platforms": data.get("platforms", {}),
                "bungie_ok": data.get("bungie_ok", False),
                "bungie_available": data.get("bungie_available", False),
            }
        return {"success": False, "status": "unknown", "error": data.get("error", "status request failed")}
    except requests.RequestException as e:
        return {"success": False, "status": "unknown", "error": str(e)}


def format_marathon_status_line(status: str, reports: int) -> tuple[str, str]:
    status_key = str(status or "unknown").lower()
    if status_key == "outage":
        return ("OUTAGE", COLORS['orange'])
    if status_key == "degraded":
        return ("DEGRADED", COLORS['orange'])
    if status_key in ("online", "operational", "all systems operational"):
        return ("ONLINE", COLORS['bright_green'])
    if status_key == "maintenance":
        return ("MAINTENANCE", COLORS['orange'])
    if status_key == "checking":
        return ("CHECKING", COLORS['cyan'])
    return (status_key.upper(), COLORS['cyan'])


def append_history_point(value):
    """Append a new history point, keeping the history bounded."""
    with data_lock:
        history_points.append(value)
        if len(history_points) > MAX_HISTORY_POINTS:
            history_points.pop(0)


def render_sparkline(values, width=MAX_HISTORY_POINTS):
    """Render a compact sparkline from recent values."""
    spark_chars = '▁▂▃▄▅▆▇█'
    points = list(values[-width:])
    if not points:
        return ' ' * width
    clean = [v for v in points if v is not None]
    if not clean:
        return '·' * len(points)
    min_v = min(clean)
    max_v = max(clean)
    span = max_v - min_v or 1
    rendered = []
    for value in points:
        if value is None:
            rendered.append('·')
        else:
            idx = int((value - min_v) / span * (len(spark_chars) - 1))
            rendered.append(spark_chars[idx])
    return ''.join(rendered).rjust(width)

def glitch_effect(text: str, color_key: str = 'cyan') -> str:
    """Adds a random glitch effect to a line."""
    if random.random() > 0.8:
        glitch_chars = ['█', '▓', '░', '▒', '✖', '⚠']
        idx = random.randint(0, len(text) - 1)
        if text[idx] != ' ':
            text = text[:idx] + random.choice(glitch_chars) + text[idx+1:]
        return f"{COLORS['orange']}{text}{COLORS['reset']}"
    return f"{COLORS[color_key]}{text}{COLORS['reset']}"

def animate_banner(text: str, font: str = 'slant', color_key: str = 'cyan', speed: float = 0.05):
    """Animates the banner line by line with a glitch effect."""
    try:
        f = Figlet(font=font, justify='center')
        ascii_art = f.renderText(text)
    except Exception:
        f = Figlet()
        ascii_art = f.renderText(text)

    lines = [line for line in ascii_art.split('\n') if line.strip()]
    
    clear_screen()
    
    for i, line in enumerate(lines):
        styled_line = glitch_effect(line, color_key)
        sys.stdout.write(styled_line + "\n")
        sys.stdout.flush()
        time.sleep(speed)
        
        if random.random() > 0.9:
            time.sleep(0.1)

def animate_loading_bar(duration: float = 1.0, width: int = 40):
    """Animates a chunky loading bar and clears it after completion."""
    total_steps = int(duration / 0.05)
    max_line_length = width + 5
    
    for i in range(total_steps + 1):
        progress = i / total_steps
        filled = int(width * progress)
        remaining = width - filled
        
        bar = f"{COLORS['bright_green']}" + "█" * filled + f"{COLORS['slate']}" + "░" * remaining + f"{COLORS['reset']}"
        sys.stdout.write(f"\r{bar} {int(progress * 100)}%")
        sys.stdout.flush()
        time.sleep(0.05)
    
    sys.stdout.write("\r" + " " * max_line_length + "\r")
    sys.stdout.flush()

def print_motd(server_line=None):
    """Prints the animated MOTD."""
    animate_banner("MARATHON-CLI", font='slant', color_key='cyan', speed=0.08)
    
    time.sleep(0.2)
    
    sys.stdout.write(f"{COLORS['lime']}  >> Welcome RNR{COLORS['reset']}\n")
    sys.stdout.flush()
    time.sleep(0.3)
    
    sys.stdout.write("\n")
    animate_loading_bar(duration=1.5)
    
    c = COLORS
    sys.stdout.write(f"{c['slate']}{'='*60}{c['reset']}\n")
    if server_line is None:
        sys.stdout.write(f"{c['cyan']}  MARATHON STATUS{c['reset']}  {c['bold']}CHECKING{c['reset']}\n")
    else:
        sys.stdout.write(f"{server_line}\n")
    sys.stdout.write(f"{c['slate']}{'='*60}{c['reset']}\n\n")
    sys.stdout.flush()

def render_stats_box(result: dict, last_update: datetime, history=None):
    """Render the stats box with current data."""
    if history is None:
        history = []
    c = COLORS
    INNER_WIDTH = 50
    GRAPH_WIDTH = 8

    title_line = f"{c['bold']}RUNNER STATS{c['reset']}"
    elapsed = (datetime.now() - last_update).seconds
    sync_line = f"{c['slate']}Last Sync:{c['reset']} {c['cyan']}{elapsed}s ago{c['reset']}"

    if result.get("success"):
        active_line = f"{c['lime']}{c['bold']}Active:{c['reset']} {c['bright_green']}{result.get('count', 0):,}{c['reset']}"
        appid_line = f"{c['slate']}App ID:{c['reset']} {c['cyan']}{MARATHON_APP_ID}{c['reset']}"
        left_rows = [title_line, active_line, appid_line, sync_line]
    else:
        error_line = f"{c['orange']}⚠ ERROR: {result.get('error', 'unknown')}{c['reset']}"
        appid_line = f"{c['slate']}App ID:{c['reset']} {c['cyan']}{MARATHON_APP_ID}{c['reset']}"
        left_rows = [title_line, error_line, appid_line, sync_line]

    content_width = INNER_WIDTH - GRAPH_WIDTH - 2
    graph_rows = render_vertical_bar_chart(history, height=len(left_rows), width=GRAPH_WIDTH)

    sys.stdout.write(f"{c['cyan']}┌{'─'*INNER_WIDTH}┐{c['reset']}\n")
    for i, row_text in enumerate(left_rows):
        graph_text = (graph_rows[i] if i < len(graph_rows) else ' ' * GRAPH_WIDTH).ljust(GRAPH_WIDTH)
        sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + row_text, content_width)}  {graph_text}{c['cyan']}│{c['reset']}\n")
        if i == 0:
            sys.stdout.write(f"{c['cyan']}├{'─'*INNER_WIDTH}┤{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}└{'─'*INNER_WIDTH}┘{c['reset']}\n")
    sys.stdout.flush()

def update_display():
    """Update only the stats box without clearing the screen."""
    global current_data, last_fetch_time
    
    with data_lock:
        result = current_data.copy()
        last_update = last_fetch_time
        history_snapshot = history_points.copy()
    
    with display_lock:
        sys.stdout.write("\033[s")
        sys.stdout.write(f"\033[{STATS_BOX_HEIGHT + 1}A")
        render_stats_box(result, last_update, history_snapshot)
        sys.stdout.write("\033[u")
        sys.stdout.flush()

def data_fetcher(update_interval: int = 60):
    """Background thread that fetches data periodically."""
    global current_data, last_fetch_time, running
    
    while running:
        show_refresh_indicator()
        player_result = get_current_players(MARATHON_APP_ID)
        status_result = get_marathon_server_status()
        clear_refresh_indicator()
        
        combined_result = {
            "success": player_result.get("success", False),
            "count": player_result.get("count", 0),
            "error": player_result.get("error"),
            "marathon_status": status_result.get("status", "unknown"),
            "reports_10m": status_result.get("reports_10m", 0),
            "platforms": status_result.get("platforms", {}),
            "status_error": status_result.get("error"),
        }
        
        with data_lock:
            current_data = combined_result
            last_fetch_time = datetime.now()
        append_history_point(combined_result['count'] if combined_result.get('success') else None)
        
        time.sleep(update_interval)

def live_monitor(update_interval: int = 60):
    """Continuously monitor and update player count."""
    global running, last_fetch_time, current_data
    
    c = COLORS
    
    # Initial fetch
    player_result = get_current_players(MARATHON_APP_ID)
    status_result = get_marathon_server_status()
    status_label, status_color = format_marathon_status_line(status_result.get('status', 'unknown'), status_result.get('reports_10m', 0))
    server_line = f"{COLORS['slate']}SERVER STATUS:{COLORS['reset']} {status_color}{status_label}{COLORS['reset']}"
    if status_result.get('reports_10m', 0):
        server_line = f"{server_line} {COLORS['slate']}({status_result['reports_10m']} rpt){COLORS['reset']}"
    
    print_motd(server_line)
    
    # Start data fetcher in background thread
    fetch_thread = threading.Thread(target=data_fetcher, args=(update_interval,), daemon=True)
    fetch_thread.start()
    
    last_fetch_time = datetime.now()
    combined_result = {
        "success": player_result.get("success", False),
        "count": player_result.get("count", 0),
        "error": player_result.get("error"),
        "marathon_status": status_result.get("status", "unknown"),
        "reports_10m": status_result.get("reports_10m", 0),
        "platforms": status_result.get("platforms", {}),
        "status_error": status_result.get("error"),
    }
    with data_lock:
        current_data = combined_result
    append_history_point(combined_result['count'] if combined_result.get('success') else None)
    
    render_stats_box(combined_result, last_fetch_time, history_points.copy())
    
    sys.stdout.write(f"{c['dim']}  Press Ctrl+C to exit{c['reset']}\n")
    sys.stdout.flush()
    
    # Live update loop - update display every second
    while running:
        time.sleep(1)
        
        if not running:
            break
        
        # Update the display in place (ticks up the sync counter)
        update_display()

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Marathon CLI — Stats and info for Bungie's Marathon."""
    if ctx.invoked_subcommand is None:
        live_monitor(update_interval=60)

@cli.command()
def players():
    """Show current player count on Steam (single snapshot)."""
    print_motd()
    result = get_current_players(MARATHON_APP_ID)
    last_update = datetime.now()
    render_stats_box(result, last_update)

@cli.command()
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def status(output_json):
    """Full system status check (single snapshot)."""
    c = COLORS
    
    if output_json:
        player_result = get_current_players(MARATHON_APP_ID)
        status_result = get_marathon_server_status()
        click.echo(f'{{"success": {str(player_result["success"]).lower()}, "count": {player_result.get("count", "null")}, "marathon_status": "{status_result.get("status", "unknown")}"}}')
        return
    
    print_motd()
    INNER_WIDTH = 50
    
    title_line = f"{c['bold']}SYSTEM STATUS{c['reset']}"
    
    player_result = get_current_players(MARATHON_APP_ID)
    status_result = get_marathon_server_status()
    status_label, status_color = format_marathon_status_line(status_result.get('status', 'unknown'), status_result.get('reports_10m', 0))
    marathon_line = f"{c['lime']}●{c['reset']} Marathon: {status_color}{status_label}{c['reset']}"
    if status_result.get('reports_10m', 0):
        marathon_line = f"{marathon_line} {c['slate']}({status_result['reports_10m']} rpt){c['reset']}"

    if player_result["success"]:
        steam_line = f"{c['lime']}●{c['reset']} Steam API: {c['bright_green']}OPERATIONAL{c['reset']}"
        runners_line = f"{c['lime']}●{c['reset']} Runners: {c['cyan']}{player_result['count']:,}{c['reset']}"
    else:
        steam_line = f"{c['orange']}●{c['reset']} Steam API: {c['orange']}ERROR{c['reset']}"
        runners_line = f"{c['orange']}●{c['reset']} Runners: N/A{c['reset']}"
    
    sys.stdout.write(f"{c['cyan']}┌{'─'*INNER_WIDTH}┐{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + title_line, INNER_WIDTH)}{c['cyan']}│{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}├{'─'*INNER_WIDTH}┤{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + steam_line, INNER_WIDTH)}{c['cyan']}│{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + marathon_line, INNER_WIDTH)}{c['cyan']}│{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + runners_line, INNER_WIDTH)}{c['cyan']}│{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}└{'─'*INNER_WIDTH}┘{c['reset']}\n\n")
    sys.stdout.flush()

@cli.command()
@click.option('--interval', '-i', default=60, help='Data refresh interval in seconds (default: 60)')
def monitor(interval):
    """Live monitor mode with continuous updates."""
    live_monitor(update_interval=interval)

if __name__ == "__main__":
    cli()