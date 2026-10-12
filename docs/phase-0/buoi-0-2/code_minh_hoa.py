# -*- coding: utf-8 -*-
import csv
from io import StringIO
from collections import Counter

# CSV mẫu được cấp ngay trong code; không cần tìm tệp bên ngoài.
raw = "id,label\n3,cat\n1,dog\n2,cat\n"
rows = list(csv.DictReader(StringIO(raw)))
print("Mỗi dòng là một dict:", rows[0])
# Đếm theo nhãn, không dùng vị trí dòng như một ID.
counts = Counter(row["label"] for row in rows)
print("Tần suất:", dict(sorted(counts.items())))
# Sắp xếp ID theo số; sort chuỗi có thể đặt '10' trước '2'.
ordered = sorted(rows, key=lambda row: int(row["id"]))
print("ID theo thứ tự số:", [r["id"] for r in ordered])
assert counts["cat"] == 2
