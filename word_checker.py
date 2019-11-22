import os
import time
import pycurl
import sqlite3
from io import BytesIO
from bs4 import BeautifulSoup

class WordDirectory():
    def __init__(self, all_words):
        self.all_words = all_words
        try:
            self._init_memory()
            self.use_memory = True
        except Exception as e:
            print('|{}| error occurred. No memory will be using.'.format(e))
            self.use_memory = False

    def checkout(self, word):
        if self.use_memory():
            self.c.execute("Select * FROM mydictionary WHERE WORD LIKE '{}'".format(word))
            x = self.c.fetchone()
            if x:
                explain = dict(word=x[0], meanings=x[1], examples=x[2], date=x[3])
                return explain

        if word not in self.all_words:
            print('{} is not a valid word.'.format(word))
            return '{} is not a valid word.'.format(word)
        explain = checkout_word(word)
        explain['word'] = word
        explain['datestr'] = time.ctime()
        self._buffer_memory(explain)
        return explain

    def _buffer_memory(self, entry):
        if not self.use_memory:
            print('No memory buffered.')
            return
        print('Remembering {}.'.format(entry['word']))
        self.c.execute("INSERT INTO mydictionary VALUES ('{word}', '{meanings}', '{examples}', '{datestr}')".format(**entry))

    def _recall_memory(self):
        if not self.use_memory:
            print('No memory to recall.')
            return
        self.c.execute("Select word FROM mydictionary")
        print([e[0] for e in self.c.fetchall()])

    def _solid_memory(self):
        if not self.use_memory:
            print('No memory solidified.')
        self.conn.commit()

    def _init_memory(self):
        conn = sqlite3.connect(os.path.join('memory', 'memory.db'))
        c = conn.cursor()

        try:
            c.execute("SELECT word FROM mydictionary")
        except sqlite3.OperationalError as e:
            print(e)
            c.execute('''CREATE TABLE mydictionary (word text, meanings text, examples text, datestr text)''')
            c.execute("SELECT word FROM mydictionary")
        finally:
            print('I remember these words:')
            print(c.fetchall())

        self.conn = conn
        self.c = c


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

    # Output good tags for explain entry
    meanings = []
    for tag in explain.recursiveChildGenerator():
        if goodtag(tag):
            meanings.append(shrink(tag.get_text()))

    # Output all example sentences
    # Useless stuffs like 'Read more...' should be removed by shrink
    examples = []
    examples.append(shrink(assets.get_text()))

    output = {
        'meanings': '\n'.join(meanings),
        'examples': '\n'.join(examples)
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

print('Loading all_words done.', '{} words found.'.format(len(all_words)))

# Build my dictionary
mydictionary = WordDirectory(all_words)
