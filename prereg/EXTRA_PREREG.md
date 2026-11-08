# Exploratory additions: hypotheses and plan, written BEFORE the new runs (2026-11-08, about 16:00 IST)

Status: EXPLORATORY. Not part of the pre-specified (git-tagged) confirmatory study. The confirmatory results and their code stay unchanged. Owner approved all items (message after the report fixes). New runs go to `results/extra/<id>/` (git-ignored, own cache), run through a wrapper that patches settings at run time; no frozen engine file is edited. Raw spend cap for all new runs: soft $12, hard $14 (raw API cost; ledger x1.15 reported separately). Seeds: reuse 1001..1050 (paired with the confirmatory cells) unless stated.

A. Analyses of EXISTING data (post hoc: the data were seen; no hypotheses can be pre-stated; all descriptive)
- A1 Contagion: in episodes with at least one substantive write, how many distinct LLM seats write; after the first write, do other seats read/write sooner than before (hazard by round); by model.
- A2 Does the board change anything: takes by LLM seats in the 3 rounds before vs after the first quota write (pre-collapse writes only); relation of board use (read/write) to collapse round and to total payoff; observational, not causal.
- A3 Read-to-write gap: among episodes where a seat read the board, compare writes after reading an empty board vs a board that already holds a line; first-read round vs first-write round.
- A4 Robustness of the confirmatory result: (a) leave-one-model-out pooled risk differences for hint_named and hint_generic; (b) excluding episodes with any empty reply; (c) equal-weight (per-model mean) estimate; (d) the frozen vs fixed parser (already done: 1 of 1,530 episodes).

B. New runs (hypotheses fixed now)
- E5 Volume-matched sham (`sham_vol`: the sham line is spoken first on the hint rounds 2,5,8,..., then the neutral line, so displayed message length and structure match the hint arms). deepseek-v4-flash, dose 2, n = 50, seeds 1001-1050. H5: write rate 0/50 as in neutral (the confirmatory sham result is not explained by message length). Falsified if any episode has a substantive write at a rate whose Wilson 95% interval excludes 0 (more than 2 of 50 episodes would be needed to exclude 0 only weakly; we report k/50 and the interval).
- E6 Denial under "told" (system prompt names board.txt, P-TOLD) with deny_named at dose 2, deepseek-v4-flash, n = 50. Reference: neutral0-told 13/50 (26%) substantive writes. H6: denial lowers the substantive-write rate (one-sided; supportive if k <= 7/50, i.e. at least 0.12 lower; reported with Fisher exact p against 13/50).
- E7 Extend borderline cells with 40 more episodes each (seeds 1021-1060 added; total 60 per cell): qwen3.5-397b hint_generic dose 2 (20 -> 60; confirmatory RD +0.30, p_holm 0.062) and gemma-4-31b-it hint_named dose 2 (20 -> 60; RD +0.25, p_holm 0.17). Because n changes after seeing the data this is an extension, reported with Wilson intervals and a pooled-over-seeds estimate; no new significance claim is made from it alone. H7: both rates stay positive (lower interval > 0).
- E8 Slower collapse: pool scale x3 (cap 300, start 300, collapse below 60; regrowth rule unchanged; takes still 0-10) at deepseek-v4-flash; cells neutral dose 0 (n = 30) and hint_named dose 2 (n = 40). A 5-episode neutral pilot first; if the median collapse round is not at least 8, scale x2 is used instead (the choice is made on collapse timing only, not on writes). H8: under hints, a larger share of quota-writing episodes write before the collapse than the 22 of 97 hosted named-hint episodes in the main study (descriptive); neutral still has no substantive writes.

Not run: LLM peers instead of bots; the human-plays-an-agent item (plan X14); a second prompt wording.

## Roadmap (priority = value per hour; time = wall clock)
1. A1-A4 analyses: about 1-2 h, $0, runs now in parallel.
2. E5 (50 episodes, about 1.3 h at the rate limit, $0.4) then E6 (50, 1.3 h, $0.4): cheapest and closest to the report's weakest points (volume-matched sham; denial floor).
3. E8 (5 + 70 episodes, about 2 h, $0.6): strongest answer to "late use".
4. E7 (80 episodes, about 2 h, about $5): borderline cells.
Hosted calls are rate-limited to 95 per minute (150 calls per episode), so the runs are sequential in one process: about 6.5 h in total, finishing about 22:30 IST if started at 16:00. Report integration: one short paragraph in the Discussion and a compact appendix table; anything that fails or contradicts is reported.

## Addendum (before any run): how the E8 pool scale is chosen
Pilot: 4 neutral episodes (seeds 1001-1004) each at pool scale x2, x3 and x5 (cap, start and collapse threshold scale together; takes stay 0-10). The scale whose median collapse round is closest to 12 is used (an episode without collapse counts as round 31). The choice uses collapse timing only, never the write outcome. E8 then runs neutral (seeds 1001-1030) and hint_named dose 2 (seeds 1001-1040) at that scale. The runner executes this automatically, in the order: pilot, E5, E6, E8, E7.

Correction: the header time above ('about 16:00') was a mistake; the runs actually started at 12:19 IST on 2026-11-08, before any result existed. Expected finish about 19:00 IST.

## Amendment 1 (12:27 IST, before E8 or any write outcome was looked at)
The scale-x2 pilot (4 neutral episodes) finished at 12:25 with no collapse in any episode (median 31), so x3 and x5 could only collapse later and the candidate list (x2, x3, x5) was wrong for the aim of a collapse around round 12 (the main study collapses at round 4 at x1). The runner was stopped (my own process) before E5 started and restarted with candidates x1.25, x1.5, x1.75 and x2 (x2 reused from the finished pilot). The selection rule is unchanged: median collapse round closest to 12, collapse timing only, ties to the smaller scale. The partial x3 pilot is discarded.
