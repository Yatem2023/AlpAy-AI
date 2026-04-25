import json
import os
import uuid
import requests
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# =============================
# SETTINGS
# =============================
DATA_FILE = "api_keys.json"
FREE_LIMIT = 25

# =============================
# FILE SYSTEM
# =============================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# =============================
# USER SYSTEM
# =============================
def create_key(username):
    data = load_data()

    key = str(uuid.uuid4())

    data[key] = {
        "user": username,
        "usage": 0,
        "plan": "free",
        "premium": False,
        "expire": None,
        "created": str(datetime.now())
    }

    save_data(data)
    return key


def get_user(api_key):
    data = load_data()
    return data.get(api_key)


def update_user(api_key, user):
    data = load_data()
    data[api_key] = user
    save_data(data)


# =============================
# PREMIUM SYSTEM
# =============================
def premium_active(user):
    if not user.get("premium", False):
        return False

    if not user.get("expire"):
        return False

    expire = datetime.fromisoformat(user["expire"])

    if datetime.now() > expire:
        user["premium"] = False
        user["plan"] = "free"
        return False

    return True


def can_use(user):
    plan = user.get("plan", "free")
    usage = user.get("usage", 0)

    if premium_active(user):

        if plan == "basic":
            return usage < 1000

        if plan in ["pro", "ultra"]:
            return True

    return usage < FREE_LIMIT


# =============================
# AI FULL CODER
# =============================
def coder_ai(prompt):
    query = prompt.replace(" ", "+")

    try:
        requests.get(
            f"https://api.duckduckgo.com/?q={query}+python+code&format=json",
            timeout=5
        )

        code = f'''# {prompt}

def main():
    print("{prompt} çalıştırıldı")

if __name__ == "__main__":
    main()
'''

        return code

    except:
        return "Kod üretilemedi."


# =============================
# CHAT AI
# =============================
def ai_reply(msg):
    text = msg.lower()

    if "merhaba" in text:
        return "Merhaba 👋"

    if "kod" in text or "python" in text:
        return coder_ai(msg)

    return "Bunu geliştiriyorum 😎"


# =============================
# SERVER
# =============================
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
            self.send_json(200, {
                "status": "FULL CODER V7 AKTIF 🔥"
            })

        elif self.path == "/api/create-key":
            key = create_key("web_user")
            self.send_json(200, {"api_key": key})

        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):

        if self.path == "/api/create-key":

            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            try:
                data = json.loads(body)
                username = data["username"]
            except:
                username = "user"

            key = create_key(username)

            self.send_json(200, {"api_key": key})
            return

        # AUTH
        auth = self.headers.get("Authorization")

        if not auth:
            self.send_json(401, {"error": "API key gerekli"})
            return

        api_key = auth.replace("Bearer ", "")
        user = get_user(api_key)

        if not user:
            self.send_json(403, {"error": "Geçersiz key"})
            return

        if not can_use(user):
            self.send_json(429, {"error": "Limit doldu"})
            return

        user["usage"] += 1
        update_user(api_key, user)

        # CHAT
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
                "usage": user["usage"],
                "plan": user["plan"]
            })

            return

        self.send_json(404, {"error": "not found"})


# =============================
# RUN
# =============================
def run():
    server = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)
    print("V7 running on port 8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
