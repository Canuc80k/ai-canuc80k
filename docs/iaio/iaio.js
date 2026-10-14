// Trang luyện đề IAIO: ba đề 100 câu. Hai chế độ: luyện tập (từng câu, chấm ngay) và thi thử (180 phút, nộp bài mới chấm).
// Bài làm lưu trong máy người xem; nền sáng/tối dùng chung cài đặt với trang chính.
(() => {
  const D = window.IAIO, $ = s => document.querySelector(s), app = $('#app'), root = document.documentElement;
  const LETTERS = 'ABCD';
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const ICON = {
    moon: '<path d="M19.5 14.5A8 8 0 0 1 9.5 4.5a8 8 0 1 0 10 10z"/>',
    sun: '<circle cx="12" cy="12" r="3.75"/><path d="M12 3v2m0 14v2M3 12h2m14 0h2M5.6 5.6 7 7m10 10 1.4 1.4M5.6 18.4 7 17M17 7l1.4-1.4"/>',
    back: '<path d="M19 12H5m5-5-5 5 5 5"/>', arrow: '<path d="M5 12h14m-5-5 5 5-5 5"/>'
  };
  const icon = n => `<svg class="i" viewBox="0 0 24 24" aria-hidden="true">${ICON[n]}</svg>`;
  const get = k => { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (_) { return null; } };
  const put = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (_) {} };
  const del = k => { try { localStorage.removeItem(k); } catch (_) {} };
  const EK = id => `iaio.v1.${id}`, PK = id => `iaio.v1.${id}.luyen`;
  const setOf = id => D.sets.find(s => s.id === id);
  const same = (a, b) => a.length === b.length && a.every(x => b.includes(x));
  const left = (s, st) => Math.max(0, st.start + s.minutes * 60000 - Date.now());
  const clock = ms => { const t = Math.ceil(ms / 1000), h = Math.floor(t / 3600), m = Math.floor(t / 60) % 60, x = t % 60; return `${h}:${String(m).padStart(2, '0')}:${String(x).padStart(2, '0')}`; };
  const score = (s, ans) => s.questions.filter(q => same(ans[q.id] || [], q.answer)).length;
  let tick = 0, view = 'all';

  // ---------- nền sáng/tối ----------
  const isDark = () => (root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')) === 'dark';
  const themeBtn = () => `<button class="icon-btn ia-theme" type="button" data-theme-toggle aria-label="${isDark() ? 'Chuyển sang nền sáng' : 'Chuyển sang nền tối'}" title="${isDark() ? 'Nền sáng' : 'Nền tối'}">${icon(isDark() ? 'sun' : 'moon')}</button>`;
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-theme-toggle]');
    if (!b) return;
    const t = isDark() ? 'light' : 'dark';
    root.dataset.theme = t;
    const p = get('aicanuc80k.portal.v2') || {}; p.theme = t; put('aicanuc80k.portal.v2', p);
    document.querySelectorAll('[data-theme-toggle]').forEach(x => { x.outerHTML = themeBtn(); });
  });

  function route() {
    const [id, sub] = location.hash.replace(/^#\/?/, '').split('/');
    clearInterval(tick); app.onclick = null; document.onkeydown = null;
    const s = setOf(id);
    if (!s) return home();
    if (sub === 'luyen') return practice(s);
    const st = get(EK(s.id));
    if (sub === 'thi' && !(st && st.done)) return exam(s, st);
    if (st && st.done) return result(s, st);
    location.replace(`#/${s.id}/thi`);
  }

  // ---------- trang chọn đề ----------
  function home() {
    document.title = 'IAIO · Luyện đề';
    app.innerHTML = `<div class="ia-head"><h1>IAIO</h1>${themeBtn()}</div><div class="ia-sets">${D.sets.map((s, k) => {
      const st = get(EK(s.id)), pr = get(PK(s.id)), n = s.questions.length;
      const done = pr ? Object.keys(pr.checked || {}).length : 0;
      const meta = [done ? `Luyện ${done}/${n}` : `${n} câu`,
        !st ? `${s.minutes} phút` : st.done ? `Thi thử ${score(s, st.answers)}/${n}` : `Đang thi · còn ${clock(left(s, st))}`].join(' · ');
      return `<section class="ia-set"><span class="ia-set-num">${k + 1}</span>
        <span class="ia-set-body"><span class="ia-set-title">${esc(s.title)}</span><span class="ia-set-meta">${meta}</span></span>
        <span class="ia-set-acts"><a class="btn" href="#/${s.id}/luyen">Luyện tập</a><a class="btn is-primary" href="#/${s.id}/${st && st.done ? 'ket-qua' : 'thi'}">${st && st.done ? 'Kết quả' : 'Thi thử'}</a></span></section>`;
    }).join('')}</div>`;
  }

  // ---------- một câu hỏi ----------
  // mode: 'exam' (chọn, chưa chấm), 'review' (đã chấm, có lời giải)
  function qHtml(q, n, pick, mode, extra = '') {
    const review = mode === 'review';
    const opts = q.options.map((o, k) => {
      let cls = pick.includes(k) ? ' is-on' : '';
      if (review) cls = (q.answer.includes(k) ? ' is-right' : '') + (pick.includes(k) ? (q.answer.includes(k) ? ' is-picked' : ' is-wrong') : '');
      return `<li><button type="button" class="ia-opt${cls}" data-q="${q.id}" data-k="${k}"${review ? ' disabled' : ''}><span class="ia-key">${LETTERS[k]}</span><span>${esc(o)}</span></button></li>`;
    }).join('');
    const ok = same(pick, q.answer), key = q.answer.map(k => LETTERS[k]).join(', ');
    const why = review ? `<p class="ia-why"><span class="ia-verdict ${ok ? 'ok' : 'no'}">${ok ? 'Đúng.' : pick.length ? `Sai. Đáp án: ${key}.` : `Bỏ trống. Đáp án: ${key}.`}</span> ${esc(q.why)}</p>` : '';
    return `<section class="ia-q${q.multi ? ' is-multi' : ''}" id="q${n}">
      <div class="ia-q-head"><span class="ia-q-num">Câu ${n}</span>${q.multi ? '<span class="ia-q-tag">Nhiều đáp án</span>' : ''}${extra}</div>
      <p class="ia-q-stem">${esc(q.q)}</p><ol class="ia-opts">${opts}</ol>${why}</section>`;
  }
  const toggle = (q, a, k) => q.multi ? (a.includes(k) ? a.filter(x => x !== k) : [...a, k].sort()) : (a[0] === k ? [] : [k]);

  // ---------- luyện tập: từng câu, chấm ngay ----------
  function practice(s) {
    const n = s.questions.length;
    const st = get(PK(s.id)) || {index: 0, answers: {}, checked: {}};
    st.index = Math.min(Math.max(0, st.index || 0), n - 1);
    const save = () => put(PK(s.id), st);
    document.title = `${s.title} · Luyện tập · IAIO`;

    function draw() {
      const q = s.questions[st.index], pick = st.answers[q.id] || [], done = !!st.checked[q.id];
      const checked = Object.keys(st.checked), right = checked.filter(id => { const x = s.questions.find(y => y.id === id); return same(st.answers[id] || [], x.answer); }).length;
      app.innerHTML = `<div class="ia-head"><a class="ia-back" href="#/">IAIO</a>${themeBtn()}</div>
        <h1>${esc(s.title)}</h1>
        <p class="ia-score">Luyện tập · ${checked.length}/${n} câu · ${right} đúng</p>
        <div class="ia-practice">${qHtml(q, st.index + 1, pick, done ? 'review' : 'exam', `<span class="ia-q-muc">${esc(D.muc[q.muc])}</span>`)}
          ${!done && q.multi ? `<div class="ia-check"><button class="btn is-primary" type="button" data-act="check"${pick.length ? '' : ' disabled'}>Kiểm tra</button></div>` : ''}</div>
        <nav class="ia-nav"><button class="btn" type="button" data-act="prev"${st.index ? '' : ' disabled'}>${icon('back')}Câu trước</button>
          <button class="btn${done ? ' is-primary' : ''}" type="button" data-act="next"${st.index < n - 1 ? '' : ' disabled'}>Câu tiếp${icon('arrow')}</button></nav>
        <div class="ia-grid">${s.questions.map((x, i) => {
          const c = st.checked[x.id] ? (same(st.answers[x.id] || [], x.answer) ? ' is-right' : ' is-wrong') : '';
          return `<button type="button" class="ia-cell${c}${i === st.index ? ' is-cur' : ''}" data-jump="${i}">${i + 1}</button>`;
        }).join('')}</div>
        <div class="ia-end"><button class="ia-link" type="button" data-act="reset">Làm lại từ đầu</button></div>`;
    }
    const go = i => { if (i < 0 || i >= n) return; st.index = i; save(); draw(); window.scrollTo(0, 0); };
    const check = () => { const q = s.questions[st.index]; if (!(st.answers[q.id] || []).length) return; st.checked[q.id] = true; save(); draw(); };
    const pickK = k => {
      const q = s.questions[st.index];
      if (st.checked[q.id]) return;
      st.answers[q.id] = toggle(q, st.answers[q.id] || [], k);
      if (!q.multi) st.checked[q.id] = true;
      save(); draw();
    };
    app.onclick = e => {
      const opt = e.target.closest('.ia-opt'), act = e.target.closest('[data-act]'), jump = e.target.closest('[data-jump]');
      if (opt && !opt.disabled) pickK(Number(opt.dataset.k));
      if (jump) go(Number(jump.dataset.jump));
      if (!act) return;
      if (act.dataset.act === 'check') check();
      if (act.dataset.act === 'prev') go(st.index - 1);
      if (act.dataset.act === 'next') go(st.index + 1);
      if (act.dataset.act === 'reset' && confirm('Xóa toàn bộ câu đã luyện của đề này?')) { st.index = 0; st.answers = {}; st.checked = {}; save(); draw(); }
    };
    document.onkeydown = e => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      const k = '1234'.indexOf(e.key) >= 0 ? '1234'.indexOf(e.key) : 'abcd'.indexOf(e.key.toLowerCase());
      if (e.key.length === 1 && k >= 0) { e.preventDefault(); pickK(k); }
      else if (e.key === 'Enter' && s.questions[st.index].multi) { e.preventDefault(); check(); }
      else if (e.key === 'ArrowRight') go(st.index + 1);
      else if (e.key === 'ArrowLeft') go(st.index - 1);
    };
    // vuốt ngang trên điện thoại để chuyển câu
    let tx = null;
    app.ontouchstart = e => { tx = e.touches.length === 1 && !e.target.closest('.ia-q-stem') ? [e.touches[0].clientX, e.touches[0].clientY] : null; };
    app.ontouchend = e => {
      if (!tx) return;
      const dx = e.changedTouches[0].clientX - tx[0], dy = e.changedTouches[0].clientY - tx[1]; tx = null;
      if (Math.abs(dx) > 70 && Math.abs(dx) > 1.5 * Math.abs(dy)) go(st.index + (dx < 0 ? 1 : -1));
    };
    draw();
  }

  // ---------- thi thử: 180 phút ----------
  function exam(s, st) {
    if (!st) { st = {start: Date.now(), answers: {}}; put(EK(s.id), st); }
    if (!left(s, st)) return finish(s, st);
    document.title = `${s.title} · Thi thử · IAIO`;
    const n = () => Object.values(st.answers).filter(a => a.length).length;
    app.innerHTML = `<div class="ia-bar"><span class="ia-bar-title">${esc(s.title)}</span><span class="ia-bar-count" id="cnt">${n()}/${s.questions.length}</span>
        <span class="ia-timer" id="timer">${clock(left(s, st))}</span>${themeBtn()}<button class="btn is-primary" type="button" data-act="submit">Nộp bài</button></div>
      ${s.questions.map((q, i) => qHtml(q, i + 1, st.answers[q.id] || [], 'exam')).join('')}
      <div class="ia-grid">${s.questions.map((q, i) => `<button type="button" class="ia-cell${(st.answers[q.id] || []).length ? ' is-done' : ''}" data-go="${i + 1}">${i + 1}</button>`).join('')}</div>
      <div class="ia-end"><button class="btn is-primary" type="button" data-act="submit">Nộp bài</button><a class="ia-link" href="#/">Về danh sách đề</a></div>`;
    const timer = $('#timer');
    tick = setInterval(() => {
      const ms = left(s, st);
      timer.textContent = clock(ms); timer.classList.toggle('is-low', ms < 600000);
      if (!ms) finish(s, st);
    }, 1000);
    app.onclick = e => {
      const opt = e.target.closest('.ia-opt'), go = e.target.closest('[data-go]'), act = e.target.closest('[data-act]');
      if (opt && !opt.disabled) {
        const q = s.questions.find(x => x.id === opt.dataset.q), a = toggle(q, st.answers[q.id] || [], Number(opt.dataset.k));
        st.answers[q.id] = a; put(EK(s.id), st);
        opt.closest('.ia-opts').querySelectorAll('.ia-opt').forEach(b => b.classList.toggle('is-on', a.includes(Number(b.dataset.k))));
        app.querySelector(`[data-go="${s.questions.indexOf(q) + 1}"]`).classList.toggle('is-done', a.length > 0);
        $('#cnt').textContent = `${n()}/${s.questions.length}`;
      }
      if (go) document.getElementById(`q${go.dataset.go}`).scrollIntoView({behavior: 'smooth', block: 'start'});
      if (act && act.dataset.act === 'submit') {
        const miss = s.questions.length - n();
        if (confirm(miss ? `Còn ${miss} câu bỏ trống. Nộp bài?` : 'Nộp bài?')) finish(s, st);
      }
    };
  }

  function finish(s, st) {
    clearInterval(tick);
    st.done = true; st.end = Math.min(Date.now(), st.start + s.minutes * 60000); put(EK(s.id), st);
    view = 'all';
    location.hash = `#/${s.id}/ket-qua`;
    window.scrollTo(0, 0);
  }

  function result(s, st) {
    document.title = `${s.title} · Kết quả · IAIO`;
    const right = score(s, st.answers), total = s.questions.length;
    const ok = q => same(st.answers[q.id] || [], q.answer);
    const rows = Object.entries(D.muc).map(([m, name]) => {
      const qs = s.questions.filter(q => String(q.muc) === m);
      return qs.length ? `<div class="ia-row"><b>${m}</b><span>${esc(name)}</span><span>${qs.filter(ok).length}/${qs.length}</span></div>` : '';
    }).join('');
    const list = s.questions.map((q, i) => [q, i]).filter(([q]) => view === 'all' || !ok(q));
    app.innerHTML = `<div class="ia-head"><a class="ia-back" href="#/">IAIO</a>${themeBtn()}</div><h1>${esc(s.title)}</h1>
      <p class="ia-score">Thi thử · ${right}/${total} câu đúng${st.end ? ` · ${clock(st.end - st.start)}` : ''}</p>
      <div class="ia-rows">${rows}</div>
      <div class="ia-grid">${s.questions.map((q, i) => `<button type="button" class="ia-cell ${ok(q) ? 'is-right' : 'is-wrong'}" data-go="${i + 1}">${i + 1}</button>`).join('')}</div>
      <div class="ia-end"><button class="btn" type="button" data-act="redo">Thi lại</button><a class="ia-link" href="#/">Về danh sách đề</a></div>
      <div class="ia-tabs"><button class="ia-tab${view === 'all' ? ' is-on' : ''}" data-view="all">Tất cả</button><button class="ia-tab${view === 'wrong' ? ' is-on' : ''}" data-view="wrong">Câu sai ${total - right}</button></div>
      ${list.map(([q, i]) => qHtml(q, i + 1, st.answers[q.id] || [], 'review')).join('')}`;
    app.onclick = e => {
      const go = e.target.closest('[data-go]'), tab = e.target.closest('[data-view]'), act = e.target.closest('[data-act]');
      if (go) { if (view !== 'all') { view = 'all'; result(s, st); } document.getElementById(`q${go.dataset.go}`).scrollIntoView({behavior: 'smooth', block: 'start'}); }
      if (tab) { view = tab.dataset.view; const y = window.scrollY; result(s, st); window.scrollTo(0, y); }
      if (act && act.dataset.act === 'redo' && confirm('Xóa bài thi đã nộp và thi lại từ đầu?')) { del(EK(s.id)); location.hash = `#/${s.id}/thi`; }
    };
  }

  window.addEventListener('hashchange', () => { route(); window.scrollTo(0, 0); });
  route();
})();
