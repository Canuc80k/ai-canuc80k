# -*- coding: utf-8 -*-
# Attention và Transformer — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(41)
Q = np.array([[1.]])
K = np.array([[1.], [0.]])
V = np.array([[2., 0.], [0., 4.]])
scores = Q @ K.T / np.sqrt(Q.shape[-1])
shifted = scores - scores.max(axis=-1, keepdims=True)
weights = np.exp(shifted)
weights /= weights.sum(axis=-1, keepdims=True)
output = weights @ V
print('weights:', np.round(weights, 6).tolist())
print('output:', np.round(output, 6).tolist())
tq, tk, tv = [torch.tensor(a) for a in [Q, K, V]]
torch_output = (tq @ tk.T / np.sqrt(Q.shape[-1])).softmax(dim=-1) @ tv
print('match:', np.allclose(output, torch_output.numpy()))

# Bước 2
rng = np.random.default_rng(0)

def mean_top_weight(scores):
    shifted = scores - scores.max(axis=-1, keepdims=True)
    weights = np.exp(shifted)
    weights /= weights.sum(axis=-1, keepdims=True)
    return weights.max(axis=-1).mean()

for d_k in [4, 64, 1024]:
    q = rng.standard_normal((2000, 1, d_k))   # 2000 query
    k = rng.standard_normal((2000, 8, d_k))   # 8 key cho mỗi query
    raw = (q * k).sum(axis=-1)                # score chưa chia, shape (2000, 8)
    scaled = raw / np.sqrt(d_k)
    print(f'd_k={d_k:<4}  std {raw.std():5.2f} -> {scaled.std():4.2f}   '
          f'max weight {mean_top_weight(raw):.3f} -> {mean_top_weight(scaled):.3f}')

# Bước 3
class TinyEncoder(nn.Module):
    def __init__(self, width=4, heads=2):
        super().__init__()
        self.attention = nn.MultiheadAttention(width, heads, batch_first=True, dropout=0.)
        self.norm1 = nn.LayerNorm(width)
        self.ffn = nn.Sequential(nn.Linear(width, 8), nn.ReLU(), nn.Linear(8, width))
        self.norm2 = nn.LayerNorm(width)

    def forward(self, x, padding_mask=None, causal_mask=None):
        attended, weights = self.attention(x, x, x,
            key_padding_mask=padding_mask, attn_mask=causal_mask,
            need_weights=True, average_attn_weights=False)
        x = self.norm1(x + attended)
        x = self.norm2(x + self.ffn(x))
        return x, weights

block = TinyEncoder()
block.eval()
x = torch.randn(2, 3, 4)
padding_mask = torch.tensor([[False, False, True], [False, False, False]])
with torch.no_grad():
    encoded, attn = block(x, padding_mask=padding_mask)
print('output:', tuple(encoded.shape))
print('weights:', tuple(attn.shape))
print('PAD key max weight:', round(attn[0, :, :, 2].abs().max().item(), 6))
print('weight row sums:', torch.allclose(attn.sum(dim=-1), torch.ones(2, 2, 3), atol=1e-6))

# Bước 4
causal = torch.triu(torch.ones(3, 3, dtype=torch.bool), diagonal=1)
one_sequence = x[1:2].clone()
changed = one_sequence.clone()
changed[:, 2, :] += torch.tensor([10., -3., 7., 2.])
with torch.no_grad():
    before, _ = block(one_sequence, causal_mask=causal)
    after, _ = block(changed, causal_mask=causal)
print('past unchanged:', torch.allclose(before[:, :2], after[:, :2], atol=1e-6))
print('last position changed:', not torch.allclose(before[:, 2], after[:, 2], atol=1e-6))

# Bước 5
permutation = torch.tensor([2, 0, 1])
with torch.no_grad():
    original, _ = block(one_sequence)
    permuted, _ = block(one_sequence[:, permutation])
print('equivariant without positions:', torch.allclose(
    permuted, original[:, permutation], atol=1e-6))

# Bước 6
positions = torch.arange(3, dtype=torch.float32).unsqueeze(1)
frequencies = torch.exp(-np.log(10000.) * torch.arange(0, 4, 2) / 4)
pe = torch.zeros(3, 4)
pe[:, 0::2] = torch.sin(positions * frequencies)
pe[:, 1::2] = torch.cos(positions * frequencies)
with torch.no_grad():
    ordered, _ = block(one_sequence + pe)
    swapped, _ = block(one_sequence[:, permutation] + pe)
print('position 0:', pe[0].tolist())
print('equivariant with fixed slots:', torch.allclose(swapped, ordered[:, permutation], atol=1e-6))

# Bước 7
block.train()
block.zero_grad(set_to_none=True)
encoded, _ = block(x, padding_mask=padding_mask)
target = torch.randn_like(encoded)
valid = ~padding_mask
loss = ((encoded - target).square().mean(dim=-1) * valid).sum() / valid.sum()
loss.backward()
print('finite loss:', torch.isfinite(loss).item())
print('all parameter gradients finite:', all(p.grad is not None and torch.isfinite(p.grad).all()
                                             for p in block.parameters()))
