(() => {
  'use strict';

  const D = window.COURSE_DATA;
  const {$, $$, esc, words, icon, a, meter, pager, loadScript, highlightPy: highlight, compactJSON, looksJSON, looksPython, wrapTables} = window.Kit;

  const lessonHref = (id, tab = 'learn', task = 1, part = 0) => {
    const q = [];
    if (part) q.push(`part=${part}`);
    if (tab !== 'learn') q.push(`tab=${tab}`);
    if (tab === 'homework') q.push(`task=${task}`);
    return `#/lesson/${id}${q.length ? '?' + q.join('&') : ''}`;
  };
  const findLesson = id => D.lessons.find(l => l.id === id);
  const phaseLessons = id => D.lessons.filter(l => l.phase === Number(id));
  const kindLabel = kind => kind === 'standard_json' ? 'Lập trình' : 'Dữ liệu';
  const isCheck = l => l.kind === 'checkpoint';
  const T = window.THEORY || {lessons: {}, phases: {}};
  const theoryOf = l => T.lessons[l.id];
  const CE = window.CODE_EXAMPLES || {lessons: {}};
  const codeExamplesOf = l => CE.lessons?.[l.id];
  const LINKS = window.LESSON_LINKS || {};

  // ---------- nạp dữ liệu theo nhu cầu ----------
  // Trang chủ chỉ cần ui/data/index.js (mục lục). Nội dung một bài (ui/data/l/<id>.js) và kho trắc nghiệm
  // (ui/quiz-bank.js) được nạp khi cần. Khi chạy với bản đầy đủ (theory.js…), mọi thứ đã có sẵn.
  const lessonReady = id => { const t = T.lessons[id]; return !t || !t.lazy; };
  window.__lessonChunk = c => {
    if (c.theory) T.lessons[c.id] = c.theory;
    const l = findLesson(c.id);
    if (l && c.lesson) Object.assign(l, c.lesson);
    if (c.examples) CE.lessons[c.id] = c.examples;
    else if (CE.lessons[c.id]?.lazy) delete CE.lessons[c.id];
  };
  const ensureLesson = id => lessonReady(id) ? Promise.resolve() : loadScript(`ui/data/l/${id}.js`);
  const quizReady = () => !!window.QUIZ_BANK;
  const ensureQuiz = () => quizReady() ? Promise.resolve() : loadScript('ui/quiz-bank.js').then(() => initQuiz());
  const hasWork = l => l.parts.length > 0;
  // Bài tập: ưu tiên bộ soạn mới (l.homework, dựng từ content/phase-N/homework/<id>/), nếu chưa có thì dùng bài tập cũ trong parts.
  const homeworkOf = (l, m) => l.homework?.length ? {tasks: l.homework, fresh: true} : m?.homework?.length ? {tasks: m.homework, folder: m.folder, fresh: false} : null;
  const hasHomework = l => !!(l.homework?.length || l.parts.some(m => m.homework.length));
  const ready = l => hasWork(l) || !!theoryOf(l);
  const idLabel = l => isCheck(l) ? '' : l.id;
  const nameLabel = l => isCheck(l) ? 'Kiểm tra' : `Bài ${l.id}`;
  const LESSONS = D.lessons.filter(l => !isCheck(l));
  const INTERNAL = 'Tham khảo';  // ghi chú nguồn nội bộ của bài cũ, không hiển thị

  // ---------- state: khung trang, thanh bên, tìm kiếm, sự kiện chung nằm trong ui/kit.js ----------
  const K = window.Kit.create({
    key: 'aicanuc80k.portal.v2', sub: 'AI', search: 'Tìm bài học', navLabel: 'Các chương',
    copyFail: 'Không sao chép được, hãy tải tệp về', findLesson, nameLabel
  });
  const {S, route, toast, render, chrome, spy, persist} = K;
  const doneIn = phase => phaseLessons(phase).filter(l => !isCheck(l) && S.done.has(l.id)).length;
  const haystack = new Map();
  const matches = l => {
    const q = words(S.q);
    if (!q.length) return true;
    if (!haystack.has(l.id)) haystack.set(l.id, ' ' + words([l.id, l.title, l.summary, D.phases[l.phase].title, ...(theoryOf(l)?.headings || []), ...l.parts.flatMap(m => [m.title, ...m.homework.map(h => h.title)])].join(' ')).join(' '));
    const text = haystack.get(l.id);
    return q.every(w => text.includes(w));
  };
  Object.assign(K.hooks, {
    nav: [
      ['home', 'route', 'Lộ trình', '#/'],
      ['quiz', 'quiz', 'Trắc nghiệm', '#/quiz'],
      ['practice', 'practice', 'Thực hành', '#/practice'],
      ['contests', 'trophy', 'Các cuộc thi', '#/contests'],
      ['resources', 'book', 'Tài liệu', '#/resources']
    ],
    section: r => ['home', 'phase', 'lesson'].includes(r.type) ? 'home' : r.type === 'resource' ? 'resources' : r.type,
    tree(r) {
      const lesson = r.type === 'lesson' ? findLesson(r.id) : null;
      return {
        phase: lesson ? lesson.phase : r.type === 'phase' ? Number(r.id) : null,
        lesson: lesson ? lesson.id : null,
        sections: D.courses.map(k => ({label: `Khóa ${k.id.slice(1)}`, title: k.title, phases: k.phases.map(id => D.phases[id]).map(p => ({
          id: p.id, short: p.short,
          items: phaseLessons(p.id).map(l => ({href: lessonHref(l.id), id: l.id, label: idLabel(l), title: l.title, done: S.done.has(l.id), draft: !ready(l)}))
        }))}))
      };
    },
    crumbs(r) {
      const lesson = r.type === 'lesson' ? findLesson(r.id) : null;
      const activePhase = lesson ? lesson.phase : r.type === 'phase' ? Number(r.id) : null;
      const crumbs = [a('#/', 'Lộ trình', 'data-nav')];
      if (activePhase !== null && D.phases[activePhase]) crumbs.push(a(`#/phase/${activePhase}`, `Chương ${activePhase}`, 'data-nav'));
      if (lesson) crumbs.push(`<span aria-current="page">${nameLabel(lesson)}</span>`);
      if (r.type === 'resources') crumbs.splice(0, 1, '<span aria-current="page">Tài liệu</span>');
      if (r.type === 'resource') crumbs.splice(0, 1, a('#/resources', 'Tài liệu', 'data-nav'), `<span aria-current="page">${esc((D.resources.find(x => x.id === r.id) || {}).title || '')}</span>`);
      if (r.type === 'quiz') crumbs.splice(0, crumbs.length, ...quizCrumbs(r));
      if (r.type === 'exam') crumbs.splice(0, crumbs.length, a('#/quiz', 'Trắc nghiệm', 'data-nav'), ...(exSet() ? [a(`#/quiz/${exSet().id}`, esc(exSet().title), 'data-nav'), '<span aria-current="page">Kiểm tra</span>'] : []));
      if (r.type === 'practice') crumbs.splice(0, crumbs.length, ...practiceCrumbs(r));
      if (r.type === 'contests') crumbs.splice(0, crumbs.length, ...(r.id && CT.contests.some(c => c.id === r.id)
        ? [a('#/contests', 'Các cuộc thi', 'data-nav'), `<span aria-current="page">${esc(CT.contests.find(c => c.id === r.id).short)}</span>`]
        : ['<span aria-current="page">Các cuộc thi</span>']));
      return crumbs;
    },
    progress: () => ({html: S.done.size ? `${S.done.size}<span>/${LESSONS.length}</span>` : '', title: `${S.done.size}/${LESSONS.length} bài đã học`})
  });

  // ---------- shared pieces ----------
  function footer() {
    return `<footer class="foot"><span>AI Canuc80k</span><nav>${a('#/resource/guide', 'Hướng dẫn', 'data-nav')}${a('#/resource/framework', 'Khung giáo trình', 'data-nav')}</nav></footer>`;
  }
  function empty() {
    return `<div class="empty"><p>Không có bài học nào khớp với “${esc(S.q.trim())}”.</p><button class="btn" data-action="clear-search">Xóa tìm kiếm</button></div>`;
  }
  function lessonRow(l) {
    const done = S.done.has(l.id);
    return a(lessonHref(l.id),
      `<span class="row-id">${idLabel(l)}</span>
       <span class="row-body"><span class="row-title">${esc(l.title)}</span></span>
       <span class="row-end">${done ? `<span class="row-done" title="Đã học">${icon('check')}</span>` : ''}${icon('arrow')}</span>`,
      `class="row${done ? ' is-done' : ''}${ready(l) ? '' : ' is-draft'}" data-nav`);
  }

  // ---------- pages ----------
  function renderHome() {
    if (S.q.trim()) {
      const hits = D.lessons.filter(matches);
      return `<div class="page">
        <header class="page-head"><h1>Kết quả tìm kiếm</h1><p class="lead">${hits.length} bài học khớp với “${esc(S.q.trim())}”.</p></header>
        <div class="rows">${hits.map(lessonRow).join('') || empty()}</div>${footer()}</div>`;
    }
    const phaseRow = p => {
      const n = doneIn(p.id);
      return a(`#/phase/${p.id}`,
        `<span class="phase-num">${p.id}</span><span class="phase-title">${esc(p.title)}</span>${n ? `<span class="phase-progress">${meter(n, p.count)}</span>` : ''}${icon('arrow')}`,
        'class="phase" data-nav');
    };
    const courses = D.courses.map(k => `<section class="course">
        <h2 class="course-head">Khóa ${k.id.slice(1)} · ${esc(k.title)}</h2>
        <div class="phases">${k.phases.map(id => phaseRow(D.phases[id])).join('')}</div>
      </section>`).join('');
    return `<div class="page page-home">
      <h1 class="home-title">AI Canuc80k</h1>
      <div class="courses" id="roadmap">${courses}</div>
      ${footer()}</div>`;
  }

  function renderPhase(id) {
    const p = D.phases[Number(id)];
    if (!p) return notFound();
    const lessons = phaseLessons(p.id).filter(matches);
    const n = doneIn(p.id);
    return `<div class="page">
      <header class="page-head">
        <p class="kicker">Chương ${p.id}</p>
        <h1>${esc(p.title)}</h1>
        ${n ? `<p class="page-meta"><span>${n}/${p.count} đã học</span>${meter(n, p.count)}</p>` : ''}
      </header>
      <div class="rows">${lessons.map(lessonRow).join('') || empty()}</div>
      ${pagerPhase(p)}${footer()}</div>`;
  }
  function pagerPhase(p) {
    const prev = D.phases[p.id - 1], next = D.phases[p.id + 1];
    return pager('Chương liền kề', prev && {href: `#/phase/${prev.id}`, label: `Chương ${prev.id}`, title: prev.title}, next && {href: `#/phase/${next.id}`, label: `Chương ${next.id}`, title: next.title});
  }

  function codeBlock(code, filename, l, kind = 'main', index = 0) {
    return `<figure class="code">
      <figcaption class="code-head"><span class="code-name">${esc(filename)}</span>
        <span class="code-tools">
          <button class="tool" data-action="copy" data-kind="${kind}" data-index="${index}" title="Sao chép" aria-label="Sao chép">${icon('copy')}</button>
          <button class="tool" data-action="wrap" title="Ngắt dòng" aria-label="Ngắt dòng" aria-pressed="${S.wrap}">${icon('wrap')}</button>
          ${a(`${l.folder}/${filename}`, icon('download'), 'class="tool" download title="Tải về" aria-label="Tải về"')}
        </span>
      </figcaption>
      <pre class="code-body${S.wrap ? ' is-wrap' : ''}"><code>${highlight(code)}</code></pre>
    </figure>`;
  }
  function textDoc(text) {
    const lines = text.split(/\r?\n/);
    let html = '', para = [];
    const flush = () => { if (para.length) { html += `<p>${esc(para.join('\n'))}</p>`; para = []; } };
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i], t = line.trim();
      if (!t) { flush(); continue; }
      if (t.startsWith('{') || t.startsWith('[')) {
        let json = t, end = i;
        const limit = Math.min(lines.length, i + 300);
        while (end < limit) { try { JSON.parse(json); break; } catch (_) { end++; if (end < lines.length) json += '\n' + lines[end]; } }
        if (end < limit) { flush(); html += `<pre>${esc(compactJSON(json))}</pre>`; i = end; continue; }
      }
      if (t.length < 90 && /[A-ZÀ-Ỹ]/u.test(t) && t === t.toLocaleUpperCase('vi') && !/^https?:/.test(t)) { flush(); html += `<h3 class="label">${esc(t)}</h3>`; continue; }
      if (/^\s*[-•]\s+/.test(line) && !para.length) {
        const items = [];
        while (i < lines.length && /^\s*[-•]\s+/.test(lines[i])) { items.push(lines[i].replace(/^\s*[-•]\s+/, '')); i++; }
        i--; html += `<ul>${items.map(x => `<li>${esc(x)}</li>`).join('')}</ul>`; continue;
      }
      para.push(line);
    }
    flush();
    return html;
  }
  function statement(text) {
    // The title and local code are shown in the page header; skip them in the body.
    const lines = text.split(/\r?\n/);
    let start = 0;
    if (/^BTVN\s*\d/i.test(lines[0] || '')) start = 1;
    if (/^Mã local:/i.test((lines[start] || '').trim())) start++;
    return textDoc(lines.slice(start).join('\n'));
  }
  const LEGACY_LABEL = {'YÊU CẦU': 'Yêu cầu', 'INPUT': 'Input', 'OUTPUT': 'Output', 'GIẢI THÍCH VÍ DỤ': 'Giải thích ví dụ',
    'CẦN NỘP': 'Cần nộp', 'TỰ KIỂM TRA': 'Tự kiểm tra', 'VÍ DỤ INPUT': 'Input mẫu', 'VÍ DỤ OUTPUT': 'Output mẫu'};
  const ioBox = (label, pre) => `<div><p class="hw-io-label">${label}</p>${pre}</div>`;
  function legacyStatement(text) {
    // Bài tập cũ là văn bản thuần: ghép input/output mẫu thành hai cột, đổi nhãn in hoa thành tiêu đề, danh sách tự kiểm thành checklist.
    return statement(text)
      .replace(/<h3 class="label">VÍ DỤ INPUT<\/h3>(<pre>[\s\S]*?<\/pre>)<h3 class="label">VÍ DỤ OUTPUT<\/h3>(<pre>[\s\S]*?<\/pre>)/,
        (_, i, o) => `<div class="hw-io">${ioBox('Input mẫu', i)}${ioBox('Output mẫu', o)}</div>`)
      .replace(/<h3 class="label">TỰ KIỂM TRA<\/h3><ul>/, '<h3>Tự kiểm tra</h3><ul class="hw-check">')
      .replace(/<h3 class="label">([^<]+)<\/h3>/g, (_, t) => `<h3>${LEGACY_LABEL[t] || t.charAt(0) + t.slice(1).toLocaleLowerCase('vi')}</h3>`);
  }
  function homeworkView(l, hw, task, pi) {
    const h = hw.tasks[task - 1], n = hw.tasks.length;
    const cards = hw.fresh
      ? hw.tasks.map((x, i) => a(lessonHref(l.id, 'homework', i + 1, pi),
        `<span class="hw-tab-num">${i + 1}</span><span class="hw-tab-name">${esc(x.title)}</span>`,
        `class="hw-tab${i + 1 === task ? ' is-active' : ''}" role="tab" aria-selected="${i + 1 === task}"`)).join('')
      : hw.tasks.map((x, i) => a(lessonHref(l.id, 'homework', i + 1, pi),
        `<span class="task-num">Bài ${i + 1}</span><span class="task-name">${esc(x.title)}</span>`,
        `class="task${i + 1 === task ? ' is-active' : ''}" role="tab" aria-selected="${i + 1 === task}"`)).join('');
    const files = hw.fresh ? (h.files || []) : [
      {label: 'Đề bài', path: `${hw.folder}/${h.file}`}, {label: 'Code khởi đầu', path: `${hw.folder}/${h.starterFile}`},
      ...(h.sample ? [{label: 'Input mẫu', path: `${hw.folder}/${h.sample}`}] : []),
      ...(h.sampleOut ? [{label: 'Output mẫu', path: `${hw.folder}/${h.sampleOut}`}] : [])];
    const doc = hw.fresh ? `<div class="prose theory hw-doc">${h.html}</div>` : `<div class="doc hw-doc hw-legacy">${legacyStatement(h.text)}</div>`;
    const starter = h.starter ? `<section class="block"><h2 class="block-title">Code khởi đầu</h2>${codeBlock(h.starter, h.starterFile, {folder: hw.fresh ? h.folder : hw.folder}, 'starter', task - 1)}</section>` : '';
    const fileLinks = files.length ? `<div class="hw-files">${files.map(f => a(f.path, `${icon('download')}${esc(f.label)}`, 'class="btn" download')).join('')}</div>` : '';
    const head = hw.fresh
      ? `<header class="hw-head hw-head-row"><h2 class="hw-title">${esc(h.title)}</h2>${fileLinks}</header>`
      : `<header class="hw-head"><p class="hw-kicker">Bài tập ${task}${n > 1 ? ` / ${n}` : ''}</p><h2 class="hw-title">${esc(h.title)}</h2>${fileLinks}</header>`;
    return `${n > 1 ? `<div class="${hw.fresh ? 'hw-tabs' : 'tasks'}" role="tablist" aria-label="Chọn bài tập">${cards}</div>` : ''}
      <article class="hw${hw.fresh ? ' hw-fresh' : ''}">
        ${head}
        ${doc}
        ${starter}
      </article>`;
  }
  function lessonPager(l) {
    const i = D.lessons.indexOf(l), prev = D.lessons[i - 1], next = D.lessons[i + 1];
    return pager('Bài học liền kề', prev && {href: lessonHref(prev.id), label: nameLabel(prev), title: prev.title}, next && {href: lessonHref(next.id), label: nameLabel(next), title: next.title});
  }

  const practiceTask = code => { for (const t of PB.tiers) { const x = t.tasks.find(y => y.code === code); if (x) return {...x, tier: t}; } return null; };
  function renderLesson(r) {
    const l = findLesson(r.id);
    if (!l) return notFound();
    const p = D.phases[l.phase];
    const pi = Math.min(Math.max(Number(r.params.get('part') || 0), 0), Math.max(l.parts.length - 1, 0));
    const m = l.parts[pi];
    const th = theoryOf(l);
    const ce = codeExamplesOf(l);
    const lk = LINKS[l.id] || {};
    if (m || th) { S.last = l.id; persist(); }
    const tabList = [['learn', 'Bài học'], ...(m || l.deck ? [['slides', 'Slide']] : []), ...(m || l.code || ce ? [['code', 'Code mẫu']] : []), ...(homeworkOf(l, m) ? [['homework', 'Bài tập']] : [])];
    const tab = tabList.some(([k]) => k === r.params.get('tab')) ? r.params.get('tab') : 'learn';
    const ownDeck = tab === 'slides' && l.deck;
    const ownCode = tab === 'code' && l.code;
    const ownExamples = tab === 'code' && ce;
    const hw = homeworkOf(l, m);
    let task = Number(r.params.get('task') || 1);
    if (!hw || !(task >= 1 && task <= hw.tasks.length)) task = 1;
    const done = S.done.has(l.id);
    let body = '';
    if (m || th) {

    if (tab === 'learn') {
      const doc = th || m;
      body = `<div class="learn">
        <article class="prose${th ? ' theory' : ''}" id="lesson-doc">${doc.html}</article>
        <aside class="toc" aria-label="Mục lục bài">${doc.headings.filter(h => h !== INTERNAL).map((h, i) => `<a href="#sec-${i}" data-scroll="sec-${i}">${esc(h)}</a>`).join('')}</aside>
      </div>`;
    }
    if (ownDeck) {
      body = `<div class="actions">
          <button class="btn" data-action="fullscreen">${icon('expand')}Toàn màn hình</button>
          ${a(l.deck, `${icon('external')}Mở tab mới`, 'class="btn" target="_blank" rel="noopener"')}
          ${l.deckPdf ? a(l.deckPdf, `${icon('download')}PDF slide`, 'class="btn" download') : ''}
        </div>
        <div class="stage"><iframe id="slide-frame" src="${l.deck}${S.theme ? `#theme=${S.theme}` : ''}" title="Slide ${esc(l.title)}" allowfullscreen></iframe></div>`;
    } else if (tab === 'slides') {
      body = `<div class="actions">
          <button class="btn" data-action="fullscreen">${icon('expand')}Toàn màn hình</button>
          ${a(`${m.folder}/slides.html`, `${icon('external')}Mở tab mới`, 'class="btn" target="_blank" rel="noopener"')}
          ${a(`${m.folder}/slides.pptx`, `${icon('download')}PowerPoint`, 'class="btn" download')}
        </div>
        <div class="stage"><iframe id="slide-frame" src="${m.folder}/slides.html${S.theme ? `#theme=${S.theme}` : ''}" title="Slide ${esc(m.title)}" allowfullscreen></iframe></div>`;
    }
    if (ownExamples) {
      body = `<div class="actions">
          ${lk.kaggle ? a(lk.kaggle, `${icon('external')}Chạy trên Kaggle`, 'class="btn" target="_blank" rel="noopener"') : ''}
          ${ce.notebook ? a(ce.notebook, `${icon('download')}Notebook ví dụ`, 'class="btn" download') : ''}
          ${ce.codeFile ? a(ce.codeFile, `${icon('download')}Code mẫu .py`, 'class="btn" download') : ''}
        </div>
        <div class="learn">
          <article class="prose theory code-examples" id="lesson-doc">${ce.html}</article>
          <aside class="toc" aria-label="Mục lục code mẫu">${(ce.headings || []).filter(h => h !== INTERNAL).map((h, i) => `<a href="#sec-${i}" data-scroll="sec-${i}">${esc(h)}</a>`).join('')}</aside>
        </div>`;
    } else if (ownCode) {
      const fname = l.codeFile.split('/').pop();
      body = `<div class="actions">
          ${l.notebook ? a(l.notebook, `${icon('download')}Notebook`, 'class="btn" download') : ''}
        </div>
        ${codeBlock(l.code, fname, {folder: l.codeFile.slice(0, -fname.length - 1)}, 'lesson')}
        <section class="output"><h2 class="output-title">Kết quả</h2><pre>${esc(l.codeOutput)}</pre></section>`;
    } else if (tab === 'code') {
      body = `<div class="actions">
          ${a(`${m.folder}/code_minh_hoa.ipynb`, `${icon('download')}Notebook`, 'class="btn" download')}
        </div>
        ${codeBlock(m.code, 'code_minh_hoa.py', m)}
        <section class="output"><h2 class="output-title">Kết quả</h2><pre>${esc(m.output)}</pre></section>
        ${m.extra.length ? `<section class="block"><h2 class="block-title">Code bổ sung</h2>
          ${m.extraGuide ? `<details class="disclosure"><summary>Môi trường và checkpoint</summary><div class="doc">${textDoc(m.extraGuide)}</div></details>` : ''}
          ${m.extra.map((e, i) => codeBlock(e.code, e.filename, m, 'extra', i)).join('')}</section>` : ''}`;
    }
    if (tab === 'homework' && hw) body = homeworkView(l, hw, task, pi);

    }

    const tabs = (tabList.length > 1 ? tabList : [])
      .map(([key, label]) => a(lessonHref(l.id, key, task, pi), label, `class="tab${tab === key ? ' is-active' : ''}"${tab === key ? ' aria-current="page"' : ''}`)).join('');

    const parts = m && l.parts.length > 1 && !(th && tab === 'learn') && !ownDeck && !ownCode && !ownExamples && !(tab === 'homework' && hw?.fresh) ? `<div class="parts" role="tablist" aria-label="Phần của bài">${l.parts.map((x, k) =>
      a(lessonHref(l.id, tab, 1, k), esc(x.title), `class="part${k === pi ? ' is-active' : ''}"${k === pi ? ' aria-current="true"' : ''}`)).join('')}</div>` : '';
    // Mọi thứ đi kèm bài trên một hàng: trắc nghiệm theo bài, bài thực hành, notebook Kaggle, PDF.
    const links = [
      lk.quiz ? a(`#/quiz/L-${l.id}`, `${icon('quiz')}Trắc nghiệm <b>${lk.quiz}</b>`, 'data-nav') : '',
      (lk.drill || []).length ? a(`#/practice/bai/${l.id}`, `${icon('practice')}Thực hành <b>${lk.drill.length}</b>`, 'data-nav') : '',
      lk.kaggle ? a(lk.kaggle, `${icon('external')}Chạy trên Kaggle`, 'target="_blank" rel="noopener"') : '',
      l.lessonPdf ? a(l.lessonPdf, `${icon('download')}PDF bài`, 'download') : '',
    ].filter(Boolean).join('');
    const draft = `<p class="draft">${isCheck(l) ? 'Đề kiểm tra đang được soạn.' : 'Bài này đang được soạn.'}</p>`;
    return `<div class="page page-wide">
      <header class="lesson-head">
        <p class="kicker">${a(`#/phase/${p.id}`, `Chương ${p.id}`, 'data-nav')}<span class="kicker-sep">·</span>${nameLabel(l)}</p>
        <h1>${esc(l.title)}</h1>
        ${m || th ? `<button class="mark${done ? ' is-done' : ''}" data-action="complete" aria-pressed="${done}">${icon(done ? 'done' : 'circle')}<span>${done ? 'Đã học' : 'Đánh dấu đã học'}</span></button>` : ''}
        ${links && (m || th) ? `<nav class="lesson-links" aria-label="Đi kèm bài">${links}</nav>` : ''}
      </header>
      ${m || th ? `${parts}${tabs ? `<nav class="tabs" aria-label="Nội dung bài">${tabs}</nav>` : ''}<div class="tab-body">${body}</div>` : draft}
      ${lessonPager(l)}${footer()}</div>`;
  }

  function tidyLessonDoc() {
    const doc = $('#lesson-doc');
    if (!doc) return;
    const h1 = doc.querySelector('h1');
    if (h1) {
      const hook = h1.nextElementSibling;
      if (hook && hook.tagName === 'P' && !hook.querySelector('a')) hook.classList.add('hook');
      h1.remove();
    }
    $$('#lesson-doc p').forEach(p => { if (p.querySelector('a[href$="slides.pptx"]')) p.remove(); });
    $$('#lesson-doc h2').forEach(h => {
      if (h.textContent.trim() !== INTERNAL) return;
      let n = h.nextElementSibling;
      while (n && n.tagName !== 'H2') { const next = n.nextElementSibling; n.remove(); n = next; }
      h.remove();
    });
    $$('#lesson-doc h2').forEach((h, i) => { h.id = `sec-${i}`; });
    K.ioBlocks('#lesson-doc.theory', {out: 'Kết quả', in: 'Input'});
    // ```py: đoạn code ngắn trong câu hỏi; tô màu tại chỗ, không chạy, không vào notebook.
    $$('#lesson-doc.theory pre > code.language-py').forEach(code => { code.innerHTML = highlight(code.textContent); code.parentElement.classList.add('snip'); });
    $$('#lesson-doc.theory pre > code.language-python').forEach(code => K.linkRun(K.codeFigure(code, 'Python', highlight, doc.classList.contains('code-examples'))));
    $$('#lesson-doc pre:not(.out):not(.code-body)').forEach(pre => {
      const text = pre.textContent;
      if (looksJSON(text)) pre.textContent = compactJSON(text);
      else if (looksPython(text)) pre.innerHTML = highlight(text);
    });
    wrapTables('#lesson-doc');
    // Link tới tệp .md của bài khác thì mở trang bài; README recipe mở bản đã định dạng trên GitHub.
    $$('#lesson-doc a[href^="giao_trinh/assets/phase-"]').forEach(x => {
      const h = x.getAttribute('href'), m = h.match(/^giao_trinh\/assets\/phase-\d+\/((?:\d+\.\d+|kt\d+))\.md$/);
      if (m && findLesson(m[1])) { x.setAttribute('href', `#/lesson/${m[1]}`); x.setAttribute('data-nav', ''); }
      else if (/\/README\.md$/.test(h)) {
        x.href = `https://github.com/Canuc80k/ai-canuc80k/blob/main/course/content/${h.replace(/^giao_trinh\/assets\//, '')}`;
        x.target = '_blank'; x.rel = 'noopener';
      }
    });
    $$('#lesson-doc.theory a[href^="http"]').forEach(x => { x.target = '_blank'; x.rel = 'noopener'; });
    window.Kit.fitMath();
  }
  function quizScore(sec) {
    const all = [...sec.querySelectorAll('.quiz')], done = all.filter(q => q.classList.contains('is-answered'));
    const right = done.filter(q => q.querySelector('.quiz-opt.is-right.is-chosen')).length;
    const box = sec.querySelector('.quiz-score');
    if (!box) return;
    box.classList.toggle('is-done', done.length === all.length);
    box.querySelector('span').textContent = done.length === all.length
      ? `Kết quả: ${right}/${all.length} câu đúng.` : `Đã làm ${done.length}/${all.length} câu.`;
  }
  function renderResources() {
    const docs = D.resources.map(res => `<div class="res">
        ${a(`#/resource/${res.id}`, `<span class="res-title">${esc(res.title)}</span>`, 'class="res-main" data-nav')}
        ${a(res.path, `${icon('download')}<span class="sr">Tải ${esc(res.title)}</span>`, 'class="icon-btn" download title="Tải tệp"')}
      </div>`).join('');
    const groups = [...new Set(D.sources.map(s => s.group || 'Học thêm'))].map(g => `<section class="block"><h2 class="block-title">${esc(g)}</h2><div class="res-list">${
      D.sources.filter(s => (s.group || 'Học thêm') === g).map(s => a(s.url,
        `<span class="res-title">${esc(s.title)}</span>${icon('external')}`,
        'class="res-main res-ext" target="_blank" rel="noopener"')).join('')}</div></section>`).join('');
    return `<div class="page">
      <header class="page-head"><h1>Tài liệu</h1></header>
      <div class="res-list">${docs}</div>
      ${groups}
      ${footer()}</div>`;
  }
  function inlineMd(text) {
    return esc(text)
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  }
  // Mục lý thuyết cần học để trả lời câu: q.learn = [[id bài, vị trí <h2> trên trang, tên mục, [câu cần đọc]], ...].
  // Link mở bài ở tab mới, giữ nguyên trang làm bài; &q= cho trang bài biết câu nào cần tô (learnSpot).
  function learnLine(q) {
    const links = (q.learn || []).map(([id, k, h]) => {
      const l = findLesson(id);
      return l ? a(`#/lesson/${id}?sec=${k}&q=${q.id}`, `<span class="quiz-learn-at">${esc(isCheck(l) ? l.title : `Bài ${id}`)}</span>${esc(h)}${icon('external')}`,
        'target="_blank" rel="noopener" title="Mở bài ở tab mới"') : '';
    }).join('');
    return links ? `<p class="quiz-learn"><span class="quiz-learn-kind">Ôn lại</span>${links}</p>` : '';
  }
  function mdDoc(text) {
    const lines = text.split(/\r?\n/);
    const para = [];
    let html = '', i = 0;
    const flush = () => { if (para.length) { html += `<p>${inlineMd(para.join(' '))}</p>`; para.length = 0; } };
    const cells = row => row.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim());
    while (i < lines.length) {
      const t = lines[i].trim();
      let m;
      if (!t) { flush(); i++; continue; }
      if ((m = t.match(/^(#{1,4})\s+(.*)$/))) {
        flush();
        const level = Math.min(Math.max(m[1].length, 2), 4);
        html += `<h${level}>${inlineMd(m[2])}</h${level}>`;
        i++; continue;
      }
      if (t.startsWith('|')) {
        flush();
        const rows = [];
        while (i < lines.length && lines[i].trim().startsWith('|')) rows.push(lines[i++]);
        const head = cells(rows[0]), body = rows.slice(2);
        html += `<div class="table-wrap"><table><thead><tr>${head.map(c => `<th>${inlineMd(c)}</th>`).join('')}</tr></thead><tbody>${body.map(r => `<tr>${cells(r).map(c => `<td>${inlineMd(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
        continue;
      }
      if (/^([-*]|\d+\.)\s+/.test(t)) {
        flush();
        const ordered = /^\d+\./.test(t), items = [];
        while (i < lines.length && /^\s*([-*]|\d+\.)\s+/.test(lines[i])) items.push(lines[i++].replace(/^\s*([-*]|\d+\.)\s+/, ''));
        const tag = ordered ? 'ol' : 'ul';
        html += `<${tag}>${items.map(x => `<li>${inlineMd(x)}</li>`).join('')}</${tag}>`;
        continue;
      }
      para.push(t); i++;
    }
    flush();
    return html;
  }
  function renderResource(id) {
    const res = D.resources.find(x => x.id === id);
    if (!res) return notFound();
    let content;
    if (res.format === 'md') {
      content = `<article class="prose md">${mdDoc(res.text.replace(/^#\s+.*\n+/, ''))}</article>`;
    } else {
      const lines = res.text.split(/\r?\n/);
      const text = lines[0] && lines[0] === lines[0].toLocaleUpperCase('vi') && /AI CANUC80K/i.test(lines[0]) ? lines.slice(1).join('\n') : res.text;
      content = `<article class="doc">${textDoc(text)}</article>`;
    }
    return `<div class="page${res.format === 'md' ? ' page-wide' : ''}">
      <header class="page-head"><p class="kicker">${a('#/resources', 'Tài liệu', 'data-nav')}</p><h1>${esc(res.title)}</h1>
        <div class="actions">${a(res.path, `${icon('download')}Tải tệp`, 'class="btn" download')}</div></header>
      ${content}${footer()}</div>`;
  }
  const notFound = K.notFound;

  // ---------- các cuộc thi (dữ liệu: ui/contests.js, dựng bằng tools/build_contests.py) ----------
  const CT = window.CONTESTS || {contests: [], pages: {}, columns: [], intro: ''};
  function renderContests(r) {
    if (r.id) {
      const c = CT.contests.find(x => x.id === r.id), pg = CT.pages[r.id];
      if (!c || !pg) return notFound();
      const k = CT.contests.indexOf(c), prev = CT.contests[k - 1], next = CT.contests[k + 1];
      return `<div class="page page-wide">
        <header class="lesson-head">
          <p class="kicker">${a('#/contests', 'Các cuộc thi', 'data-nav')}</p>
          <h1>${esc(c.name)}</h1>
          <nav class="lesson-links" aria-label="Liên kết">${(c.links || []).map(([label, url]) => a(url, `${icon('external')}${esc(label)}`, 'target="_blank" rel="noopener"')).join('')}</nav>
        </header>
        <div class="learn">
          <article class="prose theory" id="lesson-doc">${pg.html}</article>
          <aside class="toc" aria-label="Mục lục">${pg.headings.map((h, i) => `<a href="#sec-${i}" data-scroll="sec-${i}">${esc(h)}</a>`).join('')}</aside>
        </div>
        ${pager('Cuộc thi liền kề', prev && {href: `#/contests/${prev.id}`, label: '', title: prev.name}, next && {href: `#/contests/${next.id}`, label: '', title: next.name})}
        ${footer()}</div>`;
    }
    const rows = CT.contests.map((c, k) => a(`#/contests/${c.id}`,
      `<span class="phase-num">${k + 1}</span>
       <span class="phase-body"><span class="phase-title">${esc(c.name)}</span>${c.summary ? `<span class="phase-text">${esc(c.summary)}</span>` : ''}</span>
      `, 'class="phase" data-nav')).join('');
    const cols = CT.columns || [];
    const table = cols.length ? `<section class="block"><h2 class="block-title">So sánh nhanh</h2><div class="table-wrap"><table>
        <thead><tr>${cols.map(col => `<th>${esc(col.label)}</th>`).join('')}</tr></thead>
        <tbody>${CT.contests.map(c => `<tr>${cols.map((col, j) => `<td>${j ? inlineMd(String((c.compare || {})[col.key] || '')) : a(`#/contests/${c.id}`, esc(c.short), 'data-nav')}</td>`).join('')}</tr>`).join('')}</tbody>
      </table></div></section>` : '';
    return `<div class="page">
      <header class="page-head"><h1>Các cuộc thi</h1>${CT.intro ? `<p class="lead">${inlineMd(CT.intro)}</p>` : ''}</header>
      <div class="phases">${rows}</div>
      ${table}${footer()}</div>`;
  }

  // ---------- thực hành (dữ liệu: ui/practice-bank.js, dựng bằng tools/build_practice.py) ----------
  const PB = window.PRACTICE_BANK || {tiers: []};
  const practiceTier = id => PB.tiers.find(t => t.id === id);
  const PKEY = 'aicanuc80k.practice.v1';
  const PCODES = new Set(PB.tiers.flatMap(t => t.tasks.map(x => x.code)));
  let PS = new Set();
  try { const raw = JSON.parse(localStorage.getItem(PKEY) || '[]'); if (Array.isArray(raw)) PS = new Set(raw.filter(c => PCODES.has(c))); } catch (_) { PS = new Set(); }
  const pSave = () => K.store(PKEY, [...PS]);
  const pDone = t => t.tasks.filter(x => PS.has(x.code)).length;
  // Mã đề -> các bài học dùng nhiều nhất (đảo từ LESSON_LINKS[bài].drill).
  const DRILL_OF = {};
  Object.entries(LINKS).forEach(([lid, k]) => (k.drill || []).forEach(c => (DRILL_OF[c] = DRILL_OF[c] || []).push(lid)));
  const usesLine = x => (DRILL_OF[x.code] || []).length ? `<span class="pr-uses">Dùng bài ${DRILL_OF[x.code].sort((p, q) => D.lessons.findIndex(l => l.id === p) - D.lessons.findIndex(l => l.id === q))
    .map(lid => a(lessonHref(lid), lid, 'data-nav')).join(', ')}</span>` : '';
  function practiceCrumbs(r) {
    const t = practiceTier(r.id), here = text => `<span aria-current="page">${esc(text)}</span>`;
    if (r.id === 'ch') return [a('#/practice', 'Thực hành', 'data-nav'), here(`Chương ${r.sub}`)];
    if (r.id === 'bai') return [a('#/practice', 'Thực hành', 'data-nav'), here(`Bài ${r.sub}`)];
    return t ? [a('#/practice', 'Thực hành', 'data-nav'), here(t.title)] : [here('Thực hành')];
  }
  function renderPracticeHome() {
    const rows = PB.tiers.map((t, k) => {
      const n = t.tasks.length, d = pDone(t);
      return a(`#/practice/${t.id}`,
        `<span class="phase-num">${k + 1}</span>
         <span class="phase-body"><span class="phase-title">${esc(t.title)}</span></span>
         <span class="phase-meta">${d ? `<span class="phase-progress">${meter(d, n)}${d}/${n}</span>` : `${n} bài`}</span>`,
        'class="phase" data-nav');
    }).join('');
    const byCh = D.phases.map(p => { const n = PB.tiers.reduce((x, t) => x + t.tasks.filter(y => y.chapters.includes(p.id)).length, 0);
      return n ? a(`#/practice/ch/${p.id}`, `<b>${p.id}</b>${esc(p.short)}<span>${n}</span>`, 'class="qz-lchip ch-chip" data-nav') : ''; }).join('');
    return `<div class="page">
      <header class="page-head"><h1>Thực hành</h1></header>
      <div class="phases">${rows}</div>
      <section class="block"><h2 class="block-title">Theo chương</h2><div class="qz-lessons-chips">${byCh}</div></section>${footer()}</div>`;
  }
  function renderPracticeTier(t) {
    const d = pDone(t), n = t.tasks.length;
    const rows = t.tasks.map((x, k) => {
      const done = PS.has(x.code);
      const ch = x.chapters.length ? ` · chương ${x.chapters.join(', ')}` : '';
      const body = `<span class="pr-name">${esc(x.name)}</span><span class="pr-src">${esc(x.source)}${ch}</span>`;
      const main = x.status === 'soon'
        ? `<div class="pr-main">${body}</div>`
        : a(x.url, `${body}`, 'class="pr-main" target="_blank" rel="noopener"');
      const tail = x.status === 'soon' ? '<span class="pr-tag">Sắp có</span>'
        : x.status === 'link' ? a(x.url, `<span>Nộp tại nguồn</span>${icon('external')}`, 'class="pr-go" target="_blank" rel="noopener"')
        : a(x.url, `<span>LQDOJ</span>${icon('external')}`, 'class="pr-go" target="_blank" rel="noopener"');
      const data = x.data ? a(x.data, `${icon('download')}<span class="sr">Tải dữ liệu ${esc(x.name)}</span>`, 'class="icon-btn" target="_blank" rel="noopener" title="Tải dữ liệu"') : '';
      return `<div class="pr${done ? ' is-done' : ''}${x.status === 'soon' ? ' is-soon' : ''}">
        <button class="pr-check" type="button" data-action="pr-done" data-code="${x.code}" aria-pressed="${done}" aria-label="Đã làm ${esc(x.name)}" title="${done ? 'Bỏ đánh dấu' : 'Đánh dấu đã làm'}">${icon(done ? 'done' : 'circle')}</button>
        <span class="pr-num">${k + 1}</span><div class="pr-body">${main}${usesLine(x)}</div><span class="pr-tail">${data}${tail}</span></div>`;
    }).join('');
    return `<div class="page">
      <header class="page-head"><p class="kicker">${a('#/practice', 'Thực hành', 'data-nav')}</p><h1>${esc(t.title)}</h1>
        ${d ? `<div class="page-meta"><span class="phase-progress">${meter(d, n)}${d}/${n} bài</span></div>` : ''}</header>
      <div class="pr-list">${rows}</div>${footer()}</div>`;
  }
  function practiceList(rows, uses = true) {
    return rows.map((x, k) => {
      const done = PS.has(x.code);
      return `<div class="pr${done ? ' is-done' : ''}">
        <button class="pr-check" type="button" data-action="pr-done" data-code="${x.code}" aria-pressed="${done}" aria-label="Đã làm ${esc(x.name)}">${icon(done ? 'done' : 'circle')}</button>
        <span class="pr-num">${k + 1}</span><div class="pr-body">${a(x.url, `<span class="pr-name">${esc(x.name)}</span><span class="pr-src">${esc(x.tier.title)} · ${esc(x.source)}</span>`, 'class="pr-main" target="_blank" rel="noopener"')}${uses ? usesLine(x) : ''}</div>
        <span class="pr-tail">${x.data ? a(x.data, `${icon('download')}<span class="sr">Tải dữ liệu</span>`, 'class="icon-btn" target="_blank" rel="noopener" title="Tải dữ liệu"') : ''}${a(x.url, `<span>${x.status === 'link' ? 'Nộp tại nguồn' : 'LQDOJ'}</span>${icon('external')}`, 'class="pr-go" target="_blank" rel="noopener"')}</span></div>`;
    }).join('');
  }
  function renderPracticeChapter(ch) {
    const p = D.phases[ch];
    if (!p) return notFound();
    const rows = PB.tiers.flatMap(t => t.tasks.filter(x => x.chapters.includes(ch)).map(x => ({...x, tier: t})));
    return `<div class="page">
      <header class="page-head"><p class="kicker">${a('#/practice', 'Thực hành', 'data-nav')}</p><h1>Chương ${p.id} · ${esc(p.title)}</h1></header>
      <div class="pr-list">${practiceList(rows) || empty()}</div>${footer()}</div>`;
  }
  function renderPracticeLesson(id) {
    const l = findLesson(id);
    if (!l) return notFound();
    const rows = ((LINKS[id] || {}).drill || []).map(practiceTask).filter(Boolean);
    return `<div class="page">
      <header class="page-head"><p class="kicker">${a('#/practice', 'Thực hành', 'data-nav')}</p><h1>${nameLabel(l)} · ${esc(l.title)}</h1></header>
      <div class="pr-list">${practiceList(rows, false) || empty()}</div>${footer()}</div>`;
  }
  function renderPractice(r) {
    if (!r.id) return renderPracticeHome();
    if (r.id === 'ch') return renderPracticeChapter(Number(r.sub));
    if (r.id === 'bai') return renderPracticeLesson(r.sub);
    const t = practiceTier(r.id);
    return t && !r.sub ? renderPracticeTier(t) : notFound();
  }

  // ---------- trắc nghiệm (dữ liệu: ui/quiz-bank.js, dựng bằng tools/build_quizzes.py) ----------
  let QB = window.QUIZ_BANK || {sets: []};
  // Kho ẩn (hidden) không mở để luyện; bộ có pool thì chế độ kiểm tra bốc câu từ cả bộ lẫn kho.
  const quizAny = id => String(id || '').startsWith('L-') ? lessonSet(id) : QB.sets.find(s => s.id === id);
  const quizSet = id => { const s = quizAny(id); return s && !s.hidden ? s : undefined; };
  const QKEY = 'aicanuc80k.quiz.v1';
  const LETTERS = 'ABCD';
  let QS = {};
  // Chỉ giữ dữ liệu lưu hợp lệ: câu còn tồn tại, đáp án 0–3, lượt làm trỏ đúng chỉ số.
  let QRAW = {};
  function qInit(s) {
    const raw = QRAW[s.id] && typeof QRAW[s.id] === 'object' ? QRAW[s.id] : {};
    const st = {answers: {}, mode: null, ids: [], index: 0};
    const known = new Set(s.questions.map(q => q.id)), n = s.questions.length;
    if (raw.answers && typeof raw.answers === 'object') {
      for (const [k, v] of Object.entries(raw.answers)) if (known.has(k) && Number.isInteger(v) && v >= 0 && v < 4) st.answers[k] = v;
    }
    const modeOk = ['all', 'wrong', 'todo'].includes(raw.mode) || s.groups.some(g => g.id === raw.mode);
    if (modeOk && Array.isArray(raw.ids) && raw.ids.length && new Set(raw.ids).size === raw.ids.length && raw.ids.every(i => Number.isInteger(i) && i >= 0 && i < n)) {
      st.mode = raw.mode; st.ids = raw.ids;
      st.index = Number.isInteger(raw.index) && raw.index >= 0 && raw.index < raw.ids.length ? raw.index : 0;
    }
    QS[s.id] = st;
  }
  function qLoad() {
    try { QRAW = JSON.parse(localStorage.getItem(QKEY) || '{}') || {}; } catch (_) { QRAW = {}; }
    QS = {};
    for (const s of QB.sets) qInit(s);
    for (const s of LSETS.values()) qInit(s);
  }
  // Bộ “theo bài”: mọi câu của sáu bộ có dòng Ôn lại trỏ về bài ấy, chia nhóm theo mức (Light, Medium…).
  const LSETS = new Map();
  function lessonSet(id) {
    if (LSETS.has(id)) return LSETS.get(id);
    const lid = id.slice(2), l = findLesson(lid);
    if (!l || !QB.sets.length) return undefined;
    const groups = [], qs = [], seen = new Set();
    for (const s of QB.sets) {
      if (s.hidden) continue;
      const gid = s.id.replace(/\d+$/, '');
      for (const q of s.questions) {
        if (seen.has(q.id) || !(q.learn || []).some(x => x[0] === lid)) continue;
        seen.add(q.id);
        if (!groups.some(g => g.id === gid)) groups.push({id: gid, name: s.title.replace(/\s*\d+$/, '')});
        qs.push({...q, group: gid});
      }
    }
    if (!qs.length) return undefined;
    const set = {id, title: `${nameLabel(l)} · ${l.title}`, lesson: lid, questions: qs, groups};
    LSETS.set(id, set);
    qInit(set);
    return set;
  }
  const qSave = () => K.store(QKEY, {...QRAW, ...QS});
  const qAll = s => s.questions.map((_, i) => i);
  const qInGroup = (s, gid) => qAll(s).filter(i => s.questions[i].group === gid);
  function qStats(s, idx) {
    const st = QS[s.id];
    let right = 0, wrong = 0;
    for (const i of idx) {
      const q = s.questions[i], v = st.answers[q.id];
      if (v !== undefined) v === q.answer ? right++ : wrong++;
    }
    return {right, wrong, done: right + wrong, todo: idx.length - right - wrong};
  }
  function qPick(s, mode) {
    const st = QS[s.id];
    if (mode === 'wrong') return qAll(s).filter(i => { const q = s.questions[i], v = st.answers[q.id]; return v !== undefined && v !== q.answer; });
    if (mode === 'todo') return qAll(s).filter(i => st.answers[s.questions[i].id] === undefined);
    return mode === 'all' ? qAll(s) : qInGroup(s, mode);
  }
  const qModeName = (s, mode) => mode === 'wrong' ? 'Câu làm sai' : mode === 'todo' ? 'Câu chưa làm'
    : (s.groups.find(g => g.id === mode) || {}).name || `Cả ${s.questions.length} câu`;
  const qBtn = (s, mode, label, cls = 'btn') => `<button class="${cls}" type="button" data-action="qz-start" data-set="${s.id}" data-mode="${mode}">${label}</button>`;
  function qStart(s, mode) {
    const ids = qPick(s, mode);
    if (!ids.length) { toast(mode === 'wrong' ? 'Chưa có câu nào làm sai' : 'Đã làm hết các câu'); return; }
    const st = QS[s.id], first = ids.findIndex(i => st.answers[s.questions[i].id] === undefined);
    st.mode = mode; st.ids = ids; st.index = Math.max(first, 0);
    qSave();
    const href = `#/quiz/${s.id}/play`;
    if (location.hash === href) { render(); window.scrollTo(0, 0); } else location.hash = href;
  }
  function quizCrumbs(r) {
    const s = quizSet(r.id), here = text => `<span aria-current="page">${esc(text)}</span>`;
    if (!s) return [here('Trắc nghiệm')];
    const out = [a('#/quiz', 'Trắc nghiệm', 'data-nav'), r.sub ? a(`#/quiz/${s.id}`, s.title, 'data-nav') : here(s.title)];
    if (r.sub === 'play') out.push(here(qModeName(s, QS[s.id].mode)));
    if (r.sub === 'result') out.push(here('Kết quả'));
    return out;
  }
  // Trang chủ trắc nghiệm gom các bộ theo mức (Light, Light 2, … → Light); mỗi lần mở trang các mức đều đóng, mở mức này thì đóng mức khác.
  const qLevelOf = id => id.replace(/\d+$/, '');
  let QL = new Set();
  try { localStorage.removeItem('aicanuc80k.quizlevels.v1'); } catch (_) {}
  function quizLevels() {
    const out = [];
    for (const s of QB.sets) {
      if (s.hidden) continue;
      const id = qLevelOf(s.id);
      let lv = out.find(x => x.id === id);
      if (!lv) out.push(lv = {id, title: s.title.replace(/\s*\d+$/, ''), sets: []});
      lv.sets.push(s);
    }
    return out;
  }
  function renderQuizHome() {
    const levels = quizLevels().map((lv, k) => {
      const n = lv.sets.reduce((x, s) => x + s.questions.length, 0);
      const done = lv.sets.reduce((x, s) => x + qStats(s, qAll(s)).done, 0);
      const meta = done ? `<span class="phase-progress">${meter(done, n)}${done}/${n}</span>` : `${lv.sets.length > 1 ? `${lv.sets.length} bộ · ` : ''}${n} câu`;
      if (lv.sets.length === 1) return `<section class="qz-level">${a(`#/quiz/${lv.sets[0].id}`,
        `<span class="phase-num">${k + 1}</span>
          <span class="phase-body"><span class="phase-title">${esc(lv.title)}</span></span>
          <span class="phase-meta">${meta}</span>
          ${icon('arrow')}`, 'class="phase qz-level-head" data-nav')}</section>`;
      const open = QL.has(lv.id);
      const subs = lv.sets.map((s, j) => {
        const t = qStats(s, qAll(s)), m = s.questions.length;
        return a(`#/quiz/${s.id}`,
          `<span class="qz-sub-name">Bộ ${j + 1}</span>
           <span class="qz-sub-meta">${t.done ? `${t.done}/${m}` : `${m} câu`}</span>
           <span class="qz-sub-bar"><span style="width:${Math.round(100 * t.done / m)}%"></span></span>`,
          `class="qz-sub${t.done ? ' is-started' : ''}" data-nav aria-label="${esc(s.title)}"`);
      }).join('');
      return `<section class="qz-level${open ? ' is-open' : ''}">
        <button class="phase qz-level-head" type="button" data-action="qz-level" data-level="${lv.id}" aria-expanded="${open}" aria-controls="qzl-${lv.id}">
          <span class="phase-num">${k + 1}</span>
          <span class="phase-body"><span class="phase-title">${esc(lv.title)}</span></span>
          <span class="phase-meta">${meta}</span>
          ${icon('chev')}
        </button>
        <div class="qz-subs" id="qzl-${lv.id}"${open ? '' : ' hidden'}><div class="qz-subs-grid">${subs}</div></div>
      </section>`;
    }).join('');
    return `<div class="page">
      <header class="page-head"><h1>Trắc nghiệm</h1></header>
      <div class="phases qz-levels">${levels}</div>
      ${footer()}</div>`;
  }
  function renderQuizSet(s) {
    QL = new Set([qLevelOf(s.id)]);
    const st = QS[s.id], all = qAll(s), tot = qStats(s, all);
    const cur = st.ids.length ? qStats(s, st.ids) : null;
    const resume = cur && cur.done && cur.todo
      ? a(`#/quiz/${s.id}/play`, 'Làm tiếp', 'class="btn is-primary" data-nav')
      : qBtn(s, tot.done && tot.todo ? 'todo' : 'all', tot.done ? (tot.todo ? 'Làm tiếp' : 'Làm lại') : 'Làm bài', 'btn is-primary');
    const lead = (s.lesson ? a(lessonHref(s.lesson), `${icon('book')}Đọc lại bài`, 'class="btn" data-nav') : '') + resume + exBtn(s);
    const reset = tot.done ? `<button class="qz-reset" type="button" data-action="qz-reset" data-set="${s.id}">Xóa kết quả</button>` : '';
    const topics = s.groups.map((g, k) => {
      const idx = qInGroup(s, g.id), t = qStats(s, idx);
      return qBtn(s, g.id,
        `<span class="phase-num">${k + 1}</span>
         <span class="phase-body"><span class="phase-title">${esc(g.name)}</span></span>
         <span class="phase-meta">${t.done ? `<span class="phase-progress">${meter(t.done, idx.length)}${t.done}/${idx.length}</span>` : `${idx.length} câu`}</span>`, 'phase');
    }).join('');
    return `<div class="page">
      <header class="page-head"><p class="kicker">${a('#/quiz', 'Trắc nghiệm', 'data-nav')}</p><div class="qz-title-row"><h1>${esc(s.title)}</h1><div class="actions">${lead}</div></div>
        ${tot.done ? `<div class="page-meta"><span class="phase-progress">${meter(tot.done, all.length)}${tot.done}/${all.length} câu</span><span>${tot.right} đúng · ${tot.wrong} sai</span>${reset}</div>` : ''}</header>
      <section class="block"><h2 class="block-title">${s.lesson ? 'Theo mức' : 'Chủ đề'}</h2><div class="phases">${topics}</div></section>
      ${footer()}</div>`;
  }
  function renderQuizPlay(s) {
    const st = QS[s.id];
    if (!st.ids.length) { st.mode = 'all'; st.ids = qAll(s); st.index = 0; }
    const q = s.questions[st.ids[st.index]], chosen = st.answers[q.id], open = chosen !== undefined;
    const g = s.groups.find(x => x.id === q.group), t = qStats(s, st.ids), last = st.index === st.ids.length - 1;
    const opts = q.options.map((o, k) => {
      const cls = !open ? '' : (k === q.answer ? ' is-right' : k === chosen ? ' is-wrong' : '') + (k === chosen ? ' is-chosen' : '');
      return `<li><button type="button" class="quiz-opt${cls}" data-action="qz-answer" data-choice="${k}"${open ? ' aria-disabled="true"' : ''}><span class="quiz-key">${LETTERS[k]}</span><span>${inlineMd(o)}</span></button></li>`;
    }).join('');
    const verdict = chosen === q.answer ? 'Chính xác.' : `Chưa đúng. Đáp án là ${LETTERS[q.answer]}.`;
    const src = q.src ? `<p class="quiz-src${q.src.kind === 'Phỏng theo' ? ' quiz-src-adapted' : ''}"><span class="quiz-src-kind">${esc(q.src.kind)}</span>${q.src.url ? `<a href="${esc(q.src.url)}" target="_blank" rel="noopener">${esc(q.src.label)}</a>` : esc(q.src.label)}</p>` : '';
    const cells = st.ids.map((i, p) => {
      const v = st.answers[s.questions[i].id], ok = v === s.questions[i].answer;
      return `<button type="button" class="qz-cell${v === undefined ? '' : ok ? ' is-right' : ' is-wrong'}${p === st.index ? ' is-current' : ''}" data-action="qz-jump" data-index="${p}"
        aria-label="Câu ${p + 1}${v === undefined ? '' : ok ? ', đúng' : ', sai'}"${p === st.index ? ' aria-current="step"' : ''}>${p + 1}</button>`;
    }).join('');
    return `<div class="page qz-page">
      <div class="qz-head"><span>${esc(g.name)}</span><span class="qz-pos">Câu ${st.index + 1}<span>/${st.ids.length}</span></span></div>
      <div class="qz-bar" role="progressbar" aria-label="Số câu đã trả lời" aria-valuemin="0" aria-valuemax="${st.ids.length}" aria-valuenow="${t.done}"><i style="width:${t.done / st.ids.length * 100}%"></i></div>
      <article class="quiz qz-card${open ? ' is-answered' : ''}">
        <h1 class="qz-q" id="qz-q">${inlineMd(q.q)}</h1>
        ${q.code ? `<pre class="qz-code"><code>${highlight(q.code)}</code></pre>` : ''}
        <ol class="quiz-opts" aria-labelledby="qz-q">${opts}</ol>
        <div class="quiz-why" id="qz-why" tabindex="-1" aria-live="polite"${open ? '' : ' hidden'}>${open ? `<p class="quiz-verdict">${verdict}</p><p>${inlineMd(q.why)}</p>${learnLine(q)}` : ''}</div>
        ${src}
      </article>
      <nav class="qz-nav" aria-label="Chuyển câu">
        <button class="btn" type="button" data-action="qz-prev"${st.index ? '' : ' disabled'}>${icon('back')}Câu trước</button>
        <button class="btn is-primary" type="button" data-action="qz-next">${last ? 'Xem kết quả' : 'Câu tiếp'}${icon('arrow')}</button>
      </nav>
      <div class="qz-grid" role="group" aria-label="Chọn câu">${cells}</div>
    </div>`;
  }
  function renderQuizResult(s) {
    const st = QS[s.id];
    if (!st.ids.length) return renderQuizSet(s);
    const t = qStats(s, st.ids), n = st.ids.length, tot = qStats(s, qAll(s));
    const groups = s.groups.map(g => ({g, idx: st.ids.filter(i => s.questions[i].group === g.id)})).filter(x => x.idx.length);
    const byTopic = groups.length > 1 ? `<section class="block"><h2 class="block-title">Theo chủ đề</h2><div class="qz-rows">${groups.map(({g, idx}) => {
      const x = qStats(s, idx);
      return `<div class="qz-row"><span>${esc(g.name)}</span><span class="phase-progress">${meter(x.right, idx.length)}${x.right}/${idx.length}</span></div>`;
    }).join('')}</div></section>` : '';
    const nextSet = quizSet({light: 'light2', light2: 'light3', light3: 'light4', light4: 'light5', light5: 'medium', medium: 'medium2', medium2: 'medium3', medium3: 'high', high: 'high2', high2: 'extra', extra: 'extra2', extra2: 'max', max: 'ultra'}[s.id]);
    const next = nextSet ? a(`#/quiz/${nextSet.id}`, `Sang bộ ${esc(nextSet.title)}${icon('arrow')}`, 'class="btn" data-nav') : '';
    const acts = [
      tot.wrong ? qBtn(s, 'wrong', `Ôn câu sai <span class="qz-n">${tot.wrong}</span>`, 'btn is-primary') : '',
      tot.todo ? qBtn(s, 'todo', `Câu chưa làm <span class="qz-n">${tot.todo}</span>`) : '',
      a(`#/quiz/${s.id}`, `Về bộ ${esc(s.title)}`, 'class="btn" data-nav'), next
    ].join('');
    return `<div class="page qz-page">
      <header class="page-head"><p class="kicker">${a(`#/quiz/${s.id}`, esc(s.title), 'data-nav')}</p><h1>Kết quả</h1></header>
      <div class="qz-score"><span class="qz-score-num">${t.right}<span>/${n}</span></span><span class="qz-score-text">câu đúng${t.todo ? `, còn ${t.todo} câu chưa làm` : ''}</span></div>
      ${byTopic}
      <div class="actions qz-actions">${acts}</div>
      ${footer()}</div>`;
  }
  function renderQuiz(r) {
    if (!r.id) return renderQuizHome();
    const s = quizSet(r.id);
    if (!s) return notFound();
    return r.sub === 'play' ? renderQuizPlay(s) : r.sub === 'result' ? renderQuizResult(s) : r.sub ? notFound() : renderQuizSet(s);
  }
  function qCurrent() {
    const r = route(), s = r.type === 'quiz' && r.sub === 'play' ? quizSet(r.id) : null;
    return s && QS[s.id].ids.length ? {s, st: QS[s.id]} : null;
  }
  function qAnswer(k) {
    const c = qCurrent();
    if (!c || !(k >= 0 && k < 4)) return;
    const q = c.s.questions[c.st.ids[c.st.index]];
    if (c.st.answers[q.id] !== undefined) return;
    c.st.answers[q.id] = k;
    qSave(); render();
    const why = $('#qz-why');
    if (why) { why.focus({preventScroll: true}); why.scrollIntoView({block: 'nearest', behavior: 'smooth'}); }
  }
  // Giữ tiêu điểm ở đúng nút vừa bấm sau khi vẽ lại, để Enter liên tiếp không vô tình chọn đáp án.
  function qJump(p, focus) {
    const c = qCurrent();
    if (!c || !(p >= 0 && p < c.st.ids.length)) return;
    c.st.index = p;
    qSave(); render(); window.scrollTo(0, 0);
    const el = focus && $(focus);
    (el && !el.disabled ? el : $('.qz-nav [data-action="qz-next"]'))?.focus({preventScroll: true});
  }
  function qMove(step) {
    const c = qCurrent();
    if (!c) return;
    const p = c.st.index + step;
    if (p >= c.st.ids.length) { location.hash = `#/quiz/${c.s.id}/result`; return; }
    qJump(p, `.qz-nav [data-action="${step > 0 ? 'qz-next' : 'qz-prev'}"]`);
  }

  // ---------- kiểm tra: đề ngẫu nhiên, tính giờ, khóa điều hướng đến khi nộp bài ----------
  const EKEY = 'aicanuc80k.exam.v1', ELOG = 'aicanuc80k.examlog.v1';
  const EX_SIZES = [100];
  const exSecs = s => s.id.startsWith('light') ? 45 : s.id.startsWith('medium') ? 60 : 90;
  const exMinutes = (s, n) => Math.round(n * exSecs(s) / 60);
  const exPools = {};
  function exPool(s) {
    const r = s && s.pool && quizAny(s.pool);
    return r ? exPools[s.id] || (exPools[s.id] = {...s, questions: s.questions.concat(r.questions)}) : s;
  }
  let EX = null, EXLOG = {};
  // Có bài kiểm tra đang làm dở (lưu trong máy) thì phải nạp kho câu hỏi trước lần vẽ đầu.
  const examPending = () => { try { const r = JSON.parse(localStorage.getItem(EKEY) || 'null'); return !!(r && !r.done); } catch (_) { return false; } };
  function initQuiz() {
    if (initQuiz.done || !window.QUIZ_BANK) return;
    initQuiz.done = true;
    QB = window.QUIZ_BANK;
    qLoad();
    exRestore();
  }
  function exRestore() {
  try {
    const raw = JSON.parse(localStorage.getItem(EKEY) || 'null'), s = raw && exPool(quizSet(raw.set)), n = s ? s.questions.length : 0;
    const okIds = raw && Array.isArray(raw.ids) && raw.ids.length && new Set(raw.ids).size === raw.ids.length && raw.ids.every(i => Number.isInteger(i) && i >= 0 && i < n);
    const okOrder = okIds && Array.isArray(raw.order) && raw.order.length === raw.ids.length && raw.order.every(o => Array.isArray(o) && [...o].sort().join() === '0,1,2,3');
    if (okOrder && Number.isFinite(raw.end) && Number.isFinite(raw.start)) {
      const answers = {};
      for (const [k, v] of Object.entries(raw.answers || {})) if (Number.isInteger(+k) && +k < raw.ids.length && Number.isInteger(v) && v >= 0 && v < 4) answers[k] = v;
      EX = {set: raw.set, ids: raw.ids, order: raw.order, answers, start: raw.start, end: raw.end,
        index: Number.isInteger(raw.index) && raw.index >= 0 && raw.index < raw.ids.length ? raw.index : 0,
        done: !!raw.done, finished: Number.isFinite(raw.finished) ? raw.finished : null};
    }
  } catch (_) { EX = null; }
  }
  try { EXLOG = JSON.parse(localStorage.getItem(ELOG) || '{}') || {}; } catch (_) { EXLOG = {}; }
  function exSave() { K.store(EKEY, EX); K.store(ELOG, EXLOG); }
  const exActive = () => !!(EX && !EX.done);
  const exSet = () => EX && exPool(quizSet(EX.set));
  function exShuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [arr[i], arr[j]] = [arr[j], arr[i]]; }
    return arr;
  }
  function exStart(s, n) {
    if (exActive()) { location.hash = '#/exam'; return; }
    s = exPool(s); n = Math.min(n, s.questions.length);
    const ids = exShuffle(qAll(s)).slice(0, n), now = Date.now();
    EX = {set: s.id, ids, order: ids.map(() => exShuffle([0, 1, 2, 3])), answers: {}, start: now, end: now + n * exSecs(s) * 1000, index: 0, done: false, finished: null};
    exSave();
    location.hash = '#/exam';
  }
  function exRight() { const s = exSet(); return EX.ids.filter((i, p) => EX.answers[p] === s.questions[i].answer).length; }
  function exSubmit() {
    if (!exActive()) return;
    EX.done = true; EX.finished = Math.min(Date.now(), EX.end);
    (EXLOG[EX.set] = EXLOG[EX.set] || []).push({n: EX.ids.length, right: exRight(), secs: Math.round((EX.finished - EX.start) / 1000), at: EX.finished});
    EXLOG[EX.set] = EXLOG[EX.set].slice(-20);
    exSave(); exTick.stop();
    location.hash = '#/exam/result';
  }
  const clock = secs => { secs = Math.max(0, Math.round(secs)); const h = Math.floor(secs / 3600), m = Math.floor(secs % 3600 / 60), x = secs % 60;
    return (h ? `${h}:${String(m).padStart(2, '0')}` : `${m}`) + `:${String(x).padStart(2, '0')}`; };
  const exTick = {
    id: null,
    start() { if (!this.id) this.id = setInterval(() => this.update(), 500); this.update(); },
    stop() { clearInterval(this.id); this.id = null; },
    update() {
      if (!exActive()) { this.stop(); return; }
      const left = (EX.end - Date.now()) / 1000, el = $('#ex-clock');
      if (left <= 0) { exSubmit(); return; }
      if (el) { el.textContent = clock(left); el.classList.toggle('is-low', left <= 60); }
    }
  };
  function exJump(p, focus) {
    if (!exActive() || !(p >= 0 && p < EX.ids.length)) return;
    EX.index = p; exSave(); render(); window.scrollTo(0, 0);
    const el = focus && $(focus);
    (el && !el.disabled ? el : $('.qz-nav [data-action="ex-next"]'))?.focus({preventScroll: true});
  }
  function exPick(k) {
    if (!exActive() || !(k >= 0 && k < 4)) return;
    const orig = EX.order[EX.index][k];
    if (EX.answers[EX.index] === orig) delete EX.answers[EX.index]; else EX.answers[EX.index] = orig;
    exSave(); render();
    $(`.quiz-opt[data-choice="${k}"]`)?.focus({preventScroll: true});
  }
  function exAskSubmit() {
    const left = EX.ids.length - Object.keys(EX.answers).length;
    if (window.confirm(left ? `Còn ${left} câu chưa làm. Nộp bài?` : 'Nộp bài?')) exSubmit();
  }
  function renderExamPlay() {
    const s = exSet(), p = EX.index, q = s.questions[EX.ids[p]], g = s.groups.find(x => x.id === q.group), n = EX.ids.length;
    const done = Object.keys(EX.answers).length, last = p === n - 1;
    const opts = EX.order[p].map((orig, k) => `<li><button type="button" class="quiz-opt${EX.answers[p] === orig ? ' is-picked' : ''}" data-action="ex-pick" data-choice="${k}" aria-pressed="${EX.answers[p] === orig}"><span class="quiz-key">${LETTERS[k]}</span><span>${inlineMd(q.options[orig])}</span></button></li>`).join('');
    const cells = EX.ids.map((_, k) => `<button type="button" class="qz-cell${EX.answers[k] !== undefined ? ' is-done' : ''}${k === p ? ' is-current' : ''}" data-action="ex-jump" data-index="${k}"
      aria-label="Câu ${k + 1}${EX.answers[k] !== undefined ? ', đã làm' : ''}"${k === p ? ' aria-current="step"' : ''}>${k + 1}</button>`).join('');
    return `<div class="page qz-page ex-page">
      <div class="ex-bar"><span class="ex-title">${esc(s.title)} · Kiểm tra</span><span class="ex-clock" id="ex-clock" role="timer" aria-label="Thời gian còn lại">${clock((EX.end - Date.now()) / 1000)}</span>
        <button class="btn is-primary" type="button" data-action="ex-submit">Nộp bài</button></div>
      <div class="qz-head"><span>${esc(g.name)}</span><span class="qz-pos">Câu ${p + 1}<span>/${n}</span></span></div>
      <div class="qz-bar" role="progressbar" aria-label="Số câu đã làm" aria-valuemin="0" aria-valuemax="${n}" aria-valuenow="${done}"><i style="width:${done / n * 100}%"></i></div>
      <article class="quiz qz-card">
        <h1 class="qz-q" id="qz-q">${inlineMd(q.q)}</h1>
        ${q.code ? `<pre class="qz-code"><code>${highlight(q.code)}</code></pre>` : ''}
        <ol class="quiz-opts" aria-labelledby="qz-q">${opts}</ol>
      </article>
      <nav class="qz-nav" aria-label="Chuyển câu">
        <button class="btn" type="button" data-action="ex-prev"${p ? '' : ' disabled'}>${icon('back')}Câu trước</button>
        ${last ? '<button class="btn is-primary" type="button" data-action="ex-submit">Nộp bài</button>' : `<button class="btn is-primary" type="button" data-action="ex-next">Câu tiếp${icon('arrow')}</button>`}
      </nav>
      <div class="qz-grid" role="group" aria-label="Chọn câu">${cells}</div>
    </div>`;
  }
  function renderExamResult() {
    const s = exSet(), n = EX.ids.length, right = exRight(), blank = n - Object.keys(EX.answers).length;
    const byTopic = s.groups.map(g => {
      const ps = EX.ids.map((i, p) => p).filter(p => s.questions[EX.ids[p]].group === g.id);
      if (!ps.length) return '';
      const r = ps.filter(p => EX.answers[p] === s.questions[EX.ids[p]].answer).length;
      return `<div class="qz-row"><span>${esc(g.name)}</span><span class="phase-progress">${meter(r, ps.length)}${r}/${ps.length}</span></div>`;
    }).join('');
    const review = EX.ids.map((i, p) => {
      const q = s.questions[i], pick = EX.answers[p];
      const opts = EX.order[p].map((orig, k) => {
        const cls = (orig === q.answer ? ' is-right' : orig === pick ? ' is-wrong' : '') + (orig === pick ? ' is-chosen' : '');
        return `<li><span class="quiz-opt${cls}"><span class="quiz-key">${LETTERS[k]}</span><span>${inlineMd(q.options[orig])}</span></span></li>`;
      }).join('');
      const verdict = pick === undefined ? 'Bỏ trống.' : pick === q.answer ? 'Đúng.' : 'Sai.';
      const src = q.src ? `<p class="quiz-src${q.src.kind === 'Phỏng theo' ? ' quiz-src-adapted' : ''}"><span class="quiz-src-kind">${esc(q.src.kind)}</span>${q.src.url ? `<a href="${esc(q.src.url)}" target="_blank" rel="noopener">${esc(q.src.label)}</a>` : esc(q.src.label)}</p>` : '';
      return `<article class="quiz qz-card is-answered ex-review${pick === q.answer ? ' is-ok' : ''}">
        <p class="ex-num">Câu ${p + 1}</p>
        <h2 class="qz-q">${inlineMd(q.q)}</h2>
        ${q.code ? `<pre class="qz-code"><code>${highlight(q.code)}</code></pre>` : ''}
        <ol class="quiz-opts">${opts}</ol>
        <div class="quiz-why"><p class="quiz-verdict">${verdict}</p><p>${inlineMd(q.why)}</p>${learnLine(q)}</div>${src}
      </article>`;
    }).join('');
    return `<div class="page qz-page">
      <header class="page-head"><p class="kicker">${a(`#/quiz/${s.id}`, esc(s.title), 'data-nav')}</p><h1>Kết quả kiểm tra</h1></header>
      <div class="qz-score"><span class="qz-score-num">${right}<span>/${n}</span></span><span class="qz-score-text">câu đúng${blank ? `, bỏ trống ${blank} câu` : ''} · ${clock((EX.finished - EX.start) / 1000)}</span></div>
      <section class="block"><h2 class="block-title">Theo chủ đề</h2><div class="qz-rows">${byTopic}</div></section>
      <div class="actions qz-actions">
        <button class="btn is-primary" type="button" data-action="ex-start" data-set="${s.id}" data-n="${n}">Làm đề mới ${n} câu</button>
        ${a(`#/quiz/${s.id}`, `Về bộ ${esc(s.title)}`, 'class="btn" data-nav')}
      </div>
      <section class="block ex-reviews"><h2 class="block-title">Xem lại bài</h2>${review}</section>
      ${footer()}</div>`;
  }
  function renderExam(r) {
    if (exActive()) return renderExamPlay();
    return EX && exSet() ? renderExamResult() : notFound();
  }
  // Một nút Kiểm tra cạnh nút Làm bài: đề 100 câu (bộ ít hơn thì lấy cả bộ), giờ làm theo mức.
  function exBtn(s) {
    const n = s.questions.length >= EX_SIZES[0] ? EX_SIZES[0] : s.questions.length;
    if (n < 5) return '';
    return `<button class="btn" type="button" data-action="ex-start" data-set="${s.id}" data-n="${n}" title="${n} câu · ${exMinutes(s, n)} phút">Kiểm tra</button>`;
  }

  function needs(r) {
    const wait = [];
    if (r.type === 'lesson' && findLesson(r.id) && !lessonReady(r.id)) wait.push(ensureLesson(r.id));
    if (!quizReady() && (r.type === 'quiz' || r.type === 'exam' || (r.type === 'lesson' && r.params.get('q')))) wait.push(ensureQuiz());
    return wait;
  }
  Object.assign(K.hooks, {
    needs,
    views: {home: renderHome, phase: r => renderPhase(r.id), lesson: renderLesson,
      quiz: renderQuiz, exam: renderExam, practice: renderPractice, contests: renderContests, resources: renderResources, resource: r => renderResource(r.id)},
    before(r) { if (r.type === 'exercises') { location.replace('#/'); return true; } },
    after(r) {
      const l = r.type === 'lesson' ? findLesson(r.id) : null;
      const qs = r.type === 'quiz' ? quizSet(r.id) : null;
      const pt = r.type === 'practice' ? practiceTier(r.id) : null;
      document.documentElement.classList.toggle('exam-lock', exActive());
      if (r.type === 'exam' && exActive()) exTick.start(); else exTick.stop();
      document.title = l ? `${l.title} — AI Canuc80k` : r.type === 'exam' && exSet() ? `Kiểm tra ${exSet().title} — AI Canuc80k` : r.type === 'quiz' ? `Trắc nghiệm${qs ? ' ' + qs.title : ''} — AI Canuc80k`
        : r.type === 'practice' ? `Thực hành${pt ? ' ' + pt.title : ''} — AI Canuc80k`
        : r.type === 'contests' ? `${(CT.contests.find(c => c.id === r.id) || {name: 'Các cuộc thi'}).name} — AI Canuc80k` : 'AI Canuc80k';
      if (l) { tidyLessonDoc(); chrome(r); spy(); }
      if (r.type === 'contests' && r.id && CT.pages[r.id]) { tidyLessonDoc(); spy(); }
      window.Anim?.scan($('#main'));
    },
    // Mở bài từ “Ôn lại” (&q=): tô câu cần đọc và đặt câu đó ở khoảng một phần ba màn hình.
    spot(r, sec, h, k) {
      const marks = learnSpot(sec, r.id, k, r.params.get('q'));
      if (!marks.length) return false;
      // Câu cần đọc nằm ở khoảng một phần ba màn hình; câu gần đầu mục thì giữ cả tiêu đề mục trong khung nhìn.
      if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
      const place = () => {
        const pad = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
        const y = el => el.getBoundingClientRect().top + window.scrollY;
        const top = y(marks[0]) - y(h) < window.innerHeight * .45 ? y(h) - pad : y(marks[0]) - Math.max(pad + 24, window.innerHeight * .32);
        window.scrollTo(0, Math.max(0, top));
      };
      place();
      // Phông chữ và ảnh nạp xong có thể đẩy chữ xuống: đặt lại một lần, nếu người đọc chưa tự cuộn.
      let moved = false;
      for (const ev of ['wheel', 'touchstart', 'keydown', 'mousedown']) window.addEventListener(ev, () => { moved = true; }, {once: true, passive: true});
      const loaded = document.readyState === 'complete' ? null : new Promise(ok => window.addEventListener('load', ok, {once: true}));
      Promise.all([document.fonts && document.fonts.ready, loaded]).then(() => { if (!moved && marks[0].isConnected) place(); });
      requestAnimationFrame(() => marks.forEach(m => m.classList.add('is-on')));
      return true;
    }
  });

  // ---------- câu cần đọc ----------
  // Chữ của một phần tử, đúng như quiz_learn.learn_text: công thức KaTeX viết thành $mã TeX$, khoảng trắng gộp một dấu cách.
  // at[i] là [nút chữ, vị trí trong nút] của ký tự thứ i; ký tự của công thức trỏ tới cả phần tử .katex.
  function learnText(el) {
    let text = '', space = true;
    const at = [];
    (function go(n) {
      for (const k of n.childNodes) {
        if (k.nodeType === 3) {
          for (let i = 0; i < k.data.length; i++) {
            if (/\s/.test(k.data[i])) { if (!space) { text += ' '; at.push([k, i]); } space = true; }
            else { text += k.data[i]; at.push([k, i]); space = false; }
          }
        } else if (k.nodeType === 1 && k.classList.contains('katex')) {
          const t = `$${k.querySelector('annotation')?.textContent || ''}$`;
          text += t; for (let i = 0; i < t.length; i++) at.push([k, -1]);
          space = false;
        } else if (k.nodeType === 1 && !['svg', 'button', 'script', 'style'].includes(k.localName) && !k.classList.contains('out-label')) go(k);
      }
    })(el);
    if (text.endsWith(' ')) { text = text.slice(0, -1); at.pop(); }
    return {text, at};
  }
  let quizById = null;
  function learnSpot(sec, lid, k, qid) {
    if (!qid) return [];
    quizById = quizById || new Map(QB.sets.flatMap(s => s.questions.map(q => [q.id, q])));
    const link = (quizById.get(qid)?.learn || []).find(x => x[0] === lid && x[1] === k);
    const paras = [...sec.querySelectorAll('p, li, figcaption, tr')].filter(p => !p.closest('.quiz'));
    const marks = [];
    for (const quote of (link && link[3]) || []) {
      // đoạn nhỏ nhất chứa câu (một <li> nằm trong <li> khác thì chọn <li> trong)
      const hit = paras.map(p => [p, learnText(p)]).filter(([, t]) => t.text.includes(quote)).sort((x, y) => x[1].text.length - y[1].text.length)[0];
      if (!hit) continue;
      // hàng bảng: tô cả hàng; bọc chữ trong <tr> sẽ chèn phần tử lạ vào giữa các ô
      if (hit[0].localName === 'tr') { const cells = [...hit[0].cells]; cells.forEach(c => c.classList.add('learn-mark')); marks.push(...cells); }
      else marks.push(...markRange(hit[1], hit[1].text.indexOf(quote), quote.length));
      // câu dẫn vào công thức (kết thúc bằng dấu hai chấm ở cuối đoạn): tô luôn các công thức khối ngay sau đoạn
      if (quote.endsWith(':') && hit[1].text.endsWith(quote)) {
        for (let n = hit[0].nextElementSibling; n && n.classList.contains('katex-display'); n = n.nextElementSibling) { n.classList.add('learn-mark'); marks.push(n); }
      }
    }
    return marks;
  }
  // Bọc đoạn chữ [i, i + n) trong <mark class="learn-mark">; công thức thì gắn class lên chính nó.
  function markRange({at}, i, n) {
    const parts = new Map();
    for (let c = i; c < i + n; c++) {
      const [node, off] = at[c];
      const p = parts.get(node);
      if (p) p[1] = off + 1; else parts.set(node, [off, off + 1]);
    }
    const marks = [], run = [];
    // chữ và công thức nội dòng liền nhau vào chung một mark, để dải tô liền mạch
    const flush = () => {
      if (!run.length) return;
      const m = document.createElement('mark');
      m.className = 'learn-mark';
      run[0].before(m);
      m.append(...run.splice(0));
      marks.push(m);
    };
    for (const [node, [lo, hi]] of parts) {
      let piece = node;
      if (node.nodeType === 1) {
        if (node.parentElement.classList.contains('katex-display')) {
          flush();
          node.parentElement.classList.add('learn-mark');
          marks.push(node.parentElement);
          continue;
        }
      } else {
        // khoảng trắng nằm giữa các khối (ô bảng, mục danh sách) không bọc được vào phần tử nội dòng
        if (!node.data.slice(lo, hi).trim() && /^(ul|ol|table|thead|tbody|tr)$/.test(node.parentElement.localName)) continue;
        if (hi < piece.length) piece.splitText(hi);
        if (lo > 0) piece = piece.splitText(lo);
      }
      // thẻ nội dòng (chữ đậm, code...) nằm trọn trong câu thì vào chung dải với chữ hai bên
      while (!piece.previousSibling && !piece.nextSibling && /^(strong|em|b|i|code|a|sub|sup)$/.test(piece.parentElement.localName)) piece = piece.parentElement;
      if (run.length && run[run.length - 1].nextSibling !== piece) flush();
      run.push(piece);
    }
    flush();
    return marks;
  }

  // ---------- events: phần chung trong ui/kit.js ----------
  Object.assign(K.hooks, {
    // Đang làm bài kiểm tra thì không rời trang được, phải nộp bài trước.
    guard() { if (exActive() && route().type !== 'exam') { location.replace('#/exam'); toast('Đang làm bài kiểm tra, nộp bài rồi mới rời được'); return true; } },
    // Tab khác (ví dụ tab bài mở từ “Ôn lại”) vừa ghi kết quả trắc nghiệm: đọc lại để lần ghi sau của tab này không đè mất.
    storage(e) { if (e.key === QKEY) qLoad(); },
    onTheme() {
      const f = $('#slide-frame');
      if (f) try { f.contentDocument.documentElement.dataset.theme = S.theme; } catch (_) { f.src = f.src.split('#')[0] + '#theme=' + S.theme; }
    },
    onQuiz(quiz) { const sec = quiz.closest('.is-check'); if (sec) quizScore(sec); },
    live: ['home', 'phase'],
    pop() {
      const hits = D.lessons.filter(matches).slice(0, 8);
      return S.q.trim()
        ? hits.map(l => a(lessonHref(l.id), `<span class="row-id">${idLabel(l)}</span><span>${esc(l.title)}</span>`, 'class="hit" data-nav')).join('') || '<p class="hit-none">Không có kết quả.</p>'
        : '';
    },
    enter() { const first = D.lessons.find(matches); return first ? lessonHref(first.id) : null; },
    actions: {
      async copy(act, r) {
        const l = findLesson(r.id);
        if (act.dataset.kind === 'lesson' && l?.code) { await K.copyText(l.code); return; }
        const m = l && l.parts[Math.min(Number(r.params.get('part') || 0), l.parts.length - 1)];
        const hw = l && act.dataset.kind === 'starter' ? homeworkOf(l, m) : null;
        if (hw) { await K.copyText(hw.tasks[+act.dataset.index].starter); return; }
        if (m) await K.copyText(act.dataset.kind === 'extra' ? m.extra[+act.dataset.index].code : act.dataset.kind === 'starter' ? m.homework[+act.dataset.index].starter : m.code);
      },
      'quiz-reset'(act) {
        const sec = act.closest('.is-check');
        [...sec.querySelectorAll('.quiz')].forEach(q => {
          q.classList.remove('is-answered');
          q.querySelectorAll('.quiz-opt').forEach(b => { b.classList.remove('is-right', 'is-wrong', 'is-chosen'); b.removeAttribute('aria-disabled'); });
          const why = q.querySelector('.quiz-why'); why.hidden = true; why.querySelector('.quiz-verdict')?.remove();
        });
        quizScore(sec);
        sec.querySelector('.quiz')?.scrollIntoView({behavior: 'smooth', block: 'center'});
      },
      'pr-done'(act) {
        const code = act.dataset.code;
        PS.has(code) ? PS.delete(code) : PS.add(code);
        pSave(); render();
        $(`[data-action="pr-done"][data-code="${code}"]`)?.focus({preventScroll: true});
      },
      'ex-start'(act) { const s = quizSet(act.dataset.set); if (s) exStart(s, Number(act.dataset.n)); },
      'ex-pick'(act) { exPick(Number(act.dataset.choice)); },
      'ex-prev'() { exJump(EX.index - 1, '.qz-nav [data-action="ex-prev"]'); },
      'ex-next'() { exJump(EX.index + 1, '.qz-nav [data-action="ex-next"]'); },
      'ex-jump'(act) { exJump(Number(act.dataset.index), `.qz-cell[data-index="${act.dataset.index}"]`); },
      'ex-submit'() { exAskSubmit(); },
      'qz-level'(act) {
        const id = act.dataset.level, sec = act.closest('.qz-level'), box = document.getElementById(`qzl-${id}`);
        const open = !QL.has(id);
        for (const o of QL) if (o !== id) {
          const b = document.getElementById(`qzl-${o}`);
          if (b) { b.hidden = true; b.closest('.qz-level')?.classList.remove('is-open'); }
          $(`.qz-level-head[data-level="${o}"]`)?.setAttribute('aria-expanded', 'false');
        }
        QL = new Set(open ? [id] : []);
        act.setAttribute('aria-expanded', String(open)); sec.classList.toggle('is-open', open);
        if (box) box.hidden = !open;
      },
      'qz-start'(act) { const s = quizSet(act.dataset.set); if (s) qStart(s, act.dataset.mode); },
      'qz-answer'(act) { if (act.getAttribute('aria-disabled') !== 'true') qAnswer(Number(act.dataset.choice)); },
      'qz-prev'() { qMove(-1); },
      'qz-next'() { qMove(1); },
      'qz-jump'(act) { qJump(Number(act.dataset.index), `.qz-cell[data-index="${act.dataset.index}"]`); },
      'qz-reset'(act) {
        const s = quizSet(act.dataset.set);
        if (s && window.confirm(`Xóa mọi câu trả lời của bộ ${s.title}?`)) {
          QS[s.id] = {answers: {}, mode: null, ids: [], index: 0};
          qSave(); render(); toast(`Đã xóa kết quả bộ ${s.title}`);
        }
      },
      async fullscreen() {
        const f = $('#slide-frame');
        try { await f.requestFullscreen(); f.contentWindow?.focus(); } catch (_) { toast('Trình duyệt chặn toàn màn hình, hãy dùng “Mở tab mới”'); }
      }
    },
    // Trang làm trắc nghiệm và kiểm tra: 1–4 hoặc A–D để chọn, mũi tên trái/phải để chuyển câu.
    keys(e) {
      if (!(e.ctrlKey || e.metaKey || e.altKey || /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) && exActive() && route().type === 'exam') {
        const k = '1234'.indexOf(e.key) >= 0 ? '1234'.indexOf(e.key) : 'abcd'.indexOf(e.key.toLowerCase());
        if (e.key.length === 1 && k >= 0) { e.preventDefault(); exPick(k); }
        else if (e.key === 'ArrowRight' && EX.index < EX.ids.length - 1) { e.preventDefault(); exJump(EX.index + 1); }
        else if (e.key === 'ArrowLeft' && EX.index > 0) { e.preventDefault(); exJump(EX.index - 1); }
        return;
      }
      if (e.ctrlKey || e.metaKey || e.altKey || /INPUT|TEXTAREA|SELECT/.test(e.target.tagName) || !qCurrent()) return;
      const k = '1234'.indexOf(e.key) >= 0 ? '1234'.indexOf(e.key) : 'abcd'.indexOf(e.key.toLowerCase());
      if (e.key.length === 1 && k >= 0) { e.preventDefault(); qAnswer(k); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); qMove(1); }
      else if (e.key === 'ArrowLeft' && qCurrent().st.index > 0) { e.preventDefault(); qMove(-1); }
    },
    // Trên điện thoại, trang làm trắc nghiệm và kiểm tra vuốt ngang để chuyển câu; đang kiểm tra thì khóa thanh bên.
    locked: () => document.documentElement.classList.contains('exam-lock'),
    swipe: {
      when: () => qCurrent() || (exActive() && route().type === 'exam'),
      move(dx) { const card = $('.qz-card'); if (card) card.style.transform = `translateX(${dx * .25}px)`; },
      end(dx, fast) {
        const card = $('.qz-card');
        if (card) { card.style.transition = 'transform .18s ease'; card.style.transform = ''; }
        if (!(Math.abs(dx) > 70 || (fast && Math.abs(dx) > 30))) return;
        const step = dx < 0 ? 1 : -1;
        if (exActive() && route().type === 'exam') { const i = EX.index + step; if (i >= 0 && i < EX.ids.length) exJump(i); }
        else if (qCurrent() && (step > 0 || qCurrent().st.index > 0)) qMove(step);
        document.activeElement?.blur?.();
      }
    }
  });

  window.addEventListener('beforeunload', e => { if (exActive()) { e.preventDefault(); e.returnValue = ''; } });
  initQuiz();
  K.listen();
  const boot = () => {
    if (exActive() && route().type !== 'exam') location.replace('#/exam');
    render();
    K.goSection(route());
    // Nạp sẵn kho trắc nghiệm lúc rảnh để trang Trắc nghiệm mở tức thì.
    const idle = window.requestIdleCallback || (f => setTimeout(f, 1500));
    idle(() => ensureQuiz().catch(() => {}));
  };
  if (!quizReady() && examPending()) ensureQuiz().then(boot, boot); else boot();
})();
