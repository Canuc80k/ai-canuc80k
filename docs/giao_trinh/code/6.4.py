# -*- coding: utf-8 -*-
# Language model — chạy các bước như notebook từ trên xuống.

# Bước 1
from collections import Counter, defaultdict
import numpy as np

train_sentences = ["em học toán", "em học tin", "em đọc sách", "bạn học toán", "bạn đọc sách"]
BOS, EOS, UNK = "<bos>", "<eos>", "<unk>"
target_vocab = sorted({token for text in train_sentences for token in text.split()} | {EOS, UNK})
bigram_counts = defaultdict(Counter)
for text in train_sentences:
    tokens = [BOS] + text.split() + [EOS]
    for previous, following in zip(tokens, tokens[1:]):
        bigram_counts[previous][following] += 1

print("vocabulary size:", len(target_vocab))
print("sau 'em':", dict(bigram_counts["em"]))

# Bước 2
alpha = 1.0

def next_distribution(previous):
    counts = bigram_counts.get(previous, Counter())
    denominator = sum(counts.values()) + alpha * len(target_vocab)
    return np.array([(counts[token] + alpha) / denominator for token in target_vocab])

em_distribution = next_distribution("em")
print("p(học|em):", round(em_distribution[target_vocab.index("học")], 3))
print("tổng xác suất:", round(em_distribution.sum(), 6))

# Bước 3
def sentence_nll(text):
    words = [word if word in target_vocab else UNK for word in text.split()]
    tokens = [BOS] + words + [EOS]
    log_probabilities = []
    for previous, following in zip(tokens, tokens[1:]):
        probability = next_distribution(previous)[target_vocab.index(following)]
        log_probabilities.append(np.log(probability))
    return -np.mean(log_probabilities), len(log_probabilities)

for text in ["em học toán", "em sách học", "robot học toán"]:
    nll, count = sentence_nll(text)
    print(text, "N=", count, "NLL=", round(nll, 3), "PPL=", round(np.exp(nll), 3))
print("PPL xác suất 1/4:", round(np.exp(-np.log(0.25)), 3))

# Bước 4
import torch
import torch.nn.functional as F

def bigram_logits(tokens):
    # Hàng i chỉ đọc tokens[i]: một causal language model có ngữ cảnh dài 1.
    rows = [np.log(next_distribution(token)) for token in tokens]
    return torch.tensor(np.array(rows), dtype=torch.float32)

sequence = [BOS, "em", "học", "toán", EOS]
inputs, labels = sequence[:-1], sequence[1:]
logits = bigram_logits(inputs)
label_ids = torch.tensor([target_vocab.index(token) for token in labels])
print("input:", inputs)
print("label:", labels)
print("logits shape:", tuple(logits.shape))
print("cross-entropy:", round(F.cross_entropy(logits, label_ids).item(), 3))

# Thêm hai vị trí đệm; label -100 bị cross_entropy bỏ qua theo mặc định.
padded_logits = bigram_logits(inputs + [EOS, EOS])
padded_labels = torch.cat([label_ids, torch.tensor([-100, -100])])
print("thêm 2 vị trí đệm:", round(F.cross_entropy(padded_logits, padded_labels).item(), 3))

# Bước 5
def softmax_temperature(logits, temperature):
    if temperature <= 0:
        raise ValueError("Temperature phải dương trong công thức sampling")
    scaled = logits / temperature
    weights = np.exp(scaled - scaled.max())
    return weights / weights.sum()

example_logits = np.array([2.0, 1.0, 0.0])
for temperature in [0.5, 1.0, 2.0]:
    probability = softmax_temperature(example_logits, temperature)
    print("T=", temperature, "p=", probability.round(3))

# Bước 6
def top_p_distribution(probability, threshold):
    if not 0 < threshold <= 1:
        raise ValueError("top-p nằm trong (0, 1]")
    order = np.argsort(-probability, kind="stable")
    sorted_probability = probability[order]
    # Giữ token khi tổng trước nó còn dưới ngưỡng, gồm cả token vượt ngưỡng.
    keep = np.cumsum(sorted_probability) - sorted_probability < threshold
    result = np.zeros_like(probability)
    result[order[keep]] = sorted_probability[keep]
    return result / result.sum()

base_probability = softmax_temperature(example_logits, 1.0)
filtered = top_p_distribution(base_probability, 0.8)
print("base:", base_probability.round(3))
print("top-p=0.8:", filtered.round(3))
print("số token giữ:", np.count_nonzero(filtered))

# Bước 7
def generate_bigram(sample=False, seed=0, max_tokens=6):
    rng = np.random.default_rng(seed)
    previous = BOS
    generated = []
    for _ in range(max_tokens):
        probability = next_distribution(previous)
        if sample:
            index = rng.choice(len(target_vocab), p=probability)
        else:
            index = int(probability.argmax())
        token = target_vocab[index]
        if token == EOS:
            break
        generated.append(token)
        previous = token
    return " ".join(generated)

print("greedy:", generate_bigram())
print("sampling seed 0:", generate_bigram(sample=True))
