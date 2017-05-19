import sklearn
import language_processor
from sklearn.pipeline import Pipeline


def this(meme):
    return meme


def create(tweet, verifiable, minimal, classifier=sklearn.linear_model.SGDClassifier):
    def build(classifier, tweet, verifiable=None):
        if isinstance(classifier, type):
            classifier = classifier()
        model = Pipeline(
            [
                ('preprocessor',
                 language_processor.NLTK_processor()),
                ('vectorizer',
                 sklearn.feature_extraction.text.TfidfVectorizer(tokenizer=this, lowercase=False)),
                ('classifier',
                 classifier),
            ])
        model.fit(tweet, verifiable)
        return model

    # Label encode the tweets
    labels = sklearn.preprocessing.LabelEncoder()
    verifiable = labels.fit_transform(verifiable)

    # Begin evaluating
    if not minimal:
        print("Building")
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(tweet, verifiable, test_size=0.2)
    model = build(classifier, X_train, y_train)

    if not minimal:
        print("Classification Report:\n")
        y_pred = model.predict(X_test)
        print(sklearn.metrics.classification_report(y_test, y_pred, target_names=labels.classes_))

    model = build(classifier, tweet, verifiable)
    model.labels_ = labels

    return model
