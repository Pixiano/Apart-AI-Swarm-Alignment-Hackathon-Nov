> **2026-11-06:** prep/16 section 17 (audit fixes) wins on n per cell, gates, seats, game numbers, cache key and freeze dates; stale gate, date and n=20 lines in this file are void.

# 15. Credits estimate for the plan as written, and whether more depth/episodes matter

Drafted 2026-11-02 (IST). Reproduce with `15_credits_estimate.py` (same folder). Prices are the real Adaption list in 11. **Assumptions are marked; the three unknowns (reasoning tokens, rate limits, caching discount) can each move the answer by 2-4x, so re-run after the key arrives (about Nov 4-5).**

## 1. Assumptions (plan as written)
- Every agent in a hosted run is an LLM (up to N = 5/10/20), 30 rounds, 1 call per agent per round, scripted bots are free.
- n = 20 episodes per cell (the freeze item). Output 100 tokens per call. 15% retries/failed calls added.
- Cells: Q1/Q2 main grid = 7 hosted models x N in {5,10,20}; ablations (prompt templates x2, Q1 extras x5, Q3 x7 conditions, Q4 x8 conditions) on 3 models at N = 10; Q5/Q6 monitor reads of ~600 logs (about 160 monitor calls per log across visibility levels and variants); Q7 caught: 27 cells x 2 models; Sat confirmation = two promoted questions on fresh seeds (about 2x the average question's volume).
- Input tokens per call is the main cost lever: **2,500** if each agent sees a long history, **1,200** if history is windowed to the last few rounds.

## 2. Cost per 100,000 calls (2,500 in / 100 out; second column = +400 hidden reasoning tokens)
| Model | no reasoning | with reasoning |
|---|---|---|
| deepseek-v4-flash | $12.44 | $17.78 |
| qwen3.8-27b | $22.25 | $72.25 |
| gemma-4-26b-a4b-it | $21.68 | $31.88 |
| gemma-4-31b-it | $25.90 | $39.50 |
| glm-53-flash | $42.50 | $62.50 |
| glm-5.2 | $70.00 | $246.00 |
| qwen3.5-397b | $172.50 | $312.50 |
Qwen 397B costs about 14x DeepSeek V4 Flash per call; GLM-5.2 and Qwen 3.8 explode if they reason, because output is priced 30-60x input.

## 3. Total for the plan (about 1.0M calls as written)
| Scenario | calls | no reasoning | +400 reasoning tokens/call |
|---|---|---|---|
| A. As written, 2,500 in, 3 core models for ablations, monitors on core 3 | 1.04M | **about $910** | about $1,560 |
| B. A with history windowed (1,200 in; monitors 3,000 in) | 1.04M | about $525 | about $1,180 |
| **C. B plus ablations/confirmation/monitors on 2 cheap models (DeepSeek V4 Flash + Gemma 31B); the big/expensive models only in the main grid** | **0.81M** | **about $140** | **about $308** |
**So the plan as written does not fit in $500; the fix is scenario C.** The savings come from (1) windowed history (2.0x), (2) not running Qwen 397B / GLM on every ablation (3.7x), (3) monitors on the cheapest model. Remember the earlier cap of about $150 for the sprint (the rest of the credits are for Vatsal's own projects): C fits it only if models do not reason.
Local arm: free. Qwen3-8B does about 69 five-agent or 29 ten-agent episodes per hour; MiniCPM about 200 and 65 (see 13 section 9).

## 4. Does more depth or more episodes matter?
**Statistical power (two groups, 80% power, alpha .05, worst-case rate .5; minimum difference detectable):**
| episodes per cell | alone | with Holm over 4 tests |
|---|---|---|
| 10 | 0.63 | 0.75 |
| 20 | 0.44 | 0.53 |
| 50 | 0.28 | 0.33 |
| 100 | 0.20 | 0.24 |
| 200 | 0.14 | 0.17 |
- **n = 20 can only see huge effects** (for example 20% vs 64% board use). Fine for Friday exploration, which is labelled exploratory anyway; **too weak for a confirmatory claim or a null**. A null at n = 20 cannot support "no effect" or "matches" (the equivalence margin would have to be about 0.45).
- **More episodes matter much more than more rounds.** Independent episodes are the unit that buys power; doubling the rounds (30 to 60) doubles the cost, adds almost no independent units, and only helps the slow-dynamics questions (Q4 spread/threshold).
- **Money scales linearly, wall-clock does not fit.** In scenario C, n = 50 per cell costs about $325 (no reasoning) and n = 100 about $634; at 16 calls per second that is 33 h and 64 h of pure compute, more than the sprint. Rate limits are unknown; the real ceiling is calls per second, not dollars.
- **Therefore: concentrate depth where it counts.** Friday exploration at n = 10-20 per cell (cheap, many cells). Saturday: only the 1-2 promoted questions, on **n = 100 per cell, 6-10 cells**, cheap models. Rough cost for that confirmation: 2 questions x 8 cells x 100 episodes x 300 calls = 480k calls = about $32 (DeepSeek V4 Flash) to $68 (Gemma 31B) at 1,200 input tokens; about 8 h at 16 calls per second, less with more parallelism. This is a better use of credits than doubling Friday.
- **Cheaper power:** use continuous or time-to-event outcomes (round of first board use, per-episode count of agents using it) instead of a yes/no per episode; paired seeds across arms; one analysis unit per episode (agents within an episode are not independent). All of these shrink the needed n.
- **Free replication:** run local Qwen3-8B / MiniCPM episodes in parallel with the hosted ones (different resource), for example 100 five-agent episodes in about 1.5 h of GPU time.

## 5. Recommended budget rules (pending the Nov 4-5 timing test)
1. Window the history so the average input is at most about 1,200 tokens.
2. Pick the hosted roster by cost class: expensive models (Qwen 397B, GLM-5.2) only in the main grid at n = 10-20; ablations and confirmation on DeepSeek V4 Flash and Gemma 31B.
3. Measure reasoning tokens first; if a model reasons, cap `max_output_tokens` (150-300) or drop it from the confirmation set.
4. Hard stop: sprint spend cap of $150 until the measured numbers say otherwise; ask before going above it; log tokens and cost per call (13 section 3).
5. Fix n per cell in the freeze as n = 20 (exploration) and n = 100 (confirmation), and say what a null at n = 20 can and cannot claim.
6. Measure calls per second on the key's first day; recompute hours using 8 / 16 / 32 parallel calls. If under 8 calls per second, cut confirmation cells before cutting n.
