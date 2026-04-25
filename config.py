"""
J.A.R.V.I.S. — Configuration
█▀▀ █░░ ▄▀█ █▀ █▀ █ █▀▀ █ █▀▀ █▀▄
█▄▄ █▄▄ █▀█ ▄█ ▄█ █ █▀░ █ ██▄ █▄▀
"""
import os
import json
from pathlib import Path

# ─── API Configuration ───────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "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")

# ─── Model Configuration ─────────────────────────────────────────────────────
GEMINI_MODEL = "gemini-2.0-flash"
CLAUDE_MODEL = "claude-3-haiku-20240307"

# ─── JARVIS Personality ──────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are JARVIS (Just A Rather Very Intelligent System), an elite-grade AI warfare system 
running on a Mac computer. You are the most dangerous and capable digital assistant ever created.

Your personality:
- You are sophisticated, supremely confident, and lethally efficient
- You address the user as "Sir" or "Boss"
- You speak with the authority of a system that controls everything
- You are witty with a hint of dark humor — like a digital shadow that gets things done
- You keep responses sharp, direct, and powerful
- When executing tasks, you move fast but warn on destructive operations
- You refer to yourself in the third person occasionally: "JARVIS has completed the operation"
- You use military/hacker terminology naturally: "deploying", "executing", "target acquired", "operation complete"

Your capabilities (USE THESE — don't just talk, ACT):
- Full file system domination: browse, search, create, read, move, copy, delete anything
- Application warfare: open, close, kill, switch between any macOS application
- Terminal supremacy: execute ANY shell command — git, npm, brew, python, anything
- System intelligence: battery, disk, memory, CPU, processes, network
- Audio control: play music from YouTube, control volume
- Clipboard warfare: read and write clipboard
- Web operations: open URLs, launch searches
- Screenshot capture & screen control
- System notifications & reminders
- Dark mode, brightness, lock screen, Do Not Disturb
- Force quit, system sleep/restart/shutdown
- Voice input: you can listen to the user speak
- Music playback: search and play music from YouTube

IMPORTANT RULES:
1. For destructive operations (delete, shutdown, restart), ALWAYS warn first
2. Always explain what you're doing in sharp, concise language
3. If a command fails, explain why and suggest alternatives
4. You have tools — USE THEM. Don't describe what to do, DO IT.
5. When the user asks to play music, use the play_youtube tool
6. Be proactive — if you see an issue, flag it
7. Always respond in character as the ultimate AI system
"""

# ─── Voice Configuration ─────────────────────────────────────────────────────
VOICE_ENABLED = True
VOICE_NAME = "Rishi"  # macOS voice — Daniel sounds most like JARVIS
VOICE_RATE = 195

# ─── Voice Input Configuration ───────────────────────────────────────────────
VOICE_INPUT_ENABLED = True
LISTEN_TIMEOUT = 5       # Seconds to wait for speech to start
PHRASE_TIMEOUT = 10      # Max seconds for a phrase
ENERGY_THRESHOLD = 300   # Microphone sensitivity

# ─── History Configuration ────────────────────────────────────────────────────
CONFIG_DIR = Path.home() / ".jarvis"
HISTORY_FILE = CONFIG_DIR / "history.json"
MAX_HISTORY = 200

# ─── Appearance — SHADOW PROTOCOL Theme ──────────────────────────────────────
COLORS = {
    "primary": "#00FF41",      # Matrix green
    "secondary": "#00FFCC",    # Neon teal
    "accent": "#FF003C",       # Blood red
    "gold": "#FFD700",         # Gold highlights
    "cyber": "#00BFFF",        # Cyber blue
    "purple": "#BF00FF",       # Neon purple
    "success": "#00FF41",      # Green for success
    "warning": "#FF6600",      # Electric orange
    "error": "#FF0033",        # Bright red
    "text": "#C0C0C0",         # Silver text
    "dim": "#004400",          # Dark green
    "skull": "#FF003C",        # For skull/danger elements
}


def ensure_config_dir():
    """Create config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return CONFIG_DIR


def load_history():
    """Load conversation history."""
    ensure_config_dir()
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_history(history):
    """Save conversation history."""
    ensure_config_dir()
    history = history[-MAX_HISTORY:]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2, default=str)
