# -*- coding: utf-8 -*-
import torch
torch.manual_seed(42)
torch.set_num_threads(1)

x = torch.tensor(2.0,requires_grad=True)
y = x*x+3*x
y.backward()
print("y:",y.item(),"dy/dx:",x.grad.item())
matrix = torch.arange(6,dtype=torch.float32).reshape(2,3)
print("shape:",tuple(matrix.shape),"dtype:",matrix.dtype,"device:",matrix.device)
assert x.grad.item()==7
# Numpy array không mang graph autograd của torch.
