"""
JARVIS Core Tools — System-level operations for macOS
"""
import os
import sys
import json
import shutil
import subprocess
import datetime
import platform
import glob
import mimetypes
import signal
from pathlib import Path
from urllib.parse import quote_plus

# Music process state
_music_process = None

def _human_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"

# ═══════════ FILE SYSTEM ═══════════════════════════════════════════════════════

def list_directory(path="~", show_hidden=False):
    path = os.path.expanduser(path)
    if not os.path.exists(path): return {"error": f"Path does not exist: {path}"}
    if not os.path.isdir(path): return {"error": f"Not a directory: {path}"}
    items = []
    try:
        for entry in sorted(os.scandir(path), key=lambda e: e.name):
            if not show_hidden and entry.name.startswith('.'): continue
            try:
                stat = entry.stat()
                items.append({"name": entry.name, "type": "directory" if entry.is_dir() else "file",
                    "size": stat.st_size if entry.is_file() else None,
                    "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()})
            except (PermissionError, OSError):
                items.append({"name": entry.name, "type": "unknown", "error": "permission denied"})
    except PermissionError: return {"error": f"Permission denied: {path}"}
    return {"path": path, "count": len(items), "items": items}

def read_file(path, max_lines=200):
    path = os.path.expanduser(path)
    if not os.path.exists(path): return {"error": f"File does not exist: {path}"}
    if not os.path.isfile(path): return {"error": f"Not a file: {path}"}
    mime_type, _ = mimetypes.guess_type(path)
    file_size = os.path.getsize(path)
    if mime_type and not mime_type.startswith('text') and mime_type not in ['application/json','application/xml','application/javascript']:
        return {"path": path, "type": mime_type, "size": file_size, "content": f"[Binary file — {mime_type}, {file_size} bytes]"}
    try:
        with open(path, 'r', errors='replace') as f: lines = f.readlines()
        total = len(lines)
        return {"path": path, "size": file_size, "total_lines": total, "truncated": total > max_lines, "content": ''.join(lines[:max_lines])}
    except Exception as e: return {"error": str(e)}

def write_file(path, content, create_dirs=True):
    path = os.path.expanduser(path)
    try:
        if create_dirs: os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w') as f: f.write(content)
        return {"success": True, "path": path, "size": len(content)}
    except Exception as e: return {"error": str(e)}

def create_directory(path):
    path = os.path.expanduser(path)
    try: os.makedirs(path, exist_ok=True); return {"success": True, "path": path}
    except Exception as e: return {"error": str(e)}

def delete_path(path):
    path = os.path.expanduser(path)
    if not os.path.exists(path): return {"error": f"Path does not exist: {path}"}
    try:
        if os.path.isfile(path): os.remove(path); return {"success": True, "deleted": path, "type": "file"}
        else: shutil.rmtree(path); return {"success": True, "deleted": path, "type": "directory"}
    except Exception as e: return {"error": str(e)}

def move_path(source, destination):
    source, destination = os.path.expanduser(source), os.path.expanduser(destination)
    if not os.path.exists(source): return {"error": f"Source does not exist: {source}"}
    try: shutil.move(source, destination); return {"success": True, "from": source, "to": destination}
    except Exception as e: return {"error": str(e)}

def copy_path(source, destination):
    source, destination = os.path.expanduser(source), os.path.expanduser(destination)
    if not os.path.exists(source): return {"error": f"Source does not exist: {source}"}
    try:
        if os.path.isfile(source): os.makedirs(os.path.dirname(destination) or '.', exist_ok=True); shutil.copy2(source, destination)
        else: shutil.copytree(source, destination)
        return {"success": True, "from": source, "to": destination}
    except Exception as e: return {"error": str(e)}

def search_files(directory="~", pattern="*", recursive=True):
    directory = os.path.expanduser(directory)
    try:
        if recursive: matches = list(glob.glob(os.path.join(directory, "**", pattern), recursive=True))
        else: matches = list(glob.glob(os.path.join(directory, pattern)))
        total = len(matches); matches = matches[:50]
        return {"directory": directory, "pattern": pattern, "total_matches": total, "showing": len(matches), "matches": matches}
    except Exception as e: return {"error": str(e)}

def get_file_info(path):
    path = os.path.expanduser(path)
    if not os.path.exists(path): return {"error": f"Path does not exist: {path}"}
    stat = os.stat(path); mime_type, _ = mimetypes.guess_type(path)
    return {"path": os.path.abspath(path), "name": os.path.basename(path), "type": "directory" if os.path.isdir(path) else "file",
        "size": stat.st_size, "size_human": _human_size(stat.st_size),
        "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(), "mime_type": mime_type}

def search_with_spotlight(query, limit=20):
    try:
        result = subprocess.run(["mdfind", "-limit", str(limit), query], capture_output=True, text=True, timeout=15)
        matches = [m for m in result.stdout.strip().split('\n') if m]
        return {"query": query, "matches": matches, "count": len(matches)}
    except Exception as e: return {"error": str(e)}

# ═══════════ APPLICATION CONTROL ═══════════════════════════════════════════════

def open_application(app_name):
    try:
        result = subprocess.run(["open", "-a", app_name], capture_output=True, text=True, timeout=10)
        if result.returncode == 0: return {"success": True, "app": app_name, "action": "opened"}
        return {"error": f"Cannot open {app_name}: {result.stderr.strip()}"}
    except Exception as e: return {"error": str(e)}

def close_application(app_name):
    try:
        result = subprocess.run(["osascript", "-e", f'tell application "{app_name}" to quit'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0: return {"success": True, "app": app_name, "action": "closed"}
        return {"error": result.stderr.strip()}
    except Exception as e: return {"error": str(e)}

def list_running_apps():
    try:
        script = 'tell application "System Events" to return name of every application process whose background only is false'
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            apps = [a.strip() for a in result.stdout.strip().split(",")]
            return {"running_apps": apps, "count": len(apps)}
        return {"error": result.stderr.strip()}
    except Exception as e: return {"error": str(e)}

def activate_application(app_name):
    try:
        subprocess.run(["osascript", "-e", f'tell application "{app_name}" to activate'], capture_output=True, text=True, timeout=10)
        return {"success": True, "app": app_name, "action": "activated"}
    except Exception as e: return {"error": str(e)}

def list_installed_apps():
    apps = []
    for app_dir in ["/Applications", os.path.expanduser("~/Applications")]:
        if os.path.exists(app_dir):
            for item in os.listdir(app_dir):
                if item.endswith('.app'): apps.append(item.replace('.app', ''))
    apps.sort()
    return {"installed_apps": apps, "count": len(apps)}

def force_quit_app(app_name):
    try:
        subprocess.run(["pkill", "-9", "-f", app_name], capture_output=True, text=True, timeout=5)
        return {"success": True, "force_killed": app_name}
    except Exception as e: return {"error": str(e)}

def get_frontmost_app():
    try:
        script = 'tell application "System Events" to return name of first application process whose frontmost is true'
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=5)
        return {"frontmost_app": result.stdout.strip()}
    except Exception as e: return {"error": str(e)}

# ═══════════ SHELL COMMANDS ════════════════════════════════════════════════════

def run_shell_command(command, timeout=30):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout, cwd=os.path.expanduser("~"))
        return {"command": command, "exit_code": result.returncode, "stdout": result.stdout[:5000], "stderr": result.stderr[:2000], "success": result.returncode == 0}
    except subprocess.TimeoutExpired: return {"error": f"Command timed out after {timeout}s", "command": command}
    except Exception as e: return {"error": str(e)}

# ═══════════ SYSTEM INFO ═══════════════════════════════════════════════════════

def get_system_info():
    try: import psutil
    except ImportError: psutil = None
    info = {"os": platform.system(), "os_version": platform.mac_ver()[0], "architecture": platform.machine(),
        "hostname": platform.node(), "user": os.environ.get("USER", "unknown"), "home": str(Path.home())}
    if psutil:
        info["cpu_count"] = psutil.cpu_count(); info["cpu_percent"] = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory(); info["memory_total"] = _human_size(mem.total); info["memory_available"] = _human_size(mem.available); info["memory_percent"] = mem.percent
        disk = psutil.disk_usage('/'); info["disk_total"] = _human_size(disk.total); info["disk_free"] = _human_size(disk.free); info["disk_percent"] = disk.percent
        battery = psutil.sensors_battery()
        if battery: info["battery_percent"] = battery.percent; info["battery_charging"] = battery.power_plugged
    return info

def get_running_processes(sort_by="memory", limit=15):
    try: import psutil
    except ImportError: return {"error": "psutil not installed"}
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try: processes.append(proc.info)
        except: continue
    key = 'memory_percent' if sort_by == 'memory' else 'cpu_percent'
    processes.sort(key=lambda p: p.get(key, 0) or 0, reverse=True)
    return {"processes": processes[:limit], "total_count": len(processes)}

def get_battery_status():
    try:
        result = subprocess.run(["pmset", "-g", "batt"], capture_output=True, text=True, timeout=5)
        return {"battery_info": result.stdout.strip()}
    except Exception as e: return {"error": str(e)}

def get_disk_usage(path="/"):
    try:
        import psutil; usage = psutil.disk_usage(path)
        return {"path": path, "total": _human_size(usage.total), "used": _human_size(usage.used), "free": _human_size(usage.free), "percent": usage.percent}
    except: 
        result = subprocess.run(["df", "-h", path], capture_output=True, text=True)
        return {"disk_usage": result.stdout.strip()}

def get_current_datetime():
    now = datetime.datetime.now()
    return {"date": now.strftime("%A, %B %d, %Y"), "time": now.strftime("%I:%M:%S %p"), "unix": int(now.timestamp())}

# ═══════════ SYSTEM CONTROLS ══════════════════════════════════════════════════

def set_volume(level):
    level = max(0, min(100, level))
    try:
        subprocess.run(["osascript", "-e", f"set volume output volume {level}"], capture_output=True, timeout=5)
        return {"success": True, "volume": level}
    except Exception as e: return {"error": str(e)}

def toggle_dark_mode():
    try:
        script = 'tell application "System Events" to tell appearance preferences to set dark mode to not dark mode\nreturn dark mode of appearance preferences of application "System Events"'
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=5)
        return {"success": True, "dark_mode": result.stdout.strip() == "true"}
    except Exception as e: return {"error": str(e)}

def take_screenshot(save_path="~/Desktop/screenshot.png"):
    save_path = os.path.expanduser(save_path)
    try:
        subprocess.run(["screencapture", "-x", save_path], capture_output=True, timeout=10)
        return {"success": True, "path": save_path} if os.path.exists(save_path) else {"error": "Screenshot failed"}
    except Exception as e: return {"error": str(e)}

def send_notification(title, message):
    try:
        subprocess.run(["osascript", "-e", f'display notification "{message}" with title "{title}"'], capture_output=True, timeout=5)
        return {"success": True, "title": title}
    except Exception as e: return {"error": str(e)}

def open_url(url):
    try: subprocess.run(["open", url], capture_output=True, timeout=5); return {"success": True, "url": url}
    except Exception as e: return {"error": str(e)}

def get_clipboard():
    try: result = subprocess.run(["pbpaste"], capture_output=True, text=True, timeout=5); return {"clipboard": result.stdout[:2000]}
    except Exception as e: return {"error": str(e)}

def set_clipboard(text):
    try:
        p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE); p.communicate(text.encode('utf-8'))
        return {"success": True, "copied_length": len(text)}
    except Exception as e: return {"error": str(e)}

def get_wifi_info():
    try:
        result = subprocess.run(["networksetup", "-getairportnetwork", "en0"], capture_output=True, text=True, timeout=5)
        return {"wifi_info": result.stdout.strip()}
    except Exception as e: return {"error": str(e)}

def get_ip_address():
    info = {}
    try: result = subprocess.run(["ipconfig", "getifaddr", "en0"], capture_output=True, text=True, timeout=5); info["local_ip"] = result.stdout.strip()
    except: info["local_ip"] = "unknown"
    try: result = subprocess.run(["curl", "-s", "https://api.ipify.org"], capture_output=True, text=True, timeout=10); info["public_ip"] = result.stdout.strip()
    except: info["public_ip"] = "unknown"
    return info

def empty_trash():
    try:
        subprocess.run(["osascript", "-e", 'tell application "Finder" to empty trash'], capture_output=True, timeout=30)
        return {"success": True, "action": "Trash emptied"}
    except Exception as e: return {"error": str(e)}

def lock_screen():
    try:
        subprocess.run(["pmset", "displaysleepnow"], capture_output=True, timeout=5)
        return {"success": True, "action": "Screen locked"}
    except Exception as e: return {"error": str(e)}

def kill_process(process_name):
    try: subprocess.run(["pkill", "-f", process_name], capture_output=True, timeout=5); return {"success": True, "killed": process_name}
    except Exception as e: return {"error": str(e)}

def set_brightness(level):
    return {"info": f"Install brightness CLI: brew install brightness. Requested: {level}%"}

def create_reminder(title, notes=""):
    try:
        script = f'tell application "Reminders" to tell list "Reminders" to make new reminder with properties {{name:"{title}", body:"{notes}"}}'
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=10)
        return {"success": True, "reminder": title}
    except Exception as e: return {"error": str(e)}

def get_calendar_events():
    try:
        script = '''set today to current date
set tomorrow to today + 1 * days
tell application "Calendar"
    set todayEvents to {}
    repeat with cal in calendars
        set evts to (every event of cal whose start date >= today and start date < tomorrow)
        repeat with evt in evts
            set end of todayEvents to {summary of evt, start date of evt as string}
        end repeat
    end repeat
    return todayEvents
end tell'''
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=10)
        return {"events": result.stdout.strip()}
    except Exception as e: return {"error": str(e)}

def type_text(text):
    try:
        escaped = text.replace('"', '\\"')
        subprocess.run(["osascript", "-e", f'tell application "System Events" to keystroke "{escaped}"'], capture_output=True, timeout=5)
        return {"success": True, "typed": text[:50]}
    except Exception as e: return {"error": str(e)}

# ═══════════ NEW: YOUTUBE MUSIC ═══════════════════════════════════════════════

def play_youtube(query):
    """Search and play music from YouTube."""
    global _music_process
    # Stop any currently playing music
    if _music_process:
        try: _music_process.terminate(); _music_process.wait(timeout=3)
        except: pass
        _music_process = None

    # Try yt-dlp + mpv (background audio streaming)
    try:
        subprocess.run(["which", "mpv"], capture_output=True, check=True)
        # Get stream URL with yt-dlp (pip installed)
        result = subprocess.run(
            ["yt-dlp", "--get-url", "--get-title", "-f", "bestaudio",
             f"ytsearch1:{query}"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            title = lines[0] if len(lines) >= 2 else query
            url = lines[-1]
            _music_process = subprocess.Popen(
                ["mpv", "--no-video", "--really-quiet", url],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return {"success": True, "playing": title, "method": "mpv_stream"}
    except Exception:
        pass

    # Fallback: open YouTube in browser
    search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    subprocess.run(["open", search_url], capture_output=True, timeout=5)
    return {"success": True, "query": query, "method": "browser", "message": f"Opened YouTube search for: {query}"}

def stop_music():
    """Stop currently playing music."""
    global _music_process
    if _music_process:
        try: _music_process.terminate(); _music_process.wait(timeout=3)
        except: 
            try: _music_process.kill()
            except: pass
        _music_process = None
        return {"success": True, "action": "Music stopped"}
    return {"info": "No music currently playing"}

def pause_resume_music():
    """Pause or resume music playback (mpv only — sends SIGSTOP/SIGCONT)."""
    global _music_process
    if _music_process and _music_process.poll() is None:
        try:
            os.kill(_music_process.pid, signal.SIGSTOP)
            return {"success": True, "action": "Music paused/resumed (toggle)"}
        except: return {"error": "Cannot pause music"}
    return {"info": "No music currently playing"}

# ═══════════ NEW: POWER CONTROLS ═════════════════════════════════════════════

def sleep_system():
    """Put the Mac to sleep."""
    try:
        subprocess.run(["pmset", "sleepnow"], capture_output=True, timeout=5)
        return {"success": True, "action": "System sleeping"}
    except Exception as e: return {"error": str(e)}

def restart_system():
    """Restart the Mac. DANGEROUS — warns user."""
    try:
        subprocess.run(["osascript", "-e", 'tell application "System Events" to restart'], capture_output=True, timeout=5)
        return {"success": True, "action": "System restarting"}
    except Exception as e: return {"error": str(e)}

def shutdown_system():
    """Shutdown the Mac. DANGEROUS — warns user."""
    try:
        subprocess.run(["osascript", "-e", 'tell application "System Events" to shut down'], capture_output=True, timeout=5)
        return {"success": True, "action": "System shutting down"}
    except Exception as e: return {"error": str(e)}

def toggle_do_not_disturb():
    """Toggle Do Not Disturb / Focus mode."""
    try:
        script = '''
        tell application "System Events"
            tell process "ControlCenter"
                click menu bar item "Focus" of menu bar 1
            end tell
        end tell'''
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
        return {"success": True, "action": "Toggled Do Not Disturb"}
    except Exception as e: return {"error": str(e)}

def open_finder_at(path="~"):
    """Open Finder at a specific path."""
    path = os.path.expanduser(path)
    try:
        subprocess.run(["open", path], capture_output=True, timeout=5)
        return {"success": True, "opened": path}
    except Exception as e: return {"error": str(e)}

def get_screen_resolution():
    """Get current screen resolution."""
    try:
        result = subprocess.run(["system_profiler", "SPDisplaysDataType"], capture_output=True, text=True, timeout=10)
        for line in result.stdout.split('\n'):
            if 'Resolution' in line:
                return {"resolution": line.strip()}
        return {"display_info": result.stdout[:500]}
    except Exception as e: return {"error": str(e)}

def compress_files(paths, output_path="~/Desktop/archive.zip"):
    """Compress files/folders into a zip archive."""
    output_path = os.path.expanduser(output_path)
    try:
        cmd = ["zip", "-r", output_path] + [os.path.expanduser(p) for p in paths.split(",")]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return {"success": True, "archive": output_path} if result.returncode == 0 else {"error": result.stderr}
    except Exception as e: return {"error": str(e)}

def get_storage_breakdown():
    """Get storage breakdown by major folders."""
    folders = {"Desktop": "~/Desktop", "Downloads": "~/Downloads", "Documents": "~/Documents", "Pictures": "~/Pictures", "Music": "~/Music", "Movies": "~/Movies"}
    breakdown = {}
    for name, path in folders.items():
        path = os.path.expanduser(path)
        if os.path.exists(path):
            try:
                result = subprocess.run(["du", "-sh", path], capture_output=True, text=True, timeout=30)
                breakdown[name] = result.stdout.split('\t')[0].strip()
            except: breakdown[name] = "unknown"
    return {"breakdown": breakdown}


# ═══════════ TOOL REGISTRY ════════════════════════════════════════════════════

TOOL_FUNCTIONS = {
    "list_directory": list_directory, "read_file": read_file, "write_file": write_file,
    "create_directory": create_directory, "delete_path": delete_path, "move_path": move_path,
    "copy_path": copy_path, "search_files": search_files, "get_file_info": get_file_info,
    "search_with_spotlight": search_with_spotlight,
    "open_application": open_application, "close_application": close_application,
    "list_running_apps": list_running_apps, "activate_application": activate_application,
    "list_installed_apps": list_installed_apps, "force_quit_app": force_quit_app,
    "get_frontmost_app": get_frontmost_app,
    "run_shell_command": run_shell_command,
    "get_system_info": get_system_info, "get_running_processes": get_running_processes,
    "get_battery_status": get_battery_status, "get_disk_usage": get_disk_usage,
    "get_current_datetime": get_current_datetime,
    "set_volume": set_volume, "toggle_dark_mode": toggle_dark_mode,
    "take_screenshot": take_screenshot, "send_notification": send_notification,
    "open_url": open_url, "get_clipboard": get_clipboard, "set_clipboard": set_clipboard,
    "get_wifi_info": get_wifi_info, "get_ip_address": get_ip_address,
    "empty_trash": empty_trash, "lock_screen": lock_screen, "kill_process": kill_process,
    "set_brightness": set_brightness, "create_reminder": create_reminder,
    "get_calendar_events": get_calendar_events, "type_text": type_text,
    "play_youtube": play_youtube, "stop_music": stop_music, "pause_resume_music": pause_resume_music,
    "sleep_system": sleep_system, "restart_system": restart_system, "shutdown_system": shutdown_system,
    "toggle_do_not_disturb": toggle_do_not_disturb, "open_finder_at": open_finder_at,
    "get_screen_resolution": get_screen_resolution, "compress_files": compress_files,
    "get_storage_breakdown": get_storage_breakdown,
}
