# -*- coding: utf-8 -*-
import torch,math
from torch import nn
torch.manual_seed(42)
torch.set_num_threads(1)

# Hai tokens, dimension2. Giá trị bên phải là token sẽ bị mask.
Q = torch.tensor([[1.,0.]])
K = torch.tensor([[1.,0.],[0.,1.]])
V = torch.tensor([[10.,0.],[0.,20.]])
score = Q@K.T/math.sqrt(2)
weights = torch.softmax(score,dim=-1)
print("Weights:",weights.round(decimals=4).tolist())
print("Output:",(weights@V).round(decimals=4).tolist())
masked = score.masked_fill(torch.tensor([[False,True]]),float("-inf"))
print("Masked output:",(torch.softmax(masked,-1)@V).tolist())
layer = nn.TransformerEncoderLayer(d_model=4,nhead=2,dim_feedforward=8,
                                   dropout=0,batch_first=True)
layer.eval(); tokens = torch.arange(12,dtype=torch.float32).reshape(1,3,4)
with torch.no_grad(): print("Transformer shape:",tuple(layer(tokens).shape))
assert (torch.softmax(masked,-1)@V).tolist()==[[10.,0.]]
