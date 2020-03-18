import re
from string import punctuation

import nltk
from nltk.tokenize.casual import reduce_lengthening
from nltk import word_tokenize
import pattern
from pattern.text.en import suggest
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english') + list(punctuation))
wnl = nltk.WordNetLemmatizer()

def line_format(tweet):
    for i in range(len(tweet)):
        for data in tweet[i]:
            for regex in {"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                          "#[0-9a-zA-Z]+",
                          "@[0-9a-zA-Z]+"}:
                data = re.sub(regex, '', data)
            return data.strip()


def fixed_wrong_word(tweet):
    datas = []
    for i in range(len(tweet)):
        for word in tweet[i].split():
            if word.isalpha():
                try:
                    result = suggest(reduce_lengthening(word))
                    datas.append(result[0][0])
                    continue
                except Exception as e:
                    pass
            datas.append(word)
        return ' '.join(datas)


def processData(tweet):

    try:
        line_format(tweet)
        fixed_wrong_word(tweet)
        tweet = tweet.lower()
        # remove RT in the head
        tweet = tweet.replace('rt', '', 1)
        # remove 'text' on head
        tweet = tweet.replace('text', '', 1)
        # remove URLs
        tweet = re.sub(r"(http[s:…]*(//\S*)?)|(@\w+)", "", tweet)
        # remove usernames
        tweet = re.sub('@[^\s]+', '', tweet)
        # remove number
        tweet = re.sub(r'\d +', '', tweet)
        # change loooooove to love
        tweet = [wnl.lemmatize(word) for word in nltk.word_tokenize(tweet)]
        # remove punctuation
        tweet = [word for word in tweet if word not in stop_words and len(word) >= 3]
        return tweet
    except:
        return tweet