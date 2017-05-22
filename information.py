import operator


def show_features(model, n=15):
    """
    Takes the created model and prints information about the features the make it up.
    
    Keyword Arguments:
        model -- The classifier's pipeline itself. This contains all the information about the classifier (go figure),
        and is called upon to retrieve the vectorizer and classifier, and uses this to pull the information.
        
        n -- Int, the number of features for each catagory to show. Mostly just an easier way of configuring this
        function for the developer.

    Return:
         Returns a list of features based on 2 lists, outputNeg and outputPos. As you may have guessed, these contain
         the most positive and negative features in the classifier. These are passed and printed to console in standard
         mode.
    """
    # take vectorizer and classifier from the pipeline
    vectorizer = model.named_steps['vectorizer']
    classifier = model.named_steps['classifier']

    verbose_text_features = classifier.coef_

    # zip the feature names with the coefs and sort
    coefs = sorted(
        zip(verbose_text_features[0], vectorizer.get_feature_names()),
        key=operator.itemgetter(0), reverse=True
    )

    # Get the top and bottom coefs in name pairs
    important_features = zip(coefs[:n], coefs[:-(n + 1):-1])

    # Create two lists with most negative and most positive features.
    outputPos = ["Positive Examples"]
    outputNeg = ["Negative Examples"]
    for (positive_coef, positive_feature), (negative_coef, negative_feature) in important_features:
        outputPos.append(
            "{:0.4f}{: >15}".format(
                positive_coef, positive_feature
            )
        )
        outputNeg.append(
            "{:0.4f}{: >15}".format(
                negative_coef, negative_feature
            )
        )
    outputPos.append("\n")
    return "\n".join(outputPos + outputNeg)
