# -*- coding: utf-8 -*-
# Embedding và dữ liệu chuỗi — chạy các bước như notebook từ trên xuống.

# Bước 1
import torch
from torch import nn
from torch.nn.utils.rnn import pad_sequence

torch.set_num_threads(1)
torch.manual_seed(37)
PAD, UNK = 0, 1
sequences = [torch.tensor([2, 3]), torch.tensor([3]), torch.tensor([4, 2, 3])]
ids = pad_sequence(sequences, batch_first=True, padding_value=PAD)
valid_mask = ids.ne(PAD)
print(ids.tolist())
print(valid_mask.int().tolist())
print('lengths:', valid_mask.sum(dim=1).tolist())

# Bước 2
table = torch.tensor([[0., 0.], [1., 1.], [2., 0.], [0., 4.], [2., 2.]])
embedding = nn.Embedding(5, 2, padding_idx=PAD)
with torch.no_grad():
    embedding.weight.copy_(table)
vectors = embedding(ids)
print('shapes:', tuple(ids.shape), tuple(embedding.weight.shape), tuple(vectors.shape))
print(vectors[0].tolist())

# Bước 3
def masked_mean(vectors, valid_mask):
    assert vectors.shape[:2] == valid_mask.shape
    counts = valid_mask.sum(dim=1, keepdim=True)
    if torch.any(counts == 0):
        raise ValueError('Mỗi chuỗi cần ít nhất một token hợp lệ')
    weighted = vectors * valid_mask.unsqueeze(-1)
    return weighted.sum(dim=1) / counts

pooled = masked_mean(vectors, valid_mask)
print('masked:', [[round(v, 4) for v in row] for row in pooled.tolist()])
print('naive first:', [round(v, 4) for v in vectors.mean(dim=1)[0].tolist()])

# Bước 4
extra_ids = torch.cat([ids, torch.zeros(len(ids), 2, dtype=torch.long)], dim=1)
extra_pooled = masked_mean(embedding(extra_ids), extra_ids.ne(PAD))
print('adding PAD changes nothing:', torch.allclose(pooled, extra_pooled))
try:
    empty_ids = torch.zeros(1, 3, dtype=torch.long)
    masked_mean(embedding(empty_ids), empty_ids.ne(PAD))
except ValueError:
    print('empty sequence rejected:', True)

# Bước 5
embedding.zero_grad(set_to_none=True)
embedding(ids).sum().backward()
print('gradient rows:', embedding.weight.grad.tolist())
print('PAD has zero gradient:', embedding.weight.grad[PAD].eq(0).all().item())
classifier = nn.Linear(2, 2)
print('classifier logits shape:', tuple(classifier(pooled.detach()).shape))

# Bước 6
pair = torch.tensor([[2, 3], [3, 2]])
pair_vectors = masked_mean(embedding(pair), pair.ne(PAD))
print('same after swapping:', torch.allclose(pair_vectors[0], pair_vectors[1]))

# Bước 7
from torch.nn.utils.rnn import pack_padded_sequence

torch.manual_seed(38)
rnn = nn.RNN(input_size=2, hidden_size=3, batch_first=True)
print('RNN parameters:', sum(p.numel() for p in rnn.parameters()))
with torch.no_grad():
    outputs, _ = rnn(vectors)                       # (B, L, H): trạng thái sau từng cột
    lengths = valid_mask.sum(dim=1)
    last_column = outputs[:, -1]                    # cột cuối, có thể nằm sau PAD
    last_valid = outputs[torch.arange(len(ids)), lengths - 1]
    packed = pack_padded_sequence(vectors, lengths, batch_first=True, enforce_sorted=False)
    _, h_packed = rnn(packed)                       # (1, B, H): dừng ở token thật cuối
    swapped = rnn(embedding(pair))[0][:, -1]
print('outputs shape:', tuple(outputs.shape))
print('last column is last token:', torch.isclose(last_column, last_valid).all(dim=1).tolist())
print('gather matches packed:', torch.allclose(last_valid, h_packed[0]))
print('RNN same after swapping:', torch.allclose(swapped[0], swapped[1]))

# Bước 8
torch.manual_seed(0)
long_x = torch.randn(1, 40, 2, requires_grad=True)
_, h_end = rnn(long_x)
h_end.sum().backward()
grad_norm = long_x.grad[0].norm(dim=1)              # độ lớn gradient theo từng token
for t in [40, 30, 20, 10, 1]:
    print(f'token {t:2d}: {grad_norm[t - 1].item():.1e}')
