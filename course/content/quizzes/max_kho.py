"""Kho kiểm tra mức Max: 100 câu không nằm trong bộ Max luyện tập, chỉ bốc vào chế độ kiểm tra."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _choice import MAX  # noqa: E402
from _pick import rest  # noqa: E402

GROUPS = rest('_max_a', '_max_b', MAX)
