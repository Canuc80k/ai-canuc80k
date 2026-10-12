# -*- coding: utf-8 -*-
import torch
from torch import nn

logits = torch.tensor([[1000.,1001.]])
prob = torch.softmax(logits,dim=1)
target = torch.tensor([1],dtype=torch.long)
loss = nn.CrossEntropyLoss()(logits,target)
print("Softmax:",prob.round(decimals=6).tolist())
print("Sum:",prob.sum().item(),"CE:",round(loss.item(),6))
binary_logits = torch.tensor([0.0])
binary_y = torch.tensor([1.0])
print("BCE logits:",round(nn.BCEWithLogitsLoss()(binary_logits,binary_y).item(),6))
assert torch.isfinite(prob).all() and torch.isfinite(loss)
# Không softmax trước CrossEntropyLoss, không sigmoid trước BCEWithLogitsLoss.
