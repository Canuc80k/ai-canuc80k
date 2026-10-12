/* Hình động của giáo trình (lượt 9): chuỗi khung ảnh đóng trong một sprite WebP.
   Tự chạy lặp khi hình hiện trên màn hình, bấm vào hình để dừng/chạy, kéo thanh để xem từng khung.
   Bản in hiện các khung chính cạnh nhau. Dùng chung cho trang bài (app.js) và slide. */
(function () {
  'use strict';
  const reduce = window.matchMedia ? matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  const sysDark = window.matchMedia ? matchMedia('(prefers-color-scheme: dark)') : { matches: false, addEventListener() {} };
  const isDark = () => {
    const t = document.documentElement.getAttribute('data-theme');
    return t ? t === 'dark' : sysDark.matches;
  };
  const ICON = {
    play: '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M5 3.2v9.6L12.6 8z" fill="currentColor"/></svg>',
    pause: '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 3h2.4v10H4.5zM9.1 3h2.4v10H9.1z" fill="currentColor"/></svg>',
  };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmt = s => esc(s).replace(/`([^`]+)`/g, '<code>$1</code>');
  const players = new Set();
  const cache = new Map();

  function load(url) {
    if (!cache.has(url)) cache.set(url, new Promise((ok, fail) => {
      const im = new Image();
      im.decoding = 'async';
      im.onload = () => ok(im);
      im.onerror = fail;
      im.src = url;
    }));
    return cache.get(url);
  }

  class Player {
    constructor(fig) {
      this.fig = fig;
      this.m = JSON.parse(fig.dataset.anim);
      const src = t => fig.querySelector(`a.anim-src[data-v="${t}"]`);
      this.url = { light: src('light').getAttribute('href'), dark: src('dark') ? src('dark').getAttribute('href') : null };
      this.i = 0; this.playing = false; this.userPaused = false; this.visible = false; this.timer = 0; this.img = null;
      const m = this.m;
      this.canvas = fig.querySelector('canvas.anim-stage');
      this.canvas.width = m.w; this.canvas.height = m.h;
      this.canvas.style.maxWidth = `min(100%, ${m.dw}px)`;
      this.canvas.style.aspectRatio = `${m.w} / ${m.h}`;
      fig.style.setProperty('--ar', (m.w / m.h).toFixed(4));
      const bar = fig.querySelector('.anim-bar');
      bar.innerHTML = `<button type="button" class="anim-play" aria-label="Phát">${ICON.play}</button>`
        + `<input class="anim-seek" type="range" min="0" max="${m.n - 1}" value="0" step="1" aria-label="Chọn khung hình">`
        + `<span class="anim-label" aria-live="off"></span>`;
      this.btn = bar.querySelector('.anim-play');
      this.seek = bar.querySelector('.anim-seek');
      this.label = bar.querySelector('.anim-label');
      bar.style.maxWidth = `min(100%, ${Math.max(m.dw, 420)}px)`;
      this.btn.addEventListener('click', () => this.toggle());
      this.canvas.addEventListener('click', () => this.toggle());
      this.seek.addEventListener('input', () => { this.pause(true); this.show(+this.seek.value); });
      this.keys = fig.querySelector('.anim-keys');
      // trên slide, khung rộng (từ 1.9 : 1) in tối đa 2 cột cho đủ lớn; trang bài giữ số cột của recipe
      this.keys.style.setProperty('--pcols', fig.closest('.deck') && m.w / m.h >= 1.9 ? Math.min(2, m.pcols) : m.pcols);
      this.keys.innerHTML = m.key.map(k => `<div class="anim-key"><canvas width="${m.w}" height="${m.h}"></canvas>`
        + `<span>${fmt(m.labels[k] || '')}</span></div>`).join('');
      this.setLabel(0);
    }
    theme() { return isDark() && this.url.dark ? 'dark' : 'light'; }
    ensure() {
      const t = this.theme();
      if (this.loading === t) return this.ready;
      this.loading = t;
      this.ready = load(this.url[t]).then(im => { if (this.loading === t) { this.img = im; this.draw(); this.drawKeys(); } return im; });
      return this.ready;
    }
    blit(ctx, k) {
      const m = this.m, c = k % m.cols, r = Math.floor(k / m.cols);
      ctx.clearRect(0, 0, m.w, m.h);
      ctx.drawImage(this.img, c * m.w, r * m.h, m.w, m.h, 0, 0, m.w, m.h);
    }
    draw() { if (this.img) this.blit(this.canvas.getContext('2d'), this.i); }
    drawKeys() {
      if (!this.img) return;
      this.keys.querySelectorAll('canvas').forEach((cv, j) => this.blit(cv.getContext('2d'), this.m.key[j]));
    }
    setLabel(k) {
      const m = this.m;
      this.label.innerHTML = `<span class="anim-step">${k + 1}/${m.n}</span>${m.labels[k] ? ' ' + fmt(m.labels[k]) : ''}`;
      this.seek.setAttribute('aria-valuetext', `Khung ${k + 1}/${m.n}${m.labels[k] ? ': ' + m.labels[k] : ''}`);
    }
    show(k) {
      this.i = k; this.seek.value = k; this.setLabel(k); this.draw();
    }
    dur(k) {
      const d = this.m.dur;
      return (Array.isArray(d) ? d[k] : d) + (k === this.m.n - 1 ? this.m.hold : 0);
    }
    tick() {
      clearTimeout(this.timer);
      if (!this.playing) return;
      this.timer = setTimeout(() => {
        if (!this.playing) return;
        this.show((this.i + 1) % this.m.n);
        this.tick();
      }, this.dur(this.i));
    }
    play() {
      if (this.playing) return;
      this.playing = true; this.userPaused = false;
      this.btn.innerHTML = ICON.pause; this.btn.setAttribute('aria-label', 'Tạm dừng');
      this.fig.classList.add('is-playing');
      this.ensure().then(() => this.tick());
    }
    pause(byUser) {
      if (byUser) this.userPaused = true;
      if (!this.playing) return;
      this.playing = false; clearTimeout(this.timer);
      this.btn.innerHTML = ICON.play; this.btn.setAttribute('aria-label', 'Phát');
      this.fig.classList.remove('is-playing');
    }
    toggle() { if (this.playing) this.pause(true); else { if (this.i === this.m.n - 1) this.show(0); this.play(); } }
    seen(v) {
      this.visible = v;
      if (v) { this.ensure(); if (!this.userPaused && !reduce.matches) this.play(); }
      else this.pause(false);
    }
  }

  const near = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) e.target._anim && e.target._anim.ensure();
  }), { rootMargin: '600px 0px' }) : null;
  const view = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => {
    e.target._anim && e.target._anim.seen(e.isIntersecting);
  }), { threshold: 0.45 }) : null;

  function scan(root) {
    // trang bài vẽ lại cả khối khi đổi route: bỏ player của hình đã rời trang
    players.forEach(p => { if (!p.fig.isConnected) { p.pause(false); near && near.unobserve(p.fig); view && view.unobserve(p.fig); players.delete(p); } });
    (root || document).querySelectorAll('figure.anim[data-anim]').forEach(fig => {
      if (fig._anim) return;
      const p = new Player(fig);
      fig._anim = p; players.add(p);
      if (near) { near.observe(fig); view.observe(fig); } else p.ensure();
    });
  }
  function retheme() { players.forEach(p => { if (p.img || p.loading) p.ensure(); }); }
  new MutationObserver(retheme).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  sysDark.addEventListener && sysDark.addEventListener('change', retheme);
  // Xuất PDF: nạp mọi sprite và vẽ khung chính trước khi in.
  function readyAll() { return Promise.all([...players].map(p => p.ensure().catch(() => null))); }
  window.Anim = { scan, readyAll };
})();
