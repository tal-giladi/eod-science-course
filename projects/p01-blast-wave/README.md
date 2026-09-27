# P01 · Blast-wave library and shock-tube solver (`blastwave`)

<div class="module-card">

**Lessons** [01.3 Waves → shocks](lessons/stage-01/lesson-03.md) (core: Rankine–Hugoniot, Euler equations) · [01.4 Reflection & dynamic pressure](lessons/stage-01/lesson-04.md) · [01.5 Scaling laws](lessons/stage-01/lesson-05.md) · [04.1 Anatomy of a blast wave](lessons/stage-04/lesson-01.md) · [04.2 Distance, reflection, confinement](lessons/stage-04/lesson-02.md)

**Level** Intermediate · **Estimated time** 8–10 h

**Simulators** [Sim D · Blast physics](sims/blast-physics/index.html) · [Sim I · Shock tube](sims/shock-tube/index.html) · **Feeds** the loading step of 01.6 / 04.3 (SDOF, P–I)

<p class="tags"><span>Rankine–Hugoniot</span><span>Kinney–Graham</span><span>Friedlander</span><span>Hopkinson–Cranz</span><span>Sachs scaling</span><span>finite volume</span><span>HLL</span><span>exact Riemann</span></p>
</div>

## Goal

Build a small, tested Python library that reproduces the blast numbers used throughout the
course — shock jump ratios, reflected and dynamic pressure, free-air overpressure, duration and
impulse versus scaled distance, arrival time, and Friedlander gauge traces — and a 1D
finite-volume Euler solver that you verify against the exact Sod shock-tube solution. Then plot
$p(t)$, $p(Z)$ and $i(Z)$.

The library is a line-by-line Python mirror of `sims/common/blast.js`, which drives Sims D and I.
When your tests pass, the simulators and your code agree to the last printed digit.

<div class="callout boundary">

**Boundary.** All yields are abstract **yield units (YU)**. $Z = R/W^{1/3}$ in m/YU$^{1/3}$. The
project describes how a blast wave *behaves* and how it scales — the protective side of the
problem. It contains nothing about explosive materials, quantities or devices, and it must not be
extended in that direction.

</div>

## Background

- 1D Euler equations, characteristics, Rankine–Hugoniot jump conditions, entropy: [01.3](lessons/stage-01/lesson-03.md) §1–§5 and its programming exercise.
- Normal reflection factor (2 → 8 for air), dynamic pressure $q=\tfrac52 p_s^2/(7p_0+p_s)$: [01.4](lessons/stage-01/lesson-04.md).
- Hopkinson–Cranz cube-root scaling and Sachs scaling for non-standard ambient: [01.5](lessons/stage-01/lesson-05.md).
- Friedlander waveform, impulse integral, arrival-time integral, Kinney–Graham fits: [04.1](lessons/stage-04/lesson-01.md); surface bursts and reflection in practice: [04.2](lessons/stage-04/lesson-02.md).

Key relations (all implemented in `blastwave.py`):

$$
\frac{p_2}{p_1}=1+\frac{2\gamma}{\gamma+1}(M_s^2-1),\quad
\frac{\rho_2}{\rho_1}=\frac{(\gamma+1)M_s^2}{(\gamma-1)M_s^2+2},\quad
C_r=\frac{p_r}{p_s}=2+\frac{(\gamma+1)y}{(\gamma-1)y+2\gamma},\ y=\frac{p_s}{p_0},\quad
q=\frac{p_s^2}{2\gamma p_0+(\gamma-1)p_s}
$$

$$
p(t)=p_s\Big(1-\frac{t}{t_d}\Big)e^{-bt/t_d},\qquad
i=\int_0^{t_d}p\,dt=p_st_d\Big[\frac1b-\frac{1-e^{-b}}{b^2}\Big],\qquad
t_a(R)=\int_{r_0}^{R}\frac{dr}{a_0M(p_s(r))}
$$

## Requirements

1. **Rankine–Hugoniot**: `shock_jump`, `mach_from_overpressure`, `dynamic_pressure` (general $\gamma$),
   `reflected_overpressure` ($\gamma=1.4$ closed form), `reflected_ratio` (general $\gamma$).
2. **Empirical fits and scaling**: `kg_overpressure_ratio`, `kg_duration_scaled`, `kg_impulse_scaled`
   (Kinney & Graham 1985, exactly as in `blast.js`), `scaled_distance` (Sachs-scaled, sea-level equivalent).
3. **Waveform**: `friedlander`, analytic `friedlander_impulse`, `friedlander_impulse_numeric`
   (composite Simpson), `solve_decay` (bisection for $b$ given a target impulse).
4. **Prediction**: `arrival_time` (midpoint-rule integral) and `predict(W, R, p0, a0, surface_factor)`,
   including the far-field rule of `blast.js`: if the fits demand $b<0.5$, floor $b$ at 0.5 and
   stretch $t_d$ so the impulse fit is honoured. `gauge_trace` (provided) combines them into $p(t)$.
5. **Euler solver**: `euler_flux`, `hll_flux` (Davis wave speeds), `euler_step` (first-order,
   conservative, transmissive/periodic/reflective ghost cells), `max_wave_speed`, and
   `euler_solve` (CFL time step, last step lands exactly on `t_end`).
6. **Plots**: `plot_blastwave.py` writes `p_t.png`, `p_Z.png`, `i_Z.png` and `sod.png`.

**Design choice — the exact Riemann solver is provided.** `exact_riemann` and `sample_riemann`
(after Toro, ch. 4; a port of `sims/common/riemann.js`) are implemented in the starter. They are
the *reference* against which your solver is judged, not the learning goal of this project; a
test checks them against the published Sod values so you can trust them. Implementing them
yourself is extension 1. `prim_to_cons`, `cons_to_prim`, `sod_initial` and `gauge_trace` are
also provided.

## API

```python
P0 = 101.325; A0 = 340.3; GAMMA = 1.4                      # kPa, m/s, —
shock_jump(M, gamma=1.4) -> {"p", "rho", "T", "u_over_a1", "M_down"}
mach_from_overpressure(ps, p0=P0, gamma=1.4) -> M
dynamic_pressure(ps, p0=P0, gamma=1.4) -> q                 # same unit as ps
reflected_overpressure(ps, p0=P0) -> pr                     # gamma = 1.4
reflected_ratio(ps, p0=P0, gamma=1.4) -> Cr
kg_overpressure_ratio(Z) -> ps/p0
kg_duration_scaled(Z) -> td / W^(1/3)   [ms/YU^(1/3)]
kg_impulse_scaled(Z)  -> i / W^(1/3)    [bar·ms/YU^(1/3)]  (×100 → kPa·ms)
scaled_distance(R, W, p0=P0) -> Z
friedlander(t, ps, td, b) -> p;  friedlander_impulse(ps, td, b) -> i
friedlander_impulse_numeric(ps, td, b, n=2001) -> i;  solve_decay(ps, td, i_target) -> b
arrival_time(R, W, a0=A0, p0=P0, n=400) -> ta [ms]
predict(W, R, p0=P0, a0=A0, surface_factor=1.0) -> dict(W, We, R, Z, ps, td, i, i_fit, b, ta, M, U, q, pr, Cr, ir)
gauge_trace(W, R, t, **kw) -> p(t)                                            # provided
prim_to_cons(rho, u, p, gamma) -> U (3,N);  cons_to_prim(U, gamma) -> (rho, u, p)   # provided
euler_flux(U, gamma) -> F;  hll_flux(UL, UR, gamma) -> F
euler_step(U, dx, dt, gamma=1.4, bc="transmissive") -> U
max_wave_speed(U, gamma) -> float
euler_solve(rho, u, p, dx, t_end, gamma=1.4, cfl=0.5, bc="transmissive") -> (rho, u, p, nsteps)
exact_riemann(left, right, gamma=1.4) -> dict;  sample_riemann(sol, xi) -> (rho, u, p)  # provided
sod_initial(n=400, x0=0.5) -> (x, rho, u, p, dx)                                        # provided
```

`plot_blastwave.make_plots(bw, outdir, W=1.0, ranges=(3, 5, 8, 12), sod_cells=400) -> [paths]`.

## Input / output

- **Units**: kPa, ms, m, m/s, kPa·ms, YU. The Euler solver is non-dimensional (Sod units).
- **Input**: yield $W$ [YU], range $R$ [m], optional ambient $p_0$ [kPa] and $a_0$ [m/s],
  surface factor; for the solver, primitive arrays on a uniform grid, `dx`, `t_end`, `cfl`, `bc`.
- **Output**: scalars/arrays as documented; `predict` returns a dict; plots as PNG files.

## Constraints

- NumPy (+ SciPy only in tests, matplotlib only in the plot script). Python ≥ 3.10.
- Vectorise over arrays (every RH and fit function accepts arrays); the solver loops over time
  steps only, never over cells.
- `euler_solve` on 400 cells to $t=0.2$ in well under a second; whole test suite < 30 s.
- Formulas must stay consistent with `sims/common/blast.js`. The one deliberate difference: the
  arrival-time lower limit $r_0 = 0.05\,W^{1/3}(P_0/p_0)^{1/3}$ is Sachs-scaled (identical at sea
  level), which makes $t_a$ exactly Sachs-invariant.

## Expected behaviour

| Quantity | Expected |
|---|---|
| $\Delta p = 100$ kPa (01.3 example) | $M_s = 1.359$, $p_2/p_1 = 1.987$, $\rho_2/\rho_1 = 1.618$, $u_2 = 177$ m/s |
| Strong-shock limits | $\rho_2/\rho_1 \to 6$, $C_r \to 8$ (air), $C_r\to(3\gamma-1)/(\gamma-1)$ in general; weak: $C_r\to2$ |
| `predict(10, 15)` (01.4 example) | $p_s = 16.74$ kPa, $p_r = 35.8$ kPa, $i = 60.5$ kPa·ms, $i_r = 129.4$ kPa·ms |
| Hopkinson–Cranz | $W\to kW$, $R\to k^{1/3}R$: $p_s$ unchanged; $t_d$, $i$, $t_a$ × $k^{1/3}$ |
| Sachs | at fixed scaled $Z$: $p_s/p_0$, $t_d a_0 p_0^{1/3}/W^{1/3}$, $i a_0/(p_0^{2/3}W^{1/3})$, $t_a a_0 p_0^{1/3}/W^{1/3}$ invariant to 1e-9 |
| Sod, $t = 0.2$ | exact $p^* = 0.30313$, $u^* = 0.92745$, shock at $x = 0.850$, contact 0.685; HLL with $N=400$: $L_1(\rho)\approx 0.0075$ |
| Weak pulse ($A = 0.01$) | splits into two acoustic pulses travelling at $\sqrt\gamma = 1.183$ (within 1 %) |
| Periodic domain | mass, momentum, energy conserved to round-off |

## Test cases (`tests/test_blastwave.py`)

| Test | What it checks |
|---|---|
| `test_shock_jump_lesson_example`, `test_shock_jump_limits` | 01.3 worked numbers; $M=1$ identity; strong-shock density limit 6 and downstream Mach $\sqrt{(\gamma-1)/2\gamma}$; subsonic flow behind every shock |
| `test_mach_from_overpressure_inverts_jump` | exact inverse for several $\gamma$ |
| `test_dynamic_pressure_equals_half_rho_u2` | $q = \tfrac12\rho_2u_2^2$ from the jump conditions; the $\gamma=1.4$ closed form |
| `test_reflection_factor_limits`, `test_reflected_ratio_matches_two_shock_calculation` | limits 2 and 8; monotone; **independent** check by solving the reflected shock that stops the flow at a rigid wall |
| `test_kinney_graham_values`, `test_predict_matches_lesson_01_4` | fit values; `predict` reproduces the 01.4 numbers; $b$ honours the impulse fit |
| `test_hopkinson_cranz_scaling`, `test_sachs_scaling` | scaling invariance over yields 0.1–1000 YU and random $(p_0, a_0)$ |
| `test_friedlander_*`, `test_solve_decay_roundtrip` | shape, negative phase, numeric vs analytic impulse (1e-8), triangle limit $b\to0$, $b$ round trip |
| `test_arrival_time_behaviour` | monotone, faster than sound, far-field slope $1/a_0$ |
| `test_exact_riemann_sod_values` | provided helper vs published Sod star state (passes on the starter) |
| `test_hll_flux_consistency` | $F_{HLL}(U,U) = F(U)$; upwinding for supersonic flow |
| `test_sod_against_exact`, `test_conservation_periodic`, `test_weak_pulse_travels_at_sound_speed` | $L_1$ error, star plateau, shock position, CFL step count; conservation to 1e-12; acoustic speed |
| `test_plot_script_writes_figures` | `make_plots` produces the four figures |

## Milestones

1. Rankine–Hugoniot block; pass the first six tests. Derive $C_r$ yourself first (hint 2).
2. Kinney–Graham fits, `scaled_distance`, Friedlander functions, `solve_decay`.
3. `arrival_time` and `predict`; pass the scaling tests. Compare a few values with Sim D's probe readout.
4. Euler solver: flux, HLL, step, solve. Pass the Sod, conservation and weak-pulse tests.
5. Run `plot_blastwave.py`; write three sentences on what the $i(Z)$ plot says about the far-field $b$-floor rule.

## Extension challenges

1. Implement the exact Riemann solver yourself (Newton on $f_L(p)+f_R(p)+\Delta u=0$) and replace the provided one; test on Toro's five standard problems, including the near-vacuum 123 problem.
2. Second-order MUSCL–Hancock with a minmod limiter; measure the convergence order on a smooth entropy wave (expect ≈ 2) and on Sod (why is the observed order well below 2?).
3. Spherical symmetry: add the geometric source $-\tfrac{2}{r}[\rho u,\ \rho u^2,\ u(E+p)]$ and release an abstract high-pressure sphere; compare the decay of peak overpressure with $r$ against the shape (not the magnitude) of the Kinney–Graham curve.
4. HLLC flux: show that it resolves the contact discontinuity much more sharply than HLL.
5. Port `front_face_history` from the [01.4](lessons/stage-01/lesson-04.md) programming exercise (reflection + clearing) on top of `predict`.
6. Animate $p(x,t)$ for the Sod problem with `matplotlib.animation` and mark the three waves from `exact_riemann`.

## Hints

<details><summary>Hint 1 — vectorise the fits</summary>

Write every function with `np.asarray(..., dtype=float)` at the top and use `**`, `np.sqrt`,
`np.cbrt`; then `kg_overpressure_ratio(np.logspace(-1, 2, 200))` works for the plots with no loop.

</details>

<details><summary>Hint 2 — reflected pressure from two shocks</summary>

The incident shock sets gas 2 moving at $u_2$ toward the wall. The reflected shock must bring it
to rest: in gas 2's frame it is a shock of Mach $M_R$ with $u_2 = a_2\frac{2}{\gamma+1}(M_R - 1/M_R)$.
Solve for $M_R$, apply the pressure jump again, and simplify $(p_5-p_1)/(p_2-p_1)$ — the algebra
collapses to $2+\frac{(\gamma+1)y}{(\gamma-1)y+2\gamma}$.

</details>

<details><summary>Hint 3 — HLL in five lines</summary>

Compute $(\rho,u,p)$ and $c$ on both sides; $S_L=\min(u_L-c_L,u_R-c_R)$, $S_R=\max(u_L+c_L,u_R+c_R)$;
compute $F_L$, $F_R$ and the HLL average, then pick with two nested `np.where`. Pad with one ghost
cell per side and take `F[:, 1:] - F[:, :-1]` for the update.

</details>

<details><summary>Hint 4 — conservation to round-off</summary>

If you update $U$ only by flux differences and the boundary fluxes cancel (periodic ghost cells),
the sum of $U$ changes only by floating-point round-off. If your conservation test fails at 1e-6,
you are probably converting to primitives and back inside the step, or clipping negative pressures.

</details>

<details><summary>Hint 5 — the Friedlander impulse near b = 0</summary>

$\frac1b-\frac{1-e^{-b}}{b^2}$ suffers cancellation for tiny $b$; its series is
$\tfrac12-\tfrac b6+\tfrac{b^2}{24}-\dots$. The tests stay at $b\ge10^{-3}$, but a production
version would switch to the series.

</details>

## How to run

```bash
python -m pytest projects/p01-blast-wave                      # your starter
EOD_SOLUTION=1 python -m pytest projects/p01-blast-wave       # reference solution (bash)
python projects/p01-blast-wave/plot_blastwave.py              # figures → projects/p01-blast-wave/out/
```

On Windows `cmd`: `set EOD_SOLUTION=1 && py -m pytest projects/p01-blast-wave`. The plot script
uses the same switch (`EOD_SOLUTION=1`) to choose between starter and solution.
