import re

import tweepy

# Tweepy configuration details
consumer_key = 'wPZXlCsAfESR3MIoAxNXed8vV'
consumer_secret = '4cInX9P4YASfCrZ7XFCXzdT2gPTUJSI2XXjqP0oCaPQgNxkoPR'
access_token = '847075059382464512-04gtpjfXxxTSfGVAIOjjUGhXhbuCpI7'
access_token_secret = 'WM27Xys78EIvEGsX1gJjJ42iqfVyAwm0udhgjP2hpJqbe'
authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_token_secret)
api = tweepy.API(authentication)


# Twitter crawler code
# TODO: Exception for invalid ID/handle
def crawler(twitter_input):
    try:
        try:
            return re.sub(r"http\S+", "", api.get_status(twitter_input).retweeted_text), twitter_input
        except AttributeError:
            return re.sub(r"http\S+", "", api.get_status(twitter_input).text), twitter_input
    except:
        return_list = []
        return_id_list = []
        for i in api.user_timeline(twitter_input, count=20):
            try:
                return_list.append(re.sub(r"http\S+", "", i.retweeted_text))
            except AttributeError:
                return_list.append(re.sub(r"http\S+", "", i.text))
            return_id_list.append(i.id_str)
        return return_list, return_id_list
