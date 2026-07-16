"""
AlpAy Engine
Transformer Block
Version: 0.1
"""

import torch
import torch.nn as nn

from .attention import MultiHeadAttention
from .layers import LayerNorm, FeedForward


class TransformerBlock(nn.Module):

    def __init__(
        self,
        embedding_dim: int,
        num_heads: int,
        ff_hidden_dim: int,
        dropout: float = 0.1
    ):
        super().__init__()

        self.norm1 = LayerNorm(embedding_dim)

        self.attention = MultiHeadAttention(
            embedding_dim=embedding_dim,
            num_heads=num_heads,
            dropout=dropout
        )

        self.dropout1 = nn.Dropout(dropout)

        self.norm2 = LayerNorm(embedding_dim)

        self.feed_forward = FeedForward(
            embedding_dim=embedding_dim,
            hidden_dim=ff_hidden_dim,
            dropout=dropout
        )

        self.dropout2 = nn.Dropout(dropout)

    def forward(self, x):

        residual = x

        x = self.norm1(x)

        attn_output, attention = self.attention(x)

        x = residual + self.dropout1(attn_output)

        residual = x

        x = self.norm2(x)

        ff_output = self.feed_forward(x)

        x = residual + self.dropout2(ff_output)

        return x, attention
class Transformer(nn.Module):

    """
    AlpAy Transformer Stack
    """

    def __init__(
        self,
        num_layers: int,
        embedding_dim: int,
        num_heads: int,
        ff_hidden_dim: int,
        dropout: float = 0.1
    ):

        super().__init__()

        self.layers = nn.ModuleList(

            [

                TransformerBlock(

                    embedding_dim=embedding_dim,

                    num_heads=num_heads,

                    ff_hidden_dim=ff_hidden_dim,

                    dropout=dropout

                )

                for _ in range(num_layers)

            ]

        )

        self.norm = LayerNorm(

            embedding_dim

        )

    def forward(self, x):

        attention_maps = []

        for layer in self.layers:

            x, attention = layer(x)

            attention_maps.append(attention)

        x = self.norm(x)

        return x, attention_maps
