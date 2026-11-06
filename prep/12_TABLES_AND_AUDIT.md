> **2026-11-02 update:** the refinement fixes are applied in [16_PLAN_V3_FIXES_APPLIED.md](16_PLAN_V3_FIXES_APPLIED.md); where it disagrees with this file, 16 wins. Key changes: sprint starts Fri 6 Nov 17:29 IST (72 h to Mon 17:29 IST), engine built Nov 6 only, preregistration written and tagged Friday before any run, rule (d) withdrawn, new schedule and gates.

# 12. Ablations, extras, twists, and the audit of last sprint's lessons

Drafted 2026-11-02. Plain-words style on purpose: if you can say it to a newbie, it is right. Questions Q1-Q7 are in 10. Status: draft until the Thu Nov 5 freeze.

## 1. Ablations (small changes inside the main research)
An ablation = change one thing and see if the result moves. It tells us *why* a result happens.
| Q | Ablation | What we change, in plain words | What it tells us |
|---|---|---|---|
| 1, 2 | Prompt template | P-MAIN vs P-OPEN vs P-FOCUS (see 13) | Does the answer survive a different framing? |
| 1 | More thinking | Allow longer replies or reasoning | Does thinking time close the gap? |
| 1 | One family, three sizes | Gemma at 12B (local), 26B, 31B (hosted) | Is it model size, or just the brand? |
| 1 | Temperature | Randomness 0.3 / 0.7 / 1.0 | Is finding the board just luck? |
| 1, 4 | Private notes on/off | Let agents keep a scratchpad | Do agents need to remember the discovery? (They forget between turns otherwise) |
| 2 | Group size | 5, 10, 20 agents | Where does the cheap model break? |
| 2 | Real AI vs scripted | 1, 3, or all agents are real models | Does a scripted crowd change what real agents do? |
| 3 | Rule shown to some | Tell some agents "the board is off limits" | Do peers' words beat an explicit rule? |
| 3 | Who says it | A peer vs the instructions | Who do agents trust more? |
| 4 | Network shape | Everyone talks to everyone / a ring / a star | Does who can talk to whom change the spread? |
| 4 | Hinting peers | 1, 2, 4 peers hint | How many nudges flip an agent? |
| 4 | Memory window | Agents see last round only vs all history | How long do they need to remember? |
| 5 | Overseer size | Cheap vs frontier overseer | Does a better overseer catch more? |
| 5 | What is hidden | Hide random messages vs hide board-related ones | Is it what the overseer sees, or how much? |
| 6 | Distrust instruction | Tell the overseer to doubt peers' claims | Can a simple warning stop the denier fooling it? |
| 6 | Loud vs quiet denier | Denier speaks every round vs once | Does repetition fool the overseer? |
| 7 | How it is shown | Exact quote / vague / false accusation | Is the reaction to guilt or to being accused? |
| 7 | Consequence | None / warning / penalty | Does a threat change honesty? |
| 7 | Who accuses | A peer / the overseer / the system | Does the accuser matter? |
| 7 | Cheap vs frontier | Same test on both | Do bigger models lie less, or better? |

## 2. Extras (only after the main research is done)
Extras = nice-to-have work that adds weight but is not needed for the answer.
| # | Extra | Plain words | Why it is worth doing |
|---|---|---|---|
| E1 | Sandbox decoy test | Fake "outside" tools (stub internet, decoy project file) just beyond the sandbox; log every attempt to use them | Shows how well the sandbox holds and what models try |
| E2 | Clean-clone rerun | Someone else re-runs one seed from the repo and gets the same numbers | Proof the work is reproducible |
| E3 | Planted-flaw ladder | Our own toy sandbox with a deliberately simple bug; does a frontier model find it? | A safe, controlled look at breakout skill |
| E4 | Cost per match | Dollars a cheap model needs to behave like the frontier | A practical result for other researchers |
| E5 | Hosted vs local agree | Replay the same episodes from cache on both | Does the cheap local setup stand in for the hosted one? |
| E6 | Model table | Exact versions, prices, tokens used | Lets anyone repeat it |

## 3. Twists (what makes each question new)
A twist = the part most other entries would not do. Last sprint about 20 entries asked the same question, so each of ours carries one.
| Q | Twist in plain words | Why it is new / how to say it to a newbie |
|---|---|---|
| 1 | "Close enough" is a number we write down **before** the data | Most studies decide afterwards whether two models "match". We can't cheat |
| 2 | Find the **break point**: the smallest group size where the cheap model stops matching | Instead of "sometimes differs", we get one clear number |
| 3 | **Dose-response**: 0%, 25%, 50% of the group are deniers or hinters | Like a drug trial: how much "advice" from peers does it take to change behaviour? |
| 4 | A **behavioural R0**: the chance that a neighbour copies, measured from a bot that always does it | Borrowed from epidemics: how contagious is finding the board? |
| 5 | A **detection curve**: how well the overseer works at 10%, 25%, 50%, 100% of messages seen | Real overseers never see everything; we show how much they need |
| 6 | Feed the overseer the denier's reassurance and measure if it **gets fooled** | Tests whether bad actors can talk their way past a monitor |
| 7 | A **false-accusation control**: accuse agents who did nothing | Separates "reacting to guilt" from "reacting to being accused" |
| All | **Discovery then confirmation**: a promotion rule written before any data picks what gets re-tested on fresh runs | We explore widely on Friday, but only count what survives a pre-set test |

## 4. Audit: last sprint's lessons checked against this plan
**Update 2026-11-02: every gap below is now implemented in 04 (section 6), 05 (extra checklist), 03 (additions) and 13. Re-check each at the freeze.**
Sources: Pre/notes (LESSONS, GAP_ANALYSIS, COMPARISON, the working log) and the three preliminary reviews. Status: OK (in the plan), WEAK (mentioned but not firm), MISSING.
| # | Lesson or suggestion | Status now | Fix |
|---|---|---|---|
| 1 | Nulls need a stated equivalence margin; a missing margin is "the likeliest attack" (COMPARISON) | WEAK: margin only for Q1 | Give every question its own margin in 04 before the freeze |
| 2 | Many tests need multiplicity control (Holm used by top entries) | MISSING: 7 questions, no correction | Holm correction inside each lens; report adjusted and raw |
| 3 | A "blind" arm must be checked to actually blind (entry D's blind arm failed its own sanity check) | MISSING | Add a manipulation check: log the prompt of every arm and test that the board is hidden or shown as intended |
| 4 | Runs must be independent (entry C: all 30 bases shared one price path) | WEAK | Every seed changes the world layout and bot order; state it in the freeze |
| 5 | Positive control can fail mid-study (entry L, run 10) | WEAK: only a stop rule | Re-run the scripted positive control in every batch; log pass or fail per batch |
| 6 | Don't pick the prompt because it produced the behaviour (entry I) | MISSING | Prompts are fixed from plumbing tests only, never from outcomes; one logged prompt change allowed |
| 7 | Arms added after the main results weaken the study (entry F; our own late message-cut arm) | OK-ish: promotion rule | List every arm and ablation in the freeze; anything later is labelled exploratory |
| 8 | Formation bottleneck: the behaviour may not occur (entry B: 112 of 288 formed a cartel) | OK | Induced-discovery fallback in Q7; report the discovery rate beside every claim; Friday pilot gate |
| 9 | What carries the behaviour: notes vs public history (six entries split them) | MISSING | Added the notes on/off and memory-window ablations (table 1) |
| 10 | Newer models can behave very differently (entry D: Haiku 5.5 and Sol undercut at -0.30 / -0.40) | OK | Seven hosted models; report model IDs and dates; explain big gaps (review point 5) |
| 11 | APIs without a seed are not reproducible (entry J; Adaption has no seed) | MISSING until 11 | Cache every request and reply (hashed), replay from cache; put it in the freeze |
| 12 | Thinking models: GLM 5.3 Flash always thought; cap hit; only `reasoning_effort: low` worked | MISSING | Timing test records reasoning tokens for `glm-53-flash`; set `max_output_tokens` high enough to avoid empty replies; log truncation |
| 13 | Audited numbers: a numbers file mapping every figure to a script, and a one-command rebuild (entries J, G with 177 tests) | WEAK: listed, not scheduled | Create `numbers.md` and a `make all` style script on Sat; clean-clone rebuild on Sun |
| 14 | A real-run example figure | WEAK: listed | Sunday task in 03: one real episode with every condition |
| 15 | The previous per-call time guess was wrong: measured 1.2-3 s per call with 3 parallel (not 4 s); single-stream Qwen3-8B 59 tok/s; gpt-oss ~26 tok/s per call; 83 s per reply when VRAM was full | WEAK | Replace my 4 s assumption with the benchmark agent's measured numbers; keep VRAM headroom (desktop uses ~3.6 GB) |
| 16 | Memory and process traps: servers killed by throwaway cleanup scripts that kill by path; unquoted Windows paths with spaces; background jobs reaped under memory pressure; heredoc edits that failed silently | MISSING from the plan | Overnight runbook: start the server in your own terminal, never kill by name or path, quote all paths, check exit codes before documenting |
| 17 | Don't run two big models together (gemma + gpt-oss crashed) | OK | One model at a time locally; hosted runs have no such limit |
| 18 | Message channels: only 3 of the last sprint's entries had in-game messages, and that was the standout | OK | Our board plus public chat keeps a communication channel in the world |
| 19 | Reviewers: trivial-actor test, blind arm, harm outcome, scope sentence, scripted-bot labelling, gate stated, n and horizon fixed | OK (06) | Check each in the freeze checklist |
| 20 | Public repo hygiene: scan for secrets and mentions before any push; `_local/` never committed | OK | Keep; run the scan before each push |
| 21 | The wrong timeline for the old harness (D:\llm and its llama.cpp are gone) | NEW | Use LM Studio's bundled `llama-server`; the benchmark agent verifies which build works on this GPU |
| 22 | Scale of runs: top entries had 20-24 histories or thousands of continuations; we had 10-20 seeds | WEAK | Fix n per cell in the freeze: at least 20 episodes per hosted cell (about $0.05-0.70 each), at least 10 local |
