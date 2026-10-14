# Data inventory

What exists, how much of it, and where. **None of it is in this repository** — see
[`privacy.md`](privacy.md). This page is the map so you can find a file without
re-deriving the folder archaeology.

Paths are relative to the project working drive (`.../cornell/2025_honda/`).
`[NO ACCESS]` means the artefact is referenced by the protocol, the papers, or the
code but is not present on that drive.

---

## Study 2 — dyadic, online

### Raw

| Artefact | Count | Location |
|---|---|---|
| Per-participant video (`.mp4`) + audio (`.mp3`) | 2 per session | `2023_honda/2023_study2_data/study_data/Study Sessions/<sessionID>/` (30 sessions) and `Pilot Sessions/` (5) |
| Merged session audio (`.mp3`) | 27 | `2023_honda/2023_study2_data/audio_files/` |
| Merged session audio, WAV for openSMILE | 27 | `.../audio_files_wav/` |
| Cleaned/used subset | 27 sessions, 54 JSONs | `.../study_data_clean/` |
| CORAE annotation JSONs | 67 raw / 54 used | `.../study_data/ParticipantsJSON/`, `2024_code/data/ParticipantsJSON/` |
| Mid-survey (Qualtrics) | 79 responses | `.../survey_data/midq.csv` — **PII: IP address, geolocation, recipient name/email** |
| Exit survey (Qualtrics) | 24 responses | `.../survey_data/RRA_FinalForm_March+31,+2023_08.45.csv` — **same PII columns** |
| Participant log | 137 rows | `.../ParticipantLog.xlsx` — **PII: Prolific IDs** |
| Session videos as hosted for annotation | — | Cornell Box, `[NO ACCESS]` locally |

A near-complete duplicate of the raw tree also sits in `2025_data/Study Sessions/`
(29 sessions) and inside two very large zip archives (`2023_honda.zip`,
`.fr-y5Py3k/2023_honda.zip`). Prefer `2023_honda/2023_study2_data/` as the source
of truth.

### Intermediate features

| Artefact | Count | Location |
|---|---|---|
| OpenFace per-participant CSVs | 54 | `2024_code/data/openface/features_extracted/<participantID>/` |
| openSMILE ComParE_2016 CSVs | 54 (~42 k rows each) | `2024_code/data/opensmile_feats/<session>_<participant>.csv` |
| VAD logs (raw, `_vad`, `_vad_full`) | 27 sessions | `2024_code/data/vad_logs/<session>/` |
| Merged per-session features | 27 | `2024_code/data/merged_feats/<session>_merged.csv` (237 cols) |
| …plus VAD-derived turn features | 27 | `.../merged_feats_vad/` |
| …plus groundtruth joined | 27 | `.../merged_feats_gt5/` |
| Interpolated ratings, 10 Hz | — | `df_interpolated1dec.{csv,pkl}` (several copies) |
| Interpolated ratings, 2 Hz | — | `df_interpolated5dec.{csv,pkl}` |

### Model-ready

| Artefact | Location |
|---|---|
| `all_data_05*.csv` family (absolute rating / sign, raw / normalised / PCA) | `2025_data/` and `2024_code/data/training/` |
| `all_data_l{2.5,5,7.5}t{2.5,5}_norm[_pca].csv` — 12 IDC-regression datasets | `training_22aug/` |
| `scaler.pkl`, `scaler_sign.pkl` | `2025_data/data/` |
| `dict_cols.json`, `dict_cols_sign.json` | `2025_data/data/` — **copied into this repo** under `docs/` |

### Trained artefacts

| Artefact | Location |
|---|---|
| ~1000 GRU checkpoints from the IDC regression sweep (`model_*.pth`) | `training_22aug/best_model*/` |
| Per-run training logs | `training_22aug/logs/results_{gru,lstm,blstm}_*.txt` |
| 2024 classification run dirs (`model_data/`, `results.txt`) | `2024_training/{gru,lstm,bilstm}/results/`, `2024_training/results_allfolds/` |
| Best-model dirs for IDC2, IDC2_n, IDC15, IDC15_n | `2024_training/best_model_performances/` |
| W&B run data | `2024_code_cluster_jun1/2024_idc/code/*/wandb/` |
| Held-out predictions used for the final figure | `training_22aug/final_plot/{x_test,y_test,y_testpred}.csv` |

---

## Study 3 — triadic, in person

| Artefact | Count | Location |
|---|---|---|
| Session audio (`.wav`) | **34** | `2024_study3_data/extracted_audio/` |
| Whisper transcripts (`.vtt`) | **34** | `2024_study3_data/extracted_audio_transcripts/` |
| Transcripts as dataframes (start, end, speaker, text) | **34** | `2024_study3_data/transcript_dfs/` |
| OpenFace per-participant CSVs (714 cols) | **34 sessions / 102 streams** | `2024_study3_data/openface/<session>_<A\|B\|C>.csv` |
| CORAE annotation JSONs | **15 sessions × 3 participants** + aggregates | `2024_study3_data/json/<session>/` |
| Flattened annotations (long form) | 3460 rows, 90 curves | `2024_study3_code/study3_json.csv` |
| Resampled annotations, 2 Hz | 27 000 rows, **45 of 90 curves** ⚠️ | `2024_study3_code/study3_json_interp.csv` |
| OpenFace confidence QC | 104 rows | `2024_study3_code/openface_predictions.csv` — **copied into this repo** |
| Room / rig photographs | 5 | `2024_reports/photos_data_study/` — no people visible, but kept out of the repo by policy |
| Per-participant RGB-D video | — | `[NO ACCESS]` — on Cornell Box |
| ROS `.bag` files | — | `[NO ACCESS]` — on Cornell Box |
| ReSpeaker multi-channel audio | — | `[NO ACCESS]` — inside the bag files |
| Mid-survey and post-survey responses | — | `[NO ACCESS]` — collected per protocol, not on this drive |
| Individual paper rankings, consent forms | — | `[NO ACCESS]` — physical folder |
| Participant log / demographics | — | `[NO ACCESS]` — no Study 3 equivalent of `ParticipantLog.xlsx` found |
| `record_social_dining` ROS package | — | `[NO ACCESS]` — on the lab recording machine |
| Model-ready feature matrix | — | **never built** |

The four zip archives in `2024_study3_data/` (`download.zip`, `download2.zip`,
`selected.zip`, `mybox-selected.zip`) are Box bulk downloads. The first three are
identical in size (751 776 562 bytes) but differ in content; `mybox-selected.zip`
is 182 MB. `openface.zip` is a 30-byte empty archive.

---

## Study 1 — dyadic, Zoom (predecessor, no CORAE data)

Reported in the Q2 2022 progress report. 20 participants, 10 dyads, ~25-minute
case-study discussions over Zoom with a Wizard-of-Oz "Cornell Recorder" account in
the breakout room. 4 sessions were manually annotated in Label Studio with a custom
label set derived from the Cardiff Conversation Database, covering backchannels and
turn-taking. **[NO ACCESS]** — none of this data is on the working drive; it is
hosted on Cornell Box. It matters mainly because its findings shaped Study 2: Zoom
was dropped for Zencastr (no separate per-speaker audio), participants were
switched to strangers (social-desirability bias), and explicit
keep-your-face-in-frame instructions were added.

---

## Orphans and dead ends on the drive

Worth knowing about so nobody re-opens them expecting something:

| Path | What it is |
|---|---|
| `2024_code_cluster_jun20/2024_honda_study3/` | empty `code/` and `data/` directories |
| `2024_study3_code/OpenFace_2.2.0_win_x64/` | a full vendored OpenFace 2.2.0 Windows binary distribution; only `run_all_vids.ps1` is ours (copied into this repo) |
| `2023_honda/gym_folders/teresa_affect/erc/` | a clone of a third-party emotion-recognition-in-conversation repo (MELD/IEMOCAP text models), evaluated and not adopted |
| `2024_code/data/users.csv` | a Google Workspace user export unrelated to the study — **contains a real name and email addresses** |
| `2023_honda.zip`, `.fr-y5Py3k/2023_honda.zip` | 79 GB and 61 GB archives of the 2023 tree |
| `Cornell-HRI 2nd Amendment Executed (1)-1.pdf` | the sponsored-research contract amendment |
