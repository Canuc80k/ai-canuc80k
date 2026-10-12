// Liệt kê phần tử làm trang tràn ngang ở một viewport hẹp.
const { chromium } = require('playwright-core'); const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1200', 'chrome-win64', 'chrome.exe') });
  const p = await (await b.newContext({ viewport: { width: Number(process.argv[3] || 375), height: 812 } })).newPage();
  await p.goto(`http://127.0.0.1:56872/START_HERE.html#/lesson/${process.argv[2]}`, { waitUntil: 'networkidle' });
  console.log(JSON.stringify(await p.evaluate(() => {
    const W = document.documentElement.clientWidth, out = [];
    for (const e of document.querySelectorAll('body *')) {
      const r = e.getBoundingClientRect();
      if (r.right > W + 1 && !e.closest('pre, .katex-display, .table-wrap, .tasks, .parts, .code-body, .tabs') && r.width > 0)
        out.push([e.tagName, e.className, Math.round(r.right), (e.textContent || '').trim().slice(0, 60)]);
    }
    return {W, scroll: document.documentElement.scrollWidth, items: out.slice(-8)};
  }), null, 1));
  await b.close();
})();
