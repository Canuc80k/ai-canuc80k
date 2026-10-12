# Code mẫu — Ôn kiểm tra khóa 2

Buổi ôn này ghép mọi bước của một bài chuyển học thành một quy trình trọn vẹn: từ dữ liệu, qua học và chọn checkpoint, tới lưu model và xuất file dự đoán. Ví dụ thứ hai tập trung vào hai cái bẫy ở bước cuối: chọn sai tiêu chí, và gán nhầm ID.

## Ví dụ 1: Học lớp đầu ra, chọn checkpoint, mở lại, rồi xuất dự đoán

Dữ liệu nguồn là 64 điểm trên lưới, gán nhãn theo góc phần tư. Một encoder `2 → 6 → Tanh` học bài nguồn này ngay tại chỗ. Bài mới có ba lớp: so ba số `x`, `y` và `−x − y`, số nào lớn nhất thì đó là nhãn. Dữ liệu đích gồm 48 điểm train, 24 điểm validation, và 24 điểm chỉ dùng để xuất dự đoán. Nhãn của phần cuối không được dùng vào bất kỳ lựa chọn nào. Mọi thứ đều là dữ liệu tổng hợp và model nhỏ tự train.

```python
import copy
import io
import pandas as pd
import torch
from torch import nn
from sklearn.metrics import f1_score

torch.set_num_threads(1)
torch.manual_seed(48)
axis = torch.tensor([-1., -.7, -.4, -.1, .1, .4, .7, 1.])
source_X = torch.cartesian_prod(axis, axis)
source_y = (2 * (source_X[:, 0] > 0) + (source_X[:, 1] > 0)).long()
encoder = nn.Sequential(nn.Linear(2, 6), nn.Tanh())
source_model = nn.Sequential(encoder, nn.Linear(6, 4))
source_model.train()
source_optimizer = torch.optim.Adam(source_model.parameters(), lr=0.04)
for _ in range(100):
    source_optimizer.zero_grad(set_to_none=True)
    loss = nn.functional.cross_entropy(source_model(source_X), source_y)
    loss.backward()
    source_optimizer.step()
source_model.eval()

generator = torch.Generator().manual_seed(480)
target_X = torch.rand((96, 2), generator=generator) * 2 - 1
train_X, valid_X, predict_X = target_X[:48], target_X[48:72], target_X[72:]
def target_labels(values):
    return torch.stack([values[:, 0], values[:, 1], -values.sum(1)], dim=1).argmax(1)
train_y, valid_y = target_labels(train_X), target_labels(valid_X)
ids = [f"P{(i * 17) % 101:03d}" for i in range(96)]
assert len(set(ids)) == 96 and set(ids[:48]).isdisjoint(ids[48:72])
encoder.requires_grad_(False)
encoder.zero_grad(set_to_none=True)
encoder.eval()
encoder_before = copy.deepcopy(encoder.state_dict())
with torch.no_grad():
    train_Z, valid_Z = encoder(train_X), encoder(valid_X)
print("split train/valid/predict:", len(train_X), len(valid_X), len(predict_X))
print("embedding train:", tuple(train_Z.shape))
```

```output
split train/valid/predict: 48 24 24
embedding train: (48, 6)
```

Shape `(48, 6)` nghĩa là mỗi điểm trong 48 điểm train được encoder biến thành sáu tọa độ. ID được tạo theo một thứ tự xáo trộn, không trùng nhau, để bước xuất file về sau không thể tình cờ đúng nhờ thứ tự. Encoder được khóa lại, và ta lưu một bản trọng số để kiểm về sau. Các vector được tính trong `no_grad()`, nhưng lớp đầu ra mới vẫn học được bình thường trên chúng.

Tiếp theo, ta học lớp đầu ra ba lớp trong 120 epoch. Sau mỗi epoch, ta chấm validation bằng macro-F1. Nếu hai epoch có F1 bằng nhau, ta chọn epoch có validation loss thấp hơn.

```python
head = nn.Linear(6, 3)
optimizer = torch.optim.Adam(head.parameters(), lr=0.04)
best_key = (-1., -float("inf"))
best_state, best_epoch = None, None
for epoch in range(1, 121):
    head.train()
    optimizer.zero_grad(set_to_none=True)
    loss = nn.functional.cross_entropy(head(train_Z), train_y)
    loss.backward()
    optimizer.step()
    head.eval()
    with torch.no_grad():
        logits = head(valid_Z)
        valid_loss = nn.functional.cross_entropy(logits, valid_y).item()
        prediction = logits.argmax(1).numpy()
    macro_f1 = f1_score(valid_y.numpy(), prediction, labels=[0, 1, 2],
                        average="macro", zero_division=0)
    key = (float(macro_f1), -valid_loss)  # Xét F1 trước. Nếu hòa thì chọn loss thấp hơn.
    if key > best_key:
        best_key, best_epoch = key, epoch
        best_state = copy.deepcopy(head.state_dict())
head.load_state_dict(best_state)
assert all(torch.equal(encoder_before[k], value) for k, value in encoder.state_dict().items())
print("epoch duoc chon:", best_epoch)
print("valid macro-F1:", round(best_key[0], 4), "valid loss:", round(-best_key[1], 4))
print("head trainable:", sum(p.numel() for p in head.parameters()))
print("encoder giu nguyen:", True)
```

```output
epoch duoc chon: 120
valid macro-F1: 0.9185 valid loss: 0.2947
head trainable: 21
encoder giu nguyen: True
```

Mẹo ở đây là ghép hai tiêu chí thành một cặp `(F1, −loss)`. Python so cặp theo thứ tự: so F1 trước, nếu bằng nhau mới so phần sau. Đổi dấu loss để “lớn hơn là tốt hơn” cho cả hai thành phần.

Checkpoint được chọn là epoch 120, epoch cuối cùng, với macro-F1 0.9185. Chọn trúng epoch cuối là dấu hiệu có thể học thêm được nữa. Lớp đầu ra có $6\cdot3+3=21$ tham số, và encoder vẫn giữ nguyên. Validation đã được dùng để chọn epoch, nên 0.9185 không phải điểm test độc lập.

Giờ ta đóng gói model, mở lại thành đối tượng mới, chạy trên 24 điểm cần dự đoán, và ghi kết quả ra một file CSV trong bộ nhớ.

```python
stream = io.BytesIO()
package = {
    "encoder": encoder.state_dict(), "head": head.state_dict(),
    "input_dim": 2, "embedding_dim": 6,
    "labels": ["truc_x", "truc_y", "goc_am"],
    "mean": torch.zeros(2), "scale": torch.ones(2),
    "source": "local-quadrant-v1", "epoch": best_epoch,
}
torch.save(package, stream)
stream.seek(0)
saved = torch.load(stream, map_location="cpu", weights_only=True)
new_encoder = nn.Sequential(nn.Linear(saved["input_dim"], saved["embedding_dim"]), nn.Tanh())
new_head = nn.Linear(saved["embedding_dim"], len(saved["labels"]))
new_encoder.load_state_dict(saved["encoder"], strict=True)
new_head.load_state_dict(saved["head"], strict=True)
new_encoder.eval()
new_head.eval()
processed = (predict_X - saved["mean"]) / saved["scale"]
with torch.inference_mode():
    before = head(encoder(predict_X))
    after = new_head(new_encoder(processed))
assert torch.equal(before, after)
submission = pd.DataFrame({"id": ids[72:], "label": after.argmax(1).tolist()})
csv = io.StringIO()
submission.to_csv(csv, index=False)
csv.seek(0)
readback = pd.read_csv(csv, dtype={"id": str})
assert readback["id"].tolist() == ids[72:] and readback["id"].is_unique
assert readback["label"].between(0, 2).all() and len(readback) == len(predict_X)
print("mo lai trung logits:", torch.equal(before, after))
print("so dong du doan:", len(readback))
print(readback.head(5).to_string(index=False))
```

```output
mo lai trung logits: True
so dong du doan: 24
  id  label
P012      2
P029      1
P046      0
P063      0
P080      2
```

Gói lưu chứa đủ mọi thứ để dựng lại model mà không cần biến nào cũ trong notebook: trọng số của hai phần, kích thước các lớp, tên nhãn, mean và scale để chuẩn hóa, nguồn gốc, và epoch đã chọn. Model dựng lại cho đúng các logit như model cũ.

File CSV được đọc lại và kiểm ba điều: đủ 24 dòng, ID đúng thứ tự và không trùng, nhãn nằm trong khoảng 0 tới 2. Đọc ID dưới dạng chuỗi để `P012` không bị biến thành số. Ở đây việc lưu và mở diễn ra trong cùng một chương trình. Khi đem checkpoint sang máy khác, phải chạy lại từ file trong một chương trình mới, và kiểm cả môi trường cài đặt.

## Ví dụ 2: Đúng số hàng chưa đủ, đúng accuracy cũng chưa đủ

Sáu nhãn thật và sáu dự đoán được đặt sẵn để tính metric bằng tay. Phần sau là ba ID phải xuất theo thứ tự `R3, R1, R2`, trong khi bảng dự đoán lại đang được sắp theo ID. Nếu lấy cột nhãn theo vị trí, nhãn sẽ bị gán nhầm mẫu.

```python
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

truth = np.array([0, 0, 1, 1, 2, 2])
prediction = np.array([0, 0, 0, 1, 1, 2])
class_f1 = []
for label in [0, 1, 2]:
    tp = int(((truth == label) & (prediction == label)).sum())
    fp = int(((truth != label) & (prediction == label)).sum())
    fn = int(((truth == label) & (prediction != label)).sum())
    class_f1.append(2 * tp / (2 * tp + fp + fn))
macro = f1_score(truth, prediction, labels=[0, 1, 2], average="macro")
assert np.isclose(macro, np.mean(class_f1))
print("accuracy:", round(accuracy_score(truth, prediction), 4))
print("F1 tung lop:", np.round(class_f1, 4).tolist())
print("macro-F1:", round(macro, 4))

required_ids = ["R3", "R1", "R2"]
table = pd.DataFrame({"id": ["R1", "R2", "R3"], "label": [0, 2, 1]})
assert table["id"].is_unique and set(table["id"]) == set(required_ids)
wrong = table["label"].tolist()
correct = table.set_index("id").loc[required_ids, "label"].tolist()
assert wrong != correct
print("lay theo vi tri:", list(zip(required_ids, wrong)))
print("ghep bang ID:", list(zip(required_ids, correct)))
```

```output
accuracy: 0.6667
F1 tung lop: [0.8, 0.5, 0.6667]
macro-F1: 0.6556
lay theo vi tri: [('R3', 0), ('R1', 2), ('R2', 1)]
ghep bang ID: [('R3', 1), ('R1', 0), ('R2', 2)]
```

Đúng 4 trên 6 mẫu, nên accuracy là 0.6667. Macro-F1 lấy trung bình F1 của ba lớp, ra 0.6556. Lớp 1 chỉ có F1 0.5, và accuracy không cho thấy điều đó. Hai con số đo hai thứ khác nhau, nên phải dùng đúng metric mà đề yêu cầu.

Phần xuất file có hai bảng trông đều hợp lệ: đủ ba dòng, đúng tập ID, nhãn trong khoảng cho phép. Nhưng lấy theo vị trí thì `R3` nhận nhãn 0, trong khi dự đoán thật của `R3` là 1. Chỉ cách ghép bằng ID cho kết quả đúng. Bước kiểm cuối cùng phải xét từng cặp ID với dự đoán của nó, không chỉ đếm số hàng và kiểm khoảng giá trị.
