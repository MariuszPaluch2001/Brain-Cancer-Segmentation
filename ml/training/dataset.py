from torch.utils.data import Dataset
from PIL import Image


class Brain_MRI_Dataset(Dataset):
    def __init__(
        self, image_paths, mask_paths, img_transform=None, mask_transform=None
    ):
        self.image_paths = image_paths
        self.mask_paths = mask_paths

        self.img_transform = img_transform
        self.mask_transform = mask_transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_file = self.image_paths[idx]
        mask_file = self.mask_paths[idx]

        img = Image.open(img_file)
        mask = Image.open(mask_file)

        if self.img_transform:
            img = self.img_transform(img)
        if self.mask_transform:
            mask = self.mask_transform(mask)

        mask[mask == 255] = 1
        mask[mask == 0] = 0

        return img, mask
