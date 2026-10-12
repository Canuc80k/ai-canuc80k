# -*- coding: utf-8 -*-
# Code mẫu — BERT

# Ví dụ 1: Che chữ “đọc”, nhưng nhãn vẫn là “đọc”
import math
import torch
from torch import nn

torch.set_num_threads(1)
original = ["An", "đọc", "sách", "PAD"]
selected = torch.tensor([[False, True, False, False]])
corrupted = ["[MASK]" if chosen else token
             for token, chosen in zip(original, selected[0].tolist())]
labels = torch.tensor([[-100, 0, -100, -100]])
logits = torch.zeros(1, 4, 3)
logits[0, 1] = torch.tensor([2., 0., 0.])

def masked_loss(logits, labels):
    if not labels.ne(-100).any():
        raise ValueError("Không có vị trí MLM để tính loss")
    return nn.CrossEntropyLoss(ignore_index=-100)(
        logits.reshape(-1, 3), labels.reshape(-1))

loss = masked_loss(logits, labels)
probability = math.exp(2) / (math.exp(2) + 2)
print("input:", corrupted)
print("label:", labels.tolist())
print("số vị trí chấm:", int(labels.ne(-100).sum()))
print(f"p(đọc)={probability:.4f} loss={loss.item():.4f}")
assert math.isclose(loss.item(), -math.log(probability), abs_tol=1e-6)

changed = logits.clone()
changed[0, [0, 2, 3]] = torch.tensor([100., -100., 0.])
print("đổi logits vị trí bỏ qua, loss không đổi:", torch.allclose(loss, masked_loss(changed, labels)))
try:
    masked_loss(logits, torch.full_like(labels, -100))
except ValueError as error:
    print("bắt ca rỗng:", error)


# Ví dụ 2: Đổi token bên phải để kiểm attention hai chiều
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(63)
token_embedding = nn.Embedding(6, 8, padding_idx=0)
position_embedding = nn.Embedding(8, 8)
layer = nn.TransformerEncoderLayer(8, 2, dim_feedforward=16,
                                   dropout=0, batch_first=True)
encoder = nn.TransformerEncoder(layer, 1, enable_nested_tensor=False)
encoder.eval()

def encode(ids, causal=False):
    positions = torch.arange(ids.shape[1]).unsqueeze(0)
    inputs = token_embedding(ids) + position_embedding(positions)
    mask = None
    if causal:
        # True nghĩa là cấm query ở hàng i nhìn key ở cột j nằm phía sau.
        mask = torch.ones(ids.shape[1], ids.shape[1], dtype=torch.bool).triu(1)
    return encoder(inputs, mask=mask, src_key_padding_mask=ids.eq(0))

first = torch.tensor([[1, 2, 3]])
second = torch.tensor([[1, 2, 4]])
with torch.no_grad():
    bidirectional_a, bidirectional_b = encode(first), encode(second)
    causal_a, causal_b = encode(first, True), encode(second, True)
    padded = encode(torch.tensor([[1, 2, 3, 0, 0]]))
print("hidden shape:", tuple(bidirectional_a.shape))
print("hai chiều: token đầu đổi:", not torch.allclose(bidirectional_a[:, 0], bidirectional_b[:, 0]))
print("causal: tiền tố giữ nguyên:", torch.allclose(causal_a[:, :2], causal_b[:, :2], atol=1e-6))
print("thêm PAD: token thật giữ nguyên:", torch.allclose(bidirectional_a, padded[:, :3], atol=1e-6))
assert not torch.allclose(bidirectional_a[:, 0], bidirectional_b[:, 0])
assert torch.allclose(causal_a[:, :2], causal_b[:, :2], atol=1e-6)
assert torch.allclose(bidirectional_a, padded[:, :3], atol=1e-6)

sequence_head = nn.Linear(8, 2)
token_head = nn.Linear(8, 3)
print("head câu:", tuple(sequence_head(bidirectional_a[:, 0]).shape))
print("head token:", tuple(token_head(bidirectional_a).shape))


# Ví dụ 3: Gắn bốn nhãn từ lên bảy subword
import math
import torch
from torch import nn

torch.set_num_threads(1)
tokens = ["[CLS]", "An", "đến", "Hà", "##Nội", "sớm", "[SEP]"]
word_ids = [None, 0, 1, 2, 2, 3, None]
word_labels = ["B-PER", "O", "B-LOC", "O"]
label_to_id = {"O": 0, "B-PER": 1, "B-LOC": 2}

def align_first_subword(word_ids, labels):
    result, previous = [], None
    for word_id in word_ids:
        if word_id is None or word_id == previous:
            result.append(-100)
        else:
            result.append(label_to_id[labels[word_id]])
        previous = word_id
    return result

aligned = align_first_subword(word_ids, word_labels)
for token, label in zip(tokens, aligned):
    print(f"{token:7s} -> {label}")

# Ở mỗi vị trí được chấm, lớp đúng có logit 2, hai lớp còn lại có logit 0.
logits = torch.zeros(len(tokens), 3)
for position, label in enumerate(aligned):
    if label != -100:
        logits[position, label] = 2
loss = nn.CrossEntropyLoss(ignore_index=-100)(logits, torch.tensor(aligned))
print("vị trí chấm / tổng token:", sum(x != -100 for x in aligned), "/", len(tokens))
print("loss:", round(loss.item(), 4))
assert aligned == [-100, 1, 0, 2, -100, 0, -100]
assert math.isclose(loss.item(), math.log(math.exp(2) + 2) - 2, abs_tol=1e-6)

