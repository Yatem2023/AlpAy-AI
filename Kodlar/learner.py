import json
FILE="learned_commands.json"
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FILE = BASE_DIR / "learned_commands.json"

def load_learned():␍␊
    try:␍␊
        with open(FILE,"r",encoding="utf-8") as f:␍␊
            return json.load(f)␍␊
    except:␍␊
        return {}␍␊
def load_learned():␊
    try:␊
        with open(FILE,"r",encoding="utf-8") as f:␊
            return json.load(f)␊
    except:␊
        return {}␊

def learn(cmd, action):
    data = load_learned()
    data[cmd] = action
    with open(FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

def get_learned(cmd):
    return load_learned().get(cmd)
