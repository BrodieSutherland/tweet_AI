# -*- coding: UTF-8 -*-
import io
import re

import tweepy

"""
Quick Script I used to generate train data based on people followed. Might be a bad idea to have these codes up on 
GitHub but I don't care about my Twitter account.
"""

# Tweepy configuration details
consumer_key = 'wPZXlCsAfESR3MIoAxNXed8vV'
consumer_secret = '4cInX9P4YASfCrZ7XFCXzdT2gPTUJSI2XXjqP0oCaPQgNxkoPR'
access_token = '847075059382464512-04gtpjfXxxTSfGVAIOjjUGhXhbuCpI7'
access_token_secret = 'WM27Xys78EIvEGsX1gJjJ42iqfVyAwm0udhgjP2hpJqbe'
authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_token_secret)
api = tweepy.API(authentication)

# Tweepy pulling tweets to file for dataset
userlist = []
for i in api.friends_ids():
    for j in api.user_timeline(i, count=50):
        try:
            tweet_text = j.retweeted_text
        except AttributeError:
            tweet_text = j.text
        userlist.append(re.sub(r"http\S+", "", tweet_text))
counter = 0
for i in userlist:
    question = input(i + ": ")
    if question == 'y':
        file = io.open('{}/{}.txt'.format(question, counter), 'w', encoding='utf8')
    else:
        file = io.open('{}/{}.txt'.format('n', counter), 'w', encoding='utf8')
    try:
        file.write("{}".format(i))
    except UnicodeEncodeError:
        file.write("{}".format(i))
    counter += 1
    file.close()
