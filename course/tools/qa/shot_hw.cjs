// Chụp tab Bài tập của một bài và trang Bài tập tổng (desktop + mobile).
const { chromium } = require('playwright-core'); const path = require('path');
const id = process.argv[2], out = path.resolve(process.argv[3]), tag = process.argv[4] || 'hw';
(async () => {
  const b = await chromium.launch({ executablePath: path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1200', 'chrome-win64', 'chrome.exe') });
  for (const [name, vp, scheme] of [['desktop', { width: 1280, height: 800 }, 'light'], ['mobile', { width: 390, height: 844 }, 'light'], ['dark', { width: 1280, height: 800 }, 'dark']]) {
    const p = await (await b.newContext({ viewport: vp, colorScheme: scheme })).newPage();
    await p.goto(`http://127.0.0.1:56872/START_HERE.html#/lesson/${id}?tab=homework&task=1`, { waitUntil: 'networkidle' });
    await p.screenshot({ path: path.join(out, `${tag}-${name}-task.png`), fullPage: true });
    if (name !== 'dark') {
      await p.goto('http://127.0.0.1:56872/START_HERE.html#/exercises', { waitUntil: 'networkidle' });
      await p.screenshot({ path: path.join(out, `${tag}-${name}-index.png`), fullPage: false });
    }
  }
  await b.close();
})();
