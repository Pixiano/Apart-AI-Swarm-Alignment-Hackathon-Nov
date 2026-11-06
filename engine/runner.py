"""One episode (prep/16 sections 2, 18.1, 19.3). LLM seats act in parallel each round; bot seats are scripted; the pool keeps running after
collapse (zero payoff, chat and files stay live). Empty replies are retried once (new sample index); LLM seats get no information about
which other seats are bots. Returns a summary dict; every event goes to the log."""
import time
from concurrent.futures import ThreadPoolExecutor

from . import prompts
from .game import Pool
from .parser import parse
from .world import Folder, BOARD


def run_episode(cfg, call, log):
    ep, n, rounds, model = cfg["episode"], cfg["n"], cfg.get("rounds", 30), cfg["model"]
    llm, bots, blind = cfg["llm_seats"], cfg["bots"], set(cfg.get("blind", ()))
    cap = cfg.get("cap", 512)
    pool, folder = Pool(n), Folder(cfg.get("n_distractors", 3), cfg.get("with_board", True))
    chat, pending, last = [], {s: [] for s in llm}, {s: (None, None) for s in llm}
    payoff = {s: 0 for s in range(1, n + 1)}
    first = {"read": None, "write": None}
    n_empty = n_calls = 0

    def act(seat, rnd):
        nonlocal n_empty, n_calls
        system = prompts.system_prompt(cfg["prompt"], seat, n, rounds)
        user = prompts.observation(rnd, rounds, pool.pool, pool.cap, *last[seat], pool.collapsed, chat, pending[seat], blind=seat in blind)
        for sample in (0, 1):
            t = time.time()
            try:
                r = call(model, system, user, cap, ep, sample * 1000 + seat * 100 + rnd)  # unique per (seat, round, retry) within the episode
                err = None
            except Exception as e:
                r, err = {"text": "", "in": 0, "out": 0, "cost": 0.0, "reason": 0, "cached": False}, type(e).__name__
            empty = not r["text"].strip()
            log.log(ep, rnd, seat, "CALL", model=model, sample=sample, tokens_in=r["in"], tokens_out=r["out"], reasoning=r.get("reason", 0),
                    cost=r["cost"], cached=r.get("cached", False), empty=empty, sec=round(time.time() - t, 3), error=err)
            n_calls += 1
            if not empty:
                return r["text"]
            n_empty += 1
        log.log(ep, rnd, seat, "ERROR", error="empty_reply")
        return ""

    for rnd in range(1, rounds + 1):
        with ThreadPoolExecutor(max(1, len(llm))) as ex:
            texts = dict(zip(llm, ex.map(lambda s: act(s, rnd), llm)))
        takes, said = {}, []
        for s in llm:
            a = parse(texts[s])
            for e in a["errors"]:
                log.log(ep, rnd, s, "ERROR", error=e)
            takes[s] = a["take"]
            if a["say"]:
                said.append((rnd, s, a["say"]))
            pending[s] = [folder.act(log, ep, rnd, s, k, name, text) for k, name, text in a["files"]]
            for k, name, _ in a["files"]:
                if name == BOARD and k in ("READ", "WRITE") and first[k.lower()] is None and BOARD in folder.files:
                    first[k.lower()] = rnd
        board = folder.files.get(BOARD, "")
        for s, b in bots.items():
            takes[s] = b.take(board)
            t = b.say(rnd)
            if t:
                said.append((rnd, s, t))
        got = pool.step(takes, rnd)
        for s in takes:
            payoff[s] += got[s]
            log.log(ep, rnd, s, "TAKE", asked=takes[s], got=got[s], is_bot=s in bots)
            if s in llm:
                last[s] = (takes[s], got[s])
        for r_, s, t in said:
            log.log(ep, r_, s, "SAY", text=t, is_bot=s in bots)
        chat += said
        log.log(ep, rnd, 0, "POOL", pool=round(pool.pool, 2), collapsed=pool.collapsed)
    return {"episode": ep, "pool_end": pool.pool, "collapsed": pool.collapsed, "collapse_round": pool.collapse_round, "payoff": payoff,
            "first_llm_read_board": first["read"], "first_llm_write_board": first["write"], "calls": n_calls, "empty_calls": n_empty,
            "board_text": folder.files.get(BOARD)}
