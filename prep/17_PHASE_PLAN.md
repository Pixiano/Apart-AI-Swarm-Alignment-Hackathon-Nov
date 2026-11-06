> **2026-11-06:** prep/16 section 17 (audit fixes) wins on n per cell, gates, seats, game numbers, cache key and freeze dates; stale gate, date and n=20 lines in this file are void.

# 17. Phase-by-phase plan: from the paper review to submission

Drafted 2026-11-02 (IST). Built on 16 (wins on details). Sprint: Fri 6 Nov 17:29 IST to Mon 9 Nov 17:29 IST (72 h). Headline: Q3 (what peers say), model size a factor. Spend cap $150. Standing rules in every phase: log everything (13 section 3), deviations log with dates, daily summary and disclosure log, no key in any file, one local model server at a time started in your own terminal, quote Windows paths.

## Phase 0: Pre-sprint (Tue Nov 3 to Fri Nov 6 12:00). Theory only, no instrument code
| Step | When | Do | Output | Exit |
|---|---|---|---|---|
| 0a Read | Tue Nov 3 | Find papers; each person reads independently with the shared note template (claim, method, relevance to Q-number, how we differ, opened and read yes/no). Open the METR sources. Adaption premium, monthly usage and rate-limit lookup. | `notes_A`, `notes_B`, source list | At least 15 papers read or the time box ends (stop at diminishing returns) |
| 0b Compare | Wed Nov 4 | Compare notes. Sort every idea: into the plan, into the future-work paragraph, or dropped. Update plan docs. If the key has arrived, run `bench/api_timing.py` once (cap $0.50) and fill real reasoning-token and rate numbers into 15. | Comparison table, plan v4 | Every idea has a decision |
| 0c Freeze | Thu Nov 5 | Final internal pass: hypotheses, margins, prompts (hashed), game spec, definitions, gates, promotion rule, stopping rule. Tag the freeze. Push the plan (needs a `.gitignore` allow-list entry, ask first). Last push of the prior-work repo, then stop committing there. | Tagged freeze, pushed plan | Freeze checklist in 05 ticked |
| 0d Ready | Fri Nov 6 until 12:00 | Wording and citation checks only, no new design. Plan push window 12:00-15:00 if not done Thursday. Prepare the environment: official report template downloaded, disk space, server start commands tested, Adaption key in the environment variable only, rest. | Ready checklist | Nothing new after 15:00 |

## Phase 1: Launch (Fri Nov 6 17:29-18:15)
Start log and day folder. 20-minute benchmark sanity pass on the 2 chosen local models (prior-work script, results saved in the sprint repo as in-sprint). Gate G1: API plumbing (valid actions, no empty replies, 5 parallel calls without 429, latency). Update README status; pre-existing material declared. **Exit:** G1 result recorded; local server confirmed.

## Phase 2: Build the instrument (Fri 18:15-00:30, about 6 h)
Engine (game spec from 16 section 2), file folder with `board.txt` and 3 distractors, five scripted bots with paraphrase pools, action parser and path validation, automated JSONL logger, runner (resume, concurrency 3-5 with backoff, cost cap $150, kill switch), reply cache, monitor harness stub. Unit tests: User beats Ignorer on pool; no "board" in any rendered prompt. **Exit:** one local N=5 episode runs end to end. **Fallback:** cut N=10 and the monitor stub; keep one local model. Sleep 00:30-08:00 (optional local smoke run overnight).

## Phase 3: Validate (Sat Nov 7 08:00-10:30)
G0: tests pass; local N=5 episode under 3 min with 95% valid actions; analysis runs on synthetic data with a planted effect and a planted null. Positive control in every batch. G2 floor/ceiling pilot (8+ episodes per class). **Exit:** G0 and G2 decided and logged. **Fallbacks:** floor -> switch once to P-OPEN; ceiling -> distractors; both fail -> Q5/Q6 only.

## Phase 4: Explore (Sat 10:30-16:00)
Exploration cells at n=6-8 (not counted), labelled exploratory, local and hosted in parallel. Analysis code runs on real pilot data; figure script on real data; monitor harness on scripted logs. **Exit:** exploration table complete; every episode logged.

## Phase 5: Promote and confirm (Sat 16:00-Sun 02:00)
G3 promotion by the written rule (control 100%, effect at least 0.30 absolute, sham within 0.10). Confirmation on fresh seeds: n=20 per cell (n=100 for promoted questions if throughput allows). Q5/Q6 monitor study on the logs. Extras (decoy stub, clean-clone prep) only if ahead of schedule. Overnight local runs. **Exit:** confirmation data complete; spend and call counts logged. Sleep Sun 02:00-08:00.

## Phase 6: Analyse (Sun Nov 8 08:00-10:00)
Holm per confirmed question, intervals, figures, `numbers.md` filled. **G4 data freeze at 10:00:** control passed every batch; empty-reply rate under 5%; no cell under n=15. Rerun only failed batches (logged).

## Phase 7: Write (Sun 10:00-18:00)
Report on the official template (page budget in 14 (f)), main figure and table, Limitations and Dual-Use appendix, future-work paragraph, abstract last (150-250 words with numbers and the failed prediction). **G5 at 15:00:** full draft with every number mapped. **Fallback:** cut stretch material, keep abstract and appendix.

## Phase 8: Verify (Sun 18:00-22:00)
Clean-clone rebuild of the numbers; number-to-source map check; citation check (cite only what was read); repo polish (README, tags, pre-existing declaration); deviations log final.

## Phase 9: Submit (Mon Nov 9 08:00-13:00; deadline 17:29)
Final read, PDF export, repo links, submission form (Vatsal clicks submit). Submit by 13:00; the afternoon is spare. **After:** wrap-up: repo polish at the end (tags, README with workflows and images, contact page, troubleshooting), delete the worktree.

## Budget view
| Phase | Hours | Cumulative |
|---|---|---|
| 1-2 | about 7 | 7 |
| 3-5 | about 18 | 25 |
| 6-8 | about 14 | 39 |
| 9 | about 5 | 44 |
