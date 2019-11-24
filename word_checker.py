import os
import time
import requests
import sqlite3
from io import BytesIO
from bs4 import BeautifulSoup

class WordDirectory():
    def __init__(self, quiet=False):
        try:
            self._init_memory(quiet=quiet)
            self.use_memory = True
        except Exception as e:
            print('|{}| error occurred. No memory will be using.'.format(e))
            self.use_memory = False

    def checkout(self, word, quiet=False):
        if self.use_memory:
            self.c.execute("Select * FROM mydictionary WHERE word LIKE '{}'".format(word))
            x = self.c.fetchone()
            if x:
                if not quiet:
                    print('I remember {}.'.format(word))
                explain = dict(word=x[0], dictname=x[1], meanings=x[2], examples=x[3])
                return explain

        explain = checkout_word(word, quiet=True)

        if all([explain['meanings']]):
            self._buffer_memory(explain, quiet)
        else:
            print('{} is broken, not remember.'.format(word))

        return explain

    def _buffer_memory(self, entry, quiet):
        if not self.use_memory:
            print('No memory buffered.')
            return
        if not quiet:
            print('Remembering {}.'.format(entry['word']))
        self.c.execute("INSERT INTO mydictionary(word, dictname, meanings, examples) VALUES(?, ?, ?, ?)",
        (entry['word'], entry['dictname'], entry['meanings'], entry['examples']))

    def _recall_memory(self):
        if not self.use_memory:
            print('No memory to recall.')
            return
        self.c.execute("Select word FROM mydictionary")
        return [e[0] for e in self.c.fetchall()]

    def _solid_memory(self):
        if not self.use_memory:
            print('No memory solidified.')
        self.conn.commit()

    def _init_memory(self, quiet):
        conn = sqlite3.connect(os.path.join('memory', 'memory.db'))
        c = conn.cursor()

        try:
            c.execute("SELECT word FROM mydictionary")
        except sqlite3.OperationalError as e:
            print(e)
            c.execute('''CREATE TABLE mydictionary (word text, dictname text, meanings text, examples text)''')
            c.execute("SELECT word FROM mydictionary")
        finally:
            print('I remember [{}] words.'.format(len(c.fetchall())))
            try:
                c.execute("CREATE INDEX word_index ON mydictionary (word)")
            except sqlite3.OperationalError as e:
                pass
            c.execute("PRAGMA table_info(mydictionary)")
            print('Format are.')
            [print(e) for e in c.fetchall()]
            if not quiet:
                print('I remember these words:')
                print([e[0] for e in c.fetchall()])

        self.conn = conn
        self.c = c


# Fetch html from given url
def fetch_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729)'}
    response = requests.get(url, headers=headers)
    return response.content


# Checkout the word from collinsdictionary.com
def checkout_word(word, quiet=False):

    def _print(message, quiet=quiet):
        if not quiet:
            print('<--', message, '-->')

    _print('{}'.format(word))
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
        string = string.replace('\n)', ')').replace(')', ')\n').replace('Read more…', '').replace('Show more...','')
        # Return stripped string
        return string.strip()

    _print(url)
    _print('Available dictionaries:')
    dictionary_name = ''
    for divs in soup.find_all('div', 'dictionaries dictionary'):
        for div in divs.recursiveChildGenerator():
            if hasattr(div, 'attrs'):
                if 'class' in div.attrs:
                    cls = ' '.join(div.attrs['class'])
                    if cls.startswith('dictionary '):
                        _print(cls)
                        # Setup dictionary_name as first met dictionary
                        if not dictionary_name:
                            dictionary_name = cls

    # Get explain entry using dictionary [dictionary_name]
    explain = soup.find('div', dictionary_name)
    _print('Using {}'.format(dictionary_name))

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

    # Output good tags for explain entry
    meanings = []
    if explain:
        for tag in explain.recursiveChildGenerator():
            if goodtag(tag):
                meanings.append(shrink(tag.get_text()))

    # Output all example sentences
    # Useless stuffs like 'Read more...' should be removed by shrink
    examples = []
    if assets:
        examples.append(shrink(assets.get_text()))

    output = {
        'word': word,
        'dictname': dictionary_name,
        'meanings': '\n'.join(meanings),
        'examples': '\n'.join(examples),
        }
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

for e in ['regulatory', 'sharply']:
    all_words.pop(all_words.index(e))

print('Loading all_words done.', '{} words found.'.format(len(all_words)))

# Build my dictionary
mydictionary = WordDirectory(quiet=True)
