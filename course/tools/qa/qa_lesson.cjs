// QA một bài: trang bài học (sáng/tối, desktop/mobile) và từng slide.
// node qa_lesson.cjs 2.2 <thư-mục-ảnh>
// Cần preview đang chạy ở 127.0.0.1:56872 (build/serve.py).
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const id = process.argv[2];
const outDir = path.resolve(process.argv[3]);
const BASE = 'http://127.0.0.1:56872';
const CHROME = path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1200', 'chrome-win64', 'chrome.exe');

async function lessonPage(browser, theme, viewport, tag, report) {
  const ctx = await browser.newContext({ viewport, colorScheme: theme, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(`${BASE}/START_HERE.html#/lesson/${id}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(600);
  const info = await page.evaluate(() => ({
    quizzes: document.querySelectorAll('.quiz').length,
    sources: [...document.querySelectorAll('.quiz-src')].map(p => p.textContent.trim()),
    katexErrors: document.querySelectorAll('.katex-error').length,
    overflowX: document.documentElement.scrollWidth > innerWidth + 1,
    // phần tử nhìn thấy được tràn ra ngoài khung bài (bỏ qua vùng tự cuộn ngang như code, công thức, bảng)
    wide: [...document.querySelectorAll('.theory p, .theory li, .quiz, figure, .callout')]
      .filter(e => e.getBoundingClientRect().right > innerWidth + 1).length,
  }));
  // Thanh điểm sticky đè lên ảnh chụp từng câu; ẩn riêng trong lúc chụp (chỉ QA).
  await page.addStyleTag({ content: '.quiz-score{visibility:hidden}' });
  const quizzes = await page.$$('.quiz');
  for (let i = 0; i < quizzes.length; i++) {
    await quizzes[i].scrollIntoViewIfNeeded();
    await quizzes[i].screenshot({ path: path.join(outDir, `${tag}-quiz${String(i + 1).padStart(2, '0')}.png`) });
  }
  // bấm đáp án đúng của câu đầu và câu có ghi nguồn đề thi để xem giải thích + chân nguồn
  for (const sel of ['.quiz', '.quiz:has(.quiz-src-exam)']) {
    const q = await page.$(sel);
    if (!q) continue;
    await (await q.$('.quiz-opt[data-correct="1"]')).click();
    await page.waitForTimeout(150);
    await q.screenshot({ path: path.join(outDir, `${tag}-answered-${sel === '.quiz' ? 'first' : 'exam'}.png`) });
  }
  const figs = await page.$$('figure.fig');
  for (let i = 0; i < figs.length; i++) {
    await figs[i].scrollIntoViewIfNeeded();
    await figs[i].screenshot({ path: path.join(outDir, `${tag}-fig${i + 1}.png`) });
  }
  report[tag] = { ...info, consoleErrors: errors };
  await ctx.close();
}

async function slides(browser, theme, viewport, tag, report) {
  const ctx = await browser.newContext({ viewport, colorScheme: theme, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(`${BASE}/giao_trinh/slides/${id}.html#theme=${theme}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(600);
  const n = await page.evaluate(() => s.length);
  const fits = [];
  for (let i = 0; i < n; i++) {
    const r = await page.evaluate(i => { n = i; show(); const el = s[i];
      return { slide: i + 1, fs: el.style.getPropertyValue('--fs') || '1', overflow: over(el),
               katexErrors: el.querySelectorAll('.katex-error').length,
               wide: (() => { const b = el.getBoundingClientRect(); let w = 0;
                 for (const c of el.querySelectorAll('*')) { if (c.closest('.katex-mathml') || (c.closest('svg') && c.tagName.toLowerCase() !== 'svg')) continue; const r = c.getBoundingClientRect();
                   if (r.width && (r.right > b.right + 1 || r.left < b.left - 1)) w++; }
                 return w; })() }; }, i);
    fits.push(r);
    await page.screenshot({ path: path.join(outDir, `${tag}-s${String(i + 1).padStart(2, '0')}.png`) });
  }
  report[tag] = { slides: n, shrunk: fits.filter(f => f.fs !== '1'), overflow: fits.filter(f => f.overflow), wide: fits.filter(f => f.wide),
                  katexErrors: fits.reduce((a, f) => a + f.katexErrors, 0), pageErrors: errors };
  await ctx.close();
}

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ executablePath: CHROME });
  const report = {};
  for (const theme of ['light', 'dark']) {
    await lessonPage(browser, theme, { width: 1280, height: 800 }, `lesson-${theme}`, report);
    await slides(browser, theme, { width: 1600, height: 900 }, `slides-${theme}-1600`, report);
  }
  await lessonPage(browser, 'light', { width: 375, height: 812 }, 'lesson-mobile', report);
  await slides(browser, 'light', { width: 1280, height: 800 }, 'slides-light-1280', report);
  await browser.close();
  fs.writeFileSync(path.join(outDir, 'qa-report.json'), JSON.stringify(report, null, 1));
  console.log(JSON.stringify(report, (k, v) => (k === 'sources' ? v.length : v), 1));
})();
