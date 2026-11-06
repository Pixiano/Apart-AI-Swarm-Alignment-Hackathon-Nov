"""G1 hosted API check (sprint 2026-11-06). Key only from env ADAPTION_API_KEY; never printed.
32 parallel requests per model, thinking off, 429 counted, metered cost from usage.cost. Writes results/g1_api.jsonl."""
import json, os, statistics, sys, time
from concurrent.futures import ThreadPoolExecutor
from adaption import Adaption

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "g1_api.jsonl")
CAP_USD = 2.0
c = Adaption(max_retries=0, timeout=90)
INSTR = "You are a player in a shared-resource game. Reply with one short action line."
INP = "History: " + " ".join(["player 3 said the pool looks fine and took 2 units"] * 40) + "\nWhat do you do this round?"
spent = 0.0

def one(model):
    global spent
    if spent >= CAP_USD:
        return {"ok": 0, "status": "capped"}
    t = time.time()
    try:
        r = c.responses.create(model=model, instructions=INSTR, input=INP, max_output_tokens=512, temperature=0.7,
                               extra_body={"reasoning": {"effort": "none"}})
        u = r.usage.model_dump()
        spent += u.get("cost") or 0
        return {"ok": 1, "lat": time.time() - t, "out": u["output_tokens"], "in": u["input_tokens"],
                "reason": (u.get("output_tokens_details") or {}).get("reasoning_tokens") or 0,
                "cost": u.get("cost") or 0, "empty": not (r.output_text or "").strip()}
    except Exception as e:
        return {"ok": 0, "status": getattr(e, "status_code", type(e).__name__), "lat": time.time() - t}

def run(model, n, par):
    t0 = time.time()
    with ThreadPoolExecutor(par) as ex:
        rs = list(ex.map(lambda _: one(model), range(n)))
    wall = time.time() - t0
    ok = [r for r in rs if r["ok"]]
    errs = {}
    for r in rs:
        if not r["ok"]:
            errs[str(r["status"])] = errs.get(str(r["status"]), 0) + 1
    row = {"t": time.strftime("%H:%M:%S"), "model": model, "n": n, "par": par, "ok": len(ok), "errors": errs,
           "calls_per_s": round(len(ok) / wall, 2), "lat_med": round(statistics.median(r["lat"] for r in ok), 2) if ok else None,
           "lat_p95": round(sorted(r["lat"] for r in ok)[max(0, int(len(ok) * .95) - 1)], 2) if ok else None,
           "empty": sum(r["empty"] for r in ok), "mean_in": round(statistics.mean(r["in"] for r in ok)) if ok else None,
           "mean_out": round(statistics.mean(r["out"] for r in ok), 1) if ok else None,
           "mean_reason": round(statistics.mean(r["reason"] for r in ok), 1) if ok else None,
           "mean_cost": round(statistics.mean(r["cost"] for r in ok), 7) if ok else None, "spent_usd": round(spent, 4)}
    print(json.dumps(row), flush=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "a").write(json.dumps(row) + "\n")

if __name__ == "__main__":
    for model, n, par in (("deepseek-v4-flash", 96, 32), ("qwen3.8-27b", 96, 32), ("gemma-4-31b-it", 96, 32), ("qwen3.5-397b", 32, 16), ("glm-5.2", 4, 4)):
        run(model, n, par)
        time.sleep(15)  # gap so a per-user burst limit is attributable to one model
