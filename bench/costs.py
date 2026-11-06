"""Cost tally: python -I bench/costs.py [results/costs.csv]. Ledger rows stay raw (API-reported); the tally is the raw total x1.15 (dashboard reads ~5% higher)."""
import csv, collections, sys

f = sys.argv[1] if len(sys.argv) > 1 else "results/costs.csv"
by = collections.defaultdict(lambda: [0, 0.0])
for r in csv.DictReader(open(f)):
    by[r["run"]][0] += 1; by[r["run"]][1] += float(r["cost_usd"])
for k, (n, c) in by.items():
    print(f"{k:14} {n:>4} eps  raw ${c:.3f}")
raw = sum(c for _, c in by.values())
print(f"TOTAL raw ${raw:.3f}  tally (x1.15) ${raw * 1.15:.3f}  (caps: soft $150, hard $160)")
