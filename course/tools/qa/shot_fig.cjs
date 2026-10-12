// Chụp nhanh một hoặc nhiều hình SVG ở nền sáng và tối, đúng font và biến màu của website (cần preview chạy ở 56872).
// node shot_fig.cjs ../../figures-recipe/staged/phase-0/fig/0-1-notebook.svg ...   [--width 640]
// Ghi vào 04. Workspace/AI-course-qa/figs/<tên>-light.png và <tên>-dark.png (một ảnh ghép hai nền: <tên>.png).
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const BASE = 'http://127.0.0.1:56872';
const CHROME = path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1200', 'chrome-win64', 'chrome.exe');
const OUT = path.resolve(__dirname, '../../../../04. Workspace/AI-course-qa/figs');

(async () => {
  const args = process.argv.slice(2);
  let width = 640;
  const files = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--width') { width = Number(args[++i]); continue; }
    files.push(args[i]);
  }
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: CHROME });
  const page = await browser.newPage({ viewport: { width: width * 2 + 120, height: 900 }, deviceScaleFactor: 2 });
  await page.goto(`${BASE}/START_HERE.html`, { waitUntil: 'networkidle' });
  for (const f of files) {
    const svg = fs.readFileSync(f, 'utf8');
    const name = path.basename(f, '.svg');
    const caption = (svg.match(/<title>([\s\S]*?)<\/title>/) || [, ''])[1];
    await page.evaluate(({ svg, width, caption }) => {
      document.documentElement.removeAttribute('data-theme');
      const pane = (theme) => `<div data-pane="${theme}" style="width:${width}px;padding:24px 20px;background:var(--bg)">
        <figure class="fig" style="margin:0">${svg}<figcaption>${caption}</figcaption></figure></div>`;
      document.body.innerHTML = `<div id="wrap" style="display:flex;gap:0;align-items:stretch">${pane('light')}${pane('dark')}</div>`;
      // Mỗi khung mang biến màu của theme riêng: chép biến từ :root theo từng theme.
      const root = document.documentElement;
      const read = (theme) => { root.dataset.theme = theme; const cs = getComputedStyle(root); const names = ['--bg','--surface','--line','--line-strong','--text','--text-2','--muted','--faint','--accent','--accent-strong','--accent-soft','--accent-ink','--ok','--code-bg','--code-head','--code-text','--t-k','--t-s','--t-n','--t-c']; const o = {}; for (const n of names) o[n] = cs.getPropertyValue(n); return o; };
      const light = read('light'), dark = read('dark');
      root.dataset.theme = 'light';
      for (const [theme, vars] of [['light', light], ['dark', dark]]) {
        const el = document.querySelector(`[data-pane="${theme}"]`);
        for (const [k, v] of Object.entries(vars)) el.style.setProperty(k, v);
        el.style.color = vars['--text'];
        el.querySelector('svg').style.color = vars['--text'];
      }
    }, { svg, width, caption });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(150);
    const wrap = await page.$('#wrap');
    const file = path.join(OUT, `${name}.png`);
    await wrap.screenshot({ path: file });
    console.log(file);
  }
  await browser.close();
})();
