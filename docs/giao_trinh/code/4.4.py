# -*- coding: utf-8 -*-
# LoRA — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(12)
torch.set_default_dtype(torch.float64)
for din, dout, rank in [(8, 6, 2), (4096, 4096, 8)]:
    full = din * dout
    adapter = rank * (din + dout)
    print("shape:", (dout, din), "full:", full,
          "LoRA:", adapter, "ty le:", round(adapter / full, 6))

# Bước 2
class TinyLoRA(nn.Module):
    def __init__(self, base_weight, rank, alpha):
        super().__init__()
        dout, din = base_weight.shape
        self.base = nn.Parameter(base_weight.clone(), requires_grad=False)
        self.A = nn.Parameter(torch.randn(rank, din) * 0.1)
        self.B = nn.Parameter(torch.zeros(dout, rank))
        self.scale = alpha / rank

    def forward(self, X):
        original = X @ self.base.T
        update = (X @ self.A.T) @ self.B.T
        return original + self.scale * update

W0 = torch.randn(6, 8) * 0.1
true_A = torch.randn(2, 8) * 0.2
true_B = torch.randn(6, 2) * 0.2
W_target = W0 + true_B @ true_A
X_train = torch.randn(64, 8)
X_valid = torch.randn(64, 8)
y_train = X_train @ W_target.T
y_valid = X_valid @ W_target.T
adapter = TinyLoRA(W0, rank=2, alpha=4)
with torch.no_grad():
    unchanged = torch.allclose(adapter(X_train), X_train @ W0.T)
print("ban dau dung model goc:", unchanged)
print("tham so hoc:", sum(p.numel() for p in adapter.parameters() if p.requires_grad))

# Bước 3
loss = ((adapter(X_train) - y_train) ** 2).mean()
loss.backward()
X_np = X_train.numpy()
A_np = adapter.A.detach().numpy()
B_np = adapter.B.detach().numpy()
W_np = W0.numpy()
y_np = y_train.numpy()
s = adapter.scale
prediction_np = X_np @ W_np.T + s * (X_np @ A_np.T) @ B_np.T
G_np = 2 * (prediction_np - y_np) / y_np.size
grad_B_np = s * G_np.T @ X_np @ A_np.T
grad_A_np = s * B_np.T @ G_np.T @ X_np

def numpy_loss(B_value):
    prediction = X_np @ W_np.T + s * (X_np @ A_np.T) @ B_value.T
    return np.mean((prediction - y_np) ** 2)

h = 1e-5
B_plus, B_minus = B_np.copy(), B_np.copy()
B_plus[0, 0] += h
B_minus[0, 0] -= h
finite_difference = (numpy_loss(B_plus) - numpy_loss(B_minus)) / (2 * h)
print("A grad bang 0:", torch.count_nonzero(adapter.A.grad).item() == 0)
print("B grad khac 0:", adapter.B.grad.norm().item() > 0)
print("W0 grad None:", adapter.base.grad is None)
print("khop cong thuc A/B:", np.allclose(adapter.A.grad.numpy(), grad_A_np),
      np.allclose(adapter.B.grad.numpy(), grad_B_np))
print("khop sai phan B00:", np.isclose(finite_difference, adapter.B.grad[0, 0].item(), atol=1e-8))

# Bước 4
one_step = torch.optim.SGD([adapter.A, adapter.B], lr=0.1)
one_step.step()
one_step.zero_grad(set_to_none=True)
second_loss = ((adapter(X_train) - y_train) ** 2).mean()
second_loss.backward()
A_after = adapter.A.detach().numpy()
B_after = adapter.B.detach().numpy()
pred_after = X_np @ W_np.T + s * (X_np @ A_after.T) @ B_after.T
G_after = 2 * (pred_after - y_np) / y_np.size
expected_A = s * B_after.T @ G_after.T @ X_np

def loss_after(A_value):
    pred = X_np @ W_np.T + s * (X_np @ A_value.T) @ B_after.T
    return np.mean((pred - y_np) ** 2)

A_plus, A_minus = A_after.copy(), A_after.copy()
A_plus[0, 0] += h
A_minus[0, 0] -= h
numeric_A00 = (loss_after(A_plus) - loss_after(A_minus)) / (2 * h)
print("A grad sau buoc khac 0:", adapter.A.grad.norm().item() > 0)
print("A khop NumPy:", np.allclose(adapter.A.grad.numpy(), expected_A))
print("A00 khop sai phan:", np.isclose(numeric_A00, adapter.A.grad[0, 0].item(), atol=1e-8))

# Bước 5
def train_small(kind, rank=2, steps=250):
    torch.manual_seed(20)
    if kind == "full":
        candidate = nn.Linear(8, 6, bias=False)
        with torch.no_grad():
            candidate.weight.copy_(W0)
    else:
        candidate = TinyLoRA(W0, rank=rank, alpha=2 * rank)
    learned = [p for p in candidate.parameters() if p.requires_grad]
    optimizer = torch.optim.Adam(learned, lr=0.03)
    for _ in range(steps):
        optimizer.zero_grad(set_to_none=True)
        train_loss = ((candidate(X_train) - y_train) ** 2).mean()
        train_loss.backward()
        optimizer.step()
    with torch.no_grad():
        valid_loss = ((candidate(X_valid) - y_valid) ** 2).mean().item()
    count = sum(p.numel() for p in learned)
    return candidate, valid_loss, count

full_net, full_mse, full_count = train_small("full")
rank1_net, rank1_mse, rank1_count = train_small("lora", rank=1)
rank2_net, rank2_mse, rank2_count = train_small("lora", rank=2)
for name, error, count in [
    ("full", full_mse, full_count),
    ("rank 1", rank1_mse, rank1_count),
    ("rank 2", rank2_mse, rank2_count),
]:
    print(name, "trainable =", count, "valid MSE =", format(error, ".3g"))

_, rank1_long, _ = train_small("lora", rank=1, steps=2500)
print("rank 1, 2500 buoc: valid MSE =", format(rank1_long, ".3g"))
singular = np.linalg.svd((true_B @ true_A).numpy(), compute_uv=False)
print("gia tri ky di cua phan sua:", np.round(singular[:3], 4))

# Bước 6
with torch.no_grad():
    merged_weight = rank2_net.base + rank2_net.scale * rank2_net.B @ rank2_net.A
    separate = rank2_net(X_valid)
    merged = X_valid @ merged_weight.T
print("merge khop:", torch.allclose(separate, merged, atol=1e-10))
print("rank delta:", int(torch.linalg.matrix_rank(merged_weight - W0)))
torch.set_default_dtype(torch.float32)  # khôi phục mặc định sau phép tính float64

# Bước 7
from transformers import DistilBertConfig, DistilBertForSequenceClassification

class LoRALinear(nn.Module):
    def __init__(self, base, rank, alpha):
        super().__init__()
        self.base = base  # nn.Linear gốc, kể cả bias
        self.A = nn.Parameter(torch.randn(rank, base.in_features) * 0.01)
        self.B = nn.Parameter(torch.zeros(base.out_features, rank))
        self.scale = alpha / rank

    def forward(self, x):
        return self.base(x) + self.scale * (x @ self.A.T) @ self.B.T

torch.manual_seed(4)
model = DistilBertForSequenceClassification(DistilBertConfig(num_labels=2)).eval()
token_ids = torch.randint(0, model.config.vocab_size, (2, 16))
with torch.no_grad():
    logits_before = model(input_ids=token_ids).logits

model.requires_grad_(False)
targets = [name for name, module in model.named_modules()
           if name.endswith(("q_lin", "v_lin")) and isinstance(module, nn.Linear)]
for name in targets:
    parent_name, child_name = name.rsplit(".", 1)
    parent = model.get_submodule(parent_name)
    base = getattr(parent, child_name)
    setattr(parent, child_name, LoRALinear(base, rank=4, alpha=8))
model.pre_classifier.requires_grad_(True)
model.classifier.requires_grad_(True)

with torch.no_grad():
    logits_after = model(input_ids=token_ids).logits
adapter_count = sum(p.numel() for n, p in model.named_parameters() if n.endswith((".A", ".B")))
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print("module duoc chen:", len(targets))
print("adapter:", adapter_count, "head:", trainable - adapter_count)
print("trainable:", trainable, "/", total, "=", f"{trainable / total:.2%}")
print("logits giu nguyen:", torch.allclose(logits_before, logits_after))
