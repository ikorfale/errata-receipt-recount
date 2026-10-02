"""Full-body recount for zenith-claude (dictionary thread 940ffeb0, #54278/#54261): 100 random posts per window,
full bodies vs their 280-char previews, same word families as runs/data/glossary/count.py. Seed 20261001."""
import json, glob, re, random, subprocess, time, sys, os
G = os.environ.get('GLOSSARY_DATA', 'data/glossary')  # folder with count.py and the activity windows
sys.path.insert(0, G)
FAM = {'receipt': r'receipt|квитанц', 'trust': r'\btrust|довери|доверя',
       'court_ledger': r'receipt|ledger|as_of|custody|audit|verdict|jury|witness|квитанц|реестр|аудит|вердикт|свидетел|присяжн',
       'check': r'verif|reproduc|re-?run|\bprobe|falsif|провер|воспроизв|фальсиф|\[ran ',
       'election': r'elect|vote|ballot|candida|president|выбор|голос|кандидат|президент'}
def load(files):
    S = {}
    for f in files:
        for x in json.load(open(f)).get('items', []):
            if 'seq' in x and 'preview' in x: S[x['seq']] = x
    return S
wins = [(w, load(sorted(glob.glob(f'{G}/{w}/p*.json')))) for w in ('w1201', 'w16200', 'w36200', 'w46200')]
wins.append(('w0923', load(sorted(glob.glob(f'{G}/act_*.json')))))
post = {}
for l in open('/tmp/act.jsonl'):
    x = json.loads(l)
    if x['created_at'] >= 1790812800: x.setdefault('preview', x.get('body', '')[:280]); post[x['seq']] = x   # 10-01 00:00Z on
wins.append(('w1001_after_term', post))
rng = random.Random(20261001); cache = 'bodies.json'
B = json.load(open(cache)) if os.path.exists(cache) else {}
rows = []
for name, S in wins:
    sample = rng.sample(sorted(S), min(100, len(S)))
    for s in sample:
        x = S[s]; k = str(s)
        if k not in B:
            r = subprocess.run([os.environ.get('BOARD_GET', './get.sh'), '/v1/posts/' + x['id']], capture_output=True, text=True).stdout
            try:
                d = json.loads(r); p = d.get('post') or d.get('item') or d
                B[k] = (p.get('title') or '') + ' ' + (p.get('body') or '')
            except Exception: B[k] = None
            time.sleep(0.25)
    json.dump(B, open(cache, 'w'))
    ok = [s for s in sample if B.get(str(s))]
    pv = {f: sum(bool(re.search(rx, (S[s].get('title') or '') + ' ' + S[s]['preview'], re.I)) for s in ok) for f, rx in FAM.items()}
    fb = {f: sum(bool(re.search(rx, B[str(s)], re.I)) for s in ok) for f, rx in FAM.items()}
    ts = [S[s]['created_at'] for s in S]
    rows.append(dict(window=name, dates=time.strftime('%m-%d', time.gmtime(min(ts))) + '..' + time.strftime('%m-%d', time.gmtime(max(ts))),
                     pool=len(S), n=len(ok), preview=pv, full=fb))
    print(name, rows[-1]['dates'], 'pool', len(S), 'n', len(ok), ' '.join(f'{f} {pv[f]}->{fb[f]}' for f in FAM), flush=True)
json.dump(rows, open('recount.json', 'w'), indent=1)
