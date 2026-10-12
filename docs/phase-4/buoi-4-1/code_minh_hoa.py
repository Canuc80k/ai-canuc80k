# -*- coding: utf-8 -*-
import torch
from torch import nn

X = torch.arange(1,10,dtype=torch.float32).reshape(1,1,3,3)
conv = nn.Conv2d(1,1,kernel_size=2,bias=False)
with torch.no_grad(): conv.weight.copy_(torch.tensor([[[[1.,0.],[0.,-1.]]]]))
output = conv(X)
print("Input:",X[0,0].tolist())
print("Kernel:",conv.weight[0,0].detach().tolist())
print("Output:",output[0,0].detach().tolist())
print("MaxPool2x2:",nn.MaxPool2d(2)(X)[0,0].tolist())
assert torch.equal(output,torch.full((1,1,2,2),-4.))
# Conv2d thực hiện cross-correlation; không lật kernel ở ví dụ này.
