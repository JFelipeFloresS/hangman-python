import requests
import bs4
from random_word import *
import random as r

def get_word_from_urban_dictionary(min, max):
    valid_word = False
    while not valid_word:
        page_number = r.randrange(1000)
        req = requests.get('https://www.urbandictionary.com/random.php?page='+str(page_number))
        # from #content get data-defid and each .word and .meaning
        soup = bs4.BeautifulSoup(req.text, 'lxml')
        words = soup.select('.word')
        word_array = []
        for word in words:
            word_array.append(word.text)
        meanings = soup.select('.meaning')
        m_array = []
        for meaning in meanings:
            m_array.append(meaning.text)
        for x in word_array:
            num = r.randrange(len(word_array))
            if min <= len(word_array[num]) <= max and not word_array[num].__contains__(' '):
                valid_word = True
                return word_array[num], m_array[num]

def get_word_from_vocabulary(min, max):
    req = requests.get('https://www.vocabulary.com/lists/258109')
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    words = soup.select('.word')
    word_array = []
    for word in words:
        word_array.append(word.text)
    meanings = soup.select('.definition')
    m_array = []
    for meaning in meanings:
        m_array.append(meaning.text)
    viable_word = False
    while not viable_word:
        num = r.randrange(len(word_array))
        if min <= len(word_array[num]) <= max and not word_array[num].__contains__(' '):
            viable_word = True
            return word_array[num], m_array[num]

def get_word_from_animals(min, max):
    req = requests.get('https://animalcorner.org/animals/')
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    words = soup.select('.one-third')
    word_array = []
    for word in words:
        word_array.append(word.text)
    viable_word = False
    while not viable_word:
        num = r.randrange(len(word_array))
        if min <= len(word_array[num]) <= max and not word_array[num].__contains__(' '):
            viable_word = True
            return word_array[num]

def get_word_noun(min, max):
    viable_word = False
    while not viable_word:
        req = requests.get('http://watchout4snakes.com/wo4snakes/Random/RandomWordPlus?level=95')
        soup = bs4.BeautifulSoup(req.text, 'lxml')
        words = soup.span
        print(words)
        word_array = []
        for word in words:
            print(word.type)
            word_array.append(word.text)
        if min <= len(word_array) <= max:
            viable_word = True
            return word_array[0].text

def get_word_from_random_words(min, max):
    valid_word = False
    guess_word = RandomWords()
    while not valid_word:
        try:
            word = guess_word.get_random_word(minLength=min, maxLength=max)
            valid_word = True
        except:
            valid_word = False

    return word
