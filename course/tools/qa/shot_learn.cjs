// Kiểm dòng "Ôn lại" của mục Trắc nghiệm trên website đang chạy: hiện sau khi trả lời; bấm vào thì mở bài ở tab mới,
// trang làm bài giữ nguyên; tab bài cuộn tới đúng mục và tô đúng câu cần đọc. Kiểm cả trang xem lại bài kiểm tra.
// Chụp nền sáng, nền tối và điện thoại.
// node shot_learn.cjs [--base=http://127.0.0.1:56872] [bộ:vị trí ...]   (mặc định light:9 light2:69 medium:0 max:72)
// node shot_learn.cjs --all     mở thẳng mọi link của mọi bộ (cùng một tab), kiểm từng câu cần đọc được tô đủ
// Ảnh ghi vào 04. Workspace/quiz-learn-20261012/shots/; in lỗi console và chỗ lệch.
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const BASE = (args.find(a => a.startsWith('--base=')) || '--base=http://127.0.0.1:56872').slice(7);
const ALL = args.includes('--all');
const picks = args.filter(a => !a.startsWith('--'));
const CASES = (picks.length ? picks : ['light:9', 'light2:69', 'medium:0', 'max:72']).map(s => s.split(':'));
const OUT = path.resolve(__dirname, '../../../../04. Workspace/quiz-learn-20261012/shots');
const CHROME = path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1200', 'chrome-win64', 'chrome.exe');
const VIEWS = [['light', { width: 1100, height: 900 }], ['dark', { width: 1100, height: 900 }], ['mobile', { width: 390, height: 844 }]];

// Trong tab bài: tiêu đề mục đích, các câu cần đọc của link, phần đã tô (chữ như app.js learnText, công thức là $TeX$).
function inspect() {
  const p = new URLSearchParams(location.hash.split('?')[1]);
  const k = Number(p.get('sec')), lid = location.hash.split('?')[0].split('/')[2];
  const h = document.getElementById('sec-' + k);
  const q = window.QUIZ_BANK.sets.flatMap(s => s.questions).find(x => x.id === p.get('q'));
  const link = q && (q.learn || []).find(x => x[0] === lid && x[1] === k);
  const text = el => {
    let t = '';
    (function go(n) {
      for (const c of n.childNodes) {
        if (c.nodeType === 3) t += c.data;
        else if (c.nodeType === 1 && c.classList.contains('katex')) t += `$${c.querySelector('annotation')?.textContent || ''}$`;
        else if (c.nodeType === 1) go(c);
      }
    })(el);
    return t;
  };
  const marks = [...document.querySelectorAll('.learn-mark')];
  const tex = k => `$${k.querySelector('annotation')?.textContent || ''}$`;
  const marked = marks.map(m => m.classList.contains('katex-display') ? tex(m.querySelector('.katex'))
    : m.classList.contains('katex') ? tex(m) : text(m)).join('').replace(/\s+/g, '');
  const quotes = (link && link[3]) || [];
  const top = marks.length ? Math.round(marks[0].getBoundingClientRect().top) : null;
  return {
    head: h ? h.textContent : null, want: link ? link[2] : null, headTop: h ? Math.round(h.getBoundingClientRect().top) : null,
    quotes: quotes.length, found: quotes.filter(x => marked.includes(x.replace(/\s+/g, ''))).length, marks: marks.length,
    on: marks.filter(m => m.classList.contains('is-on')).length, top, vh: innerHeight,
    bg: marks.length ? getComputedStyle(marks[0]).backgroundColor : null
  };
}
const okSpot = r => r && r.head && r.want && r.head.replace(/\$/g, '').endsWith(r.want) && r.quotes > 0 && r.found === r.quotes && r.on === r.marks
  && r.top > 40 && r.top < r.vh * 0.85;

async function checkAll(browser) {
  const page = await browser.newPage({ viewport: { width: 1100, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`${BASE}/START_HERE.html#/quiz`, { waitUntil: 'networkidle' });
  const links = await page.evaluate(() => window.QUIZ_BANK.sets.flatMap(s => s.questions.flatMap(q => (q.learn || []).map(l => [q.id, l[0], l[1]]))));
  let bad = 0;
  for (const [qid, lid, k] of links) {
    await page.evaluate(h => { location.hash = h; }, `#/lesson/${lid}?sec=${k}&q=${qid}`);
    await page.waitForFunction(() => document.querySelector('.learn-mark.is-on') || document.querySelector('.t-sec.is-target'), null, { timeout: 5000 }).catch(() => {});
    const r = await page.evaluate(inspect);
    if (!okSpot(r)) { bad++; console.log(`LỖI ${qid} → ${lid}?sec=${k}: ${JSON.stringify(r)}`); }
  }
  console.log(`${links.length} link, ${bad} lỗi${errors.length ? `, lỗi console: ${errors.slice(0, 3)}` : ''}`);
  return bad + errors.length;
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: CHROME });
  let problems = 0;
  if (ALL) { problems = await checkAll(browser); await browser.close(); console.log(problems ? `${problems} vấn đề` : 'PASS'); process.exit(problems ? 1 : 0); }
  for (const [name, viewport] of VIEWS) {
    const ctx = await browser.newContext({ viewport, colorScheme: name === 'dark' ? 'dark' : 'light', deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const errors = [];
    const watch = p => {
      p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
      p.on('pageerror', e => errors.push(String(e)));
      p.on('dialog', d => d.accept());
    };
    watch(page);
    ctx.on('page', watch);
    for (const [set, index] of CASES) {
      await page.goto(`${BASE}/START_HERE.html#/quiz/${set}/play`, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      await page.click(`[data-action="qz-jump"][data-index="${index}"]`);
      const hidden = await page.$eval('#qz-why', el => el.hidden);
      await page.click('[data-action="qz-answer"][data-choice="0"]');
      const links = await page.$$eval('.quiz-learn a', as => as.map(a => [a.getAttribute('href'), a.textContent, a.target]));
      const card = await page.$('.qz-card');
      await card.screenshot({ path: path.join(OUT, `${name}-${set}-${index}.png`) });
      if (!hidden || !links.length) { problems++; console.log(`LỖI ${name} ${set}:${index}: lời giải ${hidden ? 'ẩn' : 'không ẩn'} trước khi trả lời, ${links.length} link`); }
      const before = await page.evaluate(() => location.hash);
      for (let i = 0; i < links.length; i++) {
        const [tab] = await Promise.all([ctx.waitForEvent('page'), page.click(`.quiz-learn a >> nth=${i}`)]);
        await tab.waitForLoadState('networkidle');
        await tab.evaluate(() => document.fonts.ready);
        await tab.waitForTimeout(2200);
        const r = await tab.evaluate(inspect);
        if (links[i][2] !== '_blank' || !okSpot(r)) { problems++; console.log(`LỖI ${name} ${set}:${index} → ${links[i][0]}: ${JSON.stringify(r)}`); }
        await tab.screenshot({ path: path.join(OUT, `${name}-${set}-${index}-sec${i + 1}.png`) });
        await tab.close();
      }
      if (await page.evaluate(() => location.hash) !== before) { problems++; console.log(`LỖI ${name} ${set}:${index}: trang làm bài bị đổi`); }
      console.log(`${name} ${set}:${index}: ${links.map(l => l[1]).join(' | ')}`);
    }
    // trang xem lại bài kiểm tra: mọi câu có nối đều hiện dòng Ôn lại
    await page.goto(`${BASE}/START_HERE.html#/quiz/max`, { waitUntil: 'networkidle' });
    await page.click('[data-action="ex-start"]');
    await page.click('[data-action="ex-submit"]');
    await page.waitForTimeout(400);
    const ex = await page.$$eval('.ex-review', cs => [cs.length, cs.filter(c => c.querySelector('.quiz-learn')).length]);
    const first = await page.$('.ex-review .quiz-learn');
    if (first) { await first.scrollIntoViewIfNeeded(); await (await first.evaluateHandle(e => e.closest('.ex-review'))).screenshot({ path: path.join(OUT, `${name}-exam.png`) }); }
    console.log(`${name} xem lại kiểm tra: ${ex[1]}/${ex[0]} câu có Ôn lại`);
    if (errors.length) { problems += errors.length; console.log(`LỖI console ${name}:`, errors.slice(0, 5)); }
    await ctx.close();
  }
  await browser.close();
  console.log(problems ? `${problems} vấn đề` : 'PASS');
  process.exit(problems ? 1 : 0);
})();
