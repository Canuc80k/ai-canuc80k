# -*- coding: utf-8 -*-
# Code mẫu — Attention và Transformer

# Ví dụ 1: Tính scaled dot-product attention bằng tay
import numpy as np
import torch

torch.set_num_threads(1)
Q = np.array([[1.]], dtype=np.float64)
K = np.array([[1.], [0.]], dtype=np.float64)
V = np.array([[2., 0.], [0., 4.]], dtype=np.float64)
scores = Q @ K.T / np.sqrt(Q.shape[-1])
shifted = scores - scores.max(axis=-1, keepdims=True)
weights = np.exp(shifted)
weights /= weights.sum(axis=-1, keepdims=True)
output = weights @ V

torch_output = (
    torch.tensor(Q) @ torch.tensor(K).T
    / np.sqrt(Q.shape[-1])
).softmax(dim=-1) @ torch.tensor(V)
print("shapes Q/K/V:", Q.shape, K.shape, V.shape)
print("scores:", scores.round(6).tolist())
print("weights:", weights.round(6).tolist())
print("output:", output.round(6).tolist())
print("NumPy matches PyTorch:", np.allclose(output, torch_output.numpy()))
assert output.shape == (1, 2)
assert np.allclose(weights.sum(axis=-1), 1.)


# Ví dụ 2: Mask theo đúng trục query và key
import torch

torch.set_num_threads(1)
torch.manual_seed(392)
Q = torch.tensor([[[1., 0.], [0., 1.], [1., 1.], [0., 0.]]])
K = torch.tensor([[[1., 0.], [0., 1.], [1., 1.], [2., 2.]]])
V = torch.tensor([[[1., 0.], [0., 2.], [3., 3.], [9., 9.]]])
length = Q.shape[1]
padding_mask = torch.tensor([[False, False, False, True]])
causal_mask = torch.triu(torch.ones(length, length, dtype=torch.bool), diagonal=1)
scores = Q @ K.transpose(-2, -1) / (Q.shape[-1] ** 0.5)
blocked = padding_mask[:, None, :] | causal_mask[None, :, :]
masked_scores = scores.masked_fill(blocked, float("-inf"))
weights = masked_scores.softmax(dim=-1)
attended = weights @ V
future_weights = weights.masked_select(causal_mask.unsqueeze(0))
pad_weights = weights[:, :, -1]
print("score shape:", tuple(scores.shape))
print("blocked shape:", tuple(blocked.shape))
print("query 2 weights:", [round(float(v), 6) for v in weights[0, 2]])
print("max PAD-key weight:", round(float(pad_weights.abs().max()), 6))
print("max future-key weight:", round(float(future_weights.abs().max()), 6))
print("all row sums 1:", torch.allclose(
    weights.sum(dim=-1), torch.ones_like(weights[..., 0])))
print("PAD-query output norm:", round(float(attended[0, 3].norm()), 6))
assert weights.shape == (1, 4, 4)
assert float(pad_weights.abs().max()) == 0.
assert float(future_weights.abs().max()) == 0.
assert torch.allclose(weights.sum(dim=-1), torch.ones_like(weights[..., 0]))


# Ví dụ 3: MultiheadAttention, và phép kiểm rò rỉ tương lai
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(393)
block = nn.MultiheadAttention(
    embed_dim=4, num_heads=2, batch_first=True, dropout=0.
)
block.eval()
x = torch.tensor([[
    [1., 0., 0., 1.],
    [0., 1., 1., 0.],
    [1., 1., 0., 0.],
    [0., 0., 1., 1.],
]])
causal = torch.triu(torch.ones(4, 4, dtype=torch.bool), diagonal=1)
changed = x.clone()
changed[:, 3] += torch.tensor([10., -3., 7., 2.])
with torch.no_grad():
    before, weights = block(
        x, x, x, attn_mask=causal,
        need_weights=True, average_attn_weights=False,
    )
    after, _ = block(
        changed, changed, changed, attn_mask=causal,
        need_weights=True, average_attn_weights=False,
    )
blocked_weights = weights[0].masked_select(causal.unsqueeze(0).expand_as(weights[0]))
print("output shape:", tuple(before.shape))
print("weights shape (B,H,Q,K):", tuple(weights.shape))
print("max future weight:", round(float(blocked_weights.abs().max()), 6))
print("first three outputs unchanged:", torch.allclose(
    before[:, :3], after[:, :3], atol=1e-6))
assert before.shape == (1, 4, 4)
assert weights.shape == (1, 2, 4, 4)
assert float(blocked_weights.abs().max()) == 0.
assert torch.allclose(before[:, :3], after[:, :3], atol=1e-6)

