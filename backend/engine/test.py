from torch.utils.data import DataLoader

from dataset import TextDataset

dataset = TextDataset(
    context_length=16
)

loader = DataLoader(
    dataset,
    batch_size=4,
    shuffle=True
)

for x, y in loader:

    print(x.shape)

    print(y.shape)

    break