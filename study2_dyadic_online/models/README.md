# Models

Three campaigns, in order. Full results and baselines:
[`../../docs/results.md`](../../docs/results.md).

| Directory | Year | Target | Framework | Outcome |
|---|---|---|---|---|
| [`idc_regression/`](idc_regression/) | 2023 | IDC, continuous | sklearn + PyTorch | GRU, test CCC 0.226 — learnable, does not generalise |
| [`idc_classification/`](idc_classification/) | 2024 | 15-class rating; binary change direction | Keras | 15-class below the majority baseline; binary 0.609 vs 0.535 baseline |
| [`rating_classification/`](rating_classification/) | 2025 | both | sklearn + Keras + tsai | flat feature importances; 4 features significant at *p* < 0.05 |

Shared conventions across all three: 5-fold cross-validation grouped by session,
seed 42, Weights & Biases for sweeps, SLURM `.sub` files for cluster submission.
