// Chụp vài trang slide cụ thể ở 1280×800 (mặc định) để xem bằng mắt.
// node shot_slides.cjs <id> <số trang ...> [--out <thư mục>] [--theme dark] [--width 1600 --height 900]
// Ảnh: <out>/<id>-sNN.png (mặc định out = 04. Workspace/AI-course-qa/shots). Cần preview ở 127.0.0.1:56872.
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const BASE = 'http://127.0.0.1:56872';
const CHROME = path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1200', 'chrome-win64', 'chrome.exe');
const args = process.argv.slice(2);
const take = (k, d) => { const i = args.indexOf(k); return i < 0 ? d : args.splice(i, 2)[1]; };
const out = path.resolve(take('--out', path.join(__dirname, '../../../../04. Workspace/AI-course-qa/shots')));
const theme = take('--theme', 'light');
const width = Number(take('--width', 1280)), height = Number(take('--height', 800));
const [id, ...pages] = args;

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ executablePath: CHROME });
  const ctx = await browser.newContext({ viewport: { width, height }, colorScheme: theme, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/giao_trinh/slides/${id}.html#theme=${theme}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(400);
  for (const p of pages) {
    const i = Number(p) - 1;
    const fsv = await page.evaluate(i => { n = i; show(); return s[i].style.getPropertyValue('--fs') || '1'; }, i);
    const file = path.join(out, `${id}-s${String(i + 1).padStart(2, '0')}.png`);
    await page.screenshot({ path: file });
    console.log(file, 'fs=' + fsv);
  }
  await browser.close();
})();
