"""Rate-limit probe: bucket size and refill. Reads 429 headers (names only, never the key). Writes results/g1_limit.jsonl."""
import json, os, time
from concurrent.futures import ThreadPoolExecutor
from adaption import Adaption

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "g1_limit.jsonl")
c = Adaption(max_retries=0, timeout=60)
log = []

def one(i):
    t = time.time()
    try:
        c.responses.create(model="deepseek-v4-flash", instructions="Reply with one word.", input="Say hi.", max_output_tokens=16,
                           extra_body={"reasoning": {"effort": "none"}})
        return (t, 200, None)
    except Exception as e:
        h = {}
        try:
            h = {k: v for k, v in e.response.headers.items() if any(s in k.lower() for s in ("rate", "retry", "limit", "remaining", "reset"))}
            body = e.response.text[:300]
        except Exception:
            body = str(e)[:200]
        return (t, getattr(e, "status_code", type(e).__name__), {"headers": h, "body": body})

def burst(n, par, label):
    t0 = time.time()
    with ThreadPoolExecutor(par) as ex:
        rs = list(ex.map(one, range(n)))
    ok = sum(1 for r in rs if r[1] == 200)
    first429 = next((r[2] for r in rs if r[1] == 429), None)
    row = {"label": label, "t": time.strftime("%H:%M:%S"), "n": n, "ok": ok, "n429": sum(1 for r in rs if r[1] == 429),
           "other": [str(r[1]) for r in rs if r[1] not in (200, 429)][:3], "sec": round(time.time() - t0, 1), "first429": first429}
    print(json.dumps(row), flush=True)
    open(OUT, "a").write(json.dumps(row) + "\n")

time.sleep(70)                       # let the window clear
burst(200, 32, "A cold burst of 200")   # bucket size
time.sleep(10)
burst(20, 10, "B 10 s later")           # partial refill?
time.sleep(30)
burst(20, 10, "C 40 s after A")
time.sleep(30)
burst(20, 10, "D 70 s after A")
