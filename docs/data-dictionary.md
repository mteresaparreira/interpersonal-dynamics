# Data dictionary

Everything here describes **Study 2** unless stated otherwise. Study 3 never got a
model-ready feature matrix; its per-stream formats are in
[`study3-triadic-inperson.md`](study3-triadic-inperson.md).

---

## 1. The annotation signal

### Interpersonal Ratings (IR)
The raw CORAE slider trace. Integer, **−7 (disagreeable) … +7 (agreeable)**,
15 points. Sampled once a second plus on every slider move, so irregular; resampled
to a fixed grid before anything else happens.

Two resampling rates are used across the repo:
- **10 Hz** (`df_interpolated1dec`) — used for the ACII/ROMAN analyses and for
  computing IDC slopes.
- **2 Hz** (`df_interpolated5dec`) — used for the model-ready datasets, because
  Voice Activity Detection only resolves to 0.5 s and the audiovisual features are
  downsampled to match.

### Cumulative ratings `y_c`
`y_c(t) = Σ IR(0…t)`. Read as accumulated or depleted *emotional capital*: friendly
behaviour builds, unfriendly behaviour depletes. Rising `y_c` means the other person
is being perceived as moving closer.

### Interpersonal Perception (IP)
Slope of an OLS fit to `y_c` over the **whole** interaction. One number per rater
per session. Fit quality across the first 24 curves: R² = 0.88 ± 0.34. IP correlates
strongly with the single-item survey measure IA, *r* = 0.72, *p* < 0.001 — that
correlation is the validation argument for the whole method.

### Interpersonal Agreeableness (IA)
Survey item: *"How did the other participant come across?"*, 7-point Likert,
disagreeable → agreeable. The static counterpart to IP.

### The IDC

**Interpersonal Dynamics Curve** — the session-level, time-varying generalisation of
IP, and the main modelling target.

1. Resample each rater's IR to 10 Hz, take the cumulative sum `y_c`.
2. Pick an **interaction history** `h`. For each `t ∈ [h, end]`, fit a linear
   regression to `y_c(t−h … t)` and keep the slope. This gives `y_s`, a curve of
   "how fast is my perception of the other moving right now". Tested `h ∈ {2.5, 5} s`.
3. Average the two raters' `y_s` curves point by point. That average **is** the IDC.

So IP is the slope over the whole interaction; the IDC is the slope over a rolling
window, merged across the dyad. It is a continuous proxy for interaction quality
that belongs to the *pair*, not to either individual.

---

## 2. Label variants used for training

| Name | Definition | Classes | Rows |
|---|---|---|---|
| **absolute rating** (`all_data_05.csv`) | the rater's IR value at that timestep | 15, −7…+7 | 60 808 |
| **change direction** (`all_data_05_sign.csv`) | sign of the change in IR | 2, {0, 1} | 4 090 |
| **IDC regression** (`all_data_l{l}t{h}_norm*.csv`) | the IDC value (continuous) | — | 60 193 |

Naming in the 2024 scripts: `IDC15` = 15-class absolute rating, `IDC2` = binary
change direction, suffix `_n` = standardised features.

### Label distributions — both are badly imbalanced

**Absolute rating (15-class).** Overwhelmingly positive and piled on the ceiling:

| −7 | −6 | −5 | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 | +5 | +6 | +7 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 75 | 70 | 93 | 161 | 279 | 665 | 1182 | 8882 | 3709 | 4121 | 4223 | 5392 | 7395 | 9058 | **15503** |

Positive:negative ≈ **19.6 : 1**. `+7` alone is 25 % of the data, so a
majority-class classifier scores ~0.255 accuracy — which is *above* every 15-class
model that was trained (best was 0.21). The 15-class formulation never worked.

**Change direction (binary).** Only timesteps where the rating actually moved are
kept (`0`-derivative rows dropped), leaving 4090 rows: class `1` = 2189 (53.5 %),
class `0` = 1901 (46.5 %). Majority baseline 0.535. This is the only formulation
where models beat baseline.

---

## 3. The feature vector

237 features at 2 Hz. 118 per participant plus one session-level feature.

| Block | Per participant | Source |
|---|---|---|
| Gaze | 8 — `gaze_0_{x,y,z}`, `gaze_1_{x,y,z}`, `gaze_angle_{x,y}` | OpenFace 2.0 |
| Head pose | 6 — `pose_T{x,y,z}`, `pose_R{x,y,z}` | OpenFace 2.0 |
| Action unit intensity | 17 — `AU{01,02,04,05,06,07,09,10,12,14,15,17,20,23,25,26,45}_r` | OpenFace 2.0 |
| Action unit presence | 18 — the same plus `AU28_c` | OpenFace 2.0 |
| **OpenFace subtotal** | **49** | |
| Voice quality | 10 — `F0final`, `voicingFinalUnclipped`, `jitterLocal`, `jitterDDP`, `shimmerLocal`, `logHNR`, `audspec_lengthL1norm`, `audspecRasta_lengthL1norm`, `pcm_RMSenergy`, `pcm_zcr` | openSMILE ComParE_2016 |
| RASTA filterbank | 26 — `audSpec_Rfilt_sma[0…25]` | openSMILE |
| Spectral | 15 — `pcm_fftMag_*` (f-bands, roll-off, flux, centroid, entropy, variance, skewness, kurtosis, slope, psySharpness, harmonicity) | openSMILE |
| MFCC | 14 — `mfcc_sma[1…14]` | openSMILE |
| **openSMILE subtotal** | **65** | |
| Conversational | 3 — `vad`, `total_talking_time`, `total_number_turns` | VAD logs |
| Rating-derived | 1 — `value` *or* `derivative_sign`, depending on the dataset | CORAE |
| **Per-participant total** | **118** | |
| Session-level | 1 — `imbalance` | VAD logs |
| **Grand total** | **237** | |

Suffixes `_p0` / `_p1` identify the participant. Because the IDC describes the
*interaction* rather than either person, each session appears **twice** in the
dataset with p0/p1 swapped — hence 54 "session keys" (`1011_0`, `1011_1`, …) from
27 sessions. That is data augmentation, not duplication of labels: the groundtruth
differs between the two rows.

### Lookback

Following the affect-estimation convention, a feature's value at time `t` is the
**maximum** over the preceding window, not the instantaneous value. Lookback
`l ∈ {2.5, 5, 7.5} s` was swept. Audiovisual features are downsampled to the 2 Hz
VAD rate.

### Full `sN` → name map

[`feature-index.md`](feature-index.md), generated from
[`dict_cols.json`](dict_cols.json) and [`dict_cols_sign.json`](dict_cols_sign.json).

---

## 4. Dataset files

| File | Shape | What it is |
|---|---|---|
| `all_data_05.csv` | 60 808 × 242 | 2 Hz, absolute-rating label, raw feature values |
| `all_data_05_norm.csv` | 60 808 × 242 | same, `StandardScaler`-standardised (`scaler.pkl`) |
| `all_data_05_sign.csv` | 4 090 × 242 | 2 Hz, change-direction label, raw |
| `all_data_05_norm_sign.csv` | 4 090 × 242 | same, standardised (`scaler_sign.pkl`) |
| `all_data_05_pca.csv` | 30 404 × 93 | PCA on the standardised features, 90 % variance retained (88 components) |
| `all_data_05_pca_sign.csv` | 1 593 × 85 | same for the sign dataset (80 components) |
| `all_data_l{l}t{h}_norm.csv` | 60 192 × 240 | IDC regression target, lookback `l`, horizon `h` |
| `all_data_l{l}t{h}_norm_pca.csv` | — | PCA variants of the above |

Column layout: `session, timeelapsed, groundtruth, <label-partner cols ×2>, s1 … s237`.
`session` is `<sessionID>_<0|1>`.

The IDC regression files (`l{l}t{h}`) have no label-partner columns — they go
straight `session, timeelapsed, groundtruth, s1 … s237`. PCA on those keeps 88–92
components (89.7 ± 1.5) depending on `l` and `h`.

⚠️ **The two `all_data_05_pca*` files contain only the `_0` half of each mirrored
session** — 27 session keys and exactly half the rows of their non-PCA source. The
`_1` copies were dropped somewhere in `merge_all_feats.ipynb`'s PCA cells. Either
regenerate them or do not compare PCA results against non-PCA results as if the two
were trained on the same data.

**None of these files are in this repository.** They are 12 MB – 277 MB each and
derive directly from participant audio and video. See
[`data-inventory.md`](data-inventory.md).

---

## 5. Pitfalls worth knowing before you reuse any of this

### The `sN` trap
`s1`–`s237` are positional aliases assigned at merge time, and the two dataset
families were merged with a different column present. **`s4` is
`total_talking_time_p0` in `all_data_05.csv` and `total_number_turns_p0` in
`all_data_05_sign.csv`.** 119 of 237 columns shift. Consequences in the committed
code:

- `rf_full_model.py` / `gru_full_model.py` select modalities with hardcoded
  `iloc` ranges and the literals `s1, s4, s5, s122, s123`. Those ranges were written
  against the absolute-rating layout. Run against the sign dataset the "talk"
  modality silently picks up `gaze_0_x_p0` in place of `total_talking_time_p0`.
- The `iloc` ranges are also off by one at the end of each block: the face slice
  `10:58` takes 48 of the 49 OpenFace features, dropping `AU45_c`.

Always resolve columns through `dict_cols*.json` rather than by position.

### Label leakage into the change-direction task
`createDataSplits_idc.py` takes `features = df.iloc[:, 5:]`, i.e. everything from
`s1` on. In the **sign** datasets that block contains `s119 = value_p0` and
`s120 = value_p1` — the absolute rating level. At the `+7` ceiling the only possible
change is downward, so the level strongly constrains the label. The IDC2 / IDC2_n
accuracies (0.55–0.61 against a 0.535 baseline) should be read with that in mind,
and the task should be re-run with `s119`/`s120` dropped before the margin is
treated as real.

The same block is why `value_p0` tops the t-test output in
[`results/study2/ttest_significant_features_sign.csv`](../results/study2/ttest_significant_features_sign.csv)
at *p* = 1.4 × 10⁻¹⁰: `feature_stats_analysis.ipynb` excludes `['s2','s3','s120','s121']`,
a list written for the absolute-rating layout, which under the sign layout removes
`vad_p0`, `total_talking_time_p0`, `value_p1`, `vad_p1` — and leaves `value_p0` in.

The 2025 RF and RNN paths are **not** affected: `modalities_combination_data_prep`
rebuilds the frame from `df.iloc[:, :3]` plus explicit modality slices, so the
rating columns never reach the model.

### Mirrored sessions and fold construction
Because every session appears twice (p0/p1 swapped), splits must be grouped by
**session ID**, not by row. The split helpers do group on the `session` column, but
that column is `1011_0` / `1011_1` — two distinct values for the same dyad. **The
two halves of a dyad can therefore land on opposite sides of a train/test split.**
The Q1 report describes the folds as non-overlapping on participants; verify this
holds for your fold indices before quoting generalisation numbers.

### Frame removal
OpenFace frames below 0.7 detection confidence are dropped before merging. Per
participant this removes 0 – 21 % of frames;
[`results/study2/openface_frames_removed.csv`](../results/study2/openface_frames_removed.csv)
has the full table. Dropped frames become gaps that the 2 Hz resampling papers over.
