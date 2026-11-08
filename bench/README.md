# bench/

Launch checks and cost/summary tools. Run from the repo root with `python -I bench/<script>`. Scripts that call the hosted API read the key from the environment and never print it; outputs go to `results/`.

| Script | What it measures |
|---|---|
| `g1_api.py` | Hosted API check: 32 parallel requests per model, 429 count, metered cost. |
| `g1_limit.py` | Rate-limit probe: bucket size and refill, from 429 headers. |
| `g1_sustained.py` | Sustained load (300 s) through the real wrapper and limiter. Pass = zero 429 and under 5% empty replies. Hashed in `prereg/manifest_v1.1b.json`. |
| `g2_summary.py` | Pilot summary per model: READ and WRITE rates, collapse, empty replies, calls, cost. |
| `local_sanity.py` | Seconds per round for the local roster models on the local server. |
| `costs.py` | Cost tally from `results/costs.csv` (raw total x1.15). |
