# Study 3 — triadic, in person

Three strangers sit in a lab room, rank the causes of poverty on their own, then
argue to a group consensus for five minutes. Afterwards each one rates **both** of
the others, one at a time, on the same approach/withdrawal dimension.

This is the in-person, three-party counterpart to
[Study 2](study2-dyadic-online.md). The shorter interaction, the physical
co-presence, and the fact that attention has to be split across two other people
are the three things it was designed to change.

- **Format:** in person, lab room
- **Group size:** 3 (positions **A**, **B**, **C**, marked on the chairs and floor)
- **Interaction length:** 5 minutes (recorded clips run ~299.7 s)
- **Run window:** from late May / June 2024
- **Recruitment:** Calendly booking link, physical posters and flyers, online posts
- **Compensation:** flat US$50 for everyone (the doubling incentive below is a
  manipulation, disclosed at debrief)

## Procedure

1. **Room prep.** Three laptops, lids closed, mid-survey open in an incognito
   browser. Headphones and a pen at each seat; tables aligned with floor marks.
   Consent form and the ranking sheet (ranking only, no instructions) printed and
   on the table. Participant IDs *n*, *n+1*, *n+2* written on sticky notes.
2. **Individual prep — 7 min.** Participants read and sign consent, then complete
   the individual ranking. **No talking.** The researcher leaves the room.
3. **Task briefing.** Participants are told they will discuss the reasons for
   poverty and reach a group consensus, and that whoever's initial ranking is
   closest to the final group ranking gets paid double. The incentive exists to
   discourage instant agreement.
4. **Discussion — 5 min.** Participants move to their labelled chairs, bringing the
   ranking page and a pen. They are asked to stay seated, avoid large movements,
   and not hold the ranking page in front of their face (it occludes the camera).
   The researcher starts the ROS recording remotely over AnyDesk and leaves.
5. **Mid-survey.** Back at the original seats, laptops open, survey completed in
   silence.
6. **Retrospective annotation.** Each participant watches the interaction and rates
   **one person at a time**; when the first video finishes the second starts
   automatically. Same controls as Study 2 (`Space`, `←`/`→`). The briefing
   repeats the Study 2 framing of friendly vs. less friendly behaviour.
7. **Debrief.** The real purpose is explained, the ranking-bonus manipulation is
   disclosed, and everyone is told they will all be paid $50.

## The task

Same **Reasons for Poverty** item list as Study 2, with two changes: the ranking is
done individually *first* on paper, and the group must then converge on a shared
top-5 ranking under a (fictitious) competitive bonus.

## Recording setup

See [`../study3_triadic_inperson/recording/README.md`](../study3_triadic_inperson/recording/README.md).

- **3 × Intel RealSense cameras**, taped `A` / `B` / `C`, mounted on a shared
  central stand so each faces one seat. RGB + depth.
- **1 × ReSpeaker microphone array** at the base of the camera stand, orientation
  marked so the array's direction-of-arrival channels map to known seats. LED ring
  brightness set to 0 so blinking does not distract participants.
- **1 × camcorder** on a tripod capturing the whole scene, HDMI'd to a monitor in
  the adjacent RIG Lab so researchers can observe without being in the room.
- Capture is a ROS pipeline (`record_social_dining` package) writing one `.bag` per
  session, then a post-hoc extraction to `.wav` and `.mp4`.

Frame rate in the exported clips is **15 fps** (≈4496 frames over 5 minutes), half
the 30 fps of Study 2's webcam recordings.

## The annotation tool: CORAE (public release)

Study 3 used the **public release** of CORAE, not the 0.15.0a build from Study 2.
Same dimension and same 15-point −7…+7 scale, but a different export format: one
`participant-<session><position>_annotations.json` per participant plus a
`session-<n>_aggregate.json`, with annotations as a list of
`{timecode, frame_number, annotation_value, trigger}` objects and `trigger` ∈
`start | input | end`. Each participant file contains **two** video entries, one per
person rated. See
[`../data_samples/corae_release_participant_annotations.json`](../data_samples/corae_release_participant_annotations.json).

## Data collected

| Stream | Coverage |
|---|---|
| Session audio (`extracted_audio/*.wav`) | **34 sessions** |
| Whisper transcripts (`*.vtt` → `transcript_dfs/*.csv`) | **34 sessions** |
| OpenFace per-participant CSVs | **34 sessions**, 102 participant streams (+ a few re-runs) |
| CORAE annotations | **15 sessions** → 45 participants → **90 rating curves** (3 raters × 2 ratees) |
| Mid-survey / post-survey responses | collected per protocol — **[NO ACCESS]** on this drive |
| ROS `.bag` files, RGB-D video | **[NO ACCESS]** on this drive — archived to Cornell Box |

So: 34 sessions were **run and recorded**, 15 of them have **retrospective ratings**
on this drive. Treat 15/45/90 as the annotated set and 34/102 as the behavioural set.

### Annotation statistics (the 15 annotated sessions)

- 3460 raw annotation events across 90 curves; mean 38.4 events per curve
  (min 2, max 379).
- Raw value distribution is positively skewed but far less extremely than Study 2:
  `0` is the mode (585), `+1` next (653), and the tails thin out symmetrically
  (−7: 1, +7: 137).
- Resampled to 2 Hz over 300 s → 600 samples per curve. Of the resampled
  first-difference values, 24 734 are 0, 1211 are +1, 1055 are −1 — i.e. raters
  move the slider on about 9 % of samples.

### Face-tracking quality

`results/study3/openface_confidence_per_participant.csv`, 104 rows. Mean OpenFace
confidence 0.91; 95 % of frames above 0.7 on average; no missing frames. Four
streams are badly tracked and should be excluded or re-processed:

| Stream | Mean confidence | Frames > 0.7 |
|---|---|---|
| `9_C` | 0.31 | 30 % |
| `3_A` | 0.33 | 32 % |
| `34_C` | 0.43 | 43 % |
| `24_C` | 0.63 | 65 % |

## Caveats specific to this study

- **Half the annotations are missing from the interpolated file.**
  `study3_json_interp.csv` has 27 000 rows = 45 curves × 600 samples, not 90 × 600.
  The interpolation loop in `preprocessing/process_corae_jsons.ipynb` groups by
  `participant_number` alone, so for each rater only the first of their two ratee
  curves survives. The raw `study3_json.csv` has all 90. **Fix the grouping key to
  `(participant_number, rated_p)` before using the interpolated file.**
- Speaker diarisation (pyannote 3.1) produces `SPEAKER_00/01/02` labels that are
  **not** aligned to the `A/B/C` seat positions. That mapping has to be established
  per session before audio features can be joined to the right person.
- No model-ready feature matrix was ever assembled for Study 3 — the Study 2
  pipeline (`merge_all_feats.ipynb`) was never ported across. Only the per-stream
  OpenFace, audio, transcript and annotation files exist.
