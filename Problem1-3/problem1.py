# -*- coding:utf-8 -*-

class Corpus(object):
    def __init__(self):
        self._filename = '1998-01-105-带音.txt'
        self._root = {'word':'', 'next':[], 'child':[]}
        self._unreconized = 0
    
    def train(self, end_paragraph=''):
        # Read the file
        with open(self._filename) as f:
            paragraphs =  f.readlines()
            for paragraph in paragraphs: # For each paragraph
                paragraph = paragraph.split() # Split words
                for x in paragraph:
                    x = x.split('/') # divide
                    if '-' in x[0] and x[1] == 'm': # The beginning of a paragraph
                        if x[0] == end_paragraph: # End position
                            return
                    # Remove bracket []
                    if len(x[0]) > 0 and x[0][0] == '[':
                        x[0] = x[0][1:]
                    x[1] = x[1].split(']')[0]
                    # Find words in the tree
                    node = self._root
                    i = 0
                    while i < len(x[0]) and x[0][i] in node['next']:
                        node = node['child'][node['next'].index(x[0][i])] # Next Node
                        i += 1
                    # Add nodes
                    while i < len(x[0]):
                        node['next'].append(x[0][i])
                        node['child'].append({'word':x[0][i], 'next':[], 'child':[]})
                        node = node['child'][-1]
                        i += 1
                    # Mark
                    node['next'].append('')
                    node['child'].append(0)
    
    def seg(self, sentences):
        begin = near_end = end = 0
        result = list()
        while begin < len(sentences):
            end = begin
            near_end = end
            node = self._root
            while end < len(sentences) and sentences[end] in node['next']:
                node = node['child'][node['next'].index(sentences[end])] # Next Node
                if '' in node['next']:
                    near_end = end
                end += 1
            if near_end == begin: # No words
                result.append(sentences[begin:begin+1])
                self._unreconized += 1
            else:
                result.append(sentences[begin:near_end+1])
            begin = near_end + 1
        return result
    
    def unreconized_words(self): # Return the number of unreconized words during running
        return self._unreconized

if __name__=='__main__':
    corpus = Corpus()
    # Train
    print('Training...', end='', flush=True)
    corpus.train()
    print('Ok.')
    # Segmentation
    print('Please input sentences for word segmentation.')
    while True:
        print('>> ', end='')
        print(corpus.seg(input()))