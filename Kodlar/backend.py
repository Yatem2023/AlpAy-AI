import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import actions
from intent_model import IntentModel
from knowledge import search_knowledge
from learner import get_learned
from memory import remember

import uuid
import os

# ================== API KEY SYSTEM ==================

API_KEYS_FILE = "api_keys.json"
RATE_LIMIT = 100



def load_api_keys():
    if not os.path.exists(API_KEYS_FILE):
        return {}
    with open(API_KEYS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_api_keys(data):
    with open(API_KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def create_api_key(username="user"):
    data = load_api_keys()
    new_key = str(uuid.uuid4())

    data[new_key] = {
        "user": username,
        "usage": 0
    }

    save_api_keys(data)
    return new_key


def check_api_key(api_key):
    data = load_api_keys()
    return data.get(api_key)


def increment_usage(api_key):
    data = load_api_keys()

    if api_key in data:
        data[api_key]["usage"] += 1
        save_api_keys(data)
        return data[api_key]["usage"]

    return None

def get_user_keys(username):
    data = load_api_keys()
    result = []

    for key, info in data.items():
        if info["user"] == username:
            result.append({
                "key": key,
                "usage": info["usage"]
            })

    return result


# ================== AI SYSTEM ==================

QUESTION_HINTS = ["kimdir", "nedir", "nerede", "ne zaman", "nasıl", "hangi"]

MIN_CONFIDENCE = 0.30
LOW_CONFIDENCE_SAFE_INTENTS = {"chat_greetings", "chat_farewell"}

model = IntentModel()


def extract_query(text):
    keywords = ["nedir", "kimdir", "nerede", "nasıl", "ne zaman", "hangi"]
    for k in keywords:
        if k in text:
            return text.replace(k, "").strip()
    return text


def looks_like_open_question(text):
    normalized = text.lower().strip()
    if normalized.endswith("?"):
        return True
    return any(hint in normalized for hint in QUESTION_HINTS)


def generate_reply(user_text):
    user = user_text.lower().strip()

    if not user:
        return "Bir mesaj yazabilirsin."

    if "saat" in user:
        return actions.get_time()

    if "hava" in user:
        return actions.get_weather(user, "today")

    learned = get_learned(user)
    if learned:
        return learned

    intent, confidence = model.predict(user)

    if confidence < MIN_CONFIDENCE:
        if intent in LOW_CONFIDENCE_SAFE_INTENTS:
            pass
        elif looks_like_open_question(user):
            intent = "questions_open"
        else:
            intent = None

    answer = None

    if intent == "open_chrome":
        answer = "Web sürümünde uygulama açma desteklenmiyor."

    elif intent == "open_vscode":
        answer = "Web sürümünde uygulama açma desteklenmiyor."

    elif intent == "open_notepad":
        answer = "Web sürümünde uygulama açma desteklenmiyor."

    elif intent == "time":
        answer = actions.get_time()

    elif intent == "weather_today":
        answer = actions.get_weather(user, "today")

    elif intent == "weather_week":
        answer = actions.get_weather(user, "week")

    elif intent == "chat_greetings":
        answer = "Merhaba! Nasılsın?"

    elif intent == "chat_farewell":
        answer = "Görüşürüz 👋"

    elif intent == "questions_open":
        query = extract_query(user)

        if len(query) < 2:
            answer = "Sorunu biraz daha detaylandırabilir misin?"
        else:
            answer = search_knowledge(query)

    if answer is None:
        answer = "Bunu tam anlayamadım."

    remember(user, answer)
    return answer


# ================== API HANDLER ==================

class AlpAyAPIHandler(BaseHTTPRequestHandler):

    def _send_json(self, status_code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self._send_json(200, {"status": "AlpAy API çalışıyor 🚀"})

        elif self.path == "/api/create-key":
            new_key = create_api_key("web_user")
            self._send_json(200, {"api_key": new_key})

        else:
            self._send_json(404, {"error": "Not found"})

    # ✅ POST (asıl API)
    def do_POST(self):

        # 🔥 API KEY OLUŞTURMA (AUTH YOK)
        if self.path == "/api/create-key":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)

            try:
                data = json.loads(raw_body.decode("utf-8"))
                username = data.get("username", "user")
            except:
                username = "user"

            new_key = create_api_key(username)
            self._send_json(200, {"api_key": new_key})
            return
        # 🔑 KULLANICI KEYLERİNİ GETİR
        if self.path == "/api/my-keys":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)

            try:
                data = json.loads(raw_body.decode("utf-8"))
                username = data.get("username", "")
            except:
                self._send_json(400, {"error": "Invalid JSON"})
                return

            keys = get_user_keys(username)
            self._send_json(200, {"keys": keys})
            return

        # 🔐 AUTH
        auth_header = self.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            self._send_json(401, {"error": "API key gerekli"})
            return

        api_key = auth_header.split(" ")[1]
        user_data = check_api_key(api_key)

        if not user_data:
            self._send_json(403, {"error": "Geçersiz API key"})
            return

        if user_data["usage"] >= RATE_LIMIT:
            self._send_json(429, {"error": "Rate limit aşıldı"})
            return

        increment_usage(api_key)

        # 💬 CHAT
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)

            try:
                data = json.loads(raw_body.decode("utf-8"))
                message = data.get("message", "")
            except:
                self._send_json(400, {"error": "Invalid JSON"})
                return

            reply = generate_reply(message)
            self._send_json(200, {"reply": reply})
            return

        self._send_json(404, {"error": "Not found"})


# ================== RUN ==================

def run(host="0.0.0.0", port=8000):
    server = ThreadingHTTPServer((host, port), AlpAyAPIHandler)
    print(f"AlpAy API running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()

api_key = auth_header.split(" ")[1]
user_data = check_api_key(api_key)
print("GELEN KEY:", api_key)
print("JSON:", load_api_keys())
