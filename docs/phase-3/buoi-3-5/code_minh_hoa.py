# -*- coding: utf-8 -*-
import torch
from torch import nn
from torch.utils.data import TensorDataset,DataLoader
torch.manual_seed(42)
torch.set_num_threads(1)

X = torch.linspace(-1,1,40).reshape(-1,1)
y = 2*X+1
loader = DataLoader(TensorDataset(X,y),batch_size=8,shuffle=False)
model = nn.Linear(1,1)
optimizer = torch.optim.SGD(model.parameters(),lr=.1)
loss_fn = nn.MSELoss()
for epoch in range(8):
    model.train(); total = 0.0
    for xb,yb in loader:
        optimizer.zero_grad(); loss = loss_fn(model(xb),yb)
        loss.backward(); optimizer.step(); total += loss.item()*len(xb)
    print("epoch",epoch,"loss",round(total/len(X),6))
model.eval()
with torch.no_grad(): print("x=0 ->",round(model(torch.zeros(1,1)).item(),4))
# Số phần tử batch cuối có thể khác; metric epoch phải cân theo số mẫu.
