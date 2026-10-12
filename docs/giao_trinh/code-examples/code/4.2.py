# -*- coding: utf-8 -*-
# Code mẫu — Feature extraction

# Ví dụ 1: Gộp token mà không lẫn padding vào câu
import numpy as np
import torch

torch.set_num_threads(1)
hidden = torch.tensor([[[2., 0.], [0., 4.], [90., 90.]],
                       [[1., 1.], [3., 1.], [2., 4.]]])
mask = torch.tensor([[1, 1, 0], [1, 1, 1]], dtype=torch.bool)

def masked_mean(values, valid):
    counts = valid.sum(dim=1, keepdim=True)
    if (counts == 0).any():
        raise ValueError("cau khong co token hop le")
    weights = valid.unsqueeze(-1).to(values.dtype)
    return (values * weights).sum(dim=1) / counts

pooled = masked_mean(hidden, mask)
independent = np.stack([row[keep].mean(axis=0)
                        for row, keep in zip(hidden.numpy(), mask.numpy())])
assert np.allclose(pooled.numpy(), independent)
print("vector cau:", pooled.tolist())
print("khong mask, cau dau:", [round(float(v), 3) for v in hidden.mean(dim=1)[0]])
print("shape sau pooling:", tuple(pooled.shape))
try:
    masked_mean(hidden[:1], torch.zeros((1, 3), dtype=torch.bool))
except ValueError as error:
    print("cau rong:", str(error))


# Ví dụ 2: Cosine xét hướng, tích vô hướng xét cả độ dài
import numpy as np

query = np.array([[1., 0.]])
database = np.array([[2., 0.], [9., 3.], [0., 2.]])
ids = np.array(["A", "B", "C"])

def unit_rows(values):
    lengths = np.linalg.norm(values, axis=1, keepdims=True)
    if np.any(lengths == 0):
        raise ValueError("vector 0 khong co huong")
    return values / lengths

dot = (query @ database.T)[0]
cosine = (unit_rows(query) @ unit_rows(database).T)[0]
reference_B = 9 / np.sqrt(9**2 + 3**2)
assert np.isclose(cosine[1], reference_B)
normalized_distance = np.linalg.norm(unit_rows(database) - unit_rows(query), axis=1)
assert np.allclose(normalized_distance**2, 2 - 2 * cosine)
print("dot:", dot.tolist(), "chon:", ids[dot.argmax()])
print("cosine:", cosine.round(4).tolist(), "chon:", ids[cosine.argmax()])
print("khoang cach sau normalize:", normalized_distance.round(4).tolist())
try:
    unit_rows(np.array([[0., 0.]]))
except ValueError as error:
    print("vector 0:", str(error))


# Ví dụ 3: Encoder học trước, lớp đầu ra mới học nhãn mới
import copy
import numpy as np
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(42)
axis = torch.tensor([-1., -.7, -.4, -.1, .1, .4, .7, 1.])
source_X = torch.cartesian_prod(axis, axis)
source_y = (2 * (source_X[:, 0] > 0) + (source_X[:, 1] > 0)).long()
encoder = nn.Sequential(nn.Linear(2, 8), nn.Tanh())
source_head = nn.Linear(8, 4)
source_model = nn.Sequential(encoder, source_head)
source_model.train()
optimizer = torch.optim.Adam(source_model.parameters(), lr=0.04)
for _ in range(100):
    optimizer.zero_grad(set_to_none=True)
    loss = nn.functional.cross_entropy(source_model(source_X), source_y)
    loss.backward()
    optimizer.step()

generator = torch.Generator().manual_seed(420)
target_X = torch.rand((72, 2), generator=generator) * 2 - 1
target_y = (target_X.sum(dim=1) > 0).long()
train_X, valid_X = target_X[:40], target_X[40:]
train_y, valid_y = target_y[:40], target_y[40:]
encoder.eval()
source_model.eval()
encoder.requires_grad_(False)
encoder.zero_grad(set_to_none=True)
before = copy.deepcopy(encoder.state_dict())
# no_grad cho ra tensor thường. Lớp đầu ra ở bước sau vẫn được tính gradient bình thường.
with torch.no_grad():
    train_Z, valid_Z = encoder(train_X), encoder(valid_X)
    source_correct = int((source_model(source_X).argmax(1) == source_y).sum())
print("nguon dung:", source_correct, "/", len(source_X))
print("embedding train/valid:", tuple(train_Z.shape), tuple(valid_Z.shape))

head = nn.Linear(8, 2)
optimizer = torch.optim.Adam(head.parameters(), lr=0.04)
for _ in range(100):
    head.train()
    optimizer.zero_grad(set_to_none=True)
    loss = nn.functional.cross_entropy(head(train_Z), train_y)
    loss.backward()
    optimizer.step()
head.eval()
with torch.inference_mode():
    prediction = head(valid_Z).argmax(1)
correct = int((prediction == valid_y).sum())
encoder_unchanged = all(torch.equal(before[k], value)
                        for k, value in encoder.state_dict().items())
assert encoder_unchanged and all(p.grad is None for p in encoder.parameters())
assert np.array_equal(target_y.numpy(), (target_X.numpy().sum(axis=1) > 0).astype(int))
print("validation dung:", correct, "/", len(valid_y))
print("encoder giu nguyen:", encoder_unchanged)
print("tham so head:", sum(p.numel() for p in head.parameters()))

