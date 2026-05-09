import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import uuid
import os
import requests
import datetime
import re
import math

from knowledge import search_knowledge

API_KEYS_FILE = "api_keys.json"
RATE_LIMIT = 200


# ================= API =================

def load_api_keys():
    if not os.path.exists(API_KEYS_FILE):
        return {}
    with open(API_KEYS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_api_keys(data):
    with open(API_KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def check_api_key(api_key):
    data = load_api_keys()

    if api_key not in data:
        data[api_key] = {
            "user": "auto",
            "usage": 0
        }
        save_api_keys(data)

    return data[api_key]


def increment_usage(api_key):
    data = load_api_keys()
    if api_key in data:
        data[api_key]["usage"] += 1
        save_api_keys(data)


# ================= AI CORE =================

def calculate(expr):
    try:
        allowed = {
            "__builtins__": None,
            "sqrt": math.sqrt,
            "pow": pow,
            "abs": abs,
            "round": round
        }
        result = eval(expr, allowed)
        return str(result)
    except:
        return None


def chat_reply(msg):
    if any(x in msg for x in ["nasılsın", "iyi misin"]):
        return "İyiyim 😎 sen nasılsın?"

    if "adın ne" in msg:
        return "Ben AlpAy AI 😎"

    if "ne yapıyorsun" in msg:
        return "Seninle sohbet ediyorum 🚀"

    if "teşekkür" in msg:
        return "Ne demek 😎"

    if "selam" in msg or "merhaba" in msg:
        return "Selam 😎"

    return None


def generate_code(prompt):
    text = prompt.lower()

    if "hesap" in text:
        return """# Hesap Makinesi
def hesapla():
    a = float(input("Sayı1: "))
    op = input("İşlem (+ - * /): ")
    b = float(input("Sayı2: "))
    if op == "+": print(a + b)
    elif op == "-": print(a - b)
    elif op == "*": print(a * b)
    elif op == "/": print(a / b)
hesapla()
"""

    if "site" in text:
        return """<!DOCTYPE html>
<html>
<head><title>Site</title></head>
<body>
<h1>Merhaba Dünya</h1>
</body>
</html>
"""

    return "# Kod oluşturulamadı"


def internet_search(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        data = requests.get(url).json()
        return data.get("AbstractText", None)
    except:
        return None


# 🔥 ANA AI
def generate_reply(message):
    msg = message.lower().strip()

    # 💬 sohbet
    chat = chat_reply(msg)
    if chat:
        return chat

    # 🧮 matematik (direkt)
    if re.match(r"^[0-9\.\+\-\*\/\(\) ]+$", msg):
        calc = calculate(msg)
        if calc:
            return "Sonuç: " + calc

    # 🧮 "hesapla 2+2"
    if msg.startswith("hesapla "):
        expr = msg.replace("hesapla ", "")
        calc = calculate(expr)
        if calc:
            return "Sonuç: " + calc

    # 💻 kod
    if any(x in msg for x in ["kod", "yaz", "site", "program", "uygulama"]):
        return generate_code(message)

    # 📚 wiki
    if any(x in msg for x in ["nedir", "kimdir", "ne"]):
        clean = msg.replace("nedir", "").replace("kimdir", "").replace("ne", "").strip()
        wiki = search_knowledge(clean)
        if wiki:
            return wiki

    # 🌐 internet
    net = internet_search(msg)
    if net:
        return net

    # 🧠 fallback
    return "Bunu henüz bilmiyorum ama öğreniyorum 😎"


# ================= SERVER =================

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
            self.send_json(200, {"status": "AI çalışıyor 🚀"})
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        auth = self.headers.get("Authorization")

        if auth and auth.startswith("Bearer "):
            api_key = auth.split(" ")[1]
        else:
            api_key = str(uuid.uuid4())

        user = check_api_key(api_key)

        if user["usage"] >= RATE_LIMIT:
            self.send_json(429, {"error": "limit"})
            return

        increment_usage(api_key)

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body.decode("utf-8"))
        except:
            self.send_json(400, {"error": "json"})
            return

        if self.path == "/api/chat":
            msg = data.get("message", "")
            reply = generate_reply(msg)

            self.send_json(200, {
                "reply": reply,
                "key": api_key
            })
            return

        self.send_json(404, {"error": "not found"})


# ================= RUN =================

def run():
    port = int(os.environ.get("PORT", 8000))  # 🔥 render fix
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"🚀 AI hazır | Port: {port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
