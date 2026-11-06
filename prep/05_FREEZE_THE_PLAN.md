> **2026-11-02 update:** the refinement fixes are applied in [16_PLAN_V3_FIXES_APPLIED.md](16_PLAN_V3_FIXES_APPLIED.md); where it disagrees with this file, 16 wins. Key changes: sprint starts Fri 6 Nov 17:29 IST (72 h to Mon 17:29 IST), engine built Nov 6 only, preregistration written and tagged Friday before any run, rule (d) withdrawn, new schedule and gates.

# 5. Freezing the plan

Freeze = the plan is committed and tagged **before the first confirmatory model call**. Target: Thu Nov 5.

## Freeze checklist (all must be true)
- [ ] 04 skeleton is complete, no [brackets] left.
- [ ] Question is one sentence; the distinctive (mechanism) arm is inside the plan. Last time it was added after the freeze.
- [ ] Predictions written, including one expected to fail; margin and rule for a null fixed.
- [ ] Analysis code committed and run on synthetic data with a planted effect and a planted null.
- [ ] Scripted bots pass their own unit test (positive and negative control behave as designed).
- [ ] Measured time per round recorded; total calls and frontier spend fit the budget.
- [ ] Prompts, model versions, temperature, seeds, gate and fallback written.
- [ ] Pre-existing code listed (what is reused, from where).
- [ ] Sprint page re-read for rule changes the same day.

## What may change after the freeze
Allowed: writing, figures, captions, exploratory analyses (labelled exploratory), bug fixes that change no prompt, configuration value, margin or threshold (log them).
Not allowed without a logged deviation: prompts, model set, margins, thresholds, predictions, primary outcome, seed rule, analysis code for the headline.
Every deviation: dated row with what, why, and "touched prompt/config/margin/threshold: yes/no". Report it; do not hide it.

## How to freeze (local only)
Run only when you say go; no push without your command.
1. Commit the plan and analysis code on `main` (no branches, no Claude trailer, authored by you).
2. Tag: `git tag prereg-v1`.
3. Record the commit hash in the plan header and in the report's prior-work note.
Publishing the tag needs a push; that happens later and only on your command, so a public timestamp does not exist until then. If a public timestamp matters, say so and push the tag the evening of Nov 5.

## Stop rules during the sprint
- Positive control fails: stop, fix the bot (that is plumbing, log it), rerun the control only.
- Gate fails after one logged prompt change: switch to the fallback, do not keep tuning.
- Frontier spend reaches the cap: stop frontier runs, report what exists.

## Extra freeze checklist (added 2026-11-02, from the audit in 12)
- [ ] A margin for each of Q1-Q7 (04, section 6)
- [ ] Holm correction written into the analysis code and tested on fake data
- [ ] Manipulation-check test exists and passes for every arm
- [ ] Prompt templates frozen with hashes (13, section 2)
- [ ] Logging spec implemented and a dry run produces every field (13, section 3)
- [ ] Reply cache works: a rerun makes zero API calls
- [ ] Local model(s) chosen by the selection rule; hosted roster by rule (13, sections 4 and 6)
- [ ] n per cell fixed (20 hosted, 10 local) and the cost estimate checked against the real prices
- [ ] Every arm and ablation listed; the promotion rule written
- [ ] Overnight runbook read (13, section 7)
- [ ] Friday Nov 6 starts with the benchmark re-run (03, "Friday re-run"); bench code is in the prior-work repo, results are re-generated in the sprint repo
