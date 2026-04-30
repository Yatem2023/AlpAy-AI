import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import uuid
import os
import requests
import datetime

# ================== CONFIG ==================
API_KEYS_FILE = "api_keys.json"
RATE_LIMIT = 200

# ================== FILE ==================

def load_api_keys():
    if not os.path.exists(API_KEYS_FILE):
        return {}
    with open(API_KEYS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_api_keys(data):
    with open(API_KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ================== SELF HEALING ==================

def check_api_key(api_key):
    data = load_api_keys()

    if api_key not in data:
        print("🔥 Yeni key oluşturuldu:", api_key)
        data[api_key] = {
            "user": "auto_user",
            "usage": 0,
            "plan": "free"
        }
        save_api_keys(data)

    return data[api_key]

def increment_usage(api_key):
    data = load_api_keys()
    if api_key in data:
        data[api_key]["usage"] += 1
        save_api_keys(data)

# ================== AI CORE ==================

def wiki_search(query):
    try:
        url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{query}"
        r = requests.get(url).json()
        return r.get("extract", "Bilgi bulunamadı.")
    except:
        return "Wiki hatası."

def internet_search(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        data = requests.get(url).json()
        return data.get("AbstractText", "Sonuç bulunamadı.")
    except:
        return "İnternet hatası."

def generate_code(prompt):
    text = prompt.lower()

    if "hesap makinası" in text:
        return """# Python hesap makinesi
def hesapla():
    a = float(input("Sayı 1: "))
    op = input("İşlem (+ - * /): ")
    b = float(input("Sayı 2: "))

    if op == "+":
        print(a + b)
    elif op == "-":
        print(a - b)
    elif op == "*":
        print(a * b)
    elif op == "/":
        print(a / b)

hesapla()
"""

    if "website" in text or "site" in text:
        return """<!DOCTYPE html>
<html>
<head><title>Site</title></head>
<body>
<h1>Merhaba Dünya</h1>
</body>
</html>
"""

    return "# Kod üretiliyor..."

# ================== MAIN AI ==================

def generate_reply(message):
    msg = message.lower()

    # selam
    if "merhaba" in msg:
        return "Merhaba! 😎"

    # saat
    if "saat" in msg:
        return str(datetime.datetime.now())

    # kod
    if "kod" in msg or "yaz" in msg:
        return generate_code(message)

    # wiki soruları
    if any(x in msg for x in ["nedir", "kimdir", "ne", "hangi"]):
        return wiki_search(msg.replace("nedir","").replace("kimdir",""))

    # internet
    if "ara" in msg or "bul" in msg:
        return internet_search(msg)

    return "Bunu geliştiriyorum 😎"

# ================== API ==================

class Handler(BaseHTTPRequestHandler):

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.end_headers()

        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.send_json(200, {"status": "AlpAy AI V13 çalışıyor 🚀"})

        elif self.path == "/api/create-key":
            key = str(uuid.uuid4())
            check_api_key(key)
            self.send_json(200, {"api_key": key})

        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):

        # AUTH
        auth = self.headers.get("Authorization")

        if auth and auth.startswith("Bearer "):
            api_key = auth.split(" ")[1]
        else:
            api_key = str(uuid.uuid4())

        user = check_api_key(api_key)

        if user["usage"] >= RATE_LIMIT:
            self.send_json(429, {"error": "rate limit"})
            return

        increment_usage(api_key)

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body.decode("utf-8"))
        except:
            self.send_json(400, {"error": "bad json"})
            return

        if self.path == "/api/chat":
            message = data.get("message", "")
            reply = generate_reply(message)

            self.send_json(200, {
                "reply": reply,
                "api_key": api_key
            })
            return

        self.send_json(404, {"error": "not found"})

# ================== RUN ==================

def run():
    server = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)
    print("🚀 AlpAy AI V13 çalışıyor")
    server.serve_forever()

if __name__ == "__main__":
    run()
