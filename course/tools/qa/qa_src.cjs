// Chụp các câu có chân nguồn đề (chưa trả lời / đã trả lời) ở sáng, tối, mobile.
// node qa_src.cjs <id> <dir>
const { chromium } = require('playwright-core');
const path = require('path');
const id = process.argv[2], out = path.resolve(process.argv[3]);
const CHROME = path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1200', 'chrome-win64', 'chrome.exe');
(async () => {
  const b = await chromium.launch({ executablePath: CHROME });
  for (const [tag, theme, vp] of [['light', 'light', { width: 1280, height: 800 }], ['dark', 'dark', { width: 1280, height: 800 }], ['mobile', 'light', { width: 375, height: 812 }]]) {
    const p = await (await b.newContext({ viewport: vp, colorScheme: theme })).newPage();
    await p.goto(`http://127.0.0.1:56872/START_HERE.html#/lesson/${id}`, { waitUntil: 'networkidle' });
    await p.addStyleTag({ content: '.quiz-score{visibility:hidden}' });
    const qs = await p.$$('.quiz:has(.quiz-src)');
    for (let i = 0; i < qs.length; i++) {
      await qs[i].scrollIntoViewIfNeeded();
      await qs[i].screenshot({ path: path.join(out, `src-${tag}-${i + 1}-a.png`) });
      await (await qs[i].$('.quiz-opt[data-correct="1"]')).click();
      await p.waitForTimeout(100);
      await qs[i].screenshot({ path: path.join(out, `src-${tag}-${i + 1}-b.png`) });
    }
    console.log(tag, qs.length);
  }
  await b.close();
})();
