import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import uuid
import os

# ================== CONFIG ==================
API_KEYS_FILE = "api_keys.json"
RATE_LIMIT = 100

# ================== FILE SYSTEM ==================

def load_api_keys():
    if not os.path.exists(API_KEYS_FILE):
        return {}
    with open(API_KEYS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_api_keys(data):
    with open(API_KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ================== SELF HEALING KEY SYSTEM ==================

def check_api_key(api_key):
    data = load_api_keys()

    # 🔥 KEY YOKSA OTOMATİK OLUŞTUR
    if api_key not in data:
        print("⚠️ Yeni key oluşturuldu:", api_key)

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
        return data[api_key]["usage"]

    return 0

def create_api_key():
    data = load_api_keys()

    new_key = str(uuid.uuid4())

    data[new_key] = {
        "user": "web_user",
        "usage": 0,
        "plan": "free"
    }

    save_api_keys(data)

    return new_key

# ================== AI RESPONSE ==================

def generate_reply(message):
    msg = message.lower()

    if "merhaba" in msg:
        return "Merhaba! 😎"

    if "saat" in msg:
        import datetime
        return str(datetime.datetime.now())

    if "hesap makinası" in msg:
        return """# Basit hesap makinesi
def hesapla():
    a = float(input("Sayı 1: "))
    b = float(input("Sayı 2: "))
    print("Toplam:", a + b)

hesapla()
"""

    return "Bunu geliştiriyorum 😎"

# ================== API ==================

class Handler(BaseHTTPRequestHandler):

    def send_json(self, code, data):
        body = json.dumps(data).encode("utf-8")

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
            self.send_json(200, {"status": "API çalışıyor 🚀"})

        elif self.path == "/api/create-key":
            key = create_api_key()
            self.send_json(200, {"api_key": key})

        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):

        # 🔐 AUTH HEADER AL
        auth = self.headers.get("Authorization")

        if auth and auth.startswith("Bearer "):
            api_key = auth.split(" ")[1]
        else:
            # 🔥 KEY YOKSA OTOMATİK OLUŞTUR
            api_key = str(uuid.uuid4())

        # 🔥 SELF HEALING CHECK
        user = check_api_key(api_key)

        # RATE LIMIT
        if user["usage"] >= RATE_LIMIT:
            self.send_json(429, {"error": "rate limit"})
            return

        increment_usage(api_key)

        # BODY OKU
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body.decode("utf-8"))
        except:
            self.send_json(400, {"error": "bad json"})
            return

        # CHAT
        if self.path == "/api/chat":
            message = data.get("message", "")
            reply = generate_reply(message)

            self.send_json(200, {
                "reply": reply,
                "api_key": api_key  # 🔥 FRONTEND'E GERİ VER
            })
            return

        self.send_json(404, {"error": "not found"})

# ================== RUN ==================

def run():
    server = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)
    print("🚀 Server çalışıyor")
    server.serve_forever()

if __name__ == "__main__":
    run()
