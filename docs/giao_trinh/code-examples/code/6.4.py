# -*- coding: utf-8 -*-
# Code mẫu — Language model

# Ví dụ 1: Đếm bigram, và thấy tác dụng của smoothing
from collections import Counter, defaultdict
import numpy as np

train = ["em học toán", "em học tin", "em đọc sách", "bạn học toán", "bạn đọc sách"]
BOS, EOS, UNK = "<bos>", "<eos>", "<unk>"
vocabulary = sorted({word for sentence in train for word in sentence.split()} | {EOS, UNK})
counts = defaultdict(Counter)
for sentence in train:
    tokens = [BOS] + sentence.split() + [EOS]
    for previous, following in zip(tokens, tokens[1:]):
        counts[previous][following] += 1

def distribution(previous, alpha=1.):
    if alpha <= 0:
        raise ValueError("Demo yêu cầu alpha dương")
    row = counts.get(previous, Counter())
    return np.array([(row[word] + alpha) / (sum(row.values()) + alpha * len(vocabulary))
                     for word in vocabulary])

print("số token đích:", len(vocabulary))
print("sau em:", dict(counts["em"]))
print("không smoothing, p(học|em):", round(2 / 3, 3))
for alpha in [0.1, 1.]:
    probability = distribution("em", alpha)
    print(f"alpha={alpha}: p(học|em)={probability[vocabulary.index('học')]:.3f} tổng={probability.sum():.3f}")
    assert np.isclose(probability.sum(), 1)
assert np.isclose(distribution("em")[vocabulary.index("học")], 3 / 12)
assert np.all(distribution(UNK) > 0)

def sentence_nll(sentence):
    words = [word if word in vocabulary else UNK for word in sentence.split()]
    sequence = [BOS] + words + [EOS]
    probabilities = [distribution(left)[vocabulary.index(right)]
                     for left, right in zip(sequence, sequence[1:])]
    return -np.log(probabilities).mean(), len(probabilities)

for sentence in ["em học toán", "em sách học", "robot học toán"]:
    nll, token_count = sentence_nll(sentence)
    print(f"{sentence}: N={token_count} NLL={nll:.3f} PPL={np.exp(nll):.3f}")
assert sentence_nll("em học toán")[0] < sentence_nll("em sách học")[0]


# Ví dụ 2: Dịch nhãn lệch một vị trí, và bỏ PAD khỏi mẫu số
import math
import torch
from torch import nn

torch.set_num_threads(1)
names = ["PAD", "BOS", "EOS", "em", "học"]
PAD = 0
sequences = torch.tensor([[1, 3, 4, 2, 0], [1, 3, 2, 0, 0]])
inputs = sequences[:, :-1]
labels = sequences[:, 1:].clone()
labels[labels == PAD] = -100
for x, y in zip(inputs.tolist(), labels.tolist()):
    print("input:", [names[i] for i in x])
    print("label:", [names[i] if i != -100 else "bỏ" for i in y])
allowed = torch.ones(4, 4, dtype=torch.bool).tril()
print("causal: 1 là được đọc:", allowed.int().tolist())

# Logit lấy từ một phân phối đặt sẵn: ở mọi vị trí thật, lớp đúng có xác suất 1/4.
probabilities = torch.full((2, 4, 5), 0.75 / 4, dtype=torch.float64)
for row, position in labels.ne(-100).nonzero().tolist():
    probabilities[row, position, labels[row, position]] = 0.25
logits = probabilities.log()
loss = nn.CrossEntropyLoss(ignore_index=-100)(logits.reshape(-1, 5), labels.reshape(-1))
print("token được chấm:", int(labels.ne(-100).sum()))
print(f"NLL={loss.item():.3f} PPL={math.exp(loss.item()):.3f}")
assert int(labels.ne(-100).sum()) == 5
assert math.isclose(loss.item(), math.log(4), abs_tol=1e-10)
assert not allowed[0, 1] and allowed[2, 2]


# Ví dụ 3: Temperature đổi xác suất, top-k và top-p đổi tập được chọn
import numpy as np

def softmax_temperature(logits, temperature):
    if temperature <= 0:
        raise ValueError("Temperature phải dương khi chia logits")
    scaled = np.asarray(logits, dtype=float) / temperature
    weights = np.exp(scaled - scaled.max())
    return weights / weights.sum()

def retain(probability, indices):
    filtered = np.zeros_like(probability)
    filtered[indices] = probability[indices]
    return filtered / filtered.sum()

logits = np.array([2., 1., 0.])
for temperature in [0.5, 1., 2.]:
    p = softmax_temperature(logits, temperature)
    print(f"T={temperature}: {p.round(3).tolist()} greedy={int(p.argmax())}")
base = softmax_temperature(logits, 1.)
order = np.argsort(-base, kind="stable")
top_k = retain(base, order[:2])
count = int(np.searchsorted(np.cumsum(base[order]), 0.8, side="left")) + 1
top_p = retain(base, order[:count])  # Giữ luôn token làm tổng vừa chạm hoặc vượt ngưỡng.
print("top-k 2:", top_k.round(3).tolist())
print("top-p 0.8:", top_p.round(3).tolist(), "số giữ:", count)
assert np.isclose(top_p.sum(), 1)
assert count == 2 and np.array_equal(top_k, top_p)
assert softmax_temperature(logits, 0.5).argmax() == softmax_temperature(logits, 2).argmax()


# Ví dụ 4: Beam search giữ lại đường đi mà greedy bỏ sớm
import math

transitions = {
    "BOS": [("A", 0.6), ("B", 0.4)],
    "A": [("EOS", 0.5), ("C", 0.5)],
    "B": [("EOS", 0.95), ("C", 0.05)],
    "C": [("EOS", 1.0)],
}
assert all(math.isclose(sum(p for _, p in row), 1) for row in transitions.values())

def beam_search(width, max_steps=3):
    beams = [((), 0.)]  # Cộng log thay vì nhân xác suất, để tránh tràn số dưới.
    for _ in range(max_steps):
        candidates = []
        for tokens, score in beams:
            if tokens and tokens[-1] == "EOS":
                candidates.append((tokens, score))
                continue
            previous = tokens[-1] if tokens else "BOS"
            for token, probability in transitions[previous]:
                candidates.append((tokens + (token,), score + math.log(probability)))
        beams = sorted(candidates, key=lambda item: -item[1])[:width]
        if all(tokens[-1] == "EOS" for tokens, _ in beams):
            break
    return beams[0]

def all_finished(tokens=(), probability=1.):
    if tokens and tokens[-1] == "EOS":
        return [(tokens, probability)]
    if len(tokens) == 3:
        return []
    previous = tokens[-1] if tokens else "BOS"
    return [answer for token, p in transitions[previous]
            for answer in all_finished(tokens + (token,), probability * p)]

for width in [1, 2]:
    tokens, log_probability = beam_search(width)
    print(f"beam={width}: {' '.join(tokens)} p={math.exp(log_probability):.3f}")
oracle = max(all_finished(), key=lambda item: item[1])
print("duyệt hết:", " ".join(oracle[0]), "p=", round(oracle[1], 3))
assert beam_search(1)[0] == ("A", "EOS")
assert beam_search(2)[0] == oracle[0] == ("B", "EOS")

