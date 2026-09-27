/* Blast & shock physics used by Sims D and I (mirrors projects/p01-blast-wave in Python).
   All relations are standard, published ideal-gas shock physics and published empirical fits;
   see lessons 01.3, 01.4, 01.5, 04.1, 04.2 for derivations and citations.
   Yields are ABSTRACT "yield units" (YU). Scaled distance Z = R / W^(1/3)  [m / YU^(1/3)]. */
(function () {
  'use strict';
  var P0 = 101.325;   // kPa, sea-level ambient
  var A0 = 340.3;     // m/s, sea-level speed of sound
  var GAMMA = 1.4;

  // ---------- Rankine–Hugoniot, ideal gas (lesson 01.3) ----------
  function shockJump(M, g) {
    g = g || GAMMA;
    var M2 = M * M;
    var pr = 1 + 2 * g / (g + 1) * (M2 - 1);                 // p2/p1
    var rr = (g + 1) * M2 / ((g - 1) * M2 + 2);               // rho2/rho1
    var Tr = pr / rr;                                         // T2/T1
    var up = 2 / (g + 1) * (M - 1 / M);                       // u2/a1 (particle velocity behind shock)
    var M2b = Math.sqrt(((g - 1) * M2 + 2) / (2 * g * M2 - (g - 1))); // downstream Mach (shock frame)
    return { pr: pr, rr: rr, Tr: Tr, up: up, Mdown: M2b };
  }
  // Mach number from overpressure ratio ps/p0 (inverse of pr = 1 + 2g/(g+1)(M^2-1))
  function machFromOverpressure(ps, p0, g) {
    g = g || GAMMA; p0 = p0 || P0;
    return Math.sqrt(1 + (g + 1) / (2 * g) * ps / p0);
  }
  // Peak dynamic pressure behind a shock, gamma = 1.4 closed form: q = 5/2 ps^2/(7 p0 + ps)
  function dynamicPressure(ps, p0) { p0 = p0 || P0; return 2.5 * ps * ps / (7 * p0 + ps); }
  // Normally reflected overpressure, ideal gas gamma = 1.4: pr = 2 ps (7 p0 + 4 ps)/(7 p0 + ps)
  function reflectedOverpressure(ps, p0) { p0 = p0 || P0; return 2 * ps * (7 * p0 + 4 * ps) / (7 * p0 + ps); }
  // General-gamma reflected ratio (for the explorer)
  function reflectedRatio(ps, p0, g) {
    g = g || GAMMA; p0 = p0 || P0;
    var y = ps / p0;
    return 2 + (g + 1) * y / ((g - 1) * y + 2 * g);
  }

  // ---------- Kinney & Graham (1985) empirical free-air fits (lesson 04.1) ----------
  // Z in m / YU^(1/3) (in the literature: m / kg^(1/3) of TNT-equivalent).
  function kgOverpressureRatio(Z) {
    return 808 * (1 + Math.pow(Z / 4.5, 2)) /
      (Math.sqrt(1 + Math.pow(Z / 0.048, 2)) * Math.sqrt(1 + Math.pow(Z / 0.32, 2)) * Math.sqrt(1 + Math.pow(Z / 1.35, 2)));
  }
  // positive-phase duration per cube-root yield  [ms / YU^(1/3)]
  function kgDurationScaled(Z) {
    return 980 * (1 + Math.pow(Z / 0.54, 10)) /
      ((1 + Math.pow(Z / 0.02, 3)) * (1 + Math.pow(Z / 0.74, 6)) * Math.sqrt(1 + Math.pow(Z / 6.9, 2)));
  }
  // positive-phase impulse per cube-root yield [bar·ms / YU^(1/3)]
  function kgImpulseScaled(Z) {
    return 0.067 * Math.sqrt(1 + Math.pow(Z / 0.23, 4)) / (Z * Z * Math.cbrt(1 + Math.pow(Z / 1.55, 3)));
  }
  // arrival time by integrating 1/U(r) where U = a0 * M(ps(r))  [ms]
  function arrivalTime(R, W, a0, p0) {
    a0 = a0 || A0; p0 = p0 || P0;
    var n = 400, r0 = 0.05 * Math.cbrt(W), t = 0, dr = (R - r0) / n;
    if (R <= r0) return 0;
    for (var i = 0; i < n; i++) {
      var r = r0 + (i + 0.5) * dr;
      var ps = kgOverpressureRatio(r / Math.cbrt(W)) * p0;
      t += dr / (a0 * machFromOverpressure(ps, p0));
    }
    return t * 1000;
  }

  // ---------- Friedlander waveform (lesson 04.1) ----------
  function friedlander(t, ps, td, b) {
    if (t < 0) return 0;
    return ps * (1 - t / td) * Math.exp(-b * t / td);
  }
  // positive-phase impulse of a Friedlander pulse: i = ps td [1/b - (1 - e^-b)/b^2]
  function friedlanderImpulse(ps, td, b) {
    return ps * td * (1 / b - (1 - Math.exp(-b)) / (b * b));
  }
  // decay coefficient b such that the Friedlander impulse equals a target impulse (bisection)
  function solveDecay(ps, td, iTarget) {
    var f0 = function (b) { return friedlanderImpulse(ps, td, b) - iTarget; };
    var lo = 1e-4, hi = 60;
    if (f0(lo) < 0) return lo;     // target larger than triangular-ish limit: take the gentlest decay
    if (f0(hi) > 0) return hi;
    for (var k = 0; k < 80; k++) { var mid = 0.5 * (lo + hi); if (f0(mid) > 0) lo = mid; else hi = mid; }
    return 0.5 * (lo + hi);
  }

  /* Full free-air gauge prediction for yield W [YU] at range R [m].
     surfaceFactor multiplies the effective yield (1 = free air; ~1.8 typical hemispherical surface burst). */
  function predict(W, R, opts) {
    opts = opts || {};
    var p0 = opts.p0 || P0, a0 = opts.a0 || A0;
    var We = W * (opts.surfaceFactor || 1);
    var cw = Math.cbrt(We);
    var Z = R / cw;
    // Sachs scaling for non-standard ambient: ps scales with p0, times with (p0/P0)^(-1/3)(a0/A0)^-1
    var ps = kgOverpressureRatio(Z) * p0;                       // kPa
    var td = kgDurationScaled(Z) * cw;                           // ms
    var iS = kgImpulseScaled(Z) * cw * 100;                      // bar·ms -> kPa·ms
    var b = solveDecay(ps, td, iS);
    var ta = arrivalTime(R, We, a0, p0);
    var M = machFromOverpressure(ps, p0);
    var q = dynamicPressure(ps, p0);
    var pr = reflectedOverpressure(ps, p0);
    return { W: W, We: We, R: R, Z: Z, ps: ps, td: td, i: friedlanderImpulse(ps, td, b), iFit: iS, b: b,
      ta: ta, M: M, U: M * a0, q: q, pr: pr, Cr: pr / ps, ir: friedlanderImpulse(pr, td, b) };
  }

  // ---------- SDOF structural response (lesson 01.6 / 04.3) ----------
  // m x'' + c x' + k x = A * p(t); returns time history via RK4. Units consistent SI with p in kPa*1e3.
  function sdofResponse(opts) {
    var m = opts.m, k = opts.k, c = opts.c || 0, A = opts.A || 1, load = opts.load; // load(t) in Pa
    var T = 2 * Math.PI * Math.sqrt(m / k);
    var tEnd = opts.tEnd || 3 * T, dt = opts.dt || Math.min(T / 200, tEnd / 2000);
    var x = 0, v = 0, t = 0, ts = [], xs = [], xmax = 0;
    function acc(tt, xx, vv) { return (A * load(tt) - c * vv - k * xx) / m; }
    while (t <= tEnd) {
      ts.push(t); xs.push(x); if (Math.abs(x) > xmax) xmax = Math.abs(x);
      var k1v = acc(t, x, v), k1x = v;
      var k2v = acc(t + dt / 2, x + dt / 2 * k1x, v + dt / 2 * k1v), k2x = v + dt / 2 * k1v;
      var k3v = acc(t + dt / 2, x + dt / 2 * k2x, v + dt / 2 * k2v), k3x = v + dt / 2 * k2v;
      var k4v = acc(t + dt, x + dt * k3x, v + dt * k3v), k4x = v + dt * k3v;
      x += dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x);
      v += dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v);
      t += dt;
    }
    return { t: ts, x: xs, xmax: xmax, T: T };
  }
  // Peak response of an undamped elastic SDOF to a triangular pulse (peak P, duration td) — used for P–I curves.
  function peakTriangular(m, k, P, td) {
    var r = sdofResponse({ m: m, k: k, A: 1, load: function (t) { return t < td ? P * (1 - t / td) : 0; },
      tEnd: Math.max(td, 0) + 2 * Math.PI * Math.sqrt(m / k) * 1.2 });
    return r.xmax;
  }
  // Iso-damage (P–I) curve for threshold displacement xc: for each duration find P that gives xmax = xc.
  function piCurve(m, k, xc, n) {
    n = n || 40;
    var T = 2 * Math.PI * Math.sqrt(m / k), out = [];
    for (var j = 0; j < n; j++) {
      var td = T * Math.pow(10, -2.5 + 4.5 * j / (n - 1));
      var lo = 0, hi = k * xc * 100 / Math.max(1e-6, Math.min(1, td / T));
      for (var it = 0; it < 50; it++) {
        var mid = 0.5 * (lo + hi);
        if (peakTriangular(m, k, mid, td) > xc) hi = mid; else lo = mid;
      }
      var P = 0.5 * (lo + hi);
      out.push({ td: td, P: P, I: 0.5 * P * td });
    }
    return { curve: out, Pasym: k * xc / 2, Iasym: xc * Math.sqrt(k * m), T: T };
  }

  window.BLAST = {
    P0: P0, A0: A0, GAMMA: GAMMA, shockJump: shockJump, machFromOverpressure: machFromOverpressure,
    dynamicPressure: dynamicPressure, reflectedOverpressure: reflectedOverpressure, reflectedRatio: reflectedRatio,
    kgOverpressureRatio: kgOverpressureRatio, kgDurationScaled: kgDurationScaled, kgImpulseScaled: kgImpulseScaled,
    arrivalTime: arrivalTime, friedlander: friedlander, friedlanderImpulse: friedlanderImpulse, solveDecay: solveDecay,
    predict: predict, sdofResponse: sdofResponse, peakTriangular: peakTriangular, piCurve: piCurve
  };
})();
