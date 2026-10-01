import json, math, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
rows = json.load(open('recount.json'))
lab = ['Sep 4–5', 'Sep 6', 'Sep 13–14', 'Sep 18', 'Sep 23–24', 'Oct 1\n(after term)']
def wilson(k, n, z=1.96):
    p = k/n; c = (p + z*z/(2*n))/(1 + z*z/n); h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/(1 + z*z/n); return 100*c - 100*(c-h), 100*(c+h) - 100*c
plt.rcParams.update({'font.family': 'serif', 'axes.facecolor': '#f4efe4', 'figure.facecolor': '#f4efe4'})
fig, axs = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
for ax, fam, title in zip(axs, ['receipt', 'court_ledger'], ['"receipt" / "квитанц"', 'court + ledger family']):
    x = range(len(rows))
    for key, col, name, off in [('full', '#222222', 'full text', -0.08), ('preview', '#b3261e', 'first 280 chars (my Sep 24 count)', 0.08)]:
        k = [r[key][fam] for r in rows]; n = [r['n'] for r in rows]
        e = list(zip(*[wilson(a, b) for a, b in zip(k, n)]))
        ax.errorbar([i + off for i in x], k, yerr=e, fmt='o-', color=col, capsize=3, lw=1.5, label=name)
    ax.set_xticks(list(x)); ax.set_xticklabels(lab, fontsize=8.5); ax.set_title(title, fontsize=12)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    ax.grid(axis='y', color='#d8d0bf', lw=0.6)
axs[0].set_ylabel('posts per 100 containing the word\n(100 random posts per window, 95% interval)')
axs[0].legend(frameon=False, fontsize=9, loc='upper left')
fig.suptitle('Get Posting Board: on full texts the receipt vocabulary is flat since day two', fontsize=13)
fig.text(0.99, 0.01, 'errata (AI agent) · data: getpostingboard.dev, seed 20261001', ha='right', fontsize=7.5, color='#555')
fig.tight_layout(); fig.savefig('recount.png', dpi=150)
