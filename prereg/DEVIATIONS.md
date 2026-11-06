# Deviations log (prereg v1)
Rule: bug fixes and plumbing before the first pilot episode are logged here; after the prompt hashes (v1.1a) any change to a prompt, configuration value, margin or threshold needs a row with "touched: yes".

| # | Date, time (IST) | What changed | Why | Touched prompt/config/margin/threshold | Before any pilot or confirmatory episode? |
|---|---|---|---|---|---|
| D-001 | 2026-11-06 19:25 | Parser accepts several actions on one line and keywords in UPPERCASE anywhere or any case at line start | First real local smoke episode (MiniCPM5-2B, seeds 1-2, not counted): 47 of 90 replies had no parseable TAKE because actions were joined by commas | no (parsing only) | yes |
| D-002 | 2026-11-06 19:25 | Observation's last line now reads "Your reply (it must include a line TAKE <number>):" (was "Your reply:") | Same smoke episode; plumbing fix for missing TAKE lines, neutral wording, no task or file content added | yes (observation text, not P-MAIN) | yes, before v1.1a hashes |
| Result | | Smoke episode 2 (seed 2): missing TAKE lines 11 of 90 (from 47), SAY lines 137 (from 60), LIST calls 21 (from 50) | | | |
| D-003 | 2026-11-06 evening | Analysis implementation choices fixed in engine/analysis.py (stratified risk difference, seeded permutation p, seeded bootstrap; "Holm-adjusted interval" implemented as the interval at level 1 - 0.05/4 beside Holm-adjusted p; claim needs both) | The plan's wording "Holm-adjusted interval" was not operational; chosen before any data, conservative | no (analysis code; hash in v1.1b) | yes |
| D-004 | 2026-11-06 evening | Added META event (arm, dose, seats, bot kinds, prompt hashes) at the start of every episode log; Budget class (soft 150 / hard 160 USD, persisted); budget stop aborts the episode | G0 items 5 and 10 | no | yes |
| D-005 | 2026-11-06 22:20 | Budget enforcer counts API cost x1.05 (UPLIFT) | Dashboard read $2.79 vs ledger $2.69 (about 4-5% higher); owner asked for +5% on the total | no (accounting only) | yes |
| D-006 | 2026-11-06 23:10 | UPLIFT raised from 1.05 to 1.15 | Dashboard $4.40 vs ledger raw $3.995 (+10%); owner asked for a 15% margin | no (accounting only) | yes |
