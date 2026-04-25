# FULL CODER V6 - AlpAy AI
# ChatGPT tarzı internet araştıran + kod yazan sistem

import json
import os
import uuid
import requests
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8000))

API_KEYS_FILE = "api_keys.json"

# =========================
# API KEY SYSTEM
# =========================

def load_keys():
    if not os.path.exists(API_KEYS_FILE):
        return {}

    with open(API_KEYS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_keys(data):
    with open(API_KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def create_key(username="user"):
    data = load_keys()

    key = str(uuid.uuid4())

    data[key] = {
        "user": username,
        "usage": 0
    }

    save_keys(data)
    return key

def check_key(key):
    data = load_keys()
    return data.get(key)

def add_usage(key):
    data = load_keys()

    if key in data:
        data[key]["usage"] += 1
        save_keys(data)

# =========================
# INTERNET SEARCH
# =========================

def search_web(query):
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1
        }

        res = requests.get(url, params=params).json()

        if res.get("AbstractText"):
            return res["AbstractText"]

        return "İnternette net sonuç bulunamadı."

    except:
        return "Arama hatası oluştu."

# =========================
# CODE WRITER AI
# =========================

def write_code(prompt):
    text = prompt.lower()

    if "site" in text:
        return """
<!DOCTYPE html>
<html>
<head>
<title>Web Site</title>
</head>
<body>
<h1>Merhaba Dünya</h1>
</body>
</html>
"""

    elif "python" in text:
        return """
print("Merhaba Dünya")
"""

    elif "hesap makinesi" in text:
        return """
num1 = float(input("1. sayı: "))
num2 = float(input("2. sayı: "))
print(num1 + num2)
"""

    return f"{prompt} için kod araştırıldı. Yakında gelişmiş kod sistemi eklenecek."

# =========================
# CHAT AI
# =========================

def ai_reply(message):
    text = message.lower()

    if "merhaba" in text:
        return "Merhaba 😎"

    if "nasılsın" in text:
        return "Harikayım 🚀"

    if "kod" in text or "yaz" in text:
        return write_code(message)

    if "kimdir" in text or "nedir" in text or "araştır" in text:
        return search_web(message)

    return "Bunu anlayamadım."

# =========================
# SERVER
# =========================

class Handler(BaseHTTPRequestHandler):

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode()

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):

        if self.path == "/":
            self.send_json(200, {"status": "FULL CODER V6 aktif 🚀"})
            return

        if self.path == "/api/create-key":
            key = create_key("web_user")
            self.send_json(200, {"api_key": key})
            return

        self.send_json(404, {"error": "Not found"})

    def do_POST(self):

        content_length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(content_length)

        try:
            data = json.loads(raw.decode())
        except:
            data = {}

        if self.path == "/api/create-key":
            username = data.get("username", "user")
            key = create_key(username)
            self.send_json(200, {"api_key": key})
            return

        auth = self.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            self.send_json(401, {"error": "API key gerekli"})
            return

        key = auth.split(" ")[1]

        user = check_key(key)

        if not user:
            self.send_json(403, {"error": "Geçersiz key"})
            return

        if self.path == "/api/chat":

            msg = data.get("message", "")

            add_usage(key)

            reply = ai_reply(msg)

            self.send_json(200, {
                "reply": reply
            })
            return

        self.send_json(404, {"error": "Not found"})

# =========================
# START
# =========================

def run():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print("FULL CODER V6 çalışıyor 🚀")
    server.serve_forever()

if __name__ == "__main__":
    run()
