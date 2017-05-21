from sklearn.externals import joblib

import classifier
import getopt
import glob
import information
import io
import numpy
import sys
import time
import twitter_crawler


def main(argv):
    #argv = ["main.py", "-h"]
    learn = minimal = False
    loadfile = createfile = ''
    try:
        opts, args = getopt.getopt(argv, "hmLc:l:", ["createfile=", "loadfile="])
    except getopt.GetoptError:
        print("\nValid Operations:\n-L : Activate learning mode")
        print("-m : Only print valid statements\n-c <file.model> : Build a model from the provided datasets")
        print("-l <file.model> : Load a prebuilt model\n-h : Show this help screen\n\n")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("\nValid Operations:\n-L : Activate learning mode")
            print("-m : Only print valid statements")
            print("-c <file.model> : Build a model from the provided datasets")
            print("-l <file.model> : Load a prebuilt model\n-h : Show this help screen\n\n")
            sys.exit(0)
        elif opt == '-L':
            learn = True
        elif opt == '-m':
            minimal = True
        elif opt in ('-c', '--createfile'):
            createfile = arg
        elif opt in ('-l', '--loadfile'):
            loadfile = arg

    if minimal and learn:
        print("Minimal mode and Learn mode are not compatible with each other.")
        print("Please only select one and try again.")
        sys.exit(2)

    if (createfile and loadfile) or (not createfile and not loadfile):
        print("Please load OR create a file.")
        print("For help, try running with the -h operation.\n")
        sys.exit(2)

    if createfile:

        prog_time = time.time()
        # iterate through the 'yes' and 'no' folders and create 2 arrays to feed to the classifier
        tweetList = []
        catagories = []
        filelist = glob.glob('n/*.txt') + glob.glob('y/*.txt')
        for i in filelist:
            tmp = i.split('\\')
            catagories.append(tmp[0])
            try:
                twitter_file = io.open('{}/{}'.format(tmp[0], tmp[1]), 'r', encoding='utf8').read()
            except AttributeError:
                twitter_file = io.open('{}/{}'.format(tmp[0], tmp[1]), 'r').read()
            tweetList.append(twitter_file)
        X = tweetList
        y = catagories
        if not minimal:
            print("\nTweets processed in "+ str(time.time()-prog_time))
            print("\nDataset size: " + str(len(tweetList)) + "\n")

        prog_time = time.time()
        model = classifier.create(X, y, minimal)
        if not minimal:
            print("\nModel created in " + str(time.time()-prog_time) + "\n")

        joblib.dump(model, "{}".format(createfile))

        if not minimal:
            print(information.show_features(model))

    elif loadfile:
        try:
            model = joblib.load(loadfile)
        except:
            print("No such file found.\n")
            sys.exit(2)

    exit_bool = False
    while not exit_bool:
        twitter_input = input("\n\nEnter a twitter handle, or an individual tweet ID, or type exit to quit: ")
        if twitter_input == 'exit':
            sys.exit(1)
        else:
            twitter_list, twitter_id = twitter_crawler.crawler(twitter_input)
            #for i in twitter_list:
            if isinstance(twitter_list, str):
                input_predict = model.predict_proba([twitter_list]).tolist()
                if minimal:
                    if input_predict[1] > input_predict[0]:
                        print(twitter_list)
                else:
                    if input_predict[0][1] > input_predict[0][0]:
                        print(twitter_list + "- Verifiable - " + str(input_predict[0][1]) + "% sure")
                        if learn:
                            classifier.learn(twitter_id, twitter_list, numpy.array([1]))
                    else:
                        if input_predict[0][0] > input_predict[0][1]:
                            print(twitter_list + "- Not Verifiable - " + str(input_predict[0][0]) + "% sure")
                            if learn:
                                classifier.learn(twitter_id, twitter_list, numpy.array([0]))
            else:
                for i in range(len(twitter_list)):
                    input_predict = model.predict_proba(twitter_list).tolist()
                    if minimal:
                        if input_predict[i][1] > input_predict[i][0]:
                            print(str(twitter_list[i]))
                    else:
                        if input_predict[i][0] > input_predict[i][1]:
                            print(str(twitter_list[i]) + "- Not Verifiable - " + str(input_predict[i][0]) + "% sure")
                            if learn:
                                classifier.learn(twitter_id[i], twitter_list[i], numpy.array([0], dtype='int64'))
                        else:
                            print(str(twitter_list[i]) + "- Verifiable - " + str(input_predict[i][1]) + "% sure")
                            if learn:
                                classifier.learn(twitter_id[i], twitter_list[i], numpy.array([1], dtype='int64'))


if __name__ == "__main__":
    main(sys.argv[1:])
