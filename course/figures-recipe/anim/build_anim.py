"""Dựng hình động của giáo trình (lượt 9).

python -B -X utf8 build_anim.py                 # dựng mọi hình vào staged/, kèm ảnh ghép duyệt mắt
python -B -X utf8 build_anim.py 5-1 2-10-kmeans # chỉ những hình có tên bắt đầu như vậy
python -B -X utf8 build_anim.py --apply         # chép staged/phase-N/fig/* vào ../../content/phase-N/fig/

Mỗi chương một tệp a_chN.py, khai báo ANIMS = [hàm, ...]; mỗi hàm trả về một kit.Anim.
Tên hình '5-1-conv' -> content/phase-5/fig/5-1-conv.anim.webp (+ .anim.json, có thể .anim.dark.webp).
"""
from pathlib import Path
import importlib, json, shutil, sys, time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import akit as kit  # noqa: E402

CONTENT = HERE.parents[1] / 'content'
STAGED = HERE / 'staged'
QA = HERE.parents[3] / '04. Workspace' / 'AI-anim-20261011' / 'qa'
MANIFEST = HERE / 'manifest.json'


def all_anims():
    for path in sorted(HERE.glob('a_ch*.py'), key=lambda p: int(p.stem[4:])):
        mod = importlib.import_module(path.stem)
        for fn in mod.ANIMS:
            yield fn


def save_manifest(update):
    """Ghi ngay sau mỗi hình, có khóa tệp: nhiều tiến trình dựng song song không xóa kết quả của nhau."""
    import os
    lock = MANIFEST.with_suffix('.lock')
    for _ in range(600):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            time.sleep(.1)
    else:
        raise RuntimeError('manifest bị khóa quá lâu: xóa manifest.lock nếu không còn tiến trình nào chạy')
    try:
        manifest = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.is_file() else {}
        manifest.update(update)
        MANIFEST.write_text(json.dumps(dict(sorted(manifest.items())), ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    finally:
        os.close(fd)
        os.remove(lock)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--apply' in sys.argv:
        n = 0
        for f in sorted(STAGED.glob('phase-*/fig/*.anim.*')):
            if args and not any(f.name.startswith(a) for a in args):
                continue
            target = CONTENT / f.relative_to(STAGED)
            if not target.is_file() or target.read_bytes() != f.read_bytes():
                shutil.copy2(f, target)
                n += 1
        print('đã chép', n, 'tệp')
        return
    for fn in all_anims():
        name = fn.__name__[1:].replace('_', '-')   # a5_1_conv -> 5-1-conv
        if args and not any(name.startswith(a) for a in args):
            continue
        t0 = time.time()
        if 'torch' in sys.modules:          # code bài (vd. 4.4) có thể đổi trạng thái toàn cục của torch
            sys.modules['torch'].set_default_dtype(sys.modules['torch'].float32)
        anim = fn()
        assert anim.name == name, (anim.name, name)
        phase = name.split('-')[0]
        rep, light, dark = kit.build(anim, STAGED / f'phase-{phase}' / 'fig')
        kit.contact(light, dark, anim.labels, QA / f'{name}.png')
        save_manifest({name: rep})
        kb = sum(rep['bytes'].values()) / 1024
        print(f'{name}: {rep["frames"]} khung {rep["size"][0]}x{rep["size"][1]}, {kb:.0f} KB, {time.time() - t0:.1f}s'
              + (' (có bản tối)' if dark is not None else ''))


if __name__ == '__main__':
    main()
