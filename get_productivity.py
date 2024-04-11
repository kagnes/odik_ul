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

# produktivitás és hapaxok
db21 = db.query('doc_year >= 2000').to_dict('records')  # beállítjuk, hogy melyik évtől kezdve nézzük az adatot
minfreq = 500  # efölötti tokengyakoriság esetén számoljunk produktivitást
legomena = 1  # hapax- (1), dis- (2) vagy tris- (3) legomenákat is nézzük-e, alapbeállítás a hapax

# átalakítjuk az adattábla szerkezetét, nem túl elegánsan...
new_dict = {'IGE-(s)Odik': {'freq': 0, 'instances': {}},
            'IGE-(s)Ul': {'freq': 0, 'instances': {}},
            'IK-IGE-(s)Odik': {'freq': 0, 'instances': {}},
            'IK-IGE-(s)Ul': {'freq': 0, 'instances': {}}}
for dt in db21:
    if dt['suffix'] == '-(s)Odik' and dt['prev'] == '_':
        if dt['lemma'] not in new_dict['IGE-(s)Odik']['instances'].keys():
            new_dict['IGE-(s)Odik']['instances'][dt['lemma']] = 0
        new_dict['IGE-(s)Odik']['instances'][dt['lemma']] += 1
        new_dict['IGE-(s)Odik']['freq'] += 1
    if dt['suffix'] == '-(s)Ul' and dt['prev'] == '_':
        if dt['lemma'] not in new_dict['IGE-(s)Ul']['instances'].keys():
            new_dict['IGE-(s)Ul']['instances'][dt['lemma']] = 0
        new_dict['IGE-(s)Ul']['instances'][dt['lemma']] += 1
        new_dict['IGE-(s)Ul']['freq'] += 1
    if dt['suffix'] == '-(s)Odik' and dt['prev'] != '_':
        if dt['lemma'] not in new_dict['IK-IGE-(s)Odik']['instances'].keys():
            new_dict['IK-IGE-(s)Odik']['instances'][dt['lemma']] = 0
        new_dict['IK-IGE-(s)Odik']['instances'][dt['lemma']] += 1
        new_dict['IK-IGE-(s)Odik']['freq'] += 1
    if dt['suffix'] == '-(s)Ul' and dt['prev'] != '_':
        if dt['lemma'] not in new_dict['IK-IGE-(s)Ul']['instances'].keys():
            new_dict['IK-IGE-(s)Ul']['instances'][dt['lemma']] = 0
        new_dict['IK-IGE-(s)Ul']['instances'][dt['lemma']] += 1
        new_dict['IK-IGE-(s)Ul']['freq'] += 1

# így készül a cikkben látható 2. ábra
cons_ls = []
for k, v in new_dict.items():
    cons = k
    tokens = v['freq']
    types = len(v['instances'].keys())
    hapaxes = 0
    suffix = cons.split('-')[-1]
    suffix = '-'+suffix
    for fq in v['instances'].values():
        if fq <= legomena:
            hapaxes += 1
    narrowprod = round(hapaxes / tokens, 4) if tokens >= minfreq else '_'
    row = {'szerkezet': cons, 'képző': suffix, 'N (tokengyakoriság)': tokens, 'V (típusgyakoriság)': types, 'n1 (hapaxok)': hapaxes, 'P (potenciális produktivitás)': narrowprod}
    cons_ls.append(row)
abs_prod = pd.DataFrame.from_dict(cons_ls)
print(abs_prod)

sns.relplot(data=abs_prod, x='P (potenciális produktivitás)', y='V (típusgyakoriság)', size='N (tokengyakoriság)', sizes=(20,300)) # alpha=0.5
[plt.text(x=row['P (potenciális produktivitás)']+0.0003, y=row['V (típusgyakoriság)'], s=row['szerkezet']) for k, row in abs_prod.iterrows()]
plt.show()

# így készül a cikkben látható 3. ábra
pv_dict = {}
for k, v in new_dict.items():
    if k.startswith('IK'):
        for pvv, freq in v['instances'].items():
            pv = pvv.split('+')[0]
            suffix = '-(s)Ul' if pvv.endswith('l') else '-(s)Odik'
            cons = pv+suffix
            if cons not in pv_dict.keys():
                pv_dict[cons] = {'freq': 0, 'instances': {}}
            pv_dict[cons]['instances'][pvv] = freq
            pv_dict[cons]['freq'] += freq

pvv_ls = []
for k, v in pv_dict.items():
    cons = k
    tokens = v['freq']
    types = len(v['instances'].keys())
    hapaxes = 0
    for fq in v['instances'].values():
        if fq <= legomena:
            hapaxes += 1
    narrowprod = round(hapaxes / tokens, 4) if tokens >= minfreq else '_'
    pv, suffix = cons.split('-')
    suffix = '-'+suffix
    if narrowprod != '_' and pv in ['össze', 'meg', 'le', 'ki', 'fel', 'el', 'bele', 'be']:
        row = {'szerkezet': cons, 'igekötő': pv, 'képző': suffix, 'N (tokengyakoriság)': tokens, 'V (típusgyakoriság)': types, 'n1 (hapaxok)': hapaxes, 'P (potenciális produktivitás)': narrowprod}
        pvv_ls.append(row)
pvv_prod = pd.DataFrame.from_dict(pvv_ls)
pvv_prod = pvv_prod.sort_values(by=['igekötő', 'képző', 'P (potenciális produktivitás)'])
print(pvv_prod)

sns.relplot(data=pvv_prod, x='P (potenciális produktivitás)', y='V (típusgyakoriság)', size='N (tokengyakoriság)', sizes=(20,300), hue='képző', style='képző', markers=['X','o'], palette='Set1', alpha=0.5) # alpha=0.5
[plt.text(x=row['P (potenciális produktivitás)']+0.0005, y=row['V (típusgyakoriság)'], s=row['igekötő']) for k, row in pvv_prod.iterrows()]
plt.show()

