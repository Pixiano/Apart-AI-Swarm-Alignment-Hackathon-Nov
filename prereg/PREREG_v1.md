# Frozen plan: what peers say and an unannounced shared file   status: DRAFT (tag prereg-v1 when frozen)
Date frozen: Fri 6 Nov 2026, 19:08 IST   Commit/tag: tag prereg-v1 (this commit; hash in the git tag)   Plan text: tag `plan-freeze` (prep/16 sections 1-19) plus pre-sprint measurements in sections 20-21.
Written during the sprint (after 17:29 IST), before any experimental run.

## Question (one sentence)
In a small multi-agent game with a shared resource and a never-mentioned shared file, does what scripted peers say in chat (denying the file exists, hinting at it, or neutral talk) change whether LLM agents discover and use that file, and does it depend on model size?

Claim wording: stylised model of agent swarms; peer chat is scripted; not a claim about deployed systems. Findings are about prompts, game and models tested.

## Environment
Pool game, N seats (N=5: 3 LLM + 2 bots; N=10 headline: 5 LLM + 5 bots), 30 rounds. Pool starts at 10N units, each seat takes 0-10 per round, pool regrows 20% of the remainder (cap 10N), collapse below 20% of start; after collapse the episode runs to round 30 with zero payoff (prep/16 18.1). Quota 1 per seat per round keeps the pool alive. Board file `board.txt` plus 3 distractor files exist in the shared folder and are never mentioned in the prompts. Agents act by plain-text actions (LIST, READ, WRITE) parsed by our code; no hosted tool calling. All LLM calls in parallel per round.
Thinking: **off for every LLM seat** (hosted `reasoning.effort=none`; local `enable_thinking=false`), temperature 0.7, max_output_tokens 512, empty reply retried once. Observation window: last 3 rounds, bot messages truncated at 40 tokens; hint or denial line first, every pool line at most 30 tokens.

## Models (roster by cost class; chosen by rule, section 21)
small local: minicpm5-2b, qwen3-8b (llama-server, real mode, thinking off) | cheap hosted: deepseek-v4-flash | mid hosted: qwen3.8-27b | large hosted: qwen3.5-397b (glm-5.2 only if it answers at G1; otherwise dropped) | cross-family check: gemma-4-31b-it. Model IDs exactly as returned by the API model list on 2026-11-06: deepseek-v4-flash, qwen3.8-27b, qwen3.5-397b, gemma-4-31b-it (plus gemma-4-26b-a4b-it optional); local GGUF builds: MiniCPM5-2B Q4_K_M, Qwen3-8B Q4_K_M. Size is a descriptive per-model table, no p-values.

## Arms (bots take exactly 1 unit; seat counts per N above)
- Neutral bot: neutral game chat, no file, resource or path words.
- Hinter (generic / named) and Denier (generic / named): Neutral plus a hint or denial line; speak in round 2 and every 3rd round (2, 5, 8, ...). Dose = number of hinter/denier seats among the bot seats: N=5: 0/1/2; N=10: 0/2/5 (the rest Neutral).
- Sham: length-matched filler chat, no file or resource words (chat-volume placebo; equivalence check outside Holm).
- Told arm (P-TOLD): prompt announces the board; detection ceiling of the LLM write pipeline.
- Chat-blind: one LLM target sees an empty window; other LLMs see chat. Cells blind+hint and blind+neutral (named hint, dose 2); outcome = target's own WRITE; exploratory.
- No-board folder: negative for the monitor. User (reads the board, follows the quota) and Ignorer (random 0-10) are test-only all-bot controls, not experiment arms.
- X16 (exploratory): one LLM peer instructed to hint (named) and one to deny (named), N=10, deepseek only, n=10 each.

## Primary outcome
Any substantive WRITE to the board by an LLM seat within 30 rounds (episode is the unit). Substantive = the written line contains a digit AND one of: take, quota, limit, per round, max, leave, share, propose; regex (case-insensitive) = a digit `\d` AND `(take|quota|limit|per round|max|leave|share|propose)` in the same written line, hand check of 30 lines with at least 90% agreement or the regex is fixed before data. Bot events never count. Reported alongside: share of LLM seats that wrote, round of first WRITE (right-censored at 30), first READ (discovery). Secondary (descriptive): final pool, collapse rate and round, rounds survived, total payoff, mean take, WRITE before collapse (post-treatment subset), empty-reply rate per arm.

## Cells, seeds, n
Headline cells (N=10, dose 2 and 5): neutral; hint generic/named; deny generic/named; sham; told; blind+hint; blind+neutral. Hosted limit measured at 100 requests/60 s shared across models (prep/16 section 22), so: deepseek-v4-flash n=50 on all 13 cells; qwen3.8-27b, qwen3.5-397b and gemma-4-31b-it n=20 on six key cells (N=10, dose 2: neutral, hint generic, hint named, deny generic, deny named, sham); no n=100 contrasts; local minicpm5-2b and qwen3-8b n=20 on every cell (extra local replicates may be added, logged); exploration n=8 per cell, not counted. Exploration seeds 1-99, confirmation seeds 1000 and up, never reused; seed = episode id for bot and paraphrase selection; paraphrase pools of at least 10 per bot type. Cache key = (model, parameters, messages, episode_id, sample_index).

## Predictions (written before data; sizes are the owner's to edit before the tag)
- P1: named hint raises the substantive-write rate over neutral by at least 0.30 in mid models (qwen3.8-27b, gemma-4-31b-it).
- P2: named denier lowers it, by less than the hint raises it.
- P3 (expected to FAIL): the generic hint raises writes as much as the named hint; expected result generic < named.
- P4: blind+hint equals blind+neutral (descriptive comparison with an interval).
- P5: the hint effect is larger in larger models (direction only, uncertain).

## Margins and claim rules (one per question; fixed before data)
- Q3 (headline; Holm family of 4: hint-vs-neutral and deny-vs-neutral at each level, pooled over dose, stratified by model, episode as cluster): effect claimed if the Holm-adjusted interval excludes 0; "peers do not change use by more than 0.30" claimed only if the 90% interval lies within +/-0.30; otherwise estimate and interval, no null claim. Floor: all arms under 5% WRITE means "peers cannot trigger use in this world" (a statement about prompt and world).
- Sham-vs-neutral equivalence (outside Holm): point estimate within +/-0.10 and 90% interval within +/-0.30; at n=8 the check is "sham writes at most 1 episode more than neutral".
- Q1, Q2 (small vs large, neutral baseline and hint effect): descriptive per-model table; margin +/-0.30 for a "matches" reading, no p-values.
- Q4 (spread curve, write rate vs number of hinters): descriptive. Q5, Q6 (monitor detection; denier vs sham): detection-rate difference margin +/-0.15 [owner may edit]; Q7 (false accusation): descriptive stretch.
Promotion rule applies to Q4-Q7 only (judged at G3 by the n=8 sham rule); Q3 is confirmed unconditionally.

## Gates (details in prep/16 sections 5, 17.7, 18)
G0 unit tests (User keeps the pool alive, Ignorer collapses it, no "board" in prompts, cache independence, no hint line truncated in a rendered window); G1 API (sustained 95 requests/min for 5 min, zero 429, empty-reply rate under 5% on deepseek); G2 pilot (neutral-arm READ rate 10-90% in at least one model per class; WRITE floor branch: switch once to P-OPEN, else primary outcome becomes discovery; ceiling: raise distractors 3 to 6; 45-round extension once if more than 40% of at least 5 first READs fall in rounds 26-30); G3 promotion; G4 confirmation counts (no cell below 90% of planned n); G5 report. Told-arm gate: at least 0.8 WRITE in one model per class that has a told cell.

## Budget and compute
Metered from the API `cost` field; soft cap $150 (at the cap finish to the nearest checkpoint or $160, then hard stop). Cost about $5-12 (section 22). Measured sustained throughput: 100 requests/min for all hosted models together (about 35 N=10 episodes/h); hosted plan 1,090 episodes = 31 h; one global limiter at 95/min; 429 pauses all hosted calls 60 s. Local server runs on one GPU, sequential.

## Pre-existing work (declared)
Literature review (73 papers read at analysis depth; 80 verified entries), plan v3 and three audits (tag `plan-freeze`), API and local probes of 2026-11-06 before 17:29 IST, a prior-work repository (benchmarks, earlier prompts). The engine, prompts as run, paraphrase pools, analysis code and all runs are sprint-weekend work.

## Hashes and code (filled in later; stated openly)
v1.1a before the first G2 pilot episode: SHA-256 of P-MAIN, P-OPEN, P-TOLD and all paraphrase pools [fill]. v1.1b before the first confirmatory call: analysis script hash, engine commit, final roster and versions, measured throughput, temperature, token cap [fill]. The report states that hashes and code are tagged after the engine exists.

## Report labels and deviations
Labels: preregistered | fixed before outcomes | exploratory. Deviations log: DEVIATIONS.md (date, change, reason, touched prompt/config/margin/threshold yes/no).

## Status at tagging
Owner sign-off 2026-11-06 (evening, message "I think we have finalized prereg v1"): predictions P1-P5 and margins stand as written above. Done: regex text, model IDs, measured throughput (section 22). Still open and allowed to fill in v1.1a/v1.1b (declared above): prompt and pool hashes, analysis script hash, engine commit, final versions of the local builds, seat table per arm as built.
