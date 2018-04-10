# -*- coding: utf-8 -*-
from problem1 import Corpus

class Ngram(object):
    def __init__(self, corpus):
        self._filename = '1998-01-105-带音.txt'
        self._word_perplexity = dict()
        self._word_number = 0

        self._corpus = corpus

class Unigram(Ngram):
    def __init__(self, corpus):
        Ngram.__init__(self, corpus)
    
    def train(self):
        # Read the file
        with open(self._filename) as f:
            paragraphs = f.readlines()
            for paragraph in paragraphs:
                paragraph = paragraph.split()  # Split words
                for x in paragraph:
                    x = x.split('/')    # divide
                    if '-' in x[0] and x[1] == 'm': # the beginning of a paragraph
                        continue
                    if x[0] == '':
                        continue
                    # Remove bracket []
                    if len(x[0]) > 0 and x[0][0] == '[':
                        x[0] = x[0][1:]
                        x[1] = x[1].split(']')[0]
                    # Increase counter
                    if x[0] in self._word_perplexity:
                        self._word_perplexity[x[0]] += 1
                    else: # zero
                        self._word_perplexity[x[0]] = 1
                    self._word_number += 1
        # and calculate the probability
        for x in self._word_perplexity:
            self._word_perplexity[x] = (self._word_perplexity[x] + 1) / \
                (self._word_number + len(self._word_perplexity))
    
    def _calc_word_perplexity(self, word):
        if word in self._word_perplexity:
            return self._word_perplexity[word]
        else:
            return 1 / (self._word_number + len(self._word_perplexity))
    
    def evaluation(self, sentence):
        segmented_words = self._corpus.seg(sentence)
        length = len(segmented_words)
        result = 1
        for word in segmented_words:
            para = self._calc_word_perplexity(word)
            result *= para**(-1/length)
            #print(para)
        return result

class Bigram(Ngram):
    def __init__(self, corpus):
        Ngram.__init__(self, corpus)
        self._single_word = dict()
    
    def train(self):
        # assume that p(word|START) = p(word|。)
        START = '。'
        # Read the file
        with open(self._filename) as f:
            paragraphs = f.readlines()
            prev_word = START
            self._single_word[''] = 1
            for paragraph in paragraphs:
                paragraph = paragraph.split() # Split words
                for x in paragraph:
                    x = x.split('/') # divide
                    if '-' in x[0] and x[1] == 'm': # the beginning of a paragraph
                        continue
                    if x[0] == '':
                        continue
                    # Remove bracket []
                    if len(x[0]) > 0 and x[0][0] == '[':
                        x[0] = x[0][1:]
                        x[1] = x[1].split(']')[0]
                    # Increase single word counter
                    if x[0] in self._single_word:
                        self._single_word[x[0]] += 1
                    else: # zero
                        self._single_word[x[0]] = 1
                    # Increasing tuple counter
                    if (prev_word, x[0]) in self._word_perplexity:
                        self._word_perplexity[(prev_word, x[0])] += 1
                    else:
                        self._word_perplexity[(prev_word, x[0])] = 1
                    self._word_number += 1
                    '''
                    if x[0] == START:
                        prev_word = ''
                        self._single_word[''] += 1
                    else:
                        prev_word = x[0]
                    '''
                    prev_word = x[0]
        # and calculate the probability
        for x in self._word_perplexity:
            self._word_perplexity[x] = (self._word_perplexity[x] + 1) / \
                (self._single_word[x[0]] + len(self._single_word))
        
    def _calc_word_perplexity(self, word):
        if word in self._word_perplexity:
            return self._word_perplexity[word]
        else:
            if word[0] in self._single_word:
                return 1 / (self._single_word[word[0]] + len(self._single_word))
            else:
                return 1 / len(self._single_word)
        
    def evaluation(self, sentence):
        segmented_words = self._corpus.seg(sentence)
        length = len(segmented_words)
        prev_word = '。'
        result = 1
        for word in segmented_words:
            para = self._calc_word_perplexity((prev_word, word))
            result *= para**(-1/length)
            prev_word = word
            #print(para)
        return result

class Trigram(Ngram):
    def __init__(self, corpus):
        Ngram.__init__(self, corpus)
        self._single_word = set()
        self._double_word = dict()
    
    def train(self):
        # assume that p(word|START) = p(word|。)
        START = '。'
        # Read the file
        with open(self._filename) as f:
            paragraphs = f.readlines()
            prev_word = ('START0', 'START1')
            self._double_word[('START0', 'START1')] = 1
            for paragraph in paragraphs:
                paragraph = paragraph.split() # Split words
                for x in paragraph:
                    x = x.split('/') # divide
                    if '-' in x[0] and x[1] == 'm': # the beginning of a paragraph
                        continue
                    if x[0] == '':
                        continue
                    # Remove bracket []
                    if len(x[0]) > 0 and x[0][0] == '[':
                        x[0] = x[0][1:]
                        x[1] = x[1].split(']')[0]
                    # Increase double word counter
                    if (prev_word[1], x[0]) in self._double_word:
                        self._double_word[(prev_word[1], x[0])] += 1
                    else: # zero
                        self._double_word[(prev_word[1], x[0])] = 1
                    # Increasing tuple counter
                    if (prev_word[0], prev_word[1], x[0]) in self._word_perplexity:
                        self._word_perplexity[(prev_word[0], prev_word[1], x[0])] += 1
                    else:
                        self._word_perplexity[(prev_word[0], prev_word[1], x[0])] = 1
                    self._word_number += 1
                    self._single_word.add(x[0])
                    if x[0] == START:
                        prev_word = ('START0', 'START1')
                        self._double_word[('START0', 'START1')] += 1
                    else:
                        prev_word = (prev_word[1], x[0])
        # and calculate the probability
        for x in self._word_perplexity:
            self._word_perplexity[x] = (self._word_perplexity[x] + 1) / \
                (self._double_word[(x[0], x[1])] + len(self._single_word))
        
    def _calc_word_perplexity(self, word):
        if word in self._word_perplexity:
            return self._word_perplexity[word]
        else:
            if (word[0], word[1]) in self._double_word:
                return 1 / (self._double_word[(word[0], word[1])] + len(self._single_word))
            else:
                return 1 / len(self._single_word)
        
    def evaluation(self, sentence):
        segmented_words = self._corpus.seg(sentence)
        length = len(segmented_words)
        prev_word = ('START0', 'START1')
        result = 1
        for word in segmented_words:
            para = self._calc_word_perplexity((prev_word[0], prev_word[1], word))
            result *= para**(-1/length)
            if word == '。':
                prev_word = ('START0', 'START1')
            else:
                prev_word = (prev_word[1], word)
            #print(para)
        return result

if __name__ == '__main__':
    corpus = Corpus()
    print('Training corpus...', end='', flush=True)
    corpus.train()
    print('Ok.')
    u = Unigram(corpus)
    b = Bigram(corpus)
    t = Trigram(corpus)
    print('Training unigram...', end='', flush=True)
    u.train()
    print('Ok.')
    print('Training bigram...', end='', flush=True)
    b.train()
    print('Ok.')
    print('Training trigram...', end='', flush=True)
    t.train()
    print('Ok.')

    while True:
        print('>> ', end='')
        sentence = input()
        print('Unigram:', u.evaluation(sentence))
        print('Bigram:', b.evaluation(sentence))
        print('Trigram:', t.evaluation(sentence))
    
