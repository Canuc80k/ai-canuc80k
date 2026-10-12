# -*- coding: utf-8 -*-
import torch
from torch import nn
torch.manual_seed(7)
torch.set_num_threads(1)

X = torch.tensor([[0.,0.],[0.,1.],[1.,0.],[1.,1.]])
y = torch.tensor([[0.],[1.],[1.],[0.]])  # XOR
model = nn.Sequential(nn.Linear(2,8),nn.Tanh(),nn.Linear(8,1))
optimizer = torch.optim.Adam(model.parameters(),lr=.05)
loss_fn = nn.BCEWithLogitsLoss()
for step in range(200):
    optimizer.zero_grad()
    logits = model(X)
    loss = loss_fn(logits,y)
    loss.backward()
    optimizer.step()
with torch.no_grad():
    probabilities = model(X).sigmoid()
print("Params:",sum(p.numel() for p in model.parameters()))
print("P(XOR=1):",probabilities.flatten().round(decimals=3).tolist())
print("Labels:",(probabilities>=.5).int().flatten().tolist())
assert (probabilities>=.5).int().flatten().tolist()==[0,1,1,0]
