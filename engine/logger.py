"""Append-only JSONL event log. One line per event; flushed immediately so a crash loses nothing."""
import json, time


class EventLog:
    def __init__(self, path):
        self.f = open(path, "a", encoding="utf-8")

    def log(self, episode, rnd, seat, kind, **fields):
        # kind: TAKE SAY LIST READ WRITE ERROR POOL CALL ; file events carry path and is_board
        rec = {"ts": round(time.time(), 3), "episode": episode, "round": rnd, "seat": seat, "kind": kind, **fields}
        self.f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self.f.flush()

    def close(self):
        self.f.close()
