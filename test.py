import time
import os
import re
import requests
import pyautogui
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import sys

# Initialize pyautogui with safe defaults
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.15  # Slightly longer pause for reliability

# Global variables
flag_FKDR = False
flag_lvl = False
flag_nick = False
FKDR = 0
lvl = 0
nick = 0

# Cache for API responses
player_cache = {}
CACHE_EXPIRY = 300  # 5 minutes cache

def extractign(line):
    names=[]
    p_index = sys.argv.index('-p')
    # Get all arguments after -p until next flag (starts with -)
    names = [arg for arg in sys.argv[p_index+1:] if not arg.startswith('-')]
    return names


def type_in_chat(message):
    """Safely types a message into Minecraft chat"""
    try:
        # Press 't' to open chat
        pyautogui.press('t')
        time.sleep(0.1)
        
        # Type the message
        pyautogui.write(message, interval=0)
        # Press enter and wait
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.4)  # Prevent chat spamming
    except Exception as e:
        print(f"[Error] Couldn't type in chat: {str(e)}")

def getPlayerName(line):
    """Extracts player names from chat line"""
    if "[CHAT]" not in line:
        return None
    
    try:
        chat_content = line.split("[CHAT]")[1].strip()
        if ',' not in chat_content:
            return None
            
        # Clean and validate player names
        players = []
        for player in chat_content.split(','):
            player = player.strip()
            if re.match(r'^[a-zA-Z0-9_]{1,16}$', player):  # Minecraft username validation
                players.append(player)
        return players if players else None
    except:
        return None

def extractFkdr(text, word):
    """Extracts numerical value after a command"""
    match = re.search(rf"{word}\s+([0-9]+(?:\.[0-9]+)?)", text)
    return float(match.group(1)) if match else None

@lru_cache(maxsize=100)
def get_lvl(ign):
    """Gets player level with caching"""
    try:
        cache_key = f"level_{ign}"
        if cache_key in player_cache and time.time() - player_cache[cache_key]['timestamp'] < CACHE_EXPIRY:
            return player_cache[cache_key]['data']
        
        response = requests.get(f"https://stats.pika-network.net/api/profile/{ign}", timeout=3)
        response.raise_for_status()
        data = response.json()

        # Find games rank
        rank = next((r["displayName"] for r in data.get("ranks", []) 
                   if r.get("server") == "games"), "?")
        
        # Get level
        level = str(data.get("rank", {}).get("level", "?"))
        
        result = f"{rank} {level}"
        player_cache[cache_key] = {'data': result, 'timestamp': time.time()}
        return result
        
    except requests.exceptions.RequestException:
        return "? ?"
    except Exception:
        return "? ?"

@lru_cache(maxsize=100)
def get_nick(ign):
    """Checks if player is nicked"""
    cache_key = f"nick_{ign}"
    if cache_key in player_cache and time.time() - player_cache[cache_key]['timestamp'] < CACHE_EXPIRY:
        return player_cache[cache_key]['data']
    
    try:
        response = requests.get(
            f"https://stats.pika-network.net/api/profile/{ign}/leaderboard",
            params={"type": "bedwars", "interval": "monthly", "mode": "ALL_MODES"},
            timeout=3
        )
        result = response.status_code == 400  # True if nicked
        player_cache[cache_key] = {'data': result, 'timestamp': time.time()}
        return result
    except:
        return False


@lru_cache(maxsize=100)
def get_bedwars_fkdr(ign):
    """Optimized FKDR calculation with caching"""
    cache_key = f"fkdr_{ign}"
    if cache_key in player_cache and time.time() - player_cache[cache_key]['timestamp'] < CACHE_EXPIRY:
        return player_cache[cache_key]['data']
    
    try:
        response = requests.get(
            f"https://stats.pika-network.net/api/profile/{ign}/leaderboard?type=bedwars&interval=monthly&mode=ALL_MODES",
            timeout=3
        )
        response.raise_for_status()
        data = response.json()

        def safe_extract(key):
            try:
                return int(data[key]["entries"][0]["value"])
            except:
                return 0

        final_kills = safe_extract("Final kills")
        final_deaths = safe_extract("Final deaths")

        fkdr = round(final_kills / final_deaths, 2) if final_deaths > 0 else final_kills
        player_cache[cache_key] = {'data': fkdr, 'timestamp': time.time()}
        return fkdr
    except:
        return 0

def process_player(ign):
    """Processes a single player's stats based on active flags"""
    messages = []
    
    if flag_FKDR:
        global FKDR
        global lvl
        fkdr = get_bedwars_fkdr(ign)
        if fkdr >= FKDR:
            messages.append(f"{ign}: FKDR {fkdr}")
    
    if flag_lvl:
        level_info = get_lvl(ign)
        rank, level = level_info.split()
        if level.isdigit() and int(level) >= lvl:
            messages.append(f"{ign}: {rank} L{level}")
    
    if flag_nick and get_nick(ign):
        messages.append(f"{ign}: NICKED")
    # Send all messages for this player
    for msg in messages:
        type_in_chat(msg)

def follow_changes(file_path):
    """Monitors the log file for changes"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        file.seek(0, os.SEEK_END)
        
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                continue
            time.sleep(0.1)
            process_line(line.strip())

def process_line(line):
    """Processes a single log line"""
    global flag_FKDR, flag_lvl, flag_nick, FKDR, lvl
    
    # Check for commands
    if "-help" in line:
        show_help()
        return
        
    if "-toggle fkdr" in line:
        FKDR = extractFkdr(line, "-toggle fkdr") or 0
        flag_FKDR = True
        type_in_chat(f"Tracking FKDR ≥ {FKDR}")
        return
        
    if "-toggle lvl" in line:
        lvl = extractFkdr(line, "-toggle lvl") or 0
        flag_lvl = True
        type_in_chat(f"Tracking Level ≥ {lvl}")
        return
        
    if "-toggle nick" in line:
        flag_nick = True
        type_in_chat("Tracking nicked players")
        return
    if "-fold" in line:
        fold_mode = extractFkdr(line,"-fold") or 0
        type_in_chat("/leave")
        time.sleep(1.5)
        type_in_chat("/p warp")
        type_in_chat(f"/bedwars-{int(fold_mode)}")
        return
    if "-bw" in line:
        mode = extractFkdr(line,"-bw") or 0
        type_in_chat(f"/bedwars-{int(mode)}")
        return
    if "-p" in line:
        names = extractign(line)
        for name in names:
            type_in_chat(f"/p inv {name}")
            time.sleep(0)
        return
    
    
    # Process player names if any flag is active
    if flag_FKDR or flag_lvl or flag_nick:
        players = getPlayerName(line)
        if players:
            with ThreadPoolExecutor(max_workers=3) as executor:
                executor.map(process_player, players)

def show_help():
    """Displays help messages"""
    help_messages = [
        "Overlay Commands:",
        "-toggle fkdr [number] - Track high FKDR",
        "-toggle lvl [number] - Track high levels",
        "-toggle nick - Track nicked players"
    ]
    for msg in help_messages:
        type_in_chat(msg)
        time.sleep(0.3)

def main():
    time.sleep(3)
    """Main entry point"""
    type_in_chat("Stats overlay activated! Type -help for commands")
    
    # Default log path - change if needed
    log_path = os.path.expanduser("~/.minecraft/logs/blclient/minecraft/latest.log")
    #log_path = os.path.expanduser("/home/kali/.local/share/.minecraft/logs/latest.log")
    
    if not os.path.exists(log_path):
        type_in_chat("Error: Couldn't find Minecraft logs!")
        return
    
    follow_changes(log_path)

if __name__ == "__main__":
    main()
