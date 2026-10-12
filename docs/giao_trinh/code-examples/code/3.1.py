# -*- coding: utf-8 -*-
# Code mẫu — Tensor và autograd

# Ví dụ 1: Hai mẫu, ba đặc trưng và một lỗi broadcasting
import torch

torch.set_num_threads(1)
X = torch.tensor([[1., 2., 3.], [4., 5., 6.]])  # (mẫu, đặc trưng)
W = torch.tensor([[1., 0.], [0., 2.], [1., -1.]])
b = torch.tensor([0.5, -0.5])
Y = X @ W + b
assert Y.shape == (2, 2)
print("shape X, W, Y:", tuple(X.shape), tuple(W.shape), tuple(Y.shape))
print("đặc trưng mới:", Y.tolist())
print("tổng theo mẫu:", X.sum(dim=1).tolist())

prediction = torch.tensor([[1.], [3.]])
target = torch.tensor([1., 2.])
wrong_residual = prediction - target
print("hiệu bị broadcast:", wrong_residual.tolist(), tuple(wrong_residual.shape))

target_column = target.unsqueeze(1)
assert prediction.shape == target_column.shape
print("hiệu từng mẫu:", (prediction - target_column).tolist())
print("MSE sai / đúng:", wrong_residual.square().mean().item(),
      (prediction - target_column).square().mean().item())


# Ví dụ 2: Backward tính gì, và trọng số đổi lúc nào?
import torch

torch.set_num_threads(1)
w = torch.tensor(2., requires_grad=True)
u = 3 * w
loss = (u - 1).square()
loss.backward()
print("u, loss, gradient:", u.item(), loss.item(), w.grad.item())
print("w sau backward:", w.item())
assert w.item() == 2. and w.grad.item() == 30.

# Bước cập nhật là một việc riêng, không được ghi vào graph của lần forward vừa rồi.
with torch.no_grad():
    w -= 0.01 * w.grad
print("w sau cập nhật:", round(w.item(), 4))
print("loss mới:", round((3 * w - 1).square().item(), 4))

v = torch.tensor(2., requires_grad=True)
gradients = []
for _ in range(2):
    (3 * v - 1).square().backward()  # Graph mới, nhưng .grad cũ vẫn còn nguyên.
    gradients.append(v.grad.item())
v.grad = None
(3 * v - 1).square().backward()
gradients.append(v.grad.item())
print("gradient qua ba lượt:", gradients)
assert gradients == [30., 60., 30.]


# Ví dụ 3: Cắt graph giữ nguyên giá trị nhưng đổi đạo hàm
import torch

torch.set_num_threads(1)
v = torch.tensor(2., requires_grad=True)
full = v.square() * v
full.backward()
full_gradient = v.grad.item()

v.grad = None
cut = v.square().detach() * v
cut.backward()
print("giá trị full / cut:", full.item(), cut.item())
print("gradient full / cut:", full_gradient, v.grad.item())
assert full_gradient == 12. and v.grad.item() == 4.

source = torch.tensor([2., 3.], requires_grad=True)
alias = source.detach()
snapshot = source.detach().clone()  # Bản sao riêng, không đổi khi source bị sửa.
with torch.no_grad():
    source[0] = 9.
print("source, detach, snapshot:", source.tolist(), alias.tolist(), snapshot.tolist())

