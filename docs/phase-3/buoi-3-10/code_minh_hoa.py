# -*- coding: utf-8 -*-
import torch
from torch import nn
torch.manual_seed(42)

# Minh họa cơ chế LoRA ở một linear layer nhỏ, không giả là fine-tune LLM.
d,r = 4,2
base = nn.Linear(d,d,bias=False)
for p in base.parameters(): p.requires_grad=False
A = nn.Parameter(torch.randn(r,d)*.01)
B = nn.Parameter(torch.zeros(d,r))
X = torch.ones(3,d)
output = base(X)+X@A.T@B.T
loss = output.square().mean(); loss.backward()
print("Base params:",sum(p.numel() for p in base.parameters()))
print("Adapter params:",A.numel()+B.numel())
print("Base grad:",base.weight.grad)
print("B có gradient:",B.grad is not None)
assert base.weight.grad is None and A.numel()+B.numel()==16
