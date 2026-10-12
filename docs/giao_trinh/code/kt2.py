# -*- coding: utf-8 -*-
# Kiểm tra khóa 2 — chạy các bước như notebook từ trên xuống.

# Bước 1
import io
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.metrics import accuracy_score, f1_score

torch.set_num_threads(1)
features = torch.tensor([[2., 0.], [0., 2.], [-1., -1.], [1.5, 0.]])
targets = np.array([0, 1, 2, 1])
class_names = ["nhom_A", "nhom_B", "nhom_C"]
head = nn.Linear(2, 3, bias=False)
with torch.no_grad():
    head.weight.copy_(torch.tensor([[1., 0.], [0., 1.], [-1., -1.]]))
head.eval()
with torch.inference_mode():
    logits = head(features)
    predictions = logits.argmax(dim=1).numpy()
assert logits.shape == (4, 3)
assert np.isfinite(logits.numpy()).all()
print("du doan:", predictions.tolist())
print("accuracy:", accuracy_score(targets, predictions))
print("macro-F1:", round(f1_score(targets, predictions, labels=[0, 1, 2],
                                 average="macro", zero_division=0), 6))

# Bước 2
buffer = io.BytesIO()
torch.save({"state_dict": head.state_dict(), "class_names": class_names,
            "input_dim": 2}, buffer)
buffer.seek(0)
saved = torch.load(buffer, map_location="cpu", weights_only=True)
restored = nn.Linear(saved["input_dim"], len(saved["class_names"]), bias=False)
restored.load_state_dict(saved["state_dict"])
restored.eval()
with torch.inference_mode():
    restored_logits = restored(features)
assert torch.equal(logits, restored_logits)
sample_ids = [43, 41, 42, 44]
submission = pd.DataFrame({"id": sample_ids, "label": predictions})
csv_buffer = io.StringIO()
submission.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)
read_back = pd.read_csv(csv_buffer)
assert read_back["id"].tolist() == sample_ids
assert read_back["id"].is_unique and len(read_back) == len(features)
assert read_back["label"].between(0, len(class_names) - 1).all()
print("tai lai trung:", torch.equal(logits, restored_logits))
print(read_back.to_string(index=False))
