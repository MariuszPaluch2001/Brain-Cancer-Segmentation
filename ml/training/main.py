from utils.file_paths import get_paths
from utils.device import get_device
from utils.plot import output_scatter_plot
from utils.measures import dice, recall, precission, f1

from models.unet import UNet2D
from dataset import Brain_MRI_Dataset
from torch.utils.data import random_split, DataLoader
from torchvision import transforms
from torch.nn import BCEWithLogitsLoss
import torch

BATCH_SIZE = 8
LR = 0.01
TRAIN_DATASET = 0.8
MOMENTUM = 0.99
EPOCHS = 70

device = get_device()

print(f"Device: {device}")

image_paths, mask_paths = get_paths()

transform = transforms.Compose(
    [
        transforms.PILToTensor(),
        transforms.ConvertImageDtype(torch.float),
    ]
)

transform_mask = transforms.Compose(
    [
        transforms.PILToTensor(),
        transforms.ConvertImageDtype(torch.float),
    ]
)

dataset = Brain_MRI_Dataset(image_paths, mask_paths, transform, transform_mask)

train_dataset, test_dataset = random_split(dataset, [TRAIN_DATASET, 1 - TRAIN_DATASET])

train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=False)

model = UNet2D(3, 1).to(device)

model.train()

optimizer = torch.optim.SGD(model.parameters(), lr=LR, momentum=MOMENTUM)

loss_fn = BCEWithLogitsLoss()

for epoch in range(0, EPOCHS):
    print(f"Started epoch {epoch}")
    total_loss = 0.0
    losses = []
    for i, (data, mask) in enumerate(train_dataloader):
        data = data.to(device)
        mask = mask.to(device)
        optimizer.zero_grad()

        output = model(data)
        loss = loss_fn(output, mask)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        losses.append(loss.item())

    print(f"[{epoch}] Avg loss: {total_loss / len(train_dataloader)}")

model.eval()

sum_dice = 0.0
sum_recall = 0.0
sum_precission = 0.0
sum_f1 = 0.0

for idx, (data, mask) in enumerate(test_dataloader):
    data = data.to(device)
    mask = mask.to(device)
    output = model(data)
    output[output >= 0.0] = 1
    output[output < 0.0] = 0

    output = output.squeeze(0).squeeze(0).detach().cpu()
    mask = mask.squeeze(0).squeeze(0).detach().cpu()

    dice_coeff = dice(output, mask, 1)
    recall_coeff = recall(output, mask)
    precission_coeff = precission(output, mask)
    f1_coeff = f1(output, mask)

    sum_dice += dice_coeff
    sum_recall += recall_coeff
    sum_precission += precission_coeff
    sum_f1 += f1_coeff

    print(
        f"Precission: {precission_coeff}, Recall: {recall_coeff}, F1: {f1_coeff}, Dice: {dice_coeff}"
    )
    output_scatter_plot(data.squeeze(0), output.unsqueeze(0), mask.unsqueeze(0), idx)

print(f"Avg precission: {sum_precission / len(test_dataloader)}")
print(f"Avg recall: {sum_recall / len(test_dataloader)}")
print(f"Avg f1: {sum_f1 / len(test_dataloader)}")
print(f"Avg dice: {sum_dice / len(test_dataloader)}")

torch.save(model.state_dict(), "models/unet.pt")

import shutil

shutil.copytree("models/", "../model_microservice/models", dirs_exist_ok=True)
