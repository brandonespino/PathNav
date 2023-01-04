import torch
import os
import numpy as np
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
# import matplotlib.pyplot as plt

class pathDataset(Dataset):
    def __init__(self, imgs_dir, transform):
        self.imgs_dir = imgs_dir
        self.transform = transform
        self.all_imgs = os.listdir(imgs_dir)
    def __len__(self):
        return len(self.all_imgs)
    def __getitem__(self, idx):
        img_loc = os.path.join(self.imgs_dir, self.all_imgs[idx])
        image = Image.open(img_loc)
        tensor_image = self.transform(image)
        return tensor_image

colorjitter = transforms.ColorJitter(.2,.3,.4,.5) # random values for now
grey = transforms.Grayscale(num_output_channels=1) # single channel image, 3 channels has r=g=b greyscale
tensor = transforms.ToTensor()
resize = transforms.Resize(size=[144, 256])
transfm = transforms.Compose([grey, colorjitter, resize, tensor])

dataset = pathDataset('practice_images', transform=transfm)
train_loader = DataLoader(dataset, batch_size=2, shuffle=True)

for idx, images in enumerate(train_loader): # images is tensor 32, 3, 720, 1280
    print(images.shape)
    # plt.imshow(images[0].permute(1, 2, 0))
    print('image showing?')
    break

test_img = torch.rand(3, 144, 256)
test_batch = torch.rand(32, 3, 144, 256)

