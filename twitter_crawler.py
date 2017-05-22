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

def crawler(twitter_input):
    """
    This takes a string as input from main.py, and uses the Twitter API to find either a tweet ID with the string as an
    ID, or a handle matching the string. Then, depending on whether it is a single status or a list, it will return a
    tuple containing either a list or a string in the first position and the ID(s) as a string or list in second
    position.
    
    Keyword Arguments:
        twitter_input -- String, parsed in from the main function in main.py. Used to search Twitter for both statuses
        and handles matching twitter_input.
    
    Return:
        Return value changes depending on whether a status or handle was found, or an error occurred
        Upon finding a status, the string of the tweet is returned within a list alongside the tweet's ID (also in a
        list). When a handle is found, a string of the 10 latest tweets by that person is returned alongside as list
        of the IDs of these tweets
    """
    try:
        try:
            try:
                return [re.sub(r"http\S+", "", api.get_status(twitter_input).retweeted_text)], [twitter_input]
            except AttributeError:
                return [re.sub(r"http\S+", "", api.get_status(twitter_input).text)], [twitter_input]
        except:
            return_list = []
            return_id_list = []
            for i in api.user_timeline(twitter_input, count=10):
                try:
                    return_list.append(re.sub(r"http\S+", "", i.retweeted_text))
                except AttributeError:
                    return_list.append(re.sub(r"http\S+", "", i.text))
                return_id_list.append(i.id_str)
            return return_list, return_id_list
    except tweepy.error.TweepError:
        print("Sorry, that doesn't exist. Please try again.")
        return tweepy.error.TweepError
