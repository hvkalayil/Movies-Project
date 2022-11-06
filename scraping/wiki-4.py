import datetime
import json
from os import link
from bs4 import BeautifulSoup
import requests

movie = ''
director = ''
cast = []
studio = []
ref = ''
ott = ''
dt = datetime.datetime.now()
monthString = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
               'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']


def getDataSet(config):
    res = requests.get(config['link'])
    start = False

    with open('wiki.txt', 'w', encoding='utf-8') as wiki:
        wiki.write(res.text)

    with open('wiki.txt', 'r', encoding='utf-8') as wiki_read:
        result = []
        bad = []

        day = 1
        month = 1
        year = config['year']
        dt = datetime.datetime(int(year), int(month), int(day))

        state = ''
        start = False
        movie = ''
        obj = {}
        insert = False
        for line in wiki_read:
            if '<table' in line and 'wikitable' in line:
                start = True

            if '</table>' in line:
                start = False

            if start != True:
                continue

            if '<td><i>' in line:
                parts = line.split('</a></i>')[0].split('=')
                if len(parts) > 1:
                    movie = parts[-1].split('>')[-1]
                    url = parts[1].replace('"', '').replace('title', '')
                else:
                    movie = parts[-1].split('</i>')[0].split(
                        '>')[-1].replace('''\n''', '')
                    url = ''
                if '/wiki/' in url:
                    subRes = requests.get('https://en.wikipedia.org'+url)
                    with open('wiki-sub.txt', 'w', encoding='utf-8') as wikiSub:
                        wikiSub.write(subRes.text)

                    with open('wiki-sub.txt', 'r', encoding='utf-8') as wikiSubRead:
                        soup = BeautifulSoup(wikiSubRead, 'html.parser')
                        for strr in soup.strings:
                            datePartsA = strr.split(' ')
                            datePartsB = strr.split('-')
                            if len(datePartsA) == 3:
                                day = datePartsA[0].strip()
                                month = datePartsA[1].strip().upper()
                                year = datePartsA[2].strip()
                                if day.isnumeric() and month in monthString and year.isnumeric():
                                    month = monthString.index(month)+1
                                    dt = datetime.datetime(
                                        int(year), month, int(day))
                                    break

                            if len(datePartsB) == 3:
                                year = datePartsB[0].strip()
                                month = datePartsB[1].strip()
                                day = datePartsB[2].strip()
                                if day.isnumeric() and month.isnumeric() and year.isnumeric():
                                    dt = datetime.datetime(
                                        int(year), int(month), int(day))
                                    break
                else:
                    if len(result) != 0:
                        oldDate = result[-1]['ReleaseDate'].split('/')
                        month = oldDate[0]
                        day = oldDate[1]
                        year = oldDate[2]
                    dt = datetime.datetime(
                        int(year)+2000, int(month), int(day))
                obj['MovieName'] = movie
                obj['ReleaseDate'] = dt.strftime('%x')
                state = 'Cast'

            elif '<td>' in line and state == 'Director':
                obj['Director'] = line.split('</a>')[0].split('>')[-1]
                insert = True

            elif '<td>' in line and state == 'Cast':
                casts = line.split(',')
                cast = []
                for c in casts:
                    cast.append(c.split('</a>')[0].split('>')[-1])
                obj['Cast'] = cast
                state='Director'

            elif '<td>' in line and state == 'Prodcuer':
                producers = line.split(',')
                producer = []
                for p in producers:
                    producer.append(
                        p.split('</a>')[0].split('>')[-1].replace('<td>', '').replace('''\n''', ''))
                obj['ScreenPlay'] = producer
                if config['delimiter'] == 'Producer':
                    insert = True
                else:
                    state='Cast'

            if insert:
                insert = False
                result.append(obj)
                print(obj['MovieName'])
                state = ''
                obj = {}
    return result


scraps = [
    {'link': 'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_1990', 'year': 1990, 'delimiter': 'Cast', 'count': 193}
]

# r = []
# for o in range(10):
#     y = 2000 - o
#     r.append({
#         'link': 'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_'+str(y),
#         'year': y,
#         'delimiter': 'Cast',
#         'count': 193
#     })
# print(r)


dataSet = []
for scrap in scraps:
    data = getDataSet(scrap)
    dataSet += data
    print(str(scrap['year']) + ' - ' + str(len(data)))

print(len(dataSet))

with open('dataStore/1990.json','w') as f:
    f.write(json.dumps(dataSet))
