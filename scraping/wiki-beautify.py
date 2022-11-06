from itertools import chain
import json


with open('dataStore/master.json','r') as masR:
    data = json.load(masR)

res = list(set(chain.from_iterable(sub.keys() for sub in data)))
print(res)

for item in data:
    keys = item.keys()
    if 'Cast' in keys:
        cast = []
        for st in item['Cast']:
            if st == '' or st == '\n' or '=' in st:
                pass
            else:
                cast.append(str(st.replace('\n','').strip()))
        item['Cast'] = cast

    if 'Studio' in keys:
        cast = []
        for st in item['Studio']:
            if st == '' or st == '\n' or '=' in st:
                pass
            else:
                cast.append(str(st.replace('\n','').strip()))
        item['Studio'] = cast

    if 'Genre' in keys:
        cast = []
        for st in item['Genre']:
            if st == '' or st == '\n' or '=' in st:
                pass
            else:
                cast.append(str(st.replace('\n','').strip()))
        item['Genre'] = cast

    if 'ScreenPlay' in keys:
        cast = []
        for st in item['ScreenPlay']:
            if st == '' or st == '\n' or '=' in st:
                pass
            else:
                cast.append(str(st.replace('\n','').strip()))
        item['ScreenPlay'] = cast

    if 'Producer' in keys:
        cast = []
        for st in item['Producer']:
            if st == '' or st == '\n' or '=' in st:
                pass
            else:
                cast.append(str(st.replace('\n','').strip()))
        item['Producer'] = cast

    if 'Director' in keys:
        item['Director'] = item['Director'].replace('\n','').strip()
    if 'Ott' in keys:
        item['Ott'] = item['Ott'].replace('\n','').strip()

with open('dataStore/master-beauty.json','w') as masW:
    masW.write(json.dumps(data))