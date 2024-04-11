## Szimultán igekötőzés és igeképzés – konstrukcióegyesítés a magyarban

Ez a repozitórium kiegészítő anyagokat tartalmaz a _Szimultán igekötőzés és igeképzés – konstrukcióegyesítés a magyarban_ című tanulmányhoz.

### Letölthető mappák, szövegfájlok:

- `hgc_ud_sample`: Ez a mappa négy, véletlenszerűen kiválasztott szövegfájlt tartalmaz az MNSz2-UD korpuszból. A teljes korpuszt nem tehetjük nyilvánosan elérhetővé, így a kódokat ezen a mintán lehet kipróbálni.
- `manual_corrections`: Ebben a mappában érhetőek el a kézi javításhoz felhasznált, illetve kézi javítás eredményeként létrejött anyagok. Bővebben:
	- `lemma_list_complete.tsv`: A cikk 3.3 alfejezetében bemutatott adattábla összes igelemmája tokengyakorisággal együtt (5839 db lemma). Ennek a listának az elemeit néztük át egyesével.
	- `lemma_list_to_be_filtered.tsv`: Itt láthatók azok a lemmák (683 db), amelyek a vizsgált téma szempontjából hamis pozitív találatok és kiszűrendők (pl. a *közül*, amely sosem egy 'közzé válik' értelmű ige, hanem névutó).
	- `ul_suffix_fix_list.txt`: Itt azok az igék láthatók az elemzésükkel együtt (1228 db), amelyekben az emMorph elemző nem azonosított -(s)Ul képzőt, viszont a korábbi nyelvállapotokra finomhangolt változata viszont igen.
- `output_test`: Ebben a mappában a scriptek által előállított, különféle kimeneti fájlok láthatók. Fontos, hogy ezeket a `hgc_ud_sample` szövegeiből állítottuk elő, tehát csak minták! A tanulmányunkban bemutatott teljes adattábla a [https://zenodo.org/records/7607661](https://zenodo.org/records/7607661) linken érhető el.
- `hgc_ud_meta.tsv`: Segédfájl, az MNSz2-UD korpusz forrásfájljainak a metaadatai érhetőek el benne.
- `roots.tsv`: Segédfájl, a word2vec klaszterek érhetők el benne (bővebben ld. a cikk 3.2 alfejezetét).

### Letölthető scriptek (a futtatásuk sorrendjében): 

1. `extract_data.py`: Az MNSz2-UD korpuszból (jelen esetben annak néhány mintafájljából) lekér minden olyan mondatot, amelyben van [\_AdjVbz_Ntr/V] képzőt tartalmazó elemzéssel ige (finit ige vagy infinitívusz).
2. `make_dataset.py`: Részletesen feldolgozza a találatokat (kontextus, metaadatok, igekötő-igelemma-bázis-képző, stb.), és létrehozza a kiinduló adatbázist, ez az `orig_dataset.tsv`.
3. `add_relevances.py`: Végez még egy kis adattisztítást, majd megszámolja, hogy az egyes igelemmák hányszor állnak igekötővel és hányszor igekötő nélkül.
4. `get_unified_constructions.py`: Előállítja az egyesített konstrukciók jellemző példányait bemutató táblázatot (bővebben ld. 4. fejezet).
5. `get_productivity.py`: Elvégzi a produktivitás-vizsgálatot, előállítja az 5. fejezetben látható ábrákat.

### Licensz:

A repozitórium tartalma GNU General Public License 3.0 alatt érhető el.

### Hivatkozás:

Amennyiben felhasználja munkájához az itt elérhető kódokat és/vagy szövegfájlokat, kérjük, hogy az alábbi módon hivatkozza a tanulmányunkat:

Kalivoda Ágnes – Palágyi László (2024): Szimultán igekötőzés és igeképzés – konstrukcióegyesítés a magyarban. Kézirat, megjelenés alatt.
