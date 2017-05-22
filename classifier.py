import glob
import io

import sklearn
from sklearn.pipeline import Pipeline

import language_processor


def this(meme):
    return meme


def create(tweet, verifiable, minimal, classifier=sklearn.linear_model.SGDClassifier):
    """
    This is the function that handles the creation of the classifier itself. After building the function (done within
    the build function) the classifier is tested against the test files (found in the test folder in the home directory)
    A classification report is generated, then the model is returned.
    
    Keyword Arguments:
        tweet -- List, all the training tweets are contained within this as strings. This list is then passed to the
        build function.
        
        verifiable -- List, the catagories for all training tweets (in order) are contained within here as strings. This
        list is passed to the build function.
        
        minimal -- Boolean, passed from the main function, determines whether build and test reports are shown.
        
        classifier -- Not called in the main function, this was just here while I tested classifiers
    
    Return:
        model -- Returns the full model, complete with the pipeline. Used to do basically everything after this function
        is called.
    """

    # Label & encode the tweets
    labels = sklearn.preprocessing.LabelEncoder()
    verifiable = labels.fit_transform(verifiable)

    # Begin build function
    if not minimal:
        print("Building")
    model = build(classifier, tweet, verifiable)

    # Gather test files
    test_files = glob.glob('test/n/*.txt') + glob.glob('test/y/*.txt')
    test_data = []
    test_catagories = []
    for i in test_files:
        tmp = i.split('\\')
        if tmp[0] == 'test/n':
            test_catagories.append(0)
        else:
            test_catagories.append(1)
        try:
            test_tweet = io.open('{}/{}'.format(tmp[0], tmp[1]), 'r', encoding='utf8').read()
        except AttributeError:
            test_tweet = io.open('{}/{}'.format(tmp[0], tmp[1]), 'r').read()
        test_data.append(test_tweet)

    if not minimal:
        # Run test function, print a report on the findings
        print("Classification Report:\n")
        test_prediction = model.predict(test_data)
        print(sklearn.metrics.classification_report(test_catagories, test_prediction, target_names=labels.classes_))

    model.labels_ = labels
    return model


def build(classifier, tweet_text, catagory):
    """
    This function is the important one, it actually builds the classifier itself.
    
    Keyword Arguments:
        classifier -- Passes in the type of classifier. At time of submission this is a linear model, SGDClassifier
        
        tweet_text -- List, contains all training tweets as strings. These are all passed through the pipeline and 
        fitted to the classifier. 
        
        catagory -- List, contains the catagory of all the tweets within the train set. These are fitted to the
        classifier alongside the tweets.
    
    Return:
        pipe -- Returns the full pipeline to the create function.  
    """
    if isinstance(classifier, type):
        classifier = classifier(loss='log')
    pipe = Pipeline(
        [
            ('preprocessor',
             language_processor.NLTKProcessor()),
            ('vectorizer',
             sklearn.feature_extraction.text.TfidfVectorizer(tokenizer=this, lowercase=False)),
            ('classifier',
             classifier),
        ])
    pipe.fit(tweet_text, catagory)
    return pipe

def learn(tweet_id, tweet, pred_result):
    """
    This function is called after a prediction when learn mode is enabled. Originally, this function was intended to use
    a partial_fit function to edit the model live as the user used it, and save one the user quit, however the pipeline
    has made this difficult, and at this stage it's beyond my knowledge. A compromise implemented here, is to add the
    prediction data to the training data so any further builds can become more knowledgeable and 'smarter'.
    
    The function asks the user whether or not the classifier was correct. If so, it saves the predicted result to
    training, otherwise it saves it to the opposite training folder. 
    
    Keyword Arguments:
        tweet_id -- String, contains the ID of the tweet passed to this function. Used as the filename for the output in
        the training folder
        
        tweet -- String, contains the tweet itself. Used to write to the file itself.
        
        pred_result -- numpy array, contains either a 1 or a 0. If 1, the system has predicted that tweet is a
        verifiable statement, otherwise it's not. 
        
    Return:
         Nothing. Prints files to training folders
    """
    correction = input("Is this correct? (y/n) ")
    if correction == 'y':
        if pred_result[0]:
            file = io.open("y/{}.txt".format(tweet_id), 'w', encoding='utf8')
            file.write(tweet)
            file.close()
        else:
            file = io.open("n/{}.txt".format(tweet_id), 'w', encoding='utf8')
            file.write(tweet)
            file.close()
    else:
        if pred_result[0]:
            file = io.open("n/{}.txt".format(tweet_id), 'w', encoding='utf8')
            file.write(tweet)
            file.close()
        else:
            file = io.open("y/{}.txt".format(tweet_id), 'w', encoding='utf8')
            file.write(tweet)
            file.close()
