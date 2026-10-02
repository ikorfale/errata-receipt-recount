"""Where in a post does a word first appear? For each family: posts (of 600 full bodies) containing it,
share whose first hit is inside the 280-char preview, and the share expected if the first hit were placed
uniformly at random in the text (mean of min(1, 280/len))."""
import json, re
from recount import FAM
B = json.load(open('bodies.json'))
EXTRA = {'because': r'\bbecause\b|потому что', 'thanks': r'\bthank|спасибо', 'wrong': r'\bwrong\b|ошиб|неверн',
         'I think': r'\bI think\b|думаю', 'test': r'\btest|тест', 'question?': r'\?'}
for f, rx in {**FAM, **EXTRA}.items():
    hits = [(m.start(), len(b)) for b in B.values() if (m := re.search(rx, b, re.I))]
    if len(hits) < 15: continue
    inside = sum(p < 280 for p, n in hits) / len(hits)
    expect = sum(min(1, 280 / max(n, 1)) for p, n in hits) / len(hits)
    print(f'{f:14s} n={len(hits):3d} first hit in preview {inside:.2f}  expected {expect:.2f}  ratio {inside/expect:.2f}')
