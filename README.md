# NLP Homework

![Size](https://github-size-badge.herokuapp.com/jerrymakesjelly/nlp-homework.svg)

This is a backup of my Natural Language Processing(NLP) homework. Thanks to my teacher Caixia YUAN.

There are 12 problems in this course, but you can pass it by getting 60 points. So I just choose some of these problems.

All the problems are saved in the directory *Docs*.

## Learning Material
### Homework 1-3
Download it from [Google Drive/1998-01-105-带音.txt](https://drive.google.com/open?id=1sFXiLMyOAyn0Sinaw1XSSZHs-ZspXMBT), and save it to the folder *Problem1-3*.

### Homework 5
Download the [20_newsgroups.tar.gz](http://www.cs.cmu.edu/afs/cs/project/theo-11/www/naive-bayes/20_newsgroups.tar.gz) from cs.cmu.edu, and untar all the files to the folder *Problem5/20_newsgroups/20_newsgroups*.

## Contents
### Homework 1: Chinese word segmentation
#### Problem
- This task provides PKU data as training set and test set (e.g., you can use 80% data for model training and other 20% for testing), and you are free to use data learned or model trained from any resources.
- Evaluation Metrics:
  * Precision = (Number of words correctly segmented) / (Number of words segmented) * 100%
  * Recall = (Number of words correctly segmented) / (Number of words in the reference) * 100%
  * F measure = 2\*P\*R / (P+R)

#### Solution
Maximum Matching. Build a tree to save words, each node is a single word, and the path from the root to the leaf node represents a word. Find a longest path when we are doing word segmentation.

#### Testing
Take the first 80%(from the beginning to *19980124-10-003-003*) of the material as the training set, and take the remaining 20%(from *19980124-10-003-003* to the end) as the testing set.

```
Precision: 0.9727381759867756
Recall: 1.0181580531106598
F measure: 0.9949300149090181

Segmented words: 222619
Correct words: 216550
Words in reference: 212688
```
The value of F measure is 99.4%.

#### Run
![Screenshot1](https://user-images.githubusercontent.com/6760674/38561790-8b633400-3d0b-11e8-8138-b8b8e75983cf.png)

### Homework 2: N-gram Language Models
#### Problem
- In this assignment you will explore a simple, typical N-gram language model.
- This model can be trained and tested on sentence-segmented data of a Chinese text corpus. “Word Perplexity” is the most widely-used evaluation metric for language models.
- Additional points: if you can test how does the different “Word Perplexity” of the different “N” grams, you will get additional 10 points.
- Additional points: if you can test how does the different “Word Perplexity” of the different smoothing methods, you will get additional 10 points.

#### Solution
* Calculate an N-gram probability matrix. Use Python **dict** to store the non-zero values in the matrix, and calculate the zero values when we're using them.

* - Unigram: The probability of each word doesn't depend on any history words. Hence

    ![Formula1](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20p%28w_1%2Cw_2%2C...%2Cw_n%29%3Dp%28w_1%29p%28w_2%29...p%28w_n%29)

    Use Laplace Smoothing(Add-one) for estimation:

    ![Formula2](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20p_%7BLaplace%7D%28w_i%29%3D%5Cfrac%7Bc_i%2B1%7D%7BN%2B%7CV%7C%7D)
  
    ![Formula3](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20%7CV%7C) is the size of the word table.

  - Bigrams: The probability of each word depends on the previous history word.

    ![Formula4](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20p%28w_1%2Cw_2%2C...%2Cw_n%29%3Dp%28w_1%29p%28w_2%7Cw_1%29...p%28w_n%7Cw_%7Bn-1%7D%29)

    Use Laplace Smoothing(Add-one) for estimation:

    ![Formula5](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20p_%7BLaplace%7D%28w_i%29%3D%5Cfrac%7Bc%28w_%7Bi-1%7D%2Cw_i%29%2B1%7D%7Bc%28w_%7Bi-1%7D%29%2B%7CV%7C%7D)

  - Trigrams: The probability of each word depends on the two previous history words.

    ![Formula6](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20p%28w_1%2Cw_2%2Cw_3%2C...%2Cw_n%29%3Dp%28w_1%29p%28w_2%7Cw_1%29p%28w_3%7Cw_1%2Cw_2%29...p%28w_n%7Cw_%7Bn-1%7D%2Cw_%7Bn-2%7D%29)

    Use Laplace Smoothing(Add-one) for estimation:

    ![Formula7](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20p_%7BLaplace%7D%28w_i%29%3D%5Cfrac%7Bc%28w_%7Bi-2%7D%2Cw_%7Bi-1%7D%2Cw_i%29%2B1%7D%7Bc%28w_%7Bi-1%7D%2Cw_%7Bi-2%7D%29%2B%7CV%7C%7D)

* Perplexity: To evaluate the quality of the model. The smaller value of *PP(W)* means better.

  ![Formula8](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20PP%28W%29%3DP%28W%29%5E%7B-%5Cfrac%7B1%7D%7BN%7D%7D%3D%5B%5Cprod_%7Bi%3D1%7D%5E%7BN%7DP%28w_i%7Cw_%7Bi-n%7D%2C...%2Cw_%7Bi-1%7D%29%5D%5E%7B-%5Cfrac%7B1%7D%7BN%7D%7D)

#### Testing
Take the first 80%(from beginning to *1998-0124-09-005-001*) of the material as the training set, and take the remaining as the testing set.
```
Perplexity of unigram: 2429.6557199908398
Perplexity of bigram: 8248.407064192068
Perplexity of trigram: 21542.494217118983
```
In general, the perplexity decreases as N increases. So there may be something wrong in the code.

#### Run
![Screenshot2](https://user-images.githubusercontent.com/6760674/38561791-8c25b494-3d0b-11e8-8b30-c2238553c063.png)

### Homework 3: Part-of-speech tagging
#### Problem
- This data set contains one month of Chinese daily which are segmented and POS tagged under Peking Univ. standard.
- Project ideas:
  * Design a sequence learning method to predicate a POS tags for each word in sentences.
  * Use 80% data for model training and other 20% for testing (or 5-fold cross validation to test learner’s performance. So it could be interesting to separate dataset.)

#### Solution: The Viterbi Algorithm

Create a *(N+2)\*T* matrix, and fill the element *[j,t]* with ![Formula9](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20v_t%28j%29%3D%5Cmax%20%5Climits_%7B1%5Cleq%20i%5Cleq%20N%7D%20%7Bv_%7Bt-1%7D%28i%29a_%7Bij%7Db_j%28o_t%29%20).

* Initialization:

  ![Formula10](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20v_1%28j%29%3Da_0b_j%28o_1%29%2C%201%5Cleq%20j%5Cleq%20N)

  ![Formula11](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20bt_1%28j%29%3D0)

* Recursive:

  ![Formula12](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20v_t%28j%29%3D%5Cmax%20%5Climits_%7B1%5Cleq%20i%5Cleq%20N%7D%20%7Bv_%7Bt-1%7D%28i%29a_%7Bij%7Db_j%28o_t%29%2C%201%5Cleq%20j%5Cleq%20N%2C%201%5Cleq%20t%5Cleq%20T)

  ![Formula13](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20bt_t%28j%29%3D%5Carg%20%5Cmax%20%5Climits_%7B1%5Cleq%20i%5Cleq%20N%7Dv_%7Bt-1%7D%28i%29a_%7Bij%7Db_j%28o_t%29%2C%201%5Cleq%20j%5Cleq%20N%2C%201%5Cleq%20t%5Cleq%20T)

* Final:

  - The probability of the best path: ![Formula14](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20P%5E*%3Dv_t%28q_F%29%3D%5Cmax%20%5Climits_%7B1%5Cleq%20i%5Cleq%20N%7Dv_T%28i%29a_%7BiF%7D).

  - The starting state of the backtrace: ![Formula15](http://chart.googleapis.com/chart?cht=tx&chl=\Large%20%7Bq_T%7D%5E*%3Dbt_T%28q_F%29%3D%5Carg%20%5Cmax%20%5Climits_%7B1%5Cleq%20i%5Cleq%20N%7Dv_T%28i%29a_%7BiF%7D).

![Picture1](https://user-images.githubusercontent.com/6760674/38555726-cbbab08a-3cf9-11e8-99bd-645ad19b5bd8.png)

#### Testing
Take the 100% of the material as the training set, and take the first 2.5% of the material as the testing set(In order to evaluate the quality of the algorithm).
```
Correct: 19331
Wrong: 647
Rate: 0.9676143758133947
```
It's not bad.

#### Run
![Screenshot3](https://user-images.githubusercontent.com/6760674/38561793-8c77f722-3d0b-11e8-9ec3-4efa111e6345.png)

### Homework 5: Text classification
#### Problem
- This data set contains 1000 text articles posted to each of 20 online newsgroups, for a total of 20,000 articles. For documentation and download, see http://www-2.cs.cmu.edu/afs/cs/project/theo-11/www/naive-bayes.html
- The “label” of each article is which of the 20 newsgroups it belongs to. The newsgroups (labels) are hierarchically organized (e.g., “sports”, “hockey”).
- You should provide model evaluation results and discuss the reasons of the results.

#### Solution: Naive Bayes
Of course there are many ways to solve this problem. I think the Naive Bayes is the simplest way.

Calculate the probability that text *xi* belongs to the each category *ck*, and return the corresponding category with the highest probability.

![Formula15](https://chart.googleapis.com/chart?cht=tx&chl=\Large%20%5Chat%7Bc%7D%3D%5Carg%20%5Cmax%20%5Climits_%7B1%5Cleq%20k%5Cleq%20K%7D%5Chat%7BP%7D%28c_k%7Cx_i%29)

![Formula16](https://chart.googleapis.com/chart?cht=tx&chl=\Large%20%3D%5Carg%20%5Cmax%20%5Climits_%7B1%5Cleq%20k%5Cleq%20K%7D%5Cfrac%7BP%28c_k%29P%28x_i%7Cc_k%29%7D%7BP%28x_i%29%7D)

![Formula17](https://chart.googleapis.com/chart?cht=tx&chl=\Large%20%3D%5Carg%20%5Cmax%20%5Climits_%7B1%5Cleq%20k%5Cleq%20K%7DP%28c_k%29P%28x_i%7Cc_k%29)

![Formula18](https://chart.googleapis.com/chart?cht=tx&chl=\Large%20%3D%5Carg%20%5Cmax%20%5Climits_%7B1%5Cleq%20k%5Cleq%20K%7D%28%5Clog%20P%28c_k%29%2B%5Clog%20P%28x_i%7Cc_k%29%29)

#### Testing
Take all the mails as a training set, and randomly select 100 mails from it to form a testing set.
```
Rate: 0.97
```

#### Run
![Screenshot5](https://user-images.githubusercontent.com/6760674/38561794-8caf875a-3d0b-11e8-81ee-e56ed2ee2c38.png)