# -*- coding: utf-8 -*-
# Code mẫu — Sử dụng model pretrained

# Ví dụ 1: Học một bài nguồn, lưu lại, rồi mở ra dùng
import io
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(41)
raw = torch.tensor([[10., 40.], [12., 60.], [14., 50.],
                    [26., 50.], [28., 40.], [30., 60.]])
mean = torch.tensor([20., 50.])
scale = torch.tensor([10., 10.])
X = (raw - mean) / scale
y = torch.tensor([0, 0, 0, 1, 1, 1])
source = nn.Linear(2, 2)
optimizer = torch.optim.SGD(source.parameters(), lr=0.2)
source.train()
for _ in range(120):
    optimizer.zero_grad(set_to_none=True)
    loss = nn.functional.cross_entropy(source(X), y)
    loss.backward()
    optimizer.step()

package = {
    "architecture": {"input_dim": 2, "classes": 2},
    "state_dict": source.state_dict(),
    "processor": {"mean": mean, "scale": scale},
    "labels": ["mat", "nong"],
    "origin": "local-sensor-source-v1",
}
stream = io.BytesIO()
torch.save(package, stream)
stream.seek(0)
saved = torch.load(stream, map_location="cpu", weights_only=True)
config = saved["architecture"]
restored = nn.Linear(config["input_dim"], config["classes"])
restored.load_state_dict(saved["state_dict"], strict=True)
restored.eval()
processor = saved["processor"]
source.eval()
new_raw = torch.tensor([[13., 50.], [27., 50.]])
new_X = (new_raw - processor["mean"]) / processor["scale"]
with torch.inference_mode():
    prediction = restored(new_X).argmax(dim=1)
    source_prediction = source(X).argmax(dim=1)
    same = torch.equal(restored(new_X), source(new_X))
assert same and prediction.tolist() == [0, 1]
print("nguon:", saved["origin"])
print("dung tren 6 hang nguon:", int((source_prediction == y).sum()))
print("nhan moi:", [saved["labels"][i] for i in prediction.tolist()])
print("nap lai giu output:", same)


# Ví dụ 2: Cùng trọng số, khác cách tiền xử lý, ra nhãn khác
import numpy as np
import torch
from torch import nn

torch.set_num_threads(1)
model = nn.Linear(2, 2, bias=False)
with torch.no_grad():
    model.weight.copy_(torch.tensor([[-1., 0.], [1., 0.]]))
model.eval()
raw = torch.tensor([[15., 50.], [25., 50.]])
mean = torch.tensor([20., 50.])
scale = torch.tensor([10., 10.])
with torch.inference_mode():
    correct = model((raw - mean) / scale)
    wrong = model(raw / scale)  # Shape vẫn đúng, nhưng nghĩa của đầu vào đã khác.
reference = np.array([[0.5, -0.5], [-0.5, 0.5]])
assert np.array_equal(correct.numpy(), reference)
labels = ["mat", "nong"]
print("logits dung:", correct.tolist())
print("processor dung:", [labels[i] for i in correct.argmax(1).tolist()])
print("quen tru mean:", [labels[i] for i in wrong.argmax(1).tolist()])

try:
    nn.Linear(2, 3, bias=False).load_state_dict(model.state_dict(), strict=True)
except RuntimeError:
    print("head 3 lop:", "tu choi checkpoint 2 lop")


# Ví dụ 3: Năm ID chạy qua các batch 2, 2 và 1
import torch
from torch import nn

torch.set_num_threads(1)
model = nn.Linear(2, 2, bias=False)
with torch.no_grad():
    model.weight.copy_(torch.tensor([[-1., 0.], [1., 0.]]))
model.eval()
ids = ["S9", "S2", "S7", "S1", "S4"]
raw = torch.tensor([[12., 50.], [28., 50.], [14., 60.],
                    [26., 40.], [13., 45.]])

def infer(values, batch_size):
    if batch_size < 1:
        raise ValueError("batch_size phai duong")
    parts = []
    with torch.inference_mode():
        for start in range(0, len(values), batch_size):
            batch = values[start:start + batch_size]
            z = (batch - torch.tensor([20., 50.])) / 10
            parts.append(model(z))
    return torch.cat(parts) if parts else torch.empty((0, 2))

logits = infer(raw, 2)
assert torch.equal(logits, infer(raw, 5))
assert infer(raw[:0], 2).shape == (0, 2)
expected = [int(float(row[0]) > 20) for row in raw]
predicted = logits.argmax(1).tolist()
assert predicted == expected
print("kich thuoc batch:", [len(raw[i:i + 2]) for i in range(0, len(raw), 2)])
print("ID, lop:", list(zip(ids, predicted)))
print("tap rong:", tuple(infer(raw[:0], 2).shape))
print("bytes trong so:", sum(p.numel() * p.element_size() for p in model.parameters()))

