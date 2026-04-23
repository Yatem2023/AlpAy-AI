import json
import os
import uuid
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# =========================
# SETTINGS
# =========================

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8000))
DATA_FILE = "api_keys.json"

FREE_LIMIT = 20

PLANS = {
    "basic": {
        "name": "Basic Premium",
        "price": 29,
        "limit": 1000,
        "days": 30
    },
    "pro": {
        "name": "Pro",
        "price": 79,
        "limit": -1,  # unlimited
        "days": 30
    },
    "ultra": {
        "name": "Ultra",
        "price": 149,
        "limit": -1,
        "days": 30
    }
}

# =========================
# DATABASE
# =========================

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# =========================
# USER SYSTEM
# =========================

def create_key(username):
    data = load_data()

    new_key = str(uuid.uuid4())

    data[new_key] = {
        "user": username,
        "usage": 0,
        "plan": "free",
        "premium": False,
        "expire": None,
        "created": str(datetime.now())
    }

    save_data(data)
    return new_key

def get_user(api_key):
    data = load_data()
    return data.get(api_key)

def save_user(api_key, user_data):
    data = load_data()
    data[api_key] = user_data
    save_data(data)

def add_usage(api_key):
    user = get_user(api_key)

    if user:
        user["usage"] += 1
        save_user(api_key, user)

def premium_active(user):
    if not user["premium"]:
        return False

    if not user["expire"]:
        return False

    expire = datetime.fromisoformat(user["expire"])

    if datetime.now() > expire:
        user["premium"] = False
        user["plan"] = "free"
        return False

    return True

# =========================
# PREMIUM SYSTEM
# =========================

def buy_plan(api_key, plan_name):
    if plan_name not in PLANS:
        return False, "Plan bulunamadı"

    user = get_user(api_key)

    if not user:
        return False, "API key geçersiz"

    plan = PLANS[plan_name]

    expire = datetime.now() + timedelta(days=plan["days"])

    user["premium"] = True
    user["plan"] = plan_name
    user["expire"] = expire.isoformat()
    user["usage"] = 0

    save_user(api_key, user)

    return True, plan

# =========================
# LIMIT SYSTEM
# =========================

def can_use(user):
    if premium_active(user):
        plan = user["plan"]

        if plan == "basic":
            return user["usage"] < 1000

        if plan in ["pro", "ultra"]:
            return True

    return user["usage"] < FREE_LIMIT

# =========================
# AI RESPONSE
# =========================

def generate_reply(msg, user):
    text = msg.lower()

    if user["plan"] == "ultra":
        return f"🔥 ULTRA AI CEVAP:\n'{msg}' için en güçlü cevap hazır."

    elif user["plan"] == "pro":
        return f"⚡ PRO AI:\n{msg} hakkında gelişmiş cevap."

    elif user["plan"] == "basic":
        return f"💎 BASIC AI:\n{msg} hakkında premium cevap."

    return f"🙂 FREE AI:\n{msg} hakkında normal cevap."

# =========================
# API SERVER
# =========================

class Handler(BaseHTTPRequestHandler):

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")

        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):

        if self.path == "/":
            self.send_json(200, {"status": "AlpAy Premium API aktif 🚀"})

        else:
            self.send_json(404, {"error": "Not found"})

    def do_POST(self):

        content_length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(content_length)

        try:
            data = json.loads(raw.decode("utf-8"))
        except:
            data = {}

        # CREATE KEY
        if self.path == "/api/create-key":
            username = data.get("username", "user")
            key = create_key(username)

            self.send_json(200, {
                "api_key": key
            })
            return

        # AUTH
        auth = self.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            self.send_json(401, {"error": "API key gerekli"})
            return

        api_key = auth.split(" ")[1]

        user = get_user(api_key)

        if not user:
            self.send_json(403, {"error": "Geçersiz key"})
            return

        # BUY PREMIUM
        if self.path == "/api/buy-premium":

            plan = data.get("plan", "")

            ok, result = buy_plan(api_key, plan)

            if ok:
                self.send_json(200, {
                    "success": True,
                    "plan": result["name"],
                    "price": result["price"],
                    "expire_days": result["days"]
                })
            else:
                self.send_json(400, {"error": result})

            return

        # PROFILE
        if self.path == "/api/me":
            self.send_json(200, user)
            return

        # CHAT
        if self.path == "/api/chat":

            if not can_use(user):
                self.send_json(429, {
                    "error": "Mesaj limitin doldu. Premium al 😎"
                })
                return

            message = data.get("message", "")

            add_usage(api_key)

            reply = generate_reply(message, user)

            self.send_json(200, {
                "reply": reply,
                "usage": user["usage"] + 1,
                "plan": user["plan"]
            })
            return

        self.send_json(404, {"error": "Not found"})


# =========================
# START
# =========================

def run():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"AlpAy API running on {HOST}:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run()
