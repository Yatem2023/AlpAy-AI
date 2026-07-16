"""
AlpAy Engine
Transformer Layers
Version: 0.1
"""

import torch
import torch.nn as nn


class LayerNorm(nn.Module):

    def __init__(
        self,
        embedding_dim,
        eps=1e-5
    ):
        super().__init__()

        self.gamma = nn.Parameter(
            torch.ones(embedding_dim)
        )

        self.beta = nn.Parameter(
            torch.zeros(embedding_dim)
        )

        self.eps = eps


    def forward(self, x):

        mean = x.mean(
            dim=-1,
            keepdim=True
        )

        variance = x.var(
            dim=-1,
            keepdim=True,
            unbiased=False
        )

        x = (x - mean) / torch.sqrt(
            variance + self.eps
        )

        return self.gamma * x + self.beta



class FeedForward(nn.Module):

    """
    Transformer FFN

    Embedding
        |
    Linear
        |
    GELU
        |
    Linear
        |
    Output
    """

    def __init__(
        self,
        embedding_dim,
        hidden_dim,
        dropout=0.1
    ):
        super().__init__()

        self.net = nn.Sequential(

            nn.Linear(
                embedding_dim,
                hidden_dim
            ),

            nn.GELU(),

            nn.Linear(
                hidden_dim,
                embedding_dim
            ),

            nn.Dropout(
                dropout
            )
        )


    def forward(self, x):

        return self.net(x)
