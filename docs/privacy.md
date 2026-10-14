# Privacy and what must never be committed

Both studies were run under Cornell IRB approval (Study 2: **IRB0143729**). The
working data on the lab drive is **not anonymised**. This repository is code and
documentation only. Treat every rule below as hard.

## Never commit

| Category | Examples on the lab drive |
|---|---|
| Direct identifiers | `data/users.csv` (names, email addresses, recovery emails) |
| Prolific IDs | `ParticipantLog.xlsx` → `prolific_id`, sheet `Prolific_Schedule_Match` |
| Qualtrics exports | `survey_data/midq.csv`, `RRA_FinalForm_*.csv` — these carry `IPAddress`, `LocationLatitude`, `LocationLongitude`, `RecipientFirstName/LastName/Email` columns |
| Any audio or video | `*.mp4`, `*.mp3`, `*.wav`, ROS `*.bag`, extracted frames |
| Transcripts | `extracted_audio_transcripts/*.vtt`, `transcript_dfs/*.csv` — verbatim speech is identifying and the discussion topic is politically sensitive |
| Photographs of sessions | anything under `photos_data_study/` showing people |
| Consent forms and ranking sheets | held physically; scans must not be digitised into the repo |
| Credentials | the study protocol document contains shared account logins; notebooks on the drive contained a live OpenAI API key and a Hugging Face token |

### Credentials found during this audit — rotate them

Two notebooks carried live secrets. The copies in this repository have them
replaced with `REDACTED_OPENAI_API_KEY` / `REDACTED_HF_TOKEN`, but **the originals
on the lab drive still contain the real values and they should be treated as
compromised and revoked**:

- `2023_honda/gym_folders/teresa_affect/Tone_analysis.ipynb` → OpenAI API key
  (plus the `.ipynb_checkpoints/` copy)
- `2024_study3_code/Audio Diarization (Pyannote)/pyannote (1).ipynb` → Hugging Face
  `use_auth_token` (plus `pyannote.ipynb`)
- **every `*.sub` SLURM job script** → a Weights & Biases API key, exported in
  plaintext as `export WANDB_API_KEY=...`. 22 files on the drive carry it. The
  copies here read it from the environment instead.

The protocol document (`context_papers/protocol.docx`) also contains plaintext
passwords for shared lab accounts (Calendly, Zencastr, the CORAE host). Those are
paraphrased out of [`study3-triadic-inperson.md`](study3-triadic-inperson.md) and
should be rotated too.

## What *is* in this repository, and why it is safe

- **Code**, with all notebook outputs stripped. Notebook outputs on the drive
  embed rendered rating plots and printed dataframes, so they are removed on the
  way in rather than reviewed case by case.
- **Aggregate result tables** under `results/`. These contain model metrics,
  feature-importance scores, and per-stream data-quality numbers. The only
  identifiers are study-internal pseudonyms (`1011`, `3_A`) that cannot be
  resolved to a person without `ParticipantLog.xlsx`, which stays off the repo.
- **Synthetic format samples** under `data_samples/`, hand-written to show file
  shapes. No real values.
- **Feature dictionaries** `docs/dict_cols*.json` — column-name maps, no data.

## Before you push

```bash
git diff --cached --name-only            # know exactly what you are adding
grep -rIn -E "sk-[A-Za-z0-9]{20,}|hf_[A-Za-z0-9]{20,}" .
grep -rInE "export [A-Z_]*(KEY|TOKEN|SECRET)=" .          # job scripts leak these
grep -rInE "[=:] *['\"]?[A-Fa-f0-9]{32,}" .               # bare hex credentials
grep -rIln -E "prolific|Prolific" --include='*.csv' --include='*.json' .
jupyter nbconvert --clear-output --inplace <notebook>   # if you touched a notebook
```

`.gitignore` blocks the obvious file types, but it is a safety net, not a review.
