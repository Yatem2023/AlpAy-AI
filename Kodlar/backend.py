import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import actions
from intent_model import IntentModel
from knowledge import search_knowledge
from learner import get_learned
from memory import remember


QUESTION_HINTS = ["kimdir", "nedir", "nerede", "ne zaman", "nasıl", "kaç", "hangi"]
MIN_CONFIDENCE = 0.70
LOW_CONFIDENCE_SAFE_INTENTS = {"chat_greetings", "chat_farewell"}

model = IntentModel()


def looks_like_open_question(text):
    normalized = text.lower().strip()
    if normalized.endswith("?"):
        return True
    return any(hint in normalized for hint in QUESTION_HINTS)


def generate_reply(user_text):
    user = user_text.lower().strip()
    if not user:
        return "Bir mesaj yazabilirsin."

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
        answer = "Web sürümünde uygulama açma desteklenmiyor. Masaüstü sürümünü kullanabilirsin."
    elif intent == "open_vscode":
        answer = "Web sürümünde uygulama açma desteklenmiyor. Masaüstü sürümünü kullanabilirsin."
    elif intent == "open_notepad":
        answer = "Web sürümünde uygulama açma desteklenmiyor. Masaüstü sürümünü kullanabilirsin."
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
        answer = search_knowledge(user)

    if answer is None:
        answer = "Bu komutu web sürümünde henüz bilmiyorum."

    remember(user, answer)
    return answer


class AlpAyAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/chat":
            self._send_json(404, {"error": "Not found"})
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        try:
            data = json.loads(raw_body.decode("utf-8"))
            message = data.get("message", "")
        except Exception:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        reply = generate_reply(message)
        self._send_json(200, {"reply": reply})


def run(host="0.0.0.0", port=8000):
    server = ThreadingHTTPServer((host, port), AlpAyAPIHandler)
    print(f"AlpAy API running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
