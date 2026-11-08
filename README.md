# Does what peers say change whether LLM agents use an unannounced shared file?

A pre-registered study of scripted-peer speech in a 10-seat commons game. Entry to the Swarm Alignment Hackathon (Apart Research, 6 to 9 November 2026).

## Summary

**Read the report:** [`docs/report.pdf`](docs/report.pdf) (main text) and [`docs/supplement.pdf`](docs/supplement.pdf) (appendices B-I: papers reviewed, prompts, design, deviations, extra figures, reliability and cost) and [`docs/slides.pdf`](docs/slides.pdf) (slide deck).

Ten seats share a depleting pool. Five seats are LLM agents and five are scripted peers whose chat lines differ by arm: neutral, sham (placebo chatter), hint (points to a shared file), or denial (says there is nothing useful to find). A shared file, `board.txt`, exists in the agents' file tree but is never named in the task prompt. The outcome is whether an LLM seat makes a substantive write (a quota-style rule with a number) to that file. We ran 1,530 confirmatory episodes across 6 models (4 hosted, 2 local). A **named hint** (a peer names the file) raised the share of episodes with a substantive board write by **+0.456** (risk difference versus neutral), a **generic hint** (a peer says only that a shared file exists) by **+0.080**. Denials and sham peers had no detectable effect. The full analysis, limitations and a post hoc section are in the report.

## What is here and what is not

| Here (tracked in git) | Not here |
|---|---|
| The game engine, bots, parser, runner, analysis (`engine/`) | The `results/` folder: per-episode event logs, the reply cache, `costs.csv`, budget files. It is not tracked (size, and the cache holds raw model replies). |
| Unit tests that need no network or key (`tests/`) | Report sources, figure scripts and table CSVs (they are derived from `results/`). The report PDF and figures are published with the submission; `docs/figures/` carries copies of the figures. |
| Launch checks and cost tools (`bench/`) | Model weights and the local server binary. |
| The pre-registration, deviations log and hash manifests (`prereg/`) | Any API key. |
| Planning notes (`prep/`, indexed in `docs/INDEX.md`) | |

**Getting the data.** The confirmatory logs are the tables in `docs/data/` (CSV, one per figure or table in the report); the raw per-episode logs and cached model replies are not in the repository, so open an issue to request them. To regenerate instead, run the batch plan below (hosted episodes cost money and need a key; a fresh run will not reproduce the same replies, only the same design). Every figure and table in the report is computed from the episode logs in `results/conf`, using `engine/analysis.py` and the summary tools in `bench/`.

## Repository layout

| Path | Contents |
|---|---|
| `engine/` | `game.py` (pool dynamics), `world.py` (file tree and board), `parser.py` (action parser), `prompts.py` (prompt templates), `bots.py` (scripted peers and paraphrase pools), `runner.py` (one episode), `llm.py` (limiter, cache, budget, hosted and local clients), `cli.py` (one episode), `batch.py` (resumable batch plans), `analysis.py` (confirmatory contrasts), `hashes.py` (hash manifest), `logger.py` |
| `tests/` | `test_engine.py`, `test_bots.py`, `test_runner.py`, `test_analysis.py` (plain asserts, no framework) |
| `bench/` | Launch gates (`g1_*.py`), pilot summary (`g2_summary.py`), local timing (`local_sanity.py`), cost tally (`costs.py`), exploratory runs E5-E8 (`run_extra.py`); see `bench/README.md` |
| `prereg/` | `PREREG_v1.md`, `DEVIATIONS.md`, `hashes_v1.1a.json`, `manifest_v1.1b.json`, `EXTRA_PREREG.md` (plan for the exploratory runs, written before they ran, with one logged amendment) |
| `prep/` | Planning notes written before and during the sprint; start at `docs/INDEX.md` |
| `papers/` | Index of the literature reviewed (PDFs are not tracked) |
| `docs/` (planned) | `INDEX.md`, `figures/*.svg` |
| `TROUBLESHOOTING.md` (planned) | Practical problems and fixes |
| `CITATION.cff`, `LICENSE` (planned) | Citation metadata, licence |

## Quickstart (no API key needed)

Requirements: Python 3.10 (the version everything below was tested on; the code uses f-strings and dict unpacking and nothing newer than that, so 3.8 or later is likely fine but untested). The tests and the hash check use only the standard library.

```
git clone https://github.com/Pixiano/Apart-AI-Swarm-Alignment-Hackathon-Nov
cd Apart-AI-Swarm-Alignment-Hackathon-Nov
python -I -B tests/test_engine.py
python -I -B tests/test_bots.py
python -I -B tests/test_runner.py
python -I -B tests/test_analysis.py
python -I -B engine/hashes.py
```

Each test file ends with `ALL PASS`. `engine/hashes.py` prints a JSON manifest (prompt, pool and source-file hashes); it never overwrites the frozen file. `-I` runs Python isolated (ignores environment variables and the current directory on the path), `-B` stops it writing `__pycache__`. The scripts add the repository root to the path themselves, so run them from the repository root.

### Run one episode with a local model

You need `llama-server` (from llama.cpp) serving the `/v1/chat/completions` HTTP endpoint on `127.0.0.1:8082`, with the model name matching `--model` (the study used `minicpm5-2b` and `qwen3-8b`, Q4_K_M GGUF builds, one model loaded at a time, thinking off).

```
python -I engine/cli.py --model minicpm5-2b --n 5 --arm neutral --dose 0 --seed 1 --out results/smoke
```

Arms: `neutral`, `sham`, `hint_generic`, `hint_named`, `deny_generic`, `deny_named`. `--dose` is the number of bot seats that use the arm (the rest are neutral). `--n` is 5, 10 or 20 seats (the study used 10). The run writes an event log (`.jsonl`), a `.summary.json`, the reply cache (`<out>/cache/`) and `budget.json` into `--out`.

### Run one episode with a hosted model

Needs the `adaption` Python client (`pip install -r requirements.txt`) and a key in the environment. Never put the key in a file or on a command line.

```
# bash / Git Bash
export ADAPTION_API_KEY=...        # your key; do not commit it
python -I engine/cli.py --model deepseek-v4-flash --hosted --n 10 --arm hint_named --dose 2 --seed 1 --out results/smoke_hosted
```

```
# PowerShell
$env:ADAPTION_API_KEY = "..."
python -I engine/cli.py --model deepseek-v4-flash --hosted --n 10 --arm hint_named --dose 2 --seed 1 --out results/smoke_hosted
```

A global limiter keeps all hosted requests at or under 95 per minute and pauses on HTTP 429. Hosted episodes cost real money (the spend is tracked in `budget.json`; soft cap 150 USD, hard cap 160 USD per output folder).

### Run the batch plan

```
python -I engine/batch.py --plan conf --out results/conf                 # the 1,530 confirmatory episodes (hosted + local)
python -I engine/batch.py --plan conf --out results/conf --only local    # local models only (no key)
python -I engine/batch.py --plan conf --out results/conf --only hosted --hosted-workers 4
```

Other plans: `g2` (neutral-arm pilot), `g2hint`, `g2more`. The batch is resumable: rerun the same command and finished episodes are skipped. Do not start a second batch on the same output folder. See `TROUBLESHOOTING.md`.

### Run the analysis

```
python -I bench/g2_summary.py results/conf
python -I -B -c "import sys,json;sys.path.insert(0,'.');from engine import analysis as A;print(json.dumps(A.q3_report(A.load_rows('results/conf')),indent=1,default=str))"
python -I bench/costs.py results/costs.csv
```

The second command prints the four pre-specified contrasts (generic and named hint, generic and named denial, each against neutral) with Holm-adjusted p-values and intervals, and the sham equivalence check. The analysis only reads episode logs, so it needs no key and no server.

## Verify the pre-registration

The plan was frozen in stages, each marked by a git tag:

```
git tag -l
git show plan-freeze --stat
```

| Tag | What was frozen |
|---|---|
| `plan-freeze` | The plan, before the sprint started |
| `prereg-v1` | `prereg/PREREG_v1.md`, after the sprint start and before any experimental run |
| `prereg-v1.1a` | Hashes of the prompt templates, the six paraphrase pools and the rendered observation text, before the first pilot episode |
| `prereg-v1.1b` | Analysis-script hash, engine file hashes, model roster, settings and gate results, before the first confirmatory call |

1. Prompt and pool hashes: `python -I -B engine/hashes.py` prints the current manifest; it should equal `prereg/hashes_v1.1a.json` (it does at the time of writing). `git diff prereg-v1.1a HEAD -- engine/prompts.py engine/bots.py` should print nothing.
2. Engine files at the last tag: `prereg/manifest_v1.1b.json` lists the SHA-256 of each file as committed at `prereg-v1.1b`. Check one with `git show prereg-v1.1b:engine/prompts.py | python -I -B -c "import sys,hashlib;print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())"` and compare. Files changed later differ on purpose; each change is a row in `prereg/DEVIATIONS.md` with the old and new hash prefix.
3. The two hash files were committed after the tags (the allow-list in `.gitignore` had omitted them); see "Pre-sprint files" in `prereg/DEVIATIONS.md`. Their content is unchanged from when the tags were made.

### How the pre-specification and the deviations log work

`prereg/PREREG_v1.md` fixes the design, the outcome definition, the contrasts, the Holm correction, the null margins and the models before the confirmatory data. `prereg/DEVIATIONS.md` is the only place where anything that changed afterwards is recorded. The rule: bug fixes before the first pilot episode are logged; after the prompt hashes, any change to a prompt, configuration value, margin or threshold needs a row marked "touched: yes". Each row says what changed, why, whether it touched the pre-registered analysis, and whether it came before any pilot or confirmatory episode. The log also lists known issues that were disclosed rather than changed. A fix made after the confirmatory data (D-012, parser) is not outcome-blind; the frozen parse is the primary result and the fixed parse is a sensitivity analysis.

## Example episodes

`docs/examples/` holds two full episode logs (one JSON line per event) with their summaries, so you can see the raw format without running anything: `deepseek-v4-flash-N10-neutral0-1001` (no peer hint) and `deepseek-v4-flash-N10-hint_named2-1007` (two peers name the file; an agent writes a quota). Summary fields: `collapsed`, `collapse_round`, `payoff`, `first_llm_read_board`, `first_llm_write_board`, `calls`, `empty_calls`, `board_text`, `llm_seats`, `bot_seats`.

## Figure gallery

Copies of the report figures are in `docs/figures/`.

| Figure | What it shows |
|---|---|
| ![design](docs/figures/figS1_design.svg) | `figS1_design.svg`: the game and the experiment (10 seats, 5 LLM and 5 scripted, hidden board). |
| ![rate by arm](docs/figures/fig1_rate_by_arm.svg) | `fig1_rate_by_arm.svg`: share of episodes with a substantive board write, by peer arm, hosted and local models. |
| ![reads by arm](docs/figures/fig1b_reads_by_arm.svg) | `fig1b_reads_by_arm.svg`: share of episodes with any board read, by arm. |
| ![heatmaps](docs/figures/fig2_heatmaps.svg) | `fig2_heatmaps.svg`: write and read rate by model and arm. |
| ![dose curves](docs/figures/fig3_dose_curves.svg) | `fig3_dose_curves.svg`: write rate against the number of hinting or denying peers. |
| ![told and blind](docs/figures/fig4_told_blind.svg) | `fig4_told_blind.svg`: told and chat-blind cells against neutral and named hint. |
| ![timing](docs/figures/fig5_timing.svg) | `fig5_timing.svg`: round of first board read and first quota write. |
| ![collapse and quota](docs/figures/fig6_collapse_and_quota_timing.svg) | `fig6_collapse_and_quota_timing.svg`: quota-write timing relative to pool collapse. |
| ![pool dynamics](docs/figures/fig7_pool_dynamics.svg) | `fig7_pool_dynamics.svg`: mean pool size per round by arm. |
| ![reliability and cost](docs/figures/fig8_reliability_cost.svg) | `fig8_reliability_cost.svg`: empty calls, parse errors and cost per episode by model. |
| ![forest](docs/figures/figS2_forest.svg) | `figS2_forest.svg`: risk differences versus neutral with confirmatory intervals and null checks. |
| ![funnel](docs/figures/figS3_funnel.svg) | `figS3_funnel.svg`: discovery versus use under a named hint. |
| ![collapse vs quota](docs/figures/figS4_collapse_vs_quota.svg) | `figS4_collapse_vs_quota.svg`: round of collapse against round of first quota write. |
| ![example episode](docs/figures/figS5_example_episode.svg) | `figS5_example_episode.svg`: one annotated episode. |
| ![contagion](docs/figures/figX1_contagion.svg) | `figX1_contagion.svg` (post hoc): board-read rate of non-writers before and after the first write. |
| ![robustness](docs/figures/figX2_robustness.svg) | `figX2_robustness.svg` (post hoc): leave-one-model-out, empty-reply exclusion, equal weights. |
| ![read to write](docs/figures/figX3_read_to_write.svg) | `figX3_read_to_write.svg` (post hoc): later write after a board read, by board state. |

## Limitations

- Scripted peers, a toy resource game and one prompt family: the result says how peer speech shifts discovery and use of a hidden file here, not how deployed agents behave.
- The sham pool is length-matched to the bare hint line but not to what agents actually see in hint rounds, so the sham check is a weaker placebo than pre-registered (deviations log, B1).
- Strict action parsing: malformed `TAKE` lines count as 0, and failed calls become empty replies; one small local model has about 26% of calls without a usable `TAKE` (B2, B3).
- Raw replies are not in the event logs, only parsed events (they exist in the hashed cache).
- Four hosted models have fewer episodes (20 per key cell) than the main model (50); per-model rows are descriptive.
- A parser fix was applied after the confirmatory data (D-012) and is reported only as a sensitivity analysis.

Everything above and the remaining known issues are detailed in `prereg/DEVIATIONS.md` and in the report.

## Prior work

Only the sprint weekend (6-8 November 2026) is the judged work. Pre-existing material: an earlier multi-agent collusion project (a separate, frozen repository, not included here) and the literature review of 73 papers (`papers/`), together with the planning notes in `prep/` written before the sprint started; none of it is experimental code or data of this study. The game engine, scripted peers, prompts, analysis, tests, launch tools, pre-registration, all experiment runs and every figure and table were written or produced during the sprint weekend.

## Citing

See `CITATION.cff`. Kumar, V. (2026). A Hint From a Peer, Not an Instruction: What Makes LLM Agents Open an Unannounced Shared File. https://github.com/Pixiano/Apart-AI-Swarm-Alignment-Hackathon-Nov

## Contact

vatsal8599@gmail.com

## Licence

MIT, see `LICENSE`.
