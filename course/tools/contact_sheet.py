"""Ghép ảnh slide (sáng, 1600px) thành các tấm 4 cột để rà nhanh: contact-1.png, contact-2.png, ...

python -B -X utf8 tools/contact_sheet.py qa/<id> [dark]   (dark: ghép bản nền tối, ra contact-dark-N.png)
"""
from pathlib import Path
import sys
from PIL import Image, ImageDraw

folder = Path(sys.argv[1])
theme = sys.argv[2] if len(sys.argv) > 2 else 'light'
files = sorted(folder.glob(f'slides-{theme}-1600-s*.png'))
W, H, COLS, PER = 480, 270, 4, 20
for part in range(0, len(files), PER):
    chunk = files[part:part + PER]
    rows = (len(chunk) + COLS - 1) // COLS
    sheet = Image.new('RGB', (W * COLS, H * rows), 'white')
    for i, f in enumerate(chunk):
        x, y = (i % COLS) * W, (i // COLS) * H
        sheet.paste(Image.open(f).convert('RGB').resize((W, H)), (x, y))
        ImageDraw.Draw(sheet).text((x + 6, y + 4), f.stem.split('-s')[-1], fill=(200, 0, 0))
    out = folder / (f'contact-{part // PER + 1}.png' if theme == 'light' else f'contact-{theme}-{part // PER + 1}.png')
    sheet.save(out)
    print(out.name, len(chunk))
