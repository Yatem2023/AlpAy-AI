from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import json
from learner import load_learned

class IntentModel:
    def __init__(self):
        with open("rules.json", "r", encoding="utf-8") as f:
            self.rules = json.load(f)

        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression(max_iter=1000)

    def train(self):
        X, y = [], []

        for intent, phrases in self.rules.items():
            for p in phrases:
                X.append(p)
                y.append(intent)

        learned = load_learned()
        for k, v in learned.items():
            X.append(k)
            y.append(v)

        X_vec = self.vectorizer.fit_transform(X)
        self.model.fit(X_vec, y)

    def predict(self, text):
        self.train()
        X = self.vectorizer.transform([text])
        probs = self.model.predict_proba(X)[0]
        idx = probs.argmax()
        return self.model.classes_[idx], probs[idx]
