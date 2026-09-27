/* EOD course simulator toolkit — shared by every sim in sims/.
   Exposes window.EOD = { rng, plot, ui, debrief, util }. No dependencies. */
(function () {
  'use strict';

  // ------------------------------------------------------------------ util
  var util = {
    clamp: function (x, a, b) { return Math.max(a, Math.min(b, x)); },
    lerp: function (a, b, t) { return a + (b - a) * t; },
    fmt: function (x, d) {
      if (!isFinite(x)) return String(x);
      d = d === undefined ? 3 : d;
      var a = Math.abs(x);
      if (a !== 0 && (a < 1e-3 || a >= 1e5)) return x.toExponential(Math.max(1, d - 1));
      return x.toFixed(d);
    },
    param: function (name, dflt) {
      var m = new RegExp('[?&]' + name + '=([^&]*)').exec(location.search);
      return m ? decodeURIComponent(m[1]) : dflt;
    },
    el: function (tag, attrs, html) {
      var e = document.createElement(tag);
      if (attrs) Object.keys(attrs).forEach(function (k) {
        if (k === 'class') e.className = attrs[k];
        else if (k.indexOf('on') === 0) e.addEventListener(k.slice(2), attrs[k]);
        else e.setAttribute(k, attrs[k]);
      });
      if (html !== undefined) e.innerHTML = html;
      return e;
    },
    $: function (sel, root) { return (root || document).querySelector(sel); },
    esc: function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  };

  // ------------------------------------------------------------------ seeded RNG
  function rng(seed) {
    var s = (seed >>> 0) || 1;
    function next() { // mulberry32
      s = (s + 0x6D2B79F5) >>> 0;
      var t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    }
    var spare = null;
    return {
      seed: seed,
      uniform: function (a, b) { a = a || 0; b = b === undefined ? 1 : b; return a + (b - a) * next(); },
      int: function (a, b) { return a + Math.floor(next() * (b - a + 1)); },
      normal: function (mu, sd) {
        mu = mu || 0; sd = sd === undefined ? 1 : sd;
        if (spare !== null) { var v = spare; spare = null; return mu + sd * v; }
        var u, w, r;
        do { u = 2 * next() - 1; w = 2 * next() - 1; r = u * u + w * w; } while (r >= 1 || r === 0);
        var f = Math.sqrt(-2 * Math.log(r) / r);
        spare = w * f;
        return mu + sd * u * f;
      },
      bernoulli: function (p) { return next() < p; },
      poisson: function (lam) {
        var L = Math.exp(-lam), k = 0, p = 1;
        do { k++; p *= next(); } while (p > L);
        return k - 1;
      },
      pick: function (arr) { return arr[Math.floor(next() * arr.length)]; },
      shuffle: function (arr) {
        for (var i = arr.length - 1; i > 0; i--) { var j = Math.floor(next() * (i + 1)); var t = arr[i]; arr[i] = arr[j]; arr[j] = t; }
        return arr;
      },
      next: next
    };
  }
  function seedFromUrl() {
    var s = util.param('seed', null);
    return s ? parseInt(s, 10) : Math.floor(Math.random() * 1e9);
  }

  // ------------------------------------------------------------------ canvas plotting
  function hidpi(canvas, h) {
    var dpr = window.devicePixelRatio || 1;
    var w = canvas.clientWidth || canvas.parentElement.clientWidth || 600;
    h = h || canvas.clientHeight || 260;
    canvas.style.height = h + 'px';
    var cw = Math.round(w * dpr), ch = Math.round(h * dpr);
    if (canvas.width !== cw) canvas.width = cw;       // reallocating a canvas every frame is expensive
    if (canvas.height !== ch) canvas.height = ch;
    var ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, w: w, h: h };
  }

  function niceTicks(lo, hi, n) {
    var span = hi - lo; if (span <= 0) return [lo];
    var step = Math.pow(10, Math.floor(Math.log10(span / n)));
    var err = n / span * step;
    if (err <= 0.15) step *= 10; else if (err <= 0.35) step *= 5; else if (err <= 0.75) step *= 2;
    var out = [];
    for (var v = Math.ceil(lo / step) * step; v <= hi + 1e-9 * span; v += step) out.push(+v.toPrecision(12));
    return out;
  }

  /* plot(canvas, {x:[lo,hi], y:[lo,hi], logX, logY, xlabel, ylabel, series:[{x:[],y:[],color,width,dash,label}],
                   points:[{x,y,color,r,label}], vlines:[{x,color,label}], hlines:[{y,color,label}], height}) */
  function plot(canvas, o) {
    var g = hidpi(canvas, o.height), ctx = g.ctx, W = g.w, H = g.h;
    var m = { l: 58, r: 14, t: 12, b: 36 };
    var pw = W - m.l - m.r, ph = H - m.t - m.b;
    var tx = o.logX ? function (v) { return Math.log10(v); } : function (v) { return v; };
    var ty = o.logY ? function (v) { return Math.log10(v); } : function (v) { return v; };
    var x0 = tx(o.x[0]), x1 = tx(o.x[1]), y0 = ty(o.y[0]), y1 = ty(o.y[1]);
    function X(v) { return m.l + (tx(v) - x0) / (x1 - x0) * pw; }
    function Y(v) { return m.t + ph - (ty(v) - y0) / (y1 - y0) * ph; }
    ctx.fillStyle = '#070a0e'; ctx.fillRect(0, 0, W, H);
    ctx.font = '11px ui-monospace, Consolas, monospace';
    ctx.strokeStyle = '#1a2533'; ctx.fillStyle = '#7d8ba0'; ctx.lineWidth = 1;
    function ticks(lo, hi, log) {
      if (!log) return niceTicks(lo, hi, 6);
      var out = [];
      for (var e = Math.floor(Math.log10(lo)); e <= Math.ceil(Math.log10(hi)); e++) {
        [1, 2, 5].forEach(function (k) { var v = k * Math.pow(10, e); if (v >= lo * 0.999 && v <= hi * 1.001) out.push(v); });
      }
      return out;
    }
    ticks(o.x[0], o.x[1], o.logX).forEach(function (v) {
      var px = X(v); ctx.beginPath(); ctx.moveTo(px, m.t); ctx.lineTo(px, m.t + ph); ctx.stroke();
      ctx.textAlign = 'center'; ctx.fillText(tickLabel(v), px, m.t + ph + 14);
    });
    ticks(o.y[0], o.y[1], o.logY).forEach(function (v) {
      var py = Y(v); ctx.beginPath(); ctx.moveTo(m.l, py); ctx.lineTo(m.l + pw, py); ctx.stroke();
      ctx.textAlign = 'right'; ctx.fillText(tickLabel(v), m.l - 6, py + 4);
    });
    ctx.strokeStyle = '#3a4a60'; ctx.strokeRect(m.l, m.t, pw, ph);
    ctx.fillStyle = '#9fb0c6'; ctx.textAlign = 'center';
    if (o.xlabel) ctx.fillText(o.xlabel, m.l + pw / 2, H - 6);
    if (o.ylabel) { ctx.save(); ctx.translate(12, m.t + ph / 2); ctx.rotate(-Math.PI / 2); ctx.fillText(o.ylabel, 0, 0); ctx.restore(); }
    ctx.save(); ctx.beginPath(); ctx.rect(m.l, m.t, pw, ph); ctx.clip();
    (o.hlines || []).forEach(function (l) {
      ctx.strokeStyle = l.color || '#556'; ctx.setLineDash([4, 4]); ctx.beginPath();
      ctx.moveTo(m.l, Y(l.y)); ctx.lineTo(m.l + pw, Y(l.y)); ctx.stroke(); ctx.setLineDash([]);
      if (l.label) { ctx.fillStyle = l.color || '#889'; ctx.textAlign = 'left'; ctx.fillText(l.label, m.l + 4, Y(l.y) - 4); }
    });
    (o.vlines || []).forEach(function (l) {
      ctx.strokeStyle = l.color || '#556'; ctx.setLineDash([4, 4]); ctx.beginPath();
      ctx.moveTo(X(l.x), m.t); ctx.lineTo(X(l.x), m.t + ph); ctx.stroke(); ctx.setLineDash([]);
      if (l.label) { ctx.fillStyle = l.color || '#889'; ctx.textAlign = 'left'; ctx.fillText(l.label, X(l.x) + 4, m.t + 12); }
    });
    (o.fills || []).forEach(function (f) {
      ctx.fillStyle = f.color; ctx.beginPath();
      ctx.moveTo(X(f.x[0]), Y(f.base === undefined ? 0 : f.base));
      for (var i = 0; i < f.x.length; i++) ctx.lineTo(X(f.x[i]), Y(f.y[i]));
      ctx.lineTo(X(f.x[f.x.length - 1]), Y(f.base === undefined ? 0 : f.base)); ctx.closePath(); ctx.fill();
    });
    (o.series || []).forEach(function (s) {
      ctx.strokeStyle = s.color || '#fb923c'; ctx.lineWidth = s.width || 1.6;
      ctx.setLineDash(s.dash || []); ctx.beginPath();
      var started = false;
      for (var i = 0; i < s.x.length; i++) {
        var yv = s.y[i];
        if (!isFinite(yv) || (o.logY && yv <= 0) || (o.logX && s.x[i] <= 0)) { started = false; continue; }
        var px = X(s.x[i]), py = Y(yv);
        if (!started) { ctx.moveTo(px, py); started = true; } else ctx.lineTo(px, py);
      }
      ctx.stroke(); ctx.setLineDash([]);
    });
    (o.points || []).forEach(function (p) {
      ctx.fillStyle = p.color || '#22d3ee'; ctx.beginPath(); ctx.arc(X(p.x), Y(p.y), p.r || 4, 0, 2 * Math.PI); ctx.fill();
      if (p.label) { ctx.textAlign = 'left'; ctx.fillText(p.label, X(p.x) + 6, Y(p.y) - 6); }
    });
    ctx.restore();
    var ly = m.t + 14;
    (o.series || []).forEach(function (s) {
      if (!s.label) return;
      ctx.fillStyle = s.color || '#fb923c'; ctx.fillRect(m.l + pw - 150, ly - 8, 12, 3);
      ctx.fillStyle = '#b8c4d6'; ctx.textAlign = 'left'; ctx.fillText(s.label, m.l + pw - 132, ly - 4); ly += 15;
    });
    return { X: X, Y: Y, ctx: ctx, m: m, pw: pw, ph: ph };
  }
  function tickLabel(v) {
    var a = Math.abs(v);
    if (a === 0) return '0';
    if (a >= 1e4 || a < 1e-2) return v.toExponential(0);
    return String(+v.toPrecision(3));
  }

  // ------------------------------------------------------------------ UI helpers
  var LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Expert'];
  var ui = {
    LEVELS: LEVELS,
    difficultySelect: function (onChange, initial) {
      var s = util.el('select', { 'aria-label': 'Difficulty' });
      LEVELS.forEach(function (l) { var o = util.el('option', null, l); o.value = l; s.appendChild(o); });
      s.value = util.param('level', initial || 'Beginner');
      s.addEventListener('change', function () { onChange(s.value); });
      return s;
    },
    header: function (id, title, sub, extra) {
      var h = util.el('header', { class: 'sim-head' });
      h.innerHTML = '<h1><span class="id">SIM ' + id + '</span>' + util.esc(title) + '</h1><span class="sub">' + (sub || '') + '</span><span class="grow"></span>';
      (extra || []).forEach(function (e) { h.appendChild(e); });
      document.body.insertBefore(h, document.body.firstChild);
      return h;
    },
    logger: function (el) {
      var t0 = Date.now();
      return function (msg, cls) {
        var d = util.el('div', cls ? { class: cls } : null, '<span class="t">' + ((Date.now() - t0) / 1000).toFixed(1).padStart(6, ' ') + 's</span>' + msg);
        el.appendChild(d); el.scrollTop = el.scrollHeight;
      };
    },
    slider: function (parent, label, min, max, step, value, onInput, fmtFn) {
      var wrap = util.el('div', { class: 'row', style: 'flex-direction:column;align-items:stretch;gap:2px' });
      var lab = util.el('label');
      var inp = util.el('input', { type: 'range', min: min, max: max, step: step, value: value });
      function upd() { lab.innerHTML = label + ': <span class="mono" style="color:var(--ink)">' + (fmtFn ? fmtFn(+inp.value) : inp.value) + '</span>'; }
      inp.addEventListener('input', function () { upd(); onInput(+inp.value); });
      upd(); wrap.appendChild(lab); wrap.appendChild(inp); parent.appendChild(wrap);
      return inp;
    }
  };

  // ------------------------------------------------------------------ debrief
  function bandFor(pct) {
    return pct >= 85 ? 'Expert' : pct >= 70 ? 'Proficient' : pct >= 50 ? 'Developing' : 'Novice';
  }
  /* debrief.show({title, seed, level, scores:[{label, value(0..100), note}], observed:[], decided:[], missed:[],
                   uncertainty:[], reasoning:[], physics:[], engineering:[], links:[{href,text}], onClose}) */
  var debrief = {
    bandFor: bandFor,
    show: function (d) {
      var wrap = util.$('.debrief-wrap');
      if (!wrap) { wrap = util.el('div', { class: 'debrief-wrap' }); document.body.appendChild(wrap); }
      var total = d.scores && d.scores.length ? Math.round(d.scores.reduce(function (a, s) { return a + s.value; }, 0) / d.scores.length) : null;
      function list(title, items) {
        if (!items || !items.length) return '';
        return '<h3>' + title + '</h3><ul>' + items.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul>';
      }
      var html = '<div class="debrief"><h2>' + util.esc(d.title || 'Debrief') + '</h2>' +
        '<div class="hint">Seed ' + d.seed + ' · level ' + (d.level || '') +
        ' · replay with <span class="mono">?seed=' + d.seed + '&level=' + (d.level || '') + '</span></div>';
      if (total !== null) {
        html += '<div class="score-grid"><div class="score"><div class="l">Overall</div><div class="n">' + total +
          '</div><div class="band">' + bandFor(total) + '</div></div>' +
          d.scores.map(function (s) {
            return '<div class="score"><div class="l">' + s.label + '</div><div class="n">' + Math.round(s.value) +
              '</div><div class="bar"><div style="width:' + util.clamp(s.value, 0, 100) + '%"></div></div>' +
              (s.note ? '<div class="hint">' + s.note + '</div>' : '') + '</div>';
          }).join('') + '</div>';
      }
      html += list('What you observed', d.observed) + list('What you decided', d.decided) +
        list('What you missed', d.missed) + list('What uncertainty existed', d.uncertainty) +
        list('What professional reasoning would consider', d.reasoning) +
        list('Relevant physics', d.physics) + list('Relevant engineering principles', d.engineering);
      if (d.links && d.links.length) {
        html += '<h3>Back to the course</h3><ul>' + d.links.map(function (l) {
          return '<li><a target="_top" href="' + l.href + '">' + l.text + '</a></li>';
        }).join('') + '</ul>';
      }
      html += '<div class="row" style="margin-top:16px"><button class="primary" id="dbf-close">Close</button>' +
        '<button id="dbf-new">New scenario</button></div></div>';
      wrap.innerHTML = html; wrap.classList.add('show');
      util.$('#dbf-close').onclick = function () { wrap.classList.remove('show'); if (d.onClose) d.onClose(); };
      util.$('#dbf-new').onclick = function () {
        var url = location.pathname + '?level=' + encodeURIComponent(d.level || 'Beginner') + (util.param('embed') ? '&embed=1' : '');
        location.href = url;
      };
      try {
        var k = 'eod-sim-results-v1', all = JSON.parse(localStorage.getItem(k) || '[]');
        all.push({ sim: document.title, date: new Date().toISOString(), level: d.level, seed: d.seed, score: total });
        localStorage.setItem(k, JSON.stringify(all.slice(-500)));
      } catch (e) {}
    }
  };

  // Course root relative to a sim page (sims/<slug>/index.html) for debrief links.
  var COURSE = '../../index.html#/';

  window.EOD = { util: util, rng: rng, seedFromUrl: seedFromUrl, plot: plot, hidpi: hidpi, niceTicks: niceTicks, ui: ui, debrief: debrief, COURSE: COURSE };
})();
