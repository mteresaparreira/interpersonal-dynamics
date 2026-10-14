# Preprocessing

Run in this order. All notebooks have had their outputs stripped and expect the
data layout described in [`../../docs/data-inventory.md`](../../docs/data-inventory.md).

| Order | Notebook | What it does |
|---|---|---|
| 1 | `process_corae_jsons.ipynb` | Parses CORAE 0.15.0a JSONs (`"H:M:S:frame": "rating"`) into a long dataframe; measures click rate, rating range and per-participant spread; **resamples to 10 Hz and 2 Hz**; computes cumulative sums and the **IP** slope per rater; joins the Qualtrics mid-survey (demographics, BFI-10, relational communication, liking scale); and computes per-session rater **disagreement** (MSE, Pearson *r*, mean absolute difference, Cohen's κ) against personality and survey differences. |
| 2 | `merge_all_feats.ipynb` | The core pipeline. Selects usable participants from `ParticipantLog.xlsx` (`USE?` ∈ {Y, M}); drops OpenFace frames below **0.7 confidence**; aligns OpenFace, openSMILE and VAD onto a common 2 Hz grid; derives turn counts, talking time and conversational **imbalance** from the VAD logs; joins the resampled ratings as groundtruth; concatenates all sessions; drops ±inf and NaN rows; writes `all_data_05*.csv`; fits and pickles a `StandardScaler`; and runs **PCA** at 90 % explained variance. It also builds the `sN` alias map saved as `dict_cols*.json`. |
| 3 | `feature_stats_analysis.ipynb` | Shapiro–Wilk normality per feature (overall and per participant); Welch t-tests separating the two change directions; ANOVA + Tukey HSD and Kruskal–Wallis + Dunn for the 15-class target. Outputs `sign_features_*.csv`, mirrored in [`../../results/study2/`](../../results/study2/). |
| — | `idc_plots.ipynb` | Figures: IDC construction, rating-curve examples, label distributions, model predictions vs. groundtruth on the held-out fold, survey correlation heatmaps. Styled for LaTeX via `tikzplotlib`. |

> ⚠️ Cell ordering in `merge_all_feats.ipynb` is not linear — several cells are
> "check" variants of the cell above them, and the PCA cells at the end drop the
> mirrored `_1` half of each session. See
> [`../../docs/data-dictionary.md`](../../docs/data-dictionary.md#4-dataset-files).
