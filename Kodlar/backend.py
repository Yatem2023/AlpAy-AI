import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import uuid
import os
import datetime

API_KEYS_FILE = "api_keys.json"
RATE_LIMIT = 100

# ================= DB =================
def load_db():
    if not os.path.exists(API_KEYS_FILE):
        return {}
    with open(API_KEYS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(API_KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ================= USER =================
def get_user_id(handler):
    ip = handler.client_address[0]

    auth = handler.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        key = auth.split(" ")[1]
    else:
        key = "anon"

    return f"{key}_{ip}"

def check_user(user_id):
    data = load_db()
    today = str(datetime.date.today())

    if user_id not in data:
        data[user_id] = {
            "usage": 0,
            "date": today
        }

    # 🔥 günlük reset
    if data[user_id]["date"] != today:
        data[user_id]["usage"] = 0
        data[user_id]["date"] = today

    save_db(data)
    return data[user_id]

def increment(user_id):
    data = load_db()
    data[user_id]["usage"] += 1
    save_db(data)

# ================= AI =================
def generate_reply(msg):
    msg = msg.lower()

    if "merhaba" in msg:
        return "Merhaba 😎"

    if "nasılsın" in msg:
        return "İyiyim 😎 sen nasılsın?"

    if "2+2" in msg:
        return "Sonuç: 4"

    return "Bunu geliştiriyorum 😎"

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
        user_id = get_user_id(self)
        user = check_user(user_id)

        if user["usage"] >= RATE_LIMIT:
            self.send_json(429, {"error": "limit doldu"})
            return

        increment(user_id)

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
                "reply": reply
            })
            return

        self.send_json(404, {"error": "not found"})

# ================= RUN =================
def run():
    port = int(os.environ.get("PORT", 8000))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"🚀 çalışıyor: {port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
