# Data format samples

Every file here is a **synthetic or structural example**, written by hand to show the
shape of each file type. None of it is real participant data. Real data lives on
Cornell Box (see [`../docs/data-inventory.md`](../docs/data-inventory.md)).

| File | Shows |
|---|---|
| `corae_v015a_participant_results.json` | Study 2 CORAE export (build 0.15.0a) |
| `corae_release_participant_annotations.json` | Study 3 CORAE export (public release) |
| `study3_json.csv` | Study 3 annotations flattened to long form |
| `study3_json_interp.csv` | Study 3 annotations resampled to 2 Hz |
| `transcript_df.csv` | Whisper VTT converted to a dataframe (speech text removed) |
| `all_data_05.csv` | Study 2 model-ready feature matrix (237 features, columns elided) |

Column meanings for `all_data_05.csv` are in [`../docs/dict_cols.json`](../docs/dict_cols.json)
and [`../docs/data-dictionary.md`](../docs/data-dictionary.md).
