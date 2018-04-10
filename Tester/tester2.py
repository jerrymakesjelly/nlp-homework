#-*- coding:utf-8 -*-

# Please copy myself to the folder `Problem1-3`

import problem2

class Tester(object):
    def __init__(self, begin_position, end_position=''):
        self._filename = '1998-01-105-带音.txt'
        self._corpus = Corpus()
        self._corpus.train(begin_position)
        print('The corpus is well trained.')

        self._sentences = str()
        self._word_number = 0
        self._load(begin_position)
        print('The test text is ready. Words:'+str(self._word_number))

        self._unigram = Unigram(self._corpus)
        self._unigram.train()
        self._bigram = Bigram(self._corpus)
        self._bigram.train()
        self._trigram = Trigram(self._corpus)
        self._trigram.train()
        print('The N-grams models are ready.')
    
    def _load(self, begin_position, end_position=''):
        with open(self._filename) as f:
            paragraphs = f.readlines()
            enable = False
            for paragraph in paragraphs:
                paragraph = paragraph.split() # split in words
                for x in paragraph:
                    x = x.split('/')
                    if '-' in x[0] and x[1] == 'm': # Header of paragraph
                        if x[0] == begin_position: # Start reading
                            enable = True
                        if x[0] == end_position: # end reading
                            return
                    else:
                        if enable: # Words we should load
                            # Remove bracket []
                            if len(x[0]) > 0 and x[0][0] == '[':
                                x[0] = x[0][1:]
                                x[1] = x[1].split(']')[0]
                            self._sentences += x[0]
                            self._word_number += 1
    
    def perplexity(self):
        unigram_pp = self._unigram.evaluation(self._sentences)
        bigram_pp = self._bigram.evaluation(self._sentences)
        trigram_pp = self._trigram.evaluation(self._sentences)

        return {'Perplexity of unigram': unigram_pp, 'Perplexity of bigram': bigram_pp, 'Perplexity of trigram': trigram_pp}

if __name__=='__main__':
    t = Tester('19980124-09-005-001')
    #t = Tester('19980131-04-013-027')
    pp = t.perplexity()
    for x in pp:
        print(x+':', pp[x])