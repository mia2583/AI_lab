import torch
import torch.nn as nn
from torchvision.models import vgg19

# 사용할 conv 레이어
conv = {
    'conv1_1' : 0,  # style
    'conv2_1' : 5,  # style
    'conv3_1' : 10,  # style
    'conv4_1' : 19,  # style
    'conv5_1' : 28,  # style
    'conv4_2' : 21,  # content
}


class StyleTransfer(nn.Module):
    def __init__(self):
        super(StyleTransfer, self).__init__()
        #VGG 모델을 load해서 사용할 conv 레이어 분리
        self.vgg19_model = vgg19(pretrained=True) # pretrain 된 VGG19 모델 사용
        self.vgg19_features = self.vgg19_model.features

        self.style_layer = [conv['conv1_1'], conv['conv2_1'], conv['conv3_1'], conv['conv4_1'], conv['conv5_1']]
        self.content_layer = [conv['conv4_2']]

    def forward(self, x, layer_type:str):
        features = []
        if layer_type == 'style':
            layer = self.style_layer
        elif layer_type == 'content':
            layer = self.content_layer
        else : 
            print("No layer type : Choose 'style' or 'content'")
            return 
        # 종료 관련 정의하기

        for i in range(len(self.vgg19_features)):
            x = self.vgg19_features[i](x)
            if i in layer :
                features.append(x)

        return features
