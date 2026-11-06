"""LLM access: global rate limiter (prep/16 section 22), disk reply cache (key includes episode and sample index, 17.4),
hosted client (thinking off, key from env only) and local llama-server client (thinking off).
Every client call returns {"text","in","out","cost","reason","cached"}."""
import hashlib, json, os, threading, time, urllib.request

TEMP, MAX_OUT = 0.7, 512


class Limiter:
    """Sliding window: at most max_calls requests in any `window` seconds, for ALL hosted models together. 429 -> pause everything."""

    def __init__(self, max_calls=95, window=60.0, clock=time.monotonic, sleep=time.sleep):
        self.max, self.window, self.clock, self.sleep = max_calls, window, clock, sleep
        self.stamps, self.blocked_until, self.lock, self.n429 = [], 0.0, threading.Lock(), 0

    def acquire(self):
        while True:
            with self.lock:
                now = self.clock()
                self.stamps = [t for t in self.stamps if now - t < self.window]
                wait = max(self.blocked_until - now, (self.stamps[0] + self.window - now) if len(self.stamps) >= self.max else 0)
                if wait <= 0:
                    self.stamps.append(now)
                    return
            self.sleep(min(wait, 1.0))

    def pause(self, seconds=60.0):
        with self.lock:
            self.blocked_until = max(self.blocked_until, self.clock() + seconds)
            self.n429 += 1


class Cache:
    def __init__(self, folder):
        self.dir = folder
        os.makedirs(folder, exist_ok=True)

    def key(self, model, system, user, cap, episode, sample):
        raw = json.dumps([model, TEMP, cap, system, user, episode, sample], ensure_ascii=False)
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, k):
        p = os.path.join(self.dir, k + ".json")
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None

    def put(self, k, rec):
        json.dump(rec, open(os.path.join(self.dir, k + ".json"), "w", encoding="utf-8"))


def cached(call, cache):
    """Wrap call(model, system, user, cap, episode, sample); a hit replays the stored reply and makes zero API calls."""
    def f(model, system, user, cap, episode, sample):
        k = cache.key(model, system, user, cap, episode, sample)
        hit = cache.get(k)
        if hit is not None:
            return {**hit, "cached": True}
        rec = call(model, system, user, cap, episode, sample)
        cache.put(k, rec)
        return {**rec, "cached": False}
    return f


def hosted(limiter, tries=6):
    from adaption import Adaption  # key from env ADAPTION_API_KEY, never logged
    client = Adaption(max_retries=0, timeout=120)

    def call(model, system, user, cap, episode, sample):
        for _ in range(tries):
            limiter.acquire()
            try:
                r = client.responses.create(model=model, instructions=system, input=user, max_output_tokens=cap, temperature=TEMP,
                                            extra_body={"reasoning": {"effort": "none"}})
                u = r.usage.model_dump()
                return {"text": r.output_text or "", "in": u["input_tokens"], "out": u["output_tokens"], "cost": u.get("cost") or 0.0,
                        "reason": (u.get("output_tokens_details") or {}).get("reasoning_tokens") or 0}
            except Exception as e:
                if getattr(e, "status_code", None) == 429:
                    limiter.pause(60)
                    continue
                raise
        raise RuntimeError("hosted call failed after retries")
    return call


def local(base="http://127.0.0.1:8082"):
    def call(model, system, user, cap, episode, sample):
        body = json.dumps({"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                           "max_tokens": cap, "temperature": TEMP, "chat_template_kwargs": {"enable_thinking": False}}).encode()
        r = json.load(urllib.request.urlopen(urllib.request.Request(base + "/v1/chat/completions", body, {"Content-Type": "application/json"}), timeout=600))
        return {"text": r["choices"][0]["message"].get("content") or "", "in": r["usage"]["prompt_tokens"], "out": r["usage"]["completion_tokens"],
                "cost": 0.0, "reason": 0}
    return call
