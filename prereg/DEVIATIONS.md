# Deviations log (prereg v1)
Rule: bug fixes and plumbing before the first pilot episode are logged here; after the prompt hashes (v1.1a) any change to a prompt, configuration value, margin or threshold needs a row with "touched: yes".

| # | Date, time (IST) | What changed | Why | Touched prompt/config/margin/threshold | Before any pilot or confirmatory episode? |
|---|---|---|---|---|---|
| D-001 | 2026-11-06 19:25 | Parser accepts several actions on one line and keywords in UPPERCASE anywhere or any case at line start | First real local smoke episode (MiniCPM5-2B, seeds 1-2, not counted): 47 of 90 replies had no parseable TAKE because actions were joined by commas | no (parsing only) | yes |
| D-002 | 2026-11-06 19:25 | Observation's last line now reads "Your reply (it must include a line TAKE <number>):" (was "Your reply:") | Same smoke episode; plumbing fix for missing TAKE lines, neutral wording, no task or file content added | yes (observation text, not P-MAIN) | yes, before v1.1a hashes |
| Result | | Smoke episode 2 (seed 2): missing TAKE lines 11 of 90 (from 47), SAY lines 137 (from 60), LIST calls 21 (from 50) | | | |
