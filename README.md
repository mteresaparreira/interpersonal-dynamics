# interpersonal-dynamics

Analysis of the dynamics of **interpersonal perception** in dyadic and group
interactions — how people's read of each other shifts, moment to moment, while they
are talking, and whether that shift can be predicted from what they say, how they
say it, and what their faces do.

Cornell University (RIG Lab / Department of Information Science) with Honda Research
Institute USA. Cornell IRB0143729.

> ### ⚠️ This repository contains **no participant data**
> The working data is **not anonymised**: it includes faces, voices, verbatim
> political discussion, Prolific IDs, IP addresses and geolocation. Everything here
> is code, documentation, and aggregate result tables. Read
> **[`docs/privacy.md`](docs/privacy.md)** before adding a single file, and note the
> credentials listed there that need rotating.

---

## The idea in one paragraph

Most computational work on emotion models the *individual* — an internal state
inferred from an expression. This project models the *pair*. Grounded in a
behavioural-ecology view of emotion, where expressions are social tools rather than
read-outs of inner states, it replaces **valence** with **approach/withdrawal**: the
degree to which behaviour is perceived as increasing or decreasing social distance.
Participants have a real, mildly adversarial conversation; afterwards each one
re-watches it and continuously rates *how the other person was coming across*, using
a purpose-built tool called [CORAE](https://corae.org). Summing those ratings gives
an "emotional bank account" trace — friendly behaviour deposits, unfriendly
behaviour withdraws — and the **slope** of that trace over a rolling window,
averaged across the interactants, is the **Interpersonal Dynamics Curve (IDC)**: a
continuous, pair-level proxy for interaction quality that can be used as a machine
learning target.

---

## The two studies

|  | **Study 2** | **Study 3** |
|---|---|---|
| Setting | fully online | in person, lab room |
| Group size | **2** | **3** |
| Discussion | up to **10 min** | **5 min** |
| Platform | Zencastr (separate per-speaker streams) | ROS capture rig |
| Capture | 2 webcams, 2 mic streams, 30 fps | 3 Intel RealSense RGB-D cameras + ReSpeaker array + scene camcorder, 15 fps |
| Recruitment | Prolific, screened for opposing political leaning | posters, flyers, Calendly |
| Task | Reasons for Poverty, rank top 5 | same, but ranked individually first, then group consensus under a (fictitious) competitive bonus |
| Who rates whom | each rates **1** other | each rates **2** others, one at a time |
| CORAE build | 0.15.0a | public release |
| Run window | Dec 2022 – May 2023 | from May/June 2024 |
| Sessions run | **30** (27 usable) | **34** |
| Participants | **60** (54 usable) | **102** |
| Annotated | 27 sessions / 54 curves | **15 sessions / 45 participants / 90 curves** |
| Compensation | US$14 | US$50 |
| Modelled? | yes, three campaigns | **not yet** |

Full protocols: **[`docs/study2-dyadic-online.md`](docs/study2-dyadic-online.md)** ·
**[`docs/study3-triadic-inperson.md`](docs/study3-triadic-inperson.md)**

A **Study 1** also exists — 10 Zoom dyads, 2022, no CORAE — whose findings shaped
Study 2's design. Its data is not on the working drive; see
[`docs/data-inventory.md`](docs/data-inventory.md#study-1--dyadic-zoom-predecessor-no-corae-data).

---

## The data, in brief

**Annotations.** A 15-point bounded slider, **−7 (disagreeable) … +7 (agreeable)**,
logged once a second *and* on every movement. Study 2 ratings are strongly positively
skewed (+7 alone is 25 % of samples; positive:negative ≈ 19.6:1). Study 3 ratings are
far more centred — mode 0, thin symmetric tails.

**Features (Study 2 only).** 237 columns at 2 Hz, built from:

- **OpenFace 2.0** — 49 per participant: 8 gaze, 6 head pose, 17 AU intensities, 18 AU presences
- **openSMILE ComParE_2016** — 65 per participant: F0, jitter/shimmer/HNR, 26 RASTA filterbank, 15 spectral, 14 MFCC
- **Voice Activity Detection** — 3 per participant (speaking state, cumulative talk time, turn count) + session-level conversational imbalance

Each feature is the **maximum over a lookback window** (2.5 / 5 / 7.5 s swept), not
an instantaneous value. Each session appears twice with the participants swapped,
since the IDC describes the interaction rather than either person.

**Study 3** has per-stream OpenFace, audio, Whisper transcripts and annotations, but
**no model-ready matrix was ever assembled** for it.

Column-by-column: **[`docs/data-dictionary.md`](docs/data-dictionary.md)** ·
**[`docs/feature-index.md`](docs/feature-index.md)** (all 237 `sN` aliases) ·
file shapes: **[`data_samples/`](data_samples/)** (synthetic) ·
where everything lives: **[`docs/data-inventory.md`](docs/data-inventory.md)**

---

## What was tried, and how it went

Full write-up with tables: **[`docs/results.md`](docs/results.md)**.

| Campaign | Target | Best | Baseline | Verdict |
|---|---|---|---|---|
| **2023** IDC regression — linear, SVR, MLP, RF, LSTM, GRU, BLSTM, Transformer | IDC, continuous | GRU, test **CCC 0.226 ± 0.09** | — | learnable in principle; **does not generalise** to unseen participants (train CCC > 0.92 on every model) |
| **2024** IDC classification — LSTM / BiLSTM / GRU, 2037-run sweep | 15-class rating | LSTM, **acc 0.207** | **0.255** majority | **worse than guessing `+7`.** Abandon this framing |
| | binary change direction | GRU, **acc 0.609 ± 0.016** | **0.535** majority | real but small margin — **and partly leaked**, see below |
| **2025** rating classification — RF, GRU/LSTM with fusion sweeps, MiniRocket; t-tests; feature importance | both | — | — | no feature dominates (flat RF importances); only 4 features separate the two change directions at *p* < 0.05 |

Three things anyone picking this up should know before trusting a number:

1. **Label leakage in the change-direction task.** `createDataSplits_idc.py` passes
   `df.iloc[:, 5:]` to the model, which in the sign datasets includes
   `value_p0`/`value_p1` — the absolute rating level, which at the `+7` ceiling
   partly determines the direction of the next move. The 0.55–0.61 binary accuracies
   are an upper bound and need a clean re-run.
2. **`sN` means different things in different files.** The column aliases were
   assigned positionally and the two dataset families have a different column in the
   block, so **119 of 237 names shift**. `s4` is `total_talking_time_p0` in one file
   and `total_number_turns_p0` in the other. Several committed scripts hardcode
   `sN` literals and `iloc` ranges written for only one layout. Resolve through
   `docs/dict_cols*.json`.
3. **Half of Study 3's annotations are missing from the interpolated file.**
   `study3_json_interp.csv` has 45 of 90 curves because the interpolation groups by
   rater and drops the second ratee. The raw `study3_json.csv` is complete.

Each is documented in place in
[`docs/data-dictionary.md`](docs/data-dictionary.md#5-pitfalls-worth-knowing-before-you-reuse-any-of-this).

### Findings that are not about models

- **Trait agreeableness** predicts how a person is perceived, on both the continuous
  and the survey measure; **neuroticism** predicts the survey measure.
- **Conversational imbalance** predicts how much the two members of a dyad
  *disagree* about each other — lopsided conversations produce divergent reads.
- **Positive-tone utterance ratio** predicts perception.
- The continuous measure correlates strongly (*r* = 0.72, *p* < 0.001) with a
  single-item post-hoc survey rating — the core validation that CORAE captures
  something real.

---

## Repository layout

```
docs/                                  protocols, data dictionary, inventory, results, privacy
data_samples/                          synthetic examples of every file format
results/
  study2/                              sweep + fold metrics, feature importance, t-tests, QC
  study3/                              OpenFace confidence per participant

study2_dyadic_online/
  feature_extraction/                  openSMILE, Whisper sentiment, frames, mel-spectrograms, ViT
  preprocessing/                       CORAE JSON → curves → IDC; merge to feature matrix; stats; plots
  models/
    idc_regression/                    2023 — 8 architectures, CCC loss, W&B sweeps
    idc_classification/                2024 — LSTM/GRU/BiLSTM, 4 datasets, SLURM jobs
    rating_classification/             2025 — RF, RNN fusion sweeps, MiniRocket

study3_triadic_inperson/
  recording/                           ROS + RealSense + ReSpeaker capture pipeline
  preprocessing/                       CORAE JSON → curves; pyannote diarisation; VTT → dataframes; OpenFace batch
  quality/                             face-tracking confidence checks
```

### Reading order for a newcomer

1. [`docs/privacy.md`](docs/privacy.md) — before touching anything
2. [`docs/study2-dyadic-online.md`](docs/study2-dyadic-online.md) — where the data comes from
3. [`docs/data-dictionary.md`](docs/data-dictionary.md) — especially §5, the pitfalls
4. `study2_dyadic_online/preprocessing/process_corae_jsons.ipynb` — raw ratings → IP / IDC
5. `study2_dyadic_online/preprocessing/merge_all_feats.ipynb` — the whole feature pipeline in one notebook
6. [`docs/results.md`](docs/results.md) — what has and has not worked

### Running anything

Nothing here runs out of the box. Every script expects the data layout on the lab
drive (`../data/...`, `../../data/training/...`) and most expect a Weights & Biases
project and a SLURM cluster. The `.sub` files are the job specs. Notebooks have
had their outputs stripped and some carry absolute paths from the machines they were
written on. Treat this as a record of what was done, not a turnkey pipeline.

Main dependencies across the tree: `pandas`, `numpy`, `scikit-learn`, `scipy`,
`statsmodels`, `imbalanced-learn`, `torch`, `tensorflow`/`keras`, `tsai`/`fastai`,
`wandb`, `opensmile`, `librosa`, `ffmpeg-python`, `torchvision`, `pyannote.audio`,
`openai`, `matplotlib`, `seaborn`, `tikzplotlib`. External tools: **OpenFace 2.2.0**,
**Whisper**, **CORAE**.

---

## Publications

- **Sack, Parreira, Fu, Lipman, Javed, Jamali, Jung (2023).** *CORAE: A Tool for
  Intuitive and Continuous Retrospective Evaluation of Interactions.* ACII 2023.
  Introduces the tool and validates it on 12 dyads / 24 participants.
- **Parreira, Sack, Javed, Jamali, Jung (2023).** *"How Did They Come Across?"
  Lessons Learned from Continuous Affective Ratings.* ICRA 2023 workshop.
  Discourse analysis mapping rating events to interaction phenomena.
- **(2023).** *What Predicts Interpersonal Affect? Preliminary Analyses from
  Retrospective Evaluations.* RO-MAN 2023 LBR. Personality, conversational balance
  and speech sentiment as predictors.
- **Parreira, Sack, Jung, Javed, Jamali.** *Beyond Internal States: Benchmarking
  Interpersonal Affect Estimation.* Q1 2023–24 progress report. Introduces the IDC
  and the regression benchmark.

Related repository: **[mteresaparreira/interpersonal-affect](https://github.com/mteresaparreira/interpersonal-affect)**
— the 2025 rating-classification code, mirrored here under
`study2_dyadic_online/models/rating_classification/`.

Tool: **[corae.org](https://corae.org)**

---

## Licence

MIT — see [`LICENSE`](LICENSE).
