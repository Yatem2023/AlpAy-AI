import wikipedia, requests
wikipedia.set_lang("tr")

def search_knowledge(query):
    try:
        return "📚 Wikipedia:\n" + wikipedia.summary(query, sentences=2)
    except:
        try:
            url = f"https://api.duckduckgo.com/?q={query}&format=json"
            r = requests.get(url, timeout=5).json()
            if r.get("AbstractText"):
                return "🌐 İnternet:\n" + r["AbstractText"]
        except:
            pass
    return "Bu konuda bilgi bulamadım."

