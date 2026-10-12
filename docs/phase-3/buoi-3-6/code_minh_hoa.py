# -*- coding: utf-8 -*-
import torch
from torch import nn
torch.set_num_threads(1)

X = torch.linspace(-1,1,50).reshape(-1,1); y = 3*X-2
for name,optimizer_type in [("SGD",torch.optim.SGD),("AdamW",torch.optim.AdamW)]:
    torch.manual_seed(42)  # Hai lần bắt đầu cùng weights.
    model = nn.Linear(1,1)
    optimizer = optimizer_type(model.parameters(),lr=.1)
    for step in range(40):
        optimizer.zero_grad(); loss = ((model(X)-y)**2).mean()
        loss.backward(); optimizer.step()
    print(name,"loss",round(loss.item(),6),"w",round(model.weight.item(),4))
# Đây là so sánh 40 updates trên fixture, không khẳng định optimizer nào luôn tốt.
