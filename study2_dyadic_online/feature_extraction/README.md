# Feature extraction

Two generations of approach, in chronological order.

## Hand-crafted features — what the models actually used

| File | What it does |
|---|---|
| `opensmile_extract.ipynb` | Walks the session folders, converts each participant `.mp3` to a format openSMILE accepts, and runs the **ComParE_2016** low-level-descriptor set → 65 features per participant per frame. |
| `transcript_sentiment.ipynb` | Parses Whisper `.vtt` output into per-utterance dataframes and labels each utterance positive / negative / neutral via the OpenAI completions API, batched ~60 lines at a time. Only the **positive-tone ratio** was used downstream — the poverty-task wording makes raw negative counts meaningless. |

Facial features come from **OpenFace 2.2.0** run as an external binary; see
`../../study3_triadic_inperson/preprocessing/openface_run_all_vids.ps1` for the
batch driver (the same approach was used for both studies). Voice Activity
Detection was produced by the lab's own logging during the sessions — the logs are
on the drive, the logger is not in this repository.

> The API key in `transcript_sentiment.ipynb` has been replaced with
> `REDACTED_OPENAI_API_KEY`. The original on the lab drive is live and should be
> revoked — see [`../../docs/privacy.md`](../../docs/privacy.md).

## Learned representations — started, never evaluated

A 2025 pivot away from hand-crafted features. No results from this path exist.

| File | What it does |
|---|---|
| `video_frames.py` | ffmpeg → JPEG frames at a fixed 30 fps, one directory per video |
| `audio_melspectrograms.py` | 48 kHz audio → one 128×128 mel-spectrogram **per video frame**, so audio and video are index-aligned; saved as `.npy` |
| `vit_feats.py` | ViT-B/16 (ImageNet-1k weights), CLS token from the final encoder block per frame, written to HDF5 |
