#!/usr/bin/env python3
"""
J.A.R.V.I.S. — SHADOW PROTOCOL v3.0
Just A Rather Very Intelligent System

Voice + Text • 50 Tools • YouTube Music • Full Mac Control
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.terminal import (
    console, boot_sequence, print_prompt, print_user_message,
    print_jarvis_response, print_tool_call, print_tool_result,
    print_thinking, print_error, print_info, print_help,
    print_shutdown, print_voice_status, print_warning,
    print_voice_listening, print_voice_result, print_voice_error,
)
from core.voice import JarvisVoice
from config import VOICE_ENABLED, VOICE_NAME, VOICE_RATE, GEMINI_API_KEY, CLAUDE_API_KEY


def authenticate_user():
    """Verify biometric signature (Touch ID / Password)."""
    import subprocess
    import time
    
    auth_bin = os.path.join(os.path.dirname(__file__), "core", "jarvis_auth")
    if os.path.exists(auth_bin):
        console.clear()
        console.print("\n[bold red]    ⚠ BIOMETRIC LOCK ENGAGED ⚠[/bold red]")
        console.print("[dim cyan]    Awaiting fingerprint signature...[/dim cyan]\n")
        
        try:
            result = subprocess.run([auth_bin], capture_output=True, text=True)
            if "SUCCESS" in result.stdout:
                console.print("[bold green]    ✔ SIGNATURE VERIFIED[/bold green]")
                time.sleep(0.5)
                return True
            elif "UNAVAILABLE" in result.stdout:
                # No Touch ID hardware available
                return True
            else:
                return False
        except Exception as e:
            return True # Fail open if binary crashes
    return True

def main():
    parser = argparse.ArgumentParser(description="JARVIS — SHADOW PROTOCOL")
    parser.add_argument("--no-voice", action="store_true", help="Disable voice output")
    parser.add_argument("--voice", type=str, default=VOICE_NAME, help="macOS voice name")
    args = parser.parse_args()

    # Biometric Security Check
    if not authenticate_user():
        console.print("\n[bold red]█ ACCESS DENIED: UNAUTHORIZED USER █[/bold red]\n")
        sys.exit(1)

    # Check API Key
    if not GEMINI_API_KEY and not CLAUDE_API_KEY:
        console.print("\n[bold red]█ NO API KEY █[/bold red]")
        console.print("[white]Get one at:[/white] [cyan]https://console.anthropic.com/settings/keys[/cyan]")
        console.print("[white]Then:[/white] [green]export CLAUDE_API_KEY='your-key'[/green]\n")
        sys.exit(1)

    # Initialize voice
    voice = JarvisVoice(enabled=VOICE_ENABLED and not args.no_voice, voice_name=args.voice, rate=VOICE_RATE)

    # Boot
    boot_sequence()

    # Initialize brain
    try:
        if CLAUDE_API_KEY:
            from core.claude_brain import ClaudeBrain
            brain = ClaudeBrain()
            print_info("Neural engine: CLAUDE 3 HAIKU")
        else:
            from core.brain import JarvisBrain
            brain = JarvisBrain()
            print_info("Neural engine: GEMINI 2.0 FLASH")
    except Exception as e:
        print_error(f"Brain init failed: {e}")
        sys.exit(1)

    voice.speak("All systems online. JARVIS at your command, Sir.")

    # ── Main Loop ────────────────────────────────────────────────────────
    while True:
        try:
            print_prompt()
            user_input = input().strip()
            if not user_input: continue

            lower = user_input.lower()

            # ── Built-in Commands ────────────────────────────────────
            if lower in ("quit", "exit", "bye", "shutdown jarvis"):
                voice.speak("Disengaging. Until next time, Sir.")
                print_shutdown()
                break

            if lower == "help":
                print_help(); continue

            if lower == "clear":
                console.clear(); continue

            if lower == "reset":
                brain.reset()
                print_info("Neural pathways wiped. Memory cleared.")
                voice.speak("Memory purged. Starting fresh.")
                continue

            if lower in ("voice on", "voice enable"):
                voice.enabled = True; print_voice_status(True)
                voice.speak("Voice synthesis armed."); continue

            if lower in ("voice off", "voice disable"):
                voice.enabled = False; print_voice_status(False); continue

            # ── Voice Input Mode ─────────────────────────────────────
            if lower in ("v", "voice", "listen", "mic"):
                if not voice.can_listen():
                    print_error("Voice input not available!\nInstall: pip install SpeechRecognition PyAudio\nAlso: brew install portaudio")
                    continue
                
                print_voice_listening()
                text, error = voice.listen(timeout=7, phrase_timeout=15)
                
                if error:
                    print_voice_error(error)
                    continue
                if not text:
                    print_voice_error("No speech detected.")
                    continue
                
                print_voice_result(text)
                user_input = text  # Process the voice input as a command
                # Fall through to AI processing below

            # ── Process with Offline Engine (Fallback/Speed) ─────────
            from core.offline import OfflineProcessor
            offline_engine = OfflineProcessor()
            handled, off_response, tool_name, tool_args, tool_res = offline_engine.process(user_input)
            
            if handled:
                print_user_message(user_input)
                if tool_name:
                    print_tool_call(tool_name, tool_args)
                    print_tool_result(tool_name, tool_res)
                print_jarvis_response(off_response)
                voice.speak(off_response)
                continue

            # ── Process with AI ──────────────────────────────────────
            print_user_message(user_input)

            with print_thinking():
                response = brain.process(
                    user_input,
                    on_tool_call=print_tool_call,
                    on_tool_result=print_tool_result,
                )

            # Intercept API errors to sound cooler
            if "Communication error" in response:
                error_msg = "Sir, my connection to the primary neural core is compromised. The API key may be invalid or quota-restricted. However, my local offline systems remain fully functional."
                print_jarvis_response(response) # Print actual technical error
                voice.speak(error_msg)
            else:
                print_jarvis_response(response)
                voice.speak(response)

        except KeyboardInterrupt:
            console.print()
            print_info("Interrupted. Type 'quit' to disengage.")
            try: continue
            except KeyboardInterrupt:
                print_shutdown(); break

        except EOFError:
            print_shutdown(); break

        except Exception as e:
            print_error(f"Unexpected: {e}")
            continue

    voice.stop()
    sys.exit(0)


if __name__ == "__main__":
    main()
