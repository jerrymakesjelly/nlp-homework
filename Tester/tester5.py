#-*- coding:utf-8 -*-

# Please copy myself to the folder `Problem5`

from problem5 import TextClassifier

class Tester(object):
    def __init__(self, path, count):
        self._path = path
        self._count = count
        self._test_list = list()
        self._answer = list()
        self._tc = TextClassifier()
        self._tc.train()
        print('Text classifier is well trained.')
    
    def random_choose(self):
        classes = os.listdir(self._path)
        count = self._count
        while count > 0:
            clas = classes[random.randint(0, len(classes)-1)]
            subpath = os.path.join(self._path, clas)
            files = os.listdir(subpath)
            self._test_list.append(os.path.join(subpath, files[random.randint(0, len(files)-1)]))
            self._answer.append(clas)
            print('Add: '+self._test_list[-1])
            count -= 1
    
    def start(self):
        count = self._count-1
        correct = 0
        wrong = 0
        while count >= 0:
            result = self._tc.classify(self._test_list[count])
            if self._answer[count] == result:
                print("Accepted: "+self._test_list[count]+" -> "+result)
                correct += 1
            else:
                print("Rejected: "+self._test_list[count]+" -> "+result)
                wrong += 1
            count -= 1
        print("Rate: "+str(correct/(correct+wrong)))

if __name__ == '__main__':
    t = Tester('./20_newsgroups/20_newsgroups', 100)
    t.random_choose()
    t.start()