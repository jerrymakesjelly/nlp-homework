#-*- coding:utf-8 -*-

# Please copy myself to the folder `Problem1-3`

import problem3

class Tester(object):
    def __init__(self, start_segment, end_segment=''):
        self._viterbi = Viterbi()
        self._viterbi.train()
        print('The Viterbi Algorithm is trained.')
        self._filename = '1998-01-105-带音.txt'
        self._word_set = list()
        self._answer_set = list()
        self._load_testset(start_segment, end_segment)
        print('The test data is ready. '+str(len(self._word_set))+' line(s).')
    
    def _load_testset(self, start_segment, end_segment):
        start = False
        # Read the file
        with open(self._filename) as f:
            paragraphs = f.readlines()
            for paragraph in paragraphs:
                one_word_set = list()
                one_answer_set = list()
                paragraph = paragraph.split() # Split words
                for x in paragraph:
                    x = x.split('/') # Split
                    if '-' in x[0] and x[1] == 'm': # The beginning of a paragraph
                        if x[0] == start_segment: # Reach end position
                            start=True
                        if x[0] == end_segment:
                            start=False
                        continue
                    if not start:
                        break # Go to the next paragraph
                    # Remove brackets
                    if len(x[0]) > 0 and x[0][0] == '[': # Left bracket
                        x[0] = x[0][1:]
                    x[1] = x[1].split(']')[0] # Right bracket
                    one_word_set.append(x[0])
                    one_answer_set.append(x[1])
                if len(one_word_set) > 0:
                    self._word_set.append(one_word_set)
                    self._answer_set.append(one_answer_set)

    def test(self):
        correct = 0
        wrong = 0
        for i in range(len(self._word_set)):
            result = self._viterbi.viterbi(self._word_set[i])
            if 'START' in self._word_set[i]:
                self._word_set[i].remove('START')
            # Check the answer
            for j in range(len(result)):
                if result[j] == self._answer_set[i][j]:
                    correct += 1
                else:
                    print('Wrong Answer: '+self._word_set[i][j]+': '+result[j]+'->'+self._answer_set[i][j])
                    wrong += 1
        print('Correct: '+str(correct))
        print('Wrong: '+str(wrong))
        print('Rate: '+str(correct/(correct+wrong)))

if __name__ == '__main__':
    Tester('19980101-01-001-001', '19980102-01-005-001').test()