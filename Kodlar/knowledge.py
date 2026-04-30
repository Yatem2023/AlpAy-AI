import wikipedia

def search_knowledge(query):
    try:
        wikipedia.set_lang("tr")

        q = query.replace("nedir","").replace("kimdir","").strip()

        if not q:
            return None

        return wikipedia.summary(q, sentences=2)

    except:
        try:
            # 🔥 fallback EN (çok önemli)
            wikipedia.set_lang("en")
            return wikipedia.summary(q, sentences=2)
        except:
            return None
