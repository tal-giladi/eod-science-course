# P11 · Teleoperation simulator and experiment harness

<div class="module-card">

**Lessons** [06.5 Teleoperation & human–machine interfaces](lessons/stage-06/lesson-05.md) (core: move-and-wait, delay and phase margin, Smith predictor, predictive displays) · [06.9 Communications, reliability & fail-safe design](lessons/stage-06/lesson-09.md) (delay, jitter, loss) · [06.4 Mobile bases and control](lessons/stage-06/lesson-04.md) (unicycle kinematics, P control)

**Simulators** [Sim B — EOD robot](sims/eod-robot/index.html) (latency panel, predictive overlay) · [Sim G — robotics engineering](sims/robotics-engineering/index.html)

**Module** `teleop` · **Level** Advanced · **Time** 8–12 h · **Builds on** [P05 2D robot simulator](projects/p05-robot-sim/README.md) · **Next** [P12 Human-in-the-loop decisions](projects/p12-hitl-decision/README.md)

</div>

<div class="callout boundary">

**Scope.** This is a driving-to-waypoints experiment about delay, human control and displays. The
robot, course and obstacles are abstract; no manipulation task, tool or procedure is modelled.

</div>

## Goal

Quantify, with a reproducible harness, what round-trip delay does to a human-in-the-loop
controller and what each mitigation buys: continuous control degrades and then goes unstable,
move-and-wait stays accurate but pays one round trip per corrective move, and a predictive
(dead-reckoned ghost) display removes the delay from the loop. Tie the simulation to the
control-theoretic limit $K\tau<\pi/2$.

## Background

- **Move-and-wait** (06.5 §2, Ferrell 1965): $n=\lceil\ln(2D/W)/\ln(1/\varepsilon)\rceil$ open-loop
  moves, $T(\tau)\approx n(t_m+\tau)$ — completion time is linear in delay with slope $n$.
- **Delay eats phase margin** (06.5 §3): for $L(s)=Ke^{-s\tau}/s$, crossover $\omega_c=K$, phase
  $-\pi/2-K\tau$, so the loop is stable iff $K\tau<\pi/2$; at the limit it oscillates at $\omega=K$.
- **Smith predictor / predictive display** (06.5 §4–5): close the loop on a delay-free model and
  correct with the delayed measurement; the response becomes the delay-free one shifted by $\tau$.
  It cannot remove delay from *exogenous* events, and it degrades with model error.
- **Channels** (06.9): one-way delay + jitter + i.i.d. loss; time-stamped, sequence-numbered packets.

## Requirements

1. **Channel.** `Channel(delay, jitter, loss, rng)`: `send(t, seq, payload) -> bool` (False if lost),
   arrival at `t + max(0, delay + U(-jitter, jitter))`; `receive(t)` pops packets arrived by `t`.
2. **Robot.** Unicycle with speed limits executing the newest *plan* received (list of
   `(v, w, duration)` segments; `inf` = hold until replaced); stale sequence numbers are ignored;
   `busy` while a non-zero segment remains; telemetry `{t, pose, seq, busy, v}` every step.
3. **Operator model.** `p_command` — proportional law on along-track distance (plus remaining course
   length for intermediate waypoints) and heading error, reversing when the target is behind; reaction
   time as a pipeline delay; multiplicative command noise.
4. **Modes** in `run_episode`: `continuous` (control on delayed telemetry), `move_and_wait`
   (`plan_move`: turn-then-drive open-loop plan with judgement error, re-plan only when the display
   shows the previous plan finished and the robot at rest; timeout on lost plans), `predictive`
   (`predict_ghost`: telemetry pose + unacknowledged commands, optional `model_gain` error).
5. **Metrics.** Completion (declared on *telemetry*: final waypoint within tolerance, at rest, held),
   completion time, final error (true), overshoot past the final waypoint, RMS distance from the
   course polyline, path-length ratio, collisions (entries into inflated obstacles), commands, moves.
6. **Harness.** `sweep_latency(course, round_trips, modes, seeds)` → one row per (delay, mode) with
   seed-averaged metrics; `format_table`, `plot_sweep`.
7. **Theory.** `critical_gain`, `phase_margin`, `simulate_p_loop` (plain and Smith),
   `find_stability_limit` (bisection on simulated envelope growth), `oscillation_frequency`.

## API

```python
MODES = ("continuous", "move_and_wait", "predictive")
@dataclass Course(start, waypoints, obstacles).polyline()
@dataclass OperatorParams(k_v, k_w, reaction_time, noise, pass_radius, tolerance, settle_speed,
                          hold_time, mw_speed, mw_turn_rate, mw_error)
@dataclass RobotParams(v_max, w_max, radius);   @dataclass EpisodeResult(...).metrics()
class Channel: send(t, seq, payload) -> bool; receive(t) -> list[(seq, send_t, payload)]
class Robot:   accept(packets); step(dt); busy
p_command(pose, target, op, rp, extra_along=0.0) -> (v, w)
predict_ghost(pose, applied_seq, sent: {seq: (v, w)}, dt, model_gain=1.0) -> pose
plan_move(pose, target, op, rng) -> [(v, w, duration), ...]
run_episode(course, mode, round_trip, jitter=0, loss=0, op=None, robot=None, dt=0.02,
            t_max=120, seed=0, model_gain=1.0) -> EpisodeResult
sweep_latency(course, round_trips, modes=MODES, seeds=(0, 1, 2), **kw) -> list[dict]
critical_gain(tau); phase_margin(K, tau)
simulate_p_loop(K, tau, T=10, dt=1e-3, r=1, smith=False, tau_model=None) -> (t, x)
envelope_growth(t, x, r=1) -> float;  find_stability_limit(tau, ...) -> K;  oscillation_frequency(t, x, r=1)
```

Given in the starter: `wrap_angle`, `unicycle_step`, `polyline_distance`, the dataclasses,
`Channel.__init__`, `Robot.__init__`, `format_table`, `plot_sweep`, `envelope_growth`,
`oscillation_frequency`.

## Input / output

| | |
|---|---|
| **Input** | course (start pose, waypoints, obstacles), mode, round-trip delay (split equally up/down), jitter, loss, operator and robot parameters, seed |
| **Output** | `EpisodeResult`: metrics + trajectory `t`, `xy` and the operator's control-pose trace `ghost`; sweep rows (mean over seeds) |

## Constraints

- NumPy (+ Matplotlib for plots). Fixed seeds; the operator uses only packets it has received
  (sequence numbers and sender time stamps, no access to the robot's true state).
- Step order per $t=k\,\Delta t$: operator reads and decides → reaction pipeline → uplink; robot
  applies newest plan, integrates, sends telemetry stamped $t+\Delta t$. With this order and a
  perfect model, the predictive run is the zero-delay run shifted by exactly the round trip.
- Tests < 30 s in total.

## Expected behaviour

Reference sweep, L-shaped course (0,0) → (3,0) → (3,3) → (0,3), default operator ($k_v = 1$ s⁻¹,
reaction 0.2 s), mean of 3 seeds:

| Round trip [s] | continuous: time / overshoot | move-and-wait: time / overshoot | predictive: time / overshoot |
|---|---|---|---|
| 0.0 | 12.5 s / 0.00 m | 32.7 s / 0.24 m | 12.5 s / 0.00 m |
| 0.5 | 23.2 s / 0.00 m | 35.8 s / 0.24 m | 13.0 s / 0.00 m |
| 1.0 | 45.3 s / 0.72 m | 38.7 s / 0.24 m | 13.5 s / 0.00 m |
| 2.0 | not completed in 120 s / 2.62 m | 44.7 s / 0.24 m | 14.6 s / 0.00 m |

Continuous control's effective loop delay is round trip + reaction time; with $k_v=1$ it rings
around 1 s and diverges at 2 s ($K\tau_{\text{eff}}\approx2.2>\pi/2$). Move-and-wait's time grows
by exactly (number of moves) × Δτ (≈ 6 moves here). Numeric stability limit at τ = 0.5 s:
3.13 s⁻¹ vs $\pi/(2\tau)=3.14$ s⁻¹.

## Test cases (`tests/test_teleop.py`)

| Test | Checks |
|---|---|
| `test_channel_delay_and_loss`, `test_robot_ignores_stale_packets`, `test_robot_executes_timed_plan_then_stops` | channel timing and loss rate; sequence-number discipline; timed plans |
| `test_ghost_is_exact_with_perfect_model` | dead reckoning over unacknowledged commands |
| `test_zero_latency_baseline_converges` | τ = 0: completes, within tolerance, no overshoot, no collisions |
| `test_predictive_identical_to_continuous_without_delay` | modes coincide at τ = 0 (bit-identical trajectory) |
| `test_predictive_display_only_adds_the_delay` | perfect-model predictive time = zero-delay time + τ (± 2 steps) |
| `test_continuous_high_gain_and_latency_oscillates` | high $k_v$ and τ: overshoot > 0.3 m, ≥ 3 error sign changes, slow or no completion |
| `test_move_and_wait_trades_time_for_accuracy` | at τ = 1.5 s: less overshoot and path error than continuous, slower than zero-delay control |
| `test_move_and_wait_time_linear_in_delay` | $T(\tau)-T(0)=n\tau$ (Ferrell) |
| `test_predictive_robust_to_jitter_loss_and_model_error` | completes under jitter/loss/20 % gain error, faster than raw; model error degrades accuracy |
| `test_collisions_counted`, `test_sweep_harness` | metrics bookkeeping; harness shape and determinism |
| `test_critical_gain_formula`, `test_stability_boundary_matches_theory`, `test_decay_below_and_growth_above_limit`, `test_oscillation_frequency_at_limit_equals_gain` | $K\tau<\pi/2$ within 2 %; ω = K at the limit within 5 % |
| `test_smith_predictor_removes_delay_from_loop` | K τ = 2: plain loop unstable, Smith response $1-e^{-K(t-\tau)}$ |

## Milestones

1. Channel and robot (unit tests first), then the 1-D delay loop and the stability-limit finder.
2. Continuous mode at τ = 0, then with delay; watch the ringing appear near $K\tau_{\text{eff}}\approx1$.
3. Predictive ghost; verify the exact "+τ" shift before adding jitter and loss.
4. Move-and-wait; verify the linear-in-delay law. Then the sweep and plots.

## Extension challenges

- Add a watchdog: the robot stops if no command arrives within $T_w$; measure the effect under 20 % loss.
- Draw the ghost with an uncertainty band ($\sigma_x\approx\sigma_v\tau$, 06.5 §5) and let the operator
  slow down when the band is wide.
- Replace the synthetic operator with keyboard input (pygame) and run a small within-subject study;
  record RTLX workload per condition (06.5 §8).
- Adaptive operator gain: lower $k_v$ as measured delay grows to keep 45° phase margin
  ($K=\pi/(4\tau)$) and compare with move-and-wait.
- Wave-variable force feedback for a 1-DOF master–slave pair; verify passivity numerically.

## Hints

<details class="answer"><summary>Hint 1 — exact predictive shift</summary>

Send one hold-command per step and give telemetry the sequence number of the command the robot
executed during the step that produced the pose. The ghost integrates every command with a larger
sequence number for one step each. Then the ghost equals the pose the robot will have once the
commands in flight are applied, and the whole run is the zero-delay run shifted by τ.

</details>

<details class="answer"><summary>Hint 2 — when is move-and-wait "settled"?</summary>

Require both: telemetry's applied sequence number ≥ the last plan you sent, and `busy` false.
Checking only "speed ≈ 0" re-plans during the turn-in-place leg or before the plan has even arrived.

</details>

<details class="answer"><summary>Hint 3 — detecting the stability boundary</summary>

Simulate ≥ 60 τ with Δt = τ/200 and compare the maximum error in the last third with that in the
middle third. Near the boundary the growth rate is $\operatorname{Re}\,ds/dK \approx 0.45$ per unit
of $K$ (differentiate $s+Ke^{-s\tau}=0$ at $s=jK$), so a 1 % gain change is visible over 20 τ.

</details>

## How to run

```bash
python -m pytest projects/p11-teleoperation                  # your starter
EOD_SOLUTION=1 python -m pytest projects/p11-teleoperation   # reference solution
python projects/p11-teleoperation/solution/teleop.py         # sweep table + stability limit
```
