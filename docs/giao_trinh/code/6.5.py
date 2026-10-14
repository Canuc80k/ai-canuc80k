# -*- coding: utf-8 -*-
# Encoder–decoder — chạy các bước như notebook từ trên xuống.

# Bước 1
import itertools
import torch
from torch import nn

torch.manual_seed(65)
torch.set_num_threads(1)
PAD, BOS, EOS = 0, 1, 2
symbol_to_id = {"A": 3, "B": 4, "C": 5}
id_to_symbol = {value: key for key, value in symbol_to_id.items()}
pairs = list(itertools.product("ABC", repeat=2))
train_pairs = pairs[:7]
valid_pairs = pairs[7:]

def make_seq2seq_batch(pairs):
    sources = []
    decoder_inputs = []
    labels = []
    for pair in pairs:
        source = [symbol_to_id[symbol] for symbol in pair]
        target = list(reversed(source))
        sources.append(source)
        decoder_inputs.append([BOS] + target)
        labels.append(target + [EOS])
    return (torch.tensor(sources), torch.tensor(decoder_inputs), torch.tensor(labels))

source_ids, decoder_ids, target_ids = make_seq2seq_batch(train_pairs)
print("nguồn/input đích/label:", tuple(source_ids.shape), tuple(decoder_ids.shape), tuple(target_ids.shape))
print("cặp A B:", source_ids[1].tolist(), decoder_ids[1].tolist(), target_ids[1].tolist())

# Bước 2
class SmallSeq2Seq(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(6, 12, padding_idx=PAD)
        self.encoder = nn.GRU(12, 24, batch_first=True)
        self.decoder = nn.GRU(12, 24, batch_first=True)
        self.output_layer = nn.Linear(24, 6)

    def forward(self, source, decoder_input):
        _, source_state = self.encoder(self.embedding(source))
        decoded, _ = self.decoder(self.embedding(decoder_input), source_state)
        return self.output_layer(decoded)

model = SmallSeq2Seq()
logits = model(source_ids, decoder_ids)
print("logits:", tuple(logits.shape))

# Bước 3
optimizer = torch.optim.Adam(model.parameters(), lr=0.02)
loss_function = nn.CrossEntropyLoss(ignore_index=PAD)
loss_history = []
model.train()
for step in range(220):
    optimizer.zero_grad()
    logits = model(source_ids, decoder_ids)
    loss = loss_function(logits.reshape(-1, 6), target_ids.reshape(-1))
    loss.backward()
    optimizer.step()
    loss_history.append(loss.item())

valid_source, valid_input, valid_target = make_seq2seq_batch(valid_pairs)
model.eval()
with torch.no_grad():
    valid_logits = model(valid_source, valid_input)
    valid_loss = loss_function(valid_logits.reshape(-1, 6), valid_target.reshape(-1))
print("train loss đầu/cuối:", round(loss_history[0], 4), round(loss_history[-1], 4))
print("validation teacher-forced loss:", round(valid_loss.item(), 4))

# Bước 4
def generate_reverse(pair, max_steps=4):
    source = torch.tensor([[symbol_to_id[symbol] for symbol in pair]])
    generated = []
    with torch.no_grad():
        _, state = model.encoder(model.embedding(source))
        current = torch.tensor([[BOS]])
        for _ in range(max_steps):
            decoded, state = model.decoder(model.embedding(current), state)
            next_logits = model.output_layer(decoded[:, -1]).clone()
            next_logits[:, [PAD, BOS]] = -torch.inf
            token = int(next_logits.argmax(dim=-1).item())
            if token == EOS:
                break
            generated.append(id_to_symbol[token])
            current = torch.tensor([[token]])
    return tuple(generated)

for split_name, split_pairs in [("train", train_pairs), ("validation", valid_pairs)]:
    correct = 0
    for pair in split_pairs:
        prediction = generate_reverse(pair)
        gold = tuple(reversed(pair))
        correct += prediction == gold
        if split_name == "validation":
            print("nguồn:", pair, "đích thật:", gold, "tự sinh:", prediction)
    print(split_name, "exact match:", f"{correct}/{len(split_pairs)}")

# Bước 5
with torch.no_grad():
    token_nll = nn.functional.cross_entropy(
        valid_logits.reshape(-1, 6), valid_target.reshape(-1), reduction="none"
    ).reshape(2, 3)
    step2_probs = valid_logits[1, 1].softmax(dim=-1)  # cặp C C, vị trí 2, input BOS C
print("NLL từng vị trí:", [[round(x, 3) for x in row] for row in token_nll.tolist()])
print("C C, bước 2 sau BOS C:", {s: round(step2_probs[i].item(), 3) for s, i in symbol_to_id.items()})

# Bước 6
def beam_search(pair, beam_size=3, max_steps=4):
    source = torch.tensor([[symbol_to_id[symbol] for symbol in pair]])
    finished = []
    with torch.no_grad():
        _, state = model.encoder(model.embedding(source))
        beams = [((), 0.0, state, BOS)]  # (đã sinh, tổng log-prob, trạng thái, token cuối)
        for _ in range(max_steps):
            candidates = []
            for tokens, score, state, last in beams:
                decoded, new_state = model.decoder(model.embedding(torch.tensor([[last]])), state)
                log_probs = torch.log_softmax(model.output_layer(decoded[:, -1]), dim=-1)[0]
                for token in [EOS, *symbol_to_id.values()]:
                    candidates.append((tokens, score + log_probs[token].item(), new_state, token))
            candidates.sort(key=lambda item: item[1], reverse=True)
            beams = []
            for tokens, score, state, token in candidates[:beam_size]:
                if token == EOS:
                    finished.append((" ".join(tokens), round(score, 3)))
                else:
                    beams.append((tokens + (id_to_symbol[token],), score, state, token))
            if not beams:
                break
    return sorted(finished, key=lambda item: item[1], reverse=True)

for pair in valid_pairs:
    print(" ".join(pair), "->", beam_search(pair)[:3])

# Bước 7
import numpy as np

query = np.array([[1.0, 0.0]])
keys = np.array([[1.0, 0.0], [0.0, 1.0]])
values = np.array([[2.0, 0.0], [0.0, 2.0]])
scores = query @ keys.T / np.sqrt(keys.shape[1])
weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
weights /= weights.sum(axis=-1, keepdims=True)
context = weights @ values
print("attention:", weights.round(3))
print("context:", context.round(3))

# Bước 8
from collections import Counter
import math

def ngram_counts(tokens, n):
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))

def bleu2(candidate, reference):
    precisions = []
    for n in (1, 2):
        counts, ref_counts = ngram_counts(candidate, n), ngram_counts(reference, n)
        clipped = sum(min(count, ref_counts[gram]) for gram, count in counts.items())
        precisions.append(clipped / sum(counts.values()))
    brevity = min(1.0, math.exp(1 - len(reference) / len(candidate)))
    return precisions, brevity, brevity * math.sqrt(precisions[0] * precisions[1])

reference = "câu lạc bộ họp vào thứ sáu".split()
for candidate in ["họp họp họp họp", "câu lạc bộ họp thứ sáu", "câu lạc bộ họp vào thứ bảy"]:
    (p1, p2), bp, score = bleu2(candidate.split(), reference)
    print(f"{candidate:27} p1={p1:.3f} p2={p2:.3f} BP={bp:.3f} BLEU-2={score:.3f}")
