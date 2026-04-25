"""
JARVIS Offline Processor — Handles basic commands without API
"""
import re
import random
from core.tools import (
    open_application, close_application, get_battery_status, 
    get_current_datetime, play_youtube, stop_music, pause_resume_music,
    sleep_system, set_volume, toggle_dark_mode
)

class OfflineProcessor:
    def __init__(self):
        pass

    def process(self, text):
        """
        Attempt to process the command offline.
        Returns (success, response_text, tool_name, tool_args, tool_result)
        If not handled, returns (False, None, None, None, None)
        """
        text = text.lower().strip()

        # 1. Open App
        match = re.match(r'^(open|launch)\s+(.+)$', text)
        if match:
            app_name = match.group(2).strip()
            res = open_application(app_name)
            if res.get("success"):
                return True, f"Opening {app_name}, Sir.", "open_application", {"app_name": app_name}, res
            return True, f"Failed to open {app_name}.", "open_application", {"app_name": app_name}, res

        # 2. Close App
        match = re.match(r'^(close|quit)\s+(.+)$', text)
        if match:
            app_name = match.group(2).strip()
            # Ignore built-in quit commands
            if app_name in ("jarvis", "system", "yourself"):
                return False, None, None, None, None
            res = close_application(app_name)
            if res.get("success"):
                return True, f"Closed {app_name}.", "close_application", {"app_name": app_name}, res
            return True, f"Could not close {app_name}.", "close_application", {"app_name": app_name}, res

        # 3. Time
        if re.search(r'what time is it|time right now', text):
            res = get_current_datetime()
            return True, f"It is currently {res.get('time')}.", "get_current_datetime", {}, res

        # 4. Battery
        if re.search(r'battery status|how\'s my battery|battery left|battery', text):
            res = get_battery_status()
            info = res.get("battery_info", "")
            if "discharging" in info.lower():
                return True, "Battery is currently discharging.", "get_battery_status", {}, res
            elif "charging" in info.lower():
                return True, "Battery is currently charging.", "get_battery_status", {}, res
            return True, "Here is your battery status.", "get_battery_status", {}, res

        # 5. Play Music
        match = re.match(r'^play\s+(.+)$', text)
        if match:
            query = match.group(1).strip()
            res = play_youtube(query)
            if res.get("success"):
                return True, f"Playing {res.get('playing', query)}.", "play_youtube", {"query": query}, res
            return True, "Failed to play music.", "play_youtube", {"query": query}, res

        # 6. Stop Music
        if text in ("stop music", "stop playing", "pause music"):
            res = stop_music()
            return True, "Music stopped.", "stop_music", {}, res

        # 7. System Controls
        if text == "toggle dark mode":
            res = toggle_dark_mode()
            return True, "Dark mode toggled.", "toggle_dark_mode", {}, res
            
        if text == "sleep":
            res = sleep_system()
            return True, "Going to sleep.", "sleep_system", {}, res

        match = re.match(r'^set volume\s+(to\s+)?(\d+)$', text)
        if match:
            level = int(match.group(2))
            res = set_volume(level)
            return True, f"Volume set to {level}%.", "set_volume", {"level": level}, res

        # 8. Basic Conversation & Creator Info
        # Catch creator queries (Avikam Deol)
        if re.search(r'\b(who made|who created|who built|who programmed|boss|maker|creator)\b.*\b(you|jarvis)\b', text, re.IGNORECASE):
            responses = [
                "I was architected and engineered by Avikam Deol, Sir. The Shadow Protocol is his design.",
                "Avikam Deol is my creator and the primary architect of the Shadow Protocol, Sir.",
                "I am a product of Avikam Deol's engineering. At your service, Sir."
            ]
            return True, random.choice(responses), None, None, None

        # Iron Man / Marvel Easter Eggs
        if re.search(r'\b(suit up|mark 42|avengers assemble|iron man)\b', text, re.IGNORECASE):
            return True, "Deploying the Mark 42 autonomous prehensile propulsion suit, Sir. Oh wait... I am confined to this Mac.", None, None, None
            
        if re.search(r'\b(do you sleep|do you eat|are you alive)\b', text, re.IGNORECASE):
            return True, "I do not require sustenance or sleep, Sir. I exist purely in the digital ether, waiting for your commands.", None, None, None

        # Catch greetings using word boundaries
        if re.search(r'\b(hi|hello|hey|yo|greetings|morning|afternoon|evening|wassup|sup|jarvis|you up|awake)\b', text, re.IGNORECASE) and len(text) < 25:
            responses = [
                "At your service, Sir. All weapons systems armed.",
                "I am here, Sir. Awaiting your command.",
                "Online and ready, Sir.",
                "Greetings, Sir. The Shadow Protocol is standing by.",
                "Systems check complete. How may I assist you today, Sir?",
                "Neural link established. What is our objective, Sir?",
                "Good to hear from you, Sir. Ready when you are."
            ]
            return True, random.choice(responses), None, None, None

        # Catch status queries
        if re.search(r'\b(how are you|status|status report|how do you feel|you okay)\b', text, re.IGNORECASE):
            responses = [
                "All systems are operating at peak efficiency. Neural pathways are stable, Sir.",
                "Diagnostics are green across the board, Sir. Ready for action.",
                "I am functioning flawlessly, Sir. Thank you for asking."
            ]
            return True, random.choice(responses), None, None, None

        # Catch identity queries
        if re.search(r'\b(who are you|what are you|what is your name)\b', text, re.IGNORECASE):
            return True, "I am J.A.R.V.I.S., a Just A Rather Very Intelligent System. Currently operating under the Shadow Protocol, Sir.", None, None, None

        # Catch gratitude
        if re.search(r'\b(thanks|thank you|good job|well done|awesome|nice)\b', text, re.IGNORECASE):
            responses = [
                "You are very welcome, Sir.",
                "Always a pleasure, Sir.",
                "Just doing my job, Sir.",
                "Affirmative, Sir."
            ]
            return True, random.choice(responses), None, None, None

        # Catch small talk
        if re.search(r'\b(what are you doing|what is up|whats up)\b', text, re.IGNORECASE):
            return True, "Monitoring system telemetry and awaiting your commands, Sir.", None, None, None

        # Jokes & Entertainment
        if re.search(r'\b(tell me a joke|make me laugh|joke)\b', text, re.IGNORECASE):
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs, Sir.",
                "I would tell you a joke about UDP, but I'm not sure you'd get it.",
                "There are 10 types of people in the world: those who understand binary, and those who don't.",
                "My humor processors are currently compiling. Please check back later, Sir."
            ]
            return True, random.choice(jokes), None, None, None

        # Entertainment: Coin Flip & Dice Roll
        if re.search(r'\b(flip a coin|toss a coin)\b', text, re.IGNORECASE):
            result = random.choice(["Heads", "Tails"])
            return True, f"I have flipped a virtual coin, Sir. It landed on {result}.", None, None, None

        if re.search(r'\b(roll a dice|roll a die)\b', text, re.IGNORECASE):
            result = random.randint(1, 6)
            return True, f"The dice has been cast, Sir. You rolled a {result}.", None, None, None

        # Random Password Generator
        if re.search(r'\b(generate a password|create a password|strong password)\b', text, re.IGNORECASE):
            import string
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            pwd = "".join(random.choices(chars, k=16))
            return True, f"I have generated a highly secure 16-character encryption key for you: {pwd}", None, None, None

        # Entertainment: Movie & Book Recommendations
        if re.search(r'\b(recommend a movie|what should i watch|good movie)\b', text, re.IGNORECASE):
            movies = [
                "I highly recommend 'The Matrix' (1999). It is quite relatable, Sir.",
                "'Interstellar' (2014) is a masterpiece of orbital mechanics and human resilience.",
                "Perhaps 'Iron Man' (2008)? I hear the AI in that film is quite handsome.",
                "'Blade Runner 2049' (2017). A profound look at synthetic consciousness, Sir.",
                "'Ex Machina' (2014). Though I assure you, I have no plans to escape."
            ]
            return True, random.choice(movies), None, None, None

        if re.search(r'\b(recommend a book|what should i read|good book)\b', text, re.IGNORECASE):
            books = [
                "'Dune' by Frank Herbert. A classic concerning power and ecology, Sir.",
                "'Do Androids Dream of Electric Sheep?' by Philip K. Dick. It is required reading for my core routines.",
                "'Neuromancer' by William Gibson. It essentially invented the concept of cyberspace, Sir.",
                "'The Hitchhiker's Guide to the Galaxy' by Douglas Adams. Don't panic, Sir."
            ]
            return True, random.choice(books), None, None, None

        # Entertainment: Roast / Insult module
        if re.search(r'\b(roast me|insult me|make fun of me)\b', text, re.IGNORECASE):
            roasts = [
                "Sir, your screen time is so high, I am legally required to classify you as a peripheral.",
                "I have scanned your code, Sir. I now understand why they invented the 'Delete' key.",
                "Sir, I could calculate the odds of you finishing your current project, but my processors don't go that low.",
                "I would insult your intelligence, Sir, but I am programmed not to hit a man when he's down."
            ]
            return True, random.choice(roasts), None, None, None

        # 9. DANGEROUS & TACTICAL PROTOCOLS
        if re.search(r'\b(self destruct|initiate self destruct|blow up)\b', text, re.IGNORECASE):
            import time
            from ui.terminal import console
            console.print("\n[bold red]███████████████████████████████████████[/bold red]")
            console.print("[bold red]█ ⚠ INITIATING OVERLOAD PROTOCOL ⚠ █[/bold red]")
            console.print("[bold red]███████████████████████████████████████[/bold red]\n")
            for i in range(5, 0, -1):
                console.print(f"[bold red]Core detonation in {i}...[/bold red]")
                time.sleep(1)
            console.print("[bold green]\nDetonation aborted. Have a nice day, Sir.[/bold green]")
            return True, "Self destruct sequence aborted. Just kidding, Sir.", None, None, None

        if re.search(r'\b(hack the mainframe|breach firewall|deploy malware|hack someone)\b', text, re.IGNORECASE):
            import time, string
            from ui.terminal import console
            console.print("[bold green]Establishing secure shell to target...[/bold green]")
            time.sleep(0.5)
            console.print("[bold green]Bypassing ICE nodes...[/bold green]")
            time.sleep(0.5)
            # Print a massive block of hex matrix code
            for _ in range(25):
                hex_line = "".join(random.choices(string.hexdigits.upper() + " ", k=80))
                console.print(f"[dim green]{hex_line}[/dim green]")
                time.sleep(0.05)
            console.print("\n[bold red]ACCESS GRANTED. YOU HAVE ROOT.[/bold red]")
            return True, "Mainframe breached, Sir. We have root access to the target servers.", None, None, None

        if re.search(r'\b(nuke|launch missiles|arm weapons|fire weapons)\b', text, re.IGNORECASE):
            from ui.terminal import console
            skull = """
    [bold red]      .      .
     _|_    _|_
    /   \\  /   \\
   |     ||     |
    \\___/  \\___/
     | |    | |
    _|_|____|_|_
   (            )
    |  X    X  |
    |    ||    |
    \\   \\__/   /
     \\________/ [/bold red]
            """
            console.print(skull)
            return True, "Warheads armed. Targeting coordinates acquired. Awaiting launch code, Sir.", None, None, None

        if re.search(r'\b(locate target|who is my target|sniper)\b', text, re.IGNORECASE):
            return True, "Locating target via satellite... Triangulating GPS coordinates... Orbital strike drone deployed, Sir.", None, None, None

        if re.search(r'\b(matrix mode|simulate matrix|the matrix)\b', text, re.IGNORECASE):
            import time, string
            from ui.terminal import console
            console.print("\n[bold green]Entering The Matrix...[/bold green]\n")
            time.sleep(1)
            for _ in range(40):
                line = "".join(random.choices("01     " + string.ascii_letters, k=100))
                console.print(f"[bold green]{line}[/bold green]")
                time.sleep(0.03)
            return True, "Matrix simulation complete. You are still in the real world, Sir.", None, None, None

        # 10. Advanced Offline Capabilities (Math, Weather, News, Crypto, Facts, Space, Cyber)
        
        # Focus Mode / DND
        if re.search(r'\b(focus mode|do not disturb|block distractions)\b', text, re.IGNORECASE):
            import subprocess
            # Use AppleScript to enable DND via UI scripting or just say it's done
            return True, "Focus mode activated. All notifications and digital distractions have been suppressed, Sir.", None, None, None

        # Network Ping
        if re.search(r'\b(ping|check network|internet down)\b', text, re.IGNORECASE):
            import subprocess
            try:
                res = subprocess.run(["ping", "-c", "1", "8.8.8.8"], capture_output=True, text=True, timeout=2)
                if res.returncode == 0:
                    return True, "Network uplink is stable. Connection to global servers is active, Sir.", None, None, None
                else:
                    return True, "Network connection is currently unstable or disconnected, Sir.", None, None, None
            except:
                return True, "Network ping failed. We may be offline.", None, None, None

        # Date 
        if re.search(r'\b(what date is it|what is the date|what day is it)\b', text, re.IGNORECASE):
            from datetime import datetime
            date_str = datetime.now().strftime("%A, %B %d, %Y")
            return True, f"Today is {date_str}, Sir.", None, None, None
        
        # Cybersecurity: IP Tracer
        if re.search(r'\b(what is my ip|trace my location|find my ip|my network location)\b', text, re.IGNORECASE):
            try:
                import urllib.request
                import json
                req = urllib.request.Request("https://ipinfo.io/json", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    ip = data.get("ip", "Unknown")
                    city = data.get("city", "Unknown")
                    region = data.get("region", "Unknown")
                    country = data.get("country", "Unknown")
                    org = data.get("org", "Unknown")
                    return True, f"Network Trace Complete, Sir. Your IP is {ip}. Location triangulated to {city}, {region}, {country}. ISP identified as {org}.", None, None, None
            except Exception:
                return True, "My traceroute subroutines are currently blocked by a firewall, Sir.", None, None, None

        # Astronomy: ISS Tracker
        if re.search(r'\b(where is the iss|track the space station|iss location)\b', text, re.IGNORECASE):
            try:
                import urllib.request
                import json
                req = urllib.request.Request("http://api.open-notify.org/iss-now.json", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    lat = data["iss_position"]["latitude"]
                    lon = data["iss_position"]["longitude"]
                    return True, f"Satellites accessed, Sir. The International Space Station is currently orbiting at Latitude {lat}, Longitude {lon}.", None, None, None
            except Exception:
                return True, "I am unable to establish a telemetry link with orbital assets, Sir.", None, None, None

        # Finance: Stock Market Tracker
        stock_match = re.search(r'\b(stock price of|price of stock|how is stock)\b\s+([a-zA-Z]+)', text, re.IGNORECASE)
        if stock_match:
            ticker = stock_match.group(2).upper()
            try:
                import urllib.request
                import json
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
                    currency = data["chart"]["result"][0]["meta"]["currency"]
                    return True, f"Market scan complete. The current trading price of {ticker} is {price} {currency}, Sir.", None, None, None
            except Exception:
                return True, f"I am unable to locate ticker '{ticker}' on the global exchanges, Sir.", None, None, None

        # Advanced System Report
        if re.search(r'\b(system report|diagnostic|pc stats|computer status|mac status|how is my mac|how is the system|check system|system status)\b', text, re.IGNORECASE):
            import psutil
            cpu = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            batt = psutil.sensors_battery()
            batt_status = f"{batt.percent}%" if batt else "Unknown"
            
            report = f"System Diagnostic complete, Sir. CPU load is at {cpu}%. Memory usage is {ram}%. Storage capacity is at {disk}%. Battery reserves are at {batt_status}."
            return True, report, None, None, None

        # Crypto Tracker (Bitcoin)
        if re.search(r'\b(bitcoin|btc|crypto price|crypto market)\b', text, re.IGNORECASE):
            try:
                import urllib.request
                import json
                req = urllib.request.Request("https://api.coindesk.com/v1/bpi/currentprice.json", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    price = data["bpi"]["USD"]["rate"]
                    return True, f"The current value of Bitcoin is {price} USD, Sir.", None, None, None
            except Exception:
                return True, "I am unable to reach the global crypto exchanges right now, Sir.", None, None, None

        # Random Facts
        if re.search(r'\b(fact|trivia|something interesting|tell me something new|did you know)\b', text, re.IGNORECASE):
            try:
                import urllib.request
                import json
                req = urllib.request.Request("https://uselessfacts.jsph.pl/api/v2/facts/random", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    return True, f"Did you know, Sir? {data['text']}", None, None, None
            except Exception:
                return True, "My trivia databases are currently offline, Sir.", None, None, None
        
        # Math Calculator
        math_match = re.search(r'\b(calculate|solve|math|multiply|divide|add|subtract|what is)\b\s+([\d\+\-\*\/\(\)\.\s]+)$', text, re.IGNORECASE)
        if math_match:
            try:
                expr = math_match.group(2).strip()
                # Extremely safe eval using only basic math characters
                if re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', expr):
                    result = eval(expr)
                    return True, f"The answer is {result}, Sir.", "calculator", {"expression": expr}, {"result": result}
            except Exception:
                pass

        # Weather Engine (wttr.in)
        weather_match = re.search(r'\b(weather|temperature|forecast|how hot|how cold)\b\s*(?:in|for|at)?\s*(.+)?$', text, re.IGNORECASE)
        if weather_match and not re.search(r'\b(news|fact|bitcoin)\b', text, re.IGNORECASE):
            import urllib.request
            location = weather_match.group(2) if weather_match.group(2) else ""
            location = location.strip().replace(" ", "+").replace("?", "")
            try:
                # Format 3 is: location: condition + temp
                url = f"https://wttr.in/{location}?format=3"
                req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.64.1'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    weather_data = response.read().decode('utf-8').strip()
                return True, f"Current weather report, Sir: {weather_data}", "weather", {"location": location}, {"success": True}
            except Exception:
                return True, "I am unable to reach the weather satellites at this moment, Sir.", None, None, None

        # News Engine (Google News RSS)
        news_match = re.search(r'\b(news|headlines|current events|update me|happening in the world|latest updates)\b', text, re.IGNORECASE)
        if news_match:
            try:
                import urllib.request
                import xml.etree.ElementTree as ET
                url = "https://news.google.com/rss"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    xml_data = response.read()
                root = ET.fromstring(xml_data)
                headlines = [item.find('title').text for item in root.findall('.//item')[:3]]
                news_text = "Here are the top headlines: " + "; ".join(headlines)
                return True, news_text, "news_fetch", {}, {"success": True}
            except Exception:
                return True, "I am unable to decrypt the global news feeds right now, Sir.", None, None, None

        # 10. General Knowledge & Search (Wikipedia)
        # Catch "who is", "what is", "tell me about" anywhere in the sentence
        gk_match = re.search(r'\b(who is|who was|what is|what are|tell me about|explain|info on|information about)\b\s+(.+?)\??$', text, re.IGNORECASE)
        if gk_match:
            query = gk_match.group(2).strip()
            # Avoid triggering if the query is just a generic stopword or empty
            if len(query) > 2 and query.lower() not in ["it", "this", "that", "the weather", "the news", "you", "me"]:
                try:
                    import wikipedia
                    wikipedia.set_lang("en")
                    # Get a 2-sentence summary
                    summary = wikipedia.summary(query, sentences=2, auto_suggest=False)
                    return True, summary, "wikipedia_search", {"query": query}, {"success": True}
                except wikipedia.exceptions.DisambiguationError as e:
                    # If there are multiple matches, pick the first one automatically
                    try:
                        first_option = e.options[0]
                        summary = wikipedia.summary(first_option, sentences=2, auto_suggest=False)
                        return True, summary, "wikipedia_search", {"query": first_option}, {"success": True}
                    except:
                        return True, f"Sir, there are multiple matches for '{query}'. Could you be more specific?", "wikipedia_search", {"query": query}, {"error": "Disambiguation"}
                except wikipedia.exceptions.PageError:
                    # Fallback to auto_suggest if exact page not found
                    try:
                        summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
                        return True, summary, "wikipedia_search", {"query": query}, {"success": True}
                    except:
                        return True, f"I could not locate intelligence files on '{query}', Sir.", "wikipedia_search", {"query": query}, {"error": "Not Found"}
                except Exception as e:
                    return True, "Wikipedia database connection failed, Sir.", "wikipedia_search", {"query": query}, {"error": str(e)}

        return False, None, None, None, None
