import json
import tweepy
import urllib.parse
import pandas as pd
import time
import re
from datetime import date
from textblob import TextBlob

import os
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from flask import escape


class StreamListener(tweepy.StreamListener):
    """Listen for tweets

    """
    def __init__(self, api=None, file_name='tweets.txt', mode='a', req_loc=False, max_tweets=100):
        super(StreamListener, self).__init__()
        self.num_tweets = 0
        self.file = open(file_name, mode)
        self.max_tweets = max_tweets
        self.req_loc = req_loc

    def get_tweets(self):
        """Get tweets after HTTP Cloud Function

        """
        keyword = 'covid'

        # Load tokens from file
        with open('../data/tokens.json', 'r') as f:
            tokens = json.load(f)

        # Stream tweets
        auth = tweepy.OAuthHandler(tokens['consumer_key'], tokens['consumer_secret'])
        auth.set_access_token(tokens['access_token_key'], tokens['access_token_secret'])
        api = tweepy.API(auth)

        # listen for tweets
        while True:

            # TODO: save file in Cloud Storage
            file_name = date.today().strftime('corpus-%d-%m-%Y.json')
            print(f'Updating {file_name} ...')

            StreamListener = StreamListener(
                file_name=file_name, 
                max_tweets=1000)
            myStream = tweepy.Stream(
                auth=api.auth, 
                listener=StreamListener)

            myStream.filter(track=[keyword], languages=['en'])
            
            time.sleep(60)

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            time.sleep(15 * 60)
            return False
        
    def on_status(self, tweet):
        if hasattr(tweet, "extended_tweet") and (tweet.geo or ~self.req_loc):
            
            entry = {
                'id': tweet.id,
                'user': tweet.user.screen_name,
                'text': tweet.extended_tweet['full_text'],
                'geo': tweet.geo,
                'location': tweet.user.location,
                'timestamp': tweet.timestamp_ms 
            }

            self.file.write( json.dumps(entry) + '\n' )
            self.num_tweets += 1

            if self.num_tweets <= self.max_tweets:
                return True
            else:
                return False
            self.file.close()


class TweetPreprocessor(object):
    """Preprocess tweets for downstream analysis

    """
    def __init__(self, tweets):
        super(TweetPrep rocessor, self).__init__()
        filename = '../data/corpus-06-05-2020.json'
        self.tweets = pd.read_json(filename, lines=True)
        
    def get_emojis(self):
        """return emojis from tweets"""
        return self.tweets.str.findall(r':{1}[\d\w\-]+:{1}')

    def clean_tweets(self):
        """clean tweets"""
        cleaned = (self.tweets
                   .replace(' ?https.* ?', '', regex=True) # remove hyperlink
                   .replace(' ?@\w+ ?', '', regex=True) # remove mentions
                   .replace(' ?#\w+ ?', '', regex=True) # remove hashtags
                   .replace(' ?\$\d* ?', '', regex=True) # remove dollar amounts
                   .replace(' ?\xa0 ?', ' ', regex=True) # remove non-breaking space
                   .replace(' ?&amp ?', '', regex=True) # remove &amp
                   .replace(' ?\n ?', '', regex=True) # remove new line
                   .str.lower() # lower case
                   .transform(lambda x: emoji.demojize(x))) # demojize# remove new line

        self.tweets = cleaned

    def feat_eng(self, tweets):
        """Get emojis, word counts and text polarity"""
        self.tweets['emojis'] = get_emojis(self.tweets['text']) # get emojis as text
        self.tweets['polarity'] = self.tweets['text'].map(
            lambda x: TextBlob(x).sentiment.polarity)
        self.tweets['word_count'] = self.tweets['text'].map(lambda x: len(str(x).split()))


class TweetAnalyzer(object):
    """Tweet Analyzer

    """
    def __init__(self, arg):
        super(TweetAnalyzer, self).__init__()
        self.arg = arg

    def high_pol_tweets(self):
        """Check tweets with highest sentiment polarity score (i.e. polarity=1)"""
        positive = sdf.loc[sdf.polarity == sdf.polarity.max(), ['text']].sample(5).values
        [print(text[0], '\n') for text in positive]; 

    def neut_pol_tweets(self):
        """check tweets with neutral sentiment polarity score (0)"""
        positive = sdf.loc[sdf.polarity == 0, ['text']].sample(5).values
        [print(text[0], '\n') for text in positive];

    def low_po_tweets(self):
        # check tweets with neutral sentiment polarity score (0)
        positive = sdf.loc[sdf.polarity == sdf.polarity.min(), ['text']].sample(5).values
        [print(text[0], '\n') for text in positive];

    def make_word_cloud(self):
        """Generate word cloud"""
        # Generate text
        text= ""
        for key,value in df.iterrows():
            text += value.text
        
        # Generate word cloud
        wordcloud = WordCloud(max_font_size=40, collocations=False).generate(text)
        # plt.figure(figsize=(15,15))
        # plt.imshow(wordcloud, interpolation="bilinear")
        # plt.axis("off")
        # plt.show()
        return wordcloud 
        


