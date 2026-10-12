# -*- coding: utf-8 -*-
# Chạy: python resnet_demo.py --weights resnet18.pth --image sample.png
import argparse
from pathlib import Path
import torch
from torch import nn
from PIL import Image
from torchvision.models import resnet18,ResNet18_Weights
ap=argparse.ArgumentParser();ap.add_argument("--weights",required=True);ap.add_argument("--image",required=True);args=ap.parse_args()
if not Path(args.weights).is_file():raise FileNotFoundError("Cần checkpoint ResNet18 đã được cấp")
torch.set_num_threads(1)
model=resnet18(weights=None)
model.load_state_dict(torch.load(args.weights,map_location="cpu",weights_only=True))
# Thay head bằng Identity để lấy pretrained features, không ImageNet label logits.
model.fc=nn.Identity();model.eval()
image=Image.open(args.image).convert("RGB")
preprocess=ResNet18_Weights.DEFAULT.transforms()
X=preprocess(image).unsqueeze(0)
with torch.no_grad():features=model(X)
print("Input:",tuple(X.shape),"Features:",tuple(features.shape))
print(features[0,:8].tolist())
# Fine-tune/probe: huấn luyện head mới trên train của task, không đánh giá bằng random head.
