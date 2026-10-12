# -*- coding: utf-8 -*-
# Code mẫu — Huấn luyện trên GPU

# Ví dụ 1: Kiểm device, rồi cho model học thuộc một batch
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(307)

cuda_available = torch.cuda.is_available()
print("CUDA available:", cuda_available)
print("CUDA device count:", torch.cuda.device_count())

demo_device = torch.device("cpu")
features = torch.tensor([[-1., -1.], [-1., 1.], [1., -1.], [1., 1.]],
                        device=demo_device)
labels = torch.tensor([0, 0, 1, 1], dtype=torch.long, device=demo_device)
model = nn.Sequential(nn.Linear(2, 8), nn.Tanh(), nn.Linear(8, 2)).to(demo_device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
criterion = nn.CrossEntropyLoss()

initial = criterion(model(features), labels).item()
for _ in range(60):
    optimizer.zero_grad(set_to_none=True)
    logits = model(features)
    assert logits.shape == (4, 2)
    loss = criterion(logits, labels)
    assert torch.isfinite(loss)
    loss.backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all()
               for p in model.parameters())
    optimizer.step()

with torch.no_grad():
    final_logits = model(features)
    final = criterion(final_logits, labels).item()
    accuracy = (final_logits.argmax(dim=1) == labels).float().mean().item()
print("selected device:", demo_device)
print("parameter dtype:", next(model.parameters()).dtype)
print("loss:", round(initial, 6), "->", round(final, 6))
print("one-batch accuracy:", accuracy)
assert next(model.parameters()).device == demo_device
assert accuracy == 1.0


# Ví dụ 2: Chia nhỏ batch và cộng dồn gradient
import copy
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(308)
inputs = torch.tensor([[-2., 0.], [-1., 1.], [0., 2.], [1., 1.],
                      [2., 0.], [3., -1.]])
targets = torch.tensor([[0.], [1.], [2.], [1.], [0.], [-1.]])

base = nn.Linear(2, 1)
full_model = copy.deepcopy(base)
micro_model = copy.deepcopy(base)

full_loss = (full_model(inputs) - targets).square().mean()
full_loss.backward()

total = len(inputs)
for start in range(0, total, 2):
    stop = min(start + 2, total)
    micro_loss = (micro_model(inputs[start:stop]) - targets[start:stop]).square().mean()
    (micro_loss * ((stop - start) / total)).backward()

gradient_gap = max(
    (a.grad - b.grad).abs().max().item()
    for a, b in zip(full_model.parameters(), micro_model.parameters())
)
full_optimizer = torch.optim.SGD(full_model.parameters(), lr=0.1)
micro_optimizer = torch.optim.SGD(micro_model.parameters(), lr=0.1)
full_optimizer.step()
micro_optimizer.step()
parameter_gap = max(
    (a - b).abs().max().item()
    for a, b in zip(full_model.parameters(), micro_model.parameters())
)
print("full-batch MSE:", round(full_loss.item(), 6))
print("microbatch sizes:", [2, 2, 2])
print("max gradient difference:", gradient_gap)
print("max parameter difference after step:", parameter_gap)
assert gradient_gap < 1e-7
assert parameter_gap < 1e-7


# Ví dụ 3: Ước lượng từng phần của bộ nhớ
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(309)
memory_model = nn.Sequential(nn.Linear(6, 10), nn.ReLU(), nn.Linear(10, 3))
parameter_count = sum(p.numel() for p in memory_model.parameters())
weight_bytes = sum(p.numel() * p.element_size() for p in memory_model.parameters())
print("parameters:", parameter_count)
print("weight bytes:", weight_bytes)
print("FP32 Adam weight+grad+2 moments estimate:", 16 * parameter_count, "bytes")

for batch in [8, 16]:
    hidden_activation_bytes = batch * 10 * 4
    print("batch", batch, "hidden activation:", hidden_activation_bytes, "bytes")

def mib(byte_count):
    return round(byte_count / 2**20, 3)

for length in [128, 256]:
    score_bytes = 2 * 4 * length * length * 4  # B × số head × L × L × 4 byte FP32.
    print("attention score B=2,H=4,L=", length, ":", mib(score_bytes), "MiB")
assert parameter_count == 103
assert 16 * parameter_count == 1648

