"""Đồng bộ repo GitHub Canuc80k/ai-canuc80k từ bản dựng hiện tại rồi commit + push.

Cấu trúc repo:
  docs/      website (giống bản Cloudflare; GitHub Pages: Settings → Pages → main /docs)
  course/    nguồn giáo trình: bài học, slide, hình, trắc nghiệm, công cụ dựng
  README.md  sinh lại mỗi lần từ curriculum.json

Không đưa lên: phần riêng của giáo viên, bản gốc dữ liệu lớn chỉ dùng cho công cụ (theory.js, course-data.js,
code-examples.js), archive, receipt, node_modules.

    python -B -X utf8 tools/publish_repo.py -m "Thông điệp commit" [--no-push]
"""
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

COURSE = Path(__file__).resolve().parent.parent
OUT = COURSE / 'output'
ROOT = COURSE.parent.parent  # D:/Project/Canuc80k Problemset
REPO_DIR = ROOT / '04. Workspace' / 'ai-canuc80k-repo'
REMOTE = 'https://github.com/Canuc80k/ai-canuc80k.git'
LIVE = 'https://ai-canuc80k.ai-web-deploy-20261010.workers.dev/'
PAGES = 'https://canuc80k.github.io/ai-canuc80k/'

SITE_SKIP_TOP = {'teacher_private', 'current', 'smoke-final.pptx', 'HUONG_DAN_GIAO_VIEN.txt', 'KE_HOACH_CONTEST.txt'}
SITE_SKIP_FILES = {'ui/theory.js', 'ui/course-data.js', 'ui/code-examples.js'}
COURSE_KEEP = ['content', 'figures-recipe', 'code-examples', 'exam-sources', 'tools', 'curriculum.json',
               'theory.json', 'AUTHORING_BRIEF.md', 'README.md']
SKIP_NAMES = {'node_modules', '__pycache__', '.pytest_cache', 'build', 'verification'}


def git(*args, check=True):
    return subprocess.run(['git', *args], cwd=REPO_DIR, check=check, text=True, capture_output=True, encoding='utf-8')


def copy_tree(src: Path, dst: Path, skip=lambda rel: False, base=None):
    base = base or src
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.iterdir():
        rel = p.relative_to(base).as_posix()
        if p.name in SKIP_NAMES or skip(rel) or p.is_symlink():
            continue
        q = dst / p.name
        if p.is_dir():
            copy_tree(p, q, skip, base)
        elif not q.exists() or q.stat().st_size != p.stat().st_size or q.stat().st_mtime < p.stat().st_mtime:
            shutil.copy2(p, q)


def prune(src: Path, dst: Path, skip=lambda rel: False, base=None, dbase=None):
    """Xóa trong dst những gì không còn (hoặc bị loại) ở src."""
    base, dbase = base or src, dbase or dst
    for q in list(dst.iterdir()):
        rel = q.relative_to(dbase).as_posix()
        p = src / q.name
        if not p.exists() or q.name in SKIP_NAMES or skip(rel):
            shutil.rmtree(q) if q.is_dir() else q.unlink()
        elif q.is_dir():
            prune(p, q, skip, base, dbase)


def readme():
    cur = json.loads((COURSE / 'curriculum.json').read_text(encoding='utf-8'))
    phases = {p['id']: p for p in cur['phases']}
    lessons = cur['lessons']
    rows = []
    for k in cur['courses']:
        for pid in k['phases']:
            p = phases[pid]
            ls = [l for l in lessons if l['phase'] == pid and not str(l['id']).startswith('kt')]
            rows.append(f"| {k['title']} | {pid} · {p['title']} | {len(ls)} | {p.get('description', '')} |")
    nb = lambda i: f"https://colab.research.google.com/github/Canuc80k/ai-canuc80k/blob/main/docs/giao_trinh/notebook/{i}.ipynb"
    return f"""<p align="center"><img src="docs/ui/brand/social.png" alt="AI Canuc80k" width="720"></p>

<h3 align="center">Từ dòng Python đầu tiên tới đề thi IOAI.</h3>

<p align="center">Giáo trình AI cho học sinh lập trình thi đấu, hướng tới VOAI và IOAI.<br>
<a href="{LIVE}"><b>Mở website</b></a> · <a href="docs/giao_trinh/notebook">Notebook</a> · <a href="course/content">Nguồn bài học</a></p>

---

## Có gì ở đây

- **63 bài học + 4 bài kiểm tra.** Mỗi bài đi từ một câu hỏi thật, tính tay trước, rồi chạy code thấy kết quả (nút **Chạy** trên web).
- **2700+ câu hỏi.** Câu hỏi nhanh giữa bài, 10 câu cuối bài và sáu bộ trắc nghiệm Light → Ultra phỏng theo đề NOAI, USAAIO, CMU, MIT. Sai câu nào, bấm “Ôn lại” để mở đúng đoạn lý thuyết.
- **Bài tập tự chấm** cho từng bài (nộp trên LQDOJ) và **71 đề thi thật** (ROAI, OJIA, AIIS, IOAI…) xếp theo mức và theo chương.
- **Slide, PDF, notebook** cho mọi bài. Notebook mở thẳng trên Colab hoặc Kaggle.

## Lộ trình

| Khóa | Phase | Số bài | Nội dung |
|---|---|---|---|
{chr(10).join(rows)}

## Chạy notebook

Mỗi bài có một notebook ở [`docs/giao_trinh/notebook`](docs/giao_trinh/notebook). Mở trên Colab bằng đường dẫn
`https://colab.research.google.com/github/Canuc80k/ai-canuc80k/blob/main/docs/giao_trinh/notebook/<mã bài>.ipynb`, ví dụ
[Bài 0.1]({nb('0.1')}) · [Bài 2.7]({nb('2.7')}) · [Bài 6.3]({nb('6.3')}). Trên website, nút **Mở trên Colab** / **Mở trên Kaggle** nằm ngay dưới tên bài.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `docs/` | Website tĩnh (mở `docs/index.html`). Bật GitHub Pages: *Settings → Pages → Deploy from branch → main / docs*. |
| `docs/giao_trinh/` | Slide, PDF, notebook, code mẫu, đề bài tập. |
| `course/content/` | Nguồn bài học (`phase-N/<mã>.md`), slide, hình SVG, hình động, bài tập, trắc nghiệm. |
| `course/tools/` | Công cụ dựng từng bài, kiểm code, QA trình duyệt, xuất PDF, dựng web (`split_site.py`), đẩy repo (`publish_repo.py`). |
| `course/figures-recipe/` | Script vẽ lại hình và hình động. |

Xem web ở máy: `python -m http.server -d docs 8000` rồi mở `http://localhost:8000`.

## Nguồn và giấy phép

Câu hỏi phỏng theo đề thi ghi nguồn ngay dưới câu. Phông chữ Lora, Inter, JetBrains Mono theo SIL Open Font License (`docs/ui/fonts/OFL.txt`).
Ảnh mẫu lấy từ scikit-learn, scikit-image (ghi ở cuối mỗi bài). Nội dung giáo trình © Canuc80k.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-m', '--message', default='Cập nhật giáo trình và website')
    ap.add_argument('--no-push', action='store_true')
    args = ap.parse_args()

    subprocess.run([sys.executable, '-B', '-X', 'utf8', str(COURSE / 'tools' / 'split_site.py')], check=True)

    if not (REPO_DIR / '.git').exists():
        REPO_DIR.mkdir(parents=True, exist_ok=True)
        git('init', '-b', 'main')
        git('remote', 'add', 'origin', REMOTE)

    site_skip = lambda rel: rel.split('/')[0] in SITE_SKIP_TOP or rel in SITE_SKIP_FILES
    docs = REPO_DIR / 'docs'
    copy_tree(OUT, docs, site_skip)
    prune(OUT, docs, site_skip)
    shutil.copy2(OUT / 'START_HERE.html', docs / 'index.html')
    (docs / '.nojekyll').write_text('', encoding='utf-8')

    course_dst = REPO_DIR / 'course'
    course_dst.mkdir(exist_ok=True)
    for name in COURSE_KEEP:
        src = COURSE / name
        if src.is_dir():
            copy_tree(src, course_dst / name)
            prune(src, course_dst / name)
        elif src.exists():
            shutil.copy2(src, course_dst / name)
    for q in list(course_dst.iterdir()):
        if q.name not in COURSE_KEEP:
            shutil.rmtree(q) if q.is_dir() else q.unlink()

    (REPO_DIR / 'README.md').write_text(readme(), encoding='utf-8')
    (REPO_DIR / '.gitignore').write_text('__pycache__/\n*.pyc\nnode_modules/\n.DS_Store\nThumbs.db\n', encoding='utf-8')
    (REPO_DIR / '.gitattributes').write_text('* text=auto\n*.ipynb text eol=lf\n*.webp binary\n*.png binary\n*.pdf binary\n*.zip binary\n*.woff binary\n', encoding='utf-8')

    git('add', '-A')
    status = git('status', '--porcelain').stdout.strip()
    if not status:
        print('Không có thay đổi.')
        return
    git('-c', 'user.name=Canuc80k', '-c', 'user.email=canuc80k@gmail.com', 'commit', '-q', '-m', args.message, '-m', 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>')
    print(git('log', '--oneline', '-1').stdout.strip(), f'({len(status.splitlines())} tệp)')
    if not args.no_push:
        r = git('push', '-u', 'origin', 'main', check=False)
        print(r.stdout[-2000:], r.stderr[-2000:])
        if r.returncode:
            sys.exit(r.returncode)


if __name__ == '__main__':
    main()
