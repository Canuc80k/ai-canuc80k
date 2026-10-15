# -*- coding: utf-8 -*-
# Training loop — chạy các bước như notebook từ trên xuống.

# Bước 1
from pathlib import Path
import json
import subprocess
import sys
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader

torch.set_num_threads(1)
torch.manual_seed(21)
torch.use_deterministic_algorithms(True)
generator = torch.Generator().manual_seed(21)
raw_X = torch.randn(96, 2, generator=generator)
y = (raw_X[:, 0] + .5 * raw_X[:, 1] > 0).long()
order = torch.randperm(96, generator=generator)
train_id, valid_id = order[:72], order[72:]
mean = raw_X[train_id].mean(dim=0)
scale = raw_X[train_id].std(dim=0, unbiased=False).clamp_min(1e-6)
X = (raw_X - mean) / scale
train_data = TensorDataset(X[train_id], y[train_id])
valid_data = TensorDataset(X[valid_id], y[valid_id])
train_loader = DataLoader(train_data, batch_size=16, shuffle=True,
    generator=torch.Generator().manual_seed(21), num_workers=0)
valid_loader = DataLoader(valid_data, batch_size=16, shuffle=False, num_workers=0)
print(len(train_data), len(valid_data), len(train_loader))
print(tuple(next(iter(valid_loader))[0].shape))

# Bước 2
w = torch.zeros(2, requires_grad=True)
for xi in [torch.tensor([1., 2.]), torch.tensor([3., -1.])]:
    (xi @ w).backward()
    print(w.grad.tolist())

# Bước 3
def make_model():
    return nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2))

model = make_model()
optimizer = torch.optim.Adam(model.parameters(), lr=.03)
criterion = nn.CrossEntropyLoss()

def train_epoch(model, loader, optimizer):
    model.train()
    loss_sum = 0.
    seen = 0
    for xb, yb in loader:
        optimizer.zero_grad(set_to_none=True)
        logits = model(xb)
        assert logits.shape == (len(yb), 2)
        loss = criterion(logits, yb)
        assert torch.isfinite(loss)
        loss.backward()
        optimizer.step()
        loss_sum += loss.item() * len(yb)
        seen += len(yb)
    return loss_sum / seen

def evaluate(model, loader):
    model.eval()
    loss_sum = 0.
    correct = 0
    seen = 0
    with torch.no_grad():
        for xb, yb in loader:
            logits = model(xb)
            loss_sum += criterion(logits, yb).item() * len(yb)
            correct += (logits.argmax(dim=1) == yb).sum().item()
            seen += len(yb)
    return loss_sum / seen, correct / seen

print('initial validation:', tuple(round(v, 4) for v in evaluate(model, valid_loader)))

# Bước 4
best_loss = float('inf')
best_epoch = -1
best_state = None
history = []
for epoch in range(35):
    training_loss = train_epoch(model, train_loader, optimizer)
    valid_loss, valid_accuracy = evaluate(model, valid_loader)
    history.append((epoch + 1, training_loss, valid_loss, valid_accuracy))
    if valid_loss < best_loss:
        best_loss = valid_loss
        best_epoch = epoch + 1
        best_state = {name: value.detach().cpu().clone()
                      for name, value in model.state_dict().items()}
    if epoch in [0, 9, 19, 34]:
        print(epoch + 1, round(training_loss, 4),
              round(valid_loss, 4), round(valid_accuracy, 4))

perfect = [e for e, _, _, accuracy in history if accuracy == 1.0]
print('accuracy 1.0:', len(perfect), 'epochs, first', perfect[0])
model.load_state_dict(best_state)
model.eval()
print('best epoch:', best_epoch)
print('best validation:', tuple(round(v, 4) for v in evaluate(model, valid_loader)))

# Bước 5
artifact_dir = Path('receipts/phase-3')
artifact_dir.mkdir(parents=True, exist_ok=True)
checkpoint_path = artifact_dir / '3-4-best.pt'
query = torch.tensor([[1., 0.], [-1., 0.]])
with torch.no_grad():
    expected = model((query - mean) / scale)
torch.save({'state': best_state, 'mean': mean, 'scale': scale,
            'query': query, 'expected': expected, 'epoch': best_epoch}, checkpoint_path)
fresh = make_model()
packet = torch.load(checkpoint_path, map_location='cpu', weights_only=True)
fresh.load_state_dict(packet['state'])
fresh.eval()
with torch.no_grad():
    reloaded = fresh((packet['query'] - packet['mean']) / packet['scale'])
print('same logits:', torch.allclose(reloaded, expected, atol=1e-7))
print('classes:', reloaded.argmax(dim=1).tolist())

# Bước 6
inference_source = '''import sys
import torch
from torch import nn
torch.set_num_threads(1)
packet = torch.load(sys.argv[1], map_location="cpu", weights_only=True)
model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2))
model.load_state_dict(packet["state"])
model.eval()
with torch.no_grad():
    x = (packet["query"] - packet["mean"]) / packet["scale"]
    logits = model(x)
print("new process match:", torch.allclose(logits, packet["expected"], atol=1e-7))
print("new process classes:", logits.argmax(dim=1).tolist())
'''
inference_path = artifact_dir / '3-4-infer.py'
inference_path.write_text(inference_source, encoding='utf-8')
result = subprocess.check_output([sys.executable, '-B', '-X', 'utf8',
    str(inference_path), str(checkpoint_path)], text=True)
print(result.rstrip())

# Bước 7
import numpy as np
import pandas as pd
from PIL import Image
from tempfile import TemporaryDirectory
from torch.utils.data import Dataset

class FolderDataset(Dataset):
    def __init__(self, root, table, size=8):
        self.root, self.table, self.size = Path(root), table.reset_index(drop=True), size

    def __len__(self):
        return len(self.table)

    def __getitem__(self, i):
        row = self.table.iloc[i]
        image = Image.open(self.root / row["file"]).convert("L").resize((self.size, self.size))
        x = torch.from_numpy(np.asarray(image, dtype=np.float32) / 255).unsqueeze(0)   # (1, H, W)
        return x, int(row["label"])

with TemporaryDirectory() as directory:
    root = Path(directory)
    rng = np.random.default_rng(0)
    rows = []
    for i in range(10):
        w, h = rng.integers(10, 30, size=2)                    # mỗi ảnh một kích thước
        label = i % 2                                          # nhãn 1: ảnh sáng hơn
        pixels = rng.integers(0, 120, size=(h, w)) + 120 * label
        Image.fromarray(pixels.astype(np.uint8)).save(root / f"{i}.png")
        rows.append({"file": f"{i}.png", "label": label})
    data = FolderDataset(root, pd.DataFrame(rows))
    loader = DataLoader(data, batch_size=4, shuffle=False, num_workers=0)
    xb, yb = next(iter(loader))
    print(len(data), len(loader), tuple(data[0][0].shape), tuple(xb.shape), yb.tolist())
    print(round(float(xb[yb == 0].mean()), 3), round(float(xb[yb == 1].mean()), 3))

# Bước 8
from torch.nn.utils.rnn import pad_sequence

pairs = [(torch.tensor([5, 2, 9]), 1), (torch.tensor([7]), 0), (torch.tensor([3, 3, 1, 4]), 1)]
try:
    next(iter(DataLoader(pairs, batch_size=3)))
except RuntimeError as error:
    print("không có collate_fn:", str(error).split(" at entry")[0])

def pad_collate(batch):
    seqs, labels = zip(*batch)
    lengths = torch.tensor([len(s) for s in seqs])
    padded = pad_sequence(seqs, batch_first=True, padding_value=0)
    return padded, lengths, torch.tensor(labels)

for tokens, lengths, labels in DataLoader(pairs, batch_size=3, collate_fn=pad_collate):
    print(tokens)
    print(lengths.tolist(), labels.tolist())
