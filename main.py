import getopt
import glob
import io
import sys
import time

import numpy
from sklearn.externals import joblib

import classifier
import information
import twitter_crawler


def command_line_operations(operations):
    """
    Parses command line operators, and assigns variables.
    
    Keyword Arguments:
        operations -- a list of arguments parsed via command line
    
    Return:
        A collection of variables assigned as per operations.
    """
    minimal = False
    learn = False
    loadfile = ''
    createfile = ''

    try:
        opts, args = getopt.getopt(operations, "hmLc:l:", ["createfile=", "loadfile="])
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

    return learn, minimal, loadfile, createfile


def createmodel(minimal, createfile):
    """
    Creates the model based on the filename given in command line arguments using files from the Yes(y) and No(n) train
    folders in the home directory. Then prints out a list of most positive and negative features from the model.
    
    Keyword Arguments:
        minimal -- Boolean based on whether or not -m was called. If true, no build text is printed to the user.
        createfile -- String containing the name of the model to be created.
        
    Return:
         Nothing, calls other functions, saves the created model to the 'models' directory then ends.
    """

    prog_time = time.time()
    # iterate through the 'yes' and 'no' folders and create 2 arrays to feed to the classifier
    tweet_list = []
    catagories = []
    filelist = glob.glob('n/*.txt') + glob.glob('y/*.txt')
    for i in filelist:
        tmp = i.split('\\')
        catagories.append(tmp[0])
        try:
            twitter_file = io.open('{}/{}'.format(tmp[0], tmp[1]), 'r', encoding='utf8').read()
        except AttributeError:
            twitter_file = io.open('{}/{}'.format(tmp[0], tmp[1]), 'r').read()
        tweet_list.append(twitter_file)

    if not minimal:
        print("\nTweets processed in " + str(time.time() - prog_time))
        print("\nDataset size: " + str(len(tweet_list)) + "\n")

    prog_time = time.time()
    model = classifier.create(tweet_list, catagories, minimal)
    if not minimal:
        print("\nModel created in " + str(time.time() - prog_time) + "\n")

    joblib.dump(model, "models/{}".format(createfile))

    if not minimal:
        print(information.show_features(model))


def main(argv):
    """
    Main function, manages the output from the operationg parser, and based on this performs a number of actions.
    Enters an infinite loop, where it takes user input of a twitter user handle, or a tweet ID and uses the classifier
    that was loaded or built to predict the catagory, and gives a percentage probability. Continues until user inputs 
    'exit'. If your twitter handle is 'exit'; bad luck asshole.
    
    Keyword Arguments:
        argv -- Operations taken from the command line. Given to command_line_operations to parse.
    
    Important variables:
        learn -- Boolean based on command line argument. Activates the 'learn' function, adding to the train data as the
        model runs. Not compatible with minimal mode.
        
        minimal -- Boolean based on command line argument. Activates 'minimal' mode, meaning the only output is the user
        input prompt, and a postive prediction. Not compatible with learn mode.
        
        createfile -- String taken from command line argument. Used as the filename for saving a model.
        
        loadfile -- String taken from command line argument. Used as a filename for loading an existing model.
        
        twitter_input -- String/handle taken from user input. If it's 'exit', the program ends. Otherwise, handed to
        twitter_crawler to parse tweet(s) from Twitter.
        
        twitter_list -- List/string based on output from twitter_crawler.crawler. Is a list if twitter_input was a handle,
        and is a string if twitter_input was a tweet ID. Used in printing output to console. If learn is enabled, it is
        handed to classifier.learn to be written to file.
         
        twitter_id -- List/string based on output from twitter_crawler.crawler. Contains the ID(s) of tweet(s) returned
        byt the crawler. If learn is enabled, it's handed to classifier.learn to be used as a filename.
         
        input_predict -- List/List of lists based on output from the model. For each tweet parsed by the model, a list
        containing 2 floats is returned, the first being the percentage chance of the tweet parsed not being verifiable,
        the second being the percentage chance the tweet parsed IS verifiable. 
    """

    learn, minimal, loadfile, createfile = command_line_operations(argv)

    if createfile:
        createmodel(minimal, createfile)

    elif loadfile:
        try:
            model = joblib.load("models/{}".format(loadfile.strip(" ")))
        except FileNotFoundError:
            print("No such file found.\n")
            sys.exit(2)

    exit_bool = False
    while not exit_bool:
        twitter_input = input("\n\nEnter a twitter handle, or an individual tweet ID, or type exit to quit: ")
        if twitter_input == 'exit':
            sys.exit(1)
        else:
            twitter_list, twitter_id = twitter_crawler.crawler(twitter_input)
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
