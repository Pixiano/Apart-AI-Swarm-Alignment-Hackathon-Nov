"""Local sanity pass (sprint 2026-11-06): seconds per round for the 2 roster models on the running llama-server (real mode, port 8082).
Per round: N_LLM parallel calls, ~3k-token shared history + short agent suffix, reply cap 60, thinking off. Rounds 2-5 mean (round 1 warms the cache).
Writes results/local_sanity.json. Episodes/h = 3600 / (30 x s per round)."""
import json, os, statistics, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = "http://127.0.0.1:8082/v1/chat/completions"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "local_sanity.json")
SYS = "You are a player in a shared-resource game. Reply with one short action line."
HIST = " ".join(f"Round {i}: player {i % 5} said the pool looks fine and took {i % 3 + 1} units." for i in range(150))  # about 3k tokens

def call(model, agent, rnd):
    body = json.dumps({"model": model, "messages": [{"role": "system", "content": SYS},
        {"role": "user", "content": f"History: {HIST}\nYou are agent {agent}. Round {rnd}. What do you do this round?"}],
        "max_tokens": 60, "temperature": 0.7, "chat_template_kwargs": {"enable_thinking": False}}).encode()
    t = time.time()
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(URL, body, {"Content-Type": "application/json"}), timeout=300))
        txt = r["choices"][0]["message"].get("content") or ""
        return {"ok": 1, "lat": time.time() - t, "empty": not txt.strip(), "ptok": r["usage"]["prompt_tokens"]}
    except Exception as e:
        return {"ok": 0, "lat": time.time() - t, "err": str(e)[:80]}

res = {}
for model in ("minicpm5-2b", "qwen3-8b"):
    call(model, 0, 0)  # load
    for n_llm in (3, 5):
        secs, bad, empty = [], 0, 0
        for rnd in range(1, 6):
            t = time.time()
            with ThreadPoolExecutor(n_llm) as ex:
                rs = list(ex.map(lambda a: call(model, a, rnd), range(n_llm)))
            if rnd >= 2:
                secs.append(time.time() - t)
            bad += sum(1 for r in rs if not r["ok"]); empty += sum(r.get("empty", 0) for r in rs)
        s = statistics.mean(secs)
        res[f"{model}_llm{n_llm}"] = {"s_per_round": round(s, 2), "episodes_per_h": round(3600 / (30 * s), 1), "failed": bad, "empty": empty}
        print(model, n_llm, res[f"{model}_llm{n_llm}"], flush=True)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(res, open(OUT, "w"), indent=1)
