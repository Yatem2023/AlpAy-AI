"""
AlpAy Engine Dataset
Version: 0.1
"""

from tokenizer import Tokenizer
from vocabulary import Vocabulary


class TextDataset:

    def __init__(
        self,
        file_path: str,
        context_length: int = 32,
        min_freq: int = 1
    ):

        self.file_path = file_path
        self.context_length = context_length

        self.tokenizer = Tokenizer()
        self.vocab = Vocabulary()

        self.tokens = []
        self.encoded = []

        self.inputs = []
        self.targets = []

        self.load(min_freq)

    def load(self, min_freq):

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        self.tokens = self.tokenizer.tokenize(text)

        self.vocab.build(
            [self.tokens],
            min_freq=min_freq
        )

        self.encoded = self.vocab.encode(self.tokens)

        self.create_sequences()

    def create_sequences(self):

        self.inputs = []
        self.targets = []

        length = len(self.encoded)

        if length <= self.context_length:
            return

        for i in range(length - self.context_length):

            x = self.encoded[
                i:i + self.context_length
            ]

            y = self.encoded[
                i + 1:i + self.context_length + 1
            ]

            self.inputs.append(x)
            self.targets.append(y)

    def __len__(self):

        return len(self.inputs)

    def __getitem__(self, index):

        return (
            self.inputs[index],
            self.targets[index]
        )


if __name__ == "__main__":

    dataset = TextDataset(
        "../datasets/tr.txt",
        context_length=8
    )

    print("Toplam örnek:", len(dataset))

    x, y = dataset[0]

    print()

    print("INPUT")
    print(x)

    print()

    print("TARGET")
    print(y)

    print()

    print(
        dataset.vocab.decode(x)
    )

    print(
        dataset.vocab.decode(y)
    )