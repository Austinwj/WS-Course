import re

from preprocessData import processData

import nltk
import numpy as np
import pandas as pd

raw_data = pd.read_csv('today.csv', header=None, usecols=[0,3,11,12,13,14,15,16,17,18,19])
raw_data = raw_data.dropna().reset_index(drop=True)
for i in range(len(raw_data)):
    raw_data.iloc[i,0] = raw_data.iloc[i,0][15:-1]
    raw_data.iloc[i,1] = raw_data.iloc[i,1][6:]
    flag = 1
    for j in range(2,11):
        if raw_data.iloc[i,j].find('user:{"id":')!=-1:
            raw_data.iloc[i,2] = raw_data.iloc[i,j][11:]
            flag=0
            break
    if flag:
        print("User ID Not Found at Row",i)
raw_data = raw_data.iloc[:,0:3]
raw_data.columns = ["created_at","text","user_id"]
raw_data.to_csv('raw_data_created_at_text_user_id.csv')

raw_data = pd.read_csv('today.csv', header=None, usecols=[3])

excitement_lex = pd.read_csv('SixLexicons//excitementLex.csv', header=None, usecols=[0])
happy_lex = pd.read_csv('SixLexicons//happyLex.csv', header=None, usecols=[0])
pleasant_lex = pd.read_csv('SixLexicons//pleasantLex.csv', header=None, usecols=[0])
surprise_lex = pd.read_csv('SixLexicons//surpriseLex.csv', header=None, usecols=[0])
fear_lex = pd.read_csv('SixLexicons//fearLex.csv', header=None, usecols=[0])
angry_lex = pd.read_csv('SixLexicons//angryLex.csv', header=None, usecols=[0])

excitement_lex = np.array(excitement_lex)
happy_lex = np.array(happy_lex)
pleasant_lex = np.array(pleasant_lex)
surprise_lex = np.array(surprise_lex)
fear_lex = np.array(fear_lex)
angry_lex = np.array(angry_lex)

excitement_lex.flatten()
happy_lex.flatten()
pleasant_lex.flatten()
surprise_lex.flatten()
fear_lex.flatten()
angry_lex.flatten()

# pre-processing data
nltk.download("stopwords")
processed = raw_data.applymap(processData)

excitement_list = []
happy_list = []
pleasant_list = []
surprise_list = []
fear_list = []
angry_list = []


class Classifier:
    def __init__(self):
        self.excitement_count = 0
        self.happy_count = 0
        self.pleasant_count = 0
        self.surprise_count = 0
        self.fear_count = 0
        self.angry_count = 0

    # There are three methods to detect
    # Search lexicons
    def SearchLex(self, tweet):

        if type(tweet) == list:
            for i in range(len(tweet)):
                if tweet[i] in excitement_lex:
                    self.excitement_count += 1
                if tweet[i] in happy_lex:
                    self.happy_count += 1
                if tweet[i] in pleasant_lex:
                    self.pleasant_count += 1
                if tweet[i] in surprise_lex:
                    self.surprise_count += 1
                if tweet[i] in fear_lex:
                    self.fear_count += 1
                if tweet[i] in angry_lex:
                    self.angry_count += 1

    # Search hashtag
    def SearchHashtag(self, tweet):
        try:
            if re.search(' #exciting', tweet) is not None:
                self.excitement_count += 2
            if re.search(' #happy', tweet) is not None:
                self.happy_count += 2
            if re.search(' #enjoy', tweet) is not None:
                self.pleasant_count += 2
            if re.search(' #surprise', tweet) is not None:
                self.surprise_count += 2
            if re.search(' #fear', tweet) is not None:
                self.fear_count += 2
            if re.search(' #angry', tweet) is not None:
                self.angry_count += 2
        except:
            pass

    # Search emoticons
    # For more detailed information about emojis, refer to: https://cn.piliapp.com/twitter-symbols/
    def SearchEmoticons(self, tweet):
        emoticons = [('excitement', ['🤩', '😝', '😆', '😍', ]),
                     ('happy', ['😀', '😜', '🤓', '😁', '🙂', ]),
                     ('pleasant', ['😌', '😊', '☺']),
                     ('surprise', ['😯', '😱', '🙀']),
                     ('fear', ['😨', '😣', '😫', '😰']),
                     ('angry', ['😠', '🤬', '😾', '👿']),
                     ]
        for (s, emojis) in emoticons:
            for emoji in emojis:
                try:
                    if re.search(emoji, tweet) is not None:
                        self.excitement_count += 1
                    if re.search(emoji, tweet) is not None:
                        self.happy_count += 1
                    if re.search(emoji, tweet) is not None:
                        self.pleasant_count += 1
                    if re.search(emoji, tweet) is not None:
                        self.surprise_count += 1
                    if re.search(emoji, tweet) is not None:
                        self.fear_count += 1
                    if re.search(emoji, tweet) is not None:
                        self.angry_count += 1
                except:
                    pass

    # restart counting
    def reCount(self):
        self.excitement_count = 0
        self.happy_count = 0
        self.pleasant_count = 0
        self.surprise_count = 0
        self.fear_count = 0
        self.angry_count = 0

    # counting sum to compare
    def judge(self, tweet):

        self.SearchLex(tweet)
        self.SearchHashtag(tweet)
        self.SearchEmoticons(tweet)
        max_sentiment = max(self.excitement_count, self.happy_count, self.pleasant_count, self.surprise_count,
                            self.fear_count,
                            self.angry_count)
        if max_sentiment == self.excitement_count and self.excitement_count > 0:
            excitement_list.append(tweet)
            self.reCount()
        elif max_sentiment == self.happy_count and self.happy_count > 0:
            happy_list.append(tweet)
            self.reCount()
        elif max_sentiment == self.pleasant_count and self.pleasant_count > 0:
            pleasant_list.append(tweet)
            self.reCount()
        elif max_sentiment == self.surprise_count and self.surprise_count > 0:
            surprise_list.append(tweet)
            self.reCount()
        elif max_sentiment == self.fear_count and self.fear_count > 0:
            fear_list.append(tweet)
            self.reCount()
        elif max_sentiment == self.angry_count and self.angry_count > 0:
            angry_list.append(tweet)
            self.reCount()
        else:
            pass


classifier = Classifier()
processed.applymap(classifier.judge)


def outputCsv(sentiment_list, path):
    print("Outputting data in CSV file format")
    print("Length of the list is", len(sentiment_list))
    sentiment_list = pd.DataFrame(columns=None, data=sentiment_list)
    sentiment_list.to_csv(path, header=None, encoding='gbk')

def outputJson(sentiment_list, path):
    print("Outputting data in JSON file format")
    print("Length of the list is", len(sentiment_list))
    sentiment_list = pd.DataFrame(columns=None, data=sentiment_list)
    sentiment_list.to_json(path, header=None, encoding='gbk')

outputCsv(excitement_list, 'data//excitement.csv')
outputCsv(happy_list, 'data//happy.csv')
outputCsv(pleasant_list, 'data//pleasant.csv')
outputCsv(surprise_list, 'data//surprise.csv')
outputCsv(fear_list, 'data//fear.csv')
outputCsv(angry_list, 'data//angry.csv')

outputJson(excitement_list, 'data//excitement.json')
outputJson(happy_list, 'data//happy.json')
outputJson(pleasant_list, 'data//pleasant.json')
outputJson(surprise_list, 'data//surprise.json')
outputJson(fear_list, 'data//fear.json')
outputJson(angry_list, 'data//angry.json')