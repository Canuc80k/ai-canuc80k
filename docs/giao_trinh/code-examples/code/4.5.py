# -*- coding: utf-8 -*-
# Code mẫu — Zero-shot

# Ví dụ 1: Hai mô tả cho mỗi lớp, năm truy vấn
import numpy as np

def unit_rows(values):
    norms = np.linalg.norm(values, axis=-1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("khong normalize vector 0")
    return values / norms

templates = np.array([[[2., 0.], [3., 1.]],
                      [[0., 2.], [1., 3.]]])  # Shape (lớp, mô tả, tọa độ).
prototypes = unit_rows(unit_rows(templates).mean(axis=1))
queries = unit_rows(np.array([[3., 1.], [1., 3.], [2., 0.],
                              [0., 2.], [1., 1.]]))
names = np.array(["san", "phong"])

def classify_batches(values, batch_size):
    return np.concatenate([values[i:i + batch_size] @ prototypes.T
                           for i in range(0, len(values), batch_size)])

scores = classify_batches(queries, 2)
reference = np.array([[sum(q[d] * p[d] for d in range(2))
                       for p in prototypes] for q in queries])
assert np.allclose(scores, reference)
assert np.allclose(scores, classify_batches(queries, 5))
assert np.allclose(np.linalg.norm(prototypes, axis=1), 1)
print("prototype:", prototypes.round(3).tolist())
print("shape diem:", scores.shape)
print("cosine:", scores.round(3).tolist())
print("nhan:", names[scores.argmax(axis=1)].tolist())


# Ví dụ 2: Temperature đổi độ chắc chắn, tập lớp đổi ý nghĩa
import numpy as np

def softmax(rows):
    values = np.exp(rows - rows.max(axis=1, keepdims=True))
    return values / values.sum(axis=1, keepdims=True)

prototypes = np.eye(2)
query = np.array([[0.8, 0.6]])
cosine = query @ prototypes.T
for temperature in [1.0, 0.2]:
    probability = softmax(cosine / temperature)
    assert probability.argmax(1)[0] == 0
    print("temperature:", temperature, "softmax:", probability.round(4).tolist())

outside = np.array([[-1., -0.1]])
outside /= np.linalg.norm(outside)
old_scores = outside @ prototypes.T
old_probability = softmax(old_scores / 0.2)
extended_prototypes = np.vstack([prototypes, outside])
new_probability = softmax(outside @ extended_prototypes.T / 0.2)
print("ngoai hai lop, cosine:", old_scores.round(4).tolist())
print("truoc them lop:", old_probability.round(4).tolist(),
      "lop thang:", int(old_probability.argmax(1)[0]))
print("sau them lop:", new_probability.round(4).tolist(),
      "lop thang:", int(new_probability.argmax(1)[0]))
assert old_scores.max() < 0 and old_probability.max() > 0.98
assert new_probability.argmax(1)[0] == 2


# Ví dụ 3: Tổng log và trung bình log chọn hai chuỗi khác nhau
import numpy as np

paths = {"A": np.array([0.6, 0.6]), "B": np.array([0.4, 0.8, 0.8])}
total, average = {}, {}
for name, probabilities in paths.items():
    total[name] = np.log(probabilities).sum()
    average[name] = total[name] / len(probabilities)
    perplexity = np.exp(-average[name])
    independent = (1 / probabilities.prod())**(1 / len(probabilities))
    assert np.isclose(perplexity, independent)
    print(name, "P(chuoi):", round(float(probabilities.prod()), 3),
          "sum log:", round(float(total[name]), 4),
          "mean log:", round(float(average[name]), 4),
          "PPL:", round(float(perplexity), 4))
print("tong log chon:", max(total, key=total.get))
print("mean log chon:", max(average, key=average.get))


# Ví dụ 4: Học một bigram nhỏ, rồi chấm đúng token kế tiếp
from collections import Counter
import numpy as np

vocabulary = ["BOS", "troi", "nang", "mua", "am", "lanh", "EOS"]
source = (["BOS", "troi", "nang", "am", "EOS"],) * 3
source += (["BOS", "troi", "mua", "lanh", "EOS"],) * 2
source += (["BOS", "troi", "nang", "lanh", "EOS"],)
pair_counts = Counter()
context_counts = Counter()
for sentence in source:
    for previous, target in zip(sentence[:-1], sentence[1:]):
        pair_counts[previous, target] += 1
        context_counts[previous] += 1

def next_probability(previous, target):
    return (pair_counts[previous, target] + 1) / (context_counts[previous] + len(vocabulary))

prompt = ["BOS", "troi"]
candidates = {"A": ["nang", "am", "EOS"], "B": ["mua", "lanh", "EOS"]}
scores = {}
for name, completion in candidates.items():
    previous_tokens = [prompt[-1]] + completion[:-1]
    pairs = list(zip(previous_tokens, completion))
    probabilities = np.array([next_probability(previous, target) for previous, target in pairs])
    scores[name] = float(np.log(probabilities).sum())
    print(name, "context -> target:", pairs)
    print("P token:", probabilities.round(4).tolist(), "sum log:", round(scores[name], 4))
assert np.isclose(next_probability("troi", "nang"), 5 / 13)
assert np.isclose(sum(next_probability("troi", word) for word in vocabulary), 1)
print("chon:", max(scores, key=scores.get))

