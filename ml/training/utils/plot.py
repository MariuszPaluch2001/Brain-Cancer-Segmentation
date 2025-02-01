import os
import matplotlib.pyplot as plt
from torchvision import transforms


def output_scatter_plot(origin, scan, mask, idx):
    fig = plt.figure(figsize=(12, 8))
    fig.add_subplot(1, 3, 1)
    plt.imshow(transforms.ToPILImage()(origin))
    fig.add_subplot(1, 3, 2)
    plt.imshow(transforms.ToPILImage()(scan), cmap="gray")
    fig.add_subplot(1, 3, 3)
    plt.imshow(transforms.ToPILImage()(mask), cmap="gray")

    os.makedirs(f"results", exist_ok=True)
    plt.savefig(f"results/{idx}-{'true' if mask.sum().item() > 0 else 'false'}.png")
    plt.clf()
    plt.close()
