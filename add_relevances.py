# -*- coding: utf-8 -*-

# author: kagnes
# created: 2022/10/11

import re

infile = 'orig_dataset.tsv'

formdict = {'belé': 'bele',
            'bé': 'be',
            'föl': 'fel',
            'fölül': 'felül',
            'fönn': 'fenn',
            'odább': 'odébb',
            'reá': 'rá',
            'teli': 'tele'}

header = 'id\tform\tlemma\tprev\tprevtype\tverb\troot\tsuffix\tw2v_cluster\targframe_cases\targframe_long\tdoc_year' \
         '\tdoc_style\tdoc_id\tleft_context\tkwic\tright_context\tfreqsum\tprev_vs_all' \
         '\tactprev_vs_allprev'

prevset = {'abba', 'ágyba', 'agyon', 'ajtót', 'alá', 'alább', 'állást', 'által', 'alul', 'arcul', 'át', 'be', 'bé',
            'békén', 'bele', 'belé', 'benn', 'bent', 'bérbe', 'bosszút', 'célba', 'cserben', 'csődbe', 'csonttá',
            'csúcsra', 'égbe', 'egybe', 'egyet', 'együtt', 'éhen', 'el', 'elé', 'élen', 'életben', 'életre', 'ellen',
            'ellent', 'elő', 'előre', 'érvénybe', 'észhez', 'észre', 'falra', 'fejbe', 'fejen', 'fel', 'félbe', 'félre',
            'felül', 'fenn', 'férjhez', 'főbe', 'föl', 'földet', 'földhöz', 'földre', 'fölé', 'fölül', 'fönn', 'fülön',
            'füstbe', 'görcsbe', 'gúzsba', 'hadat', 'hadba', 'hajba', 'hanyatt', 'harcba', 'hasba', 'hasra', 'hatályba',
            'hátba', 'hátra', 'haza', 'házhoz', 'hegyet', 'helybe', 'helyben', 'helyre', 'helyt', 'hozzá', 'ide',
            'igazat', 'irányt', 'jól', 'jót', 'jóvá', 'kárba', 'karban', 'keresztbe', 'keresztül', 'készen', 'kétségbe',
            'ketté', 'kézben', 'kézen', 'kezet', 'kézhez', 'kézre', 'ki', 'kinn', 'kívül', 'kölcsön', 'körbe', 'körül',
            'közbe', 'közben', 'közé', 'közre', 'közzé', 'külön', 'kupán', 'küszöbön', 'kútba', 'lábra', 'lángba',
            'lángra', 'latba', 'lázba', 'le', 'lényegre', 'létre', 'lóvá', 'meg', 'mellbe', 'mellé', 'mennybe',
            'nagyot', 'nagyra', 'neki', 'nyakon', 'nyélbe', 'nyilván', 'nyomon', 'nyomra', 'oda', 'odább', 'odébb',
            'oldalba', 'össze', 'ott', 'padlót', 'partra', 'piacra', 'pofán', 'pofon', 'porba', 'pórul', 'rá', 'rabul',
            'rajta', 'reá', 'rendbe', 'rendre', 'részre', 'részt', 'ringbe', 'romba', 'rosszul', 'sárba', 'seggbe',
            'seggre', 'semmibe', 'síkra', 'sorba', 'sorban', 'sorra', 'szájon', 'számba', 'számon', 'számot', 'szárba',
            'szárnyra', 'szarrá', 'széjjel', 'szembe', 'szemben', 'szemen', 'szemet', 'szemmel', 'szemre', 'szénné',
            'szerte', 'szét', 'színre', 'szóba', 'szörnyet', 'szót', 'szóvá', 'talpon', 'talpra', 'táncra', 'tarkón',
            'tele', 'teli', 'témába', 'térdre', 'testet', 'testre', 'tetten', 'tisztán', 'tökön', 'tollba', 'tönkre',
            'tőrbe', 'torkon', 'törvényt', 'tova', 'tovább', 'trónra', 'tükörbe', 'túl', 'tűzbe', 'újjá', 'újra',
            'utána', 'utat', 'útba', 'utol', 'útra', 'valóra', 'végbe', 'véget', 'véghez', 'végig', 'végre', 'vérig',
            'világgá', 'világra', 'vissza', 'viszont', 'vízre', 'zavarba', 'zokon', 'zsebre', '_'}

bad_lemmas = {'el+pusztul', 'ki+pusztul', 'bele+pusztul', 'svédül', 'készülget', 'meg+készül', 'csehül', 'le+pusztul', 'közül', 'meg+pusztul', 'dánul', 'szarul', 'észtül', 'össze+kutyul', 'vendül', 'rosszabbul', 'gyérül', 'ellen+készül', 'előre+készül', 'rútul', 'hozzá+készül', 'épül-szépül', 'baszkul', 'grúzul', 'vissza+részesül', 'szászul', 'vissza+készül', 'le+készül', 'kurdul', 'ott+készül', 'tótul', 'lezserül', 'angolszászul', 'ott+pusztul', 'ott+épül', 'be+készül', 'szentül', 'ki+részesül', 'el+épül', 'vissza+gyorsul', 'ott+érvényesül', 'tovább+pusztul', 'oda+pusztul', 'skótul', 'meg+teljesül', 'klasszul', 'falsul', 'frízül', 'szlávul', 'lettül', 'által+gazdagodik', 'ott+porosodik', 'el+kutyul', 'ki+üdvözül', 'el+erősödik', 'éhen+pusztul', 'ide+készül', 'szárdul', 'által+erősödik', 'svábul', 'remekül', 'be+lesűrűsödik', 'ott+boldogul', 'ki+szépül', 'ki+butul', 'frankul', 'bele+kutyul', 'ott+valósul', 'hozzá+készülődik', 'fel+készülődik', 'örökül', 'vissza+valósul', 'végre+készül', 'szírül', 'ott+tornyosul', 'ott+magasodik', 'halhatatlanul', 'ellen+készülődik', 'el+érvényesül', 'bele+készül', 'szemben+bővül', 'épült-szépül', 'rosszul', 'ott+üdül', 'gazul', 'elé+készül', 'be+lészerelmesedik', 'által+szabadul', 'által+épül', 'végre+szabadul', 'rácul', 'popul', 'mellé+készül', 'körül+sűrűsödik', 'körül+ritkul', 'körül+csoportosul', 'kékül-zöldül', 'kékült-zöldül', 'el+bénul', 'végre+épül', 'szerte+épül', 'rá+teljesül', 'ott+lelkesedik', 'össze+pontosul', 'körül+sokasodik', 'körül+erősödik', 'körül+épül', 'komplettül', 'ki+gyengül', 'ide+nősül', 'fel+tarul', 'felemásul', 'faszul', 'etruszkul', 'át+lázasodik', 'által+részesül', 'vissza+pusztul', 'tágul-szűkül', 'szemben+épül', 'ott+tömörül', 'ott+szabadul', 'ott+létesül', 'ott+erősödik', 'ott+bizonyul', 'orvul', 'linkül', 'létre+készül', 'le+híresül', 'körül+tágul', 'körül+állandósul', 'koptul', 'ki+nősül', 'ki+lázasodik', 'ki+kutyul', 'hívül', 'ellen+bizonyul', 'el+lelkesedik', 'elevenül', 'együtt+készül', 'egyet+mordul', 'egesedik', 'csupaszul', 'be+kutyul', 'balogul', 'át+nősül', 'által+teljesül', 'végre+részesül', 'utána+szabadul', 'szűkül-tágul', 'szét+ritkul', 'szét+elegyedik', 'szerte+létesül', 'szemben+magasodik', 'szemben+erősödik', 'strammul', 'reszesedik', 'rá+közösül', 'ott+tompul', 'ott+sötétedik', 'ott+rozsdásodik', 'ott+gyengül', 'ott+görbül', 'ószlávul', 'meg+veszekszik-vénül', 'meg+kutyul', 'meg+közül', 'magyarul', 'le+vakul', 'közé+készül', 'ki+valósul', 'ki+bizonyul', 'készül-készül', 'karosodik', 'kacérul', 'irásodik', 'indül', '-frissül', 'fel+tevésedik', 'fel+pusztul', 'előre+bizonyul', 'el+létesül', 'el+egyesül', 'derekul', 'át+érvényesül', 'által+üdvözül', 'által+készül', 'által+bővül', 'zordonul', 'vényesül', 'véletlenül', 'végre+tudatosul', 'végre+teljesül', 'végre+egyesül', 'végre+boldogul', 'végig+érvényesül', 'végig+bizonyul', 'vásik-vénül', 'utána+pusztul', 'utána+készül', 'utána+boldogul', 'tova+épül', 'tovább+boldogul', 'tétlenül', 'tejesül', 'tarul', 'szolidul', 'szét+épül', 'szerte+semmisül', 'szerte+lazul', 'szemben+részesül', 'szemben+készül', 'szemben+károsodik', '-rosszul', 'rá+dadásul', 'ott+terebélyesedik', 'ott+szilárdul', 'ott+sűrűsödik', 'ott+részesül', 'ott+öregedik', 'ott+melegedik', 'ott+készülődik', 'ott+házasodik', 'ott+hasznosul', 'ott+gyökeresedik', 'ott+feketedik', 'ott+csúcsosodik', 'összesürüsödik', 'össze+pusztul', 'nettül', 'mórul', 'meztelenül', 'meg+mohosodik', 'lívül', 'létre+készülődik', 'lassul-gyorsul', 'külön+készül', 'körül+zöldül', 'körül+szűkül', 'körül+szépül', 'körül+készülődik', 'körül+készül', 'körül+csendesedik', 'ki+tejesedik', 'ki+-kerekedik', 'ki+érvényesül', 'ide+pusztul', 'hunul', 'harsul-falsul', 'gyorsul-lassul', 'gyorsul-gyorsul', 'gyógyult-üszkösödik', 'gyermetegül', 'göndörül', 'gallul', 'frígül', 'fettül', 'fenn+mordul', 'fel+zöldül', 'fel+valósul', 'fárad-okosodik', 'extrémül', 'erősödött-gyengül', 'épül-omol', 'épül-készül', '-épül', 'előre+valósul', 'elő+épül', 'ellen+tömörül', 'el+-komorodik', 'egybe+kutyul', 'dobásodik', 'cipszerül', 'bővült-bővül', 'bonyolultul', 'be+pusztul', 'benn+erősödik', 'balfaszul', 'át+részesül', 'át+gyengül', 'által+valósul', 'által+érvényesül', 'agyon+pusztul', 'abba+vakul', 'zsírosodik-gazdagodik', '-zsírosodik', 'zöldült-lilul', 'vizigótul', 'vizesedett-világosodik', 'vissza+kutyul', 'vehemensül', 'végre+valósul', 'végre+üdül', 'végre+önállósodik', 'végre+nehezedik', 'végre+mordul', 'végre+módosul', 'végre+kerekedik', 'végre+igazodik', 'végre+érvényesül', 'végre+enyhül', 'végre+elegyedik', 'végre+bizonyul', 'végig+sebesül', 'végig+pusztul', 'vár-készül', 'van-készül', 'vakul-káprázik', '-vakul', 'vakkan-mordul', 'vadul-bolondul', 'útrakészül', 'utol+sósul', 'utol+épül', 'utána+vakul', 'utána+részesül', 'utána+önállósodik', 'utána+melegedik', 'utána+komolyodik', 'utána+igazodik', 'utána+gyökeresedik', 'utána+épül', 'utána+bővül', 'utána+bolondul', 'utána+barnul', 'ülepedett-posványosodik', 'túl+szabadul', 'túl+ritkul', 'túl+pusztul', 'túl+gyengül', 'túl+épül', 'tova+szőkül', 'tova+halkul', 'tovább+vakul', 'tovább+testesül', 'tovább+teljesedik', 'tovább+kutyul', 'tovább+dánul', 'tovább+csonkul', 'tovább+csendesedik', 'tovább+adósodik', 'torzul-torzít', 'tönkre+pusztul', 'tökélestesedik', 'telik-teljesedik', 'teléresedik', 'tekereg-torzul', 'teher-mentesedik', 'támad-kerekedik', 'tágul-zárul', 'tágult-szűkül', 'tágul-terebélyesedik', 'tágult-ás', 'szülésedik', 'szűkül-szűkül', '-szövetesedik', 'szórakozik-okosodik', 'színeződött-gazdagodik', 'Szin-esedik', 'szideritesedik', 'szét+szépül', 'szét+magasodik', 'szét+különül', 'szét+kapusodik', 'szépült-csinosodik', 'szépült-bővül', 'szépül-épül', 'szembe+részesül', 'szemben+szeplősödik', 'szemben+részesedik', 'szemben+módosul', 'szemben+mocsarasodik', 'szemben+létesül', 'szemben+hasznosul', 'szemben+érvényesül', 'szembe+közösül', 'szembe+kerekedik', 'szembe+erősödik', 'szelektál-igazodik', 'szárítkozik-melegedik', '-szakosodik', 'súg-fodrosodik', 'sárgul-kékül', 'rútult-szaglik', 'rosszul-esik', 'rá+tudatosul', 'rá+pusztul', 'ráncosodik-repedezik', 'rá+kutyul', 'rá+jogosul', 'rá+érvényesül', 'rá+érdemesül', 'rá+enyhül', 'rá+diótulajdonosodik', 'porosodik-porlad', 'pirul-kékül', 'pihésedik-foszladozik', 'pendült-telt-teljesedik', 'pedánsul', 'pazarul', 'ott+világosodik', 'ott+vastagodik', 'ott+tudatosodik', 'ott+tisztul', 'ott+teljesül', 'ott+teljesedik', 'ott+tejesedik', 'ott+tágul', 'ott+szürkül', 'ott+szélesedik', 'ott+sokasodik', 'ott+sárgul', 'ott+rosszabbodik', 'ott+ritkul', 'ott+puhul', 'ott+pörösödik', 'ott+piacosodik', 'ott+nehezül', 'ott+nehezedik', 'ott+módosul', 'ott+mentesül', 'ott+melegül', 'ott+kukul', 'ott+kopaszodik', 'ott+kékül', 'ott+ízesül', 'ott+iszaposodik', 'ott+hűvösödik', 'ott+hűsül', 'ott+hülyül', 'otthoniasodik', 'ott+gyorsul', 'ott+gazdagodik', 'ott+frissül', 'ott+fakul', 'ott+enyhül', 'ott+elegyedik', 'ott+egyesül', 'ott+drágul', 'ott+csontosul', 'ott+csomósodik', 'ott+butul', 'ott+búsul', 'ott+bővül', 'ott+bodorodik', 'ott+bizonyosodik', 'ószászul', 'összesűrösödik', 'orvosul', 'öregszik-fiatalodik', 'okosul', 'óírül', 'nyúlik-tágul', 'nyúlik-kerekedik', 'nyúl-hosszabbodik', 'nemtörődömül', '-nehezedik', 'mordul-kordul', '-mordul', 'mélyül-mélyül', 'mellé+vénül', 'mellé+teljesül', 'mellé+oszloposodik', 'mellé+bizonyul', 'meg+szelésedik', 'meg+szarul', 'meg+merősödik', 'meg+hazásodik', 'meg+erőtlenül', 'médül', 'másododik', 'magyarul-külföldiül', 'M-agyarosodik', 'magyar-lágyul', 'magasodik-magasztosul', 'l-rosszul', 'lilul-zöldül', 'létre+nehezedik', 'létre+érvényesül', 'lemma', 'le+mérgesedik', 'lelkesedik-szorong', '-lelkesedik', 'le+kutyul', 'le+közösül', '-legyesedik', 'le+érvényesül', 'le+erősödik', 'le+elevenedik', 'le+boldogul', 'le+álmosodik', 'le+állandósul', 'lassult-gyorsul', 'lassúdadul', 'külön+részesül', 'közzé+tökéletesedik', 'közzé+kutyul', 'közzé+erősödik', 'közzé+általánosodik', 'közvetlenül', 'közeledik-simul', 'közben+melegedik', 'közben+készül', 'közben+gazdagodik', 'közben+épül', 'közben+enyhül', 'közben+egyesül', 'körül+tisztul', 'körül+szürkül', 'körül+szagosodik', 'körül+szabadul', 'körül+sötétedik', 'körül+pusztul', 'körül+lazul', 'körül+kukul', 'körül+egyesül', 'körbe+némul', 'ki+zöldült-vidul', 'ki+zápul', 'kívül+melegedik', 'kívül+csinosodik', 'ki+tarul', 'ki-tágul', 'ki+szinesedik', 'ki+svédül', 'ki+sérvesedik', 'ki+semmisül', 'ki+némul', 'ki+kurdul', 'ki+különül', 'ki+közül', 'ki+idősödik', 'ki+hidegül', 'ki+észtül', 'ki+eminensül', 'ki-albínósodik', 'keveredik-házasodik', 'készült-készül', 'készülőzik', 'készülőz', 'készül-épül', 'készül-alakul', '-készül', 'keserű-vadul', 'kerül-gazdagodik', 'keresztül+valósul', 'keresztül+részesül', 'kerekedik-gazdagodik', 'kerekedik-bontakozik', 'kékült-sötétül', 'karacsájul', 'jugoszlávul', 'jászul', 'jámborul', 'írül', '-igazodik', 'időtlenül', 'ide+üdül', 'ide+készülődik', 'ide+kergül', 'ide+kerekedik', 'idegesül', 'ide+egyesül', 'horgasodik-élesedik', 'hízik-kövéredik', 'helyt+bizonyul', 'helyesül', 'haza+pusztul', 'haza-készül', 'haza+kerekedik', 'haza+kékül', 'haza+honosodik', 'haza+fényesedik', 'haza+egyesül', 'hasasodik-púposodik', 'harsányul', 'hardul', 'gyűlik-vastagodik', 'gyűlik-sokasodik', 'gyepesedik-bokrosodik', 'gőzölődik-habosodik', 'gótul', 'furakszik-forrósodik', 'frappánsul', 'foszlott-foltosodik', 'fordul-gyorsul', 'fölé+szűkül', 'fölé+sötétedik', 'fölé+létesül', 'fenn+épül', 'fenn+egyesül', 'felül+simul', 'felül+bővül', 'felül+bizonyul', 'fel+legesedik', 'fel+kurdul', 'fel+konyul', 'fel+edésedik', 'fekszik-porosodik', 'fejlődik-vastagodik', 'fejlődik-gazdagodik', 'fásult-rezignál', '-fásul', 'fagyott-merevedik', 'fádul', 'evidensül', 'észre+tornyosul', 'észre+frissül', 'erősödött-ír', 'épül-omlik', 'épkézlábul', 'el+szánásodik', 'elő+valósul', 'előre+lelkesedik', 'előre+épül', 'elő+jogosul', 'elő+halkul', 'elő+enyhül', 'elő+boldogul', 'elő+adásodik', 'ellen+sokasodik', 'ellen+mordul', 'ellen+épül', 'ellen+egyesül', 'elé+tarul', 'élesedett-szélesedik', 'elegyedik-avatkozik', 'el+egészül', 'elé+erősödik', 'el+azonosul', 'elásodik', 'eladósul', 'egyet+búsul', 'egyesül-társul', 'édesedik-kegyesedik', 'dolgoz-készül', 'délcegül', 'decensül', 'csontosodik-lágyul', 'csehszlovákul', 'büdösödik-porosodik', 'bővült-változik', 'bővül-szépül', 'bitangul', 'bent+erősödik', 'benn+pusztul', 'be+lérozsdásodik', 'be+lékövesedik', 'bátorul', 'át+semmisül', 'át+kutyul', 'át+közül', 'át+alnedvesedik', 'át+alhasasodik', 'árnedvesedik', 'antikul', 'angolul-franciául-oroszul', 'alul+szabadul', 'alul+nősül', 'alul+népesedik', 'által+világosodik', 'által+ügyesedik', 'által+üdül', 'által+sűrűsödik', 'által+módosul', 'által+mentesül', 'által+mélyül', 'által+gyorsul', 'által+fiatalodik', 'által+enyhül', 'által+egyesül', 'által+egészül', 'álszentül', 'alá+zatosodik', 'alá+szentül', 'alá+párosul', 'alá+létesül', 'alakul-mélyül', 'alakul-épül', 'alá+könnyesedik', 'alá+kerekedik', 'alá+kábul', 'alá+gyengül', 'alá+fiatalodik', 'abba+pusztul'}

tsv = {}
rels = {}
with open(infile, 'r', encoding='utf-8') as fr:
    for i, line in enumerate(fr):
        line = line.strip()
        orig_cells = line.split('\t')
        cells = [i]
        cells.extend(orig_cells)
        tokeep = True

        if cells[3] in formdict.keys():
            cells[3] = formdict[cells[3]]
            cells[2] = cells[3] + '+' + cells[5]
            
        if cells[2].endswith('+sül') or cells[2].endswith('+ül'):
            tokeep = False
            
        if cells[3] not in prevset:
            tokeep = False
            
        if cells[2] in bad_lemmas:
            tokeep = False

        lc = rc = ''
        split_context = cells[-1].strip()
        if split_context.startswith('¤'):
            lc = 'NONE'
            split_context = re.sub(r'^¤ *', r'', split_context).strip()
        if split_context.endswith('¤'):
            rc = 'NONE'
            split_context = re.sub(r' *¤$', r'', split_context).strip()

        if split_context.count('¤') == 2:
            lc, kwic, rc = re.split(r' *¤ *', split_context)
        elif split_context.count('¤') == 0:
            lc = ''
            rc = ''
            kwic = split_context
        elif lc == 'NONE':
            lc = ''
            kwic, rc = re.split(r' *¤ *', split_context)
        elif rc == 'NONE':
            rc = ''
            lc, kwic = re.split(r' *¤ *', split_context)
        else:
            tokeep = False

        if tokeep:
            lc = re.sub(r' ([’),;?.:!])', r'\1', lc)
            lc = re.sub(r'([(]) ', r'\1', lc)
            kwic = re.sub(r' ([’),;?.:!])', r'\1', kwic)
            kwic = re.sub(r'([(]) ', r'\1', kwic)
            rc = re.sub(r' ([’),;?.:!])', r'\1', rc)
            rc = re.sub(r'([(]) ', r'\1', rc)
        
            cells.pop(-1)
            cells.extend([lc, kwic, rc])
            tsv[cells[0]] = cells

            if cells[5] not in rels.keys():
                rels[cells[5]] = {}
            if cells[3] not in rels[cells[5]].keys():
                rels[cells[5]][cells[3]] = 0
            rels[cells[5]][cells[3]] += 1

calcdict = {}
for verb, data in rels.items():
    prevs = noprevs = 0
    for prev, freq in data.items():
        if prev != '_':
            prevs += freq
    noprevs = 0 if '_' not in data.keys() else data['_']

    # az igekötős előfordulások számát elosztjuk az összes előfordulás számával
    freqsum = noprevs + prevs
    rel1 = round(prevs / freqsum, 2)

    # az adott igekötős előfordulások számát elosztjuk az összes igekötős előfordulás számával
    for prev, freq in data.items():
        if prev != '_':
            prevs_todiv = 0.00001 if prevs == 0 else prevs  # hogy ne legyen nullával való osztás
            rel2 = round(freq / prevs, 2)
            calcdict[prev + '+' + verb] = [str(freqsum), str(rel1), str(rel2)]
        else:
            calcdict[verb] = [str(freqsum), str(0.0), str(0.0)]

print(header)
counter = 0
for k, cells in tsv.items():
    if not re.search(r'^[0-9]+', cells[1]):
        try:
            cells.extend(calcdict[cells[2]])
            counter += 1
            cells[0] = str(counter)
            cells.pop(12)
            print('\t'.join(cells))
        except KeyError:
            pass
            
