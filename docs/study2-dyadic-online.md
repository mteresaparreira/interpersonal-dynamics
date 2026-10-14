# Study 2 — dyadic, online

Two strangers with opposing political leanings meet over a video call, argue their
way to a shared ranking of the causes of poverty, and then each privately re-watches
the discussion and rates, moment by moment, how the other person was coming across.

- **Format:** fully remote
- **Group size:** 2
- **Interaction length:** up to 10 minutes (mean 560.0 ± 111.4 s in the first 12 sessions)
- **Session length:** ~45 minutes end to end
- **Run window:** December 2022 – May 2023
- **Recruitment:** Prolific, screened on self-declared political leaning (one
  liberal-leaning, one conservative-leaning), English proficiency, working camera
  and microphone
- **Compensation:** US$14
- **Ethics:** Cornell IRB0143729

## Procedure

1. **Consent.** Signed on Qualtrics before the slot is scheduled. Separate consent
   links for the A and B roles.
2. **Setup.** Both participants join a Zencastr room named `corae-<idA>_<idB>`.
   Zencastr is used rather than Zoom specifically because it records each
   participant's audio and video as **separate streams** — a limitation of Zoom
   identified in the Study 1 pilots that made per-speaker vocal analysis impossible.
   Participants are told their numeric participant ID and asked to memorise it.
3. **Task instructions.** The researcher posts the Reasons for Poverty item list
   into the Zencastr chat, one paragraph at a time, and starts recording.
4. **Discussion.** Participants agree on the 5 most accurate reasons for poverty
   and rank them. They post `FINAL RANKING` in the chat when done. Warnings are
   posted at 5 minutes and 9 minutes; hard stop at 10. Cameras stay on; no other
   apps.
5. **Mid-survey.** Qualtrics: demographics, Big Five, religiousness, political
   leaning, and the interpersonal measures (see below). Microphones muted.
6. **Retrospective annotation.** Each participant opens their own CORAE instance
   (`/pa` for the lower participant ID, `/pb` for the higher) and rates the whole
   discussion continuously. They see **only the other participant's video**, with
   the audio of both. On completion the browser downloads
   `a_results.json` / `b_results.json`, which the participant uploads to a Box
   file-request link.
7. **Exit survey.** Open comments and an opt-in to a future-participant database.

## The task

A modified **Reasons for Poverty** task (Shek 2002). Participants rank the 5 most
"accurate" of 13 statements. Roughly half attribute poverty to *situation*, half to
*disposition*, so people with opposing priors are unlikely to agree instantly.

> Poor people lack the ability to manage money · Poor people waste their money on
> inappropriate items · Poor people do not actively seek to improve their lives ·
> Poor people lack talents and abilities · Poor people are exploited by the rich ·
> Society lacks justice · Distribution of wealth in society is uneven · Poor people
> lack opportunities because they live in poor families · Poor people live in places
> where there are not many opportunities · Poor people have encountered personal
> misfortunes, which limit their opportunities · Poor people are discriminated
> against in society · Poor people have bad fate · Poor people lack luck

The 10-minute cap exists so that the retrospective annotation pass does not become
so long that participants disengage.

## The annotation tool: CORAE 0.15.0a

CORAE (COntinuous Retrospective Affect Evaluation) — <https://corae.org>. Study 2
used build **0.15.0a**.

- Rating dimension: **approach / withdrawal**, not valence. Labelled
  *Disagreeable* ↔ *Agreeable*; participants were briefed that friendlier behaviour
  means a closer emotional connection and less friendly means growing emotional
  disconnection, cold or argumentative but not necessarily hostile.
- Scale: bounded and discretised, **15 points, −7 to +7**.
- Controls: `Space` toggles playback, `←`/`→` move the slider. The slider cannot
  jump — it steps through intermediate values, which enforces continuity.
- Ratings can only change during playback.
- Logging: one sample per second **plus** a sample on every slider change. Video is
  30 fps so resolution is up to 1/30 s.
- Output: a JSON file, keys `"H:M:S:frame"`, values the slider position as a string.
  See [`../data_samples/corae_v015a_participant_results.json`](../data_samples/corae_v015a_participant_results.json).

Observed usage in the 12 validation sessions: click rate 0.42 ± 0.02 s,
1116 ± 222 rating data points per session, mean rating range 8.08 of the 14-point span.

## Measures

### Mid-survey (Qualtrics)

| Block | Items |
|---|---|
| Demographics | age; gender (self-describe option); nationality; race/ethnicity (multi-select, self-describe option); English proficiency; other languages |
| Personality | BFI-10 (Rammstedt & John 2007), 10 items → extraversion, agreeableness, conscientiousness, neuroticism, openness |
| Religiousness | 1 item, 7-point |
| Political leaning | 1 item, 7-point, very liberal → very conservative |
| **Interpersonal Agreeableness (IA)** | "How did the other participant come across?", 7-point, disagreeable → agreeable |
| Relational Communication | 16 items ("The other participant tried to establish good relations", "…created a sense of distance between us", …) |
| Liking scale | 7 items ("I feel that the other participant is a very likeable person", "The other participant and I just 'clicked'", …) |

### Derived from the CORAE ratings

- **Interpersonal Ratings (IR)** — the raw continuous curve.
- **Cumulative ratings** `y_c` — cumulative sum of IR, read as accumulated or
  depleted "emotional capital".
- **Interpersonal Perception (IP)** — slope of a linear regression fitted to `y_c`
  over the whole interaction. A single-number summary of how the perception of the
  other moved. Linear fit quality across the first 24 curves: R² 0.88 ± 0.34.
- **Interpersonal Dynamics Curve (IDC)** — see
  [`data-dictionary.md`](data-dictionary.md#the-idc). The per-participant
  slope-over-a-rolling-horizon curves, averaged point by point across the dyad into
  one session-level trace.

### Behavioural / conversational

Extracted from Voice Activity Detection at 2 Hz: per-participant speaking state,
cumulative speaking time, number of turns holding the floor, plus session-level
**conversational imbalance** `Σ|sᵢ − s̄|` over relative speaking times.

### Speech content

Whisper transcription, then per-utterance sentiment (neutral / positive / negative).
Only the **positive-tone ratio** was used, because the task prompts themselves are
negatively worded and skew a raw negative count. Agreement-word counts were also
extracted.

## Participants

| Analysis | N sessions | N participants |
|---|---|---|
| ACII 2023 / ICRA workshop validation | 12 | 24 |
| ROMAN 2023 LBR, Q1 report, all later modelling | 27 of 30 run (3 dropped to hardware/connection faults) | 54 |

For the 54-participant set: age 20–87 (M = 42.33, SD = 15.78); 28 female, 25 male,
1 non-binary; race/ethnicity mostly Caucasian/White (41), then Asian/Asian American
(5), Hispanic/Latino (5), African/African American/Black (3), Middle Eastern/North
African (1), American Indian (1), multi-select; 49 native English speakers, 5
proficient. 3663 transcribed utterances.

The `ParticipantLog.xlsx` on the lab drive has 137 rows (126 main study, 11 pilot);
`USE?` ∈ {Y, M} selects the 54 that reach the model-ready dataset, and
`USE4platform?` ∈ {Y, M} selects 58 usable for tool-validation analyses.

## Known limitations

- Sample skews heavily to native English speakers in the United States.
- Retrospective rather than simultaneous annotation: ratings may be coloured by what
  happened later in the interaction. The trade-off was deliberate — simultaneous
  rating imposes a meta-affective load that distorts the social behaviour being
  measured.
- Standard annotation threats apply: anchoring, framing, recency.
- Two participants hit playback failures caused by unreliable network connections to
  the CORAE web server; their data was still usable.
