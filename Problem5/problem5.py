# -*- coding:utf-8 -*-
import os
import codecs
import string
import math
import random

class TextClassifier(object):
    def __init__(self):
        self._path = './20_newsgroups/20_newsgroups'
        self._classes = dict()
        self._word_in_classes = dict()
        self._mails = dict()

    def _trainning_preprocessor(self, path):
        catalog = os.listdir(path)
        for x in catalog:
            subpath = os.path.join(path, x)
            if os.path.isdir(subpath):
                self._trainning_processor(x, subpath)
    
    def _trainning_processor(self, catalog, directory):
        mails = os.listdir(directory)
        for mail in mails:
            with codecs.open(os.path.join(directory, mail), 'r', 'utf-8') as f:
                paragraphs = dict()
                try:
                    paragraphs = f.readlines()
                except UnicodeDecodeError:
                    pass
                for paragraph in paragraphs:
                    # Remove punctuations
                    for c in string.punctuation:
                        paragraph = paragraph.replace(c, ' ')
                    # Split
                    paragraph = paragraph.split()
                    for x in paragraph:
                        x = x.lower()
                        if catalog in self._word_in_classes:
                            if x in self._word_in_classes[catalog]:
                                self._word_in_classes[catalog][x] += 1
                            else:
                                self._word_in_classes[catalog][x] = 1
                            self._classes[catalog] += 1
                        else:
                            self._classes[catalog] = 1
                            self._word_in_classes[catalog] = dict()
                            self._word_in_classes[catalog][x] = 1
            if catalog in self._mails:
                self._mails[catalog] += 1
            else:
                self._mails[catalog] = 1
        # Compute 1
        for cat in self._word_in_classes:
            for x in self._word_in_classes[cat]:
                self._word_in_classes[cat][x] /= self._classes[cat]
        print(catalog)
    
    def train(self):
        self._trainning_preprocessor(self._path)
        # Compute 2
        total = 0
        for mail in self._mails:
            total += self._mails[mail]
        for mail in self._mails:
            self._mails[mail] /= total
    
    def _log_prob(self, word, clas):
        if clas in self._word_in_classes and word in self._word_in_classes[clas]:
            return math.log(self._word_in_classes[clas][word])
        else:
            return -math.inf

    def _argmax(self, di):
        maxarg = list(di.keys())[0]
        for x in di:
            if di[x] > di[maxarg]:
                maxarg = x
        return maxarg

    def classify(self, filename):
        classes_nbc = {x:0 for x in self._classes}
        with codecs.open(filename, 'r', 'utf-8') as f:
            paragraphs = dict()
            try:
                paragraphs = f.readlines()
            except UnicodeDecodeError:
                pass
            for paragraph in paragraphs:
                # Remove punctuations
                for c in string.punctuation:
                    paragraph = paragraph.replace(c, ' ')
                # Split
                paragraph = paragraph.split()
                for x in paragraph:
                    x = x.lower()
                    for clas in classes_nbc:
                        classes_nbc[clas] += self._log_prob(x, clas)
            for clas in classes_nbc:
                classes_nbc[clas] += math.log(self._mails[clas])
        return self._argmax(classes_nbc)

if __name__ == '__main__':
    tc = TextClassifier()
    print('Training text classifier...')
    tc.train()
    print("The text clasifier is well trained.")
    print("Input the PATH of a text file which is going to be analyzed.")
    while True:
        print('>> ', end='')
        print(tc.classify(input()))