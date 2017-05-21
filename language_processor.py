import string

import nltk
import sklearn


class NLTKProcessor(sklearn.base.BaseEstimator, sklearn.base.TransformerMixin):
    def __init__(self, stopwords=None, punct=None, lower=True, strip=True):
        self.lower = lower
        self.strip = strip
        self.stopwords = stopwords or set(nltk.corpus.stopwords.words('english'))
        self.punct = punct or set(string.punctuation)
        self.lemmatizer = nltk.WordNetLemmatizer()

    def fit(self, x, y=None):
        return self

    def inverse_transform(self, x):
        return [" ".join(doc) for doc in x]

    def transform(self, x):
        return [list(self.features(doc)) for doc in x]

    def features(self, tweet):
        # Break tweet into sentences
        for sent in nltk.sent_tokenize(tweet):
            # Sentence to part-of-speech tagged word
            for token, tag in nltk.pos_tag(nltk.wordpunct_tokenize(sent)):
                # preprocess the word
                token = token.lower() if self.lower else token
                token = token.strip() if self.strip else token
                token = token.strip('_') if self.strip else token
                token = token.strip('*') if self.strip else token
                # if stopword, ignore word and continue
                if token in self.stopwords:
                    continue
                # If punctuation, ignore and continue
                if all(char in self.punct for char in token):
                    continue
                # lemmatise word and return
                lemma = self.lemmatize(token, tag)
                yield lemma

    def lemmatize(self, token, tag):
        tag = {
            'N': nltk.corpus.wordnet.NOUN,
            'V': nltk.corpus.wordnet.VERB,
            'R': nltk.corpus.wordnet.ADV,
            'J': nltk.corpus.wordnet.ADJ
        }.get(tag[0], nltk.corpus.wordnet.NOUN)
        return self.lemmatizer.lemmatize(token, tag)
