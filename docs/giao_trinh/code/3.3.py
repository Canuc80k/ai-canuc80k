# -*- coding: utf-8 -*-
# Activation và loss — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

torch.set_num_threads(1)
torch.manual_seed(13)
z = torch.tensor([-10., 0., 10.], requires_grad=True)
torch.sigmoid(z).sum().backward()
print('sigmoid :', [round(v, 6) for v in torch.sigmoid(z).tolist()])
print("sigmoid':", [round(v, 6) for v in z.grad.tolist()])
z.grad = None                       # xóa gradient cũ trước lần backward thứ hai
torch.tanh(z).sum().backward()
print("tanh'   :", [round(v, 6) for v in z.grad.tolist()])
r = torch.tensor([-2., 0., 3.], requires_grad=True)
torch.relu(r).sum().backward()
print('relu    :', torch.relu(r).tolist(), "relu':", r.grad.tolist())

# Bước 2
def depth_probe(std, depth=10, width=256):
    torch.manual_seed(0)                   # cùng dữ liệu và cùng ma trận cho mọi std
    h = torch.randn(512, width)
    weights = [(torch.randn(width, width) * std).requires_grad_() for _ in range(depth)]
    scales = []
    for w in weights:
        pre = h @ w                        # pre-activation, shape (512, 256)
        scales.append(pre.std().item())
        h = torch.relu(pre)
    h.mean().backward()                    # loss đơn giản để đo gradient về lớp 1
    return scales, weights[0].grad.norm().item()

scales_small, grad_small = depth_probe(0.01)
scales_he, grad_he = depth_probe((2 / 256) ** 0.5)
print('std pre-activation ở lớp 1, 4, 7, 10 và ‖grad W1‖:')
for name, scales, grad in [('N(0,0.01²)', scales_small, grad_small), ('He', scales_he, grad_he)]:
    print(f'{name:10s}', [float(f'{v:.2g}') for v in scales[::3]], f'{grad:.2g}')

# Bước 3
prediction = torch.tensor([1., 5., 12.])
target = torch.tensor([2., 3., 2.])
assert prediction.shape == target.shape
print('residual:', (prediction - target).tolist())
print('MSE:', round(F.mse_loss(prediction, target).item(), 4))
print('MAE:', round(F.l1_loss(prediction, target).item(), 4))
print('per item:', F.mse_loss(prediction, target, reduction='none').tolist())

# Bước 4
logits_np = np.array([-2., 0., 2., -1000., 1000.])
labels_np = np.array([0., 1., 1., 0., 1.])
stable_bce = np.maximum(logits_np, 0) - logits_np * labels_np
stable_bce += np.log1p(np.exp(-np.abs(logits_np)))
logits = torch.tensor(logits_np, requires_grad=True)
labels = torch.tensor(labels_np)
individual = F.binary_cross_entropy_with_logits(logits, labels, reduction='none')
print(np.round(stable_bce, 6).tolist())
print('match:', np.allclose(stable_bce, individual.detach().numpy()))
individual.sum().backward()
print('gradient:', [round(v, 6) for v in logits.grad.tolist()])

# Bước 5
scores = torch.tensor([[np.log(2.), 0.], [0., np.log(2.)]], dtype=torch.float64)
classes = torch.tensor([0, 1], dtype=torch.long)
probabilities = scores.softmax(dim=1)
hand_loss = -probabilities[torch.arange(2), classes].log().mean()
correct_loss = F.cross_entropy(scores, classes)
double_softmax_loss = F.cross_entropy(probabilities, classes)
print(probabilities.tolist())
print(round(hand_loss.item(), 6), round(correct_loss.item(), 6))
print('softmax twice:', round(double_softmax_loss.item(), 6))
print('prediction:', scores.argmax(dim=1).tolist())

# Bước 6
import warnings

out = torch.tensor([[2.], [-1.], [0.5], [-3.]])     # (4, 1): đầu ra nn.Linear(h, 1)
y = torch.tensor([1., 0., 1., 0.])                  # (4,), float

def try_loss(name, call):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')         # đếm cảnh báo thay vì in ra
        try:
            value = call()
        except (ValueError, RuntimeError) as err:
            print(f'{name}: dừng, {type(err).__name__}')
            return
    print(f'{name}: chạy, loss {value.item():.4f}, {len(caught)} cảnh báo')

try_loss('BCE (4,1) và (4,)', lambda: F.binary_cross_entropy_with_logits(out, y))
try_loss('CE nhãn float    ', lambda: F.cross_entropy(torch.zeros(4, 3), y))
try_loss('L1  (4,1) và (4,)', lambda: F.l1_loss(out, y))
try_loss('BCE sau squeeze  ', lambda: F.binary_cross_entropy_with_logits(out.squeeze(1), y))
