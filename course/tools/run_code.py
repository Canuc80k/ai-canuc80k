"""Chạy file code hoàn chỉnh của từng bài và ghi kết quả bên cạnh (<id>.out.txt).

Chạy: python run_code.py <thư-mục-content>   (dừng nếu có file chạy lỗi)
"""
import subprocess, sys
from pathlib import Path

CONTENT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'content'
for path in sorted(CONTENT.glob('phase-*/code/*.py')):
    r = subprocess.run([sys.executable, path.name], cwd=path.parent, capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        raise SystemExit(f'{path}: lỗi\n{r.stderr}')
    path.with_suffix('.out.txt').write_text(r.stdout, encoding='utf-8')
    print(f'{path.name}: {len(r.stdout.splitlines())} dòng kết quả')
