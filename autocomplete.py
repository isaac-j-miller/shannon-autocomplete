import string
import random
import time
import re
import requests
import os


class AutoCompleter():
    def __init__(self, source=None, title=None):
        random.seed(time.time())
        self.data = ''
        self.raw_data = ''
        self.words = ['']
        self.num_words = 0
        if source is not None:
            self.add_reference(source, title)

    def add_reference(self, source, title=None):
        if 'http' in source or 'www.' in source or '//' in source:
            req = requests.get(source, allow_redirects=True)
            content=req.content
            if title is None:
                title ='text'
            fname = title+'.txt'
            fname = fname.replace(' ', '_')
            while fname in os.listdir(os.getcwd()):
                with open(fname,'rb') as f:
                    if f.read() == req.content:
                        break
                fname_list = fname.split('.')
                fname_list[0]+='_'
                fname = '.'.join(fname_list)
            with open(fname, 'wb') as f:
                f.write(content)
            source = fname

        with open(source, 'rb') as f:
            self.raw_data += ' '+ f.read().decode('utf-8', '')
        self.data += ''.join([l if l in string.ascii_letters + ' u\2014u\2013' else ' ' for l in self.raw_data])
        self.data = re.sub(' +', ' ', self.data)
        self.words += self.data.lower().split(' ')
        self.words = [word for word in self.words if word]
        self.num_words = len(self.words)

    def autocomplete_word(self, fragment):
        fraglen = len(fragment)
        tempSource = [word for word in self.words if word[:fraglen] == fragment]
        if tempSource:
            index = random.randint(0, len(tempSource)-1)
            return tempSource[index]
        else:
            return ''

    def guess_next_word(self, word):
        if word in self.words:
            matchIndices = [index+1 for mword,index in zip(self.words, range(len(self.words)))
                            if mword == word and index + 1 < self.num_words]
            index = random.choice(matchIndices)
            return self.words[index]
        return ''

    def generate_string(self, length, seed=None):
        if seed is None:
            words = [random.choice(self.words)]
        else:
            words = [seed]
        for i in range(length):
            words.append(self.guess_next_word(words[-1]))
        return ' '.join(words)


if __name__ == '__main__':
    ac = AutoCompleter('http://www.gutenberg.org/cache/epub/345/pg345.txt','dracula')
