"""
JARVIS Brain — AI reasoning engine with Gemini function calling.
"""
import json
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT
from core.tools import TOOL_FUNCTIONS

TOOL_DECLARATIONS = [types.Tool(function_declarations=[
    types.FunctionDeclaration(name="list_directory", description="List files and folders in a directory.",
        parameters=types.Schema(type="OBJECT", properties={"path": types.Schema(type="STRING", description="Directory path. ~ for home."), "show_hidden": types.Schema(type="BOOLEAN", description="Show hidden files")})),
    types.FunctionDeclaration(name="read_file", description="Read contents of a text file.",
        parameters=types.Schema(type="OBJECT", properties={"path": types.Schema(type="STRING", description="File path."), "max_lines": types.Schema(type="INTEGER", description="Max lines to read.")}, required=["path"])),
    types.FunctionDeclaration(name="write_file", description="Write content to a file. Creates dirs if needed.",
        parameters=types.Schema(type="OBJECT", properties={"path": types.Schema(type="STRING", description="File path."), "content": types.Schema(type="STRING", description="Content to write.")}, required=["path", "content"])),
    types.FunctionDeclaration(name="create_directory", description="Create a new directory.",
        parameters=types.Schema(type="OBJECT", properties={"path": types.Schema(type="STRING", description="Directory path.")}, required=["path"])),
    types.FunctionDeclaration(name="delete_path", description="DELETE a file or directory permanently! DESTRUCTIVE!",
        parameters=types.Schema(type="OBJECT", properties={"path": types.Schema(type="STRING", description="Path to delete.")}, required=["path"])),
    types.FunctionDeclaration(name="move_path", description="Move or rename a file/directory.",
        parameters=types.Schema(type="OBJECT", properties={"source": types.Schema(type="STRING"), "destination": types.Schema(type="STRING")}, required=["source", "destination"])),
    types.FunctionDeclaration(name="copy_path", description="Copy a file or directory.",
        parameters=types.Schema(type="OBJECT", properties={"source": types.Schema(type="STRING"), "destination": types.Schema(type="STRING")}, required=["source", "destination"])),
    types.FunctionDeclaration(name="search_files", description="Search for files matching a glob pattern.",
        parameters=types.Schema(type="OBJECT", properties={"directory": types.Schema(type="STRING"), "pattern": types.Schema(type="STRING", description="Glob pattern e.g. *.py"), "recursive": types.Schema(type="BOOLEAN")}, required=["pattern"])),
    types.FunctionDeclaration(name="get_file_info", description="Get detailed info about a file/directory.",
        parameters=types.Schema(type="OBJECT", properties={"path": types.Schema(type="STRING")}, required=["path"])),
    types.FunctionDeclaration(name="search_with_spotlight", description="Search using macOS Spotlight (mdfind). Very powerful.",
        parameters=types.Schema(type="OBJECT", properties={"query": types.Schema(type="STRING"), "limit": types.Schema(type="INTEGER")}, required=["query"])),
    types.FunctionDeclaration(name="open_application", description="Open/launch a macOS application.",
        parameters=types.Schema(type="OBJECT", properties={"app_name": types.Schema(type="STRING", description="App name e.g. Safari, VS Code")}, required=["app_name"])),
    types.FunctionDeclaration(name="close_application", description="Quit an application gracefully.",
        parameters=types.Schema(type="OBJECT", properties={"app_name": types.Schema(type="STRING")}, required=["app_name"])),
    types.FunctionDeclaration(name="list_running_apps", description="List all running visible applications.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="activate_application", description="Bring an app to foreground.",
        parameters=types.Schema(type="OBJECT", properties={"app_name": types.Schema(type="STRING")}, required=["app_name"])),
    types.FunctionDeclaration(name="list_installed_apps", description="List all installed applications.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="force_quit_app", description="Force kill an application immediately.",
        parameters=types.Schema(type="OBJECT", properties={"app_name": types.Schema(type="STRING")}, required=["app_name"])),
    types.FunctionDeclaration(name="get_frontmost_app", description="Get the currently focused app.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="run_shell_command", description="Execute ANY shell/terminal command. Very powerful.",
        parameters=types.Schema(type="OBJECT", properties={"command": types.Schema(type="STRING", description="Shell command to run."), "timeout": types.Schema(type="INTEGER")}, required=["command"])),
    types.FunctionDeclaration(name="get_system_info", description="Get system info: OS, CPU, memory, disk, battery.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="get_running_processes", description="Get top processes by CPU or memory.",
        parameters=types.Schema(type="OBJECT", properties={"sort_by": types.Schema(type="STRING", description="'cpu' or 'memory'"), "limit": types.Schema(type="INTEGER")})),
    types.FunctionDeclaration(name="get_battery_status", description="Get battery level and charging status.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="get_disk_usage", description="Get disk space usage.",
        parameters=types.Schema(type="OBJECT", properties={"path": types.Schema(type="STRING")})),
    types.FunctionDeclaration(name="get_current_datetime", description="Get current date and time.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="set_volume", description="Set system volume 0-100.",
        parameters=types.Schema(type="OBJECT", properties={"level": types.Schema(type="INTEGER", description="Volume 0-100.")}, required=["level"])),
    types.FunctionDeclaration(name="toggle_dark_mode", description="Toggle macOS dark/light mode.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="take_screenshot", description="Capture a screenshot.",
        parameters=types.Schema(type="OBJECT", properties={"save_path": types.Schema(type="STRING")})),
    types.FunctionDeclaration(name="send_notification", description="Send a macOS notification.",
        parameters=types.Schema(type="OBJECT", properties={"title": types.Schema(type="STRING"), "message": types.Schema(type="STRING")}, required=["title", "message"])),
    types.FunctionDeclaration(name="open_url", description="Open a URL in browser.",
        parameters=types.Schema(type="OBJECT", properties={"url": types.Schema(type="STRING")}, required=["url"])),
    types.FunctionDeclaration(name="get_clipboard", description="Get clipboard contents.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="set_clipboard", description="Copy text to clipboard.",
        parameters=types.Schema(type="OBJECT", properties={"text": types.Schema(type="STRING")}, required=["text"])),
    types.FunctionDeclaration(name="get_wifi_info", description="Get Wi-Fi network info.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="get_ip_address", description="Get local and public IP.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="empty_trash", description="Empty the Trash. DESTRUCTIVE!",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="lock_screen", description="Lock the screen.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="kill_process", description="Force kill a process by name.",
        parameters=types.Schema(type="OBJECT", properties={"process_name": types.Schema(type="STRING")}, required=["process_name"])),
    types.FunctionDeclaration(name="create_reminder", description="Create a Reminder.",
        parameters=types.Schema(type="OBJECT", properties={"title": types.Schema(type="STRING"), "notes": types.Schema(type="STRING")}, required=["title"])),
    types.FunctionDeclaration(name="get_calendar_events", description="Get today's calendar events.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="type_text", description="Simulate keyboard typing in focused app.",
        parameters=types.Schema(type="OBJECT", properties={"text": types.Schema(type="STRING")}, required=["text"])),
    types.FunctionDeclaration(name="play_youtube", description="Search and play music from YouTube. Streams audio in background if mpv is installed, otherwise opens in browser.",
        parameters=types.Schema(type="OBJECT", properties={"query": types.Schema(type="STRING", description="Song name, artist, or search query.")}, required=["query"])),
    types.FunctionDeclaration(name="stop_music", description="Stop the currently playing music.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="pause_resume_music", description="Pause or resume music playback.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="sleep_system", description="Put the Mac to sleep.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="restart_system", description="Restart the Mac. DANGEROUS!",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="shutdown_system", description="Shutdown the Mac. DANGEROUS!",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="toggle_do_not_disturb", description="Toggle Do Not Disturb mode.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="open_finder_at", description="Open Finder at a specific path.",
        parameters=types.Schema(type="OBJECT", properties={"path": types.Schema(type="STRING")})),
    types.FunctionDeclaration(name="get_screen_resolution", description="Get screen resolution.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="compress_files", description="Compress files into a zip archive.",
        parameters=types.Schema(type="OBJECT", properties={"paths": types.Schema(type="STRING", description="Comma-separated paths."), "output_path": types.Schema(type="STRING")})),
    types.FunctionDeclaration(name="get_storage_breakdown", description="Get storage usage by major folders.",
        parameters=types.Schema(type="OBJECT", properties={})),
    types.FunctionDeclaration(name="set_brightness", description="Set screen brightness.",
        parameters=types.Schema(type="OBJECT", properties={"level": types.Schema(type="INTEGER")}, required=["level"])),
])]


class JarvisBrain:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set! export GEMINI_API_KEY='your-key'")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT, tools=TOOL_DECLARATIONS, temperature=0.7, max_output_tokens=4096)
        self.chat = self.client.chats.create(model=GEMINI_MODEL, config=self.config)

    def process(self, user_input, on_tool_call=None, on_tool_result=None):
        try: response = self.chat.send_message(user_input)
        except Exception as e: return f"Communication error, Sir: {str(e)}"

        for _ in range(10):
            if not response.candidates or not response.candidates[0].content.parts: break
            fcs = [p for p in response.candidates[0].content.parts if p.function_call]
            if not fcs: break

            func_responses = []
            for fc_part in fcs:
                fc = fc_part.function_call
                name, args = fc.name, dict(fc.args) if fc.args else {}
                if on_tool_call: on_tool_call(name, args)
                try: result = TOOL_FUNCTIONS[name](**args) if name in TOOL_FUNCTIONS else {"error": f"Unknown tool: {name}"}
                except Exception as e: result = {"error": str(e)}
                if on_tool_result: on_tool_result(name, result)
                func_responses.append(types.Part.from_function_response(name=name, response=result))

            try: response = self.chat.send_message(func_responses)
            except Exception as e: return f"Error processing results: {str(e)}"

        if response.candidates and response.candidates[0].content.parts:
            texts = [p.text for p in response.candidates[0].content.parts if hasattr(p, 'text') and p.text]
            if texts: return "\n".join(texts)
        return "Operation complete, Sir."

    def reset(self):
        self.chat = self.client.chats.create(model=GEMINI_MODEL, config=self.config)
