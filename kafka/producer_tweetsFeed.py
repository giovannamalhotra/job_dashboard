import sys
import tweepy
#from tweepy import Stream
#from tweepy import OAuthHandler
#from tweepy.streaming import StreamListener
import os
import json
from kafka import KafkaProducer

# Make sure these variables are exported in a bash file anywhere in the host where this program is run
ckey = os.environ['consumerkey']
csecret = os.environ['consumersecret']
atoken = os.environ['accesstoken']
asecret = os.environ['accesssecret']
kafka_node_dns = os.environ['kafka_node_dns']
topic = os.environ['twitter_topic']


producer = KafkaProducer(bootstrap_servers = kafka_node_dns + ':9092')

class TweetStreamProducer(tweepy.StreamListener):

    def on_data(self, data):
        # Send raw data to kafka
        producer.send(topic, str(data))
        json_data = json.loads(data)
        print str(json_data['id']), " sent"
        return True

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

def start():
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = tweepy.streaming.Stream(auth, TweetStreamProducer())

    # Filter to get English tweets only
    twitterStream.sample(languages=["en"])
    twitterStream.filter(track=["#tech"])

if __name__ == "__main__":
    start()
