# -*- coding: utf-8 -*-
# Code mẫu — Regularization cho mạng neural

# Ví dụ 1: Dropout giữ đúng trung bình, không giữ từng đầu ra
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(53)
h = torch.arange(1., 9.)
mask = torch.tensor([1., 0., 1., 0., 1., 0., 1., 0.])
print("mask tính tay:", (h * mask / .5).tolist())
dropout = nn.Dropout(p=.5)
dropout.train()
with torch.no_grad():
    first, second = dropout(h), dropout(h)
print("train lượt 1:", first.tolist())
print("train lượt 2:", second.tolist())
print("no_grad làm hai lượt bằng nhau:", torch.equal(first, second))
dropout.eval()
print("eval:", dropout(h).tolist())
assert torch.equal(dropout(h), h)
assert ((first == 0) | (first == 2 * h)).all()


# Ví dụ 2: BatchNorm, và một lượt validation chạy nhầm chế độ
import copy
import torch
from torch import nn

torch.set_num_threads(1)
batch = torch.tensor([[1., 10.], [3., 14.]])
bn = nn.BatchNorm1d(2, affine=False, momentum=1.)
bn.train()
train_output = bn(batch)
state = copy.deepcopy(bn.state_dict())
bn.eval()
eval_output = bn(batch)
rounded = lambda t: [[round(x, 4) for x in row] for row in t.tolist()]
print("train:", rounded(train_output))
print("running mean:", bn.running_mean.tolist())
print("running variance:", bn.running_var.tolist())
print("eval:", rounded(eval_output))
assert torch.allclose(bn.running_mean, torch.tensor([2., 12.]))
assert torch.allclose(bn.running_var, torch.tensor([2., 8.]))

validation = batch + 100
bn.train()
with torch.no_grad():
    bn(validation)
print("running mean sau validation ở train:", bn.running_mean.tolist())

bn.load_state_dict(state)
bn.eval()
before = bn.running_mean.clone()
with torch.no_grad():
    bn(validation)
print("running mean sau validation ở eval:", bn.running_mean.tolist())
print("buffer giữ nguyên:", torch.equal(before, bn.running_mean))
assert torch.equal(before, bn.running_mean)


# Ví dụ 3: Chọn epoch tốt nhất trước, rồi mới so weight decay
import copy
import torch
from torch import nn

torch.set_num_threads(1)
generator = torch.Generator().manual_seed(9)
train_x = torch.linspace(-1, 1, 16).unsqueeze(1)
train_y = train_x.square() + .18 * torch.randn(16, 1, generator=generator)
valid_x = torch.linspace(-1, 1, 64).unsqueeze(1)
valid_y = valid_x.square()
print("shape train / validation:", tuple(train_x.shape), tuple(valid_x.shape))
print("MSE của đường sạch trên nhãn train có nhiễu:",
      round((train_x.square() - train_y).square().mean().item(), 5))

def fit(decay):
    torch.manual_seed(29)  # Khởi tạo y hệt nhau cho mỗi giá trị decay.
    model = nn.Sequential(nn.Linear(1, 16), nn.Tanh(),
                          nn.Linear(16, 16), nn.Tanh(), nn.Linear(16, 1))
    optimizer = torch.optim.AdamW(model.parameters(), lr=.02, weight_decay=decay)
    best, best_epoch, waiting = float("inf"), 0, 0
    best_state, history = None, []
    for epoch in range(1, 121):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        loss = (model(train_x) - train_y).square().mean()
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            train_mse = (model(train_x) - train_y).square().mean().item()
            valid_mse = (model(valid_x) - valid_y).square().mean().item()
        history.append((epoch, train_mse, valid_mse))
        if valid_mse < best - 1e-5:
            best, best_epoch, waiting = valid_mse, epoch, 0
            best_state = copy.deepcopy(model.state_dict())
        else:
            waiting += 1
        if waiting == 15:
            break
    last = history[-1]
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        restored_mse = (model(valid_x) - valid_y).square().mean().item()
    assert abs(restored_mse - best) < 1e-7
    return history, best_epoch, restored_mse, last

for decay in [0., .1]:
    history, best_epoch, restored, last = fit(decay)
    print("decay", decay, "(epoch, train MSE, valid MSE):")
    for record in [history[0], history[best_epoch - 1], last]:
        print(record[0], round(record[1], 5), round(record[2], 5))
    print("khôi phục epoch", best_epoch, "valid MSE", round(restored, 5))

