"""scenegen -- procedural synthetic EOD-style scenes with multi-sensor renders (Project P10).

STARTER -- implement every function that raises NotImplementedError
(the helpers that are already implemented are not the learning goal). Only FICTIONAL, generic geometric objects are modelled (boxes, lying
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
CLASSES = ('container', 'cylinder', 'debris', 'clutter')
CLASS_ID = {c: i for i, c in enumerate(CLASSES)}
ITEM_CLASSES = ('container', 'cylinder', 'debris')
OMEGA = 2.0 * np.pi / 86400.0
C_LIGHT = 0.299792458
GENERATOR_VERSION = 'scenegen-1.0'
DEFAULT_SPEC: dict[str, dict] = {'n_objects': {'dist': 'int', 'low': 1, 'high': 5, 'unit': '-', 'doc': 'number of fictional items of interest (container/cylinder/debris)'}, 'n_clutter': {'dist': 'int', 'low': 0, 'high': 12, 'unit': '-', 'doc': 'number of rocks/clutter (distractors)'}, 'terrain_amplitude_m': {'dist': 'uniform', 'low': 0.0, 'high': 0.04, 'unit': 'm', 'doc': 'std of terrain height-field undulation'}, 'terrain_corr_px': {'dist': 'uniform', 'low': 6.0, 'high': 30.0, 'unit': 'px', 'doc': 'correlation length of terrain undulation'}, 'soil_brightness': {'dist': 'uniform', 'low': 0.25, 'high': 0.6, 'unit': '-', 'doc': 'mean soil albedo'}, 'soil_hue_shift': {'dist': 'uniform', 'low': -0.1, 'high': 0.1, 'unit': '-', 'doc': 'red-blue tint of soil albedo'}, 'texture_amplitude': {'dist': 'uniform', 'low': 0.0, 'high': 0.15, 'unit': '-', 'doc': 'relative amplitude of soil texture'}, 'texture_corr_px': {'dist': 'uniform', 'low': 1.0, 'high': 6.0, 'unit': 'px', 'doc': 'correlation length of soil texture'}, 'sun_elevation_deg': {'dist': 'uniform', 'low': 15.0, 'high': 80.0, 'unit': 'deg', 'doc': 'sun elevation for RGB shading'}, 'sun_azimuth_deg': {'dist': 'uniform', 'low': 0.0, 'high': 360.0, 'unit': 'deg', 'doc': 'sun azimuth for RGB shading'}, 'ambient': {'dist': 'uniform', 'low': 0.1, 'high': 0.4, 'unit': '-', 'doc': 'ambient (sky) fraction of illumination'}, 'camera_gain': {'dist': 'uniform', 'low': 0.7, 'high': 1.3, 'unit': '-', 'doc': 'RGB sensor gain'}, 'camera_offset': {'dist': 'uniform', 'low': -0.05, 'high': 0.05, 'unit': '-', 'doc': 'RGB sensor offset'}, 'rgb_noise_sigma': {'dist': 'uniform', 'low': 0.0, 'high': 0.03, 'unit': '-', 'doc': 'RGB additive Gaussian noise std'}, 'foliage_cover': {'dist': 'uniform', 'low': 0.0, 'high': 0.3, 'unit': '-', 'doc': 'fraction of scene covered by occluding foliage'}, 'foliage_height_m': {'dist': 'uniform', 'low': 0.15, 'high': 0.4, 'unit': 'm', 'doc': 'canopy height of foliage above terrain'}, 'burial_max': {'dist': 'uniform', 'low': 0.0, 'high': 1.0, 'unit': '-', 'doc': 'per-object burial fraction ~ U(0, burial_max)'}, 'p_fully_buried': {'dist': 'uniform', 'low': 0.0, 'high': 0.4, 'unit': '-', 'doc': 'probability an item is fully buried (burial fraction 1 + cover)'}, 'hour': {'dist': 'uniform', 'low': 0.0, 'high': 24.0, 'unit': 'h', 'doc': 'local solar time of capture (drives the diurnal thermal model)'}, 'T_mean_K': {'dist': 'uniform', 'low': 280.0, 'high': 305.0, 'unit': 'K', 'doc': 'daily mean soil temperature'}, 'diurnal_amplitude_K': {'dist': 'uniform', 'low': 3.0, 'high': 15.0, 'unit': 'K', 'doc': 'surface diurnal temperature amplitude A0'}, 'soil_diffusivity': {'dist': 'loguniform', 'low': 2e-07, 'high': 1e-06, 'unit': 'm^2/s', 'doc': 'soil thermal diffusivity alpha'}, 'thermal_noise_K': {'dist': 'uniform', 'low': 0.02, 'high': 0.2, 'unit': 'K', 'doc': 'thermal sensor noise (NETD)'}, 'xray_N0': {'dist': 'loguniform', 'low': 1000.0, 'high': 100000.0, 'unit': 'counts', 'doc': 'incident photon count per pixel (dose)'}, 'gpr_eps_r': {'dist': 'uniform', 'low': 3.0, 'high': 25.0, 'unit': '-', 'doc': 'soil relative permittivity (sets GPR velocity)'}, 'gpr_noise': {'dist': 'uniform', 'low': 0.0, 'high': 0.05, 'unit': '-', 'doc': 'GPR additive noise std (relative to unit wavelet)'}, 'camera_altitude_m': {'dist': 'uniform', 'low': 1.5, 'high': 3.0, 'unit': 'm', 'doc': 'nadir camera altitude above z = 0'}}
DEFAULT_FIXED: dict[str, object] = {'image_size': 128, 'gsd_m': 0.02, 'soil_column_m': 0.2, 'mu_soil_low': 0.05, 'mu_soil_high': 0.035, 'visibility_threshold': 0.25, 'depth_noise_m': 0.003, 'thermal_peak_hour': 14.0, 'gpr_row': None, 'gpr_n_t': 128, 'gpr_window_ns': 20.0, 'gpr_freq_ghz': 1.5, 'gpr_antenna_height_m': 0.05, 'gpr_attenuation_np_per_m': 2.0, 'foliage_rgb': (0.15, 0.35, 0.1)}
_COMMON = {'albedo_r': (0.1, 0.9), 'albedo_g': (0.1, 0.9), 'albedo_b': (0.1, 0.9), 'thermal_gain': (0.5, 1.6), 'thermal_lag_rad': (-0.8, 0.8), 'mu_low': (0.04, 0.3), 'high_low_ratio': (0.5, 0.9), 'reflectivity': (0.3, 1.0), 'angle_rad': (0.0, math.pi)}
OBJECT_FAMILIES: dict[str, dict[str, tuple[float, float]]] = {'container': {**_COMMON, 'length_m': (0.25, 0.6), 'width_m': (0.15, 0.35), 'height_m': (0.08, 0.25)}, 'cylinder': {**_COMMON, 'length_m': (0.2, 0.6), 'diameter_m': (0.06, 0.2)}, 'debris': {**_COMMON, 'radius_m': (0.05, 0.2), 'height_m': (0.01, 0.05), 'roughness': (0.05, 0.35)}, 'clutter': {**_COMMON, 'radius_m': (0.02, 0.08), 'height_m': (0.02, 0.08), 'aspect': (0.5, 1.0)}}
COVER_DEPTH_RANGE_M = (0.01, 0.15)


@dataclass
class SceneObject:
    """One fictional object. ``cx, cy`` in pixels; ``params`` sampled from OBJECT_FAMILIES."""
    cls: str
    cx: float
    cy: float
    params: dict
    burial_fraction: float = 0.0
    cover_depth_m: float = 0.0
    harmonics: tuple = ()


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
    return (yy.astype(float), xx.astype(float))


def bbox_of(mask: np.ndarray):
    """Inclusive (x0, y0, x1, y1) bounding box of a boolean mask, or None if empty."""
    if not mask.any():
        return None
    ys, xs = np.nonzero(mask)
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def sample_parameters(spec: dict, rng: np.random.Generator) -> dict:
    """Draw one scene-level parameter vector xi from ``spec``.

    Supported distributions: ``uniform`` (low, high), ``loguniform`` (low, high > 0),
    ``int`` (inclusive low..high), ``choice`` (``values`` list), ``fixed`` (``value``).
    Keys are sampled in sorted order so the result does not depend on dict insertion order.
    """
    raise NotImplementedError('TODO: implement sample_parameters')


def check_parameters(xi: dict, spec: dict) -> list[str]:
    """Return a list of human-readable violations (empty if ``xi`` lies in ``spec``'s support)."""
    raise NotImplementedError('TODO: implement check_parameters')


def sample_object_params(cls: str, rng: np.random.Generator) -> dict:
    """Sample the per-object parameters of family ``cls`` uniformly from OBJECT_FAMILIES."""
    raise NotImplementedError('TODO: implement sample_object_params')


def make_terrain(xi: dict, fixed: dict, rng: np.random.Generator) -> np.ndarray:
    """Height field [m], shape (N, N): ``terrain_amplitude_m`` x smooth_noise(corr)."""
    raise NotImplementedError('TODO: implement make_terrain')


def make_foliage(xi: dict, fixed: dict, rng: np.random.Generator) -> np.ndarray:
    """Boolean occluder mask covering approximately ``foliage_cover`` of the image
    (thresholded smooth noise with correlation length 6 px)."""
    raise NotImplementedError('TODO: implement make_foliage')


def place_objects(xi: dict, fixed: dict, rng: np.random.Generator) -> list[SceneObject]:
    """Sample ``n_objects`` items (classes drawn uniformly from ITEM_CLASSES) and ``n_clutter``
    rocks at uniform positions (8 px margin), each with per-object params, burial fraction
    ~ U(0, burial_max) and, for items, full burial with probability ``p_fully_buried`` (then
    burial_fraction = 1 and cover_depth ~ U(COVER_DEPTH_RANGE_M)). Clutter is never fully buried."""
    raise NotImplementedError('TODO: implement place_objects')


def object_height(obj: SceneObject) -> float:
    """Maximum vertical extent of the object [m]."""
    p = obj.params
    return p['diameter_m'] if obj.cls == 'cylinder' else p['height_m']


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
    raise NotImplementedError('TODO: implement object_geometry')


def compose_surface(terrain, footprints, z_top, foliage, foliage_height_m, exclude=None):
    """Z-buffer the visible surface seen by the nadir camera.

    Start from the terrain; for each object k (in order, skipping ``exclude``), pixels in its
    footprint with ``z_top > surface`` become that object's top and ``owner = k``. Finally foliage
    pixels with canopy (terrain + foliage_height) above the surface become foliage (owner -2).
    Returns (surface [m], owner int array).
    """
    raise NotImplementedError('TODO: implement compose_surface')


def assemble_scene(xi, fixed, terrain, objects, foliage) -> Scene:
    """Compute every object's geometry and the z-buffered surface/owner maps."""
    raise NotImplementedError('TODO: implement assemble_scene')


def generate_scene(xi: dict, fixed: dict, rng: np.random.Generator) -> Scene:
    """terrain -> foliage -> objects -> assemble, all from ``rng`` in that order."""
    raise NotImplementedError('TODO: implement generate_scene')


def damping_depth(alpha: float) -> float:
    """Diurnal damping depth delta = sqrt(2 alpha / omega) [m]."""
    raise NotImplementedError('TODO: implement damping_depth')


def soil_temperature(z, t, T_mean=293.0, A0=10.0, alpha=5e-07):
    """T(z, t) = T_mean + A0 exp(-z/delta) cos(omega t - z/delta) for a homogeneous half-space.
    ``t`` [s] is measured from the time of peak surface temperature."""
    raise NotImplementedError('TODO: implement soil_temperature')


def thermal_contrast(t, depth_m, A0, alpha, gain, lag_rad):
    """Heuristic surface temperature contrast [K] above an object whose top is ``depth_m`` below
    the surface (0 = exposed). The object perturbs the diurnal wave locally: its response has
    relative amplitude ``gain`` and extra phase ``lag_rad``; the perturbation seen at the surface
    decays and lags like the diurnal wave itself:

        dT = A0 exp(-d/delta) [gain cos(w t - lag - d/delta) - cos(w t - d/delta)].

    With gain != 1 or lag != 0 the sign changes twice a day (thermal crossover)."""
    raise NotImplementedError('TODO: implement thermal_contrast')


def xray_projection(mu_maps, thickness, N0=10000.0, rng=None, noise=True):
    """Beer-Lambert projection. ``mu_maps`` (M, H, W) [1/cm], ``thickness`` (M, H, W) [cm].
    Returns ln(N0/N) with N ~ Poisson(N0 exp(-sum mu t)) (counts clipped at 1), or the exact
    line integral if ``noise`` is False."""
    raise NotImplementedError('TODO: implement xray_projection')


def gpr_velocity(eps_r: float) -> float:
    """EM wave speed in soil [m/ns]: c / sqrt(eps_r)."""
    return C_LIGHT / math.sqrt(eps_r)


def render_depth(scene: Scene, rng=None, noise=True) -> np.ndarray:
    """Nadir depth image [m] = camera_altitude - surface (+ Gaussian noise ``depth_noise_m``)."""
    raise NotImplementedError('TODO: implement render_depth')


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
    raise NotImplementedError('TODO: implement render_rgb')


def capture_time_s(xi: dict, fixed: dict) -> float:
    """Capture time [s] measured from the daily surface-temperature peak."""
    return (xi['hour'] - fixed['thermal_peak_hour']) * 3600.0


def render_thermal(scene: Scene, rng=None, noise=True) -> np.ndarray:
    """Thermal-like image [K]: soil surface temperature from the diurnal model, plus the
    heuristic object contrast over each footprint (depth = max(0, terrain - z_top)), foliage at
    ``T_mean + 0.5 A0 cos(w t - 0.3)``, plus NETD noise."""
    raise NotImplementedError('TODO: implement render_thermal')


def xray_stack(scene: Scene, energy: str='low'):
    """Material stack for the top-down density projection: soil + one layer per object.
    Soil path = soil_column + (terrain - min terrain) - buried part of every object; object path
    = z_top - z_bottom. Returns (mu_maps [1/cm], thickness [cm]) of shape (1 + K, H, W)."""
    raise NotImplementedError('TODO: implement xray_stack')


def render_xray(scene: Scene, energy='low', rng=None, noise=True) -> np.ndarray:
    """X-ray-like log-attenuation image ln(N0/N) at 'low' or 'high' energy."""
    raise NotImplementedError('TODO: implement render_xray')


def gpr_reflectors(scene: Scene):
    """Per object: (x_px, lateral offset dy [m], top depth d [m] >= 0.01, reflectivity).
    d = terrain at the centre pixel - highest point of the object, floored at 0.01 m."""
    raise NotImplementedError('TODO: implement gpr_reflectors')


def gpr_apex_time_ns(dy_m: float, d_m: float, eps_r: float, antenna_height_m: float) -> float:
    """Two-way travel time at the hyperbola apex: 2 h/c + 2 sqrt(dy^2 + d^2) / v."""
    raise NotImplementedError('TODO: implement gpr_apex_time_ns')


def render_gpr(scene: Scene, rng=None, noise=True) -> np.ndarray:
    """GPR-like B-scan (n_t, W) along row ``gpr_row``: surface reflection (-1 x wavelet at
    2h/c) plus, per object, a Ricker wavelet at t(x) = 2h/c + 2 sqrt((x-x0)^2 + dy^2 + d^2)/v with
    amplitude refl * exp(-2 a r) * 0.1 / max(r, 0.1); plus Gaussian noise ``gpr_noise``."""
    raise NotImplementedError('TODO: implement render_gpr')


def render_all(scene: Scene, rng=None, noise=True) -> dict:
    """All modalities: rgb, thermal, depth, xray_low, xray_high, gpr (fixed order of rng use)."""
    raise NotImplementedError('TODO: implement render_all')


def make_labels(scene: Scene) -> list[dict]:
    """One label dict per object:

    id, class_name, class_id, mask (visible pixels, owner == k), amodal_mask (footprint), box /
    amodal_box (inclusive x0, y0, x1, y1 or None), visible_area, footprint_area, visibility
    (= visible/footprint), visible (mask area > 0), positive (visibility >= visibility_threshold,
    the labelling policy), burial_fraction, top_depth_m (>= 0, 0 if any part protrudes),
    gpr_apex (x_px, t_ns)."""
    raise NotImplementedError('TODO: implement make_labels')


def generate_sample(seed_seq: np.random.SeedSequence, spec=None, fixed=None, noise=True) -> dict:
    """One sample from a SeedSequence: three child streams for (xi, layout, render noise), so
    changing render noise never moves objects. Returns {xi, objects, renders, labels, scene}."""
    raise NotImplementedError('TODO: implement generate_sample')


def generate_dataset(n: int, seed: int, spec=None, fixed=None, noise=True) -> list[dict]:
    """``n`` samples from independent child seeds of ``np.random.SeedSequence(seed)``."""
    return [generate_sample(s, spec, fixed, noise) for s in np.random.SeedSequence(seed).spawn(n)]


def dataset_statistics(samples: list[dict]) -> dict:
    """Counts per class, visible / positive counts, and empirical min/max of every xi key."""
    raise NotImplementedError('TODO: implement dataset_statistics')


def build_dataset_card(samples, spec=None, fixed=None, name='synthetic-eod-scenes', seed=None) -> dict:
    """Dataset card (dict, JSON-serialisable) with the sections of lesson 09.3 section 7:
    provenance, parameter_distribution (every spec key), fixed_factors (every fixed key),
    object_families, labelling_policy, physics_models, intended_use, known_gaps, splits,
    validation_evidence, safety_review, statistics."""
    raise NotImplementedError('TODO: implement build_dataset_card')


def card_to_markdown(card: dict) -> str:
    """Render the card as Markdown: a parameter table (name, dist, range, unit, doc), a fixed
    factors table and the text sections."""
    L = [f"# Dataset card: {card['name']}", '']
    L += ['## Provenance', ''] + [f'- **{k}**: {v}' for k, v in card['provenance'].items()] + ['']
    L += ['## Parameter distribution', '', '| Factor | Distribution | Range / values | Unit | Meaning |', '|---|---|---|---|---|']
    for k, d in card['parameter_distribution'].items():
        rng_ = d.get('values', d.get('value', f"[{d.get('low')}, {d.get('high')}]"))
        L.append(f"| `{k}` | {d['dist']} | {rng_} | {d.get('unit', '')} | {d.get('doc', '')} |")
    L += ['', '## Fixed factors', '', '| Factor | Value |', '|---|---|']
    L += [f'| `{k}` | {v} |' for k, v in card['fixed_factors'].items()]
    L += ['', '## Object families (fictional)', '']
    for c, fam in card['object_families'].items():
        L.append(f'- **{c}**: ' + ', '.join((f'`{k}` in {v}' for k, v in fam.items())))
    L += ['', '## Labelling policy', ''] + [f'- **{k}**: {v}' for k, v in card['labelling_policy'].items()]
    L += ['', '## Physics models', ''] + [f'- **{k}**: {v}' for k, v in card['physics_models'].items()]
    L += ['', '## Intended use', '', card['intended_use'], '', '## Known gaps', '']
    L += [f'- {g}' for g in card['known_gaps']]
    L += ['', '## Splits', '', card['splits'], '', '## Validation evidence', '', card['validation_evidence'], '', '## Safety review', '', card['safety_review'], '', '## Statistics', '', '```json', json.dumps(card['statistics'], indent=2), '```', '']
    return '\n'.join(L)


def write_dataset_card(card: dict, out_dir) -> tuple[Path, Path]:
    """Write ``dataset_card.json`` and ``dataset_card.md`` into ``out_dir``; return both paths."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pj, pm = (out / 'dataset_card.json', out / 'dataset_card.md')
    pj.write_text(json.dumps(card, indent=2, default=str), encoding='utf-8')
    pm.write_text(card_to_markdown(card), encoding='utf-8')
    return (pj, pm)
