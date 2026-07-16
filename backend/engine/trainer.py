"""
AlpAy Engine
Trainer
"""

import torch

from loss import LanguageModelLoss

from optimizer import create_optimizer


class Trainer:

    def __init__(

        self,

        model,

        dataloader,

        device="cpu",

        lr=3e-4

    ):

        self.model = model.to(device)

        self.dataloader = dataloader

        self.device = device

        self.loss_fn = LanguageModelLoss()

        self.optimizer = create_optimizer(

            self.model,

            learning_rate=lr

        )

    def train_epoch(self):

        self.model.train()

        total_loss = 0

        for inputs, targets in self.dataloader:

            inputs = inputs.to(self.device)

            targets = targets.to(self.device)

            logits, _ = self.model(inputs)

            loss = self.loss_fn(

                logits,

                targets

            )

            self.optimizer.zero_grad()

            loss.backward()

            self.optimizer.step()

            total_loss += loss.item()

        return total_loss / len(self.dataloader)

    def train(

        self,

        epochs

    ):

        for epoch in range(epochs):

            loss = self.train_epoch()

            print(

                f"Epoch {epoch+1}/{epochs}"

            )

            print(

                f"Loss: {loss:.4f}"

            )