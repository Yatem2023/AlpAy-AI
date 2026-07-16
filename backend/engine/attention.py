"""
AlpAy Engine
Attention Module

Part 1

Scaled Dot Product Attention
"""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class CausalMask:

    """
    GPT tipi causal mask üretir.

    Gelecekteki tokenlara bakılmasını engeller.
    """

    @staticmethod
    def create(seq_length, device):

        mask = torch.triu(

            torch.ones(

                seq_length,

                seq_length,

                device=device

            ),

            diagonal=1

        )

        return mask.bool()


class ScaledDotProductAttention(nn.Module):

    """
    Scaled Dot Product Attention

    Attention(Q,K,V)
    """

    def __init__(

        self,

        dropout=0.1

    ):

        super().__init__()

        self.dropout = nn.Dropout(dropout)

    def forward(

        self,

        query,

        key,

        value,

        mask=None

    ):

        d_k = query.size(-1)

        scores = torch.matmul(

            query,

            key.transpose(-2, -1)

        )

        scores = scores / math.sqrt(d_k)

        if mask is not None:

            scores = scores.masked_fill(

                mask,

                float("-inf")

            )

        attention = F.softmax(

            scores,

            dim=-1

        )

        attention = self.dropout(attention)

        output = torch.matmul(

            attention,

            value

        )

        return output, attention


if __name__ == "__main__":

    batch = 2

    seq = 8

    head_dim = 32

    q = torch.randn(

        batch,

        seq,

        head_dim

    )

    k = torch.randn(

        batch,

        seq,

        head_dim

    )

    v = torch.randn(

        batch,

        seq,

        head_dim

    )

    mask = CausalMask.create(

        seq,

        q.device

    )

    attention = ScaledDotProductAttention()

    out, weights = attention(

        q,

        k,

        v,

        mask

    )

    print()

    print("Output")

    print(out.shape)

    print()

    print("Attention")

    print(weights.shape)