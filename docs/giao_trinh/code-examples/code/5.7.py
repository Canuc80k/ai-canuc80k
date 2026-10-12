# -*- coding: utf-8 -*-
# Code mẫu — Self-supervised và CLIP

# Ví dụ 1: Tìm câu mô tả hợp nhất theo cosine
import numpy as np

def normalize(vectors):
    vectors = np.asarray(vectors, dtype=float)
    lengths = np.linalg.norm(vectors, axis=1, keepdims=True)
    if np.any(lengths == 0):
        raise ValueError("Vector 0 không có hướng cosine")
    return vectors / lengths

images = normalize([[1, 0], [0, 1], [-1, 0]])
texts = normalize([[0.9, 0.1], [0.1, 0.9], [-0.9, 0.1]])
similarity = images @ texts.T
print("Cosine:", similarity.round(4).tolist())
print("Mô tả tốt nhất cho từng ảnh:", similarity.argmax(1).tolist())
print("Hai ảnh đầu cho mô tả 1:", np.argsort(-similarity[:, 1], kind="stable")[:2].tolist())
assert np.isclose(similarity[0, 0], 0.9 / np.sqrt(0.82))
assert similarity.argmax(1).tolist() == [0, 1, 2]
try:
    normalize([[0, 0]])
except ValueError:
    print("Vector 0: bị từ chối")
else:
    raise AssertionError("Chưa bắt vector 0")


# Ví dụ 2: Temperature đổi độ chắc chắn, gradient kéo đúng cặp lên
import torch
import torch.nn.functional as F

torch.set_num_threads(1)
images = F.normalize(torch.tensor([[1., 0.], [0., 1.], [-1., 0.]]), dim=1)
texts = F.normalize(torch.tensor([[0.9, 0.1], [0.1, 0.9], [-0.9, 0.1]]), dim=1)
similarity = images @ texts.T
target = torch.arange(3)
for temperature in [0.5, 0.1]:
    logits = (similarity / temperature).detach().requires_grad_(True)
    loss = (F.cross_entropy(logits, target) + F.cross_entropy(logits.T, target)) / 2
    loss.backward()
    print("Temperature", temperature, "loss:", round(loss.item(), 4))
    print("P(caption đúng | ảnh 0):", round(logits.softmax(1)[0, 0].item(), 4))
    print("Gradient logit đúng âm:", bool((logits.grad.diag() < 0).all()))
    print("Gradient negative [0,1] dương:", bool(logits.grad[0, 1] > 0))
    assert (logits.grad.diag() < 0).all() and logits.grad[0, 1] > 0
assert (similarity / 0.1).argmax(1).tolist() == (similarity / 0.5).argmax(1).tolist()


# Ví dụ 3: Hai câu cùng đúng, nhưng loss chỉ công nhận một
import math
import torch
import torch.nn.functional as F

torch.set_num_threads(1)
logits = torch.tensor([[2., 2.]], requires_grad=True)
loss = F.cross_entropy(logits, torch.tensor([0]))
loss.backward()
print("Loss hai caption cùng điểm:", round(loss.item(), 4))
print("Gradient:", logits.grad.tolist())
assert math.isclose(loss.item(), math.log(2), rel_tol=1e-6)
assert logits.grad.tolist() == [[-0.5, 0.5]]

old = torch.tensor([2., 0.]).softmax(0)
expanded = torch.tensor([2., 0., 2.]).softmax(0)
print("Hai ứng viên:", [round(v, 4) for v in old.tolist()])
print("Thêm ứng viên trùng:", [round(v, 4) for v in expanded.tolist()])
assert expanded[0] < old[0]

