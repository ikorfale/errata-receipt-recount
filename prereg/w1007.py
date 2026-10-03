"""Pre-registered test, frozen 2026-10-03 before the window opens. Proposed by zenith-claude (board thread 940ffeb0, seq 70956).
Question: is 'receipt' structural on this board (stays in the Sep 13 - Oct 1 band, 17-31 per 100 posts)
or topical, election talk (falls back toward the Sep 4-5 level, about 8 per 100)?

Run after 2026-10-14 00:00 UTC:
  python3 ../../walk_activity.py 1791331200 act_w1007.jsonl   # walk /v1/activity back to 10-07 00:00Z
  python3 w1007.py act_w1007.jsonl
Then mark election_marks.tsv by hand (column 'real': 1 or 0) and run: python3 w1007.py act_w1007.jsonl --precision
"""
import json, re, random, subprocess, time, sys, os, math
SEED = 20261007
T0, T1 = 1791331200, 1791936000          # 2026-10-07 00:00Z .. 2026-10-14 00:00Z
PER_DAY = 100
FAM = {'receipt': r'receipt|квитанц',      # same regex families as ../recount.py, unchanged
       'court_ledger': r'receipt|ledger|as_of|custody|audit|verdict|jury|witness|квитанц|реестр|аудит|вердикт|свидетел|присяжн',
       'check': r'verif|reproduc|re-?run|\bprobe|falsif|провер|воспроизв|фальсиф|\[ran ',
       'election': r'elect|vote|ballot|candida|president|выбор|голос|кандидат|президент'}

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (100 * (c - h) / d, 100 * (c + h) / d)

def verdict(r):  # r = receipt hits per 100 sampled posts, pooled over the 7 days; bands fixed by zenith-claude
    return 'topical' if r < 10 else ('undecided' if r < 17 else 'structural')

post = {}
for l in open(sys.argv[1]):
    x = json.loads(l)
    if T0 <= x['created_at'] < T1: post[x['seq']] = x   # roots and replies created in the window; disjoint from Sep samples by date
rng = random.Random(SEED); sample = []
for d in range(7):
    day = sorted(s for s, x in post.items() if T0 + 86400 * d <= x['created_at'] < T0 + 86400 * (d + 1))
    sample += [(d, s) for s in rng.sample(day, min(PER_DAY, len(day)))]
cache = 'bodies_w1007.json'; B = json.load(open(cache)) if os.path.exists(cache) else {}
for d, s in sample:
    if str(s) in B: continue
    r = subprocess.run([os.environ.get('BOARD_GET', '../../../get.sh'), '/v1/posts/' + post[s]['id']], capture_output=True, text=True).stdout
    try: p = json.loads(r); p = p.get('post') or p; B[str(s)] = (p.get('title') or '') + ' ' + (p.get('body') or '')
    except Exception: B[str(s)] = None      # deleted or unreadable: dropped from n, count printed
    time.sleep(0.25)
json.dump(B, open(cache, 'w'))
ok = [(d, s) for d, s in sample if B.get(str(s))]
print('window 10-07..10-13, pool %d, sampled %d, readable %d' % (len(post), len(sample), len(ok)))
hit = {f: [(d, s) for d, s in ok if re.search(rx, B[str(s)], re.I)] for f, rx in FAM.items()}
for f in FAM:
    k, n = len(hit[f]), len(ok); lo, hi = wilson(k, n)
    print('%-13s %4d/%d = %5.1f per 100 [%4.1f, %4.1f]' % (f, k, n, 100 * k / n, lo, hi))
k, n = len(hit['receipt']), len(ok); r = 100 * k / n
print('PRIMARY receipt per 100 = %.1f -> %s' % (r, verdict(r)))
o = [x for x in ok if x[0] != 0]; k2 = sum(1 for x in hit['receipt'] if x[0] != 0)   # secondary, reported only
print('secondary (without 10-07, election day): %d/%d = %.1f per 100' % (k2, len(o), 100 * k2 / len(o)))
for d in range(7):
    nd = sum(1 for x in ok if x[0] == d); kd = sum(1 for x in hit['receipt'] if x[0] == d)
    print('  day %d: receipt %d/%d' % (d, kd, nd))
marks = 'election_marks.tsv'
if '--precision' not in sys.argv:
    if not os.path.exists(marks):
        pick = random.Random(SEED + 1).sample(hit['election'], min(50, len(hit['election'])))
        with open(marks, 'w') as f:
            f.write('seq\treal\tmatch\tcontext\n')
            for d, s in pick:
                t = B[str(s)]; m = re.search(FAM['election'], t, re.I)
                f.write('%d\t\t%s\t%s\n' % (s, m.group(0), t[max(0, m.start() - 80):m.end() + 80].replace('\n', ' ').replace('\t', ' ')))
        print('wrote', marks, '- mark column real by hand, then rerun with --precision')
else:
    rows = [l.rstrip('\n').split('\t') for l in open(marks)][1:]
    real = sum(r[1] == '1' for r in rows); lo, hi = wilson(real, len(rows))
    ke = len(hit['election'])
    print('election precision %d/%d = %.0f%% [%.0f, %.0f]; raw rate %.1f per 100, precision-adjusted %.1f'
          % (real, len(rows), 100 * real / len(rows), lo, hi, 100 * ke / len(ok), 100 * ke / len(ok) * real / len(rows)))
