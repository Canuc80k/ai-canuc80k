# -*- coding: utf-8 -*-
# Code mẫu — Training loop

# Ví dụ 1: Nhìn tham số ở ba thời điểm của một batch
import torch
from torch.utils.data import DataLoader, TensorDataset

torch.set_num_threads(1)
x = torch.arange(1., 6.).unsqueeze(1)
y = 2 * x
loader = DataLoader(TensorDataset(x, y), batch_size=2, shuffle=False)
print("kích thước các batch:", [len(xb) for xb, _ in loader])
weight = torch.nn.Parameter(torch.tensor(1.))
optimizer = torch.optim.SGD([weight], lr=.1)
xb, yb = next(iter(loader))
optimizer.zero_grad(set_to_none=True)
prediction = xb * weight
assert prediction.shape == yb.shape
loss = (prediction - yb).square().mean()
before = weight.item()
loss.backward()
print("loss, gradient:", loss.item(), weight.grad.item())
print("trước / sau backward:", before, weight.item())
optimizer.step()
print("sau step:", weight.item())
assert before == 1. and weight.grad.item() == -5. and weight.item() == 1.5


# Ví dụ 2: Chia tập, chọn checkpoint, rồi suy luận từ trạng thái đã lưu
import copy
import io
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

torch.set_num_threads(1)
torch.manual_seed(41)
raw_train = torch.tensor([[-2., -1.], [-1., -1.], [-1., 1.], [-.5, -.5],
                          [.5, -1.], [.5, .5], [1., -1.], [1., 1.],
                          [2., 1.], [2., -1.], [-2., 1.], [-.5, 1.]])
raw_valid = torch.tensor([[-1.5, 0.], [-.5, 0.], [.5, 0.], [1.5, 0.]])
train_y = (raw_train[:, 0] + .5 * raw_train[:, 1] > 0).long()
valid_y = (raw_valid[:, 0] + .5 * raw_valid[:, 1] > 0).long()
mean = raw_train.mean(dim=0)
scale = raw_train.std(dim=0, unbiased=False).clamp_min(1e-6)
train_x, valid_x = (raw_train - mean) / scale, (raw_valid - mean) / scale
train_data = TensorDataset(train_x, train_y)
loader = DataLoader(train_data, batch_size=5, shuffle=True, num_workers=0,
                    generator=torch.Generator().manual_seed(41))
model = nn.Linear(2, 2)
optimizer = torch.optim.SGD(model.parameters(), lr=.2)
print("train / validation:", len(train_y), len(valid_y))
print("mean train:", [round(v, 4) for v in mean.tolist()])
print("batch mỗi epoch:", len(loader))

def evaluate(x, y):
    model.eval()
    with torch.no_grad():
        logits = model(x)
        loss = nn.functional.cross_entropy(logits, y).item()
        accuracy = (logits.argmax(dim=1) == y).float().mean().item()
    return loss, accuracy

best_loss, best_epoch, best_state = float("inf"), 0, None
print("epoch | loss trong loop | train eval | valid loss | valid accuracy")
for epoch in range(1, 31):
    model.train()
    total, seen = 0., 0
    for xb, yb in loader:
        optimizer.zero_grad(set_to_none=True)
        logits = model(xb)
        assert logits.shape == (len(yb), 2) and yb.dtype == torch.long
        loss = nn.functional.cross_entropy(logits, yb)
        assert torch.isfinite(loss)
        loss.backward()
        optimizer.step()
        total += loss.item() * len(yb)
        seen += len(yb)
    train_loss, _ = evaluate(train_x, train_y)
    valid_loss, valid_accuracy = evaluate(valid_x, valid_y)
    if valid_loss < best_loss:
        best_loss, best_epoch = valid_loss, epoch
        best_state = copy.deepcopy(model.state_dict())
    if epoch in [1, 5, 15, 30]:
        print(epoch, *[round(v, 4) for v in
                       [total / seen, train_loss, valid_loss, valid_accuracy]])
model.load_state_dict(best_state)
print("epoch được chọn:", best_epoch)
print("validation sau khôi phục:", tuple(round(v, 4) for v in evaluate(valid_x, valid_y)))
assert abs(evaluate(valid_x, valid_y)[0] - best_loss) < 1e-7

model.eval()
with torch.no_grad():
    expected = model(valid_x)
packet = {"state": best_state, "mean": mean, "scale": scale,
          "features": ["x1", "x2"], "classes": ["không", "có"]}
buffer = io.BytesIO()
torch.save(packet, buffer)
buffer.seek(0)
restored = torch.load(buffer, map_location="cpu", weights_only=True)
fresh = nn.Linear(2, 2)
fresh.load_state_dict(restored["state"])
fresh.eval()
with torch.no_grad():
    new_x = (raw_valid - restored["mean"]) / restored["scale"]
    actual = fresh(new_x)
print("logits khôi phục khớp:", torch.allclose(expected, actual))
print("nhãn bốn mẫu mới:", actual.argmax(dim=1).tolist())
print("thứ tự feature:", restored["features"])
assert torch.allclose(expected, actual) and not actual.requires_grad


# Ví dụ 3: Batch cuối nhỏ không được tính ngang một batch đầy
import torch
from torch.utils.data import DataLoader

torch.set_num_threads(1)
item_losses = torch.tensor([1., 1., 1., 9.])
loader = DataLoader(item_losses, batch_size=3, shuffle=False)
batch_means, total, seen = [], 0., 0
for losses in loader:
    mean_loss = losses.mean().item()
    batch_means.append(mean_loss)
    total += mean_loss * len(losses)
    seen += len(losses)
print("mean từng batch:", batch_means)
print("mean ngang batch / theo mẫu:", sum(batch_means) / len(batch_means), total / seen)
assert total / seen == item_losses.mean().item() == 3.

