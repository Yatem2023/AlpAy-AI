import json
import os
import uuid
import requests
import wikipedia
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# =========================
# SETTINGS
# =========================
PORT = 8000
DATA_FILE = "users.json"
LIMIT = 100
wikipedia.set_lang("tr")

# =========================
# DATABASE
# =========================
def load_db():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# =========================
# USER SYSTEM
# =========================
def create_key(username="user"):
    db = load_db()
    key = str(uuid.uuid4())

    db[key] = {
        "user": username,
        "usage": 0,
        "memory": [],
        "plan": "free"
    }

    save_db(db)
    return key

def get_user(key):
    return load_db().get(key)

def save_user(key, user):
    db = load_db()
    db[key] = user
    save_db(db)

# =========================
# MEMORY
# =========================
def remember(user, text):
    user["memory"].append(text)
    user["memory"] = user["memory"][-10:]

# =========================
# WIKI AI
# =========================
def wiki_ai(query):
    try:
        return wikipedia.summary(query, sentences=3)
    except:
        return "Bilgi bulunamadı."

# =========================
# IMAGE AI
# =========================
def image_ai(prompt):
    return f"🎨 Görsel hazırlanıyor: {prompt}"

# =========================
# CODER AI
# =========================
def coder_ai(prompt):
    t = prompt.lower()

    if "hesap" in t:
        return '''
# Hesap Makinası

a = float(input("1. sayı: "))
op = input("İşlem (+,-,*,/): ")
b = float(input("2. sayı: "))

if op == "+":
    print(a+b)
elif op == "-":
    print(a-b)
elif op == "*":
    print(a*b)
elif op == "/":
    print(a/b)
'''

    if "site" in t:
        return '''
<!DOCTYPE html>
<html>
<head><title>Site</title></head>
<body>
<h1>Merhaba Dünya</h1>
</body>
</html>
'''

    if "discord" in t or "bot" in t:
        return '''
import discord

client = discord.Client()

@client.event
async def on_ready():
    print("Bot aktif")

client.run("TOKEN")
'''

    return f"# {prompt}\nprint('Kod hazır')"

# =========================
# MAIN AI
# =========================
def ai_reply(msg, user):
    text = msg.lower()

    remember(user, msg)

    if "merhaba" in text:
        return "Merhaba 👋"

    if "beni hatırla" in text:
        return "Seni hafızama aldım 😎"

    if "hafıza" in text:
        return "Son mesajların: " + ", ".join(user["memory"][-5:])

    if any(x in text for x in [
        "nedir","kimdir","nerede","nasıl","ne zaman"
    ]):
        q = text.replace("nedir","").replace("kimdir","") \
                .replace("nerede","").replace("nasıl","") \
                .replace("ne zaman","").strip()
        return wiki_ai(q)

    if any(x in text for x in [
        "logo","wallpaper","tasarla","afiş","görsel"
    ]):
        return image_ai(msg)

    if any(x in text for x in [
        "kod","python","yaz","oluştur","yap",
        "hesap","site","bot","discord","html"
    ]):
        return coder_ai(msg)

    return "Bunu geliştiriyorum 😎"

# =========================
# SERVER
# =========================
class Handler(BaseHTTPRequestHandler):

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode()

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):

        if self.path == "/":
            self.send_json(200, {"status": "V9 ULTRA ACTIVE 🔥"})

        elif self.path == "/api/create-key":
            key = create_key("web_user")
            self.send_json(200, {"api_key": key})

        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):

        auth = self.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            self.send_json(401, {"error": "API key gerekli"})
            return

        key = auth.split(" ")[1]
        user = get_user(key)

        if not user:
            self.send_json(403, {"error": "Geçersiz key"})
            return

        if user["usage"] >= LIMIT:
            self.send_json(429, {"error": "Limit doldu"})
            return

        user["usage"] += 1

        if self.path == "/api/chat":

            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)

            try:
                data = json.loads(raw.decode())
                msg = data["message"]
            except:
                msg = ""

            reply = ai_reply(msg, user)
            save_user(key, user)

            self.send_json(200, {
                "reply": reply,
                "usage": user["usage"]
            })
            return

        self.send_json(404, {"error": "not found"})

# =========================
# RUN
# =========================
def run():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print("V9 FULL BACKEND RUNNING 🔥")
    server.serve_forever()

if __name__ == "__main__":
    run()
