"""
JARVIS Terminal UI — SHADOW PROTOCOL Theme
Dangerous. Elite. Unstoppable.
"""
import time
import sys
import random
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.markdown import Markdown
from rich.align import Align
from rich.columns import Columns
from rich import box

console = Console()

# ═══════════ MATRIX RAIN ══════════════════════════════════════════════════════

def matrix_rain(lines=12):
    """Display matrix-style falling code."""
    width = min(console.width, 120)
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ@#$%&<>{}[]"
    for _ in range(lines):
        line = ""
        for c in range(width):
            if random.random() > 0.6:
                char = random.choice(chars)
                if random.random() > 0.7:
                    line += f"[bold green]{char}[/bold green]"
                else:
                    line += f"[dim green]{char}[/dim green]"
            else:
                line += " "
        console.print(line, highlight=False)
        time.sleep(0.04)

# ═══════════ GLITCH TEXT ══════════════════════════════════════════════════════

def glitch_text(text, iterations=3):
    """Display text with glitch effect."""
    glitch_chars = "█▓▒░╗╔╝╚═║╬╫╪┼┴┬├┤"
    for i in range(iterations):
        glitched = ""
        for ch in text:
            if random.random() > 0.7:
                glitched += random.choice(glitch_chars)
            else:
                glitched += ch
        console.print(f"\r[red]{glitched}[/red]", end="")
        time.sleep(0.08)
    console.print(f"\r[bold green]{text}[/bold green]")

# ═══════════ LOGO ═════════════════════════════════════════════════════════════

SKULL_LOGO = """[bold red]
                    ██████████████████
                ████░░░░░░░░░░░░░░░░████
              ██░░░░░░░░░░░░░░░░░░░░░░░░██
            ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░██
           ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██
          ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██
          ██░░░░░░████████░░░░████████░░░░░░░██
          ██░░░░░░████████░░░░████████░░░░░░░██
          ██░░░░░░████████░░░░████████░░░░░░░██
          ██░░░░░░░░░░░░░░░██░░░░░░░░░░░░░░░██
           ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██
            ██░░░░░░░████████████░░░░░░░░██
              ██░░░░░░░░░░░░░░░░░░░░░░░██
                ██░░██░░░░░░░░░░░██░░██
                  ██████████████████[/bold red]"""

JARVIS_TEXT = """[bold green]
       ▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
       ▐  ░█▀█░█▀█░█▀▀░█▀█░█▀█░▀█▀░█░█░█▀▄░█▀▀  ▌
       ▐  ░█░█░█▀▀░█▀▀░█▀▄░█▀█░░█░░█░█░█░█░█▀▀  ▌
       ▐  ░▀▀▀░▀░░░▀▀▀░▀░▀░▀░▀░░▀░░▀▀▀░▀▀░░▀▀▀  ▌
       ▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌[/bold green]"""

JARVIS_TITLE = """[bold cyan]
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
     ██║███████║██████╔╝██║   ██║██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝[/bold cyan]"""


# ═══════════ BOOT SEQUENCE ════════════════════════════════════════════════════

def boot_sequence():
    """OMEGA-class boot animation."""
    console.clear()
    
    # Phase 1: Matrix rain
    matrix_rain(10)
    time.sleep(0.2)
    console.clear()
    
    # Phase 2: Warning header
    console.print()
    warning_bar = "▓" * min(console.width, 80)
    console.print(f"[bold red]{warning_bar}[/bold red]")
    console.print(Align.center("[bold red blink]⚠  CLASSIFIED — OMEGA CLEARANCE REQUIRED  ⚠[/bold red blink]"))
    console.print(f"[bold red]{warning_bar}[/bold red]")
    time.sleep(0.3)
    
    # Phase 3: Skull
    console.print(Align.center(SKULL_LOGO))
    time.sleep(0.2)
    
    # Phase 4: JARVIS title with glitch
    console.print(Align.center(JARVIS_TITLE))
    console.print(Align.center("[dim green]Just A Rather Very Intelligent System[/dim green]"))
    console.print(Align.center("[dim red]█ SHADOW PROTOCOL v3.0 █[/dim red]"))
    console.print()
    
    # Phase 5: Boot sequence with hacker messages
    boot_steps = [
        ("Breaching neural firewall", "green"),
        ("Injecting AI consciousness", "green"),
        ("Establishing quantum link to Gemini core", "cyan"),
        ("Deploying system infiltration modules", "green"),
        ("Weaponizing file system access", "yellow"),
        ("Loading application warfare suite", "yellow"),
        ("Initializing voice recognition array", "cyan"),
        ("Arming YouTube music pipeline", "magenta"),
        ("Scanning all connected devices", "green"),
        ("Encrypting communication channel", "red"),
        ("AUTHORIZATION: OMEGA", "red"),
    ]
    
    for step_text, color in boot_steps:
        # Glitch effect on some steps
        if random.random() > 0.6:
            glitch_chars = "█▓▒░"
            glitched = ''.join(random.choice(glitch_chars) if random.random() > 0.7 else c for c in step_text)
            console.print(f"  [dim red]{glitched}[/dim red]", end="\r")
            time.sleep(0.06)
        
        with console.status(f"[{color}]{step_text}...[/{color}]", spinner="dots12"):
            time.sleep(random.uniform(0.15, 0.35))
        console.print(f"  [green]■[/green] [dim]{step_text}[/dim]")
    
    console.print()
    
    # Phase 6: ACCESS GRANTED
    time.sleep(0.2)
    granted_bar = "═" * min(console.width - 4, 76)
    console.print(f"[bold green]╔{granted_bar}╗[/bold green]")
    console.print(Align.center("[bold green on black]  ███  ACCESS GRANTED  ███  [/bold green on black]"))
    console.print(f"[bold green]╚{granted_bar}╝[/bold green]")
    console.print()
    
    # Phase 7: Status panel
    import psutil
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    
    status_content = Text.from_markup(
        f"[bold green]◉ JARVIS ONLINE[/bold green] — [dim]All 50 weapons systems armed[/dim]\n"
        f"[dim cyan]SYS_LD: CPU [{cpu_usage}%] | RAM [{ram_usage}%] | NET [STABLE][/dim cyan]\n\n"
        "[bold cyan]▸[/bold cyan] [white]Voice Input:[/white]  [green]Type [bold]'v'[/bold] to activate mic[/green]\n"
        "[bold cyan]▸[/bold cyan] [white]Music:[/white]        [green]\"Play [song name]\" — YouTube streaming[/green]\n"
        "[bold cyan]▸[/bold cyan] [white]Commands:[/white]     [green]Type [bold]'help'[/bold] for full arsenal[/green]\n"
        "[bold cyan]▸[/bold cyan] [white]Shutdown:[/white]     [red]Type [bold]'quit'[/bold] to disengage[/red]\n"
    )
    
    status_panel = Panel(
        Align.center(status_content),
        border_style="green",
        box=box.HEAVY,
        padding=(1, 3),
        title="[bold red]◆ OMEGA PROTOCOL ACTIVE ◆[/bold red]",
        subtitle="[dim green]v3.0 • Claude AI • Voice Enabled[/dim green]"
    )
    console.print(status_panel)
    console.print()


# ═══════════ DISPLAY FUNCTIONS ════════════════════════════════════════════════

def print_prompt():
    """Hacker-style prompt with dynamic elements."""
    user = os.environ.get("USER", "ghost")
    from datetime import datetime
    time_str = datetime.now().strftime("%H:%M")
    console.print(f"[dim white][{time_str}][/dim white] [bold red]┌──([/bold red][bold green]{user}@JARVIS[/bold green][bold red])─[/bold red][bold yellow][OMEGA][/bold yellow]")
    console.print(f"        [bold red]└──╼[/bold red] [bold green]$[/bold green] ", end="")

def print_user_message(message):
    console.print(f"\n[bold red]▶[/bold red] [bold white]{message}[/bold white]")

def print_jarvis_response(response):
    """Display response in hacker-style panel with telemetry."""
    console.print()
    try:
        from datetime import datetime
        import random
        
        now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        hex_key = "".join(random.choices("0123456789ABCDEF", k=12))
        
        panel = Panel(
            Markdown(response),
            border_style="green",
            box=box.HEAVY,
            padding=(1, 2),
            title=f"[bold green]◆ JARVIS[/bold green] [dim red]// OMEGA CLEARANCE[/dim red]",
            title_align="left",
            subtitle=f"[dim green]T:{now} | ENC:[bold]{hex_key}[/bold] | SECURE[/dim green]",
        )
        console.print(panel)
    except Exception as e:
        console.print(f"[green]JARVIS:[/green] {response}")
    console.print()

def print_tool_call(tool_name, args):
    display = tool_name.replace("_", " ").upper()
    args_str = ""
    if args:
        parts = []
        for k, v in args.items():
            vs = str(v); vs = vs[:50] + "..." if len(vs) > 50 else vs
            parts.append(f"[dim]{k}=[/dim][white]{vs}[/white]")
        args_str = " → " + ", ".join(parts)
    console.print(f"  [bold yellow]⚡ DEPLOYING:[/bold yellow] [bold cyan]{display}[/bold cyan]{args_str}")

def print_tool_result(tool_name, result):
    if isinstance(result, dict) and result.get("error"):
        console.print(f"  [bold red]✗ FAILED:[/bold red] [dim red]{result['error']}[/dim red]")
    else:
        console.print(f"  [bold green]■ TARGET HIT[/bold green]")

def print_thinking():
    return console.status("[bold cyan]◉ PROCESSING NEURAL PATHWAYS...[/bold cyan]", spinner="dots12")

def print_error(message):
    console.print(f"\n[bold red]█ SYSTEM ERROR █[/bold red] [red]{message}[/red]\n")

def print_info(message):
    console.print(f"[dim cyan]◈ {message}[/dim cyan]")

def print_warning(message):
    console.print(f"[bold yellow]⚠ ALERT: {message}[/bold yellow]")

def print_voice_listening():
    """Show listening indicator."""
    console.print(f"\n[bold magenta]🎙  VOICE ARRAY ACTIVE[/bold magenta] [dim]— Speak now, Sir...[/dim]")

def print_voice_result(text):
    """Show what was heard."""
    if text:
        console.print(f"[bold green]◉ CAPTURED:[/bold green] [white]\"{text}\"[/white]")

def print_voice_error(error):
    console.print(f"[dim red]◈ Voice: {error}[/dim red]")

def print_voice_status(enabled):
    if enabled:
        console.print("[bold green]🔊 Voice synthesis: ARMED[/bold green]")
    else:
        console.print("[bold yellow]🔇 Voice synthesis: SILENCED[/bold yellow]")

def print_music_status(info):
    console.print(f"[bold magenta]♫ NOW PLAYING:[/bold magenta] [white]{info}[/white]")


def print_help():
    """Display the full arsenal."""
    console.print()
    
    # Header
    header = "═" * min(console.width - 4, 76)
    console.print(f"[bold red]╔{header}╗[/bold red]")
    console.print(Align.center("[bold red]◆ JARVIS — FULL WEAPONS MANIFEST ◆[/bold red]"))
    console.print(f"[bold red]╚{header}╝[/bold red]")
    console.print()
    
    t = Table(box=box.SIMPLE_HEAVY, border_style="green", show_header=True, header_style="bold red", padding=(0, 2))
    t.add_column("SYSTEM", style="bold cyan", width=16)
    t.add_column("CAPABILITIES", style="white")
    
    t.add_row("📁 FILESYSTEM", "\"Show Desktop\" • \"Find all .py files\" • \"Read notes.txt\"\n\"Create folder\" • \"Delete/Move/Copy anything\"")
    t.add_row("🖥️ APPS", "\"Open Safari\" • \"Kill Chrome\" • \"What's running?\"\n\"Force quit Slack\" • \"Switch to VS Code\"")
    t.add_row("⚡ TERMINAL", "\"Run git status\" • \"npm install\" • \"brew update\"\nExecute ANY shell command")
    t.add_row("🧠 OFFLINE AI", "Math calculations • Wikipedia • Live Weather • Breaking News\nCrypto/Stock Prices • ISS Space Tracker • Cybersecurity IP Trace")
    t.add_row("⚠ TACTICAL", "\"Hack the mainframe\" • \"Initiate self destruct\"\n\"Arm weapons\" • \"Locate target\" • \"Matrix mode\"")
    t.add_row("📊 SYSTEM", "\"System report\" • \"Ping network\" • \"Battery?\"\n\"RAM usage?\" • \"Disk space?\" • \"Top processes\"")
    t.add_row("🎵 MUSIC", "\"Play Blinding Lights\" • \"Stop music\" • \"Pause\"\nYouTube streaming via yt-dlp + mpv")
    t.add_row("🗣️ VOICE", "\"[bold]v[/bold]\" = mic input • \"voice on/off\" = TTS toggle\nSpeak commands hands-free")
    t.add_row("🎛️ CONTROLS", "\"Volume 50\" • \"Dark mode\" • \"Screenshot\"\n\"Lock screen\" • \"Focus mode\" • \"Brightness\"")
    t.add_row("⚔️ POWER", "\"Sleep\" • \"Restart\" • \"Shutdown\"\n[red]REQUIRES CONFIRMATION[/red]")
    t.add_row("🌐 WEB", "\"Open github.com\" • \"Search Google for...\"\nOpen any URL instantly")
    t.add_row("🎲 OTHER", "\"Generate password\" • \"Tell a joke\" • \"Flip a coin\"\n\"Random fact\" • \"What day is it\" • \"Recommend a movie\"")
    
    console.print(t)
    console.print()
    
    cmd_table = Table(box=box.SIMPLE, border_style="dim green", show_header=True, header_style="bold green")
    cmd_table.add_column("HOTKEY", style="bold yellow", width=16)
    cmd_table.add_column("ACTION", style="white")
    cmd_table.add_row("v", "Activate voice input (speak a command)")
    cmd_table.add_row("voice on/off", "Toggle voice output (TTS)")
    cmd_table.add_row("help", "Show this manifest")
    cmd_table.add_row("clear", "Clear terminal")
    cmd_table.add_row("reset", "Wipe conversation memory")
    cmd_table.add_row("quit / exit", "Disengage JARVIS")
    console.print(cmd_table)
    console.print()


def print_shutdown():
    console.print()
    matrix_rain(5)
    
    shutdown_content = Text.from_markup(
        "[bold red]◉ DISENGAGING ALL SYSTEMS[/bold red]\n\n"
        "[dim]Neural link severed.\n"
        "Weapon systems powered down.\n"
        "Encryption protocols purged.\n\n"
        "Until next time, Sir.[/dim]"
    )
    panel = Panel(
        Align.center(shutdown_content),
        border_style="red",
        box=box.HEAVY,
        padding=(1, 3),
        title="[bold red]◆ SHADOW PROTOCOL TERMINATED ◆[/bold red]",
    )
    console.print(panel)
    console.print()
