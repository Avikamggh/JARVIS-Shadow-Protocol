"""
JARVIS Brain — AI reasoning engine powered by Claude 3.5 Sonnet.
"""
import json
import anthropic
from config import CLAUDE_API_KEY, CLAUDE_MODEL, SYSTEM_PROMPT
from core.tools import TOOL_FUNCTIONS

CLAUDE_TOOLS = [
    {"name": "list_directory", "description": "List files in a directory", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "show_hidden": {"type": "boolean"}}}},
    {"name": "read_file", "description": "Read file contents", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "write_file", "description": "Write to file", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
    {"name": "create_directory", "description": "Create dir", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "delete_path", "description": "Delete path", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "move_path", "description": "Move/rename", "input_schema": {"type": "object", "properties": {"source": {"type": "string"}, "destination": {"type": "string"}}, "required": ["source", "destination"]}},
    {"name": "copy_path", "description": "Copy file/dir", "input_schema": {"type": "object", "properties": {"source": {"type": "string"}, "destination": {"type": "string"}}, "required": ["source", "destination"]}},
    {"name": "search_files", "description": "Search glob", "input_schema": {"type": "object", "properties": {"directory": {"type": "string"}, "pattern": {"type": "string"}}, "required": ["pattern"]}},
    {"name": "get_file_info", "description": "File details", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "open_application", "description": "Open app", "input_schema": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}},
    {"name": "close_application", "description": "Close app", "input_schema": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}},
    {"name": "list_running_apps", "description": "List apps", "input_schema": {"type": "object", "properties": {}}},
    {"name": "activate_application", "description": "Focus app", "input_schema": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}},
    {"name": "force_quit_app", "description": "Kill app", "input_schema": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}},
    {"name": "run_shell_command", "description": "Run shell cmd", "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}},
    {"name": "get_system_info", "description": "System info", "input_schema": {"type": "object", "properties": {}}},
    {"name": "get_battery_status", "description": "Battery status", "input_schema": {"type": "object", "properties": {}}},
    {"name": "get_current_datetime", "description": "Get time", "input_schema": {"type": "object", "properties": {}}},
    {"name": "set_volume", "description": "Set volume", "input_schema": {"type": "object", "properties": {"level": {"type": "integer"}}, "required": ["level"]}},
    {"name": "toggle_dark_mode", "description": "Dark mode", "input_schema": {"type": "object", "properties": {}}},
    {"name": "take_screenshot", "description": "Screenshot", "input_schema": {"type": "object", "properties": {"save_path": {"type": "string"}}}},
    {"name": "open_url", "description": "Open browser URL", "input_schema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}},
    {"name": "get_clipboard", "description": "Get clipboard", "input_schema": {"type": "object", "properties": {}}},
    {"name": "set_clipboard", "description": "Set clipboard", "input_schema": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}},
    {"name": "empty_trash", "description": "Empty trash", "input_schema": {"type": "object", "properties": {}}},
    {"name": "lock_screen", "description": "Lock screen", "input_schema": {"type": "object", "properties": {}}},
    {"name": "type_text", "description": "Type keyboard", "input_schema": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}},
    {"name": "play_youtube", "description": "Play music from YT", "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "stop_music", "description": "Stop music", "input_schema": {"type": "object", "properties": {}}},
    {"name": "sleep_system", "description": "Sleep Mac", "input_schema": {"type": "object", "properties": {}}},
    {"name": "toggle_do_not_disturb", "description": "Toggle DND", "input_schema": {"type": "object", "properties": {}}},
]

class ClaudeBrain:
    def __init__(self):
        if not CLAUDE_API_KEY:
            raise ValueError("CLAUDE_API_KEY not set! export CLAUDE_API_KEY='your-key'")
        self.client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        self.messages = []

    def process(self, user_input, on_tool_call=None, on_tool_result=None):
        self.messages.append({"role": "user", "content": user_input})
        
        try:
            for _ in range(10): # Loop for multiple tool calls
                response = self.client.messages.create(
                    model=CLAUDE_MODEL,
                    max_tokens=4096,
                    system=SYSTEM_PROMPT,
                    messages=self.messages,
                    tools=CLAUDE_TOOLS,
                    temperature=0.7
                )
                
                self.messages.append({"role": "assistant", "content": response.content})
                
                tool_uses = [block for block in response.content if block.type == "tool_use"]
                if not tool_uses:
                    break
                    
                tool_results = []
                for tool_use in tool_uses:
                    name = tool_use.name
                    args = tool_use.input
                    if on_tool_call: on_tool_call(name, args)
                    
                    try:
                        result = TOOL_FUNCTIONS[name](**args) if name in TOOL_FUNCTIONS else {"error": f"Unknown tool: {name}"}
                    except Exception as e:
                        result = {"error": str(e)}
                        
                    if on_tool_result: on_tool_result(name, result)
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": json.dumps(result, default=str)
                    })
                    
                self.messages.append({"role": "user", "content": tool_results})
                
            # Final text response
            final_text = "".join([block.text for block in self.messages[-1]["content"] if getattr(block, "type", "") == "text"])
            if not final_text:
                for block in response.content:
                    if block.type == "text": final_text += block.text
                    
            return final_text if final_text else "Operation complete, Sir."
            
        except Exception as e:
            return f"Claude Communication error, Sir: {str(e)}"

    def reset(self):
        self.messages = []
