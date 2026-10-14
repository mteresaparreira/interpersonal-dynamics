# Preprocessing

| File | What it does |
|---|---|
| `process_corae_jsons.ipynb` | Walks `json/<session>/`, parses each `participant-*_annotations.json` (skipping the `*_aggregate.json`), and flattens the nested `videos[].annotations[]` structure into one long dataframe keyed by rater **and** ratee (`rater_rated` ∈ {A_B, A_C, B_A, B_C, C_A, C_B}) → `study3_json.csv`. Plots all three raters per session on shared axes. Then resamples each curve to 2 Hz over the 300 s session and computes first differences and their sign → `study3_json_interp.csv`. ⚠️ **the resampling step drops half the curves** — see [`../README.md`](../README.md). |
| `vtt_to_transcript_dfs.ipynb` | Converts Whisper `.vtt` subtitle files into `start, end, speaker, text` dataframes, one CSV per session. |
| `diarization_pyannote.ipynb` | `pyannote/speaker-diarization-3.1` over the session `.wav`, producing speaker turns. Labels are `SPEAKER_00/01/02` and are **not** aligned to seats A/B/C. |
| `openface_run_all_vids.ps1` | PowerShell driver that walks a directory tree of `.mp4` files and runs OpenFace `FeatureExtraction.exe` on each, mirroring the input structure under `.\processed`. The OpenFace 2.2.0 Windows binaries themselves are vendored on the lab drive, not here. |

> The Hugging Face token in `diarization_pyannote.ipynb` has been replaced with
> `REDACTED_HF_TOKEN`. The original on the lab drive is live and should be revoked —
> see [`../../docs/privacy.md`](../../docs/privacy.md).
