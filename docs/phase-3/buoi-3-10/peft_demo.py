# -*- coding: utf-8 -*-
# Ví dụ LoRA cho BERT classification; cần base checkpoint BERT đã cấp.
import argparse
import torch
from transformers import AutoTokenizer,AutoModelForSequenceClassification
from peft import LoraConfig,TaskType,get_peft_model
ap=argparse.ArgumentParser();ap.add_argument("--model",required=True);args=ap.parse_args()
tokenizer=AutoTokenizer.from_pretrained(args.model,local_files_only=True)
base=AutoModelForSequenceClassification.from_pretrained(args.model,num_labels=3,
    ignore_mismatched_sizes=True,local_files_only=True,trust_remote_code=False)
config=LoraConfig(task_type=TaskType.SEQ_CLS,r=4,lora_alpha=8,lora_dropout=.05,
                  target_modules=["query","value"])
model=get_peft_model(base,config);model.print_trainable_parameters()
inputs=tokenizer(["students read books","rain hits the city","team wins match"],
                  padding=True,truncation=True,max_length=64,return_tensors="pt")
labels=torch.tensor([0,1,2],dtype=torch.long)
optimizer=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=1e-3)
model.train();optimizer.zero_grad();loss=model(**inputs,labels=labels).loss
loss.backward();optimizer.step();print("Một train step:",loss.item())
model.save_pretrained("adapter_demo")
# Đây chỉ một step minh họa; dùng validation để train hoàn chỉnh trước báo chất lượng.
