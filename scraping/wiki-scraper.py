import datetime
import json
from os import link
import requests

movie = ''
director = ''
cast = []
studio = []
ref = ''
ott = ''
dt = datetime.datetime.now()
monthsString = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
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
        month = 0
        year = config['year']

        state = ''
        start = False
        movie = ''
        obj = {}
        for line in wiki_read:
            if '<table class="wikitable">' in line:
                start = True

            if '</table>' in line:
                start = False

            if start != True:
                continue

            if '<td rowspan' in line and '<br />' in line:
                m = line.split(
                    '</b>')[0].split('<b>')[-1].replace('<br />', '').upper()
                month = monthsString.index(m)+1
                state = 'Day'
                continue
            if '<td rowspan' in line and state == 'Day':
                day = line.split(
                    '</b>')[0].split('>')[-1].replace('''\n''', '')
                state = 'Movie'
                continue

            if '<td' in line and '<i>' in line:
                movie = line.split(
                    '<td><i>')[-1].split('</i>')[0].split('</a>')[0].split('>')[-1]
                obj['MovieName'] = movie
                state = 'Director'
                continue

            if '<td>' in line and state == 'Director':
                director = line.split(
                    '<td>')[-1].split('</i>')[0].split('</a>')[0].split('>')[-1].replace('''\n''', '')
                obj['Director'] = director
                state = 'Cast'
                continue

            if '<td>' in line and state == 'Cast':
                casts = line.split('<td>')[-1].split(',')
                cast = []
                for c in casts:
                    cast.append(c.split('</a>')
                                [0].split('>')[-1].replace('''\n''', ''))
                obj['Cast'] = cast
                if config['delimiter'] == 'Cast':
                    state = ''
                    dt = datetime.datetime(
                        year=year, month=month, day=int(day))
                    obj['ReleaseDate'] = dt.strftime('%x')
                    result.append(obj)
                    obj = {}
                else:
                    state = 'Studio'
                continue

            if '<td>' in line and state == 'Studio':
                studios = line.split(
                    '<td>')[-1].replace('''\n''', '').split(',')
                studio = []
                for s in studios:
                    studio.append(
                        s.split('</a>')[0].split('>')[-1].replace('''\n''', ''))
                obj['Studio'] = studio
                if config['delimiter'] == 'Studio':
                    state = ''
                    dt = datetime.datetime(
                        year=year, month=month, day=int(day))
                    obj['ReleaseDate'] = dt.strftime('%x')
                    result.append(obj)
                    obj = {}
                else:
                    state = 'Ref'
                continue

            if '<td>' in line and state == 'Ref':
                ref = line.split(
                    '<td>')[-1].split('<sup id=')[0].replace('''\n''', '')
                obj['Ref'] = ref
                state = 'Ott'
                continue

            if '<td>' in line and state == 'Ott':
                ott = line.split(
                    '<td>')[-1].split('</a>')[0].split('>')[-1].replace('''\n''', '')
                obj['Ott'] = ott
                state = ''
                dt = datetime.datetime(year=year, month=month, day=int(day))
                obj['ReleaseDate'] = dt.strftime('%x')
                result.append(obj)
                obj = {}
                continue
    return result


scraps = [
     {'link': 'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_2009', 'year': 2009, 'delimiter': 'Cast', 'count': 193},
    # {'link': 'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_2008', 'year': 2008, 'delimiter': 'Cast', 'count': 193},
    # {'link': 'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_2007', 'year': 2007, 'delimiter': 'Cast', 'count': 193},
    # {'link': 'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_2006', 'year': 2006, 'delimiter': 'Cast', 'count': 193},
    # {'link': 'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_2005', 'year': 2005, 'delimiter': 'Cast', 'count': 193},
    # {'link': 'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_2004', 'year': 2004, 'delimiter': 'Cast', 'count': 193},
    # {'link': 'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_2003', 'year': 2003, 'delimiter': 'Cast', 'count': 193},
    # {'link': 'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_2002', 'year': 2002, 'delimiter': 'Cast', 'count': 193},
    # {'link': 'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_2001', 'year': 2001, 'delimiter': 'Cast', 'count': 193}
]

# r = []
# for o in range(10):
#     y = 2010 - o
#     r.append({
#         'link': 'https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_'+str(y),
#         'year': y,
#         'delimiter': 'Cast',
#         'count': 193
#     })
# print(r)


dataSet = []
for scrap in scraps:
    old = len(dataSet)
    dataSet += getDataSet(scrap)
    l = old - len(dataSet)
    print(str(scrap['year']) + ' - ' + str(l))

print(len(dataSet))

with open('dataStore/sample.json','w') as f:
    f.write(json.dumps(dataSet))
