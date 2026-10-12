# -*- coding: utf-8 -*-
import torch
from torch import nn
torch.manual_seed(42)
torch.set_num_threads(1)

# GAN 1D: dữ liệu thật ở đây là Gaussian tổng hợp, không ảnh thực.
G=nn.Sequential(nn.Linear(1,8),nn.Tanh(),nn.Linear(8,1))
D=nn.Sequential(nn.Linear(1,8),nn.ReLU(),nn.Linear(8,1))
opt_G=torch.optim.Adam(G.parameters(),lr=.01); opt_D=torch.optim.Adam(D.parameters(),lr=.01)
loss_fn=nn.BCEWithLogitsLoss()
real=torch.randn(64,1)*.5+2; z=torch.randn(64,1)
opt_D.zero_grad(); fake=G(z).detach()
loss_D=loss_fn(D(real),torch.ones(64,1))+loss_fn(D(fake),torch.zeros(64,1))
loss_D.backward(); opt_D.step()
opt_G.zero_grad(); fake=G(z)
loss_G=loss_fn(D(fake),torch.ones(64,1))
loss_G.backward(); opt_G.step()
print("Một D step loss:",round(loss_D.item(),4))
print("Một G step loss:",round(loss_G.item(),4))
# Một update không đủ học distribution; bài GAN ảnh sử dụng DCGAN tutorial.
