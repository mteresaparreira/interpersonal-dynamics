# What we tried and what came out

Three modelling campaigns over two and a half years, all on Study 2 data. Study 3
has never been modelled.

| # | Campaign | Target | Framing | Best result |
|---|---|---|---|---|
| 1 | 2023 — IDC benchmarking | IDC (continuous) | regression | GRU, test CCC **0.226 ± 0.09** |
| 2 | 2024 — IDC classification | 15-class rating / binary change | classification | GRU, binary acc **0.609 ± 0.016** |
| 3 | 2025 — rating classification | same two targets | classification + feature analysis | see below |

---

## 1. IDC regression (2023) — `models/idc_regression/`

Reported in the Q1 2023–24 progress report, *Beyond Internal States: Benchmarking
Interpersonal Affect Estimation*.

**Setup.** Sequential decision framing: at each timestep the model sees a state
vector and emits an IDC estimate. 54 mirrored sessions, 60 192 samples, 237
features reduced by PCA to 88–92 components (90 % variance). Datasets swept over
feature lookback `l ∈ {2.5, 5, 7.5} s` and IDC horizon `h ∈ {2.5, 5} s`.

**Protocol.** Hyperparameters tuned on an 80/20 split (47 770 train, 12 422 test),
then the winner retrained over 5 non-overlapping-participant folds for 1000 epochs;
reported numbers are fold averages. Regression models via scikit-learn +
`GridSearchCV`; RNNs and the Transformer via PyTorch + Weights & Biases. CCC was
used as both the tuning metric and the training loss. Hardware: AMD EPYC 7313 for
the sklearn models, NVIDIA GTX TITAN X for the neural ones.

**Metrics.** RMSE and Concordance Correlation Coefficient
`CCC = 2ρσₓσᵧ / (σₓ² + σᵧ² + (μₓ − μᵧ)²)` — CCC penalises bias as well as
decorrelation, which matters for curve-shaped targets.

**Results** (mean ± SD across 5 test folds):

| Model | Dataset | Train RMSE | Train CCC | Test RMSE | **Test CCC** |
|---|---|---|---|---|---|
| Linear | l=7.5, h=2.5 | 18.32 ± 0.69 | 0.554 ± 0.026 | 27.14 ± 4.72 | 0.040 ± 0.142 |
| SVR | l=2.5, h=5.0 | 13.73 ± 0.37 | 0.763 ± 0.035 | **23.40 ± 4.93** | 0.108 ± 0.081 |
| MLP | l=5.0, h=2.5 | 1.72 ± 0.10 | 0.997 ± 0.000 | 24.23 ± 4.37 | 0.166 ± 0.051 |
| LSTM | l=2.5, h=2.5 | 3.80 ± 0.28 | 0.986 ± 0.003 | 25.23 ± 4.10 | 0.187 ± 0.030 |
| RF | l=5.0, h=5.0 | 0.32 ± 0.02 | 0.999 | 23.67 ± 4.16 | 0.197 ± 0.100 |
| BLSTM | l=2.5, h=2.5 | 2.96 ± 0.26 | 0.992 ± 0.002 | 24.67 ± 4.48 | 0.201 ± 0.065 |
| Transformer | l=2.5, h=5.0 | 6.98 ± 0.48 | 0.962 ± 0.007 | 27.21 ± 3.28 | 0.215 ± 0.117 |
| **GRU** | l=2.5, h=2.5 | 8.72 ± 2.66 | 0.924 ± 0.041 | 25.58 ± 4.67 | **0.226 ± 0.09** |

Best GRU: batch 64, dropout 0.2, hidden 128, lr 1e-4, sequence length 10 samples
(= 5 s of memory), Adam.

**Reading.** Every model trains to near-perfect CCC and lands between 0.04 and 0.23
on held-out participants. That gap is the headline: the IDC *is* learnable from
interaction features — which is the validation argument for the measure — but
nothing generalises to unseen people. Two secondary observations held up: the
best deep models all preferred the **shortest** lookback (`l = 2.5`), suggesting the
IDC is better predicted from fine-grained input; and an initial sweep over sequence
length `s ∈ {5, 10, 15}` settled on `s = 10` for every RNN.

---

## 2. IDC classification (2024) — `models/idc_classification/`

The regression framing hit a ceiling, so the target was discretised. Four datasets:
`IDC15` (15-class absolute rating), `IDC15_n` (standardised), `IDC2` (binary change
direction), `IDC2_n` (standardised). Keras/TensorFlow, single recurrent layer +
dropout + dense softmax.

**Swept:** sequence length {5, 10, 15} · units {32, 64, 128, 256} · dropout
{0, 0.2, 0.6} · activation {softmax, sigmoid, relu} · optimiser {Adam, SGD,
Adadelta} · batch {512, 1024} · lr 1e-3 · 200 epochs · categorical cross-entropy ·
LSTM / BiLSTM / GRU. 2037 runs — the full sweep table is
[`results/study2/idc_classification_sweep.csv`](../results/study2/idc_classification_sweep.csv).

**Metrics.** Macro accuracy / precision / recall / F1, plus **tolerant** variants
where a prediction counts as correct if it matches any true label within ±1
timestep in the same session (`get_metrics.py`, `tolerance=1`).

### Best single configuration per dataset

| Dataset | Arch | Seq | Units | Drop | Act | Opt | Batch | Acc | F1 | Tol. acc | Tol. F1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IDC15 | LSTM | 10 | 64 | 0 | softmax | Adadelta | 1024 | 0.207 | 0.061 | 0.228 | 0.112 |
| IDC15_n | GRU | 10 | 64 | 0.6 | softmax | Adadelta | 512 | 0.170 | 0.061 | 0.191 | 0.120 |
| IDC2 | GRU | 5 | 64 | 0.6 | softmax | Adam | 512 | 0.553 | 0.532 | 0.858 | 0.857 |
| IDC2_n | GRU | 5 | 256 | 0.6 | sigmoid | Adam | 512 | **0.591** | **0.582** | 0.874 | 0.873 |

### 5-fold averages — [`results/study2/idc_classification_fold_metrics.csv`](../results/study2/idc_classification_fold_metrics.csv)

| Run | Acc | F1 | Tol. acc | Tol. F1 |
|---|---|---|---|---|
| `gru_05_sn_all1` (binary, normalised) | **0.609 ± 0.016** | **0.604 ± 0.018** | 0.898 ± 0.023 | 0.897 ± 0.023 |
| `gru_05_sn_all2` | 0.604 ± 0.017 | 0.595 ± 0.022 | 0.897 ± 0.032 | 0.896 ± 0.033 |
| `gru_05_s_all1` (binary, raw) | 0.529 ± 0.020 | 0.413 ± 0.081 | 0.864 ± 0.029 | 0.860 ± 0.030 |
| `gru_05_s_all2` | 0.525 ± 0.013 | 0.389 ± 0.080 | 0.861 ± 0.030 | 0.857 ± 0.031 |
| `lstm_05_all1` (15-class) | 0.210 ± 0.017 | 0.058 ± 0.008 | 0.223 ± 0.021 | 0.080 ± 0.021 |
| `lstm_05_all2` | 0.203 ± 0.019 | 0.058 ± 0.007 | 0.216 ± 0.021 | 0.081 ± 0.021 |
| `lstm_05_n_all2` | 0.205 ± 0.029 | 0.069 ± 0.008 | 0.220 ± 0.030 | 0.094 ± 0.018 |
| `gru_05_n_all1` (15-class, normalised) | 0.189 ± 0.047 | 0.090 ± 0.014 | 0.206 ± 0.048 | 0.114 ± 0.010 |

**Reading, with the baselines attached.**

- **15-class is dead.** 0.19–0.21 accuracy against a **0.255 majority-class
  baseline** — the models are worse than always guessing `+7`. Macro F1 of 0.06
  confirms they collapse onto the head of a distribution where the top class holds a
  quarter of the mass and the bottom five classes hold under 1 % between them.
- **Binary change direction works, modestly.** 0.609 against a **0.535 majority
  baseline**: a real but small margin, and standardising the features is what
  produces it (0.609 vs 0.529 raw). **See the leakage caveat below before quoting
  this number.**
- Tolerant metrics (~0.90) are much higher than strict, which tells you the models
  get the *timing* of changes roughly right while missing the exact sample.
- The contemporaneous conclusion in the May 2024 SOW was exactly this: *"norm binary
  performs really well… TIMING really matters for sign."*

> ⚠️ **Leakage caveat.** `createDataSplits_idc.py` feeds `df.iloc[:, 5:]` to the
> model, and in the sign datasets that block contains `s119 = value_p0` and
> `s120 = value_p1` — the absolute rating level. At the `+7` ceiling the only
> available move is downward, so the level partly determines the label. The
> 0.553–0.609 binary numbers are therefore an upper bound and should be re-run with
> those two columns dropped. Details in
> [`data-dictionary.md`](data-dictionary.md#label-leakage-into-the-change-direction-task).

---

## 3. Rating classification and feature analysis (2025) — `models/rating_classification/`

Mirrored in the companion repo
[`mteresaparreira/interpersonal-affect`](https://github.com/mteresaparreira/interpersonal-affect).
Three model families, all swept through W&B, all sharing `create_data_splits.py`
(70/20/10 by session, 5 folds) and `get_metrics.py`:

- **Random Forest** — `rf/rf_full_model.py`. SMOTE balancing available, modality
  ablation over {audio, face, talk}, feature-set tag {Full, Stat, RF}. Emits
  per-fold feature importances.
- **GRU / LSTM** — `rnn/`. Keras. Sweeps fusion strategy (`early` /
  `intermediate` / `late`) at two levels: across **modalities** and across
  **participants** (`part_fusion`), plus bidirectionality, 1–3 layers, 64/128/256
  units, four optimisers, sequence lengths {2, 5, 10, 30, 60}.
- **MiniRocket** — `minirocket/`, via `tsai`. Interval-based time-series
  classification with configurable context length, stride, and over/under-sampling.

The RNN sweep space here is combinatorially much larger than 2024's — it is the
only place fusion strategy is treated as a variable — but no consolidated fold
metrics were saved for it.

### What distinguishes the two change directions

**Welch t-tests**, raw sign dataset, 233 features tested. Only **five** reach
*p* < 0.05 ([`results/study2/ttest_significant_features_sign.csv`](../results/study2/ttest_significant_features_sign.csv)):

| Feature | p |
|---|---|
| `value_p0` (`s119`) | 1.4 × 10⁻¹⁰ ⚠️ leakage, see above |
| `F0final_sma_p0` (`s54`) | 0.0093 |
| `AU12_r_p0` (`s27`) — lip corner puller, i.e. smiling | 0.0135 |
| `mfcc_sma[2]_p0` (`s106`) | 0.0222 |
| `mfcc_sma[6]_p0` (`s110`) | 0.0233 |

Discounting the leaked one, the signal that survives is **pitch, smiling, and
vocal timbre in the person being rated** — four weak effects out of 233, none of
which would survive multiple-comparison correction. By contrast, on the 15-class
absolute-rating dataset nearly every feature returns *p* ≈ 0
([`ttest_significant_features_multiclass.csv`](../results/study2/ttest_significant_features_multiclass.csv)),
which reflects 60 808 samples and the mirrored-session structure far more than it
reflects any effect.

### Random Forest feature importance

Binary change direction, Full feature set, raw dataset. 229 features ranked (the
committed table is the top 194, carrying 98.5 % of total importance). The
distribution is almost flat — the top feature carries 0.0080 and the tenth 0.0069,
against 1/229 ≈ 0.0044 for uniform, and the smallest is 0.0003.
**No feature dominates.**

| Rank | Feature | Importance |
|---|---|---|
| 1 | `pose_Rz_p0` (head roll) | 0.0080 |
| 2 | `total_talking_time_p1` | 0.0079 |
| 3 | `pose_Rz_p1` | 0.0079 |
| 4 | `pose_Tx_p0` | 0.0078 |
| 5 | `imbalance` | 0.0077 |
| 6 | `mfcc_sma[10]_p1` | 0.0077 |
| 7 | `mfcc_sma[3]_p1` | 0.0076 |
| 8 | `AU25_r_p0` (lips part) | 0.0075 |
| 9 | `pose_Ty_p1` | 0.0070 |
| 10 | `AU17_r_p0` (chin raiser) | 0.0069 |

Full table: [`results/study2/rf_feature_importance_sign.csv`](../results/study2/rf_feature_importance_sign.csv).
Head pose and conversational share lead; `imbalance` at rank 5 is consistent with
the ROMAN 2023 finding below.

### Representation experiments that were started but not evaluated

`feature_extraction/` also contains a late pivot away from hand-crafted features
toward learned ones — 30 fps video frames, 128×128 mel-spectrograms aligned
frame-for-frame with the video, and ViT-B/16 CLS-token embeddings written to HDF5.
No results from this path exist on the drive.

---

## Non-model findings worth carrying forward

From ROMAN 2023 (*What Predicts Interpersonal Affect?*), ANCOVAs on the 27-session
set controlling for gender and age:

- **Trait agreeableness** predicts how a person is perceived, on both the continuous
  measure IP (*F*(1,53) = 6.67, *p* = 0.01) and the survey measure IA
  (*F*(1,53) = 4.48, *p* = 0.04). Trait **neuroticism** also predicts IA
  (*F*(1,53) = 4.65, *p* = 0.04).
- **Conversational imbalance** predicts the *disagreement* between the dyad's two IP
  values (*F*(1,26) = 4.79, *p* = 0.04). More lopsided conversations produce more
  divergent perceptions — the two people do not come away with the same read.
- **Positive-tone utterance ratio** predicts IP (*F*(1,54) = 8.55, *p* = 0.005).

From the ICRA 2023 workshop paper, a discourse analysis of the 12 validation
sessions: features of the rating curves map onto identifiable interaction events,
and raters sometimes show **synchronised dips** despite annotating alone — evidence
that a shared reading of the interaction's affective content gets established
during it.

---

## Honest summary

The measurement apparatus is validated and the data is real. The modelling is not
finished:

1. The 15-class formulation should be abandoned, not re-tuned.
2. The binary result needs a clean re-run without `value_p0`/`value_p1`.
3. Nothing generalises across participants — every campaign shows a near-perfect
   train fit and a weak test fit. That is the problem to solve, and 27 sessions is
   probably too few to solve it with this feature set.
4. Study 3 is an untouched dataset of 34 triadic sessions with 15 sessions of
   three-way annotation. Nothing has been modelled on it.

### Explicitly listed as future work in the May 2024 SOW

- Other architectures — Transformers, DNNs
- A different VAD method to lift the sampling rate from 2 Hz toward 30 Hz
- Longer time horizons (e.g. 30 s)
- Late fusion rather than early fusion of modalities and participants
- Different averaging horizons for features
- More PCA / feature-selection work
- Data augmentation and class balancing
- Group-level features (synchrony, resonance) rather than only individual ones
- Speech content via sentiment or agreement markers — noting that the poverty task's
  wording makes raw sentiment unreliable
- Collecting interpersonal perception data in person — which became Study 3
