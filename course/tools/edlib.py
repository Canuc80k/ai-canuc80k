"""Sửa một tệp nguồn bằng các phép thay chuỗi chính xác (mỗi chuỗi cũ phải xuất hiện đúng một lần)."""
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / 'content'


class Doc:
    def __init__(self, rel):
        self.path = CONTENT / rel
        self.text = self.path.read_text(encoding='utf-8')

    def rep(self, old, new, count=1):
        n = self.text.count(old)
        assert n == count, f'{self.path.name}: tìm thấy {n} lần, cần {count}: {old[:90]!r}'
        self.text = self.text.replace(old, new)

    def save(self):
        self.path.write_text(self.text, encoding='utf-8')
        print('saved', self.path.relative_to(CONTENT), self.text.count('::: quiz'), 'quiz')
