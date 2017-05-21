import glob
import io

import sklearn
from sklearn.pipeline import Pipeline

import language_processor


def this(meme):
    return meme


def create(tweet, verifiable, minimal, classifier=sklearn.linear_model.SGDClassifier):
    def build(classifier, tweet_text, catagory=None):
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

    # Label encode the tweets
    labels = sklearn.preprocessing.LabelEncoder()
    verifiable = labels.fit_transform(verifiable)

    # Begin evaluating
    if not minimal:
        print("Building")
    model = build(classifier, tweet, verifiable)

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
        print("Classification Report:\n")
        test_prediction = model.predict(test_data)
        print(sklearn.metrics.classification_report(test_catagories, test_prediction, target_names=labels.classes_))

    model.labels_ = labels

    return model


def learn(tweet_id, tweet, pred_result):
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
