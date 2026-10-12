"""Render lại mọi bài bằng renderer hiện tại và so với theory.js đang chạy, không ghi gì.

python -B -X utf8 tools/check_all_lessons.py [id_được_phép_khác ...]
In ra các bài có HTML khác bản đang chạy. Dùng sau khi sửa renderer để chắc bài khác không bị đổi.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rebuild_lesson as rb  # noqa: E402

ig = rb.ig
theory = ig.json_js(rb.OUT / 'ui/theory.js', rb.THEORY_PREFIX)
allowed = set(sys.argv[1:])
ig.copy_asset = lambda source: (rb.OUT / 'giao_trinh/assets' / source.resolve().relative_to(rb.CONTENT.resolve())).relative_to(rb.OUT).as_posix()
recipe_zips = {p.parent.name: f'giao_trinh/assets/{p.parent.name}/recipes.zip' for p in rb.CONTENT.glob('phase-*/recipes') if any(p.rglob('*.py'))}
diff, same = [], 0
for path in sorted(rb.CONTENT.glob('phase-*/*.md')):
    item = ig.rt.render(path)
    html = ig.asset_links(item['html'], path.parent)
    if path.stem == '_intro':
        old = theory['phases'][path.parent.name.split('-')[1]]['html']
    else:
        text = path.read_text(encoding='utf-8')
        if 'recipes/' in text and path.parent.name in recipe_zips:
            html += (f'<p><a href="{recipe_zips[path.parent.name]}" download>Tải gói recipe của chương</a>'
                     ' — gồm các module phụ và hướng dẫn chuẩn bị asset.</p>')
        old = theory['lessons'][path.stem]['html']
    if html == old:
        same += 1
    else:
        diff.append(path.stem if path.stem != '_intro' else path.parent.name + '/_intro')
print('giống:', same, 'khác:', diff)
unexpected = [d for d in diff if d not in allowed]
print('khác ngoài danh sách cho phép:', unexpected)
sys.exit(1 if unexpected else 0)
