# -*- coding: utf-8 -*-
# Speech recognition — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

def ctc_collapse(path, blank=0):
    result = []
    for step, token in enumerate(path):
        different_from_previous = step == 0 or token != path[step - 1]
        if token != blank and different_from_previous:
            result.append(token)
    return tuple(result)

vocabulary = {0: "_", 1: "a"}
for path in [(1, 1, 0, 1), (1, 1, 1)]:
    transcript = "".join(vocabulary[token] for token in ctc_collapse(path))
    print(" ".join(vocabulary[token] for token in path), "->", transcript)

# Bước 2
from itertools import product

frame_probabilities = np.array([[0.6, 0.4], [0.5, 0.5], [0.4, 0.6]])
transcript_probabilities = {}
for path in product(range(2), repeat=3):
    probability = np.prod(frame_probabilities[np.arange(3), path])
    transcript = ctc_collapse(path)
    transcript_probabilities[transcript] = transcript_probabilities.get(transcript, 0) + probability
print(f"P(rong) = {transcript_probabilities[()]:.3f}")
print(f"P(a) = {transcript_probabilities[(1,)]:.3f}")
print(f"P(aa) = {transcript_probabilities[(1, 1)]:.3f}")
print(f"loss = {-np.log(transcript_probabilities[(1,)]):.4f}")

# Bước 3
def ctc_forward(frame_probabilities, target, blank=0):
    extended = [blank]
    for token in target:
        extended += [token, blank]
    alpha = np.zeros(len(extended))
    alpha[0] = frame_probabilities[0, blank]
    alpha[1] = frame_probabilities[0, extended[1]]
    history = [alpha]
    for t in range(1, len(frame_probabilities)):
        previous, alpha = alpha, np.zeros(len(extended))
        for s, label in enumerate(extended):
            total = previous[s]
            if s >= 1:
                total += previous[s - 1]
            if s >= 2 and label != blank and label != extended[s - 2]:
                total += previous[s - 2]
            alpha[s] = total * frame_probabilities[t, label]
        history.append(alpha)
    return alpha[-1] + alpha[-2], history

probability_a, history = ctc_forward(frame_probabilities, [1])
for t, row in enumerate(history, start=1):
    print(f"t={t}:", "  ".join(f"{value:.2f}" for value in row))
print(f"P(a) = {probability_a:.2f}")

# Bước 4
import torch

log_probabilities = torch.tensor(frame_probabilities, dtype=torch.float64).log()[:, None, :]
criterion = torch.nn.CTCLoss(blank=0, reduction="sum")
target = torch.tensor([1], dtype=torch.long)
loss = criterion(
    log_probabilities,
    target,
    torch.tensor([3]),
    torch.tensor([1]),
)
print(tuple(log_probabilities.shape))
print(f"CTCLoss = {loss.item():.4f}")
too_short_loss = criterion(
    log_probabilities[:2],
    torch.tensor([1, 1]),
    torch.tensor([2]),
    torch.tensor([2]),
)
print(f"target aa, 2 frame: inf = {bool(torch.isinf(too_short_loss))}")

# Bước 5
rng = np.random.default_rng(0)
random_logits = rng.normal(size=(12, 4))
random_probabilities = np.exp(random_logits) / np.exp(random_logits).sum(axis=1, keepdims=True)
random_target = [1, 2, 2, 3]
dp_loss = -np.log(ctc_forward(random_probabilities, random_target)[0])
torch_loss = criterion(
    torch.tensor(random_probabilities).log()[:, None, :],
    torch.tensor(random_target),
    torch.tensor([12]),
    torch.tensor([4]),
)
print(f"DP = {dp_loss:.6f}, CTCLoss = {torch_loss.item():.6f}")

# Bước 6
import unicodedata

def word_tokens(text):
    return unicodedata.normalize("NFC", text).lower().split()

def edit_distance(reference_tokens, predicted_tokens):
    previous = list(range(len(predicted_tokens) + 1))
    for row, reference_token in enumerate(reference_tokens, start=1):
        current = [row]
        for column, predicted_token in enumerate(predicted_tokens, start=1):
            deletion = previous[column] + 1
            insertion = current[column - 1] + 1
            substitution = previous[column - 1] + (reference_token != predicted_token)
            current.append(min(deletion, insertion, substitution))
        previous = current
    return previous[-1]

reference = word_tokens("em học AI hôm nay")
prediction = word_tokens("em học toán nay")
errors = edit_distance(reference, prediction)
print(f"loi = {errors}, token tham chieu = {len(reference)}")
print(f"WER = {errors / len(reference):.3f}")

# Bước 7
references = ["em học AI", "mai lớp em học lập trình thi đấu"]
predictions = ["em học", "mai lớp em học lập trình thi đấu"]
error_counts = [edit_distance(word_tokens(r), word_tokens(p)) for r, p in zip(references, predictions)]
lengths = [len(word_tokens(r)) for r in references]
corpus_wer = sum(error_counts) / sum(lengths)
mean_sentence_wer = np.mean([e / n for e, n in zip(error_counts, lengths)])
print(error_counts, lengths)
print(f"corpus WER = {corpus_wer:.3f}")
print(f"mean sentence WER = {mean_sentence_wer:.3f}")

# Bước 8
reference_text = "mai thi ai"
original_text = "mai thi ai"
edited_text = "mai thi toán"
reference_tokens = word_tokens(reference_text)
for name, text in [("goc", original_text), ("sua", edited_text)]:
    error_count = edit_distance(reference_tokens, word_tokens(text))
    print(f"{name}: WER = {error_count / len(reference_tokens):.3f}")
