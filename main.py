# marathon_cli/main.py
import requests
import click
import sys
import time
import random
from datetime import datetime
from pyfiglet import Figlet
import re

MARATHON_APP_ID = 3065800

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

def glitch_effect(text: str, color_key: str = 'cyan') -> str:
    """Adds a random glitch effect to a line."""
    if random.random() > 0.8: # 20% chance to glitch
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
    """Animates a chunky loading bar."""
    sys.stdout.write(f"\n{COLORS['cyan']}INITIALIZING SYSTEM...{COLORS['reset']}\n")
    
    blocks = ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']
    total_steps = int(duration / 0.05)
    
    for i in range(total_steps + 1):
        progress = i / total_steps
        filled = int(width * progress)
        remaining = width - filled
        
        bar = f"{COLORS['bright_green']}" + "█" * filled + f"{COLORS['slate']}" + "░" * remaining + f"{COLORS['reset']}"
        
        sys.stdout.write(f"\r{bar} {int(progress * 100)}%")
        sys.stdout.flush()
        time.sleep(0.05)
    
    sys.stdout.write("\n")

def print_motd():
    """Prints the animated MOTD."""
    animate_banner("MARATHON-CLI", font='slant', color_key='cyan', speed=0.08)
    
    time.sleep(0.2)
    
    sys.stdout.write(f"{COLORS['lime']}  >> Welcome RNR{COLORS['reset']}\n")
    sys.stdout.flush()
    time.sleep(0.3)
    
    animate_loading_bar(duration=1.5)
    
    c = COLORS
    sys.stdout.write(f"{c['slate']}{'='*60}{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}  SYSTEM STATUS{c['reset']}  {c['bold']}ONLINE{c['reset']}\n")
    sys.stdout.write(f"{c['slate']}{'='*60}{c['reset']}\n\n")
    sys.stdout.flush()

def print_player_stats(result: dict):
    """Display player count with Marathon styling."""
    c = COLORS
    INNER_WIDTH = 50
    
    if result["success"]:
        count = result["count"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        title_line = f"{c['bold']}CURRENT RUNNER COUNT{c['reset']}"
        active_line = f"{c['lime']}{c['bold']}Active:{c['reset']} {c['bright_green']}{count:,}{c['reset']}"
        appid_line = f"{c['slate']}App ID:{c['reset']} {c['cyan']}{MARATHON_APP_ID}{c['reset']}"
        sync_line = f"{c['slate']}Synced:{c['reset']} {c['cyan']}{timestamp}{c['reset']}"
        
        sys.stdout.write(f"{c['cyan']}┌{'─'*INNER_WIDTH}┐{c['reset']}\n")
        sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + title_line, INNER_WIDTH)}{c['cyan']}│{c['reset']}\n")
        sys.stdout.write(f"{c['cyan']}├{'─'*INNER_WIDTH}┤{c['reset']}\n")
        sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + active_line, INNER_WIDTH)}{c['cyan']}│{c['reset']}\n")
        sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + appid_line, INNER_WIDTH)}{c['cyan']}│{c['reset']}\n")
        sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + sync_line, INNER_WIDTH)}{c['cyan']}│{c['reset']}\n")
        sys.stdout.write(f"{c['cyan']}└{'─'*INNER_WIDTH}┘{c['reset']}\n\n")
        sys.stdout.flush()
    else:
        sys.stdout.write(f"{c['orange']}⚠ ERROR: {result['error']}{c['reset']}\n\n")
        sys.stdout.flush()

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Marathon CLI — Stats and info for Bungie's Marathon."""
    if ctx.invoked_subcommand is None:
        print_motd()
        result = get_current_players(MARATHON_APP_ID)
        print_player_stats(result)

@cli.command()
def players():
    """Show current player count on Steam."""
    print_motd()
    result = get_current_players(MARATHON_APP_ID)
    print_player_stats(result)

@cli.command()
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def status(output_json):
    """Full system status check."""
    c = COLORS
    
    if output_json:
        result = get_current_players(MARATHON_APP_ID)
        click.echo(f'{{"success": {str(result["success"]).lower()}, "count": {result.get("count", "null")}}}')
        return
    
    print_motd()
    INNER_WIDTH = 50
    
    # Build content strings first to avoid quote nesting issues
    title_line = f"{c['bold']}SYSTEM STATUS{c['reset']}"
    
    result = get_current_players(MARATHON_APP_ID)
    if result["success"]:
        steam_line = f"{c['lime']}●{c['reset']} Steam API: {c['bright_green']}OPERATIONAL{c['reset']}"
        marathon_line = f"{c['lime']}●{c['reset']} Marathon: {c['bright_green']}ONLINE{c['reset']}"
        runners_line = f"{c['lime']}●{c['reset']} Runners: {c['cyan']}{result['count']:,}{c['reset']}"
    else:
        steam_line = f"{c['orange']}●{c['reset']} Steam API: {c['orange']}ERROR{c['reset']}"
        marathon_line = f"{c['orange']}●{c['reset']} Marathon: {c['orange']}UNREACHABLE{c['reset']}"
        runners_line = f"{c['orange']}●{c['reset']} Runners: N/A{c['reset']}"
    
    sys.stdout.write(f"{c['cyan']}┌{'─'*INNER_WIDTH}┐{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + title_line, INNER_WIDTH)}{c['cyan']}│{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}├{'─'*INNER_WIDTH}┤{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + steam_line, INNER_WIDTH)}{c['cyan']}│{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + marathon_line, INNER_WIDTH)}{c['cyan']}│{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}│{c['reset']}{rpad('  ' + runners_line, INNER_WIDTH)}{c['cyan']}│{c['reset']}\n")
    sys.stdout.write(f"{c['cyan']}└{'─'*INNER_WIDTH}┘{c['reset']}\n\n")
    sys.stdout.flush()

if __name__ == "__main__":
    cli()