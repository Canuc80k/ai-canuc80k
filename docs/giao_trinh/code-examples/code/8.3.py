# -*- coding: utf-8 -*-
# Code mẫu — Bài toán mở

# Ví dụ 1: Nên hỏi câu nào để thu hẹp nhiều nhất?
from collections import Counter
import numpy as np

points = np.arange(8, dtype=float)
def verdict(a, b, hidden):
    left, right = abs(points[a] - points[hidden]), abs(points[b] - points[hidden])
    return 0 if left == right else (-1 if left < right else 1)

for proposal in [1, 6]:
    partitions = {response: [hidden for hidden in range(8)
                             if verdict(0, proposal, hidden) == response]
                  for response in [-1, 0, 1]}
    sizes = [len(group) for group in partitions.values()]
    expected = sum(size ** 2 for size in sizes) / 8
    # Duyệt từng hidden một, để kiểm công thức tính theo kích thước nhóm bằng một cách độc lập.
    enumerated = np.mean([len(partitions[verdict(0, proposal, hidden)])
                          for hidden in range(8)])
    assert expected == enumerated
    print("proposal:", proposal, "nhóm:", partitions)
    print("số còn lại kỳ vọng:", f"{expected:.2f}")


# Ví dụ 2: Ghép các đoạn, mỗi đoạn dùng đúng một lần
from itertools import permutations

pieces = ("A", "B", "C", "D")
score = {("A", "B"): 9, ("A", "C"): 7,
         ("B", "C"): 1, ("B", "D"): 8,
         ("C", "B"): 8, ("C", "D"): 2}
answers = []
for order in permutations(pieces):
    if order[0] != "A" or order[-1] != "D":
        continue
    value = sum(score[left, right] for left, right in zip(order, order[1:]))
    assert len(set(order)) == len(pieces)
    answers.append((value, order))
for value, order in sorted(answers):
    print("thứ tự:", order, "tổng điểm:", value)
best = max(answers)
assert best == (23, ("A", "C", "B", "D"))
print("cặp đầu cao nhất:", max((value, pair) for pair, value in score.items() if pair[0] == "A"))
print("lời giải toàn cục:", best)


# Ví dụ 3: Giữ nguyên người chơi, đổi cách judge nhìn thế giới
import numpy as np

public = np.arange(8, dtype=float)
def predict_response(points, a, b, hidden):
    left, right = abs(points[a] - points[hidden]), abs(points[b] - points[hidden])
    return 0 if left == right else (-1 if left < right else 1)

def make_judge(private_points, hidden):
    asked = set()
    def ask(champion, proposal):
        assert 0 <= proposal < len(private_points) and proposal not in asked
        asked.add(proposal)
        # Chỉ judge biết hidden. Player chỉ nhận về: có trúng không, và một câu trả lời.
        return proposal == hidden, predict_response(private_points, champion, proposal, hidden)
    return ask

def player(ask, budget=3):
    possible, asked, champion = list(range(len(public))), set(), 0
    for turn in range(1, budget + 1):
        available = [item for item in possible if item not in asked]
        if not available:
            return False, turn - 1
        def expected(proposal):
            counts = [sum(predict_response(public, champion, proposal, h) == response
                          for h in possible) for response in [-1, 0, 1]]
            return sum(count ** 2 for count in counts) / len(possible)
        proposal = min(available, key=lambda q: (expected(q), q))
        asked.add(proposal)
        hit, response = ask(champion, proposal)
        if hit:
            return True, turn
        possible = [h for h in possible if h != proposal and
                    predict_response(public, champion, proposal, h) == response]
        if response == 1:
            champion = proposal
    return False, budget

shifted = public.copy()
shifted[[4, 5]] = shifted[[5, 4]]
for name, private in [("cùng miền", public), ("đổi 4 và 5", shifted)]:
    results = [player(make_judge(private, hidden)) for hidden in range(8)]
    solved = sum(success for success, turns in results)
    print(name, "giải được:", solved, "/ 8", "từng game:", results)

response = predict_response(shifted, 4, 5, 6)
kept = [h for h in range(8) if predict_response(public, 4, 5, h) == response]
penalty = np.maximum(0, abs(public - public[4]) - abs(public - public[5]))
print("phản hồi judge cho (4,5):", response, "lọc giữ:", kept)
print("hidden 6 còn sau lọc:", 6 in kept, "penalty mềm:", float(penalty[6]))
assert 6 not in kept and np.isfinite(penalty[6])

