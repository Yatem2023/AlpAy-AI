import wikipedia

def search_knowledge(query):
    try:
        wikipedia.set_lang("tr")

        # query temizleme
        q = query.replace("nedir", "").replace("kimdir", "").strip()

        if not q:
            return None

        result = wikipedia.summary(q, sentences=2)
        return result

    except Exception as e:
        print("Wiki hata:", e)
        return None
