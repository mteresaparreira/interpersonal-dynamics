# Data quality checks

`check_openface.ipynb` walks the OpenFace output directories and, per participant
stream, reports total frames, the fraction tracked above 0.5 and 0.7 confidence,
mean confidence, and missing frames. Output:
[`../../results/study3/openface_confidence_per_participant.csv`](../../results/study3/openface_confidence_per_participant.csv).

104 streams. Mean confidence 0.91; 95 % of frames above 0.7 on average; zero missing
frames anywhere. Four streams are outliers and should be excluded or re-processed:

| Stream | Mean confidence | Frames > 0.7 |
|---|---|---|
| `9_C` | 0.31 | 30 % |
| `3_A` | 0.33 | 32 % |
| `34_C` | 0.43 | 43 % |
| `24_C` | 0.63 | 65 % |

For reference, Study 2 applied a hard **0.7 confidence floor** per frame before
merging, which removed 0–21 % of frames per participant
([`../../results/study2/openface_frames_removed.csv`](../../results/study2/openface_frames_removed.csv)).
Applying the same floor here would discard most of those four streams.
