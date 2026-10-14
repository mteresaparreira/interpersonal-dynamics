# Rating classification (2025)

Three model families on the same two targets, all swept through Weights & Biases.
Mirrors [`mteresaparreira/interpersonal-affect`](https://github.com/mteresaparreira/interpersonal-affect).

| Path | Model | Notable |
|---|---|---|
| `rf/rf_full_model.py` | RandomForestClassifier | SMOTE balancing; modality ablation over {audio, face, talk}; feature-set tag {Full, Stat, RF}; emits per-fold feature importances → [`rf_feature_importance_sign.csv`](../../../results/study2/rf_feature_importance_sign.csv) |
| `rnn/gru_full_model.py`, `rnn/lstm_full_model.py` | GRU / LSTM (Keras) | the largest sweep space in the repo: **fusion strategy** {early, intermediate, late} applied both across modalities *and* across participants (`part_fusion`), bidirectionality, 1–3 layers, 64/128/256 units, 4 optimisers, sequence lengths {2,5,10,30,60} |
| `minirocket/all_models.py` | MINIROCKET via `tsai` | interval-based time-series classification; `TimeSeries_Helpers.py` holds the interval/context/stride construction, PCA, over- and under-sampling, and a baseline comparison metric |
| `create_data_splits.py` | — | 70/20/10 split by session, 5 rolling folds. `create_data_splits_feats` additionally filters to a statistics-selected feature list |
| `get_metrics.py` | — | same tolerant-metric implementation as the 2024 campaign |

**Modality selection** happens before the splitter: `modalities_combination_data_prep`
rebuilds the frame from `df.iloc[:, :3]` plus explicit column slices, so the rating
columns never reach the model — this path is **not** affected by the leakage that
affects the 2024 campaign.

> ⚠️ The modality slices are hardcoded `iloc` ranges plus the literals
> `s1, s4, s5, s122, s123`, written against the **absolute-rating** column layout.
> Run against the sign dataset the "talk" modality silently substitutes
> `gaze_0_x_p0` for `total_talking_time_p0`, and every slice is off by one at the
> end of its block. See
> [`../../../docs/data-dictionary.md`](../../../docs/data-dictionary.md#the-sn-trap).

No consolidated fold metrics were saved for this campaign; what exists is the
feature-importance and significance output in
[`../../../results/study2/`](../../../results/study2/).
