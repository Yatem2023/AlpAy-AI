"""
AlpAy Engine
Embedding Layer
Version: 0.1
"""

import math
import torch
import torch.nn as nn


class TokenEmbedding(nn.Module):

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int
    ):

        super().__init__()

        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embedding_dim
        )

        self.scale = math.sqrt(embedding_dim)

    def forward(self, tokens):

        return self.embedding(tokens) * self.scale


class PositionalEncoding(nn.Module):

    def __init__(
        self,
        embedding_dim: int,
        max_length: int = 4096
    ):

        super().__init__()

        pe = torch.zeros(
            max_length,
            embedding_dim
        )

        position = torch.arange(
            0,
            max_length,
            dtype=torch.float
        ).unsqueeze(1)

        div_term = torch.exp(

            torch.arange(
                0,
                embedding_dim,
                2
            ).float()

            *

            (
                -math.log(10000.0)
                /
                embedding_dim
            )

        )

        pe[:, 0::2] = torch.sin(
            position * div_term
        )

        pe[:, 1::2] = torch.cos(
            position * div_term
        )

        pe = pe.unsqueeze(0)

        self.register_buffer(
            "pe",
            pe
        )

    def forward(self, x):

        seq_len = x.size(1)

        return x + self.pe[:, :seq_len]


class EmbeddingLayer(nn.Module):

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int,
        dropout: float = 0.1
    ):

        super().__init__()

        self.token_embedding = TokenEmbedding(
            vocab_size,
            embedding_dim
        )

        self.position_embedding = PositionalEncoding(
            embedding_dim
        )

        self.dropout = nn.Dropout(
            dropout
        )

    def forward(self, tokens):

        x = self.token_embedding(tokens)

        x = self.position_embedding(x)

        x = self.dropout(x)

        return x


if __name__ == "__main__":

    VOCAB = 5000

    EMBED = 128

    layer = EmbeddingLayer(

        vocab_size=VOCAB,

        embedding_dim=EMBED

    )

    sample = torch.randint(

        0,

        VOCAB,

        (2, 16)

    )

    out = layer(sample)

    print(out.shape)