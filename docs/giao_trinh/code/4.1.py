# -*- coding: utf-8 -*-
# Sử dụng model pretrained — chạy các bước như notebook từ trên xuống.

# Bước 1
import io
import numpy as np
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(0)
source = nn.Linear(2, 3)
with torch.no_grad():
    source.weight.copy_(torch.tensor([[1., -1.], [-1., 1.], [.5, .5]]))
    source.bias.copy_(torch.tensor([0., 0., .25]))

package = {
    "state_dict": source.state_dict(),
    "mean": torch.tensor([10., 10.]),
    "scale": torch.tensor([2., 2.]),
    "labels": ["hoat_dong_A", "hoat_dong_B", "chua_ro"],
}
buffer = io.BytesIO()
torch.save(package, buffer)
buffer.seek(0)
loaded = torch.load(buffer, map_location="cpu", weights_only=True)

model = nn.Linear(2, 3)
model.load_state_dict(loaded["state_dict"], strict=True)
model.eval()
print("shape W:", tuple(model.weight.shape))
print("nhan:", loaded["labels"])

# Bước 2
def process(raw):
    raw_tensor = torch.as_tensor(raw, dtype=torch.float32)
    return (raw_tensor - loaded["mean"]) / loaded["scale"]

raw = np.array([[12., 8.], [8., 12.], [10., 10.], [14., 6.], [9., 11.]])
with torch.inference_mode():
    logits = model(process(raw))
    predicted = logits.argmax(dim=1)
print(logits.numpy().round(2))
print([loaded["labels"][i] for i in predicted.tolist()])

# Bước 3
def infer_batches(raw, batch_size):
    rows = []
    with torch.inference_mode():
        for start in range(0, len(raw), batch_size):
            rows.append(model(process(raw[start:start + batch_size])))
    return torch.cat(rows, dim=0)

batched = infer_batches(raw, batch_size=2)
z_numpy = (raw - np.array([10., 10.])) / np.array([2., 2.])
W_numpy = np.array([[1., -1.], [-1., 1.], [.5, .5]])
expected = z_numpy @ W_numpy.T + np.array([0., 0., .25])
print("batch khop:", torch.allclose(batched, logits))
print("NumPy khop:", np.allclose(batched.numpy(), expected))
print("so mau:", len(batched))

# Bước 4
P = 100_000_000
print("FP32 MiB:", round(P * 4 / 2**20, 2))
print("FP16 MiB:", round(P * 2 / 2**20, 2))
input_bytes = 16 * 3 * 224 * 224 * 4
print("input batch MiB:", round(input_bytes / 2**20, 2))
actual_bytes = sum(p.numel() * p.element_size() for p in model.parameters())
print("mang tuyen tinh bytes:", actual_bytes)
