# Results

Aggregate tables only. The only identifiers are study-internal pseudonyms
(`1011`, `3_A`) that cannot be resolved to a person without the participant log,
which is not in this repository. See [`../docs/privacy.md`](../docs/privacy.md).

Narrative interpretation of all of these: [`../docs/results.md`](../docs/results.md).

## `study2/`

| File | Rows | What |
|---|---|---|
| `idc_classification_sweep.csv` | 2037 | the full 2024 hyperparameter sweep — architecture, dataset tag, sequence length, units, dropout, activation, loss, optimiser, batch, and the eight test metrics. Per-epoch loss/accuracy curves have been dropped to keep the file readable. |
| `idc_classification_fold_metrics.csv` | 8 | 5-fold means ± SD for the all-folds re-runs. The headline table. |
| `rf_feature_importance_sign.csv` | 194 | Random Forest importances for the binary change-direction task, descending. Names are `sN` aliases — resolve via [`../docs/dict_cols_sign.json`](../docs/dict_cols_sign.json). Flat distribution: top 0.0080, bottom 0.0023, uniform would be 0.0044. |
| `ttest_significant_features_sign.csv` | 5 | Welch t-tests, *p* < 0.05, separating the two change directions. One of the five (`s119` = `value_p0`) is a leaked label — see the data dictionary. |
| `ttest_significant_features_multiclass.csv` | 233 | the same test against the 15-class target. Almost everything returns *p* ≈ 0, which reflects 60 808 samples and mirrored sessions more than any effect. |
| `openface_frames_removed.csv` | 54 | fraction of frames dropped per participant by the 0.7 OpenFace confidence floor. Range 0 – 21 %. |

## `study3/`

| File | Rows | What |
|---|---|---|
| `openface_confidence_per_participant.csv` | 104 | per-stream face-tracking quality. No confidence floor was applied to Study 3 data. |
