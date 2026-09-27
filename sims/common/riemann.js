/* Exact Riemann solver for the 1D Euler equations, ideal gas, single gamma (after Toro,
   "Riemann Solvers and Numerical Methods for Fluid Dynamics", ch. 4). Used by Sim I. */
(function () {
  'use strict';
  function solve(L, R, g) {
    g = g || 1.4;
    var cL = Math.sqrt(g * L.p / L.r), cR = Math.sqrt(g * R.p / R.r);
    var AL = 2 / ((g + 1) * L.r), BL = (g - 1) / (g + 1) * L.p;
    var AR = 2 / ((g + 1) * R.r), BR = (g - 1) / (g + 1) * R.p;
    function fk(p, s, c, A, Bc) {
      if (p > s.p) { var q = Math.sqrt(A / (p + Bc)); return [(p - s.p) * q, q * (1 - 0.5 * (p - s.p) / (Bc + p))]; }
      var pr = p / s.p;
      return [2 * c / (g - 1) * (Math.pow(pr, (g - 1) / (2 * g)) - 1), 1 / (s.r * c) * Math.pow(pr, -(g + 1) / (2 * g))];
    }
    var du = R.u - L.u;
    // initial guess: two-rarefaction approximation
    var p = Math.pow((cL + cR - 0.5 * (g - 1) * du) / (cL / Math.pow(L.p, (g - 1) / (2 * g)) + cR / Math.pow(R.p, (g - 1) / (2 * g))), 2 * g / (g - 1));
    p = Math.max(1e-8, p);
    for (var it = 0; it < 60; it++) {
      var a = fk(p, L, cL, AL, BL), b = fk(p, R, cR, AR, BR);
      var f = a[0] + b[0] + du, df = a[1] + b[1];
      var pn = Math.max(1e-8, p - f / df);
      if (Math.abs(pn - p) / (0.5 * (pn + p)) < 1e-10) { p = pn; break; }
      p = pn;
    }
    var fl = fk(p, L, cL, AL, BL)[0], fr = fk(p, R, cR, AR, BR)[0];
    var u = 0.5 * (L.u + R.u) + 0.5 * (fr - fl);
    // star densities
    var rL = p > L.p ? L.r * ((p / L.p + (g - 1) / (g + 1)) / ((g - 1) / (g + 1) * p / L.p + 1)) : L.r * Math.pow(p / L.p, 1 / g);
    var rR = p > R.p ? R.r * ((p / R.p + (g - 1) / (g + 1)) / ((g - 1) / (g + 1) * p / R.p + 1)) : R.r * Math.pow(p / R.p, 1 / g);
    var sol = { p: p, u: u, rL: rL, rR: rR, g: g, L: L, R: R, cL: cL, cR: cR };
    sol.shockR = p > R.p ? R.u + cR * Math.sqrt((g + 1) / (2 * g) * p / R.p + (g - 1) / (2 * g)) : null;
    sol.shockL = p > L.p ? L.u - cL * Math.sqrt((g + 1) / (2 * g) * p / L.p + (g - 1) / (2 * g)) : null;
    return sol;
  }
  // sample state at similarity coordinate xi = x/t
  function sample(s, xi) {
    var g = s.g, L = s.L, R = s.R, cL = s.cL, cR = s.cR;
    if (xi <= s.u) { // left of contact
      if (s.p > L.p) { // left shock
        return xi < s.shockL ? L : { r: s.rL, u: s.u, p: s.p };
      }
      var cLs = cL * Math.pow(s.p / L.p, (g - 1) / (2 * g));
      var head = L.u - cL, tail = s.u - cLs;
      if (xi <= head) return L;
      if (xi >= tail) return { r: s.rL, u: s.u, p: s.p };
      var uu = 2 / (g + 1) * (cL + (g - 1) / 2 * L.u + xi), c = 2 / (g + 1) * (cL + (g - 1) / 2 * (L.u - xi));
      return { r: L.r * Math.pow(c / cL, 2 / (g - 1)), u: uu, p: L.p * Math.pow(c / cL, 2 * g / (g - 1)) };
    }
    if (s.p > R.p) return xi > s.shockR ? R : { r: s.rR, u: s.u, p: s.p };
    var cRs = cR * Math.pow(s.p / R.p, (g - 1) / (2 * g));
    var headR = R.u + cR, tailR = s.u + cRs;
    if (xi >= headR) return R;
    if (xi <= tailR) return { r: s.rR, u: s.u, p: s.p };
    var u2 = 2 / (g + 1) * (-cR + (g - 1) / 2 * R.u + xi), c2 = 2 / (g + 1) * (cR - (g - 1) / 2 * (R.u - xi));
    return { r: R.r * Math.pow(c2 / cR, 2 / (g - 1)), u: u2, p: R.p * Math.pow(c2 / cR, 2 * g / (g - 1)) };
  }
  window.RIEMANN = { solve: solve, sample: sample };
})();
