"""
AlpAy Engine
Loss Functions
"""

import torch
import torch.nn as nn


class LanguageModelLoss(nn.Module):

    def __init__(self):

        super().__init__()

        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, logits, targets):

        """
        logits:
        (batch, seq, vocab)

        targets:
        (batch, seq)
        """

        batch, seq, vocab = logits.shape

        logits = logits.view(
            batch * seq,
            vocab
        )

        targets = targets.view(
            batch * seq
        )

        return self.loss_fn(
            logits,
            targets
        )