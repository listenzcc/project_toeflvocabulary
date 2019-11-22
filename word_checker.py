import os
import pycurl
from io import BytesIO
from bs4 import BeautifulSoup

class WordDirectory():
    def __init__(self, all_words):
        self.all_words = all_words
        self.memory = self._init_memory()

    def checkout(self, word):
        if word not in self.all_words:
            print('{} is not a valid word'.format(word))
            return '{} is not a valid word'.format(word)
        explain = checkout_word(word)
        self._buffer_memory(word, explain)
        return explain

    def _buffer_memory(self, word, explain):
        # print('Remember {} as \n{}'.format(word, explain))
        pass

    def _solid_memory(self):
        pass

    def _init_memory(self):
        return 0


# Fetch html from given url
def fetch_url(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729)')
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    return buffer.getvalue()


# Checkout the word from collinsdictionary.com
def checkout_word(word):
    print('{}'.format(word))
    url = 'https://www.collinsdictionary.com/dictionary/english/{}'.format(word)
    # Fetch html
    html = fetch_url(url)
    # Creat soup
    soup = BeautifulSoup(html, features='lxml')
    # Extract all scripts, we don't need them in the content
    [s.extract() for s in soup('script')]

    # Shrinking string by removing '\n\n' and other stuffs like 'Read more...' 
    def shrink(string):
        # Removing '\n\n'
        while '\n\n' in string:
            string = string.replace('\n\n', '\n')
        # Removing other stuffs like 'Read more...'
        string = string.replace('\'', '\"')
        string = string.replace('\n)', ')').replace(')', ')\n').replace('Read more…', '').replace('Show more...','')
        # Return stripped string
        return string.strip()

    # Get explain entry using Cob_Adv_Brit, don't know what dictionary it is, but it seems pretty.
    explain = soup.find('div', 'dictionary Cob_Adv_Brit')
    # Get example sentences containing the word, it is called assets in current site
    assets = soup.find('div', 'assets')

    # To tell if give tag is what we want
    def goodtag(tag):
        # Return True if its class is either 'hom' for meaning or 'mini_h2' for pronounce
        if hasattr(tag, 'attrs'):
            return any([tag.attrs == {'class': ['hom']},
                        tag.attrs == {'class': ['mini_h2']}])
        # Return False for others
        return False

    output = {
        'meanings': [],
        'examples': []
        }

    # Output good tags for explain entry
    for tag in explain.recursiveChildGenerator():
        if goodtag(tag):
            output['meanings'].append(shrink(tag.get_text()))

    # Output all example sentences
    # Useless stuffs like 'Read more...' should be removed by shrink
    output['examples'].append(shrink(assets.get_text()))

    return output


# Get all the words from html files in raw_htmls folder
def get_words(fname, name='div', attrs={'class': 'glface'}):
    with open(fname, 'r') as f:
        html = f.readlines()
        soup = BeautifulSoup(''.join(html), features='lxml')
        entries = soup.find_all(name, attrs=attrs)
        return [e.get_text() for e in entries]

all_words = []

# There are 10 html files well organized
for j in range(10):
    fname = 'raw_htmls/v{}.html'.format(j+1)
    # print(fname)
    all_words += get_words(fname)

print('Loading all_words done.', '{} words found.'.format(len(all_words)))

# Build my dictionary
mydictionary = WordDirectory(all_words)
