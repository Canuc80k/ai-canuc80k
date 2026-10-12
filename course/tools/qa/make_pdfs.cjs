// Xuất PDF bài học (A4) và PDF slide (16:9) bằng Chromium, từ bản website đang chạy ở preview.
// node make_pdfs.cjs 2.2 2.3 ...      (hoặc --all)
// Ghi vào output/giao_trinh/pdf/bai-<id>.pdf và slide-<id>.pdf (PDF cũ trong giao_trinh/slides/ giữ nguyên).
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const BASE = process.env.AI_BASE || 'http://127.0.0.1:56872';
const OUT = path.resolve(__dirname, '../../output');
const CHROME = path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1200', 'chrome-win64', 'chrome.exe');

function lessonIds() {
  const text = fs.readFileSync(path.join(OUT, 'ui/course-data.js'), 'utf8');
  const data = JSON.parse(text.slice(text.indexOf('{')).trim().replace(/;$/, ''));
  return data.lessons.filter(l => l.deck).map(l => l.id);
}

async function lessonPdf(browser, id) {
  const ctx = await browser.newContext({ viewport: { width: 900, height: 1200 }, colorScheme: 'light' });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/START_HERE.html#/lesson/${id}`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  await page.evaluate(() => window.Anim ? Anim.readyAll() : null);   // hình động: nạp sprite, vẽ khung chính cho bản in
  const title = await page.evaluate(() => document.querySelector('.lesson-head h1').textContent.trim());
  await page.emulateMedia({ media: 'print' });
  const file = path.join(OUT, 'giao_trinh/pdf', `bai-${id}.pdf`);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  await page.pdf({
    path: file, format: 'A4', printBackground: true,
    margin: { top: '16mm', bottom: '18mm', left: '16mm', right: '16mm' },
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `<div style="width:100%;padding:0 16mm;font:9px Inter,Arial,sans-serif;color:#8a877f;display:flex;justify-content:space-between">
      <span>AI Canuc80k · Bài ${id} · ${title.replace(/</g, '&lt;')}</span><span><span class="pageNumber"></span>/<span class="totalPages"></span></span></div>`,
  });
  await ctx.close();
  return file;
}

async function slidePdf(browser, id) {
  const ctx = await browser.newContext({ viewport: { width: 1600, height: 900 }, colorScheme: 'light' });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/giao_trinh/slides/${id}.html#theme=light`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  await page.evaluate(() => window.Anim ? Anim.readyAll() : null);   // hình động: nạp sprite, vẽ khung chính cho bản in
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => document.querySelectorAll('.slide').forEach(fit));
  const file = path.join(OUT, 'giao_trinh/pdf', `slide-${id}.pdf`);
  await page.pdf({ path: file, width: '16in', height: '9in', printBackground: true, margin: { top: '0', right: '0', bottom: '0', left: '0' } });
  await ctx.close();
  return file;
}

(async () => {
  const ids = process.argv[2] === '--all' ? lessonIds() : process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: CHROME });
  for (const id of ids) {
    const a = await lessonPdf(browser, id), b = await slidePdf(browser, id);
    console.log(id, Math.round(fs.statSync(a).size / 1024) + 'KB', Math.round(fs.statSync(b).size / 1024) + 'KB');
  }
  await browser.close();
})();
