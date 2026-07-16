"""
AlpAy Engine
Core Layers
Version: 0.1
"""

import torch
import torch.nn as nn


class LayerNorm(nn.Module):

    def __init__(self, dim, eps=1e-5):

        super().__init__()

        self.gamma = nn.Parameter(torch.ones(dim))
        self.beta = nn.Parameter(torch.zeros(dim))

        self.eps = eps

    def forward(self, x):

        mean = x.mean(dim=-1, keepdim=True)

        var = ((x - mean) ** 2).mean(dim=-1, keepdim=True)

        x = (x - mean) / torch.sqrt(var + self.eps)

        return self.gamma * x + self.beta


class GELU(nn.Module):

    def forward(self, x):

        return 0.5 * x * (

            1.0 +

            torch.tanh(

                0.7978845608 *

                (

                    x +

                    0.044715 *

                    torch.pow(x, 3)

                )

            )

        )


class FeedForward(nn.Module):

    def __init__(

        self,

        embedding_dim,

        hidden_dim,

        dropout=0.1

    ):

        super().__init__()

        self.linear1 = nn.Linear(

            embedding_dim,

            hidden_dim

        )

        self.activation = GELU()

        self.linear2 = nn.Linear(

            hidden_dim,

            embedding_dim

        )

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):

        x = self.linear1(x)

        x = self.activation(x)

        x = self.dropout(x)

        x = self.linear2(x)

        return x


class Residual(nn.Module):

    def __init__(self, module):

        super().__init__()

        self.module = module

    def forward(self, x):

        return x + self.module(x)


if __name__ == "__main__":

    sample = torch.randn(

        4,

        16,

        128

    )

    norm = LayerNorm(128)

    ffn = FeedForward(

        128,

        512

    )

    out = norm(sample)

    out = ffn(out)

    print(out.shape)