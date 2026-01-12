from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class NiyetModeli:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1,2))
        self.model = MultinomialNB()
        self.texts = []
        self.labels = []
        self.egitildi = False

    def ekle(self, metin, etiket):
        self.texts.append(metin.lower())
        self.labels.append(etiket)

    def egit(self):
        if len(self.texts) < 3:
            return
        X = self.vectorizer.fit_transform(self.texts)
        self.model.fit(X, self.labels)
        self.egitildi = True

    def tahmin(self, metin):
        if not self.egitildi:
            return "SOHBET", 0.0
        X = self.vectorizer.transform([metin.lower()])
        probs = self.model.predict_proba(X)[0]
        i = probs.argmax()
        return self.model.classes_[i], probs[i]
