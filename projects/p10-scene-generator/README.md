# P10 · Synthetic EOD scene generator

<div class="module-card">

**Lessons** [09.3 Synthetic data & sim-to-real](lessons/stage-09/lesson-03.md) (core) · [08.2 Reconstruction as an inverse problem](lessons/stage-08/lesson-02.md) (scene generation for inversion) · [05.3 Penetrating radiation](lessons/stage-05/lesson-03.md) (Beer–Lambert, dual energy) · [05.5 Imaging & remote sensing](lessons/stage-05/lesson-05.md) (thermal crossover) · [09.1 Perception tasks](lessons/stage-09/lesson-01.md) (GPR hyperbolas, labels, metrics)

**Simulators** [Sim H — recognition trainer](sims/recognition-trainer/index.html) (a generator under test) · [Sim A — scene assessment](sims/scene-assessment/index.html)

**Module** `scenegen` · **Level** Advanced · **Time** 10–14 h · **Next** [P11 Teleoperation](projects/p11-teleoperation/README.md), feeds [P09 CV detection](projects/p09-cv-detection/README.md)

</div>

<div class="callout boundary">

**Fictional objects only.** The generator models four generic geometric families — rectangular
*containers*, lying *cylinders*, flat irregular *debris* plates and *clutter* rocks — with invented
material constants. It encodes no real ordnance or device geometry, no components, and nothing
about how any object functions. What it teaches is the *data* side: randomisation design,
physics-based sensor rendering, label policy and honest documentation.

</div>

## Goal

Build a procedural generator of 2.5D scenes (height-field terrain + fictional objects + foliage
occluders) that renders five co-registered sensor modalities with exact labels, logs the full
parameter vector $\xi$ per sample, and writes a dataset card. The point is not photorealism: it is
an explicit, sampleable $p(\text{scene})$ whose every factor is declared, bounded and reported.

## Background

- **Domain randomisation** (09.3 §3): train over $\xi\sim P_{\text{rand}}(\xi)$ wide enough that
  the real world is one more sample. Your spec must declare *every* factor with its distribution;
  fixed factors are listed explicitly (they are the gaps DR cannot cover).
- **Diurnal thermal model** (09.3 §4.1): $T(z,t)=\bar T + A_0 e^{-z/\delta}\cos(\omega t - z/\delta)$,
  $\delta=\sqrt{2\alpha/\omega}$. Objects perturb the wave; the surface contrast changes sign twice a
  day (thermal crossover).
- **X-ray-like projection** (09.3 §4.2, 05.3): $\ln(N_0/N)$ with $N\sim\mathrm{Poisson}(N_0 e^{-\sum\mu_i t_i})$;
  dual-energy log ratio is thickness-independent for one material.
- **GPR B-scan** (09.3 §4.3, 09.1): $t(x)=2h/c + \tfrac{2}{v}\sqrt{(x-x_0)^2+\Delta y^2+d^2}$,
  $v=c/\sqrt{\varepsilon_r}$ — randomise $\varepsilon_r$, never width and apex time separately.
- **Label policy and dataset cards** (09.3 §7–8): a label is a *policy* (what counts as positive),
  not a fact; the card states it.

## Requirements

1. **Parameter sampling.** `sample_parameters(spec, rng)` supports `uniform`, `loguniform`, `int`
   (inclusive), `choice`, `fixed`; sample keys in sorted order. `check_parameters(xi, spec)` returns
   all violations. Per-object parameters come from `OBJECT_FAMILIES` (uniform ranges).
2. **Scene layout.** Terrain height field (`make_terrain`), foliage mask (`make_foliage`), object
   placement with burial fraction $\sim U(0,\text{burial\_max})$ and full burial (+ cover depth)
   with probability `p_fully_buried` for items (`place_objects`), per-object geometry
   (`object_geometry`: footprint, per-pixel bottom/top height), and a z-buffer
   (`compose_surface`) that yields the visible surface and an `owner` map
   (−1 terrain, −2 foliage, $k$ object).
3. **Renders** (`render_all`): RGB-like (albedo × Lambertian shading, gain, offset, noise), thermal-like
   (diurnal model + object contrast + NETD), depth (nadir orthographic: altitude − surface),
   X-ray-like low/high energy (soil + object layers, Poisson counts), GPR-like B-scan (Ricker
   wavelet hyperbolas, surface reflection, noise). Every render takes `noise=False` for exact checks.
4. **Labels** (`make_labels`): modal mask (visible pixels), amodal mask (footprint), boxes,
   visibility fraction, `visible` (mask area > 0), `positive` (visibility ≥ `visibility_threshold`),
   burial fraction, top depth, GPR apex $(x_0, t_0)$.
5. **Dataset.** `generate_sample(SeedSequence)` uses three child streams (ξ, layout, render noise) so
   re-rendering never moves objects; `generate_dataset(n, seed)`.
6. **Dataset card.** `build_dataset_card` (JSON-serialisable dict with provenance, parameter
   distribution, fixed factors, object families, labelling policy, physics models, intended use,
   known gaps, splits, validation evidence, safety review, statistics) and `card_to_markdown` /
   `write_dataset_card`.

## API

```python
DEFAULT_SPEC: dict; DEFAULT_FIXED: dict; OBJECT_FAMILIES: dict; CLASSES = ("container", "cylinder", "debris", "clutter")

@dataclass class SceneObject: cls, cx, cy, params, burial_fraction=0.0, cover_depth_m=0.0, harmonics=()
@dataclass class Scene: xi, fixed, terrain, foliage, objects, footprints, z_bottom, z_top, surface, owner

sample_parameters(spec, rng) -> dict                 check_parameters(xi, spec) -> list[str]
sample_object_params(cls, rng) -> dict
make_terrain(xi, fixed, rng) -> (N, N) [m]           make_foliage(xi, fixed, rng) -> bool (N, N)
place_objects(xi, fixed, rng) -> list[SceneObject]   object_geometry(obj, terrain, gsd) -> (fp, z_bot, z_top)
compose_surface(terrain, footprints, z_top, foliage, foliage_height_m, exclude=None) -> (surface, owner)
assemble_scene(xi, fixed, terrain, objects, foliage) -> Scene
generate_scene(xi, fixed, rng) -> Scene
damping_depth(alpha) -> m                            soil_temperature(z, t, T_mean, A0, alpha) -> K
thermal_contrast(t, depth_m, A0, alpha, gain, lag_rad) -> K
xray_projection(mu_maps, thickness, N0, rng, noise=True) -> ln(N0/N)
render_rgb / render_thermal / render_depth / render_gpr(scene, rng=None, noise=True)
render_xray(scene, energy="low"|"high", rng=None, noise=True);  render_all(scene, rng, noise) -> dict
make_labels(scene) -> list[dict]
generate_sample(seed_seq, spec=None, fixed=None, noise=True) -> dict
generate_dataset(n, seed, spec=None, fixed=None, noise=True) -> list[dict]
dataset_statistics(samples) -> dict
build_dataset_card(samples, spec, fixed, name, seed) -> dict
card_to_markdown(card) -> str;  write_dataset_card(card, out_dir) -> (json_path, md_path)
```

Helpers already implemented in the starter: `smooth_noise`, `ricker`, `pixel_grid`, `bbox_of`,
`object_height`, `gpr_velocity`, `capture_time_s`, `surface_normals`, `generate_dataset`,
`card_to_markdown`, `write_dataset_card`.

## Input / output

| | |
|---|---|
| **Input** | `spec` (factor → `{dist, low/high or values or value, unit, doc}`), `fixed` (held factors: image size, GSD, soil constants, visibility threshold, GPR settings), `n`, `seed` |
| **Output per sample** | `xi` (full parameter vector), `objects` (per-object params), `renders` = `rgb` (N,N,3) ∈ [0,1], `thermal` [K], `depth` [m], `xray_low`, `xray_high` [ln(N0/N)], `gpr` (n_t, N); `labels` (list of dicts); `scene` (geometry) |
| **Dataset card** | `dataset_card.json` + `dataset_card.md` |

## Constraints

- NumPy only (SciPy optional); matplotlib only for your own visualisation.
- Deterministic given the seed: identical seeds → byte-identical renders and labels.
- Throughput: the reference reaches ≈ 12 scenes/s at 128×128 with all six renders on a laptop CPU;
  the 100 scenes/s of 09.3 is an extension (local windows per object, fewer allocations).
- Test suite < 30 s (tests use 64×64 images).

## Expected behaviour

- Thermal contrast of a shallow object changes sign during the day; a 0.5 m deep object is
  thermally invisible (< 5 % of the shallow amplitude).
- $\delta(5\times10^{-7}\ \mathrm{m^2/s}) = 0.117$ m.
- A uniform slab's mean transmission matches $e^{-\mu t}$ within 1 % at $N_0=10^5$; the dual-energy
  ratio is 2.0 for $\mu_L/\mu_H = 0.6/0.3$ at any thickness.
- A fully buried object has an empty mask, no box and leaves the depth image unchanged, yet appears
  in the X-ray projection and as a GPR hyperbola.
- Removing an object from the z-buffer changes the noise-free depth exactly on its modal mask.

## Test cases (`tests/test_scenegen.py`)

| Test | Checks |
|---|---|
| `test_damping_depth_value`, `test_soil_temperature_satisfies_heat_equation` | diurnal model: $\delta$ and $\partial_tT=\alpha\partial_z^2T$ (FD, rel. err. < 1e-3) |
| `test_thermal_contrast_changes_sign_over_day_for_shallow_object` | thermal crossover; decay with depth |
| `test_xray_uniform_slab_matches_beer_lambert`, `test_dual_energy_ratio_independent_of_thickness` | X-ray physics |
| `test_parameters_within_declared_ranges`, `test_object_parameters_within_family_ranges`, `test_sampling_is_order_independent` | randomisation stays inside the declared support |
| `test_deterministic_by_seed` | byte-identical outputs for equal seeds; different seeds differ |
| `test_render_shapes_and_ranges` | shapes, finite values, plausible temperatures |
| `test_labels_consistent_with_renders` | mask area > 0 ⇔ visible; box ⇔ visible and tight; modal ⊂ amodal; positive ⇒ visible; buried ⇒ invisible; object removal changes depth exactly on its mask |
| `test_fully_buried_object_invisible_but_seen_by_xray` | label/render consistency across modalities |
| `test_depth_geometry_flat_ground`, `test_foliage_occludes` | depth = altitude − exposed height; burial halves the exposed height; cylinder crest; occlusion |
| `test_gpr_hyperbola_timing` | apex and off-apex arrival times match $2h/c + 2\sqrt{x^2+d^2}/v$ within 1.5 samples |
| `test_dataset_card_lists_every_factor` | card lists every spec and fixed key; JSON round-trip; Markdown table |

## Milestones

1. Parameter sampling + checking; terrain and foliage fields.
2. Object geometry and the z-buffer; depth render and labels (get the consistency tests green first).
3. Physics: diurnal model, thermal contrast, X-ray projection; then RGB and GPR renders.
4. Seeding discipline (three child streams) and the dataset card.

## Extension challenges

- Reproduce the 09.3 §3 lab with your generator: train on narrow vs randomised ξ, test on a
  held-out "real" configuration; report per-factor ablations using the logged ξ.
- Replace the heuristic object contrast with a 1D finite-difference heat solver through an object layer.
- Cast shadows (ray-march the height field towards the sun) and check which detector shortcut they create.
- Local-window geometry to exceed 100 scenes/s; profile before and after.
- FDTD-lite GPR channel (2D scalar wave) and compare its hyperbolas with the geometric model.
- Feed the generator to [P09](projects/p09-cv-detection/README.md) and compute recall@FAR vs burial fraction.

## Hints

<details class="answer"><summary>Hint 1 — z-buffer and masks</summary>

Keep one `owner` map. For object $k$, update pixels where `footprint & (z_top > surface)`, then set
`owner = k` there. The modal mask is simply `owner == k`; this makes the "mask ⇔ visible" and
"removal changes depth exactly on the mask" invariants hold by construction. Foliage goes last.

</details>

<details class="answer"><summary>Hint 2 — burial</summary>

Put the object's base at `z_ref - burial_fraction * H - cover_depth`, with `z_ref` the terrain at
the object's centre. Exposure then falls out of the z-buffer; do not compute visibility from
`burial_fraction` directly (terrain slope makes that wrong).

</details>

<details class="answer"><summary>Hint 3 — seeding</summary>

`np.random.SeedSequence(seed).spawn(n)` gives independent per-sample seeds; spawn three children per
sample for ξ, layout and render noise. Sample dict keys in `sorted()` order so reordering the spec
does not change the data.

</details>

<details class="answer"><summary>Hint 4 — GPR</summary>

Compute $r(x)=\sqrt{(x-x_0)^2+\Delta y^2+d^2}$ for all columns at once and add
`amp * ricker(t - (t_air + 2 r / v))` as a broadcast (n_t, N) array. Floor $d$ at 1 cm so exposed
objects still produce a hyperbola.

</details>

## How to run

```bash
python -m pytest projects/p10-scene-generator                  # your starter
EOD_SOLUTION=1 python -m pytest projects/p10-scene-generator   # reference solution
python projects/p10-scene-generator/solution/scenegen.py       # throughput demo (100 scenes)
```
