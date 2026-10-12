# -*- coding: utf-8 -*-
# Code mẫu — Tokenization và text classification

# Ví dụ 1: Cùng một chữ có dấu, hai cách lưu
import unicodedata

def normalize_text(text):
    nfc = unicodedata.normalize("NFC", text)
    return " ".join(nfc.lower().split())

composed = "Học sinh học máy"
decomposed = unicodedata.normalize("NFD", composed)
print("bằng nhau trước NFC:", composed == decomposed)
print("số mã Unicode:", len(composed), len(decomposed))
print("bằng nhau sau NFC:", normalize_text(composed) == normalize_text(decomposed))
print("split:", normalize_text(composed).split())
print("giữ khác biệt ma/má:", normalize_text("ma") != normalize_text("má"))
assert normalize_text(composed) == normalize_text(decomposed)
assert normalize_text("ma") != normalize_text("má")


# Ví dụ 2: Học hai luật BPE từ số lần xuất hiện
from collections import Counter

word_counts = {"low": 3, "lower": 2, "new": 1}
pieces = {word: list(word) for word in word_counts}

def count_pairs(pieces, frequencies):
    counts = Counter()
    for word, tokens in pieces.items():
        for pair in zip(tokens, tokens[1:]):
            counts[pair] += frequencies[word]
    return counts

def merge_pair(tokens, pair):
    result, i = [], 0
    while i < len(tokens):
        if i + 1 < len(tokens) and tuple(tokens[i:i + 2]) == pair:
            result.append(tokens[i] + tokens[i + 1])
            i += 2  # Hai token vừa gộp không được dùng lại trong cùng một lượt.
        else:
            result.append(tokens[i])
            i += 1
    return result

weighted = count_pairs(pieces, word_counts)
unweighted = count_pairs(pieces, dict.fromkeys(word_counts, 1))
print("cặp l,o: có trọng số / đếm mỗi từ một lần:", weighted[("l", "o")], unweighted[("l", "o")])
rules = []
for step in range(2):
    counts = count_pairs(pieces, word_counts)
    pair = min(counts, key=lambda p: (-counts[p], p))
    rules.append(pair)
    print("bước", step + 1, "gộp", pair, "tần suất", counts[pair])
    pieces = {word: merge_pair(tokens, pair) for word, tokens in pieces.items()}
print("sau hai bước:", pieces)
assert weighted[("l", "o")] == 3 + 2
assert merge_pair(list("aaa"), ("a", "a")) == ["aa", "a"]

def encode_with_rules(word, rules):
    tokens = list(word)
    for pair in rules:
        tokens = merge_pair(tokens, pair)
    return tokens

encoded = encode_with_rules("lowest", rules)
print("lowest:", encoded)
print("khôi phục đúng chữ:", "".join(encoded) == "lowest")
assert "".join(encoded) == "lowest"


# Ví dụ 3: Tính một hàng TF-IDF bằng tay
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

train = ["hay dễ", "hay rõ", "khó"]
vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(train)
columns = [vectorizer.vocabulary_[term] for term in ["hay", "dễ"]]
idf_hand = np.array([np.log(4 / 3) + 1, np.log(4 / 2) + 1])
unit_hand = idf_hand / np.linalg.norm(idf_hand)
print("cột hay/dễ, IDF:", vectorizer.idf_[columns].round(3).tolist())
print("hàng hay dễ:", matrix[0, columns].toarray().ravel().round(3).tolist())
unknown = vectorizer.transform(["robot"])
print("robot: số feature khác 0:", unknown.nnz)
assert np.allclose(vectorizer.idf_[columns], idf_hand)
assert np.allclose(matrix[0, columns].toarray().ravel(), unit_hand)
assert unknown.nnz == 0


# Ví dụ 4: Phân loại nhận xét, và truy nguyên hai câu phủ định
import unicodedata
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

def normalize_text(text):
    return " ".join(unicodedata.normalize("NFC", text).lower().split())

train_texts = [
    "bài học hay dễ hiểu", "nội dung rõ ràng bổ ích",
    "bài giảng tốt dễ theo dõi", "ví dụ hay hữu ích",
    "khóa học thú vị", "lời giải rõ ràng",
    "bài học khó hiểu nhàm chán", "nội dung kém rối",
    "bài giảng tệ khó theo dõi", "ví dụ sai vô ích",
    "khóa học nhàm chán", "lời giải rối sai",
]
labels = np.array([1] * 6 + [0] * 6)
valid_texts = ["bài học hay", "lời giải sai", "bài giảng không hay",
               "ví dụ rõ ràng", "nội dung rối", "khóa học không tệ"]
gold = np.array([1, 0, 0, 1, 0, 1])
model = Pipeline([
    ("tfidf", TfidfVectorizer(preprocessor=normalize_text, ngram_range=(1, 2))),
    ("classifier", LogisticRegression(C=4, random_state=0, max_iter=1000)),
])
model.fit(train_texts, labels)  # Từ điển, IDF và bộ phân loại đều chỉ học từ train.
fitted_idf = model["tfidf"].idf_.copy()
prediction = model.predict(valid_texts)
positive_column = list(model["classifier"].classes_).index(1)
probability = model.predict_proba(valid_texts)[:, positive_column]
print("đúng:", int((prediction == gold).sum()), "/", len(gold))
print("confusion matrix [0,1]:", confusion_matrix(gold, prediction, labels=[0, 1]).tolist())
for i in [2, 5]:
    print(f"thật={gold[i]} đoán={prediction[i]} p1={probability[i]:.3f} | {valid_texts[i]}")
assert np.array_equal(model["tfidf"].idf_, fitted_idf)
assert "không" not in model["tfidf"].vocabulary_

tfidf = model["tfidf"]
left = tfidf.transform(["bài giảng hay"])
right = tfidf.transform(["bài giảng không hay"])
print("hai vector giống nhau:", np.allclose(left.toarray(), right.toarray()))
has_bigram = tfidf.transform(["bài học hay"])
breaks_bigram = tfidf.transform(["bài học không hay"])
print("chèn không làm đứt bigram học hay:", not np.allclose(has_bigram.toarray(), breaks_bigram.toarray()))
assert np.allclose(left.toarray(), right.toarray())
assert not np.allclose(has_bigram.toarray(), breaks_bigram.toarray())

extra_texts = ["bài giảng không hay", "ví dụ không hay",
               "bài học không tệ", "lời giải không tệ"]
extended = Pipeline([
    ("tfidf", TfidfVectorizer(preprocessor=normalize_text, ngram_range=(1, 2))),
    ("classifier", LogisticRegression(C=4, random_state=0, max_iter=1000)),
])
extended.fit(train_texts + extra_texts, np.r_[labels, [0, 0, 1, 1]])
probes = ["nội dung không hay", "khóa học không tệ"]
for text, pred in zip(probes, extended.predict(probes)):
    print("sau bổ sung:", text, "->", int(pred))
print("đã học bigram không hay:", "không hay" in extended["tfidf"].vocabulary_)
assert "không hay" in extended["tfidf"].vocabulary_

