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
DB_FILE = "users.json"
LIMIT = 500
HF_TOKEN = "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"
wikipedia.set_lang("tr")

# =========================
# DATABASE
# =========================
def load_db():
    if not os.path.exists(DB_FILE):
        return {}

    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
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
# WIKI
# =========================
def wiki_ai(query):
    try:
        return wikipedia.summary(query, sentences=3)
    except:
        return "Bilgi bulunamadı."

# =========================
# IMAGE AI (GERÇEK)
# =========================
def image_ai(prompt):
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "inputs": prompt
    }

    r = requests.post(url, headers=headers, json=payload)

    if r.status_code == 200:
        filename = "image.png"

        with open(filename, "wb") as f:
            f.write(r.content)

        return {
            "type": "image",
            "url": "/image.png",
            "prompt": prompt
        }

    return {
        "type": "text",
        "reply": "Görsel üretilemedi."
    }

# =========================
# CODER AI
# =========================
def coder_ai(text):

    t = text.lower()

    if "hesap" in t:
        return """
# Hesap Makinesi

a = float(input("1. sayı: "))
b = float(input("2. sayı: "))
islem = input("+, -, *, / : ")

if islem == "+":
    print(a+b)
elif islem == "-":
    print(a-b)
elif islem == "*":
    print(a*b)
elif islem == "/":
    print(a/b)
"""

    if "site" in t:
        return """
<!DOCTYPE html>
<html>
<head>
<title>Site</title>
</head>
<body>
<h1>Merhaba</h1>
</body>
</html>
"""

    return "# Kod oluşturuldu"

# =========================
# NORMAL CHAT
# =========================
def chat_ai(text):
    t = text.lower()

    if "merhaba" in t:
        return "Merhaba 👋"

    if "nasılsın" in t:
        return "Harikayım 😎"

    return "Bunu geliştiriyorum 🔥"

# =========================
# MAIN AI
# =========================
def ai_reply(msg, user):

    text = msg.lower().strip()

    remember(user, msg)

    # Görsel
    if any(k in text for k in [
        "çiz", "logo", "afiş",
        "wallpaper", "görsel",
        "resim"
    ]):
        user["last_topic"] = "image"
        return image_ai(msg)

    # Kod
    if any(k in text for k in [
        "kod", "python", "html",
        "css", "js", "site",
        "uygulama", "hesap"
    ]):
        user["last_topic"] = "code"

        return {
            "type": "code",
            "reply": coder_ai(msg)
        }

    # Wiki
    if any(k in text for k in [
        "nedir", "kimdir",
        "nerede", "nasıl"
    ]):
        q = text.replace("nedir", "") \
                .replace("kimdir", "") \
                .replace("nerede", "") \
                .replace("nasıl", "") \
                .strip()

        return {
            "type": "text",
            "reply": wiki_ai(q)
        }

    return {
        "type": "text",
        "reply": chat_ai(msg)
    }

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
                "status": "V11 ACTIVE 🔥"
            })
            return

        if self.path == "/api/create-key":

            key = create_key("web_user")

            self.send_json(200, {
                "api_key": key
            })
            return

        if self.path == "/image.png":
            try:
                with open("image.png", "rb") as f:
                    data = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            except:
                pass

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
                self.headers.get(
                    "Content-Length", 0
                )
            )

            raw = self.rfile.read(length)

            try:
                data = json.loads(
                    raw.decode("utf-8")
                )
                msg = data.get(
                    "message", ""
                )
            except:
                msg = ""

            result = ai_reply(msg, user)

            save_user(key, user)

            self.send_json(200, result)
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

    print("V11 ACTIVE 🔥")
    server.serve_forever()

if __name__ == "__main__":
    run()
