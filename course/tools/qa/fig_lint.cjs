// Kiểm hình SVG bằng hình học thật trong Chromium (đúng font của web): chữ tràn khỏi khung/ô chứa nó, chữ đè chữ,
// đường kẻ/mũi tên cắt qua chữ, chữ ra ngoài khung hình.
// node fig_lint.cjs <file.svg | thư mục fig ...> [--json out.json]
// In một dòng cho mỗi vấn đề; mã thoát 1 nếu có vấn đề.
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const BASE = 'http://127.0.0.1:56872';
const CHROME = path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1200', 'chrome-win64', 'chrome.exe');

function collect(args) {
  const out = [];
  for (const a of args) {
    if (fs.statSync(a).isDirectory()) for (const f of fs.readdirSync(a).sort()) { if (f.endsWith('.svg')) out.push(path.join(a, f)); }
    else out.push(a);
  }
  return out;
}

(async () => {
  const args = process.argv.slice(2);
  let jsonOut = null;
  const j = args.indexOf('--json');
  if (j >= 0) { jsonOut = args[j + 1]; args.splice(j, 2); }
  const files = collect(args);
  const browser = await chromium.launch({ executablePath: CHROME });
  const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
  await page.goto(`${BASE}/START_HERE.html`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const report = {};
  let bad = 0;
  for (const f of files) {
    const svg = fs.readFileSync(f, 'utf8');
    const issues = await page.evaluate((svg) => {
      document.body.innerHTML = `<div class="theory" style="width:640px;background:var(--bg)"><figure class="fig">${svg}</figure></div>`;
      const root = document.querySelector('figure svg');
      root.style.width = '640px';
      const R = root.getBoundingClientRect();
      const box = (el) => { const b = el.getBoundingClientRect(); return { x: b.left - R.left, y: b.top - R.top, w: b.width, h: b.height }; };
      const inter = (a, b) => Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x)) * Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));
      const shrink = (b, d) => ({ x: b.x + d, y: b.y + d, w: Math.max(0, b.w - 2 * d), h: Math.max(0, b.h - 2 * d) });
      const out = [];
      const texts = [...root.querySelectorAll('text')].filter(t => t.textContent.trim());
      // Hộp chữ: dùng chiều cao thật của glyph (bỏ phần đệm dòng) bằng cách co dọc 18%.
      const tb = texts.map(t => { const b = box(t); const d = b.h * 0.18; return { t: t.textContent.trim(), b: { x: b.x, y: b.y + d, w: b.w, h: b.h - 2 * d } }; });
      for (const { t, b } of tb) {
        if (b.x < -1 || b.y < -1 || b.x + b.w > R.width + 1 || b.y + b.h > R.height + 1) out.push(`ra ngoài khung hình: "${t}"`);
      }
      for (let i = 0; i < tb.length; i++) for (let k = i + 1; k < tb.length; k++) {
        const a = tb[i].b, c = tb[k].b, s = inter(shrink(a, 1), shrink(c, 1));
        if (s > 2) out.push(`chữ đè chữ: "${tb[i].t}" / "${tb[k].t}"`);
      }
      // Ô/khung: rect có viền hoặc nền. Chữ nằm một phần trong rect là tràn ô.
      const rects = [...root.querySelectorAll('rect')].filter(r => {
        const st = r.getAttribute('stroke'), fl = r.getAttribute('fill');
        const sw = parseFloat(r.getAttribute('stroke-width') || '1');
        const visible = (st && st !== 'none' && sw > 0) || (fl && fl !== 'none');
        return visible && !r.closest('clipPath');
      }).map(r => box(r)).filter(b => b.w > 6 && b.h > 6 && b.w < R.width * 0.98);
      for (const { t, b } of tb) {
        for (const r of rects) {
          const s = inter(b, r);
          const area = b.w * b.h;
          if (s > area * 0.02 && s < area * 0.98) { out.push(`chữ tràn ô: "${t}"`); break; }
        }
      }
      // Đường kẻ và mũi tên đi qua chữ.
      const paths = [...root.querySelectorAll('path, line, polyline')].filter(p => {
        const st = p.getAttribute('stroke'); return st && st !== 'none' && !p.closest('clipPath') && !p.closest('defs');
      });
      const m = root.getScreenCTM();
      for (const p of paths) {
        let L = 0; try { L = p.getTotalLength(); } catch (e) { continue; }
        if (!L || L > 4000) continue;
        const pm = p.getScreenCTM();
        const hits = new Set();
        for (let s = 0; s <= L; s += 1.5) {
          const q = p.getPointAtLength(s);
          const sp = new DOMPoint(q.x, q.y).matrixTransform(pm);
          const x = sp.x - R.left, y = sp.y - R.top;
          for (const { t, b } of tb) {
            const bb = shrink(b, 1.5);
            if (x > bb.x && x < bb.x + bb.w && y > bb.y && y < bb.y + bb.h) hits.add(t);
          }
        }
        for (const t of hits) out.push(`đường kẻ cắt qua chữ: "${t}"`);
      }
      return [...new Set(out)];
    }, svg);
    const name = path.basename(f, '.svg');
    report[name] = issues;
    if (issues.length) { bad++; for (const s of issues) console.log(`${name}: ${s}`); }
  }
  console.log(`--- ${files.length} hình, ${bad} hình có vấn đề`);
  if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(report, null, 1));
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
