// Quét nhanh mọi slide (không chụp ảnh): phần tử tràn khỏi slide, khỏi cột của bố cục split,
// khỏi ô đáp án; slide tràn dọc (over()) và slide phải co chữ dưới 0.88. In một dòng cho mỗi slide có vấn đề.
// node scan_slides.cjs [id ...] [--width 1280 --height 800]   (mặc định: mọi bài có trong giao_trinh/slides)
// Cần preview đang chạy ở 127.0.0.1:56872.
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const BASE = 'http://127.0.0.1:56872';
const CHROME = path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1200', 'chrome-win64', 'chrome.exe');
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i < 0 ? d : Number(args.splice(i, 2)[1]); };
const width = opt('--width', 1280), height = opt('--height', 800);
let ids = args;
if (!ids.length) {
  const dir = path.resolve(__dirname, '../../output/giao_trinh/slides');
  ids = fs.readdirSync(dir).filter(f => f.endsWith('.html')).map(f => f.slice(0, -5))
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  let bad = 0, total = 0, shrunk = 0;
  for (const id of ids) {
    await page.goto(`${BASE}/giao_trinh/slides/${id}.html#theme=light`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(300);
    const n = await page.evaluate(() => s.length);
    for (let i = 0; i < n; i++) {
      total++;
      const r = await page.evaluate(i => {
        n = i; show(); const el = s[i];
        const out = [];
        const box = (e) => e.getBoundingClientRect();
        const beyond = (inner, outer, tol = 1.5) => inner.width > 0 && (inner.right > outer.right + tol || inner.left < outer.left - tol);
        const name = (e) => (e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : '') + ' ' + (e.textContent || '').trim().slice(0, 40));
        const sb = box(el);
        // Bỏ phần MathML ẩn của KaTeX và hình học bên trong SVG (bị cắt bởi viewBox); vẫn kiểm chính thẻ svg.
        const skip = (c) => c.closest('.katex-mathml') || (c.closest('svg') && c.tagName.toLowerCase() !== 'svg');
        const all = (root) => [...root.querySelectorAll('*')].filter(c => !skip(c));
        for (const c of all(el)) if (beyond(box(c), sb)) { out.push('slide: ' + name(c)); break; }
        for (const col of el.querySelectorAll('.s-split .s-body > *')) {
          const cb = box(col);
          for (const c of all(col)) {
            if (c.closest('pre') && c.tagName !== 'PRE') continue;   // pre tự cuộn
            if (beyond(box(c), cb)) { out.push('cột: ' + name(c)); break; }
          }
        }
        for (const o of el.querySelectorAll('.quiz-opt')) {
          const ob = box(o);
          for (const c of all(o)) if (beyond(box(c), ob)) { out.push('đáp án: ' + name(c)); break; }
        }
        for (const p of el.querySelectorAll('pre')) if (p.scrollWidth > p.clientWidth + 1) out.push('pre cuộn ngang: ' + name(p));
        return { fs: el.style.getPropertyValue('--fs') || '1', over: over(el), out };
      }, i);
      const small = Number(r.fs) < 0.88; if (Number(r.fs) < 1) shrunk++;
      if (r.over || r.out.length || small) { bad++; console.log(`${id} s${String(i + 1).padStart(2, '0')} fs=${r.fs}${r.over ? ' TRÀN-DỌC' : ''}${small ? ' CHỮ-NHỎ' : ''} ${r.out.join(' | ')}`); }
    }
  }
  console.log(`--- ${ids.length} bài, ${total} slide, ${bad} slide có vấn đề, ${shrunk} slide phải co chữ (${width}×${height})`);
  await browser.close();
})();
