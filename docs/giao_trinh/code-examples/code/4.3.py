# -*- coding: utf-8 -*-
# Code mẫu — Fine-tuning

# Ví dụ 1: Mở tham số mà quên đưa vào optimizer
import torch
from torch import nn

torch.set_num_threads(1)
w = nn.Parameter(torch.tensor(3.0))
a = nn.Parameter(torch.tensor(1.0))
optimizer = torch.optim.SGD([
    {"params": [a], "lr": 0.02},
    {"params": [w], "lr": 0.005},
])
loss = (a * w * 2 - 8)**2
loss.backward()
assert w.grad.item() == -8 and a.grad.item() == -24
print("gradient head/encoder:", a.grad.item(), w.grad.item())
optimizer.step()
print("sau buoc head/encoder:", round(a.item(), 2), round(w.item(), 2))

w2 = nn.Parameter(torch.tensor(3.0))
a2 = nn.Parameter(torch.tensor(1.0))
head_only_optimizer = torch.optim.SGD([a2], lr=0.02)
((a2 * w2 * 2 - 8)**2).backward()
head_only_optimizer.step()
print("quen encoder trong optimizer:", "co gradient =", w2.grad is not None,
      "w =", w2.item())
assert w2.item() == 3


# Ví dụ 2: Giữ block đầu, thử mở block cuối
import copy
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(43)
axis = torch.tensor([-1., -.7, -.4, -.1, .1, .4, .7, 1.])
source_X = torch.cartesian_prod(axis, axis)
source_y = (2 * (source_X[:, 0] > 0) + (source_X[:, 1] > 0)).long()
source_encoder = nn.Sequential(nn.Linear(2, 8), nn.Tanh(),
                               nn.Linear(8, 4), nn.Tanh())
source_model = nn.Sequential(source_encoder, nn.Linear(4, 4))
source_model.train()
source_optimizer = torch.optim.Adam(source_model.parameters(), lr=0.04)
for _ in range(120):
    source_optimizer.zero_grad(set_to_none=True)
    loss = nn.functional.cross_entropy(source_model(source_X), source_y)
    loss.backward()
    source_optimizer.step()
source_encoder.zero_grad(set_to_none=True)
source_model.eval()

generator = torch.Generator().manual_seed(430)
target_X = torch.rand((104, 2), generator=generator) * 2 - 1
target_y = (target_X[:, 0] + 0.6 * target_X[:, 1] > 0.15).long()
train_X, valid_X = target_X[:24], target_X[24:]
train_y, valid_y = target_y[:24], target_y[24:]
initial_head = nn.Linear(4, 2)
with torch.no_grad():
    source_correct = int((source_model(source_X).argmax(1) == source_y).sum())
print("nguon dung:", source_correct, "/ 64")
print("target train/valid:", len(train_y), len(valid_y))

def fit_transfer(open_last):
    encoder = copy.deepcopy(source_encoder)
    head = copy.deepcopy(initial_head)
    encoder.requires_grad_(False)
    if open_last:
        encoder[2].requires_grad_(True)
    model = nn.Sequential(encoder, head)
    before = copy.deepcopy(encoder.state_dict())
    groups = [{"params": head.parameters(), "lr": 0.04}]
    if open_last:
        groups.append({"params": encoder[2].parameters(), "lr": 0.004})
    optimizer = torch.optim.Adam(groups)
    best_loss = float("inf")
    best_state, best_epoch = None, None
    for epoch in range(1, 101):
        model.train()
        encoder.eval()  # Mạng này không có Dropout hay BatchNorm, nhưng vẫn ghi rõ chế độ của encoder.
        optimizer.zero_grad(set_to_none=True)
        loss = nn.functional.cross_entropy(model(train_X), train_y)
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            valid_loss = nn.functional.cross_entropy(model(valid_X), valid_y).item()
        if valid_loss < best_loss:
            best_loss, best_epoch = valid_loss, epoch
            best_state = copy.deepcopy(model.state_dict())
    model.load_state_dict(best_state)
    with torch.inference_mode():
        correct = int((model(valid_X).argmax(1) == valid_y).sum())
    first_fixed = all(torch.equal(before[name], encoder.state_dict()[name])
                      for name in ["0.weight", "0.bias"])
    last_changed = any(not torch.equal(before[name], encoder.state_dict()[name])
                       for name in ["2.weight", "2.bias"])
    assert first_fixed and last_changed == open_last
    count = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return best_epoch, best_loss, correct, count, first_fixed, last_changed

for opened in [False, True]:
    epoch, loss, correct, count, first_fixed, last_changed = fit_transfer(opened)
    print("mo block cuoi:", opened, "trainable:", count, "epoch:", epoch)
    print("valid loss:", round(loss, 4), "dung:", correct, "/ 80")
    print("block dau giu nguyen:", first_fixed, "block cuoi doi:", last_changed)


# Ví dụ 3: Khóa tham số không giữ yên thống kê của BatchNorm
import torch
from torch import nn

torch.set_num_threads(1)
bn = nn.BatchNorm1d(1, momentum=0.25)
bn.requires_grad_(False)
bn.running_mean.fill_(2)
batch = torch.tensor([[6.], [10.]])
bn.train()
with torch.no_grad():
    bn(batch)
after = bn.running_mean.clone()
assert after.item() == 3.5
bn.eval()
with torch.no_grad():
    bn(batch + 100)
print("sau train forward:", after.item())
print("eval giu mean:", torch.equal(after, bn.running_mean))
print("tham so co gradient:", any(p.grad is not None for p in bn.parameters()))

