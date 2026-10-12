# -*- coding: utf-8 -*-
# Code mẫu — Activation và loss

# Ví dụ 1: Cùng đầu vào, mỗi activation truyền gradient một kiểu
import torch
from torch.nn import functional as F

torch.set_num_threads(1)
values = torch.tensor([-4., -1., 0., 1., 4.], dtype=torch.float64)
for name, activation in [("ReLU", F.relu),
                         ("LeakyReLU", lambda x: F.leaky_relu(x, .1)),
                         ("sigmoid", torch.sigmoid)]:
    z = values.clone().requires_grad_()
    output = activation(z)
    output.sum().backward()
    print(name, "output:", [round(v, 5) for v in output.tolist()])
    print(name, "gradient:", [round(v, 5) for v in z.grad.tolist()])


# Ví dụ 2: MSE phạt nặng lỗi lớn, và có đơn vị bình phương
import torch
from torch.nn import functional as F

torch.set_num_threads(1)
prediction = torch.tensor([4., 7., 15.])
target = torch.tensor([5., 5., 5.])
assert prediction.shape == target.shape
per_item = F.mse_loss(prediction, target, reduction="none")
mse = per_item.mean()
mae = F.l1_loss(prediction, target)
print("phần dư (phút):", (prediction - target).tolist())
print("MSE từng mẫu:", per_item.tolist())
print("MSE / MAE:", round(mse.item(), 4), round(mae.item(), 4))
print("MSE theo giây:", F.mse_loss(60 * prediction, 60 * target).item())
assert torch.allclose(F.mse_loss(60 * prediction, 60 * target), 3600 * mse)


# Ví dụ 3: Logit sai rất tự tin vẫn phải cho loss hữu hạn
import torch
from torch.nn import functional as F

torch.set_num_threads(1)
z = torch.tensor([-1000., 0., 1000.], dtype=torch.float64, requires_grad=True)
y = torch.tensor([1., 1., 0.], dtype=torch.float64)
hand = z.clamp_min(0) - z * y + torch.log1p(torch.exp(-z.abs()))
individual = F.binary_cross_entropy_with_logits(z, y, reduction="none")
assert torch.allclose(hand, individual) and torch.isfinite(individual).all()
individual.sum().backward()
sum_gradient = z.grad.clone()
print("loss từng mẫu:", [round(v, 6) for v in individual.tolist()])
print("gradient loss sum:", sum_gradient.tolist())

z.grad = None
mean_loss = F.binary_cross_entropy_with_logits(z, y, reduction="mean")
mean_loss.backward()
print("loss mean:", round(mean_loss.item(), 6))
print("gradient loss mean:", [round(v, 6) for v in z.grad.tolist()])
assert torch.allclose(z.grad * len(y), sum_gradient)


# Ví dụ 4: Chọn một trong ba lớp, hay hai thuộc tính độc lập
import math
import torch
from torch.nn import functional as F

torch.set_num_threads(1)
logits = torch.tensor([[math.log(3), 0., math.log(2)]], dtype=torch.float64)
label = torch.tensor([0], dtype=torch.long)
probabilities = logits.softmax(dim=1)  # Trục 1 là trục lớp, không phải trục batch.
correct = F.cross_entropy(logits, label)
wrong = F.cross_entropy(probabilities, label)
shifted = F.cross_entropy(logits + 1000, label)
print("xác suất ba lớp:", [[round(v, 6) for v in row]
                            for row in probabilities.tolist()])
print("CE logits / CE sau softmax:", round(correct.item(), 6), round(wrong.item(), 6))
print("CE sau cộng 1000:", round(shifted.item(), 6))
print("lớp dự đoán:", logits.argmax(dim=1).tolist())
assert math.isclose(correct.item(), math.log(2))
assert torch.allclose(correct, shifted)

attribute_logits = torch.tensor([[math.log(4), math.log(4)]], dtype=torch.float64)
attribute_target = torch.tensor([[1., 1.]], dtype=torch.float64)
assert attribute_logits.shape == attribute_target.shape
print("sigmoid từng thuộc tính:", attribute_logits.sigmoid().tolist())
print("softmax ép tổng 1:", attribute_logits.softmax(dim=1).tolist())
print("BCE mean:", round(F.binary_cross_entropy_with_logits(
    attribute_logits, attribute_target).item(), 6))

