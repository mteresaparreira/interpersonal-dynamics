# IDC classification (2024)

The regression framing plateaued, so the target was discretised. Keras/TensorFlow;
single recurrent layer → dropout → dense softmax.

## Four datasets

| Tag | Source file | Target |
|---|---|---|
| `IDC15` | `all_data_05.csv` | 15-class absolute rating, −7…+7 |
| `IDC15_n` | `all_data_05_norm.csv` | same, standardised features |
| `IDC2` | `all_data_05_sign.csv` | binary change direction |
| `IDC2_n` | `all_data_05_norm_sign.csv` | same, standardised features |

## Script naming

`{arch}_05[_s][_n|_norm][_all{1,2}].py` — `_s` = sign/binary target, `_n`/`_norm` =
standardised features, `_all{1,2}` = the all-folds re-runs that produced
[`idc_classification_fold_metrics.csv`](../../../results/study2/idc_classification_fold_metrics.csv).
Each `.py` has a matching `.sub` SLURM job spec.

| Path | What |
|---|---|
| `lstm/`, `gru/`, `bilstm/` | the grid-search drivers, one per architecture × dataset |
| `best_models/` | the single winning configuration per dataset, extracted for re-training |
| `createDataSplits_idc.py` | 5-fold splitter (36 train / 6 val / 12 test session keys), sequence builder, one-hot target encoding |
| `get_metrics.py` | macro accuracy/precision/recall/F1 plus **tolerant** variants — a prediction counts if it matches any true label within ±`tolerance` timesteps *in the same session* |
| `collect_results.ipynb` | regex-parses the `results.txt` files from every run directory into one table, then reloads winning checkpoints to re-predict |

## Swept

sequence length {5,10,15} · units {32,64,128,256} · dropout {0,0.2,0.6} ·
activation {softmax, sigmoid, relu} · optimiser {Adam, SGD, Adadelta} ·
batch {512,1024} · lr 1e-3 · 200 epochs · categorical cross-entropy.
2037 runs total — see
[`idc_classification_sweep.csv`](../../../results/study2/idc_classification_sweep.csv).

> ⚠️ `createDataSplits_idc.py` uses `features = df.iloc[:, 5:]`, which in the **sign**
> datasets includes `s119 = value_p0` and `s120 = value_p1` — the absolute rating
> level, which at the scale ceiling partly determines the direction of the next
> change. The binary accuracies are an upper bound. See
> [`../../../docs/data-dictionary.md`](../../../docs/data-dictionary.md#label-leakage-into-the-change-direction-task).

Results: [`../../../docs/results.md`](../../../docs/results.md#2-idc-classification-2024--modelsidc_classification).
