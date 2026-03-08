from intent_model import IntentModel
import actions
from memory import remember, recall
from learner import learn, get_learned
from knowledge import search_knowledge

model = IntentModel()

print("🤖 Mini AI hazır. ('çık' yazarak kapatabilirsin)")

while True:
    user = input("Sen: ").lower().strip()
    if not user:
        continue

    if user == "az önce ne dedim":
        answer = recall()
        print("AI:", answer)
        remember(user, answer)
        continue

    if user in ["çık", "kapat", "bye"]:
        print("AI: 👋 Görüşürüz")
        break

    learned = get_learned(user)
    if learned:
        if learned.endswith(" aç"):
            actions.open_app_by_name(learned)
            answer = f"{learned} (öğrenilmiş)"
        else:
            answer = learned
        print("AI:", answer)
        remember(user, answer)
        continue

    intent, confidence = model.predict(user)
    print(f"DEBUG intent = {intent} | conf={confidence:.2f}")

    if confidence < 0.30:
        intent = None

    answer = None

    if intent == "open_chrome":
        actions.open_chrome()
        answer = "Chrome açıldı."
    elif intent == "open_vscode":
        actions.open_vscode()
        answer = "VS Code açıldı."
    elif intent == "open_notepad":
        actions.open_notepad()
        answer = "Not defteri açıldı."
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

    elif user.endswith(" aç"):
        if actions.open_app_by_name(user):
            answer = "Uygulama açıldı."

    if answer is None:
        print("AI: Bu komutu bilmiyorum. Ne yapmamı istersin?")
        teach = input("Sen (öğret): ").lower().strip()
        if teach:
            learn(user, teach)
            answer = "Tamam 👍 öğrendim."
        else:
            answer = "Öğrenmeden geçiyorum."

    print("AI:", answer)
    remember(user, answer)

