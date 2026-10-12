# -*- coding: utf-8 -*-

# Dữ liệu: điểm của bốn bài kiểm tra, thang 0..10.
scores = [8, 5, 9, 4]
# Hàm trả True nếu điểm đạt yêu cầu; không chỉ print kết quả.
def passed(score):
    return score >= 6
# Duyệt từng điểm và đếm bằng một biến có ý nghĩa.
count = 0
for score in scores:
    if passed(score):
        count += 1
print("Điểm:", scores)
print("Số bài đạt:", count)
print("Trung bình:", sum(scores) / len(scores))
assert count == 2
