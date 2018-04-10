#!/usr/env python3
#-*- coding:utf-8 -*-

# Please copy myself to the folder `Problem1-3`

import problem1


class Tester(object):
    def __init__(self, begin_position, end_position=''):
        self._filename = '1998-01-105-带音.txt'
        self._sentences = list()
        self._reference_segment = list()
        self._result_segment = list()

        self._load(begin_position, end_position)
        print('The test text is ready.')
        self._corpus = Corpus()
        self._corpus.train()
        print('The corpus is ready.')
    
    def _load(self, begin_position, end_position):
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
                        if enable: # New line
                            self._sentences.append('')
                    else:
                        if enable: # Words we should load
                            # Remove bracket []
                            if len(x[0]) > 0 and x[0][0] == '[':
                                x[0] = x[0][1:]
                                x[1] = x[1].split(']')[0]
                            self._sentences[-1] += x[0]
                            self._reference_segment.append(x[0])

    def test_segmentation(self, p=True):
        for sentence in self._sentences:
            self._result_segment.append(self._corpus.seg(sentence))
            # Print the result
            if p:
                for word in self._result_segment[-1]:
                    print(word+'/', end='')
                print('')
    
    def analysis(self):
        correct = 0
        segmented_words = 0
        # Count correct words
        for segment in self._result_segment:
            for word in segment:
                if word in self._reference_segment:
                    correct += 1
                segmented_words += 1
        # calculate
        precision = float(correct) / segmented_words
        recall = float(correct) / len(self._reference_segment)
        f_measure = 2 * precision * recall / (precision + recall)

        return {
            'Precision': precision, 'Recall': recall, 'F measure': f_measure,
            'Correct words': correct, 'Total words': segmented_words,
            'Words in reference': len(self._reference_segment),
            'Unreconized words': self._corpus.unreconized_words()
        }
    
if __name__ == '__main__':
    #t = Tester('19980124-10-003-003')
    t = Tester('19980131-04-013-001')
    t.test_segmentation(True)  
    analy = t.analysis()
    for x in analy:
        print(x+":", analy[x])