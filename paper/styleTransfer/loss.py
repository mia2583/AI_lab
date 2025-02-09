import torch
import torch.nn as nn
import torch.nn.functional as F

# content loss - vgg19 feature map
class ContentLoss(nn.Module):
    def __init__(self):
        super(ContentLoss, self).__init__()
    
    def forward(self, x:torch.Tensor, y:torch.Tensor):
        loss = F.mse_loss(x, y)
        return loss


# style loss - gram matrix
class StyleLoss(nn.Module):
    def __init__(self):
        super(StyleLoss, self).__init__()

    def gram_matrix(self, x:torch.Tensor):
        b, c, h, w = x.size()
        features = x.view(b, c, h*w) # (b, N,M)
        features_T = features.transpose(1, 2) # (b, M,N)
        G = torch.matmul(features, features_T) # (b,N, N)
        return G.div(b*c*h*w)
    
    def forward(self, x, y):
        Gx = self.gram_matrix(x)
        Gy = self.gram_matrix(y)
        loss = F.mse_loss(Gx, Gy)
        return loss