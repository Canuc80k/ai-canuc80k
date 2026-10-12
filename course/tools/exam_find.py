"""Tra cứu đề chính thức/đề luyện đã trích văn bản trong exam-sources/.

python -B -X utf8 tools/exam_find.py "lasso" "regulari"        # liệt kê trang khớp (mọi từ, không phân biệt hoa thường)
python -B -X utf8 tools/exam_find.py --page noai2026prelim 59   # in nguyên một trang
"""
from pathlib import Path
import re, sys

SRC = Path(__file__).resolve().parents[1] / 'exam-sources'
LABEL = {
    'noai2026prelim': 'NOAI 2026 · Vòng sơ loại (Singapore)', 'noai2026final': 'NOAI 2026 · Chung kết, Phần 1 (Singapore)',
    'noai2025mcq': 'NOAI 2025 · Phần 1 trắc nghiệm (Singapore)', 'usaaio2026r1': 'USA-NA-AIO 2026 · Vòng 1',
    'usaaio2026r2d1': 'USA-NA-AIO 2026 · Vòng 2 · Ngày 1', 'usaaio2026r2d2': 'USA-NA-AIO 2026 · Vòng 2 · Ngày 2',
    'cmu_exam1': 'CMU 10-601 · Practice Problems, Exam 1', 'cmu_exam2': 'CMU 10-601 · Practice Problems, Exam 2',
    'cmu_exam3': 'CMU 10-601 · Practice Problems, Exam 3', 'mit6036_final_sp22': 'MIT 6.036 · Final, Spring 2022',
}


def pages(name):
    parts = re.split(r'\n=== PAGE (\d+) ===\n', (SRC / f'{name}.txt').read_text(encoding='utf-8'))
    return {int(parts[k]): parts[k + 1] for k in range(1, len(parts), 2)}


if __name__ == '__main__':
    if sys.argv[1] == '--page':
        print(pages(sys.argv[2])[int(sys.argv[3])]); sys.exit()
    words = [w.lower() for w in sys.argv[1:]]
    for f in sorted(SRC.glob('*.txt')):
        for no, body in pages(f.stem).items():
            low = body.lower()
            if all(w in low for w in words):
                nums = re.findall(r'^(\d+)\.\nMark only one oval', body, re.M)
                print(f'{f.stem:20} p{no:<4} {LABEL.get(f.stem, "")}  {"Q" + ",".join(nums) if nums else ""}')
