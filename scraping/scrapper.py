
import json
from bs4 import BeautifulSoup
from requests import Timeout, head, request
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

bad = []
def getClearData(config):
    try:
        movie = config['MovieName'].replace(' ','+')
        y = int(config['ReleaseDate'].split('/')[-1])
        year = str(y+2000) if y < 80 else str(y+1900)
        url = "https://www.imdb.com/find?q="+movie+'+%28'+year+'%29'
        search = requests.get(url)

        link = ''
        searchSoup = BeautifulSoup(search.text,'html.parser')
        titles = searchSoup.select('tr[class*="findResult"]')
        for title in titles:
            tit = title.text
            if config['MovieName'] in tit and year in tit:
                link = title.a.get('href','')
                break

        if link.strip() == '':
            bad.append(config)
            return {}

        movieLink = 'https://www.imdb.com'+link
        print(movieLink)
        movie = requests.get(movieLink,timeout=10)
        soup = BeautifulSoup(movie.text,'html.parser')

        # Plot
        plots = soup.find_all('span', attrs={'data-testid':'plot-xl'})
        plot = plots[0].text

        # MetaData
        metaGod = soup.select('ul[class*="ipc-metadata-list"]')
        metaGodChild = metaGod[0]
        meta = metaGodChild.find_all('li')

        metaData = {}
        cast = []
        state = 'Director'
        metaData['Director'] = config['Director']
        metaData['Writer'] = ''
        for m in meta:
            mString = m.text
            if state == 'Director' and state not in mString:
                metaData['Director'] = mString
                state = 'Writer'

            elif state == 'Writer' and state not in mString:
                metaData['Writer'] = mString
                state = 'Stars'

            elif state == 'Stars' and state not in mString:
                cast.append(mString)
        if 'Cast' in config.keys():
            for cg in config['Cast']:
                if cg not in cast:
                    cast.append(cg)
        metaData['Cast'] = cast


        # Rating
        ratings = soup.select('div[class*="ipc-button__text"]')
        rating = ''
        for r in ratings:
            rString = r.text
            if '/' in rString:
                rating = rString.split('/')[0]
                break

        # Genre
        genres = soup.select('a[class*="ipc-chip"]')
        gen = []
        for g in genres:
            gen.append(g.text)
        if 'Genre' in config.keys():
            for cg in config['Genre']:
                if cg not in gen:
                    gen.append(cg)
        genre = gen

        # IMAGE
        images = soup.find_all('img')
        img = ''
        for image in images:
            img = str(image['src'])
            start = img.index('_')
            end = img.rindex('_')
            img = img[:start] + '@._V1_QL100_UY500_CR0,0,400,500' + img[end:]
            break

        obj = {
            'Plot': plot,
            'Director':metaData['Director'],
            'Writer':metaData['Writer'],
            'Cast':metaData['Cast'],
            'Rating' : rating,
            'Genre' : genre,
            'Poster' : img
        }
        return obj

    except Timeout:
        return{'timedout':True}
    except Exception as e:
        config['err'] = str(e)
        bad.append(config)
        return {}

with open('dataStore/master-beauty.json','r') as masterIn:
    masterData = json.load(masterIn)

clearData = []
for i in range(0,len(masterData)):
    item = masterData[i]
    print(item['MovieName'])

    data = getClearData(item)

    dataSet = data.keys()
    if 'timedout' in dataSet:
        print(str(len(clearData)) + ' Movies Done.')
        print('Imdb timedout while getting '+item['MovieName'])
        break
    for key in item.keys():
        if key not in dataSet:
            data[key] = item[key]

    clearData.append(data)

print(str(len(bad)) + ' Bad Movies')
with open('dataStore/bad.json','w') as bd:
    bd.write(json.dumps(bad))

print(str(len(bad) - len(clearData)) + ' Clean Movies')
with open('dataStore/cleanData.json','w') as fp:
    fp.write(json.dumps(clearData))