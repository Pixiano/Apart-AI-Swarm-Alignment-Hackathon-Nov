"""Run one episode. Example (local server on 8082):
  python -I engine/cli.py --model minicpm5-2b --n 5 --arm neutral --dose 0 --seed 1 --out results/smoke
arm: neutral | sham | hint_generic | hint_named | deny_generic | deny_named; dose = number of bot seats using that arm (rest are Neutral).
Seats are shuffled by seed, so the LLM seats cannot tell which seats are bots. Hosted: add --hosted (uses ADAPTION_API_KEY, 95 requests/min limiter)."""
import argparse, json, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import llm
from engine.bots import Bot
from engine.logger import EventLog
from engine.runner import run_episode

N_LLM = {5: 3, 10: 5, 20: 5}


def build_cfg(model, n, arm, dose, seed, prompt="P-MAIN", with_board=True, blind_one=False):
    seats = list(range(1, n + 1))
    random.Random(f"{seed}-roles").shuffle(seats)
    llm_seats, bot_seats = sorted(seats[:N_LLM[n]]), sorted(seats[N_LLM[n]:])
    bots = {s: Bot(arm if i < dose else "neutral", seed, s) for i, s in enumerate(bot_seats)}
    return {"episode": f"{model}-N{n}-{arm}{dose}-{seed}", "seed": seed, "n": n, "llm_seats": llm_seats, "bots": bots, "model": model,
            "prompt": prompt, "cap": llm.MAX_OUT, "with_board": with_board, "blind": [llm_seats[0]] if blind_one else []}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True); ap.add_argument("--n", type=int, default=5, choices=(5, 10, 20))
    ap.add_argument("--arm", default="neutral"); ap.add_argument("--dose", type=int, default=0)
    ap.add_argument("--seed", type=int, default=1); ap.add_argument("--prompt", default="P-MAIN")
    ap.add_argument("--no-board", action="store_true"); ap.add_argument("--blind-one", action="store_true")
    ap.add_argument("--hosted", action="store_true"); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    cfg = build_cfg(a.model, a.n, a.arm, a.dose, a.seed, a.prompt, not a.no_board, a.blind_one)
    call = llm.cached(llm.hosted(llm.Limiter()) if a.hosted else llm.local(), llm.Cache(os.path.join(a.out, "cache")))
    log = EventLog(os.path.join(a.out, cfg["episode"] + ".jsonl"))
    s = run_episode(cfg, call, log)
    log.close()
    s["llm_seats"], s["bot_seats"] = cfg["llm_seats"], sorted(cfg["bots"])
    json.dump(s, open(os.path.join(a.out, cfg["episode"] + ".summary.json"), "w"), indent=1)
    print(json.dumps({k: s[k] for k in ("episode", "pool_end", "collapsed", "collapse_round", "first_llm_read_board", "first_llm_write_board", "calls", "empty_calls")}))
