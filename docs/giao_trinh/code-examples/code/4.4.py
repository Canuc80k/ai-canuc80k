# -*- coding: utf-8 -*-
# Code mẫu — LoRA

# Ví dụ 1: Một hướng sửa, ba đầu vào, hai đầu ra
import numpy as np

W0 = np.array([[1., 0., 0.], [0., 1., 0.]])
A = np.array([[1., 0., 2.]])       # Shape (rank=1, số đầu vào=3).
B = np.array([[0.5], [-0.5]])     # Shape (số đầu ra=2, rank=1).
alpha, rank = 2, 1
scale = alpha / rank
X = np.array([[2., 1., 3.]])
base = X @ W0.T
update = scale * (X @ A.T) @ B.T
separate = base + update
merged = X @ (W0 + scale * B @ A).T
assert np.array_equal(separate, np.array([[10., -7.]]))
assert np.array_equal(separate, merged)
print("base:", base.tolist())
print("nhanh sua:", update.tolist())
print("output:", separate.tolist())
print("tham so full/adapter:", W0.size, A.size + B.size)
print("rank ma tran sua:", np.linalg.matrix_rank(B @ A))
print("merge trung:", np.array_equal(separate, merged))


# Ví dụ 2: B bằng 0 thì bước đầu A đứng yên
import numpy as np
import torch
from torch import nn

torch.set_num_threads(1)
X = torch.eye(2, dtype=torch.float64)
Y = torch.tensor([[1., 2.], [3., 4.]], dtype=torch.float64)
W0 = nn.Parameter(torch.zeros((2, 2), dtype=torch.float64), requires_grad=False)
A = nn.Parameter(torch.tensor([[1., 2.]], dtype=torch.float64))
B = nn.Parameter(torch.zeros((2, 1), dtype=torch.float64))
optimizer = torch.optim.SGD([A, B], lr=0.1)
prediction = X @ W0.T + (X @ A.T) @ B.T
loss = ((prediction - Y)**2).mean()
loss.backward()
assert torch.equal(B.grad, torch.tensor([[-3.5], [-5.]], dtype=torch.float64))
print("buoc dau, A grad:", A.grad.tolist())
print("buoc dau, B grad:", B.grad.tolist())
print("base grad None:", W0.grad is None)
optimizer.step()
optimizer.zero_grad(set_to_none=True)
prediction = X @ W0.T + (X @ A.T) @ B.T
((prediction - Y)**2).mean().backward()
# Kiểm lại bằng chain rule viết tay. Mẫu số là 4, số phần tử của MSE.
G = 2 * (prediction.detach().numpy() - Y.numpy()) / Y.numel()
expected_A = B.detach().numpy().T @ G.T @ X.numpy()
assert np.allclose(A.grad.numpy(), expected_A)
print("buoc hai, A grad:", A.grad.numpy().round(5).tolist())

zero_A = nn.Parameter(torch.zeros_like(A))
zero_B = nn.Parameter(torch.zeros_like(B))
bad_prediction = (X @ zero_A.T) @ zero_B.T
((bad_prediction - Y)**2).mean().backward()
print("ca A/B khoi tao 0, gradient deu 0:",
      bool((zero_A.grad == 0).all() and (zero_B.grad == 0).all()))


# Ví dụ 3: Rank 1 và rank 2 học cùng một thay đổi
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(44)
dtype = torch.float64
W0 = torch.arange(24, dtype=dtype).reshape(4, 6) / 50
delta = torch.zeros((4, 6), dtype=dtype)
delta[0, 0], delta[1, 1] = 1., 0.6
train_X = torch.randn((48, 6), dtype=dtype)
valid_X = torch.randn((40, 6), dtype=dtype)
train_Y = train_X @ (W0 + delta).T
valid_Y = valid_X @ (W0 + delta).T

class LoRALinear(nn.Module):
    def __init__(self, base, rank):
        super().__init__()
        self.base = nn.Parameter(base.clone(), requires_grad=False)
        self.A = nn.Parameter(torch.randn((rank, base.shape[1]), dtype=dtype) * 0.1)
        self.B = nn.Parameter(torch.zeros((base.shape[0], rank), dtype=dtype))
        self.scale = 2.0  # Đặt alpha = 2 × rank, nên alpha / rank luôn bằng 2.

    def forward(self, values):
        return values @ self.base.T + self.scale * (values @ self.A.T) @ self.B.T

def train_adapter(rank):
    torch.manual_seed(440)
    model = LoRALinear(W0, rank)
    optimizer = torch.optim.Adam([model.A, model.B], lr=0.04)
    model.train()
    for _ in range(240):
        optimizer.zero_grad(set_to_none=True)
        loss = ((model(train_X) - train_Y)**2).mean()
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.inference_mode():
        mse = ((model(valid_X) - valid_Y)**2).mean().item()
        merged_weight = model.base + model.scale * model.B @ model.A
        merged = valid_X @ merged_weight.T
        assert torch.allclose(model(valid_X), merged, atol=1e-10)
    assert torch.equal(model.base, W0) and model.base.grad is None
    trainable = model.A.numel() + model.B.numel()
    return mse, trainable

results = [train_adapter(rank) for rank in [1, 2]]
for rank, (mse, count) in zip([1, 2], results):
    print("rank:", rank, "trainable:", count, "valid MSE:", format(mse, ".3g"))
assert results[1][0] < results[0][0]
print("rank muc tieu:", int(torch.linalg.matrix_rank(delta)))
print("base giu nguyen, merge khop:", True)

