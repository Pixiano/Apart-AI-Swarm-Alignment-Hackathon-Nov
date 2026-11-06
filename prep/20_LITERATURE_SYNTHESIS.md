# 20. Literature synthesis and re-ranked top 15 (2026-11-04)

Basis: 73 per-paper analyses in `papers/analysis/` (each with section 8 Relevance). Depth is analysis-level: partial reads, scrambled tables and unread appendices are flagged per file. This is review input for the pre-freeze review (prep/16 section 12), not a decision. After the freeze, ideas go to the deviations log as exploratory.

## 1. Main finding
No paper tests the headline: peers saying deny / hint / neutral things changes whether LLM agents find and use an unannounced shared file. Nearest neighbours, all of which differ in a way that matters:
- Peer statements move answers: Cho, Mehdizadeh, Laustsen, Wynn, Baltaji, Kasprova, Yang 2609.12446, Ys 2608.02758 (all questions or classification; no tool or file, no resource).
- Visible counts move later agents: Hashemi (counts, not messages).
- Agents act on discovered files or hints: Meinke, Lynch, Marchand (single agent, no peers).
- Shared-pool worlds: Piatti, Curvo, Gupta, Rehm, Willis, Piedrahita (no hidden file, peers' statements not manipulated).
Claim wording allowed after the freeze: "to our knowledge, not tested in the 73 papers we read at analysis depth". Not "first".

## 2. Ideas that could change the plan (decide BEFORE the freeze)
1. Dose-response is sigmoid in peer share (Mehdizadeh, Cho: agree minus disagree count is the best predictor). Our dose-by-count design fits. Keep N=5: 0/1/2, N=10: 0/2/5.
2. Wording format changes flip rate a lot (Cho: Reason format 0.30 vs Count 0.22). Freeze the generic/named hint wording and the paraphrase set before any run; this is already in the plan, now with evidence.
3. Speaker credibility matters (Yang 12446, Ys, Kasprova). The "named hint" level may work as credibility, not information. Report it as such; do not interpret generic vs named as an information effect alone.
4. Neutral bot can carry hidden steering (Choi Table 4). Add a plumbing check: Neutral paraphrases must not change the WRITE rate against the Ignorer/sham in a pilot of non-outcome type. Cheap.
5. Model size is confounded with provider and reasoning class in nearly every paper (Gupta, Hashemi, Piedrahita, Thaman). Pre-declare size x condition as descriptive, not causal, unless the same family is used.
6. Eval-awareness confound (Greenblatt 2024, Knecht, Schoen, Chaudhary, Nguyen): bigger models may notice a test. The board is never mentioned, which helps. Log reasoning where available; no mechanism claims.
7. Self-report is unreliable (Ren 2503, Florin, Pacchiardi). Primary outcome stays the logged WRITE event. Optional post-episode question (Joglekar-style) is exploratory only.
8. Seed variance is large (Curvo 3 runs, Gupta 10 trials wide SE, Ashery cells of 3-10 runs). n=20 per cell is a minimum; the plan's n=100 for promoted questions is justified.
9. Analysis hygiene (Murtuza): candidate pairs built blind to condition labels; a negative-control permutation; never read adjacency as coordination. Miller: episode is the cluster, report cluster count. Knopov: equivalence claims need many runs; our margin of +-0.30 is coarse, so nulls are "not detectably different at the margin".
10. Growth rate sensitivity (Gupta: punishment effects non-linear in growth rate). Optional: one second regrowth rate as an exploratory check. Owner decision; adds cost.

## 3. Conflicts with the current design
- Choi: majority and capability effects are large and both need to be separated from N; our N is confounded with prompt length (already a known issue in prep/14). Keep the fixed observation window.
- Hashemi: effect arises from visible counts. Our board contents are text, but if agents can see how many peers have written, count visibility could contaminate Q3. Check the engine does not expose per-agent write counts in prompts.
- Murtuza: Q4 spread must stay a descriptive curve (already decided); do not call it coordination.
No finding forces a cut.

## 4. Re-ranked top 15 (replaces prep/19 order after full-text analysis)
| # | Paper | Reason for move |
|---|---|---|
| 1 | Piatti 2024 (+ Curvo 2025) | Closest world; cite sections, not intro numbers |
| 2 | Laustsen 2026 | Peer influence by family and size; abstract contradicts Sec 3.3, cite body |
| 3 | Cho 2025 | Dose and format evidence |
| 4 | Mehdizadeh 2025 | Sigmoid dose-response, topology for Q4 |
| 5 | Yang 2609.12446 | Speaker credibility (moved up from 12) |
| 6 | Ys 2608.02758 | Single public dissenter cascades (new in top 15) |
| 7 | Kasprova 2026 | Peer-reputation information changes group behaviour (new) |
| 8 | Ashery 2024 | Committed-minority tipping; dose design (new) |
| 9 | Miller 2024 | Cluster statistics |
| 10 | Murtuza 2026 | Method lesson (circular test) plus incident |
| 11 | Kale 2025 | Monitor design for Q5/Q6; cite 15.6 pp |
| 12 | Hashemi 2026 | Count-visibility herding, contamination check |
| 13 | Qian 2026 | Preregistration with honest failure reporting |
| 14 | Gupta 2025 | Sibling pool, variance, growth-rate sensitivity (new) |
| 15 | Greenblatt 2024 | Observer-effect threat (new) |
Also cite: Knopov 2026 (margins), Mao 2026 (Q7, headline range only), Hammond 2025 (framing), Motwani 2024, Meinke 2024, Willis 2026, Rehm 2026.
Dropped from the earlier top 15: Wu 2026 (encoding damage, formal model unread, and we avoid R0), Alnuhait 2026 (0.9% vs 1.50% unreconciled). METR blog stays as a primary-source citation outside the ranking.

## 5. Do not quote the abstract (body disagrees)
Laustsen (small vs large models), Kutasov 2511 (50 to 89% safety), Kale ("about 15%" is 15.6 pp), Knecht (omega bounds), Tailor (TPR=1), Mehdizadeh (over 70%), Hagag (benign accuracy), Thaman, Vaugrante, Ying, Ys (authority effect), Piatti intro numbers, Alnuhait (0.9 vs 1.50), Schoen (26 vs 20 evals), Ren 2511 (16 models), Rehm (G1 after Holm).

## 6. Review limits
Appendices are unread in many files; tables are scrambled in about half. Before citing any number in the report, re-open the PDF at the named section.
