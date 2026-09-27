"""scenegen -- procedural synthetic EOD-style scenes with multi-sensor renders (Project P10).

Reference solution. Only FICTIONAL, generic geometric objects are modelled (boxes, lying
cylinders, flat irregular plates, rocks). Nothing here describes any real ordnance or device;
materials are fictional ("mu" values in 1/cm are invented), yields are not involved at all.

Coordinate conventions
----------------------
* Images are ``(H, W)`` arrays, row index ``i`` = y, column index ``j`` = x, pixel centres at
  integer coordinates. Ground sample distance ``gsd_m`` converts pixels to metres.
* Heights ``z`` are in metres, positive up. The camera is an orthographic nadir camera at
  ``camera_altitude_m`` above ``z = 0``; depth = altitude - visible surface height.
* A parameter vector ``xi`` (dict) holds every scene-level randomised factor; every object
  carries its own ``params`` dict sampled from ``OBJECT_FAMILIES``. Both are logged per sample.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

# ----------------------------------------------------------------------------- constants
CLASSES = ("container", "cylinder", "debris", "clutter")
CLASS_ID = {c: i for i, c in enumerate(CLASSES)}
ITEM_CLASSES = ("container", "cylinder", "debris")      # "objects of interest" (fictional)
OMEGA = 2.0 * np.pi / 86_400.0                            # diurnal angular frequency [rad/s]
C_LIGHT = 0.299792458                                     # speed of light [m/ns]
GENERATOR_VERSION = "scenegen-1.0"

# Scene-level randomisation distribution P_rand(xi). Every factor: dist + range + unit + doc.
DEFAULT_SPEC: dict[str, dict] = {
    "n_objects": {"dist": "int", "low": 1, "high": 5, "unit": "-",
                  "doc": "number of fictional items of interest (container/cylinder/debris)"},
    "n_clutter": {"dist": "int", "low": 0, "high": 12, "unit": "-",
                  "doc": "number of rocks/clutter (distractors)"},
    "terrain_amplitude_m": {"dist": "uniform", "low": 0.0, "high": 0.04, "unit": "m",
                            "doc": "std of terrain height-field undulation"},
    "terrain_corr_px": {"dist": "uniform", "low": 6.0, "high": 30.0, "unit": "px",
                        "doc": "correlation length of terrain undulation"},
    "soil_brightness": {"dist": "uniform", "low": 0.25, "high": 0.6, "unit": "-",
                        "doc": "mean soil albedo"},
    "soil_hue_shift": {"dist": "uniform", "low": -0.1, "high": 0.1, "unit": "-",
                       "doc": "red-blue tint of soil albedo"},
    "texture_amplitude": {"dist": "uniform", "low": 0.0, "high": 0.15, "unit": "-",
                          "doc": "relative amplitude of soil texture"},
    "texture_corr_px": {"dist": "uniform", "low": 1.0, "high": 6.0, "unit": "px",
                        "doc": "correlation length of soil texture"},
    "sun_elevation_deg": {"dist": "uniform", "low": 15.0, "high": 80.0, "unit": "deg",
                          "doc": "sun elevation for RGB shading"},
    "sun_azimuth_deg": {"dist": "uniform", "low": 0.0, "high": 360.0, "unit": "deg",
                        "doc": "sun azimuth for RGB shading"},
    "ambient": {"dist": "uniform", "low": 0.1, "high": 0.4, "unit": "-",
                "doc": "ambient (sky) fraction of illumination"},
    "camera_gain": {"dist": "uniform", "low": 0.7, "high": 1.3, "unit": "-",
                    "doc": "RGB sensor gain"},
    "camera_offset": {"dist": "uniform", "low": -0.05, "high": 0.05, "unit": "-",
                      "doc": "RGB sensor offset"},
    "rgb_noise_sigma": {"dist": "uniform", "low": 0.0, "high": 0.03, "unit": "-",
                        "doc": "RGB additive Gaussian noise std"},
    "foliage_cover": {"dist": "uniform", "low": 0.0, "high": 0.3, "unit": "-",
                      "doc": "fraction of scene covered by occluding foliage"},
    "foliage_height_m": {"dist": "uniform", "low": 0.15, "high": 0.4, "unit": "m",
                         "doc": "canopy height of foliage above terrain"},
    "burial_max": {"dist": "uniform", "low": 0.0, "high": 1.0, "unit": "-",
                   "doc": "per-object burial fraction ~ U(0, burial_max)"},
    "p_fully_buried": {"dist": "uniform", "low": 0.0, "high": 0.4, "unit": "-",
                       "doc": "probability an item is fully buried (burial fraction 1 + cover)"},
    "hour": {"dist": "uniform", "low": 0.0, "high": 24.0, "unit": "h",
             "doc": "local solar time of capture (drives the diurnal thermal model)"},
    "T_mean_K": {"dist": "uniform", "low": 280.0, "high": 305.0, "unit": "K",
                 "doc": "daily mean soil temperature"},
    "diurnal_amplitude_K": {"dist": "uniform", "low": 3.0, "high": 15.0, "unit": "K",
                            "doc": "surface diurnal temperature amplitude A0"},
    "soil_diffusivity": {"dist": "loguniform", "low": 2e-7, "high": 1e-6, "unit": "m^2/s",
                         "doc": "soil thermal diffusivity alpha"},
    "thermal_noise_K": {"dist": "uniform", "low": 0.02, "high": 0.2, "unit": "K",
                        "doc": "thermal sensor noise (NETD)"},
    "xray_N0": {"dist": "loguniform", "low": 1e3, "high": 1e5, "unit": "counts",
                "doc": "incident photon count per pixel (dose)"},
    "gpr_eps_r": {"dist": "uniform", "low": 3.0, "high": 25.0, "unit": "-",
                  "doc": "soil relative permittivity (sets GPR velocity)"},
    "gpr_noise": {"dist": "uniform", "low": 0.0, "high": 0.05, "unit": "-",
                  "doc": "GPR additive noise std (relative to unit wavelet)"},
    "camera_altitude_m": {"dist": "uniform", "low": 1.5, "high": 3.0, "unit": "m",
                          "doc": "nadir camera altitude above z = 0"},
}

# Factors deliberately held fixed (the dataset card must list them).
DEFAULT_FIXED: dict[str, object] = {
    "image_size": 128,
    "gsd_m": 0.02,
    "soil_column_m": 0.2,
    "mu_soil_low": 0.05,
    "mu_soil_high": 0.035,
    "visibility_threshold": 0.25,
    "depth_noise_m": 0.003,
    "thermal_peak_hour": 14.0,
    "gpr_row": None,               # None -> centre row
    "gpr_n_t": 128,
    "gpr_window_ns": 20.0,
    "gpr_freq_ghz": 1.5,
    "gpr_antenna_height_m": 0.05,
    "gpr_attenuation_np_per_m": 2.0,
    "foliage_rgb": (0.15, 0.35, 0.10),
}

# Per-object randomisation ranges (uniform). All fictional.
_COMMON = {
    "albedo_r": (0.1, 0.9), "albedo_g": (0.1, 0.9), "albedo_b": (0.1, 0.9),
    "thermal_gain": (0.5, 1.6), "thermal_lag_rad": (-0.8, 0.8),
    "mu_low": (0.04, 0.3), "high_low_ratio": (0.5, 0.9), "reflectivity": (0.3, 1.0),
    "angle_rad": (0.0, math.pi),
}
OBJECT_FAMILIES: dict[str, dict[str, tuple[float, float]]] = {
    "container": {**_COMMON, "length_m": (0.25, 0.6), "width_m": (0.15, 0.35),
                  "height_m": (0.08, 0.25)},
    "cylinder": {**_COMMON, "length_m": (0.2, 0.6), "diameter_m": (0.06, 0.2)},
    "debris": {**_COMMON, "radius_m": (0.05, 0.2), "height_m": (0.01, 0.05),
               "roughness": (0.05, 0.35)},
    "clutter": {**_COMMON, "radius_m": (0.02, 0.08), "height_m": (0.02, 0.08),
                "aspect": (0.5, 1.0)},
}
COVER_DEPTH_RANGE_M = (0.01, 0.15)


# ----------------------------------------------------------------------------- data classes
@dataclass
class SceneObject:
    """One fictional object. ``cx, cy`` in pixels; ``params`` sampled from OBJECT_FAMILIES."""
    cls: str
    cx: float
    cy: float
    params: dict
    burial_fraction: float = 0.0
    cover_depth_m: float = 0.0
    harmonics: tuple = ()          # debris outline: ((k, a_k, psi_k), ...)


@dataclass
class Scene:
    """A composed scene: geometry + z-buffer. ``owner`` = -1 terrain, -2 foliage, k object."""
    xi: dict
    fixed: dict
    terrain: np.ndarray
    foliage: np.ndarray
    objects: list
    footprints: list = field(default_factory=list)
    z_bottom: list = field(default_factory=list)
    z_top: list = field(default_factory=list)
    surface: np.ndarray | None = None
    owner: np.ndarray | None = None


# ----------------------------------------------------------------------------- helpers (given)
def smooth_noise(shape: tuple[int, int], corr_px: float, rng: np.random.Generator) -> np.ndarray:
    """Zero-mean, unit-std Gaussian random field with Gaussian correlation length ``corr_px``
    (FFT filtering of white noise, periodic boundaries)."""
    white = rng.standard_normal(shape)
    if corr_px <= 0.5:
        f = white
    else:
        ky = np.fft.fftfreq(shape[0])[:, None]
        kx = np.fft.fftfreq(shape[1])[None, :]
        filt = np.exp(-2.0 * (np.pi * corr_px) ** 2 * (kx ** 2 + ky ** 2))
        f = np.real(np.fft.ifft2(np.fft.fft2(white) * filt))
    s = f.std()
    return (f - f.mean()) / (s if s > 0 else 1.0)


def ricker(t: np.ndarray, f_ghz: float) -> np.ndarray:
    """Ricker (Mexican-hat) wavelet with peak 1 at t = 0; ``t`` in ns, ``f_ghz`` in GHz."""
    a = (np.pi * f_ghz * t) ** 2
    return (1.0 - 2.0 * a) * np.exp(-a)


def pixel_grid(n: int) -> tuple[np.ndarray, np.ndarray]:
    """(yy, xx) integer pixel-centre coordinate grids for an n x n image."""
    yy, xx = np.mgrid[0:n, 0:n]
    return yy.astype(float), xx.astype(float)


def bbox_of(mask: np.ndarray):
    """Inclusive (x0, y0, x1, y1) bounding box of a boolean mask, or None if empty."""
    if not mask.any():
        return None
    ys, xs = np.nonzero(mask)
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


# ----------------------------------------------------------------------------- parameters
def sample_parameters(spec: dict, rng: np.random.Generator) -> dict:
    """Draw one scene-level parameter vector xi from ``spec``.

    Supported distributions: ``uniform`` (low, high), ``loguniform`` (low, high > 0),
    ``int`` (inclusive low..high), ``choice`` (``values`` list), ``fixed`` (``value``).
    Keys are sampled in sorted order so the result does not depend on dict insertion order.
    """
    xi = {}
    for name in sorted(spec):
        d = spec[name]
        kind = d["dist"]
        if kind == "uniform":
            xi[name] = float(rng.uniform(d["low"], d["high"]))
        elif kind == "loguniform":
            xi[name] = float(math.exp(rng.uniform(math.log(d["low"]), math.log(d["high"]))))
        elif kind == "int":
            xi[name] = int(rng.integers(d["low"], d["high"] + 1))
        elif kind == "choice":
            xi[name] = d["values"][int(rng.integers(len(d["values"])))]
        elif kind == "fixed":
            xi[name] = d["value"]
        else:
            raise ValueError(f"unknown distribution {kind!r} for {name}")
    return xi


def check_parameters(xi: dict, spec: dict) -> list[str]:
    """Return a list of human-readable violations (empty if ``xi`` lies in ``spec``'s support)."""
    bad = []
    for name, d in spec.items():
        if name not in xi:
            bad.append(f"{name}: missing")
            continue
        v, kind = xi[name], d["dist"]
        if kind in ("uniform", "loguniform"):
            if not (d["low"] <= v <= d["high"]):
                bad.append(f"{name}={v} outside [{d['low']}, {d['high']}]")
        elif kind == "int":
            if int(v) != v or not (d["low"] <= v <= d["high"]):
                bad.append(f"{name}={v} not an int in [{d['low']}, {d['high']}]")
        elif kind == "choice":
            if v not in d["values"]:
                bad.append(f"{name}={v} not in {d['values']}")
        elif kind == "fixed":
            if v != d["value"]:
                bad.append(f"{name}={v} != fixed {d['value']}")
    return bad


def sample_object_params(cls: str, rng: np.random.Generator) -> dict:
    """Sample the per-object parameters of family ``cls`` uniformly from OBJECT_FAMILIES."""
    fam = OBJECT_FAMILIES[cls]
    return {k: float(rng.uniform(lo, hi)) for k, (lo, hi) in sorted(fam.items())}


# ----------------------------------------------------------------------------- scene layout
def make_terrain(xi: dict, fixed: dict, rng: np.random.Generator) -> np.ndarray:
    """Height field [m], shape (N, N): ``terrain_amplitude_m`` x smooth_noise(corr)."""
    n = int(fixed["image_size"])
    return xi["terrain_amplitude_m"] * smooth_noise((n, n), xi["terrain_corr_px"], rng)


def make_foliage(xi: dict, fixed: dict, rng: np.random.Generator) -> np.ndarray:
    """Boolean occluder mask covering approximately ``foliage_cover`` of the image
    (thresholded smooth noise with correlation length 6 px)."""
    n = int(fixed["image_size"])
    field_ = smooth_noise((n, n), 6.0, rng)
    cover = xi["foliage_cover"]
    if cover <= 1e-3:
        return np.zeros((n, n), dtype=bool)
    return field_ > np.quantile(field_, 1.0 - cover)


def place_objects(xi: dict, fixed: dict, rng: np.random.Generator) -> list[SceneObject]:
    """Sample ``n_objects`` items (classes drawn uniformly from ITEM_CLASSES) and ``n_clutter``
    rocks at uniform positions (8 px margin), each with per-object params, burial fraction
    ~ U(0, burial_max) and, for items, full burial with probability ``p_fully_buried`` (then
    burial_fraction = 1 and cover_depth ~ U(COVER_DEPTH_RANGE_M)). Clutter is never fully buried."""
    n = int(fixed["image_size"])
    objs = []
    classes = [ITEM_CLASSES[int(rng.integers(len(ITEM_CLASSES)))] for _ in range(xi["n_objects"])]
    classes += ["clutter"] * xi["n_clutter"]
    for cls in classes:
        cx, cy = rng.uniform(8, n - 9, size=2)
        p = sample_object_params(cls, rng)
        bf = float(rng.uniform(0.0, xi["burial_max"]))
        cover = 0.0
        full = rng.uniform() < xi["p_fully_buried"]
        if cls != "clutter" and full:
            bf = 1.0
            cover = float(rng.uniform(*COVER_DEPTH_RANGE_M))
        harm = ()
        if cls == "debris":
            harm = tuple((k, float(rng.uniform(0, p["roughness"])), float(rng.uniform(0, 2 * np.pi)))
                         for k in (2, 3, 4, 5))
        objs.append(SceneObject(cls, float(cx), float(cy), p, bf, cover, harm))
    return objs


def object_height(obj: SceneObject) -> float:
    """Maximum vertical extent of the object [m]."""
    p = obj.params
    return p["diameter_m"] if obj.cls == "cylinder" else p["height_m"]


def object_geometry(obj: SceneObject, terrain: np.ndarray, gsd: float):
    """Footprint mask and per-pixel bottom/top heights of the object.

    The base height is ``z_ref - burial_fraction * H`` (minus ``cover_depth_m`` if fully buried),
    with ``z_ref`` the terrain height at the object's centre pixel and H = object_height.
    Shapes (u along the long axis, v across, in metres, rotated by ``angle_rad``):

    * container: rectangle length x width, flat top at base + H;
    * cylinder: lying cylinder of diameter D; top/bottom = base + D/2 +/- sqrt(r^2 - v^2);
    * debris: star-shaped plate, radius R (1 + sum a_k cos(k phi + psi_k)), thickness H;
    * clutter: ellipse (R, aspect R), dome top base + H sqrt(1 - rho^2).

    Returns (footprint bool, z_bottom, z_top); z arrays are NaN outside the footprint.
    """
    n = terrain.shape[0]
    yy, xx = pixel_grid(n)
    p = obj.params
    ci = int(np.clip(round(obj.cy), 0, n - 1))
    cj = int(np.clip(round(obj.cx), 0, n - 1))
    z_ref = terrain[ci, cj]
    H = object_height(obj)
    base = z_ref - obj.burial_fraction * H - obj.cover_depth_m
    dx, dy = (xx - obj.cx) * gsd, (yy - obj.cy) * gsd
    ca, sa = math.cos(p["angle_rad"]), math.sin(p["angle_rad"])
    u = dx * ca + dy * sa
    v = -dx * sa + dy * ca
    zb = np.full(terrain.shape, np.nan)
    zt = np.full(terrain.shape, np.nan)
    if obj.cls == "container":
        fp = (np.abs(u) <= p["length_m"] / 2) & (np.abs(v) <= p["width_m"] / 2)
        zb[fp] = base
        zt[fp] = base + H
    elif obj.cls == "cylinder":
        r = p["diameter_m"] / 2
        fp = (np.abs(u) <= p["length_m"] / 2) & (np.abs(v) < r)
        half = np.sqrt(np.maximum(r * r - v * v, 0.0))
        zb[fp] = (base + r - half)[fp]
        zt[fp] = (base + r + half)[fp]
    elif obj.cls == "debris":
        phi = np.arctan2(v, u)
        rad = np.full(terrain.shape, 1.0)
        for k, a, psi in obj.harmonics:
            rad = rad + a * np.cos(k * phi + psi)
        rad = p["radius_m"] * np.maximum(rad, 0.3)
        fp = np.hypot(u, v) <= rad
        zb[fp] = base
        zt[fp] = base + H
    elif obj.cls == "clutter":
        rho2 = (u / p["radius_m"]) ** 2 + (v / (p["radius_m"] * p["aspect"])) ** 2
        fp = rho2 < 1.0
        zb[fp] = base
        zt[fp] = (base + H * np.sqrt(np.maximum(1.0 - rho2, 0.0)))[fp]
    else:
        raise ValueError(obj.cls)
    return fp, zb, zt


def compose_surface(terrain, footprints, z_top, foliage, foliage_height_m, exclude=None):
    """Z-buffer the visible surface seen by the nadir camera.

    Start from the terrain; for each object k (in order, skipping ``exclude``), pixels in its
    footprint with ``z_top > surface`` become that object's top and ``owner = k``. Finally foliage
    pixels with canopy (terrain + foliage_height) above the surface become foliage (owner -2).
    Returns (surface [m], owner int array).
    """
    surface = terrain.copy()
    owner = np.full(terrain.shape, -1, dtype=np.int32)
    for k, (fp, zt) in enumerate(zip(footprints, z_top)):
        if exclude is not None and k == exclude:
            continue
        up = fp & (np.nan_to_num(zt, nan=-np.inf) > surface)
        surface[up] = zt[up]
        owner[up] = k
    canopy = terrain + foliage_height_m
    fol = foliage & (canopy > surface)
    surface[fol] = canopy[fol]
    owner[fol] = -2
    return surface, owner


def assemble_scene(xi, fixed, terrain, objects, foliage) -> Scene:
    """Compute every object's geometry and the z-buffered surface/owner maps."""
    sc = Scene(xi=xi, fixed=fixed, terrain=terrain, foliage=foliage, objects=list(objects))
    gsd = fixed["gsd_m"]
    for obj in sc.objects:
        fp, zb, zt = object_geometry(obj, terrain, gsd)
        sc.footprints.append(fp)
        sc.z_bottom.append(zb)
        sc.z_top.append(zt)
    sc.surface, sc.owner = compose_surface(terrain, sc.footprints, sc.z_top, foliage,
                                           xi["foliage_height_m"])
    return sc


def generate_scene(xi: dict, fixed: dict, rng: np.random.Generator) -> Scene:
    """terrain -> foliage -> objects -> assemble, all from ``rng`` in that order."""
    terrain = make_terrain(xi, fixed, rng)
    foliage = make_foliage(xi, fixed, rng)
    objects = place_objects(xi, fixed, rng)
    return assemble_scene(xi, fixed, terrain, objects, foliage)


# ----------------------------------------------------------------------------- physics models
def damping_depth(alpha: float) -> float:
    """Diurnal damping depth delta = sqrt(2 alpha / omega) [m]."""
    return math.sqrt(2.0 * alpha / OMEGA)


def soil_temperature(z, t, T_mean=293.0, A0=10.0, alpha=5e-7):
    """T(z, t) = T_mean + A0 exp(-z/delta) cos(omega t - z/delta) for a homogeneous half-space.
    ``t`` [s] is measured from the time of peak surface temperature."""
    delta = damping_depth(alpha)
    z = np.asarray(z, dtype=float)
    return T_mean + A0 * np.exp(-z / delta) * np.cos(OMEGA * np.asarray(t, dtype=float) - z / delta)


def thermal_contrast(t, depth_m, A0, alpha, gain, lag_rad):
    """Heuristic surface temperature contrast [K] above an object whose top is ``depth_m`` below
    the surface (0 = exposed). The object perturbs the diurnal wave locally: its response has
    relative amplitude ``gain`` and extra phase ``lag_rad``; the perturbation seen at the surface
    decays and lags like the diurnal wave itself:

        dT = A0 exp(-d/delta) [gain cos(w t - lag - d/delta) - cos(w t - d/delta)].

    With gain != 1 or lag != 0 the sign changes twice a day (thermal crossover)."""
    delta = damping_depth(alpha)
    d = np.asarray(depth_m, dtype=float)
    ph = OMEGA * np.asarray(t, dtype=float) - d / delta
    return A0 * np.exp(-d / delta) * (gain * np.cos(ph - lag_rad) - np.cos(ph))


def xray_projection(mu_maps, thickness, N0=1e4, rng=None, noise=True):
    """Beer-Lambert projection. ``mu_maps`` (M, H, W) [1/cm], ``thickness`` (M, H, W) [cm].
    Returns ln(N0/N) with N ~ Poisson(N0 exp(-sum mu t)) (counts clipped at 1), or the exact
    line integral if ``noise`` is False."""
    line = (np.asarray(mu_maps) * np.asarray(thickness)).sum(0)
    if not noise:
        return line
    rng = rng if rng is not None else np.random.default_rng(0)
    counts = rng.poisson(N0 * np.exp(-line))
    return np.log(N0 / np.maximum(counts, 1))


def gpr_velocity(eps_r: float) -> float:
    """EM wave speed in soil [m/ns]: c / sqrt(eps_r)."""
    return C_LIGHT / math.sqrt(eps_r)


# ----------------------------------------------------------------------------- renders
def render_depth(scene: Scene, rng=None, noise=True) -> np.ndarray:
    """Nadir depth image [m] = camera_altitude - surface (+ Gaussian noise ``depth_noise_m``)."""
    d = scene.xi["camera_altitude_m"] - scene.surface
    if noise:
        d = d + scene.fixed["depth_noise_m"] * rng.standard_normal(d.shape)
    return d


def surface_normals(surface: np.ndarray, gsd: float) -> np.ndarray:
    """Unit normals (H, W, 3) of the height field via central differences."""
    gy, gx = np.gradient(surface, gsd)
    nrm = np.stack([-gx, -gy, np.ones_like(surface)], axis=-1)
    return nrm / np.linalg.norm(nrm, axis=-1, keepdims=True)


def render_rgb(scene: Scene, rng=None, noise=True) -> np.ndarray:
    """RGB-like image in [0, 1], shape (H, W, 3).

    albedo (soil colour x texture | object albedo | foliage colour) x Lambertian shading
    ``ambient + (1 - ambient) max(0, n . s)`` from the sun direction, then gain, offset and
    Gaussian noise, clipped. The soil texture is a fixed function of the terrain (seeded from
    the scene's own randomness via ``texture_seed`` in xi if present, else 0)."""
    xi, fx = scene.xi, scene.fixed
    n = scene.surface.shape[0]
    tex_rng = np.random.default_rng(int(xi.get("texture_seed", 0)))
    tex = smooth_noise((n, n), xi["texture_corr_px"], tex_rng)
    b, h = xi["soil_brightness"], xi["soil_hue_shift"]
    soil = np.array([b * (1 + h), b, b * (1 - h)])
    albedo = soil[None, None, :] * (1 + xi["texture_amplitude"] * tex)[..., None]
    for k, obj in enumerate(scene.objects):
        m = scene.owner == k
        if m.any():
            albedo[m] = [obj.params["albedo_r"], obj.params["albedo_g"], obj.params["albedo_b"]]
    fol = scene.owner == -2
    if fol.any():
        albedo[fol] = np.asarray(fx["foliage_rgb"])[None, :] * (1 + 0.2 * tex[fol])[:, None]
    el, az = math.radians(xi["sun_elevation_deg"]), math.radians(xi["sun_azimuth_deg"])
    s = np.array([math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)])
    lam = np.clip(surface_normals(scene.surface, fx["gsd_m"]) @ s, 0.0, 1.0)
    shade = xi["ambient"] + (1 - xi["ambient"]) * lam
    img = xi["camera_gain"] * albedo * shade[..., None] + xi["camera_offset"]
    if noise:
        img = img + xi["rgb_noise_sigma"] * rng.standard_normal(img.shape)
    return np.clip(img, 0.0, 1.0)


def capture_time_s(xi: dict, fixed: dict) -> float:
    """Capture time [s] measured from the daily surface-temperature peak."""
    return (xi["hour"] - fixed["thermal_peak_hour"]) * 3600.0


def render_thermal(scene: Scene, rng=None, noise=True) -> np.ndarray:
    """Thermal-like image [K]: soil surface temperature from the diurnal model, plus the
    heuristic object contrast over each footprint (depth = max(0, terrain - z_top)), foliage at
    ``T_mean + 0.5 A0 cos(w t - 0.3)``, plus NETD noise."""
    xi = scene.xi
    t = capture_time_s(xi, scene.fixed)
    A0, alpha = xi["diurnal_amplitude_K"], xi["soil_diffusivity"]
    T = np.full(scene.surface.shape, float(soil_temperature(0.0, t, xi["T_mean_K"], A0, alpha)))
    for k, obj in enumerate(scene.objects):
        fp = scene.footprints[k]
        if not fp.any():
            continue
        d = np.maximum(scene.terrain[fp] - scene.z_top[k][fp], 0.0)
        exposed = scene.owner[fp] == k
        d = np.where(exposed, 0.0, d)
        T[fp] += thermal_contrast(t, d, A0, alpha, obj.params["thermal_gain"],
                                  obj.params["thermal_lag_rad"])
    fol = scene.owner == -2
    T[fol] = xi["T_mean_K"] + 0.5 * A0 * math.cos(OMEGA * t - 0.3)
    if noise:
        T = T + xi["thermal_noise_K"] * rng.standard_normal(T.shape)
    return T


def xray_stack(scene: Scene, energy: str = "low"):
    """Material stack for the top-down density projection: soil + one layer per object.
    Soil path = soil_column + (terrain - min terrain) - buried part of every object; object path
    = z_top - z_bottom. Returns (mu_maps [1/cm], thickness [cm]) of shape (1 + K, H, W)."""
    fx = scene.fixed
    shape = scene.terrain.shape
    mus, ths = [], []
    soil_path = fx["soil_column_m"] + scene.terrain - scene.terrain.min()
    for k, obj in enumerate(scene.objects):
        fp = scene.footprints[k]
        th = np.zeros(shape)
        th[fp] = (scene.z_top[k] - scene.z_bottom[k])[fp]
        buried = np.zeros(shape)
        buried[fp] = np.clip(np.minimum(scene.z_top[k][fp], scene.terrain[fp]) - scene.z_bottom[k][fp], 0, None)
        soil_path = soil_path - buried
        mu = obj.params["mu_low"] * (1.0 if energy == "low" else obj.params["high_low_ratio"])
        mus.append(np.full(shape, mu))
        ths.append(th * 100.0)
    mu_soil = fx["mu_soil_low"] if energy == "low" else fx["mu_soil_high"]
    mus.insert(0, np.full(shape, mu_soil))
    ths.insert(0, np.maximum(soil_path, 0.0) * 100.0)
    return np.stack(mus), np.stack(ths)


def render_xray(scene: Scene, energy="low", rng=None, noise=True) -> np.ndarray:
    """X-ray-like log-attenuation image ln(N0/N) at 'low' or 'high' energy."""
    mu, th = xray_stack(scene, energy)
    return xray_projection(mu, th, scene.xi["xray_N0"], rng, noise)


def gpr_reflectors(scene: Scene):
    """Per object: (x_px, lateral offset dy [m], top depth d [m] >= 0.01, reflectivity).
    d = terrain at the centre pixel - highest point of the object, floored at 0.01 m."""
    out = []
    fx = scene.fixed
    n = scene.terrain.shape[0]
    row = fx["gpr_row"] if fx["gpr_row"] is not None else n // 2
    for k, obj in enumerate(scene.objects):
        ci = int(np.clip(round(obj.cy), 0, n - 1))
        cj = int(np.clip(round(obj.cx), 0, n - 1))
        top = np.nanmax(scene.z_top[k]) if scene.footprints[k].any() else scene.terrain[ci, cj]
        d = max(float(scene.terrain[ci, cj] - top), 0.01)
        out.append((obj.cx, (obj.cy - row) * fx["gsd_m"], d, obj.params["reflectivity"]))
    return out


def gpr_apex_time_ns(dy_m: float, d_m: float, eps_r: float, antenna_height_m: float) -> float:
    """Two-way travel time at the hyperbola apex: 2 h/c + 2 sqrt(dy^2 + d^2) / v."""
    return 2 * antenna_height_m / C_LIGHT + 2 * math.hypot(dy_m, d_m) / gpr_velocity(eps_r)


def render_gpr(scene: Scene, rng=None, noise=True) -> np.ndarray:
    """GPR-like B-scan (n_t, W) along row ``gpr_row``: surface reflection (-1 x wavelet at
    2h/c) plus, per object, a Ricker wavelet at t(x) = 2h/c + 2 sqrt((x-x0)^2 + dy^2 + d^2)/v with
    amplitude refl * exp(-2 a r) * 0.1 / max(r, 0.1); plus Gaussian noise ``gpr_noise``."""
    xi, fx = scene.xi, scene.fixed
    n = scene.terrain.shape[0]
    nt = int(fx["gpr_n_t"])
    t = np.linspace(0.0, fx["gpr_window_ns"], nt)[:, None]
    x_m = np.arange(n)[None, :] * fx["gsd_m"]
    f = fx["gpr_freq_ghz"]
    v = gpr_velocity(xi["gpr_eps_r"])
    t_air = 2 * fx["gpr_antenna_height_m"] / C_LIGHT
    b = -ricker(t - t_air, f) * np.ones((1, n))
    for x0, dy, d, refl in gpr_reflectors(scene):
        r = np.sqrt((x_m - x0 * fx["gsd_m"]) ** 2 + dy ** 2 + d ** 2)
        amp = refl * np.exp(-2 * fx["gpr_attenuation_np_per_m"] * r) * 0.1 / np.maximum(r, 0.1)
        b = b + amp * ricker(t - (t_air + 2 * r / v), f)
    if noise:
        b = b + xi["gpr_noise"] * rng.standard_normal(b.shape)
    return b


def render_all(scene: Scene, rng=None, noise=True) -> dict:
    """All modalities: rgb, thermal, depth, xray_low, xray_high, gpr (fixed order of rng use)."""
    return {
        "rgb": render_rgb(scene, rng, noise),
        "thermal": render_thermal(scene, rng, noise),
        "depth": render_depth(scene, rng, noise),
        "xray_low": render_xray(scene, "low", rng, noise),
        "xray_high": render_xray(scene, "high", rng, noise),
        "gpr": render_gpr(scene, rng, noise),
    }


# ----------------------------------------------------------------------------- labels
def make_labels(scene: Scene) -> list[dict]:
    """One label dict per object:

    id, class_name, class_id, mask (visible pixels, owner == k), amodal_mask (footprint), box /
    amodal_box (inclusive x0, y0, x1, y1 or None), visible_area, footprint_area, visibility
    (= visible/footprint), visible (mask area > 0), positive (visibility >= visibility_threshold,
    the labelling policy), burial_fraction, top_depth_m (>= 0, 0 if any part protrudes),
    gpr_apex (x_px, t_ns)."""
    fx, xi = scene.fixed, scene.xi
    labels = []
    refl = gpr_reflectors(scene)
    for k, obj in enumerate(scene.objects):
        mask = scene.owner == k
        fp = scene.footprints[k]
        va, fa = int(mask.sum()), int(fp.sum())
        vis = va / fa if fa else 0.0
        # top depth = shallowest point below ground; 0 if the object protrudes anywhere
        top_depth = 0.0
        if fa:
            gap = scene.terrain[fp] - scene.z_top[k][fp]
            top_depth = float(max(gap.min(), 0.0))
        x0, dy, d, _ = refl[k]
        labels.append({
            "id": k,
            "class_name": obj.cls,
            "class_id": CLASS_ID[obj.cls],
            "mask": mask,
            "amodal_mask": fp,
            "box": bbox_of(mask),
            "amodal_box": bbox_of(fp),
            "visible_area": va,
            "footprint_area": fa,
            "visibility": vis,
            "visible": va > 0,
            "positive": bool(vis >= fx["visibility_threshold"] and va > 0),
            "burial_fraction": obj.burial_fraction,
            "top_depth_m": top_depth,
            "gpr_apex": (obj.cx, gpr_apex_time_ns(dy, d, xi["gpr_eps_r"], fx["gpr_antenna_height_m"])),
        })
    return labels


# ----------------------------------------------------------------------------- dataset
def generate_sample(seed_seq: np.random.SeedSequence, spec=None, fixed=None, noise=True) -> dict:
    """One sample from a SeedSequence: three child streams for (xi, layout, render noise), so
    changing render noise never moves objects. Returns {xi, objects, renders, labels, scene}."""
    spec = DEFAULT_SPEC if spec is None else spec
    fixed = DEFAULT_FIXED if fixed is None else fixed
    s_xi, s_layout, s_render = seed_seq.spawn(3)
    xi = sample_parameters(spec, np.random.default_rng(s_xi))
    xi["texture_seed"] = int(s_layout.generate_state(1)[0])
    scene = generate_scene(xi, fixed, np.random.default_rng(s_layout))
    renders = render_all(scene, np.random.default_rng(s_render), noise)
    return {"xi": xi, "objects": [{"cls": o.cls, "cx": o.cx, "cy": o.cy, "params": o.params,
                                   "burial_fraction": o.burial_fraction,
                                   "cover_depth_m": o.cover_depth_m} for o in scene.objects],
            "renders": renders, "labels": make_labels(scene), "scene": scene}


def generate_dataset(n: int, seed: int, spec=None, fixed=None, noise=True) -> list[dict]:
    """``n`` samples from independent child seeds of ``np.random.SeedSequence(seed)``."""
    return [generate_sample(s, spec, fixed, noise) for s in np.random.SeedSequence(seed).spawn(n)]


def dataset_statistics(samples: list[dict]) -> dict:
    """Counts per class, visible / positive counts, and empirical min/max of every xi key."""
    counts = {c: 0 for c in CLASSES}
    vis = {c: 0 for c in CLASSES}
    pos = {c: 0 for c in CLASSES}
    for s in samples:
        for lab in s["labels"]:
            counts[lab["class_name"]] += 1
            vis[lab["class_name"]] += int(lab["visible"])
            pos[lab["class_name"]] += int(lab["positive"])
    keys = sorted({k for s in samples for k in s["xi"]})
    emp = {}
    for k in keys:
        vals = [s["xi"][k] for s in samples if k in s["xi"] and isinstance(s["xi"][k], (int, float))]
        if vals:
            emp[k] = {"min": float(min(vals)), "max": float(max(vals))}
    return {"n_samples": len(samples), "objects": counts, "visible": vis, "positive": pos,
            "empirical_ranges": emp}


def build_dataset_card(samples, spec=None, fixed=None, name="synthetic-eod-scenes", seed=None) -> dict:
    """Dataset card (dict, JSON-serialisable) with the sections of lesson 09.3 section 7:
    provenance, parameter_distribution (every spec key), fixed_factors (every fixed key),
    object_families, labelling_policy, physics_models, intended_use, known_gaps, splits,
    validation_evidence, safety_review, statistics."""
    spec = DEFAULT_SPEC if spec is None else spec
    fixed = DEFAULT_FIXED if fixed is None else fixed
    stats = dataset_statistics(samples)
    return {
        "name": name,
        "provenance": {"generator": GENERATOR_VERSION, "seed": seed, "n_samples": len(samples),
                       "assets": "procedural only (no external assets)", "licence": "course material"},
        "parameter_distribution": {k: dict(v) for k, v in spec.items()},
        "fixed_factors": {k: (list(v) if isinstance(v, tuple) else v) for k, v in fixed.items()},
        "object_families": {c: {k: list(r) for k, r in fam.items()} for c, fam in OBJECT_FAMILIES.items()},
        "labelling_policy": {
            "positive": f"visible fraction of footprint >= {fixed['visibility_threshold']} (nadir view)",
            "visible": "at least one pixel of the object is the top-most surface",
            "mask": "visible pixels (modal); amodal_mask = full footprint",
            "box": "inclusive pixel bbox (x0, y0, x1, y1) of the modal mask; None if not visible",
            "frames": "image rows = y, columns = x; heights in metres, up positive",
        },
        "physics_models": {
            "thermal": "physics-based diurnal half-space solution for soil; object contrast is heuristic",
            "xray": "Beer-Lambert line integral with Poisson counts (top-down density projection)",
            "depth": "exact orthographic nadir z-buffer + Gaussian noise",
            "gpr": "geometric hyperbolas with Ricker wavelet; no full-wave effects",
            "rgb": "Lambertian shading, no cast shadows, no specularity",
        },
        "intended_use": "pretraining / augmentation / pipeline testing; NOT for final evaluation",
        "known_gaps": ["no cast shadows or specular materials", "no multipath or layered soil in GPR",
                       "thermal object model is heuristic", "no motion blur or lens distortion",
                       "only four fictional object families"],
        "splits": "split by seed; no shared assets exist (all geometry is procedural)",
        "validation_evidence": "none yet -- must be validated on held-out real data (TSTR) before use",
        "safety_review": "only fictional generic geometric objects and detection physics are modelled",
        "statistics": stats,
    }


def card_to_markdown(card: dict) -> str:
    """Render the card as Markdown: a parameter table (name, dist, range, unit, doc), a fixed
    factors table and the text sections."""
    L = [f"# Dataset card: {card['name']}", ""]
    L += ["## Provenance", ""] + [f"- **{k}**: {v}" for k, v in card["provenance"].items()] + [""]
    L += ["## Parameter distribution", "", "| Factor | Distribution | Range / values | Unit | Meaning |",
          "|---|---|---|---|---|"]
    for k, d in card["parameter_distribution"].items():
        rng_ = d.get("values", d.get("value", f"[{d.get('low')}, {d.get('high')}]"))
        L.append(f"| `{k}` | {d['dist']} | {rng_} | {d.get('unit', '')} | {d.get('doc', '')} |")
    L += ["", "## Fixed factors", "", "| Factor | Value |", "|---|---|"]
    L += [f"| `{k}` | {v} |" for k, v in card["fixed_factors"].items()]
    L += ["", "## Object families (fictional)", ""]
    for c, fam in card["object_families"].items():
        L.append(f"- **{c}**: " + ", ".join(f"`{k}` in {v}" for k, v in fam.items()))
    L += ["", "## Labelling policy", ""] + [f"- **{k}**: {v}" for k, v in card["labelling_policy"].items()]
    L += ["", "## Physics models", ""] + [f"- **{k}**: {v}" for k, v in card["physics_models"].items()]
    L += ["", "## Intended use", "", card["intended_use"], "", "## Known gaps", ""]
    L += [f"- {g}" for g in card["known_gaps"]]
    L += ["", "## Splits", "", card["splits"], "", "## Validation evidence", "", card["validation_evidence"],
          "", "## Safety review", "", card["safety_review"], "", "## Statistics", "",
          "```json", json.dumps(card["statistics"], indent=2), "```", ""]
    return "\n".join(L)


def write_dataset_card(card: dict, out_dir) -> tuple[Path, Path]:
    """Write ``dataset_card.json`` and ``dataset_card.md`` into ``out_dir``; return both paths."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pj, pm = out / "dataset_card.json", out / "dataset_card.md"
    pj.write_text(json.dumps(card, indent=2, default=str), encoding="utf-8")
    pm.write_text(card_to_markdown(card), encoding="utf-8")
    return pj, pm


if __name__ == "__main__":  # pragma: no cover
    import time
    t0 = time.perf_counter()
    data = generate_dataset(100, seed=0)
    dt = time.perf_counter() - t0
    print(f"100 scenes in {dt:.2f} s ({100 / dt:.0f} scenes/s)")
    print(json.dumps(dataset_statistics(data)["objects"]))
