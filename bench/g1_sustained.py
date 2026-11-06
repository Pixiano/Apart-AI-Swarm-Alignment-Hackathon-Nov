"""G1 final (prereg v1): sustained load through the real hosted wrapper and limiter, 300 s, deepseek-v4-flash. Pass = zero 429 and empty replies under 5%.
Run: python -I bench/g1_sustained.py   (key from env, never printed). Writes results/g1_sustained.json."""
import json, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine import llm

SECONDS, WORKERS = 300, 16
lim = llm.Limiter()
call = llm.hosted(lim)
stop = time.time() + SECONDS
n = empty = err = 0
lock = threading.Lock()


def worker(_):
    global n, empty, err
    while time.time() < stop:
        try:
            r = call("deepseek-v4-flash", "Reply with one short sentence.", "Say something about a river.", 64, "g1", 0)
            bad = not r["text"].strip()
            e = 0
        except Exception:
            bad, e = False, 1
        with lock:
            n += 1; empty += bad; err += e


t0 = time.time()
with ThreadPoolExecutor(WORKERS) as ex:
    list(ex.map(worker, range(WORKERS)))
sec = time.time() - t0
res = {"seconds": round(sec), "calls": n, "per_min": round(n / sec * 60, 1), "n429": lim.n429, "empty": empty, "errors": err,
       "pass": lim.n429 == 0 and empty / max(1, n) < 0.05 and err == 0}
print(json.dumps(res))
json.dump(res, open(os.path.join(ROOT, "results", "g1_sustained.json"), "w"))
