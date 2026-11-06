> **2026-11-02 update:** the refinement fixes are applied in [16_PLAN_V3_FIXES_APPLIED.md](16_PLAN_V3_FIXES_APPLIED.md); where it disagrees with this file, 16 wins. Key changes: sprint starts Fri 6 Nov 17:29 IST (72 h to Mon 17:29 IST), engine built Nov 6 only, preregistration written and tagged Friday before any run, rule (d) withdrawn, new schedule and gates.

# 3. Timeline (very rough)

Today is Thu 2026-10-29. Exams are on until a date you set; the pre-sprint blocks are light and movable. Deadline: **Sun Nov 8, 11:59 PM AoE = Mon Nov 9, 17:29 IST**. Aim to submit Sunday early afternoon IST, not at the wire.

| When | What | Output |
|---|---|---|
| Thu Oct 29 - Sat Oct 31 | Read the METR report, Swarm Traces page, reading list for your track (open and verify each citation before using it). Claim the $500 credits and test one cheap call. Check the Google Doc template. | Notes, working endpoint |
| Sun Nov 1 | Choose track and the one narrow question (02, section 3). Decide fallback. | One-paragraph question |
| Mon Nov 2 - Tue Nov 3 | Adapt the harness enough to time **one round of N agents** on the GPU (throwaway seeds, no outcome analysis). Write scripted bots. Fill the compute table with measured numbers. | Measured budget |
| Wed Nov 4 | Draft the preregistration (04): predictions, margin, analysis code, sample sizes. | Draft plan |
| **Thu Nov 5** | **Freeze and tag** (05) before any confirmatory run. Re-read the sprint page for last changes. | Tagged plan |
| **Fri Nov 6** | Sprint start tag. Disclosure log opened. Pilot gate (~3 PM IST): does the environment produce the measured behaviour? Go or switch to fallback by evening. Launch confirmatory runs in the background. | Gate decision, runs going |
| **Sat Nov 7** | Runs continue (cheap local first, frontier arm early). Write Introduction, Related Work, Methods. Number-to-source map started. Template copied. | Draft of sections 1-3 |
| **Sun Nov 8** | Stop new runs by midday. Analysis, figures (one real-run example figure), report, appendix, abstract written last at 150-250 words. Clean-clone rebuild, link check logged out, tag `submitted`, upload form. | Submitted PDF |
| Mon Nov 9 | Buffer only (IST deadline 17:29). Do not plan work here. | - |

## If time shrinks (cut from the bottom)
Frontier replicate seeds, N=20 seeds, the mechanism arm's second variant, optional video. Never cut: positive control, sham arm, frozen margin, Limitations and Dual-Use appendix, the number-to-source map.

## Additions (2026-11-02), all times IST
| When | What |
|---|---|
| Mon Nov 2 | GPU benchmark runs in the background (all six local models). Tables, audit fixes and plan docs written. |
| Tue Nov 3 | Read benchmark results. Build the minimal world and scripted bots in the prior-work repo (declared as pre-existing). |
| Wed Nov 4 | Local model sweep with the three prompt templates (selection rule in 13). Draft margins, predictions, analysis code. Credits and API key may arrive by email on Nov 4-5. |
| Thu Nov 5 | Freeze and tag, using the extra checklist in 05. If the key has arrived, run `bench/api_timing.py` once (cap 0.50 USD); if not, the hosted roster is fixed by rule. |
| Fri Nov 6 | Morning API plumbing check, then the Friday exploration. |
| Sat Nov 7 | Confirmation runs. Build `numbers.md` and the one-command rebuild. |
| Sun Nov 8 | Clean-clone rebuild, one real-run example figure, report, submit early. |

## Friday re-run (decided 2026-11-02, Vatsal)
The GPU/speed/format benchmark and the local-model sweep are repeated on **Fri Nov 6, inside the sprint**, as the FIRST task, so the sprint has its own in-sprint timing data (pre-sprint results stay declared as prior work). Order on Fri Nov 6 (IST): (1) re-run bench grid on the 1-2 chosen models plus a quick sanity pass on the rest, (2) API plumbing check if the key has arrived, (3) Friday exploration. Log the pre-sprint vs in-sprint numbers side by side.

## Update 2026-11-02 (evening)
Benchmark done and pushed. Nov 3 is free for building the world; the Friday re-run keeps the same scripts (`python bench/run_all.py`, then `run_tools.py`, `summarize.py`, `timings.py`).
