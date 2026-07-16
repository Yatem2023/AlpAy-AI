"""
AlpAy Engine Vocabulary
Version: 0.1
"""

from collections import Counter
import json


class Vocabulary:

    PAD = "<PAD>"
    UNK = "<UNK>"
    BOS = "<BOS>"
    EOS = "<EOS>"

    def __init__(self):

        self.token_to_id = {}
        self.id_to_token = {}

        self.special_tokens = [
            self.PAD,
            self.UNK,
            self.BOS,
            self.EOS
        ]

    def build(self, token_lists, min_freq=1):

        counter = Counter()

        for tokens in token_lists:
            counter.update(tokens)

        self.token_to_id = {}
        self.id_to_token = {}

        current_id = 0

        # özel tokenlar

        for token in self.special_tokens:

            self.token_to_id[token] = current_id
            self.id_to_token[current_id] = token

            current_id += 1

        # normal tokenlar

        for token, freq in counter.items():

            if freq >= min_freq:

                if token not in self.token_to_id:

                    self.token_to_id[token] = current_id
                    self.id_to_token[current_id] = token

                    current_id += 1

    def encode(self, tokens):

        unk = self.token_to_id[self.UNK]

        return [
            self.token_to_id.get(token, unk)
            for token in tokens
        ]

    def decode(self, ids):

        return [
            self.id_to_token.get(i, self.UNK)
            for i in ids
        ]

    def vocab_size(self):

        return len(self.token_to_id)

    def save(self, path):

        with open(path, "w", encoding="utf-8") as f:

            json.dump(
                self.token_to_id,
                f,
                ensure_ascii=False,
                indent=4
            )

    def load(self, path):

        with open(path, "r", encoding="utf-8") as f:

            self.token_to_id = json.load(f)

        self.id_to_token = {
            idx: token
            for token, idx in self.token_to_id.items()
        }


if __name__ == "__main__":

    from tokenizer import Tokenizer

    tokenizer = Tokenizer()

    texts = [

        "Merhaba ben AlpAy",

        "Merhaba dünya",

        "Ben yapay zekayım"

    ]

    token_lists = [

        tokenizer.tokenize(text)

        for text in texts

    ]

    vocab = Vocabulary()

    vocab.build(token_lists)

    print(vocab.token_to_id)

    encoded = vocab.encode(
        tokenizer.tokenize("Merhaba AlpAy")
    )

    print(encoded)

    print(vocab.decode(encoded))

    vocab.save("vocab.json")