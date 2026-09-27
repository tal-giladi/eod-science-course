"""Tests for P11 -- teleoperation experiment harness. Run from the repo root:

    python -m pytest projects/p11-teleoperation             (your starter)
    EOD_SOLUTION=1 python -m pytest projects/p11-teleoperation   (reference solution)
"""
import os, sys, pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
import teleop as mod  # noqa: E402

import math

import numpy as np
import pytest

DT = 0.02
COURSE = mod.Course(start=(0.0, 0.0, 0.0), waypoints=((3.0, 0.0), (3.0, 3.0), (0.0, 3.0)))
LINE = mod.Course(start=(0.0, 0.0, 0.0), waypoints=((4.0, 0.0),))


# ---------------------------------------------------------------- channel & robot
def test_channel_delay_and_loss():
    ch = mod.Channel(0.3, 0.0, 0.0)
    ch.send(1.0, 1, "a")
    assert ch.receive(1.29) == []
    got = ch.receive(1.3)
    assert [g[0] for g in got] == [1] and got[0][1] == 1.0
    lossy = mod.Channel(0.0, 0.0, 0.25, np.random.default_rng(0))
    ok = sum(lossy.send(0.0, i, None) for i in range(4000))
    assert ok / 4000 == pytest.approx(0.75, abs=0.03)


def test_robot_ignores_stale_packets():
    bot = mod.Robot((0, 0, 0))
    bot.accept([(5, 0.0, [(1.0, 0.0, math.inf)])])
    bot.accept([(3, 0.0, [(0.0, 1.0, math.inf)])])      # older packet arriving late (jitter)
    bot.step(1.0)
    assert bot.seq == 5 and bot.x == pytest.approx(1.0) and bot.th == pytest.approx(0.0)


def test_robot_executes_timed_plan_then_stops():
    bot = mod.Robot((0, 0, 0))
    bot.accept([(1, 0.0, [(0.0, 1.0, math.pi / 2), (0.5, 0.0, 2.0)])])
    for _ in range(300):
        bot.step(DT)
    assert (bot.x, bot.y) == pytest.approx((0.0, 1.0), abs=1e-6)
    assert not bot.busy and bot.v == 0.0


def test_ghost_is_exact_with_perfect_model():
    sent = {1: (0.5, 0.0), 2: (0.5, 0.0), 3: (0.5, 0.2)}
    g = mod.predict_ghost((0.0, 0.0, 0.0), 1, sent, 0.1)
    x, y, th = 0.0, 0.0, 0.0
    for v, w in (sent[2], sent[3]):
        x, y, th = mod.unicycle_step(x, y, th, v, w, 0.1)
    assert g == pytest.approx((x, y, th))


# ---------------------------------------------------------------- closed-loop behaviour
def test_zero_latency_baseline_converges():
    r = mod.run_episode(COURSE, "continuous", 0.0, seed=1)
    assert r.completed and r.completion_time < 30
    assert r.final_error < mod.OperatorParams().tolerance
    assert r.overshoot < 0.05 and r.collisions == 0


def test_predictive_identical_to_continuous_without_delay():
    a = mod.run_episode(COURSE, "continuous", 0.0, seed=3)
    b = mod.run_episode(COURSE, "predictive", 0.0, seed=3)
    assert a.metrics() == b.metrics()
    assert np.array_equal(a.xy, b.xy)


def test_predictive_display_only_adds_the_delay():
    base = mod.run_episode(COURSE, "continuous", 0.0, seed=4)
    for tau in (0.4, 1.2):
        p = mod.run_episode(COURSE, "predictive", tau, seed=4)
        assert p.completed
        assert p.completion_time == pytest.approx(base.completion_time + tau, abs=2 * DT)
        assert p.final_error < mod.OperatorParams().tolerance


def test_continuous_high_gain_and_latency_oscillates():
    op = mod.OperatorParams(k_v=1.5, reaction_time=0.0, noise=0.0)
    calm = mod.run_episode(LINE, "continuous", 0.0, op=op, t_max=60)
    wild = mod.run_episode(LINE, "continuous", 0.8, op=op, t_max=60)
    assert calm.completed and calm.overshoot < 0.02
    assert wild.overshoot > 0.3
    assert (not wild.completed) or wild.completion_time > 2 * calm.completion_time
    e = 4.0 - wild.xy[:, 0]                              # along-track error
    crossings = np.count_nonzero(np.signbit(e[1:]) != np.signbit(e[:-1]))
    assert crossings >= 3                                # it rings, not a single overshoot


def test_move_and_wait_trades_time_for_accuracy():
    tau = 1.5
    cont = mod.run_episode(COURSE, "continuous", tau, seed=2, t_max=150)
    mw = mod.run_episode(COURSE, "move_and_wait", tau, seed=2, t_max=150)
    fast = mod.run_episode(COURSE, "continuous", 0.0, seed=2)
    assert mw.completed and mw.final_error < mod.OperatorParams().tolerance
    assert mw.overshoot < cont.overshoot
    assert mw.path_error_rms < cont.path_error_rms
    assert mw.completion_time > fast.completion_time     # accuracy is paid for in time


def test_move_and_wait_time_linear_in_delay():
    t0 = mod.run_episode(COURSE, "move_and_wait", 0.0, seed=5, t_max=200)
    for tau in (1.0, 2.0):
        r = mod.run_episode(COURSE, "move_and_wait", tau, seed=5, t_max=200)
        assert r.n_moves == t0.n_moves
        # each move-and-wait cycle costs exactly one extra round trip (Ferrell)
        assert r.completion_time - t0.completion_time == pytest.approx(r.n_moves * tau, abs=2 * DT * r.n_moves)


def test_predictive_robust_to_jitter_loss_and_model_error():
    perfect = mod.run_episode(COURSE, "predictive", 1.0, seed=6)
    noisy = mod.run_episode(COURSE, "predictive", 1.0, jitter=0.1, loss=0.05, seed=6)
    biased = mod.run_episode(COURSE, "predictive", 1.0, model_gain=0.8, seed=6)
    raw = mod.run_episode(COURSE, "continuous", 1.0, seed=6)
    for r in (noisy, biased):
        assert r.completed and r.final_error < mod.OperatorParams().tolerance
        assert r.completion_time < raw.completion_time
    # a ghost that under-predicts motion makes the operator over-drive: accuracy degrades
    assert biased.path_error_rms > perfect.path_error_rms
    assert biased.overshoot >= perfect.overshoot


def test_collisions_counted():
    blocked = mod.Course(start=(0.0, 0.0, 0.0), waypoints=((4.0, 0.0),), obstacles=((2.0, 0.1, 0.2),))
    assert mod.run_episode(blocked, "continuous", 0.0).collisions >= 1
    assert mod.run_episode(LINE, "continuous", 0.0).collisions == 0


def test_sweep_harness():
    rows = mod.sweep_latency(LINE, (0.0, 0.5), modes=("continuous", "predictive"), seeds=(0, 1))
    assert [(r["round_trip"], r["mode"]) for r in rows] == [
        (0.0, "continuous"), (0.0, "predictive"), (0.5, "continuous"), (0.5, "predictive")]
    assert all(r["n"] == 2 and 0 <= r["completion_rate"] <= 1 for r in rows)
    assert rows == mod.sweep_latency(LINE, (0.0, 0.5), modes=("continuous", "predictive"), seeds=(0, 1))
    assert "completion_time" in mod.format_table(rows)


# ---------------------------------------------------------------- stability theory
def test_critical_gain_formula():
    assert mod.critical_gain(0.5) == pytest.approx(math.pi)
    assert mod.phase_margin(1.57, 0.5) == pytest.approx(math.pi / 2 - 0.785)


def test_stability_boundary_matches_theory():
    for tau in (0.25, 0.5, 1.0):
        k_num = mod.find_stability_limit(tau)
        assert k_num == pytest.approx(mod.critical_gain(tau), rel=0.02)


def test_decay_below_and_growth_above_limit():
    tau = 0.5
    kc = mod.critical_gain(tau)
    t, x = mod.simulate_p_loop(0.9 * kc, tau, T=30 * tau, dt=tau / 200)
    assert mod.envelope_growth(t, x) < 1
    t, x = mod.simulate_p_loop(1.1 * kc, tau, T=30 * tau, dt=tau / 200)
    assert mod.envelope_growth(t, x) > 1


def test_oscillation_frequency_at_limit_equals_gain():
    tau = 0.5
    kc = mod.critical_gain(tau)
    t, x = mod.simulate_p_loop(kc, tau, T=40 * tau, dt=tau / 400)
    assert mod.oscillation_frequency(t, x) == pytest.approx(kc, rel=0.05)


def test_smith_predictor_removes_delay_from_loop():
    K, tau = 4.0, 0.5                                    # K tau = 2 > pi/2
    t, x = mod.simulate_p_loop(K, tau, T=10.0)
    assert mod.envelope_growth(t, x) > 1                 # plain loop unstable
    t, xs = mod.simulate_p_loop(K, tau, T=10.0, smith=True)
    assert xs[1500] == pytest.approx(1 - math.exp(-(1.5 - 0.5) * K), abs=0.01)
    assert abs(xs[-1] - 1.0) < 1e-3
