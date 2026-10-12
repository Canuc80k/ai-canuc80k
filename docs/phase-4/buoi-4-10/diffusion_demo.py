# -*- coding: utf-8 -*-
# Chạy: python diffusion_demo.py --model local_ddpm_pipeline --out sample.png
import argparse
import torch
from diffusers import DDPMPipeline
ap=argparse.ArgumentParser();ap.add_argument("--model",required=True);ap.add_argument("--out",default="sample.png");args=ap.parse_args()
pipeline=DDPMPipeline.from_pretrained(args.model,local_files_only=True,torch_dtype=torch.float32)
pipeline=pipeline.to("cpu")
generator=torch.Generator(device="cpu").manual_seed(42)
result=pipeline(num_inference_steps=10,generator=generator)
result.images[0].save(args.out)
print("Ảnh đã lưu:",args.out)
# Model+scheduler cần tương thích.10 steps chỉ demo pipeline, không hứa chất lượng tốt.
