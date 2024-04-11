# -*- coding: utf-8 -*-

# author: kagnes
# created: 2022/07/10

import re


def get_clusters(rootfile):
    """ beolvassa a root-okhoz tartozó w2v clustereket, ezeket előzőleg innen nyertük ki: http://pi.itk.ppke.hu/w2v/ """

    clusters = {}
    with open(rootfile, 'r', encoding='utf-8') as fr:
        for line in fr:
            clustnum, wordline = line.strip().split('\t')
            words = wordline.split(' ')
            for word in words:
                clusters[word] = int(clustnum)
    return clusters


def process_file(infile, clusters):
    """ beolvassa a fájlt úgy, hogy ha egy mondat összeáll, azt rögtön feldolgozza, nem tárolja el """

    actsent = []
    with open(infile, 'r', encoding='utf-8') as fr:
        for line in fr:
            line = line.strip()
            if len(line) == 0:
                sents = handle_multihits(actsent)
                dt = get_basic_meta(sents)
                get_dep_infos(dt, clusters)
                actsent = []
            else:
                actsent.append(line)


def handle_multihits(actsent):
    """
	itt oldjuk meg az olyan eseteket, ahol a # infós hits 1-nél nagyobb: hits="2" ids="1 2"
	→ itt két külön példány a mondatból, hits törölve, id="1" és id="2" külön
	magyarán, ha egy mondatban két külön találat van, akkor kétszer vesszük a mondatot a megfelelő egy-egy találattal
	"""

    sents = []
    tempie = []
    if 'hits="1"' not in actsent[0]:
        ids = re.search(r'ids="([^"]+)"', actsent[0]).group(1)
        hits = ids.split(' ')
        for hit in hits:
            actheader = re.sub(r' hits="[^"]+" ids="[^"]+"', r' id="' + hit + '"', actsent[0])
            tempie.append(actheader)
            for line in actsent[1:]:
                tempie.append(line)
            sents.append(tempie)
            tempie = []
    else:
        actheader = re.sub(r' hits="[^"]+" ids=', r' id=', actsent[0])
        tempie.append(actheader)
        for line in actsent[1:]:
            tempie.append(line)
        sents.append(tempie)
    return sents


def get_basic_meta(sents):
    """ a találatokat dictionary-be rakjuk át, és kinyerjük az alapvető metaadat oszlopokat, majd töröljük a # sort """

    dt = {}
    for i, sent in enumerate(sents):
        meta = re.findall(r'"([^"]+)"', sent[0])
        dt[i] = {'doc_id': meta[0], 'doc_style': meta[1], 'doc_year': meta[2], 'hitid': meta[3], 'todo': sent[1:]}
    return dt


def create_kwic(data):
    """ keyword-in-context berakás hit ID alapján """

    lc = []
    rc = []
    kwic = ''
    hitid = int(data['hitid'])

    for line in data['todo']:
        actid, form, _, _, _, _, _, _, _, _ = line.split('\t')
        if int(actid) < hitid:
            lc.append(form)
        elif int(actid) == hitid:
            kwic = form
        else:
            rc.append(form)

    left_context = ' '.join(lc).strip()
    right_context = ' '.join(rc).strip()

    return left_context, kwic, right_context


def get_dep_infos(dt, clusters):
    """ az összes többi információ kinyerése """

    for i, data in dt.items():
        hit = data['todo'][int(data['hitid']) - 1]
        tid, form, lemma, upos, xpos, feats, head, deprel, deps, misc = hit.split('\t')

        form = form.lower()
        deps = find_dependents(int(data['hitid']), data['todo'])

        prevtype = ''
        prev = ''
        verb = ''
        sep_prev = ''
        for line in deps:
            if 'compound:preverb' in line:
                _, _, sep_prev, _, _, _, _, _, _, _ = line.split('\t')
                break

        prefixed = re.search(r' "([^"]*?)\[/Prev]', misc)
        if prefixed:
            lemmarest = re.search(r'^' + prefixed.group(1) + r'(.*)$', lemma)
            if lemmarest:
                prevtype = 'PFX'
                prev = prefixed.group(1)
                verb = lemmarest.group(1)
                lemma = prev + '+' + verb
        elif len(sep_prev) > 0:
            prevtype = 'SEP'
            prev = sep_prev
            verb = lemma
            lemma = prev + '+' + lemma
        else:
            prevtype = '_'
            prev = '_'
            verb = lemma

        readable = re.findall(r'"readable": "([^"]*?)"', misc)
        relevants = []
        for item in readable:
            if '[_AdjVbz_Ntr/V]' in item:
                item = re.sub(r'^[^ ]+\[/Prev] \+ ', r'', item)
                item = re.sub(r' \+ [^ ]+\[_AdjVbz_Ntr/V].*$', r'', item)
                relevants.append(item)

        if ' ' not in relevants[-1]:
            root = relevants[-1].split('[')[0]
        else:
            morphs = re.split(r' \+ ', relevants[-1])
            if '=' in morphs[-1]:
                morphs[-1] = morphs[-1].split('=')[0]
            root = ''
            for morph in morphs:
                if '=' in morph:
                    root += morph.split('=')[1]
                else:
                    root += morph.split('[')[0]

            if root == 'felhangos':
                root = 'hangos'
            elif root == 'összesűrű':
                root = 'sűrűs'
            elif root == 'lemeztelen':
                root = 'meztelen'

        suffix = '-(s)Ul' if lemma.lower().endswith('l') else '-Odik'
        if root in clusters.keys():
            w2v_cluster = clusters[root]
        else:
            w2v_cluster = 999

        argframe_cases, argframe_long = get_argframe(hit, deps)
        if len(argframe_cases) == 0:
            argframe_cases = '_'
        if len(argframe_long) == 0:
            argframe_long = '_'

        doc_year = data['doc_year'] if re.search(r'^\d{4}$', data['doc_year']) else '0'
        year_exact = 'n' if doc_year == '0' else 'y'
        doc_id = data['doc_id']
        doc_style = data['doc_style']
        left_context, kwic, right_context = create_kwic(data)

        if not re.search(r'[.,;/:]', form):
            tsv_line = '\t'.join([form, lemma, prev, prevtype, verb, root, suffix, str(w2v_cluster), argframe_cases, argframe_long, str(doc_year), year_exact, doc_style, doc_id, left_context, kwic, right_context])
            tsv_line = re.sub("'", "’", tsv_line)
            tsv_line = re.sub('"', '“', tsv_line)
            print(tsv_line)


def find_dependents(hitid, lines):
    """ azokat a sorokat hozza ki, amiknek a hit a feje """

    cases = {}
    transformed = []
    for line in lines:
        ltid, lform, llemma, lupos, lxpos, lfeats, lhead, ldeprel, ldeps, lmisc = line.split('\t')
        if ldeprel == 'case':
            cases[int(lhead)] = llemma
    for line in lines:
        ltid, lform, llemma, lupos, lxpos, lfeats, lhead, ldeprel, ldeps, lmisc = line.split('\t')
        if int(ltid) in cases.keys():
            lfeats = 'Case=' + cases[int(ltid)] + '|' + lfeats
        transformed.append('\t'.join([ltid, lform, llemma, lupos, lxpos, lfeats, lhead, ldeprel, ldeps, lmisc]))

    deps = []
    for line in transformed:
        ltid, lform, llemma, lupos, lxpos, lfeats, lhead, ldeprel, ldeps, lmisc = line.split('\t')
        line_head = int(lhead)
        if line_head == hitid and lupos != 'PUNCT' and (ldeprel == 'compound:preverb' or 'Case=' in lfeats):
            deps.append(line)

    return deps


def get_argframe(hit, deps):
    """ a vonzatkeretet igyekszünk kinyerni """

    argdict = {}
    for dep in deps:
        if 'compound:preverb' not in dep:
            ltid, lform, llemma, lupos, lxpos, lfeats, lhead, ldeprel, ldeps, lmisc = dep.split('\t')
            cases = re.findall(r'Case=([^ |]+)\|', lfeats)
            if len(cases) > 1:
                cases.reverse()
            caselist = '.'.join(cases)
            if caselist not in argdict.keys():
                argdict[caselist] = []
            argdict[caselist].append(llemma)

    htid, hform, hlemma, hupos, hxpos, hfeats, hhead, hdeprel, hdeps, hmisc = hit.split('\t')
    persnum = re.search(r'\.([123](Pl|Sg))]', hxpos)
    actor = ''
    if persnum:
        if persnum.group(1) == '1Sg':
            actor = 'én'
        elif persnum.group(1) == '2Sg':
            actor = 'te'
        elif persnum.group(1) == '3Sg':
            actor = 'ő/az'
        elif persnum.group(1) == '1Pl':
            actor = 'mi'
        elif persnum.group(1) == '2Pl':
            actor = 'ti'
        elif persnum.group(1) == '3Pl':
            actor = 'ők/azok'

    if actor != '':
        if actor in ['ő/az', 'ők/azok'] and 'Nom' not in argdict.keys():
            argdict['Nom'] = [actor]

        if actor in ['én', 'te', 'mi', 'ti']:
            if 'Nom' not in argdict.keys():
                argdict['Nom'] = [actor]
            else:
                if actor not in argdict['Nom']:
                    argdict['Nom'].append(actor)
    sorted_argdict = {k: argdict[k] for k in sorted(argdict)}
    argframe_cases = ' '.join(list(sorted_argdict.keys()))
    argframe_long = ''
    for case, args in argdict.items():
        for arg in args:
            piece = arg+'['+case+'] '
            argframe_long += piece
    argframe_long = argframe_long.strip()
    return argframe_cases, argframe_long


""" MAIN """

infile = 'hgc_ud_hits.txt'
rootfile = 'roots.txt'

clusters = get_clusters(rootfile)
process_file(infile, clusters)

