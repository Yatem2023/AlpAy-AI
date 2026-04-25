import json
import os
import uuid
import wikipedia
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ==========================
# SETTINGS
# ==========================
DATA_FILE = "api_keys.json"
LIMIT = 100

wikipedia.set_lang("tr")

# ==========================
# DATABASE
# ==========================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ==========================
# USER SYSTEM
# ==========================
def create_key(username="user"):
    data = load_data()

    key = str(uuid.uuid4())

    data[key] = {
        "user": username,
        "usage": 0,
        "plan": "free"
    }

    save_data(data)
    return key

def get_user(key):
    data = load_data()
    return data.get(key)

def update_user(key, user):
    data = load_data()
    data[key] = user
    save_data(data)

# ==========================
# WIKI AI
# ==========================
def wiki_ai(q):
    try:
        return wikipedia.summary(q, sentences=3)
    except:
        return "Bilgi bulunamadı."

# ==========================
# SMART CODER V8
# ==========================
def coder_ai(prompt):
    text = prompt.lower()

    if "hesap" in text:
        return '''
# Hesap Makinası

s1 = float(input("1. sayı: "))
islem = input("İşlem (+ - * /): ")
s2 = float(input("2. sayı: "))

if islem == "+":
    print(s1 + s2)
elif islem == "-":
    print(s1 - s2)
elif islem == "*":
    print(s1 * s2)
elif islem == "/":
    print(s1 / s2)
'''

    elif "site" in text or "html" in text:
        return '''
<!DOCTYPE html>
<html>
<head>
<title>Site</title>
</head>
<body>
<h1>Merhaba Dünya</h1>
</body>
</html>
'''

    elif "discord" in text or "bot" in text:
        return '''
import discord

client = discord.Client()

@client.event
async def on_ready():
    print("Bot aktif")

client.run("TOKEN")
'''

    return f'''
# {prompt}

print("Kod hazır")
'''

# ==========================
# AI CHAT
# ==========================
def ai_reply(msg):
    text = msg.lower()

    if "merhaba" in text:
        return "Merhaba 👋"

    if any(x in text for x in [
        "nedir","kimdir","nerede","nasıl","ne zaman"
    ]):
        soru = text.replace("nedir","") \
                   .replace("kimdir","") \
                   .replace("nerede","") \
                   .replace("nasıl","") \
                   .replace("ne zaman","") \
                   .strip()

        return wiki_ai(soru)

    if any(x in text for x in [
        "kod","python","yaz","oluştur","yap",
        "hesap","site","bot","discord","html"
    ]):
        return coder_ai(msg)

    return "Bunu anlayamadım 😎"

# ==========================
# SERVER
# ==========================
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
            self.send_json(200, {"status": "V8 SMART AI AKTIF 🔥"})

        elif self.path == "/api/create-key":
            key = create_key("web_user")
            self.send_json(200, {"api_key": key})

        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):

        auth = self.headers.get("Authorization")

        if not auth:
            self.send_json(401, {"error": "API key gerekli"})
            return

        key = auth.replace("Bearer ", "")
        user = get_user(key)

        if not user:
            self.send_json(403, {"error": "Geçersiz key"})
            return

        if user["usage"] >= LIMIT:
            self.send_json(429, {"error": "Limit doldu"})
            return

        user["usage"] += 1
        update_user(key, user)

        if self.path == "/api/chat":

            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            try:
                data = json.loads(body)
                msg = data["message"]
            except:
                msg = ""

            reply = ai_reply(msg)

            self.send_json(200, {
                "reply": reply,
                "usage": user["usage"]
            })
            return

        self.send_json(404, {"error": "not found"})

# ==========================
# RUN
# ==========================
def run():
    server = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)
    print("V8 SMART AI RUNNING")
    server.serve_forever()

if __name__ == "__main__":
    run()
