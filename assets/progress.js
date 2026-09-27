/* In-browser progress tracking for the EOD course (docsify plugin).
   Stores per-page status in localStorage; the CLI tracker (course.py) is the durable record.
   Tracked page kinds: lessons, projects, simulations, case studies, capstones, assessments. */
(function () {
  var KEY = 'eod-course-progress-v1';
  var TRACKED = /^\/?(lessons|projects|sims|case-studies|capstones|assessments)\//;

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function save(p) {
    try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) {}
  }
  function norm(path) {
    return (path || '').replace(/^#?\/?/, '').replace(/\?.*$/, '').replace(/\.md$/, '');
  }
  function kind(path) {
    var m = norm(path).match(/^([a-z-]+)\//);
    return m ? m[1] : 'other';
  }

  function markSidebar(p) {
    document.querySelectorAll('.sidebar-nav a').forEach(function (a) {
      var href = norm((a.getAttribute('href') || '').replace(/^#\//, ''));
      var li = a.parentElement;
      if (!li) return;
      li.classList.toggle('eod-done', !!(p[href] && p[href].status === 'completed'));
    });
  }

  function widget(path) {
    var p = load();
    var e = p[path] || {};
    var box = document.createElement('div');
    box.className = 'eod-progress';
    box.innerHTML =
      '<strong>Progress</strong>' +
      '<select data-f="status">' +
        ['not-started', 'in-progress', 'completed', 'review'].map(function (s) {
          return '<option value="' + s + '"' + (e.status === s ? ' selected' : '') + '>' + s + '</option>';
        }).join('') +
      '</select>' +
      '<label><input type="checkbox" data-f="exercises"' + (e.exercises ? ' checked' : '') + '> exercises done</label>' +
      '<label><input type="checkbox" data-f="sim"' + (e.sim ? ' checked' : '') + '> simulation done</label>' +
      '<label><input type="checkbox" data-f="code"' + (e.code ? ' checked' : '') + '> programming done</label>' +
      '<span class="spacer"></span>' +
      '<span>confidence</span><select data-f="confidence">' +
        ['', '1', '2', '3', '4', '5'].map(function (s) {
          return '<option' + (String(e.confidence || '') === s ? ' selected' : '') + '>' + s + '</option>';
        }).join('') +
      '</select>';
    box.addEventListener('change', function (ev) {
      var t = ev.target, f = t.getAttribute('data-f');
      if (!f) return;
      var all = load();
      var rec = all[path] || {};
      rec[f] = t.type === 'checkbox' ? t.checked : t.value;
      rec.updated = new Date().toISOString().slice(0, 10);
      all[path] = rec;
      save(all);
      markSidebar(all);
    });
    return box;
  }

  function dashboard(el) {
    var p = load();
    var links = Array.prototype.slice.call(document.querySelectorAll('.sidebar-nav a'))
      .map(function (a) { return { href: norm((a.getAttribute('href') || '').replace(/^#\//, '')), title: a.textContent }; })
      .filter(function (l) { return TRACKED.test(l.href); });
    var seen = {}, groups = {};
    links.forEach(function (l) {
      if (seen[l.href]) return; seen[l.href] = 1;
      var k = kind(l.href);
      (groups[k] = groups[k] || []).push(l);
    });
    var names = { lessons: 'Lessons', sims: 'Simulations', projects: 'Programming projects',
      'case-studies': 'Case studies', capstones: 'Capstones', assessments: 'Assessments' };
    var html = '<div class="dash-grid">';
    Object.keys(groups).forEach(function (k) {
      var g = groups[k];
      var done = g.filter(function (l) { return p[l.href] && p[l.href].status === 'completed'; }).length;
      var pct = Math.round(100 * done / g.length);
      html += '<div class="dash-card"><strong>' + (names[k] || k) + '</strong><br>' + done + ' / ' + g.length +
        ' completed<div class="dash-bar"><div style="width:' + pct + '%"></div></div></div>';
    });
    html += '</div><h3>Detail</h3><table><thead><tr><th>Item</th><th>Status</th><th>Ex.</th><th>Sim</th><th>Code</th><th>Conf.</th></tr></thead><tbody>';
    Object.keys(groups).forEach(function (k) {
      groups[k].forEach(function (l) {
        var e = p[l.href] || {};
        html += '<tr><td><a href="#/' + l.href + '">' + l.title + '</a></td><td>' + (e.status || 'not-started') +
          '</td><td>' + (e.exercises ? '✓' : '') + '</td><td>' + (e.sim ? '✓' : '') + '</td><td>' +
          (e.code ? '✓' : '') + '</td><td>' + (e.confidence || '') + '</td></tr>';
      });
    });
    html += '</tbody></table>';
    var sims = [];
    try { sims = JSON.parse(localStorage.getItem('eod-sim-results-v1') || '[]'); } catch (e) {}
    html += '<h3>Simulator debriefs</h3>' + (sims.length ? '<table><thead><tr><th>Date</th><th>Simulator</th><th>Level</th><th>Seed</th><th>Score</th></tr></thead><tbody>' +
      sims.slice(-40).reverse().map(function (r) {
        return '<tr><td>' + String(r.date).slice(0, 10) + '</td><td>' + r.sim + '</td><td>' + (r.level || '') + '</td><td>' + r.seed + '</td><td>' + (r.score === null ? '—' : r.score) + '</td></tr>';
      }).join('') + '</tbody></table>' : '<p>No simulator debriefs recorded yet in this browser.</p>') +
      '<p><button id="eod-export">Export progress JSON</button> <button id="eod-import">Import progress JSON</button></p>';
    el.innerHTML = html;
    document.getElementById('eod-export').onclick = function () {
      var blob = new Blob([JSON.stringify(load(), null, 2)], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'eod-progress.json'; a.click();
    };
    document.getElementById('eod-import').onclick = function () {
      var inp = document.createElement('input'); inp.type = 'file'; inp.accept = 'application/json';
      inp.onchange = function () {
        var r = new FileReader();
        r.onload = function () { try { save(JSON.parse(r.result)); dashboard(el); markSidebar(load()); } catch (e) { alert('Invalid file'); } };
        r.readAsText(inp.files[0]);
      };
      inp.click();
    };
  }

  window.EODProgressPlugin = function (hook, vm) {
    hook.doneEach(function () {
      var path = norm(vm.route.path);
      var section = document.querySelector('.markdown-section');
      if (section && TRACKED.test(path) && !/\/(index|README)$/.test(path)) {
        section.appendChild(widget(path));
      }
      var dash = document.getElementById('eod-dashboard');
      if (dash) dashboard(dash);
      markSidebar(load());
    });
  };
})();
