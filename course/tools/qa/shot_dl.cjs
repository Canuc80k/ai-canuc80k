// Chụp vùng nút tải ở desktop (mục lục) và màn hình hẹp (hàng nút đầu bài), cùng tab Slide.
const { chromium } = require('playwright-core'); const path = require('path');
const id = process.argv[2], out = path.resolve(process.argv[3]);
(async () => {
  const b = await chromium.launch({ executablePath: path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1200', 'chrome-win64', 'chrome.exe') });
  let p = await (await b.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
  await p.goto(`http://127.0.0.1:56872/START_HERE.html#/lesson/${id}`, { waitUntil: 'networkidle' });
  await (await p.$('.toc')).screenshot({ path: path.join(out, 'dl-desktop-toc.png') });
  await p.goto(`http://127.0.0.1:56872/START_HERE.html#/lesson/${id}?tab=slides`, { waitUntil: 'networkidle' });
  await p.screenshot({ path: path.join(out, 'dl-desktop-slides.png'), clip: { x: 0, y: 0, width: 1280, height: 330 } });
  p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage();
  await p.goto(`http://127.0.0.1:56872/START_HERE.html#/lesson/${id}`, { waitUntil: 'networkidle' });
  await p.screenshot({ path: path.join(out, 'dl-mobile.png') });
  await b.close();
})();
