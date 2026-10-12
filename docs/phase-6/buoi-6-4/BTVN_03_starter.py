# -*- coding: utf-8 -*-
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"data"/'hw_6_4'

def read_csv(name):
    with (DATA/name).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

train=read_csv("train.csv")
valid=read_csv("valid.csv")
test=read_csv("test.csv")
print("Số mẫu:",len(train),len(valid),len(test))
meta=json.loads((DATA/"DATA_NOTE.json").read_text(encoding="utf-8"))
print("Cần output:",meta["output_header"])
# Hoàn thành preprocessing/model và predict. Chưa tạo submission vì chưa có thuật toán.
# Khi viết CSV dùng csv.writer, UTF-8, newline="", và giữ ID.
