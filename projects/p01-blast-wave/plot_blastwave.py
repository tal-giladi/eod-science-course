"""Plots for Project P01: p(t) gauge traces, p(Z) and i(Z) curves, and the Sod shock tube.

Usage (from the repo root):
    python projects/p01-blast-wave/plot_blastwave.py            # uses starter/blastwave.py
    EOD_SOLUTION=1 python projects/p01-blast-wave/plot_blastwave.py   # uses the reference
Figures are written to projects/p01-blast-wave/out/ (or the directory given as argv[1]).
All yields are abstract yield units (YU).
"""
from __future__ import annotations

import os
import pathlib
import sys

import numpy as np

_HERE = pathlib.Path(__file__).resolve().parent


def _load_module():
    sys.path.insert(0, str(_HERE / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
    import blastwave  # noqa: E402
    return blastwave


def make_plots(bw, outdir, W: float = 1.0, ranges=(3.0, 5.0, 8.0, 12.0), sod_cells: int = 400):
    """Write p_t.png, p_Z.png, i_Z.png and sod.png to ``outdir``; return the list of paths."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    files = []

    # p(t) at several ranges
    fig, ax = plt.subplots(figsize=(7, 4))
    t = np.linspace(0, 60, 3000)
    for R in ranges:
        ax.plot(t, bw.gauge_trace(W, R, t), label=f"R = {R:g} m")
    ax.axhline(0, color="k", lw=0.5)
    ax.set(xlabel="time since release [ms]", ylabel="overpressure [kPa]",
           title=f"Friedlander gauge traces, W = {W:g} YU (free air)")
    ax.legend()
    files.append(outdir / "p_t.png")
    fig.tight_layout(); fig.savefig(files[-1], dpi=120); plt.close(fig)

    Z = np.logspace(np.log10(0.3), np.log10(40), 200)

    # p(Z): incident and reflected
    fig, ax = plt.subplots(figsize=(7, 4))
    ps = np.asarray(bw.kg_overpressure_ratio(Z)) * bw.P0
    ax.loglog(Z, ps, label="incident $p_s$ (Kinney–Graham)")
    ax.loglog(Z, np.asarray(bw.reflected_overpressure(ps)), "--", label="normally reflected $p_r$")
    ax.loglog(Z, np.asarray(bw.dynamic_pressure(ps)), ":", label="dynamic $q$")
    ax.set(xlabel="scaled distance Z [m/YU$^{1/3}$]", ylabel="pressure [kPa]", title="p(Z)")
    ax.grid(True, which="both", alpha=0.3); ax.legend()
    files.append(outdir / "p_Z.png")
    fig.tight_layout(); fig.savefig(files[-1], dpi=120); plt.close(fig)

    # i(Z): scaled impulse, fit vs numerically integrated fitted Friedlander pulse
    fig, ax = plt.subplots(figsize=(7, 4))
    i_fit = np.asarray(bw.kg_impulse_scaled(Z)) * 100
    i_num = []
    for z in Z:
        r = bw.predict(1.0, z)
        i_num.append(bw.friedlander_impulse_numeric(r["ps"], r["td"], r["b"]))
    ax.loglog(Z, i_fit, label="Kinney–Graham fit")
    ax.loglog(Z, i_num, "--", label="numeric ∫p dt of fitted pulse")
    ax.set(xlabel="scaled distance Z [m/YU$^{1/3}$]", ylabel="i / W$^{1/3}$ [kPa·ms/YU$^{1/3}$]", title="i(Z)")
    ax.grid(True, which="both", alpha=0.3); ax.legend()
    files.append(outdir / "i_Z.png")
    fig.tight_layout(); fig.savefig(files[-1], dpi=120); plt.close(fig)

    # Sod shock tube: numerical vs exact
    x, rho, u, p, dx = bw.sod_initial(sod_cells)
    r, v, pp, _ = bw.euler_solve(rho, u, p, dx, 0.2)
    ex = bw.exact_riemann((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))
    xf = np.linspace(0, 1, 1000)
    re, ue, pe = bw.sample_riemann(ex, (xf - 0.5) / 0.2)
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.4))
    for a, num, exact, lab in zip(axs, (r, v, pp), (re, ue, pe), ("density", "velocity", "pressure")):
        a.plot(x, num, ".", ms=2, label="HLL"); a.plot(xf, exact, "k-", lw=1, label="exact")
        a.set(xlabel="x", title=lab)
    axs[0].legend()
    files.append(outdir / "sod.png")
    fig.tight_layout(); fig.savefig(files[-1], dpi=120); plt.close(fig)
    return [str(f) for f in files]


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else _HERE / "out"
    for f in make_plots(_load_module(), out):
        print("wrote", f)
