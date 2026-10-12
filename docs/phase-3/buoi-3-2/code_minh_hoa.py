# -*- coding: utf-8 -*-
import torch
from torch.utils.data import TensorDataset,DataLoader
torch.manual_seed(42)

X = torch.arange(18,dtype=torch.float32).reshape(9,2)
y = torch.arange(9)%2
ids = torch.arange(9)
dataset = TensorDataset(X,y,ids)
loader = DataLoader(dataset,batch_size=4,shuffle=False,drop_last=False)
seen = []
for features,labels,batch_ids in loader:
    print("batch shape",tuple(features.shape),"ids",batch_ids.tolist())
    seen.extend(batch_ids.tolist())
assert seen==list(range(9))
# Khi shuffle inference, phải sắp output lại theo ID, không theo thứ tự batch.
