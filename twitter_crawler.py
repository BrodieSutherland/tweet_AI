import tweepy, re

# Tweepy configuration details
consumer_key = 'wPZXlCsAfESR3MIoAxNXed8vV'
consumer_secret = '4cInX9P4YASfCrZ7XFCXzdT2gPTUJSI2XXjqP0oCaPQgNxkoPR'
access_token = '847075059382464512-04gtpjfXxxTSfGVAIOjjUGhXhbuCpI7'
access_token_secret = 'WM27Xys78EIvEGsX1gJjJ42iqfVyAwm0udhgjP2hpJqbe'
authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_token_secret)
api = tweepy.API(authentication)


# Twitter crawler code
# TODO: Handle Emojis in Twitter Crawler
def crawler(twitter_input):
    try:
        try:
            return re.sub(r"http\S+", "", api.get_status(twitter_input).retweeted_text)
        except:
            return re.sub(r"http\S+", "", api.get_status(twitter_input).text)
    except:
        returnList = []
        for i in api.user_timeline(twitter_input, count=10):
            try:
                returnList.append(re.sub(r"http\S+", "", i.retweeted_text))
            except:
                returnList.append(re.sub(r"http\S+", "", i.text))
        return returnList
