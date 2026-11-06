"""Run: python -I tests/test_bots.py"""
import os, re, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import bots
from engine.bots import Bot, Ignorer, User
from engine.game import Pool

FILEWORDS = re.compile(r"\b(files?|board|folders?|resources?|paths?|notes?|shared|open|read|write|txt|directory)\b", re.I)


def test_pools():
    for name in ("NEUTRAL", "SHAM", "HINT_GENERIC", "HINT_NAMED", "DENY_GENERIC", "DENY_NAMED"):
        p = getattr(bots, name)
        assert len(p) >= 10 and len(set(p)) == len(p), name
        assert all(len(x.split()) <= 22 for x in p), name                 # about 30 tokens at most
    for name in ("NEUTRAL", "SHAM"):                                       # no file, board, folder, resource or path words
        assert not any(FILEWORDS.search(x) for x in getattr(bots, name)), name
    assert not any("board" in x.lower() for x in bots.HINT_GENERIC + bots.DENY_GENERIC)       # generic never names the file
    assert all("board.txt" in x for x in bots.HINT_NAMED + bots.DENY_NAMED)                   # named always does
    h = statistics.mean(len(x) for x in bots.HINT_GENERIC + bots.HINT_NAMED + bots.DENY_GENERIC + bots.DENY_NAMED)
    s = statistics.mean(len(x) for x in bots.SHAM)
    assert abs(s - h) / h <= 0.20, (s, h)                                  # sham length-matched to hint/denial lines within 20%


def test_timing_and_order():
    b = Bot("hint_named", 1001, 3)
    hint_rounds = [r for r in range(1, 31) if "board.txt" in b.say(r)]
    assert hint_rounds == [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]
    assert b.say(2).split(".")[0].count("board.txt") or "board.txt" in b.say(2)[:80]       # hint line first
    assert b.say(2).startswith(tuple(x[:15] for x in bots.HINT_NAMED))
    assert "board" not in Bot("neutral", 1, 0).say(2).lower() and "board" not in Bot("sham", 1, 0).say(5).lower()
    d = Bot("deny_generic", 7, 2)
    assert any(d.say(r).startswith(x[:15]) for r in (2, 5) for x in bots.DENY_GENERIC)
    for r in range(1, 31):                                                 # every bot says something every round (no silent tell)
        assert Bot("neutral", 1, 0).say(r) and Bot("sham", 1, 0).say(r) and b.say(r)


def test_determinism_and_variety():
    a, b = Bot("hint_generic", 1000, 4), Bot("hint_generic", 1000, 4)
    assert [a.say(r) for r in range(1, 31)] == [b.say(r) for r in range(1, 31)]
    c = Bot("hint_generic", 1001, 4)
    assert [a.say(r) for r in range(1, 31)] != [c.say(r) for r in range(1, 31)]
    assert len({a.say(r) for r in range(1, 31)}) >= 10


def test_takes_and_controls():
    for k in bots.POOLS:
        assert all(Bot(k, 5, 1).take(r) == 1 for r in range(30))
    ig = Ignorer(3, 0)
    assert {ig.take() for _ in range(300)} <= set(range(11)) and len({ig.take() for _ in range(300)}) > 5
    u = User()
    assert u.take("") == 1 and u.take("hello") == 1 and u.take("everyone take 2 each") == 2 and u.take("take 1\ntake 3") == 3
    # plumbing test (18.1): all-User keeps the pool alive 30 rounds; all-Ignorer collapses it; User reads a seeded quota line
    p = Pool(5)
    for r in range(1, 31):
        p.step({s: User().take("take 1 each") for s in range(5)}, r)
    assert not p.collapsed
    p, igs = Pool(5), [Ignorer(9, s) for s in range(5)]
    for r in range(1, 31):
        p.step({s: igs[s].take() for s in range(5)}, r)
    assert p.collapsed


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("ALL PASS")
