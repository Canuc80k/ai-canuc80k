# -*- coding: utf-8 -*-
# Code mẫu — MLP và backpropagation

# Ví dụ 1: Tạo đặc trưng ẩn để giải XOR
import numpy as np

X = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
target = np.array([0., 1., 1., 0.])
W1 = np.ones((2, 2))  # Mỗi cột tạo ra một đặc trưng ẩn.
b1 = np.array([0., -1.])
Z = X @ W1 + b1
hidden = np.maximum(Z, 0.)
prediction = hidden @ np.array([1., -2.])
print("hidden:", hidden.tolist())
print("XOR:", prediction.tolist())
print("bỏ ReLU:", (Z @ np.array([1., -2.])).tolist())
assert np.array_equal(prediction, target)


# Ví dụ 2: Tính gradient bằng tay rồi đối chiếu bằng hai cách khác
import numpy as np
import torch

torch.set_num_threads(1)
X = np.array([[1., 0.], [0., 2.]])
y = np.array([[1.], [0.]])
params = [np.array([[1., -1.], [.5, 1.]]), np.array([.5, -.5]),
          np.array([[1.], [-1.]]), np.array([.25])]

def forward(ps):
    W1, b1, W2, b2 = ps
    z = X @ W1 + b1
    h = np.maximum(z, 0.)
    return h @ W2 + b2, z, h

def objective(ps):
    p, _, _ = forward(ps)
    assert p.shape == y.shape
    return ((p - y) ** 2).mean()

prediction, z, h = forward(params)
g_output = 2 * (prediction - y) / len(X)
# Dùng W2 của chính lần forward này. Chưa tham số nào được cập nhật.
g_hidden = (g_output @ params[2].T) * (z > 0)
manual = [X.T @ g_hidden, g_hidden.sum(axis=0),
          h.T @ g_output, g_output.sum(axis=0)]
print("z:", z.tolist())
print("prediction, MSE:", prediction.ravel().tolist(), objective(params))
for name, gradient in zip(["W1", "b1", "W2", "b2"], manual):
    print("gradient", name, np.round(gradient, 4).tolist())

numeric = []
eps = 1e-5
for parameter in params:
    gradient = np.zeros_like(parameter)
    for index in np.ndindex(parameter.shape):
        old = parameter[index]
        parameter[index] = old + eps
        plus = objective(params)
        parameter[index] = old - eps
        minus = objective(params)
        parameter[index] = old
        gradient[index] = (plus - minus) / (2 * eps)
    numeric.append(gradient)

tp = [torch.tensor(p, dtype=torch.float64, requires_grad=True) for p in params]
tx, ty = torch.tensor(X), torch.tensor(y)
pred = torch.relu(tx @ tp[0] + tp[1]) @ tp[2] + tp[3]
(pred - ty).square().mean().backward()
numeric_ok = all(np.allclose(a, b, atol=1e-8) for a, b in zip(manual, numeric))
autograd_ok = all(np.allclose(g, p.grad.numpy(), atol=1e-10)
                  for g, p in zip(manual, tp))
updated = [p - .05 * g for p, g in zip(params, manual)]
print("sai phân khớp:", numeric_ok, "autograd khớp:", autograd_ok)
print("loss trước / sau một bước:", round(objective(params), 6),
      round(objective(updated), 6))
assert numeric_ok and autograd_ok and objective(updated) < objective(params)


# Ví dụ 3: Một MLP tự học bốn mẫu từ khởi tạo ngẫu nhiên
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(31)
X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y = torch.tensor([0., 1., 1., 0.])
model = nn.Sequential(nn.Linear(2, 8), nn.Tanh(), nn.Linear(8, 1))
optimizer = torch.optim.Adam(model.parameters(), lr=.05)
criterion = nn.BCEWithLogitsLoss()
print("tham số:", sum(p.numel() for p in model.parameters()))
for step in range(301):
    model.train()
    optimizer.zero_grad(set_to_none=True)
    logits = model(X).squeeze(-1)  # Chỉ bỏ trục đầu ra, giữ nguyên trục batch.
    assert logits.shape == y.shape
    loss = criterion(logits, y)
    if step in [0, 50, 150, 300]:
        print("step", step, "loss", round(loss.item(), 5))
    if step < 300:
        loss.backward()
        optimizer.step()

model.eval()
with torch.no_grad():
    probabilities = model(X).squeeze(-1).sigmoid()
    labels = (probabilities >= .5).long()
print("xác suất:", [round(p, 4) for p in probabilities.tolist()])
print("nhãn:", labels.tolist())
assert torch.equal(labels, y.long())

