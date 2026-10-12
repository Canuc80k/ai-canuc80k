# -*- coding: utf-8 -*-
# Chạy: python ssl_demo.py --model local_dinov2 --image sample.png
import argparse
import torch
from PIL import Image
from transformers import AutoImageProcessor,AutoModel
ap=argparse.ArgumentParser();ap.add_argument("--model",required=True);ap.add_argument("--image",required=True);args=ap.parse_args()
processor=AutoImageProcessor.from_pretrained(args.model,local_files_only=True)
model=AutoModel.from_pretrained(args.model,local_files_only=True,trust_remote_code=False)
model.eval();image=Image.open(args.image).convert("RGB")
inputs=processor(images=image,return_tensors="pt")
with torch.no_grad():output=model(**inputs)
print("Token hidden states:",tuple(output.last_hidden_state.shape))
features=output.last_hidden_state[:,0]
print("CLS features:",tuple(features.shape))
# Đây là DINOv2 khi --model thực sự là checkpoint DINOv2; giữ config/model revision.
