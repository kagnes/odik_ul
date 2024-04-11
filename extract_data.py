# -*- coding: utf-8 -*-

# author: kagnes
# created: 2022/06/04

import os
import re


def get_meta(f):
	""" beolvassa a metaadatokat egy dictionary-be """

	metadt = {}
	with open(f, 'r', encoding='utf-8') as fr:
		for i, line in enumerate(fr):
			docid, _, texttype, _, year, _ = line.strip().split('\t')
			metadt[docid] = [texttype, year]
	return metadt


def process_file(cpath, fname, texttype, year, outfile):
	""" beolvassa a korpuszfájlokat és kigyűjt minden olyan mondatot, ami a keresésünkre illeszkedik """

	actsent = []
	with open(outfile, 'a', encoding='utf-8') as fw:
		with open(cpath+'/'+fname, 'r', encoding='utf-8') as fr:
			for line in fr:
				cells = line.strip().split('\t')
				if len(cells) == 1:
					count_hits, hit_cells = get_hits(actsent)
					if count_hits > 0:
						print('# file="{}" style="{}" year="{}" hits="{}" ids="{}"'.format(fname, texttype, year, count_hits, ' '.join(hit_cells)), file=fw)
						for item in actsent:
							print('\t'.join(item), file=fw)
						print('', file=fw)
					actsent = []
				else:
					actsent.append(cells)


def get_hits(actsent):
	""" az adott mondatban megnézi, hogy van-e a keresésünkre illeszkedő szakasz """

	count_hits = 0
	hit_cells = []
	for cells in actsent:
		if cells[3] == 'VERB':
			hit = re.search(r'\[_AdjVbz_Ntr/V\]', cells[9], flags=re.IGNORECASE)
			if hit:
				count_hits += 1
				hit_cells.append(cells[0])
	return count_hits, hit_cells


""" MAIN """

corpus_path = 'hgc_ud_sample'
meta_file = 'hgc_ud_meta.tsv'
outfile = 'hgc_ud_hits.txt'

metadt = get_meta(meta_file)
files = sorted(os.listdir(corpus_path))

for i, fname in enumerate(files):
	print('{} : {}'.format(i+1, fname))
	process_file(corpus_path, fname, metadt[fname][0], metadt[fname][1], outfile)
	
