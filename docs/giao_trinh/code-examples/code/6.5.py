# -*- coding: utf-8 -*-
# Code mẫu — Encoder–decoder

# Ví dụ 1: Decoder nhận token đúng của bước trước
import torch

torch.set_num_threads(1)
names = ["PAD", "BOS", "EOS", "A", "B", "C"]
PAD, START = 0, 1
source = torch.tensor([[3, 4], [5, 0]])
target = torch.tensor([[4, 3, 2], [5, 2, 0]])
decoder_input = torch.full_like(target, PAD)
decoder_input[:, 0] = START
decoder_input[:, 1:] = target[:, :-1]
labels = target.masked_fill(target.eq(PAD), -100)
for x, y, z in zip(source.tolist(), decoder_input.tolist(), labels.tolist()):
    print("nguồn:", [names[i] for i in x])
    print("decoder:", [names[i] for i in y])
    print("label:", [names[i] if i != -100 else "bỏ" for i in z])
print("số token đích được chấm:", int(labels.ne(-100).sum()))
assert torch.equal(decoder_input[:, 1:], target[:, :-1])
assert decoder_input[:, 0].eq(START).all()
assert labels[:, -1].tolist() == [2, -100]


# Ví dụ 2: Hai query đích đọc ba key nguồn, trong đó có một PAD
import numpy as np

queries = np.array([[[1., 0.], [0., 1.]]])
keys = np.array([[[1., 0.], [0., 1.], [9., 9.]]])
values = np.array([[[2., 0.], [0., 2.], [99., 99.]]])
source_keep = np.array([[True, True, False]])

def cross_attention(queries, keys, values, source_keep):
    if not source_keep.any(axis=1).all():
        raise ValueError("Nguồn không có token thật")
    scores = queries @ keys.swapaxes(-1, -2) / np.sqrt(keys.shape[-1])
    scores = np.where(source_keep[:, None, :], scores, -np.inf)
    weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
    weights /= weights.sum(axis=-1, keepdims=True)
    return weights, weights @ values

weights, context = cross_attention(queries, keys, values, source_keep)
_, wrong_context = cross_attention(queries, keys, values, np.ones_like(source_keep))
print("shape Q/K/weights:", queries.shape, keys.shape, weights.shape)
print("weights:", weights.round(3).tolist())
print("context có mask:", context.round(3).tolist())
print("context quên mask:", wrong_context.round(3).tolist())
assert np.allclose(weights.sum(axis=-1), 1)
assert np.all(weights[:, :, 2] == 0)
_, without_pad = cross_attention(queries, keys[:, :2], values[:, :2], source_keep[:, :2])
assert np.allclose(context, without_pad)


# Ví dụ 3: Học đảo hai ký hiệu, và chấm chuỗi model tự sinh
import itertools
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(65)
PAD, BOS, EOS = 0, 1, 2
symbol_to_id = {"A": 3, "B": 4, "C": 5}
id_to_symbol = {value: key for key, value in symbol_to_id.items()}
pairs = list(itertools.product("ABC", repeat=2))
train_pairs, valid_pairs = pairs[:7], pairs[7:]

def make_batch(pairs):
    source = [[symbol_to_id[symbol] for symbol in pair] for pair in pairs]
    target = [row[::-1] for row in source]
    return (torch.tensor(source),
            torch.tensor([[BOS] + row for row in target]),
            torch.tensor([row + [EOS] for row in target]))

source, decoder_input, target = make_batch(train_pairs)
print("shape nguồn/input/label:", tuple(source.shape), tuple(decoder_input.shape), tuple(target.shape))
print("A B ->", source[1].tolist(), decoder_input[1].tolist(), target[1].tolist())
assert target[1].tolist() == [4, 3, EOS]

class SmallSeq2Seq(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(6, 12, padding_idx=PAD)
        self.encoder = nn.GRU(12, 24, batch_first=True)
        self.decoder = nn.GRU(12, 24, batch_first=True)
        self.output_layer = nn.Linear(24, 6)

    def forward(self, source, decoder_input):
        _, state = self.encoder(self.embedding(source))
        hidden, _ = self.decoder(self.embedding(decoder_input), state)
        return self.output_layer(hidden)

model = SmallSeq2Seq()
optimizer = torch.optim.Adam(model.parameters(), lr=0.02)
criterion = nn.CrossEntropyLoss(ignore_index=PAD)
history = []
for step in range(220):
    optimizer.zero_grad()
    logits = model(source, decoder_input)
    loss = criterion(logits.reshape(-1, 6), target.reshape(-1))
    loss.backward()
    optimizer.step()
    history.append(loss.item())

model.eval()
valid_source, valid_input, valid_target = make_batch(valid_pairs)
with torch.no_grad():
    train_logits = model(source, decoder_input)
    valid_logits = model(valid_source, valid_input)
    valid_loss = criterion(valid_logits.reshape(-1, 6), valid_target.reshape(-1))
print("logits train:", tuple(train_logits.shape))
print("loss train đầu/cuối:", round(history[0], 4), round(history[-1], 4))
print("loss validation teacher-forced:", round(valid_loss.item(), 4))
assert history[-1] < history[0]

def generate(pair, max_steps=4):
    source = torch.tensor([[symbol_to_id[symbol] for symbol in pair]])
    result, ended = [], False
    with torch.no_grad():
        _, state = model.encoder(model.embedding(source))
        current = torch.tensor([[BOS]])
        for _ in range(max_steps):
            hidden, state = model.decoder(model.embedding(current), state)
            logits = model.output_layer(hidden[:, -1]).clone()
            logits[:, [PAD, BOS]] = -torch.inf  # PAD và BOS không bao giờ là token đầu ra hợp lệ.
            token = int(logits.argmax(dim=-1).item())
            if token == EOS:
                ended = True
                break
            result.append(id_to_symbol[token])
            current = torch.tensor([[token]])
    return tuple(result), ended

for name, split in [("train", train_pairs), ("validation", valid_pairs)]:
    correct = 0
    for pair in split:
        prediction, ended = generate(pair)
        gold = tuple(reversed(pair))
        correct += ended and prediction == gold
        if name == "validation":
            print("nguồn", " ".join(pair), "gold", " ".join(gold),
                  "sinh", " ".join(prediction), "EOS", ended)
    print(name, "exact match:", f"{correct}/{len(split)}")

