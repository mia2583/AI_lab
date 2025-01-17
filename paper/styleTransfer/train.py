import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
import os

import numpy as np
from PIL import Image

from models import StyleTransfer
from loss import ContentLoss, StyleLoss
from tqdm import tqdm

mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

# image -> tensor (1, c, h, w)
def pre_processing(image:Image.Image) -> torch.Tensor:
    preprocessing = T.Compose([
        T.Resize((512, 512)),
        T.ToTensor(),
        T.Normalize(mean, std)
    ]) # (c, h, w)

    image_tensor:torch.Tensor = preprocessing(image) 

    return image_tensor.unsqueeze(0) # (1, c, h, w)


# tensor (1, c, w) -> image
def post_processing(tensor:torch.Tensor) -> Image.Image:
    image:np.ndarray = tensor.detach().numpy() # (1, c, h, w)
    image = image.squeeze() #(c, h, w)
    image = image.transpose(1, 2, 0) #(h, w, c)
    image = image*std + mean # de-norm
    image = image.clip(0, 1)*255 # 이미지 값 범위 제한
    image = image.astype(np.uint8)
    return Image.fromarray(image) # ndarry to image


def train_main():
    # load data
    content_image = Image.open('./content.jpg')
    content_image = pre_processing(content_image)

    style_image = Image.open('./style.jpg')
    style_image = pre_processing(style_image)

    # load model
    style_transfer = StyleTransfer().eval()

    # load loss
    content_loss = ContentLoss()
    style_loss = StyleLoss()

    # hyper parameter
    alpha = 1
    beta = 1e6
    lr = 1

    save_root = f'{alpha}_{beta}_{lr}_initContent_style_LBFGS'
    os.makedirs(save_root, exist_ok=True)

    # start image
    x = content_image.clone()
    x.requires_grad_(True)

    # optimizer
    optimizer = optim.LBFGS([x], lr=lr) 

    def closure():
        optimizer.zero_grad()

        x_content_list = style_transfer(x, 'content')
        y_content_list = style_transfer(content_image, 'content')

        x_style_list = style_transfer(x, 'style')
        y_style_list = style_transfer(style_image, 'style')

        # loss
        loss_c = 0
        loss_s = 0
        loss_total = 0

        for x_content, y_content in zip(x_content_list, y_content_list) :
            loss_c += content_loss(x_content, y_content)

        for x_style, y_style in zip(x_style_list, y_style_list) :
            loss_s += style_loss(x_style, y_style)
    
        loss_total = alpha*loss_c + beta*loss_s

        loss_total.backward()

        return loss_total


    # train loop
    steps = 1000
    for step in tqdm(range(steps)):
        optimizer.step(closure)

        # 중간에 학습 결과 따로 저장하기
        if step%100 == 0:
            with torch.no_grad():
                x_content_list = style_transfer(x, 'content')
                y_content_list = style_transfer(content_image, 'content')

                x_style_list = style_transfer(x, 'style')
                y_style_list = style_transfer(style_image, 'style')

                ## loss_content, loss_style
                loss_c = 0
                loss_s = 0
                loss_total = 0

                for x_content, y_content in zip(x_content_list, y_content_list):
                    loss_c += content_loss(x_content, y_content)
                loss_c = alpha*loss_c

                for x_style, y_style in zip(x_style_list, y_style_list):
                    loss_s += style_loss(x_style, y_style)
                loss_s = beta*loss_s

                loss_total = loss_c + loss_s

                print(f"loss_c: {loss_c.cpu()}")
                print(f"loss_s: {loss_s.cpu()}")
                print(f"loss_total: {loss_total.cpu()}")

                # post processing
                gen_image:Image.Image = post_processing(x)
                gen_image.save(os.path.join(save_root, 'result.jpg'))

if __name__ =="__main__":
    train_main()