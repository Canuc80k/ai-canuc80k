# -*- coding: utf-8 -*-
# Huấn luyện trên GPU — chạy các bước như notebook từ trên xuống.

# Bước 1
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(31)
xb = torch.tensor([[-1., -1.], [-1., 1.], [1., -1.], [1., 1.]])
yb = torch.tensor([0, 0, 1, 1], dtype=torch.long)
model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2))
optimizer = torch.optim.Adam(model.parameters(), lr=.05)
criterion = nn.CrossEntropyLoss()
initial_loss = criterion(model(xb), yb).item()
for step in range(100):
    model.train()
    optimizer.zero_grad(set_to_none=True)
    logits = model(xb)
    assert logits.shape == (4, 2)
    loss = criterion(logits, yb)
    assert torch.isfinite(loss)
    loss.backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all()
               for p in model.parameters())
    optimizer.step()
model.eval()
with torch.no_grad():
    final_logits = model(xb)
    final_loss = criterion(final_logits, yb).item()
    accuracy = (final_logits.argmax(dim=1) == yb).float().mean().item()
print('loss:', round(initial_loss, 6), '->', round(final_loss, 6))
print('one-batch accuracy:', accuracy)

# Bước 2
bad_input = torch.tensor([[1., float('nan')], [2., 3.]])
finite_rows = torch.isfinite(bad_input).all(dim=1)
print('finite rows:', finite_rows.tolist())
print('bad row indices:', (~finite_rows).nonzero(as_tuple=True)[0].tolist())

# Bước 3
parameter_count = sum(p.numel() for p in model.parameters())
weight_bytes = sum(p.numel() * p.element_size() for p in model.parameters())
print('parameters:', parameter_count)
print('weight bytes:', weight_bytes)
print('FP32 Adam parameter-state estimate:', 16 * parameter_count, 'bytes')
B, heads, L = 16, 8, 1024
score_bytes = B * heads * L * L * 4
print('materialized attention scores:', score_bytes // 2**20, 'MiB')

# Bước 4
torch.manual_seed(7)
X_acc = torch.randn(32, 2)
y_acc = (X_acc[:, 0] > 0).long()
net = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2))

def gradient_vector(module):
    return torch.cat([p.grad.flatten() for p in module.parameters()])

net.zero_grad(set_to_none=True)
criterion(net(X_acc), y_acc).backward()            # cả batch 32 mẫu một lần
full_grad = gradient_vector(net).clone()

accumulation_steps = 4
for divide_loss in (True, False):
    net.zero_grad(set_to_none=True)
    x_parts = X_acc.chunk(accumulation_steps)
    y_parts = y_acc.chunk(accumulation_steps)
    for x_part, y_part in zip(x_parts, y_parts):
        micro_loss = criterion(net(x_part), y_part)  # mỗi microbatch 8 mẫu
        if divide_loss:
            micro_loss = micro_loss / accumulation_steps
        micro_loss.backward()                         # .grad cộng dồn qua các lần backward
    accumulated = gradient_vector(net)
    ratio = (accumulated.norm() / full_grad.norm()).item()
    print('divide by 4:', divide_loss, '| norm ratio:', round(ratio, 4),
          '| matches full batch:', torch.allclose(accumulated, full_grad, atol=1e-6))

# Bước 5
tiny_grad = torch.tensor(1e-8)
scale = 65536.0
print('FP16 of 1e-8:', tiny_grad.half().item())
scaled_half = (tiny_grad * scale).half()
print('FP16 of 1e-8 * 65536:', round(scaled_half.item(), 8))
print('unscaled in FP32:', f'{scaled_half.float().item() / scale:.4e}')
