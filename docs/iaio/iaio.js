// Trang luyện đề IAIO: ba đề 100 câu, 180 phút, có câu nhiều đáp án. Bài làm lưu trong máy người xem.
(() => {
  const D = window.IAIO, $ = s => document.querySelector(s), app = $('#app');
  const LETTERS = 'ABCD';
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const arrow = '<svg class="i" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  const KEY = id => `iaio.v1.${id}`;
  const load = id => { try { return JSON.parse(localStorage.getItem(KEY(id)) || 'null'); } catch (_) { return null; } };
  const save = (id, st) => { try { localStorage.setItem(KEY(id), JSON.stringify(st)); } catch (_) {} };
  const drop = id => { try { localStorage.removeItem(KEY(id)); } catch (_) {} };
  const setOf = id => D.sets.find(s => s.id === id);
  const same = (a, b) => a.length === b.length && a.every(x => b.includes(x));
  const left = (s, st) => Math.max(0, st.start + s.minutes * 60000 - Date.now());
  const clock = ms => { const t = Math.ceil(ms / 1000), h = Math.floor(t / 3600), m = Math.floor(t / 60) % 60, x = t % 60; return `${h}:${String(m).padStart(2, '0')}:${String(x).padStart(2, '0')}`; };
  const score = (s, st) => s.questions.filter(q => same(st.answers[q.id] || [], q.answer)).length;
  let tick = 0, view = 'all';

  function route() {
    const [id, sub] = location.hash.replace(/^#\/?/, '').split('/');
    clearInterval(tick);
    const s = setOf(id);
    if (!s) return home();
    const st = load(s.id);
    if (st && (st.done || sub === 'ket-qua')) return result(s, st || {answers: {}});
    exam(s, st);
  }

  function home() {
    document.title = 'IAIO · Luyện đề';
    app.innerHTML = `<h1>IAIO</h1><div class="ia-sets">${D.sets.map((s, k) => {
      const st = load(s.id);
      const meta = !st ? `${s.questions.length} câu · ${s.minutes} phút`
        : st.done ? `Đã nộp · ${score(s, st)}/${s.questions.length}`
        : `Đang làm · còn ${clock(left(s, st))}`;
      return `<a class="ia-set" href="#/${s.id}"><span class="ia-set-num">${k + 1}</span><span class="ia-set-title">${esc(s.title)}</span><span class="ia-set-meta">${meta}</span>${arrow}</a>`;
    }).join('')}</div>`;
  }

  function qHtml(q, n, st, review) {
    const pick = st.answers[q.id] || [];
    const opts = q.options.map((o, k) => {
      let cls = pick.includes(k) ? ' is-on' : '';
      if (review) cls = (q.answer.includes(k) ? ' is-right' : '') + (pick.includes(k) ? (q.answer.includes(k) ? ' is-picked' : ' is-wrong') : '');
      return `<li><button type="button" class="ia-opt${cls}" data-q="${q.id}" data-k="${k}"${review ? ' disabled' : ''}><span class="ia-key">${LETTERS[k]}</span><span>${esc(o)}</span></button></li>`;
    }).join('');
    const ok = same(pick, q.answer);
    const why = review ? `<p class="ia-why"><span class="ia-verdict ${ok ? 'ok' : 'no'}">${ok ? 'Đúng.' : pick.length ? `Sai. Đáp án: ${q.answer.map(k => LETTERS[k]).join(', ')}.` : `Bỏ trống. Đáp án: ${q.answer.map(k => LETTERS[k]).join(', ')}.`}</span> ${esc(q.why)}</p>` : '';
    return `<section class="ia-q${q.multi ? ' is-multi' : ''}" id="q${n}">
      <div class="ia-q-head"><span class="ia-q-num">Câu ${n}</span>${q.multi ? '<span class="ia-q-tag">Nhiều đáp án</span>' : ''}</div>
      <p class="ia-q-stem">${esc(q.q)}</p><ol class="ia-opts">${opts}</ol>${why}</section>`;
  }

  function exam(s, st) {
    if (!st) { st = {start: Date.now(), answers: {}}; save(s.id, st); }
    document.title = `${s.title} · IAIO`;
    const n = () => Object.values(st.answers).filter(a => a.length).length;
    app.innerHTML = `<div class="ia-bar"><span class="ia-bar-title">${esc(s.title)}</span><span class="ia-bar-count" id="cnt">${n()}/${s.questions.length}</span>
        <span class="ia-timer" id="timer">${clock(left(s, st))}</span><button class="btn is-primary" type="button" data-act="submit">Nộp bài</button></div>
      ${s.questions.map((q, i) => qHtml(q, i + 1, st, false)).join('')}
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
        const q = s.questions.find(x => x.id === opt.dataset.q), k = Number(opt.dataset.k);
        let a = st.answers[q.id] || [];
        a = q.multi ? (a.includes(k) ? a.filter(x => x !== k) : [...a, k].sort()) : (a[0] === k ? [] : [k]);
        st.answers[q.id] = a; save(s.id, st);
        opt.closest('.ia-opts').querySelectorAll('.ia-opt').forEach(b => b.classList.toggle('is-on', a.includes(Number(b.dataset.k))));
        const i = s.questions.indexOf(q);
        app.querySelector(`[data-go="${i + 1}"]`).classList.toggle('is-done', a.length > 0);
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
    st.done = true; st.end = Math.min(Date.now(), st.start + s.minutes * 60000); save(s.id, st);
    view = 'all';
    location.hash = `#/${s.id}/ket-qua`;
    route(); window.scrollTo(0, 0);
  }

  function result(s, st) {
    document.title = `${s.title} · Kết quả · IAIO`;
    const right = score(s, st), total = s.questions.length;
    const used = st.end ? clock(st.end - st.start) : '';
    const rows = Object.entries(D.muc).map(([m, name]) => {
      const qs = s.questions.filter(q => String(q.muc) === m);
      if (!qs.length) return '';
      return `<div class="ia-row"><b>${m}</b><span>${esc(name)}</span><span>${qs.filter(q => same(st.answers[q.id] || [], q.answer)).length}/${qs.length}</span></div>`;
    }).join('');
    const list = s.questions.map((q, i) => [q, i]).filter(([q]) => view === 'all' || !same(st.answers[q.id] || [], q.answer));
    app.innerHTML = `<a class="ia-back" href="#/">IAIO</a><h1>${esc(s.title)}</h1>
      <p class="ia-score">${right}/${total} câu đúng${used ? ` · ${used}` : ''}</p>
      <div class="ia-rows">${rows}</div>
      <div class="ia-grid">${s.questions.map((q, i) => `<button type="button" class="ia-cell ${same(st.answers[q.id] || [], q.answer) ? 'is-right' : 'is-wrong'}" data-go="${i + 1}">${i + 1}</button>`).join('')}</div>
      <div class="ia-end"><button class="btn" type="button" data-act="redo">Làm lại</button><a class="ia-link" href="#/">Về danh sách đề</a></div>
      <div class="ia-tabs"><button class="ia-tab${view === 'all' ? ' is-on' : ''}" data-view="all">Tất cả</button><button class="ia-tab${view === 'wrong' ? ' is-on' : ''}" data-view="wrong">Câu sai ${total - right}</button></div>
      ${list.map(([q, i]) => qHtml(q, i + 1, st, true)).join('')}`;
    app.onclick = e => {
      const go = e.target.closest('[data-go]'), tab = e.target.closest('[data-view]'), act = e.target.closest('[data-act]');
      if (go) { if (view !== 'all') { view = 'all'; result(s, st); } document.getElementById(`q${go.dataset.go}`).scrollIntoView({behavior: 'smooth', block: 'start'}); }
      if (tab) { view = tab.dataset.view; const y = window.scrollY; result(s, st); window.scrollTo(0, y); }
      if (act && act.dataset.act === 'redo' && confirm('Xóa bài đã làm và bắt đầu lại?')) { drop(s.id); location.hash = `#/${s.id}`; }
    };
  }

  window.addEventListener('hashchange', () => { route(); window.scrollTo(0, 0); });
  route();
})();
