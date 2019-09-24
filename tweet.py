import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sqlite3
import time
from datetime import datetime
from unidecode import unidecode

analyzer = SentimentIntensityAnalyzer()

conn = sqlite3.connect('twitter.db')
c = conn.cursor()


def create_tweet_db():
    try:
        c.execute(""" CREATE TABLE IF NOT EXISTS sentiment(unix REAL, user_name TEXT,
        tweet TEXT, positive REAL, negative REAL, neutral REAL, compound REAL)""")
        c.execute("""CREATE INDEX fast_unix ON sentiment(unix)""")
        c.execute("""CREATE INDEX fast_tweet ON sentiment(user_name)""")
        c.execute("""CREATE INDEX fast_tweet ON sentiment(tweet)""")
        c.execute("""CREATE INDEX fast_sentiment ON sentiment(positive)""")
        c.execute("""CREATE INDEX fast_sentiment ON sentiment(negative)""")
        c.execute("""CREATE INDEX fast_sentiment ON sentiment(neutral)""")
        c.execute("""CREATE INDEX fast_sentiment ON sentiment(compound)""")
        conn.commit()
    except:
        pass


create_tweet_db()
# Authenticate to Twitter
auth = tweepy.OAuthHandler("2x1lZlbFVH5Ka6zjiKjVRfJOR", "yuqFCYOI97MfgcsNI1ncyW4fGm5MYF6iKnfcharR2gJHnitvwI")
auth.set_access_token("910701534685560832-o4cPFN0gbpcUOKu5x8TIZL1Uw05Ku0a",
                      "Qy6KD34v4VKdc543rr1ZGNKzjTuikpKef0APMIF0I5XIK")


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        super().__init__(api)
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        try:
            user_name = tweet.user.name
            tweet_ = unidecode(tweet.text)
            # time_now = datetime.now()
            time_ms = datetime.now()
            sentiment = analyzer.polarity_scores(tweet.text)
            positive = sentiment['pos']
            negative = sentiment['neg']
            neutral = sentiment['neu']
            compound = sentiment['compound']
            print(time_ms, user_name, tweet_, positive, negative, neutral, compound)
            c.execute("""INSERT INTO sentiment(unix, user_name, tweet, positive, negative, neutral, compound) VALUES 
            (?, ?, ?, ?, ?, ? , ?)""",
                      (time_ms, user_name, tweet_, positive, negative, neutral, compound))
            conn.commit()
        except KeyError as e:
            print(str(e))
        return True

    def on_error(self, status):
        print(status)


while True:
    api = tweepy.API(auth, wait_on_rate_limit=False,
                     wait_on_rate_limit_notify=False)
    try:
        tweets_listener = MyStreamListener(api)
        stream = tweepy.Stream(api.auth, tweets_listener)
        stream.filter(track=["a", "e", "i", "o", "u", "y"], languages=["en"])
    except Exception as e:
        print(str(e))
        time.sleep(1)
