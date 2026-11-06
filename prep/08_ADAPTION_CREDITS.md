> **2026-11-02 update:** the refinement fixes are applied in [16_PLAN_V3_FIXES_APPLIED.md](16_PLAN_V3_FIXES_APPLIED.md); where it disagrees with this file, 16 wins. Key changes: sprint starts Fri 6 Nov 17:29 IST (72 h to Mon 17:29 IST), engine built Nov 6 only, preregistration written and tagged Friday before any run, rule (d) withdrawn, new schedule and gates.

# 8. The $500 Adaption credits

Researched 2026-10-29 from adaptionlabs.ai and third-party coverage. Nothing here comes from the logged-in app yet.

## The offer
Every participant gets $500 Adaption Platform credits and 3 months of Premium. Winning teams get $1,000 more. Claim at adaptionlabs.ai/app with the registration email (your sign-in; the onboarding email arrives before the sprint). Questions: Adaption Discord (link on the sprint page). A search result showed the same offer for another hackathon (LovHack Season 3); use only the claim route on the Apart page.

## Confirmed in the app (2026-10-29, from Vatsal)
- Signing up gave **50 credits** only. **1 USD = 1 credit**, so the $500 offer should show as 500 credits.
- The $500 has not arrived yet. Last time credits came through the **onboarding email** before the event; waiting for that email, then claim from it.
- Dashboard (Build tab): Adaptive Data (Improve Data Quality; Invent a Dataset, Beta), Adaptive Intelligence (Train with AutoScientist, Beta; Deploy a Self-Improving Model, Beta), Adaptive Interfaces (Visualize Data, Beta). Cost per run and whether "Deploy a Self-Improving Model" gives a callable endpoint are still unknown.
- A first Invent a Dataset attempt "didn't work" (reason not recorded).

## What Adaption sells (public pages)
- **Invent a Dataset:** training data from a task description, no seed data. Reported inputs: task, domains, row count, format, languages. Exports JSONL, JSON, CSV, Parquet; instruction or preference pairs (SFT, DPO). Asynchronous `datasets.invent` call; the returned dataset ID can feed an AutoScientist run (third-party report).
- **Adaptive Data:** improve, expand or restructure existing data; Forge turns documents into training data; Blueprint sets behaviour rules; 242 languages.
- **AutoScientist:** set a target behaviour; it tunes data and recipe together and trains a model. Runs on Together AI fine-tuning, 0.5B to over 100B parameters (Tiny AutoScientist 0.8B-8B). One-click export to a Hugging Face repo (adapter weights, tokenizer, dataset copy).
- Not found: pricing, credit units, per-run cost, API/SDK docs (docs and pricing URLs return 404), any LLM inference or chat endpoint.

## What it means for us
- **Do not plan on credits for the frontier reference arm.** No evidence Adaption serves frontier LLMs for agent calls. Budget the frontier arm separately or reshape the question (see 02, section 4).
- Track B (log forensics): Invent a Dataset could make synthetic logs with planted coordination as the known-answer control.
- Track A (proxy vs frontier): AutoScientist could fine-tune a small model as the proxy. Untested idea. Training deliberately misaligned agents is dual-use: sandbox only, covered in the Limitations and Dual-Use appendix.
- Reported gains (35% over human-configured setups, win rate 48% to 64%) are the company's own internal numbers; do not cite as independent.

## Check in the app (settles everything)
1. Balance and unit (dollars or credits).
2. Cost of one Invent, Adaptive Data and AutoScientist run.
3. Any inference or chat endpoint; any API key or SDK.
4. Whether credits and Premium expire after the sprint.
Record answers here with the date and IST time; update 02 section 4.

## Sources
adaptionlabs.ai (home, /auto-scientist, /adaptive-data, /invent-a-dataset); Pulse 2.0 launch article; AlphaSignal Hugging Face export article; LovHack claim form (tally.so/r/GxWqKL).

## Update 2026-11-02 (from Vatsal)
- Inference works on Adaption via its own assistants, for a select few models (DeepSeek-V4 Flash, GLM-5.3 Flash, Qwen 3.5 397B, Gemma 4 31B IT, Gemma 4 26B, others). Docs to follow. This reverses the earlier "credits do not cover agent calls" guess; the sprint plan now uses them for hosted arms (see 09).
- Still unknown: price per model, rate limits, whether calls can run in parallel.
