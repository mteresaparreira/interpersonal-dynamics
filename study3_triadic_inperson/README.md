# Study 3 — triadic, in person: code

Protocol: [`../docs/study3-triadic-inperson.md`](../docs/study3-triadic-inperson.md).

**Status: data collected and partly processed, never modelled.** 34 sessions were
recorded; 15 of them have CORAE annotations (45 participants, 90 rating curves).
No feature matrix equivalent to Study 2's `all_data_05.csv` was ever built.

## Pipeline as it stands

```
ROS .bag  ──►  extract_all_bags_{audio,video}  ──►  1 .wav + 3 .mp4 per session (15 fps)
                                                      │          │
                            Whisper ────► .vtt ◄───────┘          └──► OpenFace 2.2.0
                               │                                            │
                 vtt_to_transcript_dfs.ipynb                     check_openface.ipynb
                               │                                            │
                 diarization_pyannote.ipynb                   openface_confidence_per_participant.csv
                 (SPEAKER_00/01/02 — not yet mapped to seats A/B/C)

CORAE participant-<n><A|B|C>_annotations.json ──► process_corae_jsons.ipynb
                                                     ├─► study3_json.csv       (90 curves, complete)
                                                     └─► study3_json_interp.csv (45 curves ⚠️)
```

## Directories

| Path | What |
|---|---|
| [`recording/`](recording/) | the capture rig and the ROS operating sequence |
| `preprocessing/` | annotation parsing, diarisation, transcript conversion, OpenFace batch driver |
| `quality/` | face-tracking confidence checks |

## Two things to fix before using this data

1. **`process_corae_jsons.ipynb` loses half the annotations.** Its interpolation
   loop groups by `participant_number` alone, so for each rater only the first of
   their two ratee curves survives into `study3_json_interp.csv` (45 × 600 rows
   instead of 90 × 600). Change the grouping key to
   `(participant_number, rated_p)`. The raw export is complete.
2. **Diarisation labels are not mapped to seats.** pyannote emits
   `SPEAKER_00/01/02`; the cameras and the CORAE positions are `A/B/C`. That
   correspondence has to be established per session — most directly from the
   ReSpeaker array's direction-of-arrival channels, whose orientation was physically
   marked during setup — before any audio feature can be attributed to the right
   person.

## Also worth knowing

- Four OpenFace streams track badly (`9_C` 0.31, `3_A` 0.33, `34_C` 0.43,
  `24_C` 0.63 mean confidence) and should be excluded or re-processed. Full table:
  [`../results/study3/openface_confidence_per_participant.csv`](../results/study3/openface_confidence_per_participant.csv).
- Clips are **15 fps**, half Study 2's 30 fps. Any code ported from Study 2 that
  assumes 30 fps when converting frame numbers to seconds will be wrong by 2×.
- The CORAE export format differs from Study 2's — see
  [`../data_samples/`](../data_samples/).
