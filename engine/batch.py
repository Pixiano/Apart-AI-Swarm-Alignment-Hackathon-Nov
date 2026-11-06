"""Run many episodes. Resumable (an episode with a .summary.json is skipped; a partial log is renamed .partial and the episode rerun, the cache replays
finished calls for free). Hosted and local jobs run concurrently (different resources); hosted episodes in flight = --hosted-workers (the limiter, not the
worker count, sets the speed); local runs one episode at a time. At the soft budget cap no new episode starts; at the hard cap the running ones abort.
  python -I engine/batch.py --plan g2 --out results/g2_pilot
Plans: g2 = neutral arm, N=10, seeds 11-18, 4 hosted + 2 local models (the G2 pilot); g2hint = named hint at dose 5, seeds 21-28; g2more = generic hint, generic denial, named denial at dose 5, seeds 31-38. Every finished episode adds a row to results/costs.csv."""
import argparse, json, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import llm
from engine.cli import build_cfg
from engine.logger import EventLog
from engine.runner import run_episode

PLANS = {"g2": {"hosted": ["deepseek-v4-flash", "qwen3.8-27b", "qwen3.5-397b", "gemma-4-31b-it"], "local": ["minicpm5-2b", "qwen3-8b"],
                "n": 10, "arms": [("neutral", 0)], "seeds": range(11, 19)}}
PLANS["g2more"] = {**PLANS["g2"], "arms": [("hint_generic", 5), ("deny_generic", 5), ("deny_named", 5)], "seeds": range(31, 39)}   # direction and ceiling check
PLANS["g2hint"] = {**PLANS["g2"], "arms": [("hint_named", 5)], "seeds": range(21, 29)}   # strongest hint (named, all 5 bot seats) to see whether hints lift READ/WRITE


def jobs_for(plan, models):
    if "cells" in plan:                      # confirmatory: seed outermost so a stopped run leaves every cell with equal n
        return [dict(model=m, n=10, arm=c[0], dose=c[1], prompt=c[2], blind_one=c[3], seed=1000 + i)
                for i in range(1, max(plan["n_by_model"][x] for x in models) + 1) for m in models if i <= plan["n_by_model"][m]
                for c in (plan["cells"] if m in plan["full_cells"] else plan["key_cells"])]
    return [dict(model=m, n=plan["n"], arm=a, dose=d, seed=s) for m in models for s in plan["seeds"] for a, d in plan["arms"]]


KEY = [("neutral", 0, "P-MAIN", False), ("hint_generic", 2, "P-MAIN", False), ("hint_named", 2, "P-MAIN", False),
       ("deny_generic", 2, "P-MAIN", False), ("deny_named", 2, "P-MAIN", False), ("sham", 2, "P-MAIN", False)]
EXTRA = [("hint_generic", 5, "P-MAIN", False), ("hint_named", 5, "P-MAIN", False), ("deny_generic", 5, "P-MAIN", False), ("deny_named", 5, "P-MAIN", False),
         ("neutral", 0, "P-TOLD", False), ("hint_named", 2, "P-MAIN", True), ("neutral", 0, "P-MAIN", True)]
# prereg v1 / prep/16 section 22: deepseek n=50 on all 13 cells; other hosted n=20 on the 6 key cells; local n=20 on all 13 cells; seeds 1001 and up
PLANS["conf"] = {"hosted": ["deepseek-v4-flash", "qwen3.8-27b", "qwen3.5-397b", "gemma-4-31b-it"], "local": ["minicpm5-2b", "qwen3-8b"],
                 "cells": KEY + EXTRA, "key_cells": KEY, "full_cells": ["deepseek-v4-flash", "minicpm5-2b", "qwen3-8b"],
                 "n_by_model": {"deepseek-v4-flash": 50, "qwen3.8-27b": 20, "qwen3.5-397b": 20, "gemma-4-31b-it": 20, "minicpm5-2b": 20, "qwen3-8b": 20}}


_LEDGER = threading.Lock()


def ledger(out, episode, model, path):
    """Append one row per finished episode to <out>/../costs.csv, summing the API-reported per-call cost from the episode log."""
    calls = cost = 0
    for line in open(path, encoding="utf-8"):
        e = json.loads(line)
        if e["kind"] == "CALL":
            calls += 1; cost += e["cost"] or 0.0
    f = os.path.join(os.path.dirname(os.path.abspath(out)), "costs.csv")
    with _LEDGER:
        new = not os.path.exists(f)
        with open(f, "a", encoding="utf-8") as h:
            if new: h.write("time_ist,run,episode,model,calls,cost_usd\n")
            h.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{os.path.basename(os.path.abspath(out))},{episode},{model},{calls},{cost:.6f}\n")


def run_jobs(jobs, call, out, workers, budget, stop, say=print):
    def one(j):
        if stop.is_set() or budget.state != "ok":
            return None
        cfg = build_cfg(j["model"], j["n"], j["arm"], j["dose"], j["seed"], j.get("prompt", "P-MAIN"), j.get("with_board", True), j.get("blind_one", False))
        base = os.path.join(out, cfg["episode"])
        if os.path.exists(base + ".summary.json"):
            return json.load(open(base + ".summary.json"))
        if os.path.exists(base + ".jsonl"):
            os.replace(base + ".jsonl", base + ".partial")
        log = EventLog(base + ".jsonl")
        try:
            s = run_episode(cfg, call, log)
        except llm.BudgetExceeded:
            stop.set()
            say(f"STOP hard budget cap at {cfg['episode']}")
            return None
        finally:
            log.close()
        s["llm_seats"], s["bot_seats"] = cfg["llm_seats"], sorted(cfg["bots"])
        json.dump(s, open(base + ".summary.json", "w"), indent=1)
        ledger(out, cfg["episode"], j["model"], base + ".jsonl")
        say(f"done {cfg['episode']} collapsed={s['collapsed']} read={s['first_llm_read_board']} write={s['first_llm_write_board']} spent=${budget.spent:.3f}")
        return s
    with ThreadPoolExecutor(workers) as ex:
        return [r for r in ex.map(one, jobs) if r]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True, choices=list(PLANS)); ap.add_argument("--out", required=True)
    ap.add_argument("--hosted-workers", type=int, default=4); ap.add_argument("--only", choices=("hosted", "local"))
    a = ap.parse_args()
    plan = PLANS[a.plan]
    os.makedirs(a.out, exist_ok=True)
    budget, stop, cache = llm.Budget(os.path.join(a.out, "budget.json")), threading.Event(), llm.Cache(os.path.join(a.out, "cache"))
    groups = []
    if a.only in (None, "hosted"):
        groups.append((jobs_for(plan, plan["hosted"]), llm.budgeted(llm.cached(llm.hosted(llm.Limiter()), cache), budget), a.hosted_workers))
    if a.only in (None, "local"):
        groups.append((jobs_for(plan, plan["local"]), llm.budgeted(llm.cached(llm.local(), cache), budget), 1))
    ts = [threading.Thread(target=run_jobs, args=(j, c, a.out, w, budget, stop)) for j, c, w in groups]
    [t.start() for t in ts]; [t.join() for t in ts]
    print("finished; spent $%.4f state=%s" % (budget.spent, budget.state))
