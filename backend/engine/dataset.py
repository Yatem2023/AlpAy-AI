"""
AlpAy Engine
Dataset
Version: 1.0
"""

from pathlib import Path

import torch
from torch.utils.data import Dataset

from tokenizer import Tokenizer
from vocabulary import Vocabulary


class TextDataset(Dataset):

    def __init__(
        self,
        context_length=64,
        min_freq=1,
        dataset_name="tr.txt"
    ):

        self.context_length = context_length

        # backend klasörü
        backend_dir = Path(__file__).resolve().parent.parent

        # dataset yolu
        dataset_path = backend_dir / "datasets" / dataset_name

        if not dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset bulunamadı:\n{dataset_path}"
            )

        with open(
            dataset_path,
            "r",
            encoding="utf-8"
        ) as f:
            text = f.read()

        self.tokenizer = Tokenizer()

        self.tokens = self.tokenizer.tokenize(text)

        self.vocab = Vocabulary()

        self.vocab.build(
            [self.tokens],
            min_freq=min_freq
        )

        self.ids = self.vocab.encode(
            self.tokens
        )

        print(f"📖 Dataset yüklendi")
        print(f"Toplam token : {len(self.tokens)}")
        print(f"Vocabulary : {len(self.vocab.token_to_id)}")

    def __len__(self):

        return max(
            0,
            len(self.ids) - self.context_length
        )

    def __getitem__(self, idx):

        x = self.ids[
            idx:
            idx + self.context_length
        ]

        y = self.ids[
            idx + 1:
            idx + self.context_length + 1
        ]

        return (
            torch.tensor(
                x,
                dtype=torch.long
            ),
            torch.tensor(
                y,
                dtype=torch.long
            )
        )