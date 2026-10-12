# -*- coding: utf-8 -*-
import torch
from torch import nn
torch.manual_seed(42)
torch.set_num_threads(1)

# Tiny Transformer encoder minh họa head/mask; KHÔNG giả là BERT pretrained.
embedding=nn.Embedding(8,4,padding_idx=0)
layer=nn.TransformerEncoderLayer(4,2,8,dropout=0,batch_first=True)
classifier=nn.Linear(4,2)
ids=torch.tensor([[1,2,0],[3,4,5]])
pad=(ids==0)
hidden=layer(embedding(ids),src_key_padding_mask=pad)
mask=(~pad).unsqueeze(-1)
pooled=(hidden*mask).sum(1)/mask.sum(1)
logits=classifier(pooled)
print("IDs shape:",tuple(ids.shape),"padding mask:",pad.tolist())
print("Hidden:",tuple(hidden.shape),"logits:",tuple(logits.shape))
assert tuple(logits.shape)==(2,2)
# BERT thật: tokenizer và checkpoint phải khớp; bert_demo.py có code inference cache-only.
