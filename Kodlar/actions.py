import os, datetime, requests, re
from app_discovery import discover_apps

APPS = discover_apps()

def open_chrome():
    os.startfile("chrome")

def open_vscode():
    os.startfile(r"C:\Program Files\Microsoft VS Code\Code.exe")

def open_notepad():
    os.startfile("notepad")

def open_app_by_name(text):
    name = text.replace(" aç", "").lower()
    if name in APPS:
        os.startfile(APPS[name])
        return True
    return False

def get_time():
    return datetime.datetime.now().strftime("%H:%M")

def extract_city(text):
    match = re.search(r"(\w+)'?da|\b(\w+)'?de", text)
    return match.group(1) if match else "istanbul"

def get_weather(text, mode):
    city = extract_city(text)
    try:
        url = f"https://wttr.in/{city}?format=3" if mode=="today" else f"https://wttr.in/{city}?format=4"
        return requests.get(url, timeout=5).text
    except:
        return "Hava durumu alınamadı."
