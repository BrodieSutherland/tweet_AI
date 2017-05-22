import string

import nltk
import sklearn


class NLTKProcessor(sklearn.base.BaseEstimator, sklearn.base.TransformerMixin):
    """
    Used in the classifier pipeline, this class is used to preprocess all the words fromt the tweet into word types, 
    ignoring common structural words (stopwords), and punctuation. Hashtags are an exception, when the '#' symbol is 
    encountered, it triggers a hashtag boolean, making the next word encountered have a '#' at the front of it.
    
    Class also is used in fitting and transforming data in the classifier.
    """
    def __init__(self, stopwords=None, punct=None, lower=True, strip=True):
        """
        Basically giving myself options on how i could set up the processor, all variables are defined in the event 
        they aren't called.
        
        Keyword Arguments:
            lower -- Boolean, if true sets all alphabet characters to lowercase.
            
            strip -- Boolean, if true strips input words.
            
            stopwords -- List of all 'stopwords', structural words used in sentences that have little bearing on the
            meaning. By removing these, we are left with only the words that actually mean something.
            
            punct -- List of punctuation. This is used in removing punctuation from sentences.
            
            lemmatizer -- Basically a shortcut for NLTK's wordnet lemmatizer. Used in assigning word type tags to parsed
            words.
        """
        self.lower = lower
        self.strip = strip
        self.stopwords = stopwords or set(nltk.corpus.stopwords.words('english'))
        self.punct = punct or set(string.punctuation)
        self.lemmatizer = nltk.WordNetLemmatizer()

    def fit(self, x, y):
        return self

    def inverse_transform(self, x):
        return [" ".join(doc) for doc in x]

    def transform(self, x):
        return [list(self.features(doc)) for doc in x]

    def features(self, tweet):
        """
        Parses tweets by breaking them up into sentences, then into words and parsing each of these words based on the
        initialised values. After the word is preprocessed, if it run through a variety of if statements to determine if
        it's actually a word. If each of these is passed, the word it then passed to the lemmatizer, the result of which
        is then yielded to the calling function.
        
        Keyword Arguments:
            tweet -- String, the full tweet parsed to the function.
        
        Important Variables:
            hashtag -- Boolean, if true the next/current word is a hashtag, and requires a '#' symbol at the start.
            
            sent -- String, a full sentence from the tweet. This is then examined word by word.
            
            token -- String, the word currently being examined. Passed through a whole bunch of if statements, then
            lemmatized and yielded.
            
            tag -- String, the token assigned to each word in sent based on NLTK's wordpunct_tokenize function.
            
        Return:
             word -- word is yielded, rather than returned. Word is a cleaned version of the word currently being 
             examined.
        """
        # Break tweet into sentences
        for sent in nltk.sent_tokenize(tweet):
            hashtag = False
            # Sentence to part-of-speech tagged word
            for token, tag in nltk.pos_tag(nltk.wordpunct_tokenize(sent)):
                if hashtag:
                    token = "#" + token
                    hashtag = False
                # preprocess the word
                token = token.lower() if self.lower else token
                token = token.strip() if self.strip else token
                token = token.strip('_') if self.strip else token
                token = token.strip('*') if self.strip else token
                # if stopword, ignore word and continue
                if token in self.stopwords:
                    continue
                if token == '#':
                    hashtag = True
                # If punctuation, ignore and continue
                if all(char in self.punct for char in token):
                    continue
                # lemmatise word and return
                word = self.lemmatize(token, tag)
                yield word

    def lemmatize(self, token, tag):
        """
        Breaks a word up into a wide variety of types based on their usage in the sentence, and NLTK's library.
        
        Keyword Arguments:
            token -- String, token is the word passed to the lemmatizer by the feature processor.
             
            tag -- String, tag is the tag passed to this function from the feature processor. Based on the first letter
            of the tag (N, V, R, J) the broad type of the word is determined. 
            
        Return:
             
        """
        tag = {
            'N': nltk.corpus.wordnet.NOUN,
            'V': nltk.corpus.wordnet.VERB,
            'R': nltk.corpus.wordnet.ADV,
            'J': nltk.corpus.wordnet.ADJ
        }.get(tag[0], nltk.corpus.wordnet.NOUN)
        return self.lemmatizer.lemmatize(token, tag)
