import json
import random

with open('vocabulary5000_all_words.json', 'r') as f:
    s = f.readline()
    all_words = json.loads(s)

def random_word():
    return random.choice(all_words)