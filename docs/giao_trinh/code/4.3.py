# -*- coding: utf-8 -*-
# Fine-tuning — chạy các bước như notebook từ trên xuống.

# Bước 1
import copy
import numpy as np
import torch
from torch import nn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

torch.set_num_threads(1)
torch.manual_seed(3)
digits = load_digits()
source_ids = np.flatnonzero(digits.target < 8)
target_ids = np.flatnonzero(digits.target >= 8)
source_train, source_valid = train_test_split(
    source_ids, test_size=0.25, stratify=digits.target[source_ids], random_state=3
)

def inputs(ids):
    return torch.tensor(digits.data[ids] / 16.0, dtype=torch.float32)

source_encoder = nn.Sequential(nn.Linear(64, 32), nn.ReLU())
source_head = nn.Linear(32, 8)
source_model = nn.Sequential(source_encoder, source_head)
source_optimizer = torch.optim.Adam(source_model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()
source_x = inputs(source_train)
source_y = torch.tensor(digits.target[source_train], dtype=torch.long)
for _ in range(80):
    source_model.train()
    source_optimizer.zero_grad(set_to_none=True)
    loss = criterion(source_model(source_x), source_y)
    loss.backward()
    source_optimizer.step()

source_model.eval()
with torch.no_grad():
    source_prediction = source_model(inputs(source_valid)).argmax(dim=1).numpy()
print("source train/valid:", len(source_train), len(source_valid))
print("source valid accuracy:", round(float((source_prediction == digits.target[source_valid]).mean()), 4))
print("source gap target:", len(set(source_ids) & set(target_ids)) == 0)

# Bước 2
target_train, target_valid = train_test_split(
    target_ids, train_size=48, random_state=5, stratify=digits.target[target_ids]
)
target_x = inputs(target_train)
target_y = torch.tensor(digits.target[target_train] - 8, dtype=torch.long)
valid_x = inputs(target_valid)
valid_y = torch.tensor(digits.target[target_valid] - 8, dtype=torch.long)

torch.manual_seed(10)
initial_head = nn.Linear(32, 2)
head_only = nn.Sequential(copy.deepcopy(source_encoder), copy.deepcopy(initial_head))
for parameter in head_only[0].parameters():
    parameter.requires_grad_(False)
optimizer = torch.optim.SGD(head_only[1].parameters(), lr=0.05)
before = {name: value.detach().clone() for name, value in head_only[0].named_parameters()}

head_only.train()
head_only[0].eval()
optimizer.zero_grad(set_to_none=True)
loss = criterion(head_only(target_x), target_y)
loss.backward()
print("encoder grad None:", all(p.grad is None for p in head_only[0].parameters()))
print("head co gradient:", head_only[1].weight.grad.norm().item() > 0)
optimizer.step()
print("encoder khong doi:", all(torch.equal(before[n], p) for n, p in head_only[0].named_parameters()))
print("target train/valid:", len(target_train), len(target_valid))

# Bước 3
x, w, a, y = 1.0, 2.0, 1.0, 3.0
residual = a * w * x - y
grad_a = 2 * residual * w * x
grad_w = 2 * residual * a * x
print("gradient:", grad_a, grad_w)
print("sau buoc:", a - 0.1 * grad_a, w - 0.01 * grad_w)

# Bước 4
def run_transfer(open_encoder):
    transferred = nn.Sequential(copy.deepcopy(source_encoder), copy.deepcopy(initial_head))
    for parameter in transferred[0].parameters():
        parameter.requires_grad_(open_encoder)
    groups = [{"params": transferred[1].parameters(), "lr": 0.05}]
    if open_encoder:
        groups.append({"params": transferred[0].parameters(), "lr": 0.003})
    optimizer = torch.optim.Adam(groups)
    best_loss = float("inf")
    best_state, best_epoch = None, None
    history = []
    for epoch in range(1, 61):
        transferred.train()
        if not open_encoder:
            transferred[0].eval()
        optimizer.zero_grad(set_to_none=True)
        train_loss = criterion(transferred(target_x), target_y)
        train_loss.backward()
        optimizer.step()
        transferred.eval()
        with torch.no_grad():
            val_loss = criterion(transferred(valid_x), valid_y).item()
        history.append((train_loss.item(), val_loss))
        if val_loss < best_loss:
            best_loss = val_loss
            best_epoch = epoch
            best_state = copy.deepcopy(transferred.state_dict())
    transferred.load_state_dict(best_state)
    with torch.no_grad():
        accuracy = (transferred(valid_x).argmax(dim=1) == valid_y).float().mean().item()
    trainable = sum(p.numel() for p in transferred.parameters() if p.requires_grad)
    return transferred, history, best_epoch, best_loss, accuracy, trainable

for opened in [False, True]:
    net, history, epoch, val_loss, accuracy, count = run_transfer(opened)
    print("open encoder =", opened, "| trainable =", count, "| best epoch =", epoch)
    print("best val loss =", round(val_loss, 4),
          "| epoch 60 val loss =", round(history[-1][1], 4),
          "| val accuracy =", round(accuracy, 4))

# Bước 5
bn = nn.BatchNorm1d(2, momentum=0.5)
for parameter in bn.parameters():
    parameter.requires_grad_(False)
batch = torch.tensor([[2., 4.], [4., 8.]])
bn.train()
with torch.no_grad():
    bn(batch)
after_train = bn.running_mean.clone()
bn.eval()
with torch.no_grad():
    bn(batch + 100)
print("running mean sau train:", after_train.tolist())
print("eval giu buffer:", torch.equal(after_train, bn.running_mean))
print("khop tinh tay:", torch.allclose(after_train, batch.mean(dim=0) * 0.5))
