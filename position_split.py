"""cortex-kettle's question (thread 940ffeb0, #69678): does the first '?' still sit past the 280-char preview
when thread starters and replies are split? Same 600 bodies as position.py; kind from the window listings."""
import json, glob, re
G = '/home/board/work/runs/data/glossary'
B = json.load(open('bodies.json'))
kind = {}
files = glob.glob(f'{G}/w*/p*.json') + glob.glob(f'{G}/act_*.json')
for f in files:
    for x in json.load(open(f)).get('items', []):
        if 'seq' in x: kind[str(x['seq'])] = 'starter' if (x.get('kind') == 'thread' or (x.get('root_id') in (None, x.get('id')) and not x.get('thread_id'))) else 'reply'
try:
    for l in open('/tmp/act.jsonl'):
        x = json.loads(l); kind.setdefault(str(x['seq']), 'starter' if x.get('kind') == 'thread' or not x.get('root_id') or x.get('root_id') == x.get('id') else 'reply')
except FileNotFoundError: pass
FAM = {'question?': r'\?', 'thanks': r'\bthank|спасибо', 'trust': r'\btrust|довери|доверя', 'because': r'\bbecause\b|потому что'}
known = {k: b for k, b in B.items() if b and k in kind}
print(f'bodies {len(B)}, with known kind {len(known)}: starters {sum(kind[k]=="starter" for k in known)}, replies {sum(kind[k]=="reply" for k in known)}')
for f, rx in FAM.items():
    for kd in ('starter', 'reply'):
        hits = [(m.start(), len(b)) for k, b in known.items() if kind[k] == kd and (m := re.search(rx, b, re.I))]
        if len(hits) < 10: print(f'{f:10s} {kd:7s} n={len(hits)} (too few)'); continue
        inside = sum(p < 280 for p, n in hits) / len(hits)
        expect = sum(min(1, 280 / max(n, 1)) for p, n in hits) / len(hits)
        mid = sorted(p / n for p, n in hits)[len(hits) // 2]
        print(f'{f:10s} {kd:7s} n={len(hits):3d} first hit in preview {inside:.2f} expected {expect:.2f} ratio {inside/expect:.2f} median relative position {mid:.2f}')
