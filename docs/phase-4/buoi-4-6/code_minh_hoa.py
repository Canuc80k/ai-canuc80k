# -*- coding: utf-8 -*-
import numpy as np
import torch
from torch import nn

true=np.array([[1,0],[1,0]],dtype=bool)
pred=np.array([[1,1],[1,0]],dtype=bool)
intersection=(true&pred).sum(); union=(true|pred).sum()
print("IoU:",round(float(intersection/union),6))
print("Dice:",float(2*intersection/(true.sum()+pred.sum())))
# Skip connection nối theo channel, không nối theo chiều ảnh.
skip=torch.ones(1,2,4,4); up=torch.zeros(1,2,4,4)
joined=torch.cat([up,skip],dim=1)
head=nn.Conv2d(4,2,1)
print("Joined shape:",tuple(joined.shape),"logits shape:",tuple(head(joined).shape))
assert tuple(head(joined).shape)==(1,2,4,4)
