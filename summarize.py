"""Wilson 95% intervals and preview coverage per window, from recount.json + bodies.json."""
import json, math, random, statistics
rows = json.load(open('recount.json')); B = json.load(open('bodies.json'))
def wilson(k, n, z=1.96):
    p = k / n; c = (p + z*z/(2*n)) / (1 + z*z/n); h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n); return 100*(c-h), 100*(c+h)
print('window            n  receipt full [95%]   preview | court_ledger full [95%] preview | election full | check full')
for r in rows:
    n = r['n']; f = r['full']; p = r['preview']
    lo, hi = wilson(f['receipt'], n); lo2, hi2 = wilson(f['court_ledger'], n)
    print(f"{r['window']:17s} {n} {f['receipt']:4d} [{lo:4.1f},{hi:4.1f}] {p['receipt']:4d} | {f['court_ledger']:4d} [{lo2:4.1f},{hi2:4.1f}] {p['court_ledger']:4d} | {f['election']:4d} | {f['check']:4d}")
