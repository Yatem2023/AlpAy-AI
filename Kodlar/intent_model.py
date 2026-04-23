from pathlib import Path
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class IntentModel:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent
        rules_path = base_dir / "rules.json"

        with open(rules_path, "r", encoding="utf-8") as f:
            self.rules = json.load(f)

        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression(max_iter=1000)
        self.is_trained = False

    def _build_dataset(self):
        x_data, y_data = [], []

        for intent, phrases in self.rules.items():
            for phrase in phrases:
                x_data.append(phrase)
                y_data.append(intent)

        return x_data, y_data

    def train(self):
        x_data, y_data = self._build_dataset()

        if not x_data:
            self.is_trained = False
            return

        x_vec = self.vectorizer.fit_transform(x_data)
        self.model.fit(x_vec, y_data)
        self.is_trained = True

    def _ensure_trained(self):
        if not self.is_trained:
            self.train()

    def predict(self, text):
        self._ensure_trained()

        if not self.is_trained:
            return None, 0.0

        x_vec = self.vectorizer.transform([text])
        probs = self.model.predict_proba(x_vec)[0]
        idx = probs.argmax()
        return self.model.classes_[idx], probs[idx]