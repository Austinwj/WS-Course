from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

CONSUMER_KEY = "I5bn8DLzOlBi9zzsirvB2HFos"
CONSUMER_SECRET = "bgZXyN7u8j3yNICGkfA1ZzgMDGqKaC5I53bGSmIjgepJx5qFOH"
ACCESS_TOKEN = "1230152400197083137-Rmrn97XY3EFMuFP9bbBMFH3hQ7llNI"
ACCESS_TOKEN_SECRET = "SQu1SAfBMzj0OXZdwsLiu3V1hNnsxy5brsa8Ku4tiLZl0"

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


class MyStreamListener(StreamListener):

    def __init__(self, data_name, ):
        self.fetched_tweets_filename = data_name

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: s" % str(e))
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    hashtag = ['today']
    fetched_tweets_filename = "today.csv"

    twitter_streamer = MyStreamListener(fetched_tweets_filename)
    stream = Stream(auth, twitter_streamer)
    stream.filter(track=hashtag)
