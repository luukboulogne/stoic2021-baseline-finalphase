from torch.utils.data import Dataset
import torch
import os
import numpy as np
from torchio.transforms import Compose, RandomAffine, RandomNoise

class CTDataset(Dataset):
    def __init__(self, data, augment=False):
        self.data = data
        if augment:
            self.transform = Compose([
                RandomAffine(scales=0.1, degrees=15, translation=20),
                RandomNoise(std=(0, 0.05)),
            ])
        else:
            self.transform = lambda x: x

    def __len__(self):
        return len(self.data)

    def get_x(self, idx):
        return np.load(self.data[idx]['x'])

    def get_y(self, idx):
        return np.asarray(self.data[idx]['y']).astype(np.float32)

    def __getitem__(self, idx):
        x = self.get_x(idx)
        x = self.transform(np.expand_dims(x, axis=0))
        x = torch.from_numpy(x)
        y = torch.from_numpy(self.get_y(idx))
        return x, y


if __name__ == "__main__":
    import sys
    import glob
    import matplotlib.pyplot as plt

    image_dir = sys.argv[1]

    data = [
        {'x': filename, 'y': [0, 0]}
        for filename in glob.glob(os.path.join(image_dir, "*.mha"))
    ]
    ctdataset = CTDataset(data)

    steps = 4
    for x, y in ctdataset:
        print(y)
        print(x.shape)
        x = x.numpy()[0]
        length = x.shape[1]
        start = length // 3
        stop = (length // 5) * 4
        step = (stop - start) // steps
        fig, axes = plt.subplots(1, steps, figsize=(15, 4))
        its = range(start, stop, step)
        for it, axis in zip(its, axes):
            screenshot = x[:, it, :][::-1]
            axis.imshow(screenshot, cmap='gray')
            axis.axis('off')
        plt.suptitle(f'label: {y}')
        plt.show()

