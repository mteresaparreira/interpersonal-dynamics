# Study 2 — dyadic, online: code

Protocol: [`../docs/study2-dyadic-online.md`](../docs/study2-dyadic-online.md).
This is the only study with a complete feature pipeline and trained models.

## Pipeline

```
per-participant .mp4 / .mp3        CORAE a_results.json / b_results.json
        │                                   │
        ├─ OpenFace 2.2.0  ──► 49 feats     ├─ process_corae_jsons.ipynb
        │                                   │     ├─ resample 10 Hz / 2 Hz
        ├─ opensmile_extract ─► 65 feats    │     ├─ cumulative sum  y_c
        │                                   │     ├─ IP  = slope over whole session
        └─ VAD logs ───────► 3 feats + imbalance   └─ IDC = rolling slope, averaged over the dyad
                        │                   │
                        └────► merge_all_feats.ipynb ◄────┘
                                     │
                       ┌─────────────┼─────────────┐
                 all_data_05*    all_data_05*_sign   all_data_l{l}t{h}
                  (15-class)        (binary)          (IDC, continuous)
                       │                 │                    │
            models/idc_classification    │        models/idc_regression
            models/rating_classification ┘
```

## Directories

| Path | What |
|---|---|
| `feature_extraction/` | openSMILE and Whisper-sentiment extraction, plus a later unfinished pivot to learned representations (frames, mel-spectrograms, ViT embeddings) |
| `preprocessing/` | CORAE JSON → rating curves → IP/IDC; the full feature merge; per-feature statistics; figures |
| `models/idc_regression/` | 2023: eight architectures regressing the continuous IDC, CCC as loss and metric |
| `models/idc_classification/` | 2024: LSTM / BiLSTM / GRU over four discretised datasets |
| `models/rating_classification/` | 2025: Random Forest, RNNs with fusion sweeps, MiniRocket |

Results for all three campaigns: [`../docs/results.md`](../docs/results.md).
