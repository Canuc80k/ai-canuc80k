# -*- coding: utf-8 -*-
# Code mẫu — Python

# Ví dụ 1: Thay ngưỡng điểm, danh sách đạt đổi thế nào?
def summarize_scores(values, threshold=5.0):
    if not values:
        raise ValueError("danh sách điểm rỗng")
    passed = []
    for value in values:
        if value >= threshold:
            passed.append(value)
    # Gom đủ các điểm rồi mới trả về. Đặt return trong vòng for sẽ bỏ sót các điểm phía sau.
    return sum(values) / len(values), passed

scores = [4.5, 6.0, 8.0, 5.0]
for threshold in [5.0, 6.0]:
    mean_score, passed = summarize_scores(scores, threshold=threshold)
    print(f"ngưỡng {threshold:.1f}: trung bình {mean_score:.3f}, đạt {passed}")

try:
    summarize_scores([])
except ValueError as error:
    print("ValueError:", error)


# Ví dụ 2: Sửa thử một bảng mà vẫn giữ được bảng gốc
from copy import deepcopy

original = [[6, 8], [5, 7]]
trial = original
trial[0][0] = 10
print("gán tên:", original, "cùng đối tượng:", trial is original)

original = [[6, 8], [5, 7]]
trial = original.copy()
trial[0][0] = 10
print("copy một tầng:", original, "cùng hàng:", trial[0] is original[0])

original = [[6, 8], [5, 7]]
trial = deepcopy(original)
trial[0][0] = 10
print("deepcopy:", original, trial)
assert original == [[6, 8], [5, 7]]

# Mỗi hàng của bảng kết quả phải là một list mới, không dùng chung.
table_bad = [[0, 0]] * 2
table_good = [[0, 0] for _ in range(2)]
table_bad[0][1] = table_good[0][1] = 9
print("hàng dùng chung:", table_bad)
print("hàng độc lập:", table_good)


# Ví dụ 3: Đánh mã cho từ vựng sao cho chạy lại vẫn ra như cũ
from collections import Counter

def make_vocab(tokens):
    # Bỏ từ trùng, để <UNK> ở vị trí 0, rồi sắp xếp các từ còn lại cho thứ tự luôn cố định.
    words = ["<UNK>"] + sorted(set(tokens) - {"<UNK>"})
    return {word: index for index, word in enumerate(words)}

tokens = ["mèo", "chó", "mèo", "chim"]
vocab = make_vocab(tokens)
encoded = [vocab[token] for token in tokens]
print("bảng mã:", vocab)
print("dãy ID:", encoded)
print("tần suất:", sorted(Counter(tokens).items()))
print("đảo dữ liệu, giữ bảng mã:", vocab == make_vocab(tokens[::-1]))
assert make_vocab(["<UNK>", "mèo"])["<UNK>"] == 0

new_tokens = ["chó", "cá"]
new_ids = [vocab.get(token, vocab["<UNK>"]) for token in new_tokens]
print("từ mới:", new_ids)


# Ví dụ 4: Đọc điểm từ CSV, ghi lại lỗi, rồi kiểm file đã ghi
import csv
from pathlib import Path
from tempfile import TemporaryDirectory

def read_scores(path):
    valid, problems = [], []
    with path.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            try:
                score = float(row["score"])
            except ValueError:
                problems.append((row["id"], "điểm không phải số"))
                continue
            if not 0 <= score <= 10:
                problems.append((row["id"], "điểm ngoài thang 0–10"))
                continue
            valid.append({"id": row["id"], "name": row["name"], "score": score})
    return valid, problems

with TemporaryDirectory(prefix="python-csv-", dir=".") as directory:
    data_dir = Path(directory)
    source = data_dir / "scores.csv"
    source.write_text(
        'id,name,score\n001,An,8.5\n002,"Bình, lớp A",6.0\n'
        '003,Chi,?\n004,Dũng,4.5\n', encoding="utf-8")
    rows, problems = read_scores(source)
    print("lỗi cần kiểm:", problems)
    print("tên có dấu phẩy:", rows[1]["name"])

    selected = sorted((row for row in rows if row["score"] >= 6),
                      key=lambda row: -row["score"])
    assert len({row["id"] for row in selected}) == len(selected)
    destination = data_dir / "accepted.csv"
    with destination.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "score"])
        writer.writeheader()
        writer.writerows(selected)

    # Đọc lại chính file vừa ghi để kiểm, chứ không chỉ kiểm biến selected trong bộ nhớ.
    restored, restored_problems = read_scores(destination)
    assert restored == selected and not restored_problems
    print("đọc lại:", [(row["id"], row["score"]) for row in restored])
    print("CSV giữ đúng dữ liệu:", restored == selected)

