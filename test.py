import codecs

with codecs.open('db.json', 'r', 'utf-8-sig') as f:
    data = f.read()

with open('db.json', 'w', encoding='utf-8') as f:
    f.write(data)
