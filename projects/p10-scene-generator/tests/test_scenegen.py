"""Tests for P10 -- synthetic scene generator. Run from the repo root:

    python -m pytest projects/p10-scene-generator             (your starter)
    EOD_SOLUTION=1 python -m pytest projects/p10-scene-generator   (reference solution)
"""
import os, sys, pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / ("solution" if os.environ.get("EOD_SOLUTION") else "starter")))
import scenegen as mod  # noqa: E402

import json
import math

import numpy as np
import pytest

SMALL = {**mod.DEFAULT_FIXED, "image_size": 64}


def _flat_xi(**over):
    """A mid-range parameter vector with flat terrain and no foliage."""
    xi = {k: (d["low"] + d["high"]) / 2 if d["dist"] != "int" else d["low"]
          for k, d in mod.DEFAULT_SPEC.items()}
    xi.update(terrain_amplitude_m=0.0, foliage_cover=0.0, n_objects=1, n_clutter=0)
    xi.update(over)
    return xi


def _container(cx=32.0, cy=32.0, h=0.2, bf=0.0, cover=0.0, angle=0.3):
    p = mod.sample_object_params("container", np.random.default_rng(0))
    p.update(height_m=h, length_m=0.4, width_m=0.2, angle_rad=angle)
    return mod.SceneObject("container", cx, cy, p, bf, cover)


def _scene(xi, objects, n=64):
    fixed = {**mod.DEFAULT_FIXED, "image_size": n}
    terrain = np.zeros((n, n))
    foliage = np.zeros((n, n), dtype=bool)
    return mod.assemble_scene(xi, fixed, terrain, objects, foliage)


# ---------------------------------------------------------------- physics
def test_damping_depth_value():
    assert mod.damping_depth(5e-7) == pytest.approx(0.117, abs=5e-4)


def test_soil_temperature_satisfies_heat_equation():
    alpha, z, t, h, k = 5e-7, 0.05, 20_000.0, 1e-3, 10.0
    dT_dt = (mod.soil_temperature(z, t + k, alpha=alpha) - mod.soil_temperature(z, t - k, alpha=alpha)) / (2 * k)
    d2T = (mod.soil_temperature(z + h, t, alpha=alpha) - 2 * mod.soil_temperature(z, t, alpha=alpha)
           + mod.soil_temperature(z - h, t, alpha=alpha)) / h ** 2
    assert abs(dT_dt - alpha * d2T) / abs(dT_dt) < 1e-3


def test_thermal_contrast_changes_sign_over_day_for_shallow_object():
    t = np.linspace(0, 86_400, 289)
    c = mod.thermal_contrast(t, 0.02, 10.0, 5e-7, gain=1.3, lag_rad=0.4)
    assert c.max() > 0.5 and c.min() < -0.5          # thermal crossover exists
    deep = mod.thermal_contrast(t, 0.5, 10.0, 5e-7, gain=1.3, lag_rad=0.4)
    assert np.abs(deep).max() < 0.05 * np.abs(c).max()  # deep objects are thermally invisible


def test_xray_uniform_slab_matches_beer_lambert():
    mu, t, N0 = 0.3, 4.0, 1e5
    mu_maps = np.full((1, 64, 64), mu)
    th = np.full((1, 64, 64), t)
    img = mod.xray_projection(mu_maps, th, N0, np.random.default_rng(1))
    assert np.mean(np.exp(-img)) == pytest.approx(math.exp(-mu * t), rel=0.01)


def test_dual_energy_ratio_independent_of_thickness():
    ratios = []
    for t in (1.0, 3.0, 9.0):
        lo = mod.xray_projection(np.full((1, 4, 4), 0.6), np.full((1, 4, 4), t), noise=False)
        hi = mod.xray_projection(np.full((1, 4, 4), 0.3), np.full((1, 4, 4), t), noise=False)
        ratios.append(float(lo.mean() / hi.mean()))
    assert np.allclose(ratios, 2.0)


# ---------------------------------------------------------------- randomisation
def test_parameters_within_declared_ranges():
    rng = np.random.default_rng(7)
    for _ in range(300):
        xi = mod.sample_parameters(mod.DEFAULT_SPEC, rng)
        assert mod.check_parameters(xi, mod.DEFAULT_SPEC) == []
        assert isinstance(xi["n_objects"], int)
    spec = {"a": {"dist": "choice", "values": ["x", "y"]}, "b": {"dist": "fixed", "value": 3}}
    xi = mod.sample_parameters(spec, rng)
    assert xi["a"] in ("x", "y") and xi["b"] == 3
    assert mod.check_parameters({"a": "z", "b": 3}, spec) != []


def test_object_parameters_within_family_ranges():
    data = mod.generate_dataset(6, seed=11, fixed=SMALL)
    for s in data:
        for o in s["objects"]:
            for k, (lo, hi) in mod.OBJECT_FAMILIES[o["cls"]].items():
                assert lo <= o["params"][k] <= hi, (o["cls"], k)
            assert 0.0 <= o["burial_fraction"] <= 1.0
            if o["cover_depth_m"] > 0:
                assert o["burial_fraction"] == 1.0 and o["cls"] != "clutter"


def test_sampling_is_order_independent():
    spec2 = dict(reversed(list(mod.DEFAULT_SPEC.items())))
    a = mod.sample_parameters(mod.DEFAULT_SPEC, np.random.default_rng(3))
    b = mod.sample_parameters(spec2, np.random.default_rng(3))
    assert a == b


# ---------------------------------------------------------------- determinism
def test_deterministic_by_seed():
    a = mod.generate_dataset(3, seed=5, fixed=SMALL)
    b = mod.generate_dataset(3, seed=5, fixed=SMALL)
    c = mod.generate_dataset(3, seed=6, fixed=SMALL)
    for sa, sb in zip(a, b):
        assert sa["xi"] == sb["xi"]
        for key in sa["renders"]:
            assert sa["renders"][key].tobytes() == sb["renders"][key].tobytes()
        for la, lb in zip(sa["labels"], sb["labels"]):
            assert la["box"] == lb["box"] and la["mask"].tobytes() == lb["mask"].tobytes()
    assert any(sa["renders"]["rgb"].tobytes() != sc["renders"]["rgb"].tobytes() for sa, sc in zip(a, c))


def test_render_shapes_and_ranges():
    s = mod.generate_dataset(1, seed=2, fixed=SMALL)[0]
    r = s["renders"]
    assert r["rgb"].shape == (64, 64, 3) and r["rgb"].min() >= 0 and r["rgb"].max() <= 1
    for key in ("thermal", "depth", "xray_low", "xray_high"):
        assert r[key].shape == (64, 64) and np.isfinite(r[key]).all()
    assert r["gpr"].shape == (SMALL["gpr_n_t"], 64)
    assert 250 < r["thermal"].mean() < 330


# ---------------------------------------------------------------- labels vs renders
def test_labels_consistent_with_renders():
    data = mod.generate_dataset(8, seed=21, fixed=SMALL)
    n_vis = n_hidden = 0
    for s in data:
        scene = s["scene"]
        for lab in s["labels"]:
            m, am = lab["mask"], lab["amodal_mask"]
            assert (m.sum() > 0) == lab["visible"]
            assert (lab["box"] is None) == (not lab["visible"])
            assert not (m & ~am).any()                      # visible part lies in the footprint
            assert 0.0 <= lab["visibility"] <= 1.0
            if lab["positive"]:
                assert lab["visible"]
            if lab["visible"]:
                n_vis += 1
                x0, y0, x1, y1 = lab["box"]
                ys, xs = np.nonzero(m)
                assert xs.min() == x0 and xs.max() == x1 and ys.min() == y0 and ys.max() == y1
            else:
                n_hidden += 1
            if lab["top_depth_m"] > 0:                       # entirely below ground
                assert not lab["visible"]
        # removing an object changes the (noise-free) depth exactly on its visible mask
        for k, lab in enumerate(s["labels"]):
            surf, _ = mod.compose_surface(scene.terrain, scene.footprints, scene.z_top,
                                          scene.foliage, scene.xi["foliage_height_m"], exclude=k)
            changed = np.abs(surf - scene.surface) > 1e-12
            assert np.array_equal(changed, lab["mask"])
    assert n_vis > 0 and n_hidden > 0


def test_fully_buried_object_invisible_but_seen_by_xray():
    xi = _flat_xi()
    buried = _scene(xi, [_container(bf=1.0, cover=0.05)])
    empty = _scene(xi, [])
    lab = mod.make_labels(buried)[0]
    assert not lab["visible"] and lab["mask"].sum() == 0 and lab["box"] is None
    assert lab["top_depth_m"] == pytest.approx(0.05)
    assert np.array_equal(mod.render_depth(buried, noise=False), mod.render_depth(empty, noise=False))
    xr = mod.render_xray(buried, noise=False) - mod.render_xray(empty, noise=False)
    assert (np.abs(xr[lab["amodal_mask"]]) > 0).all()


# ---------------------------------------------------------------- depth geometry
def test_depth_geometry_flat_ground():
    xi = _flat_xi(camera_altitude_m=2.0)
    h = 0.2
    for bf, exposed in ((0.0, h), (0.5, h / 2)):
        sc = _scene(xi, [_container(h=h, bf=bf)])
        d = mod.render_depth(sc, noise=False)
        m = mod.make_labels(sc)[0]["mask"]
        assert np.allclose(d[~m], 2.0)
        assert np.allclose(d[m], 2.0 - exposed)
    # a lying cylinder is highest along its axis: depth minimum = altitude - diameter
    p = mod.sample_object_params("cylinder", np.random.default_rng(1))
    p.update(diameter_m=0.16, length_m=0.4, angle_rad=0.0)
    sc = _scene(xi, [mod.SceneObject("cylinder", 32.0, 32.0, p)])
    d = mod.render_depth(sc, noise=False)
    assert d.min() == pytest.approx(2.0 - 0.16, abs=1e-3)


def test_foliage_occludes():
    n = 64
    xi = _flat_xi(foliage_height_m=0.3)
    fixed = {**mod.DEFAULT_FIXED, "image_size": n}
    foliage = np.zeros((n, n), dtype=bool)
    foliage[:, :32] = True
    sc = mod.assemble_scene(xi, fixed, np.zeros((n, n)), [_container(cx=32.0, h=0.2, angle=0.0)], foliage)
    lab = mod.make_labels(sc)[0]
    assert lab["visible"] and 0.2 < lab["visibility"] < 0.8
    assert not lab["mask"][:, :32].any()


# ---------------------------------------------------------------- GPR
def test_gpr_hyperbola_timing():
    xi = _flat_xi(gpr_eps_r=9.0, gpr_noise=0.0)
    obj = _container(cx=32.0, cy=32.0, bf=1.0, cover=0.1, angle=0.0)
    sc = _scene(xi, [obj])
    b = mod.render_gpr(sc, noise=False)
    fx = sc.fixed
    t = np.linspace(0, fx["gpr_window_ns"], fx["gpr_n_t"])
    dt = t[1] - t[0]
    v = mod.gpr_velocity(9.0)
    assert v == pytest.approx(0.0999, abs=1e-3)
    t_air = 2 * fx["gpr_antenna_height_m"] / mod.C_LIGHT
    apex = mod.make_labels(sc)[0]["gpr_apex"]
    assert apex[1] == pytest.approx(t_air + 2 * 0.1 / v, rel=1e-6)
    late = t > t_air + 1.0                              # skip the surface reflection
    for off in (0, 8, 16):
        col = b[:, 32 + off]
        t_pk = t[late][np.argmax(col[late])]
        x = off * fx["gsd_m"]
        assert t_pk == pytest.approx(t_air + 2 * math.hypot(x, 0.1) / v, abs=1.5 * dt)


# ---------------------------------------------------------------- dataset card
def test_dataset_card_lists_every_factor(tmp_path):
    data = mod.generate_dataset(3, seed=1, fixed=SMALL)
    card = mod.build_dataset_card(data, mod.DEFAULT_SPEC, SMALL, seed=1)
    assert set(card["parameter_distribution"]) == set(mod.DEFAULT_SPEC)
    assert set(card["fixed_factors"]) == set(SMALL)
    for section in ("provenance", "labelling_policy", "physics_models", "intended_use",
                    "known_gaps", "safety_review", "statistics"):
        assert section in card
    assert card["statistics"]["n_samples"] == 3
    pj, pm = mod.write_dataset_card(card, tmp_path)
    back = json.loads(pj.read_text(encoding="utf-8"))
    assert back["parameter_distribution"].keys() == card["parameter_distribution"].keys()
    md = pm.read_text(encoding="utf-8")
    for k in list(mod.DEFAULT_SPEC) + list(SMALL):
        assert f"`{k}`" in md
    assert "fictional" in md.lower()
