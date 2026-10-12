# -*- coding: utf-8 -*-
import torch
from torch import nn
torch.manual_seed(42)

dropout = nn.Dropout(p=.5)
X = torch.ones(1,8)
dropout.train(); a = dropout(X)
dropout.eval(); b = dropout(X)
print("train dropout:",a.tolist())
print("eval dropout:",b.tolist())
losses = [.8,.6,.65,.7]
best=float("inf"); patience=2; bad=0; best_epoch=None
for epoch,loss in enumerate(losses,1):
    if loss<best: best=loss; best_epoch=epoch; bad=0
    else: bad+=1
    if bad>=patience:
        print("stop",epoch,"restore best epoch",best_epoch); break
assert torch.equal(b,X) and best_epoch==2
