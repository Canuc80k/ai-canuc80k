# -*- coding: utf-8 -*-
# Chạy: python bert_demo.py --model local_bert --text "students read books"
import argparse
import torch
from transformers import AutoTokenizer,AutoModel
ap=argparse.ArgumentParser();ap.add_argument("--model",required=True);ap.add_argument("--text",required=True);args=ap.parse_args()
tokenizer=AutoTokenizer.from_pretrained(args.model,local_files_only=True)
model=AutoModel.from_pretrained(args.model,local_files_only=True,trust_remote_code=False);model.eval()
inputs=tokenizer([args.text],padding=True,truncation=True,max_length=64,return_tensors="pt")
with torch.no_grad():output=model(**inputs)
mask=inputs["attention_mask"].unsqueeze(-1)
pooled=(output.last_hidden_state*mask).sum(1)/mask.sum(1)
print("IDs:",inputs["input_ids"].tolist())
print("Hidden:",tuple(output.last_hidden_state.shape),"Pooled:",tuple(pooled.shape))
# Muốn class probabilities cần head đã học đúng task; pooled features chưa phải predictions.
