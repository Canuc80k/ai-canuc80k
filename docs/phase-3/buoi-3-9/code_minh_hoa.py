# -*- coding: utf-8 -*-
import torch
from torch import nn
from sklearn.datasets import load_digits
torch.manual_seed(42)
torch.set_num_threads(1)

X = torch.tensor(load_digits().data[:128]/16,dtype=torch.float32)
encoder = nn.Sequential(nn.Linear(64,16),nn.ReLU(),nn.Linear(16,4))
decoder = nn.Sequential(nn.Linear(4,16),nn.ReLU(),nn.Linear(16,64),nn.Sigmoid())
optimizer = torch.optim.Adam(list(encoder.parameters())+list(decoder.parameters()),lr=.01)
for step in range(20):
    optimizer.zero_grad(); latent=encoder(X); reconstruction=decoder(latent)
    loss=((reconstruction-X)**2).mean(); loss.backward(); optimizer.step()
print("input",tuple(X.shape),"latent",tuple(latent.shape),"reconstruction",tuple(reconstruction.shape))
print("Training reconstruction loss:",round(loss.item(),5))
# Không có nhãn chữ số đi vào loss; loss tái tạo không phải accuracy phân loại.
