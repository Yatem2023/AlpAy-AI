import json
from datetime import datetime

FILE = "memory.json"

def load():
    try:
        with open(FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def remember(user, ai):
    mem = load()
    mem.append({"time":datetime.now().strftime("%H:%M"),"user":user,"ai":ai})
    with open(FILE,"w",encoding="utf-8") as f:
        json.dump(mem[-20:],f,ensure_ascii=False,indent=2)

def recall():
    mem = load()
    if not mem:
        return "Henüz bir şey hatırlamıyorum."
    return f"Az önce '{mem[-1]['user']}' dedin."
