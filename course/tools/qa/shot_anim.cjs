// Kiểm hình động (lượt 9) trên website đang chạy: mỗi hình chụp ở nền sáng, nền tối, bản in (khung chính),
// và trang slide chứa hình. node shot_anim.cjs [--base=http://127.0.0.1:56873] <id ...>
// Ảnh ghi vào 04. Workspace/AI-anim-20261011/shots/<id>/; in ra lỗi console và hình không vẽ được.
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const BASE = (args.find(a => a.startsWith('--base=')) || '--base=http://127.0.0.1:56873').slice(7);
const ids = args.filter(a => !a.startsWith('--'));
const OUT = path.resolve(__dirname, '../../../../04. Workspace/AI-anim-20261011/shots');
const CHROME = path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1200', 'chrome-win64', 'chrome.exe');

async function lesson(browser, id, scheme) {
  const ctx = await browser.newContext({ viewport: { width: 1100, height: 900 }, colorScheme: scheme, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(`${BASE}/START_HERE.html#/lesson/${id}`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const figs = await page.$$('figure.anim');
  const res = [];
  for (let i = 0; i < figs.length; i++) {
    await figs[i].scrollIntoViewIfNeeded();
    await page.waitForTimeout(1600);
    const st = await figs[i].evaluate(f => {
      const c = f.querySelector('canvas.anim-stage'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
      let ink = 0; for (let k = 3; k < d.length; k += 4 * 97) if (d[k] > 0) ink++;
      return { label: f.querySelector('.anim-label').textContent, playing: f.classList.contains('is-playing'), ink, w: Math.round(c.getBoundingClientRect().width) };
    });
    // dừng ở khung giữa để ảnh chụp ổn định
    await figs[i].evaluate(f => { const p = f._anim; p.pause(true); p.show(Math.floor(p.m.n * 0.6)); });
    await page.waitForTimeout(200);
    await figs[i].screenshot({ path: path.join(OUT, id, `${scheme}-anim${i + 1}.png`) });
    res.push(st);
  }
  if (scheme === 'light' && figs.length) {
    await page.evaluate(() => window.Anim.readyAll());
    await page.emulateMedia({ media: 'print' });
    await page.waitForTimeout(300);
    for (let i = 0; i < figs.length; i++) await figs[i].screenshot({ path: path.join(OUT, id, `print-anim${i + 1}.png`) });
  }
  await ctx.close();
  return { res, errors };
}

async function slides(browser, id) {
  const ctx = await browser.newContext({ viewport: { width: 1600, height: 900 }, colorScheme: 'light' });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(`${BASE}/giao_trinh/slides/${id}.html#theme=light`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const idx = await page.evaluate(() => [...document.querySelectorAll('.slide')].map((s, i) => s.querySelector('figure.anim') ? i : -1).filter(i => i >= 0));
  const out = [];
  for (const k of idx) {
    await page.evaluate(k => { n = k; show(); }, k);
    await page.waitForTimeout(1500);
    const fs_ = await page.evaluate(() => { const s = document.querySelector('.slide.active'); return { fs: s.style.getPropertyValue('--fs') || '1', over: s.scrollHeight > s.clientHeight + 1 }; });
    await page.screenshot({ path: path.join(OUT, id, `slide${k + 1}.png`) });
    out.push({ slide: k + 1, ...fs_ });
  }
  await ctx.close();
  return { out, errors };
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  for (const id of ids) {
    fs.mkdirSync(path.join(OUT, id), { recursive: true });
    const L = await lesson(browser, id, 'light');
    const D = await lesson(browser, id, 'dark');
    const S = await slides(browser, id);
    console.log(JSON.stringify({ id, light: L.res, dark: D.res.map(r => r.ink), slides: S.out, errors: [...L.errors, ...D.errors, ...S.errors] }));
  }
  await browser.close();
})();
