# -*- coding: utf-8 -*-
import torch
import torch.nn.functional as F

# Giả sử encoder tạo hai views cùng ảnh và một view ảnh khác.
# Đây là embeddings fixture để hiểu contrastive score, không output DINO thật.
anchor=torch.tensor([[1.,0.]])
views=torch.tensor([[.9,.1],[0.,1.]])
anchor=F.normalize(anchor,dim=1); views=F.normalize(views,dim=1)
similarity=anchor@views.T
logits=similarity/.1
loss=F.cross_entropy(logits,torch.tensor([0]))
print("Similarities:",similarity.round(decimals=4).tolist())
print("Contrastive CE:",round(loss.item(),6))
assert similarity[0,0]>similarity[0,1]
# Thực hành pretrained SSL thật theo DINOv2 docs trong bài, không nhầm fixture với checkpoint.
