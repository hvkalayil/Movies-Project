from itertools import chain
import json

files = [
    '2022-2018.json',
    '2017-2014.json',
    '2013-2010.json',
    '2009.json',
    '2008.json',
    '2007-2005.json',
    '2004-2000.json',
    '1999-1996.json',
    '1995-1991.json',
]
data = []

for fi in files:
    with open('dataStore/'+fi,'r') as js:
        fData = json.load(js)
        data += fData
        
with open('dataStore/master.json','w') as master:
    master.write(json.dumps(data))
    
print(len(data))