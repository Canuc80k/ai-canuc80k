# -*- coding: utf-8 -*-
import torch
from torch import nn
from torchvision.models import resnet18
torch.manual_seed(42)
torch.set_num_threads(1)

# weights=None minh họa architecture và freezing, KHÔNG phải pretrained model.
model=resnet18(weights=None)
for p in model.parameters(): p.requires_grad=False
model.fc=nn.Linear(model.fc.in_features,3)
model.eval()
X=torch.randn(2,3,64,64)
with torch.no_grad(): output=model(X)
print("Output shape:",tuple(output.shape))
print("Params cần train:",sum(p.numel() for p in model.parameters() if p.requires_grad))
print("Ví dụ này không đo chất lượng transfer learning.")
assert tuple(output.shape)==(2,3)
# Bài thực hành thật: dùng checkpoint được cấp trong nguồn và transforms đúng weights.
