"""Exploratory runs E5-E8 (see prereg/EXTRA_PREREG.md). One process, one shared rate limiter, run-time patches only (no frozen engine file edited).
Usage (hosted API key in the environment, never in a file):  python -I -B bench/run_extra.py"""
import json, os, statistics, sys, threading, time   # exploratory runs E5-E8; E7 uses seeds 1021-1060 of two existing cells

WT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # repository root
sys.path.insert(0, WT)
os.chdir(WT)
sys.stdout.reconfigure(encoding="utf-8")
from engine import bots, game, llm
from engine.batch import run_jobs

ROOT = os.path.join(WT, "results", "extra")
os.makedirs(ROOT, exist_ok=True)
BUDGET = llm.Budget(os.path.join(ROOT, "budget.json"), soft=12.0, hard=14.0)   # raw x1.15 uplift is inside Budget; caps are on the uplifted tally
LIMITER, STOP = llm.Limiter(), threading.Event()
DS = "deepseek-v4-flash"


def say(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


def run(exp, jobs, workers=4):
    out = os.path.join(ROOT, exp)
    os.makedirs(out, exist_ok=True)
    call = llm.budgeted(llm.cached(llm.hosted(LIMITER), llm.Cache(os.path.join(out, "cache"))), BUDGET)
    say(f"START {exp}: {len(jobs)} episodes, tally ${BUDGET.spent:.3f}")
    res = run_jobs(jobs, call, out, workers, BUDGET, STOP, say)
    say(f"END {exp}: {len(res)} finished, tally ${BUDGET.spent:.3f}, state {BUDGET.state}")
    return res


def J(model, arm, dose, seeds, prompt="P-MAIN"):
    return [dict(model=model, n=10, arm=arm, dose=dose, seed=s, prompt=prompt) for s in seeds]


# E8 pilot: choose the pool scale by collapse timing only (rule fixed in EXTRA_PREREG.md, candidates amended): median collapse round closest to 12; no collapse counts as 31
def pilot():
    best = None
    for k in (1.25, 1.5, 1.75, 2):
        game.MAX_TAKE = 10 * k
        res = run(f"E8pilot_x{k}", J(DS, "neutral", 0, range(1001, 1005)))
        rounds = [r["collapse_round"] if r["collapsed"] else 31 for r in res]
        med = statistics.median(rounds) if rounds else 99
        say(f"PILOT scale x{k}: collapse rounds {rounds} median {med}")
        if best is None or abs(med - 12) < abs(best[1] - 12):
            best = (k, med)
    game.MAX_TAKE = 10
    say(f"PILOT chose scale x{best[0]} (median collapse round {best[1]})")
    json.dump({"scale": best[0], "median_collapse_round": best[1]}, open(os.path.join(ROOT, "E8_scale.json"), "w"))
    return best[0]


if __name__ == "__main__":
    bots.POOLS["sham_vol"] = (bots.NEUTRAL, bots.SHAM)      # E5: sham line first on hint rounds, then the neutral line (volume and structure matched to the hint arms)
    k = pilot()
    run("E5_sham_vol", J(DS, "sham_vol", 2, range(1001, 1051)))
    run("E6_deny_told", J(DS, "deny_named", 2, range(1001, 1051), "P-TOLD"))
    game.MAX_TAKE = 10 * k
    run("E8_scale", J(DS, "neutral", 0, range(1001, 1031)) + J(DS, "hint_named", 2, range(1001, 1041)))
    game.MAX_TAKE = 10
    run("E7_extend", J("qwen3.5-397b", "hint_generic", 2, range(1021, 1061)) + J("gemma-4-31b-it", "hint_named", 2, range(1021, 1061)))
    say(f"ALL DONE tally ${BUDGET.spent:.3f}")
