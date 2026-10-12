# -*- coding: utf-8 -*-
# Chạy: python clip_demo.py --model local_clip --images cat.png dog.png --texts "a cat" "a dog"
import argparse
import torch
from PIL import Image
from transformers import CLIPProcessor,CLIPModel
ap=argparse.ArgumentParser();ap.add_argument("--model",required=True);ap.add_argument("--images",nargs="+",required=True);ap.add_argument("--texts",nargs="+",required=True);args=ap.parse_args()
processor=CLIPProcessor.from_pretrained(args.model,local_files_only=True)
model=CLIPModel.from_pretrained(args.model,local_files_only=True);model.eval()
images=[Image.open(p).convert("RGB") for p in args.images]
inputs=processor(text=args.texts,images=images,return_tensors="pt",padding=True)
with torch.no_grad():result=model(**inputs)
scores=result.logits_per_image
for name,row in zip(args.images,scores):
    order=torch.argsort(row,descending=True).tolist()
    print(name,[(args.texts[i],round(row[i].item(),4)) for i in order])
# Logits có temperature scale; ranking không tự trở thành calibrated class probabilities.
