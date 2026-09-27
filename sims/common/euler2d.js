/* 2D compressible Euler solver (finite volume, HLL flux, first order, ideal gas) for the
   wave-propagation panels. Non-dimensional: ambient rho = 1, p = 1, so c0 = sqrt(gamma).
   Solid cells reflect (mirror state with the normal velocity reversed); outer boundaries are
   zero-gradient (waves leave the domain). Intentionally simple and readable — see lesson 01.3
   "How it is represented computationally". Not a design tool. */
(function () {
  'use strict';
  var G = 1.4;

  function Euler2D(nx, ny) {
    this.nx = nx; this.ny = ny; this.n = nx * ny;
    this.r = new Float32Array(this.n); this.mu = new Float32Array(this.n);
    this.mv = new Float32Array(this.n); this.E = new Float32Array(this.n);
    this.solid = new Uint8Array(this.n);
    this.peak = new Float32Array(this.n);
    this.t = 0;
    this._fr = new Float32Array(4 * (nx + 1) * ny);
    this._gr = new Float32Array(4 * nx * (ny + 1));
    this.reset();
  }
  Euler2D.prototype.reset = function () {
    for (var i = 0; i < this.n; i++) { this.r[i] = 1; this.mu[i] = 0; this.mv[i] = 0; this.E[i] = 1 / (G - 1); this.peak[i] = 0; }
    this.t = 0;
  };
  Euler2D.prototype.idx = function (i, j) { return j * this.nx + i; };
  // Deposit a high-pressure, high-temperature region (abstract energy source).
  Euler2D.prototype.source = function (ci, cj, radius, pRatio, rhoRatio) {
    for (var j = 0; j < this.ny; j++) for (var i = 0; i < this.nx; i++) {
      var d2 = (i - ci) * (i - ci) + (j - cj) * (j - cj);
      if (d2 <= radius * radius && !this.solid[this.idx(i, j)]) {
        var k = this.idx(i, j);
        this.r[k] = rhoRatio; this.mu[k] = 0; this.mv[k] = 0; this.E[k] = pRatio / (G - 1);
      }
    }
  };
  Euler2D.prototype.pressure = function (k) {
    var r = this.r[k];
    return (G - 1) * (this.E[k] - 0.5 * (this.mu[k] * this.mu[k] + this.mv[k] * this.mv[k]) / r);
  };

  // HLL flux in direction d (0 = x, 1 = y) between left state L and right state R (primitive arrays).
  function hll(rL, uL, vL, pL, rR, uR, vR, pR, d, out, o) {
    var unL = d === 0 ? uL : vL, unR = d === 0 ? uR : vR;
    var cL = Math.sqrt(G * pL / rL), cR = Math.sqrt(G * pR / rR);
    var SL = Math.min(unL - cL, unR - cR), SR = Math.max(unL + cL, unR + cR);
    var EL = pL / (G - 1) + 0.5 * rL * (uL * uL + vL * vL);
    var ER = pR / (G - 1) + 0.5 * rR * (uR * uR + vR * vR);
    // physical fluxes
    var fL0 = rL * unL, fR0 = rR * unR;
    var fL1 = rL * uL * unL + (d === 0 ? pL : 0), fR1 = rR * uR * unR + (d === 0 ? pR : 0);
    var fL2 = rL * vL * unL + (d === 1 ? pL : 0), fR2 = rR * vR * unR + (d === 1 ? pR : 0);
    var fL3 = (EL + pL) * unL, fR3 = (ER + pR) * unR;
    if (SL >= 0) { out[o] = fL0; out[o + 1] = fL1; out[o + 2] = fL2; out[o + 3] = fL3; return Math.max(Math.abs(SL), Math.abs(SR)); }
    if (SR <= 0) { out[o] = fR0; out[o + 1] = fR1; out[o + 2] = fR2; out[o + 3] = fR3; return Math.max(Math.abs(SL), Math.abs(SR)); }
    var inv = 1 / (SR - SL);
    out[o]     = (SR * fL0 - SL * fR0 + SL * SR * (rR - rL)) * inv;
    out[o + 1] = (SR * fL1 - SL * fR1 + SL * SR * (rR * uR - rL * uL)) * inv;
    out[o + 2] = (SR * fL2 - SL * fR2 + SL * SR * (rR * vR - rL * vL)) * inv;
    out[o + 3] = (SR * fL3 - SL * fR3 + SL * SR * (ER - EL)) * inv;
    return Math.max(Math.abs(SL), Math.abs(SR));
  }

  Euler2D.prototype.maxSpeed = function () {
    var s = 0;
    for (var k = 0; k < this.n; k++) {
      if (this.solid[k]) continue;
      var r = this.r[k], u = this.mu[k] / r, v = this.mv[k] / r, p = Math.max(1e-6, this.pressure(k));
      var c = Math.sqrt(G * p / r);
      s = Math.max(s, Math.abs(u) + c, Math.abs(v) + c);
    }
    return s;
  };

  Euler2D.prototype.step = function (cfl) {
    cfl = cfl || 0.4;
    var nx = this.nx, ny = this.ny, self = this;
    var dt = cfl / Math.max(1e-6, this.maxSpeed());
    var F = this._fr, Gf = this._gr;
    function prim(k) {
      var r = Math.max(1e-4, self.r[k]);
      var u = self.mu[k] / r, v = self.mv[k] / r;
      var p = Math.max(1e-4, (G - 1) * (self.E[k] - 0.5 * r * (u * u + v * v)));
      return [r, u, v, p];
    }
    // x-faces: face (i, j) between cell i-1 and i, i in [0, nx]
    for (var j = 0; j < ny; j++) {
      for (var i = 0; i <= nx; i++) {
        var kl = j * nx + Math.max(0, i - 1), kr = j * nx + Math.min(nx - 1, i);
        var L = prim(kl), R = prim(kr);
        var sl = this.solid[kl], sr = this.solid[kr];
        if (sl && sr) { var o0 = 4 * (j * (nx + 1) + i); F[o0] = F[o0 + 1] = F[o0 + 2] = F[o0 + 3] = 0; continue; }
        if (sl) L = [R[0], -R[1], R[2], R[3]];
        if (sr) R = [L[0], -L[1], L[2], L[3]];
        hll(L[0], L[1], L[2], L[3], R[0], R[1], R[2], R[3], 0, F, 4 * (j * (nx + 1) + i));
      }
    }
    for (var j2 = 0; j2 <= ny; j2++) {
      for (var i2 = 0; i2 < nx; i2++) {
        var kb = Math.max(0, j2 - 1) * nx + i2, kt = Math.min(ny - 1, j2) * nx + i2;
        var B = prim(kb), T = prim(kt);
        var sb = this.solid[kb], st = this.solid[kt];
        if (sb && st) { var o1 = 4 * (j2 * nx + i2); Gf[o1] = Gf[o1 + 1] = Gf[o1 + 2] = Gf[o1 + 3] = 0; continue; }
        if (sb) B = [T[0], T[1], -T[2], T[3]];
        if (st) T = [B[0], B[1], -B[2], B[3]];
        hll(B[0], B[1], B[2], B[3], T[0], T[1], T[2], T[3], 1, Gf, 4 * (j2 * nx + i2));
      }
    }
    for (var jj = 0; jj < ny; jj++) {
      for (var ii = 0; ii < nx; ii++) {
        var k = jj * nx + ii;
        if (this.solid[k]) continue;
        var fl = 4 * (jj * (nx + 1) + ii), fr = fl + 4;
        var gb = 4 * (jj * nx + ii), gt = 4 * ((jj + 1) * nx + ii);
        this.r[k]  -= dt * (F[fr] - F[fl] + Gf[gt] - Gf[gb]);
        this.mu[k] -= dt * (F[fr + 1] - F[fl + 1] + Gf[gt + 1] - Gf[gb + 1]);
        this.mv[k] -= dt * (F[fr + 2] - F[fl + 2] + Gf[gt + 2] - Gf[gb + 2]);
        this.E[k]  -= dt * (F[fr + 3] - F[fl + 3] + Gf[gt + 3] - Gf[gb + 3]);
        if (this.r[k] < 1e-4) this.r[k] = 1e-4;
        var op = this.pressure(k) - 1;
        if (op > this.peak[k]) this.peak[k] = op;
      }
    }
    this.t += dt;
    return dt;
  };

  // Render overpressure (p - 1) or peak overpressure to an ImageData-backed canvas.
  Euler2D.prototype.render = function (ctx, w, h, mode, scale) {
    var nx = this.nx, ny = this.ny;
    if (!this._img || this._img.width !== nx) {
      this._off = document.createElement('canvas'); this._off.width = nx; this._off.height = ny;
      this._octx = this._off.getContext('2d'); this._img = this._octx.createImageData(nx, ny);
    }
    var d = this._img.data;
    for (var j = 0; j < ny; j++) for (var i = 0; i < nx; i++) {
      var k = j * nx + i, o = 4 * ((ny - 1 - j) * nx + i);
      if (this.solid[k]) { d[o] = 90; d[o + 1] = 100; d[o + 2] = 115; d[o + 3] = 255; continue; }
      var v = mode === 'peak' ? this.peak[k] : this.pressure(k) - 1;
      var c = colormap(v / scale);
      d[o] = c[0]; d[o + 1] = c[1]; d[o + 2] = c[2]; d[o + 3] = 255;
    }
    this._octx.putImageData(this._img, 0, 0);
    ctx.imageSmoothingEnabled = true;
    ctx.drawImage(this._off, 0, 0, w, h);
  };
  // diverging map: negative -> blue, 0 -> near black, positive -> orange -> yellow -> white
  function colormap(x) {
    if (x < 0) { var a = Math.min(1, -x * 3); return [10 + 20 * a, 20 + 90 * a, 30 + 200 * a]; }
    var t = Math.min(1, x);
    if (t < 0.33) { var s = t / 0.33; return [10 + 190 * s, 14 + 50 * s, 20]; }
    if (t < 0.66) { var s2 = (t - 0.33) / 0.33; return [200 + 55 * s2, 64 + 120 * s2, 20 + 10 * s2]; }
    var s3 = (t - 0.66) / 0.34; return [255, 184 + 71 * s3, 30 + 225 * s3];
  }

  window.Euler2D = Euler2D;
})();
