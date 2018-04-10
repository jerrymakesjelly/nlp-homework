# -*- coding:utf-8 -*-

class Viterbi(object):
    def __init__(self):
        self._filename = '1998-01-105-带音.txt'
        # the part of speech. P(After|Before)
        self._pos_relations = dict()
        # the part of speech of each word. P(Word|Part of Speech)
        self._pos_total = dict()
        self._pos_of_word = dict()
        # the sequence of part of speech
        self._pos_vector = list()
        # the number of states
        self._N = 0
    
    def train(self, end_segmentation=''):
        # Read the file
        with open(self._filename) as f:
            paragraphs = f.readlines()
            for paragraph in paragraphs:
                paragraph = paragraph.split() # Split words
                paragraph.append('END/END')
                prev = 'START'
                for x in paragraph:
                    x = x.split('/') # Split
                    if '-' in x[0] and x[1] == 'm': # The beginning of a paragraph
                        if x[0] == end_segmentation: # Reach end position
                            return
                        continue
                    # Remove brackets
                    if len(x[0]) > 0 and x[0][0] == '[': # Left bracket
                        x[0] = x[0][1:]
                    x[1] = x[1].split(']')[0] # Right bracket
                    # Statistics 1
                    if prev in self._pos_relations:
                        if x[1] in self._pos_relations[prev]:
                            self._pos_relations[prev][x[1]] += 1
                        else:
                            self._pos_relations[prev][x[1]] = 1
                    else:
                        self._pos_relations[prev] = dict()
                        self._pos_relations[prev][x[1]] = 1
                    # Statistics 2
                    if x[1] in self._pos_total:
                        self._pos_total[x[1]] += 1
                    else:
                        self._pos_total[x[1]] = 1
                    # Statistics 3
                    if x[1] in self._pos_of_word:
                        if x[0] in self._pos_of_word[x[1]]:
                            self._pos_of_word[x[1]][x[0]] += 1
                        else:
                            self._pos_of_word[x[1]][x[0]] = 1
                    else:
                        self._pos_of_word[x[1]] = dict()
                        self._pos_of_word[x[1]][x[0]] = 1
                    prev = x[1]
        # Compute 1
        for p in self._pos_relations:
            sum = 0
            for (o, w) in self._pos_relations[p].items():
                sum += w#self._pos_relations[p][o]
            for o in self._pos_relations[p]:
                self._pos_relations[p][o] /= 0.05*sum
        # Compute 2
        for p in self._pos_of_word:
            for o in self._pos_of_word[p]:
                self._pos_of_word[p][o] /= 0.05*self._pos_total[p]
        # Generate sequence of Part of Speech
        self._pos_vector = [p for p in self._pos_total]
        self._pos_vector.insert(0, 'START')
        self._pos_vector.remove('END')
        # Calculate N
        self._N = len(self._pos_total)
        self._pos_vector.append('END')
        #print('Training Completed.')

    def _a(self, before, after):
        if self._pos_vector[after] in self._pos_relations[self._pos_vector[before]]:
            return self._pos_relations[self._pos_vector[before]][self._pos_vector[after]]
        else:
            return 0
    
    def _b(self, state, word):
        if word in self._pos_of_word[self._pos_vector[state]]:
            return self._pos_of_word[self._pos_vector[state]][word]
        else:
            return 0
    
    def _max(self, li):
        max = li[0]
        for x in li:
            if x > max:
                max = x
        return max

    def _argmax(self, li):
        maxarg = 0
        for i in range(len(li)):
            if li[i] > li[maxarg]:
                maxarg = i
        return maxarg

    def viterbi(self, sentence):
        # The sentence should start with START
        sentence.insert(0, 'START')
        T = len(sentence)-1

        # Create a path probability matrix[N+2, T]
        vit = [[0 for i in range(T+1)] for j in range(self._N+2)]
        backpointer = [[0 for i in range(T+1)] for j in range(self._N+2)]

        for state in range(1, self._N):
            vit[state][1] = self._a(0, state) * self._b(state, sentence[1])
            backpointer[state][1] = 0
        for t in range(2, T+1):
            for state in range(1, self._N):
                vit[state][t] = self._max([vit[s][t-1]*self._a(s, state)*self._b(state, sentence[t]) for s in range(1, self._N)])
                backpointer[state][t] = self._argmax([vit[s][t-1]*self._a(s, state) for s in range(1, self._N)])+1
        # The state N+1 is END
        vit[self._N+1][T] = self._max([vit[s][T]*self._a(s, self._N) for s in range(1, self._N)])
        backpointer[self._N+1][T] = self._argmax([vit[s][T]*self._a(s, self._N) for s in range(1, self._N)])+1
        return self._backtrace(backpointer)
        #print('Completed.')
    
    def _backtrace(self, backpointer):
        t = len(backpointer[0])-1
        result = list()
        state = backpointer[self._N+1][t]
        while t > 0:
            result.insert(0, self._pos_vector[state])
            state = backpointer[state][t]
            t = t-1
        return result


if __name__ == '__main__':
    vi = Viterbi()
    print('Training Viterbi...', end='', flush=True)
    vi.train()
    print("Ok.")
    print("Input the word sequence (NOT sentence) which is going to be analyzed.")
    while True:
        print('>> ', end='')
        sentence = input()
        print(vi.viterbi(sentence.split()))