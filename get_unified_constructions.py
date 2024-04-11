#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import locale
locale.setlocale(locale.LC_NUMERIC, ('hu_HU', 'UTF-8'))
plt.rcdefaults()
plt.rcParams['axes.formatter.use_locale'] = True
sns.set_style("darkgrid")

# adattábla betöltése
db = pd.read_csv('odik_ul.tsv', sep='\t', index_col=0)
db.info()
db.head(5)

# jellemző példányok, jellemző mintázatok
relstuff = db.query('freqsum >= 500')
rellike = relstuff.query('prev_vs_all > 0.9 & actprev_vs_allprev > 0.9')
nonrel = relstuff.query('prev_vs_all < 0.25')
blurry = relstuff.query('prev_vs_all <= 0.75 & actprev_vs_allprev <= 0.75 & prev_vs_all >= 0.25 & actprev_vs_allprev >= 0.25')

rellikegrp = pd.DataFrame(rellike[['lemma', 'prev_vs_all', 'actprev_vs_allprev', 'freqsum']].groupby('lemma').value_counts()).reset_index()
rellikeord = rellikegrp.sort_values(by=['actprev_vs_allprev', 'prev_vs_all', 'freqsum'], ascending=False)
pd.set_option('display.max_rows', None)
print(rellikeord)

