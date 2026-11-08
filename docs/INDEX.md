# Index of the planning notes (`prep/`)

The notes are numbered in the order they were written (from 2026-11-01), not by importance. They are the planning record, kept as written; later notes correct earlier ones instead of rewriting them. Code comments and the pre-registration cite them as `prep/NN`, so the folder name and the numbers are fixed.
## Which note is current

- **`prep/16_PLAN_V3_FIXES_APPLIED.md` is the current plan.** Where it disagrees with an earlier note, 16 wins. Its section 17 and later (audit fixes and measurements, 2026-11-06) win over every older line, including its own sections 1 to 16, on n per cell, gates, seats, game numbers, cache key and freeze dates.
- **`prep/20_LITERATURE_SYNTHESIS.md` is the current literature view** (re-ranked top 15); it supersedes `prep/19`. `prep/18` is the current collection index.
- **What was actually run** is defined by `prereg/PREREG_v1.md` and the hash manifests, and every later change is in `prereg/DEVIATIONS.md`. Where a planning note and the pre-registration differ, the pre-registration wins.

## Index

| Note | Topic | Status |
|---|---|---|
| `01_WHAT_IS_THIS.md` | What the event and the project are | Background |
| `03_TIMELINE.md` | Rough timeline and what to cut if time shrinks | Stale: gate, date and n=20 lines are void (see 16, section 17) |
| `04_PREREGISTRATION.md` | Draft of what the pre-registration must contain | Stale: superseded by 16 and by `prereg/PREREG_v1.md` |
| `05_FREEZE_THE_PLAN.md` | Freeze checklist and what may change after it | Stale: freeze dates void (see 16) |
| `06_LESSONS_APPLIED.md` | Lessons from an earlier sprint, as actions | Background |
| `08_ADAPTION_CREDITS.md` | Hosted API credits: what was offered and confirmed | Partly stale (see 16) |
| `09_PLAN_V2.md` | Plan v2: one world, three lenses, explore then confirm | Superseded by 16 |
| `10_QUESTIONS_AND_SANDBOX.md` | The questions, ablations, extras and the sandbox | Superseded by 16 |
| `11_ADAPTION_API.md` | Hosted API: models, prices, how to call it safely | Reference; read 2026-11-02, models and limits were re-measured at launch (`bench/`) |
| `12_TABLES_AND_AUDIT.md` | Ablations, extras, twists, audit of lessons | Superseded by 16 |
| `13_HOLM_PROMPTS_LOGGING_MODELS.md` | Holm correction, prompt templates, logging, local model sweep | Partly stale: n and gates void; prompts are frozen in `prereg/` and `engine/prompts.py` |
| `15_CREDITS_ESTIMATE.md` and `15_credits_estimate.py` | Cost estimate for the plan as first written | Partly stale: n void |
| `16_PLAN_V3_FIXES_APPLIED.md` | Plan v3: refinement and audit fixes applied | **Current; wins on conflicts** |
| `17_PHASE_PLAN.md` | Phase-by-phase plan to submission | Partly stale: dates and gates void |
| `18_LITERATURE_COLLECTION.md` | Index of the literature collected (2026-11-04) | Current |
| `19_TOP_PAPERS_PRELIMINARY.md` | Preliminary top 15 papers (abstract level) | Superseded by 20 |
| `20_LITERATURE_SYNTHESIS.md` | Literature synthesis and re-ranked top 15 | **Current** |

## Supersession at a glance

```
03, 04, 05, 13, 15, 17 (stale lines)  ->  16, section 17
09, 10, 12                            ->  16
08                                    ->  16 (partly)
19                                    ->  20
all planning notes                    ->  prereg/PREREG_v1.md and prereg/DEVIATIONS.md for what was run
```
