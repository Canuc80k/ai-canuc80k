(() => {
  'use strict';
  // Lõi chung của các trang Canuc80k (AI, Thuật toán, ...): khung trang, thanh bên, thanh trên, tìm kiếm, chủ đề sáng/tối,
  // khối code và nút Chạy, mục lục bám cuộn, nạp dữ liệu theo nhu cầu, cử chỉ trên điện thoại.
  // Nguồn: tools/site-kit/kit.js. Mỗi trang nhận bản chép ui/kit.js qua tools/site-kit/sync.py; không sửa bản chép.
  // Mỗi trang gọi Kit.create({...}) trong ui/app.js, gắn trang và móc riêng vào đối tượng trả về rồi gọi start().

  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
  const fold = value => String(value).normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D').toLowerCase();
  const words = text => fold(text).replace(/[-_/,;:()]+/g, ' ').split(/\s+/).filter(Boolean);
  const sleep = ms => new Promise(ok => setTimeout(ok, ms));

  const ICONS = {
    route: '<path d="M6 19a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM18 9a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"/><path d="M8 17h7.5a3.5 3.5 0 0 0 0-7h-7a3.5 3.5 0 0 1 0-7H16"/>',
    book: '<path d="M5 4.5A1.5 1.5 0 0 1 6.5 3H19v15H6.5A1.5 1.5 0 0 0 5 19.5z"/><path d="M5 19.5A1.5 1.5 0 0 0 6.5 21H19v-3"/>',
    quiz: '<rect x="4" y="4" width="16" height="16" rx="3.5"/><path d="m8.5 12.2 2.5 2.5 4.5-5"/>',
    trophy: '<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5v1.5A3 3 0 0 0 8 10.5M16 6h3v1.5a3 3 0 0 1-3 3M12 13v4m-3.5 3h7"/>',
    practice: '<rect x="3.5" y="5" width="17" height="14" rx="2.5"/><path d="m7.5 10 2.5 2.25-2.5 2.25M12.5 14.5h4"/>',
    search: '<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/>',
    arrow: '<path d="M5 12h14m-5-5 5 5-5 5"/>',
    back: '<path d="M19 12H5m5-5-5 5 5 5"/>',
    external: '<path d="M14 4h6v6m0-6-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    check: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    circle: '<circle cx="12" cy="12" r="8.5"/>',
    done: '<circle cx="12" cy="12" r="8.5"/><path d="m8.5 12.2 2.5 2.5 4.5-5"/>',
    download: '<path d="M12 4v11m-4.5-4.5L12 15l4.5-4.5M5 20h14"/>',
    copy: '<rect x="8.5" y="8.5" width="11" height="11" rx="2"/><path d="M15.5 8.5V6a1.5 1.5 0 0 0-1.5-1.5H6A1.5 1.5 0 0 0 4.5 6v8A1.5 1.5 0 0 0 6 15.5h2.5"/>',
    wrap: '<path d="M4 7h16M4 12h13a3 3 0 0 1 0 6h-4m2-2-2 2 2 2M4 17h5"/>',
    expand: '<path d="M4 9V4h5m6 0h5v5M4 15v5h5m6 0h5v-5"/>',
    menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
    chev: '<path d="m9.5 6.5 5.5 5.5-5.5 5.5"/>',
    panel: '<rect x="3.5" y="4.5" width="17" height="15" rx="2.5"/><path d="M9.5 4.5v15"/>',
    up: '<path d="M12 19V5m-6 6 6-6 6 6"/>',
    close: '<path d="m6 6 12 12M18 6 6 18"/>',
    moon: '<path d="M19.5 14.5A8 8 0 0 1 9.5 4.5a8 8 0 1 0 10 10z"/>',
    sun: '<circle cx="12" cy="12" r="3.75"/><path d="M12 3v2m0 14v2M3 12h2m14 0h2M5.6 5.6 7 7m10 10 1.4 1.4M5.6 18.4 7 17M17 7l1.4-1.4"/>',
    play: '<path d="M8 5.8v12.4a.8.8 0 0 0 1.2.7l10-6.2a.8.8 0 0 0 0-1.4l-10-6.2A.8.8 0 0 0 8 5.8z"/>',
    replay: '<path d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3M4.5 4.5v3.8h3.8"/>',
    notebook: '<rect x="5" y="3.5" width="14" height="17" rx="2.5"/><path d="M9 3.5v17M12.5 8h3M12.5 11.5h3"/>',
    flag: '<path d="M5.5 21V4.5m0 0h11l-2 4 2 4h-11"/>',
    send: '<path d="M4.5 12 20 4.5 15.5 20l-3-6.5z"/><path d="m12.5 13.5 3-3"/>',
    bulb: '<path d="M9 18h6m-5 3h4"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.6.5 1.1 1.2 1.1 2V16h5v-.2c0-.8.5-1.5 1.1-2A6 6 0 0 0 12 3z"/>'
  };
  // Logo: ba con cá nục chụm đuôi.
  const MARK = `<svg class="logo" viewBox="-29.72 -11 40.73 37.48" aria-hidden="true"><defs><mask id="lg0" maskUnits="userSpaceOnUse" x="-29.72" y="-11" width="40.73" height="37.48"><rect x="-29.72" y="-11" width="40.73" height="37.48" fill="#fff"/><path transform="translate(0 0) rotate(-26) scale(0.6 0.5) translate(-50 -32)" d="M3 32C9 25.5 16 23 24 23c9 0 16.5 3.6 22.5 7.2C47.5 31 47.5 33 46.5 33.8C40.5 37.4 33 41 24 41 16 41 9 38.5 3 32z" fill="#000" stroke="#000" stroke-width="5" stroke-linejoin="round"/><path transform="translate(0 0) rotate(-46) scale(0.6 0.5) translate(-50 -32)" d="M3 32C9 25.5 16 23 24 23c9 0 16.5 3.6 22.5 7.2C47.5 31 47.5 33 46.5 33.8C40.5 37.4 33 41 24 41 16 41 9 38.5 3 32z" fill="#000" stroke="#000" stroke-width="5" stroke-linejoin="round"/></mask><mask id="lg1" maskUnits="userSpaceOnUse" x="-29.72" y="-11" width="40.73" height="37.48"><rect x="-29.72" y="-11" width="40.73" height="37.48" fill="#fff"/><path transform="translate(0 0) rotate(-46) scale(0.6 0.5) translate(-50 -32)" d="M3 32C9 25.5 16 23 24 23c9 0 16.5 3.6 22.5 7.2C47.5 31 47.5 33 46.5 33.8C40.5 37.4 33 41 24 41 16 41 9 38.5 3 32z" fill="#000" stroke="#000" stroke-width="5" stroke-linejoin="round"/></mask></defs><g mask="url(#lg0)"><g transform="translate(0 0) rotate(-6) scale(0.6 0.5) translate(-50 -32)"><path d="M3 32C9 25.5 16 23 24 23c9 0 16.5 3.6 22.5 7.2C47.5 31 47.5 33 46.5 33.8C40.5 37.4 33 41 24 41 16 41 9 38.5 3 32z" fill="#D97757"/><ellipse cx="12.4" cy="30.4" rx="4.3" ry="5.16" fill="#FAF9F5"/><ellipse cx="11.8" cy="30.6" rx="2.2" ry="2.64" fill="#1F1E1C"/></g></g><g mask="url(#lg1)"><g transform="translate(0 0) rotate(-26) scale(0.6 0.5) translate(-50 -32)"><path d="M3 32C9 25.5 16 23 24 23c9 0 16.5 3.6 22.5 7.2C47.5 31 47.5 33 46.5 33.8C40.5 37.4 33 41 24 41 16 41 9 38.5 3 32z" fill="#D97757"/><ellipse cx="12.4" cy="30.4" rx="4.3" ry="5.16" fill="#FAF9F5"/><ellipse cx="11.8" cy="30.6" rx="2.2" ry="2.64" fill="#1F1E1C"/></g></g><g><g transform="translate(0 0) rotate(-46) scale(0.6 0.5) translate(-50 -32)"><path d="M3 32C9 25.5 16 23 24 23c9 0 16.5 3.6 22.5 7.2L58.8 18c1-.9 2.6-.1 2.3 1.2L56 32l5.1 12.8c.3 1.3-1.3 2.1-2.3 1.2L46.5 33.8C40.5 37.4 33 41 24 41 16 41 9 38.5 3 32z" fill="#D97757"/><ellipse cx="12.4" cy="30.4" rx="4.3" ry="5.16" fill="#FAF9F5"/><ellipse cx="11.8" cy="30.6" rx="2.2" ry="2.64" fill="#1F1E1C"/></g></g></svg>`;
  const icon = name => `<svg class="i" viewBox="0 0 24 24" aria-hidden="true">${ICONS[name]}</svg>`;
  const a = (href, html, attrs = '') => `<a href="${esc(href)}" ${attrs}>${html}</a>`;
  const meter = (n, total) => `<span class="meter" aria-hidden="true"><i style="width:${total ? n / total * 100 : 0}%"></i></span>`;
  const here = html => `<span aria-current="page">${html}</span>`;
  // Hàng trước/sau cuối trang: prev, next = {href, label, title}; label là chữ nhỏ cạnh mũi tên (có thể rỗng).
  const pager = (aria, prev, next) => `<nav class="pager" aria-label="${aria}">${prev ? a(prev.href, `<small>${icon('back')}${prev.label ? ' ' + prev.label : ''}</small><span>${esc(prev.title)}</span>`, 'class="pager-link" data-nav') : '<span></span>'}${next ? a(next.href, `<small>${next.label ? next.label + ' ' : ''}${icon('arrow')}</small><span>${esc(next.title)}</span>`, 'class="pager-link is-next" data-nav') : ''}</nav>`;

  // ---------- nạp dữ liệu theo nhu cầu ----------
  const scriptCache = new Map();
  function loadScript(src) {
    if (!scriptCache.has(src)) scriptCache.set(src, new Promise((ok, fail) => {
      const s = document.createElement('script');
      s.src = src; s.async = true;
      s.onload = ok; s.onerror = () => { scriptCache.delete(src); fail(new Error(src)); };
      document.head.appendChild(s);
    }));
    return scriptCache.get(src);
  }

  // ---------- tô màu code ----------
  function paint(code, pattern, kind) {
    code = code.normalize('NFC');
    let html = '', cursor = 0;
    for (const m of code.matchAll(pattern)) {
      html += esc(code.slice(cursor, m.index));
      html += `<span class="t-${kind(m[0])}">${esc(m[0])}</span>`;
      cursor = m.index + m[0].length;
    }
    return html + esc(code.slice(cursor));
  }
  const PY_RE = /#.*?$|'''[\s\S]*?'''|"""[\s\S]*?"""|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'|\b(?:def|return|import|from|for|in|if|else|elif|class|True|False|None|with|as|assert|try|except|finally|raise|lambda|and|or|not|is|while|pass|break|continue|yield|global|nonlocal)\b|\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b/gm;
  const highlightPy = code => paint(code, PY_RE, t => t.startsWith('#') ? 'c' : (t[0] === '"' || t[0] === "'") ? 's' : /^\d/.test(t) ? 'n' : 'k');
  // C++: chú thích, chỉ thị tiền xử lý, chuỗi, ký tự, từ khóa, kiểu, số.
  const CPP_KW = 'alignas|alignof|auto|bool|break|case|catch|char|class|const|constexpr|continue|default|delete|do|double|else|enum|explicit|extern|false|float|for|friend|goto|if|inline|int|long|mutable|namespace|new|noexcept|nullptr|operator|private|protected|public|register|return|short|signed|sizeof|static|static_assert|struct|switch|template|this|throw|true|try|typedef|typename|union|unsigned|using|virtual|void|volatile|while|int64_t|uint64_t|int32_t|uint32_t|size_t|__int128';
  const CPP_RE = new RegExp(String.raw`\/\/.*?$|\/\*[\s\S]*?\*\/|^[ \t]*#\s*\w+[^\n]*$|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])+'|\b(?:${CPP_KW})\b|\b(?:0x[\da-fA-F]+|\d+(?:\.\d+)?(?:e[+-]?\d+)?)(?:[uUlLfF]*)\b`, 'gm');
  const highlightCpp = code => paint(code, CPP_RE, t => { const s = t.trimStart(); return s.startsWith('//') || s.startsWith('/*') ? 'c' : s.startsWith('#') ? 'p' : (t[0] === '"' || t[0] === "'") ? 's' : /^\d/.test(t) ? 'n' : 'k'; });
  // Gộp các mảng trong cùng (không lồng) về một dòng; chỉ bỏ xuống dòng + thụt lề, không đổi giá trị.
  const compactJSON = text => text.replace(/\[([^\[\]{}]*)\]/g, (m, inner) => inner.includes('\n') ? `[${inner.replace(/\n\s*/g, ' ').trim()}]` : m);
  const looksJSON = text => /^\s*[\[{]/.test(text);
  const looksPython = text => /^(import |from |def |class |print\(|#|for |[A-Za-z_][\w]*\s*=)/m.test(text) && !looksJSON(text);

  // Công thức dài trên màn hình hẹp: thu nhỏ vừa khung (tối đa còn 66%), quá nữa thì cuộn ngang.
  function fitMath() {
    $$('.theory .katex-display > .katex').forEach(k => {
      k.style.fontSize = '';
      const box = k.parentElement, ratio = box.clientWidth / box.scrollWidth;
      if (ratio < 1) k.style.fontSize = `${Math.max(.66, ratio * .98) * parseFloat(getComputedStyle(k).fontSize)}px`;
    });
  }
  function wrapTables(root) {
    $$(`${root} table`).forEach(t => { if (!t.parentElement.classList.contains('table-wrap')) { const w = document.createElement('div'); w.className = 'table-wrap'; t.replaceWith(w); w.appendChild(t); } });
  }
  const NO_MOTION = !!navigator.webdriver || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);

  // ---------- một trang ----------
  // cfg: key (localStorage), sub (chữ nhỏ cạnh logo), search (chữ gợi ý ô tìm), navLabel (aria của danh sách chương),
  // copyFail (thông báo khi không sao chép được), findLesson(id), nameLabel(l),
  // load(saved) -> phần trạng thái riêng, dump(S) -> phần riêng cần lưu.
  // cfg cũng là nơi giữ móc của trang (K.hooks): trang gán thêm views, tree, crumbs... trước khi gọi start().
  function create(cfg) {
    const KEY = cfg.key, H = cfg;
    H.actions = H.actions || {};
    H.live = H.live || [];
    let saved = {};
    let canStore = true;
    try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (_) { canStore = false; }
    const S = {
      q: '',
      done: new Set((saved.done || []).filter(H.findLesson)),
      last: H.findLesson(saved.last) ? saved.last : null,
      theme: saved.theme === 'dark' || saved.theme === 'light' ? saved.theme : null,
      side: saved.side === 'closed' ? 'closed' : 'open',
      wrap: false,
      // Nhóm đang mở trên thanh bên chỉ sống trong một lần mở trang; mở lại thì chỉ nhóm của bài đang xem được mở.
      open: new Set(),
      ...(H.load ? H.load(saved) : {})
    };
    const systemDark = () => window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const effectiveTheme = () => S.theme || (systemDark() ? 'dark' : 'light');
    function applyTheme() {
      if (S.theme) document.documentElement.dataset.theme = S.theme;
      else delete document.documentElement.dataset.theme;
    }
    applyTheme();
    const applySide = () => { document.documentElement.dataset.side = S.side; };
    applySide();
    function store(key, value) {
      if (!canStore) return;
      try { localStorage.setItem(key, JSON.stringify(value)); } catch (_) { canStore = false; }
    }
    const persist = () => store(KEY, {done: [...S.done], last: S.last, theme: S.theme, side: S.side, ...(H.dump ? H.dump(S) : {})});
    function route() {
      const [path, query = ''] = location.hash.replace(/^#/, '').split('?');
      const bits = (path || '/').split('/').filter(Boolean);
      return {type: bits[0] || 'home', id: bits[1], sub: bits[2], params: new URLSearchParams(query)};
    }

    let toastTimer;
    function toast(text) {
      const box = $('#toast');
      box.textContent = text;
      box.classList.add('show');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => box.classList.remove('show'), 2200);
    }
    function openMenu() { $('#side').classList.add('open'); $('#scrim').classList.add('show'); $('#menu-btn').setAttribute('aria-expanded', 'true'); }
    function closeMenu() { $('#side').classList.remove('open'); $('#scrim').classList.remove('show'); $('#menu-btn').setAttribute('aria-expanded', 'false'); }
    function setQuery(value) { S.q = value; $('#q').value = value; $('#search-pop').innerHTML = ''; }

    // Thanh bên, đường dẫn, tiến độ, nút sáng/tối. Trang cho biết:
    // H.nav: [[khóa, biểu tượng, nhãn, href]], H.section(r) -> khóa đang sáng,
    // H.tree(r) -> {phase, lesson, sections: [{label, title?, phases: [{id, short, items: [{href, id, title, done, draft}]}]}]},
    // H.crumbs(r) -> [html], H.progress() -> {html, title}.
    function chrome(r) {
      const section = H.section(r);
      $('#side-nav').innerHTML = H.nav.map(([key, i, label, href]) => a(href, `${icon(i)}<span>${label}</span>`,
        `class="side-link${section === key ? ' is-active' : ''}" data-nav`)).join('');

      const tree = H.tree(r), activePhase = tree.phase === null || tree.phase === undefined ? null : String(tree.phase), cur = tree.lesson;
      if (chrome.lastPhase !== activePhase) S.open = new Set(activePhase === null ? [] : [activePhase]);
      chrome.lastPhase = activePhase;
      const phaseNav = p => {
        const id = String(p.id), open = S.open.has(id);
        const items = p.items.map(x => {
          const on = cur !== null && cur !== undefined && x.id === cur;
          return a(x.href,
            `<span class="side-lesson-id">${x.label}</span><span class="side-lesson-name">${esc(x.title)}</span>${x.done ? `<span class="side-lesson-done">${icon('check')}</span>` : ''}`,
            `class="side-lesson${on ? ' is-active' : ''}${x.draft ? ' is-draft' : ''}" title="${esc(x.title)}"${on ? ' aria-current="page"' : ''} data-nav`);
        }).join('');
        return `<div class="side-group${activePhase === id ? ' is-current' : ''}">
        <button class="side-phase" type="button" data-action="toggle-phase" data-phase="${id}" aria-expanded="${open}" aria-controls="sp-${id}">
          <span class="side-phase-num">${p.num ?? p.id}</span><span class="side-phase-name">${esc(p.short)}</span>${icon('chev')}
        </button>
        <div class="side-lessons" id="sp-${id}" data-open="${open}"><div class="side-lessons-inner">
          ${items}
        </div></div>
      </div>`;
      };
      $('#phase-nav').innerHTML = tree.sections.map(k =>
        `<div class="side-label"${k.title ? ` title="${esc(k.title)}"` : ''}>${k.label}</div>` + k.phases.map(phaseNav).join('')).join('');
      const activeLink = $('.side-lesson.is-active');
      if (activeLink && chrome.lastLesson !== cur) {
        const box = $('.side-scroll'), r1 = activeLink.getBoundingClientRect(), r2 = box.getBoundingClientRect();
        if (r1.top < r2.top || r1.bottom > r2.bottom) box.scrollTop += r1.top - r2.top - r2.height / 3;
      }
      chrome.lastLesson = cur ?? null;

      $('#crumbs').innerHTML = H.crumbs(r).join('<span class="crumb-sep" aria-hidden="true">/</span>');
      const pg = H.progress();
      $('#top-progress').innerHTML = pg.html;
      $('#top-progress').title = pg.title;
      const dark = effectiveTheme() === 'dark';
      $('#theme-btn').innerHTML = icon(dark ? 'sun' : 'moon');
      $('#theme-btn').setAttribute('aria-label', dark ? 'Chuyển sang nền sáng' : 'Chuyển sang nền tối');
      $('#theme-btn').title = dark ? 'Nền sáng' : 'Nền tối';
    }

    // ---------- khối code trong bài ----------
    // Bọc <pre><code> thành khối có tên ngôn ngữ, nút sao chép (và nút ngắt dòng nếu wrap).
    function codeFigure(code, name, paintFn, wrap = false) {
      const pre = code.parentElement, fig = document.createElement('figure');
      fig.className = 'code t-code';
      fig.innerHTML = `<figcaption class="code-head"><span class="code-name">${name}</span><span class="code-tools">
        <button class="tool" data-action="copy-block" title="Sao chép" aria-label="Sao chép">${icon('copy')}</button>${wrap ? `<button class="tool" data-action="wrap" title="Ngắt dòng" aria-label="Ngắt dòng" aria-pressed="${S.wrap}">${icon('wrap')}</button>` : ''}</span></figcaption>`;
      pre.replaceWith(fig);
      pre.className = `code-body${wrap && S.wrap ? ' is-wrap' : ''}`;
      code.innerHTML = paintFn(code.textContent);
      fig.appendChild(pre);
      return fig;
    }
    // Khối kết quả (và input) ngay sau code: ```output, ```input.
    function ioBlocks(root, labels) {
      $$(`${root} pre > code.language-output, ${root} pre > code.language-input`).forEach(code => {
        const pre = code.parentElement, kind = code.classList.contains('language-input') ? 'in' : 'out';
        pre.className = labels.io ? `out io-${kind}` : 'out';
        pre.insertAdjacentHTML('afterbegin', `<span class="out-label" aria-hidden="true">${kind === 'in' ? labels.in : labels.out}</span>`);
      });
    }
    // Nút Chạy: kết quả đã chạy thật lúc soạn bài, ẩn đi; bấm Chạy thì in ra từng dòng (giảm chuyển động thì in ngay).
    function prepRun(fig, out = fig.nextElementSibling) {
      const code = out.querySelector('code');
      if (!code) return;
      fig.classList.add('can-run');
      out.dataset.text = code.textContent.replace(/\n$/, '');
      out.hidden = true;
      fig.querySelector('.code-tools').insertAdjacentHTML('afterbegin', `<button class="run-btn" data-action="run">${icon('play')}Chạy</button>`);
    }
    // Gắn nút Chạy cho khối code có output ngay sau (hoặc input rồi output).
    function linkRun(fig) {
      const nx = fig.nextElementSibling;
      if (nx && nx.classList.contains('out')) fig.classList.add('has-out');
      if (nx && nx.classList.contains('io-in') && nx.nextElementSibling?.classList.contains('io-out')) { nx.classList.add('io-mid'); prepRun(fig, nx.nextElementSibling); }
      else if (nx && nx.classList.contains('out') && !nx.classList.contains('io-in')) prepRun(fig, nx);
    }
    async function runBlock(fig) {
      if (!fig || fig.classList.contains('is-running')) return;
      let out = fig.nextElementSibling;
      if (out && out.classList.contains('io-in')) out = out.nextElementSibling;
      const code = out.querySelector('code');
      fig.classList.add('is-running');
      out.hidden = false; code.textContent = '';
      if (NO_MOTION) { code.textContent = out.dataset.text; fig.classList.remove('is-running'); return; }
      await sleep(180);
      const rows = out.dataset.text.split('\n'), per = Math.min(40, 400 / rows.length);
      for (let k = 0; k < rows.length; k++) {
        if (!code.isConnected) return;
        code.textContent += (k ? '\n' : '') + rows[k];
        if (per >= 4) await sleep(per);
      }
      fig.classList.remove('is-running');
    }
    async function copyText(text) {
      try {
        if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(text);
        else {
          const t = document.createElement('textarea');
          t.value = text; t.style.position = 'fixed'; t.style.opacity = '0';
          document.body.appendChild(t); t.select();
          const ok = document.execCommand('copy'); t.remove();
          if (!ok) throw new Error('copy');
        }
        toast('Đã sao chép');
      } catch (_) { toast(cfg.copyFail || 'Không sao chép được'); }
    }

    // ---------- mục lục bám cuộn ----------
    let spyHeads = [], spyLinks = [];
    function spyUpdate() {
      if (!spyHeads.length) return;
      const line = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--top-h')) + 90;
      let cur = spyHeads[0];
      for (const h of spyHeads) { if (h.getBoundingClientRect().top <= line) cur = h; else break; }
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) cur = spyHeads[spyHeads.length - 1];
      spyLinks.forEach(x => x.classList.toggle('is-active', x.dataset.scroll === cur.id));
    }
    function spy() { spyHeads = $$('#lesson-doc h2'); spyLinks = $$('.toc a'); spyUpdate(); }

    // ---------- vẽ trang ----------
    // H.views: {loại trang: r => html}, H.needs(r) -> [promise], H.before(r) -> true nếu bỏ lần vẽ, H.after(r) sau khi gắn DOM.
    function skeleton() {
      setTimeout(() => { const x = $('#main .loading'); if (x) x.hidden = false; }, 400);
      return '<div class="page" aria-busy="true"><p class="loading" hidden>Đang tải…</p></div>';
    }
    const notFound = () => `<div class="page"><div class="empty"><p>Không tìm thấy trang này.</p>${a('#/', 'Về lộ trình', 'class="btn" data-nav')}</div></div>`;
    render.token = 0;
    function render() {
      const r = route();
      if (H.before && H.before(r)) return;
      const wait = H.needs ? H.needs(r) : [];
      if (wait.length) {
        const token = ++render.token;
        chrome(r);
        $('#main').innerHTML = skeleton();
        Promise.all(wait).then(() => {
          if (token !== render.token) return;
          render();
          goSection(route());
        }, () => {
          if (token === render.token) $('#main').innerHTML = `<div class="page"><div class="empty"><p>Không tải được nội dung. Kiểm tra mạng rồi thử lại.</p><button class="btn" data-action="reload">Thử lại</button></div></div>`;
        });
        return;
      }
      ++render.token;
      chrome(r);
      const view = H.views[r.type];
      spyHeads = []; spyLinks = [];
      $('#main').innerHTML = view ? view(r) : notFound();
      if (H.after) H.after(r);
    }
    // ?sec=k: cuộn tới mục thứ k của bài và nhấn sáng mục đó; H.spot(r, sec, h, k) -> true nếu trang tự xử lý.
    function goSection(r) {
      const k = r.type === 'lesson' && !r.params.get('tab') ? r.params.get('sec') : null;
      const h = k !== null && $(`#sec-${Number(k)}`);
      if (!h) return false;
      const sec = h.closest('.t-sec') || h;
      if (H.spot && H.spot(r, sec, h, Number(k))) return true;
      h.scrollIntoView({block: 'start'});
      sec.classList.remove('is-target'); void sec.offsetWidth; sec.classList.add('is-target');
      return true;
    }

    // ---------- khung trang ----------
    $('#app').innerHTML = `
    <a class="skip" href="#main" data-scroll="main">Đến nội dung chính</a>
    <aside class="side" id="side" aria-label="Điều hướng">
      <div class="side-head">
        <a class="wordmark" href="#/" data-nav>${MARK}Canuc80k<span class="wordmark-sub">${cfg.sub}</span></a>
        <button class="icon-btn side-collapse" data-action="sidebar" aria-label="Ẩn thanh bên" title="Ẩn thanh bên">${icon('panel')}</button>
        <button class="icon-btn side-close" data-action="menu-close" aria-label="Đóng menu">${icon('close')}</button>
      </div>
      <nav class="side-nav" id="side-nav"></nav>
      <div class="side-scroll">
        <nav id="phase-nav" aria-label="${cfg.navLabel}"></nav>
      </div>
    </aside>
    <button class="scrim" id="scrim" data-action="menu-close" aria-label="Đóng menu" tabindex="-1"></button>
    <div class="shell">
      <header class="top">
        <button class="icon-btn menu-btn" id="menu-btn" data-action="menu" aria-expanded="false" aria-controls="side" aria-label="Mở menu">${icon('menu')}</button>
        <button class="icon-btn side-open" data-action="sidebar" aria-label="Hiện thanh bên" title="Hiện thanh bên">${icon('panel')}</button>
        <nav class="crumbs" id="crumbs" aria-label="Vị trí"></nav>
        <div class="top-tools">
          <div class="search">
            <label class="search-box">${icon('search')}<input id="q" type="search" autocomplete="off" spellcheck="false" placeholder="${cfg.search}" aria-label="${cfg.search}"></label>
            <div class="search-pop" id="search-pop" role="listbox"></div>
          </div>
          <span class="top-progress" id="top-progress"></span>
          <button class="icon-btn" id="theme-btn" data-action="theme"></button>
        </div>
      </header>
      <main class="main" id="main" tabindex="-1"></main>
    </div>
    <div class="toast" id="toast" role="status" aria-live="polite"></div>`;

    // ---------- sự kiện ----------
    // H.guard() -> true để chặn đổi trang, H.storage(e), H.actions {tên: (nút, r) => ...}, H.keys(e),
    // H.live: loại trang lọc tại chỗ khi gõ tìm, H.pop() -> html gợi ý, H.enter() -> href khi Enter,
    // H.swipe {when(), move(dx), end(dx, fast)}: vuốt ngang riêng của trang, H.locked() -> true khi khóa thanh bên.
    function listen() {
      if (document.fonts) { document.fonts.ready.then(fitMath); document.fonts.addEventListener?.('loadingdone', fitMath); }
      let fitTick = 0;
      window.addEventListener('resize', () => { clearTimeout(fitTick); fitTick = setTimeout(fitMath, 120); });
      let spyTick = false;
      window.addEventListener('scroll', () => { if (!spyTick) { spyTick = true; requestAnimationFrame(() => { spyTick = false; spyUpdate(); }); } }, {passive: true});

      let prevRoute = route();
      window.addEventListener('hashchange', () => {
        if (H.guard && H.guard()) return;
        const next = route();
        const sameLesson = prevRoute.type === 'lesson' && next.type === 'lesson' && prevRoute.id === next.id;
        const keepY = window.scrollY;
        closeMenu(); $('#search-pop').innerHTML = ''; render();
        if (goSection(next)) { prevRoute = next; return; }
        if (sameLesson) {
          const tabs = $('.tabs');
          const top = tabs ? tabs.getBoundingClientRect().top + window.scrollY - parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--top-h')) : 0;
          window.scrollTo(0, Math.min(keepY, top));
        } else window.scrollTo(0, 0);
        prevRoute = next;
      });
      // Tab khác vừa ghi tiến độ: đọc lại để lần ghi sau của tab này không đè mất.
      window.addEventListener('storage', e => {
        if (e.key === KEY) {
          try {
            const v = JSON.parse(e.newValue || '{}');
            S.done = new Set((v.done || []).filter(H.findLesson));
            if (H.findLesson(v.last)) S.last = v.last;
            if (H.load) Object.assign(S, H.load(v));
          } catch (_) {}
        } else if (H.storage) H.storage(e);
      });
      if (window.matchMedia) window.matchMedia('(prefers-color-scheme: dark)').addEventListener?.('change', () => { if (!S.theme) chrome(route()); });

      $('#q').addEventListener('input', e => {
        S.q = e.target.value;
        const r = route();
        if (H.live.includes(r.type)) { render(); $('#q').focus(); return; }
        $('#search-pop').innerHTML = H.pop();
      });
      $('#q').addEventListener('keydown', e => {
        if (e.key === 'Escape') { $('#search-pop').innerHTML = ''; e.target.blur(); }
        if (e.key === 'ArrowDown') { const first = $('#search-pop .hit'); if (first) { e.preventDefault(); first.focus(); } }
        if (e.key === 'Enter' && !H.live.includes(route().type)) {
          const href = H.enter();
          if (href) { setQuery(''); location.hash = href; }
        }
      });
      $('#search-pop').addEventListener('keydown', e => {
        const hits = $$('#search-pop .hit'), i = hits.indexOf(document.activeElement);
        if (e.key === 'ArrowDown' && i < hits.length - 1) { e.preventDefault(); hits[i + 1].focus(); }
        if (e.key === 'ArrowUp') { e.preventDefault(); i > 0 ? hits[i - 1].focus() : $('#q').focus(); }
      });

      document.addEventListener('click', async e => {
        if (!e.target.closest('.search')) $('#search-pop').innerHTML = '';
        const nav = e.target.closest('[data-nav]');
        if (nav) { setQuery(''); closeMenu(); if (nav.getAttribute('href') === location.hash) render(); }
        const scroll = e.target.closest('[data-scroll]');
        if (scroll) { e.preventDefault(); const el = document.getElementById(scroll.dataset.scroll); if (el) { el.scrollIntoView({behavior: 'smooth', block: 'start'}); if (el.id === 'main') el.focus({preventScroll: true}); } return; }
        const act = e.target.closest('[data-action]');
        if (!act) return;
        const r = route(), l = H.findLesson(r.id);
        switch (act.dataset.action) {
          case 'menu': $('#side').classList.contains('open') ? closeMenu() : openMenu(); break;
          case 'sidebar': {
            const root = document.documentElement;
            root.classList.add('side-anim');
            S.side = S.side === 'open' ? 'closed' : 'open'; applySide(); persist();
            clearTimeout(window.__sideAnim); window.__sideAnim = setTimeout(() => root.classList.remove('side-anim'), 320);
            break;
          }
          case 'toggle-phase': {
            // Mở một nhóm thì đóng các nhóm khác, để thanh bên luôn gọn.
            const id = act.dataset.phase, open = !S.open.has(id);
            for (const o of S.open) if (o !== id) {
              $(`.side-phase[data-phase="${o}"]`)?.setAttribute('aria-expanded', 'false');
              const box = $(`#sp-${o}`); if (box) box.dataset.open = 'false';
            }
            S.open = new Set(open ? [id] : []);
            act.setAttribute('aria-expanded', open);
            $(`#sp-${id}`).dataset.open = open;
            break;
          }
          case 'menu-close': closeMenu(); break;
          case 'reload': render(); break;
          case 'run': runBlock(act.closest('figure.t-code')); break;
          case 'theme': S.theme = effectiveTheme() === 'dark' ? 'light' : 'dark'; applyTheme(); persist(); chrome(r); if (H.onTheme) H.onTheme(); break;
          case 'clear-search': setQuery(''); render(); break;
          case 'complete': if (l) {
            const now = !S.done.has(l.id);
            now ? S.done.add(l.id) : S.done.delete(l.id);
            persist(); render();
            toast(now ? `Đã đánh dấu ${H.nameLabel(l)} là đã học` : `Đã bỏ đánh dấu ${H.nameLabel(l)}`);
          } break;
          case 'wrap': S.wrap = !S.wrap; $$('.code-body').forEach(x => x.classList.toggle('is-wrap', S.wrap)); $$('[data-action="wrap"]').forEach(x => x.setAttribute('aria-pressed', S.wrap)); break;
          case 'copy-block': await copyText(act.closest('figure').querySelector('pre').textContent); break;
          // Câu hỏi nhanh trong bài: chọn một lần, hiện đúng/sai và lời giải thích.
          case 'quiz': {
            const quiz = act.closest('.quiz');
            if (quiz.classList.contains('is-answered')) break;
            quiz.classList.add('is-answered');
            quiz.querySelectorAll('.quiz-opt').forEach(b => {
              if (b === act) b.classList.add('is-chosen');
              if (b.dataset.correct === '1') b.classList.add('is-right');
              else if (b === act) b.classList.add('is-wrong');
              b.setAttribute('aria-disabled', 'true');
            });
            const why = quiz.querySelector('.quiz-why');
            why.hidden = false;
            why.insertAdjacentHTML('afterbegin', `<p class="quiz-verdict">${act.dataset.correct === '1' ? 'Chính xác.' : 'Chưa đúng.'}</p>`);
            if (H.onQuiz) H.onQuiz(quiz);
            break;
          }
          default: if (H.actions[act.dataset.action]) await H.actions[act.dataset.action](act, r);
        }
      });
      document.addEventListener('keydown', e => {
        if (e.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) { e.preventDefault(); $('#q').focus(); }
        if (e.key === 'Escape') { closeMenu(); $('#search-pop').innerHTML = ''; }
        if (H.keys) H.keys(e);
      });

      // Cử chỉ trên điện thoại: vuốt từ mép trái để mở thanh bên, vuốt sang trái để đóng; trang có thể thêm vuốt ngang riêng (H.swipe).
      const side = $('#side'), scrim = $('#scrim');
      const narrow = () => window.matchMedia('(max-width: 920px)').matches;
      const hScroll = el => {
        for (; el && el !== document.body; el = el.parentElement)
          if (el.scrollWidth > el.clientWidth + 2 && /auto|scroll/.test(getComputedStyle(el).overflowX)) return true;
        return false;
      };
      let t = null;
      document.addEventListener('touchstart', e => {
        t = null;
        if (e.touches.length !== 1) return;
        const p = e.touches[0], open = side.classList.contains('open');
        let kind = null;
        if (narrow() && !(H.locked && H.locked())) {
          if (open && (side.contains(e.target) || e.target === scrim)) kind = 'close';
          else if (!open && p.clientX < 28) kind = 'open';
        }
        if (!kind && !open && H.swipe && H.swipe.when() && !hScroll(e.target) && !e.target.closest('input, textarea, select')) kind = 'page';
        if (kind) t = {kind, x: p.clientX, y: p.clientY, at: Date.now(), axis: null, dx: 0, w: side.offsetWidth || 280};
      }, {passive: true});
      document.addEventListener('touchmove', e => {
        if (!t) return;
        const p = e.touches[0], dx = p.clientX - t.x, dy = p.clientY - t.y;
        if (!t.axis) {
          if (Math.abs(dx) < 8 && Math.abs(dy) < 8) return;
          t.axis = Math.abs(dx) > Math.abs(dy) * 1.2 ? 'x' : 'y';
          if (t.axis === 'y') { t = null; return; }
          if (t.kind !== 'page') { side.style.transition = scrim.style.transition = 'none'; scrim.classList.add('show'); }
        }
        t.dx = dx;
        if (t.kind === 'page') { H.swipe.move(dx); return; }
        const off = t.kind === 'open' ? Math.max(-t.w, Math.min(0, dx - t.w)) : Math.max(-t.w, Math.min(0, dx));
        side.style.transform = `translateX(${off}px)`;
        scrim.style.opacity = String(1 + off / t.w);
      }, {passive: true});
      const end = () => {
        const g = t; t = null;
        if (!g || g.axis !== 'x') return;
        const dx = g.dx, fast = Math.abs(dx) / Math.max(1, Date.now() - g.at) > .5;
        if (g.kind === 'page') { H.swipe.end(dx, fast); return; }
        side.style.transition = scrim.style.transition = side.style.transform = scrim.style.opacity = '';
        const pass = d => d > g.w / 3 || (fast && d > 20);
        (g.kind === 'open' ? pass(dx) : !pass(-dx)) ? openMenu() : closeMenu();
      };
      document.addEventListener('touchend', end, {passive: true});
      document.addEventListener('touchcancel', end, {passive: true});
    }

    // Trang gắn móc (nav, section, tree, crumbs, progress, views, live, pop, enter, actions, ...) rồi gọi start().
    const K = {
      S, saved, KEY, store, persist, route, toast, openMenu, closeMenu, setQuery, chrome, render, goSection, spy, notFound,
      effectiveTheme, applyTheme, codeFigure, ioBlocks, prepRun, linkRun, runBlock, copyText, listen, hooks: H,
      canStore: () => canStore,
      start() { listen(); render(); goSection(route()); }
    };
    return K;
  }

  window.Kit = {create, $, $$, esc, fold, words, sleep, ICONS, MARK, icon, a, meter, here, pager, loadScript,
    highlightPy, highlightCpp, compactJSON, looksJSON, looksPython, fitMath, wrapTables, NO_MOTION};
})();
