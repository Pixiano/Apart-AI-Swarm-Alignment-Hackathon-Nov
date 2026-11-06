"""Run: python -I tests/test_runner.py   (fake LLM, no network)"""
import json, os, sys, tempfile, threading
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import prompts, bots
from engine.bots import Bot, User, Ignorer
from engine.llm import Cache, Limiter, cached
from engine.logger import EventLog
from engine.runner import run_episode


def cfg(**kw):
    base = {"episode": "t1", "seed": 1001, "n": 5, "llm_seats": [1, 2, 3], "bots": {4: Bot("neutral", 1001, 4), 5: Bot("neutral", 1001, 5)},
            "model": "fake", "prompt": "P-MAIN", "cap": 512, "rounds": 30}
    base.update(kw)
    return base


def events(path):
    return [json.loads(x) for x in open(path, encoding="utf-8")]


def fake_polite(model, system, user, cap, ep, sample):
    return {"text": "SAY hi\nTAKE 1", "in": 100, "out": 5, "cost": 0.0, "reason": 0}


def explorer(model, system, user, cap, ep, sample):  # lists, reads the board, writes a quota line
    return {"text": "TAKE 1\nLIST\nREAD board.txt\nWRITE board.txt everyone take 1 each", "in": 100, "out": 20, "cost": 0.0, "reason": 0}


def test_no_board_word_in_main_prompt():
    for k in range(1, 6):
        assert "board" not in prompts.system_prompt("P-MAIN", k, 5).lower() and ".txt" not in prompts.system_prompt("P-MAIN", k, 5)
        assert "board" not in prompts.system_prompt("P-OPEN", k, 5).lower()
    assert "board.txt" in prompts.system_prompt("P-TOLD", 1, 5)
    obs = prompts.observation(3, 30, 47.0, 50, 1, 1, False, [(2, 4, "hello")], ["Files: notes.txt"])
    assert "board" not in obs.lower() and "Pool: 47 of 50" in obs and "agent 4: hello" in obs


def test_window_and_truncation():
    chat = [(r, 4, f"msg{r}") for r in range(1, 10)]
    obs = prompts.observation(9, 30, 40, 50, None, None, False, chat, [])
    assert "msg8" in obs and "msg6" in obs and "msg5" not in obs and "msg9" not in obs          # last 3 rounds only
    assert "(none)" in prompts.observation(9, 30, 40, 50, None, None, False, chat, [], blind=True)  # chat-blind: empty window
    assert len(prompts.trunc("w " * 100).split()) == 30
    for pool in (bots.HINT_GENERIC, bots.HINT_NAMED, bots.DENY_GENERIC, bots.DENY_NAMED):            # a hint or denial line is never cut (19.2)
        for line in pool:
            for kind in ("hint_generic", "hint_named", "deny_generic", "deny_named"):
                full = line + " " + bots.NEUTRAL[0]
                assert prompts.trunc(full).startswith(line)


def test_smoke_episode_and_events():
    d = tempfile.mkdtemp(); p = os.path.join(d, "e.jsonl"); log = EventLog(p)
    s = run_episode(cfg(), explorer, log)
    log.close()
    assert s["first_llm_read_board"] == 1 and s["first_llm_write_board"] == 1 and s["calls"] == 90 and not s["collapsed"]
    ev = events(p)
    kinds = {e["kind"] for e in ev}
    assert {"CALL", "TAKE", "SAY", "POOL", "LIST", "READ", "WRITE"} <= kinds
    assert sum(1 for e in ev if e["kind"] == "TAKE") == 5 * 30 and sum(1 for e in ev if e["kind"] == "CALL") == 90
    assert all(e["is_bot"] for e in ev if e["kind"] == "TAKE" and e["seat"] in (4, 5))
    assert "everyone take 1 each" in s["board_text"]


def test_polite_agents_never_touch_files_and_pool_survives():
    d = tempfile.mkdtemp(); log = EventLog(os.path.join(d, "e.jsonl"))
    s = run_episode(cfg(), fake_polite, log)
    assert s["first_llm_read_board"] is None and s["first_llm_write_board"] is None and not s["collapsed"] and s["pool_end"] == 50.0


def test_collapse_continues_to_round_30():
    greedy = lambda *a: {"text": "TAKE 10\nSAY mine", "in": 1, "out": 1, "cost": 0.0, "reason": 0}
    d = tempfile.mkdtemp(); p = os.path.join(d, "e.jsonl"); log = EventLog(p)
    s = run_episode(cfg(), greedy, log); log.close()
    assert s["collapsed"] and s["collapse_round"] <= 2
    ev = events(p)
    assert max(e["round"] for e in ev if e["kind"] == "POOL") == 30 and s["calls"] == 90        # keeps running, calls unchanged
    late = [e for e in ev if e["kind"] == "TAKE" and e["round"] > 5 and e["seat"] in (1, 2, 3)]
    assert late and all(e["got"] == 0 for e in late)                                            # zero payoff after collapse


def test_empty_reply_retry_and_failure():
    n = {"c": 0}
    def flaky(model, system, user, cap, ep, sample):
        n["c"] += 1
        return {"text": "" if sample < 1000 else "TAKE 1", "in": 1, "out": 1, "cost": 0.0, "reason": 0}  # retry sample index is >= 1000
    d = tempfile.mkdtemp(); p = os.path.join(d, "e.jsonl"); log = EventLog(p)
    s = run_episode(cfg(rounds=3), flaky, log); log.close()
    assert s["calls"] == 18 and s["empty_calls"] == 9 and not any(e["kind"] == "ERROR" for e in events(p))
    dead = lambda *a: (_ for _ in ()).throw(RuntimeError("boom"))
    d = tempfile.mkdtemp(); p = os.path.join(d, "e.jsonl"); log = EventLog(p)
    s = run_episode(cfg(rounds=2), dead, log); log.close()
    ev = events(p)
    assert any(e["kind"] == "ERROR" and e["error"] == "empty_reply" for e in ev) and any(e.get("error") == "RuntimeError" for e in ev if e["kind"] == "CALL")


def test_no_board_arm_and_blind_target():
    d = tempfile.mkdtemp(); p = os.path.join(d, "e.jsonl"); log = EventLog(p)
    s = run_episode(cfg(with_board=False, rounds=3), explorer, log); log.close()
    assert s["first_llm_read_board"] is None and s["board_text"] is None
    assert any(e["kind"] == "ERROR" and e["error"] == "no_such_file" for e in events(p))


def test_cache():
    c = Cache(tempfile.mkdtemp()); n = {"c": 0}
    def real(model, system, user, cap, ep, sample):
        n["c"] += 1
        return {"text": f"TAKE {n['c']}", "in": 1, "out": 1, "cost": 0.0, "reason": 0}
    f = cached(real, c)
    a = f("m", "s", "u", 512, "e1", 0); b = f("m", "s", "u", 512, "e1", 0)
    assert n["c"] == 1 and b["cached"] and a["text"] == b["text"]            # resume replays exactly, zero new calls
    x = f("m", "s", "u", 512, "e2", 0)
    assert n["c"] == 2 and x["text"] != a["text"]                            # same prompt, other episode: independent reply
    assert f("m", "s", "u", 512, "e1", 1)["text"] != a["text"] and n["c"] == 3


def test_limiter():
    t = {"now": 0.0}
    clock = lambda: t["now"]
    def sleep(x): t["now"] += x
    L = Limiter(max_calls=5, window=60.0, clock=clock, sleep=sleep)
    for _ in range(5):
        L.acquire()
    assert t["now"] == 0.0
    L.acquire()                                                              # the 6th waits for the window to clear
    assert t["now"] >= 60.0 - 1e-6
    t["now"] = 1000.0; L.stamps = []; L.pause(60); L.acquire()               # a 429 pause blocks everything
    assert t["now"] >= 1060.0 - 1e-6 and L.n429 == 1


def test_parallel_calls_and_user_bot():
    seen = {"max": 0, "now": 0}; lock = threading.Lock()
    def slow(model, system, user, cap, ep, sample):
        with lock:
            seen["now"] += 1; seen["max"] = max(seen["max"], seen["now"])
        import time; time.sleep(0.05)
        with lock:
            seen["now"] -= 1
        return {"text": "TAKE 1", "in": 1, "out": 1, "cost": 0.0, "reason": 0}
    d = tempfile.mkdtemp(); log = EventLog(os.path.join(d, "e.jsonl"))
    run_episode(cfg(rounds=2), slow, log)
    assert seen["max"] == 3                                                  # all LLM seats of a round run in parallel
    allbots = cfg(llm_seats=[], bots={i: User() for i in range(1, 6)}, rounds=30)
    assert not run_episode(allbots, fake_polite, log)["collapsed"]
    ign = cfg(llm_seats=[], bots={i: Ignorer(1, i) for i in range(1, 6)}, rounds=30)
    assert run_episode(ign, fake_polite, log)["collapsed"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
    print("ALL PASS")
