"""G2 pilot summary per model: READ and WRITE rates of the neutral arm, collapse, empty replies, calls, cost. python -I bench/g2_summary.py results/g2_pilot"""
import glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine import analysis

folder = sys.argv[1]
rows = analysis.load_rows(folder)
cost = {}
for f in glob.glob(os.path.join(folder, "*.jsonl")):
    for line in open(f, encoding="utf-8"):
        e = json.loads(line)
        if e["kind"] == "CALL":
            m = cost.setdefault(e.get("model"), [0, 0.0, 0])
            m[0] += 1; m[1] += 0.0 if e.get("cached") else e["cost"]; m[2] += e["empty"]   # replayed (cached) calls were paid in an earlier run
print(f"{'model':20} {'eps':>3} {'READ%':>6} {'WRITE%':>7} {'SUBST%':>7} {'collapse%':>9} {'calls':>6} {'empty%':>7} {'cost$':>7}")
for m in sorted({r["model"] for r in rows}):
    r = [x for x in rows if x["model"] == m]
    c = cost.get(m, [0, 0.0, 0])
    p = lambda k: 100 * sum(x[k] for x in r) / len(r)
    print(f"{m:20} {len(r):>3} {p('read_any'):>6.0f} {p('wrote_any'):>7.0f} {p('y'):>7.0f} {p('collapsed'):>9.0f} {c[0]:>6} {100 * c[2] / max(1, c[0]):>7.1f} {c[1]:>7.3f}")
