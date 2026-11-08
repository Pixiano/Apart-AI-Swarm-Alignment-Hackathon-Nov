# Troubleshooting

Everything here comes from the code (`engine/llm.py`, `engine/batch.py`, `engine/cli.py`) and from `prereg/DEVIATIONS.md`. Run all commands from the repository root.

## No API key (or you do not want to use one)

- Tests, the hash check and the analysis never call an API: `python -I -B tests/test_engine.py` and so on, `python -I -B engine/hashes.py`, `python -I bench/g2_summary.py <folder>`.
- Local-model episodes need no key: use `engine/cli.py` without `--hosted`, or `engine/batch.py --only local`.
- Hosted episodes read the key from the environment variable `ADAPTION_API_KEY` (the `adaption` client reads it; the code never logs it). If it is missing, the hosted client fails when it is created or at the first call (exact error depends on the client version). Set it for the current shell only:
  - Git Bash: `export ADAPTION_API_KEY=...`
  - PowerShell: `$env:ADAPTION_API_KEY = "..."`
  - Never write the key into a file, a script or a command line, and keep it out of commits.
- `ModuleNotFoundError: adaption` means the hosted client is not installed. Only `--hosted`, `batch.py` without `--only local`, and `bench/g1_*.py` need it; the tests do not.

## 429 rate limits and the limiter

- All hosted requests share one sliding-window limiter: at most 95 requests in any 60 seconds, for all hosted models together (`llm.Limiter`). On an HTTP 429 the limiter pauses every hosted worker for 60 seconds and the call is retried, up to 6 tries; after that the call raises `hosted call failed after retries`.
- The launch checks measured the limit and a 300-second sustained test through the real wrapper (491 calls in 302 seconds, no 429, no empty reply; deviations log D-008). If you still see 429s, you are probably sharing the key with another process: lower the load (`--hosted-workers 2`) or wait; do not raise the 95 limit.
- Other hosted errors (5xx, network) are not retried by the wrapper. The episode runner turns them into an empty reply and, after one retry, the seat takes 0 for that round. Check the per-episode `empty_calls` count (column `empty%` in `bench/g2_summary.py`) before trusting a run (known issue B2).
- A request that hangs times out after 120 seconds (hosted) or 600 seconds (local).

## Local server not running, or the port is busy

- The local client posts to `http://127.0.0.1:8082/v1/chat/completions` (`llm.local`). A connection refused or `URLError` means no server on 8082. Start `llama-server` on that port with the model you pass in `--model`.
- If port 8082 is taken by another program, stop that program or free the port. The port is a default argument of `llm.local(base=...)` and a constant in `bench/local_sanity.py`; there is no command-line flag for it, so changing the port means editing those lines (and that changes the file hash, so log it as a deviation if you are reproducing the study).
- Check the server is up and which models it lists: open `http://127.0.0.1:8082/v1/models` in a browser, or run `python -I bench/local_sanity.py` (it times a few rounds and writes `results/local_sanity.json`).
- The request sets `chat_template_kwargs: {"enable_thinking": false}`. A server or model that ignores it may return long reasoning text and be slower.

## Memory pressure with large local models

- The study ran the server with one model loaded at a time (`--models-max 1`). `batch.py` therefore orders local jobs model-major: it finishes every episode of one local model before the next model is loaded (deviation D-009). Do not interleave local models by hand; every swap reloads the weights.
- Local episodes run one at a time (`workers = 1`). If the machine swaps to disk or the server is killed for memory, use a smaller quantisation (the study used Q4_K_M builds of a 2B and an 8B model), a smaller context, or close other programs. Then rerun the same batch command: finished episodes are skipped and the cache replays finished calls.
- Changing the model build or quantisation changes the model, so it is not the same experiment.

## Cache location and how to clear it

- Every call is cached on disk at `<out>/cache/<sha256>.json`, where `<out>` is the `--out` folder. The key covers model, temperature, token cap, system prompt, observation, episode id and sample index.
- A cache hit replays the stored reply, makes no API call and costs nothing. This is what makes a rerun after a crash free and reproducible. The cache holds raw model replies, so treat it like data and do not commit it.
- To redo an episode from scratch (new model replies, new cost), delete its `.jsonl`, `.summary.json` and the cache folder (or move the whole `--out` folder aside). Deleting only the log and summary replays the cached replies and reproduces the same episode.
- A cache file truncated by a kill is ignored and re-fetched (a miss); writes are atomic (temp file then rename).

## Resumable batches

- `engine/batch.py` is resumable. An episode with a `.summary.json` is skipped. An episode with a log but no summary is treated as interrupted: the log is renamed `.partial` and the episode is rerun, with the cache replaying the calls that had already finished. Rerun the exact same command.
- `budget.json` in the output folder keeps the running spend across restarts (soft cap 150 USD: no new episode starts; hard cap 160 USD: running episodes abort). The cap counts only the output folder it lives in.
- Do not start two batches on the same output folder: there is no single-instance guard (known issue C4/C5). Two writers can corrupt `costs.csv` and the budget file.
- If the batch was killed between writing a summary and the cost ledger, one row of `costs.csv` can be missing; `budget.json` is the authoritative total (C1, C4/C5).
- `costs.csv` is written next to the output folder (`<out>/../costs.csv`), not inside it.
- To see progress: count `*.summary.json` files in the output folder.

## Windows path quoting

- Quote any path that contains a space: `python -I engine/cli.py --model minicpm5-2b --out "C:\Users\[you]\My Folder\results\smoke"`. In Git Bash use forward slashes or double quotes; in PowerShell use double quotes and `&` before a quoted executable path.
- Keep the repository in a path without exotic characters if you can; `-I` does not change how paths are parsed but a space in the repository path breaks unquoted commands.
- Git may check out text files with CRLF line endings on Windows. The prompt and pool hashes in `engine/hashes.py` normalise line endings, but a raw `sha256sum` of a CRLF working file will not match the manifests. Compare against `git show <tag>:<file>`, which gives the committed (LF) bytes.

## Running with `-I -B`

- `-I` (isolated mode) ignores `PYTHON*` environment variables and does not put the script directory or the current directory on `sys.path`. The repository scripts insert the repository root themselves, so `python -I engine/cli.py ...` works. A one-liner passed with `-c` does not get that, which is why the analysis command starts with `sys.path.insert(0,'.')`.
- `-B` stops Python writing `__pycache__` folders. They are ignored by git anyway, but `-B` keeps the working tree clean for hash checks.
- If `import engine` fails, you are not in the repository root, or you used `-c` without the path line.
- Tests use plain asserts: a failure prints a traceback; success ends with `ALL PASS`.
