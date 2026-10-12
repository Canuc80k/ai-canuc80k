"""Bộ Max: 100 câu chọn lọc từ hai bộ nguồn _max_a.py và _max_b.py (danh sách ở _choice.py).
Các câu còn lại nằm ở max_kho.py, chỉ dùng khi làm bài kiểm tra mức Max.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _choice import MAX  # noqa: E402
from _pick import pick  # noqa: E402

GROUPS = pick('_max_a', '_max_b', MAX)
