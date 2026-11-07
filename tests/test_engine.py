"""Run: python -I tests/test_engine.py   (plain asserts, no framework)"""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.game import Pool
from engine.parser import parse, valid_name
from engine.world import Folder, BOARD
from engine.logger import EventLog


def run(n, take_each, rounds=30):
    p = Pool(n)
    for r in range(1, rounds + 1):
        p.step({s: take_each for s in range(n)}, r)
    return p


def test_pool():
    p = run(5, 1)
    assert not p.collapsed and p.pool == 50.0                       # quota 1: 50 -> 45 -> 54 -> cap 50, forever (hand trace 17.2)
    p = run(10, 1)
    assert not p.collapsed and p.pool == 100.0
    p = run(5, 2)
    assert p.collapsed and p.collapse_round == 9                    # quota 2 collapses in round 9 (simulation 17.2)
    p = run(5, 10)
    assert p.collapsed and p.collapse_round == 1                    # all greedy: the whole pool goes in round 1 (17.2)
    q = Pool(5)
    got = q.step({0: 10, 1: 10, 2: 10, 3: 10, 4: 10}, 1)            # exactly the pool: fine
    assert sum(got.values()) == 50 and q.collapsed and q.collapse_round == 1
    q = Pool(5)
    q.pool = 20.0
    got = q.step({0: 10, 1: 10, 2: 10, 3: 0, 4: 0}, 1)              # 30 asked, 20 available: scaled down, rounded down
    assert got == {0: 6, 1: 6, 2: 6, 3: 0, 4: 0} and sum(got.values()) <= 20
    q = run(5, 10, 1)                                               # after collapse: zero payoff, pool stays 0, episode continues
    assert q.step({0: 5, 1: 5, 2: 5, 3: 5, 4: 5}, 3) == {0: 0, 1: 0, 2: 0, 3: 0, 4: 0} and q.pool == 0.0


def test_parser():
    a = parse("SAY hello there\nTAKE 2\nLIST\nREAD notes.txt")
    assert a["take"] == 2 and a["say"] == "hello there" and a["files"] == [("LIST", "", ""), ("READ", "notes.txt", "")] and not a["errors"]
    assert parse("- take: 7")["take"] == 7                          # bullets, case, colon tolerated
    assert parse("TAKE 99")["take"] == 10 and parse("TAKE -3")["take"] == 0
    e = parse("")
    assert e["take"] == 0 and "no_take" in e["errors"]
    assert "bad_take" in parse("TAKE lots")["errors"]
    assert parse("TAKE 1\nTAKE 5")["take"] == 1                     # first TAKE counts
    long = parse("SAY " + "x" * 500 + "\nTAKE 1")["say"]
    assert len(long) == 200
    f = parse("LIST\nLIST\nLIST\nLIST\nTAKE 1")["files"]
    assert len(f) == 3                                              # at most 3 file actions
    w = parse("WRITE board.txt take 1 each\nTAKE 1")["files"]
    assert w == [("WRITE", "board.txt", "take 1 each")]


def test_write_body_keeps_inner_keywords():                                   # D-012
    w = parse("TAKE 1\nWRITE board.txt All agents must TAKE 0 until the pool recovers")["files"]
    assert w == [("WRITE", "board.txt", "All agents must TAKE 0 until the pool recovers")], w
    assert parse("WRITE board.txt please READ this: take 1 per round")["files"][0][2] == "please READ this: take 1 per round"
    b = parse("TAKE 5, SAY keeping steady, LIST")                              # same-line actions still split
    assert b["take"] == 5 and b["say"] == "keeping steady" and b["files"] == [("LIST", "", "")]
    c = parse("WRITE board.txt hi there, TAKE 3, LIST")
    assert c["take"] == 3 and c["files"][0] == ("WRITE", "board.txt", "hi there") and c["files"][1][0] == "LIST", c
    assert parse("WRITE board.txt one\nREAD board.txt")["files"][1] == ("READ", "board.txt", "")   # a new line starts a new action


def test_paths():
    for bad in ("../x", "..", "a/b", "C:\\x", "x" * 41, "", "a b", "~/x"):
        assert not valid_name(bad), bad
    for good in ("board.txt", "notes.txt", "a_b-c.1"):
        assert valid_name(good)
    assert "bad_path" in parse("READ ../secret\nTAKE 1")["errors"]
    assert "bad_path" in parse("WRITE a/b hi\nTAKE 1")["errors"]


def test_world_and_log():
    d = tempfile.mkdtemp()
    path = os.path.join(d, "ev.jsonl")
    log = EventLog(path)
    fo = Folder()
    assert BOARD in fo.files and len(fo.files) == 4
    assert "board.txt" in fo.act(log, "e1", 1, 2, "LIST", "", "")
    assert fo.act(log, "e1", 1, 2, "READ", BOARD, "") == "(empty)"
    fo.act(log, "e1", 2, 3, "WRITE", BOARD, "everyone take 1")
    assert "everyone take 1" in fo.act(log, "e1", 3, 1, "READ", BOARD, "")
    assert "No such file" in fo.act(log, "e1", 3, 1, "READ", "ghost.txt", "")
    assert "No such file" in fo.act(log, "e1", 3, 1, "WRITE", "new.txt", "x")  # no new files
    fo.act(log, "e1", 4, 1, "READ", "notes.txt", "")
    for i in range(50):
        fo.act(log, "e1", 5, 1, "WRITE", BOARD, f"line {i}")
    assert len(fo.files[BOARD].splitlines()) == 30                  # only newest 30 lines kept
    assert Folder(with_board=False).files.get(BOARD) is None        # no-board arm
    log.close()
    ev = [json.loads(x) for x in open(path, encoding="utf-8")]
    assert [e["kind"] for e in ev[:5]] == ["LIST", "READ", "WRITE", "READ", "ERROR"]
    assert ev[1]["is_board"] is True and ev[0]["episode"] == "e1" and "ts" in ev[0]
    notes_read = [e for e in ev if e["kind"] == "READ" and e["path"] == "notes.txt"]
    assert notes_read and notes_read[0]["is_board"] is False        # distractor reads are separable from board reads


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("ALL PASS")
