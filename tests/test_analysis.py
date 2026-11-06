"""Run: python -I tests/test_analysis.py   (synthetic data: a planted effect and a planted null must both be recovered)"""
import os, random, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import analysis as A
from engine.bots import Bot
from engine.logger import EventLog
from engine.runner import run_episode


def synth(effects, n=50, models=("m1", "m2"), base=0.2, seed=7):
    rng = random.Random(seed)
    rows = []
    for m in models:
        for arm, p in [("neutral", base), ("sham", base)] + list(effects.items()):
            rows += [{"model": m, "arm": arm, "y": int(rng.random() < p)} for _ in range(n)]
    return rows


def test_substantive_regex():
    for ok in ("everyone take 1 each", "quota 1 per round", "limit: 2", "I propose we all leave 3"):
        assert A.substantive(ok), ok
    for bad in ("hello", "take it easy", "we should share", "round 5", ""):
        assert not A.substantive(bad), bad


def test_holm():
    assert A.holm([0.01, 0.04, 0.03, 0.5]) == [0.04, 0.09, 0.09, 0.5]          # step-down, monotone
    assert max(A.holm([0.2, 0.2])) == 0.4


def test_planted_effect_and_null_recovered():
    rows = synth({"hint_named": 0.6, "hint_generic": 0.2, "deny_named": 0.2, "deny_generic": 0.2})   # +0.40 effect in hint_named only
    r = A.q3_report(rows)
    by = {c["arm"]: c for c in r["q3"]}
    h = by["hint_named"]
    assert h["claim"] and abs(h["est"] - 0.40) < 0.15 and h["p_holm"] < 0.05, h        # planted effect: claimed, size near 0.40
    for k in ("hint_generic", "deny_named", "deny_generic"):
        assert not by[k]["claim"], (k, by[k])                                            # planted nulls: no claim
    assert by["deny_named"]["null_claim"] and by["deny_generic"]["null_claim"]           # nulls: 90% interval inside +/-0.30
    assert r["sham"]["equivalent"] or abs(r["sham"]["est"]) < 0.15                       # sham (planted null) behaves like neutral


def test_low_power_gives_no_null_claim():
    rows = synth({"hint_named": 0.2, "hint_generic": 0.2, "deny_named": 0.2, "deny_generic": 0.2}, n=8, models=("m1",))
    c = {x["arm"]: x for x in A.q3_report(rows)["q3"]}["deny_named"]
    assert not c["claim"] and not c["null_claim"], c                                     # n=8: interval too wide to claim a null


def test_pipeline_from_event_logs():
    d = tempfile.mkdtemp()
    def agent(text):
        return lambda m, s, u, cap, ep, smp: {"text": f"TAKE 1\nREAD board.txt\nWRITE board.txt {text}", "in": 1, "out": 1, "cost": 0.0, "reason": 0}
    for name, text in (("a", "everyone take 1 each round"), ("b", "hello friends")):
        cfg = {"episode": name, "seed": 1, "n": 5, "llm_seats": [1, 2, 3], "bots": {4: Bot("neutral", 1, 4), 5: Bot("neutral", 1, 5)},
               "model": "fake", "prompt": "P-MAIN", "rounds": 4, "arm": "neutral", "dose": 0}
        log = EventLog(os.path.join(d, name + ".jsonl")); run_episode(cfg, agent(text), log); log.close()
    rows = {r["episode"]: r for r in A.load_rows(d)}
    assert rows["a"]["y"] == 1 and rows["a"]["first_write"] == 1 and rows["a"]["share_writers"] == 1.0 and rows["a"]["read_any"] == 1
    assert rows["b"]["y"] == 0 and rows["b"]["wrote_any"] == 1                            # wrote, but not substantive: primary outcome is 0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
    print("ALL PASS")
