import json
import os
import uuid
import re
import wikipedia
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# =========================
# SETTINGS
# =========================
PORT = 8000
DATA_FILE = "users.json"
LIMIT = 250
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
        "plan": "free",
        "memory": [],
        "last_topic": ""
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
    user["memory"] = user["memory"][-15:]

# =========================
# HELPERS
# =========================
def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def contains_any(text, words):
    return any(w in text for w in words)

# =========================
# WIKI SYSTEM
# =========================
def wiki_ai(query):
    try:
        result = wikipedia.summary(query, sentences=3)
        return result
    except:
        return "Bu konu hakkında bilgi bulunamadı."

# =========================
# IMAGE SYSTEM
# =========================
def image_ai(prompt):
    return f"🎨 Görsel hazırlanıyor: {prompt}"

# =========================
# CODER AI
# =========================
def coder_ai(prompt):
    text = prompt.lower()

    if "hesap" in text:
        return """
# Hesap Makinesi

a = float(input("1. sayı: "))
islem = input("İşlem (+,-,*,/): ")
b = float(input("2. sayı: "))

if islem == "+":
    print(a+b)
elif islem == "-":
    print(a-b)
elif islem == "*":
    print(a*b)
elif islem == "/":
    print(a/b)
"""

    if "site" in text:
        return """
<!DOCTYPE html>
<html>
<head>
<title>Web Site</title>
</head>
<body>
<h1>Merhaba Dünya</h1>
<p>V10 AI Site</p>
</body>
</html>
"""

    if "login" in text:
        return """
<form>
<input placeholder='Kullanıcı adı'>
<input type='password' placeholder='Şifre'>
<button>Giriş</button>
</form>
"""

    if "discord" in text or "bot" in text:
        return """
import discord

client = discord.Client()

@client.event
async def on_ready():
    print("Bot aktif")

client.run("TOKEN")
"""

    return f"# {prompt}\nprint('Kod oluşturuldu')"

# =========================
# SMART CHAT
# =========================
def normal_chat(msg):
    t = msg.lower()

    if "merhaba" in t:
        return "Merhaba 👋"

    if "nasılsın" in t:
        return "Harikayım 😎 Sen nasılsın?"

    if "teşekkür" in t:
        return "Rica ederim 🔥"

    if "bye" in t or "görüşürüz" in t:
        return "Görüşürüz 👋"

    return "Bunu geliştiriyorum 😎"

# =========================
# MAIN AI
# =========================
def ai_reply(msg, user):
    text = clean_text(msg.lower())

    remember(user, msg)

    # Hafıza sor
    if "hafıza" in text:
        return "Son mesajların: " + ", ".join(user["memory"][-5:])

    # Görsel
    if contains_any(text, [
        "logo", "wallpaper", "afiş",
        "tasarla", "görsel"
    ]):
        user["last_topic"] = "image"
        return image_ai(msg)

    # Kod
    if contains_any(text, [
        "kod", "python", "html", "css",
        "javascript", "js", "bot",
        "site", "uygulama", "hesap"
    ]):
        user["last_topic"] = "code"
        return coder_ai(msg)

    # Wiki
    if contains_any(text, [
        "nedir", "kimdir", "nerede",
        "nasıl", "ne zaman", "hangi"
    ]):
        q = text.replace("nedir", "") \
                .replace("kimdir", "") \
                .replace("nerede", "") \
                .replace("nasıl", "") \
                .replace("ne zaman", "") \
                .replace("hangi", "") \
                .strip()

        user["last_topic"] = q
        return wiki_ai(q)

    # Devam et sistemi
    if text == "devam et":
        if user["last_topic"] == "code":
            return "Kod geliştiriliyor 🔥"

        if user["last_topic"] == "image":
            return "Yeni tasarım hazırlanıyor 🎨"

        if user["last_topic"]:
            return wiki_ai(user["last_topic"])

    return normal_chat(msg)

# =========================
# SERVER
# =========================
class Handler(BaseHTTPRequestHandler):

    def send_json(self, code, data):
        body = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(code)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.end_headers()

    def do_GET(self):

        if self.path == "/":
            self.send_json(200, {
                "status": "V10 ACTIVE 🔥"
            })

        elif self.path == "/api/create-key":
            key = create_key("web_user")
            self.send_json(200, {
                "api_key": key
            })

        else:
            self.send_json(404, {
                "error": "not found"
            })

    def do_POST(self):

        auth = self.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            self.send_json(401, {
                "error": "API key gerekli"
            })
            return

        key = auth.split(" ")[1]
        user = get_user(key)

        if not user:
            self.send_json(403, {
                "error": "Geçersiz key"
            })
            return

        if user["usage"] >= LIMIT:
            self.send_json(429, {
                "error": "Limit doldu"
            })
            return

        user["usage"] += 1

        if self.path == "/api/chat":

            length = int(
                self.headers.get("Content-Length", 0)
            )

            raw = self.rfile.read(length)

            try:
                data = json.loads(raw.decode("utf-8"))
                msg = data.get("message", "")
            except:
                msg = ""

            reply = ai_reply(msg, user)
            save_user(key, user)

            self.send_json(200, {
                "reply": reply,
                "usage": user["usage"],
                "plan": user["plan"]
            })
            return

        self.send_json(404, {
            "error": "not found"
        })

# =========================
# RUN
# =========================
def run():
    server = ThreadingHTTPServer(
        ("0.0.0.0", PORT),
        Handler
    )

    print("V10 BACKEND ACTIVE 🔥")
    server.serve_forever()

if __name__ == "__main__":
    run()
