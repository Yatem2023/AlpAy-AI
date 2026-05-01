import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import uuid
import os
import requests
import datetime
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

# ================= AI =================

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

def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

    headers = {
        "Authorization": "Bearer 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"
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt}
        )

        print("STATUS:", response.status_code)
        print("TYPE:", response.headers.get("content-type"))

        if response.status_code == 503:
            return "⏳ Model yükleniyor..."

        if "application/json" in response.headers.get("content-type", ""):
            print("HATA:", response.text)
            return "Görsel üretilemedi 😢"

        with open("image.png", "wb") as f:
            f.write(response.content)

        return "https://alpay-ai.onrender.com/image.png"

    except Exception as e:
        print("ERR:", e)
        return "Hata oluştu"
# 🔥 ANA AI (EN ÖNEMLİ YER)
def generate_reply(message):
    msg = message.lower()

    # selam
    if "merhaba" in msg:
        return "Merhaba 😎"

    # saat
    if "saat" in msg:
        return str(datetime.datetime.now())

    # kod
    if "kod" in msg or "yaz" in msg:
        code = generate_code(message)
        if code:
            return code
    if any(x in msg for x in ["çiz", "görsel", "resim", "afiş", "logo"]):
        image_url = generate_image(message)
        return f"🎨 Görsel hazır:\n{image_url}"

    # wiki soruları (ZORUNLU)
    if any(x in msg for x in ["nedir", "kimdir", "ne"]):
        clean = msg.replace("nedir","").replace("kimdir","").replace("ne","").strip()
        wiki = search_knowledge(clean)

    # internet
    net = internet_search(msg)
    if net:
        return net

    # 🔥 SON ÇARE (HER ZAMAN CEVAP)
    # 🔥 SON ÇARE
    wiki = search_knowledge(msg)
    if wiki:
        return wiki

    return "Bilmiyorum ama öğreniyorum 😎"

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
        return

    if self.path == "/image.png":
        try:
            with open("image.png", "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                self.wfile.write(f.read())
        except:
            self.send_json(404, {"error": "no image"})
        return

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
    server = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)
    print("🚀 AI hazır")
    server.serve_forever()

if __name__ == "__main__":
    run()
