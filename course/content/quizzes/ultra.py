"""Bộ Ultra: 100 câu chọn lọc từ hai bộ nguồn _ultra_a.py và _ultra_b.py (danh sách ở _choice.py).
Các câu còn lại nằm ở ultra_kho.py, chỉ dùng khi làm bài kiểm tra mức Ultra.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _choice import ULTRA  # noqa: E402
from _pick import pick  # noqa: E402

GROUPS = pick('_ultra_a', '_ultra_b', ULTRA)
