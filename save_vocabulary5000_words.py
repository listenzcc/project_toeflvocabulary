# %%
import json
from bs4 import BeautifulSoup

def get_words(fname, name='div', attrs={'class': 'glface'}):
    with open(fname, 'r') as f:
        html = f.readlines()
        soup = BeautifulSoup(''.join(html))
        entries = soup.find_all(name, attrs=attrs)
        return [e.get_text() for e in entries]

all_words = []

for j in range(10):
    fname = 'raw_htmls/v{}.html'.format(j+1)
    print(fname)
    all_words += get_words(fname)

print(all_words)

# %%
with open('vocabulary5000_all_words.json', 'w') as f:
    f.write(json.dumps(all_words))

# %%
