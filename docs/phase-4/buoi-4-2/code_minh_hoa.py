# -*- coding: utf-8 -*-
import torch
from torch import nn
from sklearn.datasets import load_digits
torch.manual_seed(42)
torch.set_num_threads(1)

digits=load_digits(); X=torch.tensor(digits.images[:200]/16,dtype=torch.float32).unsqueeze(1)
y=torch.tensor(digits.target[:200],dtype=torch.long)
model=nn.Sequential(nn.Conv2d(1,8,3,padding=1),nn.ReLU(),nn.MaxPool2d(2),
                    nn.Flatten(),nn.Linear(8*4*4,10))
optimizer=torch.optim.Adam(model.parameters(),lr=.02)
for step in range(20):
    optimizer.zero_grad(); logits=model(X)
    loss=nn.CrossEntropyLoss()(logits,y); loss.backward(); optimizer.step()
with torch.no_grad(): pred=model(X).argmax(1)
print("Input:",tuple(X.shape),"logits:",tuple(logits.shape))
print("Training accuracy:",round((pred==y).float().mean().item(),4))
# Accuracy trên train chỉ kiểm loop; muốn so model cần split độc lập.
