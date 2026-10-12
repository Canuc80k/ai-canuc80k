# -*- coding: utf-8 -*-
import json,sys

def solve(data):
    # Viết thuật toán theo BTVN tương ứng.
    raise NotImplementedError("Hoàn thành hàm solve")

if __name__ == "__main__":
    data=json.loads(sys.stdin.read())
    print(json.dumps(solve(data),ensure_ascii=False,allow_nan=False))
