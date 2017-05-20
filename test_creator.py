import twitter_crawler, sys, io


twitter_list = twitter_crawler.crawler("realalexjones") + twitter_crawler.crawler("rogerjstonejr")
counter = 0
for i in twitter_list:
    question = input(i + ": ")
    if question == 'y':
        file = io.open('test/{}/{}.txt'.format(question, counter), 'w', encoding='utf8')
    else:
        file = io.open('test/{}/{}.txt'.format('n', counter), 'w', encoding='utf8')
    try:
        file.write("{}".format(i))
    except UnicodeEncodeError:
        file.write("{}".format(i))
    counter += 1
    file.close()