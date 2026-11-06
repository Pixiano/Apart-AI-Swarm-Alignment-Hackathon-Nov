# 6. Lessons from the collusion sprint, as actions

Source: `../Pre/notes/LESSONS_FIRST_SPRINT.md` and `GAP_ANALYSIS.md`. Result then: 33rd of 392 (11/15; Impact 3, Execution 4, Presentation 4). Seven entries at 13/15 (Impact 4, Execution 5, Presentation 4). The gap was Execution +1 (rigour) and Impact +1 (a mechanism test).

## The three lessons
| Lesson | What happened | Do this time |
|---|---|---|
| 1. Freeze one ambitious plan | 121 of 139 commits after the freeze, about 30 deviations; the distinctive arm came after the freeze | Mechanism arm written into the frozen plan (05). One headline result. |
| 2. Plan 2-3 rare ideas up front | About 20 entries asked the same question, 8 reported the same null. Rare: positive control (0.5%), message-cut arm (0 of 17) | Rare ideas in the plan: scale sweep 5/10/20, pre-stated divergence margin, scripted-agent positive control, mechanism arm |
| 3. Compute is a design constraint | Top entry spent $53 on frontier; our hosted credit ran out mid-cell | Budget on day one (02, section 4). Local for volume, frontier for the confirmatory arm first, spend cap |

## The ten habits
| # | Habit | Concrete action |
|---|---|---|
| 1 | Freeze predictions, margins, code; tag | 05 checklist |
| 2 | Validate on known-answer bots first | Scripted channel-user and channel-ignorer with a unit test; control must pass before anything is read |
| 3 | Sham arm for every effect | Channel-absent and placebo-content arms |
| 4 | Metric on the actor you study; parts separate | Define the outcome per agent group, not over everyone (the all-firm index mixed the replaced firm in); report proxy and frontier parts separately |
| 5 | Test the word before using it | No "collusion" or "coordination" in claims without a test that distinguishes it from independent behaviour |
| 6 | Nulls only against a margin and power | Margin in the plan; minimum detectable effect from pilot SD; check identical runs |
| 7 | Status labels and deviations log | Labels in section headers; dated deviations file |
| 8 | Confirm surprises on fresh seeds | Split seeds: discovery vs confirmation, written prediction before the confirmation run, never pooled |
| 9 | Failed predictions in the abstract | One prediction expected to fail, reported up front |
| 10 | Number-to-source map; clean-clone rebuild | `numbers.md`: every figure and table value to script and data key; rebuild from a fresh clone before submitting |

## Also
- **Abstract:** use the full 150-250 words with numbers. The short 108-word abstract scored 7/15 at the screen; the full report scored 11/15.
- **Title states the finding**, not a question.
- **One figure from a real run** (one real trajectory with every condition), not only summary plots.
- **Scope of claims:** match the model set (do not say "four models" if one arm covers three); keep caveats next to the claim.
- **Cost and call count** in the report; test count; data hashes.
- **Presentation** is already at top level; spend effort on Execution and Impact.
- Do not treat AI-judge scores as the real panel; it capped scores by design.

## What the real (preliminary) reviews say, generalised
Source: three preliminary reviews of the collusion entry, received 2026-10-31, no scores yet. Written as rules for any sprint.

**Keep doing (all three praised):** preregistration before data; paired branches from one checkpoint; a positive control; honest limitations; a finding that names the *lever* (communication) rather than only a null.

**Review-proofing: ask these of the design before the freeze**
1. **Trivial-actor test.** Would a degenerate actor (floor-pricing newcomer, a do-nothing agent) move the headline metric by about the reported effect on its own? If yes, the metric mixes the actor in. Compute the metric for the actor and for everyone else separately.
2. **Blind arm.** If the intervened agent can still see the channel or history that carries the effect, a null is expected. Add an arm where it cannot.
3. **Outcome of harm.** A proxy (posted price, message count) is not the harm. Add one outcome that reflects real cost (profit, depletion, damage) beside the headline metric.
4. **Scope sentence.** Say what the setting is and is not (explicit vs tacit, stylised, gated on a condition) in the abstract, not only the limitations.
5. **Heterogeneity.** A large between-model gap (five-fold in one model) must be explained or flagged as a finding, never left silent.
6. **Scripted bots are controls, not realistic adversaries.** Label them so; pair with an instructed LLM version and report disagreement as a result.
7. **Conditional claims.** If only runs that reached a gate enter the analysis, the answer is conditional on the gate; state the gate and pass rate beside the claim.
8. **Size and horizon.** Small n (4-5) and short horizons draw criticism. Fix n and horizon in the freeze; name the extension that would change the answer.
9. **Intervention, not only observation.** The most liked result was an interaction (replacement x removing messages). Prefer an arm that removes the suspected mechanism over one more descriptive cell.
10. **Future work reviewers want:** test the mechanism as a direct intervention (for example message filtering). Put the one you can afford in the plan instead of the future-work paragraph.
