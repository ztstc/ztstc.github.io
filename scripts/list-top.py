"""List top-level files/dirs of ztstc/note."""
import urllib.request
import json
from urllib.parse import quote

url = 'https://api.github.com/repos/ztstc/note/contents/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github+json'})
items = json.loads(urllib.request.urlopen(req, timeout=15).read().decode('utf-8'))
for it in items:
    name = it['name']
    typ = 'DIR ' if it['type'] == 'dir' else 'FILE'
    size = it.get('size', 0)
    if typ == 'DIR ':
        print(f'{typ} /{name}')
    else:
        print(f'{typ} /{name}  ({size} bytes)')
