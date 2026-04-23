# backend.py
from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "AlpAy AI Backend Aktif 🚀"

# =========================
# DOSYALAR
# =========================
API_FILE = "api_keys.json"
MEMORY_FILE = "memory.json"

# =========================
# YOKSA OLUŞTUR
# =========================
if not os.path.exists(API_FILE):
    with open(API_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "test123": {
                "user": "admin",
                "plan": "ultra",
                "messages_used": 0,
                "messages_limit": 999999,
                "premium": True
            }
        }, f, indent=4)

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=4)

# =========================
# LOAD
# =========================
def load_users():
    with open(API_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    with open(API_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_memory():
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# =========================
# PLAN AYARLARI
# =========================
PLANS = {
    "basic": {
        "price": 29,
        "limit": 1000
    },
    "pro": {
        "price": 79,
        "limit": 999999
    },
    "ultra": {
        "price": 149,
        "limit": 999999
    }
}

# =========================
# BASİT AI
# =========================
def ai_reply(msg, plan, username):
    text = msg.lower()

    if "merhaba" in text:
        return f"Merhaba {username} 👋"

    if "saat" in text:
        return "Şu an saat: " + datetime.now().strftime("%H:%M")

    if "nasılsın" in text:
        return "Harikayım 😎"

    if plan == "ultra":
        return f"🔥 ULTRA MODE CEVAP:\n{msg}"

    elif plan == "pro":
        return f"⚡ PRO MODE:\n{msg}"

    return f"💬 {msg}"

# =========================
# CHAT API
# =========================
@app.route("/api/chat", methods=["POST"])
def chat():

    auth = request.headers.get("Authorization")

    if not auth:
        return jsonify({"reply": "API KEY yok"}), 401

    key = auth.replace("Bearer ", "")

    users = load_users()

    if key not in users:
        return jsonify({"reply": "Geçersiz API KEY"}), 403

    user = users[key]

    plan = user["plan"]
    used = user["messages_used"]
    limit = user["messages_limit"]

    if used >= limit:
        return jsonify({
            "reply": "Mesaj hakkın bitti. Premium yenile."
        })

    data = request.json
    message = data.get("message", "")

    # Kullanım artır
    users[key]["messages_used"] += 1
    save_users(users)

    # Hafıza sistemi
    memory = load_memory()

    if plan == "ultra":
        memory[key] = {
            "last_message": message,
            "time": str(datetime.now())
        }
        save_memory(memory)

    reply = ai_reply(message, plan, user["user"])

    return jsonify({
        "reply": reply,
        "plan": plan,
        "used": users[key]["messages_used"],
        "limit": limit
    })

# =========================
# ADMIN PANEL
# =========================
@app.route("/admin/users")
def admin_users():
    return jsonify(load_users())

# =========================
# PREMIUM YÜKSELT
# =========================
@app.route("/admin/upgrade/<key>/<plan>")
def upgrade(key, plan):

    users = load_users()

    if key not in users:
        return "Kullanıcı yok"

    if plan not in PLANS:
        return "Plan yok"

    users[key]["plan"] = plan
    users[key]["messages_limit"] = PLANS[plan]["limit"]
    users[key]["premium"] = True

    save_users(users)

    return f"{key} artık {plan}"

# =========================
# YENİ KULLANICI EKLE
# =========================
@app.route("/admin/create/<key>/<username>")
def create_user(key, username):

    users = load_users()

    users[key] = {
        "user": username,
        "plan": "basic",
        "messages_used": 0,
        "messages_limit": 1000,
        "premium": True
    }

    save_users(users)

    return "oluşturuldu"

# =========================
# RESET AYLIK
# =========================
@app.route("/admin/reset")
def reset():

    users = load_users()

    for key in users:
        users[key]["messages_used"] = 0

    save_users(users)

    return "reset tamam"

# =========================
# START
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
