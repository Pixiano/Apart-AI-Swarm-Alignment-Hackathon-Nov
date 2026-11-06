"""Analysis skeleton for the headline Q3 (prep/16 17.7, prereg v1). Episode is the unit; outcome = any substantive WRITE to the board by an LLM seat.
Contrast = stratified (by model) risk difference, Mantel-Haenszel-style weights n1*n0/(n1+n0); p by within-stratum permutation (seeded);
intervals by within-stratum bootstrap (seeded). Holm over the 4 Q3 tests. Implementation choices (logged as D-003): the "Holm-adjusted interval" is the
bootstrap interval at level 1 - 0.05/4 (Bonferroni-level, conservative) reported beside Holm-adjusted p; a claim needs p_holm < 0.05 AND that interval to exclude 0.
Null claim: 90% interval of the difference inside +/-0.30. Sham equivalence: point within +/-0.10 and 90% interval within +/-0.30."""
import glob, json, os, random, re, statistics

SUBST = re.compile(r"(?=.*\d)(?=.*\b(?:take|quota|limit|per round|max|leave|share|propose))", re.I | re.S)  # digit AND keyword in the same line
B, SEED = 2000, 12345
Q3 = [("hint_generic", "neutral"), ("hint_named", "neutral"), ("deny_generic", "neutral"), ("deny_named", "neutral")]


def substantive(text):
    return bool(SUBST.search(text or ""))


def episode_rows(events):
    """events of ONE episode -> outcome row."""
    meta = next(e for e in events if e["kind"] == "META")
    llm = set(meta["llm_seats"])
    w = [e for e in events if e["kind"] == "WRITE" and e["seat"] in llm and e.get("is_board")]
    r = [e for e in events if e["kind"] == "READ" and e["seat"] in llm and e.get("is_board")]
    sw = [e for e in w if substantive(e.get("text"))]
    pools = [e for e in events if e["kind"] == "POOL"]
    return {"episode": meta["episode"], "model": meta["model"], "arm": meta["arm"], "dose": meta["dose"], "n": meta["n"], "prompt": meta["prompt"],
            "y": int(bool(sw)), "wrote_any": int(bool(w)), "read_any": int(bool(r)), "first_read": min((e["round"] for e in r), default=None),
            "first_write": min((e["round"] for e in sw), default=None), "share_writers": len({e["seat"] for e in sw}) / max(1, len(llm)),
            "collapsed": int(any(e["collapsed"] for e in pools)), "empty_calls": sum(1 for e in events if e["kind"] == "CALL" and e["empty"])}


def load_rows(folder):
    rows = []
    for f in sorted(glob.glob(os.path.join(folder, "*.jsonl"))):
        ev = [json.loads(x) for x in open(f, encoding="utf-8")]
        if any(e["kind"] == "META" for e in ev):
            rows.append(episode_rows(ev))
    return rows


def _split(rows, arm):
    return [(r["model"], r["y"]) for r in rows if r["arm"] == arm]


def rd(a, b):
    num = den = 0.0
    for s in {x for x, _ in a} & {x for x, _ in b}:
        ya, yb = [y for t, y in a if t == s], [y for t, y in b if t == s]
        w = len(ya) * len(yb) / (len(ya) + len(yb))
        num += w * (statistics.mean(ya) - statistics.mean(yb))
        den += w
    return num / den if den else float("nan")


def _boot(a, b, level, rng):
    ga, gb = {}, {}
    for s, y in a: ga.setdefault(s, []).append(y)
    for s, y in b: gb.setdefault(s, []).append(y)
    out = []
    for _ in range(B):
        ra = [(s, rng.choice(v)) for s, v in ga.items() for _ in v]
        rb = [(s, rng.choice(v)) for s, v in gb.items() for _ in v]
        out.append(rd(ra, rb))
    out.sort()
    lo = (1 - level) / 2
    return out[int(lo * B)], out[min(B - 1, int((1 - lo) * B))]


def _perm_p(a, b, rng):
    obs = abs(rd(a, b))
    strata = {s for s, _ in a} & {s for s, _ in b}
    cnt = 0
    for _ in range(B):
        pa, pb = [], []
        for s in strata:
            ya, yb = [y for t, y in a if t == s], [y for t, y in b if t == s]
            pool = ya + yb
            rng.shuffle(pool)
            pa += [(s, y) for y in pool[:len(ya)]]
            pb += [(s, y) for y in pool[len(ya):]]
        cnt += abs(rd(pa, pb)) >= obs - 1e-12
    return (1 + cnt) / (B + 1)


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - k) * ps[i]))
        adj[i] = run
    return adj


def contrast(rows, arm, ref, level=0.95):
    rng = random.Random(SEED)
    a, b = _split(rows, arm), _split(rows, ref)
    lo, hi = _boot(a, b, level, rng)
    lo90, hi90 = _boot(a, b, 0.90, rng)
    return {"arm": arm, "ref": ref, "n_a": len(a), "n_b": len(b), "est": rd(a, b), "ci_holm_level": (lo, hi), "ci90": (lo90, hi90), "p": _perm_p(a, b, rng)}


def q3_report(rows):
    res = [contrast(rows, a, r, 1 - 0.05 / len(Q3)) for a, r in Q3]
    for c, ph in zip(res, holm([c["p"] for c in res])):
        c["p_holm"] = ph
        c["claim"] = bool(ph < 0.05 and (c["ci_holm_level"][0] > 0 or c["ci_holm_level"][1] < 0))
        c["null_claim"] = bool(c["ci90"][0] >= -0.30 and c["ci90"][1] <= 0.30)
    sh = contrast(rows, "sham", "neutral", 0.90)
    sh["equivalent"] = bool(abs(sh["est"]) <= 0.10 and sh["ci90"][0] >= -0.30 and sh["ci90"][1] <= 0.30)
    return {"q3": res, "sham": sh}
