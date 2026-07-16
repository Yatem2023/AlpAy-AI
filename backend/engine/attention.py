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

class MultiHeadAttention(nn.Module):

    """
    GPT tarzı Multi Head Self Attention
    """

    def __init__(
        self,
        embedding_dim,
        num_heads,
        dropout=0.1
    ):

        super().__init__()

        if embedding_dim % num_heads != 0:
            raise ValueError(
                "embedding_dim num_heads'e tam bölünmelidir."
            )

        self.embedding_dim = embedding_dim
        self.num_heads = num_heads
        self.head_dim = embedding_dim // num_heads

        # QKV projeksiyonları
        self.q_proj = nn.Linear(
            embedding_dim,
            embedding_dim
        )

        self.k_proj = nn.Linear(
            embedding_dim,
            embedding_dim
        )

        self.v_proj = nn.Linear(
            embedding_dim,
            embedding_dim
        )

        # Çıkış projeksiyonu
        self.out_proj = nn.Linear(
            embedding_dim,
            embedding_dim
        )

        self.attention = ScaledDotProductAttention(
            dropout=dropout
        )

        self.dropout = nn.Dropout(
            dropout
        )

    def split_heads(self, x):

        batch, seq, _ = x.shape

        x = x.view(
            batch,
            seq,
            self.num_heads,
            self.head_dim
        )

        x = x.transpose(1, 2)

        return x

    def merge_heads(self, x):

        batch, heads, seq, dim = x.shape

        x = x.transpose(1, 2)

        x = x.contiguous()

        x = x.view(
            batch,
            seq,
            heads * dim
        )

        return x

    def forward(self, x):

        batch, seq, _ = x.shape

        q = self.q_proj(x)
        k = self.k_proj(x)
        v = self.v_proj(x)

        q = self.split_heads(q)
        k = self.split_heads(k)
        v = self.split_heads(v)

        mask = CausalMask.create(
            seq,
            x.device
        )

        mask = mask.unsqueeze(0).unsqueeze(0)

        out, attention = self.attention(
            q,
            k,
            v,
            mask
        )

        out = self.merge_heads(out)

        out = self.out_proj(out)

        out = self.dropout(out)

        return out, attention
