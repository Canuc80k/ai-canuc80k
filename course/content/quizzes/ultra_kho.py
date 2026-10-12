"""Kho kiểm tra mức Ultra: 100 câu không nằm trong bộ Ultra luyện tập, chỉ bốc vào chế độ kiểm tra."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _choice import ULTRA  # noqa: E402
from _pick import rest  # noqa: E402

GROUPS = rest('_ultra_a', '_ultra_b', ULTRA)
