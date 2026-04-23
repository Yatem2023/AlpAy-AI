import wikipedia

wikipedia.set_lang("tr")

def search_knowledge(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return "Bilgi bulamadım."

        page = wikipedia.page(results[0])
        return page.summary[:100000000000]

    except Exception as e:
        return "Bilgi alınırken hata oluştu."