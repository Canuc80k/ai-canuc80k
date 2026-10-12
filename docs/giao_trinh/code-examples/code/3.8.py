# -*- coding: utf-8 -*-
# Code mẫu — Embedding và dữ liệu chuỗi

# Ví dụ 1: Ghép chuỗi và tạo mask
import torch
from torch.nn.utils.rnn import pad_sequence

torch.set_num_threads(1)
torch.manual_seed(381)
PAD, UNK = 0, 1
sequences = [
    torch.tensor([2, 3]),
    torch.tensor([UNK]),
    torch.tensor([4, 2, 3]),
]
ids = pad_sequence(sequences, batch_first=True, padding_value=PAD)
valid_mask = ids.ne(PAD)
lengths = valid_mask.sum(dim=1)
print("ids:", ids.tolist())
print("valid mask:", valid_mask.int().tolist())
print("lengths:", lengths.tolist())
print("shape:", tuple(ids.shape), "mask shape:", tuple(valid_mask.shape))
assert ids.dtype == torch.long
assert lengths.tolist() == [2, 1, 3]


# Ví dụ 2: Lấy trung bình có mask, và kiểm khi thêm PAD
import torch
from torch import nn
from torch.nn.utils.rnn import pad_sequence

torch.set_num_threads(1)
torch.manual_seed(382)
PAD = 0
sequences = [torch.tensor([2, 3]), torch.tensor([3]), torch.tensor([4, 2, 3])]
ids = pad_sequence(sequences, batch_first=True, padding_value=PAD)
valid_mask = ids.ne(PAD)
table = torch.tensor([
    [0., 0.],  # PAD
    [1., 1.],  # UNK
    [2., 0.],  # token 2
    [0., 4.],  # token 3
    [2., 2.],  # token 4
])
embedding = nn.Embedding(5, 2, padding_idx=PAD)
with torch.no_grad():
    embedding.weight.copy_(table)

def masked_mean(vectors, mask):
    assert vectors.shape[:2] == mask.shape
    counts = mask.sum(dim=1, keepdim=True)
    if torch.any(counts == 0):
        raise ValueError("empty sequence has no valid token")
    return (vectors * mask.unsqueeze(-1)).sum(dim=1) / counts

vectors = embedding(ids)
pooled = masked_mean(vectors, valid_mask)
naive = vectors.mean(dim=1)
print("embedding shape:", tuple(vectors.shape))
print("masked mean:", [[round(v, 4) for v in row] for row in pooled.tolist()])
print("naive first mean:", [round(v, 4) for v in naive[0].tolist()])

extra_ids = torch.cat([ids, torch.zeros(len(ids), 2, dtype=torch.long)], dim=1)
extra_pooled = masked_mean(embedding(extra_ids), extra_ids.ne(PAD))
print("adding PAD changes nothing:", torch.allclose(pooled, extra_pooled))
try:
    empty = torch.zeros(1, 3, dtype=torch.long)
    masked_mean(embedding(empty), empty.ne(PAD))
except ValueError as error:
    print("empty sequence rejected:", str(error))
assert torch.allclose(pooled[0], torch.tensor([1., 2.]))
assert not torch.allclose(pooled[0], naive[0])
assert torch.allclose(pooled, extra_pooled)


# Ví dụ 3: Hàng nào của embedding nhận gradient, và thứ tự bị mất ra sao?
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(383)
PAD = 0
embedding = nn.Embedding(5, 2, padding_idx=PAD)
with torch.no_grad():
    embedding.weight.copy_(torch.tensor([
        [0., 0.], [1., 1.], [2., 0.], [0., 4.], [2., 2.]
    ]))
ids = torch.tensor([[2, 3, 0], [3, 0, 0], [4, 2, 3]])
embedding(ids).sum().backward()
grad = embedding.weight.grad
print("gradient row 0 (PAD):", grad[PAD].tolist())
print("gradient rows 2,3,4:", grad[2:5].tolist())
print("token counts 2,3,4:", [2, 3, 1])

def mean_without_pad(token_ids):
    vectors = embedding(token_ids)
    mask = token_ids.ne(PAD)
    return (vectors * mask.unsqueeze(-1)).sum(dim=1) / mask.sum(dim=1, keepdim=True)

pair = torch.tensor([[2, 3], [3, 2]])
pair_pooled = mean_without_pad(pair)
print("swapping token order keeps mean:", torch.allclose(pair_pooled[0], pair_pooled[1]))
print("pair means:", pair_pooled.tolist())
assert grad[PAD].eq(0).all()
assert torch.allclose(grad[2], torch.tensor([2., 2.]))
assert torch.allclose(grad[3], torch.tensor([3., 3.]))
assert torch.allclose(pair_pooled[0], pair_pooled[1])

