"""
AlpAy Engine
Language Model
Version: 0.1
"""

import torch
import torch.nn as nn

from .embedding import EmbeddingLayer
from .transformer import Transformer


class AlpAyModel(nn.Module):

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int = 256,
        num_layers: int = 6,
        num_heads: int = 8,
        ff_hidden_dim: int = 1024,
        dropout: float = 0.1
    ):
        super().__init__()

        self.embedding = EmbeddingLayer(
            vocab_size=vocab_size,
            embedding_dim=embedding_dim,
            dropout=dropout
        )

        self.transformer = Transformer(
            num_layers=num_layers,
            embedding_dim=embedding_dim,
            num_heads=num_heads,
            ff_hidden_dim=ff_hidden_dim,
            dropout=dropout
        )

        # GPT'deki LM Head
        self.lm_head = nn.Linear(
            embedding_dim,
            vocab_size,
            bias=False
        )

        # İleride weight tying için:
        # self.lm_head.weight = self.embedding.token_embedding.embedding.weight

    def forward(self, input_ids):

        x = self.embedding(input_ids)

        x, attention_maps = self.transformer(x)

        logits = self.lm_head(x)

        return logits, attention_maps

    @torch.no_grad()
    def predict(self, input_ids):

        self.eval()

        logits, _ = self.forward(input_ids)

        next_token = torch.argmax(
            logits[:, -1, :],
            dim=-1
        )

        return next_token
